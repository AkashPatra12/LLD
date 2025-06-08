from abc import ABC, abstractmethod
import time
from collections import deque
from threading import Lock, Thread

# Abstract Interface
class RateLimiter(ABC):
    @abstractmethod
    def allow_request(self, client_id: str) -> bool:
        pass

# 1. Fixed Window Rate Limiter
class FixedWindowRateLimiter(RateLimiter):
    def __init__(self, max_requests: int, window_size: int):
        self.max_requests = max_requests
        self.window_size = window_size
        self.request_counts = {}
        self.window_start_times = {}
        self.lock = Lock()

    def allow_request(self, client_id: str) -> bool:
        current_time = int(time.time())
        with self.lock:
            self.window_start_times.setdefault(client_id, current_time) # sets to default value if key doesn't exist
            self.request_counts.setdefault(client_id, 0)

            window_start_time = self.window_start_times[client_id]
            if current_time - window_start_time >= self.window_size: # elapsed time > window_size
                self.window_start_times[client_id] = current_time
                self.request_counts[client_id] = 0

            if self.request_counts[client_id] < self.max_requests:
                self.request_counts[client_id] += 1
                return True
            return False

# 2. Sliding Window Log Rate Limiter
class SlidingWindowRateLimiter(RateLimiter):
    def __init__(self, max_requests: int, window_size: int):
        self.max_requests = max_requests
        self.window_size = window_size
        self.request_timestamps = {}
        self.lock = Lock()

    def allow_request(self, client_id: str) -> bool:
        current_time = int(time.time())
        with self.lock:
            self.request_timestamps.setdefault(client_id, deque())

            timestamps = self.request_timestamps[client_id]
            while timestamps and current_time - timestamps[0] >= self.window_size:
                timestamps.popleft()

            if len(timestamps) < self.max_requests:
                timestamps.append(current_time)
                return True
            return False

# 3. Sliding Window Counter Rate Limiter
class SlidingWindowCounterRateLimiter(RateLimiter):
    def __init__(self, max_requests: int, window_size: int):
        self.max_requests = max_requests
        self.window_size = window_size
        self.counters = {}
        self.lock = Lock()

    def allow_request(self, client_id: str) -> bool:
        current_time = int(time.time())
        current_window = current_time // self.window_size

        with self.lock:
            if client_id not in self.counters:
                self.counters[client_id] = {}
            counters = self.counters[client_id]

            # Clear outdated windows
            for window in list(counters.keys()):
                if window < current_window:
                    del counters[window]

            counters.setdefault(current_window, 0)
            total_requests = sum(counters.values())

            if total_requests < self.max_requests:
                counters[current_window] += 1
                return True
            return False

# 4. Leaky Bucket Rate Limiter
class LeakyBucketRateLimiter(RateLimiter):
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.water = 0
        self.last_time = time.time()
        self.lock = Lock()

    def allow_request(self, client_id: str) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.last_time
            self.last_time = now
            leaked = elapsed * self.leak_rate
            self.water = max(0, self.water - leaked)
            if self.water < self.capacity:
                self.water += 1
                return True
            return False

# 5. Token Bucket Rate Limiter
class TokenBucketRateLimiter(RateLimiter):
    def __init__(self, rate, capacity):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_time = time.time()
        self.lock = Lock()

    def allow_request(self, client_id: str) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.last_time
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_time = now
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

# Factory Pattern
class RateLimiterFactory:
    @staticmethod
    def create_rate_limiter(type: str, max_requests: int, window_size: int) -> RateLimiter:
        if type == "fixed":
            return FixedWindowRateLimiter(max_requests, window_size)
        elif type == "sliding":
            return SlidingWindowRateLimiter(max_requests, window_size)
        elif type == "sliding_counter":
            return SlidingWindowCounterRateLimiter(max_requests, window_size)
        elif type == "leaky":
            return LeakyBucketRateLimiter(max_requests, window_size)
        elif type == "token":
            return TokenBucketRateLimiter(max_requests, window_size)
        else:
            raise ValueError("Unknown rate limiter type")

# Threading Simulation
def simulate_requests(rate_limiter, client_id, request_count):
    for _ in range(request_count):
        allowed = rate_limiter.allow_request(client_id)
        print(f"Client: {client_id}, Allowed: {allowed}")
        time.sleep(0.1)

# Main Entry
if __name__ == "__main__":
    limiters = {
        "fixed": RateLimiterFactory.create_rate_limiter("fixed", 5, 5),
        "sliding": RateLimiterFactory.create_rate_limiter("sliding", 5, 5),
        "sliding_counter": RateLimiterFactory.create_rate_limiter("sliding_counter", 5, 5),
        "leaky": RateLimiterFactory.create_rate_limiter("leaky", 5, 1),
        "token": RateLimiterFactory.create_rate_limiter("token", 1, 5)
    }

    for name, limiter in limiters.items():
        print(f"\n{name.capitalize()} Rate Limiter with Threads:")
        threads = []
        for i in range(3):
            t = Thread(target=simulate_requests, args=(limiter, f'client_{name}_{i}', 10))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
