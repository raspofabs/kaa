import pytest
from pathlib import Path
from .fixtures import source_simple, source_main

@pytest.fixture
def cpp_parser():
    from kaa.parser import get_parser_cpp

    parser = get_parser_cpp()
    return parser


def test_read_simple_source(source_simple, cpp_parser):
    simple_tree = cpp_parser.parse(source_simple)


def test_read_main_source(source_main, cpp_parser):
    main_tree = cpp_parser.parse(source_main)

