import pytest


@pytest.fixture
def path_gold_point_card_plus(resource_path_root):
    yield resource_path_root / "common/gold_point_card_plus.csv"


@pytest.fixture
def path_gold_point_card_plus_201912(resource_path_root):
    yield resource_path_root / "common/gold_point_card_plus_201912.csv"


@pytest.fixture
def path_view_card(resource_path_root):
    yield resource_path_root / "common/view_card.csv"


@pytest.fixture
def path_sf_card_viewer(resource_path_root):
    yield resource_path_root / "common/sf_card_viewer.csv"


@pytest.fixture
def path_itabashiku_population(resource_path_root):
    yield resource_path_root / "common/itabashiku_population.csv"


@pytest.fixture
def path_itabashiku_population_newline_contains(resource_path_root):
    yield resource_path_root / "common/itabashiku_population_newline_contains.csv"
