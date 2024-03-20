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
    print(f"Root: {root_node.type}")
    if root_node.type == "translation_unit":
        return [node for node in root_node.children if is_function(node)]


import click

@click.command("spc")
@click.argument("source_path")
def run(source_path: Path):
    source_path = Path(source_path)
    source = read_source(source_path)
    tree = parse_source_to_tree(source)
    root_node = tree.root_node
    for node in root_node.children:
        print(f"N: {node}")
    functions = get_functions(tree)

