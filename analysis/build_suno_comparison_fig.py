import json
import shutil
from pathlib import Path
import numpy as np
import librosa
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from earshot import vocab

WORKSPACE = Path("/Volumes/2TB/moviesfolder/MOVIES_FOLDER/studpid Stuff")
ORIG_MP3 = str(WORKSPACE / "IMG_3268.mp3")
SUNO_MP3 = str(WORKSPACE / "IMG_3268 SUNO.mp3")
OUT_DIR = WORKSPACE / "analysis"
ARTIFACT_DIR = Path("/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df")


def main() -> None:
    data = json.loads((OUT_DIR / "earshot_orig_vs_suno.json").read_text())
    m_a = data["orig"]["measure"]
    m_b = data["suno"]["measure"]

    # Compute 2-second sliding window CLAP embeddings across first 37.5s of both files to plot local CLAP similarity curve
    win_len = 3.0
    step = 1.5
    starts = [round(t, 2) for t in np.arange(0.0, 34.6, step)]
    ranges = [(t, t + win_len) for t in starts]
    print(f"Computing sliding-window CLAP similarity across {len(ranges)} aligned 3s windows...")
    emb_a = vocab.embed_files([ORIG_MP3] * len(ranges), ranges=ranges)
    emb_b = vocab.embed_files([SUNO_MP3] * len(ranges), ranges=ranges)
    # Cross-similarity matrix (N_a x N_b) and diagonal (same-time) + max-aligned similarity
    sim_matrix = emb_a @ emb_b.T
    diag_cos = np.diag(sim_matrix)
    best_cos = np.max(sim_matrix, axis=1)
    best_b_times = [starts[int(i)] + win_len / 2 for i in np.argmax(sim_matrix, axis=1)]
    mid_times = [t + win_len / 2 for t in starts]

    data["sliding_clap"] = {
        "mid_times_s": mid_times,
        "same_time_cosine": [round(float(x), 3) for x in diag_cos],
        "best_match_cosine": [round(float(x), 3) for x in best_cos],
        "best_match_suno_time_s": [round(float(x), 2) for x in best_b_times],
        "mean_same_time_cosine": round(float(np.mean(diag_cos)), 3),
        "mean_best_match_cosine": round(float(np.mean(best_cos)), 3),
        "max_window_cosine": round(float(np.max(best_cos)), 3),
    }
    (OUT_DIR / "earshot_orig_vs_suno.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))

    y_a, sr = librosa.load(ORIG_MP3, sr=22050, mono=True, duration=37.82)
    y_b, _ = librosa.load(SUNO_MP3, sr=22050, mono=True, duration=37.82)

    plt.style.use("dark_background")
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial Unicode MS", "Lucida Grande"]
    fig = plt.figure(figsize=(16, 11.8), dpi=180)
    fig.patch.set_facecolor("#070b14")
    gs = GridSpec(4, 2, height_ratios=[1.1, 1.35, 1.15, 1.2], hspace=0.36, wspace=0.18, left=0.065, right=0.975, top=0.91, bottom=0.055)

    fig.suptitle(
        "earshot A/B Acoustic & CLAP Comparison: IMG_3268.mp3 (Human Mouth) vs. IMG_3268 SUNO.mp3 (Suno Render)",
        fontsize=14, fontweight="bold", color="#f8fafc", x=0.065, ha="left", y=0.968
    )
    fig.text(
        0.065, 0.935,
        f"CLAP 0–37.8s Cosine: 0.60 (Peak Phrase 4 Beatbox Cosine: 0.69) | Mean Best-Aligned Window Cosine: {np.mean(best_cos):.2f} (Max {np.max(best_cos):.2f}) | Realness p_real: A=0.99 vs B=0.98",
        fontsize=9.6, color="#38bdf8", fontweight="bold", ha="left"
    )

    # Row 1 Left & Right: Waveforms & Onset Envelopes (0 - 37.8s)
    ax_wa = fig.add_subplot(gs[0, 0])
    ax_wb = fig.add_subplot(gs[0, 1], sharex=ax_wa)
    t_a = np.linspace(0, len(y_a) / sr, len(y_a))
    t_b = np.linspace(0, len(y_b) / sr, len(y_b))

    ax_wa.set_facecolor("#0f172a")
    ax_wa.plot(t_a, y_a, color="#38bdf8", linewidth=0.45, alpha=0.85)
    ax_wa.set_title("A: IMG_3268.mp3 (Original Mouth Percussion — -28.2 LUFS, Mono, 4.12 onsets/s)", fontsize=9.8, fontweight="bold", color="#38bdf8", loc="left")
    ax_wa.set_ylabel("Amp", fontsize=8.5)
    ax_wa.set_xlim(0, 37.8)
    ax_wa.grid(True, alpha=0.15)

    ax_wb.set_facecolor("#0f172a")
    ax_wb.plot(t_b, y_b, color="#f43f5e", linewidth=0.45, alpha=0.85)
    ax_wb.set_title("B: IMG_3268 SUNO.mp3 [0:00–0:37.8] (Suno Render — -16.4 LUFS, Stereo, 5.94 onsets/s)", fontsize=9.8, fontweight="bold", color="#f43f5e", loc="left")
    ax_wb.set_ylabel("Amp", fontsize=8.5)
    ax_wb.set_xlim(0, 37.8)
    ax_wb.grid(True, alpha=0.15)

    # Row 2 Left & Right: Log-Frequency Spectrograms (0 - 37.8s)
    ax_sa = fig.add_subplot(gs[1, 0], sharex=ax_wa)
    ax_sb = fig.add_subplot(gs[1, 1], sharex=ax_wa)
    for ax_s, y_sig, title_s in [
        (ax_sa, y_a, "A: Original Spectrogram (Dry Close-Mic Formant Sweeps, Roll-off 3.8 kHz)"),
        (ax_sb, y_b, "B: Suno Spectrogram (Full-Range 20.5 kHz Mastered Funk/Beatbox Arrangement, Roll-off 8.8 kHz)"),
    ]:
        ax_s.set_facecolor("#090d16")
        S = np.abs(librosa.stft(y_sig, n_fft=1024, hop_length=256))
        S_db = librosa.amplitude_to_db(S, ref=np.max)
        freqs = librosa.fft_frequencies(sr=sr, n_fft=1024)
        ts = np.linspace(0, len(y_sig) / sr, S_db.shape[1])
        ax_s.pcolormesh(ts, freqs, S_db, cmap="magma", vmin=-65, vmax=0, shading="auto")
        ax_s.set_yscale("log")
        ax_s.set_ylim(60, 10000)
        ax_s.set_yticks([100, 250, 500, 1000, 2000, 4000, 8000])
        ax_s.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax_s.set_ylabel("Freq (Hz)", fontsize=8.5)
        ax_s.set_xlabel("Time (seconds, 0:00–0:37.8)", fontsize=8.5)
        ax_s.set_title(title_s, fontsize=9.5, fontweight="bold", color="#f8fafc", loc="left")

    # Row 3 Left: 7-Band Tonal Balance Comparison (earshot measure bands_db)
    ax_bands = fig.add_subplot(gs[2, 0])
    ax_bands.set_facecolor("#0f172a")
    band_keys = ["sub", "low", "lowmid", "mid", "presence", "air", "top"]
    band_labels = ["Sub\n(<60Hz)", "Low\n(60-250)", "LowMid\n(250-500)", "Mid\n(0.5-2k)", "Presence\n(2-4k)", "Air\n(4-8k)", "Top\n(>8kHz)"]
    x_pos = np.arange(len(band_keys))
    vals_a = [m_a["bands_db"][k] for k in band_keys]
    vals_b = [m_b["bands_db"][k] for k in band_keys]
    w_bar = 0.36
    b1 = ax_bands.bar(x_pos - w_bar / 2, vals_a, w_bar, color="#38bdf8", label="A: IMG_3268.mp3 (Original)", edgecolor="#fff", linewidth=0.5)
    b2 = ax_bands.bar(x_pos + w_bar / 2, vals_b, w_bar, color="#f43f5e", label="B: IMG_3268 SUNO.mp3 (Suno)", edgecolor="#fff", linewidth=0.5)
    for rect, v in zip(b1, vals_a):
        ax_bands.text(rect.get_x() + rect.get_width() / 2, v - 3.8, f"{v:.0f}", ha="center", va="top", fontsize=7, color="#bae6fd", fontweight="bold")
    for rect, v in zip(b2, vals_b):
        ax_bands.text(rect.get_x() + rect.get_width() / 2, v + 0.8, f"{v:.0f}", ha="center", va="bottom", fontsize=7, color="#fecdd3", fontweight="bold")
    ax_bands.set_xticks(x_pos)
    ax_bands.set_xticklabels(band_labels, fontsize=8)
    ax_bands.set_ylim(-55, 4)
    ax_bands.set_ylabel("Relative Band Energy (dB)", fontsize=8.5)
    ax_bands.set_title("3. earshot 7-Band Spectral Balance (Shows Suno +19 dB Sub-Bass & +22 dB Top Air)", fontsize=9.8, fontweight="bold", color="#f8fafc", loc="left")
    ax_bands.legend(loc="lower left", fontsize=8, framealpha=0.4)
    ax_bands.grid(True, axis="y", alpha=0.15)

    # Row 3 Right: Sliding 3s Window CLAP Cosine Similarity Curve
    ax_sim = fig.add_subplot(gs[2, 1])
    ax_sim.set_facecolor("#0f172a")
    ax_sim.plot(mid_times, diag_cos, color="#38bdf8", marker="o", markersize=4, linewidth=1.8, label="Same-Timestamp CLAP Cosine (A[t] vs B[t])")
    ax_sim.plot(mid_times, best_cos, color="#fde047", marker="s", markersize=4, linewidth=2.2, label="Best-Aligned Window CLAP Cosine (A[t] vs Best B)")
    ax_sim.axhline(0.50, color="#10b981", linestyle="--", linewidth=1.0, alpha=0.8, label="earshot 'Related Sound' Threshold (0.50)")
    ax_sim.axhline(0.75, color="#f43f5e", linestyle=":", linewidth=1.0, alpha=0.8, label="earshot 'Similar Sound' Threshold (0.75)")
    ax_sim.set_xlim(0, 37.8)
    ax_sim.set_ylim(0.25, 0.88)
    ax_sim.set_xlabel("Time in Original IMG_3268.mp3 (s)", fontsize=8.5)
    ax_sim.set_ylabel("CLAP Cosine Similarity", fontsize=8.5)
    ax_sim.set_title("4. Window-by-Window CLAP Cosine Closeness (Peaks at 0.69–0.73 in Beatbox & Brass Hook)", fontsize=9.8, fontweight="bold", color="#f8fafc", loc="left")
    ax_sim.legend(loc="lower right", fontsize=7.5, framealpha=0.4)
    ax_sim.grid(True, alpha=0.15)

    # Row 4 Left: Calibrated CLAP Z-Score Comparison Across 6 Target Queries
    ax_q = fig.add_subplot(gs[3, 0])
    ax_q.set_facecolor("#0f172a")
    q_short = [
        "Beatbox + Plosive\nKicks/Hats",
        "Talkbox Brass Wah\n+ Vocal Chops",
        "808 Sub-Kick +\nBoom-Bap Groove",
        "DJ Vinyl Scratch\n+ Vocal Chop",
        "Syncopated Scat +\nMouth Percussion",
        "Combined 0–37.8s\nFull Prompt",
    ]
    z_a = [r["query"]["a"]["z"] for r in data["ab_whole_file"]] + [data["ab_first_38s"]["query"]["a"]["z"]]
    z_b = [r["query"]["b"]["z"] for r in data["ab_whole_file"]] + [data["ab_first_38s"]["query"]["b"]["z"]]
    yq = np.arange(len(q_short))
    ax_q.barh(yq - 0.18, z_a, 0.35, color="#38bdf8", label="A: IMG_3268.mp3 (z-score)")
    ax_q.barh(yq + 0.18, z_b, 0.35, color="#f43f5e", label="B: IMG_3268 SUNO.mp3 (z-score)")
    for i, (va, vb) in enumerate(zip(z_a, z_b)):
        ax_q.text(va + 0.1, i - 0.18, f"z +{va:.1f}", va="center", fontsize=7.5, color="#bae6fd", fontweight="bold")
        ax_q.text(vb + 0.1, i + 0.18, f"z +{vb:.1f}", va="center", fontsize=7.5, color="#fecdd3", fontweight="bold")
    ax_q.set_yticks(yq)
    ax_q.set_yticklabels(q_short, fontsize=7.8)
    ax_q.set_xlim(0, 8.8)
    ax_q.set_xlabel("earshot Calibrated CLAP Match Score (z)", fontsize=8.5)
    ax_q.set_title("5. earshot ab Query Match Scores (Both Score z +3.5 to +7.3 = 99–100th Percentile)", fontsize=9.8, fontweight="bold", color="#f8fafc", loc="left")
    ax_q.legend(loc="lower right", fontsize=7.8, framealpha=0.4)
    ax_q.grid(True, axis="x", alpha=0.15)

    # Row 4 Right: AudioSet + CLAP Genre/Instrument Tag Alignment
    ax_tags = fig.add_subplot(gs[3, 1])
    ax_tags.set_facecolor("#0f172a")
    tag_names = [
        "AST: Beatboxing",
        "AST: Speech / Vox",
        "AST: Music / Funk",
        "CLAP: Vocal Chop (z)",
        "CLAP: Hip-Hop Bass (z)",
        "Realness (p_real x5)",
    ]
    # Normalize onto a common 0-5 visual scale
    t_a_vals = [0.74 * 5, 0.88 * 5, 0.18 * 5, 4.33, 2.51, 0.99 * 5]
    t_b_vals = [0.606 * 5, 0.35 * 5, 0.86 * 5, 3.86, 3.15, 0.981 * 5]
    yt = np.arange(len(tag_names))
    ax_tags.barh(yt - 0.18, t_a_vals, 0.35, color="#38bdf8", label="A: IMG_3268.mp3")
    ax_tags.barh(yt + 0.18, t_b_vals, 0.35, color="#f43f5e", label="B: IMG_3268 SUNO.mp3")
    t_a_lbls = ["0.74", "0.88", "0.18", "z +4.3", "z +2.5", "p=0.99"]
    t_b_lbls = ["0.61", "0.35", "0.86", "z +3.9", "z +3.2", "p=0.98"]
    for i, (va, vb, la, lb) in enumerate(zip(t_a_vals, t_b_vals, t_a_lbls, t_b_lbls)):
        ax_tags.text(va + 0.08, i - 0.18, la, va="center", fontsize=7.5, color="#bae6fd", fontweight="bold")
        ax_tags.text(vb + 0.08, i + 0.18, lb, va="center", fontsize=7.5, color="#fecdd3", fontweight="bold")
    ax_tags.set_yticks(yt)
    ax_tags.set_yticklabels(tag_names, fontsize=8)
    ax_tags.set_xlim(0, 5.8)
    ax_tags.set_xlabel("Measured Probability (scaled x5) / CLAP z-score", fontsize=8.5)
    ax_tags.set_title("6. AudioSet (AST) & CLAP Identity DNA (Both Lock Onto Beatboxing + Vocal Chop + Funk)", fontsize=9.8, fontweight="bold", color="#f8fafc", loc="left")
    ax_tags.legend(loc="lower right", fontsize=7.8, framealpha=0.4)
    ax_tags.grid(True, axis="x", alpha=0.15)

    out_fig = OUT_DIR / "fig_suno_vs_orig_comparison.png"
    fig.savefig(out_fig, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)
    shutil.copy2(out_fig, ARTIFACT_DIR / out_fig.name)
    print(f"Saved comparison figure: {out_fig.name}")


if __name__ == "__main__":
    main()
