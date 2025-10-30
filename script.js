document.addEventListener('DOMContentLoaded', () => {
    const boardElement = document.getElementById('sudoku-board');
    const solveBtn = document.getElementById('solve-btn');
    const generateBtn = document.getElementById('generate-btn');
    const clearBtn = document.getElementById('clear-btn');
    const cells = [];

    const flaskApiUrl = 'http://127.0.0.1:5000'; // Your Flask server URL

    // --- Create the Board ---
    function createBoard() {
        boardElement.innerHTML = ''; 
        cells.length = 0; 
        for (let i = 0; i < 81; i++) {
            const cell = document.createElement('input');
            cell.type = 'text';
            cell.maxLength = 1;
            cell.classList.add('cell');
            cell.addEventListener('input', (e) => {
                e.target.value = e.target.value.replace(/[^1-9]/g, '');
            });
            boardElement.appendChild(cell);
            cells.push(cell);
        }
    }

    // --- Board Helper Functions ---
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

    function updateBoard(board) {
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

    // --- API Call Functions ---
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
        } catch (error) {
            console.error('Error generating puzzle:', error);
            alert('Could not connect to the generator. Is the Python server running?');
        }
    }

    function clearBoard() {
        for (const cell of cells) {
            cell.value = '';
            cell.readOnly = false;
            cell.classList.remove('given');
        }
    }

    // --- Event Listeners ---
    solveBtn.addEventListener('click', solvePuzzle);
    generateBtn.addEventListener('click', generatePuzzle);
    clearBtn.addEventListener('click', clearBoard);

    // --- Initialize ---
    createBoard(); 
});