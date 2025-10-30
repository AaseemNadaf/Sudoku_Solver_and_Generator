# FILE: app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
# Import the functions from your sudoku_logic.py file
from sudoku_logic import solve, generate_puzzle

app = Flask(__name__)
CORS(app)  # This allows your web-based frontend to talk to your backend

# --- API Routes ---

@app.route('/solve', methods=['POST'])
def solve_api():
    """API route to solve a puzzle."""
    data = request.json
    board = data['board']
    
    # Call your imported solve function
    if solve(board):
        return jsonify({'status': 'success', 'solution': board})
    else:
        return jsonify({'status': 'error', 'message': 'No solution found'})

@app.route('/generate', methods=['GET'])
def generate_api():
    """API route to generate a new puzzle."""
    # Call your imported generate function
    # We can pass a difficulty from the web later if we want.
    # For now, we'll use the default.
    board = generate_puzzle() 
    return jsonify({'board': board})

if __name__ == '__main__':
    app.run(debug=True, port=5000)