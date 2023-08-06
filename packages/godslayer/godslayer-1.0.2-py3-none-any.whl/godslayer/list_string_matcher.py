"""This module implements row pattern matcher."""
import re
from typing import List


class ListStringMatcher:
    """This class implements row pattern matcher."""

    @staticmethod
    def is_matched(list_pattern: List[str], list_column: List[str]) -> bool:
        """Returns whether all column is same or match with pattern or not."""
        if len(list_pattern) != len(list_column):
            return False
        for pattern, column in zip(list_pattern, list_column):
            compiled_pattern = re.compile(pattern, re.UNICODE)
            if pattern != column and not compiled_pattern.search(column):
                return False
        return True
