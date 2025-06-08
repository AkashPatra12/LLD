from abc import ABC, abstractmethod
from typing import List, Tuple, Dict

class IFileProcessor(ABC):
    @abstractmethod
    def process(self, files: List[Tuple[str, int, List[str]]]) -> None:
        pass

class IReporter(ABC):
    @abstractmethod
    def report_total_size(self) -> int:
        pass

    @abstractmethod
    def report_top_k_collections(self, k: int) -> List[Tuple[str, int]]:
        pass

from collections import defaultdict
import heapq

class FileProcessor(IFileProcessor):
    def __init__(self, reporter: 'IReporter'):
        self.reporter = reporter

    def process(self, files: List[Tuple[str, int, List[str]]]) -> None:
        for file_name, size, collections in files:
            self.reporter.add_file(file_name, size, collections)

class FileStatsReporter(IReporter):
    def __init__(self):
        self.total_size = 0
        self.collection_sizes = defaultdict(int)

    def add_file(self, file_name: str, size: int, collections: List[str]) -> None:
        self.total_size += size
        for collection in collections:
            self.collection_sizes[collection] += size

    def report_total_size(self) -> int:
        return self.total_size

    def report_top_k_collections(self, k: int) -> List[Tuple[str, int]]:
        return heapq.nlargest(k, self.collection_sizes.items(), key=lambda x: x[1])

if __name__ == "__main__":
    files = [
        ("file1.txt", 100, []),
        ("file2.txt", 200, ["collection1"]),
        ("file3.txt", 200, ["collection1"]),
        ("file4.txt", 300, ["collection2"]),
        ("file5.txt", 100, []),
    ]

    reporter = FileStatsReporter()
    processor = FileProcessor(reporter)
    processor.process(files)

    print("Total size of files processed:", reporter.report_total_size())
    print("Top 2 collections:")
    for name, size in reporter.report_top_k_collections(2):
        print(f"- {name} : {size}")
