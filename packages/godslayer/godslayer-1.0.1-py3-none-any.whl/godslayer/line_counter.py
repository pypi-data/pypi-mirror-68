"""This module implements last line detector."""
from mmap import mmap
from pathlib import Path


class LineCounter:
    @staticmethod
    def count(path_to_file: Path, encoding: str = "utf-8") -> int:
        # noinspection LongLine
        # pylint:disable=line-too-long
        """
        Counts number of line.
        Count starts with 1.
        If content of file ends with line separator, next line is out of count.
        @see https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python/850962#850962 # noqa
        """
        with path_to_file.open("r+", encoding=encoding) as f:
            buf = mmap(f.fileno(), 0)
            lines = 0
            readline = buf.readline
            while readline():
                lines += 1
        return lines
