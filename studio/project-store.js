/* Versioned local project storage. Media stays in this browser. */
(function (root) {
  'use strict';
  const VERSION = 1;
  function bounds(start, end, duration) {
    if (![start, end, duration].every(Number.isFinite) || start < 0 || end > duration || end - start < 0.005 - 1e-9) {
      throw new Error('Keep the slice inside the recording, with at least 5 ms between start and end.');
    }
    return { s: start, e: end };
  }
  function validateProject(p) {
    if (!p || p.version !== VERSION || typeof p.id !== 'string' || !p.id || typeof p.name !== 'string' ||
        !(p.media instanceof Blob) || !p.result || !Number.isFinite(p.result.dur) || p.result.dur <= 0 || !Array.isArray(p.result.hits)) {
      throw new Error('This project is incomplete or uses an unsupported format.');
    }
    const ids = new Set();
    const r = p.result;
    if (!Number.isInteger(r.specRows) || r.specRows < 1 || r.specRows > 256 ||
        !Number.isInteger(r.specCols) || r.specCols < 1 || r.specCols > 2000 ||
        !r.spec || r.spec.length !== r.specRows * r.specCols ||
        !Array.isArray(r.wf) || r.wf.length < 2 || r.wf.length > 10000 || r.wf.length % 2 ||
        !r.wf.every(Number.isFinite) || !Array.isArray(r.bands) || r.bands.length > 20 ||
        !r.bands.every((b) => ['sub', 'low', 'lowmid', 'mid', 'presence', 'air', 'top'].includes(b.name) && Number.isFinite(b.db)) ||
        !['sr', 'channels', 'peakDb', 'rmsDb', 'lufs', 'lra', 'centroid', 'bpm', 'onsetsPerSec', 'fmin', 'fmax'].every((k) => Number.isFinite(r[k])) ||
        r.hits.length > 100000 || typeof p.fileName !== 'string' || p.fileName.length > 255) {
      throw new Error('Project analysis is invalid or exceeds supported limits.');
    }
    for (const h of p.result.hits) {
      bounds(h.s, h.e, p.result.dur);
      if (!Number.isInteger(h.i) || h.i < 1 || ids.has(h.i)) throw new Error('Invalid slice IDs in project.');
      ids.add(h.i);
      if (!['KICK', 'SNARE', 'HAT', 'TONAL', 'PERC', 'BREATH'].includes(h.cat) ||
          (h.label != null && (typeof h.label !== 'string' || h.label.length > 100)) ||
          (h.ipa != null && (typeof h.ipa !== 'string' || h.ipa.length > 200))) {
        throw new Error('Project slice metadata is invalid.');
      }
    }
    return p;
  }
  let opening;
  function db() {
    if (!opening) opening = new Promise((resolve, reject) => {
      const request = indexedDB.open('rhythm-atlas-projects', VERSION);
      request.onupgradeneeded = () => request.result.createObjectStore('projects', { keyPath: 'id' });
      request.onsuccess = () => {
        const connection = request.result;
        connection.onversionchange = () => { connection.close(); opening = null; };
        resolve(connection);
      };
      request.onerror = () => { opening = null; reject(request.error); };
      request.onblocked = () => { opening = null; reject(new Error('Close other Atlas tabs and retry project storage.')); };
    });
    return opening;
  }
  async function transaction(mode, action) {
    const connection = await db();
    return new Promise((resolve, reject) => {
      const tx = connection.transaction('projects', mode);
      const req = action(tx.objectStore('projects'));
      tx.oncomplete = () => resolve(req.result);
      tx.onerror = () => reject(tx.error || req.error || new Error('Project storage failed.'));
      tx.onabort = () => reject(tx.error || new Error('Project save was interrupted.'));
    });
  }
  root.AtlasProjects = {
    VERSION, bounds, validateProject,
    save: (p) => transaction('readwrite', (s) => s.put(validateProject(p))),
    get: (id) => transaction('readonly', (s) => s.get(id)),
    list: async () => (await transaction('readonly', (s) => s.getAll())).map(({ id, name, updatedAt }) => ({ id, name, updatedAt })).sort((a,b) => b.updatedAt - a.updatedAt)
  };
  if (typeof module !== 'undefined') module.exports = root.AtlasProjects;
})(typeof window !== 'undefined' ? window : globalThis);
