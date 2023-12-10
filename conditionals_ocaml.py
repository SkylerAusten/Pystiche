import ast
from help_strings import EXCEPTION_HELP
from help_strings import CONDITIONALS_HELP as HELP_STRING


def generate(tree):
    output_code = ""
    for node in tree.body:
        output_code += eval_node(node, 1)

    return output_code


def expr_check(expr):
    """Turn a specific expression into a code string."""
    return_val = ""

    if isinstance(expr, ast.BinOp):
        if isinstance(expr.op, ast.Add):
            return_val += expr_check(expr.left) + \
                " + " + expr_check(expr.right)
        elif isinstance(expr.op, ast.Sub):
            return_val += expr_check(expr.left) + \
                " - " + expr_check(expr.right)
        elif isinstance(expr.op, ast.Mult):
            return_val += expr_check(expr.left) + \
                " * " + expr_check(expr.right)
        elif isinstance(expr.op, ast.Div):
            return_val += expr_check(expr.left) + \
                " / " + expr_check(expr.right)
        elif isinstance(expr.op, ast.Mod):
            return_val += expr_check(expr.left) + \
                " % " + expr_check(expr.right)
        elif isinstance(expr.op, ast.Pow):
            return_val += expr_check(expr.left) + \
                " ** " + expr_check(expr.right)
        else:
            raise ValueError(EXCEPTION_HELP)

    elif isinstance(expr, ast.UnaryOp):
        if isinstance(expr.op, ast.Not):
            return_val += "not " + \
                "ocaml_truth(" + expr_check(expr.operand) + ")"
        elif isinstance(expr.op, ast.USub):
            return_val = "-" + expr_check(expr.operand)
        elif isinstance(expr.op, ast.UAdd):
            return_val = "+" + expr_check(expr.operand)
        else:
            raise ValueError(EXCEPTION_HELP)

    elif isinstance(expr, ast.Call):
        args = [expr_check(arg) for arg in expr.args]

        print("ID", expr.func.id)

        if expr.func.id == "help":
            return_val = f'print("""{HELP_STRING}""")'

        elif expr.func.id == "print":
            return_val = f"print({', '.join(args)})"

        elif expr.func.id == "bool":
            return_val = "ocaml_truth(" + expr_check(expr.args[0]) + ")"

        else:
            raise ValueError(EXCEPTION_HELP)

    elif isinstance(expr, ast.BoolOp):
        values = [expr_check(value) for value in expr.values]

        if isinstance(expr.op, ast.And):
            # op_symbol = " and "
            # return_val += op_symbol.join(values)
            return_val += "ocaml_and([" + ", ".join(values) + "])"
        elif isinstance(expr.op, ast.Or):
            return_val += "ocaml_or([" + ", ".join(values) + "])"
        else:
            raise ValueError(EXCEPTION_HELP)
    elif isinstance(expr, ast.Constant):
        if isinstance(expr.value, str):
            # Check if the string is multi-line
            if '\n' in expr.value:
                # Use triple quotes for multi-line strings
                triple_quoted_string = '"""' + \
                    expr.value.replace('"""', '\\"""') + '"""'
                return_val += triple_quoted_string
            else:
                # Properly escape single quotes in single-line strings
                escaped_string = expr.value.replace("'", "\\'")
                return_val += f"'{escaped_string}'"
        else:
            return_val += str(expr.value)

    elif isinstance(expr, ast.Subscript):
        return_val += expr_check(expr.value) + "[" + \
            expr_check(expr.slice) + "]"

    elif isinstance(expr, ast.List):
        return_val += "[" + ", ".join([expr_check(elt)
                                      for elt in expr.elts]) + "]"

    elif isinstance(expr, ast.Dict):
        return_val += "{" + ", ".join([expr_check(key) + ": " + expr_check(value)
                                       for key, value in zip(expr.keys, expr.values)]) + "}"

    elif isinstance(expr, ast.Tuple):
        return_val += "(" + ", ".join([expr_check(elt)
                                      for elt in expr.elts]) + ")"

    elif isinstance(expr, ast.Name):
        return_val += str(expr.id)
    elif isinstance(expr, ast.Compare):
        return_val += expr_check(expr.left)
        for op, val in zip(expr.ops, expr.comparators):
            op_symbol = ""
            if isinstance(op, ast.Eq):
                op_symbol = "=="
            elif isinstance(op, ast.NotEq):
                op_symbol = "!="
            elif isinstance(op, ast.Lt):
                op_symbol = "<"
            elif isinstance(op, ast.LtE):
                op_symbol = "<="
            elif isinstance(op, ast.Gt):
                op_symbol = ">"
            elif isinstance(op, ast.GtE):
                op_symbol = ">="
            elif isinstance(op, ast.Is):
                op_symbol = "is"
            elif isinstance(op, ast.IsNot):
                op_symbol = "is not"
            elif isinstance(op, ast.In):
                op_symbol = "in"
            elif isinstance(op, ast.NotIn):
                op_symbol = "not in"
            else:
                raise ValueError(EXCEPTION_HELP)
            return_val += " " + op_symbol + " " + expr_check(val)
    elif isinstance(expr, ast.Slice):
        if expr.lower is not None:
            return_val += expr_check(expr.lower)
        return_val += ":"
        if expr.upper is not None:
            return_val += expr_check(expr.upper)
        if expr.step is not None:
            return_val += ":" + expr_check(expr.step)
    else:
        raise ValueError(EXCEPTION_HELP)

    return return_val


def eval_node(node, indent_level):
    current_line = ""
    if isinstance(node, ast.Expr):
        current_line += expr_check(node.value)
    # Broaden to Control Flow Stuff

    elif isinstance(node, ast.Assign):
        for target in node.targets:
            current_line += expr_check(target)
        current_line += " = " + expr_check(node.value)

    elif isinstance(node, ast.If):
        current_line += "if(" + \
            "ocaml_truth(" + expr_check(node.test) + ")):\n"

        for body_node in node.body:
            current_line += "\t" * indent_level + \
                eval_node(body_node, indent_level + 1)

        if len(node.orelse) > 0:
            current_line += "\t" * (indent_level - 1) + "else:\n"

            for body_node in node.orelse:
                current_line += "\t" * indent_level + \
                    eval_node(body_node, indent_level + 1)
    else:
        raise ValueError(EXCEPTION_HELP)

    current_line += "\n"
    return current_line
