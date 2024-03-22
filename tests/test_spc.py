import pytest
from pathlib import Path
from .fixtures import source_simple, tree_simple, tree_multiple, get_tree

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


def test_spc_simple(tree_simple):
    from kaa.spc import SPC, get_functions
    functions = get_functions(tree_simple)
    for f in functions:
        result = SPC(f)
        assert result == 0


spc_tests = [
        ("one_if.cpp",2),
        ("one_while.cpp",2),
        ("one_switch.cpp",5),
        ("one_dowhile.cpp",3),
        ("one_for.cpp",2),
        ("two_ifs.cpp",4),
        ]

@pytest.mark.parametrize("variant, expected", spc_tests)
def test_spc_other(variant, expected):
    source, tree = get_tree(variant)
    from kaa.spc import SPC, get_functions, describe_func

    try:
        result = SPC(tree.root_node)
        print(f"node : {tree.root_node.type}")
        assert False
    except ValueError:
        pass


    functions = get_functions(tree)
    for f in functions:
        result = SPC(f)
        if result != expected:
            describe_func(f, source)
        assert result == expected

