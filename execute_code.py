from io import StringIO
from contextlib import redirect_stdout
from fractions import Fraction
from exec_helpers import ruby_and, ruby_or, ruby_truth, perl_and, perl_or, perl_truth, ocaml_truth, ocaml_and, ocaml_or


def execute_code(output_codes: list) -> list[str]:
    """Execute the generated code and return the HTML-rendered outputs in a list."""
    output_html_list = []

    for code in output_codes:
        try:
            io_capture = StringIO()
            with redirect_stdout(io_capture):
                exec(code)
            output = io_capture.getvalue()

            # Use <pre> tag to preserve formatting
            output_html_list.append(f"<pre>{output}</pre>")
        except Exception as e:
            output_html_list.append(f"<pre>{str(e)}</pre>")

    return output_html_list
