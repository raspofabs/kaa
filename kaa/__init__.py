from pathlib import Path

def read_source(source_file: Path):
    if source_file.is_file():
        with open(source_file,"rb") as fh:
            return fh.read()
    return None


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


