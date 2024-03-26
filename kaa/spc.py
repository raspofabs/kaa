from pathlib import Path
from kaa import read_source, parse_source_to_tree
from kaa import get_functions, render_func

def debug_node(node):
    print(f"Node:{node.type}/{node.id}/{node.grammar_name} -> {node.sexp()}")
    cursor = node.walk()
    if cursor.goto_first_child():
        more = True
        while more:
            print(f"Child: {cursor.node.type}/{cursor.field_name}")
            more = cursor.goto_next_sibling()

def non_comment(nodes):
    return filter(lambda x: x.type != "comment", nodes)

def non_comma(nodes):
    return filter(lambda x: x.type != ",", nodes)

def non_comment_children(node):
    return non_comment(node.children)

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
        #debug_node(node)
        body = node.child_by_field_name("body")
        assert body.type == "compound_statement"
        return SPC(body)

    if node.type == "return_statement":
        #debug_node(node)
        r, expression, semicolon = non_comment_children(node)
        return SPC(expression)

    if node.type == "case_statement":
        case, *tail = non_comment_children(node)
        if case.type == "case":
            s_literal, s_col, *statement = tail
            if len(statement):
                return SPC_S(statement[0])
            else:
                return 0
        else:
            assert case.type == "default"
            s_col, *statement = tail
            # we already account for an empty default, so if we have one, subtract one from the SPC
            if len(statement):
                return SPC_S(statement[0]) - 1
            else:
                return 0

    if node.type == "condition_clause":
        #debug_node(node)
        e_exp = node.child_by_field_name("value")
        return SPC(e_exp)

    if node.type == "else_clause":
        #debug_node(node)
        s_else, s_statement = non_comment_children(node)
        return SPC(s_statement)

    if node.type == "parenthesized_expression":
        #debug_node(node)
        l_paren, e_exp, r_paren = non_comment_children(node)
        return SPC_E(e_exp)

    if node.type in ["field_expression"]:
        return None

    if node.type == "call_expression":
        debug_node(node)
        e_arguments = node.child_by_field_name("arguments")
        return SPC_E(e_arguments)

    if node.type == "argument_list":
        debug_node(node)
        s_open, *e_arguments, s_close = non_comma(non_comment_children(node))
        return sum(map(SPC_E, e_arguments))

    if node.type == "subscript_expression":
        #debug_node(node)
        e_argument = node.child_by_field_name("argument")
        e_index = node.child_by_field_name("indices")
        return SPC_E(e_argument) + SPC_E(e_index)

    if node.type == "subscript_argument_list":
        debug_node(node)
        s_open, e_index, s_close = non_comment_children(node)
        assert e_index is not None
        return SPC_E(e_index)

    if node.type == "binary_expression":
        e_left = node.child_by_field_name("left")
        s_op = node.child_by_field_name("operator")
        e_right = node.child_by_field_name("right")
        return SPC_E(e_left) + OPCOST(s_op) + SPC_E(e_right)

    # NPC(E1 ? E2 : E3) = 2 + NPC(E1) + NPC(E2) + NPC(E3)  // conditional operator
    if node.type == "conditional_expression":
        e_condition = node.child_by_field_name("condition")
        e_left = node.child_by_field_name("consequence")
        e_right = node.child_by_field_name("alternative")
        return 2 + SPC_E(e_condition) + SPC_E(e_left) + SPC_E(e_right)

    #sum(1 for c in node.children if c.type in ["&&", "||"])
    if node.type == "update_expression":
        return 0

    if node.type in ["declaration", "identifier", "number_literal", "string_literal"]:
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
        condition_clause = node.child_by_field_name("condition")
        compound_statement = node.child_by_field_name("body")
        return 1 + SPC_E(condition_clause) + SPC_S( compound_statement )

    # NPC(do S1 while (E1)) = 1 + NPC(E1) + NPC(S1)  // do-while statement
    if node.type == "do_statement":
        e_condition = node.child_by_field_name("condition")
        s_body = node.child_by_field_name("body")
        return 1 + SPC(s_body) + SPC_E(e_condition)

    # NPC(switch (C1) { case E1: S1; case E2: S2; ... case En; Sn; }) = SUM(i = 1..n | NPC(Si))  // switch statement
    # The above is wrong as it ignores the condition. 
    # It's SPC(Condition) + sum(SPC(x) for x in cases (including implicit default))
    if node.type == "switch_statement":
        condition_clause = node.child_by_field_name("condition")
        compound_statement = node.child_by_field_name("body")
        cases = [n for n in compound_statement.children if n.type == "case_statement"]
        # even if there is no explicit default, we can end up there, so always
        # count it (this is wrong in some cases, such as when all possible
        # values are branched upon, such as when you use switch(value&3) and
        # provide all four cases
        return SPC_E(condition_clause) + sum(map(SPC, cases)) + 1

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
        #debug_node(node)
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
