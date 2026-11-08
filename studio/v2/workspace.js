/* One active-project context for every studio view. Prepared report is demo-only. */
(function () {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const model = window.AtlasProjectModel;
  const A = window.ANALYZER.state;
  const W = window.ATLAS_WORKSPACE = { mode:'demo', project:null, media:null, index:0 };
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const nodes = new Map();
  let list = [], selectedId = null;
  const originalToggle = window.togglePlayPause;
  const fmt = (n) => Number(n || 0).toFixed(2) + 's';
  const evs = () => model.events(A.res, PROJECTS.content);
  const name = () => PROJECTS.current ? ($('projectName').value || A.file?.name || 'Untitled project') : 'New project';
  function go(slide) { const slides = [...document.querySelectorAll('.slide')]; const i = slides.findIndex(s=>s.dataset.slide===slide); if(i>=0) DECK.go(i); }
  function stop() {
    document.querySelectorAll('audio,video').forEach(m=>m.pause());
    window.PLAY?.stopAll(); window.ANALYZER?.stop();
  }
  function setMode(mode, project) {
    stop(); W.mode=mode; W.project=project || null; W.index=0;
    document.body.classList.toggle('workspace-project',mode==='project');
    document.body.classList.toggle('workspace-empty',mode==='empty');
    document.querySelectorAll('[data-demo-view]').forEach(n=>{n.hidden=mode!=='demo';n.inert=mode!=='demo';});
    document.querySelectorAll('[data-project-view]').forEach(n=>{n.hidden=mode==='demo';n.inert=mode==='demo';});
    if(W.media) { W.media.removeAttribute('src'); W.media.load(); W.media=null; }
    if(mode==='project') { PLAY.useUpload(); PLAY.setSettings(PROJECTS.content.sampler); }
    if(mode==='demo') { PLAY.state.src='orig'; PLAY.state.bank=0; }
    PLAY.refresh();
    render(); updateHeader(); if($('workspaceMessage')) $('workspaceMessage').textContent='';
    const downloadMenu = document.querySelector('.dl-menu'); if(downloadMenu) downloadMenu.hidden=mode!=='demo';
    const brand = document.querySelector('.deck-brand'); if(brand) brand.setAttribute('aria-label',mode==='demo'?'Back to overview':'Active project overview');
    $('miniSyl').textContent=mode==='demo'?'Original demo':mode==='project'?name():'New project';
    $('miniMeta').textContent=mode==='demo'?'Prepared IMG_3268 atlas':mode==='project'?A.file.name:'Import a recording';
  }
  function updateHeader() {
    $('activeProjectName').textContent=W.mode==='demo'?'Original demo · IMG_3268':name();
    $('activeProjectSelect').replaceChildren(new Option('Original demo · prepared atlas','demo'),new Option('New / empty project','empty'));
    list.forEach(p=>$('activeProjectSelect').add(new Option(p.name,p.id)));
    $('activeProjectSelect').value=W.mode==='demo'?'demo':W.mode==='empty'?'empty':PROJECTS.current?.id || '';
    $('activeProjectSave').disabled=W.mode!=='project';
    // The original brand is an identity label, not a second project's title.
    const title=document.querySelector('.deck-brand-text b'); if(title) title.textContent=W.mode==='demo'?'IMG_3268':name();
    document.title=(W.mode==='demo'?'IMG_3268':name())+' · Phonetic Rhythm Atlas';
  }
  function button(text,action,extra='') { return `<button type="button" class="play-btn" data-project-action="${action}" ${extra}>${text}</button>`; }
  function empty(text) { return `<div class="project-empty"><h3>Not analyzed yet</h3><p>${text}</p>${button('Open project analysis','analyze')}</div>`; }
  function eventButtons(max=100000) {
    return evs().slice(0,max).map((e,i)=>`<button type="button" class="project-event" data-event="${i}"><small>#${e.i} · ${fmt(e.s)}–${fmt(e.e)}</small><strong>${esc(e.label || e.cat)}</strong><code>${e.ipa?'['+esc(e.ipa)+']':'IPA not analyzed'}</code></button>`).join('');
  }
  function render() {
    if(!nodes.size) return;
    for(const [key,pair] of nodes) {
      pair.cap.querySelector('h2').textContent=key==='overview'?name():({watch:'Watch this project',pads:'Project slices',compare:'Project comparison',phrases:'Project phrases',scorecard:'Project scorecard',microscope:'Project microscope',rhythm:'Project rhythm',ipa:'Project phonetics',lyrics:'Project lyrics', 'suno-style':'Project style prompt',events:'Project events',play:'Play this project'})[key];
      pair.cap.querySelector('p').textContent=W.mode==='project'?`Active project: ${name()}. All results here belong to this recording.`:'Create or open a project to populate this workspace.';
      if(key==='play') continue;
      if(W.mode==='demo') continue;
      if(W.mode==='empty' || !A.res) { pair.body.innerHTML='<div class="project-empty"><h3>No active recording</h3><p>Import a song or video, or select a saved project above.</p>'+button('Import a recording','analyze')+'</div>';continue; }
      const r=A.res,c=PROJECTS.content;
      switch(key) {
        case 'overview': pair.body.innerHTML=`<div class="project-summary"><h3>${esc(A.file.name)}</h3><p>${fmt(r.dur)} · ${r.channels===1?'Mono':'Stereo'} · ${r.hits.length} slices · ${r.bpm?Math.round(r.bpm)+' BPM estimate':'Tempo unknown'}</p><div class="project-actions">${button('Watch / listen','watch')}${button('Edit slices','analyze')}${button('Play sampler','play')}</div><div class="project-status-grid"><div class="panel"><h3>Acoustic analysis</h3><p>Measured for this recording: levels, spectrum, rough categories and onset slices.</p></div><div class="panel"><h3>Lyrics and phonetics</h3><p>${evs().some(e=>e.ipa)?'Project IPA annotations available.':c.lyrics?'Project lyrics saved. IPA not analyzed yet.':'Not analyzed yet. Add project lyrics or import timed annotations.'}</p>${button('Open lyrics','lyrics')}</div><div class="panel"><h3>Style prompt</h3><p>${c.stylePrompt?'Project-specific prompt saved.':'Build a draft from this project and your style direction.'}</p>${button('Open prompt builder','suno-style')}</div></div><p class="project-note">The original prepared video, Suno render and scorecard belong to Original demo only.</p></div>`;break;
        case 'watch': renderWatch(pair.body);break;
        case 'pads': pair.body.innerHTML=`<p>${r.hits.length} slices from ${esc(A.file.name)}. Labels and IPA reflect your project edits.</p><div class="project-event-grid">${eventButtons()}</div>`;break;
        case 'events': pair.body.innerHTML=`<p>${evs().length} project events · ${button('Edit slice annotations','analyze')}</p><div class="project-table-wrap"><table class="project-events-table"><thead><tr><th>Time</th><th>Sound / text</th><th>IPA</th><th>Category</th><th>Listen</th></tr></thead><tbody>${evs().map((e,i)=>`<tr><td>${fmt(e.s)}–${fmt(e.e)}</td><td>${esc(e.label||'Unlabeled')}</td><td>${esc(e.ipa||'Not analyzed')}</td><td>${esc(e.cat)}</td><td>${button('Play','event',`data-event-index="${i}"`)}</td></tr>`).join('')}</tbody></table></div>`;break;
        case 'microscope': pair.body.innerHTML=`<p>Inspect this recording's spectrogram, waveform and editable slices in Analyze.</p>${button('Open waveform / spectrogram','analyze')}<div class="project-event-grid">${eventButtons(32)}</div>`;break;
        case 'rhythm': pair.body.innerHTML=`<div class="panel"><h3>${r.bpm?Math.round(r.bpm)+' BPM · estimate':'Tempo unknown'}</h3><p>${r.hits.length} editable slices over ${fmt(r.dur)}. A detailed beat grid and note-value score have not been generated for this project.</p></div><div class="project-onset-strip" aria-label="Onset positions across the recording">${r.hits.map(h=>`<i style="left:${Math.min(100,h.s/r.dur*100)}%" title="${fmt(h.s)}"></i>`).join('')}</div><p>Slice onsets across the full recording; spacing follows source time.</p>${button('Inspect timing','analyze')}`;break;
        case 'ipa': { const annotated=evs().filter(e=>e.ipa); pair.body.innerHTML=annotated.length?`<p>${annotated.length} project IPA annotations. Manual or imported annotations; not inferred from the demo.</p><pre class="project-text">${esc(annotated.map(e=>`${fmt(e.s)} [${e.ipa}] ${e.label}`).join('\n'))}</pre>`:empty('Automatic transcription and narrow-IPA inference are not connected in this build. Enter IPA on a slice, or import timed annotations on Lyrics.');break; }
        case 'lyrics': pair.body.innerHTML=`<p>Lyrics and timed annotations are saved with this project. Automatic transcription/IPA is not connected yet.</p><label class="project-field">Project lyrics<textarea id="workspaceLyrics" rows="10" maxlength="100000" placeholder="Enter or paste lyrics for this recording…">${esc(c.lyrics)}</textarea></label><div class="project-actions">${button('Save lyrics','save-lyrics')}${button('Build draft from labeled events','draft-lyrics')}<label class="play-btn">Import timed annotations<input id="projectAnnotations" type="file" accept=".json,application/json" hidden /></label></div><p class="project-note">Annotation JSON must contain fileName, duration and events [{start,end,text,ipa,category}] matching this source file.</p><p>${evs().filter(e=>e.ipa).length} IPA-annotated events in this project.</p><pre class="project-text">${esc(evs().filter(e=>e.ipa).map(e=>`${fmt(e.s)} [${e.ipa}] ${e.label}`).join('\n') || 'IPA: Not analyzed yet' )}</pre>`;break;
        case 'suno-style': pair.body.innerHTML=`<p>Build a project-specific draft from measured rhythm, corrected labels and your direction. This is an editable template, not a claim that transcription has run.</p><label class="project-field">Style direction<textarea id="workspaceIntent" rows="3" maxlength="100000" placeholder="Genre, instruments, feel, energy…">${esc(c.styleIntent)}</textarea></label>${button('Build prompt from this project','build-prompt')}<label class="project-field">Project Suno prompt<textarea id="workspacePrompt" rows="9" maxlength="100000" placeholder="Build or write a prompt for this recording…">${esc(c.stylePrompt)}</textarea></label>${button('Save prompt','save-prompt')}`;break;
        default: pair.body.innerHTML=empty(key==='phrases'?'No phrase segmentation has been generated for this recording. Its detected slices are available in Pads.':'This project has no paired render or semantic comparison results. The original-vs-Suno comparison is available only in Original demo.');
      }
    }
  }
  function renderWatch(body) {
    if(!W.media) {
      body.innerHTML='<div class="project-watch"><div id="projectMediaSlot"></div><div id="projectCaption" class="project-caption" aria-live="polite">No timed phonetics yet.</div><p id="projectMediaStatus" role="status"></p></div>';
      const video=/^video\//.test(A.file.type)||/\.(mov|mp4|m4v|webm)$/i.test(A.file.name);
      const m=document.createElement(video?'video':'audio');m.id='projectMedia';m.controls=true;m.preload='metadata';m.setAttribute('playsinline','');m.src=A.url;W.media=m;$('projectMediaSlot').append(m);
      m.addEventListener('timeupdate',updateNow);m.addEventListener('play',()=>{$('miniPlay').textContent='❚❚';});m.addEventListener('pause',()=>{$('miniPlay').textContent='▶';});
      m.addEventListener('error',()=>{if($('projectMediaStatus')) $('projectMediaStatus').textContent='This browser cannot play the source container. Audio slices are still available in Analyze and Play.';});
    }
    updateNow();
  }
  function updateNow() {
    if(W.mode!=='project') return;
    const t=W.media?.currentTime||0, e=evs().find(e=>t>=e.s&&t<=e.e);
    $('miniSyl').textContent=name();$('miniMeta').textContent=`${fmt(t)} · ${A.file.name}`;
    if($('projectCaption')) $('projectCaption').textContent=e?`${e.label||e.cat}${e.ipa?' ['+e.ipa+']':' · IPA not analyzed'}`:'No timed text at this position.';
  }
  async function toggle() {
    if(W.mode==='demo') return originalToggle();
    if(!W.media) return go('analyze');
    if(W.media.paused) { ANALYZER.stop();try{await W.media.play();}catch(e){$('workspaceMessage').textContent=e.message;} } else W.media.pause();
  }
  async function playEvent(i) {
    const e=evs()[i];if(!e||!A.buf)return;W.index=i;
    W.media?.pause(); await PLAY.enable();PLAY.sampleSlice(A.buf,e.s,e.e,112);
    $('miniSyl').textContent=e.label||e.cat;$('miniMeta').textContent=`${fmt(e.s)} · ${e.ipa?'['+e.ipa+']':'IPA not analyzed'}`;
  }
  function init() {
    const nav=document.querySelector('.deck-nav'), bar=document.createElement('div');bar.id='workspaceBar';
    bar.innerHTML='<strong id="activeProjectName">Original demo · IMG_3268</strong><label>Active project <select id="activeProjectSelect"><option value="demo">Original demo · prepared atlas</option></select></label>'+button('New project','new')+button('Manage / import','analyze')+'<button type="button" class="play-btn" id="activeProjectSave">Save project</button><span id="workspaceMessage" role="status"></span>';
    nav.after(bar);
    document.querySelectorAll('.slide').forEach(slide=>{
      if(slide.dataset.slide==='analyze')return;
      const key=slide.dataset.slide,cap=slide.querySelector(':scope > .slide-cap'),body=slide.querySelector(':scope > .slide-body');
      cap.dataset.demoView='';if(key!=='play')body.dataset.demoView='';
      const pc=document.createElement('div');pc.className='slide-cap';pc.dataset.projectView='';pc.hidden=true;pc.innerHTML='<div class="slide-eyebrow">Active project</div><h2></h2><p></p>'+button('Manage this project','analyze');
      const pb=key==='play'?body:document.createElement('div');if(key!=='play'){pb.className='slide-body project-view-body';pb.dataset.projectView='';pb.hidden=true;slide.append(pc,pb);}else slide.insertBefore(pc,body);
      nodes.set(key,{cap:pc,body:pb});
    });
    $('activeProjectSelect').addEventListener('change',async event=>{
      const id=event.target.value; event.target.disabled=true;
      try { if(id==='demo')await PROJECTS.demo();else if(id==='empty')PROJECTS.newProject();else await PROJECTS.open(id); }
      catch(e){$('workspaceMessage').textContent=e.message;}finally{event.target.disabled=false;}
    });
    $('activeProjectSave').addEventListener('click',()=>PROJECTS.save());
    document.addEventListener('click',async e=>{
      const item=e.target.closest('[data-project-action],[data-event]');if(!item)return;
      if(item.dataset.event!=null)return playEvent(+item.dataset.event);
      const action=item.dataset.projectAction;
      if(action==='event')return playEvent(+item.dataset.eventIndex);
      if(action==='new')return PROJECTS.newProject();
      if(action==='save-lyrics'){PROJECTS.setContent({lyrics:$('workspaceLyrics').value});$('workspaceMessage').textContent='Project lyrics updated; saving…';return;}
      if(action==='draft-lyrics'){const lyrics=evs().filter(x=>x.label).map(x=>x.label).join(' ');if(!lyrics){$('workspaceMessage').textContent='Label slices or import timed text first.';return;}PROJECTS.setContent({lyrics});return;}
      if(action==='save-prompt'){PROJECTS.setContent({styleIntent:$('workspaceIntent').value,stylePrompt:$('workspacePrompt').value});return;}
      if(action==='build-prompt'){const c={...PROJECTS.content,styleIntent:$('workspaceIntent').value};PROJECTS.setContent({...c,stylePrompt:model.prompt(A.res,c)});return;}
      go(action);
    });
    document.addEventListener('change',async e=>{
      const keys={workspaceLyrics:'lyrics',workspaceIntent:'styleIntent',workspacePrompt:'stylePrompt'};
      if(keys[e.target.id]) { PROJECTS.setContent({[keys[e.target.id]]:e.target.value},false); return; }
      if(e.target.id!=='projectAnnotations')return;
      try{const file=e.target.files[0];if(!file)return;if(file.size>4*1024*1024)throw new Error('Annotation JSON must be under 4 MB.');const annotations=model.importAnnotations(JSON.parse(await file.text()),A.file.name,A.res.dur);PROJECTS.setContent({annotations});$('workspaceMessage').textContent='Timed annotations imported for this project.';}catch(err){$('workspaceMessage').textContent=err.message;}
    });
    // Capture project transport keys before the legacy demo's global handlers.
    window.addEventListener('keydown',e=>{
      if(W.mode==='demo'||e.target.closest('input,textarea,select,[contenteditable]')||e.metaKey||e.ctrlKey||e.altKey)return;
      if(e.code==='Space'||e.key==='.'||e.key===','||e.key.toLowerCase()==='l'){
        e.preventDefault();e.stopImmediatePropagation();
        if(e.code==='Space')toggle();else if(e.key==='.'||e.key===',')playEvent(Math.max(0,Math.min(evs().length-1,W.index+(e.key==='.'?1:-1))));else if(W.media){W.media.loop=!W.media.loop;$('workspaceMessage').textContent=W.media.loop?'Loop recording on':'Loop recording off';}
      }
    },true);
    $('miniPlay').addEventListener('click',e=>{if(W.mode!=='demo'){e.preventDefault();e.stopImmediatePropagation();toggle();}},true);
    window.togglePlayPause=toggle;
    window.addEventListener('atlas:project-loading',()=>{stop();$('workspaceMessage').textContent='Opening project…';});
    window.addEventListener('atlas:project-activated',e=>setMode('project',e.detail));
    window.addEventListener('atlas:project-cleared',()=>setMode('empty'));
    window.addEventListener('atlas:demo',()=>setMode('demo'));
    window.addEventListener('atlas:project-edited',()=>{if(W.mode==='project'){render();updateHeader();}});
    window.addEventListener('atlas:project-list',e=>{list=e.detail;updateHeader();});
    document.getElementById('projectName').addEventListener('input',()=>{if(W.mode==='project'){updateHeader();for(const pair of nodes.values())pair.cap.querySelector('p').textContent=`Active project: ${name()}. All results here belong to this recording.`;}});
    PROJECTS.list().then(items=>{list=items;updateHeader();}).catch(e=>{$('workspaceMessage').textContent=e.message;});
    const observer=new MutationObserver(()=>{if(W.mode==='project')render();});
    document.querySelectorAll('.slide').forEach(s=>observer.observe(s,{attributes:true,attributeFilter:['class']}));
    document.querySelector('#pane-play').addEventListener('change',()=>{if(W.mode==='project')PROJECTS.setContent({sampler:PLAY.getSettings()},false);});
    updateHeader();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
