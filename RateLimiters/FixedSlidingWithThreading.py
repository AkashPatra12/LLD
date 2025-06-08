from abc import ABC, abstractmethod
import time
from collections import deque
from threading import Lock, Thread

class RateLimiter(ABC):
    @abstractmethod
    def allow_request(self, client_id: str) -> bool:
        pass

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

class RateLimiterFactory:
    @staticmethod
    def create_rate_limiter(type: str, max_requests: int, window_size: int) -> RateLimiter:
        if type == "fixed":
            return FixedWindowRateLimiter(max_requests, window_size)
        elif type == "sliding":
            return SlidingWindowRateLimiter(max_requests, window_size)
        elif type == "sliding_counter":
            return SlidingWindowCounterRateLimiter(max_requests, window_size)
        else:
            raise ValueError("Unknown rate limiter type")


# Thread handling demonstration
def simulate_requests(rate_limiter, client_id, request_count):
    for _ in range(request_count):
        allowed = rate_limiter.allow_request(client_id)
        print(f"Client: {client_id}, Allowed: {allowed}")
        time.sleep(0.1)

if __name__ == "__main__":
    fixed_limiter = RateLimiterFactory.create_rate_limiter("fixed", 5, 5)
    sliding_limiter = RateLimiterFactory.create_rate_limiter("sliding", 5, 5)
    sliding_counter_limiter = RateLimiterFactory.create_rate_limiter("sliding_counter", 5, 5)

    print("Fixed Window Rate Limiter with Threads:")
    threads = []
    for i in range(3):
        t = Thread(target=simulate_requests, args=(fixed_limiter, f'client_fixed_{i}', 10))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nSliding Window Rate Limiter with Threads:")
    threads = []
    for i in range(3):
        t = Thread(target=simulate_requests, args=(sliding_limiter, f'client_sliding_{i}', 10))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nSliding Window Counter Rate Limiter with Threads:")
    threads = []
    for i in range(3):
        t = Thread(target=simulate_requests, args=(sliding_counter_limiter, f'client_sliding_counter_{i}', 10))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
