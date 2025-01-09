from flask import Flask, request, jsonify
from flask_cors import CORS
from lexer import run

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/run', methods=['POST'])
def run_lexer():
    data = request.json
    text = data.get('text', '')
    tokens, errors = run(text)  # Call run with text and default fn
    if errors:
        error_messages = [f"Error {i+1}: {error.as_string()}" for i, error in enumerate(errors)]
        print(f"{error_messages}\n\n")  # Print the errors for debugging
        return jsonify({'errors': error_messages}), 400
    token_list = [{'type': token.type, 'value': token.value} for token in tokens]
    return jsonify({'tokens': token_list})

if __name__ == '__main__':
    app.run(debug=True)