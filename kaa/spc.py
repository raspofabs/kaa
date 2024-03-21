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
    #print(f"Root: {root_node.type}")
    if root_node.type == "translation_unit":
        return [node for node in root_node.children if is_function(node)]


def render_func(f_def, source):
    source_as_text = source.decode("utf8")
    lines = source_as_text.split("\n")
    start_line = f_def.start_point[0]
    end_line = f_def.end_point[0]
    print("\n".join(lines[start_line:end_line+1]))


# NPC(switch (C1) { case E1: S1; case E2: S2; ... case En; Sn; }) = SUM(i = 1..n | NPC(Si))  // switch statement
# NPC(do S1 while (E1)) = 1 + NPC(E1) + NPC(S1)  // do-while statement
# NPC(for(E1; E2; E3) S1) = 1 + NPC(E1) + NPC(E2) + NPC(E3) + NPC(S1)  // for statement
def SPC(node):
    if node.type == "translation_unit":
        raise ValueError("SPC only works on functions and methods.")
    if node.type == "function_definition": # calculate with the compound statement
        body = node.children[2]
        assert body.type == "compound_statement"
        return SPC(body)
    if node.type == "return_statement":
        r, expression, semicolon = node.children
        return SPC(expression)
    if node.type == "if_statement": # NPC(if (E1) S1 else S2) = NPC(E1) + NPC(S1) + NPC(S2)  // if statement: in case of no else, NPC(S2) = 1
        s_if, condition_clause, compound_statement, else_clause = node.children
        return SPC(condition_clause) + SPC( compound_statement ) + SPC( else_clause )
    if node.type == "while_statement": # NPC(while (E1) S1) = 1 + NPC(E1) + NPC(S1)  // while statement
        s_while, condition_clause, compound_statement = node.children
        return SPC(condition_clause) + SPC( compound_statement )
    if node.type == "compound_statement": # NPC(S1; S2) = NPC(S1) * NPC(S2)  // sequential statements
        total = 1
        for child in node.children:
            total *= SPC(child)
        return total
    # NPC(S1) = 1  // any other statement; not one of the above
    return 1

def describe_node(node, indent):
    print(f"{indent}{node.type} = {SPC(node)}")
    for child in node.children:
        describe_node(child, indent + "> ")

def describe_func(f_def, source):
    source_as_text = source.decode("utf8")
    lines = source_as_text.split("\n")
    print(f"Function: {f_def}")
    for child in f_def.children:
        describe_node(child, " > ")
    print(f"SPC: {SPC(f_def)}")

import click

@click.command("spc")
@click.argument("source_path")
def run(source_path: Path):
    source_path = Path(source_path)
    source = read_source(source_path)
    tree = parse_source_to_tree(source)
    root_node = tree.root_node
    #for node in root_node.children:
        #print(f"N: {node}")
    functions = get_functions(tree)
    for f in functions:
        render_func(f, source)
        describe_func(f, source)
