from pathlib import Path
from typing import List, Optional

from godslayer.csv.god_slayer import GodSlayer
from godslayer.reader_operator_factory import ReaderOperatorFactory


class GodSlayerFactory:
    def __init__(
        self,
        *,
        header: Optional[List[str]] = None,
        partition: Optional[List[str]] = None,
        footer: Optional[List[str]] = None,
        encoding: str = "utf-8"
    ):
        self.header = header
        self.partition = partition
        self.footer = footer
        self.encoding = encoding

    def create(self, path_to_file: Path) -> GodSlayer:
        return GodSlayer(
            path_to_file,
            ReaderOperatorFactory(
                path_to_file, header=self.header, partition=self.partition, footer=self.footer, encoding=self.encoding
            ),
            encoding=self.encoding,
        )
