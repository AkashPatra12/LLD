# Rate Limiter Implementation

This repository provides two rate-limiting algorithms implemented in Python:

1. **Fixed Window Rate Limiter**
2. **Sliding Window Rate Limiter**

---

## Algorithms and Logic

### 1. Fixed Window Rate Limiter

#### Mechanism:

* Divides time into fixed-size windows.
* Counts requests within the current window.
* Resets count after each window duration.

#### Example:

* Window size: 60 seconds, Max requests: 5

```
| 0s      | 30s     | 59s  | 60s (reset) |
|---------|---------|------|-------------|
| req#1 ✅| req#3 ✅| req#5 ✅| req#1 ✅     |
| req#2 ✅| req#4 ✅| req#6 ❌| req#2 ✅     |
```

#### Visual Representation:

```
[------Window 1------] [------Window 2------]
 req req req req req    req req req req req
 ✅   ✅   ✅   ✅   ✅    ✅   ✅   ✅   ✅   ✅
 ❌ (6th request)        reset
```

#### Time Complexity:

* **O(1)** per request.

### 2. Sliding Window Rate Limiter (Log)

#### Mechanism:

* Maintains timestamps of requests within a sliding window.
* Removes timestamps older than the sliding window's timeframe.

#### Example:

* Sliding window: 60 seconds, Max requests: 3

```
Timestamps: [10s, 20s, 50s]  # Requests within window
New request at 65s:
[20s, 50s, 65s] ✅ Allowed

New request at 66s:
[50s, 65s, 66s] ✅ Allowed

New request at 67s:
[50s, 65s, 66s, 67s] ❌ Blocked (limit exceeded)
```

#### Visual Representation:

```
Sliding window moves forward:

0s----10s----20s----30s----40s----50s----60s----70s
      |-----------Sliding Window-----------|
      ✅    ✅                     ✅
                               New ✅  New ✅
                                     New ❌
```

#### Time Complexity:

* **O(1)** average per request (with deque).

---

## Advantages and Disadvantages

### Fixed Window

* **Advantages:**

  * Simple implementation.
  * Constant-time operations.

* **Disadvantages:**

  * Burst of requests at window boundaries.
  * Potential for short-term unfairness.

### Sliding Window (Log)

* **Advantages:**

  * Smooth rate control, fairer distribution.
  * Precise control over request flow.

* **Disadvantages:**

  * Higher memory usage (storing timestamps).
  * Slightly more computational overhead.

---

## Scaling and Handling High Traffic in Distributed Systems

### Strategies:

1. **Centralized Store (e.g., Redis):**

   * Use Redis or another in-memory store to maintain counters or timestamps.
   * Benefits: easy synchronization across instances, fast atomic operations.
   * Considerations: single point of failure, requires replication for high availability.

2. **Distributed Rate Limiter Instances:**

   * Run multiple rate-limiting instances with eventual consistency.
   * Benefits: better availability, reduced latency.
   * Trade-offs: slightly less precise rate limiting due to eventual consistency.

3. **Hybrid Approach:**

   * Local rate limiting (approximate control).
   * Global rate limiting through periodic synchronization.
   * Balances precision and scalability.

### Recommendations for High Traffic:

* **Sliding Window Counter:** Aggregate counts per short interval to minimize memory overhead.
* **Caching and Sharding:** Distribute the rate limiter across multiple nodes to prevent bottlenecks.
* **Monitoring and Alerting:** Implement real-time monitoring and adaptive throttling for sudden spikes.

---

## Usage Example

```python
if __name__ == "__main__":
    fixed_window_rate_limiter = RateLimiterFactory.create_rate_limiter("fixed", 10, 60)
    sliding_window_rate_limiter = RateLimiterFactory.create_rate_limiter("sliding", 10, 60)

    print("Fixed Window Rate Limiter:")
    for _ in range(12):
        print(fixed_window_rate_limiter.allow_request("client1"))

    print("\nSliding Window Rate Limiter:")
    for _ in range(12):
        print(sliding_window_rate_limiter.allow_request("client2"))
```

---

## Conclusion

Choose your rate-limiting algorithm based on your specific requirements:

* Use **Fixed Window** for simplicity and predictable performance.
* Use **Sliding Window** when accuracy and fairness are critical.

When scaling, prefer centralized state management for consistency, or distributed approaches for availability and performance.
