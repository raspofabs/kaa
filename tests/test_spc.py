import pytest
from pathlib import Path
from .fixtures import source_simple, source_main, tree_simple, tree_multiple

def test_parse_to_tree(source_simple):
    from kaa.spc import parse_source_to_tree
    import tree_sitter
    tree = parse_source_to_tree(source_simple)
    assert tree is not None
    assert isinstance(tree, tree_sitter.Tree)

def test_get_functions(tree_simple, tree_multiple):
    from kaa.spc import get_functions
    functions = get_functions(tree_simple)
    assert functions is not None
    assert isinstance(functions, list)
    assert len(functions) == 1

    functions = get_functions(tree_multiple)
    assert functions is not None
    assert isinstance(functions, list)
    assert len(functions) == 4

