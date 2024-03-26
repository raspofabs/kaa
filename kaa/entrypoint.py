import click
from pathlib import Path
from kaa import read_source, parse_source_to_tree, get_functions, render_func, get_function_name
from kaa.spc import describe_func, SPC

@click.command("spc")
@click.option("-v", "--verbose", is_flag=True, default=False)
@click.argument("source_path")
def run(source_path: Path, verbose: bool):
    source_path = Path(source_path)
    source = read_source(source_path)
    tree = parse_source_to_tree(source)
    root_node = tree.root_node
    #for node in root_node.children:
        #print(f"N: {node}")
    functions = get_functions(tree)
    for f in functions:
        if verbose:
            render_func(f, source)
            describe_func(f, source)
        else:
            print(f"SPC of {get_function_name(f, source)}: {SPC(f)}")
