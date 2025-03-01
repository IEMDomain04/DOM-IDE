from flask import Flask, request, jsonify
from flask_cors import CORS
from lexer import run as lexer
from syntax import parse_run as syntax
from semantic import semantic_run as semantic

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/lexer', methods=['POST'])
def run_lexer():
    data = request.json
    text = data.get('text', '')
    tokens, errors = lexer(text)  # Call run with text and default fn
    if errors:  
        error_messages = [f"Error {i+1}: {error.as_string()}\n" for i, error in enumerate(errors)]
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
        return jsonify({'result': "Error: Failure from Syntax Analyzer\nFile: <stdin>, Message: Check lexical analysis.", 'error': None})
    syntax_result, syntax_error = syntax(tokens)
    if syntax_error:
        return jsonify({'result': syntax_result, 'error': syntax_error})
    return jsonify({'result': syntax_result, 'error': None})

@app.route('/api/semantic', methods=['POST'])
def run_semantic():
    data = request.json
    text = data.get('text', '')
    tokens, lexer_errors = lexer(text)
    if lexer_errors:  
        return jsonify({'semantic_result': "Error: Failure from Semantic Analyzer\nFile: <stdin>, Message: Check lexical analysis.", 'errors': None})
    syntax_result, syntax_error = syntax(tokens)

    if syntax_error:
        return jsonify({'semantic_result': "Error: Failure from Semantic Analyzer\nFile: <stdin>, Message: Check syntax analysis.", 'errors': None})
    
    ast, errors = semantic(tokens)
    if errors:  
        error_messages = [f"Error {i+1}: {error.as_string()}\n" for i, error in enumerate(errors)]
        return jsonify({'semantic_result': "AST Building Failed", 'errors': error_messages})
    if ast:
        return jsonify({'semantic_result': "Successful from Semantic Analyzer", 'errors': None})
    return jsonify({'semantic_result': "No AST Built", 'errors': None})

if __name__ == '__main__':
    app.run(debug=True)