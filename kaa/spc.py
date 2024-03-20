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
    return True


def get_functions(tree):
    root_node = tree.root_node
    return [node for node in root_node.children if is_function(node)]
