from abc import ABC, abstractmethod
import time
from collections import deque
from threading import Lock

class RateLimiter(ABC):
    @abstractmethod
    def allow_request(self, client_id: str) -> bool:
        pass

class FixedWindowRateLimiter(RateLimiter):
    def __init__(self, max_requests: int, window_size: int):
        self.max_requests = max_requests
        self.window_size_in_millis = window_size
        self.request_counts = {}
        self.window_start_times = {}

    def allow_request(self, client_id: str) -> bool:
        current_time = int(time.time())
        self.window_start_times.setdefault(client_id, current_time)
        self.request_counts.setdefault(client_id, 0)

        window_start_time = self.window_start_times[client_id]
        if current_time - window_start_time >= self.window_size_in_millis:
            self.window_start_times[client_id] = current_time
            self.request_counts[client_id] = 0

        if self.request_counts[client_id] < self.max_requests:
            self.request_counts[client_id] += 1
            return True
        return False

class SlidingWindowRateLimiter(RateLimiter):
    def __init__(self, max_requests: int, window_size_in_millis: int):
        self.max_requests = max_requests
        self.window_size_in_millis = window_size_in_millis
        self.request_timestamps = {}

    def allow_request(self, client_id: str) -> bool:
        current_time = int(time.time())
        self.request_timestamps.setdefault(client_id, deque())

        timestamps = self.request_timestamps[client_id]
        while timestamps and current_time - timestamps[0] > self.window_size_in_millis:
            timestamps.popleft()

        if len(timestamps) < self.max_requests:
            timestamps.append(current_time)
            return True
        return False

class RateLimiterFactory:
    @staticmethod
    def create_rate_limiter(type: str, max_requests: int, window_size: int) -> RateLimiter:
        if type == "fixed":
            return FixedWindowRateLimiter(max_requests, window_size)
        elif type == "sliding":
            return SlidingWindowRateLimiter(max_requests, window_size)
        else:
            raise ValueError("Unknown rate limiter type")
#
# class RateLimiterManager:
#     _instance = None
#     _lock = Lock()
#
#     def __init__(self):
#         self.rate_limiter = RateLimiterFactory.create_rate_limiter("fixed", 100, 60000)
#
#     @classmethod
#     def get_instance(cls):
#         if not cls._instance:
#             with cls._lock:
#                 if not cls._instance:
#                     cls._instance = cls()
#         return cls._instance
#
#     def allow_request(self, client_id: str) -> bool:
#         return self.rate_limiter.allow_request(client_id)

if __name__ == "__main__":
    fixed_window_rate_limiter = RateLimiterFactory.create_rate_limiter("fixed", 10, 60)
    sliding_window_rate_limiter = RateLimiterFactory.create_rate_limiter("sliding", 10, 60)

    print("Fixed Window Rate Limiter:")
    for _ in range(12):
        print(fixed_window_rate_limiter.allow_request("client1"))

    print("\nSliding Window Rate Limiter:")
    for _ in range(12):
        print(sliding_window_rate_limiter.allow_request("client2"))