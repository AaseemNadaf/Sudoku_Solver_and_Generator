# sudoku_logic.py
import random
from typing import List, Tuple, Optional

# --- Constants ---
GRID_SIZE = 9

Board = List[List[int]]
Position = Tuple[int, int]

def find_empty(board: Board) -> Optional[Position]:
    """Finds the next empty cell (represented by 0) in the board."""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 0:
                return (r, c)
    return None

def is_valid(board: Board, num: int, pos: Position) -> bool:
    """Checks if placing a number in a given position is valid."""
    row, col = pos

    # Check row
    for i in range(GRID_SIZE):
        if board[row][i] == num and col != i:
            return False

    # Check column
    for i in range(GRID_SIZE):
        if board[i][col] == num and row != i:
            return False

    # Check 3x3 box
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

def solve(board: Board) -> bool:
    """Solves a Sudoku board using the backtracking algorithm."""
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num

            if solve(board):
                return True

            board[row][col] = 0

    return False

def generate_puzzle(difficulty: int = 50) -> Board:
    """
    Generates a new, random Sudoku puzzle.
    1. Creates a valid, fully-solved, and random board.
    2. Removes a number of cells based on difficulty.
    """
    board: Board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # --- KEY CHANGE FOR RANDOMIZATION ---
    # To create a different puzzle each time, we need to solve a randomized board.
    # A common and effective method is to fill the diagonal 3x3 boxes first,
    # as they do not interact with each other.

    numbers = list(range(1, GRID_SIZE + 1))
    
    # Fill the three diagonal 3x3 boxes
    for i in range(0, GRID_SIZE, 3):
        random.shuffle(numbers)
        for r in range(3):
            for c in range(3):
                board[i + r][i + c] = numbers[r * 3 + c]
    
    # Now, solve this partially-filled board. Because the seed is random,
    # the resulting solved board will also be random.
    solve(board)
    
    # Remove cells to create the puzzle, same as before
    cells_to_remove = difficulty
    while cells_to_remove > 0:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if board[row][col] != 0:
            board[row][col] = 0
            cells_to_remove -= 1
            
    return board