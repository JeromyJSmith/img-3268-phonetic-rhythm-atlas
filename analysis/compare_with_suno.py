import json
import shutil
from pathlib import Path
import numpy as np
import librosa
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.signal import lfilter
from earshot import api

WORKSPACE = Path("/Volumes/2TB/moviesfolder/MOVIES_FOLDER/studpid Stuff")
ORIG_MP3 = str(WORKSPACE / "IMG_3268.mp3")
SUNO_MP3 = str(WORKSPACE / "IMG_3268 SUNO.mp3")
OUT_DIR = WORKSPACE / "analysis"
ARTIFACT_DIR = Path("/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df")


def main() -> None:
    print("1. Running earshot measure, describe, realness, timeline, sheet on both files...")
    m_orig = api.measure(ORIG_MP3)
    m_suno = api.measure(SUNO_MP3)

    d_orig = api.describe(ORIG_MP3)
    d_suno = api.describe(SUNO_MP3)

    r_orig = api.realness(ORIG_MP3)
    r_suno = api.realness(SUNO_MP3)

    tl_orig = api.timeline(ORIG_MP3, detail="high")
    tl_suno = api.timeline(SUNO_MP3, detail="high")

    sh_suno_path = OUT_DIR / "IMG_3268_SUNO_sheet.png"
    api.sheet(SUNO_MP3, str(sh_suno_path), detail="high")
    shutil.copy2(sh_suno_path, ARTIFACT_DIR / sh_suno_path.name)

    print("2. Running earshot ab & match across vocal-percussion queries...")
    queries = [
        "rhythmic human beatboxing and vocal percussion with plosive kicks and hi-hats",
        "funky talkbox synth-brass wah stabs and rhythmic vocal chops",
        "heavy 808 sub-bass kick and boom-bap beatbox groove",
        "turntable DJ vinyl record scratch and vocal chop",
        "syncopated vocal scatting and crisp mouth percussion",
    ]
    ab_results = []
    for q in queries:
        res = api.ab(ORIG_MP3, SUNO_MP3, query=q)
        ab_results.append(res)

    # Also compare the first 37.8s of SUNO directly against the 37.8s original
    ab_first38 = api.ab(
        ORIG_MP3, SUNO_MP3,
        query="rhythmic human beatboxing, vocal chops, brass wah stabs and 808 sub-bass groove",
        a_start=0.0, a_end=37.8, b_start=0.0, b_end=37.8
    )

    # Use earshot.find on SUNO to locate the best moments matching each of the 5 signature phrases of IMG_3268.mp3
    phrase_queries = [
        ("Phrase 1: Plosive-Fricative Scat Pocket ('thuh-bitch camp brah / pant thence')", 0.26, 4.35, "crisp plosive vocal scatting and brushed hi-hat mouth percussion"),
        ("Phrase 2: Sub-Hum & Cork-Pop Groove ('Mmmm! / pink cane / ki-'in / NOW!')", 4.75, 11.72, "syncopated vocal percussion pop and neo-soul scat groove"),
        ("Phrase 3A–3B: Brass Wah Stabs & Falsetto ('You know what BOW-buh-BOW / WHEN!')", 12.50, 18.12, "punchy brass wah horn stab and high vocal chop"),
        ("Phrase 3C–3D: 32nd Drum Roll & Chopper ('thuh-buh-chuh-kuh-buh-GAH / skibidi-BAH / buh-lip-uh-gih')", 18.47, 22.75, "fast rapid double-tongue vocal chopper roll and drum fill"),
        ("Phrase 4: Heavy 808 Beatbox & DJ Scratch ('FWOO-BWAH / Boom-ts-boom / Hhh-RA-hh-RA!')", 22.92, 34.10, "heavy 808 sub-bass beatbox kick and turntable vinyl scratch"),
        ("Phrase 5: Outro Coda Tag ('Duh-rip-it-NOW!')", 36.48, 37.38, "staccato vocal cadence hit and final stop"),
    ]

    phrase_comparisons = []
    for pname, os_t, oe_t, pq in phrase_queries:
        f_suno = api.find(SUNO_MP3, pq, top=3)
        best_seg = f_suno["segments"][0] if f_suno.get("segments") else {"start": os_t, "end": oe_t, "z": 0.0}
        ss_t = float(best_seg["start"])
        se_t = float(best_seg["end"])
        # Ensure window is at least 1.0s for stable CLAP comparison
        if se_t - ss_t < 1.0:
            se_t = min(float(m_suno["duration"]), ss_t + (oe_t - os_t))
        ab_p = api.ab(
            ORIG_MP3, SUNO_MP3,
            query=pq,
            a_start=os_t, a_end=oe_t,
            b_start=ss_t, b_end=se_t,
        )
        # Also compare same-timestamp window in Suno (if within duration)
        ab_same_t = api.ab(
            ORIG_MP3, SUNO_MP3,
            query=pq,
            a_start=os_t, a_end=oe_t,
            b_start=os_t, b_end=oe_t,
        )
        phrase_comparisons.append({
            "phrase": pname,
            "query": pq,
            "orig_range": [os_t, oe_t],
            "suno_best_match_range": [round(ss_t, 2), round(se_t, 2)],
            "suno_find_top": best_seg,
            "ab_best_window": ab_p,
            "ab_same_timestamp": ab_same_t,
        })

    out_json = {
        "orig": {
            "measure": m_orig,
            "describe": d_orig,
            "realness": r_orig,
            "timeline_summary": tl_orig.get("summary"),
            "sections": tl_orig.get("sections"),
        },
        "suno": {
            "measure": m_suno,
            "describe": d_suno,
            "realness": r_suno,
            "timeline_summary": tl_suno.get("summary"),
            "sections": tl_suno.get("sections"),
        },
        "ab_whole_file": ab_results,
        "ab_first_38s": ab_first38,
        "phrase_comparisons": phrase_comparisons,
    }
    (OUT_DIR / "earshot_orig_vs_suno.json").write_text(json.dumps(out_json, indent=2, ensure_ascii=False))
    print("Saved earshot_orig_vs_suno.json successfully!")


if __name__ == "__main__":
    main()
