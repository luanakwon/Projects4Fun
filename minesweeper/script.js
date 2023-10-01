document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('board');
    const resetButton = document.getElementById('reset');
    const gridSize = 10;
    const numMines = 20;
    let cells = [];

    // Initialize the game board
    function initializeBoard() {
        board.innerHTML = '';
        cells = [];
        for (let i = 0; i < gridSize; i++) {
            const row = [];
            for (let j = 0; j < gridSize; j++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.setAttribute('data-row', i);
                cell.setAttribute('data-col', j);
                row.push(cell);
                board.appendChild(cell);
            }
            cells.push(row);
        }
    }

    // Generate random mines
    function generateMines() {
        const mines = [];
        while (mines.length < numMines) {
            const row = Math.floor(Math.random() * gridSize);
            const col = Math.floor(Math.random() * gridSize);
            if (!mines.some(mine => mine.row === row && mine.col === col)) {
                mines.push({ row, col });
                cells[row][col].classList.add('mine');
            }
        }
    }

    // Event listener for cell clicks
    board.addEventListener('click', (e) => {
        const cell = e.target;
        if (!cell.classList.contains('revealed')) {
            const row = parseInt(cell.getAttribute('data-row'));
            const col = parseInt(cell.getAttribute('data-col'));
            if (cell.classList.contains('mine')) {
                // Game over
                cell.style.backgroundColor = '#f00';
                alert('Game over!');
                revealMines();
            } else {
                const mineCount = countAdjacentMines(row, col);
                cell.textContent = mineCount > 0 ? mineCount : '';
                cell.classList.add('revealed');
                if (mineCount === 0) {
                    // Auto-reveal adjacent cells
                    revealEmptyCells(row, col);
                }
            }
        }
    });

    // Event listener for the reset button
    resetButton.addEventListener('click', () => {
        initializeBoard();
        generateMines();
    });

    // Count adjacent mines
    function countAdjacentMines(row, col) {
        let count = 0;
        for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j++) {
                const newRow = row + i;
                const newCol = col + j;
                if (newRow >= 0 && newRow < gridSize && newCol >= 0 && newCol < gridSize) {
                    if (cells[newRow][newCol].classList.contains('mine')) {
                        count++;
                    }
                }
            }
        }
        return count;
    }

    // Auto-reveal empty cells
    function revealEmptyCells(row, col) {
        for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j++) {
                const newRow = row + i;
                const newCol = col + j;
                if (newRow >= 0 && newRow < gridSize && newCol >= 0 && newCol < gridSize) {
                    const cell = cells[newRow][newCol];
                    if (!cell.classList.contains('revealed')) {
                        const mineCount = countAdjacentMines(newRow, newCol);
                        cell.textContent = mineCount > 0 ? mineCount : '';
                        cell.classList.add('revealed');
                        if (mineCount === 0) {
                            revealEmptyCells(newRow, newCol);
                        }
                    }
                }
            }
        }
    }

    // Reveal all mines
    function revealMines() {
        cells.flat().forEach(cell => {
            if (cell.classList.contains('mine')) {
                cell.textContent = '';
                cell.classList.add('revealed');
            }
        });
    }

    // Initialize the game
    initializeBoard();
    generateMines();
});
