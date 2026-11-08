(function (root) {
  'use strict';
  function content(value = {}) {
    const text = (key) => typeof value[key] === 'string' ? value[key].slice(0, 100000) : '';
    return { lyrics: text('lyrics'), styleIntent: text('styleIntent'), stylePrompt: text('stylePrompt'), annotations: Array.isArray(value.annotations) ? value.annotations : [], sampler: value.sampler && typeof value.sampler === 'object' ? value.sampler : {} };
  }
  function events(result, value) {
    const c = content(value);
    if (c.annotations.length) return c.annotations.map((e,i) => ({ i:i+1, s:e.start, e:e.end, label:e.text || '', ipa:e.ipa || '', cat:e.category || 'PERC' }));
    return (result?.hits || []).map((h) => ({ ...h, label:h.label || '', ipa:h.ipa || '' }));
  }
  function importAnnotations(data, fileName, duration) {
    if (!data || data.fileName !== fileName || !Number.isFinite(data.duration) || Math.abs(data.duration-duration) > .05 || !Array.isArray(data.events) || data.events.length > 10000) throw new Error('Annotations must name this source file and match its duration.');
    return data.events.map((e) => {
      if (!Number.isFinite(e.start) || !Number.isFinite(e.end) || e.start < 0 || e.end > duration || e.end <= e.start) throw new Error('Annotation times must stay inside this recording.');
      for (const k of ['text','ipa','category']) if (e[k] != null && (typeof e[k] !== 'string' || e[k].length > 1000)) throw new Error('Invalid annotation text.');
      return { start:e.start,end:e.end,text:e.text || '',ipa:e.ipa || '',category:e.category || 'PERC' };
    }).sort((a,b) => a.start-b.start);
  }
  function prompt(result, value) {
    const c = content(value), cats = [...new Set((result?.hits || []).map(h=>h.cat.toLowerCase()))];
    return [c.styleIntent.trim(), result?.bpm ? `Tempo reference: approximately ${Math.round(result.bpm)} BPM; retain the source feel.` : 'Keep the source rhythmic feel.', cats.length ? `Detected sound categories (rough estimates): ${cats.join(', ')}.` : '', 'Use the project lyrics and corrected pronunciation; preserve intentional pauses and accents.'].filter(Boolean).join('\n');
  }
  root.AtlasProjectModel = { content, events, importAnnotations, prompt };
  if (typeof module !== 'undefined') module.exports = root.AtlasProjectModel;
})(typeof window !== 'undefined' ? window : globalThis);
