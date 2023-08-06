from typing import Generator, Iterator, List, Optional

from godslayer.csv.reader_operators.reader_operator import ReaderOperator


class RecordBeforeFooterReader(ReaderOperator):
    def __init__(self, index_footer_line: int, *, before_task: Optional[ReaderOperator] = None):
        super().__init__(before_task=before_task)
        self.index_footer_line = index_footer_line

    def process(self, reader_input: Iterator[List[str]]) -> Generator[List[str], None, None]:
        yield from super().process(reader_input)
        for self._index, list_input_row_standard_type_value in enumerate(reader_input):
            if self.index >= self.index_footer_line:
                break
            yield list_input_row_standard_type_value
