const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const video = document.getElementById('video');
const deviceSelect = document.getElementById('deviceSelect');
const mirrorToggle = document.getElementById('mirrorToggle');
const captureBtn = document.getElementById('captureBtn');
const canvas = document.getElementById('canvas');
const downloadLink = document.getElementById('downloadLink');
const status = document.getElementById('status');

let stream = null;

function setStatus(s){ status.textContent = s; }

async function enumerateCameras(){
    try{
    const devices = await navigator.mediaDevices.enumerateDevices();
    const cams = devices.filter(d => d.kind === 'videoinput');
    deviceSelect.innerHTML = '';
    cams.forEach((c, i)=>{
        const opt = document.createElement('option');
        opt.value = c.deviceId;
        opt.text = c.label || `Camera ${i+1}`;
        deviceSelect.appendChild(opt);
    });
    if(cams.length===0) deviceSelect.innerHTML = '<option disabled>No cameras found</option>';
    }catch(err){
    console.error('Cannot list devices', err);
    deviceSelect.innerHTML = '<option disabled>Unable to enumerate devices</option>';
    }
}

async function startCamera(deviceId){
    stopCamera();
    setStatus('Requesting camera...');
    const constraints = {
    audio: false,
    video: {
        width: {ideal: 1280},
        height: {ideal: 720},
    }
    };
    if(deviceId) constraints.video.deviceId = { exact: deviceId };
    try{
    stream = await navigator.mediaDevices.getUserMedia(constraints);
    video.srcObject = stream;
    startBtn.disabled = true;
    stopBtn.disabled = false;
    captureBtn.disabled = false;
    setStatus('Camera started');
    await enumerateCameras(); // refresh labels (some browsers only expose labels after permission)
    applyMirror();
    }catch(err){
    console.error('getUserMedia error', err);
    setStatus('Camera error: ' + (err.message || err.name));
    }
}

function stopCamera(){
    if(stream){
    stream.getTracks().forEach(t => t.stop());
    stream = null;
    video.srcObject = null;
    startBtn.disabled = false;
    stopBtn.disabled = true;
    captureBtn.disabled = true;
    setStatus('Camera stopped');
    }
}

function applyMirror(){
    const mirrored = mirrorToggle.checked;
    // For the live preview, the easiest and smoothest approach is CSS transform.
    // This flips the DOM element visually but does not change the underlying camera frames.
    video.style.transform = mirrored ? 'scaleX(-1)' : 'none';
}

function captureSnapshot(){
    if(!video || video.readyState < 2) return;
    const w = canvas.width = video.videoWidth || 320;
    const h = canvas.height = video.videoHeight || 240;
    const ctx = canvas.getContext('2d');

    ctx.save();
    if(mirrorToggle.checked){
    // To make the saved image match the mirrored preview, draw the video flipped on the canvas.
    ctx.translate(w, 0);
    ctx.scale(-1, 1);
    }
    // draw the video frame to canvas
    ctx.drawImage(video, 0, 0, w, h);
    ctx.restore();

    // Create a download link for the snapshot
    canvas.toBlob(blob => {
    if(!blob) return;
    const url = URL.createObjectURL(blob);
    downloadLink.href = url;
    downloadLink.style.display = 'inline-block';
    downloadLink.textContent = 'Download snapshot';
    }, 'image/png');

    setStatus('Snapshot captured');
}

// Wire up UI
startBtn.addEventListener('click', async ()=>{
    const selected = deviceSelect.value || null;
    await startCamera(selected);
});
stopBtn.addEventListener('click', ()=>stopCamera());
mirrorToggle.addEventListener('change', applyMirror);
captureBtn.addEventListener('click', captureSnapshot);

// If the user changes camera from the dropdown, restart with that device
deviceSelect.addEventListener('change', async ()=>{
    if(deviceSelect.value) await startCamera(deviceSelect.value);
});

// On load: try to enumerate devices and set a helpful default
(async function init(){
    if(!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia){
    setStatus('getUserMedia not supported in this browser');
    startBtn.disabled = true;
    return;
    }
    await enumerateCameras();
    // Try to pre-select a camera if available
    if(deviceSelect.options.length>0 && deviceSelect.options[0].value){
    deviceSelect.selectedIndex = 0;
    }
    setStatus('Ready — click "Start Camera"');
})();

// Optional: stop camera when the page is hidden to be polite with permissions
document.addEventListener('visibilitychange', ()=>{
    if(document.hidden) stopCamera();
});