import unittest
import time
from FixedAndSliding import *

class TestRateLimiters(unittest.TestCase):

    def test_fixed_window_rate_limiter(self):
        limiter = FixedWindowRateLimiter(max_requests=3, window_size_in_millis=1000)
        client_id = 'client_test'

        # Initially allow 3 requests
        self.assertTrue(limiter.allow_request(client_id))
        self.assertTrue(limiter.allow_request(client_id))
        self.assertTrue(limiter.allow_request(client_id))

        # 4th request should fail
        self.assertFalse(limiter.allow_request(client_id))

        # Wait for window reset
        time.sleep(1.1)

        # Requests should be allowed again after window reset
        self.assertTrue(limiter.allow_request(client_id))

    def test_sliding_window_rate_limiter(self):
        limiter = SlidingWindowRateLimiter(max_requests=3, window_size_in_millis=1000)
        client_id = 'client_test_sliding'

        # Initially allow 3 requests
        self.assertTrue(limiter.allow_request(client_id))
        self.assertTrue(limiter.allow_request(client_id))
        self.assertTrue(limiter.allow_request(client_id))

        # 4th request immediately should fail
        self.assertFalse(limiter.allow_request(client_id))

        # After some requests slide out of the window, allow new requests
        time.sleep(1.1)

        self.assertTrue(limiter.allow_request(client_id))
        self.assertTrue(limiter.allow_request(client_id))
        self.assertTrue(limiter.allow_request(client_id))

        # Again hitting limit
        self.assertFalse(limiter.allow_request(client_id))

    def test_rate_limiter_factory(self):
        fixed_limiter = RateLimiterFactory.create_rate_limiter('fixed', 5, 1000)
        self.assertIsInstance(fixed_limiter, FixedWindowRateLimiter)

        sliding_limiter = RateLimiterFactory.create_rate_limiter('sliding', 5, 1000)
        self.assertIsInstance(sliding_limiter, SlidingWindowRateLimiter)

        with self.assertRaises(ValueError):
            RateLimiterFactory.create_rate_limiter('unknown', 5, 1000)

    def test_singleton_rate_limiter_manager(self):
        manager1 = RateLimiterManager.get_instance()
        manager2 = RateLimiterManager.get_instance()

        self.assertIs(manager1, manager2)
        self.assertTrue(manager1.allow_request('singleton_client'))

if __name__ == '__main__':
    unittest.main()
