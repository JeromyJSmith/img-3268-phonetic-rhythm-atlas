# Rhythm Atlas studio research and next decisions

Research pass: 2026-11-07 (America/Denver).
Status: source/document investigation; implementation choices remain subject to
browser/audio compatibility tests. Use alongside [ROADMAP.md](../ROADMAP.md).

## Product contract

Build our own BandLab-like browser studio around the existing Atlas look and
analysis: import audio/video, correct phonetics and slices, play polyphonically,
use in-app devices and third-party web effects, save projects, separate stems,
sequence/remix material, and eventually host native plug-ins and integrate with
Ableton. Preserve a fun, readable dark amber/cyan interface.

In-app tracks, mixer and device chains are required. Ableton is an additional
integration destination. Keep original media, generated analysis and manual
corrections distinct; a new analysis must never silently erase edits.

## Current implementation evidence

Inspected local source commit `cfda233` and matching remote tree
`5d63d56fa18980b58dde8fa5392e1f5dd286aa1c`, represented by draft
[PR #1](https://github.com/JeromyJSmith/img-3268-phonetic-rhythm-atlas/pull/1).

| Finding | Source evidence | Consequence |
| --- | --- | --- |
| Sampler is already polyphonic | `index.html`, `sampleVoice`, `padOn`, `padVoices` map | Extend the existing engine instead of replacing it with a generic synth |
| Pads and oscillator share one filter/master path | `ensureCtx`: padBus/synBus -> S.fx -> master -> compressor -> analyzer/output | Add track/device-bus abstraction before claiming a real mixer |
| Timeline audition bypasses that filter | Analyzer `playFrom` connects source directly to `PLAY.state.master` | Route all intended auditions through the same selected-track chain |
| Project v1 persists media and analysis/corrected slices | `studio/project-store.js`, `studio/projects.js` | Introduce a migration for device state, mappings, routing and later tracks |
| New-upload full phonetics are absent | Browser worker computes measurements/onsets; original Python scripts are recording/path-specific | Treat a reusable analysis service as separate implementation work |
| First foundation has automated coverage | `node --test tests/foundation.test.cjs`: 11 pass | DSP/validation/job-state checks pass; this is not browser/audio QA |
| Browser review is pending | Connected browser could not reach workspace localhost: connection refused | Do not merge/deploy on the strength of unit tests alone |

## Hosting and persistence boundaries

GitHub Pages can continue serving the static UI; it does not execute a Python
analysis server. Run heavy analysis in a tested browser-capable worker/model or
a separately configured local/remote processing service. Default to a local
service prototype before choosing external processing destinations for media.

Browser storage is quota-managed and can be evicted. Keep explicit save status,
quota/error handling and portable backups. Investigate `navigator.storage.estimate`
and persistent-storage availability, without presenting either as a backup.
Store decoded audio carefully: models, PCM copies and undo history can dominate
memory even when compressed media is small.

Sources:
- [GitHub Pages hosting limits](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [Browser storage quotas and eviction](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria)
- [Storage estimate API](https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/estimate)

## In-app chains and browser plug-ins

Decision: prototype a WAM host around our existing engine; use openDAW as
architecture inspiration for now. Preserve the current UI and project work.

| Candidate | Decision | Source finding | Remaining test |
| --- | --- | --- | --- |
| WAM2 SDK | Prototype | Web modules expose audio nodes, parameter/events and saved-state interfaces | Load one built plug-in, restore its state, test lifecycle and audio |
| PingPongDelay example | Compatibility target | Native delay/stereo/feedback graph; SDK parameter manager | Resolve package `UNLICENSED` vs root MIT discrepancy before vendoring/distributing; test packaged build |
| Quadrafuzz example | Second order/automation target | Filtered bands with waveshapers; parameter changes rebuild curves | Same licence metadata discrepancy; measure parameter-update cost |
| openDAW SDK | Borrow architecture; defer engine replacement | Separates project graph, UI, worklet and workers; SDK 0.0.182 declares AGPL-3.0-or-later | Evaluate adoption scope before choosing an engine migration |

Pinned WAM SDK revision: `d425ee7ec0479b2a2ee0940374242356997b8ba6`.
The actual source API is:

```js
const [groupId] = await initializeWamHost(audioContext);
const { default: Plugin } = await import(compatibleBuiltPluginUrl);
const instance = await Plugin.createInstance(groupId, audioContext);
await instance.audioNode.setState(savedState); // restore explicitly after creation
```

The inspected base `initialize(state)` does not forward state to
`createAudioNode`, so passing initial state to the factory alone is insufficient
for that base implementation. Verify behavior for each chosen device. The old
README factory examples do not match the current pinned source signature.

The inspected SDK has a message-port event path when shared-memory event queues
are not enabled. SharedArrayBuffer/cross-origin isolation is therefore not a
universal WAM requirement; verify requirements of the selected plug-in/build.
Raw source with bare package imports is not automatically a deployable plug-in.

Sources:
- [SDK host initialization](https://github.com/webaudiomodules/sdk/blob/d425ee7ec0479b2a2ee0940374242356997b8ba6/src/initializeWamHost.js)
- [Factory and initialization](https://github.com/webaudiomodules/sdk/blob/d425ee7ec0479b2a2ee0940374242356997b8ba6/src/WebAudioModule.js)
- [Node state/parameter/event lifecycle](https://github.com/webaudiomodules/sdk/blob/d425ee7ec0479b2a2ee0940374242356997b8ba6/src/WamNode.js)
- [Example host](https://github.com/webaudiomodules/wam-examples/blob/2179e50cf7bbc1f038a6e423651d9915505621f8/packages/host/main.js)
- [Delay graph](https://github.com/webaudiomodules/wam-examples/blob/2179e50cf7bbc1f038a6e423651d9915505621f8/packages/pingpongdelay/src/Node.js), [package metadata](https://github.com/webaudiomodules/wam-examples/blob/2179e50cf7bbc1f038a6e423651d9915505621f8/packages/pingpongdelay/package.json)
- [Quadrafuzz graph](https://github.com/webaudiomodules/wam-examples/blob/2179e50cf7bbc1f038a6e423651d9915505621f8/packages/quadrafuzz/src/Node.js)
- [openDAW architecture](https://github.com/andremichelle/openDAW/blob/516b197f0610ede0081c5ea8f7ed0829b78cb271/introduction.md), [SDK licence/version](https://github.com/andremichelle/openDAW/blob/516b197f0610ede0081c5ea8f7ed0829b78cb271/packages/studio/sdk/package.json)

## Analysis and stems

Decision: immediate browser preview/correction plus cancellable local Python
jobs. Keep MIR, stems, transcription and phonetic measurements independently
replaceable, with explicit provenance and human overrides.

| Candidate | Decision | Scope and gap |
| --- | --- | --- |
| librosa | Prototype classical MIR baseline | ISC algorithms without weights; onset/beat/chroma features, including time-varying BPM input. A toolkit, not a universal chord or phonetic engine. |
| Essentia / Essentia.js | Compare selected algorithms | AGPL/commercial options; confirm actual JS exports. Classical ChordsDetection is experimental and restricted to major/minor triads; RhythmExtractor2013 requires 44.1 kHz. |
| Audio Separator | Prototype swappable stem adapter | MIT wrapper; select exact checkpoint, terms, configuration and hash independently. Lead/backing labels do not identify individual singers. |
| WhisperX | Prototype ordinary speech/lyric timing | BSD-2-Clause code; language/model-specific alignment and optional diarization. Models/dependencies have separate terms. Not universal beatbox IPA or overlap separation. |
| Praat / Parselmouth | Acoustic reference and possible integration | Classical pitch/formant/intensity tools; GPLv3 integration considerations. Measurements alone do not identify narrow articulation. |
| MedleyVox | Evaluation/research only | Dedicated simultaneous-singer research; README states no pretrained weights planned. Dataset is CC-BY-NC-SA 4.0. Not a ready feature implementation. |

Use a staged pipeline:

1. Preserve original media; derive analysis PCM with channel/resampling/offset metadata.
2. Produce quick browser waveform, spectrogram and onset proposals.
3. Optionally separate stems; let the user group/include/exclude/select sources.
4. Propose beats/tempo map, tuning, key alternatives and chord intervals, with unknown states.
5. Propose transcript/timing where applicable; keep nonverbal/beatbox sound labels.
6. Attach acoustic/voicing/formant evidence and editable phonetic tiers.
7. Generate steerable Suno text from corrected events, chosen sources and user intent.

Do not gate a useful sampler release on universal automatic narrow IPA. Keep
manual corrections authoritative. Do not assume wrapper licences establish
weight rights. A historical Demucs maintainer statement limits specific weights
to scientific purposes; check exact current checkpoint terms rather than treating
that statement as a blanket current conclusion for every model.

Sources inspected by the analysis research lane:
- [librosa beat source](https://github.com/librosa/librosa/blob/main/librosa/beat.py), blob `c4c9a7805e355b8b18d3954bffd1dbed25ff3e0a`
- [Essentia chord scope](https://essentia.upf.edu/reference/std_ChordsDetection.html), [rhythm input requirements](https://essentia.upf.edu/reference/std_RhythmExtractor2013.html), [licensing](https://essentia.upf.edu/licensing_information.html)
- [Audio Separator dispatch](https://github.com/nomadkaraoke/python-audio-separator/blob/main/audio_separator/separator/separator.py), blob `a71f3f8e12c94cb48841ce2a89701f70fa3e2fd3`
- [WhisperX alignment](https://github.com/m-bain/whisperX/blob/main/whisperx/alignment.py), blob `378a24f8cc156c7a67aa8552b47c54a3d8e4c050`; [documented limitations](https://github.com/m-bain/whisperX/blob/main/README.md#limitations)
- [Praat](https://www.fon.hum.uva.nl/praat/), [Parselmouth](https://github.com/YannickJadoul/Parselmouth)
- [MedleyVox](https://github.com/jeonchangbin49/MedleyVox), README blob `c49ee5ef5923475fc609eb680a3f4a96ac954bad`; [dataset terms](https://zenodo.org/records/7984549)
- [Historical Demucs weight statement](https://github.com/facebookresearch/demucs/issues/327#issuecomment-1134828611)

## Ordered next work

1. Finish browser QA of draft PR #1: real import, cancel/retry, edit/audition,
   save, reload, reopen and portable backup round trip. Verify polyphony/MIDI and
   layout. The existing 11 passing tests do not substitute for this check.
2. Prototype one shared selected-track bus and ordered in-app chain. Route both
   pad voices and timeline audition through it. Start with built-in reference
   gain/filter plus one compatible WAM effect.
3. Migrate project v1 to persist stable device IDs, order, module/version, bypass,
   opaque node state, mappings and routing. Keep runtime AudioNodes out of JSON;
   retain missing-device state in a recoverable placeholder.
4. Test add/remove/reorder/bypass, parameter changes, save/reopen, tails, clipping,
   timing and live/offline agreement. Resolve dependency/version/licence questions
   for the exact plug-in artifact before distribution.
5. Build the local analysis-job contract and deterministic MIR baseline; evaluate
   one licensed stem checkpoint and one speech/alignment pipeline separately.
6. Add a sample-backed pitched keyboard, sequencing/swing/triplets and validated
   stretch processing; then expand to cross-project arrangement and harmony.

First complete studio journey:
**import -> correct slice -> play overlapping keys -> hear/edit device chain ->
save -> reopen with media, mappings and device state intact.**

## Evaluation media and evidence limits

Use ten short owned/generated fixtures: silence, impulse/clicks, drifting tempo,
known chords/key, ordinary speech, isolated singing, Jero's beatboxing, a known
stem mix, overlapping speech and overlapping singers. Add a video clap/sync test
for the watch/caption workflow. Record onset/beat error, octave/half/double-tempo
mistakes, key/chord alternatives, separation bleed/alignment, transcript coverage,
manual correction effort, peak memory, runtime and persistence failure behavior.

Three research lanes inspected documentation/source, not live audio behavior.
No models were installed or benchmarked; no recordings were sent to an analysis
service. No REA MCP/native capture was performed; the research applied its
feature-tracing and evidence/unknown method to available source. Performance,
voice separation and phonetic accuracy remain evaluation questions.

## Sampler, spectral editing and remix choices

| Goal | Source finding | Decision and theme | Acceptance test |
| --- | --- | --- | --- |
| Polyphonic sample keyboard | Tone Sampler allocates sources per attack and repitches via playbackRate, so pitch changes duration | Retain our voice engine; explicit gate/one-shot, repeated-note handling and panic; same slice map for keyboard/pads | Chords/repeated notes/note-off/sustain/panic and source-switch checks |
| Waveform slice handles | wavesurfer Regions exposes IDs, start/end, resize/update/completed-update events | Prototype adapter to our project commands; amber start/cyan end handles and numeric bounds | Impulse-accurate edits, undo checkpoints, save/reopen |
| Frequency brushing | wavesurfer frequencyMin/frequencyMax crop visualization; they do not filter audio | Shared time/frequency selection drives a separate audible processor; avoid duplicate transports | Sweep/vocal A-B proves band filtering, settings survive reopen |
| Rhythm feel | Tone Transport schedules by ticks and applies swing separately | Prototype transport adapter; rational beat positions, distinct triplet/swing controls, seeded variations | Multiple tempos, true triplet timing, intended swing subdivisions and reproducible patterns |
| Independent stretch/pitch | Signalsmith browser wrapper exposes separate rate/semitones/formants and latency | Prototype on sustained tracks/clips first; avoid expensive stretch instance per drum voice without benchmarks | Pitch/duration independence, seeks, loop seams, latency and two-track CPU |
| Cross-project remix | None of these libraries supplies our full project model | Own versioned asset/slice/track/clip/pattern/device model; source references and missing-asset recovery | Two projects combine and reconstruct after portable export/import |

Inspected candidates: Tone development revision
`105c04cc00289caf49684ac5c7621bce8a042c4c` (package 15.5.66, MIT), wavesurfer
`9fbcf154461031e070bcc11817e7047aea5c7f58` (package 8.0.5, BSD-3-Clause),
Signalsmith Stretch `88061fd4eda56a2353c5d65c74aa3f4ccf76f9da` (web package 1.3.2,
MIT). These are inspected source/package declarations, not tested installed
releases. Signalsmith's future schedule replacement/cancellation behavior needs
an explicit test because documentation and inspected field usage differ; don't
call that a confirmed bug without reproducing it.

Sources:
- [Tone voice allocation/pitch](https://github.com/Tonejs/Tone.js/blob/105c04cc00289caf49684ac5c7621bce8a042c4c/Tone/instrument/Sampler.ts#L258)
- [Tone transport/swing](https://github.com/Tonejs/Tone.js/blob/105c04cc00289caf49684ac5c7621bce8a042c4c/Tone/core/clock/Transport.ts#L239)
- [wavesurfer region contract](https://github.com/katspaugh/wavesurfer.js/blob/9fbcf154461031e070bcc11817e7047aea5c7f58/src/plugins/regions.ts#L34)
- [Spectrogram settings/rendering](https://github.com/katspaugh/wavesurfer.js/blob/9fbcf154461031e070bcc11817e7047aea5c7f58/src/spectrogram-setup.ts#L100)
- [Signalsmith browser wrapper](https://github.com/Signalsmith-Audio/signalsmith-stretch/blob/88061fd4eda56a2353c5d65c74aa3f4ccf76f9da/web/web-wrapper.js#L18)
- [Signalsmith web API](https://github.com/Signalsmith-Audio/signalsmith-stretch/blob/88061fd4eda56a2353c5d65c74aa3f4ccf76f9da/web/release/README.md)

## Reconciliation result

All three lanes converge on incremental adapters around the current sampler and
shared project state. Prototype web plug-in hosting now; keep analysis services
and clip stretching separable. Borrow full-DAW interaction/architecture ideas
without committing to an engine replacement. Native hosting, simultaneous-singer
separation and universal beatbox narrow IPA remain separate research/build goals.
