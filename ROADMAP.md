# Rhythm Atlas: analysis, sampler, remix and Ableton plan

Status: agreed product direction; implementation begins with milestone 1.
Date: 2026-11-07

Implementation checkpoint (2026-11-08): project/slice editor release prepared\nfor main. Eleven automated checks pass; Chrome preview verified demo analysis,\nslice edits/undo and save/reload/reopen. Versioned asset URLs ensure new scripts\nload after deployment. Backup generation is verified; exported-file reimport is\nunverified because the connected browser does not support blob downloads.\nHardware MIDI/listening and other browser/device checks remain pending.\n
## Product goal

Keep the existing dark amber/cyan studio interface and playful feel. Make any
recording a saved, editable project: analyze it, correct phonetics and slices,
separate stems, generate steerable Suno prompts, play samples polyphonically,
sequence rhythms, shape frequencies, and remix material from other projects.
Build a BandLab-like standalone studio with our own tracks, mixer, instruments
and in-app device chains. Eventually integrate with Ableton Live and use
favorite native plug-ins within our application.

The existing prepared IMG_3268 atlas remains available. Build incrementally on
the current app rather than discard its analysis, media, or visual identity.

## Architecture and boundaries

| Layer | Responsibility |
| --- | --- |
| Browser / GitHub Pages | UI, local project persistence, waveform/spectrogram interaction, sample playback, MIDI, sequencing, browser effects, portable project export |
| Analysis service | Durable jobs for decoding unsupported media, stems, transcription/alignment, phonetic proposals, pitch/chords/key/tempo maps, semantic audio comparison |
| Shared project model | Stable asset/event/slice/track IDs, seconds plus musical positions, user corrections, provenance/confidence, effect graphs, arrangements, versioned migrations |
| Ableton Extension | One-shot analysis/import/arrangement actions that read or change Live Set data, subject to SDK capability verification |
| Max for Live / native device | Real-time sampling/effects/routing in Live; transport and automation integration |
| Optional desktop host | Native audio I/O and third-party plug-in hosting outside Live; share the UI and project model where feasible |

Ableton currently documents Extensions for Live 12 Suite Beta 12.4.5+ and
explicitly excludes continuous audio/MIDI processing, live samplers/effects, and
sample-accurate playback. Do not build the real-time engine around Extensions.
Verify SDK APIs against the installed version before implementing the adapter.
In-app device chains are a core requirement, with reorder/bypass/parameters and
saved state. Built-in effects run in the browser; native VST3/AU hosting in our
standalone edition requires a native host and platform-specific validation;
a browser cannot load arbitrary installed native plug-ins.

Sources checked:
- https://www.ableton.com/en/live/extensions/
- https://help.ableton.com/hc/en-us/articles/27303428331420-Ableton-Extensions-FAQ
- https://www.ableton.com/en/manual/max-for-live/

## Milestones and acceptance criteria

### 1. Reliable import, saved projects, editable sampler slices

- Diagnose import, decoding and worker failures; progress, cancellation and
  actionable errors; prevent duplicate drop handlers and stale job results.
- Save original media, measurements and corrected slices locally in IndexedDB;
  create/open/name projects; display storage failures rather than imply a save.
- Initial storage assumption: this browser on this device; cloud sync is a later
  option. Warn that browser-data clearing removes local projects; add portable
  backups before calling persistence production-ready.
- Select a detected hit; zoom its waveform; edit start/end, name, category and
  IPA; audition and undo; propagate corrections to Play and JSON exports.
- Preserve overlapping pad playback; computer and MIDI mappings remain usable.
- Pass: import a known recording; save; reload; reopen with audio and edits;
  ensure unsupported files fail visibly, new imports cannot overwrite old jobs,
  and slice boundaries stay inside the decoded media.

### 2. Reusable full-analysis pipeline and steerable prompts

- Replace hard-coded Mac paths and original-specific scripts with a job API,
  explicit capability checks, persisted results, retry/cancel, and progress.
- Analyze levels, transients, beat/downbeat/tempo maps, pitch, key, chord timeline,
  structure and spectral features. Preserve channel layout and sample-rate
  provenance. Mark unpitched/key-ambiguous material as unknown.
- Benchmark candidate transcription/alignment and audio-analysis tools on this
  recording plus speech, polyphonic music, silence and noisy inputs. Ordinary
  speech recognition does not reliably transcribe beatboxing or narrow IPA.
- Keep measured acoustics separate from inferred phonetics, generated wording
  and human corrections. Require audition/review for narrow-IPA proposals;
  show uncertainty and never regenerate over manual edits silently.
- Suno lyric/style generation uses selected stems, corrected events, harmony,
  rhythm and user intent. Controls: genre, feel, instrumentation, energy,
  pronunciation, adherence and exclusions. Editable output, revisions and copy.
  Do not assume access to a Suno generation API.
- Pass: new project receives its own analysis and prompts, traceable to the
  uploaded recording; corrections survive reruns and change downstream output.

### 3. Stems and mixer

- Evaluate maintained source-separation models for vocals/drums/bass/other;
  choose based on listening tests, compute needs, licenses and artifacts.
- Keep raw media immutable; derived stems retain parent/model/version metadata.
- Checkbox selection supports isolate, exclude, group/bounce and send to sampler;
  per-stem mute/solo/gain/pan and explicit bus routing, meters and clipping cues.
- Multi-singer separation is experimental: distinguish speaker diarization
  (who/when) from overlap-capable audio separation; evaluate before promising it.
- Pass: isolated and grouped stems can be auditioned, sampled, saved and reopened;
  duration/sample alignment is preserved and separation artifacts are disclosed.

### 4. Instrument, rhythm and interactive frequency editing

- Replace emphasis on the generic synth with slice mappings, pitched sample
  keyboard mode, velocity, gate/one-shot, envelopes, voice limits and choke groups.
- Add step sequencing, swing, triplets, density, seeded randomize, lock steps,
  pattern variations and undo. Schedule on the audio clock, not UI frame timing.
- Interactive waveform and spectrogram share selection with events and pads.
  Frequency-band selection initially controls audible filters with explicit
  audition/bypass; true time-frequency masking is a separate offline process.
- Pass: chords overlap, note-off/chokes work, sequence timing is stable during UI
  activity, frequency edits are audible and saved, keyboard access is complete.

### 5. Prompted effects

- Typed, versioned effects graph with gain staging, bypass, wet/dry, parameters,
  automation, undo and presets at slice/stem/track/group/master scopes.
- Begin with validated delay, reverb, EQ/filter, dynamics and formant processing.
  Prompt -> proposed graph -> audition -> editable controls. Tempo divisions are
  explicit, including dotted and triplet values.
- New DSP generation is a later experimental path: isolated compilation and
  offline validation for NaN/Inf, extreme output, CPU/time/memory, silence and
  sample-rate changes before live use. Never eval arbitrary generated code in
  the main UI or audio thread. Limit output and offer immediate bypass.
- Pass: prompted chains sound as configured, manual tweaks persist, bypass/A-B
  work, and invalid graphs cannot connect feedback loops or uncontrolled gain.

### 6. Cross-project remix and harmony

- + Add track chooses a recording, stem, slice, loop or pattern from any project.
  Keep source IDs and a media-availability check when projects move.
- Master transport, per-track gain/pan/EQ, cueing/crossfade, clip placement,
  trimming, loops and arrangement. Preserve original sources and edit history.
- Editable beat grids/tempo maps, independent time-stretch and pitch-shift,
  downbeat alignment, estimated key alternatives, chord/Roman-numeral views.
- Start with two tracks, then scale under measured CPU/memory limits. Preserve
  the user's ability to add more; do not promise unlimited simultaneous tracks.
- Pass: two projects sync and blend, save/reopen reproduces the mix, harmonic
  edits can be corrected, and offline WAV export matches playback within limits.

### 7. Ableton integration and favorite plug-ins

- Capability spike against user's installed Live edition/version and SDK:
  import samples/analysis, create or update supported Set structures, transfer
  tempo/key/clip metadata, and establish undo behavior. Build a real end-to-end
  prototype before committing to the Extension packaging/API surface.
- Real-time instrument/effects through Max for Live or a native plug-in, with
  verified transport, latency, automation, project-state restore and routing.
- Implement favorite plug-ins inside our own device-chain UI with a desktop
  native hosting layer. Ableton integration is an additional destination, not
  a replacement for our mixer. Benchmark: discovery, licensing/architecture,
  parameter/state persistence, crash isolation and latency compensation.
- Pass: reopen a Live Set with the correct samples, routing and device state;
  process audio through a known installed plug-in and verify render/latency.

## Cross-cutting requirements

- Versioned saves, autosave status and portable backup; no secrets in Pages.
- Undoable non-destructive edits; stable IDs linking waveform/event/caption/pad.
- Analysis runs off the UI/audio threads; cancellable jobs and memory limits.
- Captions below the video, driven by corrected events. Existing portable MP4
  must be inspected for burned-in text; obtain/use a clean original where needed.
- Accessible labels, focus, keyboard controls, readable contrast, reduced motion.
- Keep the current visual language. Introduce workspace changes only when the
  workflow needs them; validate desktop and small screens with real media.
- Tests cover persistence/reload, job races, slice bounds, DSP edge cases and
  render/export consistency; listening tests remain necessary for music quality.

## Initial source findings

- Single-file app at index.html, no build system or test runner.
- Browser analyzer already computes loudness estimates, spectral flux/onsets,
  tempo and a spectrogram in a Blob worker; full phonetics are not implemented
  for newly imported files.
- Drop-zone events bubble to a second window handler, starting duplicate jobs.
- Worker errors only change a status line and leave the busy screen active.
- No import cancellation or stale-result guard; overlapping jobs share state.
- Uploaded audio/results disappear on refresh; no project persistence.
- Existing Play engine already supports overlapping sample voices and MIDI.
- Python analysis scripts reference a specific /Volumes/... path and original
  recording. These are source material for milestone 2, not a ready service.

## Delivery rule

Work on a feature branch and draft PR. Keep the currently hosted app available.
Each milestone reports implemented behavior, test evidence and limitations.
Do not represent queued roadmap capabilities as shipped features.
