import pytest
from pathlib import Path
from .fixtures import source_simple, source_main


def test_build_requirements(tmpdir):
    from kaa.parser import build_library, fetch_source
    try:
        fetch_source(Path("not_here"), None)
    except FileNotFoundError:
        pass
    else:
        assert False


def test_find_parser():
    from kaa.parser import get_parser_cpp

    parser = get_parser_cpp()
    assert parser is not None
    source = bytes("int a;","utf8")
    tree = parser.parse(source)
    assert tree is not None

