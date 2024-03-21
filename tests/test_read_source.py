import pytest
from pathlib import Path
from .fixtures import source_simple, get_source

def test_read_source():
    from kaa.spc import read_source

    source = read_source(Path(Path(__file__).parent) / "test_data/simple.cpp")
    assert source is not None
    assert isinstance(source, bytes)
    source_as_text = source.decode("utf8")
    assert "int hello(int a)" in source_as_text


def test_fail_read_source():
    from kaa.spc import read_source
    try:
        source = read_source("duck")
        assert source is None
    except AttributeError:
        pass
    else:
        #  we should have excepted with an attribute error as we did not send a
        #  path
        assert False

def test_fail_read_source(tmpdir):
    from kaa.spc import read_source
    try:
        source = read_source(Path(tmpdir / "nonexistent.hpp"))
        assert source is None
    except FileNotFound:
        assert False
        pass


def test_read_simple_source(source_simple):
    source_simple
    assert isinstance(source_simple, bytes)
    source_as_text = source_simple.decode("utf8")
    assert "int hello(int a)" in source_as_text


def test_read_main_source():
    source_main = get_source("main.cpp")
    assert isinstance(source_main, bytes)
    source_as_text = source_main.decode("utf8")
    assert "int main()" in source_as_text
    assert "std::cout" in source_as_text
