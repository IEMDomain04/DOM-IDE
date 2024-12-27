from flask import Flask, request, jsonify
from flask_cors import CORS
from lexer import run

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/run', methods=['POST'])
def run_lexer():
    data = request.json
    text = data.get('text', '')
    tokens, error = run(text)  # Call run with text and default fn
    if error:
        print(f"Error: {error.as_string()}")  # Print the error for debugging
        return jsonify({'error': error.as_string()}), 400
    token_list = [{'type': token.type, 'value': token.value} for token in tokens]
    return jsonify({'tokens': token_list})

if __name__ == '__main__':
    app.run(debug=True)