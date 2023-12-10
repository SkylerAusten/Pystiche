import arithmetic_fracs
import arithmetic_normal
import arithmetic_floor
import strings_normal
import strings_space
import strings_case_ins
import conditionals_python
import conditionals_perl
import conditionals_ocaml
import conditionals_ruby

import ast


def generate(input_ast, name):
    output_codes = []
    print(ast.dump(input_ast, indent=4))
    match name:
        case 'eval_order':
            # code = parse(code)
            output_codes += "f"
        case 'eval':
            output_codes += "f"
        case 'scope':
            output_codes += "f"
        case 'arithmetic':
            output_codes += [arithmetic_normal.generate(input_ast)]
            output_codes += [arithmetic_fracs.generate(input_ast)]
            output_codes += [arithmetic_floor.generate(input_ast)]
        case 'strings':
            output_codes += [strings_space.generate(input_ast)]
            output_codes += [strings_normal.generate(input_ast)]
            output_codes += [strings_case_ins.generate(input_ast)]
        case 'fields':
            output_codes += "f"
        case 'loops':
            output_codes += "f"
        case 'function_calls':
            output_codes += "f"
        case 'variable_mutation':
            output_codes += "f"
        case 'object_mutation':
            output_codes += "f"
        case 'conditionals':
            output_codes += [conditionals_python.generate(input_ast)]
            output_codes += [conditionals_ruby.generate(input_ast)]
            output_codes += [conditionals_perl.generate(input_ast)]
            output_codes += [conditionals_ocaml.generate(input_ast)]

    return output_codes
