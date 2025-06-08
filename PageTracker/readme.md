# 📈 Most Liked/View Page Tracker

A scalable and extensible system to track and retrieve the most liked or most viewed pages over a time period.

---

### ✅ Requirements (LLD Interview Style)

* Support tracking `likes` and `views` for any page.
* Retrieve top-N most liked/viewed pages for a custom date range.
* Ensure thread-safe updates and quick read access.
* Handle data volume increase (time-series-based writes).
* Follow **SOLID** principles and extensible design.

---

### 🔄 High-Level Flow

1. **Client** records a `like` or `view` via the `PageTracker`.
2. `PageTracker` delegates the increment to `PageStatRepository`.
3. Stats are written per-day (granular time-series).
4. `TrendingPageService` aggregates data over time to return top pages.

---

### 🧠 Detailed Component Flow

* **Page**: Entity with `page_id` and `title`.
* **IPageTracker**: Strategy interface to abstract event recording logic.
* **IPageStatRepository**: Repository abstraction for stat persistence (supports Cassandra, in-memory, etc.).
* **ITrendingPageService**: Service to retrieve top pages by views or likes.
* **InMemoryPageStatRepository**: Simple thread-safe storage with daily buckets (date + stat type + page).
* **SimplePageTracker**: Uses today's date and records likes/views.
* **TrendingPageService**: Aggregates data and ranks by count.

---

### 🧹 Design Patterns Used

| Pattern                   | Purpose                                                         |
| ------------------------- | --------------------------------------------------------------- |
| **Strategy**              | `IPageTracker` enables plug-n-play implementations              |
| **Repository**            | Decouples persistence logic (in-memory/Cassandra/other)         |
| **Dependency Injection**  | Used in `Tracker` and `Service` for testability & extensibility |
| **Single Responsibility** | Each class does one job (SRP of SOLID)                          |
| **Open/Closed Principle** | Easily extensible via new stat types, new stores                |

---

### 📊 UML Diagram

```plaintext
+-------------------+          +------------------------+
|   Page            |          |  IPageStatRepository   |
|-------------------|          |------------------------|
| - page_id: str    |<>------->|+increment_stat(...)     |
| - title: str      |          |+get_top_pages(...)      |
+-------------------+          +------------------------+
        ^                                ^
        |                                |
+-------------------+          +--------------------------+
| SimplePageTracker |          | InMemoryPageStatRepository|
|-------------------|          |--------------------------|
|+record_view()     |          |+increment_stat(...)       |
|+record_like()     |          |+get_top_pages(...)        |
+-------------------+          +--------------------------+
        |
        v
+------------------------+
| ITrendingPageService   |
|------------------------|
|+get_most_viewed_pages()|
|+get_most_liked_pages() |
+------------------------+
        ^
        |
+-------------------------+
| TrendingPageService     |
+-------------------------+
```

---

### 🚀 Scalability & Deployment in Distributed Systems

#### 1. **Stat Write Design (Cassandra)**

* Table schema:

  ```sql
  CREATE TABLE page_stats (
      stat_type TEXT,
      stat_date DATE,
      page_id TEXT,
      count COUNTER,
      PRIMARY KEY ((stat_type, stat_date), page_id)
  );
  ```
* Write-heavy design with daily partitioning → avoids hot partitions.

#### 2. **Read Optimization**

* Use Spark or Presto over Cassandra for aggregation queries.
* Precompute daily/weekly/monthly rankings and cache in Redis.

#### 3. **Deployment**

* Deploy service with horizontal scaling:

  * Tracker API → Load Balanced
  * Stats DB (e.g., Cassandra with replication)
  * Cache Layer (Redis) for fast ranking reads

#### 4. **Traffic Handling**

* Async write queue (Kafka) to buffer likes/views.
* Background consumer writes to Cassandra (eventual consistency).
* Use a CDN or frontend cache for top page displays.

---

Let us know if you want to extend this with user-based analytics, batch precomputation, or API interfaces.
