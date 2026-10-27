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

WORKSPACE = Path("/Volumes/2TB/moviesfolder/MOVIES_FOLDER/studpid Stuff")
MP3_PATH = WORKSPACE / "IMG_3268.mp3"
OUT_DIR = WORKSPACE / "analysis"
ARTIFACT_DIR = Path("/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df")

from build_ultra_zoom_report import CAT_COLORS, ZOOM_WINDOWS, compute_formant_tracks_fine

# Musical Sections / Bar Frameworks across IMG_3268.mp3
# Defines local BPM, quarter-note duration, bar downbeats, and rhythmic behavior feel
RHYTHM_SECTIONS = [
    {
        "sec_id": "S1",
        "name": "Phrase 1: Syncopated Plosive-Brush Pocket",
        "start": 0.26,
        "end": 4.35,
        "bpm": 103.0,
        "time_sig": "4/4",
        "feel": "Swung 16th-Note Pocket (58% Swing Ratio) + Anacrusis Pickup",
        "bars": [
            (1, 0.26, 2.52, "4/4", 106.2, "Bar 1 — Syncopated 16th Plosive-Fricative Groove"),
            (2, 2.52, 4.35, "4/4", 100.0, "Bar 2 — Labiodental Flams & Dotted-Quarter Fermata ('all!')"),
        ],
    },
    {
        "sec_id": "S2",
        "name": "Phrase 2: Sub-Hum Reset & Cork-Pop Backbeat Groove",
        "start": 4.75,
        "end": 12.50,
        "bpm": 96.0,
        "time_sig": "4/4",
        "feel": "Laid-Back Neo-Soul Pocket (-18 ms Behind Beat) + Glottal Syncopation",
        "bars": [
            (3, 4.75, 6.20, "2/4", 82.8, "Bar 3 — Half-Note Sub-Bass Hum ('Mmmm!') & Breath Pocket"),
            (4, 6.20, 8.78, "4/4", 93.0, "Bar 4 — Cork-Pop ('pink') & Glottal-Cut Syncopation ('ki-'in')"),
            (5, 8.78, 11.72, "4/4", 95.2, "Bar 5 — Offbeat Wah ('bow'), 16th Run & Cadence ('NOW!')"),
        ],
    },
    {
        "sec_id": "S3A",
        "name": "Phrase 3A–3B: Call-and-Response Hook & Metric Acceleration",
        "start": 12.50,
        "end": 18.47,
        "bpm": 112.0,
        "time_sig": "4/4",
        "feel": "Pushed Funk Horn Stabs + Accelerating 16th-Pickup Call-and-Response",
        "bars": [
            (6, 12.50, 15.32, "4/4", 98.0, "Bar 6 — 16th Call ('You know what') + Syncopated Brass Wah Stabs ('BOW!')"),
            (7, 15.32, 18.47, "4/4", 118.5, "Bar 7 — Accelerating 3x 'You know what' Cycles + Falsetto Upbeat ('WHEN!↑')"),
        ],
    },
    {
        "sec_id": "S3B",
        "name": "Phrase 3C–3D: 32nd-Note Drum Roll, Triplets & Double-Tongue Chopper",
        "start": 18.47,
        "end": 22.92,
        "bpm": 128.0,
        "time_sig": "4/4",
        "feel": "Virtuosic Subdivision Shift: 32nd-Note Paradiddle -> Sextuplet ('skibidi') -> Straight 16th Chopper",
        "bars": [
            (8, 18.47, 20.54, "4/4", 116.0, "Bar 8 — 32nd-Note Plosive Roll ('thuh-buh-chuh-kuh-buh') + Triplet ('ski-bi-di-BAH!')"),
            (9, 20.54, 22.92, "4/4", 131.0, "Bar 9 — Machine-Gun 16th Lateral-Labial-Velar Chopper ('buh-lip-uh-gih-buh-lep-uh-DAH!')"),
        ],
    },
    {
        "sec_id": "S4",
        "name": "Phrase 4: 4-Bar Heavy Beatbox 808 Groove & Turntable Scratch Breakdown",
        "start": 22.92,
        "end": 34.20,
        "bpm": 83.5,
        "time_sig": "4/4",
        "feel": "Heavy Halftime / Boom-Bap 808 Groove (83.5 BPM) — Dotted-8th + 16th Kick-Hat-Kick + Hook on Beat 3–4",
        "bars": [
            (10, 22.92, 25.68, "4/4", 87.0, "Bar 10 (Beatbox Bar 1) — Riser ('FWOO-BWAH') + 808 Kicks + 'ship it DOWN!'"),
            (11, 25.68, 28.57, "4/4", 83.0, "Bar 11 (Beatbox Bar 2) — Snare Splash ('BOOSH') + 808 Kicks + 'take it DOWN!'"),
            (12, 28.57, 31.38, "4/4", 85.4, "Bar 12 (Beatbox Bar 3) — Classic 'Boom-ts-boom-buh-boom' + 'rrr-right around!'"),
            (13, 31.38, 34.20, "4/4", 85.1, "Bar 13 (Beatbox Bar 4) — 'Boom-ts-boom-buh-boom' + 16th DJ Scratch ('Hhh-RA-hh-RA!')"),
        ],
    },
    {
        "sec_id": "S5",
        "name": "Phrase 5: Rubato Scrape Interlude & Final Coda Tag",
        "start": 34.20,
        "end": 37.82,
        "bpm": 96.0,
        "time_sig": "2/4",
        "feel": "Caesura Rest + Tight 16th-Note Coda Tag ('Duh-rip-it-NOW!') on Downbeat",
        "bars": [
            (14, 34.20, 36.48, "Free", 0.0, "Bar 14 — Caesura Rest + Uvular Scrape ('[velar-click] -> [throat-scrape]')"),
            (15, 36.48, 37.82, "2/4", 96.0, "Bar 15 (Coda Tag) — 16th Pickup ('Duh-rip-it') -> Accented Downbeat ('NOW!')"),
        ],
    },
]

# Map musical note values based on IOI ratio to quarter note (beat_dur = 60 / bpm)
NOTE_SYMBOLS = [
    (0.18, "♬", "32nd", "1/32 note"),
    (0.30, "♪³", "16th-trip", "16th-note triplet (sextuplet)"),
    (0.44, "♬", "16th", "16th note (semiquaver)"),
    (0.60, "♬·", "dotted-16th", "Dotted 16th note"),
    (0.72, "♪³", "8th-trip", "8th-note triplet"),
    (0.92, "♪", "8th", "8th note (quaver)"),
    (1.38, "♪·", "dotted-8th", "Dotted 8th note"),
    (1.85, "♩", "quarter", "Quarter note (crotchet)"),
    (2.75, "♩·", "dotted-quarter", "Dotted quarter note"),
    (99.0, "♩—", "half+", "Half note / sustained fermata"),
]

# Map categories to 5-lane Drum/Vocal Staff positions
STAFF_LANE = {
    "KICK-808": (1, "Kick (808/Sub)", "●"),
    "KICK-GHOST": (1, "Kick (Ghost)", "○"),
    "SNARE-SH": (2, "Snare / Clap", "◆"),
    "GLOTTAL-POP": (2, "Rim / Pop", "◈"),
    "HAT-TICK": (3, "Hi-Hat / Tick", "×"),
    "FRIC-BRUSH": (3, "Brush Hat", "+"),
    "LIQUID-CHOP": (3, "Chopper", "▲"),
    "PLOSIVE-SCAT": (3, "Plosive Scat", "■"),
    "NASAL-GATE": (4, "Nasal / Clamp", "▬"),
    "BRASS-WAH": (4, "Brass / Synth", "◆"),
    "HOOK-VOX": (4, "Hook Vocal", "♩"),
    "FALSETTO-SQ": (4, "Falsetto Lead", "↑"),
    "AIR-RISER": (5, "Turntable / FX", "≈"),
    "DJ-SCRATCH": (5, "DJ Scratch", "⚡"),
    "NONVERBAL-FX": (5, "Breath / Rest", "—"),
}


def find_bar_for_time(t: float):
    for sec in RHYTHM_SECTIONS:
        for bar_num, bs, be, tsig, bpm, bdesc in sec["bars"]:
            if bs - 0.05 <= t < be + 0.01:
                return sec, bar_num, bs, be, tsig, bpm, bdesc
    # Pre-pickup before Bar 1 (0.00 - 0.26s)
    sec0 = RHYTHM_SECTIONS[0]
    if t < 0.26:
        return sec0, 0, 0.00, 0.26, "Pickup", 103.0, "Anacrusis Pickup before Bar 1 ('thuh')"
    sec_last = RHYTHM_SECTIONS[-1]
    return sec_last, 15, 36.48, 37.82, "2/4", 96.0, "Coda Tail"


def classify_note_value(dur_s: float, ioi_s: float, bpm: float, cat: str) -> tuple[str, str, str, float]:
    if cat == "NONVERBAL-FX":
        if dur_s >= 0.45:
            return "[♩ rest]", "quarter-rest", "Quarter-note breath/rest", round(dur_s / 0.6, 2)
        return "[♪ rest]", "16th-rest", "16th-note micro-breath/pickup", round(dur_s / 0.6, 2)

    q_dur = 60.0 / bpm if bpm > 0 else 0.60
    eff_dur = ioi_s if (ioi_s > 0 and ioi_s < dur_s * 1.45) else dur_s
    beats = eff_dur / q_dur
    for max_b, sym, short_name, full_name in NOTE_SYMBOLS:
        if beats <= max_b:
            return sym, short_name, full_name, round(beats, 2)
    return "♩—", "half+", "Half note / sustained", round(beats, 2)


def compute_subdivision_label(pos_in_bar_beats: float, tsig: str, bpm: float) -> tuple[str, float]:
    if bpm <= 0 or tsig in ("Pickup", "Free"):
        return ("Pickup (4-a)" if tsig == "Pickup" else "Rubato / Free"), 0.0

    n_beats = 2 if tsig == "2/4" else 4
    wrapped = pos_in_bar_beats % n_beats
    beat_idx = int(np.floor(wrapped + 0.08)) % n_beats + 1
    rem = wrapped - np.floor(wrapped + 0.08)
    if rem < 0:
        rem += 1.0

    # Check closest 16th-note or triplet grid point
    grid_candidates = [
        (0.00, f"Beat {beat_idx} (Downbeat)" if beat_idx == 1 else f"Beat {beat_idx}"),
        (0.25, f"{beat_idx}-e"),
        (0.333, f"{beat_idx}-trip-let (2nd)"),
        (0.50, f"{beat_idx}-&"),
        (0.667, f"{beat_idx}-trip-let (3rd)"),
        (0.75, f"{beat_idx}-a"),
        (0.875, f"{beat_idx}-a+ (32nd pickup)"),
        (1.00, f"Beat {(beat_idx % n_beats) + 1}"),
    ]
    best_g, best_lbl = min(grid_candidates, key=lambda g: abs(rem - g[0]))
    q_dur = 60.0 / bpm
    dev_ms = round((rem - best_g) * q_dur * 1000.0, 1)
    return best_lbl, dev_ms


def enrich_events_with_rhythm(events: list[dict]) -> list[dict]:
    for i, ev in enumerate(events):
        s = ev["start"]
        e = ev["end"]
        next_s = events[i + 1]["start"] if i + 1 < len(events) else e
        ioi_s = max(e - s, next_s - s)
        ioi_ms = int(round(ioi_s * 1000))

        sec, bar_num, bs, be, tsig, bpm, bdesc = find_bar_for_time(s)
        q_dur = 60.0 / bpm if bpm > 0 else 0.60
        pos_beats = (s - bs) / q_dur if bpm > 0 and bar_num > 0 else 0.0

        sub_lbl, dev_ms = compute_subdivision_label(pos_beats, tsig, bpm)
        note_sym, note_short, note_full, beats_val = classify_note_value(e - s, ioi_s, bpm, ev["cat"])

        # Special precision overrides for known signature rhythmic motifs
        if 18.47 <= s < 18.94:
            note_sym, note_short, note_full = "♬", "32nd-roll", "32nd-note paradiddle roll"
        elif 19.35 <= s < 19.85:
            note_sym, note_short, note_full = "♪³", "16th-triplet", "Sextuplet / 16th-triplet figure ('ski-bi-di')"

        lane_idx, lane_name, head_sym = STAFF_LANE.get(ev["cat"], (3, "Perc", "●"))

        dev_str = f"{dev_ms:+.0f}ms" if bpm > 0 and bar_num > 0 else "free"
        rhy_tag = f"BAR:{bar_num:02d}({tsig}@{bpm:.0f}BPM) | GRID:{sub_lbl} | NOTE:{note_sym} {note_short} (IOI:{ioi_ms}ms, {dev_str})"

        ev["bar_num"] = bar_num
        ev["bar_desc"] = bdesc
        ev["time_sig"] = tsig
        ev["local_bpm"] = round(bpm, 1)
        ev["grid_pos"] = sub_lbl
        ev["note_sym"] = note_sym
        ev["note_short"] = note_short
        ev["note_full"] = note_full
        ev["ioi_ms"] = ioi_ms
        ev["microtiming_ms"] = dev_ms
        ev["staff_lane"] = lane_idx
        ev["staff_lane_name"] = lane_name
        ev["staff_head"] = head_sym

        # Update bracket to include full rhythmic notation metadata right inside the bracket
        f0_s = f"{ev['f0']}Hz" if ev["f0"] else "unvoiced"
        f1_s = f"{ev['f1']}" if ev["f1"] else "-"
        f2_s = f"{ev['f2']}" if ev["f2"] else "-"
        f3_s = f"{ev['f3']}" if ev["f3"] else "-"
        ev["bracket"] = (
            f"[#{ev['idx']:03d} | {s:05.2f}–{e:05.2f}s ({ev['dur_ms']}ms, IOI:{ioi_ms}ms) | "
            f"BAR:{bar_num:02d} {sub_lbl} | NOTE:{note_sym} {note_short} ({dev_str}@{bpm:.0f}BPM) | "
            f"CAT:{ev['cat']} | ART:{ev['art']} | ATK:{ev['atk_ms']}ms | PK:{ev['pk_db']}dB | "
            f"F0:{f0_s} | F1:{f1_s}/F2:{f2_s}/F3:{f3_s}Hz | IPA:{ev['ipa']}]"
        )
    return events


def plot_rhythm_overview(events: list[dict], y_full: np.ndarray, sr: int) -> tuple[Path, Path]:
    plt.style.use("dark_background")
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial Unicode MS", "Lucida Grande"]

    # --- FIGURE A: Global Rhythmic Architecture (Tempo Curve, IOI Subdivision Histogram, Microtiming & Groove Grid) ---
    fig = plt.figure(figsize=(16, 10.5), dpi=180)
    fig.patch.set_facecolor("#070b14")
    gs = GridSpec(3, 2, height_ratios=[1.15, 1.15, 1.35], hspace=0.34, wspace=0.20, left=0.06, right=0.97, top=0.91, bottom=0.06)

    fig.suptitle(
        "IMG_3268.mp3 — Musical Rhythm, Tempo Rubato, Subdivision Density & Drum-Staff Architecture",
        fontsize=14.5, fontweight="bold", color="#f8fafc", x=0.06, ha="left", y=0.965
    )
    fig.text(
        0.06, 0.932,
        "15 Musical Bars Across 5 Phrases | Local Tempo Curve (83–131 BPM) | IOI Note-Value Distribution | 5-Line Vocal Percussion Staff",
        fontsize=9.8, color="#94a3b8", ha="left"
    )

    # Panel 1 (Top Full Width): Local Tempo (BPM) & Subdivision Density (Notes/sec) over Time
    ax_tempo = fig.add_subplot(gs[0, :])
    ax_tempo.set_facecolor("#0f172a")
    times = [ev["start"] for ev in events if ev["cat"] != "NONVERBAL-FX"]
    bpms = [ev["local_bpm"] for ev in events if ev["cat"] != "NONVERBAL-FX"]
    iois = [max(0.06, ev["ioi_ms"] / 1000.0) for ev in events if ev["cat"] != "NONVERBAL-FX"]
    inst_nps = [min(14.0, 1.0 / x) for x in iois]

    ax_tempo.step(times, bpms, where="post", color="#38bdf8", linewidth=2.4, label="Local Metric Tempo (BPM)")
    ax_tempo.fill_between(times, bpms, 60, step="post", color="#38bdf8", alpha=0.15)
    for sec in RHYTHM_SECTIONS:
        for bar_num, bs, be, tsig, bpm, bdesc in sec["bars"]:
            ax_tempo.axvline(bs, color="#fde047", linestyle="--", linewidth=0.9, alpha=0.6)
            ax_tempo.text(bs + 0.06, 136, f"Bar {bar_num}\n{tsig}", fontsize=7.5, color="#fde047", fontweight="bold", va="top")

    ax_tempo.set_xlim(0, 37.82)
    ax_tempo.set_ylim(65, 145)
    ax_tempo.set_ylabel("Tempo (BPM)", fontsize=9, color="#38bdf8")
    ax_tempo.set_title("1. Metric Tempo Map & Bar Downbeats (Shows Accelerando in Phrase 3 -> Heavy 84 BPM Halftime Drop in Phrase 4)", fontsize=10.5, fontweight="bold", color="#f8fafc", loc="left")
    ax_tempo.grid(True, alpha=0.15)

    ax_nps = ax_tempo.twinx()
    ax_nps.scatter(times, inst_nps, s=22, color="#f43f5e", alpha=0.85, label="Instantaneous Event Rate (syllables/sec)")
    ax_nps.set_ylim(0, 15)
    ax_nps.set_ylabel("Syllables / Sec", fontsize=9, color="#f43f5e")

    # Panel 2 (Middle Left): Inter-Onset Interval (IOI) Distribution & Musical Note Value Clusters
    ax_ioi = fig.add_subplot(gs[1, 0])
    ax_ioi.set_facecolor("#0f172a")
    note_order = ["32nd-roll", "32nd", "16th-triplet", "16th-trip", "16th", "dotted-16th", "8th-trip", "8th", "dotted-8th", "quarter", "dotted-quarter", "half+"]
    label_map = {
        "32nd-roll": "♬ 32nd Roll\n(80–95ms)",
        "32nd": "♬ 32nd\n(80–110ms)",
        "16th-triplet": "♪³ 16th Triplet\n(130–160ms)",
        "16th-trip": "♪³ 16th Triplet\n(130–160ms)",
        "16th": "♬ 16th Note\n(140–230ms)",
        "dotted-16th": "♬· Dotted 16th\n(230–300ms)",
        "8th-trip": "♪³ 8th Triplet\n(240–310ms)",
        "8th": "♪ 8th Note\n(300–450ms)",
        "dotted-8th": "♪· Dotted 8th\n(450–600ms)",
        "quarter": "♩ Quarter\n(550–800ms)",
        "dotted-quarter": "♩· Dotted Qtr\n(800ms+)",
        "half+": "♩— Half / Hold\n(900ms+)",
    }
    bucket_counts = {}
    bucket_colors = {
        "♬ 32nd Roll\n(80–95ms)": "#f43f5e",
        "♬ 32nd\n(80–110ms)": "#fb7185",
        "♪³ 16th Triplet\n(130–160ms)": "#eab308",
        "♬ 16th Note\n(140–230ms)": "#10b981",
        "♬· Dotted 16th\n(230–300ms)": "#14b8a6",
        "♪³ 8th Triplet\n(240–310ms)": "#2dd4bf",
        "♪ 8th Note\n(300–450ms)": "#38bdf8",
        "♪· Dotted 8th\n(450–600ms)": "#a855f7",
        "♩ Quarter\n(550–800ms)": "#ec4899",
        "♩· Dotted Qtr\n(800ms+)": "#f97316",
        "♩— Half / Hold\n(900ms+)": "#64748b",
    }
    for ev in events:
        if ev["cat"] == "NONVERBAL-FX":
            continue
        k = label_map.get(ev["note_short"], "♬ 16th Note\n(140–230ms)")
        bucket_counts[k] = bucket_counts.get(k, 0) + 1

    keys = [k for k in bucket_colors if k in bucket_counts]
    vals = [bucket_counts[k] for k in keys]
    cols = [bucket_colors[k] for k in keys]
    bars = ax_ioi.barh(keys, vals, color=cols, alpha=0.85, edgecolor="#f8fafc", linewidth=0.6)
    for b, v in zip(bars, vals):
        ax_ioi.text(v + 0.6, b.get_y() + b.get_height() / 2, f"{v} hits", va="center", fontsize=8, color="#f8fafc", fontweight="bold")
    ax_ioi.set_xlim(0, max(vals) + 8)
    ax_ioi.set_xlabel("Number of Discrete Phonetic Hits", fontsize=8.5, color="#cbd5e1")
    ax_ioi.set_title("2. Quantized Musical Note-Value Census (134 Active Hits + 13 Rests)", fontsize=10.5, fontweight="bold", color="#f8fafc", loc="left")
    ax_ioi.tick_params(labelsize=8)
    ax_ioi.grid(True, axis="x", alpha=0.15)

    # Panel 3 (Middle Right): Microtiming Groove Feel (Push / Pull vs Grid) by Instrument Role
    ax_gro = fig.add_subplot(gs[1, 1])
    ax_gro.set_facecolor("#0f172a")
    for ev in events:
        if ev["cat"] == "NONVERBAL-FX" or ev["local_bpm"] == 0:
            continue
        c = CAT_COLORS.get(ev["cat"], "#94a3b8")
        ax_gro.scatter(ev["microtiming_ms"], ev["staff_lane"], s=45, color=c, alpha=0.8, edgecolors="black", linewidths=0.4)
    ax_gro.axvline(0, color="#fde047", linestyle="--", linewidth=1.3, label="Exact Metronome Grid (0 ms)")
    ax_gro.axvspan(-45, -8, color="#38bdf8", alpha=0.08, label="Pushed / Ahead of Beat (Urgency)")
    ax_gro.axvspan(8, 45, color="#a855f7", alpha=0.08, label="Laid-Back / Behind Beat (Dilla/Neo-Soul Pocket)")
    ax_gro.set_yticks([1, 2, 3, 4, 5])
    ax_gro.set_yticklabels(["1: 808 Kick", "2: Snare/Pop", "3: Hat/Chop", "4: Brass/Hook", "5: Scratch/FX"], fontsize=8.5)
    ax_gro.set_xlim(-65, 65)
    ax_gro.set_xlabel("Microtiming Deviation from 16th Grid (ms)", fontsize=8.5, color="#cbd5e1")
    ax_gro.set_title("3. Microtiming Pocket & Groove Feel (Ahead vs. Behind the Grid)", fontsize=10.5, fontweight="bold", color="#f8fafc", loc="left")
    ax_gro.legend(loc="lower right", fontsize=7.5, framealpha=0.4)
    ax_gro.grid(True, alpha=0.15)

    # Panel 4 (Bottom Full Width): Full-Track 5-Line Vocal Percussion Staff Notation Roll
    ax_staff = fig.add_subplot(gs[2, :])
    ax_staff.set_facecolor("#090d16")
    for lane_y in [1, 2, 3, 4, 5]:
        ax_staff.axhline(lane_y, color="#475569", linewidth=1.0, alpha=0.7)
    for sec in RHYTHM_SECTIONS:
        for bar_num, bs, be, tsig, bpm, bdesc in sec["bars"]:
            ax_staff.axvline(bs, color="#fde047", linewidth=1.4, alpha=0.85)
            ax_staff.text(bs + 0.08, 5.55, f"M.{bar_num} ({tsig})", fontsize=7.5, color="#fde047", fontweight="bold")
            # Draw quarter-note beat lines inside each bar
            if bpm > 0:
                q = 60.0 / bpm
                t_b = bs + q
                while t_b < be - 0.05:
                    ax_staff.axvline(t_b, color="#334155", linestyle=":", linewidth=0.7, alpha=0.6)
                    t_b += q

    for ev in events:
        if ev["cat"] == "NONVERBAL-FX":
            continue
        col = CAT_COLORS.get(ev["cat"], "#94a3b8")
        y_l = ev["staff_lane"]
        s = ev["start"]
        # Draw stem
        ax_staff.plot([s, s], [y_l, y_l + 0.55], color=col, linewidth=1.2, alpha=0.9)
        ax_staff.scatter([s], [y_l], s=42, color=col, edgecolors="#ffffff", linewidths=0.4, zorder=5)
        ax_staff.text(s, y_l - 0.34, ev["note_sym"], fontsize=7.5, color="#fde047", ha="center", va="top")

    ax_staff.set_xlim(0, 37.82)
    ax_staff.set_ylim(0.3, 6.0)
    ax_staff.set_yticks([1, 2, 3, 4, 5])
    ax_staff.set_yticklabels(["Kick (B.D.)", "Snare/Rim", "Hi-Hat/Chop", "Horn/Vocal", "Scratch/FX"], fontsize=8.5, fontweight="bold")
    ax_staff.set_xlabel("Time (seconds) with Measure Barlines (Yellow) & Quarter-Note Pulse Grid (Dotted)", fontsize=9, color="#e2e8f0")
    ax_staff.set_title("4. Full-Track 5-Line Vocal Percussion Staff Score (Measure Barlines M.1–M.15, Note Stems & Rhythmic Symbols)", fontsize=10.5, fontweight="bold", color="#f8fafc", loc="left")

    out_a = OUT_DIR / "fig_rhythm_overview.png"
    fig.savefig(out_a, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)
    shutil.copy2(out_a, ARTIFACT_DIR / out_a.name)

    # --- FIGURE B: Detailed 16-Step Drum-Machine Step Sequencer Grid for Phrase 4 Beatbox (Bars 10–13) & Phrase 3C–3D Chopper (Bars 8–9) ---
    fig2 = plt.figure(figsize=(16, 9.8), dpi=180)
    fig2.patch.set_facecolor("#070b14")
    gs2 = GridSpec(6, 1, height_ratios=[1, 1, 1, 1, 1, 1], hspace=0.38, left=0.14, right=0.98, top=0.90, bottom=0.06)
    fig2.suptitle(
        "Musical Step-Sequencer & Drum-Notation Grid (16th-Note Subdivision Columns: 1 e & a | 2 e & a | 3 e & a | 4 e & a)",
        fontsize=13.5, fontweight="bold", color="#f8fafc", x=0.14, ha="left", y=0.965
    )
    fig2.text(
        0.14, 0.928,
        "Exact Alignment of Phonetic Syllables & Narrow IPA onto Standard 4/4 Musical Subdivisions Across the 6 Signature Rhythmic Bars",
        fontsize=9.5, color="#94a3b8", ha="left"
    )

    featured_bars = [
        (1, 0.26, 2.38, 106.2, "Bar 1 (0:00.26–0:02.38) — Phrase 1 Syncopated Plosive-Brush Pocket"),
        (8, 18.47, 20.54, 116.0, "Bar 8 (0:18.47–0:20.54) — 32nd-Note Plosive Roll & 'ski-bi-di-BAH!' Triplet"),
        (9, 20.54, 22.75, 131.0, "Bar 9 (0:20.54–0:22.75) — 16th-Note Double-Tongued Lateral-Plosive Chopper"),
        (10, 22.92, 25.55, 87.0, "Bar 10 (0:22.92–0:25.55) — Beatbox Bar 1: Air Riser + 808 Kicks + 'ship it DOWN!'"),
        (12, 28.57, 31.12, 85.4, "Bar 12 (0:28.57–0:31.12) — Beatbox Bar 3: 'Boom - ts - boom - buh - boom - rrr-right around!'"),
        (13, 31.38, 34.10, 85.1, "Bar 13 (0:31.38–0:34.10) — Beatbox Bar 4: 'Boom - ts - boom - buh - boom - Hhh-RA-hh-RA!'"),
    ]
    step_labels = ["1", "e", "&", "a", "2", "e", "&", "a", "3", "e", "&", "a", "4", "e", "&", "a"]

    for row_idx, (bnum, bs, be, bpm, btitle) in enumerate(featured_bars):
        ax = fig2.add_subplot(gs2[row_idx])
        ax.set_facecolor("#0f172a")
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_ylabel(f"Bar {bnum}\n({bpm:.0f} BPM)", fontsize=8.5, fontweight="bold", color="#fde047", rotation=0, labelpad=38, va="center")
        ax.set_title(btitle, fontsize=9.5, fontweight="bold", color="#f8fafc", loc="left", pad=3)

        # Draw 16 step boxes
        for st in range(16):
            is_down = (st % 4 == 0)
            bg_c = "#1e293b" if is_down else "#0f172a"
            edge_c = "#475569" if is_down else "#1e293b"
            rect = patches.Rectangle((st, 0.04), 0.98, 0.92, facecolor=bg_c, edgecolor=edge_c, linewidth=0.8)
            ax.add_patch(rect)
            ax.text(st + 0.49, 0.88, step_labels[st], ha="center", va="top", fontsize=7.5, fontweight="bold", color="#fde047" if is_down else "#64748b")

        bar_evs = [ev for ev in events if ev["start"] >= bs - 0.02 and ev["start"] < be - 0.02 and ev["cat"] != "NONVERBAL-FX"]
        dur_bar = be - bs
        for idx_e, ev in enumerate(bar_evs):
            rel_step = ((ev["start"] - bs) / dur_bar) * 16.0
            rel_w = max(0.45, ((ev["end"] - ev["start"]) / dur_bar) * 16.0)
            col = CAT_COLORS.get(ev["cat"], "#38bdf8")
            y0 = 0.08 if idx_e % 2 == 0 else 0.22
            h0 = 0.62
            p = patches.FancyBboxPatch(
                (rel_step, y0), min(rel_w, 16.0 - rel_step - 0.05), h0,
                boxstyle="round,pad=0.02,rounding_size=0.06",
                facecolor=col, edgecolor="#ffffff", linewidth=0.9, alpha=0.38
            )
            ax.add_patch(p)
            tx = min(15.6, rel_step + min(rel_w, 1.4) / 2)
            ax.text(
                tx, y0 + h0 / 2,
                f"{ev['note_sym']} {ev['syl']}\n[{ev['ipa']}]",
                ha="center", va="center", fontsize=7.6, fontweight="bold", color="#ffffff", clip_on=True
            )
        ax.set_xticks([i + 0.5 for i in range(16)])
        if row_idx == len(featured_bars) - 1:
            ax.set_xticklabels(["1", "1e", "1&", "1a", "2", "2e", "2&", "2a", "3", "3e", "3&", "3a", "4", "4e", "4&", "4a"], fontsize=8, color="#cbd5e1")
        else:
            ax.tick_params(labelbottom=False)

    out_b = OUT_DIR / "fig_rhythm_sequencer_grid.png"
    fig2.savefig(out_b, dpi=180, facecolor=fig2.get_facecolor())
    plt.close(fig2)
    shutil.copy2(out_b, ARTIFACT_DIR / out_b.name)
    return out_a, out_b


def plot_zoom_strip_with_rhythm(y_full: np.ndarray, sr: int, z_id: str, title: str, s: float, e: float, ev_list: list[dict]) -> Path:
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
    fig = plt.figure(figsize=(16, 10.4), dpi=180)
    fig.patch.set_facecolor("#070b14")

    # 7 Synchronized Tiers: Waveform, Spectrogram, Musical Rhythm & Beat Grid, English Syllable, Narrow IPA, Category, Metadata
    gs = GridSpec(
        7, 1,
        height_ratios=[1.05, 2.15, 0.88, 0.68, 0.68, 0.72, 0.78],
        hspace=0.07,
        left=0.075, right=0.985, top=0.91, bottom=0.055
    )

    local_bpms = [ev["local_bpm"] for ev in ev_list if ev["local_bpm"] > 0]
    avg_bpm = np.median(local_bpms) if local_bpms else 96.0
    fig.suptitle(title, fontsize=13.5, fontweight="bold", color="#f8fafc", x=0.075, ha="left", y=0.968)
    sub_str = (
        f"Window: {s:.2f}s – {e:.2f}s ({dur:.2f}s) | Local Tempo: ~{avg_bpm:.0f} BPM | "
        f"{len(ev_list)} Events with Synchronized Musical Rhythm Notation, Narrow IPA & Formant Tracks"
    )
    fig.text(0.075, 0.933, sub_str, fontsize=9.3, color="#94a3b8", ha="left")

    # 1. Waveform + Attack Envelope + Beat Pulse Lines
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
    ax_spec.scatter(ft, f1, s=14, color="#22d3ee", edgecolors="black", linewidths=0.3, label="F1 (Jaw)", zorder=5)
    ax_spec.scatter(ft, f2, s=14, color="#a3e635", edgecolors="black", linewidths=0.3, label="F2 (Tongue)", zorder=5)
    ax_spec.scatter(ft, f3, s=12, color="#f472b6", edgecolors="black", linewidths=0.3, label="F3 (Pharynx/Lip)", zorder=5)
    if len(f0_t):
        ax_spec.plot(f0_t, f0, color="#fde047", linewidth=2.0, label="F0 (Pitch)", zorder=6)
    for ev in ev_list:
        ax_spec.axvline(ev["start"], color="#ffffff", linestyle=":", linewidth=0.65, alpha=0.45)
    ax_spec.set_yscale("log")
    ax_spec.set_ylim(60, 8000)
    ax_spec.set_yticks([100, 250, 500, 1000, 2000, 4000, 8000])
    ax_spec.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax_spec.set_ylabel("Freq (Hz)", fontsize=8.5, color="#cbd5e1")
    ax_spec.tick_params(labelbottom=False, labelsize=8)
    ax_spec.legend(loc="upper right", fontsize=7.5, ncol=4, framealpha=0.45)

    # 3. NEW Tier: Musical Rhythm Notation, Beat Subdivision & Drum Staff Lane
    ax_rhy = fig.add_subplot(gs[2], sharex=ax_wav)
    # 4. English Phonetic Syllable + Event #
    ax_syl = fig.add_subplot(gs[3], sharex=ax_wav)
    # 5. Narrow IPA
    ax_ipa = fig.add_subplot(gs[4], sharex=ax_wav)
    # 6. Category & Articulation
    ax_cat = fig.add_subplot(gs[5], sharex=ax_wav)
    # 7. Bracketed Acoustic + Rhythmic Metadata
    ax_meta = fig.add_subplot(gs[6], sharex=ax_wav)

    tier_defs = [
        (ax_rhy, "Musical\nRhythm", "#facc15"),
        (ax_syl, "English\nSyllable", "#f8fafc"),
        (ax_ipa, "Narrow\nIPA", "#38bdf8"),
        (ax_cat, "Category &\nArticulation", "#a3e635"),
        (ax_meta, "Bracketed\nMetadata", "#fde047"),
    ]
    for ax, lbl, lcol in tier_defs:
        ax.set_facecolor("#0f172a")
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_ylabel(lbl, fontsize=8, fontweight="bold", color=lcol, rotation=0, labelpad=34, va="center")
        if ax is not ax_meta:
            ax.tick_params(labelbottom=False)
        else:
            ax.set_xlabel("Time (seconds in IMG_3268.mp3)", fontsize=9, color="#e2e8f0")
            ax.tick_params(labelsize=8.5, colors="#cbd5e1")

    # Draw subtle staff lines inside ax_rhy
    for sy in [0.22, 0.50, 0.78]:
        ax_rhy.axhline(sy, color="#334155", linewidth=0.6, alpha=0.6)

    for idx, ev in enumerate(ev_list):
        ts, te = ev["start"], ev["end"]
        w = max(0.01, te - ts)
        mid = 0.5 * (ts + te)
        col = CAT_COLORS.get(ev["cat"], "#64748b")
        y_stagger = 0.66 if (idx % 2 == 0) else 0.34

        rhy_lbl = f"{ev['note_sym']} {ev['note_short']}\n{ev['grid_pos']}"
        f_str = f"F1:{ev['f1'] or '-'} F2:{ev['f2'] or '-'}"
        meta_lbl = f"[IOI:{ev['ioi_ms']}ms | {ev['pk_db']}dB\n{f_str}]"
        cat_lbl = f"{ev['cat']}\n{ev['art'].split('+')[0]}"

        rows = [
            (ax_rhy, rhy_lbl, 7.6, "bold", "#fef08a", w < 0.14),
            (ax_syl, f"#{ev['idx']:03d} {ev['syl']}", 8.5, "bold", "#ffffff", w < 0.14),
            (ax_ipa, f"[{ev['ipa']}]", 8.3, "normal", "#e0f2fe", w < 0.14),
            (ax_cat, cat_lbl, 6.7, "bold", "#f1f5f9", False),
            (ax_meta, meta_lbl, 6.5, "normal", "#fef08a", False),
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


def main():
    events = json.loads((OUT_DIR / "micro_events_138.json").read_text())
    events = enrich_events_with_rhythm(events)
    (OUT_DIR / "micro_events_138.json").write_text(json.dumps(events, indent=2, ensure_ascii=False))
    print(f"Enriched {len(events)} events with musical rhythm notation, bar/grid positions, IOI, and microtiming.")

    y_full, sr = librosa.load(str(MP3_PATH), sr=22050, mono=True)
    out_a, out_b = plot_rhythm_overview(events, y_full, sr)
    print(f"Saved rhythm overview figures: {out_a.name}, {out_b.name}")

    zoom_figs = []
    for z_id, title, zs, ze in ZOOM_WINDOWS:
        ev_sub = [ev for ev in events if ev["start"] >= zs - 0.01 and ev["end"] <= ze + 0.02]
        print(f"Re-rendering {z_id} with 7-tier musical rhythm lane ({len(ev_sub)} events)...")
        fp = plot_zoom_strip_with_rhythm(y_full, sr, z_id, title, zs, ze, ev_sub)
        zoom_figs.append((z_id, title, zs, ze, fp, ev_sub))

    # Update HTML interactive atlas to include the Rhythm Overview & Step Sequencer Grid + rhythm badges on every chip
    mp3_b64 = base64.b64encode(MP3_PATH.read_bytes()).decode("ascii")
    dash_b64 = base64.b64encode((OUT_DIR / "fig0_phonetic_acoustic_space.png").read_bytes()).decode("ascii")
    rhy_ov_b64 = base64.b64encode(out_a.read_bytes()).decode("ascii")
    rhy_seq_b64 = base64.b64encode(out_b.read_bytes()).decode("ascii")

    sections_html = []
    for z_id, title, zs, ze, fp, ev_sub in zoom_figs:
        b64 = base64.b64encode(fp.read_bytes()).decode("ascii")
        chips = []
        stream_lines = []
        for ev in ev_sub:
            col = CAT_COLORS.get(ev["cat"], "#64748b")
            chips.append(
                f'<button class="syl-chip" data-start="{ev["start"]:.2f}" data-end="{ev["end"]:.2f}" '
                f'style="border-color:{col}; background:{col}22;" onclick="playSlice({ev["start"]:.2f}, {ev["end"]:.2f})">'
                f'<span class="syl-idx">#{ev["idx"]:03d} | M.{ev["bar_num"]} {ev["grid_pos"]}</span>'
                f'<span class="syl-en">{ev["note_sym"]} {ev["syl"]}</span>'
                f'<span class="syl-ipa">[{ev["ipa"]}]</span>'
                f'<span class="syl-fn" style="color:{col}">{ev["note_short"]} ({ev["ioi_ms"]}ms)</span>'
                f'<span class="syl-meta">{ev["cat"]} | {ev["pk_db"]}dB</span>'
                f'</button>'
            )
            stream_lines.append(
                f'<div class="stream-item" onclick="playSlice({ev["start"]:.2f}, {ev["end"]:.2f})">'
                f'<code class="meta-bracket" style="color:{col}">{ev["bracket"]}</code> '
                f'<strong class="stream-syl">{ev["note_sym"]} {ev["syl"]}</strong>'
                f'</div>'
            )
        sections_html.append(f"""
        <section class="window-card" id="{z_id}">
          <div class="window-header">
            <div>
              <h2>{title}</h2>
              <p class="subtitle">{len(ev_sub)} discrete auditory events with synchronized musical rhythm notation | Click any chip or line to audition</p>
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
<title>IMG_3268.mp3 — Complete 147-Event Phonetic, Acoustic &amp; Musical Rhythm Atlas</title>
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
  .live-syl {{ font-size: 22px; font-weight: 800; color: #38bdf8; min-width: 130px; }}
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
    border-radius: 8px; border: 1.5px solid; color: var(--text); cursor: pointer; min-width: 105px;
  }}
  .syl-chip.active, .syl-chip:hover {{ box-shadow: 0 0 0 2px #fff; transform: translateY(-1px); }}
  .syl-idx {{ font-size: 9.5px; color: #cbd5e1; font-family: ui-monospace, monospace; }}
  .syl-en {{ font-size: 14px; font-weight: 800; color: #fff; margin-top: 1px; }}
  .syl-ipa {{ font-size: 12px; color: #bae6fd; font-family: ui-monospace, monospace; }}
  .syl-fn {{ font-size: 10px; font-weight: 700; margin-top: 2px; }}
  .syl-meta {{ font-size: 9px; color: #94a3b8; font-family: ui-monospace, monospace; margin-top: 1px; }}
  .stream-box {{
    margin-top: 14px; background: #090d16; border: 1px solid #1e293b; border-radius: 8px; padding: 12px 14px;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11.5px; line-height: 1.75;
  }}
  .stream-item {{ cursor: pointer; padding: 2px 4px; border-radius: 4px; }}
  .stream-item:hover {{ background: #1e293b; }}
  .stream-syl {{ font-size: 14px; color: #ffffff; background: #1e293b; padding: 1px 6px; border-radius: 4px; }}
</style>
</head>
<body>
<header>
  <h1>IMG_3268.mp3 — Complete 147-Event Phonetic, Formant &amp; Musical Rhythm Notation Atlas</h1>
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
  <h2>Musical Rhythm Architecture, Tempo Curve, Note-Value Census &amp; 16-Step Sequencer Grid</h2>
  <div class="fig-wrap"><img src="data:image/png;base64,{rhy_ov_b64}" /></div>
  <div class="fig-wrap" style="margin-top:14px;"><img src="data:image/png;base64,{rhy_seq_b64}" /></div>
  <div class="fig-wrap" style="margin-top:14px;"><img src="data:image/png;base64,{dash_b64}" /></div>
</section>
{''.join(sections_html)}
<script>
const EVENTS = {json.dumps(events)};
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
  document.getElementById('roSyl').textContent = hit ? ('#' + String(hit.idx).padStart(3,'0') + ' ' + hit.note_sym + ' ' + hit.syl) : '—';
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
    print("Updated IMG_3268_phonetic_report.html with full musical rhythm notation.")


if __name__ == "__main__":
    main()
