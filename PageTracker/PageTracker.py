from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import date, timedelta
from collections import defaultdict, Counter
import threading

# --- Entities ---

class Page:
    def __init__(self, page_id: str, title: str):
        self.page_id = page_id
        self.title = title

    def __repr__(self):
        return f"Page(id={self.page_id}, title='{self.title}')"


# --- Interfaces ---

class IPageTracker(ABC):
    @abstractmethod
    def record_view(self, page_id: str) -> None:
        pass

    @abstractmethod
    def record_like(self, page_id: str) -> None:
        pass


class IPageStatRepository(ABC):
    @abstractmethod
    def increment_stat(self, page_id: str, date_key: date, stat_type: str) -> None:
        pass

    @abstractmethod
    def get_top_pages(self, stat_type: str, from_date: date, to_date: date, limit: int) -> List[Page]:
        pass


class ITrendingPageService(ABC):
    @abstractmethod
    def get_most_liked_pages(self, from_date: date, to_date: date, top_n: int) -> List[Page]:
        pass

    @abstractmethod
    def get_most_viewed_pages(self, from_date: date, to_date: date, top_n: int) -> List[Page]:
        pass


# --- In-Memory Repository Implementation ---

class InMemoryPageStatRepository(IPageStatRepository):
    def __init__(self):
        self.data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # date -> stat_type -> page_id -> count
        self.page_meta = {}  # page_id -> Page
        self.lock = threading.Lock()

    def increment_stat(self, page_id: str, date_key: date, stat_type: str) -> None:
        with self.lock:
            self.data[date_key][stat_type][page_id] += 1
            if page_id not in self.page_meta:
                self.page_meta[page_id] = Page(page_id, f"Page {page_id}")

    def get_top_pages(self, stat_type: str, from_date: date, to_date: date, limit: int) -> List[Page]:
        aggregate = Counter()
        current_date = from_date
        while current_date <= to_date:
            aggregate.update(self.data[current_date][stat_type])
            current_date += timedelta(days=1)

        top_pages = aggregate.most_common(limit)
        return [self.page_meta[pid] for pid, _ in top_pages if pid in self.page_meta]


# --- Tracker Implementation ---

class SimplePageTracker(IPageTracker):
    def __init__(self, repo: IPageStatRepository):
        self.repo = repo

    def record_view(self, page_id: str) -> None:
        self.repo.increment_stat(page_id, date.today(), "view")

    def record_like(self, page_id: str) -> None:
        self.repo.increment_stat(page_id, date.today(), "like")


# --- Service Implementation ---

class TrendingPageService(ITrendingPageService):
    def __init__(self, repo: IPageStatRepository):
        self.repo = repo

    def get_most_liked_pages(self, from_date: date, to_date: date, top_n: int) -> List[Page]:
        return self.repo.get_top_pages("like", from_date, to_date, top_n)

    def get_most_viewed_pages(self, from_date: date, to_date: date, top_n: int) -> List[Page]:
        return self.repo.get_top_pages("view", from_date, to_date, top_n)


# --- Sample Usage ---
if __name__ == "__main__":
    repo = InMemoryPageStatRepository()
    tracker = SimplePageTracker(repo)
    service = TrendingPageService(repo)

    # Simulate activity
    tracker.record_view("p1")
    tracker.record_view("p1")
    tracker.record_like("p1")
    tracker.record_view("p2")
    tracker.record_like("p2")
    tracker.record_like("p2")
    tracker.record_view("p3")

    today = date.today()
    result_liked = service.get_most_liked_pages(today - timedelta(days=1), today, 2)
    result_viewed = service.get_most_viewed_pages(today - timedelta(days=1), today, 2)

    print("Top Liked Pages:", result_liked)
    print("Top Viewed Pages:", result_viewed)
