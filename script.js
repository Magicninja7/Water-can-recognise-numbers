let gridData = [];
let queueData = [];
let lData = 0;
let rData = 0;
let isAnimating = false;

// Four grid containers positioned around the screen
const gridContainers = Array.from(document.querySelectorAll('.grid'));
const gridLabels = Array.from(document.querySelectorAll('.grid-label'));
const vectorContent = document.getElementById('vectorContent');

const startBtn = document.getElementById('startBtn');
const resetBtn = document.getElementById('resetBtn');
const speedSlider = document.getElementById('speedSlider');

async function fetchData() {
    try {
        // Use production API or local Flask server
        const apiUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? 'http://127.0.0.1:5000/api/data'
            : 'https://magic01.pythonanywhere.com/api/data';
            
        const res = await fetch(apiUrl, {
            headers: { 'Accept': 'application/json' }
        });
        if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
        const ct = res.headers.get('content-type') || '';
        if (!ct.includes('application/json')) {
            const text = await res.text();
            throw new Error(`Non-JSON response (${ct}): ${text.slice(0, 200)}`);
        }
        const data = await res.json();
        console.log(data);
        gridData = data.grid;
        queueData = data.queue;
        lData = data.l;
        rData = data.r;
        renderGrid();
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function renderGrid() {
    if (!Array.isArray(gridData) || gridData.length === 0) return;
    // gridData[0] = top-left, gridData[1] = top-right, gridData[2] = bottom-left, gridData[3] = bottom-right
    gridContainers.forEach((container, gridIndex) => {
        container.innerHTML = '';
        const currentGrid = gridData[gridIndex];
        if (!currentGrid || !Array.isArray(currentGrid) || currentGrid.length === 0) return;
        
        // Get dynamic grid dimensions
        const rows = currentGrid.length;
        const cols = currentGrid[0] ? currentGrid[0].length : 0;
        
        if (cols === 0) return;
        
        // Update grid CSS to match dimensions
        container.style.gridTemplateRows = `repeat(${rows}, 25px)`;
        container.style.gridTemplateColumns = `repeat(${cols}, 25px)`;
        
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                const cell = document.createElement('div');
                const cellValue = currentGrid[i] && currentGrid[i][j] !== undefined ? currentGrid[i][j] : 0;
                cell.className = `cell ${cellValue === 1 ? 'one' : 'zero'}`;
                cell.dataset.row = i;
                cell.dataset.col = j;
                container.appendChild(cell);
            }
        }
        
        // Update label with l and r values
        if (gridLabels[gridIndex] && lData && rData) {
            gridLabels[gridIndex].textContent = `l: ${lData[gridIndex]}, r: ${rData[gridIndex]}`;
        }
    });
    
    // Update vector display
    updateVectorDisplay();
}

function updateVectorDisplay() {
    if (!vectorContent || !lData || !rData) return;
    
    // Create vector array: [l0, r0, l1, r1, l2, r2, l3, r3]
    const vector = [];
    for (let i = 0; i < 4; i++) {
        vector.push(lData[i]);
        vector.push(rData[i]);
    }
    
    // Display the vector
    let html = '';
    for (let i = 0; i < vector.length; i++) {
        html += `<div>vector[${i}] = ${vector[i]}</div>`;
    }
    
    vectorContent.innerHTML = html;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function animateBFS() {
    if (isAnimating) return;
    isAnimating = true;
    startBtn.disabled = true;

    const delay = 510 - speedSlider.value;

    // queueData[0] = top-left, queueData[1] = top-right, queueData[2] = bottom-left, queueData[3] = bottom-right
    // Find the maximum queue length to animate all grids in parallel
    const maxQueueLength = Math.max(...queueData.map(q => q.length));
    
    for (let i = 0; i < maxQueueLength; i++) {
        // For each grid, get the cell at position i in its queue
        const cells = gridContainers.map((container, gridIndex) => {
            const currentQueue = queueData[gridIndex];
            if (!currentQueue || i >= currentQueue.length) return null;
            
            const [row, col] = currentQueue[i];
            return container.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        });

        cells.forEach(cell => cell && cell.classList.add('visiting'));
        await sleep(delay);
        cells.forEach(cell => {
            if (!cell) return;
            cell.classList.remove('visiting');
            cell.classList.add('visited');
        });
    }

    isAnimating = false;
    startBtn.disabled = false;
}

startBtn.addEventListener('click', animateBFS);
resetBtn.addEventListener('click', () => {
    if (!isAnimating) {
        fetchData();
    }
});

// Initial load
fetchData();
