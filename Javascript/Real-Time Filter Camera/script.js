const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d', { willReadFrequently: true });
const startBtn = document.getElementById('startBtn');
const filterBtns = document.querySelectorAll('.filter-btn');
const status = document.getElementById('status');
const filterLabel = document.getElementById('filterLabel');

let currentFilter = 'none';
let stream = null;
let animationId = null;
let isWebcamActive = false;

startBtn.addEventListener('click', async () => {
    if (isWebcamActive) {
        stopWebcam();
        return;
    }

    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 640, height: 480 } 
        });
        video.srcObject = stream;
        
        video.addEventListener('loadedmetadata', () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            startBtn.textContent = 'Stop Webcam';
            startBtn.style.background = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
            status.textContent = 'Webcam active! Select a filter below';
            isWebcamActive = true;
            applyFilter();
        });
    } catch (err) {
        status.textContent = 'Error: Could not access webcam';
        console.error('Webcam error:', err);
    }
});

function stopWebcam() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
    }
    video.srcObject = null;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    startBtn.textContent = 'Start Webcam';
    startBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    status.textContent = 'Webcam stopped. Click to restart';
    isWebcamActive = false;
}

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter;
        const filterName = btn.textContent;
        filterLabel.textContent = `Current Filter: ${filterName}`;
    });
});

function applyFilter() {
    if (!video.paused && !video.ended) {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        if (currentFilter !== 'none') {
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const data = imageData.data;

            switch(currentFilter) {
                case 'grayscale':
                    for (let i = 0; i < data.length; i += 4) {
                        const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
                        data[i] = avg;
                        data[i + 1] = avg;
                        data[i + 2] = avg;
                    }
                    break;

                case 'sepia':
                    for (let i = 0; i < data.length; i += 4) {
                        const r = data[i];
                        const g = data[i + 1];
                        const b = data[i + 2];
                        data[i] = Math.min(255, (r * 0.393) + (g * 0.769) + (b * 0.189));
                        data[i + 1] = Math.min(255, (r * 0.349) + (g * 0.686) + (b * 0.168));
                        data[i + 2] = Math.min(255, (r * 0.272) + (g * 0.534) + (b * 0.131));
                    }
                    break;

                case 'invert':
                    for (let i = 0; i < data.length; i += 4) {
                        data[i] = 255 - data[i];
                        data[i + 1] = 255 - data[i + 1];
                        data[i + 2] = 255 - data[i + 2];
                    }
                    break;

                case 'blur':
                    ctx.filter = 'blur(4px)';
                    ctx.drawImage(canvas, 0, 0);
                    ctx.filter = 'none';
                    break;

                case 'brightness':
                    for (let i = 0; i < data.length; i += 4) {
                        data[i] = Math.min(255, data[i] * 1.5);
                        data[i + 1] = Math.min(255, data[i + 1] * 1.5);
                        data[i + 2] = Math.min(255, data[i + 2] * 1.5);
                    }
                    break;

                case 'contrast':
                    const factor = 1.5;
                    const intercept = 128 * (1 - factor);
                    for (let i = 0; i < data.length; i += 4) {
                        data[i] = Math.min(255, Math.max(0, data[i] * factor + intercept));
                        data[i + 1] = Math.min(255, Math.max(0, data[i + 1] * factor + intercept));
                        data[i + 2] = Math.min(255, Math.max(0, data[i + 2] * factor + intercept));
                    }
                    break;
            }

            if (currentFilter !== 'blur') {
                ctx.putImageData(imageData, 0, 0);
            }
        }

        animationId = requestAnimationFrame(applyFilter);
    }
}