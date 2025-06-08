# Rate Limiter Implementation

This repository provides three rate-limiting algorithms implemented in Python:

1. **Fixed Window Rate Limiter**
2. **Sliding Window Rate Limiter (Log)**
3. **Sliding Window Counter Rate Limiter**

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

### 3. Sliding Window Counter Rate Limiter

#### Mechanism:

* Divides time into smaller fixed intervals.
* Counts requests in each interval.
* Aggregates counts within the sliding window.

#### Example:

* Window size: 60 seconds, Interval: 10 seconds, Max requests: 6

```
Intervals: [0-10s, 10-20s, 20-30s, 30-40s, 40-50s, 50-60s]
Counts: [1, 1, 1, 1, 1, 1] Total: 6 ✅
New interval (60-70s): [1, 1, 1, 1, 1, 2] Total: 7 ❌
```

#### Visual Representation:

```
Intervals:
|0-10|10-20|20-30|30-40|40-50|50-60|60-70|
|  1 |  1  |  1  |  1  |  1  |  1  |  1  |
Total requests ≤ Max allowed ✅
Exceeding total requests ❌
```

#### Time Complexity:

* **O(1)** per request.

---

## Advantages and Disadvantages

### Fixed Window

* **Advantages:**

  * Simple implementation.
  * Constant-time operations.
* **Disadvantages:**

  * Potential burstiness at window boundaries.

### Sliding Window (Log)

* **Advantages:**

  * Smooth and fair request handling.
  * Precise control.
* **Disadvantages:**

  * Higher memory overhead.

### Sliding Window Counter

* **Advantages:**

  * Lower memory overhead than sliding log.
  * High throughput capability.
* **Disadvantages:**

  * Approximate accuracy.

---

## Scaling and Handling High Traffic in Distributed Systems

### Strategies:

1. **Centralized Store (Redis):**

   * Synchronize across instances.
   * Atomic and quick operations.

2. **Distributed Instances:**

   * Eventual consistency.
   * Scalable and resilient.

3. **Hybrid Approach:**

   * Balance between precision and scalability.

### Recommendations:

* Use **Sliding Window Counter** for scalability.
* Implement **caching and sharding**.
* Add real-time monitoring.

---

## Usage Example

See Python code in the repository for a full implementation demonstration using threads to simulate concurrent clients.

---

## Conclusion

* **Fixed Window**: Simple, predictable.
* **Sliding Window (Log)**: Precise, fair.
* **Sliding Window Counter**: Scalable, efficient.

Choose your rate limiter based on your application's specific scalability, accuracy, and performance requirements.
