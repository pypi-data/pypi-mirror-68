"""Tests for row_pattern_matcher.py"""
import pytest

from godslayer.list_string_matcher import ListStringMatcher
from tests.testlibraries.instance_resource import InstanceResource

HEADER_GOLD_POINT_CARD_PLUS_1 = ["ゴールドポイントカードプラス ユーザー　様", "****-****-****-*456", "ゴールドポイントカードプラス"]
HEADER_GOLD_POINT_CARD_PLUS_2 = ["ゴールドポイントカードプラス ユーザー　様", "1234-5678-9012-3***", "ゴールドポイントカードプラス"]


class TestListStringMatcher:
    """Tests for Row Pattern Matcher."""

    @staticmethod
    @pytest.mark.parametrize(
        "list_pattern, row, expected",
        [
            (InstanceResource.HEADER_SF_CARD_VIEWER, InstanceResource.HEADER_SF_CARD_VIEWER, True),
            (
                InstanceResource.HEADER_SF_CARD_VIEWER,
                ["利用年月日", "定期", "鉄道会社名", "入場駅/事業者名", "定期", "鉄道会社名", "出場駅/降車場所", "利用額(円)", "メモ", "残額(円)"],
                False,
            ),
            (InstanceResource.REGEX_HEADER_GOLD_POINT_CARD_PLUS, HEADER_GOLD_POINT_CARD_PLUS_1, True),
            (InstanceResource.REGEX_HEADER_GOLD_POINT_CARD_PLUS, HEADER_GOLD_POINT_CARD_PLUS_2, True),
            (
                InstanceResource.REGEX_HEADER_GOLD_POINT_CARD_PLUS,
                ["ゴールドポイントカードプラス ユーザー　様", "****-****-****-*abc", "ゴールドポイントカードプラス"],
                False,
            ),
            (
                InstanceResource.REGEX_HEADER_GOLD_POINT_CARD_PLUS,
                ["ゴールドポイントカードプラス ユーザー　さん", "****-****-****-*456", "ゴールドポイントカードプラス"],
                False,
            ),
        ],
    )
    def test_create_by_path_csv_input(list_pattern, row, expected):
        """
        List of pattern should match row of same list with pattern.
        List of pattern should not match row which is different order.
        List of pattern should match row which match as regex.
        List of pattern should not match row which not match even as regex.
        """
        assert ListStringMatcher.is_matched(list_pattern, row) is expected
