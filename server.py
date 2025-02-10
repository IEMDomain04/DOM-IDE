from flask import Flask, request, jsonify
from flask_cors import CORS
from lexer import run as lexer
from syntax import parse_run as syntax

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/lexer', methods=['POST'])
def run_lexer():
    data = request.json
    text = data.get('text', '')
    tokens, errors = lexer(text)  # Call run with text and default fn
    if errors:  
        error_messages = [f"Error {i+1}: {error.as_string()}" for i, error in enumerate(errors)]
        print(f"{error_messages}\n\n")  # Print the errors for debugging
        token_list = [{'type': token.type, 'value': token.value} for token in tokens]
        return jsonify({'tokens': token_list, 'errors': error_messages})
    token_list = [{'type': token.type, 'value': token.value} for token in tokens]
    return jsonify({'tokens': token_list})

@app.route('/api/syntax', methods=['POST'])
def run_syntax():
    data = request.json
    text = data.get('text', '')
    tokens, lexer_errors = lexer(text)  # Call lexer with text
    if lexer_errors:  
        return jsonify({'syntax_tree': "Failure from Syntax Analyzer"})
    syntax_result, ast = syntax(tokens)  # Call syntax with tokens
    return jsonify({'syntax_tree': syntax_result})

if __name__ == '__main__':
    app.run(debug=True)