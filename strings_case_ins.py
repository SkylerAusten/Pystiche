import ast
from help_strings import EXCEPTION_HELP
from help_strings import STRINGS_HELP as HELP_STRING


def generate(tree):
    output_code = ""
    output_code += """def case_insensitive_compare(str1, str2):
    return str1.lower() == str2.lower()\n"""
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

    elif isinstance(expr, ast.Call):
        args = [expr_check(arg) for arg in expr.args]

        if expr.func.id == "help":
            return_val = f'print("""{HELP_STRING}""")'

        elif expr.func.id == "print":
            return_val = f"print({', '.join(args)})"

        else:
            raise ValueError(EXCEPTION_HELP)

    elif isinstance(expr, ast.UnaryOp):
        if isinstance(expr.op, ast.USub):
            return_val = "-" + expr_check(expr.operand)
        elif isinstance(expr.op, ast.UAdd):
            return_val = "+" + expr_check(expr.operand)
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
        left_expr = expr_check(expr.left)
        comparisons = []
        for op, right_expr in zip(expr.ops, expr.comparators):
            if isinstance(op, ast.Eq) or isinstance(op, ast.NotEq):
                # Check if both sides are strings before using the helper function
                if isinstance(expr.left, ast.Str) and isinstance(right_expr, ast.Str):
                    comp_method = "case_insensitive_compare"
                    if isinstance(op, ast.NotEq):
                        comp_method = "not " + comp_method
                    comparisons.append(
                        f"{comp_method}({left_expr}, {expr_check(right_expr)})")
                    continue
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
            # return_val += " " + op_symbol + " " + expr_check(val)
            comparisons.append(
                f"{left_expr} {op_symbol} {expr_check(right_expr)}")
            return_val += ' and '.join(comparisons)

        return ' and '.join(comparisons)
    elif isinstance(expr, ast.Subscript):
        return_val += expr_check(expr.value) + "[" + \
            expr_check(expr.slice) + "]"
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


def eval_node(node):
    current_line = ""
    if isinstance(node, ast.Expr):
        current_line += expr_check(node.value)
    # Broaden to Control Flow Stuff

    elif isinstance(node, ast.Assign):
        for target in node.targets:
            current_line += assign_expr_check(target)
        current_line += " = " + assign_expr_check(node.value)
    else:
        raise ValueError(EXCEPTION_HELP)

    current_line += "\n"
    return current_line
