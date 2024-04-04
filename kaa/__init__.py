from pathlib import Path

import logging
logger = logging.getLogger("kaa")

def read_source(source_file: Path):
    if source_file.is_file():
        with open(source_file,"rb") as fh:
            return fh.read()
    return None


def get_source_as_text(source_bytes):
    text = source_bytes.decode("utf8", errors="ignore")
    return text


def parse_source_to_tree(source: bytes):
    from kaa.parser import get_parser_cpp
    parser = get_parser_cpp()
    return parser.parse(source)

def is_function(tree_node):
    return tree_node.type == "function_definition"


def get_functions(tree):
    root_node = tree.root_node
    if root_node.type == "translation_unit":
        return [node for node in root_node.children if is_function(node)]
    return []


def render_func(f_def, source):
    source_as_text = source.decode("utf8")
    lines = source_as_text.split("\n")
    start_line = f_def.start_point[0]
    end_line = f_def.end_point[0]
    print("\n".join(lines[start_line:end_line+1]))


def get_function_name(f_def, source):
    from kaa.sitter_util import debug_node
    source_as_text = get_source_as_text(source)
    lines = source_as_text.split("\n")
    name_declaration = f_def.child_by_field_name("declarator")
    if name_declaration is None:
        logger.error(f"Unable to find name declaration for function {f_def}")
        debug_node(f_def)
        return "none"
    if len(name_declaration.children) == 0:
        return "ERROR"
    name_node = name_declaration.child_by_field_name("declarator")
    if name_node is None:
        #print(f"No name_node... {len(name_declaration.children)}")
        #debug_node(name_declaration)
        for node in name_declaration.children:
            if node.type in ["operator_cast", "qualified_identifier"]:
                name_node = node
                break
            print(f"Child ({node.type}): {node}")

    if name_node is None:
        best_guess = [node for node in name_declaration.children if "declarator" in node.type]
        if len(best_guess) > 0:
            name_node = best_guess[0]
            better = name_node.child_by_field_name("declarator")
            if better is not None:
                name_node = better
    start_line = name_node.start_point[0]
    end_line = name_node.end_point[0]
    assert start_line == end_line
    start_column = name_node.start_point[1]
    end_column = name_node.end_point[1]
    return lines[start_line][start_column:end_column]
