from typing import Generator, Iterator, List

from godslayer.csv.reader_operators.reader_operator import ReaderOperator
from godslayer.exceptions import InvalidHeaderError
from godslayer.list_string_matcher import ListStringMatcher


class HeaderSkipper(ReaderOperator):
    def __init__(self, header: List[str]):
        super().__init__()
        self.header = header

    def process(self, reader_input: Iterator[List[str]]) -> Generator[List[str], None, None]:
        yield from super().process(reader_input)
        for self._index, list_input_row_standard_type_value in enumerate(reader_input):
            if ListStringMatcher.is_matched(self.header, list_input_row_standard_type_value):
                return
        raise InvalidHeaderError(
            f"CSV file does not contain header row." "Confirm CSV file and header again. " f"Header = {self.header}"
        )
