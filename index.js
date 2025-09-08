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

let startX;
let startY;



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
})

toolbar.addEventListener('click', async e => {
    if(e.target.id === 'clear') {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    if(e.target.id === 'save') {
        try {
            const imageData = canvas.toDataURL('image/png');
            const response = await fetch('http://localhost:5000/predict', {
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