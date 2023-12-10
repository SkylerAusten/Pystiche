from math import isnan


def ruby_truth(value=False):
    """Ruby truthiness."""
    if value is False:
        return False
    elif value is None:
        return False
    else:
        return True


def ocaml_truth(value=False, if_expr=False):
    """OCaml truthiness."""
    value_type = type(value)

    if value_type is bool:
        return value

    else:
        type_str = ""
        if value is None:
            type_str = "option"
        elif value_type is int:
            type_str = "int"
        elif value_type is float:
            type_str = "float"
        elif value_type is str:
            type_str = "string"
        elif value_type is list:
            type_str = "list"
        elif value_type is dict:
            type_str = "dict"
        elif value_type is tuple:
            type_str = "tuple"
        elif value_type is bytes:
            type_str = "bytes"
        else:
            type_str = "unknown"

        if if_expr:
            raise TypeError(
                "If error: This expression has type " + type_str + " but an expression was expected of type bool because it is in the condition of an if-statement")
        else:
            raise TypeError(
                "Error: This expression has type " + type_str + " but an expression was expected of type bool")


def perl_truth(value=False):
    """Perl truthiness."""
    if value is False:
        return False
    if value == 0:
        return False
    elif value == "":
        return False
    elif value is None:
        return False
    elif value == "0":
        return False
    else:
        return True


def js_truth(value=False):
    """JavaScript truthiness."""
    if value is False:
        return False
    if value == 0:
        return False
    elif value == "":
        return False
    elif isnan(value):
        return False
    elif value is None:
        return False
    else:
        return True


def php_truth(value=False):
    """PHP truthiness."""
    if value is False:
        return False
    if value == 0:
        return False
    elif value == "":
        return False
    elif value == "0":
        return False
    elif value is []:
        return False
    elif value is None:
        return False
    else:
        return True


def python_truth(value=False):
    """Python truthiness."""
    return bool(value)


def ruby_and(values):
    for value in values:
        if ruby_truth(value) == False:
            return value
    return values[-1]


def ruby_or(values):
    for value in values:
        if ruby_truth(value) == True:
            return value
    return values[-1]


def perl_and(values):
    for value in values:
        if perl_truth(value) == False:
            return value
    return values[-1]


def perl_or(values):
    for value in values:
        if perl_truth(value) == True:
            return value
    return values[-1]


def ocaml_and(values):
    for value in values:
        if ocaml_truth(value) == False:
            return value
    return values[-1]


def ocaml_or(values):
    for value in values:
        if ocaml_truth(value) == True:
            return value
    return values[-1]
