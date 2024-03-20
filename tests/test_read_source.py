import pytest
from pathlib import Path
from .fixtures import source_simple, source_main

def test_read_source():
    from kaa.spc import read_source

    source = read_source(Path(Path(__file__).parent) / "test_data/simple.cpp")
    assert source is not None
    assert isinstance(source, bytes)
    source_as_text = source.decode("utf8")
    assert "int hello(int a)" in source_as_text


def test_read_simple_source(source_simple):
    source_simple
    assert isinstance(source_simple, bytes)
    source_as_text = source_simple.decode("utf8")
    assert "int hello(int a)" in source_as_text


def test_read_main_source(source_main):
    source_main
    assert isinstance(source_main, bytes)
    source_as_text = source_main.decode("utf8")
    assert "int main()" in source_as_text
    assert "std::cout" in source_as_text
