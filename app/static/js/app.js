const dz = document.getElementById('dropzone');
const fi = document.getElementById('fileInput');
const rs = document.getElementById('result');
const pg = document.getElementById('progress');
const mode = document.getElementById('modeToggle');

mode.addEventListener('change',()=>document.body.classList.toggle('dark', mode.checked));
dz.addEventListener('click', ()=>fi.click());
dz.addEventListener('dragover', e=>{e.preventDefault();});
dz.addEventListener('drop', e=>{e.preventDefault(); upload(e.dataTransfer.files[0]);});
fi.addEventListener('change', ()=>upload(fi.files[0]));

async function upload(file){
  if(!file) return;
  pg.textContent='Uploading and analyzing...';
  const form = new FormData();
  form.append('file', file);
  const res = await fetch('/api/analyze', {method:'POST', body:form});
  const data = await res.json();
  if(!res.ok){ rs.textContent = data.detail || 'Failed'; pg.textContent=''; return; }
  pg.textContent='Completed';
  rs.textContent = JSON.stringify(data, null, 2);
}
