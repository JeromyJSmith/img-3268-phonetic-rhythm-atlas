const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const store = require('../studio/v2/project-store.js');
const html = fs.readFileSync(require.resolve('../index.html'), 'utf8');
const workerSource = html.split('  const WORKER_SRC = `')[1].split('`;')[0];
function analyze(chs, sr) {
  let result;
  const sandbox = { postMessage(m) { if (m.type === 'done') result = m.res; } };
  vm.createContext(sandbox);
  vm.runInContext(workerSource, sandbox);
  sandbox.onmessage({ data: { chs, sr } });
  assert.ok(result, 'Worker must finish');
  return result;
}
function project(result) {
  return { version: 1, id: 'test-id', name: 'Test', fileName: 'test.wav', media: new Blob(['audio']), result };
}
test('all inline scripts parse', () => {
  const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)];
  assert.ok(scripts.length > 3);
  scripts.forEach((match) => new vm.Script(match[1]));
});
test('slice boundaries reject reversed, zero, negative, nonfinite and out-of-range edits', () => {
  assert.deepEqual(store.bounds(0, .005, 1), { s: 0, e: .005 });
  for (const args of [[1,0,2], [0,0,2], [-1,1,2], [0,3,2], [NaN,1,2], [0,Infinity,2]]) {
    assert.throws(() => store.bounds(...args));
  }
});
test('silent input has no hits, finite levels and no spurious tempo', () => {
  const r = analyze([new Float32Array(16000)], 8000);
  assert.equal(r.hits.length, 0);
  assert.equal(r.bpm, 0);
  assert.equal(r.dur, 2);
  assert.ok(Number.isFinite(r.lufs));
  assert.equal(store.validateProject(project(r)).version, 1);
});
test('short input completes and can be saved', () => {
  const r = analyze([new Float32Array(80)], 8000);
  assert.equal(r.specCols, 1);
  assert.equal(r.dur, .01);
  store.validateProject(project(r));
});
test('rhythmic transients create bounded slices and valid project data', () => {
  const sr = 16000, x = new Float32Array(sr * 4);
  for (let onset = .25; onset < 4; onset += .5) {
    for (let i = 0; i < 1000 && onset * sr + i < x.length; i++) x[Math.floor(onset * sr) + i] = Math.exp(-i / 200) * Math.sin(i * .3);
  }
  const r = analyze([x], sr);
  assert.ok(r.hits.length >= 6, 'Detect most pulse onsets');
  assert.ok(r.bpm >= 60 && r.bpm <= 200);
  r.hits.forEach((h) => store.bounds(h.s, h.e, r.dur));
  store.validateProject(project(r));
  const edited = structuredClone(r);
  edited.hits[0].label = '<script>sample name</script>';
  edited.hits[0].ipa = 'bʌm';
  edited.hits[0].e = edited.hits[0].s + .02;
  store.validateProject(project(edited));
  assert.notEqual(edited.hits[0].e, r.hits[0].e, 'Corrections are non-destructive');
  const portable = JSON.parse(JSON.stringify({ ...project(edited), result: { ...edited, spec: Array.from(edited.spec) } }));
  portable.media = new Blob(['audio']);
  store.validateProject(portable);
  assert.equal(portable.result.hits[0].ipa, 'bʌm');
});
test('stereo anti-phase input preserves level measurement and channel count', () => {
  const x = Float32Array.from({ length: 16000 }, (_, i) => .2 * Math.sin(2 * Math.PI * 440 * i / 8000));
  const r = analyze([x, x.map((v) => -v)], 8000);
  assert.equal(r.channels, 2);
  assert.ok(r.corr < -.99);
  assert.ok(r.lufs > -70, 'Measure stereo channels before mono downmix');
});
test('malformed or future project versions fail before restoration', () => {
  const p = project(analyze([new Float32Array(800)], 8000));
  assert.throws(() => store.validateProject({ ...p, version: 2 }));
  assert.throws(() => store.validateProject({ ...p, media: 'data:...' }));
  assert.throws(() => store.validateProject({ ...p, result: { ...p.result, specCols: 1e9 } }));
  assert.throws(() => store.validateProject({ ...p, result: { ...p.result, hits: [{ i:1, s:0, e:.05, cat:'<bad>' }] } }));
});
function analyzerHarness(decode) {
  const elements = new Map();
  const element = (id) => {
    if (!elements.has(id)) elements.set(id, { hidden: false, textContent: '', style: {}, dataset: {}, clientWidth: 0, innerHTML: '' });
    return elements.get(id);
  };
  const workers = [];
  const events = [];
  const sandbox = {
    document: { getElementById: element, readyState: 'loading', addEventListener() {}, querySelectorAll: () => [], querySelector: () => null },
    Blob, File, URL, Float32Array, Uint8Array, crypto, setTimeout, clearTimeout,
    cancelAnimationFrame() {}, CustomEvent: class { constructor(type, options) { this.type = type; this.detail = options?.detail; } },
    Worker: class { constructor() { workers.push(this); } postMessage() {} terminate() { this.terminated = true; } },
    PLAY: { prepare: () => {}, enable: async () => {}, state: { ctx: { decodeAudioData: decode } }, setUpload() {} },
    dispatchEvent(event) { events.push(event); }
  };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  const code = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map((m) => m[1]).find((x) => x.includes('const WORKER_SRC ='));
  vm.runInContext(code, sandbox);
  const buf = { sampleRate: 8000, duration: 1, numberOfChannels: 1, getChannelData: () => new Float32Array(8000) };
  const file = new File(['audio'], 'test.wav', { type: 'audio/wav' });
  return { sandbox, elements, workers, events, buf, file };
}
test('worker errors leave the busy screen and expose an actionable failure', async () => {
  const h = analyzerHarness(async () => h.buf);
  await h.sandbox.ANALYZER.handleFile(h.file);
  assert.equal(h.workers.length, 1);
  h.workers[0].onerror({ message: 'Worker blocked' });
  assert.equal(h.elements.get('anBusy').hidden, true);
  assert.equal(h.elements.get('anEmpty').hidden, false);
  assert.match(h.elements.get('anEmptyMsg').textContent, /Worker blocked/);
  assert.equal(h.workers[0].terminated, true);
});
test('cancelled decode cannot create a worker or replace the next import', async () => {
  const decodes = [];
  const h = analyzerHarness(() => new Promise((resolve) => decodes.push(resolve)));
  const first = h.sandbox.ANALYZER.handleFile(h.file);
  await new Promise(setImmediate);
  h.sandbox.ANALYZER.cancel();
  decodes[0](h.buf);
  await first;
  assert.equal(h.workers.length, 0);
  const second = h.sandbox.ANALYZER.handleFile(h.file);
  await new Promise(setImmediate);
  decodes[1](h.buf);
  await second;
  assert.equal(h.workers.length, 1);
  h.sandbox.ANALYZER.cancel();
});
test('replaced worker errors cannot interrupt a newer job', async () => {
  const h = analyzerHarness(async () => h.buf);
  await h.sandbox.ANALYZER.handleFile(h.file);
  const old = h.workers[0];
  await h.sandbox.ANALYZER.handleFile(h.file);
  assert.equal(old.terminated, true);
  old.onerror({ message: 'Stale error' });
  assert.equal(h.elements.get('anBusy').hidden, false);
  h.sandbox.ANALYZER.cancel();
});
test('unsupported audio decoding produces a visible error without starting analysis', async () => {
  const h = analyzerHarness(async () => { throw new Error('Unsupported codec'); });
  await h.sandbox.ANALYZER.handleFile(h.file);
  assert.equal(h.workers.length, 0);
  assert.match(h.elements.get('anEmptyMsg').textContent, /Unsupported codec/);
});
test('decoding does not wait for the browser playback permission', async () => {
  const h = analyzerHarness(async () => h.buf);
  h.sandbox.PLAY.enable = () => { throw new Error('Playback activation must not block import'); };
  await h.sandbox.ANALYZER.handleFile(h.file);
  assert.equal(h.workers.length, 1);
  h.sandbox.ANALYZER.cancel();
});
test('optional project text is backward compatible and annotations are bounded', () => {
  const p = project(analyze([new Float32Array(8000)], 8000));
  assert.equal(store.validateProject(p), p);
  const content = {lyrics:'Project A',styleIntent:'dub',stylePrompt:'My prompt',annotations:[{start:0,end:.5,text:'hi',ipa:'haɪ'}],sampler:{ctlVol:'50'}};
  assert.equal(store.validateProject({...p,content}).content.lyrics,'Project A');
  assert.throws(()=>store.validateProject({...p,content:{annotations:[{start:0,end:2}]}}));
  assert.throws(()=>store.validateProject({...p,content:{lyrics:7}}));
});
