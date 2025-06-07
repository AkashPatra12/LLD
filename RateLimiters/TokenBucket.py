import time
from threading import Lock

class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_time = time.time()
        self.lock = Lock()

    def allow_request(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_time
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_time = now
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

bucket = TokenBucket(rate=1, capacity=5)

print(bucket.allow_request())