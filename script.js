document.addEventListener('DOMContentLoaded', () => {
    const boardElement = document.getElementById('sudoku-board');
    const solveBtn = document.getElementById('solve-btn');
    const generateBtn = document.getElementById('generate-btn');
    const clearBtn = document.getElementById('clear-btn');
    const cells = []; // We will store all cell elements here

    const flaskApiUrl = 'http://127.0.0.1:5000';

    // ADDED: Global variable for the timer
    let timerInterval = null;

    // --- Create the Board ---
    function createBoard() {
        boardElement.innerHTML = ''; // Clear old board
        cells.length = 0; // Clear cells array
        for (let r = 0; r < 9; r++) {
            for (let c = 0; c < 9; c++) {
                const cell = document.createElement('input');
                cell.type = 'text';
                cell.maxLength = 1;
                cell.classList.add('cell');
                
                // Store row/col on the element for easy access
                cell.dataset.row = r;
                cell.dataset.col = c;
                
                // UPDATED: This event listener now also handles error checking
                cell.addEventListener('input', (e) => {
                    // Only allow numbers 1-9
                    e.target.value = e.target.value.replace(/[^1-9]/g, '');
                    
                    // ADDED: Real-time error checking
                    const num = e.target.value;
                    const r = parseInt(e.target.dataset.row);
                    const c_col = parseInt(e.target.dataset.col);
                    const board = getBoardData(); // Get current board state
                    
                    // Check if the move is valid
                    if (num !== '' && !isMoveValid(board, r, c_col, num)) {
                        e.target.classList.add('error');
                    } else {
                        e.target.classList.remove('error');
                    }
                    
                    // Re-run highlight logic on input
                    handleCellClick(e); 
                });
                
                // Add click listener for highlighting
                cell.addEventListener('click', handleCellClick);
                
                boardElement.appendChild(cell);
                cells.push(cell);
            }
        }
    }

    // --- NEW: Highlight Handler ---
    /**
     * Handles highlighting the board based on the selected cell.
     */
    function handleCellClick(event) {
        const selectedCell = event.target;
        if (!selectedCell) return;

        const row = parseInt(selectedCell.dataset.row);
        const col = parseInt(selectedCell.dataset.col);
        const selectedValue = selectedCell.value;

        // Calculate 3x3 box
        const boxRow = Math.floor(row / 3);
        const boxCol = Math.floor(col / 3);

        // Remove all old highlights
        cells.forEach(c => {
            c.classList.remove('selected', 'highlight', 'same-value');
        });

        // Add new highlights
        selectedCell.classList.add('selected');

        cells.forEach((c) => {
            const r = parseInt(c.dataset.row);
            const c_col = parseInt(c.dataset.col);
            const c_boxRow = Math.floor(r / 3);
            const c_boxCol = Math.floor(c_col / 3);

            // Highlight row, col, and box
            if (r === row || c_col === col || (c_boxRow === boxRow && c_boxCol === boxCol)) {
                c.classList.add('highlight');
            }

            // Highlight cells with the same value (if a value exists)
            if (selectedValue !== '' && c.value === selectedValue) {
                // Don't highlight error cells as "same-value"
                if (!c.classList.contains('error')) {
                    c.classList.add('same-value');
                }
            }
        });
    }

    // --- ADDED: Real-time validation function ---
    /**
     * Checks if a move is valid (no conflicts in row, col, or box).
     * This is a JS translation of your Python is_valid function.
     */
    function isMoveValid(board, row, col, num) {
        // Check row
        for (let c = 0; c < 9; c++) {
            if (board[row][c] == num && c != col) {
                return false;
            }
        }
        // Check col
        for (let r = 0; r < 9; r++) {
            if (board[r][col] == num && r != row) {
                return false;
            }
        }
        // Check 3x3 box
        const boxRow = Math.floor(row / 3) * 3;
        const boxCol = Math.floor(col / 3) * 3;
        for (let r = 0; r < 3; r++) {
            for (let c = 0; c < 3; c++) {
                if (board[boxRow + r][boxCol + c] == num && (boxRow + r != row || boxCol + c != col)) {
                    return false;
                }
            }
        }
        return true;
    }

    // --- ADDED: Timer functions ---
    function startTimer() {
        // Clear any old timer
        stopTimer(); 
        
        let seconds = 0;
        const timerElement = document.getElementById('timer');
        timerElement.textContent = "00:00"; // Reset display
        
        timerInterval = setInterval(() => {
            seconds++;
            const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
            const secs = (seconds % 60).toString().padStart(2, '0');
            timerElement.textContent = `${mins}:${secs}`;
        }, 1000);
    }

    function stopTimer() {
        clearInterval(timerInterval);
    }

    // --- Board Helper Functions (Unchanged) ---
    function getBoardData() {
        const board = [];
        for (let r = 0; r < 9; r++) {
            const row = [];
            for (let c = 0; c < 9; c++) {
                const cell = cells[r * 9 + c];
                row.push(cell.value === '' ? 0 : parseInt(cell.value));
            }
            board.push(row);
        }
        return board;
    }

    // --- THIS IS THE CORRECTED FUNCTION ---
    function updateBoard(board) {
        // Clear all highlights before updating
        cells.forEach(c => c.classList.remove('selected', 'highlight', 'same-value', 'error'));
        
        for (let r = 0; r < 9; r++) {
            for (let c = 0; c < 9; c++) {
                const cell = cells[r * 9 + c];
                const value = board[r][c];
                
                if (value !== 0) {
                    cell.value = value;
                    cell.readOnly = true;
                    cell.classList.add('given');
                } else {
                    cell.value = '';
                    cell.readOnly = false;
                    cell.classList.remove('given');
                }
            }
        }
    }

    // --- API Call Functions (Unchanged) ---
    async function solvePuzzle() {
        const board = getBoardData();
        
        try {
            const response = await fetch(`${flaskApiUrl}/solve`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ board: board })
            });
            const data = await response.json();

            if (data.status === 'success') {
                updateBoard(data.solution);
                // ADDED: Stop the timer when solved
                stopTimer();
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error solving puzzle:', error);
            alert('Could not connect to the solver. Is the Python server running?');
        }
    }

    async function generatePuzzle() {
        try {
            const response = await fetch(`${flaskApiUrl}/generate`, {
                method: 'GET'
            });
            const data = await response.json();
            updateBoard(data.board);
            // ADDED: Start the timer when a new puzzle is loaded
            startTimer();
        } catch (error)
        {
            console.error('Error generating puzzle:', error);
            alert('Could not connect to the generator. Is the Python server running?');
        }
    }

    function clearBoard() {
        // Just call updateBoard with an empty 9x9 array
        const emptyBoard = Array(9).fill(0).map(() => Array(9).fill(0));
        updateBoard(emptyBoard);
        // ADDED: Reset the timer
        startTimer();
    }

    // --- Event Listeners ---
    solveBtn.addEventListener('click', solvePuzzle);
    generateBtn.addEventListener('click', generatePuzzle);
    clearBtn.addEventListener('click', clearBoard);

    // --- Initialize ---
    createBoard(); // Create the 9x9 grid on page load
    generatePuzzle(); // Load a puzzle on start
});