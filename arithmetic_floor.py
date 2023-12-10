import ast
from help_strings import EXCEPTION_HELP
from help_strings import ARITHMETIC_HELP as HELP_STRING


def generate(tree):
    output_code = ""
    for node in tree.body:
        output_code += eval_node(node)

    return output_code


def assign_expr_check(expr):
    if isinstance(expr, ast.Tuple):
        return_val = "("
        for element in expr.elts:
            return_val += assign_expr_check(element) + ", "
        return_val = return_val[:-2] + ")"
        return return_val
    else:
        return expr_check(expr)


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
        elif isinstance(expr.op, ast.Mod):
            return_val += expr_check(expr.left) + \
                " % " + expr_check(expr.right)
        elif isinstance(expr.op, ast.Pow):
            return_val += expr_check(expr.left) + \
                " ** " + expr_check(expr.right)
        elif isinstance(expr.op, ast.Div):
            expr_left = expr_check(expr.left)
            expr_right = expr_check(expr.right)
            if int(float(expr_left)) == float(expr_left) and int(float(expr_right)) == float(expr_right):
                return_val += expr_left + " // " + expr_right
            else:
                return_val += expr_left + " / " + expr_right
        else:
            raise ValueError(EXCEPTION_HELP)

    elif isinstance(expr, ast.UnaryOp):
        if isinstance(expr.op, ast.USub):
            return_val = "-" + expr_check(expr.operand)
        elif isinstance(expr.op, ast.UAdd):
            return_val = "+" + expr_check(expr.operand)
        else:
            raise ValueError(EXCEPTION_HELP)

    elif isinstance(expr, ast.Call):
        args = [expr_check(arg) for arg in expr.args]

        if expr.func.id == "help":
            return_val = f'print("""{HELP_STRING}""")'

        elif expr.func.id == "print":
            return_val = f"print({', '.join(args)})"

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
            else:
                raise ValueError(EXCEPTION_HELP)
            return_val += " " + op_symbol + " " + expr_check(val)
    else:
        raise ValueError(EXCEPTION_HELP)

    return return_val


def eval_node(node):
    current_line = ""
    if isinstance(node, ast.Expr):
        current_line += expr_check(node.value)
    # Broaden to Control Flow Stuff

    elif isinstance(node, ast.Assign):
        for target in node.targets:
            current_line += assign_expr_check(target)
        current_line += " = " + assign_expr_check(node.value)

    elif isinstance(node, ast.AugAssign):
        current_line += expr_check(target)
        current_line += " " + \
            expr_check(node.op) + "= " + expr_check(node.value)
    else:
        raise ValueError(EXCEPTION_HELP)

    current_line += "\n"
    return current_line
