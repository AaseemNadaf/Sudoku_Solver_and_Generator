import tkinter as tk
from tkinter import messagebox
import time
from sudoku_logic import solve, generate_puzzle

# --- Constants ---
GRID_SIZE = 9
DEFAULT_DIFFICULTY = 50
WINDOW_SIZE = "1920x1080"

# --- Fonts ---
TITLE_FONT = ('Arial', 28, 'bold')
GRID_FONT = ('Arial', 24, 'bold')
BUTTON_FONT = ('Arial', 14)

# --- Theme Palettes ---
LIGHT_THEME = {
    "bg": "#F5F5F5", "title": "#333333", "grid_lines": "#BBBBBB",
    "cell_bg_1": "#FFFFFF", "cell_bg_2": "#F0F0F0", "highlight": "#D0E0FF",
    "original_num": "#000000", "new_num": "#0000A0", "button": "#4A90E2",
    "button_text": "#FFFFFF", "button_hover": "#357ABD"
}
DARK_THEME = {
    "bg": "#121212", "title": "#E0E0E0", "grid_lines": "#444444",
    "cell_bg_1": "#1E1E1E", "cell_bg_2": "#242424", "highlight": "#3A3A3A",
    "original_num": "#FFFFFF", "new_num": "#87CEFA", "button": "#333333",
    "button_text": "#FFFFFF", "button_hover": "#555555"
}

class SudokuGUI:
    """Manages the Sudoku application's GUI, state, and user interactions."""
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver & Generator")
        self.root.geometry(WINDOW_SIZE)

        self.original_puzzle_cells = set()
        self.is_dark_mode = False
        self.theme = LIGHT_THEME
        self.cells = {}
        self.buttons = {}
        
        self._setup_ui()
        self._apply_theme()
        self.generate_new_puzzle()

    def _setup_ui(self):
        """Initializes all UI components."""
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.content_frame = tk.Frame(self.root)
        self.content_frame.grid(row=0, column=0)
        
        self.title_label = tk.Label(self.content_frame, text="Sudoku Solver", font=TITLE_FONT)
        self.title_label.pack(pady=(10, 20))

        self.grid_frame = tk.Frame(self.content_frame)
        self.grid_frame.pack(pady=20)
        self._draw_grid()

        self.button_frame = tk.Frame(self.content_frame)
        self.button_frame.pack(pady=10)
        self._draw_buttons()

    def _validate_input(self, P):
        """Input validation: allow only single digits (1-9) or an empty string."""
        return (P.isdigit() and len(P) <= 1 and P != '0') or P == ""

    def _draw_grid(self):
        vcmd = (self.root.register(self._validate_input), '%P')
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                padx = (3, 0) if col % 3 == 0 else (1, 1)
                pady = (3, 0) if row % 3 == 0 else (1, 1)
                
                entry = tk.Entry(self.grid_frame, width=2, font=GRID_FONT,
                                 justify='center', bd=0, relief='solid',
                                 highlightthickness=0,
                                 validate='key', validatecommand=vcmd)
                entry.grid(row=row, column=col, padx=padx, pady=pady, ipady=5)
                entry.bind("<FocusIn>", self._on_cell_focus)
                self.cells[(row, col)] = entry

    def _draw_buttons(self):
        button_config = {
            "Solve": self.solve_puzzle, "New Puzzle": self.generate_new_puzzle,
            "Clear Board": self.clear_board, "Toggle Mode": self._toggle_mode
        }
        for text, command in button_config.items():
            btn = tk.Button(self.button_frame, text=text, command=command, font=BUTTON_FONT,
                            relief='flat', borderwidth=0, pady=5, padx=15)
            btn.pack(side='left', padx=10, pady=10)
            self.buttons[text] = btn

    def _apply_theme(self):
        self.theme = DARK_THEME if self.is_dark_mode else LIGHT_THEME
        
        self.root.config(bg=self.theme["bg"])
        self.content_frame.config(bg=self.theme["bg"])
        self.title_label.config(bg=self.theme["bg"], fg=self.theme["title"])
        self.grid_frame.config(bg=self.theme["grid_lines"])
        self.button_frame.config(bg=self.theme["bg"])
        
        for widget in self.cells.values():
            widget.config(insertbackground=self.theme['title'])

        for btn in self.buttons.values():
            btn.config(bg=self.theme["button"], fg=self.theme["button_text"],
                       activebackground=self.theme["button_hover"],
                       activeforeground=self.theme["button_text"])
        
        self._update_gui_from_board(self._get_board_from_gui())

    def _toggle_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self._apply_theme()

    def _on_cell_focus(self, event):
        self._clear_highlighting()
        for pos, widget in self.cells.items():
            if widget == event.widget:
                focused_row, focused_col = pos
                break
        else: return

        for i in range(GRID_SIZE):
            self.cells[(focused_row, i)].config(bg=self.theme["highlight"])
            self.cells[(i, focused_col)].config(bg=self.theme["highlight"])

        start_row, start_col = 3 * (focused_row // 3), 3 * (focused_col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                self.cells[(r, c)].config(bg=self.theme["highlight"])

    def _clear_highlighting(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                bg_color = self.theme["cell_bg_1"] if (row // 3 + col // 3) % 2 == 0 else self.theme["cell_bg_2"]
                self.cells[(row, col)].config(bg=bg_color)
    
    def _get_board_from_gui(self):
        board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                try: board[row][col] = int(self.cells[(row, col)].get())
                except ValueError: pass
        return board

    def _update_gui_from_board(self, board):
        self._clear_highlighting()
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                bg_color = self.theme["cell_bg_1"] if (row // 3 + col // 3) % 2 == 0 else self.theme["cell_bg_2"]
                entry = self.cells[(row, col)]
                entry.config(state='normal', readonlybackground=bg_color)
                entry.delete(0, 'end')
                
                if board[row][col] != 0:
                    entry.insert(0, str(board[row][col]))
                    if (row, col) in self.original_puzzle_cells:
                        entry.config(fg=self.theme["original_num"], state='readonly')
                    else: entry.config(fg=self.theme["new_num"])
                else: entry.config(fg=self.theme["new_num"], state='normal')

    def solve_puzzle(self):
        board = self._get_board_from_gui()
        empty_cells = sum(row.count(0) for row in board)
        
        self.original_puzzle_cells.clear()
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if board[r][c] != 0: self.original_puzzle_cells.add((r, c))
        
        start_time = time.time()
        is_solved = solve(board)
        duration = time.time() - start_time
        
        print("\n" + "="*40, "Solver Analysis", "="*40,
              f"Number of empty cells (m): {empty_cells}",
              f"Theoretical Time Complexity: O(9^m) -> O(9^{empty_cells})",
              f"Theoretical Space Complexity: O(m) -> O({empty_cells})",
              f"Actual Execution Time: {duration:.6f} seconds",
              "="*97 + "\n", sep="\n")

        if is_solved: self._update_gui_from_board(board)
        else: messagebox.showerror("Error", "This puzzle is unsolvable.")
            
    def generate_new_puzzle(self):
        self.original_puzzle_cells.clear()
        puzzle = generate_puzzle(DEFAULT_DIFFICULTY)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if puzzle[r][c] != 0: self.original_puzzle_cells.add((r, c))
        self._update_gui_from_board(puzzle)

    def clear_board(self):
        self.original_puzzle_cells.clear()
        empty_board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self._update_gui_from_board(empty_board)

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()