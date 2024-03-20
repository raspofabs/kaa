import pytest
from pathlib import Path

def test_read_source():
    from kaa.spc import read_source

    source = read_source(Path(Path(__file__).parent) / "test_data/simple.cpp")
    assert source is not None
    assert isinstance(source, bytes)
    source_as_text = source.decode("utf8")
    assert "int hello(int a)" in source_as_text

    pass
