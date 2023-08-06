import csv

import pytest

from godslayer.csv.reader_operators.header_skipper import HeaderSkipper
from godslayer.exceptions import InvalidHeaderError
from tests.testlibraries.instance_resource import InstanceResource


class TestHeaderSkipper:
    @staticmethod
    def test(path_gold_point_card_plus):
        with path_gold_point_card_plus.open("r", encoding="shift_jis_2004") as file_input:
            header_skipper = HeaderSkipper(InstanceResource.REGEX_HEADER_GOLD_POINT_CARD_PLUS)
            with pytest.raises(InvalidHeaderError):
                for list_column in header_skipper.process(csv.reader(file_input)):
                    print(list_column)
