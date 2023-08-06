"""
This module implements Reversed CSV Reader.
The reversed file reader already exists in PyPI,
however, it doesn't support shift_jis_2004.
@see https://pypi.org/project/file-read-backwards/
"""
import os


class ReversedCsvReader:
    """This class implements Reversed CSV Reader."""

    @classmethod
    def reversed_lines(cls, file):
        """Generate the lines of file in reverse order."""
        part = ""
        quoting = False
        for block in cls.reversed_blocks(file):
            for c in reversed(block):
                if c == '"':
                    quoting = not quoting
                elif c == "\n" and part and not quoting:
                    yield part[::-1]
                    part = ""
                part += c
        if part:
            yield part[::-1]

    @staticmethod
    def reversed_blocks(file, blocksize=4096):
        """Generate blocks of file's contents in reverse order."""
        file.seek(0, os.SEEK_END)
        here = file.tell()
        while 0 < here:
            delta = min(blocksize, here)
            here -= delta
            file.seek(here, os.SEEK_SET)
            yield file.read(delta)
