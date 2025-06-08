# File Processing & Collection Size Reporter

## ✨ Overview

This system ingests a list of files with their sizes and associated collections (optional) and provides:

1. ✅ Total size of all files processed
2. ⬆️ Top-K collections by cumulative file size

---

## 🔹 Input Format

Each file is a tuple of:

```python
(file_name: str, file_size: int, collections: List[str])
```

Example:

```python
files = [
    ("file1.txt", 100, []),
    ("file2.txt", 200, ["collection1"]),
    ("file3.txt", 200, ["collection1"]),
    ("file4.txt", 300, ["collection2"]),
    ("file5.txt", 100, [])
]
```

---

## ⚖️ Output

```
Total size of files processed: 900
Top 2 collections:
- collection1 : 400
- collection2 : 300
```

---

## 🧰 Design Principles & Patterns

* **SOLID Principles:**

  * S: Separation of processing vs reporting
  * O: Reporters can be extended for new metrics
  * L: Interfaces can be replaced freely
  * I: Only necessary methods per interface
  * D: FileProcessor depends on abstract `IReporter`

* **Design Pattern:** Strategy Pattern (to swap reporting logic)

---

## 🔠 Interfaces

```python
class IFileProcessor(ABC):
    def process(files): pass

class IReporter(ABC):
    def add_file(file_name, size, collections): pass
    def report_total_size(): pass
    def report_top_k_collections(k): pass
```

---

## ⏱️ Time Complexity

Let:

* `n` = number of files
* `c` = average number of collections per file
* `m` = total unique collections
* `k` = number of top collections to retrieve

| Operation                   | Complexity             |
| --------------------------- | ---------------------- |
| File processing             | `O(n * c)`             |
| Top-K collections reporting | `O(m * log k)`         |
| **Total**                   | `O(n * c + m * log k)` |

---

## 📊 Space Complexity

| Component          | Space Used |
| ------------------ | ---------- |
| Total size counter | `O(1)`     |
| Collection mapping | `O(m)`     |
| **Total**          | `O(m)`     |

---

## ⚡ Extensibility Ideas

* Add deduplication if files can repeat
* Support disk-based streaming for large inputs
* Persist collection sizes in Redis/DB for distributed use
* Add metadata reporters for file types, timestamps, etc.

---

## ✨ Example Usage

```python
reporter = FileStatsReporter()
processor = FileProcessor(reporter)
processor.process(files)

print("Total size:", reporter.report_total_size())
print("Top 2 collections:")
for name, size in reporter.report_top_k_collections(2):
    print(f"- {name} : {size}")
```

---

Let me know if you'd like REST API or persistence layer extensions!
