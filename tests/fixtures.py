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

