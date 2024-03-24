from pathlib import Path
from kaa import read_source, parse_source_to_tree
from kaa import get_functions, render_func

def SPC_E(node):
    return SPC(node) or 0

def OPCOST(operator_node):
    if operator_node.type in ["&&", "||"]:
        return 1
    return 0

def SPC_S(node):
    return SPC(node) or 1

def SPC(node):
    if node.type == "comment":
        return None
    if node.type == "translation_unit":
        raise ValueError("SPC only works on functions and methods.")
    if node.type == "function_definition": # calculate with the compound statement
        print(node.sexp())
        body = node.children[2]
        assert body.type == "compound_statement"
        return SPC(body)
    if node.type == "return_statement":
        r, expression, semicolon = node.children
        return SPC(expression)

    if node.type == "case_statement":
        case, *tail = node.children
        if case.type == "case":
            s_literal, s_col, *statement = tail
            if len(statement):
                return SPC_S(statement[0])
            else:
                return 0
        elif case.type == "default":
            s_col, *statement = tail
            if len(statement):
                return SPC_S(statement[0])
            else:
                return 0
    if node.type == "condition_clause":
        return SPC(node.children[1])
    if node.type == "else_clause":
        print(node.sexp())
        s_else, statement = node.children
        return SPC(node.children[1])
    if node.type == "binary_expression":
        print(node.sexp())
        assert len(node.children) == 3
        left, op, right = node.children
        return SPC_E(left) + OPCOST(op) + SPC_E(right)
    # NPC(E1 ? E2 : E3) = 2 + NPC(E1) + NPC(E2) + NPC(E3)  // conditional operator
    if node.type == "conditional_expression":
        print(node.sexp())
        assert len(node.children) == 5
        condition, s_q, if_true, s_colon, if_false  = node.children
        return 2 + SPC_E(condition) + OPCOST(if_true) + SPC_E(if_false)
    #sum(1 for c in node.children if c.type in ["&&", "||"])
    if node.type == "update_expression":
        return 0
    if node.type in ["declaration", "identifier", "number_literal"]:
        return None

    # NPC(if (E1) S1 else S2) = NPC(E1) + NPC(S1) + NPC(S2)  // if statement: in case of no else, NPC(S2) = 1
    if node.type == "if_statement":
        condition_clause = node.child_by_field_name("condition")
        compound_statement = node.child_by_field_name("consequence")
        else_clause = node.child_by_field_name("alternative")
        if else_clause is None:
            return SPC_E(condition_clause) + SPC_S( compound_statement ) + 1
        else:
            return SPC_E(condition_clause) + SPC_S( compound_statement ) + SPC_S( else_clause )

    # NPC(while (E1) S1) = 1 + NPC(E1) + NPC(S1)  // while statement
    if node.type == "while_statement":
        print(node.sexp())
        condition_clause = node.child_by_field_name("condition")
        compound_statement = node.child_by_field_name("body")
        return 1 + SPC_E(condition_clause) + SPC_S( compound_statement )

    # NPC(do S1 while (E1)) = 1 + NPC(E1) + NPC(S1)  // do-while statement
    if node.type == "do_statement":
        print(node.sexp())
        s_do, compound_statement, s_while, expression, semi = node.children
        return 1 + SPC( compound_statement ) + SPC_E(expression)

    # NPC(switch (C1) { case E1: S1; case E2: S2; ... case En; Sn; }) = SUM(i = 1..n | NPC(Si))  // switch statement
    if node.type == "switch_statement":
        condition_clause = node.child_by_field_name("condition")
        compound_statement = node.child_by_field_name("body")
        cases = [n for n in compound_statement.children if n.type == "case_statement"]
        return SPC_E(condition_clause) + sum(SPC(case) for case in cases)

    # NPC(for(E1; E2; E3) S1) = 1 + NPC(E1) + NPC(E2) + NPC(E3) + NPC(S1)  // for statement
    if node.type == "for_statement":
        s_initializer = node.child_by_field_name("initializer")
        s_condition = node.child_by_field_name("condition")
        s_update = node.child_by_field_name("update")
        body = node.child_by_field_name("body")
        return 1 + SPC_E(s_initializer) + SPC_E(s_condition) + SPC_E(s_update) + SPC(body)

    if node.type == "for_range_loop":
        body = node.child_by_field_name("body")
        return 1 + SPC(body)

    # NPC(S1; S2) = NPC(S1) * NPC(S2)  // sequential statements
    if node.type == "compound_statement":
        print(node.sexp())
        total = 1
        for child in node.children:
            total *= SPC_S(child)
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
