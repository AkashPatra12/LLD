import time
from threading import Lock

class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.water = 0
        self.last_time = time.time()
        self.lock = Lock()

    def allow_request(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_time
            self.last_time = now
            leaked = elapsed * self.leak_rate
            self.water = max(0, self.capacity - leaked)
            if self.water <= self.capacity:
                self.water += 1
                return True
            return False

bucket = LeakyBucket(5, 1)

print(bucket.allow_request())
