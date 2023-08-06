from typing import List, Optional

import pytest

from godslayer.csv.god_slayer import GodSlayer


class GodSlayerChecker:
    @staticmethod
    def assert_god_slayer(god_slayer: GodSlayer, expected_index_start: int, expected: List[List[str]]):
        length_record = 0
        iterator_actual = god_slayer.__iter__()
        # Order of argument for zip() is important.
        # First argument should be "expected"
        # to confirm that next iteration of actual raises StopIteration,
        # since zip() iterates first argument even if second argument is empty.
        for index, (expected_record, actual) in enumerate(zip(expected, iterator_actual)):
            assert god_slayer.index == expected_index_start + index
            assert actual == expected_record
            length_record += 1
        GodSlayerChecker.assert_length(expected, iterator_actual, length_record)

    @staticmethod
    def assert_god_slayer_partition(god_slayer: GodSlayer, expected: List[List[str]]):
        length_record = 0
        iterator_actual = god_slayer.__iter__()
        gap = False
        last_index: Optional[int] = None
        for expected_record, actual in zip(expected, iterator_actual):
            if last_index is not None and god_slayer.index - last_index > 1:
                gap = True
            last_index = god_slayer.index
            assert actual == expected_record
            length_record += 1
        GodSlayerChecker.assert_length(expected, iterator_actual, length_record)
        assert gap

    @staticmethod
    def assert_length(expected, iterator_actual, length_record):
        assert length_record == len(expected)
        with pytest.raises(StopIteration):
            next(iterator_actual)
