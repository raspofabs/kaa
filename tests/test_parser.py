import pytest

def test_find_parser():
    from kaa.parser import get_parser_cpp

    parser = get_parser_cpp()
    assert parser is not None
    source = bytes("int a;","utf8")
    tree = parser.parse(source)
    assert tree is not None
