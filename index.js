const canvas = document.getElementById('drawing-board');
const toolbar = document.getElementById('toolbar');
const ctx = canvas.getContext('2d');

const canvasOffsetX = canvas.offsetLeft;
const canvasOffsetY = canvas.offsetTop;

// Set fixed canvas size to 400x400
canvas.width = 400;
canvas.height = 400;

let isPainting = false;
let lineWidth = 25;
let hasDrawing = false;  // Track if something is drawn

let startX;
let startY;

// Get the "See in sim!!" button
exportButton.disabled = true;  // Initially disabled
exportButton.style.opacity = '0.5';  // Visual feedback
exportButton.style.cursor = 'not-allowed';

// Function to check if canvas has any drawing
function checkIfDrawn() {
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    
    // Check if any pixel has been modified (not completely transparent)
    for (let i = 3; i < data.length; i += 4) {
        if (data[i] !== 0) {  // Check alpha channel
            hasDrawing = true;
            exportButton.disabled = false;
            exportButton.style.opacity = '1';
            exportButton.style.cursor = 'pointer';
            return;
        }
    }
    
    hasDrawing = false;
    exportButton.disabled = true;
    exportButton.style.opacity = '0.5';
    exportButton.style.cursor = 'not-allowed';
}



canvas.addEventListener('mousedown', (e) => {
    isPainting = true;
    startX = e.clientX;
    startY = e.clientY;
});

canvas.addEventListener('mousemove', (e) => {
    if (!isPainting) return;
    
    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';
    
    ctx.lineTo(e.clientX - canvasOffsetX, e.clientY - canvasOffsetY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvasOffsetX, e.clientY - canvasOffsetY);
});

canvas.addEventListener('mouseup', (e) => {
    isPainting = false;
    ctx.stroke();
    ctx.beginPath();
    checkIfDrawn();  // Check if something is drawn after mouse up
})

toolbar.addEventListener('click', async e => {
    if(e.target.id === 'clear') {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        checkIfDrawn();  // Update button state after clearing
    }
    if(e.target.id === 'export-polygon') {
        if (!hasDrawing) {
            alert('Please draw something first!');
            return;
        }
        
        try {
            const imageData = canvas.toDataURL('image/png');
            
            // Use production API or local Flask server
            const apiUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
                ? 'http://127.0.0.1:5000/predict'
                : 'https://magic01.pythonanywhere.com/predict';
            
            // Send to Flask backend to process and store data
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: imageData })
            });
            
            if (response.ok) {
                // Redirect to 2nd.html after successful processing
                window.location.href = '2nd.html';
            } else {
                alert('Error processing image. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error connecting to server. Make sure Flask is running.');
        }
    }
    if(e.target.id === 'save') {
        try {
            const imageData = canvas.toDataURL('image/png');
            

            const response = await fetch('https://magic01.pythonanywhere.com/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: imageData })
            });
            
            const result = await response.json();

            const toast = document.createElement('div');
            toast.style.cssText = `
                position: fixed;
                top: 50%;
                right: 50%;
                background: #007bff;
                color: white;
                padding: 15px 25px;
                border-radius: 5px;
                font-size: 18px;
                z-index: 1000;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            `;
            toast.textContent = `Predicted digit: ${result.prediction}`;

            document.body.appendChild(toast);

            setTimeout(() => {
                document.body.removeChild(toast);
            }, 3000);
            
        } catch (error) {
            console.error('Error:', error);
            alert('Error processing image');
        }
    }
});
