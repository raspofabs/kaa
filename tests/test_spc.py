import pytest
from pathlib import Path
from .fixtures import source_simple, tree_simple, tree_multiple, get_tree

def test_spc_simple(tree_simple):
    from kaa import get_functions
    from kaa.spc import SPC, debug_node
    functions = get_functions(tree_simple)
    for f in functions:
        result = SPC(f)
        debug_node(f)
        assert result == 1


def test_node_debug(capsys):
    from kaa.parser import get_parser_cpp
    from kaa.spc import debug_node

    example = "{if(a||b){switch(c){case 0:while(d){--d; ++a;}break;default:for(int x=0;x<b;x++){do{d++;}while(x<a);break;}return d;}}}"
    parser = get_parser_cpp()
    source = bytes(example,"utf8")
    tree = parser.parse(source)
    start_node = tree.root_node.children[0]
    debug_node(start_node)
    captured = capsys.readouterr()
    #print(captured.out)
    assert len(captured.out) > len(source)
    assert "Node:" in captured.out
    assert "Child:" in captured.out
    assert "if_statement" in captured.out
    assert "switch_statement" in captured.out
    assert "case_statement" in captured.out
    assert "while_statement" in captured.out
    assert "break_statement" in captured.out
    assert "for_statement" in captured.out
    assert "do_statement" in captured.out
    assert "return_statement" in captured.out


def test_empty_node_debug(capsys):
    from kaa.parser import get_parser_cpp
    from kaa.spc import debug_node
    example = "/* just a comment */"
    parser = get_parser_cpp()
    source = bytes(example,"utf8")
    tree = parser.parse(source)
    start_node = tree.root_node.children[0]
    debug_node(start_node)
    captured = capsys.readouterr()
    assert "Child:" not in captured.out


# Lots of small tests
tiny_tests = [
        ("int i = 0;",1),
        ("int func() {}",1),
        ("int func(a) /*c*/ {if(a){}}",2),
        ("int func(a) { return /*c*/ a ? b : c;}",2),
        ("{if(a){}}",2),
        ("{if(/*c*/ a||b){}}",3),
        ("{if(a){}else{}}",2),
        ("{if(a){} /*c*/ else/*c*/{}}",2),
        ("{if(a){if(b){}}}",3),
        ("{if(a){}else{if(b){}}}",3),
        ("{if(a){}/*c*/else{if(b){}}}",3),
        ("{if(a && b){}else{}}",3),
        ("{if(a || b){}else{}}",3),
        ("{if(a && b || c){}else{}}",4),
        ("{if(a /*c*/ && b || c){}else{}}",4),
        ("{if(a && b || /*com*/ c){}else{}}",4),
        ("{while(a)/*c*/{ --a; }}",2),
        ("{do{a--;}while(a);}",2),
        ("{do/*com*/{a--;}while(/*com*/a/*com*/);}",2),
        ("int f(int a) { return a > 3 ? 1 : 0;}",2),
        ("int f(int a) { return a > 3 ? /*c*/ 1 : 0;}",2),
        ("{switch(a){case 0: break; default: break;}}",2),
        ("{switch(a)/*c*/{case 0: break; case 1: case 2: break; default: break;}}",3),
        ("{switch(a){case 0: break; case 1: /*c*/ case 2: /*c*/ break; default: /*c*/ break;}}",3),
        ("{switch(a){case 0: if(a){} break; case 1: /*c*/ if(b) {} break;}}",5),
        ("{switch(a){case 0: if(a){} break; default: /*c*/ if(b) {} break;}}",4),
        ("{switch(a){case 0: if(b){} break; default: }",3),
        ("{switch(a){case 0: if(b){} break; }",3),
        ("{for(int a = 0; a < 10; ++1) {}}",2),
        ("{for(int a = 0; /*c*/ a < 10; ++1) {}}",2),
        ("{/*c*/ for(int /*c*/a/*c*/ =/*c*/ 0/*c*/; /*c*/ a /*c*/ < /*c*/ 10 /*c*/ ; /*c*/ ++1 /*c*/ ) /*c*/ { /*c*/ } /*c*/ }",2),
        ("{for(/*c*/auto/*c*/ a/*c*/ :/*c*/ range/*c*/)/*c*/ {if(a){}}}",3),
        ("{for(auto a:b){} for(auto a:c){}}",4),
        ("{if (str == \"string\"){}}", 2),
        ("{ return x[a > 3 ? 1 : 0];}",2),
        ("{ return (a > 3 ? 1 : 0)[x];}",2),
        ("int f(int a) { return x(a > 3 ? 1 : 0);}",2),
        ("int f(int a) { return x(a > 3 ? 1 : 0, a < 7 ? 1 : 0);}",4),
        ("{ int b = a > 3 ? 1 : 0; return b; }",2),
        ("{ int b = 0; b = a > 3 ? 1 : 0; return b; }",2),
        ("{ int b = 2, c = 0; (a > 3 ? b : c) = 1; return b+c; }",2),
        ("{ std::cout << 1; }",1),
        ("{ std::cout << 1 << std::endl; }",1),
        ("{;}",1),
        ("{ for (; i < blocklen; ++i) {} }",2),
        ]

@pytest.mark.parametrize("example, expected", tiny_tests)
def test_spc_tiny(capsys, example, expected):
    from kaa.parser import get_parser_cpp
    from kaa.spc import SPC, describe_func

    parser = get_parser_cpp()
    source = bytes(example,"utf8")
    tree = parser.parse(source)
    start_node = tree.root_node.children[0]
    result = SPC(start_node)
    describe_func(start_node, source)
    captured = capsys.readouterr()
    assert len(captured.out) > len(source)
    if result != expected:
        print(captured.out)
    assert result == expected

spc_tests = [
        ("classes_one_if.cpp",2),
        ("complex.cpp",6),
        ("extended_switch.cpp",4),
        ("high_spc.cpp",256),
        ("lambda_one_if.cpp",2),
        ("main.cpp",2),
        ("one_dowhile.cpp",2),
        ("one_for.cpp",2),
        ("one_if.cpp",2),
        ("one_switch.cpp",5),
        ("one_ternary.cpp",2),
        ("one_while.cpp",2),
        ("qac_example.cpp",26),
        ("simple.cpp",1),
        ("two_ifs.cpp",4),
        ("z_example_gilded_rose.cpp",211),
        ("z_example_tennis1.cpp",20),
        ("z_example_tennis2.cpp",139968000),
        ("z_example_tennis3.cpp",12),
        ("z_example_simple.cpp",6),
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
        try:
            result = SPC(f)
            if expected is not None:
                if result != expected:
                    describe_func(f, source)
                    assert result == expected
        except:
            print("Error in parsing...")
            describe_func(f, source)
            raise
