let fileId = null;

const out = document.getElementById('out');
const statusEl = document.getElementById('status');
const progressEl = document.getElementById('progress');
const downloadsEl = document.getElementById('downloads');
const fileInput = document.getElementById('file');
const dropzone = document.getElementById('dropzone');
const dropLabel = document.getElementById('dropLabel');

const setStatus = (text) => { statusEl.textContent = text; };
const setProgress = (n) => { progressEl.style.width = `${n}%`; };

function setFile(file) {
  const dt = new DataTransfer();
  dt.items.add(file);
  fileInput.files = dt.files;
  dropLabel.textContent = `Selected: ${file.name}`;
}

['dragenter', 'dragover'].forEach(evt => dropzone.addEventListener(evt, (e) => {
  e.preventDefault();
  dropzone.classList.add('active');
}));
['dragleave', 'drop'].forEach(evt => dropzone.addEventListener(evt, (e) => {
  e.preventDefault();
  dropzone.classList.remove('active');
}));
dropzone.addEventListener('drop', (e) => {
  const file = e.dataTransfer.files?.[0];
  if (file) setFile(file);
});
fileInput.addEventListener('change', () => {
  const file = fileInput.files?.[0];
  if (file) dropLabel.textContent = `Selected: ${file.name}`;
});

document.getElementById('upload').onclick = async () => {
  const file = fileInput.files?.[0];
  if (!file) {
    setStatus('⚠ Select an .xlsx or .csv file first');
    return;
  }

  setStatus('Uploading file...');
  setProgress(20);

  const form = new FormData();
  form.append('file', file);
  const res = await fetch('/upload', { method: 'POST', body: form });
  const data = await res.json();

  if (!res.ok) {
    setStatus(`❌ Upload failed: ${data.detail || 'Unknown error'}`);
    setProgress(0);
    out.textContent = JSON.stringify(data, null, 2);
    return;
  }

  fileId = data.file_id;
  setStatus(`✅ Uploaded · file_id: ${fileId}`);
  setProgress(50);
  out.textContent = JSON.stringify(data, null, 2);
};

document.getElementById('process').onclick = async () => {
  if (!fileId) {
    setStatus('⚠ Upload a file before processing');
    return;
  }

  setStatus('Running AI pipeline...');
  setProgress(75);

  const res = await fetch(`/process/${fileId}`, { method: 'POST' });
  const data = await res.json();

  if (!res.ok) {
    setStatus(`❌ Processing failed: ${data.detail || 'Unknown error'}`);
    setProgress(0);
    out.textContent = JSON.stringify(data, null, 2);
    return;
  }

  setStatus('✅ Completed. Reports are ready for download.');
  setProgress(100);
  out.textContent = JSON.stringify(data, null, 2);
  downloadsEl.innerHTML = `
    <a href="/report/${fileId}">Download PDF Report</a>
    <a href="/cleaned/${fileId}">Download Cleaned Excel</a>
  `;
};
