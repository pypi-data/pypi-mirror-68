from typing import Generator, Iterator, List, Optional

from godslayer.csv.reader_operators.reader_operator import ReaderOperator
from godslayer.list_string_matcher import ListStringMatcher


class PartitionSkipRecordReader(ReaderOperator):
    def __init__(self, partition: List[str], *, before_task: Optional[ReaderOperator] = None):
        super().__init__(before_task=before_task)
        self.partition = partition

    def process(self, reader_input: Iterator[List[str]]) -> Generator[List[str], None, None]:
        yield from super().process(reader_input)
        for self._index, list_input_row_standard_type_value in enumerate(reader_input):
            if ListStringMatcher.is_matched(self.partition, list_input_row_standard_type_value):
                continue
            yield list_input_row_standard_type_value
