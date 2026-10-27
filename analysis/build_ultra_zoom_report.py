import base64
import json
import shutil
from pathlib import Path
import numpy as np
import librosa
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
from scipy.signal import lfilter

WORKSPACE = Path("/Volumes/2TB/moviesfolder/MOVIES_FOLDER/studpid Stuff")
MP3_PATH = WORKSPACE / "IMG_3268.mp3"
OUT_DIR = WORKSPACE / "analysis"
ARTIFACT_DIR = Path("/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df")
OUT_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

CAT_COLORS = {
    "KICK-808": "#ef4444",       # Red - Bilabial sub-bass kick
    "KICK-GHOST": "#f87171",     # Light Red - Ghost/pickup bilabial kick
    "SNARE-SH": "#f97316",       # Orange - Shibilant/affricate snare
    "HAT-TICK": "#eab308",       # Gold - Alveolar/velar hi-hat / rim click
    "GLOTTAL-POP": "#facc15",    # Bright Yellow - Glottal stop / cork pop
    "BRASS-WAH": "#a855f7",      # Purple - Open-to-rounded diphthong horn stab
    "PLOSIVE-SCAT": "#10b981",   # Emerald - Voiced/voiceless plosive scat syllable
    "FRIC-BRUSH": "#14b8a6",     # Teal - Labiodental/dental fricative brush
    "LIQUID-CHOP": "#2dd4bf",    # Aqua - Lateral/rhotic double-tongue chop
    "NASAL-GATE": "#ec4899",     # Pink - Nasal hum / nasal-clamped damper
    "FALSETTO-SQ": "#f472b6",    # Hot Pink - High-larynx pinched squeak
    "AIR-RISER": "#06b6d4",      # Cyan - Labiodental wind riser
    "DJ-SCRATCH": "#0ea5e9",     # Sky Blue - Uvular fricative-trill record scratch
    "HOOK-VOX": "#3b82f6",       # Royal Blue - Semi-lexical rhythmic hook syllable
    "NONVERBAL-FX": "#64748b",   # Slate - Breath intake, exhale, throat scrape, tail tap
}

# Every single auditory event (138 total micro-events across 0:00.00 - 0:37.82)
# Format: (start_s, end_s, english_phonetic, narrow_ipa, category_code, articulatory_desc, purpose_desc)
MICRO_EVENTS = [
    # --- ZOOM 1 (0:00.00 - 0:02.38): Phrase 1A ---
    (0.00, 0.18, "[lip-prep]", "p͡f˺", "NONVERBAL-FX", "Bilabial-Pre-Breath", "Mic proximity lip seal release"),
    (0.18, 0.26, "thuh", "ðə", "FRIC-BRUSH", "Voiced-Dental-Fric+Schwa", "Brushed pickup hi-hat"),
    (0.26, 0.38, "bitch", "ˈbɪtʃ", "SNARE-SH", "Bilabial-Stop+Postalv-Affric", "Snare/clap accent hit"),
    (0.38, 0.54, "camp", "ˈkʰæmp̚", "NASAL-GATE", "Asp-Velar+LowFront+Bilabial-Clamp", "Nasal-gated tom hit"),
    (0.54, 0.71, "brah", "ˈbɹɑː", "BRASS-WAH", "Bilabial-Rhotic+OpenBack", "Low-mid horn stab"),
    (0.71, 0.86, "thuh", "ðə", "FRIC-BRUSH", "Voiced-Dental-Fric+Schwa", "16th-note brush link"),
    (0.86, 1.07, "rup", "ˈɹʌp̚", "PLOSIVE-SCAT", "Rhotic+MidCentral+Unreleased-Labial", "Clipped labial chop"),
    (1.07, 1.16, "in", "ɪn", "NASAL-GATE", "HighFront-Lax+Alveolar-Nasal", "Nasal ghost note"),
    (1.16, 1.25, "thuh", "ðə", "FRIC-BRUSH", "Voiced-Dental-Fric+Schwa", "Dental pickup"),
    (1.25, 1.51, "pant", "ˈpʰænt̚", "HAT-TICK", "Asp-Bilabial+Nasal-Alveolar-Stop", "Snappy rim+gate"),
    (1.51, 1.73, "thence", "ˈðɛns", "SNARE-SH", "Dental-Fric+Alveolar-Sibilant-Tail", "Sibilant snare wire tail"),
    (1.73, 1.89, "bup", "ˈbʌp̚", "KICK-GHOST", "Voiced-Bilabial+Labial-Check", "Muted punch kick"),
    (1.89, 1.97, "uh", "ə", "KICK-GHOST", "Mid-Central-Schwa-Pulse", "16th ghost bounce"),
    (1.97, 2.06, "guh", "ɡə", "PLOSIVE-SCAT", "Voiced-Velar-Stop+Schwa", "Velar rebound tap"),
    (2.06, 2.21, "kah", "ˈkʰɑː", "HAT-TICK", "Asp-Velar-Stop+OpenBack", "Open rim accent"),
    (2.21, 2.38, "pump", "pʌmp̚", "NASAL-GATE", "Bilabial-Stop+Nasal-Bilabial-Clamp", "Damped chest thump"),

    # --- ZOOM 2 (0:02.38 - 0:04.75): Phrase 1B ---
    (2.38, 2.52, "thuh", "ðə", "FRIC-BRUSH", "Voiced-Dental-Fric+Schwa", "Soft dental lead-in"),
    (2.52, 2.73, "frup", "ˈfɹʌp̚", "FRIC-BRUSH", "Labiodental-Fric+Rhotic+Labial-Stop", "Flammed brush-to-pop"),
    (2.73, 2.88, "in", "ɪn", "NASAL-GATE", "HighFront-Lax+Alveolar-Nasal", "Nasal upbeat"),
    (2.88, 3.04, "thuh", "ðə", "FRIC-BRUSH", "Voiced-Dental-Fric+Schwa", "Dental connector"),
    (3.04, 3.22, "fup", "ˈfʌp̚", "FRIC-BRUSH", "Labiodental-Fric+MidCentral+Labial-Stop", "Whipped lip pop"),
    (3.22, 3.36, "it", "ɪt̚", "HAT-TICK", "HighFront-Lax+Unreleased-Alveolar", "Tight closed hi-hat"),
    (3.36, 3.70, "at", "ˈæt̚", "HAT-TICK", "LowFront-Open+Unreleased-Alveolar", "Open-jaw alveolar check"),
    (3.70, 4.35, "all!", "ˈɔːl", "BRASS-WAH", "OpenMid-Back-Rounded+Dark-Lateral", "Sustained resonant pad"),
    (4.35, 4.75, "[drop-pause]", "ʔ‿h̥", "NONVERBAL-FX", "Glottal-Release+Silent-Breath-Gap", "0.3s structural stop-down"),

    # --- ZOOM 3 (0:04.75 - 0:08.15): Phrase 2A ---
    (4.75, 5.48, "Mmmm!", "ˈmːˀp", "NASAL-GATE", "Prolonged-Bilabial-Nasal+Glottal-Lip-Pop", "Sub-bass hum pickup"),
    (5.48, 6.05, "[breath-gap]", "h̥ː", "NONVERBAL-FX", "Unvoiced-Nasal-Exhale-Gap", "0.6s pocket reset"),
    (6.05, 6.20, "thuh", "ðə", "FRIC-BRUSH", "Voiced-Dental-Fric+Schwa", "Pickup brush"),
    (6.20, 6.40, "cup", "ˈkʰʌp̚", "GLOTTAL-POP", "Asp-Velar-Stop+Unreleased-Labial", "Hollow velar-labial pop"),
    (6.40, 6.55, "uh", "ə", "KICK-GHOST", "Mid-Central-Schwa", "Ghost rebound"),
    (6.55, 6.69, "thuh", "ðə", "FRIC-BRUSH", "Voiced-Dental-Fric+Schwa", "Dental grace note"),
    (6.69, 7.00, "pink", "ˈpʰɪŋk̚", "GLOTTAL-POP", "Asp-Bilabial+Velar-Nasal-Stop", "earshot FOLEY cork pop (-12.7dB)"),
    (7.00, 7.45, "cane", "ˈkʰeɪn", "PLOSIVE-SCAT", "Asp-Velar+Front-Closing-Diphthong", "High-F2 pitched synth hit"),
    (7.45, 7.60, "tuh", "tʰə", "HAT-TICK", "Asp-Alveolar-Stop+Schwa", "Hi-hat 16th pickup"),
    (7.60, 7.80, "rip", "ˈɹɪp̚", "PLOSIVE-SCAT", "Rhotic+HighFront+Unreleased-Labial", "Snappy labial cut"),
    (7.80, 7.98, "in", "ɪn", "NASAL-GATE", "HighFront+Alveolar-Nasal", "Nasal link"),
    (7.98, 8.15, "thuh", "ðə", "FRIC-BRUSH", "Voiced-Dental-Fric+Schwa", "Dental pre-accent"),

    # --- ZOOM 4 (0:08.15 - 0:12.50): Phrase 2B + Breath Interlude ---
    (8.15, 8.46, "ki", "ˈkʰɪ", "GLOTTAL-POP", "Asp-Velar+Glottal-Cut-Vowel", "Staccato woodblock onset"),
    (8.46, 8.78, "'in", "ˈʔɪn", "GLOTTAL-POP", "Hard-Glottal-Stop+HighFront-Nasal", "Zero-VOT glottal click"),
    (8.78, 9.05, "bick", "ˈbɪk̚", "KICK-GHOST", "Voiced-Bilabial+Velar-Stop-Check", "Punchy kick-to-rim"),
    (9.05, 9.28, "in", "ɪn", "NASAL-GATE", "HighFront+Alveolar-Nasal", "Nasal offbeat"),
    (9.28, 9.44, "thuh", "ðə", "FRIC-BRUSH", "Voiced-Dental-Fric+Schwa", "Dental pre-stab"),
    (9.44, 9.73, "bow", "ˈbaʊ", "BRASS-WAH", "Voiced-Bilabial+Open-to-Rounded-Diphthong", "Mini brass wah stab"),
    (9.73, 10.01, "fen", "ˈfɛn", "FRIC-BRUSH", "Labiodental-Fric+MidFront-Nasal", "Airy snare brush"),
    (10.01, 10.18, "tuh", "tʰə", "HAT-TICK", "Asp-Alveolar-Stop+Schwa", "Crisp hi-hat tick"),
    (10.18, 10.51, "sick", "ˈsɪk̚", "SNARE-SH", "Alveolar-Sibilant+Velar-Check", "Bright sibilant rimshot"),
    (10.51, 10.67, "in", "ɪn", "NASAL-GATE", "HighFront+Alveolar-Nasal", "16th link 1"),
    (10.67, 10.80, "thuh", "ðə", "FRIC-BRUSH", "Voiced-Dental-Fric+Schwa", "16th link 2"),
    (10.80, 10.95, "kuh", "kʰə", "HAT-TICK", "Asp-Velar-Stop+Schwa", "16th velar tick 3"),
    (10.95, 11.14, "lip", "ˈlɪp̚", "LIQUID-CHOP", "Alveolar-Lateral+Labial-Stop", "Tongue-tip bounce pop"),
    (11.14, 11.30, "in", "ɪn", "NASAL-GATE", "HighFront+Alveolar-Nasal", "Pre-cadence link"),
    (11.30, 11.72, "NOW!", "ˈnaʊ", "BRASS-WAH", "Alveolar-Nasal+Wide-Diphthong-Sweep", "Phrase 2 cadence hit"),
    (11.72, 12.50, "[inhale-gasp]", "hː↓", "NONVERBAL-FX", "Deep-Ingressive-Pulmonic-Breath", "0.8s air refill (AST: Gasp)"),

    # --- ZOOM 5 (0:12.50 - 0:15.60): Phrase 3A (Horn Stabs) ---
    (12.50, 12.72, "You", "ju", "HOOK-VOX", "Palatal-Approx+HighBack-Rounded", "Call hook syllable 1"),
    (12.72, 12.92, "know", "ˈnoʊ", "HOOK-VOX", "Alveolar-Nasal+MidBack-Diphthong", "Call hook syllable 2"),
    (12.92, 13.09, "what", "ˈwʌt̚", "HOOK-VOX", "Labial-Velar+MidCentral+Alv-Stop", "Call hook setup stop"),
    (13.09, 13.55, "BOW", "ˈbaʊ", "BRASS-WAH", "Heavy-Bilabial+F1:748->350Hz-Sweep", "Max-peak (-7.2dB) brass wah 1"),
    (13.55, 13.72, "buh", "bə", "KICK-GHOST", "Soft-Bilabial-Stop+Schwa", "16th ghost kick rebound"),
    (13.72, 14.03, "BOW", "ˈbaʊ", "BRASS-WAH", "Heavy-Bilabial+Open-to-Rounded-Glide", "Brass wah stab 2 (-10.9dB)"),
    (14.03, 14.34, "BOW", "ˈbaʊ", "BRASS-WAH", "Heavy-Bilabial+Open-to-Rounded-Glide", "Brass wah stab 3 (-17.0dB)"),
    (14.34, 14.88, "BOW!", "ˈbaʊː", "BRASS-WAH", "Heavy-Bilabial+Long-Resonant-Sweep", "Brass wah stab 4 (-8.7dB)"),
    (14.88, 15.04, "You", "ju", "HOOK-VOX", "Palatal-Approx+HighBack", "Response 1 syl 1"),
    (15.04, 15.18, "know", "ˈnoʊ", "HOOK-VOX", "Alveolar-Nasal+Diphthong", "Response 1 syl 2"),
    (15.18, 15.32, "what", "wʌt̚", "HOOK-VOX", "Labial-Velar+Alv-Check", "Response 1 syl 3"),
    (15.32, 15.60, "now", "ˈnaʊ", "BRASS-WAH", "Alveolar-Nasal+Diphthong", "Response 1 cadence"),

    # --- ZOOM 6 (0:15.60 - 0:18.45): Phrase 3B (Call & Response + Falsetto) ---
    (15.60, 15.77, "[micro-breath]", "h̥", "NONVERBAL-FX", "Short-Glottal-Air-Vent", "Quick breath reset"),
    (15.77, 15.94, "You", "ju", "HOOK-VOX", "Palatal-Approx+HighBack", "Response 2 syl 1"),
    (15.94, 16.09, "know", "ˈnoʊ", "HOOK-VOX", "Alveolar-Nasal+Diphthong", "Response 2 syl 2"),
    (16.09, 16.25, "what", "wʌt̚", "HOOK-VOX", "Labial-Velar+Alv-Check", "Response 2 syl 3"),
    (16.25, 16.46, "now", "ˈnaʊ", "BRASS-WAH", "Alveolar-Nasal+Diphthong", "Response 2 cadence"),
    (16.46, 16.60, "You", "ju", "HOOK-VOX", "Palatal-Approx+HighBack", "Response 3 syl 1"),
    (16.60, 16.74, "know", "ˈnoʊ", "HOOK-VOX", "Alveolar-Nasal+Diphthong", "Response 3 syl 2"),
    (16.74, 16.90, "what", "wʌt̚", "HOOK-VOX", "Labial-Velar+Alv-Check", "Response 3 syl 3"),
    (16.90, 17.26, "then", "ˈðɛn", "NASAL-GATE", "Voiced-Dental+MidFront-Nasal", "Response 3 cadence"),
    (17.26, 17.46, "You", "ju", "HOOK-VOX", "Palatal-Approx+HighBack", "Response 4 syl 1"),
    (17.46, 17.60, "know", "ˈnoʊ", "HOOK-VOX", "Alveolar-Nasal+Diphthong", "Response 4 syl 2"),
    (17.60, 17.75, "what", "wʌt̚", "HOOK-VOX", "Labial-Velar+Alv-Check", "Response 4 syl 3"),
    (17.75, 18.12, "WHEN!↑", "ˈwɪ̃n↑", "FALSETTO-SQ", "High-Larynx-Nasalized-Falsetto-Squeak", "Pinched upper-mid synth accent"),
    (18.12, 18.27, "You", "ju", "HOOK-VOX", "Fast-Palatal-Pickup", "Chopper lead-in 1"),
    (18.27, 18.37, "know", "noʊ", "HOOK-VOX", "Fast-Nasal-Pickup", "Chopper lead-in 2"),
    (18.37, 18.47, "what", "wʌt̚", "HOOK-VOX", "Clipped-Alveolar-Setup", "Chopper launch pad"),

    # --- ZOOM 7 (0:18.45 - 0:20.54): Phrase 3C (Plosive Drum Roll + Skibidi-Bah) ---
    (18.47, 18.56, "thuh", "ðə", "FRIC-BRUSH", "Dental-Fricative-Grace-Note", "32nd-note roll onset"),
    (18.56, 18.65, "buh", "bə", "KICK-GHOST", "Bilabial-Plosive-Pop", "earshot UI chat message pop"),
    (18.65, 18.75, "chuh", "tʃə", "SNARE-SH", "Postalveolar-Affricate-Tick", "Micro snare rim"),
    (18.75, 18.84, "kuh", "kʰə", "HAT-TICK", "Velar-Plosive-Tick", "Back-tongue hi-hat"),
    (18.84, 18.94, "buh", "bə", "KICK-GHOST", "Bilabial-Pre-Hit-Bounce", "Pre-accent kick flam"),
    (18.94, 19.35, "GAH!", "ˈɡɑː", "BRASS-WAH", "Voiced-Velar+Wide-Open-Pharynx", "Open-throat tom/horn hit"),
    (19.35, 19.51, "ski", "ˈskɪ", "HAT-TICK", "Sibilant-Velar-Cluster+HighFront", "Triple-tongue chop 1"),
    (19.51, 19.65, "bi", "bɪ", "PLOSIVE-SCAT", "Bilabial-Stop+HighFront", "Triple-tongue chop 2"),
    (19.65, 19.85, "di", "dɪ", "LIQUID-CHOP", "Alveolar-Flap-Stop+HighFront", "Triple-tongue chop 3"),
    (19.85, 20.54, "BAH!", "ˈbɑː", "BRASS-WAH", "Heavy-Bilabial+Open-Back-Vowel", "Loud (-9.2dB) horn accent"),

    # --- ZOOM 8 (0:20.54 - 0:22.90): Phrase 3D (16th-Note Lateral-Plosive Chopper) ---
    (20.54, 20.72, "buh", "bə", "KICK-GHOST", "Voiced-Bilabial+Schwa", "Chopper pulse 1 (labial)"),
    (20.72, 20.96, "lip", "ˈlɪp̚", "LIQUID-CHOP", "Alveolar-Lateral+Labial-Stop", "Chopper pulse 2 (earshot: lego click)"),
    (20.96, 21.13, "uh", "ə", "KICK-GHOST", "Glottal-Schwa-Rebound", "Chopper pulse 3 (release)"),
    (21.13, 21.38, "gih", "ˈɡɪ", "PLOSIVE-SCAT", "Voiced-Velar+HighFront", "Chopper pulse 4 (velar)"),
    (21.38, 21.56, "buh", "bə", "KICK-GHOST", "Voiced-Bilabial+Schwa", "Chopper pulse 5 (labial)"),
    (21.56, 21.88, "lep", "ˈlɛp̚", "LIQUID-CHOP", "Alveolar-Lateral+MidFront+Labial", "Chopper pulse 6 (lateral)"),
    (21.88, 22.07, "uh", "ə", "KICK-GHOST", "Open-Transition-Schwa", "Chopper pulse 7 (setup)"),
    (22.07, 22.75, "DAH!", "ˈdɑː", "BRASS-WAH", "Alveolar-Plosive+Open-Back-Hold", "Phrase 3 final impact (-11.3dB)"),
    (22.75, 22.92, "[lip-inhale]", "ʍ̥↓", "NONVERBAL-FX", "Labial-Pre-Beatbox-Breath", "Transition into Beatbox Groove"),

    # --- ZOOM 9 (0:22.90 - 0:25.55): Phrase 4 Bar 1 (Riser + Sub-Kick + Ship It Down) ---
    (22.92, 23.25, "FWOO", "ˈfwuː", "AIR-RISER", "Labiodental-Bilabial-Blow+HighBack", "Reverse-cymbal air riser (-10.7dB)"),
    (23.25, 23.72, "BWAH", "ˈbwɑː", "BRASS-WAH", "Labialized-Bilabial+Wide-Jaw-Open", "Sub-bass filter open growl (-11.4dB)"),
    (23.72, 23.93, "boo", "ˈbuː", "KICK-808", "Voiced-Bilabial+Rounded-Close-Back", "808 sub-kick pulse 1"),
    (23.93, 24.18, "buh", "bə", "KICK-GHOST", "Soft-Bilabial+Schwa", "16th ghost kick pickup"),
    (24.18, 24.47, "boo", "ˈbuː", "KICK-808", "Voiced-Bilabial+Rounded-Close-Back", "808 sub-kick pulse 2"),
    (24.47, 24.75, "ship", "ˈʃɪp̚", "SNARE-SH", "Postalveolar-Sibilant+Labial-Stop", "Hook 1 snare-onset syllable"),
    (24.75, 24.94, "it", "ɪt̚", "HAT-TICK", "HighFront+Unreleased-Alveolar-Stop", "Hook 1 hi-hat link"),
    (24.94, 25.55, "DOWN!", "ˈdaʊn", "HOOK-VOX", "Alveolar-Stop+Wide-Diphthong-Nasal", "Hook 1 cadence (-11.1dB, earshot WHOOSH)"),

    # --- ZOOM 10 (0:25.55 - 0:28.45): Phrase 4 Bar 2 (Boosh + 808 Kicks + Take It Down) ---
    (25.55, 25.68, "[mouth-set]", "p˺", "NONVERBAL-FX", "Bilabial-Compression-Build", "Sub-kick pressure seal"),
    (25.68, 26.16, "BOOSH", "ˈbuʃ", "SNARE-SH", "Bilabial-Kick+Postalveolar-Snare-Wash", "Layered kick+snare splash (-13.7dB)"),
    (26.16, 26.51, "boom", "ˈbuːm", "KICK-808", "Bilabial-Stop+Rounded-Back+Nasal-Hold", "earshot DRUM 808 sub-kick (-16.1dB)"),
    (26.51, 26.70, "buh", "bə", "KICK-GHOST", "Bilabial-Flap-Pickup", "Double-kick 16th pickup"),
    (26.70, 27.20, "boom", "ˈbuːm", "KICK-808", "Bilabial-Stop+Rounded-Back+Nasal-Hold", "Sustained 808 sub-kick"),
    (27.20, 27.50, "[glottal-reset]", "ʔ", "NONVERBAL-FX", "Glottal-Closure-Before-Hook", "Micro-gap before hook"),
    (27.50, 27.68, "take", "ˈtʰɪk̚", "HAT-TICK", "Asp-Alveolar-Stop+Velar-Check", "earshot KEY click hook onset"),
    (27.68, 27.84, "it", "ɪt̚", "HAT-TICK", "HighFront+Alveolar-Check", "Crisp 16th tap"),
    (27.84, 28.45, "DOWN!", "ˈdaʊn", "HOOK-VOX", "Alveolar-Stop+Open-Diphthong-Nasal", "Hook 2 cadence (-16.7dB)"),

    # --- ZOOM 11 (0:28.45 - 0:31.25): Phrase 4 Bar 3 (Boom-ts-Boom + Right Around) ---
    (28.45, 28.57, "[lip-seal]", "b˺", "NONVERBAL-FX", "Bilabial-Pre-Closure", "Bar 3 downbeat prep"),
    (28.57, 28.92, "Boom", "ˈbuːm", "KICK-808", "Bilabial-Stop+Low-F0(93Hz)-Sub-Resonance", "Bar 3 downbeat 808 kick"),
    (28.92, 29.07, "ts", "t͡sʰ", "HAT-TICK", "Asp-Alveolar-Affricate-Burst", "earshot UI scroll wheel tick (hi-hat)"),
    (29.07, 29.42, "boom", "ˈbuːm", "KICK-808", "Bilabial-Stop+Rounded-Nasal-Sub", "Beat 2 808 kick"),
    (29.42, 29.60, "buh", "bə", "KICK-GHOST", "Bilabial-16th-Pickup", "And-of-2 ghost kick"),
    (29.60, 30.15, "boom", "ˈbuːm", "KICK-808", "Bilabial-Stop+Rounded-Nasal-Sub", "Beat 3 808 kick (earshot FOLEY)"),
    (30.15, 30.28, "rrr", "ʀː", "DJ-SCRATCH", "Voiced-Uvular-Trill-Growl", "Gravelly rhotic pre-onset"),
    (30.28, 30.50, "right", "ˈɹaɪt̚", "HOOK-VOX", "Post-Alveolar-Rhotic+Diphthong+Stop", "Hook 3 word 1"),
    (30.50, 30.65, "uh", "ə", "HOOK-VOX", "Central-Vowel-Link", "Hook 3 link"),
    (30.65, 31.12, "ROUND!", "ˈɹaʊnd", "HOOK-VOX", "Rhotic+Wide-Diphthong+Nasal-Alv-Coda", "Hook 3 cadence"),
    (31.12, 31.38, "[breath-lip]", "h̥͡p˺", "NONVERBAL-FX", "Quiet-Nasal-Inhale+Lip-Seal", "Bar 4 prep"),

    # --- ZOOM 12 (0:31.38 - 0:34.20): Phrase 4 Bar 4 (Boom-ts-Boom + Uvular Scratch HRA-HRA!) ---
    (31.38, 31.84, "Boom", "ˈbuːm", "KICK-808", "Bilabial-Stop+91Hz-Sub-Fundamental", "Bar 4 downbeat 808 kick (-16.0dB)"),
    (31.84, 32.01, "ts", "t͡sʰ", "HAT-TICK", "Unvoiced-Alveolar-Affricate-Hat", "Closed hi-hat tick (-20.1dB)"),
    (32.01, 32.36, "boom", "ˈbuːm", "KICK-808", "Bilabial-Stop+Rounded-Nasal-Sub", "Beat 2 808 kick (earshot STEP)"),
    (32.36, 32.54, "buh", "bə", "KICK-GHOST", "Bilabial-16th-Pickup", "Double-kick pickup"),
    (32.54, 33.08, "boom", "ˈbuːm", "KICK-808", "Bilabial-Stop+Rounded-Nasal-Sub", "Beat 3 808 kick"),
    (33.08, 33.26, "Hhh", "χː", "DJ-SCRATCH", "Voiceless-Uvular-Fricative-Scrape", "Turntable forward baby-scratch attack"),
    (33.26, 33.52, "RA", "ˈʀæ", "DJ-SCRATCH", "Uvular-Trill+Wide-Open-Pharynx(F1:1037Hz)", "Turntable forward scratch body"),
    (33.52, 33.63, "hh", "χ", "DJ-SCRATCH", "Voiceless-Uvular-Reverse-Cut", "Crossfader reverse cut"),
    (33.63, 34.10, "RA!", "ˈʀæː", "DJ-SCRATCH", "Uvular-Trill+Open-Front-Release", "Turntable back-scratch (-13.5dB, WHOOSH)"),

    # --- ZOOM 13 (0:34.20 - 0:36.45): Interlude & Pharyngeal/Velar Breath Scrape ---
    (34.20, 34.84, "[room-silence]", "∅", "NONVERBAL-FX", "Ambient-Room-Decay", "Post-groove decay"),
    (34.84, 35.08, "[velar-click]", "k͡x̥", "NONVERBAL-FX", "Unvoiced-Velar-Affricate-Clear", "Soft throat pre-scrape (earshot STEP)"),
    (35.08, 35.45, "[throat-scrape]", "hʀ̥ː", "DJ-SCRATCH", "Unvoiced-Pharyngeal-Uvular-Frication", "Gravelly exhale scrape (-13.9dB, WHOOSH)"),
    (35.45, 36.48, "[pre-outro-gap]", "∅", "NONVERBAL-FX", "Silent-Dramatic-Hold", "1.0s setup pause before tag"),

    # --- ZOOM 14 (0:36.45 - 0:37.82): Phrase 5 Outro Cadence Tag ('Duh-rip-it-NOW!') + Tail ---
    (36.48, 36.70, "Duh", "də", "PLOSIVE-SCAT", "Voiced-Alveolar-Stop+Schwa", "Outro pickup syllable"),
    (36.70, 36.83, "rip", "ˈɹɪp̚", "HAT-TICK", "Rhotic+HighFront+Clipped-Bilabial-Stop", "Staccato labial cut (-14.2dB)"),
    (36.83, 37.00, "it", "ˈɪt̚", "HAT-TICK", "HighFront+Clipped-Alveolar-Stop", "Staccato alveolar cut (-13.1dB)"),
    (37.00, 37.38, "NOW!", "ˈnaʊ", "HOOK-VOX", "Alveolar-Nasal+Open-to-Rounded-Diphthong", "Final cadence resolution"),
    (37.38, 37.60, "[lip-release]", "p˺", "NONVERBAL-FX", "Post-Cadence-Bilabial-Unseal", "Quiet mouth release"),
    (37.60, 37.82, "[mic-tap]", "t˺", "NONVERBAL-FX", "Handling-Stop-Click", "Recording stop transient (-34.5dB)"),
]

ZOOM_WINDOWS = [
    ("zoom_01", "Zoom 01 (0:00.00 – 0:02.38) — Phrase 1A: Dental-Fricative Brushes & Nasal-Gated Plosives", 0.00, 2.38),
    ("zoom_02", "Zoom 02 (0:02.38 – 0:04.75) — Phrase 1B: Labiodental Flams ('frup / fup-it') & Back-Vowel Hold ('all!')", 2.38, 4.75),
    ("zoom_03", "Zoom 03 (0:04.75 – 0:08.15) — Phrase 2A: Sub-Bass Hum ('Mmmm!') & Cork-Pop Velar Scat ('cup / pink / cane')", 4.75, 8.15),
    ("zoom_04", "Zoom 04 (0:08.15 – 0:12.50) — Phrase 2B: Glottal Stops ('ki-'in'), Mini-Wah ('bow') & Inhale Gasp", 8.15, 12.50),
    ("zoom_05", "Zoom 05 (0:12.50 – 0:15.60) — Phrase 3A: Call Hook & Synth-Brass Diphthong Wah Stabs ('BOW-buh-BOW-BOW-BOW!')", 12.50, 15.60),
    ("zoom_06", "Zoom 06 (0:15.60 – 0:18.47) — Phrase 3B: Metric Call-and-Response & Pinched Falsetto Squeak ('WHEN!↑')", 15.60, 18.47),
    ("zoom_07", "Zoom 07 (0:18.47 – 0:20.54) — Phrase 3C: 32nd-Note Plosive Drum Roll ('thuh-buh-chuh-kuh-buh-GAH!') & 'skibidi-BAH!'", 18.47, 20.54),
    ("zoom_08", "Zoom 08 (0:20.54 – 0:22.92) — Phrase 3D: Double-Tongued Lateral-Labial-Velar Chopper ('buh-lip-uh-gih-buh-lep-uh-DAH!')", 20.54, 22.92),
    ("zoom_09", "Zoom 09 (0:22.92 – 0:25.55) — Phrase 4 Bar 1: Air Riser ('FWOO'), Bass Filter ('BWAH'), 808 Kicks & 'ship it DOWN!'", 22.92, 25.55),
    ("zoom_10", "Zoom 10 (0:25.55 – 0:28.45) — Phrase 4 Bar 2: Shibilant Snare Splash ('BOOSH'), 808 Sub-Kicks & 'take it DOWN!'", 25.55, 28.45),
    ("zoom_11", "Zoom 11 (0:28.45 – 0:31.38) — Phrase 4 Bar 3: 808 Kick + Affricate Hi-Hat ('Boom-ts-boom') & Uvular Growl ('rrr-right around!')", 28.45, 31.38),
    ("zoom_12", "Zoom 12 (0:31.38 – 0:34.20) — Phrase 4 Bar 4: 808 Groove + Two-Stage Uvular DJ Record Scratch ('Hhh-RA-hh-RA!')", 31.38, 34.20),
    ("zoom_13", "Zoom 13 (0:34.20 – 0:36.48) — Interlude: Room Decay, Velar Click & Pharyngeal-Uvular Throat Scrape ('[hʀ̥ː]')", 34.20, 36.48),
    ("zoom_14", "Zoom 14 (0:36.48 – 0:37.82) — Phrase 5 Outro Cadence ('Duh-rip-it-NOW!') & Post-Cadence Release", 36.48, 37.82),
]


def measure_event_acoustics(y_16k: np.ndarray, sr: int, s: float, e: float) -> dict:
    i0, i1 = int(s * sr), max(int(s * sr) + 64, int(e * sr))
    seg = y_16k[i0:min(len(y_16k), i1)]
    if len(seg) < 64:
        return {"atk_ms": 0, "pk_db": -60.0, "f0": None, "f1": None, "f2": None, "f3": None, "cent": 0}

    abs_seg = np.abs(seg)
    pk_val = float(np.max(abs_seg))
    pk_db = float(20.0 * np.log10(pk_val + 1e-9))
    pk_idx = int(np.argmax(abs_seg))
    # Attack time from 10% of peak to 100% of peak
    onset_candidates = np.where(abs_seg[:max(1, pk_idx)] < 0.15 * pk_val)[0]
    i_onset = int(onset_candidates[-1]) if len(onset_candidates) else 0
    atk_ms = max(2, int(round((pk_idx - i_onset) / sr * 1000.0)))

    cent = float(np.median(librosa.feature.spectral_centroid(y=seg, sr=sr, n_fft=min(512, len(seg)))[0]))

    # Pitch F0
    f0_val = None
    if len(seg) >= 256:
        try:
            f0, _, _ = librosa.pyin(seg, fmin=65.0, fmax=550.0, sr=sr, frame_length=min(512, len(seg)), hop_length=64)
            vf0 = f0[~np.isnan(f0)] if f0 is not None else []
            if len(vf0):
                f0_val = int(round(float(np.median(vf0))))
        except Exception:
            pass

    # LPC Formants around peak energy
    win = min(len(seg), 480)
    f_start = max(0, min(len(seg) - win, pk_idx - win // 3))
    frame = seg[f_start:f_start + win]
    f1, f2, f3 = None, None, None
    if len(frame) >= 128 and pk_val > 1e-4:
        y_pre = lfilter([1.0, -0.97], [1.0], frame) * np.hamming(len(frame))
        try:
            a = librosa.lpc(y_pre, order=min(16, len(frame) // 4))
            roots = np.roots(a)
            roots = roots[np.imag(roots) >= 0]
            freqs = np.arctan2(np.imag(roots), np.real(roots)) * (sr / (2.0 * np.pi))
            bws = -0.5 * (sr / (2.0 * np.pi)) * np.log(np.abs(roots) + 1e-12)
            fms = [int(round(float(f))) for f, bw in sorted(zip(freqs, bws)) if 180 < f < 4500 and bw < 680]
            if len(fms) >= 1:
                f1 = fms[0]
            if len(fms) >= 2:
                f2 = fms[1]
            if len(fms) >= 3:
                f3 = fms[2]
        except Exception:
            pass

    return {
        "atk_ms": atk_ms,
        "pk_db": round(pk_db, 1),
        "f0": f0_val,
        "f1": f1,
        "f2": f2,
        "f3": f3,
        "cent": int(round(cent)),
    }


def compute_formant_tracks_fine(y: np.ndarray, sr: int, hop_s: float = 0.008, win_s: float = 0.025):
    hop = max(1, int(hop_s * sr))
    win = max(64, int(win_s * sr))
    times, f1_t, f2_t, f3_t = [], [], [], []
    rms = np.array([
        np.sqrt(np.mean(y[i:i + win] ** 2))
        for i in range(0, max(1, len(y) - win), hop)
    ])
    thr = np.percentile(rms, 35) if len(rms) else 1e-4
    for idx, i in enumerate(range(0, max(1, len(y) - win), hop)):
        times.append((i + win / 2) / sr)
        frame = y[i:i + win]
        if rms[idx] < thr or np.max(np.abs(frame)) < 1e-3:
            f1_t.append(np.nan)
            f2_t.append(np.nan)
            f3_t.append(np.nan)
            continue
        y_pre = lfilter([1.0, -0.97], [1.0], frame) * np.hamming(len(frame))
        try:
            a = librosa.lpc(y_pre, order=16)
            roots = np.roots(a)
            roots = roots[np.imag(roots) >= 0]
            freqs = np.arctan2(np.imag(roots), np.real(roots)) * (sr / (2.0 * np.pi))
            bws = -0.5 * (sr / (2.0 * np.pi)) * np.log(np.abs(roots) + 1e-12)
            fms = [float(f) for f, bw in sorted(zip(freqs, bws)) if 180 < f < 4500 and bw < 650]
        except Exception:
            fms = []
        f1_t.append(fms[0] if len(fms) >= 1 else np.nan)
        f2_t.append(fms[1] if len(fms) >= 2 else np.nan)
        f3_t.append(fms[2] if len(fms) >= 3 else np.nan)
    return np.array(times), np.array(f1_t), np.array(f2_t), np.array(f3_t)


def plot_zoom_strip(y_full: np.ndarray, sr: int, z_id: str, title: str, s: float, e: float, ev_list: list[dict]) -> Path:
    i0, i1 = int(s * sr), int(e * sr)
    y = y_full[i0:i1]
    t_axis = np.linspace(s, e, len(y))
    dur = e - s

    y_16k = librosa.resample(y, orig_sr=sr, target_sr=16000)
    ft, f1, f2, f3 = compute_formant_tracks_fine(y_16k, 16000)
    ft = ft + s
    f0, _, _ = librosa.pyin(y_16k, fmin=65.0, fmax=550.0, sr=16000, hop_length=128)
    f0_t = np.linspace(s, e, len(f0)) if f0 is not None else np.array([])

    rms = librosa.feature.rms(y=y, frame_length=512, hop_length=64)[0]
    rms_t = np.linspace(s, e, len(rms))
    rms_norm = rms / (np.max(rms) + 1e-9)

    plt.style.use("dark_background")
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial Unicode MS", "Lucida Grande"]
    fig = plt.figure(figsize=(16, 9.2), dpi=180)
    fig.patch.set_facecolor("#070b14")

    gs = GridSpec(
        6, 1,
        height_ratios=[1.1, 2.3, 0.72, 0.72, 0.78, 0.82],
        hspace=0.07,
        left=0.07, right=0.985, top=0.91, bottom=0.06
    )

    fig.suptitle(title, fontsize=13.5, fontweight="bold", color="#f8fafc", x=0.07, ha="left", y=0.965)
    sub_str = f"Window: {s:.2f}s – {e:.2f}s ({dur:.2f}s span) | {len(ev_list)} Individual Auditory Events | 2.9 ms Onset Resolution"
    fig.text(0.07, 0.93, sub_str, fontsize=9.5, color="#94a3b8", ha="left")

    # 1. Waveform + Attack Envelope
    ax_wav = fig.add_subplot(gs[0])
    ax_wav.set_facecolor("#0f172a")
    ax_wav.plot(t_axis, y, color="#38bdf8", linewidth=0.6, alpha=0.85, label="Waveform")
    ax_wav.plot(rms_t, rms_norm * np.max(np.abs(y)), color="#f43f5e", linewidth=1.5, label="Attack RMS Envelope")
    for ev in ev_list:
        col = CAT_COLORS.get(ev["cat"], "#64748b")
        ax_wav.axvline(ev["start"], color=col, linestyle="--", linewidth=0.9, alpha=0.75)
    ax_wav.set_xlim(s, e)
    ax_wav.set_ylabel("Amp", fontsize=8.5, color="#cbd5e1")
    ax_wav.tick_params(labelbottom=False, labelsize=8)
    ax_wav.legend(loc="upper right", fontsize=7.5, framealpha=0.35)
    ax_wav.grid(True, alpha=0.12)

    # 2. Spectrogram + F1/F2/F3 + F0
    ax_spec = fig.add_subplot(gs[1], sharex=ax_wav)
    ax_spec.set_facecolor("#090d16")
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=64))
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=1024)
    spec_t = np.linspace(s, e, S_db.shape[1])
    ax_spec.pcolormesh(spec_t, freqs, S_db, cmap="magma", vmin=-65, vmax=0, shading="auto")
    ax_spec.scatter(ft, f1, s=15, color="#22d3ee", edgecolors="black", linewidths=0.3, label="F1 (Jaw)", zorder=5)
    ax_spec.scatter(ft, f2, s=15, color="#a3e635", edgecolors="black", linewidths=0.3, label="F2 (Tongue)", zorder=5)
    ax_spec.scatter(ft, f3, s=13, color="#f472b6", edgecolors="black", linewidths=0.3, label="F3 (Pharynx/Lip)", zorder=5)
    if len(f0_t):
        ax_spec.plot(f0_t, f0, color="#fde047", linewidth=2.1, label="F0 (Pitch)", zorder=6)
    for ev in ev_list:
        ax_spec.axvline(ev["start"], color="#ffffff", linestyle=":", linewidth=0.65, alpha=0.45)
    ax_spec.set_yscale("log")
    ax_spec.set_ylim(60, 8000)
    ax_spec.set_yticks([100, 250, 500, 1000, 2000, 4000, 8000])
    ax_spec.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax_spec.set_ylabel("Freq (Hz)", fontsize=8.5, color="#cbd5e1")
    ax_spec.tick_params(labelbottom=False, labelsize=8)
    ax_spec.legend(loc="upper right", fontsize=7.5, ncol=4, framealpha=0.45)

    # 3. Tier 1: English Phonetic Syllable + Event #
    ax_syl = fig.add_subplot(gs[2], sharex=ax_wav)
    # 4. Tier 2: Narrow IPA
    ax_ipa = fig.add_subplot(gs[3], sharex=ax_wav)
    # 5. Tier 3: Category & Articulation
    ax_cat = fig.add_subplot(gs[4], sharex=ax_wav)
    # 6. Tier 4: Acoustic Metadata [ATK | PK | F1/F2]
    ax_meta = fig.add_subplot(gs[5], sharex=ax_wav)

    tier_defs = [
        (ax_syl, "English\nSyllable", "#f8fafc"),
        (ax_ipa, "Narrow\nIPA", "#38bdf8"),
        (ax_cat, "Category &\nArticulation", "#a3e635"),
        (ax_meta, "Bracketed\nMetadata", "#fde047"),
    ]
    for ax, lbl, lcol in tier_defs:
        ax.set_facecolor("#0f172a")
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_ylabel(lbl, fontsize=8, fontweight="bold", color=lcol, rotation=0, labelpad=32, va="center")
        if ax is not ax_meta:
            ax.tick_params(labelbottom=False)
        else:
            ax.set_xlabel("Time (seconds in IMG_3268.mp3)", fontsize=9, color="#e2e8f0")
            ax.tick_params(labelsize=8.5, colors="#cbd5e1")

    for idx, ev in enumerate(ev_list):
        ts, te = ev["start"], ev["end"]
        w = max(0.01, te - ts)
        mid = 0.5 * (ts + te)
        col = CAT_COLORS.get(ev["cat"], "#64748b")
        y_stagger = 0.64 if (idx % 2 == 0) else 0.34

        f_str = f"F1:{ev['f1'] or '-'} F2:{ev['f2'] or '-'}"
        meta_lbl = f"[{ev['pk_db']}dB | {ev['atk_ms']}ms\n{f_str}]"
        cat_lbl = f"{ev['cat']}\n{ev['art'].split('+')[0]}"

        rows = [
            (ax_syl, f"#{ev['idx']:03d} {ev['syl']}", 8.6, "bold", "#ffffff", w < 0.14),
            (ax_ipa, f"[{ev['ipa']}]", 8.4, "normal", "#e0f2fe", w < 0.14),
            (ax_cat, cat_lbl, 6.8, "bold", "#f1f5f9", False),
            (ax_meta, meta_lbl, 6.6, "normal", "#fef08a", False),
        ]
        for ax, txt, fsz, fwt, tcol, do_stag in rows:
            rect = patches.Rectangle((ts, 0.05), w, 0.90, linewidth=1.0, edgecolor=col, facecolor=col, alpha=0.26)
            ax.add_patch(rect)
            ax.axvline(ts, color=col, linewidth=1.0, alpha=0.85)
            ax.axvline(te, color=col, linewidth=0.6, alpha=0.5)
            ty = y_stagger if do_stag else 0.50
            ax.text(mid, ty, txt, ha="center", va="center", color=tcol, fontsize=fsz, fontweight=fwt, clip_on=True)

    out_path = OUT_DIR / f"{z_id}.png"
    fig.savefig(out_path, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)
    shutil.copy2(out_path, ARTIFACT_DIR / out_path.name)
    return out_path


def main() -> None:
    print("Loading IMG_3268.mp3...")
    y_full, sr = librosa.load(str(MP3_PATH), sr=22050, mono=True)
    y_16k = librosa.resample(y_full, orig_sr=sr, target_sr=16000)

    enriched_events = []
    for idx, (s, e, syl, ipa, cat, art, purpose) in enumerate(MICRO_EVENTS, start=1):
        ac = measure_event_acoustics(y_16k, 16000, s, e)
        f0_s = f"{ac['f0']}Hz" if ac["f0"] else "unvoiced"
        f1_s = f"{ac['f1']}" if ac["f1"] else "-"
        f2_s = f"{ac['f2']}" if ac["f2"] else "-"
        f3_s = f"{ac['f3']}" if ac["f3"] else "-"
        bracket = (
            f"[#{idx:03d} | {s:05.2f}–{e:05.2f}s ({int(round((e-s)*1000))}ms) | "
            f"CAT:{cat} | ART:{art} | ATK:{ac['atk_ms']}ms | PK:{ac['pk_db']}dB | "
            f"F0:{f0_s} | F1:{f1_s}/F2:{f2_s}/F3:{f3_s}Hz | CENT:{ac['cent']}Hz | "
            f"ROLE:{purpose} | IPA:{ipa}]"
        )
        enriched_events.append({
            "idx": idx,
            "start": s,
            "end": e,
            "dur_ms": int(round((e - s) * 1000)),
            "syl": syl,
            "ipa": ipa,
            "cat": cat,
            "art": art,
            "purpose": purpose,
            **ac,
            "bracket": bracket,
        })

    (OUT_DIR / "micro_events_138.json").write_text(json.dumps(enriched_events, indent=2, ensure_ascii=False))
    print(f"Computed exact acoustics for {len(enriched_events)} individual auditory events.")

    zoom_figs = []
    for z_id, title, zs, ze in ZOOM_WINDOWS:
        ev_sub = [ev for ev in enriched_events if ev["start"] >= zs - 0.01 and ev["end"] <= ze + 0.02]
        print(f"Rendering {z_id} ({len(ev_sub)} events)...")
        fp = plot_zoom_strip(y_full, sr, z_id, title, zs, ze, ev_sub)
        zoom_figs.append((z_id, title, zs, ze, fp, ev_sub))

    # Update interactive HTML report with all 14 ultra-zoomed windows and 138 bracketed syllable chips
    mp3_b64 = base64.b64encode(MP3_PATH.read_bytes()).decode("ascii")
    dash_b64 = base64.b64encode((OUT_DIR / "fig0_phonetic_acoustic_space.png").read_bytes()).decode("ascii")
    sheet_b64 = base64.b64encode((OUT_DIR / "IMG_3268_sheet.png").read_bytes()).decode("ascii")

    sections_html = []
    for z_id, title, zs, ze, fp, ev_sub in zoom_figs:
        b64 = base64.b64encode(fp.read_bytes()).decode("ascii")
        chips = []
        stream_lines = []
        for ev in ev_sub:
            col = CAT_COLORS.get(ev["cat"], "#64748b")
            f_str = f"F1:{ev['f1'] or '-'}/F2:{ev['f2'] or '-'}Hz"
            chips.append(
                f'<button class="syl-chip" data-start="{ev["start"]:.2f}" data-end="{ev["end"]:.2f}" '
                f'style="border-color:{col}; background:{col}22;" onclick="playSlice({ev["start"]:.2f}, {ev["end"]:.2f})">'
                f'<span class="syl-idx">#{ev["idx"]:03d} ({ev["start"]:.2f}s)</span>'
                f'<span class="syl-en">{ev["syl"]}</span>'
                f'<span class="syl-ipa">[{ev["ipa"]}]</span>'
                f'<span class="syl-fn" style="color:{col}">{ev["cat"]}</span>'
                f'<span class="syl-meta">{ev["atk_ms"]}ms | {ev["pk_db"]}dB | {f_str}</span>'
                f'</button>'
            )
            stream_lines.append(
                f'<div class="stream-item" onclick="playSlice({ev["start"]:.2f}, {ev["end"]:.2f})">'
                f'<code class="meta-bracket" style="color:{col}">{ev["bracket"]}</code> '
                f'<strong class="stream-syl">{ev["syl"]}</strong>'
                f'</div>'
            )
        sections_html.append(f"""
        <section class="window-card" id="{z_id}">
          <div class="window-header">
            <div>
              <h2>{title}</h2>
              <p class="subtitle">{len(ev_sub)} discrete auditory events | Click any chip or bracketed line below to audition that exact slice</p>
            </div>
            <button class="play-window-btn" onclick="playSlice({zs:.2f}, {ze:.2f})">
              ▶ Play {zs:.2f}s – {ze:.2f}s
            </button>
          </div>
          <div class="fig-wrap">
            <img src="data:image/png;base64,{b64}" alt="{title}" />
          </div>
          <div class="chips-row" style="margin-top:14px;">
            {''.join(chips)}
          </div>
          <div class="stream-box">
            {''.join(stream_lines)}
          </div>
        </section>
        """)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>IMG_3268.mp3 — Complete 138-Event Ultra-Zoomed Phonetic & Metadata Atlas</title>
<style>
  :root {{
    --bg: #070a12; --panel: #0f172a; --border: #1e293b; --text: #f8fafc; --muted: #94a3b8;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 20px 28px 80px; background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif;
  }}
  header {{
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    border: 1px solid #334155; border-radius: 14px; padding: 20px 24px;
    margin-bottom: 24px; position: sticky; top: 8px; z-index: 100;
    box-shadow: 0 12px 32px rgba(0,0,0,0.7);
  }}
  h1 {{ margin: 0 0 6px 0; font-size: 21px; }}
  .player-bar {{
    display: flex; align-items: center; gap: 18px; margin-top: 10px;
    background: #090d16; padding: 10px 14px; border-radius: 10px; border: 1px solid #1e293b;
  }}
  audio {{ width: 390px; height: 36px; }}
  .live-readout {{
    flex: 1; display: flex; align-items: center; gap: 14px; font-family: ui-monospace, monospace; flex-wrap: wrap;
  }}
  .live-syl {{ font-size: 22px; font-weight: 800; color: #38bdf8; min-width: 110px; }}
  .live-ipa {{ font-size: 17px; color: #fde047; min-width: 90px; }}
  .live-meta {{ font-size: 12px; color: #a3e635; background: #1e293b; padding: 4px 8px; border-radius: 6px; }}
  .window-card {{
    background: var(--panel); border: 1px solid var(--border); border-radius: 14px;
    padding: 20px; margin-bottom: 26px;
  }}
  .window-header {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; margin-bottom: 12px; }}
  .window-header h2 {{ margin: 0 0 4px 0; font-size: 17px; }}
  .subtitle {{ margin: 0; font-size: 12.5px; color: var(--muted); font-family: ui-monospace, monospace; }}
  .play-window-btn {{
    background: #0284c7; color: white; border: none; border-radius: 8px;
    padding: 8px 14px; font-size: 12.5px; font-weight: 600; cursor: pointer; white-space: nowrap;
  }}
  .fig-wrap img {{ width: 100%; height: auto; border-radius: 8px; border: 1px solid #1e293b; display: block; }}
  .chips-row {{ display: flex; flex-wrap: wrap; gap: 7px; }}
  .syl-chip {{
    display: flex; flex-direction: column; align-items: center; padding: 6px 9px;
    border-radius: 8px; border: 1.5px solid; color: var(--text); cursor: pointer; min-width: 92px;
  }}
  .syl-chip.active, .syl-chip:hover {{ box-shadow: 0 0 0 2px #fff; transform: translateY(-1px); }}
  .syl-idx {{ font-size: 9.5px; color: #cbd5e1; font-family: ui-monospace, monospace; }}
  .syl-en {{ font-size: 14px; font-weight: 800; color: #fff; margin-top: 1px; }}
  .syl-ipa {{ font-size: 12px; color: #bae6fd; font-family: ui-monospace, monospace; }}
  .syl-fn {{ font-size: 10px; font-weight: 700; margin-top: 2px; }}
  .syl-meta {{ font-size: 9px; color: #94a3b8; font-family: ui-monospace, monospace; margin-top: 1px; }}
  .stream-box {{
    margin-top: 14px; background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 12px 14px;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; line-height: 1.75;
  }}
  .stream-item {{ cursor: pointer; padding: 2px 4px; border-radius: 4px; }}
  .stream-item:hover {{ background: #1e293b; }}
  .stream-syl {{ font-size: 14px; color: #ffffff; background: #1e293b; padding: 1px 6px; border-radius: 4px; }}
</style>
</head>
<body>
<header>
  <h1>IMG_3268.mp3 — Ultra-Zoomed 138-Event Auditory &amp; Bracketed-Metadata Phonetic Atlas</h1>
  <div class="player-bar">
    <audio id="mainAudio" controls src="data:audio/mpeg;base64,{mp3_b64}"></audio>
    <div class="live-readout">
      <div><span id="roTime">0.00s</span></div>
      <div class="live-syl" id="roSyl">—</div>
      <div class="live-ipa" id="roIpa">—</div>
      <div class="live-meta" id="roMeta">Click any syllable chip or bracketed line to audition</div>
    </div>
  </div>
</header>
<section class="window-card">
  <h2>Overview — Formant Space (F1 × F2), Drum-Kit Separation &amp; earshot Sheet</h2>
  <div class="fig-wrap"><img src="data:image/png;base64,{dash_b64}" /></div>
  <div class="fig-wrap" style="margin-top:14px;"><img src="data:image/png;base64,{sheet_b64}" /></div>
</section>
{''.join(sections_html)}
<script>
const EVENTS = {json.dumps(enriched_events)};
const audio = document.getElementById('mainAudio');
let stopAt = null;
function playSlice(s, e) {{
  stopAt = e;
  audio.currentTime = s;
  audio.play();
}}
audio.addEventListener('timeupdate', () => {{
  const t = audio.currentTime;
  document.getElementById('roTime').textContent = t.toFixed(2) + 's';
  if (stopAt !== null && t >= stopAt) {{ audio.pause(); stopAt = null; }}
  const hit = EVENTS.find(x => t >= x.start && t <= x.end);
  document.getElementById('roSyl').textContent = hit ? ('#' + String(hit.idx).padStart(3,'0') + ' ' + hit.syl) : '—';
  document.getElementById('roIpa').textContent = hit ? ('[' + hit.ipa + ']') : '—';
  document.getElementById('roMeta').textContent = hit ? hit.bracket : '—';
  document.querySelectorAll('.syl-chip').forEach(btn => {{
    const bs = parseFloat(btn.dataset.start), be = parseFloat(btn.dataset.end);
    btn.classList.toggle('active', t >= bs && t <= be);
  }});
}});
</script>
</body>
</html>
"""
    (OUT_DIR / "IMG_3268_phonetic_report.html").write_text(html, encoding="utf-8")
    print("Updated IMG_3268_phonetic_report.html with all 14 ultra-zoomed windows and 138 bracketed events.")


if __name__ == "__main__":
    main()
