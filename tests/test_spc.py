import pytest
from pathlib import Path
from .fixtures import source_simple, tree_simple, tree_multiple, get_tree

def test_spc_simple(tree_simple):
    from kaa import get_functions
    from kaa.spc import SPC
    functions = get_functions(tree_simple)
    for f in functions:
        result = SPC(f)
        assert result == 1

tiny_tests = [
        ("int i = 0;",None),
        ("{if(a){}else{}}",2),
        ("{if(a && b){}else{}}",3),
        ("{if(a || b){}else{}}",3),
        ("{if(a && b || c){}else{}}",4),
        ]

@pytest.mark.parametrize("example, expected", tiny_tests)
def test_spc_tiny(example, expected):
    from kaa.parser import get_parser_cpp
    from kaa.spc import SPC, describe_func

    parser = get_parser_cpp()
    source = bytes(example,"utf8")
    tree = parser.parse(source)
    start_node = tree.root_node.children[0]
    result = SPC(start_node)
    if result != expected:
        describe_func(start_node, source)
    assert result == expected

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
    from kaa import get_functions
    from kaa.spc import SPC, describe_func

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

