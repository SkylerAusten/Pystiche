import ast
from flask import Flask, render_template, request, jsonify
from lang_router import generate
from execute_code import execute_code

app = Flask(__name__)


@app.route('/challenge/<name>')
def challenge_router(name):
    """Renders the challenge pages."""
    match name:
        case 'eval_order' | 'eval' | 'scope':
            outputs = 2
        case 'arithmetic' | 'strings' | 'fields' | 'loops' | 'function_calls' | 'variable_mutation' | 'object_mutation':
            outputs = 3
        case 'conditionals':
            outputs = 4
        case _:
            return render_template('not_found.html')
    return render_template('challenge.html', challenge_name=name, outputs=outputs)


@app.errorhandler(404)
def not_found(e):
    """Renders the error 404 page."""
    return render_template('not_found.html')


@app.route('/')
def index():
    """Renders the index page."""
    return render_template('index.html')


@app.route('/execute/<name>', methods=['POST'])
def execute(name: str) -> str:
    """Executes the code from the website form and returns the results as a JSON object."""
    # Grab input code
    input_code = request.form['code']

    try:
        if name == "fields":
            pass

        # Parse the input code into AST
        input_ast = ast.parse(input_code)

        # Generate challenge's 2-4 output codes
        output_codes = generate(input_ast, name)
        print(output_codes)

        # Execute the output codes
        outputs = execute_code(output_codes)

    except Exception as e:
        outputs = [f"<pre>{str(e)}</pre>"] * 4

    return jsonify(outputs)


if __name__ == '__main__':
    app.run(debug=True)
