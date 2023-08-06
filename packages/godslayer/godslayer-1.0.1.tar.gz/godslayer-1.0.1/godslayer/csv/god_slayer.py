"""This module implements analyzing process of CSV."""
import csv
from pathlib import Path
from typing import Generator, List, Optional

from godslayer.csv.reader_operators.reader_operator import ReaderOperator
from godslayer.exceptions import LogicError
from godslayer.reader_operator_factory import ReaderOperatorFactory


class GodSlayer:
    """This class implements analyzing process of CSV."""

    def __init__(self, path_to_file: Path, reader_operator_factory: ReaderOperatorFactory, *, encoding: str = "utf-8"):
        self.path_to_file = path_to_file
        self.reader_operator_factory = reader_operator_factory
        self.encoding = encoding
        self.reader_operator: Optional[ReaderOperator] = None

    def __iter__(self) -> Generator[List[str], None, None]:
        # noinspection LongLine
        # pylint:disable=line-too-long
        """
        This method convert this csv into Zaim format CSV.
        @see https://stackoverflow.com/questions/14797930/python-custom-iterator-close-a-file-on-stopiteration/14798115#14798115 # noqa
        """
        self.reader_operator = self.reader_operator_factory.create()
        with self.path_to_file.open("r", encoding=self.encoding) as file_input:
            yield from self.reader_operator.process(csv.reader(file_input))

    @property
    def index(self) -> int:
        if self.reader_operator is None:
            raise LogicError("Index can't be accessed before iterate.")  # pragma: no cover
        return self.reader_operator.index
