/* Saved-project and non-destructive slice editor for the existing Atlas. */
(function () {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const store = window.AtlasProjects;
  const analyzer = window.ANALYZER;
  if (!store || !analyzer) return;
  let current = null, selected = null, undo = [], saveTimer, saving = false, revision = 0, opening = false;
  const state = analyzer.state;
  const CATEGORIES = ['KICK', 'SNARE', 'HAT', 'TONAL', 'PERC', 'BREATH'];
  $('projectToolbar').innerHTML = `
    <div class="project-tools">
      <label>Project name<input id="projectName" maxlength="100" placeholder="Untitled project" /></label>
      <button type="button" class="play-btn" id="projectSave" disabled>Save project</button>
      <button type="button" class="play-btn" id="projectNew">New project</button>
      <label>Saved projects<select id="projectList"><option value="">Choose a project…</option></select></label>
      <button type="button" class="play-btn" id="projectOpen">Open</button>
      <button type="button" class="play-btn" id="projectBackup" disabled>Export project</button>
      <label class="play-btn">Import project<input type="file" id="projectImport" accept=".atlas,application/json" hidden /></label>
    </div>
    <p class="project-note">Saved in this browser on this device. Export a project backup before clearing browser data. <span id="projectStatus" role="status" aria-live="polite">Import a recording to begin.</span></p>`;
  $('sliceEditor').innerHTML = `
    <section class="panel slice-editor" aria-label="Slice editor">
      <div class="panel-title">Slice editor <span id="sliceId">Select a hit pad</span></div>
      <canvas id="sliceWave" height="100" role="img" aria-label="Zoomed waveform; start is amber, end is cyan"></canvas>
      <form id="sliceForm">
        <div class="slice-fields">
          <label>Start (seconds)<input id="sliceStart" type="number" min="0" step="0.001" required /></label>
          <label>End (seconds)<input id="sliceEnd" type="number" min="0.005" step="0.001" required /></label>
          <label>Name<input id="sliceLabel" maxlength="100" placeholder="Sound name" /></label>
          <label>IPA (editable)<input id="sliceIPA" maxlength="200" placeholder="Your transcription" /></label>
          <label>Category<select id="sliceCategory">${CATEGORIES.map((c) => `<option>${c}</option>`).join('')}</select></label>
        </div>
        <div class="slice-actions">
          <button class="play-btn" type="submit">Apply slice edit</button>
          <button class="play-btn" type="button" id="sliceAudition">Audition slice</button>
          <button class="play-btn" type="button" id="sliceUndo" disabled>Undo edit</button>
          <button class="play-btn" type="button" id="sliceAdd">Add slice</button>
          <span id="sliceStatus" role="status">Original audio stays intact.</span>
        </div>
      </form>
    </section>`;
  function status(text, error = false) {
    $('projectStatus').textContent = text;
    $('projectStatus').classList.toggle('error', error);
  }
  function slice() { return state.res?.hits.find((h) => h.i === selected); }
  function capture() {
    if (!state.res || !state.file) throw new Error('Import and analyze a recording first.');
    if (!current) current = { id: crypto.randomUUID(), createdAt: Date.now() };
    return {
      version: store.VERSION, ...current,
      name: $('projectName').value.trim() || state.file.name,
      updatedAt: Date.now(), fileName: state.file.name, media: state.file,
      result: structuredClone(state.res)
    };
  }
  async function listProjects(id = current?.id) {
    const items = await store.list();
    const select = $('projectList');
    select.replaceChildren(new Option('Choose a project…', ''));
    items.forEach((p) => select.add(new Option(p.name, p.id)));
    if (id) select.value = id;
  }
  async function save() {
    clearTimeout(saveTimer);
    if (!state.res || opening) return;
    if (saving) { saveTimer = setTimeout(save, 400); return; }
    saving = true;
    const atRevision = revision;
    try {
      const project = capture();
      status('Saving…');
      await store.save(project);
      if (current?.id === project.id && revision === atRevision) status('Saved.');
      await listProjects();
    } catch (e) { status('Not saved: ' + e.message + '. Export a backup if storage is full.', true); }
    finally { saving = false; }
  }
  function changed() {
    revision++;
    status('Unsaved changes…');
    clearTimeout(saveTimer);
    saveTimer = setTimeout(save, 700);
  }
  function ready() {
    selected = state.res.hits[0]?.i ?? null;
    undo = [];
    $('projectSave').disabled = $('projectBackup').disabled = false;
    fillEditor();
  }
  function fillEditor() {
    const h = slice();
    $('sliceForm').hidden = !state.res;
    ['sliceStart', 'sliceEnd', 'sliceLabel', 'sliceIPA', 'sliceCategory', 'sliceAudition'].forEach((id) => $(id).disabled = !h);
    $('sliceId').textContent = h ? '#' + String(h.i).padStart(3, '0') : 'No detected hits. Add a slice.';
    $('sliceStart').value = h ? h.s.toFixed(3) : '';
    $('sliceEnd').value = h ? h.e.toFixed(3) : '';
    $('sliceStart').max = $('sliceEnd').max = state.res?.dur || 0;
    $('sliceLabel').value = h?.label || '';
    $('sliceIPA').value = h?.ipa || '';
    $('sliceCategory').value = h?.cat || 'PERC';
    $('sliceUndo').disabled = !undo.length;
    drawWave();
  }
  function drawWave() {
    const cv = $('sliceWave'), g = cv.getContext('2d');
    const w = cv.clientWidth || 500, height = 100, dpr = window.devicePixelRatio || 1;
    cv.width = w * dpr; cv.height = height * dpr; g.scale(dpr, dpr);
    g.fillStyle = '#080a0f'; g.fillRect(0, 0, w, height);
    const h = slice(); if (!h || !state.buf) return;
    const start = Number($('sliceStart').value), end = Number($('sliceEnd').value);
    const lo = Math.max(0, Math.min(h.s, start) - 0.15), hi = Math.min(state.buf.duration, Math.max(h.e, end) + 0.15);
    const samples = state.buf.getChannelData(0), sr = state.buf.sampleRate;
    g.fillStyle = '#38bdf8';
    for (let x = 0; x < w; x++) {
      const a = Math.floor((lo + x / w * (hi - lo)) * sr), b = Math.min(samples.length, Math.ceil((lo + (x + 1) / w * (hi - lo)) * sr));
      let min = 0, max = 0;
      for (let i = a; i < b; i++) { min = Math.min(min, samples[i]); max = Math.max(max, samples[i]); }
      g.fillRect(x, 50 - max * 42, 1, Math.max(1, (max - min) * 42));
    }
    for (const [t, color, label] of [[start, '#f59e0b', 'START'], [end, '#38bdf8', 'END']]) {
      const x = (t - lo) / (hi - lo) * w;
      g.fillStyle = color; g.fillRect(x, 0, 2, height); g.font = '10px monospace';
      g.fillText(label + ' ' + t.toFixed(3), Math.max(3, Math.min(w - 90, x + 5)), label === 'START' ? 14 : 95);
    }
  }
  async function applyProject(p) {
    if (opening) return;
    opening = true;
    clearTimeout(saveTimer);
    try {
      // Save the outgoing project before replacing it.
      if (state.res) await store.save(capture());
      status('Opening project…');
      if (!await analyzer.restore(p)) return;
      current = { id: p.id, createdAt: p.createdAt };
      $('projectName').value = p.name;
      revision++; ready();
      await listProjects(p.id); status('Opened saved project.');
    } catch (e) { status('Could not open project: ' + e.message, true); }
    finally { opening = false; }
  }
  window.ATLAS_BEFORE_REPLACE = async () => {
    clearTimeout(saveTimer);
    if (state.res) await store.save(capture());
  };
  $('projectSave').addEventListener('click', save);
  $('projectName').addEventListener('input', () => { if (state.res) changed(); });
  $('projectOpen').addEventListener('click', async () => {
    try {
      const id = $('projectList').value;
      if (!id) { status('Choose a saved project first.'); return; }
      const p = await store.get(id);
      if (!p) throw new Error('Project is no longer available.');
      await applyProject(p);
    } catch (e) { status(e.message, true); }
  });
  $('projectNew').addEventListener('click', async () => {
    if (opening) return;
    clearTimeout(saveTimer);
    try {
      if (state.res) await store.save(capture());
      current = null; selected = null; undo = []; revision++;
      analyzer.reset();
      $('projectName').value = '';
      $('projectSave').disabled = $('projectBackup').disabled = true;
      fillEditor(); await listProjects(''); status('New project. Import a recording.');
    } catch (e) { status('Could not save current project. Export it before starting a new one: ' + e.message, true); }
  });
  $('sliceForm').addEventListener('submit', (event) => {
    event.preventDefault();
    const h = slice(); if (!h) return;
    try {
      const valid = store.bounds(Number($('sliceStart').value), Number($('sliceEnd').value), state.buf.duration);
      undo.push(structuredClone(state.res.hits)); if (undo.length > 50) undo.shift();
      Object.assign(h, valid, { label: $('sliceLabel').value.trim(), ipa: $('sliceIPA').value.trim(), cat: $('sliceCategory').value, edited: true });
      analyzer.refresh(); fillEditor(); changed(); $('sliceStatus').textContent = 'Applied to pads and JSON export.';
    } catch (e) { $('sliceStatus').textContent = e.message; }
  });
  $('sliceAudition').addEventListener('click', async () => {
    try {
      const b = store.bounds(Number($('sliceStart').value), Number($('sliceEnd').value), state.buf.duration);
      await PLAY.enable(); PLAY.sampleSlice(state.buf, b.s, b.e, 112);
    } catch (e) { $('sliceStatus').textContent = e.message; }
  });
  $('sliceUndo').addEventListener('click', () => {
    if (!undo.length) return;
    state.res.hits = undo.pop();
    if (!slice()) selected = state.res.hits[0]?.i ?? null;
    analyzer.refresh(); fillEditor(); changed(); $('sliceStatus').textContent = 'Previous slice edit restored.';
  });
  $('sliceAdd').addEventListener('click', () => {
    if (!state.res) return;
    undo.push(structuredClone(state.res.hits));
    const id = Math.max(0, ...state.res.hits.map((h) => h.i)) + 1;
    const start = slice()?.e || 0, s = Math.min(start, Math.max(0, state.res.dur - 0.01));
    state.res.hits.push({ i: id, id: crypto.randomUUID(), s, e: Math.min(state.res.dur, s + 0.5), cat: 'PERC', pk: 0, label: 'New slice', ipa: '', edited: true });
    selected = id; state.bank = Math.floor((state.res.hits.length - 1) / 16);
    analyzer.refresh(); fillEditor(); changed();
  });
  ['sliceStart', 'sliceEnd'].forEach((id) => $(id).addEventListener('input', drawWave));
  window.addEventListener('atlas:select-slice', (event) => { selected = event.detail; fillEditor(); });
  window.addEventListener('atlas:import-start', () => {
    clearTimeout(saveTimer);
    // beforeReplace committed the previous project; a new recording gets a new ID.
    current = null; selected = null; undo = []; revision++;
    $('projectSave').disabled = $('projectBackup').disabled = true;
    status('Analyzing recording…');
  });
  window.addEventListener('atlas:import-error', (event) => status(event.detail, true));
  window.addEventListener('atlas:analyzed', () => {
    current = null;
    $('projectName').value = state.file.name.replace(/\.[^.]+$/, '');
    ready(); changed();
  });
  $('projectBackup').addEventListener('click', async () => {
    try {
      const p = capture();
      if (p.media.size > 40 * 1024 * 1024) throw new Error('Portable backup currently supports media up to 40 MB. The local save still supports larger files.');
      const data = await new Promise((resolve, reject) => { const reader = new FileReader(); reader.onload = () => resolve(reader.result); reader.onerror = () => reject(reader.error); reader.readAsDataURL(p.media); });
      const portable = { ...p, media: { type: p.media.type, data }, result: { ...p.result, spec: Array.from(p.result.spec) } };
      const url = URL.createObjectURL(new Blob([JSON.stringify(portable)], { type: 'application/json' }));
      const link = document.createElement('a'); link.href = url; link.download = p.name.replace(/[^a-z0-9_-]/gi, '_') + '.atlas'; link.click();
      setTimeout(() => URL.revokeObjectURL(url), 60000);
      status('Project backup download started.');
    } catch (e) { status('Export failed: ' + e.message, true); }
  });
  $('projectImport').addEventListener('change', async (event) => {
    try {
      const file = event.target.files[0]; if (!file) return;
      if (file.size > 80 * 1024 * 1024) throw new Error('Project backup is too large (80 MB limit).');
      const p = JSON.parse(await file.text());
      if (!p.media || typeof p.media.data !== 'string' || !/^data:[^,]*;base64,[A-Za-z0-9+/=]*$/.test(p.media.data)) throw new Error('Project backup media is invalid.');
      const binary = atob(p.media.data.slice(p.media.data.indexOf(',') + 1));
      p.media = new Blob([Uint8Array.from(binary, (c) => c.charCodeAt(0))], { type: p.media.type });
      store.validateProject(p);
      // Import a separate copy; never overwrite an existing saved project ID.
      p.id = crypto.randomUUID(); p.createdAt = p.updatedAt = Date.now();
      p.result.spec = Uint8Array.from(p.result.spec);
      await applyProject(p);
      if (current?.id === p.id) await save();
    } catch (e) { status('Import failed: ' + e.message, true); }
    finally { event.target.value = ''; }
  });
  window.addEventListener('resize', drawWave);
  new ResizeObserver(drawWave).observe($('sliceWave'));
  listProjects().catch((e) => status('Project storage unavailable: ' + e.message, true));
})();
