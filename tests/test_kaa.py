import pytest
from pathlib import Path
from .fixtures import source_simple, tree_simple, tree_multiple, get_tree


def test_parse_to_tree(source_simple):
    from kaa import parse_source_to_tree
    import tree_sitter
    tree = parse_source_to_tree(source_simple)
    assert tree is not None
    assert isinstance(tree, tree_sitter.Tree)


def test_get_functions(tree_simple, tree_multiple):
    from kaa import is_function, get_functions
    functions = get_functions(tree_simple)
    assert functions is not None
    assert isinstance(functions, list)
    assert len(functions) == 1

    functions = get_functions(tree_multiple)
    assert functions is not None
    assert isinstance(functions, list)
    assert len(functions) == 4


