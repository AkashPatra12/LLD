
# 🚦 Python Rate Limiter

This project demonstrates **five rate limiting algorithms** in Python to control client request rates, useful for API protection, login throttling, and infrastructure traffic shaping.

Supported algorithms:
- ✅ Fixed Window Counter
- ✅ Sliding Window Log
- ✅ Sliding Window Counter
- ✅ Leaky Bucket
- ✅ Token Bucket

It uses a unified interface and supports multithreaded request simulation.

---

## 🧠 Algorithm Details with Visuals

### 1. ⏲️ Fixed Window Counter
**Logic**: Count requests in a fixed-sized time bucket (e.g., 5 seconds).

```
Time:   0s    5s   10s   15s   20s
        |-----|-----|-----|-----|
Client:  ● ● ● ● ●         ● ● ● ● ●
         (limit hit)       (limit hit)
```

- ✅ **Pros**: Fast, easy to implement  
- ❌ **Cons**: Allows burst at boundary of time windows

---

### 2. 📜 Sliding Window Log
**Logic**: Maintain a deque of timestamps and remove outdated entries continuously.

```
Sliding window moves forward:

0s----10s----20s----30s----40s----50s----60s----70s
      |-----------Sliding Window-----------|
      ✅    ✅                     ✅
                               New ✅  New ✅
                                     New ❌ (limit exceeded)
```

- ✅ **Pros**: Highly accurate  
- ❌ **Cons**: Memory-intensive for high-frequency clients

---

### 3. 📊 Sliding Window Counter
**Logic**: Divide total window into equal-length buckets and sum request counts.

```
Buckets:
| 12:00 | 12:01 | 12:02 | 12:03 | 12:04 |
|   2   |   1   |   0   |   3   |   2   |
           <--- Sliding Window --->
Total = 6 requests in the last 3 buckets
```

- ✅ **Pros**: Space-efficient, good accuracy  
- ❌ **Cons**: Slightly approximate due to time binning

---

### 4. 💧 Leaky Bucket
**Logic**: Requests enter a queue that leaks at a steady rate.

```
Rate: 1 req/sec | Capacity: 5

Time ➜   [0s][1s][2s][3s][4s][5s][6s][7s]
Input ➜   ✅  ✅  ✅  ✅  ✅  ❌  ✅  ✅
Bucket ➜ [▓▓▓▓▓] Leaks ▽ ▽ ▽ ▽ ▽ ➜ [▓▓]
```

- ✅ **Pros**: Smooths spikes into steady flow  
- ❌ **Cons**: Not suitable for bursty traffic

---

### 5. 🪙 Token Bucket
**Logic**: Bucket refills tokens at a steady rate; requests consume tokens.

```
Rate: 1 token/sec | Capacity: 5

Time ➜  0s   1s   2s   3s   4s   5s
Tokens: 🪙🪙🪙🪙🪙
Reqs:   ✅ ✅ ✅ ✅ ✅ ❌ (no tokens left)
       [tokens consumed]
```

- ✅ **Pros**: Allows bursts + recovers over time  
- ❌ **Cons**: Requires precise token refill logic

---

## 📊 Time & Space Complexity

| Algorithm              | Time Complexity | Space per Client |
|------------------------|------------------|------------------|
| Fixed Window           | O(1)             | O(1)             |
| Sliding Window Log     | O(1) – O(n)      | O(n)             |
| Sliding Window Counter | O(1) – O(k)      | O(k)             |
| Leaky Bucket           | O(1)             | O(1)             |
| Token Bucket           | O(1)             | O(1)             |

> `n` = number of requests per window  
> `k` = number of sub-windows

---

## 🧰 Use-Case Recommendations

| Use Case                       | Recommended Limiter       | Why                                       |
|--------------------------------|----------------------------|-------------------------------------------|
| API throttling with bursts     | Token Bucket               | Burst-tolerant, smooth refill             |
| Login rate limit               | Sliding Window Log         | Timestamp precision prevents abuse        |
| Real-time message flow         | Leaky Bucket               | Drips traffic evenly                      |
| Basic request limiting         | Fixed Window               | Simple and effective                      |
| Performance + precision blend  | Sliding Window Counter     | Balanced overhead and accuracy            |

---

## 🌐 Distributed System Scaling

### 🧱 1. Centralized Data Store (Redis)
- Store rate limit state per client
- Use Redis commands: `INCR`, `EXPIRE`, `ZADD`, etc.
- ✅ Pros: Fast, atomic  
- ❌ Cons: Centralized point of failure

### 📦 2. Local + Periodic Sync
- Maintain local limits per node
- Sync with central store periodically

### ⚖️ 3. Sharded Clients
- Hash client IDs across limiter servers or Redis partitions

### 🌍 4. CDN / Edge-Based Limiting
- Rate limit at edge nodes (e.g. Cloudflare)

---

## 🚀 How to Run

```bash
python rate_limiter.py
```

### Output:
```
Fixed Rate Limiter with Threads:
Client: client_fixed_0, Allowed: True
Client: client_fixed_0, Allowed: False
...

Token Bucket Rate Limiter with Threads:
Client: client_token_1, Allowed: True
...
```

---

## 📁 Project Structure

- `RateLimiter`: Abstract interface
- `FixedWindowRateLimiter`
- `SlidingWindowRateLimiter`
- `SlidingWindowCounterRateLimiter`
- `LeakyBucketRateLimiter`
- `TokenBucketRateLimiter`
- `RateLimiterFactory`: Centralized creator
- `simulate_requests()`: Multithreaded test runner
- `main`: Demonstrates each limiter with multiple clients

---

## 🔮 Future Enhancements

- [ ] Redis integration (centralized store)
- [ ] Flask / FastAPI REST wrapper
- [ ] Prometheus / Grafana observability
- [ ] Configurable YAML-based policies
- [ ] Async / AIO support

---

## 📜 License

MIT — Use freely in production, testing, or education.
