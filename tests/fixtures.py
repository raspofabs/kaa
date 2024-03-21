import pytest
from pathlib import Path

def get_source(variant):
    from kaa.spc import read_source
    source = read_source(Path(Path(__file__).parent) / f"test_data/{variant}")
    return source


def get_tree(variant):
    from kaa.spc import parse_source_to_tree
    source = get_source(variant)
    return source, parse_source_to_tree(source)


@pytest.fixture
def source_simple():
    return get_source("simple.cpp")


@pytest.fixture
def tree_simple(source_simple):
    return get_tree("simple.cpp")[1]


@pytest.fixture
def tree_multiple():
    return get_tree("multiple.cpp")[1]
