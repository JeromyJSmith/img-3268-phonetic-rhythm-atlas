import base64
import json
import shutil
from pathlib import Path
import numpy as np
import librosa
import librosa.display
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

# Color palette for phonetic/percussive categories
ROLE_COLORS = {
    "kick": "#ef4444",      # Red - Bilabial 808 / sub-kick [buːm]
    "snare": "#f97316",     # Orange - Shibilant snare / splash [buʃ]
    "hat": "#eab308",       # Amber/Gold - Alveolar/velar hi-hat / rim [t͡sʰ, kʰ, ʔ]
    "horn": "#a855f7",      # Purple - Diphthong brass/wah stab [baʊ]
    "riser": "#06b6d4",     # Cyan - Labiodental/uvular air whoosh & scratch [fwuː, χʀæ]
    "scat": "#10b981",      # Emerald - Plosive-vowel rhythmic scat syllable
    "hook": "#3b82f6",      # Blue - Lexical/semi-lexical anchor hook
    "nasal": "#ec4899",     # Pink - Nasal hum / falsetto resonance [mː, wɪ̃nꜛ]
}

ROLE_LABELS = {
    "kick": "808 Sub-Kick [b/m]",
    "snare": "Snare / Splash [b+ʃ]",
    "hat": "Hi-Hat / Click [tʰ/kʰ/ʔ]",
    "horn": "Brass/Wah Diphthong [baʊ]",
    "riser": "Air Whoosh / Scratch [fw/χʀ]",
    "scat": "Plosive Scat Chop",
    "hook": "Vocal Hook / Cadence",
    "nasal": "Nasal Hum / Falsetto",
}

# Time-aligned syllable + IPA + role tiers across all 6 windows
WINDOWS = [
    {
        "id": "fig1_phrase1_plosive_scat",
        "title": "Window 1 (0:00.00 – 0:04.60) — Fast Bilabial / Labiodental / Alveolar Scat Run",
        "subtitle": "5.0 onsets/s | F0 = 104 Hz | F1 = 544 Hz, F2 = 1464 Hz | earshot: chat message pop (z +2.1), mouth pop (z +1.7)",
        "start": 0.00,
        "end": 4.60,
        "syllables": [
            (0.05, 0.22, "thuh", "ðə", "scat", "Dental Fric"),
            (0.22, 0.36, "bitch", "ˈbɪtʃ", "snare", "Affricate Snare"),
            (0.36, 0.52, "camp", "ˈkʰæmp", "hat", "Velar+Nasal Gate"),
            (0.52, 0.71, "brah", "ˈbɹɑː", "horn", "Open Labial Stab"),
            (0.71, 0.90, "thuh", "ðə", "scat", "Dental Pickup"),
            (0.90, 1.07, "rup", "ˈɹʌp", "scat", "Labial Stop Cut"),
            (1.07, 1.24, "in-thuh", "ɪn.ðə", "scat", "Nasal Link"),
            (1.24, 1.51, "pant", "ˈpʰænt", "hat", "Aspirated Stop"),
            (1.51, 1.72, "thence", "ˈðɛns", "hat", "Sibilant Tail"),
            (1.72, 1.89, "bup", "ˈbʌp", "kick", "Bilabial Pop"),
            (1.89, 2.05, "uh-guh", "ə.ɡə", "scat", "Velar Bounce"),
            (2.05, 2.39, "kah-pump", "ˈkʰɑː.pʌmp", "kick", "Velar->Labial Thump"),
            (2.39, 2.73, "thuh-frup", "ðə.ˈfɹʌp", "riser", "Labiodental Brush"),
            (2.73, 3.02, "in-thuh", "ɪn.ðə", "scat", "Dental Link"),
            (3.02, 3.36, "fup-it", "ˈfʌp.ɪt", "hat", "Fricative+Stop"),
            (3.36, 3.70, "at", "æt", "hat", "Alveolar Check"),
            (3.70, 4.35, "all!", "ˈɔːl", "horn", "Back-Vowel Hold"),
        ],
    },
    {
        "id": "fig2_phrase2_nasal_velar_groove",
        "title": "Window 2 (0:04.70 – 0:11.75) — Bilabial Nasal Pickup + Syncopated Velar/Glottal Scat",
        "subtitle": "5.0 onsets/s | F0 = 112 Hz | F1 = 454 Hz, F2 = 1592 Hz | earshot: FOLEY cork pop @ 0:06.72 (-12.7 dBFS)",
        "start": 4.70,
        "end": 11.75,
        "syllables": [
            (4.80, 5.45, "Mmmm!", "mːˀp", "nasal", "Closed-Lip Sub Hum"),
            (6.05, 6.40, "thuh-cup", "ðə.ˈkʰʌp", "hat", "Velar Pop"),
            (6.40, 6.70, "uh-thuh", "ə.ðə", "scat", "Dental Pickup"),
            (6.70, 7.01, "pink", "ˈpʰɪŋk", "hat", "FOLEY Cork Pop"),
            (7.01, 7.44, "cane", "ˈkʰeɪn", "scat", "High-F2 Diphthong"),
            (7.44, 7.80, "tuh-rip", "tə.ˈɹɪp", "hat", "Alveolar->Labial"),
            (7.80, 8.15, "in-thuh", "ɪn.ðə", "scat", "Nasal Link"),
            (8.15, 8.74, "ki-'in", "ˈkʰɪ.ʔɪn", "hat", "Glottal Stop [ʔ]"),
            (8.74, 9.28, "bick-in", "ˈbɪk.ɪn", "kick", "Bilabial->Velar"),
            (9.28, 9.73, "thuh-bow", "ðə.ˈbaʊ", "horn", "Diphthong Stab"),
            (9.73, 10.01, "fen", "fɛn", "riser", "Labiodental Air"),
            (10.01, 10.50, "tuh-sick", "tə.ˈsɪk", "hat", "Sibilant Hi-Hat"),
            (10.50, 10.96, "in-thuh-kuh", "ɪn.ðə.kə", "scat", "16th Velar Link"),
            (10.96, 11.31, "lip-in", "ˈlɪp.ɪn", "scat", "Lateral+Labial"),
            (11.31, 11.68, "NOW!", "ˈnaʊ", "horn", "Open Diphthong End"),
        ],
    },
    {
        "id": "fig3_phrase3a_brass_diphthong_hook",
        "title": "Window 3 (0:12.40 – 0:18.10) — Synth-Brass Diphthong Stabs ('BOW!') & Falsetto Call-and-Response",
        "subtitle": "Peak -7.2 dBFS (loudest) | F1 = 748->360 Hz, F2 = 1402->1519 Hz | earshot: boomy sub-bass / mouth pop",
        "start": 12.40,
        "end": 18.10,
        "syllables": [
            (12.50, 13.07, "You know what", "ju ˈnoʊ wʌt", "hook", "Call Hook"),
            (13.07, 13.54, "BOW", "ˈbaʊ", "horn", "Wah Stab 1"),
            (13.54, 13.72, "buh", "bə", "kick", "Ghost Kick"),
            (13.72, 14.02, "BOW", "ˈbaʊ", "horn", "Wah Stab 2"),
            (14.02, 14.33, "BOW", "ˈbaʊ", "horn", "Wah Stab 3"),
            (14.33, 14.85, "BOW!", "ˈbaʊ", "horn", "Wah Stab 4"),
            (14.90, 15.79, "You know what now", "ju ˈnoʊ wʌt ˈnaʊ", "hook", "Response 1"),
            (15.79, 16.44, "You know what now", "ju ˈnoʊ wʌt ˈnaʊ", "hook", "Response 2"),
            (16.44, 17.28, "You know what then", "ju ˈnoʊ wʌt ˈðɛn", "hook", "Response 3"),
            (17.28, 17.72, "You know what", "ju ˈnoʊ wʌt", "hook", "Setup 4"),
            (17.72, 18.08, "WHEN! (↑)", "ˈwɪ̃n↑", "nasal", "Pinched Falsetto"),
        ],
    },
    {
        "id": "fig4_phrase3b_chopper_fill",
        "title": "Window 4 (0:18.10 – 0:22.80) — Plosive Drum Fill & 16th-Note Lateral/Plosive Chopper Roll",
        "subtitle": "2 ms onset attack | Centroid 2.5 kHz | F1 = 434 Hz, F2 = 1741 Hz | earshot: UI pop @ 0:18.50, lego bricks clicking (z +2.0)",
        "start": 18.10,
        "end": 22.80,
        "syllables": [
            (18.15, 18.46, "You know what", "ju ˈnoʊ wʌt", "hook", "Lead-in"),
            (18.46, 18.94, "thuh-b-ch-k-b", "ðə.bə.tʃə.kə.bə", "hat", "UI Pop Drum Roll"),
            (18.94, 19.35, "GAH!", "ˈɡɑː", "horn", "Open Pharyngeal Hit"),
            (19.35, 19.90, "skibidi", "ˈskɪ.bɪ.dɪ", "scat", "Triple-Tongue Run"),
            (19.90, 20.52, "BAH!", "ˈbɑː", "horn", "Bilabial Accent"),
            (20.55, 21.13, "buh-lip-uh", "bə.ˈlɪp.ə", "scat", "Labial-Lateral Chop"),
            (21.13, 21.56, "gih-buh", "ɡɪ.bə", "scat", "Velar-Labial Bounce"),
            (21.56, 22.06, "lep-uh", "ˈlɛp.ə", "scat", "Lateral-Bilabial"),
            (22.06, 22.70, "DAH!", "ˈdɑː", "horn", "Alveolar Release Hit"),
        ],
    },
    {
        "id": "fig5_phrase4_beatbox_bars1_2",
        "title": "Window 5 (0:22.85 – 0:28.45) — Beatbox Groove Bars 1 & 2 (Air Riser, Sub-Kick, Shibilant Snare & Hooks)",
        "subtitle": "Loudest ST section (-25.2 LUFS) | earshot: WHOOSH @ 0:24.96, DRUM @ 0:26.19, KEY @ 0:26.70, sub bass drop (z +2.1)",
        "start": 22.85,
        "end": 28.45,
        "syllables": [
            (22.92, 23.24, "FWOO", "fwuː", "riser", "Labiodental Riser"),
            (23.24, 23.72, "BWAH", "ˈbwɑː", "horn", "Bass Filter Open"),
            (23.72, 23.93, "boo", "ˈbuː", "kick", "808 Kick"),
            (23.93, 24.16, "buh", "bə", "kick", "Ghost Kick"),
            (24.16, 24.45, "boo", "ˈbuː", "kick", "808 Kick"),
            (24.45, 24.75, "ship", "ˈʃɪp", "snare", "Shibilant Hook"),
            (24.75, 24.95, "it", "ɪt", "hat", "Alveolar Tick"),
            (24.95, 25.45, "DOWN!", "ˈdaʊn", "hook", "Hook Cadence 1"),
            (25.65, 26.14, "BOOSH", "ˈbuʃ", "snare", "Kick+Snare Splash"),
            (26.14, 26.52, "boom", "ˈbuːm", "kick", "DRUM 808 Kick"),
            (26.52, 26.70, "buh", "bə", "kick", "Double-Kick Pickup"),
            (26.70, 27.20, "boom", "ˈbuːm", "kick", "808 Sub-Kick"),
            (27.45, 27.65, "take", "ˈtʰɪk", "hat", "KEY Aspirated [tʰ]"),
            (27.65, 27.85, "it", "ɪt", "hat", "Alveolar Tap"),
            (27.85, 28.35, "DOWN!", "ˈdaʊn", "hook", "Hook Cadence 2"),
        ],
    },
    {
        "id": "fig6_phrase4_5_beatbox_scratch_outro",
        "title": "Window 6 (0:28.45 – 0:34.10) — Beatbox Bars 3 & 4 ('Boom-ts-boom') + Uvular Record Scratch ('HRA-HRA!')",
        "subtitle": "F0 = 91 Hz sub-bass | F1 = 1037 Hz on [χʀæ] scratch | earshot: UI tick @ 0:29.07, WHOOSH swish @ 0:33.20-33.66",
        "start": 28.45,
        "end": 34.10,
        "syllables": [
            (28.55, 28.90, "Boom", "ˈbuːm", "kick", "808 Kick"),
            (28.90, 29.08, "ts", "t͡sʰ", "hat", "UI Hi-Hat Tick"),
            (29.08, 29.42, "boom", "ˈbuːm", "kick", "808 Kick"),
            (29.42, 29.61, "buh", "bə", "kick", "Pickup Kick"),
            (29.61, 30.12, "boom", "ˈbuːm", "kick", "808 Kick"),
            (30.12, 30.52, "rrr-right", "ˈʀaɪt", "hook", "Uvular Growl Onset"),
            (30.52, 31.10, "around!", "ə.ˈɹaʊnd", "hook", "Hook Cadence 3"),
            (31.42, 31.82, "Boom", "ˈbuːm", "kick", "808 Kick"),
            (31.82, 32.00, "ts", "t͡sʰ", "hat", "Closed Hi-Hat"),
            (32.00, 32.36, "boom", "ˈbuːm", "kick", "808 Kick"),
            (32.36, 32.55, "buh", "bə", "kick", "Pickup Kick"),
            (32.55, 33.05, "boom", "ˈbuːm", "kick", "808 Kick"),
            (33.08, 33.48, "HRA", "ˈχʀæ", "riser", "DJ Scratch Fwd"),
            (33.50, 33.92, "HRA!", "ˈχʀæ", "riser", "DJ Scratch Back"),
        ],
    },
    {
        "id": "fig7_phrase5_grunt_and_outro",
        "title": "Window 7 (0:34.50 – 0:37.65) — Pre-Outro Pharyngeal/Velar Breath Scrape & Final Cadence ('Duh-rip-it-NOW!')",
        "subtitle": "5.6 onsets/s | F1 = 464 Hz, F2 = 1526 Hz | earshot: footsteps on gravel (z +3.8) @ 34.8s, kalimba/ice pop @ 36.5s",
        "start": 34.50,
        "end": 37.65,
        "syllables": [
            (34.80, 35.42, "[throat scrape]", "hʀ̥ ~ kx", "riser", "Pharyngeal Scrape"),
            (36.50, 36.70, "Duh", "də", "scat", "Alveolar Pickup"),
            (36.70, 36.84, "rip", "ˈɹɪp", "hat", "Labial Stop Cut"),
            (36.84, 37.01, "it", "ɪt", "hat", "Alveolar Stop"),
            (37.01, 37.42, "NOW!", "ˈnaʊ", "hook", "Final Cadence Tag"),
        ],
    },
]


def compute_formant_tracks(y: np.ndarray, sr: int, hop_s: float = 0.015, win_s: float = 0.030):
    hop = int(hop_s * sr)
    win = int(win_s * sr)
    times, f1_track, f2_track, f3_track = [], [], [], []
    rms = np.array([
        np.sqrt(np.mean(y[i:i + win] ** 2))
        for i in range(0, max(1, len(y) - win), hop)
    ])
    thr = np.percentile(rms, 45) if len(rms) else 1e-4

    for idx, i in enumerate(range(0, max(1, len(y) - win), hop)):
        t = (i + win / 2) / sr
        times.append(t)
        frame = y[i:i + win]
        if rms[idx] < thr or np.max(np.abs(frame)) < 1e-3:
            f1_track.append(np.nan)
            f2_track.append(np.nan)
            f3_track.append(np.nan)
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
        f1_track.append(fms[0] if len(fms) >= 1 else np.nan)
        f2_track.append(fms[1] if len(fms) >= 2 else np.nan)
        f3_track.append(fms[2] if len(fms) >= 3 else np.nan)

    return np.array(times), np.array(f1_track), np.array(f2_track), np.array(f3_track)


def plot_window_figure(y_full: np.ndarray, sr: int, w_cfg: dict) -> Path:
    s, e = w_cfg["start"], w_cfg["end"]
    i0, i1 = int(s * sr), int(e * sr)
    y = y_full[i0:i1]
    dur = e - s
    t_axis = np.linspace(s, e, len(y))

    # Compute spectrogram & formants on 16kHz downsampled copy for clean LPC
    y_16k = librosa.resample(y, orig_sr=sr, target_sr=16000)
    ft, f1, f2, f3 = compute_formant_tracks(y_16k, 16000)
    ft = ft + s

    # Pitch F0
    f0, _, _ = librosa.pyin(y_16k, fmin=65.0, fmax=550.0, sr=16000, hop_length=240)
    f0_t = np.linspace(s, e, len(f0)) if f0 is not None else np.array([])

    # RMS envelope
    hop_rms = 256
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=hop_rms)[0]
    rms_t = np.linspace(s, e, len(rms))
    rms_norm = rms / (np.max(rms) + 1e-9)

    plt.style.use("dark_background")
    fig = plt.figure(figsize=(16, 8.8), dpi=180)
    fig.patch.set_facecolor("#0b0f19")

    gs = GridSpec(
        5, 1,
        height_ratios=[1.15, 2.45, 0.72, 0.72, 0.72],
        hspace=0.08,
        left=0.06, right=0.98, top=0.90, bottom=0.07
    )

    fig.suptitle(w_cfg["title"], fontsize=14, fontweight="bold", color="#f8fafc", x=0.06, ha="left", y=0.965)
    fig.text(0.06, 0.928, w_cfg["subtitle"], fontsize=10, color="#94a3b8", ha="left")

    # 1. Waveform + Attack Envelope
    ax_wav = fig.add_subplot(gs[0])
    ax_wav.set_facecolor("#111827")
    ax_wav.plot(t_axis, y, color="#38bdf8", linewidth=0.55, alpha=0.82, label="Waveform")
    ax_wav.plot(rms_t, rms_norm * np.max(np.abs(y)), color="#f43f5e", linewidth=1.5, alpha=0.95, label="Attack RMS Envelope")
    for ts, te, syl, ipa, role, fn in w_cfg["syllables"]:
        ax_wav.axvline(ts, color=ROLE_COLORS.get(role, "#64748b"), linestyle="--", linewidth=0.8, alpha=0.65)
    ax_wav.set_xlim(s, e)
    ax_wav.set_ylabel("Amp", fontsize=9, color="#cbd5e1")
    ax_wav.tick_params(labelbottom=False, labelsize=8, colors="#94a3b8")
    ax_wav.legend(loc="upper right", fontsize=8, framealpha=0.3)
    ax_wav.grid(True, alpha=0.12)

    # 2. Spectrogram + Formants (F1, F2, F3) + Pitch (F0)
    ax_spec = fig.add_subplot(gs[1], sharex=ax_wav)
    ax_spec.set_facecolor("#090d16")
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=128))
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=1024)
    spec_t = np.linspace(s, e, S_db.shape[1])
    ax_spec.pcolormesh(spec_t, freqs, S_db, cmap="magma", vmin=-65, vmax=0, shading="auto")

    # Overlay Formants & F0
    ax_spec.scatter(ft, f1, s=14, color="#22d3ee", edgecolors="black", linewidths=0.3, label="F1 (Jaw/Height)", zorder=5)
    ax_spec.scatter(ft, f2, s=14, color="#a3e635", edgecolors="black", linewidths=0.3, label="F2 (Tongue Front/Back)", zorder=5)
    ax_spec.scatter(ft, f3, s=12, color="#f472b6", edgecolors="black", linewidths=0.3, label="F3 (Lip/Pharynx)", zorder=5)
    if len(f0_t):
        ax_spec.plot(f0_t, f0, color="#fde047", linewidth=2.0, label="F0 (Pitch)", zorder=6)

    for ts, te, syl, ipa, role, fn in w_cfg["syllables"]:
        ax_spec.axvline(ts, color="#ffffff", linestyle=":", linewidth=0.6, alpha=0.4)

    ax_spec.set_yscale("log")
    ax_spec.set_ylim(60, 8000)
    ax_spec.set_yticks([100, 250, 500, 1000, 2000, 4000, 8000])
    ax_spec.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax_spec.set_ylabel("Freq (Hz)", fontsize=9, color="#cbd5e1")
    ax_spec.tick_params(labelbottom=False, labelsize=8, colors="#94a3b8")
    ax_spec.legend(loc="upper right", fontsize=8, ncol=4, framealpha=0.45)

    # 3. Tier 1: English Phonetic Syllables
    ax_syl = fig.add_subplot(gs[2], sharex=ax_wav)
    ax_syl.set_facecolor("#0f172a")
    ax_syl.set_ylim(0, 1)
    ax_syl.set_yticks([])
    ax_syl.set_ylabel("Syllables\n(English)", fontsize=8.5, fontweight="bold", color="#f8fafc", rotation=0, labelpad=28, va="center")
    ax_syl.tick_params(labelbottom=False)

    # 4. Tier 2: Narrow IPA Transcription
    ax_ipa = fig.add_subplot(gs[3], sharex=ax_wav)
    ax_ipa.set_facecolor("#0f172a")
    ax_ipa.set_ylim(0, 1)
    ax_ipa.set_yticks([])
    ax_ipa.set_ylabel("IPA\nPhonetics", fontsize=8.5, fontweight="bold", color="#38bdf8", rotation=0, labelpad=28, va="center")
    ax_ipa.tick_params(labelbottom=False)

    # 5. Tier 3: Articulatory / Percussive Function
    ax_fn = fig.add_subplot(gs[4], sharex=ax_wav)
    ax_fn.set_facecolor("#0f172a")
    ax_fn.set_ylim(0, 1)
    ax_fn.set_yticks([])
    ax_fn.set_ylabel("Percussive\nFunction", fontsize=8.5, fontweight="bold", color="#a3e635", rotation=0, labelpad=28, va="center")
    ax_fn.set_xlabel("Time (seconds in IMG_3268.mp3)", fontsize=9.5, color="#e2e8f0")
    ax_fn.tick_params(labelsize=8.5, colors="#cbd5e1")

    for idx, (ts, te, syl, ipa, role, fn) in enumerate(w_cfg["syllables"]):
        col = ROLE_COLORS.get(role, "#475569")
        mid = 0.5 * (ts + te)
        w = max(0.02, te - ts)
        y_off = 0.58 if (idx % 2 == 0) else 0.38  # slight vertical stagger for tight boxes

        # Draw intervals on all 3 tiers
        for ax, txt, fsize, fweight, tcol, stagger in [
            (ax_syl, syl, 9.0, "bold", "#ffffff", False),
            (ax_ipa, f"[{ipa}]", 8.5, "normal", "#e0f2fe", False),
            (ax_fn, fn, 7.3, "normal", "#f1f5f9", True),
        ]:
            rect = patches.Rectangle(
                (ts, 0.06), w, 0.88,
                linewidth=1.0, edgecolor=col, facecolor=col, alpha=0.26
            )
            ax.add_patch(rect)
            ax.axvline(ts, color=col, linewidth=1.0, alpha=0.85)
            ax.axvline(te, color=col, linewidth=0.7, alpha=0.5)
            ty = y_off if (stagger and w < 0.35 * (dur / 6.0)) else 0.50
            ax.text(
                mid, ty, txt,
                ha="center", va="center", color=tcol,
                fontsize=fsize, fontweight=fweight, clip_on=True
            )

    out_path = OUT_DIR / f"{w_cfg['id']}.png"
    fig.savefig(out_path, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)
    shutil.copy2(out_path, ARTIFACT_DIR / out_path.name)
    return out_path


def plot_summary_dashboard(y_full: np.ndarray, sr: int, analysis_data: dict) -> Path:
    plt.style.use("dark_background")
    fig = plt.figure(figsize=(16, 10), dpi=180)
    fig.patch.set_facecolor("#0b0f19")
    fig.suptitle(
        "IMG_3268.mp3 — Acoustic-Phonetic Formant Space, Percussive Drum Taxonomy & earshot Profile",
        fontsize=15, fontweight="bold", color="#f8fafc", y=0.965
    )

    gs = GridSpec(2, 2, hspace=0.30, wspace=0.42, left=0.06, right=0.97, top=0.90, bottom=0.09)

    # Compute per-syllable acoustic metrics for scatter plots
    y_16k = librosa.resample(y_full, orig_sr=sr, target_sr=16000)
    syl_points = []
    for w in WINDOWS:
        for ts, te, syl, ipa, role, fn in w["syllables"]:
            seg = y_16k[int(ts * 16000):int(te * 16000)]
            if len(seg) < 256:
                continue
            peak_db = float(20 * np.log10(np.max(np.abs(seg)) + 1e-9))
            cent = float(np.median(librosa.feature.spectral_centroid(y=seg, sr=16000)[0]))
            zcr = float(np.median(librosa.feature.zero_crossing_rate(y=seg)[0]))
            # LPC formants at peak energy frame
            win = min(len(seg), 512)
            peak_idx = int(np.argmax(np.abs(seg)))
            start_f = max(0, min(len(seg) - win, peak_idx - win // 2))
            fr = seg[start_f:start_f + win]
            y_pre = lfilter([1.0, -0.97], [1.0], fr) * np.hamming(len(fr))
            try:
                a = librosa.lpc(y_pre, order=16)
                roots = np.roots(a)
                roots = roots[np.imag(roots) >= 0]
                freqs = np.arctan2(np.imag(roots), np.real(roots)) * (16000 / (2.0 * np.pi))
                bws = -0.5 * (16000 / (2.0 * np.pi)) * np.log(np.abs(roots) + 1e-12)
                fms = [float(f) for f, bw in sorted(zip(freqs, bws)) if 200 < f < 4200 and bw < 600]
            except Exception:
                fms = []
            f1 = fms[0] if len(fms) >= 1 else np.nan
            f2 = fms[1] if len(fms) >= 2 else np.nan
            syl_points.append({
                "ts": ts, "te": te, "syl": syl, "ipa": ipa, "role": role, "fn": fn,
                "f1": f1, "f2": f2, "cent": cent, "zcr": zcr, "peak_db": peak_db
            })

    # Panel A: IPA Vowel & Formant Space (F2 vs F1, inverted axes)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.set_facecolor("#111827")
    for role, label in ROLE_LABELS.items():
        pts = [p for p in syl_points if p["role"] == role and not np.isnan(p["f1"]) and not np.isnan(p["f2"])]
        if not pts:
            continue
        ax_a.scatter(
            [p["f2"] for p in pts],
            [p["f1"] for p in pts],
            s=[max(40, (p["peak_db"] + 35) * 4.5) for p in pts],
            color=ROLE_COLORS[role],
            alpha=0.82,
            edgecolors="#ffffff",
            linewidths=0.5,
            label=label,
        )
    # Annotate key phonetic landmarks
    landmarks = [
        (1400, 750, "BOW [baʊ] onset\n(Open Brass Wah)", "#a855f7"),
        (850, 340, "boom [buːm]\n(Rounded 808 Kick)", "#ef4444"),
        (1740, 430, "buh-lip-uh-gih [ɪ]\n(High-Front Chop)", "#10b981"),
        (1690, 1037, "HRA-HRA [χʀæ]\n(Uvular Scratch)", "#06b6d4"),
        (1520, 360, "WHEN! [wɪ̃nꜛ]\n(Pinched Falsetto)", "#ec4899"),
    ]
    for x, y_val, lbl, col in landmarks:
        ax_a.annotate(
            lbl, xy=(x, y_val), xytext=(x + 180, y_val - 45),
            fontsize=8, fontweight="bold", color=col,
            arrowprops=dict(arrowstyle="->", color=col, lw=1.0),
            bbox=dict(boxstyle="round,pad=0.25", fc="#0b0f19", ec=col, alpha=0.85)
        )
    ax_a.set_xlim(2600, 650)   # Inverted F2 (Front -> Back)
    ax_a.set_ylim(1180, 200)   # Inverted F1 (Close -> Open)
    ax_a.set_xlabel("F2 — Tongue Advancement (Hz, Front ← → Back)", fontsize=9.5, color="#cbd5e1")
    ax_a.set_ylabel("F1 — Jaw Openness (Hz, Close ↑ ↓ Open)", fontsize=9.5, color="#cbd5e1")
    ax_a.set_title("A. Vocal Tract Formant Space (F1 × F2) Across All 84 Syllables", fontsize=11, fontweight="bold", color="#f8fafc")
    ax_a.grid(True, alpha=0.15)
    ax_a.legend(loc="lower left", fontsize=7.5, framealpha=0.5, ncol=2)

    # Panel B: Percussive Drum-Space (Spectral Centroid vs Zero-Crossing Rate / Frication)
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_facecolor("#111827")
    for role, label in ROLE_LABELS.items():
        pts = [p for p in syl_points if p["role"] == role]
        if not pts:
            continue
        ax_b.scatter(
            [p["cent"] for p in pts],
            [p["zcr"] * 100 for p in pts],
            s=[max(45, (p["peak_db"] + 35) * 4.5) for p in pts],
            color=ROLE_COLORS[role],
            alpha=0.82,
            edgecolors="#ffffff",
            linewidths=0.5,
            label=label,
        )
    labeled_syls = set()
    offsets_b = {
        "BOOSH": (40, 1.2),
        "HRA": (45, 0.8),
        "ts": (-140, 1.8),
        "BOW": (-180, 1.8),
        "Mmmm!": (-210, -2.0),
        "pink": (45, -1.5),
        "FWOO": (40, -1.8),
        "WHEN! (↑)": (-120, -2.2),
    }
    for p in syl_points:
        s_name = p["syl"]
        if s_name in offsets_b and s_name not in labeled_syls:
            labeled_syls.add(s_name)
            dx, dy = offsets_b[s_name]
            ax_b.annotate(
                f"{s_name} [{p['ipa']}]",
                xy=(p["cent"], p["zcr"] * 100),
                xytext=(p["cent"] + dx, p["zcr"] * 100 + dy),
                fontsize=7.5,
                color="#f8fafc",
                arrowprops=dict(arrowstyle="-", color="#64748b", lw=0.7),
            )
    ax_b.set_xlabel("Spectral Centroid / Brightness (Hz)", fontsize=9.5, color="#cbd5e1")
    ax_b.set_ylabel("Zero-Crossing / Frication Rate (%)", fontsize=9.5, color="#cbd5e1")
    ax_b.set_title("B. Acoustic Drum-Kit Separation (Brightness vs. Frication Noise)", fontsize=11, fontweight="bold", color="#f8fafc")
    ax_b.grid(True, alpha=0.15)

    # Panel C: Phrase-by-Phrase Formant (F1/F2/F3) & Pitch (F0) Trajectory
    ax_c = fig.add_subplot(gs[1, 0])
    ax_c.set_facecolor("#111827")
    phrases = analysis_data.get("phrases", [])
    p_labels = [
        "1: Scat A\n(0-4.5s)", "2a: Mmm\n(4.8-5.5s)", "2b: Scat B\n(6.0-11.6s)",
        "3a: BOW!\n(12.5-15.5s)", "3b: WHEN!\n(15.5-19.7s)", "3c: 16th Roll\n(19.7-22.7s)",
        "4a: FWOO\n(22.9-25.3s)", "4b: BOOSH\n(25.3-28.0s)", "4c: Boom-ts\n(28.5-31.0s)",
        "4d: HRA-HRA\n(31.1-33.8s)", "5a: Grunt\n(34.7-35.5s)", "5b: Outro\n(36.5-37.3s)"
    ]
    x_idx = np.arange(len(phrases))
    f1_vals = [p["F1_median_hz"] or 0 for p in phrases]
    f2_vals = [p["F2_median_hz"] or 0 for p in phrases]
    f3_vals = [p["F3_median_hz"] or 0 for p in phrases]
    ax_c.plot(x_idx, f1_vals, "o-", color="#22d3ee", linewidth=2, label="F1 Median (Jaw Openness)")
    ax_c.plot(x_idx, f2_vals, "s-", color="#a3e635", linewidth=2, label="F2 Median (Tongue Fronting)")
    ax_c.plot(x_idx, f3_vals, "^-", color="#f472b6", linewidth=1.8, label="F3 Median (Pharyngeal/Lip)")
    ax_c.set_xticks(x_idx)
    ax_c.set_xticklabels(p_labels, fontsize=7.2, rotation=28, ha="right")
    ax_c.set_ylabel("Frequency (Hz)", fontsize=9.5, color="#cbd5e1")
    ax_c.set_title("C. Formant Trajectory (F1, F2, F3) Across All 12 Sub-Phrases", fontsize=11, fontweight="bold", color="#f8fafc")
    ax_c.legend(loc="upper left", fontsize=8, framealpha=0.45)
    ax_c.grid(True, alpha=0.15)

    # Panel D: earshot Calibrated Z-Scores & AudioSet Probabilities
    ax_d = fig.add_subplot(gs[1, 1])
    ax_d.set_facecolor("#111827")
    items = [
        ("Vocal Chop (whole file)", 4.3, "#3b82f6"),
        ("Wet Squelch (HRA-HRA scratch)", 4.0, "#06b6d4"),
        ("Gravel Step (34.8s scrape)", 3.8, "#10b981"),
        ("Punchy Impact (FWOO+BWAH)", 2.5, "#ef4444"),
        ("Chat Msg Pop (0-4s labial)", 2.3, "#ec4899"),
        ("Scroll Tick (29s [ts] hat)", 2.2, "#eab308"),
        ("Sub Bass Drop ([buːm] kick)", 2.1, "#f97316"),
        ("Lego Click (19.8s 16th roll)", 2.0, "#a855f7"),
    ]
    y_pos = np.arange(len(items))
    vals = [it[1] for it in items]
    cols = [it[2] for it in items]
    bars = ax_d.barh(y_pos, vals, color=cols, alpha=0.85, edgecolor="#ffffff", linewidth=0.6)
    ax_d.axvline(2.0, color="#94a3b8", linestyle="--", linewidth=1.0, label="Weak threshold (z=2.0)")
    ax_d.axvline(3.0, color="#fde047", linestyle="--", linewidth=1.0, label="Strong threshold (z=3.0)")
    ax_d.set_yticks(y_pos)
    ax_d.set_yticklabels([it[0] for it in items], fontsize=8.2, color="#e2e8f0")
    ax_d.invert_yaxis()
    for bar, v in zip(bars, vals):
        ax_d.text(v + 0.08, bar.get_y() + bar.get_height() / 2, f"z +{v:.1f}", va="center", fontsize=8, fontweight="bold", color="#f8fafc")
    ax_d.set_xlim(0, 5.0)
    ax_d.set_xlabel("earshot Calibrated Vocabulary Z-Score", fontsize=9.5, color="#cbd5e1")
    ax_d.set_title("D. earshot Non-Lexical Sound-Effect Readings (AST: Speech 0.88, Beatbox 0.74)", fontsize=11, fontweight="bold", color="#f8fafc")
    ax_d.legend(loc="lower right", fontsize=7.5, framealpha=0.45)
    ax_d.grid(True, axis="x", alpha=0.15)

    out_path = OUT_DIR / "fig0_phonetic_acoustic_space.png"
    fig.savefig(out_path, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)
    shutil.copy2(out_path, ARTIFACT_DIR / out_path.name)
    return out_path


def build_interactive_html(fig_paths: list[Path], dash_path: Path, sheet_path: Path) -> Path:
    mp3_b64 = base64.b64encode(MP3_PATH.read_bytes()).decode("ascii")

    def img_b64(p: Path) -> str:
        return base64.b64encode(p.read_bytes()).decode("ascii")

    windows_json = json.dumps(WINDOWS)
    role_colors_json = json.dumps(ROLE_COLORS)
    role_labels_json = json.dumps(ROLE_LABELS)

    cards_html = []
    for w, fp in zip(WINDOWS, fig_paths):
        b64 = img_b64(fp)
        chips = []
        for ts, te, syl, ipa, role, fn in w["syllables"]:
            col = ROLE_COLORS.get(role, "#475569")
            chips.append(
                f'<button class="syl-chip" data-start="{ts:.2f}" data-end="{te:.2f}" '
                f'style="border-color:{col}; background:{col}22;" onclick="playSlice({ts:.2f}, {te:.2f})">'
                f'<span class="syl-en">{syl}</span>'
                f'<span class="syl-ipa">[{ipa}]</span>'
                f'<span class="syl-fn" style="color:{col}">{fn}</span>'
                f'<span class="syl-t">{ts:.2f}–{te:.2f}s</span>'
                f'</button>'
            )
        cards_html.append(f"""
        <section class="window-card" id="{w['id']}">
          <div class="window-header">
            <div>
              <h2>{w['title']}</h2>
              <p class="subtitle">{w['subtitle']}</p>
            </div>
            <button class="play-window-btn" onclick="playSlice({w['start']:.2f}, {w['end']:.2f})">
              ▶ Play Window ({w['start']:.2f}s – {w['end']:.2f}s)
            </button>
          </div>
          <div class="fig-wrap">
            <img src="data:image/png;base64,{b64}" alt="{w['title']}" />
          </div>
          <div class="chips-label">Click any syllable below to audition that exact phonetic transient:</div>
          <div class="chips-row">
            {''.join(chips)}
          </div>
        </section>
        """)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>IMG_3268.mp3 — Complete Acoustic-Phonetic & Earshot Report</title>
<style>
  :root {{
    --bg: #070a12;
    --panel: #0f172a;
    --border: #1e293b;
    --text: #f8fafc;
    --muted: #94a3b8;
    --accent: #38bdf8;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 24px 32px 80px;
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif;
    line-height: 1.5;
  }}
  header {{
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 24px;
    position: sticky;
    top: 10px;
    z-index: 100;
    box-shadow: 0 12px 32px rgba(0,0,0,0.65);
  }}
  .top-row {{
    display: flex; align-items: center; justify-content: space-between; gap: 20px; flex-wrap: wrap;
  }}
  h1 {{ margin: 0 0 4px 0; font-size: 22px; letter-spacing: -0.02em; }}
  .meta-badges {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 8px; }}
  .badge {{
    background: #1e293b; border: 1px solid #475569; border-radius: 999px;
    padding: 3px 11px; font-size: 12px; color: #e2e8f0; font-family: ui-monospace, monospace;
  }}
  .player-bar {{
    display: flex; align-items: center; gap: 18px; margin-top: 14px;
    background: #090d16; padding: 12px 16px; border-radius: 10px; border: 1px solid #1e293b;
  }}
  audio {{ width: 420px; height: 38px; }}
  .live-readout {{
    flex: 1; display: flex; align-items: center; gap: 16px;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  }}
  .live-syl {{
    font-size: 22px; font-weight: 800; color: #38bdf8; min-width: 140px;
  }}
  .live-ipa {{
    font-size: 18px; color: #fde047; min-width: 130px;
  }}
  .live-fn {{
    font-size: 13px; color: #a3e635; background: #1e293b; padding: 4px 10px; border-radius: 6px;
  }}
  .window-card {{
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 14px; padding: 22px; margin-bottom: 28px;
  }}
  .window-header {{
    display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; margin-bottom: 14px;
  }}
  .window-header h2 {{ margin: 0 0 4px 0; font-size: 18px; color: #f1f5f9; }}
  .subtitle {{ margin: 0; font-size: 13px; color: var(--muted); font-family: ui-monospace, monospace; }}
  .play-window-btn {{
    background: #0284c7; color: white; border: none; border-radius: 8px;
    padding: 9px 16px; font-size: 13px; font-weight: 600; cursor: pointer; white-space: nowrap;
  }}
  .play-window-btn:hover {{ background: #0369a1; }}
  .fig-wrap img {{
    width: 100%; height: auto; border-radius: 8px; border: 1px solid #1e293b; display: block;
  }}
  .chips-label {{
    font-size: 12px; color: var(--muted); margin: 14px 0 8px; text-transform: uppercase; letter-spacing: 0.05em;
  }}
  .chips-row {{
    display: flex; flex-wrap: wrap; gap: 8px;
  }}
  .syl-chip {{
    display: flex; flex-direction: column; align-items: center;
    padding: 7px 11px; border-radius: 8px; border: 1.5px solid;
    color: var(--text); cursor: pointer; transition: transform 0.1s, box-shadow 0.1s;
    min-width: 82px;
  }}
  .syl-chip:hover, .syl-chip.active {{
    transform: translateY(-2px);
    box-shadow: 0 0 0 2px #f8fafc;
  }}
  .syl-en {{ font-size: 14px; font-weight: 700; color: #ffffff; }}
  .syl-ipa {{ font-size: 12.5px; color: #bae6fd; font-family: ui-monospace, monospace; margin-top: 2px; }}
  .syl-fn {{ font-size: 10.5px; font-weight: 600; margin-top: 2px; }}
  .syl-t {{ font-size: 9.5px; color: #94a3b8; font-family: ui-monospace, monospace; margin-top: 2px; }}
</style>
</head>
<body>
<header>
  <div class="top-row">
    <div>
      <h1>IMG_3268.mp3 — Acoustic-Phonetic, Formant &amp; Percussive Syllable Atlas</h1>
      <div class="meta-badges">
        <span class="badge">Duration: 37.82s</span>
        <span class="badge">199 Transient Events (5.3/s)</span>
        <span class="badge">Loudness: -28.2 LUFS / Peak -7.2 dBTP</span>
        <span class="badge">AST: Speech 0.88 | Beatboxing 0.74 | Whispering 0.43</span>
        <span class="badge">CLAP: Vocal Chop z +4.3 | p_real 0.99</span>
      </div>
    </div>
  </div>
  <div class="player-bar">
    <audio id="mainAudio" controls src="data:audio/mpeg;base64,{mp3_b64}"></audio>
    <div class="live-readout">
      <div><span style="color:#64748b;font-size:11px;display:block;">TIME</span><span id="roTime">0.00s</span></div>
      <div><span style="color:#64748b;font-size:11px;display:block;">SYLLABLE</span><span class="live-syl" id="roSyl">—</span></div>
      <div><span style="color:#64748b;font-size:11px;display:block;">IPA</span><span class="live-ipa" id="roIpa">—</span></div>
      <div><span style="color:#64748b;font-size:11px;display:block;">PERCUSSIVE ROLE</span><span class="live-fn" id="roFn">Ready</span></div>
    </div>
  </div>
</header>

<section class="window-card">
  <div class="window-header">
    <div>
      <h2>Overview 1 — Vocal Tract Formant Space (F1 × F2), Drum-Kit Separation &amp; earshot Z-Scores</h2>
      <p class="subtitle">All 84 segmented vocal-percussion syllables mapped by LPC formants, spectral centroid, frication rate, and earshot model readings</p>
    </div>
  </div>
  <div class="fig-wrap">
    <img src="data:image/png;base64,{img_b64(dash_path)}" alt="Phonetic Acoustic Space Dashboard" />
  </div>
</section>

<section class="window-card">
  <div class="window-header">
    <div>
      <h2>Overview 2 — Full-Track earshot Listening Sheet (0:00.00 – 0:37.82)</h2>
      <p class="subtitle">Video frames, sections, CLAP/AST event labels, log spectrogram (30 Hz – 16 kHz), waveform, and BS.1770 LUFS loudness curve</p>
    </div>
  </div>
  <div class="fig-wrap">
    <img src="data:image/png;base64,{img_b64(sheet_path)}" alt="Earshot Full Sheet" />
  </div>
</section>

{''.join(cards_html)}

<script>
const WINDOWS = {windows_json};
const ALL_SYLS = [];
WINDOWS.forEach(w => {{
  w.syllables.forEach(s => {{
    ALL_SYLS.push({{ start: s[0], end: s[1], syl: s[2], ipa: s[3], role: s[4], fn: s[5] }});
  }});
}});

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
  if (stopAt !== null && t >= stopAt) {{
    audio.pause();
    stopAt = null;
  }}
  const hit = ALL_SYLS.find(x => t >= x.start && t <= x.end);
  document.getElementById('roSyl').textContent = hit ? hit.syl : '—';
  document.getElementById('roIpa').textContent = hit ? '[' + hit.ipa + ']' : '—';
  document.getElementById('roFn').textContent = hit ? hit.fn : 'Pause / Breath';
  document.querySelectorAll('.syl-chip').forEach(btn => {{
    const bs = parseFloat(btn.dataset.start);
    const be = parseFloat(btn.dataset.end);
    btn.classList.toggle('active', t >= bs && t <= be);
  }});
}});
</script>
</body>
</html>
"""
    out_html = OUT_DIR / "IMG_3268_phonetic_report.html"
    out_html.write_text(html, encoding="utf-8")
    return out_html


def main() -> None:
    print("Loading audio and earshot analysis...")
    y_full, sr = librosa.load(str(MP3_PATH), sr=22050, mono=True)
    analysis_data = json.loads((OUT_DIR / "earshot_phonetic_analysis.json").read_text())

    sheet_path = OUT_DIR / "IMG_3268_sheet.png"
    shutil.copy2(sheet_path, ARTIFACT_DIR / sheet_path.name)

    fig_paths = []
    for w in WINDOWS:
        print(f"Rendering {w['id']}...")
        fp = plot_window_figure(y_full, sr, w)
        fig_paths.append(fp)

    print("Rendering summary dashboard...")
    dash_path = plot_summary_dashboard(y_full, sr, analysis_data)

    print("Building self-contained interactive HTML report...")
    html_path = build_interactive_html(fig_paths, dash_path, sheet_path)
    print(f"Done! HTML report at: {html_path}")


if __name__ == "__main__":
    main()
