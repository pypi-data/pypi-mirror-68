"""Tests for csv_with last_line_detector.py"""
from godslayer.line_counter import LineCounter


class TestLineCounter:
    @staticmethod
    def test_gold_point_card_plus_201912(path_gold_point_card_plus_201912):
        assert LineCounter.count(path_gold_point_card_plus_201912, "shift_jis_2004") == 5

    @staticmethod
    def test_itabashiku_population_newline_contains(path_itabashiku_population_newline_contains):
        assert LineCounter.count(path_itabashiku_population_newline_contains, "shift_jis_2004") == 133
