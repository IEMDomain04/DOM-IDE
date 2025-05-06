from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.lexer import run as lexer
from backend.syntax import parse_run as syntax
from backend.semantic import semantic_run as semantic
from backend.interpreter import interpreter_run as interpreter
from backend.interpreter import CodeRunner
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")  # enable CORS for WS

@app.route('/api/lexer', methods=['POST'])
def run_lexer():
    data = request.json
    text = data.get('text', '')
    tokens, errors = lexer(text)  # Call run with text and default fn
    if errors:  
        error_messages = [f"Error {i+1}: {error.as_string()}\n" for i, error in enumerate(errors)]
        error_pos = [{'idx_start': error.pos_start.idx, 'ln_start': error.pos_start.ln, 'col_start': error.pos_start.col,
                      'idx_end': error.pos_end.idx, 'ln_end': error.pos_end.ln, 'col_end': error.pos_end.col} for error in errors]
        error_pos = [{'idx_start': error.pos_start.idx, 'ln_start': error.pos_start.ln, 'col_start': error.pos_start.col,
                      'idx_end': error.pos_end.idx, 'ln_end': error.pos_end.ln, 'col_end': error.pos_end.col} for error in errors]
        token_list = [{'type': token.type, 'value': token.value} for token in tokens]
        return jsonify({'tokens': token_list, 'errors': error_messages, 'error_pos': error_pos})
        return jsonify({'tokens': token_list, 'errors': error_messages, 'error_pos': error_pos})
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
        syntax_error_message = f"{syntax_error.as_string()}"
        error_pos = {'idx_start': syntax_error.pos_start.idx, 'ln_start': syntax_error.pos_start.ln, 'col_start': syntax_error.pos_start.col,
                     'idx_end': syntax_error.pos_end.idx, 'ln_end': syntax_error.pos_end.ln, 'col_end': syntax_error.pos_end.col}
        return jsonify({'result': syntax_result, 'error': syntax_error_message, 'error_pos': error_pos})
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
    
    ast, errors, tree_str, symbol_table = semantic(tokens)
    if errors:  
        error_messages = [f"Error {i+1}: {error.as_string()}\n" for i, error in enumerate(errors)]
        error_pos = [{'idx_start': error.pos_start.idx, 'ln_start': error.pos_start.ln, 'col_start': error.pos_start.col,
                      'idx_end': error.pos_end.idx, 'ln_end': error.pos_end.ln, 'col_end': error.pos_end.col} for error in errors]
        return jsonify({'semantic_result': "AST Building Failed", 'errors': error_messages, 'tree_str': tree_str, 'error_pos': error_pos})
    
    if ast:
        return jsonify({'semantic_result': "Successful from Semantic Analyzer", 'errors': None, 'tree_str': tree_str})
    return jsonify({'semantic_result': "No AST Built", 'errors': None, 'tree_str': tree_str})

@app.route('/api/interpreter', methods=['POST'])
def run_interpreter():
    data = request.json
    text = data.get('text', '')
    tokens, lexer_errors = lexer(text)
    if lexer_errors:  
        return jsonify({'result': "Error: Failure from Interpreter\nFile: <stdin>, Message: Check lexical analysis.", 'error': None})
    syntax_result, syntax_error = syntax(tokens)
    if syntax_error:
        error_messages = f"{syntax_error.as_string()}"
        error_pos = {'idx_start': syntax_error.pos_start.idx, 'ln_start': syntax_error.pos_start.ln, 'col_start': syntax_error.pos_start.col,
                        'idx_end': syntax_error.pos_end.idx, 'ln_end': syntax_error.pos_end.ln, 'col_end': syntax_error.pos_end.col}
        return jsonify({'result': "Error: Failure from Interpreter\nFile: <stdin>, Message: Check syntax analysis.", 'error': error_messages, 'error_pos': error_pos})
    ast, semantic_errors, tree_str, symbol_table = semantic(tokens)
    if semantic_errors:  
        error_messages = [f"Error {i+1}: {error.as_string()}\n" for i, error in enumerate(semantic_errors)]
        error_pos = [{'idx_start': error.pos_start.idx, 'ln_start': error.pos_start.ln, 'col_start': error.pos_start.col,
                        'idx_end': error.pos_end.idx, 'ln_end': error.pos_end.ln, 'col_end': error.pos_end.col} for error in semantic_errors]
        return jsonify({'result': "Error: Failure from Interpreter", 'error': error_messages, 'error_pos': error_pos})
    if ast:
        global runner
        runner = CodeRunner(symbol_table, socketio=socketio) 
        runner.visit(ast)  
        output = runner.output
        error = runner.error
        if error:
            error_message = [f"Error: {error.as_string()}\n"]
            error_pos = {'idx_start': error.pos_start.idx, 'ln_start': error.pos_start.ln, 'col_start': error.pos_start.col,
                            'idx_end': error.pos_end.idx, 'ln_end': error.pos_end.ln, 'col_end': error.pos_end.col}
            return jsonify({'result': output, 'error': error_message, 'error_pos': error_pos})
        if output:
            output_messages = "".join(output)
            return jsonify({'result': output_messages, 'error': None})
        return jsonify({'result': "No Output", 'error': None})
    return jsonify({'result': "No Output", 'error': None})
        

@socketio.on('capture_input')
def handle_capture_input(data):
    var_name = data.get('var_name')
    user_input = data.get('input')

    if var_name and user_input is not None:
        socketio.emit('output_update', {'output': user_input + "\n"})
        
        runner.provide_input(var_name, user_input)
        
        emit('input_received', {
            'var_name': var_name,
            'input': user_input
        })

if __name__ == '__main__':
    socketio.run(app, debug=True)
