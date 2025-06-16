import time
from threading import Lock

import time
from threading import Lock

class LeakyBucketWithCredits:
    def __init__(self, capacity, leak_rate):
        """
        :param capacity: Maximum number of request credits
        :param leak_rate: Number of credits restored per second
        """
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.credits = capacity  # Start with full credits
        self.last_time = time.time()
        self.lock = Lock()

    def allow_request(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_time
            # Refill credits based on elapsed time
            restored = elapsed * self.leak_rate
            self.credits = min(self.capacity, self.credits + restored)
            self.last_time = now
            # If we have at least 1 credit, allow the request
            if self.credits >= 1:
                self.credits -= 1
                return True
            return False

class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity          # Max water level (max requests bucket can hold)
        self.leak_rate = leak_rate        # Requests removed (leaked) per second
        self.water = 0                    # Current water level (pending requests)
        self.last_time = time.time()      # Last time leakage was calculated
        self.lock = Lock()                # Thread-safety for concurrent access

    def allow_request(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_time  # Time passed since last check
            self.last_time = now
            leaked = elapsed * self.leak_rate
            # Reduce water level (simulate leakage)
            self.water = max(0, self.water - leaked)
            # If bucket is not full, allow request
            if self.water < self.capacity:
                self.water += 1  # Add current request as a drop
                return True
            return False

bucket = LeakyBucket(5, 1)

print(bucket.allow_request())



'''
⏱️ Time Complexity
allow_request(): O(1)
Only basic arithmetic operations and a single lock.
No iteration, data structure traversal, or complex logic.

🧮 Space Complexity: O(1)
Tracks only:
capacity (int)
leak_rate (float)
water (float)
last_time (float)

Constant memory regardless of the number of requests or time.
✅ Advantages
Smooths out traffic: requests are processed at a fixed, controlled rate.
Prevents sudden bursts that could overwhelm a system.
Lightweight and predictable.

❌ Disadvantages
Cannot handle bursty traffic well — rejects sudden spikes if bucket is full.
Less flexible compared to token bucket (which allows bursts up to capacity).
'''