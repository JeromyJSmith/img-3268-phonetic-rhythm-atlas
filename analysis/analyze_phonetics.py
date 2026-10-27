import json
from pathlib import Path
import numpy as np
import librosa
import soundfile as sf
from scipy.signal import lfilter
from earshot import api

WORKSPACE = Path("/Volumes/2TB/moviesfolder/MOVIES_FOLDER/studpid Stuff")
MP3_PATH = str(WORKSPACE / "IMG_3268.mp3")
MP4_PATH = str(WORKSPACE / "IMG_3268.mp4")
OUT_DIR = WORKSPACE / "analysis"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def estimate_formants_lpc(y_frame: np.ndarray, sr: int, order: int = 14) -> list[float]:
    if len(y_frame) < 256 or np.max(np.abs(y_frame)) < 1e-4:
        return []
    # Pre-emphasis
    y_pre = lfilter([1.0, -0.97], [1.0], y_frame)
    y_win = y_pre * np.hamming(len(y_pre))
    try:
        a = librosa.lpc(y_win, order=order)
    except Exception:
        return []
    roots = np.roots(a)
    roots = roots[np.imag(roots) >= 0]
    angs = np.arctan2(np.imag(roots), np.real(roots))
    freqs = angs * (sr / (2.0 * np.pi))
    bws = -0.5 * (sr / (2.0 * np.pi)) * np.log(np.abs(roots) + 1e-12)
    formants = [
        float(f)
        for f, bw in sorted(zip(freqs, bws))
        if 180.0 < f < 4500.0 and bw < 600.0
    ]
    return formants[:3]


def main() -> None:
    print("Running earshot measure, describe, realness, timeline, sheet...")
    m = api.measure(MP3_PATH)
    d = api.describe(MP3_PATH)
    r = api.realness(MP3_PATH)
    tl = api.timeline(MP3_PATH, video=MP4_PATH, detail="high")
    sh = api.sheet(
        MP3_PATH,
        str(OUT_DIR / "IMG_3268_sheet.png"),
        video=MP4_PATH,
        detail="high",
    )

    # Describe key windows with earshot
    phrases = [
        ("1_plosive_fricative_scat_A", 0.00, 4.55),
        ("2a_bilabial_nasal_pickup_mmm", 4.75, 5.55),
        ("2b_velar_bilabial_glottal_scat_B", 6.05, 11.65),
        ("3a_brass_diphthong_stabs_bow", 12.50, 15.50),
        ("3b_call_response_falsetto_when", 15.50, 19.75),
        ("3c_liquid_plosive_16th_roll", 19.75, 22.75),
        ("4a_fwoo_subkick_ship_it_down", 22.90, 25.30),
        ("4b_boosh_boom_take_it_down", 25.30, 28.00),
        ("4c_boom_t_boom_right_around", 28.50, 31.00),
        ("4d_boom_t_boom_uvular_scratch", 31.10, 33.80),
        ("5a_throat_grunt_pre_outro", 34.70, 35.50),
        ("5b_outro_tag_da_rip_it_now", 36.45, 37.35),
    ]

    phrase_reports = []
    y, sr = librosa.load(MP3_PATH, sr=16000, mono=True)

    for name, s, e in phrases:
        desc = api.describe(MP3_PATH, start=s, end=e)
        seg = y[int(s * sr): int(e * sr)]
        # Compute frame-wise formants on voiced/active frames
        hop = int(0.015 * sr)
        win = int(0.030 * sr)
        f1s, f2s, f3s = [], [], []
        rms = librosa.feature.rms(y=seg, frame_length=win, hop_length=hop)[0]
        cent = librosa.feature.spectral_centroid(y=seg, sr=sr, n_fft=win, hop_length=hop)[0]
        zcr = librosa.feature.zero_crossing_rate(y=seg, frame_length=win, hop_length=hop)[0]
        f0, _, _ = librosa.pyin(seg, fmin=60.0, fmax=500.0, sr=sr, hop_length=hop)

        thr = np.percentile(rms, 55) if len(rms) > 0 else 0
        for i in range(0, len(seg) - win, hop):
            frame = seg[i: i + win]
            if np.sqrt(np.mean(frame ** 2)) >= thr:
                fms = estimate_formants_lpc(frame, sr=sr, order=16)
                if len(fms) >= 1:
                    f1s.append(fms[0])
                if len(fms) >= 2:
                    f2s.append(fms[1])
                if len(fms) >= 3:
                    f3s.append(fms[2])

        valid_f0 = f0[~np.isnan(f0)] if f0 is not None else np.array([])
        phrase_reports.append({
            "name": name,
            "start": s,
            "end": e,
            "earshot_summary": desc.get("summary"),
            "top_tags": desc.get("tags"),
            "audioset": desc.get("audioset"),
            "attack_ms": desc.get("attack_ms"),
            "decay_ms": desc.get("decay_ms"),
            "peak_dbfs": desc.get("peak_dbfs"),
            "brightness_hz": desc.get("brightness_hz"),
            "f0_median_hz": float(np.median(valid_f0)) if len(valid_f0) else None,
            "f0_iqr_hz": [float(np.percentile(valid_f0, 25)), float(np.percentile(valid_f0, 75))] if len(valid_f0) else None,
            "F1_median_hz": float(np.median(f1s)) if f1s else None,
            "F2_median_hz": float(np.median(f2s)) if f2s else None,
            "F3_median_hz": float(np.median(f3s)) if f3s else None,
            "centroid_median_hz": float(np.median(cent)) if len(cent) else None,
            "zcr_median": float(np.median(zcr)) if len(zcr) else None,
        })

    out_data = {
        "measure": m,
        "describe": d,
        "realness": r,
        "timeline": tl,
        "phrases": phrase_reports,
    }
    out_file = OUT_DIR / "earshot_phonetic_analysis.json"
    out_file.write_text(json.dumps(out_data, indent=2, default=str))
    print("=== MEASURE ===")
    print(m.get("summary"))
    print("=== DESCRIBE ===")
    print(d.get("summary"))
    print("=== REALNESS ===")
    print(r.get("summary"))
    print("=== TIMELINE ===")
    print(tl.get("summary"))
    print("=== PHRASES ===")
    for p in phrase_reports:
        print(
            f"[{p['start']:.2f}-{p['end']:.2f}s] {p['name']}: "
            f"F0={p['f0_median_hz']}Hz, F1={p['F1_median_hz']}Hz, F2={p['F2_median_hz']}Hz, F3={p['F3_median_hz']}Hz | "
            f"{p['earshot_summary']}"
        )


if __name__ == "__main__":
    main()
