import pytest
from pathlib import Path


@pytest.fixture
def source_simple():
    from kaa.spc import read_source
    source = read_source(Path(Path(__file__).parent) / "test_data/simple.cpp")
    return source


@pytest.fixture
def source_main():
    from kaa.spc import read_source
    source = read_source(Path(Path(__file__).parent) / "test_data/main.cpp")
    return source


@pytest.fixture
def tree_simple(source_simple):
    from kaa.spc import parse_source_to_tree
    return parse_source_to_tree(source_simple)


@pytest.fixture
def tree_multiple(source_simple):
    from kaa.spc import read_source, parse_source_to_tree
    source = read_source(Path(Path(__file__).parent) / "test_data/multiple.cpp")
    return parse_source_to_tree(source)
