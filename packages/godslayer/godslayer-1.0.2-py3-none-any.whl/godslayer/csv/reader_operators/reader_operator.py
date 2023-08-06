from __future__ import annotations

from typing import Generator, Iterator, List, Optional


class ReaderOperator:
    def __init__(self, *, before_task: Optional[ReaderOperator] = None):
        self.before_task = before_task
        self._index: Optional[int] = None

    def process(self, reader_input: Iterator[List[str]]) -> Generator[List[str], None, None]:
        if self.before_task is None:
            return
        yield from self.before_task.process(reader_input)

    @property
    def index(self) -> int:
        return (0 if self._index is None else self._index) + (0 if self.before_task is None else self.before_task.index)
