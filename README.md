# `IMG_3268` — Vocal Percussion, Narrow IPA, Musical Rhythm & Suno A/B Studio Atlas

An interactive acoustic, phonetic, musical-rhythm, and `earshot` A/B comparison workbench analyzing **147 discrete vocal-percussion events** across `IMG_3268.mp3` (`0:00.00–0:37.82`) and comparing it against its Suno AI vocal-percussion render (`IMG_3268 SUNO.mp3`).

## 🌐 Live Interactive Studio Workbench (GitHub Pages)
- **Live URL**: **https://jeromyjsmith.github.io/img-3268-phonetic-rhythm-atlas/**
- **Web App (`index.html`)**: Full-viewport slide deck (13 slides, fixed top nav bar, `←/→` to move, no page scrolling) covering:
  1. **Left Sticky Studio Monitor Rail**: Synchronized video/audio stage (`🎥 Video + Subtitles`, `🅰️ Original MP3`, `🅱️ Suno MP3`), live Tri-Tier Phonetic + Narrow IPA + Musical Rhythm HUD, active window rhythm strip, and keyboard transport (`Space`, `←/→`, `L`, `1–5`).
  2. **Workspace 1 — `earshot` Original vs. Suno A/B Lab**: Interactive phrase-by-phrase A/B auditioning (`Original` vs. `Suno Same-Timestamp` vs. `Suno earshot find Best-Match`), full `earshot` quantitative scorecard (`CLAP cosine = 0.82` peak 3s window / `0.60` full pass, calibrated `z = +6.71` vs. `+7.34` both `#1 / 322` at `100th percentile`, `p_real = 0.994` vs. `0.981`), and side-by-side `earshot sheet` contact sheets.
  3. **Workspace 2 — 14-Window Phonetic & Rhythm Microscope**: All 14 ultra-zoomed 7-tier acoustic windows (`Z01–Z14`), tactile syllable pads, structured tabular event breakdowns, and collapsible raw bracketed metadata.
  4. **Workspace 3 — Suno Style Prompt Builder & 4 Lyric Formats**: 6 genre archetypes + interactive flavor chip mixer + 4 copy-ready lyric blocks (`Suno English Phonetics`, `Pure Narrow IPA [...]`, `Pure Broad IPA /.../`, and `Tri-Tier Combined Score`).
  5. **Workspace 4 — Musical Rhythm, 16-Step Sequencer & Narrow IPA Guide**: Tempo curve, subdivision census, 16-step drum-machine grid, formant vowel space (`F1–F2`), and Narrow IPA articulatory mechanics.
  6. **Workspace 5 — Searchable 147-Event Master Corpus Table**: Instant search and category filtering across all 147 events.

## 📁 Repository Structure
- [`index.html`](./index.html) — Fast-loading GitHub Pages Studio Workbench
- [`DESIGN.md`](./DESIGN.md) — Visual Direction Contract (`frontend-design` / `modern-web-design`)
- [`IMG_3268.mp3`](./IMG_3268.mp3) — Original close-mic mouth percussion performance (`37.82s`)
- [`IMG_3268 SUNO.mp3`](./IMG_3268%20SUNO.mp3) — Suno AI render (`89.36s`) generated from the phonetic prompt
- [`analysis/IMG_3268_phonetic_report.html`](./analysis/IMG_3268_phonetic_report.html) — 100% self-contained single-file offline HTML bundle
- [`analysis/IMG_3268_subtitled_phonetic_rhythm.mp4`](./analysis/IMG_3268_subtitled_phonetic_rhythm.mp4) — Standalone MP4 video with burned-in multi-tier karaoke subtitles
- [`analysis/earshot_orig_vs_suno.json`](./analysis/earshot_orig_vs_suno.json) — Complete `earshot` A/B comparison metrics and sliding CLAP embeddings
- [`analysis/micro_events_138.json`](./analysis/micro_events_138.json) — All 147 annotated auditory events with Narrow IPA, formants, and musical rhythm notation
