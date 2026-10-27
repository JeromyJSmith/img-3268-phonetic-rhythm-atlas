# `IMG_3268.mp3` vs. `IMG_3268 SUNO.mp3` — Complete 147-Event Phonetic, Musical Rhythm & `earshot` A/B Comparison Atlas

> [!IMPORTANT]
> **100% Portable Interactive Video + Dual-Audio A/B Comparison HTML**: Open [`IMG_3268_phonetic_report.html`](file:///Volumes/2TB/moviesfolder/MOVIES_FOLDER/studpid%20Stuff/analysis/IMG_3268_phonetic_report.html) (`34.18 MB`, completely self-contained with embedded H.264 video, WebVTT subtitles, [`IMG_3268.mp3`](file:///Volumes/2TB/moviesfolder/MOVIES_FOLDER/studpid%20Stuff/IMG_3268.mp3), [`IMG_3268 SUNO.mp3`](file:///Volumes/2TB/moviesfolder/MOVIES_FOLDER/studpid%20Stuff/IMG_3268%20SUNO.mp3), and 19 figures) to click-and-compare any phrase between the Original and Suno render or click any of the **147 individual auditory events**.

## 0. `earshot` A/B Comparison: Original (`IMG_3268.mp3`) vs. Suno Render (`IMG_3268 SUNO.mp3`)

We ran the full `earshot` suite (`measure`, `describe`, `realness`, `timeline`, `sheet`, `find`, `ab`, and 24 sliding 3-second CLAP window embeddings) comparing [`IMG_3268.mp3`](file:///Volumes/2TB/moviesfolder/MOVIES_FOLDER/studpid%20Stuff/IMG_3268.mp3) (`A`) against [`IMG_3268 SUNO.mp3`](file:///Volumes/2TB/moviesfolder/MOVIES_FOLDER/studpid%20Stuff/IMG_3268%20SUNO.mp3) (`B`).

![Original vs Suno earshot 6-Panel Comparison](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/fig_suno_vs_orig_comparison.png)

![Suno Render earshot Sheet](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/IMG_3268_SUNO_sheet.png)

### Overall `earshot` Closeness & Acoustic Scorecard

| `earshot` Metric / Command | 🅰️ Original (`IMG_3268.mp3`) | 🅱️ Suno Render (`IMG_3268 SUNO.mp3`) | `earshot` Verdict & Interpretation |
| :--- | :--- | :--- | :--- |
| **Direct CLAP Audio-to-Audio Similarity (`earshot ab`)** | `0:00.00–0:37.80` (`37.82 s`) | `0:00.00–0:37.80` (1st pass of `89.36 s` render) | **`cosine_ab = 0.60` (`"CLAP hears them as related"`)** across the full 37.8s span; **Phrase 4 (`22.92–34.10s`) reaches `cosine_ab = 0.69`**, and the 3s sliding window peaks at **`cosine = 0.82`** (`A[24.0–27.0s]` vs. `B[30.0–33.0s]`) and **`cosine = 0.78` at the exact same timestamp (`30.0–33.0s`)**! |
| **Combined Target Prompt (`earshot ab --query`)**<br/>*"rhythmic human beatboxing, vocal chops, brass wah stabs and 808 sub-bass groove"* | **`z = +6.71`** (`cos = 0.354`)<br/>**Rank #1 / 322 (`100th pct`)** | **`z = +7.34`** (`cos = 0.471`)<br/>**Rank #1 / 322 (`100th pct`)** | **Both rank #1 out of 322 in `earshot`'s calibrated vocabulary (`100.0th percentile`)**. Suno edges ahead (`dz = +0.63`) by layering full-band sub-bass and brass onto the vocal percussion. |
| **Beatboxing Prompt (`earshot ab --query`)**<br/>*"rhythmic human beatboxing and vocal percussion with plosive kicks and hi-hats"* | **`z = +4.95`** (`cos = 0.289`)<br/>**Rank #1 / 322 (`100th pct`)** | **`z = +4.71`** (`cos = 0.312`)<br/>**Rank #1 / 322 (`100th pct`)** | **`"Neither is closer (dz = 0.24)"` — Statistical Tie at #1 / 322!** Suno locks onto the exact bilabial/alveolar beatbox transients (`[p, t, k, t͡sʰ, buːm]`). |
| **808 Sub-Bass & Boom-Bap (`earshot ab --query`)**<br/>*"heavy 808 sub-bass kick and boom-bap beatbox groove"* | **`z = +3.55`** (`cos = 0.165`)<br/>**Rank #3 / 322 (`99.4th pct`)** | **`z = +3.83`** (`cos = 0.207`)<br/>**Rank #1 / 322 (`100th pct`)** | **`"Neither is closer (dz = 0.28)"` — Statistical Tie!** Both deliver the same heavy halftime/boom-bap bounce. |
| **Talkbox Brass Wah & DJ Scratch (`earshot ab --query`)** | Talkbox Wah: `z = +4.16` (#1)<br/>DJ Scratch: `z = +1.98` (#9) | Talkbox Wah: **`z = +6.01`** (#1)<br/>DJ Scratch: **`z = +4.05`** (#1) | **Suno amplifies the mouth-imitated instruments (`dz = +1.85` & `+2.07`)**: your vocal-tract formant sweeps (`BOW-buh-BOW`) and uvular trills (`Hhh-RA-hh-RA!`) become full talkbox horn stabs and vinyl scratches. |
| **Raw Mouth Percussion (`earshot ab --query`)**<br/>*"syncopated vocal scatting and crisp mouth percussion"* | **`z = +5.35`** (`cos = 0.348`)<br/>**Rank #1 / 322 (`100th pct`)** | **`z = +3.83`** (`cos = 0.295`)<br/>**Rank #1 / 322 (`100th pct`)** | **Original is closer (`dz = +1.52`)** because `IMG_3268.mp3` is 100% dry, close-miked solo mouth foley with no backing instruments. |
| **AudioSet (`AST`) & `earshot describe` Classes** | `Speech 0.88`, **`Beatboxing 0.74`**, `Whispering 0.43`, `Vocal music 0.10` | `Music 0.86`, **`Beatboxing 0.61`**, `Speech 0.35`, `Brass instrument 0.20`, `Funk 0.18`, `Trumpet 0.16` | Both are simultaneously classified as **Beatboxing** (`0.74` vs. `0.61`) and **Vocal Chop / Funk / Hip-Hop** (`CLAP funk music z = +4.60`, `vocal chop z = +3.86`, `glitch hop z = +3.21`, `hip hop beat z = +3.15`). |
| **Realness (`earshot realness`)** | **`p_real = 0.994`** (`real or pro-produced`, 0/10 synth windows, CLAP head `+4.5`) | **`p_real = 0.981`** (`real or pro-produced`, 0/23 synth windows, CLAP head `+4.1`, peak `1.00` at `24–28s`) | Both score at the ceiling of `real or pro-produced` with **0 windows** flagged as synthetic/robotic. |
| **Loudness, Attack & Spectral Balance (`earshot measure`)** | `-28.2 LUFS` (`-7.2 dBTP`, `LRA 8.1 LU`), Attack **`148 ms`**, Brightness `1952 Hz`, Roll-off `3814 Hz`, Sub `-33.0 dB`, Top `-48.7 dB`, Mono | `-16.4 LUFS` (`-3.0 dBTP`, `LRA 5.0 LU`), Attack **`146 ms`**, Brightness `4074 Hz`, Roll-off `8829 Hz`, Sub `-14.1 dB`, Top `-26.5 dB`, Stereo (`-20 dB` S/M) | **Virtually identical macro attack (`148 ms` vs. `146 ms`)**, while Suno is mastered `+11.8 LU` louder with **`+18.9 dB` more sub-60 Hz weight** and **`+22.2 dB` more >8 kHz top-end air**. |
| **Structural Pacing & Drop Alignment (`earshot timeline`)** | `156 onsets` (`4.12/s`); post-scratch breakdown pause at **`0:34.10`** before final `Duh-rip-it-NOW!` | `531 onsets` (`5.94/s`); executes a `0.4 s` stop-down drop at **`0:33.50`** (`Δt = 0.60 s` from Original!), then extends into a full funk/beatbox jam (`38–89s`) | Suno followed the 5-phrase pacing of your phonetic lyric sheet so closely that its post-scratch breakdown drop lands at **`0:33.50`** vs. **`0:34.10`** in your original recording! |

### Phrase-by-Phrase `earshot find` & `earshot ab` Alignment

| Phrase in Original (`IMG_3268.mp3`) | Original Window (`A`) | Same-Timestamp CLAP Cosine (`B` at same `t`) | Best-Matching Window in Suno (`earshot find`) | Best-Match CLAP Cosine | Calibrated Query `z` (Orig `A` vs. Suno `B`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Phrase 1**: Plosive-Brush Scat (`thuh-bitch camp brah / at ALL!`) | `0:00.26–0:04.35` | `0.460` | `0:17.30–0:21.39` (`find z = +4.97`) | `0.450` (`0.579` on 3s window at `3.0s`) | Orig `z = +2.91` (#5) vs. Suno **`z = +4.81` (#1 / 322)** |
| **Phrase 2**: Sub-Hum & Cork-Pop Groove (`Mmmm! / pink cane / ki-'in / NOW!`) | `0:04.75–0:11.72` | `0.513` (`related`) | `0:02.06–0:04.04` (`find z = +8.40`) | **`0.531`** (`0.651` on 3s window at `9.0s`) | Orig `z = +2.81` (#6) vs. Suno **`z = +8.40` (#1 / 322)** |
| **Phrase 3A–3B**: Brass Wah Stabs & Falsetto (`BOW-buh-BOW / WHEN!↑`) | `0:12.50–0:18.12` | **`0.503` (`related`)** | **`0:12.52–0:17.56`** (Exact same time!) | **`0.503`** (`0.626` on 3s window at `15.0s`) | Orig `z = +3.20` (#4) vs. Suno **`z = +4.98` (#1 / 322)** |
| **Phrase 3C–3D**: 32nd Roll & Chopper (`thuh-buh-chuh-kuh-buh-GAH / skibidi-BAH`) | `0:18.47–0:22.75` | `0.393` | `0:09.97–0:14.25` (`find z = +7.74`) | `0.411` (`0.674` on 3s window at `22.5s`) | Orig `z = +3.72` (#2) vs. Suno **`z = +6.11` (#1 / 322)** |
| **Phrase 4**: 808 Beatbox & DJ Scratch (`FWOO-BWAH / Boom-ts-boom / Hhh-RA-hh-RA!`) | `0:22.92–0:34.10` | **`0.667` (`related`)** | `0:17.30–0:28.48` & `0:30.00–0:33.50` | **`0.688` macro / `0.820` peak 3s window (`0.780` same-time at `31.5s`)** | Orig **`z = +3.94` (#1)** vs. Suno **`z = +4.36` (#1 / 322)** |
| **Phrase 5**: Staccato Coda Tag (`Duh-rip-it-NOW!`) | `0:36.48–0:37.38` | `0.206` (Suno jams on) | `0:03.80–0:04.70` (`find z = +5.12`) | **`0.529` (`related`)** | Orig **`z = +4.60` (#1)** vs. Suno **`z = +4.90` (#1 / 322)** |

---

## 1. Six Stylistic Genre Options & Suno Style Prompts

Because [`IMG_3268.mp3`](file:///Volumes/2TB/moviesfolder/MOVIES_FOLDER/studpid%20Stuff/IMG_3268.mp3) is a pure **human vocal-tract instrument** performance (`p_real = 0.99`, `Beatboxing 0.74`, `CLAP: vocal chop z = +4.3`) that shifts across **five distinct rhythmic feels** (`103 BPM` swung 16th pocket -> `96 BPM` neo-soul backbeat -> `112–131 BPM` funk horn stabs & 32nd-note chopper -> `83.5 BPM` heavy halftime 808 beatbox + turntable scratch), here are **six complete stylistic genre directions** you can use:

### Option A: Golden-Era Turntablist Boom-Bap & Underground Beatbox Cypher (*Rahzel / Scratch / Kenny Muhammad / The Roots*)
- **Why It Fits Acoustically**: Phrases 4 & 5 (`22.92s–37.82s`) lock into an **83.5 BPM halftime / boom-bap pocket** driven by sub-100 Hz bilabial 808 kicks (`[ˈbuːm]`, `F0 = 91–93 Hz`), alveolar affricate closed hats (`[t͡sʰ]`), postalveolar snare splashes (`[ˈbuʃ]`), and a two-stage uvular-trill vinyl scratch (`[χː ˈʀæ χ ˈʀæː]`, *Hhh-RA-hh-RA!*).
- **Copy-Paste Suno Style Prompt (Option A)**:
```text
90s underground boom-bap hip-hop, live human beatbox percussion, vocal bassline 808 sub-kicks, turntablism vinyl record scratches, raw vocal scatting, punchy dry close-mic vocals, Rahzel style vocal percussion, 85 BPM
```

### Option B: Future Funk / Talkbox Brass-Bounce & Glitch-Hop Vocal Chop (*Chromeo / Gramatik / Opiuo / Beardyman*)
- **Why It Fits Acoustically**: Phrase 3 (`12.50s–22.92s`) features **envelope-filtered brass wah stabs** (`BOW-buh-BOW-BOW-BOW!`, `[ˈbaʊ]` with `F1` sweeping `748 -> 350 Hz` like a Moog low-pass filter or Roger Troutman talkbox), a **500 Hz pinched falsetto synth lead squeak** (`WHEN!↑`, `[ˈwɪ̃n↑]`), and a **131 BPM 16th-note double-tongued vocal chopper** (`buh-lip-uh-gih-buh-lep-uh-DAH!`).
- **Copy-Paste Suno Style Prompt (Option B)**:
```text
glitch-hop future funk, talkbox synth-brass wah stabs, rhythmic vocal chops, slap bass, crisp percussive scatting, micro-sampled vocal percussion, high-energy funk pocket, 112 BPM
```

### Option C: Avant-Garde Acapella Loop-Station Funk & Neo-Soul Pocket (*Reggie Watts / Marc Rebillet / Bobby McFerrin / J Dilla*)
- **Why It Fits Acoustically**: Phrases 1 & 2 (`0.00s–12.50s`) use **microtimed behind-the-beat swing** (`-18 ms` Dilla pocket), **nasal-clamped clavinet muting** (`camp`, `pump`, `[ˈkʰæmp̚]`), **hollow velar-glottal cork pops** (`cup`, `pink`, `'in`, `[ˈpʰɪŋk̚, ˈʔɪn]`), and theatrical breath/hum transitions (`Mmmm!`).
- **Copy-Paste Suno Style Prompt (Option C)**:
```text
live loop-station vocal funk, neo-soul swung pocket, Reggie Watts style experimental vocal groove, mouth-percussion, clavinet vocal muting, human bass hum, playful theatrical beatbox scat, 98 BPM
```

### Option D: UK Bassline / Halftime Wonky Trap & Festival Vocal Chops (*TroyBoi / Tipper / Baauer / Hudson Mohawke*)
- **Why It Fits Acoustically**: Turns the reverse-cymbal labiodental air riser (`FWOO-BWAH!`, `[ˈfwuː ˈbwɑː]`), sub-100 Hz 808 kicks, and syncopated `ship it DOWN! / take it DOWN!` vocal hooks into a swaggering halftime festival trap drop.
- **Copy-Paste Suno Style Prompt (Option D)**:
```text
wonky halftime trap, heavy 808 sub-bass glides, pitched vocal chop hooks, festival horn stabs, crisp mouth percussion foley, reverse air risers, swaggering halftime bounce, 84 BPM
```

### Option E: Nu-Jazz / Scat-Funk & Hyper-Pocket Drumline (*Louis Cole / Knower / Cab Calloway / Caravan Palace*)
- **Why It Fits Acoustically**: Highlights the virtuosic 5-stroke **32nd-note paradiddle roll** (`thuh-buh-chuh-kuh-buh-GAH!`), the **16th-triplet ruff** (`ski-bi-di-BAH!`), and the rapid labial-lateral-velar double-tonguing (`buh-lip-uh-gih-buh-lep-uh-DAH!`).
- **Copy-Paste Suno Style Prompt (Option E)**:
```text
nu-jazz scat funk, tight drumline vocal percussion, punchy big-band brass stabs, rapid double-tongue vocal rolls, Louis Cole style hyper-funk pocket, dry studio drums, 122 BPM
```

### Option F: Underground Phonk / Memphis Cowbell & Gritty Turntable Cut (*DJ Smokey / Drift Phonk / Memphis Rap*)
- **Why It Fits Acoustically**: Pairs the gravelly pharyngeal/uvular throat scrapes (`[χː ˈʀæ]`, `[k͡x̥ hʀ̥ː]`), woodblock-like clipped stops (`[ˈpʰɪŋk̚]`, `earshot: cork pop`), and heavy `Boom-ts-boom` low end.
- **Copy-Paste Suno Style Prompt (Option F)**:
```text
underground phonk, gritty lo-fi vocal chops, distorted 808 cowbell bounce, vinyl scratch cuts, punchy Memphis rap cadence, raw close-mic vocal percussion, 86 BPM
```

### Extra Style Flavor Modifiers You Can Mix & Match in Suno
| Flavor Category | Copy-Paste Style Tags to Add to Suno's `Style of Music` Box | Effect on Suno's Vocal & Rhythm Engine |
| :--- | :--- | :--- |
| **Dry Close-Mic Intimacy** | `close-mic ASMR transients, dry studio booth, zero reverb, crisp mouth percussion` | Forces Suno to preserve the `2 ms` plosive attacks (`p̚, t̚, k̚`) instead of washing them out in reverb. |
| **Talkbox / Filter Envelope** | `talkbox formant filter, auto-wah brass stabs, resonant vowel sweep, clavinet funk` | Turns the `BOW-buh-BOW` (`[ˈbaʊ]`) and `camp / brah` syllables into biting envelope-filtered horn/clavinet hits. |
| **Turntable & Chopped FX** | `DJ scratch breaks, MPC sampler vocal chops, stutter edits, tape-stop drop` | Enhances the `ski-bi-di-BAH`, `buh-lip-uh-gih` chopper, and `Hhh-RA-hh-RA` scratch sections. |
| **Halftime 808 Weight** | `sub-bass 808 vocal kick, heavy halftime drop, boom-bap snare snap` | Gives massive low-end weight (`60–95 Hz`) to the `FWOO-BWAH / Boom-ts-boom` section. |
| **Swung Neo-Soul Pocket** | `drunk Dilla swing, unquantized human pocket, syncopated ghost notes` | Keeps the 16th-note `thuh / uh / buh` ghost bounces groovy rather than stiffly robotic. |

---

## 2. Copy-Paste Phonetic Lyrics for Suno & Pure IPA Blocks

Below are **four ready-to-copy lyrical blocks**:

1. **Version 1 — Suno-Optimized English Phonetic Performance Lyrics**: Spelled with hyphenated phonetic syllables, capitalization for peak dB accents, and Suno `[meta-tags]` so Suno's voice engine pronounces every percussive pop, brush, wah stab, chopper roll, 808 kick, and DJ scratch.
2. **Version 2 — Pure Narrow IPA (`[...]`) Only**: Just the exact narrow articulatory/allophonic IPA transcription (with aspiration `ʰ`, unreleased stops `̚`, glottal stops `ʔ`, tie-bar affricates `t͡sʰ`, uvular trills `χ/ʀ`, nasalization `̃`, and upstep `↑`) in lyrical stanza form.
3. **Version 3 — Pure Broad IPA (`/.../`) Only**: Just the clean phonemic dictionary-level IPA transcription without narrow diacritics.
4. **Version 4 — Tri-Tier Combined Score (`EN` + `Narrow IPA` + `Musical Rhythm`)**: Side-by-side alignment of all three layers.

### Version 1: Copy-Paste Suno English Phonetic Lyrics (Pronunciation-Engineered for Suno)

```text
[Intro: Close-Mic Mouth Percussion, Swung 16th-Note Scat Pocket, 103 BPM]
(pff)
thuh-BITCH! camp, brah!
thuh-rup in thuh PANT, thence!
bup-uh-guh-KAH, pump!
thuh-frup in thuh fup-it, at ALLLL!
[Stop]

[Verse 1: Sub-Bass Hum & Syncopated Cork-Pop Scat Groove, 96 BPM]
Mmmmm-mp!
(huff)
thuh-cup-uh, thuh-PINK, caaane!
tuh-rip in thuh, KI-'in!
bick in thuh BOW, fen!
tuh-SICK in thuh-kuh-lip in NOWWW!
(deep gasp)

[Chorus: Funk Horn-Stab Call and Response & Falsetto Squeak, 112 BPM]
You know what?!
BOW! buh-BOW! BOW! BOWWW!
You know what, now!
You know what, now!
You know what, then!
You know what, WHENNN?! [High Falsetto Squeak]

[Bridge: 32nd-Note Drum Roll & Double-Tongue Vocal Chopper Fill, 128 BPM]
You know what—
thuh-buh-chuh-kuh-buh-GAHHH!
ski-bi-di-BAHHH!
buh-lip-uh-gih, buh-lep-uh-DAHHH!

[Drop: Heavy Halftime 808 Beatbox Groove & Vocal Hooks, 84 BPM]
FWOOO-BWAHHH!
boo-buh-boo — SHIP it DOWN!
BOOSH! boom-buh-boom — TAKE it DOWN!
Boom, ts, boom-buh-boom — rrr-RIGHT uh-ROUND!
Boom, ts, boom-buh-boom — Hhh-RA-hh-RAAAH! [Turntable Vinyl Scratch]

[Outro: Throat Scrape Breakdown & Staccato Coda Tag]
(kxhh-hrrr)
[1 Second Silence]
Duh-rip-it-NOWWW!
(pff-tick)
```

### Version 2: Just Narrow IPA (`[ ... ]` Only — Pure Articulatory Transcription)

```text
[p͡f˺]
[ðə ˈbɪtʃ ˈkʰæmp̚ ˈbɹɑː]
[ðə ˈɹʌp̚ ɪn ðə ˈpʰænt̚ ˈðɛns]
[ˈbʌp̚ ə ɡə ˈkʰɑː pʌmp̚]
[ðə ˈfɹʌp̚ ɪn ðə ˈfʌp̚ ɪt̚ ˈæt̚ ˈɔːl]
[ʔ‿h̥]

[ˈmːˀp] [h̥ː]
[ðə ˈkʰʌp̚ ə ðə ˈpʰɪŋk̚ ˈkʰeɪn]
[tʰə ˈɹɪp̚ ɪn ðə ˈkʰɪ ˈʔɪn]
[ˈbɪk̚ ɪn ðə ˈbaʊ ˈfɛn]
[tʰə ˈsɪk̚ ɪn ðə kʰə ˈlɪp̚ ɪn ˈnaʊ]
[hː↓]

[ju ˈnoʊ ˈwʌt̚]
[ˈbaʊ bə ˈbaʊ ˈbaʊ ˈbaʊː]
[ju ˈnoʊ wʌt̚ ˈnaʊ] [h̥]
[ju ˈnoʊ wʌt̚ ˈnaʊ]
[ju ˈnoʊ wʌt̚ ˈðɛn]
[ju ˈnoʊ wʌt̚ ˈwɪ̃n↑]

[ju noʊ wʌt̚]
[ðə bə tʃə kʰə bə ˈɡɑː]
[ˈskɪ bɪ dɪ ˈbɑː]
[bə ˈlɪp̚ ə ˈɡɪ bə ˈlɛp̚ ə ˈdɑː] [ʍ̥↓]

[ˈfwuː ˈbwɑː]
[ˈbuː bə ˈbuː ˈʃɪp̚ ɪt̚ ˈdaʊn]
[p˺] [ˈbuʃ ˈbuːm bə ˈbuːm] [ʔ] [ˈtʰɪk̚ ɪt̚ ˈdaʊn]
[b˺] [ˈbuːm t͡sʰ ˈbuːm bə ˈbuːm ʀː ˈɹaɪt̚ ə ˈɹaʊnd] [h̥͡p˺]
[ˈbuːm t͡sʰ ˈbuːm bə ˈbuːm χː ˈʀæ χ ˈʀæː]

[∅] [k͡x̥ hʀ̥ː] [∅]
[də ˈɹɪp̚ ˈɪt̚ ˈnaʊ]
[p˺ t˺]
```

### Version 3: Just Broad IPA (`/ ... /` Only — Clean Phonemic Transcription)

```text
/ðə bɪtʃ kæmp bɹɑ/
/ðə ɹʌp ɪn ðə pænt ðɛns/
/bʌp ə ɡə kɑ pʌmp/
/ðə fɹʌp ɪn ðə fʌp ɪt æt ɔl/

/m/
/ðə kʌp ə ðə pɪŋk keɪn/
/tə ɹɪp ɪn ðə kɪ ɪn/
/bɪk ɪn ðə baʊ fɛn/
/tə sɪk ɪn ðə kə lɪp ɪn naʊ/

/ju noʊ wʌt/
/baʊ bə baʊ baʊ baʊ/
/ju noʊ wʌt naʊ/
/ju noʊ wʌt naʊ/
/ju noʊ wʌt ðɛn/
/ju noʊ wʌt wɪn/

/ju noʊ wʌt/
/ðə bə tʃə kə bə ɡɑ/
/skɪ bɪ dɪ bɑ/
/bə lɪp ə ɡɪ bə lɛp ə dɑ/

/fwu bwɑ/
/bu bə bu ʃɪp ɪt daʊn/
/buʃ bum bə bum tɪk ɪt daʊn/
/bum ts bum bə bum ɹaɪt ə ɹaʊnd/
/bum ts bum bə bum xɹæ xɹæ/

/kx hɹ/
/də ɹɪp ɪt naʊ/
```

### Version 4: Tri-Tier Combined Score (English Phonetics + Narrow IPA + Musical Rhythm Notation)

```text
# PHRASE 1 (Bars 1–2 | 4/4 @ 103 BPM | Swung 16th Plosive-Brush Pocket)
EN : [lip-prep] thuh-bitch  camp   brah  | thuh-rup in thuh pant  thence | bup-uh-guh-kah pump
IPA: [p͡f˺]      [ðə ˈbɪtʃ] [ˈkʰæmp̚] [ˈbɹɑː] | [ðə ˈɹʌp̚ ɪn ðə ˈpʰænt̚ ˈðɛns] | [ˈbʌp̚ ə ɡə ˈkʰɑː pʌmp̚]
RHY:  𝄾          ♬   ♬      ♬      ♬     |  ♬   ♬·  ♬  ♬   ♪     ♪      |  ♬   ♬ ♬  ♬    ♬

EN : thuh-frup in thuh fup-it at  ALLLL!  [drop-pause]
IPA: [ðə ˈfɹʌp̚ ɪn ðə ˈfʌp̚ ɪt̚ ˈæt̚ ˈɔːl]    [ʔ‿h̥]
RHY:  ♬   ♬·   ♬  ♬   ♬   ♬  ♪   ♩·      𝄽

# PHRASE 2 (Bars 3–5 | 2/4 -> 4/4 @ 96 BPM | Sub-Hum & Cork-Pop Backbeat Groove)
EN : Mmmm!    [breath] | thuh-cup-uh thuh-pink cane  | tuh-rip in thuh ki  'in
IPA: [ˈmːˀp]  [h̥ː]     | [ðə ˈkʰʌp̚ ə ðə ˈpʰɪŋk̚ ˈkʰeɪn] | [tʰə ˈɹɪp̚ ɪn ðə ˈkʰɪ ˈʔɪn]
RHY:  𝅗𝅥        𝄽        |  ♬   ♬   ♬  ♬   ♪     ♩     |  ♬   ♬   ♬  ♬  ♪   ♪

EN : bick in thuh bow  fen  | tuh-sick in thuh-kuh-lip in NOWWW! [inhale-gasp]
IPA: [ˈbɪk̚ ɪn ðə ˈbaʊ ˈfɛn] | [tʰə ˈsɪk̚ ɪn ðə kʰə ˈlɪp̚ ɪn ˈnaʊ]  [hː↓]
RHY:  ♪    ♬  ♬   ♪    ♪    |  ♬   ♪    ♬  ♬  ♬   ♬   ♬  ♩      𝄽

# PHRASE 3A–3B (Bars 6–7 | 4/4 @ 112 BPM | Synth-Brass Wah Stabs & Falsetto Call-and-Response)
EN : You know what -> BOW!   buh-BOW!  BOW!   BOWWW!  | You know what now!
IPA: [ju ˈnoʊ ˈwʌt̚]   [ˈbaʊ] [bə ˈbaʊ] [ˈbaʊ] [ˈbaʊː] | [ju ˈnoʊ wʌt̚ ˈnaʊ]
RHY:  ♬   ♬    ♬       ♪·     ♬   ♪     ♪      ♩      |  ♬   ♬   ♬    ♪

EN : You know what now! | You know what then! | You know what WHEN!↑
IPA: [ju ˈnoʊ wʌt̚ ˈnaʊ] | [ju ˈnoʊ wʌt̚ ˈðɛn] | [ju ˈnoʊ wʌt̚ ˈwɪ̃n↑]
RHY:  ♬   ♬   ♬    ♪    |  ♬   ♬   ♬    ♪·    |  ♬   ♬   ♬    ♪·

# PHRASE 3C–3D (Bars 8–9 | 4/4 @ 128 BPM | 32nd Drum Roll, Sextuplet & 16th Chopper)
EN : You know what -> thuh-buh-chuh-kuh-buh-GAH! | ski-bi-di-BAH!
IPA: [ju noʊ wʌt̚]     [ðə  bə  tʃə  kʰə bə ˈɡɑː] | [ˈskɪ bɪ dɪ ˈbɑː]
RHY:  ♬  ♬   ♬         ♬   ♬   ♬    ♬   ♬   ♩    |  ♪³  ♪³ ♪³  ♩·

EN : buh-lip-uh-gih  buh-lep-uh-DAH!  [lip-inhale]
IPA: [bə ˈlɪp̚ ə ˈɡɪ  bə ˈlɛp̚ ə ˈdɑː]  [ʍ̥↓]
RHY:  ♬   ♬   ♬  ♬    ♬   ♬   ♬  ♩·    𝄾

# PHRASE 4 (Bars 10–13 | 4/4 @ 83.5 BPM | Heavy 808 Beatbox Groove & Turntable Scratch)
EN : FWOO - BWAH! | boo - buh - boo  | ship  it   DOWN!
IPA: [ˈfwuː ˈbwɑː] | [ˈbuː bə   ˈbuː] | [ˈʃɪp̚ ɪt̚  ˈdaʊn]
RHY:  ♪      ♩    |  ♪    ♬     ♪    |  ♪    ♬    ♩·

EN : BOOSH! | boom - buh - boom | take   it   DOWN!
IPA: [ˈbuʃ] | [ˈbuːm bə   ˈbuːm]| [ˈtʰɪk̚ ɪt̚  ˈdaʊn]
RHY:  ♩     |  ♪·    ♬     ♩    |  ♬     ♬    ♩·

EN : Boom - ts  - boom - buh - boom | rrr - right - uh - ROUND!
IPA: [ˈbuːm t͡sʰ   ˈbuːm  bə   ˈbuːm]| [ʀː   ˈɹaɪt̚   ə   ˈɹaʊnd]
RHY:  ♪·    ♬     ♪·     ♬     ♩    |  ♬     ♬      ♬    ♩

EN : Boom - ts  - boom - buh - boom | Hhh - RA  - hh - RA!
IPA: [ˈbuːm t͡sʰ   ˈbuːm  bə   ˈbuːm]| [χː   ˈʀæ   χ   ˈʀæː]
RHY:  ♪·    ♬     ♪·     ♬     ♩    |  ♬     ♬    ♬    ♩

# PHRASE 5 (Bars 14–15 | Rubato -> 2/4 @ 96 BPM | Throat Scrape & Coda Tag)
EN : [velar-click] [throat-scrape] ... [1.0s silence] ... Duh - rip - it - NOW!
IPA: [k͡x̥]          [hʀ̥ː]               [∅]                [də  ˈɹɪp̚  ˈɪt̚  ˈnaʊ]
RHY:  ♬             ♪·                  𝄽                  ♬    ♬     ♬    ♩
```

---

## 3. Musical Rhythm Analysis & Drum-Staff Notation Breakdown

![Musical Rhythm Overview](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/fig_rhythm_overview.png)

![16-Step Sequencer Grid](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/fig_rhythm_sequencer_grid.png)

### How the Vocal Rhythm Works Musically (5 Distinct Rhythmic Behaviors)

| Section / Bars | Time Sig & Local Tempo | Dominant Subdivision & Note Values | Microtiming / Groove Behavior | Drum-Kit / Musical Notation Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| **Phrase 1 (`Bars 1–2`, `0:00.26–0:04.35`)** | `4/4` @ `103 BPM` (with `16th` pickup `thuh` at `0:00.18`) | Swung 16th notes (`♬`, `140–170 ms` IOI) + dotted-16th rebounds (`rup-in-thuh`) + dotted-quarter hold (`all!`, `♩·`) | **58% MPC Swing**:dental brushes (`thuh`, `[ðə]`) act as 16th-note pickup ghost notes (`1-a`, `2-a`, `4-a`) leading into clipped downbeat stops (`camp`, `pant`, `fup`). | Funk drummer playing ghosted 16th hi-hat brushes into dry gated snare/tom hits, ending on a Beat 4 brass pad hold (`all!`). |
| **Phrase 2 (`Bars 3–5`, `0:04.75–0:12.50`)** | `2/4` pickup bar -> `4/4` @ `96 BPM` | Half-note hum (`𝅗𝅥`, `730 ms`) -> syncopated 8th (`♪`) and 16th (`♬`) offbeats (`ki-'in`, `tuh-sick-in-thuh-kuh-lip-in-NOW!`) | **Laid-Back Neo-Soul Pocket (`-12 to -24 ms` behind grid)**: glottal stops (`[ʔ]`) create zero-attack syncopated offbeats on the `&` of beats. | J Dilla / Questlove unquantized pocket where cork-pop transients (`pink`, `'in`) sit slightly behind the quarter-note pulse. |
| **Phrase 3A–3B (`Bars 6–7`, `0:12.50–0:18.47`)** | `4/4` accelerating `98 -> 118.5 BPM` | Three-16th anacrusis (`You-know-what`, `♬ ♬ ♬`) answered by syncopated dotted-8th + 16th + 8th horn stabs (`BOW-buh-BOW-BOW-BOW!`, `♪· ♬ ♪ ♪ ♩`) | **Pushed Funk Urgency (`+10 to +18 ms` ahead of grid)**: each repetition of `You know what` compresses in duration (`590 ms -> 440 ms -> 350 ms`). | Tower of Power / Chromeo horn section call-and-response with an upbeat falsetto synth accent (`WHEN!↑`) on Beat 4. |
| **Phrase 3C–3D (`Bars 8–9`, `0:18.47–0:22.92`)** | `4/4` @ `116 -> 131 BPM` | **Subdivision showcase**: 5-stroke **32nd-note roll** (`thuh-buh-chuh-kuh-buh`, `♬` at `88–95 ms` IOI) -> **16th-note triplet / sextuplet** (`ski-bi-di`, `♪³` at `140–160 ms`) -> **straight 16th double-tongue chopper** (`buh-lip-uh-gih-buh-lep-uh-DAH!`) | **Razor-sharp grid lock (`±4 ms` jitter)**: alternating labial (`b`), lateral (`l`), and velar (`g/d`) articulators allow double-tonguing faster than a single articulator can repeat. | Drumline paradiddle roll into a 3-note ruff (`ski-bi-di-BAH!`) followed by a 16th-note MPC gated chopper fill. |
| **Phrase 4 (`Bars 10–13`, `0:22.92–0:34.20`)** | `4/4` @ `83.5 BPM` (Heavy Halftime / Boom-Bap) | Classic **Boom-Bap Beatbox Grid**: Beat `1` (`Boom`, `♪·`), Beat `1-a` (`ts`, `♬`), Beat `2` (`boom`, `♪·`), Beat `2-a` (`buh`, `♬`), Beat `3` (`boom`, `♩`), Beats `3-& to 4` (Hook / DJ Scratch `Hhh-RA-hh-RA!`, `♬ ♬ ♬ ♩`) | **Deep 808 Sub-Pocket**: the `ts` hi-hat (`[t͡sʰ]`) and `buh` ghost kick (`[bə]`) land squarely on the `1-a` and `2-a` 16th subdivisions, creating a classic swung hip-hop bounce. | TR-808 sub-kick + crisp closed hat + vocal sample hook on Bars 1–3, answered on Bar 4 by a 16th-note baby-scratch + flare-cut (`Hhh-RA-hh-RA!`). |
| **Phrase 5 (`Bars 14–15`, `0:34.20–0:37.82`)** | Rubato rest -> `2/4` Coda @ `96 BPM` | Quarter-rest caesura (`𝄽`) -> three 16th pickup notes (`Duh-rip-it`, `♬ ♬ ♬` on `2-e-&-a`) -> accented Quarter-Note Downbeat (`NOW!`, `♩` on Beat `1`) | **Crisp Staccato Coda**: `rip` (`130 ms`) and `it` (`170 ms`) use unreleased stops (`[p̚, t̚]`) to create zero-bleed separation before the final `NOW!`. | Full-band stop-time break followed by a 3-note 16th pickup into the final stinger chord. |

---

## 4. What is Narrow IPA (`[ ... ]`) vs. Broad IPA (`/ ... /`)?

- **Broad (Phonemic) Transcription (`/ ... /`)**: Uses slashes and records only abstract dictionary phonemes that distinguish words in a language. It omits physical details like aspiration bursts, unreleased lip clamps, or glottal stops.
- **Narrow (Allophonic / Acoustic-Articulatory) Transcription (`[ ... ]`)**: Uses square brackets and diacritics (`ʰ`, `̚`, `ʔ`, `͡`, `̃`, `↑`, `ː`) to capture the exact **vocal-tract synthesizer & drum-machine mechanics** (`ATK`, `F0`, `F1/F2/F3`, `IOI`):

| Narrow IPA Symbol | Name | Physical / Percussive Meaning in `IMG_3268.mp3` | Example in Track |
| :--- | :--- | :--- | :--- |
| **`[pʰ, tʰ, kʰ]`** (`ʰ`) | **Aspirated release** | High-velocity puff of unvoiced air after the stop burst -> **crisp hi-hat / snare brush** | `[ˈpʰɪŋk̚]` (*pink*), `[ˈtʰɪk̚]` (*take*) |
| **`[p̚, t̚, k̚]`** (`̚`) | **Unreleased stop (clamp)** | Lips/tongue clamp shut at the end of the syllable without releasing air -> **noise gate / choked drum hit** | `[ˈkʰæmp̚]` (*camp*), `[ˈɹɪp̚ ˈɪt̚]` (*rip it*) |
| **`[ʔ]`** | **Glottal stop** | Vocal folds slam shut instantaneously (`2 ms` onset) -> **dry woodblock / rim click** | `[ˈʔɪn]` (*'in* at `08.46s`) |
| **`[t͡sʰ, p͡f˺]`** (`͡`) | **Affricate tie-bar** | Stop released directly into a tight sibilant channel -> **metallic closed hi-hat (`ts`)** | `[t͡sʰ]` (*ts* at `28.92s`, `31.84s`) |
| **`[χ, ʀ]`** | **Uvular fricative & trill** | Back of tongue scrapes/vibrates against uvula while jaw opens -> **DJ vinyl record scratch** | `[χː ˈʀæ]` (*Hhh-RA!* at `33.08s`) |
| **`[ɪ̃, ↑]`** (`̃`, `↑`) | **Nasalized vowel & upstep** | Velum lowers while larynx jumps to `500 Hz` falsetto -> **pinched synth squeak** | `[ˈwɪ̃n↑]` (*WHEN!* at `17.75s`) |
| **`[ː]`** | **Sustained resonance** | Holds vocal tract filter open -> **808 sub-bass sustain (`[buːm]`) or brass wah sweep (`[baʊː]`)** | `[ˈbuːm]` (*boom*), `[ˈbaʊː]` (*BOW!*) |

![Formant and Drum-Kit Space](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/fig0_phonetic_acoustic_space.png)

![Full Track earshot Sheet](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/IMG_3268_sheet.png)

---

## 5. All 14 Ultra-Zoomed 7-Tier Windows & Complete 147-Event Bracketed-Metadata Stream

Every single auditory event (`#001` to `#147`) now includes its **7-tier zoomed visualization** (`Waveform`, `Spectrogram + F1/F2/F3/F0`, `Musical Rhythm Notation & Beat Grid`, `English Syllable`, `Narrow IPA`, `Category & Articulation`, `Bracketed Metadata`) and its complete **Rhythm + Acoustic Metadata Bracket**:

`[#ID | start–end (dur, IOI) | BAR:MM GridPos | NOTE:SymbolType (Microtiming@BPM) | CAT | ART | ATK | PK | F0 | F1/F2/F3 | IPA] NoteSymbol Syllable`

### Zoom 01 (0:00.00 – 0:02.38) — Phrase 1A: Dental-Fricative Brushes & Nasal-Gated Plosives

![Zoom 01 (0:00.00 – 0:02.38) — Phrase 1A: Dental-Fricative Brushes & Nasal-Gated Plosives](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_01.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`0.00s – 2.38s`)

- `[#001 | 00.00–00.18s (180ms, IOI:180ms) | BAR:00 Pickup (4-a) | NOTE:[♪ rest] 16th-rest (free@103BPM) | CAT:NONVERBAL-FX | ART:Bilabial-Pre-Breath | ATK:2ms | PK:-51.7dB | F0:unvoiced | F1:813/F2:1488/F3:2540Hz | IPA:p͡f˺]` **[♪ rest] [lip-prep]**
- `[#002 | 00.18–00.26s (80ms, IOI:80ms) | BAR:00 Pickup (4-a) | NOTE:♬ 32nd (free@103BPM) | CAT:FRIC-BRUSH | ART:Voiced-Dental-Fric+Schwa | ATK:2ms | PK:-37.9dB | F0:unvoiced | F1:917/F2:1719/F3:3046Hz | IPA:ðə]` **♬ thuh**
- `[#003 | 00.26–00.38s (120ms, IOI:120ms) | BAR:01 Beat 1 (Downbeat) | NOTE:♪³ 16th-trip (+0ms@106BPM) | CAT:SNARE-SH | ART:Bilabial-Stop+Postalv-Affric | ATK:2ms | PK:-25.7dB | F0:unvoiced | F1:389/F2:1470/F3:2926Hz | IPA:ˈbɪtʃ]` **♪³ bitch**
- `[#004 | 00.38–00.54s (160ms, IOI:160ms) | BAR:01 1-e | NOTE:♪³ 16th-trip (-21ms@106BPM) | CAT:NASAL-GATE | ART:Asp-Velar+LowFront+Bilabial-Clamp | ATK:2ms | PK:-23.0dB | F0:107Hz | F1:345/F2:1984/F3:2731Hz | IPA:ˈkʰæmp̚]` **♪³ camp**
- `[#005 | 00.54–00.71s (170ms, IOI:170ms) | BAR:01 1-& | NOTE:♬ 16th (-2ms@106BPM) | CAT:BRASS-WAH | ART:Bilabial-Rhotic+OpenBack | ATK:2ms | PK:-25.6dB | F0:unvoiced | F1:1100/F2:2097/F3:2928Hz | IPA:ˈbɹɑː]` **♬ brah**
- `[#006 | 00.71–00.86s (150ms, IOI:150ms) | BAR:01 1-a | NOTE:♪³ 16th-trip (+26ms@106BPM) | CAT:FRIC-BRUSH | ART:Voiced-Dental-Fric+Schwa | ATK:2ms | PK:-20.3dB | F0:123Hz | F1:365/F2:2545/F3:3098Hz | IPA:ðə]` **♪³ thuh**
- `[#007 | 00.86–01.07s (210ms, IOI:210ms) | BAR:01 Beat 2 | NOTE:♬ 16th (+35ms@106BPM) | CAT:PLOSIVE-SCAT | ART:Rhotic+MidCentral+Unreleased-Labial | ATK:2ms | PK:-24.5dB | F0:unvoiced | F1:491/F2:1992/F3:2565Hz | IPA:ˈɹʌp̚]` **♬ rup**
- `[#008 | 01.07–01.16s (90ms, IOI:90ms) | BAR:01 2-& | NOTE:♬ 32nd (-38ms@106BPM) | CAT:NASAL-GATE | ART:HighFront-Lax+Alveolar-Nasal | ATK:2ms | PK:-17.9dB | F0:115Hz | F1:603/F2:1229/F3:2106Hz | IPA:ɪn]` **♬ in**
- `[#009 | 01.16–01.25s (90ms, IOI:90ms) | BAR:01 2-trip-let (3rd) | NOTE:♬ 32nd (-42ms@106BPM) | CAT:FRIC-BRUSH | ART:Voiced-Dental-Fric+Schwa | ATK:2ms | PK:-18.4dB | F0:102Hz | F1:624/F2:1222/F3:1999Hz | IPA:ðə]` **♬ thuh**
- `[#010 | 01.25–01.51s (260ms, IOI:260ms) | BAR:01 2-a | NOTE:♬· dotted-16th (+1ms@106BPM) | CAT:HAT-TICK | ART:Asp-Bilabial+Nasal-Alveolar-Stop | ATK:2ms | PK:-20.4dB | F0:103Hz | F1:503/F2:1027/F3:2225Hz | IPA:ˈpʰænt̚]` **♬· pant**
- `[#011 | 01.51–01.73s (220ms, IOI:220ms) | BAR:01 3-e | NOTE:♬ 16th (-21ms@106BPM) | CAT:SNARE-SH | ART:Dental-Fric+Alveolar-Sibilant-Tail | ATK:2ms | PK:-16.7dB | F0:113Hz | F1:531/F2:969/F3:1966Hz | IPA:ˈðɛns]` **♬ thence**
- `[#012 | 01.73–01.89s (160ms, IOI:160ms) | BAR:01 3-trip-let (3rd) | NOTE:♪³ 16th-trip (-37ms@106BPM) | CAT:KICK-GHOST | ART:Voiced-Bilabial+Labial-Check | ATK:2ms | PK:-23.8dB | F0:98Hz | F1:462/F2:1290/F3:2517Hz | IPA:ˈbʌp̚]` **♪³ bup**
- `[#013 | 01.89–01.97s (80ms, IOI:80ms) | BAR:01 3-a+ (32nd pickup) | NOTE:♬ 32nd (+6ms@106BPM) | CAT:KICK-GHOST | ART:Mid-Central-Schwa-Pulse | ATK:2ms | PK:-29.8dB | F0:unvoiced | F1:458/F2:1510/F3:2591Hz | IPA:ə]` **♬ uh**
- `[#014 | 01.97–02.06s (90ms, IOI:90ms) | BAR:01 Beat 4 | NOTE:♬ 32nd (+15ms@106BPM) | CAT:PLOSIVE-SCAT | ART:Voiced-Velar-Stop+Schwa | ATK:2ms | PK:-25.4dB | F0:unvoiced | F1:1157/F2:1826/F3:2730Hz | IPA:ɡə]` **♬ guh**
- `[#015 | 02.06–02.21s (150ms, IOI:150ms) | BAR:01 4-e | NOTE:♪³ 16th-trip (-36ms@106BPM) | CAT:HAT-TICK | ART:Asp-Velar-Stop+OpenBack | ATK:2ms | PK:-20.8dB | F0:113Hz | F1:524/F2:1998/F3:2439Hz | IPA:ˈkʰɑː]` **♪³ kah**
- `[#016 | 02.21–02.38s (170ms, IOI:170ms) | BAR:01 4-& | NOTE:♬ 16th (-27ms@106BPM) | CAT:NASAL-GATE | ART:Bilabial-Stop+Nasal-Bilabial-Clamp | ATK:2ms | PK:-27.7dB | F0:unvoiced | F1:627/F2:1707/F3:2670Hz | IPA:pʌmp̚]` **♬ pump**

---

### Zoom 02 (0:02.38 – 0:04.75) — Phrase 1B: Labiodental Flams ('frup / fup-it') & Back-Vowel Hold ('all!')

![Zoom 02 (0:02.38 – 0:04.75) — Phrase 1B: Labiodental Flams ('frup / fup-it') & Back-Vowel Hold ('all!')](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_02.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`2.38s – 4.75s`)

- `[#017 | 02.38–02.52s (140ms, IOI:140ms) | BAR:01 4-a | NOTE:♪³ 16th-trip (+1ms@106BPM) | CAT:FRIC-BRUSH | ART:Voiced-Dental-Fric+Schwa | ATK:2ms | PK:-19.0dB | F0:128Hz | F1:400/F2:1755/F3:2211Hz | IPA:ðə]` **♪³ thuh**
- `[#018 | 02.52–02.73s (210ms, IOI:210ms) | BAR:01 Beat 1 (Downbeat) | NOTE:♬ 16th (+0ms@106BPM) | CAT:FRIC-BRUSH | ART:Labiodental-Fric+Rhotic+Labial-Stop | ATK:2ms | PK:-23.6dB | F0:unvoiced | F1:569/F2:1948/F3:2739Hz | IPA:ˈfɹʌp̚]` **♬ frup**
- `[#019 | 02.73–02.88s (150ms, IOI:150ms) | BAR:02 1-trip-let (2nd) | NOTE:♪³ 16th-trip (+10ms@100BPM) | CAT:NASAL-GATE | ART:HighFront-Lax+Alveolar-Nasal | ATK:2ms | PK:-31.9dB | F0:100Hz | F1:1586/F2:2953/F3:3622Hz | IPA:ɪn]` **♪³ in**
- `[#020 | 02.88–03.04s (160ms, IOI:160ms) | BAR:02 1-trip-let (3rd) | NOTE:♪³ 16th-trip (-40ms@100BPM) | CAT:FRIC-BRUSH | ART:Voiced-Dental-Fric+Schwa | ATK:2ms | PK:-19.9dB | F0:unvoiced | F1:545/F2:1338/F3:2117Hz | IPA:ðə]` **♪³ thuh**
- `[#021 | 03.04–03.22s (180ms, IOI:180ms) | BAR:02 1-a+ (32nd pickup) | NOTE:♬ 16th (-5ms@100BPM) | CAT:FRIC-BRUSH | ART:Labiodental-Fric+MidCentral+Labial-Stop | ATK:2ms | PK:-22.3dB | F0:86Hz | F1:499/F2:1490/F3:1991Hz | IPA:ˈfʌp̚]` **♬ fup**
- `[#022 | 03.22–03.36s (140ms, IOI:140ms) | BAR:02 2-e | NOTE:♪³ 16th-trip (-50ms@100BPM) | CAT:HAT-TICK | ART:HighFront-Lax+Unreleased-Alveolar | ATK:2ms | PK:-27.0dB | F0:unvoiced | F1:536/F2:1906/F3:2341Hz | IPA:ɪt̚]` **♪³ it**
- `[#023 | 03.36–03.70s (340ms, IOI:340ms) | BAR:02 2-trip-let (2nd) | NOTE:♬· dotted-16th (+40ms@100BPM) | CAT:HAT-TICK | ART:LowFront-Open+Unreleased-Alveolar | ATK:2ms | PK:-21.2dB | F0:unvoiced | F1:638/F2:1503/F3:2232Hz | IPA:ˈæt̚]` **♬· at**
- `[#024 | 03.70–04.35s (650ms, IOI:650ms) | BAR:02 Beat 4 | NOTE:♪· dotted-8th (-20ms@100BPM) | CAT:BRASS-WAH | ART:OpenMid-Back-Rounded+Dark-Lateral | ATK:2ms | PK:-17.8dB | F0:110Hz | F1:558/F2:1246/F3:1946Hz | IPA:ˈɔːl]` **♪· all!**
- `[#025 | 04.35–04.75s (400ms, IOI:400ms) | BAR:02 Beat 4 | NOTE:[♪ rest] 16th-rest (+30ms@100BPM) | CAT:NONVERBAL-FX | ART:Glottal-Release+Silent-Breath-Gap | ATK:2ms | PK:-21.2dB | F0:101Hz | F1:481/F2:1653/F3:2309Hz | IPA:ʔ‿h̥]` **[♪ rest] [drop-pause]**

---

### Zoom 03 (0:04.75 – 0:08.15) — Phrase 2A: Sub-Bass Hum ('Mmmm!') & Cork-Pop Velar Scat ('cup / pink / cane')

![Zoom 03 (0:04.75 – 0:08.15) — Phrase 2A: Sub-Bass Hum ('Mmmm!') & Cork-Pop Velar Scat ('cup / pink / cane')](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_03.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`4.75s – 8.15s`)

- `[#026 | 04.75–05.48s (730ms, IOI:730ms) | BAR:03 Beat 1 (Downbeat) | NOTE:♪· dotted-8th (+0ms@83BPM) | CAT:NASAL-GATE | ART:Prolonged-Bilabial-Nasal+Glottal-Lip-Pop | ATK:2ms | PK:-16.0dB | F0:100Hz | F1:570/F2:1005/F3:2270Hz | IPA:ˈmːˀp]` **♪· Mmmm!**
- `[#027 | 05.48–06.05s (570ms, IOI:570ms) | BAR:03 Beat 2 | NOTE:[♩ rest] quarter-rest (+5ms@83BPM) | CAT:NONVERBAL-FX | ART:Unvoiced-Nasal-Exhale-Gap | ATK:2ms | PK:-31.7dB | F0:unvoiced | F1:675/F2:907/F3:2331Hz | IPA:h̥ː]` **[♩ rest] [breath-gap]**
- `[#028 | 06.05–06.20s (150ms, IOI:150ms) | BAR:03 2-a | NOTE:♪³ 16th-trip (+32ms@83BPM) | CAT:FRIC-BRUSH | ART:Voiced-Dental-Fric+Schwa | ATK:2ms | PK:-19.8dB | F0:134Hz | F1:286/F2:1210/F3:2615Hz | IPA:ðə]` **♪³ thuh**
- `[#029 | 06.20–06.40s (200ms, IOI:200ms) | BAR:03 Beat 1 (Downbeat) | NOTE:♪³ 16th-trip (+1ms@83BPM) | CAT:GLOTTAL-POP | ART:Asp-Velar-Stop+Unreleased-Labial | ATK:2ms | PK:-21.3dB | F0:89Hz | F1:302/F2:1189/F3:2595Hz | IPA:ˈkʰʌp̚]` **♪³ cup**
- `[#030 | 06.40–06.55s (150ms, IOI:150ms) | BAR:04 1-trip-let (2nd) | NOTE:♪³ 16th-trip (-15ms@93BPM) | CAT:KICK-GHOST | ART:Mid-Central-Schwa | ATK:2ms | PK:-26.1dB | F0:65Hz | F1:1431/F2:2645/F3:3663Hz | IPA:ə]` **♪³ uh**
- `[#031 | 06.55–06.69s (140ms, IOI:140ms) | BAR:04 1-& | NOTE:♪³ 16th-trip (+27ms@93BPM) | CAT:FRIC-BRUSH | ART:Voiced-Dental-Fric+Schwa | ATK:2ms | PK:-24.5dB | F0:unvoiced | F1:399/F2:1813/F3:2431Hz | IPA:ðə]` **♪³ thuh**
- `[#032 | 06.69–07.00s (310ms, IOI:310ms) | BAR:04 1-a | NOTE:♬· dotted-16th (+6ms@93BPM) | CAT:GLOTTAL-POP | ART:Asp-Bilabial+Velar-Nasal-Stop | ATK:2ms | PK:-13.1dB | F0:unvoiced | F1:1059/F2:1904/F3:2517Hz | IPA:ˈpʰɪŋk̚]` **♬· pink**
- `[#033 | 07.00–07.45s (450ms, IOI:450ms) | BAR:04 2-e | NOTE:♪³ 8th-trip (-6ms@93BPM) | CAT:PLOSIVE-SCAT | ART:Asp-Velar+Front-Closing-Diphthong | ATK:2ms | PK:-17.2dB | F0:unvoiced | F1:428/F2:1144/F3:2614Hz | IPA:ˈkʰeɪn]` **♪³ cane**
- `[#034 | 07.45–07.60s (150ms, IOI:150ms) | BAR:04 3-a+ (32nd pickup) | NOTE:♪³ 16th-trip (+40ms@93BPM) | CAT:HAT-TICK | ART:Asp-Alveolar-Stop+Schwa | ATK:2ms | PK:-13.5dB | F0:128Hz | F1:985/F2:1789/F3:2941Hz | IPA:tʰə]` **♪³ tuh**
- `[#035 | 07.60–07.80s (200ms, IOI:200ms) | BAR:04 3-e | NOTE:♬ 16th (-52ms@93BPM) | CAT:PLOSIVE-SCAT | ART:Rhotic+HighFront+Unreleased-Labial | ATK:2ms | PK:-19.0dB | F0:106Hz | F1:401/F2:1216/F3:2801Hz | IPA:ˈɹɪp̚]` **♬ rip**
- `[#036 | 07.80–07.98s (180ms, IOI:180ms) | BAR:04 3-& | NOTE:♪³ 16th-trip (-13ms@93BPM) | CAT:NASAL-GATE | ART:HighFront+Alveolar-Nasal | ATK:2ms | PK:-16.4dB | F0:91Hz | F1:445/F2:1914/F3:2751Hz | IPA:ɪn]` **♪³ in**
- `[#037 | 07.98–08.15s (170ms, IOI:170ms) | BAR:04 3-a | NOTE:♪³ 16th-trip (+6ms@93BPM) | CAT:FRIC-BRUSH | ART:Voiced-Dental-Fric+Schwa | ATK:2ms | PK:-13.2dB | F0:123Hz | F1:442/F2:1619/F3:1926Hz | IPA:ðə]` **♪³ thuh**

---

### Zoom 04 (0:08.15 – 0:12.50) — Phrase 2B: Glottal Stops ('ki-'in'), Mini-Wah ('bow') & Inhale Gasp

![Zoom 04 (0:08.15 – 0:12.50) — Phrase 2B: Glottal Stops ('ki-'in'), Mini-Wah ('bow') & Inhale Gasp](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_04.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`8.15s – 12.50s`)

- `[#038 | 08.15–08.46s (310ms, IOI:310ms) | BAR:04 Beat 4 | NOTE:♬· dotted-16th (+14ms@93BPM) | CAT:GLOTTAL-POP | ART:Asp-Velar+Glottal-Cut-Vowel | ATK:2ms | PK:-20.9dB | F0:105Hz | F1:411/F2:2309/F3:3009Hz | IPA:ˈkʰɪ]` **♬· ki**
- `[#039 | 08.46–08.78s (320ms, IOI:320ms) | BAR:04 4-& | NOTE:♬· dotted-16th (+2ms@93BPM) | CAT:GLOTTAL-POP | ART:Hard-Glottal-Stop+HighFront-Nasal | ATK:2ms | PK:-22.7dB | F0:unvoiced | F1:603/F2:1765/F3:2777Hz | IPA:ˈʔɪn]` **♬· 'in**
- `[#040 | 08.78–09.05s (270ms, IOI:270ms) | BAR:04 Beat 2 | NOTE:♬ 16th (-1ms@93BPM) | CAT:KICK-GHOST | ART:Voiced-Bilabial+Velar-Stop-Check | ATK:2ms | PK:-17.6dB | F0:113Hz | F1:406/F2:1230/F3:2851Hz | IPA:ˈbɪk̚]` **♬ bick**
- `[#041 | 09.05–09.28s (230ms, IOI:230ms) | BAR:05 1-& | NOTE:♬ 16th (-45ms@95BPM) | CAT:NASAL-GATE | ART:HighFront+Alveolar-Nasal | ATK:2ms | PK:-24.1dB | F0:101Hz | F1:274/F2:1130/F3:2507Hz | IPA:ɪn]` **♬ in**
- `[#042 | 09.28–09.44s (160ms, IOI:160ms) | BAR:05 1-a | NOTE:♪³ 16th-trip (+27ms@95BPM) | CAT:FRIC-BRUSH | ART:Voiced-Dental-Fric+Schwa | ATK:2ms | PK:-15.9dB | F0:unvoiced | F1:464/F2:2057/F3:2389Hz | IPA:ðə]` **♪³ thuh**
- `[#043 | 09.44–09.73s (290ms, IOI:290ms) | BAR:05 Beat 2 | NOTE:♬· dotted-16th (+30ms@95BPM) | CAT:BRASS-WAH | ART:Voiced-Bilabial+Open-to-Rounded-Diphthong | ATK:2ms | PK:-18.6dB | F0:95Hz | F1:439/F2:2186/F3:2874Hz | IPA:ˈbaʊ]` **♬· bow**
- `[#044 | 09.73–10.01s (280ms, IOI:280ms) | BAR:05 2-& | NOTE:♬· dotted-16th (+5ms@95BPM) | CAT:FRIC-BRUSH | ART:Labiodental-Fric+MidFront-Nasal | ATK:2ms | PK:-14.4dB | F0:114Hz | F1:623/F2:1433/F3:2212Hz | IPA:ˈfɛn]` **♬· fen**
- `[#045 | 10.01–10.18s (170ms, IOI:170ms) | BAR:05 Beat 4 | NOTE:♪³ 16th-trip (-30ms@95BPM) | CAT:HAT-TICK | ART:Asp-Alveolar-Stop+Schwa | ATK:2ms | PK:-16.8dB | F0:117Hz | F1:462/F2:2178/F3:2335Hz | IPA:tʰə]` **♪³ tuh**
- `[#046 | 10.18–10.51s (330ms, IOI:330ms) | BAR:05 3-e | NOTE:♬· dotted-16th (-18ms@95BPM) | CAT:SNARE-SH | ART:Alveolar-Sibilant+Velar-Check | ATK:2ms | PK:-21.3dB | F0:unvoiced | F1:1702/F2:3087/F3:4233Hz | IPA:ˈsɪk̚]` **♬· sick**
- `[#047 | 10.51–10.67s (160ms, IOI:160ms) | BAR:05 3-a | NOTE:♪³ 16th-trip (-3ms@95BPM) | CAT:NASAL-GATE | ART:HighFront+Alveolar-Nasal | ATK:2ms | PK:-20.4dB | F0:unvoiced | F1:406/F2:2230/F3:2714Hz | IPA:ɪn]` **♪³ in**
- `[#048 | 10.67–10.80s (130ms, IOI:130ms) | BAR:05 Beat 1 | NOTE:♪³ 16th-trip (-1ms@95BPM) | CAT:FRIC-BRUSH | ART:Voiced-Dental-Fric+Schwa | ATK:2ms | PK:-13.6dB | F0:111Hz | F1:416/F2:2170/F3:2712Hz | IPA:ðə]` **♪³ thuh**
- `[#049 | 10.80–10.95s (150ms, IOI:150ms) | BAR:05 4-e | NOTE:♪³ 16th-trip (-28ms@95BPM) | CAT:HAT-TICK | ART:Asp-Velar-Stop+Schwa | ATK:2ms | PK:-17.9dB | F0:109Hz | F1:513/F2:2121/F3:2755Hz | IPA:kʰə]` **♪³ kuh**
- `[#050 | 10.95–11.14s (190ms, IOI:190ms) | BAR:05 4-& | NOTE:♬ 16th (-36ms@95BPM) | CAT:LIQUID-CHOP | ART:Alveolar-Lateral+Labial-Stop | ATK:2ms | PK:-19.9dB | F0:100Hz | F1:535/F2:1587/F3:2512Hz | IPA:ˈlɪp̚]` **♬ lip**
- `[#051 | 11.14–11.30s (160ms, IOI:160ms) | BAR:05 4-a | NOTE:♪³ 16th-trip (-3ms@95BPM) | CAT:NASAL-GATE | ART:HighFront+Alveolar-Nasal | ATK:2ms | PK:-13.8dB | F0:121Hz | F1:549/F2:1766/F3:2046Hz | IPA:ɪn]` **♪³ in**
- `[#052 | 11.30–11.72s (420ms, IOI:420ms) | BAR:05 Beat 2 | NOTE:♪³ 8th-trip (-1ms@95BPM) | CAT:BRASS-WAH | ART:Alveolar-Nasal+Wide-Diphthong-Sweep | ATK:2ms | PK:-11.8dB | F0:103Hz | F1:503/F2:1827/F3:2669Hz | IPA:ˈnaʊ]` **♪³ NOW!**
- `[#053 | 11.72–12.50s (780ms, IOI:780ms) | BAR:05 1-trip-let (3rd) | NOTE:[♩ rest] quarter-rest (-1ms@95BPM) | CAT:NONVERBAL-FX | ART:Deep-Ingressive-Pulmonic-Breath | ATK:2ms | PK:-38.2dB | F0:unvoiced | F1:832/F2:1345/F3:2525Hz | IPA:hː↓]` **[♩ rest] [inhale-gasp]**

---

### Zoom 05 (0:12.50 – 0:15.60) — Phrase 3A: Call Hook & Synth-Brass Diphthong Wah Stabs ('BOW-buh-BOW-BOW-BOW!')

![Zoom 05 (0:12.50 – 0:15.60) — Phrase 3A: Call Hook & Synth-Brass Diphthong Wah Stabs ('BOW-buh-BOW-BOW-BOW!')](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_05.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`12.50s – 15.60s`)

- `[#054 | 12.50–12.72s (220ms, IOI:220ms) | BAR:06 Beat 1 (Downbeat) | NOTE:♬ 16th (+0ms@98BPM) | CAT:HOOK-VOX | ART:Palatal-Approx+HighBack-Rounded | ATK:2ms | PK:-26.8dB | F0:unvoiced | F1:1166/F2:1622/F3:2999Hz | IPA:ju]` **♬ You**
- `[#055 | 12.72–12.92s (200ms, IOI:200ms) | BAR:06 1-trip-let (2nd) | NOTE:♬ 16th (+16ms@98BPM) | CAT:HOOK-VOX | ART:Alveolar-Nasal+MidBack-Diphthong | ATK:2ms | PK:-22.8dB | F0:91Hz | F1:356/F2:1893/F3:2556Hz | IPA:ˈnoʊ]` **♬ know**
- `[#056 | 12.92–13.09s (170ms, IOI:170ms) | BAR:06 1-trip-let (3rd) | NOTE:♪³ 16th-trip (+12ms@98BPM) | CAT:HOOK-VOX | ART:Labial-Velar+MidCentral+Alv-Stop | ATK:2ms | PK:-16.9dB | F0:98Hz | F1:488/F2:1353/F3:2423Hz | IPA:ˈwʌt̚]` **♪³ what**
- `[#057 | 13.09–13.55s (460ms, IOI:460ms) | BAR:06 Beat 3 | NOTE:♪ 8th (-22ms@98BPM) | CAT:BRASS-WAH | ART:Heavy-Bilabial+F1:748->350Hz-Sweep | ATK:2ms | PK:-7.2dB | F0:unvoiced | F1:759/F2:1350/F3:2381Hz | IPA:ˈbaʊ]` **♪ BOW**
- `[#058 | 13.55–13.72s (170ms, IOI:170ms) | BAR:06 2-a | NOTE:♪³ 16th-trip (-21ms@98BPM) | CAT:KICK-GHOST | ART:Soft-Bilabial-Stop+Schwa | ATK:2ms | PK:-21.8dB | F0:unvoiced | F1:608/F2:1040/F3:2416Hz | IPA:bə]` **♪³ buh**
- `[#059 | 13.72–14.03s (310ms, IOI:310ms) | BAR:06 Beat 4 | NOTE:♬· dotted-16th (-4ms@98BPM) | CAT:BRASS-WAH | ART:Heavy-Bilabial+Open-to-Rounded-Glide | ATK:2ms | PK:-10.9dB | F0:97Hz | F1:779/F2:1422/F3:2433Hz | IPA:ˈbaʊ]` **♬· BOW**
- `[#060 | 14.03–14.34s (310ms, IOI:310ms) | BAR:06 3-& | NOTE:♬· dotted-16th (-1ms@98BPM) | CAT:BRASS-WAH | ART:Heavy-Bilabial+Open-to-Rounded-Glide | ATK:2ms | PK:-17.3dB | F0:unvoiced | F1:967/F2:1402/F3:1898Hz | IPA:ˈbaʊ]` **♬· BOW**
- `[#061 | 14.34–14.88s (540ms, IOI:540ms) | BAR:06 Beat 4 | NOTE:♪ 8th (+3ms@98BPM) | CAT:BRASS-WAH | ART:Heavy-Bilabial+Long-Resonant-Sweep | ATK:2ms | PK:-8.9dB | F0:114Hz | F1:800/F2:1365/F3:2294Hz | IPA:ˈbaʊː]` **♪ BOW!**
- `[#062 | 14.88–15.04s (160ms, IOI:160ms) | BAR:06 4-a+ (32nd pickup) | NOTE:♪³ 16th-trip (+8ms@98BPM) | CAT:HOOK-VOX | ART:Palatal-Approx+HighBack | ATK:2ms | PK:-17.7dB | F0:118Hz | F1:499/F2:973/F3:2425Hz | IPA:ju]` **♪³ You**
- `[#063 | 15.04–15.18s (140ms, IOI:140ms) | BAR:06 1-e | NOTE:♪³ 16th-trip (-62ms@98BPM) | CAT:HOOK-VOX | ART:Alveolar-Nasal+Diphthong | ATK:2ms | PK:-18.7dB | F0:unvoiced | F1:443/F2:1450/F3:2594Hz | IPA:ˈnoʊ]` **♪³ know**
- `[#064 | 15.18–15.32s (140ms, IOI:140ms) | BAR:06 1-trip-let (2nd) | NOTE:♪³ 16th-trip (+27ms@98BPM) | CAT:HOOK-VOX | ART:Labial-Velar+Alv-Check | ATK:2ms | PK:-12.9dB | F0:99Hz | F1:814/F2:1804/F3:2256Hz | IPA:wʌt̚]` **♪³ what**
- `[#065 | 15.32–15.60s (280ms, IOI:280ms) | BAR:06 1-trip-let (3rd) | NOTE:♬· dotted-16th (-37ms@98BPM) | CAT:BRASS-WAH | ART:Alveolar-Nasal+Diphthong | ATK:2ms | PK:-16.4dB | F0:104Hz | F1:753/F2:1498/F3:2328Hz | IPA:ˈnaʊ]` **♬· now**

---

### Zoom 06 (0:15.60 – 0:18.47) — Phrase 3B: Metric Call-and-Response & Pinched Falsetto Squeak ('WHEN!↑')

![Zoom 06 (0:15.60 – 0:18.47) — Phrase 3B: Metric Call-and-Response & Pinched Falsetto Squeak ('WHEN!↑')](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_06.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`15.60s – 18.47s`)

- `[#066 | 15.60–15.77s (170ms, IOI:170ms) | BAR:07 1-& | NOTE:[♪ rest] 16th-rest (+27ms@118BPM) | CAT:NONVERBAL-FX | ART:Short-Glottal-Air-Vent | ATK:2ms | PK:-37.7dB | F0:unvoiced | F1:989/F2:1578/F3:2940Hz | IPA:h̥]` **[♪ rest] [micro-breath]**
- `[#067 | 15.77–15.94s (170ms, IOI:170ms) | BAR:07 1-a+ (32nd pickup) | NOTE:♬ 16th (+7ms@118BPM) | CAT:HOOK-VOX | ART:Palatal-Approx+HighBack | ATK:2ms | PK:-18.6dB | F0:106Hz | F1:257/F2:2161/F3:2472Hz | IPA:ju]` **♬ You**
- `[#068 | 15.94–16.09s (150ms, IOI:150ms) | BAR:07 2-e | NOTE:♪³ 16th-trip (-13ms@118BPM) | CAT:HOOK-VOX | ART:Alveolar-Nasal+Diphthong | ATK:2ms | PK:-22.6dB | F0:107Hz | F1:420/F2:964/F3:2479Hz | IPA:ˈnoʊ]` **♪³ know**
- `[#069 | 16.09–16.25s (160ms, IOI:160ms) | BAR:07 2-& | NOTE:♬ 16th (+10ms@118BPM) | CAT:HOOK-VOX | ART:Labial-Velar+Alv-Check | ATK:2ms | PK:-21.2dB | F0:114Hz | F1:353/F2:1501/F3:2443Hz | IPA:wʌt̚]` **♬ what**
- `[#070 | 16.25–16.46s (210ms, IOI:210ms) | BAR:07 2-a+ (32nd pickup) | NOTE:♬ 16th (-19ms@118BPM) | CAT:BRASS-WAH | ART:Alveolar-Nasal+Diphthong | ATK:2ms | PK:-20.6dB | F0:102Hz | F1:594/F2:1750/F3:2479Hz | IPA:ˈnaʊ]` **♬ now**
- `[#071 | 16.46–16.60s (140ms, IOI:140ms) | BAR:07 3-e | NOTE:♪³ 16th-trip (+1ms@118BPM) | CAT:HOOK-VOX | ART:Palatal-Approx+HighBack | ATK:2ms | PK:-21.0dB | F0:110Hz | F1:284/F2:2175/F3:2728Hz | IPA:ju]` **♪³ You**
- `[#072 | 16.60–16.74s (140ms, IOI:140ms) | BAR:07 3-& | NOTE:♪³ 16th-trip (+14ms@118BPM) | CAT:HOOK-VOX | ART:Alveolar-Nasal+Diphthong | ATK:2ms | PK:-20.5dB | F0:113Hz | F1:339/F2:1242/F3:2336Hz | IPA:ˈnoʊ]` **♪³ know**
- `[#073 | 16.74–16.90s (160ms, IOI:160ms) | BAR:07 3-a | NOTE:♬ 16th (+28ms@118BPM) | CAT:HOOK-VOX | ART:Labial-Velar+Alv-Check | ATK:2ms | PK:-14.7dB | F0:116Hz | F1:381/F2:1620/F3:2050Hz | IPA:wʌt̚]` **♬ what**
- `[#074 | 16.90–17.26s (360ms, IOI:360ms) | BAR:07 Beat 4 | NOTE:♪³ 8th-trip (+61ms@118BPM) | CAT:NASAL-GATE | ART:Voiced-Dental+MidFront-Nasal | ATK:2ms | PK:-18.2dB | F0:135Hz | F1:379/F2:2400/F3:3031Hz | IPA:ˈðɛn]` **♪³ then**
- `[#075 | 17.26–17.46s (200ms, IOI:200ms) | BAR:07 4-a+ (32nd pickup) | NOTE:♬ 16th (-22ms@118BPM) | CAT:HOOK-VOX | ART:Palatal-Approx+HighBack | ATK:2ms | PK:-26.5dB | F0:unvoiced | F1:903/F2:2198/F3:2729Hz | IPA:ju]` **♬ You**
- `[#076 | 17.46–17.60s (140ms, IOI:140ms) | BAR:07 1-e | NOTE:♪³ 16th-trip (-12ms@118BPM) | CAT:HOOK-VOX | ART:Alveolar-Nasal+Diphthong | ATK:2ms | PK:-22.0dB | F0:113Hz | F1:280/F2:2445/F3:3110Hz | IPA:ˈnoʊ]` **♪³ know**
- `[#077 | 17.60–17.75s (150ms, IOI:150ms) | BAR:07 1-& | NOTE:♪³ 16th-trip (+2ms@118BPM) | CAT:HOOK-VOX | ART:Labial-Velar+Alv-Check | ATK:2ms | PK:-18.6dB | F0:unvoiced | F1:416/F2:1774/F3:2470Hz | IPA:wʌt̚]` **♪³ what**
- `[#078 | 17.75–18.12s (370ms, IOI:370ms) | BAR:07 1-a | NOTE:♪ 8th (+25ms@118BPM) | CAT:FALSETTO-SQ | ART:High-Larynx-Nasalized-Falsetto-Squeak | ATK:2ms | PK:-16.8dB | F0:125Hz | F1:550/F2:693/F3:2364Hz | IPA:ˈwɪ̃n↑]` **♪ WHEN!↑**
- `[#079 | 18.12–18.27s (150ms, IOI:150ms) | BAR:07 2-& | NOTE:♪³ 16th-trip (+15ms@118BPM) | CAT:HOOK-VOX | ART:Fast-Palatal-Pickup | ATK:2ms | PK:-45.3dB | F0:unvoiced | F1:364/F2:1278/F3:2696Hz | IPA:ju]` **♪³ You**
- `[#080 | 18.27–18.37s (100ms, IOI:100ms) | BAR:07 2-a+ (32nd pickup) | NOTE:♪³ 16th-trip (-25ms@118BPM) | CAT:HOOK-VOX | ART:Fast-Nasal-Pickup | ATK:2ms | PK:-24.3dB | F0:unvoiced | F1:1085/F2:1824/F3:2815Hz | IPA:noʊ]` **♪³ know**
- `[#081 | 18.37–18.47s (100ms, IOI:100ms) | BAR:07 Beat 3 | NOTE:♪³ 16th-trip (+12ms@118BPM) | CAT:HOOK-VOX | ART:Clipped-Alveolar-Setup | ATK:2ms | PK:-27.1dB | F0:unvoiced | F1:889/F2:2182/F3:2821Hz | IPA:wʌt̚]` **♪³ what**

---

### Zoom 07 (0:18.47 – 0:20.54) — Phrase 3C: 32nd-Note Plosive Drum Roll ('thuh-buh-chuh-kuh-buh-GAH!') & 'skibidi-BAH!'

![Zoom 07 (0:18.47 – 0:20.54) — Phrase 3C: 32nd-Note Plosive Drum Roll ('thuh-buh-chuh-kuh-buh-GAH!') & 'skibidi-BAH!'](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_07.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`18.47s – 20.54s`)

- `[#082 | 18.47–18.56s (90ms, IOI:90ms) | BAR:07 3-e | NOTE:♬ 32nd-roll (-15ms@118BPM) | CAT:FRIC-BRUSH | ART:Dental-Fricative-Grace-Note | ATK:2ms | PK:-13.0dB | F0:241Hz | F1:254/F2:2368/F3:2449Hz | IPA:ðə]` **♬ thuh**
- `[#083 | 18.56–18.65s (90ms, IOI:90ms) | BAR:08 1-e | NOTE:♬ 32nd-roll (-39ms@116BPM) | CAT:KICK-GHOST | ART:Bilabial-Plosive-Pop | ATK:2ms | PK:-13.7dB | F0:219Hz | F1:250/F2:1028/F3:2380Hz | IPA:bə]` **♬ buh**
- `[#084 | 18.65–18.75s (100ms, IOI:100ms) | BAR:08 1-trip-let (2nd) | NOTE:♬ 32nd-roll (+8ms@116BPM) | CAT:SNARE-SH | ART:Postalveolar-Affricate-Tick | ATK:2ms | PK:-12.4dB | F0:168Hz | F1:340/F2:1526/F3:2642Hz | IPA:tʃə]` **♬ chuh**
- `[#085 | 18.75–18.84s (90ms, IOI:90ms) | BAR:08 1-& | NOTE:♬ 32nd-roll (+21ms@116BPM) | CAT:HAT-TICK | ART:Velar-Plosive-Tick | ATK:2ms | PK:-18.8dB | F0:257Hz | F1:344/F2:1180/F3:2853Hz | IPA:kʰə]` **♬ kuh**
- `[#086 | 18.84–18.94s (100ms, IOI:100ms) | BAR:08 1-a | NOTE:♬ 32nd-roll (-18ms@116BPM) | CAT:KICK-GHOST | ART:Bilabial-Pre-Hit-Bounce | ATK:2ms | PK:-20.6dB | F0:219Hz | F1:290/F2:1357/F3:2793Hz | IPA:bə]` **♬ buh**
- `[#087 | 18.94–19.35s (410ms, IOI:410ms) | BAR:08 1-a+ (32nd pickup) | NOTE:♪ 8th (+17ms@116BPM) | CAT:BRASS-WAH | ART:Voiced-Velar+Wide-Open-Pharynx | ATK:2ms | PK:-13.8dB | F0:unvoiced | F1:1748/F2:2518/F3:3405Hz | IPA:ˈɡɑː]` **♪ GAH!**
- `[#088 | 19.35–19.51s (160ms, IOI:160ms) | BAR:08 2-trip-let (3rd) | NOTE:♪³ 16th-triplet (+18ms@116BPM) | CAT:HAT-TICK | ART:Sibilant-Velar-Cluster+HighFront | ATK:2ms | PK:-17.1dB | F0:144Hz | F1:378/F2:652/F3:2548Hz | IPA:ˈskɪ]` **♪³ ski**
- `[#089 | 19.51–19.65s (140ms, IOI:140ms) | BAR:08 Beat 3 | NOTE:♪³ 16th-triplet (+6ms@116BPM) | CAT:PLOSIVE-SCAT | ART:Bilabial-Stop+HighFront | ATK:2ms | PK:-18.0dB | F0:169Hz | F1:469/F2:1190/F3:3090Hz | IPA:bɪ]` **♪³ bi**
- `[#090 | 19.65–19.85s (200ms, IOI:200ms) | BAR:08 3-e | NOTE:♪³ 16th-triplet (+16ms@116BPM) | CAT:LIQUID-CHOP | ART:Alveolar-Flap-Stop+HighFront | ATK:2ms | PK:-17.9dB | F0:unvoiced | F1:484/F2:2144/F3:2574Hz | IPA:dɪ]` **♪³ di**
- `[#091 | 19.85–20.54s (690ms, IOI:690ms) | BAR:08 3-trip-let (3rd) | NOTE:♪· dotted-8th (+0ms@116BPM) | CAT:BRASS-WAH | ART:Heavy-Bilabial+Open-Back-Vowel | ATK:2ms | PK:-10.4dB | F0:107Hz | F1:1680/F2:2575/F3:3561Hz | IPA:ˈbɑː]` **♪· BAH!**

---

### Zoom 08 (0:20.54 – 0:22.92) — Phrase 3D: Double-Tongued Lateral-Labial-Velar Chopper ('buh-lip-uh-gih-buh-lep-uh-DAH!')

![Zoom 08 (0:20.54 – 0:22.92) — Phrase 3D: Double-Tongued Lateral-Labial-Velar Chopper ('buh-lip-uh-gih-buh-lep-uh-DAH!')](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_08.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`20.54s – 22.92s`)

- `[#092 | 20.54–20.72s (180ms, IOI:180ms) | BAR:08 Beat 1 (Downbeat) | NOTE:♬ 16th (+1ms@116BPM) | CAT:KICK-GHOST | ART:Voiced-Bilabial+Schwa | ATK:2ms | PK:-16.0dB | F0:unvoiced | F1:596/F2:1516/F3:2714Hz | IPA:bə]` **♬ buh**
- `[#093 | 20.72–20.96s (240ms, IOI:240ms) | BAR:09 1-trip-let (2nd) | NOTE:♬· dotted-16th (+28ms@131BPM) | CAT:LIQUID-CHOP | ART:Alveolar-Lateral+Labial-Stop | ATK:2ms | PK:-26.8dB | F0:unvoiced | F1:707/F2:1839/F3:1979Hz | IPA:ˈlɪp̚]` **♬· lip**
- `[#094 | 20.96–21.13s (170ms, IOI:170ms) | BAR:09 1-a+ (32nd pickup) | NOTE:♬ 16th (+19ms@131BPM) | CAT:KICK-GHOST | ART:Glottal-Schwa-Rebound | ATK:2ms | PK:-25.9dB | F0:unvoiced | F1:781/F2:1992/F3:2211Hz | IPA:ə]` **♬ uh**
- `[#095 | 21.13–21.38s (250ms, IOI:250ms) | BAR:09 2-e | NOTE:♬· dotted-16th (+18ms@131BPM) | CAT:PLOSIVE-SCAT | ART:Voiced-Velar+HighFront | ATK:2ms | PK:-21.4dB | F0:127Hz | F1:332/F2:1563/F3:2948Hz | IPA:ˈɡɪ]` **♬· gih**
- `[#096 | 21.38–21.56s (180ms, IOI:180ms) | BAR:09 2-a+ (32nd pickup) | NOTE:♬ 16th (-19ms@131BPM) | CAT:KICK-GHOST | ART:Voiced-Bilabial+Schwa | ATK:2ms | PK:-13.1dB | F0:250Hz | F1:499/F2:1838/F3:2278Hz | IPA:bə]` **♬ buh**
- `[#097 | 21.56–21.88s (320ms, IOI:320ms) | BAR:09 3-e | NOTE:♪³ 8th-trip (-10ms@131BPM) | CAT:LIQUID-CHOP | ART:Alveolar-Lateral+MidFront+Labial | ATK:2ms | PK:-17.6dB | F0:114Hz | F1:344/F2:1732/F3:2667Hz | IPA:ˈlɛp̚]` **♪³ lep**
- `[#098 | 21.88–22.07s (190ms, IOI:190ms) | BAR:09 4-a+ (32nd pickup) | NOTE:♬ 16th (+23ms@131BPM) | CAT:KICK-GHOST | ART:Open-Transition-Schwa | ATK:2ms | PK:-17.6dB | F0:142Hz | F1:578/F2:1957/F3:2766Hz | IPA:ə]` **♬ uh**
- `[#099 | 22.07–22.75s (680ms, IOI:680ms) | BAR:09 4-trip-let (2nd) | NOTE:♩ quarter (+3ms@131BPM) | CAT:BRASS-WAH | ART:Alveolar-Plosive+Open-Back-Hold | ATK:2ms | PK:-11.2dB | F0:157Hz | F1:538/F2:1982/F3:2862Hz | IPA:ˈdɑː]` **♩ DAH!**
- `[#100 | 22.75–22.92s (170ms, IOI:170ms) | BAR:09 1-a+ (32nd pickup) | NOTE:[♪ rest] 16th-rest (-23ms@131BPM) | CAT:NONVERBAL-FX | ART:Labial-Pre-Beatbox-Breath | ATK:2ms | PK:-20.2dB | F0:unvoiced | F1:1368/F2:1446/F3:2865Hz | IPA:ʍ̥↓]` **[♪ rest] [lip-inhale]**

---

### Zoom 09 (0:22.92 – 0:25.55) — Phrase 4 Bar 1: Air Riser ('FWOO'), Bass Filter ('BWAH'), 808 Kicks & 'ship it DOWN!'

![Zoom 09 (0:22.92 – 0:25.55) — Phrase 4 Bar 1: Air Riser ('FWOO'), Bass Filter ('BWAH'), 808 Kicks & 'ship it DOWN!'](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_09.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`22.92s – 25.55s`)

- `[#101 | 22.92–23.25s (330ms, IOI:330ms) | BAR:09 2-e | NOTE:♪ 8th (-25ms@131BPM) | CAT:AIR-RISER | ART:Labiodental-Bilabial-Blow+HighBack | ATK:2ms | PK:-10.7dB | F0:228Hz | F1:242/F2:794/F3:2492Hz | IPA:ˈfwuː]` **♪ FWOO**
- `[#102 | 23.25–23.72s (470ms, IOI:470ms) | BAR:10 1-& | NOTE:♪³ 8th-trip (-15ms@87BPM) | CAT:BRASS-WAH | ART:Labialized-Bilabial+Wide-Jaw-Open | ATK:2ms | PK:-11.4dB | F0:91Hz | F1:380/F2:1100/F3:2800Hz | IPA:ˈbwɑː]` **♪³ BWAH**
- `[#103 | 23.72–23.93s (210ms, IOI:210ms) | BAR:10 2-e | NOTE:♬ 16th (-62ms@87BPM) | CAT:KICK-808 | ART:Voiced-Bilabial+Rounded-Close-Back | ATK:2ms | PK:-22.3dB | F0:unvoiced | F1:1434/F2:2364/F3:3153Hz | IPA:ˈbuː]` **♬ boo**
- `[#104 | 23.93–24.18s (250ms, IOI:250ms) | BAR:10 2-& | NOTE:♬ 16th (-24ms@87BPM) | CAT:KICK-GHOST | ART:Soft-Bilabial+Schwa | ATK:2ms | PK:-21.5dB | F0:unvoiced | F1:496/F2:1355/F3:2268Hz | IPA:bə]` **♬ buh**
- `[#105 | 24.18–24.47s (290ms, IOI:290ms) | BAR:10 2-a+ (32nd pickup) | NOTE:♬ 16th (-33ms@87BPM) | CAT:KICK-808 | ART:Voiced-Bilabial+Rounded-Close-Back | ATK:2ms | PK:-20.2dB | F0:unvoiced | F1:723/F2:1083/F3:2817Hz | IPA:ˈbuː]` **♬ boo**
- `[#106 | 24.47–24.75s (280ms, IOI:280ms) | BAR:10 3-e | NOTE:♬ 16th (-2ms@87BPM) | CAT:SNARE-SH | ART:Postalveolar-Sibilant+Labial-Stop | ATK:2ms | PK:-13.0dB | F0:unvoiced | F1:1774/F2:2266/F3:3362Hz | IPA:ˈʃɪp̚]` **♬ ship**
- `[#107 | 24.75–24.94s (190ms, IOI:190ms) | BAR:10 3-trip-let (3rd) | NOTE:♪³ 16th-trip (-9ms@87BPM) | CAT:HAT-TICK | ART:HighFront+Unreleased-Alveolar-Stop | ATK:2ms | PK:-19.1dB | F0:142Hz | F1:427/F2:1623/F3:2525Hz | IPA:ɪt̚]` **♪³ it**
- `[#108 | 24.94–25.55s (610ms, IOI:610ms) | BAR:10 4-a+ (32nd pickup) | NOTE:♪ 8th (+37ms@87BPM) | CAT:HOOK-VOX | ART:Alveolar-Stop+Wide-Diphthong-Nasal | ATK:2ms | PK:-11.0dB | F0:489Hz | F1:670/F2:1857/F3:2340Hz | IPA:ˈdaʊn]` **♪ DOWN!**

---

### Zoom 10 (0:25.55 – 0:28.45) — Phrase 4 Bar 2: Shibilant Snare Splash ('BOOSH'), 808 Sub-Kicks & 'take it DOWN!'

![Zoom 10 (0:25.55 – 0:28.45) — Phrase 4 Bar 2: Shibilant Snare Splash ('BOOSH'), 808 Sub-Kicks & 'take it DOWN!'](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_10.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`25.55s – 28.45s`)

- `[#109 | 25.55–25.68s (130ms, IOI:130ms) | BAR:10 4-a+ (32nd pickup) | NOTE:[♪ rest] 16th-rest (-42ms@87BPM) | CAT:NONVERBAL-FX | ART:Bilabial-Compression-Build | ATK:2ms | PK:-53.3dB | F0:unvoiced | F1:864/F2:1480/F3:2673Hz | IPA:p˺]` **[♪ rest] [mouth-set]**
- `[#110 | 25.68–26.16s (480ms, IOI:480ms) | BAR:10 Beat 1 (Downbeat) | NOTE:♪³ 8th-trip (+1ms@87BPM) | CAT:SNARE-SH | ART:Bilabial-Kick+Postalveolar-Snare-Wash | ATK:2ms | PK:-15.5dB | F0:96Hz | F1:1257/F2:2220/F3:3315Hz | IPA:ˈbuʃ]` **♪³ BOOSH**
- `[#111 | 26.16–26.51s (350ms, IOI:350ms) | BAR:11 1-trip-let (3rd) | NOTE:♬· dotted-16th (-2ms@83BPM) | CAT:KICK-808 | ART:Bilabial-Stop+Rounded-Back+Nasal-Hold | ATK:2ms | PK:-18.1dB | F0:89Hz | F1:850/F2:1441/F3:2551Hz | IPA:ˈbuːm]` **♬· boom**
- `[#112 | 26.51–26.70s (190ms, IOI:190ms) | BAR:11 2-e | NOTE:♪³ 16th-trip (-74ms@83BPM) | CAT:KICK-GHOST | ART:Bilabial-Flap-Pickup | ATK:2ms | PK:-18.4dB | F0:96Hz | F1:646/F2:1330/F3:2844Hz | IPA:bə]` **♪³ buh**
- `[#113 | 26.70–27.20s (500ms, IOI:500ms) | BAR:11 2-trip-let (2nd) | NOTE:♪³ 8th-trip (+56ms@83BPM) | CAT:KICK-808 | ART:Bilabial-Stop+Rounded-Back+Nasal-Hold | ATK:2ms | PK:-18.7dB | F0:91Hz | F1:1088/F2:1872/F3:2928Hz | IPA:ˈbuːm]` **♪³ boom**
- `[#114 | 27.20–27.50s (300ms, IOI:300ms) | BAR:11 Beat 3 | NOTE:[♪ rest] 16th-rest (+74ms@83BPM) | CAT:NONVERBAL-FX | ART:Glottal-Closure-Before-Hook | ATK:2ms | PK:-39.1dB | F0:unvoiced | F1:1196/F2:1942/F3:2259Hz | IPA:ʔ]` **[♪ rest] [glottal-reset]**
- `[#115 | 27.50–27.68s (180ms, IOI:180ms) | BAR:11 3-& | NOTE:♪³ 16th-trip (+13ms@83BPM) | CAT:HAT-TICK | ART:Asp-Alveolar-Stop+Velar-Check | ATK:2ms | PK:-19.6dB | F0:unvoiced | F1:446/F2:1751/F3:2542Hz | IPA:ˈtʰɪk̚]` **♪³ take**
- `[#116 | 27.68–27.84s (160ms, IOI:160ms) | BAR:11 3-a | NOTE:♪³ 16th-trip (+12ms@83BPM) | CAT:HAT-TICK | ART:HighFront+Alveolar-Check | ATK:2ms | PK:-15.5dB | F0:131Hz | F1:388/F2:1751/F3:2831Hz | IPA:ɪt̚]` **♪³ it**
- `[#117 | 27.84–28.45s (610ms, IOI:610ms) | BAR:11 Beat 1 | NOTE:♪ 8th (-9ms@83BPM) | CAT:HOOK-VOX | ART:Alveolar-Stop+Open-Diphthong-Nasal | ATK:2ms | PK:-16.9dB | F0:unvoiced | F1:1294/F2:2209/F3:3137Hz | IPA:ˈdaʊn]` **♪ DOWN!**

---

### Zoom 11 (0:28.45 – 0:31.38) — Phrase 4 Bar 3: 808 Kick + Affricate Hi-Hat ('Boom-ts-boom') & Uvular Growl ('rrr-right around!')

![Zoom 11 (0:28.45 – 0:31.38) — Phrase 4 Bar 3: 808 Kick + Affricate Hi-Hat ('Boom-ts-boom') & Uvular Growl ('rrr-right around!')](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_11.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`28.45s – 31.38s`)

- `[#118 | 28.45–28.57s (120ms, IOI:120ms) | BAR:11 4-a+ (32nd pickup) | NOTE:[♪ rest] 16th-rest (-31ms@83BPM) | CAT:NONVERBAL-FX | ART:Bilabial-Pre-Closure | ATK:2ms | PK:-28.3dB | F0:unvoiced | F1:366/F2:986/F3:2630Hz | IPA:b˺]` **[♪ rest] [lip-seal]**
- `[#119 | 28.57–28.92s (350ms, IOI:350ms) | BAR:11 Beat 2 | NOTE:♬· dotted-16th (-2ms@83BPM) | CAT:KICK-808 | ART:Bilabial-Stop+Low-F0(93Hz)-Sub-Resonance | ATK:2ms | PK:-22.6dB | F0:88Hz | F1:1139/F2:2414/F3:3775Hz | IPA:ˈbuːm]` **♬· Boom**
- `[#120 | 28.92–29.07s (150ms, IOI:150ms) | BAR:12 1-& | NOTE:♪³ 16th-trip (-1ms@85BPM) | CAT:HAT-TICK | ART:Asp-Alveolar-Affricate-Burst | ATK:2ms | PK:-22.6dB | F0:unvoiced | F1:1312/F2:2242/F3:2732Hz | IPA:t͡sʰ]` **♪³ ts**
- `[#121 | 29.07–29.42s (350ms, IOI:350ms) | BAR:12 1-a | NOTE:♬· dotted-16th (-27ms@85BPM) | CAT:KICK-808 | ART:Bilabial-Stop+Rounded-Nasal-Sub | ATK:2ms | PK:-20.4dB | F0:91Hz | F1:217/F2:592/F3:2622Hz | IPA:ˈbuːm]` **♬· boom**
- `[#122 | 29.42–29.60s (180ms, IOI:180ms) | BAR:12 2-e | NOTE:♪³ 16th-trip (-28ms@85BPM) | CAT:KICK-GHOST | ART:Bilabial-16th-Pickup | ATK:2ms | PK:-19.0dB | F0:unvoiced | F1:844/F2:1499/F3:2664Hz | IPA:bə]` **♪³ buh**
- `[#123 | 29.60–30.15s (550ms, IOI:550ms) | BAR:12 2-& | NOTE:♪ 8th (-24ms@85BPM) | CAT:KICK-808 | ART:Bilabial-Stop+Rounded-Nasal-Sub | ATK:2ms | PK:-20.0dB | F0:89Hz | F1:843/F2:1447/F3:2400Hz | IPA:ˈbuːm]` **♪ boom**
- `[#124 | 30.15–30.28s (130ms, IOI:130ms) | BAR:12 3-e | NOTE:♪³ 16th-trip (-1ms@85BPM) | CAT:DJ-SCRATCH | ART:Voiced-Uvular-Trill-Growl | ATK:2ms | PK:-22.0dB | F0:unvoiced | F1:502/F2:1139/F3:2293Hz | IPA:ʀː]` **♪³ rrr**
- `[#125 | 30.28–30.50s (220ms, IOI:220ms) | BAR:12 3-& | NOTE:♬ 16th (-46ms@85BPM) | CAT:HOOK-VOX | ART:Post-Alveolar-Rhotic+Diphthong+Stop | ATK:2ms | PK:-23.0dB | F0:unvoiced | F1:923/F2:1863/F3:2600Hz | IPA:ˈɹaɪt̚]` **♬ right**
- `[#126 | 30.50–30.65s (150ms, IOI:150ms) | BAR:12 3-a | NOTE:♪³ 16th-trip (-2ms@85BPM) | CAT:HOOK-VOX | ART:Central-Vowel-Link | ATK:2ms | PK:-24.5dB | F0:unvoiced | F1:674/F2:1320/F3:2271Hz | IPA:ə]` **♪³ uh**
- `[#127 | 30.65–31.12s (470ms, IOI:470ms) | BAR:12 Beat 1 | NOTE:♪³ 8th-trip (-28ms@85BPM) | CAT:HOOK-VOX | ART:Rhotic+Wide-Diphthong+Nasal-Alv-Coda | ATK:2ms | PK:-18.9dB | F0:unvoiced | F1:1220/F2:1809/F3:2581Hz | IPA:ˈɹaʊnd]` **♪³ ROUND!**
- `[#128 | 31.12–31.38s (260ms, IOI:260ms) | BAR:12 4-trip-let (3rd) | NOTE:[♪ rest] 16th-rest (-26ms@85BPM) | CAT:NONVERBAL-FX | ART:Quiet-Nasal-Inhale+Lip-Seal | ATK:2ms | PK:-25.4dB | F0:unvoiced | F1:280/F2:1197/F3:2489Hz | IPA:h̥͡p˺]` **[♪ rest] [breath-lip]**

---

### Zoom 12 (0:31.38 – 0:34.20) — Phrase 4 Bar 4: 808 Groove + Two-Stage Uvular DJ Record Scratch ('Hhh-RA-hh-RA!')

![Zoom 12 (0:31.38 – 0:34.20) — Phrase 4 Bar 4: 808 Groove + Two-Stage Uvular DJ Record Scratch ('Hhh-RA-hh-RA!')](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_12.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`31.38s – 34.20s`)

- `[#129 | 31.38–31.84s (460ms, IOI:460ms) | BAR:12 Beat 2 | NOTE:♪³ 8th-trip (-0ms@85BPM) | CAT:KICK-808 | ART:Bilabial-Stop+91Hz-Sub-Fundamental | ATK:2ms | PK:-16.1dB | F0:92Hz | F1:321/F2:1365/F3:2685Hz | IPA:ˈbuːm]` **♪³ Boom**
- `[#130 | 31.84–32.01s (170ms, IOI:170ms) | BAR:13 1-trip-let (3rd) | NOTE:♪³ 16th-trip (-10ms@85BPM) | CAT:HAT-TICK | ART:Unvoiced-Alveolar-Affricate-Hat | ATK:2ms | PK:-21.7dB | F0:unvoiced | F1:1326/F2:1916/F3:3030Hz | IPA:t͡sʰ]` **♪³ ts**
- `[#131 | 32.01–32.36s (350ms, IOI:350ms) | BAR:13 1-a+ (32nd pickup) | NOTE:♬· dotted-16th (+13ms@85BPM) | CAT:KICK-808 | ART:Bilabial-Stop+Rounded-Nasal-Sub | ATK:2ms | PK:-25.4dB | F0:91Hz | F1:733/F2:1569/F3:2712Hz | IPA:ˈbuːm]` **♬· boom**
- `[#132 | 32.36–32.54s (180ms, IOI:180ms) | BAR:13 2-trip-let (2nd) | NOTE:♪³ 16th-trip (+40ms@85BPM) | CAT:KICK-GHOST | ART:Bilabial-16th-Pickup | ATK:2ms | PK:-21.1dB | F0:unvoiced | F1:1230/F2:1620/F3:3009Hz | IPA:bə]` **♪³ buh**
- `[#133 | 32.54–33.08s (540ms, IOI:540ms) | BAR:13 2-trip-let (3rd) | NOTE:♪ 8th (-15ms@85BPM) | CAT:KICK-808 | ART:Bilabial-Stop+Rounded-Nasal-Sub | ATK:2ms | PK:-23.9dB | F0:89Hz | F1:1266/F2:1719/F3:2939Hz | IPA:ˈbuːm]` **♪ boom**
- `[#134 | 33.08–33.26s (180ms, IOI:180ms) | BAR:13 3-trip-let (2nd) | NOTE:♪³ 16th-trip (+55ms@85BPM) | CAT:DJ-SCRATCH | ART:Voiceless-Uvular-Fricative-Scrape | ATK:2ms | PK:-26.8dB | F0:unvoiced | F1:1414/F2:2134/F3:2587Hz | IPA:χː]` **♪³ Hhh**
- `[#135 | 33.26–33.52s (260ms, IOI:260ms) | BAR:13 3-trip-let (3rd) | NOTE:♬ 16th (-0ms@85BPM) | CAT:DJ-SCRATCH | ART:Uvular-Trill+Wide-Open-Pharynx(F1:1037Hz) | ATK:2ms | PK:-17.3dB | F0:unvoiced | F1:1204/F2:2056/F3:2572Hz | IPA:ˈʀæ]` **♬ RA**
- `[#136 | 33.52–33.63s (110ms, IOI:110ms) | BAR:13 Beat 4 | NOTE:♬ 32nd (+25ms@85BPM) | CAT:DJ-SCRATCH | ART:Voiceless-Uvular-Reverse-Cut | ATK:2ms | PK:-33.2dB | F0:unvoiced | F1:1465/F2:1658/F3:2628Hz | IPA:χ]` **♬ hh**
- `[#137 | 33.63–34.10s (470ms, IOI:570ms) | BAR:13 4-e | NOTE:♪ 8th (-41ms@85BPM) | CAT:DJ-SCRATCH | ART:Uvular-Trill+Open-Front-Release | ATK:2ms | PK:-13.6dB | F0:unvoiced | F1:1212/F2:1497/F3:2265Hz | IPA:ˈʀæː]` **♪ RA!**

---

### Zoom 13 (0:34.20 – 0:36.48) — Interlude: Room Decay, Velar Click & Pharyngeal-Uvular Throat Scrape ('[hʀ̥ː]')

![Zoom 13 (0:34.20 – 0:36.48) — Interlude: Room Decay, Velar Click & Pharyngeal-Uvular Throat Scrape ('[hʀ̥ː]')](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_13.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`34.20s – 36.48s`)

- `[#138 | 34.20–34.84s (640ms, IOI:640ms) | BAR:13 Beat 2 | NOTE:[♩ rest] quarter-rest (-0ms@85BPM) | CAT:NONVERBAL-FX | ART:Ambient-Room-Decay | ATK:2ms | PK:-55.4dB | F0:unvoiced | F1:654/F2:1651/F3:2760Hz | IPA:∅]` **[♩ rest] [room-silence]**
- `[#139 | 34.84–35.08s (240ms, IOI:240ms) | BAR:14 Rubato / Free | NOTE:[♪ rest] 16th-rest (free@0BPM) | CAT:NONVERBAL-FX | ART:Unvoiced-Velar-Affricate-Clear | ATK:2ms | PK:-29.2dB | F0:unvoiced | F1:680/F2:1038/F3:2288Hz | IPA:k͡x̥]` **[♪ rest] [velar-click]**
- `[#140 | 35.08–35.45s (370ms, IOI:370ms) | BAR:14 Rubato / Free | NOTE:♪³ 8th-trip (free@0BPM) | CAT:DJ-SCRATCH | ART:Unvoiced-Pharyngeal-Uvular-Frication | ATK:2ms | PK:-14.0dB | F0:unvoiced | F1:570/F2:783/F3:2120Hz | IPA:hʀ̥ː]` **♪³ [throat-scrape]**
- `[#141 | 35.45–36.48s (1030ms, IOI:1030ms) | BAR:14 Rubato / Free | NOTE:[♩ rest] quarter-rest (free@0BPM) | CAT:NONVERBAL-FX | ART:Silent-Dramatic-Hold | ATK:2ms | PK:-31.6dB | F0:unvoiced | F1:629/F2:961/F3:2473Hz | IPA:∅]` **[♩ rest] [pre-outro-gap]**

---

### Zoom 14 (0:36.48 – 0:37.82) — Phrase 5 Outro Cadence ('Duh-rip-it-NOW!') & Post-Cadence Release

![Zoom 14 (0:36.48 – 0:37.82) — Phrase 5 Outro Cadence ('Duh-rip-it-NOW!') & Post-Cadence Release](/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df/zoom_14.png)

#### Bracketed Rhythm & Acoustic Metadata Stream (`36.48s – 37.82s`)

- `[#142 | 36.48–36.70s (220ms, IOI:220ms) | BAR:14 Rubato / Free | NOTE:♬ 16th (free@0BPM) | CAT:PLOSIVE-SCAT | ART:Voiced-Alveolar-Stop+Schwa | ATK:2ms | PK:-24.2dB | F0:unvoiced | F1:464/F2:1432/F3:2285Hz | IPA:də]` **♬ Duh**
- `[#143 | 36.70–36.83s (130ms, IOI:130ms) | BAR:15 1-trip-let (2nd) | NOTE:♪³ 16th-trip (+12ms@96BPM) | CAT:HAT-TICK | ART:Rhotic+HighFront+Clipped-Bilabial-Stop | ATK:2ms | PK:-14.2dB | F0:unvoiced | F1:440/F2:1417/F3:1759Hz | IPA:ˈɹɪp̚]` **♪³ rip**
- `[#144 | 36.83–37.00s (170ms, IOI:170ms) | BAR:15 1-& | NOTE:♪³ 16th-trip (+38ms@96BPM) | CAT:HAT-TICK | ART:HighFront+Clipped-Alveolar-Stop | ATK:2ms | PK:-13.2dB | F0:unvoiced | F1:488/F2:1574/F3:1888Hz | IPA:ˈɪt̚]` **♪³ it**
- `[#145 | 37.00–37.38s (380ms, IOI:380ms) | BAR:15 1-a+ (32nd pickup) | NOTE:♪³ 8th-trip (-27ms@96BPM) | CAT:HOOK-VOX | ART:Alveolar-Nasal+Open-to-Rounded-Diphthong | ATK:2ms | PK:-19.7dB | F0:unvoiced | F1:635/F2:1677/F3:2000Hz | IPA:ˈnaʊ]` **♪³ NOW!**
- `[#146 | 37.38–37.60s (220ms, IOI:220ms) | BAR:15 2-& | NOTE:[♪ rest] 16th-rest (-38ms@96BPM) | CAT:NONVERBAL-FX | ART:Post-Cadence-Bilabial-Unseal | ATK:2ms | PK:-53.7dB | F0:unvoiced | F1:1250/F2:2143/F3:2714Hz | IPA:p˺]` **[♪ rest] [lip-release]**
- `[#147 | 37.60–37.82s (220ms, IOI:220ms) | BAR:15 2-a | NOTE:[♪ rest] 16th-rest (+26ms@96BPM) | CAT:NONVERBAL-FX | ART:Handling-Stop-Click | ATK:2ms | PK:-34.5dB | F0:65Hz | F1:629/F2:1083/F3:2668Hz | IPA:t˺]` **[♪ rest] [mic-tap]**

---
