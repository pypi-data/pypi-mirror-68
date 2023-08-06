"""This module implements fixture of instance."""


class InstanceResource:
    """This class implements fixture of instance."""

    REGEX_HEADER_GOLD_POINT_CARD_PLUS = [r".*　様", r"[0-9\*]{4}-[0-9\*]{4}-[0-9\*]{4}-[0-9\*]{4}", "ゴールドポイントカードプラス"]
    REGEX_FOOTER_GOLD_POINT_CARD_PLUS = ["^$", "^$", "^$", "^$", "^$", r"^\d*$", "^$"]
    HEADER_SF_CARD_VIEWER = ["利用年月日", "定期", "鉄道会社名", "入場駅/事業者名", "定期", "鉄道会社名", "出場駅/降車場所", "利用額(円)", "残額(円)", "メモ"]
    HEADER_VIEW_CARD = [
        "ご利用年月日",
        "ご利用箇所",
        "ご利用額",
        "払戻額",
        "ご請求額（うち手数料・利息）",
        "支払区分（回数）",
        "今回回数",
        "今回ご請求額・弁済金（うち手数料・利息）",
        "現地通貨額",
        "通貨略称",
        "換算レート",
    ]
    HEADER_ITABASHIKU_POPULATION = ["年齢", "総数(人)", "男(人)", "女(人)"]
    FOOTER_ITABASHIKU_POPULATION = [r"^\d*歳以上$", r"^\d*$", r"^\d*$", r"^\d*$"]
