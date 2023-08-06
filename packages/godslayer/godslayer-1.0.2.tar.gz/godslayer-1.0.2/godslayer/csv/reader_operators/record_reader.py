from typing import Generator, Iterator, List

from godslayer.csv.reader_operators.reader_operator import ReaderOperator


class RecordReader(ReaderOperator):
    def process(self, reader_input: Iterator[List[str]]) -> Generator[List[str], None, None]:
        yield from super().process(reader_input)
        for self._index, list_input_row_standard_type_value in enumerate(reader_input):
            yield list_input_row_standard_type_value
