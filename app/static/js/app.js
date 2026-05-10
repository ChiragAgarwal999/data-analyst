let fileId = null;
const out = document.getElementById('out');
const statusEl = document.getElementById('status');
const progressEl = document.getElementById('progress');
const downloadsEl = document.getElementById('downloads');

function setStatus(text, cls) {
  statusEl.textContent = text;
  statusEl.className = `status ${cls}`;
}

function setProgress(value) {
  progressEl.style.width = `${value}%`;
}

document.getElementById('upload').onclick = async () => {
  const file = document.getElementById('file').files[0];
  if (!file) {
    setStatus('Please select a .xlsx or .csv file first', 'idle');
    return;
  }

  setStatus('Uploading file...', 'working');
  setProgress(25);

  const form = new FormData();
  form.append('file', file);

  const res = await fetch('/upload', { method: 'POST', body: form });
  const data = await res.json();

  if (!res.ok) {
    setStatus(`Upload failed: ${data.detail || 'Unknown error'}`, 'idle');
    setProgress(0);
    return;
  }

  fileId = data.file_id;
  setStatus(`Uploaded successfully (file_id: ${fileId})`, 'done');
  setProgress(50);
  out.textContent = JSON.stringify(data, null, 2);
};

document.getElementById('process').onclick = async () => {
  if (!fileId) {
    setStatus('Upload a file before processing', 'idle');
    return;
  }

  setStatus('Running AI analysis pipeline...', 'working');
  setProgress(75);

  const res = await fetch(`/process/${fileId}`, { method: 'POST' });
  const data = await res.json();

  if (!res.ok) {
    setStatus(`Processing failed: ${data.detail || 'Unknown error'}`, 'idle');
    setProgress(0);
    out.textContent = JSON.stringify(data, null, 2);
    return;
  }

  setStatus('Processing completed successfully', 'done');
  setProgress(100);
  out.textContent = JSON.stringify(data, null, 2);
  downloadsEl.innerHTML = `<a href="/report/${fileId}">Download PDF Report</a><a href="/cleaned/${fileId}">Download Cleaned Excel</a>`;
};
