let fileId = null;
const out = document.getElementById('out');
const statusEl = document.getElementById('status');

document.getElementById('upload').onclick = async () => {
  const file = document.getElementById('file').files[0];
  if(!file) return;
  const form = new FormData(); form.append('file', file);
  const res = await fetch('/upload', {method:'POST', body: form});
  const data = await res.json();
  fileId = data.file_id; statusEl.textContent = `Uploaded: ${fileId}`; out.textContent = JSON.stringify(data,null,2);
};

document.getElementById('process').onclick = async () => {
  if(!fileId) return;
  statusEl.textContent = 'Processing...';
  const res = await fetch(`/process/${fileId}`, {method:'POST'});
  const data = await res.json();
  out.textContent = JSON.stringify(data, null, 2);
  statusEl.innerHTML = `Done. <a href="/report/${fileId}">PDF Report</a> | <a href="/cleaned/${fileId}">Cleaned Excel</a>`;
};
