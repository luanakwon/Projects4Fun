document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('board');
    const modes = document.querySelector('.modes');
    const infoDiv = document.getElementById('flag_info');
    let gridSize = 10;
    let numMines = 12;
    let cells = [];
    let numCellsFlagged = 0; // increase whe rightclick
    let numEmptyFound = 0;

    // Define difficulties per game mode
    const gameModes = {
        easy: {gridSize: 10, numMines: 12},
        medium: {gridSize: 16, numMines: 40},
        hard: {gridSize: 22, numMines: 99}
    }
    
    // Function to update the number of mines based on the selected game mode
    function updateGameMode() {
        const selectedMode = document.querySelector('input[name="gameMode"]:checked').value;
        gridSize = gameModes[selectedMode].gridSize;
        numMines = gameModes[selectedMode].numMines;
    }
    
    // Initialize the game board
    function initializeBoard() {
        board.innerHTML = '';
        let cellSize = Math.floor(400/gridSize-2);
        board.style.gridTemplateColumns = `repeat(${gridSize}, ${cellSize}px)`;
        board.style.gridTemplateRows = `repeat(${gridSize}, ${cellSize}px)`;
        numCellsFlagged = 0;
        numEmptyFound = 0;
        infoDiv.innerHTML = 'Flag : '+numMines;
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
        if (cell.classList.contains('cell') && !cell.classList.contains('flagged')){
            if (!cell.classList.contains('revealed')) {
                const row = parseInt(cell.getAttribute('data-row'));
                const col = parseInt(cell.getAttribute('data-col'));
                if (cell.classList.contains('mine')) {
                    // Game over
                    cell.style.backgroundColor = '#f00';
                    revealMines();
                    //alert('Game over!');
                    //TODO disallow board clicks
                    infoDiv.innerHTML = 'Game Over..';
                } else {
                    cell.style.backgroundColor = '#ccc';
                    numEmptyFound += 1;
                    const mineCount = countAdjacentMines(row, col);
                    cell.textContent = mineCount > 0 ? mineCount : '';
                    cell.classList.add('revealed');
                    if (mineCount === 0) {
                        // Auto-reveal adjacent cells
                        revealEmptyCells(row, col);
                    }
                }
                // Game Clear check
                if(numEmptyFound + numMines === gridSize*gridSize) {
                    //alert('GameClear');
                    //TODO disallow board clicks
                    infoDiv.innerHTML = '!!Congratulations!!'
                }
                console.log(numEmptyFound);
            }
        }
    });
    
    // Event listner for cell right click
    board.addEventListener('contextmenu', (e) => {
        e.preventDefault(); // Prevent the default context menu
        const cell = e.target;
        if (cell.classList.contains('cell')){
            if (!cell.classList.contains('revealed')) {
                // Add your custom logic here, e.g., flagging the cell
                // You can toggle a flag class or perform any other action
                // toggle flagged, inc/dec count 
                let flagged = cell.classList.toggle('flagged');
                numCellsFlagged += flagged ? 1 : -1;
                infoDiv.innerHTML = 'Flag : ' + (numMines - numCellsFlagged);
            }
        }
        
    });

    // Event listener for the gamemode group
    modes.addEventListener('change', () => {
        updateGameMode();
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
                    //if not revealed nor flagged
                    if(!cell.classList.contains('revealed')){
                        if (!cell.classList.contains('flagged')) {
                            cell.style.backgroundColor = '#ccc';
                            numEmptyFound += 1;
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
    }

    // Reveal all mines
    function revealMines() {
        cells.flat().forEach(cell => {
            if (cell.classList.contains('mine')) {
                cell.textContent = '';
                cell.classList.add('revealed');
                cell.style.backgroundColor = '#f00';
            }
        });
    }

    // Initialize the game in Easy mode
    updateGameMode();
    initializeBoard();
    generateMines();
});
