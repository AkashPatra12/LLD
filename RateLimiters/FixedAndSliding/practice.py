from abc import ABC, abstractmethod
import time
from collections import deque
from os import times
from wsgiref.util import request_uri


class RateLimiter(ABC):
    @abstractmethod
    def allow_request(self, client_id):
        pass

class FixedWindow(RateLimiter):
    def __init__(self, max_requests, window_size):
        self.max_requests = max_requests
        self.window_size = window_size
        self.window_starts = {}
        self.req_counts = {}

    def allow_request(self, client_id):
        curr_time = time.time()
        print(curr_time)
        self.window_starts.setdefault(client_id, curr_time) # only sets if no values are present
        self.req_counts.setdefault(client_id, 0)

        window_start = self.window_starts[client_id]
        print(window_start - curr_time )
        if window_start - curr_time >= self.window_size:
            self.window_starts[client_id] = curr_time
            self.req_counts[client_id] = 0
        print(self.window_starts)

        if self.req_counts[client_id] < self.max_requests:
            self.req_counts[client_id] += 1
            print(self.req_counts)
            return True
        return False

class SlidingWindowRateLimiter(RateLimiter):
    def __init__(self, max_requests, window_size):
        self.max_requests = max_requests
        self.window_size = window_size
        self.timestamps = {}

    def allow_request(self, client_id):
        curr_time = time.time()
        self.timestamps.setdefault(client_id, deque())

        timestamps = self.timestamps[client_id]
        while timestamps and curr_time - timestamps[0] > self.window_size:
            timestamps.popleft()

        if len(timestamps) < self.max_requests:
            timestamps.append(curr_time)
            return True
        return False


import unittest

class TestLimits(unittest.TestCase):

    def test1(self):
        rate_limiter = FixedWindow(5, 60)
        self.assertTrue(rate_limiter.allow_request(123))
        self.assertTrue(rate_limiter.allow_request(123))
        self.assertTrue(rate_limiter.allow_request(123))
        self.assertTrue(rate_limiter.allow_request(123))
        self.assertTrue(rate_limiter.allow_request(123))
        self.assertFalse(rate_limiter.allow_request(123))