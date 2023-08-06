from pathlib import Path
from typing import List, Optional

from godslayer.csv.reader_operators.header_skipper import HeaderSkipper
from godslayer.csv.reader_operators.partition_skip_record_before_footer_reader import (
    PartitionSkipRecordBeforeFooterReader,
)
from godslayer.csv.reader_operators.partition_skip_record_reader import PartitionSkipRecordReader
from godslayer.csv.reader_operators.reader_operator import ReaderOperator
from godslayer.csv.reader_operators.record_before_footer_reader import RecordBeforeFooterReader
from godslayer.csv.reader_operators.record_reader import RecordReader
from godslayer.last_line_detector import LastLineDetector


class ReaderOperatorFactory:
    def __init__(
        self,
        path_to_file: Path,
        *,
        header: Optional[List[str]] = None,
        partition: Optional[List[str]] = None,
        footer: Optional[List[str]] = None,
        encoding: str = "utf-8"
    ):
        self.path_to_file = path_to_file
        self.header = header
        self.partition = partition
        self.footer = footer
        self.encoding = encoding

    def create(self) -> ReaderOperator:
        header_skipper: Optional[HeaderSkipper] = None if self.header is None else HeaderSkipper(self.header)
        if self.footer is not None:
            index_last_line = LastLineDetector.detect_index(self.path_to_file, self.footer, self.encoding)
            reader_operator = self._create_record_before_footer_reader(index_last_line, header_skipper)
        else:
            reader_operator = self._create_no_footer_record_reader(header_skipper)
        return reader_operator

    def _create_no_footer_record_reader(self, header_skipper: Optional[HeaderSkipper]):
        if self.partition is not None:
            return PartitionSkipRecordReader(self.partition, before_task=header_skipper)
        else:
            return RecordReader(before_task=header_skipper)

    def _create_record_before_footer_reader(self, index_last_line: int, header_skipper: Optional[HeaderSkipper]):
        if self.partition is not None:
            return PartitionSkipRecordBeforeFooterReader(self.partition, index_last_line, before_task=header_skipper)
        else:
            return RecordBeforeFooterReader(index_last_line, before_task=header_skipper)
