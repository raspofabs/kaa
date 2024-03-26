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
    from kaa import get_functions
    functions = get_functions(tree_simple)
    assert functions is not None
    assert isinstance(functions, list)
    assert len(functions) == 1

    functions = get_functions(tree_multiple)
    assert functions is not None
    assert isinstance(functions, list)
    assert len(functions) == 4


def test_get_function_with_python(tree_simple, tree_multiple):
    from kaa import get_functions
    from kaa.parser import get_parser_python
    parser = get_parser_python()
    tree = parser.parse(bytes("print(1)", "utf8"))
    functions = get_functions(tree)
    assert functions is not None
    assert isinstance(functions, list)
    assert len(functions) == 0

name_tests = [
        ("simple.cpp","hello"),
        ("main.cpp","main"),
        ("one_for.cpp","one_for"),
        ("two_ifs.cpp","two_ifs"),
        ("operator.cpp","operator<<"),
        ]

@pytest.mark.parametrize("variant, expected", name_tests)
def test_get_function_name(variant, expected):
    from kaa import get_functions, get_function_name
    from kaa.sitter_util import debug_node
    source, tree = get_tree(variant)
    functions = get_functions(tree)
    f_def = functions[0]
    #debug_node(f_def)
    f_name = get_function_name(f_def, source)
    if f_name != expected:
        debug_node(f_def)
    assert f_name == expected


def test_render_func(capsys):
    from kaa import get_functions, render_func
    source, tree = get_tree("simple.cpp")
    functions = get_functions(tree)
    render_func(functions[0], source)
    captured = capsys.readouterr()
    assert "hello" in captured.out
    assert "\n" in captured.out
    assert "int hello(int a) {" in captured.out


