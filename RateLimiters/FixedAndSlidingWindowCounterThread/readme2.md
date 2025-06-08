
markdown
Copy
Edit
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

---

### 1. ⏲️ Fixed Window Counter

**Logic**: Count requests in a fixed-sized time bucket (e.g., 5 seconds).

Time: [0---|---|---|---|---|---|---|---|---|---]
Window:|----- 1st window -----|---- 2nd window---|
Reqs: ● ● ● ● ● (limit hit) ● ● ...

yaml
Copy
Edit

- ✅ **Pros**: Fast, easy to implement  
- ❌ **Cons**: Burst allowed at edges (e.g., 10 at 4.99s + 10 at 5.01s)

---

### 2. 📜 Sliding Window Log

**Logic**: Keep timestamps of each request and purge outdated ones.

Now: T=12s, Window=5s ➜ Only timestamps ≥ 7s count
Deque: [7s, 8s, 9s, 11s]

yaml
Copy
Edit

- ✅ **Pros**: High accuracy  
- ❌ **Cons**: Memory grows with request rate

---

### 3. 📊 Sliding Window Counter

**Logic**: Break time into small intervals (buckets) and sum recent buckets.

Buckets:
| 0s | 1s | 2s | 3s | 4s | 5s |
| 2 | 1 | 0 | 2 | 1 | - |
Total = 6 (last 5s)

yaml
Copy
Edit

- ✅ **Pros**: Space-efficient, good accuracy  
- ❌ **Cons**: Slightly approximate, needs cleanup

---

### 4. 💧 Leaky Bucket

**Logic**: Requests enter a queue that leaks at a constant rate.

Water level: ▓▓▓▓░ (leaking 1 req/sec)
New req: ✅ if bucket not full, ❌ if overflow

yaml
Copy
Edit

- ✅ **Pros**: Smooth, controlled flow  
- ❌ **Cons**: Not burst-friendly

---

### 5. 🪙 Token Bucket

**Logic**: Tokens refill at a constant rate. Each request consumes one.

Tokens: [🪙🪙🪙🪙🪙] ← refilled 1/sec up to capacity
Request: ✅ if ≥ 1 token, else ❌

yaml
Copy
Edit

- ✅ **Pros**: Allows bursts + sustained rate  
- ❌ **Cons**: Slightly more complex refill logic

---

## 📊 Time & Space Complexity

| Algorithm              | Time Complexity | Space per Client |
|------------------------|------------------|------------------|
| Fixed Window           | O(1)             | O(1)             |
| Sliding Window Log     | O(1)–O(n)        | O(n)             |
| Sliding Window Counter | O(1)–O(k)        | O(k)             |
| Leaky Bucket           | O(1)             | O(1)             |
| Token Bucket           | O(1)             | O(1)             |

`n` = number of requests per window  
`k` = number of sub-windows

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

**To support multiple servers or high traffic:**

### 🧱 1. Centralized Data Store (Redis)
- Store counters, timestamps, or token levels per `client_id`
- Use Redis commands like `INCR`, `EXPIRE`, `ZADD`, `ZREMRANGEBYSCORE`
- ✅ Pros: Fast, atomic  
- ❌ Cons: Centralized; can become a bottleneck

### 📦 2. Local + Periodic Sync
- Maintain local rate limits
- Push stats to a shared store periodically
- ✅ Pros: Reduces latency  
- ❌ Cons: Potential for temporary breaches

### ⚖️ 3. Sharded Clients
- Hash client IDs to different limiter instances or Redis shards
- Useful at scale (e.g., thousands of clients)

### 🌍 4. CDN / Edge-Based Limiting
- Offload rate limits to reverse proxies or CDN edges like Cloudflare, Akamai

---

## 🚀 How to Run

```bash
python rate_limiter.py
Output:
Shows multithreaded request logs like:

yaml
Copy
Edit
Fixed Rate Limiter with Threads:
Client: client_fixed_0, Allowed: True
Client: client_fixed_0, Allowed: False
...