import pytest


def test_find_parser():
    from kaa.parser import get_parser_cpp

    parser = get_parser_cpp()
    assert parser is not None
    source = bytes("int a;","utf8")
    tree = parser.parse(source)
    assert tree is not None


def test_cant_find_parser(monkeypatch):
    import kaa
    from kaa.parser import get_parser_cpp

    monkeypatch.setattr(kaa.parser, "get_language_cpp", lambda : None)
    parser = get_parser_cpp()
    assert parser is None
