# DESIGN.md — Visual Direction Contract

## One-Line Product Contract
`operate + experience / producer, musician & phonetics researcher / inspect 147 vocal-percussion syllables, audition Original vs. Suno A/B matches, and copy Suno style & IPA lyric blocks / click any syllable, phrase, or workspace tab for <50ms audio-visual feedback`

| Decision | Specification |
| :--- | :--- |
| **Product mode** | `operate` (interactive acoustic/phonetic microscope & A/B auditioning tool) + `experience` (synchronized video/subtitle performance atlas) |
| **Audience & cadence** | Music producers, vocal-percussion / beatbox analysts, and AI audio prompt engineers inspecting micro-transients, formants, rhythm notation, and `earshot` CLAP similarity |
| **Visual world** | **Precision Studio DAW & Phonetic Corpus Workbench** — inspired by Teenage Engineering, Ableton Live, Linear, and Stripe Docs |
| **Palette family** | **Obsidian Slate + Studio Amber & Cyan** (`#080a0f` canvas, `#0f131c` surface, `#161b26` elevated, `#f59e0b` playhead amber, `#38bdf8` Original A cyan, `#f97316` Suno B coral, `#10b981` calibrated match emerald) |
| **Type treatment** | Sans-first UI (`Inter` / system-ui) paired with tabular monospace (`JetBrains Mono` / `SF Mono` / `DejaVu Sans Mono`, `font-variant-numeric: tabular-nums`) for IPA diacritics, musical rhythm symbols (`♩ ♪ ♬ ♪³`), timestamps, and dBFS/Hz readouts |
| **Composition** | **Full-Viewport Slide Deck**: one fixed full-width nav bar (brand, 9 chapter links, now-playing mini transport, downloads, prev/next + slide counter) over 13 slides that each fit the viewport with no page scroll. Every slide = left caption column (number, title, 2-sentence explanation, key hints, next button) + right interactive body. Long data (tables, lists) scrolls inside its own panel only. Keys: `←/→` slides, `Space` play/pause, `,`/`.` step syllable, `L` loop. |
| **Shape language** | Crisp `10px–12px` studio panels, `1px` structural hairlines (`#1e2636`), fixed-dimension chips and tabular rows that never shift layout on hover or active playhead transitions |
| **Anti-references** | Never block >50% of vertical viewport with a giant top sticky banner; never dump raw unformatted 150-character metadata strings when a clean tabular grid can align them; never scale elements on playhead updates in a way that reflows neighbors |
