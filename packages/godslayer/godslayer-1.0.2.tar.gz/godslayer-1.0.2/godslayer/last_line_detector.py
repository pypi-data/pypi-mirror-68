"""This module implements last line detector."""
import csv
import re
from pathlib import Path
from typing import Iterator, List

from godslayer.csv.reversed_csv_reader import ReversedCsvReader
from godslayer.exceptions import InvalidFooterError
from godslayer.line_counter import LineCounter
from godslayer.list_string_matcher import ListStringMatcher


class LastLineDetector:
    @classmethod
    def detect_index(cls, path_to_file: Path, footer: List[str], encoding: str = "utf-8") -> int:
        index_from_last_line = cls._count_index_from_last_line(path_to_file, footer, encoding)
        return LineCounter.count(path_to_file, encoding) - 1 - index_from_last_line

    @classmethod
    def _count_index_from_last_line(cls, path_to_file: Path, footer: List[str], encoding: str = "utf-8") -> int:
        with path_to_file.open(encoding=encoding) as file:
            reader_input: Iterator[List[str]] = csv.reader(ReversedCsvReader.reversed_lines(file))
            number_newline = 0
            for index, list_column in enumerate(reader_input):
                for column in list_column:
                    number_newline += len(re.findall(r"(\r\n|\r|\n)", column))
                if ListStringMatcher.is_matched(footer, list_column):
                    return index + number_newline + 1
        raise InvalidFooterError(
            f"{path_to_file.name} does not contain Footer row. "
            "Confirm CSV file and footer again. "
            f"Footer = {footer}"
        )
