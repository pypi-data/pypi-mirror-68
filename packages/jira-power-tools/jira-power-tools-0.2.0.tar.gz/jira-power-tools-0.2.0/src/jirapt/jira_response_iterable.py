"""Iterable for jira requests."""
from concurrent.futures import ThreadPoolExecutor as Executor
import math
from queue import Queue
from typing import Callable, Iterator

from jira.client import ResultList

DEFAULT_WORKERS = 4


class JiraResponseIterable(object):
    """Object to iterate over paginated jira results."""

    def __init__(self, results: ResultList, get_more_fn: Callable[[int], ResultList],) -> None:
        """
        Create a JiraResponseIterable.

        :param results: Response object from Jira.
        :param get_more_fn: Function to get next page of data.
        """
        self.results = results
        self.get_more_fn = get_more_fn

    def __iter__(self) -> Iterator:
        """Get next item from jira."""
        while True:
            for item in self.results:
                yield item

            # Have we looked at all the results?
            if self.results.startAt + self.results.maxResults > self.results.total:
                break

            self.results = self.get_more_fn(self.results.startAt + self.results.maxResults)

    def __len__(self) -> int:
        """Get the total number of items available."""
        return self.results.total


class JiraResponseIterableParallel(object):
    """
    Create a response iterator that will gather results in multiple threads.

    Note: This will gather all results in memory at the start of iteration. So it may use a lot
    of memory. It will also wait for all results to be collected before starting iteration.
    """

    def __init__(
        self,
        results: ResultList,
        get_more_fn: Callable[[int], ResultList],
        n_workers: int = DEFAULT_WORKERS,
    ) -> None:
        """
        Create a JiraResponseIterableParallel.

        :param results: Response object from Jira.
        :param get_more_fn: Function to get next page of data.
        :param n_workers: Number of threads to use for processing.
        """
        self.page_size = results.maxResults
        self.total_results = results.total
        self.get_more_fn = get_more_fn
        self.n_workers = n_workers
        self.queue = Queue()

        self._add_results_to_queue(results)

    def _add_results_to_queue(self, results) -> None:
        """
        Add a set of jira responses to the queue.

        :param results: Results to add to queue.
        """
        for r in results:
            self.queue.put(r)

    def _get_more(self, index: int):
        """
        Get the specified page of results from jira.

        :param index: Index of page to query.
        :return:
        """
        return self.get_more_fn(index * self.page_size)

    def _gather_results(self) -> None:
        """Spawn workers and gather results from jira."""
        total_workers = math.ceil(self.total_results / self.page_size)
        print(f"total_workers {total_workers}")
        with Executor(max_workers=self.n_workers) as exe:
            workers = [exe.submit(self._get_more, i) for i in range(1, total_workers)]

            for w in workers:
                result = w.result()
                self._add_results_to_queue(result)

    def __iter__(self) -> Iterator:
        """Get next item from jira."""
        self._gather_results()
        i = 0
        while i < self.total_results:
            item = self.queue.get()
            yield item
            i += 1

    def __len__(self) -> int:
        """Get the total number of items available."""
        return self.total_results
