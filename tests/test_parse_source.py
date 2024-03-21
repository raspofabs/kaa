import pytest
from pathlib import Path
from .fixtures import source_simple, get_source

@pytest.fixture
def cpp_parser():
    from kaa.parser import get_parser_cpp

    parser = get_parser_cpp()
    return parser


def test_read_simple_source(source_simple, cpp_parser):
    simple_tree = cpp_parser.parse(source_simple)


def test_read_main_source(cpp_parser):
    source_main = get_source("main.cpp")
    main_tree = cpp_parser.parse(source_main)

