import base64
import json
import subprocess
from pathlib import Path
from build_ultra_zoom_report import CAT_COLORS, ZOOM_WINDOWS

WORKSPACE = Path("/Volumes/2TB/moviesfolder/MOVIES_FOLDER/studpid Stuff")
MP4_PATH = WORKSPACE / "IMG_3268.mp4"
MP3_PATH = WORKSPACE / "IMG_3268.mp3"
SUNO_MP3_PATH = WORKSPACE / "IMG_3268 SUNO.mp3"
OUT_DIR = WORKSPACE / "analysis"
ARTIFACT_DIR = Path("/Users/jero/.gemini/antigravity-cli/brain/4817f12d-36b4-4a79-bed9-d706f0fdf0df")


def fmt_vtt_time(sec: float) -> str:
    ms = int(round((sec % 1) * 1000))
    s = int(sec) % 60
    m = (int(sec) // 60) % 60
    h = int(sec) // 3600
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def fmt_ass_time(sec: float) -> str:
    cs = int(round((sec % 1) * 100))
    s = int(sec) % 60
    m = (int(sec) // 60) % 60
    h = int(sec) // 3600
    return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"


def build_webvtt(events: list[dict], zoom_windows: list) -> str:
    vtt = ["WEBVTT\n"]
    for z_id, z_title, zs, ze in zoom_windows:
        ev_sub = [e for e in events if e["start"] >= zs - 0.01 and e["end"] <= ze + 0.02]
        sec_rhy = " ".join(f"{e['note_sym']}{e['syl']}" for e in ev_sub if e["cat"] != "NONVERBAL-FX")
        for ev in ev_sub:
            t0 = fmt_vtt_time(ev["start"])
            t1 = fmt_vtt_time(ev["end"])
            line1 = f"#{ev['idx']:03d} | {ev['note_sym']} {ev['syl']}   [{ev['ipa']}]   ({ev['note_short']} @ {ev['grid_pos']})"
            line2 = f"[{ev['cat']} | {ev['art']} | {ev['pk_db']}dB | F1:{ev['f1'] or '-'}/F2:{ev['f2'] or '-'}Hz]"
            line3 = f"Section Score: {sec_rhy}"
            vtt.append(f"{t0} --> {t1}\n{line1}\n{line2}\n{line3}\n")
    return "\n".join(vtt)


def render_html_document(
    events: list[dict],
    windows_meta: list[dict],
    asset_urls: dict[str, str],
    is_portable_b64: bool,
) -> str:
    """Render the Studio Workbench HTML for either GitHub Pages (relative URLs) or Portable Single-File (Base64 Blob URLs)."""

    # Build the 14 Zoom Window cards with clean Syllable Chips + Structured Table + Collapsible Raw Brackets
    sections_html = []
    for w_idx, (z_id, title, zs, ze) in enumerate(ZOOM_WINDOWS):
        ev_sub = [ev for ev in events if ev["start"] >= zs - 0.01 and ev["end"] <= ze + 0.02]
        img_src = asset_urls[z_id]

        chips = []
        table_rows = []
        raw_lines = []
        for ev in ev_sub:
            col = CAT_COLORS.get(ev["cat"], "#64748b")
            f_str = f"{ev['f1'] or '—'} / {ev['f2'] or '—'} / {ev['f3'] or '—'}"
            f0_str = f"{ev['f0']:.0f} Hz" if ev.get("f0") else "Unvoiced"

            chips.append(
                f'<button type="button" class="syl-chip" id="chip-{ev["idx"]}" data-idx="{ev["idx"]}" '
                f'data-start="{ev["start"]:.2f}" data-end="{ev["end"]:.2f}" '
                f'style="--chip-accent:{col};" onclick="playEventByIdx({ev["idx"]})">'
                f'<div class="syl-chip-top">'
                f'<span class="syl-idx">#{ev["idx"]:03d}</span>'
                f'<span class="syl-grid">M.{ev["bar_num"]} · {ev["grid_pos"]}</span>'
                f'</div>'
                f'<div class="syl-chip-main">'
                f'<span class="syl-note">{ev["note_sym"]}</span>'
                f'<span class="syl-en">{ev["syl"]}</span>'
                f'</div>'
                f'<div class="syl-ipa">[{ev["ipa"]}]</div>'
                f'<div class="syl-chip-foot">'
                f'<span class="syl-cat-dot" style="background:{col};"></span>'
                f'<span class="syl-cat-name">{ev["cat"]}</span>'
                f'<span class="syl-db">{ev["pk_db"]}dB</span>'
                f'</div>'
                f'</button>'
            )

            table_rows.append(
                f'<tr class="ev-row" id="wrow-{ev["idx"]}" data-idx="{ev["idx"]}" onclick="playEventByIdx({ev["idx"]})">'
                f'<td class="col-id"><span class="id-pill">#{ev["idx"]:03d}</span></td>'
                f'<td class="col-time">{ev["start"]:05.2f}–{ev["end"]:05.2f}s <span class="muted-sub">({ev["dur_ms"]}ms)</span></td>'
                f'<td class="col-grid">Bar {ev["bar_num"]:02d} · <code>{ev["grid_pos"]}</code></td>'
                f'<td class="col-rhy"><span class="rhy-badge">{ev["note_sym"]} {ev["note_short"]}</span> <span class="muted-sub">IOI {ev["ioi_ms"]}ms</span></td>'
                f'<td class="col-syl"><strong>{ev["syl"]}</strong></td>'
                f'<td class="col-ipa"><code class="ipa-code">[{ev["ipa"]}]</code></td>'
                f'<td class="col-cat"><span class="cat-pill" style="--cat-col:{col};">{ev["cat"]}</span> <span class="muted-sub">{ev["art"]}</span></td>'
                f'<td class="col-ac">{ev["pk_db"]} dB · <span class="muted-sub">ATK {ev["atk_ms"]}ms</span></td>'
                f'<td class="col-fmt">{f0_str} · <span class="muted-sub">{f_str} Hz</span></td>'
                f'</tr>'
            )

            raw_lines.append(
                f'<div class="raw-bracket-item" id="line-{ev["idx"]}" onclick="playEventByIdx({ev["idx"]})">'
                f'<code style="color:{col}">{ev["bracket"]}</code> '
                f'<strong class="raw-syl">{ev["note_sym"]} {ev["syl"]}</strong>'
                f'</div>'
            )

        sections_html.append(f"""
        <article class="surface-card zoom-window-card" id="{z_id}" data-win-idx="{w_idx}">
          <header class="card-header">
            <div class="card-header-titles">
              <div class="eyebrow-row">
                <span class="window-badge">WINDOW {w_idx + 1:02d} / 14</span>
                <span class="window-Range-pill">{zs:05.2f}s – {ze:05.2f}s ({ze - zs:.2f}s span · {len(ev_sub)} events)</span>
              </div>
              <h3 class="card-title">{title}</h3>
            </div>
            <div class="card-header-actions">
              <button type="button" class="btn-secondary" onclick="openLightbox('{z_id}', '{title}')">🔍 Expand Figure</button>
              <button type="button" class="btn-primary" onclick="playSlice({zs:.2f}, {ze:.2f})">▶ Play Window ({zs:.2f}–{ze:.2f}s)</button>
            </div>
          </header>

          <div class="figure-frame" onclick="openLightbox('{z_id}', '{title}')" title="Click to inspect full-resolution figure">
            <img id="img-{z_id}" src="{img_src}" alt="{title}" loading="lazy" />
            <div class="figure-zoom-hint">🔍 Click image to open full-resolution lightbox</div>
          </div>

          <div class="section-sublabel">Interactive Syllable Pads (Click any pad to jump video &amp; audition slice)</div>
          <div class="chips-grid">
            {''.join(chips)}
          </div>

          <details class="structured-details" open>
            <summary class="details-summary">
              <span>📋 Structured Acoustic, Phonetic &amp; Musical Rhythm Breakdown ({len(ev_sub)} Events)</span>
              <span class="summary-hint">Click any row to audition</span>
            </summary>
            <div class="table-scroll">
              <table class="studio-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Timestamp (Dur)</th>
                    <th>Bar · Grid</th>
                    <th>Rhythm Note (IOI)</th>
                    <th>English</th>
                    <th>Narrow IPA</th>
                    <th>Category &amp; Articulator</th>
                    <th>Peak · Attack</th>
                    <th>F0 · Formants (F1/F2/F3)</th>
                  </tr>
                </thead>
                <tbody>
                  {''.join(table_rows)}
                </tbody>
              </table>
            </div>
          </details>

          <details class="structured-details" style="margin-top:8px;">
            <summary class="details-summary">
              <span>🧬 Raw Bracketed Metadata Stream (Copy-Ready Annotated Corpus Lines)</span>
              <span class="summary-hint">Expand to view raw `[#ID | ...]` strings</span>
            </summary>
            <div class="raw-bracket-box">
              {''.join(raw_lines)}
            </div>
          </details>
        </article>
        """)

    # Build full 147-event corpus master table rows
    master_rows = []
    for ev in events:
        col = CAT_COLORS.get(ev["cat"], "#64748b")
        f_str = f"{ev['f1'] or '—'}/{ev['f2'] or '—'}/{ev['f3'] or '—'}"
        f0_str = f"{ev['f0']:.0f}" if ev.get("f0") else "—"
        search_blob = f"{ev['idx']:03d} {ev['syl']} {ev['ipa']} {ev['cat']} {ev['art']} {ev['purpose']} {ev['note_short']} bar{ev['bar_num']}".lower()
        master_rows.append(
            f'<tr class="ev-row master-ev-row" id="mrow-{ev["idx"]}" data-idx="{ev["idx"]}" '
            f'data-cat="{ev["cat"]}" data-search="{search_blob}" onclick="playEventByIdx({ev["idx"]})">'
            f'<td><span class="id-pill">#{ev["idx"]:03d}</span></td>'
            f'<td>{ev["start"]:05.2f}–{ev["end"]:05.2f}s</td>'
            f'<td>M.{ev["bar_num"]:02d} · <code>{ev["grid_pos"]}</code> <span class="muted-sub">({ev["local_bpm"]:.0f} BPM)</span></td>'
            f'<td><span class="rhy-badge">{ev["note_sym"]} {ev["note_short"]}</span></td>'
            f'<td><strong style="color:#f8fafc; font-size:13.5px;">{ev["syl"]}</strong></td>'
            f'<td><code class="ipa-code">[{ev["ipa"]}]</code></td>'
            f'<td><span class="cat-pill" style="--cat-col:{col};">{ev["cat"]}</span></td>'
            f'<td>{ev["art"]}</td>'
            f'<td>{ev["pk_db"]} dB <span class="muted-sub">({ev["atk_ms"]}ms)</span></td>'
            f'<td>{f0_str} Hz · <span class="muted-sub">{f_str}</span></td>'
            f'<td class="muted-sub">{ev["purpose"]}</td>'
            f'</tr>'
        )

    # Window filter pills for Tab 2
    win_pills = [
        '<button type="button" class="win-filter-pill active" data-win="all" onclick="filterZoomWindow(\'all\', this)">All 14 Windows</button>'
    ]
    short_labels = [
        "Z01: Scat 1A", "Z02: 'at ALL!'", "Z03: 'Mmmm/pink'", "Z04: 'NOW!'",
        "Z05: 'BOW!'", "Z06: 'WHEN!↑'", "Z07: 'skibidi'", "Z08: Chopper",
        "Z09: 'ship it'", "Z10: 'BOOSH'", "Z11: 'Boom-ts'", "Z12: Scratch",
        "Z13: Scrape", "Z14: Coda"
    ]
    for idx, (z_id, title, zs, ze) in enumerate(ZOOM_WINDOWS):
        win_pills.append(
            f'<button type="button" class="win-filter-pill" id="wpill-{z_id}" data-win="{z_id}" '
            f'onclick="filterZoomWindow(\'{z_id}\', this)">{short_labels[idx]} <span class="pill-time">{zs:.1f}s</span></button>'
        )

    # Category filter pills for Tab 5
    cat_pills = ['<button type="button" class="win-filter-pill active" onclick="filterCorpusCat(\'ALL\', this)">All Categories (147)</button>']
    for cat_name, cat_col in CAT_COLORS.items():
        cnt = sum(1 for e in events if e["cat"] == cat_name)
        if cnt > 0:
            cat_pills.append(
                f'<button type="button" class="win-filter-pill" onclick="filterCorpusCat(\'{cat_name}\', this)">'
                f'<span class="syl-cat-dot" style="background:{cat_col};display:inline-block;margin-right:5px;"></span>'
                f'{cat_name} ({cnt})</button>'
            )

    badge_mode = (
        "100% Self-Contained Offline Bundle (Embedded Video + Dual Audio + 19 Figures)"
        if is_portable_b64
        else "Live Streaming Studio Workbench (Fast-Loading Native Media + Offline Export)"
    )

    download_menu_html = ""
    if not is_portable_b64:
        download_menu_html = """
        <div class="header-downloads">
          <a class="dl-link" href="./analysis/IMG_3268_phonetic_report.html" download>⬇ Offline Single-File HTML (34 MB)</a>
          <a class="dl-link" href="./analysis/IMG_3268_subtitled_phonetic_rhythm.mp4" download>⬇ Burned-In HUD Video (4.9 MB)</a>
          <a class="dl-link" href="./IMG_3268.mp3" download>⬇ Original MP3</a>
          <a class="dl-link" href="./IMG_3268%20SUNO.mp3" download>⬇ Suno MP3</a>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>IMG_3268 — Vocal Percussion, Narrow IPA, Musical Rhythm &amp; Suno A/B Studio Workbench</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg-canvas: #080a0f;
    --bg-surface: #0f131c;
    --bg-elevated: #161c28;
    --bg-interactive: #1c2434;
    --bg-glass: rgba(15, 19, 28, 0.88);
    --border-subtle: #1e2738;
    --border-strong: #2e3b52;
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-muted: #8b9bb4;
    --accent-amber: #f59e0b;
    --accent-orig: #38bdf8;
    --accent-suno: #f97316;
    --accent-emerald: #10b981;
    --accent-purple: #a855f7;
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
  }}

  * {{ box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; background: var(--bg-canvas); color: var(--text-primary); }}
  body {{
    margin: 0;
    padding: 0;
    background: var(--bg-canvas);
    color: var(--text-primary);
    font-family: var(--font-sans);
    font-size: 14px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
  }}

  /* Top Application Header */
  .app-topbar {{
    height: 58px;
    background: var(--bg-glass);
    backdrop-filter: blur(14px);
    border-bottom: 1px solid var(--border-subtle);
    padding: 0 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    position: sticky;
    top: 0;
    z-index: 300;
  }}
  .brand-cluster {{
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 0;
  }}
  .brand-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--accent-amber);
    box-shadow: 0 0 10px var(--accent-amber);
    flex-shrink: 0;
  }}
  .brand-title {{
    font-size: 15px;
    font-weight: 800;
    letter-spacing: -0.01em;
    color: var(--text-primary);
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .brand-badge {{
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 600;
    color: #6ee7b7;
    background: rgba(16, 185, 129, 0.14);
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 3px 9px;
    border-radius: 999px;
    white-space: nowrap;
  }}
  .header-downloads {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }}
  .dl-link {{
    font-size: 11.5px;
    font-weight: 600;
    color: var(--text-secondary);
    background: var(--bg-elevated);
    border: 1px solid var(--border-strong);
    padding: 5px 10px;
    border-radius: var(--radius-sm);
    text-decoration: none;
    transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
    white-space: nowrap;
  }}
  .dl-link:hover {{
    background: var(--bg-interactive);
    color: #fff;
    border-color: var(--accent-orig);
  }}

  /* Main Two-Column Studio Layout */
  .studio-shell {{
    max-width: 1760px;
    margin: 0 auto;
    padding: 16px 20px 64px;
    display: grid;
    grid-template-columns: 390px minmax(0, 1fr);
    gap: 22px;
    align-items: start;
  }}
  @media (max-width: 1180px) {{
    .studio-shell {{
      grid-template-columns: 1fr;
    }}
  }}

  /* Left Sticky Studio Monitor Rail */
  .monitor-rail {{
    position: sticky;
    top: 72px;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45);
    max-height: calc(100vh - 88px);
    overflow-y: auto;
  }}
  @media (max-width: 1180px) {{
    .monitor-rail {{
      position: static;
      max-height: none;
    }}
  }}

  .monitor-source-tabs {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 4px;
    background: var(--bg-canvas);
    padding: 4px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-subtle);
  }}
  .src-tab {{
    background: transparent;
    color: var(--text-muted);
    border: none;
    border-radius: 4px;
    padding: 5px 6px;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
    white-space: nowrap;
    text-align: center;
  }}
  .src-tab:hover {{ color: var(--text-primary); }}
  .src-tab.active {{
    background: var(--bg-elevated);
    color: var(--accent-orig);
    box-shadow: 0 1px 3px rgba(0,0,0,0.4);
  }}

  .video-stage-box {{
    position: relative;
    background: #000;
    border-radius: var(--radius-md);
    overflow: hidden;
    border: 1px solid var(--border-strong);
    aspect-ratio: 16 / 10;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .video-stage-box video {{
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
    background: #000;
  }}

  /* Live Synchronized Tri-Tier Readout Card */
  .live-hud-card {{
    background: var(--bg-canvas);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  .hud-meta-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 6px;
    font-family: var(--font-mono);
    font-size: 11px;
    font-variant-numeric: tabular-nums;
    color: var(--text-secondary);
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 6px;
  }}
  .hud-time-pill {{
    background: var(--bg-elevated);
    color: var(--accent-amber);
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
    border: 1px solid rgba(245, 158, 11, 0.3);
  }}
  .hud-hero-stage {{
    display: flex;
    align-items: baseline;
    justify-content: center;
    gap: 12px;
    padding: 6px 4px;
    min-height: 54px;
    text-align: center;
    flex-wrap: wrap;
  }}
  .hud-note-sym {{
    font-size: 28px;
    font-weight: 800;
    color: var(--accent-amber);
    font-family: var(--font-mono);
  }}
  .hud-en-syl {{
    font-size: 28px;
    font-weight: 800;
    color: var(--accent-orig);
    letter-spacing: -0.02em;
  }}
  .hud-ipa-syl {{
    font-size: 20px;
    font-weight: 600;
    color: #fde047;
    font-family: var(--font-mono);
    background: rgba(253, 224, 71, 0.08);
    padding: 2px 8px;
    border-radius: 6px;
    border: 1px solid rgba(253, 224, 71, 0.25);
  }}
  .hud-telemetry-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 6px;
    font-family: var(--font-mono);
    font-size: 11px;
    font-variant-numeric: tabular-nums;
  }}
  .telemetry-cell {{
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 5px;
    padding: 4px 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 6px;
  }}
  .telemetry-label {{ color: var(--text-muted); font-size: 10px; text-transform: uppercase; }}
  .telemetry-val {{ color: var(--text-primary); font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}

  /* Section Rhythm Strip inside Monitor Rail */
  .hud-strip-wrap {{
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 7px 8px;
  }}
  .hud-strip-label {{
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
  }}
  .section-score-bar {{
    display: flex;
    align-items: center;
    gap: 5px;
    overflow-x: auto;
    padding-bottom: 4px;
    scrollbar-width: thin;
  }}
  .score-note-pill {{
    flex-shrink: 0;
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    padding: 4px 8px;
    border-radius: 5px;
    border: 1px solid var(--border-strong);
    background: var(--bg-canvas);
    color: var(--text-secondary);
    font-family: var(--font-mono);
    font-size: 11px;
    cursor: pointer;
    transition: background 0.12s ease, border-color 0.12s ease, color 0.12s ease;
  }}
  .score-note-pill:hover {{
    background: var(--bg-interactive);
    color: #fff;
  }}
  .score-note-pill.current {{
    background: rgba(245, 158, 11, 0.2);
    color: #fff;
    border-color: var(--accent-amber);
    box-shadow: inset 0 0 0 1px var(--accent-amber);
  }}
  .score-note-pill .sn-rhy {{ font-size: 12px; font-weight: 700; color: var(--text-primary); }}
  .score-note-pill.current .sn-rhy {{ color: #fde047; }}
  .score-note-pill .sn-ipa {{ font-size: 9.5px; color: var(--text-muted); }}

  /* Transport Controls */
  .transport-controls {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .transport-row {{
    display: grid;
    grid-template-columns: 1fr 1.3fr 1fr;
    gap: 6px;
  }}
  .transport-btn {{
    background: var(--bg-elevated);
    color: var(--text-primary);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-sm);
    padding: 7px 8px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.12s ease, border-color 0.12s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
  }}
  .transport-btn:hover {{
    background: var(--bg-interactive);
    border-color: var(--accent-orig);
  }}
  .transport-btn.primary-play {{
    background: rgba(56, 189, 248, 0.16);
    border-color: var(--accent-orig);
    color: #e0f2fe;
  }}
  .transport-subrow {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
    flex-wrap: wrap;
  }}
  .speed-group {{
    display: inline-flex;
    background: var(--bg-canvas);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 2px;
    gap: 2px;
  }}
  .speed-btn {{
    background: transparent;
    color: var(--text-muted);
    border: none;
    border-radius: 4px;
    padding: 3px 7px;
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
  }}
  .speed-btn.active {{
    background: var(--bg-elevated);
    color: var(--accent-amber);
  }}
  .toggle-pill {{
    background: var(--bg-canvas);
    color: var(--text-muted);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 4px 8px;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
  }}
  .toggle-pill.on {{
    background: rgba(16, 185, 129, 0.15);
    color: #6ee7b7;
    border-color: rgba(16, 185, 129, 0.45);
  }}
  .kbd-hint {{
    font-size: 10.5px;
    color: var(--text-muted);
    text-align: center;
    font-family: var(--font-mono);
  }}
  kbd {{
    background: var(--bg-elevated);
    border: 1px solid var(--border-strong);
    border-radius: 3px;
    padding: 1px 4px;
    font-size: 10px;
    color: var(--text-secondary);
  }}

  /* Right Main Workbench Area */
  .main-workbench {{
    display: flex;
    flex-direction: column;
    gap: 18px;
    min-width: 0;
  }}

  /* Sticky Workspace Mode Switcher */
  .workspace-nav {{
    position: sticky;
    top: 66px;
    z-index: 250;
    background: var(--bg-glass);
    backdrop-filter: blur(14px);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    padding: 6px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
    flex-wrap: wrap;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.4);
  }}
  .ws-tabs-left {{
    display: flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
  }}
  .ws-tab {{
    background: transparent;
    color: var(--text-secondary);
    border: 1px solid transparent;
    border-radius: var(--radius-sm);
    padding: 7px 12px;
    font-size: 12.5px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.14s ease, color 0.14s ease, border-color 0.14s ease;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
  }}
  .ws-tab:hover {{
    background: var(--bg-elevated);
    color: #fff;
  }}
  .ws-tab.active {{
    background: var(--bg-interactive);
    color: #fff;
    border-color: var(--accent-orig);
    box-shadow: 0 2px 8px rgba(56, 189, 248, 0.18);
  }}
  .ws-tab.ab-tab.active {{
    border-color: var(--accent-suno);
    box-shadow: 0 2px 8px rgba(249, 115, 22, 0.22);
  }}
  .ws-pane {{
    display: none;
    flex-direction: column;
    gap: 18px;
  }}
  .ws-pane.active {{
    display: flex;
  }}
  body.show-all-panes .ws-pane {{
    display: flex;
  }}

  /* Surface Cards */
  .surface-card {{
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 20px 22px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.22);
  }}
  .card-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 16px;
    flex-wrap: wrap;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 12px;
  }}
  .eyebrow-row {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
    flex-wrap: wrap;
  }}
  .window-badge {{
    font-family: var(--font-mono);
    font-size: 10.5px;
    font-weight: 700;
    color: var(--accent-orig);
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 2px 7px;
    border-radius: 4px;
  }}
  .window-Range-pill {{
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-muted);
  }}
  .card-title {{
    margin: 0;
    font-size: 17px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.01em;
  }}
  .card-header-actions {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }}
  .btn-primary {{
    background: #0284c7;
    color: #fff;
    border: 1px solid #38bdf8;
    border-radius: var(--radius-sm);
    padding: 7px 13px;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.14s ease;
    white-space: nowrap;
  }}
  .btn-primary:hover {{ background: #0369a1; }}
  .btn-secondary {{
    background: var(--bg-elevated);
    color: var(--text-secondary);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-sm);
    padding: 7px 12px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.14s ease, color 0.14s ease;
    white-space: nowrap;
  }}
  .btn-secondary:hover {{
    background: var(--bg-interactive);
    color: #fff;
  }}

  /* Figures & Lightbox Trigger */
  .figure-frame {{
    position: relative;
    background: #06080c;
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    overflow: hidden;
    cursor: zoom-in;
  }}
  .figure-frame img {{
    width: 100%;
    height: auto;
    display: block;
  }}
  .figure-zoom-hint {{
    position: absolute;
    bottom: 8px;
    right: 10px;
    background: rgba(8, 10, 15, 0.85);
    color: var(--text-secondary);
    border: 1px solid var(--border-strong);
    border-radius: 5px;
    padding: 3px 8px;
    font-size: 11px;
    font-weight: 600;
    pointer-events: none;
    opacity: 0.85;
  }}

  /* Window Filter Bar */
  .win-filter-bar {{
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 10px 12px;
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
  }}
  .win-filter-pill {{
    background: var(--bg-canvas);
    color: var(--text-secondary);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 5px 10px;
    font-size: 11.5px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.12s ease, border-color 0.12s ease, color 0.12s ease;
  }}
  .win-filter-pill:hover {{
    background: var(--bg-elevated);
    color: #fff;
  }}
  .win-filter-pill.active {{
    background: rgba(56, 189, 248, 0.16);
    color: #fff;
    border-color: var(--accent-orig);
  }}
  .pill-time {{
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-muted);
    margin-left: 3px;
  }}

  /* Tactile Syllable Chips Grid (Zero-Jitter) */
  .section-sublabel {{
    font-size: 11.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--text-muted);
    margin: 14px 0 8px;
  }}
  .chips-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(132px, 1fr));
    gap: 8px;
  }}
  .syl-chip {{
    background: var(--bg-canvas);
    border: 1px solid var(--border-strong);
    border-left: 3px solid var(--chip-accent, #38bdf8);
    border-radius: var(--radius-sm);
    padding: 8px 10px;
    color: var(--text-primary);
    cursor: pointer;
    text-align: left;
    display: flex;
    flex-direction: column;
    gap: 4px;
    transition: background 0.12s ease, border-color 0.12s ease;
  }}
  .syl-chip:hover {{
    background: var(--bg-elevated);
    border-color: var(--chip-accent, #38bdf8);
  }}
  .syl-chip.active {{
    background: rgba(245, 158, 11, 0.16);
    border-color: var(--accent-amber);
    box-shadow: inset 0 0 0 1px var(--accent-amber);
  }}
  .syl-chip-top {{
    display: flex;
    justify-content: space-between;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-muted);
  }}
  .syl-chip-main {{
    display: flex;
    align-items: baseline;
    gap: 6px;
  }}
  .syl-note {{
    font-family: var(--font-mono);
    font-size: 15px;
    font-weight: 800;
    color: var(--accent-amber);
  }}
  .syl-en {{
    font-size: 15px;
    font-weight: 800;
    color: #fff;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }}
  .syl-ipa {{
    font-family: var(--font-mono);
    font-size: 12px;
    color: #bae6fd;
  }}
  .syl-chip-foot {{
    display: flex;
    align-items: center;
    gap: 5px;
    font-family: var(--font-mono);
    font-size: 9.5px;
    color: var(--text-muted);
    margin-top: 2px;
  }}
  .syl-cat-dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
  }}
  .syl-cat-name {{
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }}

  /* Clean Structured Data Tables */
  .structured-details {{
    margin-top: 14px;
    background: var(--bg-canvas);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    overflow: hidden;
  }}
  .details-summary {{
    padding: 10px 14px;
    background: var(--bg-elevated);
    font-size: 12.5px;
    font-weight: 700;
    color: var(--text-secondary);
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    user-select: none;
  }}
  .summary-hint {{
    font-size: 11px;
    font-weight: 500;
    color: var(--text-muted);
  }}
  .table-scroll {{
    overflow-x: auto;
  }}
  .studio-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
    font-variant-numeric: tabular-nums;
  }}
  .studio-table th, .studio-table td {{
    padding: 8px 11px;
    border-bottom: 1px solid var(--border-subtle);
    text-align: left;
    white-space: nowrap;
  }}
  .studio-table th {{
    background: #0c1018;
    color: var(--text-muted);
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }}
  .ev-row {{
    cursor: pointer;
    transition: background 0.1s ease;
  }}
  .ev-row:hover {{
    background: var(--bg-elevated);
  }}
  .ev-row.active {{
    background: rgba(245, 158, 11, 0.16);
  }}
  .id-pill {{
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    color: var(--text-secondary);
    background: var(--bg-elevated);
    padding: 2px 6px;
    border-radius: 4px;
  }}
  .rhy-badge {{
    font-family: var(--font-mono);
    font-weight: 700;
    color: var(--accent-amber);
  }}
  .ipa-code {{
    font-family: var(--font-mono);
    font-size: 12.5px;
    color: #fde047;
    background: rgba(253, 224, 71, 0.08);
    padding: 2px 6px;
    border-radius: 4px;
  }}
  .cat-pill {{
    font-family: var(--font-mono);
    font-size: 10.5px;
    font-weight: 700;
    color: #fff;
    background: color-mix(in srgb, var(--cat-col, #38bdf8) 28%, transparent);
    border: 1px solid var(--cat-col, #38bdf8);
    padding: 2px 7px;
    border-radius: 999px;
  }}
  .muted-sub {{
    color: var(--text-muted);
    font-size: 11px;
    font-family: var(--font-mono);
  }}
  .raw-bracket-box {{
    padding: 10px 14px;
    font-family: var(--font-mono);
    font-size: 11.5px;
    line-height: 1.75;
    max-height: 300px;
    overflow-y: auto;
  }}
  .raw-bracket-item {{
    padding: 2px 6px;
    border-radius: 4px;
    cursor: pointer;
  }}
  .raw-bracket-item:hover, .raw-bracket-item.active {{
    background: var(--bg-elevated);
  }}
  .raw-syl {{
    color: #fff;
    background: var(--bg-interactive);
    padding: 1px 6px;
    border-radius: 4px;
  }}

  /* Original vs. Suno A/B Studio */
  .ab-hero-banner {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 16px;
  }}
  @media (max-width: 900px) {{
    .ab-hero-banner {{ grid-template-columns: repeat(2, 1fr); }}
  }}
  .kpi-card {{
    background: var(--bg-canvas);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    padding: 12px 14px;
  }}
  .kpi-label {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--text-muted);
  }}
  .kpi-val {{
    font-family: var(--font-mono);
    font-size: 24px;
    font-weight: 800;
    color: var(--text-primary);
    margin: 4px 0 2px;
  }}
  .kpi-sub {{
    font-size: 11.5px;
    color: var(--text-secondary);
  }}

  .ab-players-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 18px;
  }}
  @media (max-width: 860px) {{
    .ab-players-grid {{ grid-template-columns: 1fr; }}
  }}
  .ab-deck {{
    background: var(--bg-canvas);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    padding: 14px 16px;
  }}
  .ab-deck.orig-deck {{ border-top: 3px solid var(--accent-orig); }}
  .ab-deck.suno-deck {{ border-top: 3px solid var(--accent-suno); }}
  .ab-deck-head {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
  }}
  .ab-deck-title {{
    font-size: 14.5px;
    font-weight: 800;
    margin: 0;
  }}
  .ab-phrase-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 10px;
  }}
  @media (max-width: 1100px) {{ .ab-phrase-grid {{ grid-template-columns: 1fr 1fr; }} }}
  @media (max-width: 720px) {{ .ab-phrase-grid {{ grid-template-columns: 1fr; }} }}
  .ab-phrase-card {{
    background: var(--bg-canvas);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    padding: 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 12px;
  }}
  .ab-phrase-card.peak-match {{
    border-color: var(--accent-emerald);
    background: rgba(16, 185, 129, 0.05);
  }}
  .ab-btn-row {{
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }}
  .ab-btn {{
    flex: 1;
    min-width: 92px;
    border: 1px solid transparent;
    border-radius: var(--radius-sm);
    padding: 6px 8px;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    text-align: center;
    transition: opacity 0.12s ease, transform 0.1s ease;
  }}
  .ab-btn:hover {{ opacity: 0.92; }}
  .ab-btn-a {{ background: rgba(56, 189, 248, 0.18); color: #bae6fd; border-color: #0284c7; }}
  .ab-btn-b-same {{ background: rgba(249, 115, 22, 0.18); color: #fed7aa; border-color: #ea580c; }}
  .ab-btn-b-best {{ background: rgba(16, 185, 129, 0.18); color: #a7f3d0; border-color: #059669; }}

  /* Style Cards & Lyric Tabs */
  .style-cards-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }}
  @media (max-width: 1080px) {{ .style-cards-grid {{ grid-template-columns: 1fr 1fr; }} }}
  @media (max-width: 700px) {{ .style-cards-grid {{ grid-template-columns: 1fr; }} }}
  .style-card {{
    background: var(--bg-canvas);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    padding: 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 10px;
    cursor: pointer;
    transition: border-color 0.14s ease, background 0.14s ease;
  }}
  .style-card:hover {{ border-color: var(--accent-orig); }}
  .style-card.selected {{
    border-color: var(--accent-orig);
    background: rgba(56, 189, 248, 0.06);
    box-shadow: inset 0 0 0 1px var(--accent-orig);
  }}
  .style-card h4 {{ margin: 0 0 4px 0; font-size: 14px; color: var(--text-primary); }}
  .style-why {{ font-size: 12px; color: var(--text-muted); margin: 0; line-height: 1.45; }}
  .style-prompt-code {{
    font-family: var(--font-mono);
    font-size: 11.5px;
    color: #fde047;
    background: var(--bg-surface);
    padding: 8px 10px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-subtle);
    line-height: 1.45;
  }}
  .flavor-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
  .flavor-chip {{
    background: var(--bg-canvas);
    color: var(--text-secondary);
    border: 1px solid var(--border-strong);
    border-radius: 999px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    user-select: none;
  }}
  .flavor-chip.on {{
    background: rgba(16, 185, 129, 0.16);
    color: #6ee7b7;
    border-color: var(--accent-emerald);
  }}
  .combined-prompt-bar {{
    margin-top: 14px;
    background: var(--bg-canvas);
    border: 1px solid var(--accent-orig);
    border-radius: var(--radius-md);
    padding: 12px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    flex-wrap: wrap;
  }}

  .lyrics-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }}
  @media (max-width: 960px) {{ .lyrics-grid {{ grid-template-columns: 1fr; }} }}
  .lyric-card {{
    background: var(--bg-canvas);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  pre.suno-box {{
    background: #06080c;
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 12px 14px;
    font-family: var(--font-mono);
    font-size: 12px;
    color: var(--text-primary);
    overflow-x: auto;
    line-height: 1.6;
    margin: 0;
    max-height: 440px;
  }}

  /* Search Input */
  .search-input {{
    background: var(--bg-canvas);
    color: var(--text-primary);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-sm);
    padding: 7px 12px;
    font-size: 13px;
    min-width: 260px;
  }}
  .search-input:focus {{
    outline: 2px solid var(--accent-orig);
    border-color: transparent;
  }}

  /* Full-Screen Image Lightbox Modal */
  .lightbox-backdrop {{
    position: fixed;
    inset: 0;
    background: rgba(5, 7, 11, 0.92);
    backdrop-filter: blur(10px);
    z-index: 1000;
    display: none;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }}
  .lightbox-backdrop.open {{ display: flex; }}
  .lightbox-top {{
    width: 100%;
    max-width: 1500px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    color: var(--text-primary);
  }}
  .lightbox-img-wrap {{
    max-width: 1500px;
    max-height: calc(100vh - 110px);
    overflow: auto;
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    background: #000;
  }}
  .lightbox-img-wrap img {{
    width: 100%;
    height: auto;
    display: block;
  }}
</style>
</head>
<body>

<!-- Top Application Bar -->
<header class="app-topbar">
  <div class="brand-cluster">
    <span class="brand-dot"></span>
    <h1 class="brand-title">IMG_3268 — Vocal Percussion, Narrow IPA, Rhythm &amp; Suno A/B Studio</h1>
    <span class="brand-badge">{badge_mode}</span>
  </div>
  {download_menu_html}
</header>

<!-- Main Two-Column Studio Shell -->
<div class="studio-shell">

  <!-- LEFT STICKY STUDIO MONITOR RAIL -->
  <aside class="monitor-rail" aria-label="Studio Media Monitor &amp; Synchronized Phonetic HUD">
    <div class="monitor-source-tabs" role="tablist">
      <button type="button" class="src-tab active" id="srctab-video" onclick="switchMonitorSource('video')">🎥 Video + Subtitles</button>
      <button type="button" class="src-tab" id="srctab-orig" onclick="switchMonitorSource('orig')">🅰️ Original MP3</button>
      <button type="button" class="src-tab" id="srctab-suno" onclick="switchMonitorSource('suno')">🅱️ Suno MP3</button>
    </div>

    <div class="video-stage-box">
      <video id="mainMedia" controls playsinline preload="auto" src="{asset_urls['web_mp4']}">
        <track label="Phonetics + IPA + Rhythm" kind="subtitles" srclang="en" src="{asset_urls['vtt']}" default />
      </video>
    </div>

    <!-- Live Tri-Tier Phonetic + Narrow IPA + Musical Rhythm Readout -->
    <div class="live-hud-card">
      <div class="hud-meta-top">
        <span class="hud-time-pill" id="hudTime">00.00s / 37.82s</span>
        <span id="hudBar">Bar — (4/4 @ — BPM)</span>
        <span id="hudGrid">Grid: —</span>
      </div>

      <div class="hud-hero-stage">
        <span class="hud-note-sym" id="hudNoteSym">♩</span>
        <span class="hud-en-syl" id="hudSyl">Ready to Audition</span>
        <span class="hud-ipa-syl" id="hudIpa">[ — ]</span>
      </div>

      <div class="hud-telemetry-grid">
        <div class="telemetry-cell">
          <span class="telemetry-label">Cat</span>
          <span class="telemetry-val" id="hudCat">—</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Artic</span>
          <span class="telemetry-val" id="hudArt">—</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Rhythm</span>
          <span class="telemetry-val" id="hudRhyShort">—</span>
        </div>
        <div class="telemetry-cell">
          <span class="telemetry-label">Peak/ATK</span>
          <span class="telemetry-val" id="hudPkAtk">—</span>
        </div>
        <div class="telemetry-cell" style="grid-column: span 2;">
          <span class="telemetry-label">F0 · F1/F2/F3</span>
          <span class="telemetry-val" id="hudFormants">—</span>
        </div>
      </div>
    </div>

    <!-- Active Window Musical Score Strip -->
    <div class="hud-strip-wrap">
      <div class="hud-strip-label">
        <span>Active Window Rhythm Strip</span>
        <span id="hudWinLabel" style="color:var(--accent-orig);">Click any note</span>
      </div>
      <div class="section-score-bar" id="hudSectionScore">
        <span style="font-size:11.5px; color:var(--text-muted);">Press Play or click any syllable pad to track live rhythm notes...</span>
      </div>
    </div>

    <!-- Transport & Speed Controls -->
    <div class="transport-controls">
      <div class="transport-row">
        <button type="button" class="transport-btn" onclick="stepEvent(-1)" title="Previous Syllable (Left Arrow)">⏮ Prev</button>
        <button type="button" class="transport-btn primary-play" onclick="togglePlayPause()" id="btnPlayPause" title="Play / Pause (Space)">⏯ Play / Pause</button>
        <button type="button" class="transport-btn" onclick="stepEvent(1)" title="Next Syllable (Right Arrow)">Next ⏭</button>
      </div>
      <div class="transport-subrow">
        <div class="speed-group" aria-label="Playback Speed">
          <button type="button" class="speed-btn active" onclick="setSpeed(1.0, this)">1.0x</button>
          <button type="button" class="speed-btn" onclick="setSpeed(0.75, this)">0.75x</button>
          <button type="button" class="speed-btn" onclick="setSpeed(0.5, this)">0.5x</button>
          <button type="button" class="speed-btn" onclick="setSpeed(0.25, this)">0.25x</button>
        </div>
        <button type="button" class="toggle-pill" id="btnLoopSlice" onclick="toggleLoopSlice()">🔁 Loop Slice: OFF</button>
        <button type="button" class="toggle-pill" id="btnScroll" onclick="toggleAutoScroll()">📜 Auto-Follow: OFF</button>
      </div>
      <div class="kbd-hint">
        Shortcuts: <kbd>Space</kbd> Play/Pause · <kbd>←</kbd><kbd>→</kbd> Step Syllable · <kbd>1</kbd>–<kbd>5</kbd> Switch View
      </div>
    </div>
  </aside>

  <!-- RIGHT MAIN WORKBENCH -->
  <main class="main-workbench">

    <!-- Segmented Workspace Switcher -->
    <nav class="workspace-nav" aria-label="Workspace Sections">
      <div class="ws-tabs-left">
        <button type="button" class="ws-tab ab-tab active" data-pane="pane-ab" onclick="switchWorkspace('pane-ab', this)">🔥 1. Original vs. Suno A/B (`earshot`)</button>
        <button type="button" class="ws-tab" data-pane="pane-microscope" onclick="switchWorkspace('pane-microscope', this)">🔬 2. 14-Window Microscope (147 Events)</button>
        <button type="button" class="ws-tab" data-pane="pane-suno" onclick="switchWorkspace('pane-suno', this)">🎤 3. Suno Styles &amp; IPA Lyrics</button>
        <button type="button" class="ws-tab" data-pane="pane-rhythm" onclick="switchWorkspace('pane-rhythm', this)">🎼 4. Rhythm &amp; Narrow IPA Guide</button>
        <button type="button" class="ws-tab" data-pane="pane-corpus" onclick="switchWorkspace('pane-corpus', this)">📊 5. Searchable 147-Event Table</button>
      </div>
      <button type="button" class="toggle-pill" id="btnShowAllPanes" onclick="toggleShowAllPanes()">📑 View All on One Page: OFF</button>
    </nav>

    <!-- =================================================================== -->
    <!-- WORKSPACE 1: ORIGINAL VS. SUNO A/B COMPARISON (EARSHOT)             -->
    <!-- =================================================================== -->
    <div class="ws-pane active" id="pane-ab">
      <section class="surface-card">
        <header class="card-header">
          <div>
            <div class="eyebrow-row">
              <span class="window-badge" style="color:#fb923c; border-color:rgba(249,115,22,0.4); background:rgba(249,115,22,0.12);">EARSHOT ACOUSTIC &amp; CLAP BENCHMARK</span>
              <span class="window-Range-pill">Commands: <code>measure</code> · <code>describe</code> · <code>realness</code> · <code>timeline</code> · <code>sheet</code> · <code>find</code> · <code>ab</code></span>
            </div>
            <h2 class="card-title">Original Mouth Performance (`IMG_3268.mp3`) vs. Suno Render (`IMG_3268 SUNO.mp3`)</h2>
          </div>
        </header>

        <!-- 4 Key Metric Highlights -->
        <div class="ab-hero-banner">
          <div class="kpi-card">
            <div class="kpi-label">Peak 3s Window Similarity</div>
            <div class="kpi-val" style="color:var(--accent-emerald);">0.82 cos</div>
            <div class="kpi-sub"><code>0.78 cos</code> at exact same time (<code>30–33s</code> scratch bar)</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Full 0–37.8s Pass &amp; Phrase 4</div>
            <div class="kpi-val" style="color:var(--accent-orig);">0.60 / 0.69</div>
            <div class="kpi-sub"><code>earshot ab</code>: "CLAP hears them as related"</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Target Prompt Rank (322 Vocab)</div>
            <div class="kpi-val" style="color:var(--accent-amber);">#1 vs #1</div>
            <div class="kpi-sub">Both <code>100th pct</code> (Orig <code>z +6.71</code>, Suno <code>z +7.34</code>)</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Realness &amp; Macro Attack</div>
            <div class="kpi-val" style="color:#e2e8f0;">0.99 vs 0.98</div>
            <div class="kpi-sub">Attack: <code>148 ms</code> Orig vs <code>146 ms</code> Suno</div>
          </div>
        </div>

        <!-- Dual Audio Decks -->
        <div class="ab-players-grid">
          <div class="ab-deck orig-deck">
            <div class="ab-deck-head">
              <h3 class="ab-deck-title" style="color:var(--accent-orig);">🅰️ Original Mouth Performance (`IMG_3268.mp3`)</h3>
              <span class="window-Range-pill">37.82s · -28.2 LUFS · Mono · p_real 0.994</span>
            </div>
            <p class="style-why" style="margin-bottom:10px;">
              AudioSet: <strong>Speech 0.88, Beatboxing 0.74, Whispering 0.43</strong> · CLAP: <code>vocal chop z +4.33</code>, <code>hip hop beat z +2.51</code>, <code>brass section z +1.91</code>
            </p>
            <audio id="origAbAudio" controls preload="auto" src="{asset_urls['orig_mp3']}" style="width:100%; height:36px;"></audio>
          </div>

          <div class="ab-deck suno-deck">
            <div class="ab-deck-head">
              <h3 class="ab-deck-title" style="color:var(--accent-suno);">🅱️ Suno Render (`IMG_3268 SUNO.mp3`)</h3>
              <span class="window-Range-pill">89.36s · -16.4 LUFS · Stereo · p_real 0.981</span>
            </div>
            <p class="style-why" style="margin-bottom:10px;">
              AudioSet: <strong>Music 0.86, Beatboxing 0.61, Speech 0.35, Brass 0.20, Funk 0.18</strong> · CLAP: <code>funk music z +4.60</code>, <code>vocal chop z +3.86</code>, <code>glitch hop z +3.21</code>
            </p>
            <audio id="sunoAbAudio" controls preload="auto" src="{asset_urls['suno_mp3']}" style="width:100%; height:36px;"></audio>
          </div>
        </div>

        <!-- Interactive Phrase-by-Phrase A/B Audition Grid -->
        <div class="section-sublabel">🎧 Phrase-by-Phrase Interactive A/B Audition (Click to compare Original A vs. Suno Same-Time B vs. Suno Best-Match Window B)</div>
        <div class="ab-phrase-grid">
          <div class="ab-phrase-card">
            <div>
              <strong style="color:var(--accent-orig); font-size:13.5px;">Phrase 1 (0.26–4.35s): Plosive-Brush Scat</strong>
              <p class="style-why" style="margin-top:4px;"><code>thuh-bitch camp brah / pant thence / at ALL!</code><br/>CLAP Cosine: <strong>0.46</strong> (same time) · <strong>0.58</strong> (3s win) · Query z: Orig <strong>+2.91</strong> vs Suno <strong>+4.81</strong> (#1/322)</p>
            </div>
            <div class="ab-btn-row">
              <button type="button" class="ab-btn ab-btn-a" onclick="playOrigAb(0.26, 4.35)">▶ Orig (0.3–4.4s)</button>
              <button type="button" class="ab-btn ab-btn-b-same" onclick="playSunoAb(0.26, 4.35)">▶ Suno Same (0.3–4.4s)</button>
              <button type="button" class="ab-btn ab-btn-b-best" onclick="playSunoAb(17.30, 21.39)">▶ Suno Best (17.3–21.4s)</button>
            </div>
          </div>

          <div class="ab-phrase-card">
            <div>
              <strong style="color:var(--accent-purple); font-size:13.5px;">Phrase 2 (4.75–11.72s): Sub-Hum &amp; Cork-Pop Groove</strong>
              <p class="style-why" style="margin-top:4px;"><code>Mmmm! / pink cane / ki-'in / NOW!</code><br/>CLAP Cosine: <strong>0.53</strong> (best) / <strong>0.51</strong> (same time) · Query z: Orig <strong>+2.81</strong> vs Suno <strong>+8.40</strong> (#1/322)</p>
            </div>
            <div class="ab-btn-row">
              <button type="button" class="ab-btn ab-btn-a" onclick="playOrigAb(4.75, 11.72)">▶ Orig (4.8–11.7s)</button>
              <button type="button" class="ab-btn ab-btn-b-same" onclick="playSunoAb(4.75, 11.72)">▶ Suno Same (4.8–11.7s)</button>
              <button type="button" class="ab-btn ab-btn-b-best" onclick="playSunoAb(2.06, 4.04)">▶ Suno Best (2.1–4.0s)</button>
            </div>
          </div>

          <div class="ab-phrase-card">
            <div>
              <strong style="color:var(--accent-amber); font-size:13.5px;">Phrase 3A–3B (12.50–18.12s): Brass Wah &amp; WHEN!↑</strong>
              <p class="style-why" style="margin-top:4px;"><code>You know what -&gt; BOW-buh-BOW-BOW-BOW! / WHEN!↑</code><br/>CLAP Cosine: <strong>0.50</strong> (aligned at <strong>12.52–17.56s</strong>!) · Query z: Orig <strong>+3.20</strong> vs Suno <strong>+4.98</strong> (#1/322)</p>
            </div>
            <div class="ab-btn-row">
              <button type="button" class="ab-btn ab-btn-a" onclick="playOrigAb(12.50, 18.12)">▶ Orig (12.5–18.1s)</button>
              <button type="button" class="ab-btn ab-btn-b-same" onclick="playSunoAb(12.50, 18.12)">▶ Suno Same (12.5–18.1s)</button>
              <button type="button" class="ab-btn ab-btn-b-best" onclick="playSunoAb(12.52, 17.56)">▶ Suno Best (12.5–17.6s)</button>
            </div>
          </div>

          <div class="ab-phrase-card">
            <div>
              <strong style="color:#ec4899; font-size:13.5px;">Phrase 3C–3D (18.47–22.75s): 32nd Roll &amp; Chopper</strong>
              <p class="style-why" style="margin-top:4px;"><code>thuh-buh-chuh-kuh-buh-GAH / skibidi-BAH / buh-lip-uh-gih</code><br/>CLAP Cosine: <strong>0.41</strong> (<strong>0.67</strong> at 22.5s) · Query z: Orig <strong>+3.72</strong> (#2) vs Suno <strong>+6.11</strong> (#1/322)</p>
            </div>
            <div class="ab-btn-row">
              <button type="button" class="ab-btn ab-btn-a" onclick="playOrigAb(18.47, 22.75)">▶ Orig (18.5–22.8s)</button>
              <button type="button" class="ab-btn ab-btn-b-same" onclick="playSunoAb(18.47, 22.75)">▶ Suno Same (18.5–22.8s)</button>
              <button type="button" class="ab-btn ab-btn-b-best" onclick="playSunoAb(9.97, 14.25)">▶ Suno Best (10.0–14.3s)</button>
            </div>
          </div>

          <div class="ab-phrase-card peak-match">
            <div>
              <strong style="color:var(--accent-emerald); font-size:13.5px;">🏆 Phrase 4 (22.92–34.10s): 808 Beatbox &amp; Scratch</strong>
              <p class="style-why" style="margin-top:4px; color:#d1fae5;"><code>FWOO-BWAH / Boom-ts-boom / Hhh-RA-hh-RA!</code><br/>Macro Cosine: <strong>0.69</strong> · <strong>Peak 3s Cosine = 0.82</strong> (A:24–27s vs B:30–33s) &amp; <strong>0.78</strong> at exact same time (30–33s)!</p>
            </div>
            <div class="ab-btn-row">
              <button type="button" class="ab-btn ab-btn-a" onclick="playOrigAb(22.92, 34.10)">▶ Orig (22.9–34.1s)</button>
              <button type="button" class="ab-btn ab-btn-b-same" onclick="playSunoAb(22.92, 34.10)">▶ Suno Same (22.9–34.1s)</button>
              <button type="button" class="ab-btn ab-btn-b-best" onclick="playSunoAb(30.00, 33.50)">▶ Peak Match (30–33.5s)</button>
            </div>
          </div>

          <div class="ab-phrase-card">
            <div>
              <strong style="color:#fde047; font-size:13.5px;">Phrase 5 (36.48–37.38s): Coda Tag + Suno Jam</strong>
              <p class="style-why" style="margin-top:4px;"><code>Duh-rip-it-NOW!</code> + Suno's <code>0.4s</code> drop at <code>0:33.50</code> (matching Orig's <code>0:34.10</code> break!) &amp; extended jam<br/>CLAP Cosine: <strong>0.53</strong> · Query z: Orig <strong>+4.60</strong> vs Suno <strong>+4.90</strong> (#1/322)</p>
            </div>
            <div class="ab-btn-row">
              <button type="button" class="ab-btn ab-btn-a" onclick="playOrigAb(36.48, 37.38)">▶ Orig Coda (36.5–37.4s)</button>
              <button type="button" class="ab-btn ab-btn-b-best" onclick="playSunoAb(3.80, 4.70)">▶ Suno Best (3.8–4.7s)</button>
              <button type="button" class="ab-btn ab-btn-b-same" onclick="playSunoAb(33.00, 42.00)">▶ Suno Drop (33–42s)</button>
            </div>
          </div>
        </div>

        <!-- Quantitative earshot Scorecard Table -->
        <div class="section-sublabel" style="margin-top:20px;">📊 Complete `earshot` Quantitative A/B Scorecard</div>
        <div class="table-scroll">
          <table class="studio-table" style="white-space:normal;">
            <thead>
              <tr>
                <th style="min-width:190px;">earshot Metric / Command</th>
                <th style="min-width:210px; color:var(--accent-orig);">🅰️ Original (`IMG_3268.mp3`)</th>
                <th style="min-width:210px; color:var(--accent-suno);">🅱️ Suno (`IMG_3268 SUNO.mp3`)</th>
                <th style="min-width:300px; color:var(--accent-emerald);">earshot Verdict &amp; Acoustic Meaning</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Direct CLAP Similarity (`earshot ab`)</strong></td>
                <td>Reference vocal-percussion track (<code>0:00–0:37.80</code>)</td>
                <td>Aligned 1st pass (<code>0:00–0:37.80</code> of <code>89.36s</code> track)</td>
                <td><strong><code>cosine_ab = 0.60</code> ("CLAP hears them as related")</strong>; Phrase 4 hits <strong><code>0.69</code></strong> and 3s sliding window peaks at <strong><code>0.82</code></strong> (and <strong><code>0.78</code></strong> at the exact same timestamp <code>30–33s</code>).</td>
              </tr>
              <tr>
                <td><strong>Combined Target Prompt (`ab --query`)</strong><br/><span class="muted-sub">"rhythmic human beatboxing, vocal chops, brass wah stabs and 808 sub-bass groove"</span></td>
                <td><strong><code>z = +6.71</code></strong> (<code>cos = 0.354</code>)<br/>Rank <strong>#1 / 322</strong> (<code>100th pct</code>)</td>
                <td><strong><code>z = +7.34</code></strong> (<code>cos = 0.471</code>)<br/>Rank <strong>#1 / 322</strong> (<code>100th pct</code>)</td>
                <td><strong>Both rank #1 of 322 in earshot's calibrated vocabulary (100th percentile)</strong>; Suno edges slightly ahead (<code>dz = +0.63</code>) with full-band sub-bass and brass backing.</td>
              </tr>
              <tr>
                <td><strong>Human Beatboxing Prompt (`ab --query`)</strong><br/><span class="muted-sub">"rhythmic human beatboxing and vocal percussion with plosive kicks and hi-hats"</span></td>
                <td><strong><code>z = +4.95</code></strong> (<code>cos = 0.289</code>)<br/>Rank <strong>#1 / 322</strong> (<code>100th pct</code>)</td>
                <td><strong><code>z = +4.71</code></strong> (<code>cos = 0.312</code>)<br/>Rank <strong>#1 / 322</strong> (<code>100th pct</code>)</td>
                <td><strong>"Neither is closer (<code>dz = 0.24</code>)" — Statistical Tie at #1 / 322!</strong> Suno preserves the crisp plosive kicks and affricate hi-hat transients.</td>
              </tr>
              <tr>
                <td><strong>808 Sub-Bass &amp; Boom-Bap (`ab --query`)</strong><br/><span class="muted-sub">"heavy 808 sub-bass kick and boom-bap beatbox groove"</span></td>
                <td><strong><code>z = +3.55</code></strong> (<code>cos = 0.165</code>)<br/>Rank <strong>#3 / 322</strong> (<code>99.4th pct</code>)</td>
                <td><strong><code>z = +3.83</code></strong> (<code>cos = 0.207</code>)<br/>Rank <strong>#1 / 322</strong> (<code>100th pct</code>)</td>
                <td><strong>"Neither is closer (<code>dz = 0.28</code>)" — Statistical Tie!</strong> Both deliver the same heavy halftime boom-bap sub-bass pocket.</td>
              </tr>
              <tr>
                <td><strong>Talkbox Brass Wah &amp; DJ Scratch (`ab --query`)</strong></td>
                <td>Talkbox Wah: <code>z = +4.16</code> (#1)<br/>DJ Scratch: <code>z = +1.98</code> (#9)</td>
                <td>Talkbox Wah: <strong><code>z = +6.01</code></strong> (#1)<br/>DJ Scratch: <strong><code>z = +4.05</code></strong> (#1)</td>
                <td><strong>Suno amplifies the mouth-imitated instruments (<code>dz = +1.85</code> &amp; <code>+2.07</code>)</strong>: translates <code>BOW-buh-BOW</code> formant sweeps and <code>Hhh-RA-hh-RA!</code> uvular trills into full horn stabs and turntable cuts.</td>
              </tr>
              <tr>
                <td><strong>Realness (`earshot realness`)</strong></td>
                <td><strong><code>p_real = 0.994</code></strong> (0/10 synth windows, CLAP head <code>+4.5</code>)</td>
                <td><strong><code>p_real = 0.981</code></strong> (0/23 synth windows, CLAP head <code>+4.1</code>, peak <code>1.00</code>)</td>
                <td>Both pass <code>earshot realness</code> as <strong><code>real or pro-produced</code></strong> with zero windows flagged as cheap synthesis.</td>
              </tr>
              <tr>
                <td><strong>Loudness, Attack &amp; Spectrum (`measure`)</strong></td>
                <td><code>-28.2 LUFS</code> · Attack <strong><code>148 ms</code></strong> · Brightness <code>1952 Hz</code> · Sub <code>-33.0 dB</code> · Top <code>-48.7 dB</code></td>
                <td><code>-16.4 LUFS</code> · Attack <strong><code>146 ms</code></strong> · Brightness <code>4074 Hz</code> · Sub <code>-14.1 dB</code> · Top <code>-26.5 dB</code></td>
                <td>Identical macro envelope attack (<strong><code>148 ms</code> vs <code>146 ms</code></strong>), while Suno adds <code>+11.8 LU</code> mastered loudness, <code>+18.9 dB</code> sub-60Hz weight, and <code>+22.2 dB</code> top-octave air.</td>
              </tr>
              <tr>
                <td><strong>Structural Drop Alignment (`timeline`)</strong></td>
                <td>Post-scratch breakdown drop at <strong><code>0:34.10</code></strong> before final <code>Duh-rip-it-NOW!</code></td>
                <td>Executes a <code>0.4s</code> stop-down drop at <strong><code>0:33.50</code></strong> (<code>Δt = 0.6s</code> apart!) then jams to <code>89.36s</code></td>
                <td>Suno's first 37.8 seconds track the 5-phrase pacing of your phonetic lyric sheet so closely that the breakdown drop lands within <code>0.6 seconds</code> of the original recording.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Comparison Visualizations -->
        <div class="section-sublabel" style="margin-top:20px;">📈 `earshot` 6-Panel A/B Diagnostic &amp; Side-by-Side Contact Sheets (Click any image to zoom)</div>
        <div class="figure-frame" onclick="openLightbox('suno_comp', 'Original vs. Suno earshot 6-Panel Comparison')">
          <img id="img-suno_comp" src="{asset_urls['suno_comp']}" alt="Original vs Suno earshot 6-Panel Comparison" />
          <div class="figure-zoom-hint">🔍 Click to expand 6-panel A/B comparison</div>
        </div>

        <div class="ab-players-grid" style="margin-top:14px; margin-bottom:0;">
          <div>
            <div class="section-sublabel" style="margin-top:0; color:var(--accent-orig);">🅰️ `earshot sheet` — Original (`IMG_3268.mp3`, 0–37.8s)</div>
            <div class="figure-frame" onclick="openLightbox('orig_sheet', 'Original IMG_3268.mp3 earshot Sheet')">
              <img id="img-orig_sheet" src="{asset_urls['orig_sheet']}" alt="Original earshot sheet" loading="lazy" />
              <div class="figure-zoom-hint">🔍 Expand sheet</div>
            </div>
          </div>
          <div>
            <div class="section-sublabel" style="margin-top:0; color:var(--accent-suno);">🅱️ `earshot sheet` — Suno Render (`IMG_3268 SUNO.mp3`, 0–89.4s)</div>
            <div class="figure-frame" onclick="openLightbox('suno_sheet', 'Suno Render IMG_3268 SUNO.mp3 earshot Sheet')">
              <img id="img-suno_sheet" src="{asset_urls['suno_sheet']}" alt="Suno earshot sheet" loading="lazy" />
              <div class="figure-zoom-hint">🔍 Expand sheet</div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- =================================================================== -->
    <!-- WORKSPACE 2: 14-WINDOW PHONETIC & MUSICAL RHYTHM MICROSCOPE         -->
    <!-- =================================================================== -->
    <div class="ws-pane" id="pane-microscope">
      <div class="win-filter-bar" aria-label="Filter Zoom Windows">
        <span style="font-size:11px; font-weight:800; color:var(--text-muted); text-transform:uppercase; margin-right:4px;">Window Filter:</span>
        {''.join(win_pills)}
      </div>

      {''.join(sections_html)}
    </div>

    <!-- =================================================================== -->
    <!-- WORKSPACE 3: SUNO PROMPT STUDIO & PURE IPA LYRIC BLOCKS             -->
    <!-- =================================================================== -->
    <div class="ws-pane" id="pane-suno">
      <section class="surface-card">
        <header class="card-header">
          <div>
            <div class="eyebrow-row">
              <span class="window-badge">SUNO STYLE &amp; FLAVOR ENGINE</span>
              <span class="window-Range-pill">6 Acoustic Genre Archetypes + Interactive Modifier Mixer</span>
            </div>
            <h2 class="card-title">Stylistic Genre Options &amp; Interactive Suno Style Prompt Builder</h2>
          </div>
        </header>

        <div class="style-cards-grid">
          <div class="style-card selected" id="scard-0" onclick="selectBaseStyle(0)">
            <div>
              <h4>Option A: 90s Turntablist Boom-Bap &amp; Beatbox Cypher</h4>
              <p class="style-why"><strong>Ref:</strong> Rahzel / Scratch / The Roots.<br/>Built around the 83.5 BPM halftime 808 vocal sub-kicks (<code>[ˈbuːm]</code>), affricate hats (<code>[t͡sʰ]</code>), snare washes (<code>[ˈbuʃ]</code>), and uvular vinyl scratches (<code>Hhh-RA-hh-RA!</code>).</p>
            </div>
            <div>
              <div class="style-prompt-code" id="sprompt-0">90s underground boom-bap hip-hop, live human beatbox percussion, vocal bassline 808 sub-kicks, turntablism vinyl record scratches, raw vocal scatting, punchy dry close-mic vocals, 85 BPM</div>
              <button type="button" class="btn-primary" style="margin-top:8px; width:100%;" onclick="event.stopPropagation(); copyText('sprompt-0', this)">Copy Style A</button>
            </div>
          </div>

          <div class="style-card" id="scard-1" onclick="selectBaseStyle(1)">
            <div>
              <h4>Option B: Future Funk / Talkbox Brass-Bounce &amp; Glitch-Hop</h4>
              <p class="style-why"><strong>Ref:</strong> Chromeo / Gramatik / Opiuo / Beardyman.<br/>Matches Phrase 3's envelope-filtered brass wah stabs (<code>BOW-buh-BOW!</code>), 500 Hz pinched falsetto squeak (<code>WHEN!↑</code>), and 131 BPM double-tongued chopper.</p>
            </div>
            <div>
              <div class="style-prompt-code" id="sprompt-1">glitch-hop future funk, talkbox synth-brass wah stabs, rhythmic vocal chops, slap bass, crisp percussive scatting, micro-sampled vocal percussion, high-energy funk pocket, 112 BPM</div>
              <button type="button" class="btn-primary" style="margin-top:8px; width:100%;" onclick="event.stopPropagation(); copyText('sprompt-1', this)">Copy Style B</button>
            </div>
          </div>

          <div class="style-card" id="scard-2" onclick="selectBaseStyle(2)">
            <div>
              <h4>Option C: Avant-Garde Loop-Station Funk &amp; Neo-Soul Pocket</h4>
              <p class="style-why"><strong>Ref:</strong> Reggie Watts / Marc Rebillet / Bobby McFerrin / J Dilla.<br/>Captures the laid-back -18ms swung 16th pocket, nasal clavinet muting (<code>camp, pump</code>), hollow cork-pop transients (<code>pink, 'in</code>), and theatrical hums.</p>
            </div>
            <div>
              <div class="style-prompt-code" id="sprompt-2">live loop-station vocal funk, neo-soul swung pocket, Reggie Watts style experimental vocal groove, mouth-percussion, clavinet vocal muting, human bass hum, playful theatrical beatbox scat, 98 BPM</div>
              <button type="button" class="btn-primary" style="margin-top:8px; width:100%;" onclick="event.stopPropagation(); copyText('sprompt-2', this)">Copy Style C</button>
            </div>
          </div>

          <div class="style-card" id="scard-3" onclick="selectBaseStyle(3)">
            <div>
              <h4>Option D: UK Bassline / Halftime Wonky Trap &amp; Vocal Chops</h4>
              <p class="style-why"><strong>Ref:</strong> TroyBoi / Tipper / Baauer / Hudson Mohawke.<br/>Turns the air riser (<code>FWOO-BWAH!</code>), sub-100Hz 808 kicks, and syncopated <code>ship it DOWN / take it DOWN</code> hooks into a heavy festival trap/halftime drop.</p>
            </div>
            <div>
              <div class="style-prompt-code" id="sprompt-3">wonky halftime trap, heavy 808 sub-bass glides, pitched vocal chop hooks, festival horn stabs, crisp mouth percussion foley, reverse air risers, swaggering halftime bounce, 84 BPM</div>
              <button type="button" class="btn-primary" style="margin-top:8px; width:100%;" onclick="event.stopPropagation(); copyText('sprompt-3', this)">Copy Style D</button>
            </div>
          </div>

          <div class="style-card" id="scard-4" onclick="selectBaseStyle(4)">
            <div>
              <h4>Option E: Nu-Jazz / Scat-Funk &amp; Hyper-Pocket Drumline</h4>
              <p class="style-why"><strong>Ref:</strong> Louis Cole (Knower) / Cab Calloway / Caravan Palace.<br/>Highlights the rapid 32nd-note paradiddle drum roll (<code>thuh-buh-chuh-kuh-buh-GAH!</code>), sextuplet <code>ski-bi-di-BAH!</code>, and punchy big-band horn articulations.</p>
            </div>
            <div>
              <div class="style-prompt-code" id="sprompt-4">nu-jazz scat funk, tight drumline vocal percussion, punchy big-band brass stabs, rapid double-tongue vocal rolls, Louis Cole style hyper-funk pocket, dry studio drums, 122 BPM</div>
              <button type="button" class="btn-primary" style="margin-top:8px; width:100%;" onclick="event.stopPropagation(); copyText('sprompt-4', this)">Copy Style E</button>
            </div>
          </div>

          <div class="style-card" id="scard-5" onclick="selectBaseStyle(5)">
            <div>
              <h4>Option F: Phonk / Memphis Cowbell &amp; Dirty Turntable Chop</h4>
              <p class="style-why"><strong>Ref:</strong> DJ Smokey / Tommy Wright III / Drift Phonk.<br/>Pairs the gritty uvular throat scrapes (<code>[χː ˈʀæ]</code>), clipped alveolar woodblock pops (<code>[ˈpʰɪŋk̚]</code>), and distorted sub-bass <code>Boom-ts-boom</code> cadence.</p>
            </div>
            <div>
              <div class="style-prompt-code" id="sprompt-5">underground phonk, gritty lo-fi vocal chops, distorted 808 cowbell bounce, vinyl scratch cuts, punchy Memphis rap cadence, raw close-mic vocal percussion, 86 BPM</div>
              <button type="button" class="btn-primary" style="margin-top:8px; width:100%;" onclick="event.stopPropagation(); copyText('sprompt-5', this)">Copy Style F</button>
            </div>
          </div>
        </div>

        <div class="section-sublabel" style="margin-top:18px;">Click Flavor Modifiers to Mix Into Your Active Style Prompt</div>
        <div class="flavor-row">
          <span class="flavor-chip" onclick="toggleFlavor(this, 'close-mic ASMR transients, dry studio booth, zero reverb')">🎙️ Dry Close-Mic ASMR Transients</span>
          <span class="flavor-chip" onclick="toggleFlavor(this, 'talkbox formant filter, auto-wah envelope sweep, clavinet funk')">🎛️ Talkbox / Auto-Wah Formant Filter</span>
          <span class="flavor-chip" onclick="toggleFlavor(this, 'DJ vinyl scratch breaks, MPC sampler stutter chops')">💿 DJ Scratch &amp; MPC Stutter Chops</span>
          <span class="flavor-chip" onclick="toggleFlavor(this, 'heavy 808 sub-bass sustain, chest-thumping low end')">🔊 Heavy 808 Sub-Bass Weight</span>
          <span class="flavor-chip" onclick="toggleFlavor(this, 'drunk J Dilla swing, unquantized human pocket, ghost notes')">🥁 Drunk Dilla Swing &amp; Ghost Notes</span>
          <span class="flavor-chip" onclick="toggleFlavor(this, 'double-time 32nd-note vocal chopper fill, virtuosic articulation')">⚡ 32nd-Note Chopper Virtuosity</span>
        </div>

        <div class="combined-prompt-bar">
          <div style="flex:1; min-width:240px;">
            <div style="font-size:10.5px; color:var(--text-muted); text-transform:uppercase; font-weight:800;">Combined Ready-to-Paste Suno Style Prompt</div>
            <div style="font-family:var(--font-mono); font-size:12.5px; color:var(--accent-orig); font-weight:700; margin-top:4px;" id="combinedStyleOut">90s underground boom-bap hip-hop, live human beatbox percussion, vocal bassline 808 sub-kicks, turntablism vinyl record scratches, raw vocal scatting, punchy dry close-mic vocals, 85 BPM</div>
          </div>
          <button type="button" class="btn-primary" onclick="copyText('combinedStyleOut', this)">📋 Copy Combined Style Prompt</button>
        </div>
      </section>

      <section class="surface-card">
        <header class="card-header">
          <div>
            <div class="eyebrow-row">
              <span class="window-badge">4 PHONETIC &amp; IPA LYRIC FORMATS</span>
              <span class="window-Range-pill">Copy-paste directly into Suno or linguistic documentation</span>
            </div>
            <h2 class="card-title">Copy-Paste Phonetic Lyrics &amp; Pure Narrow/Broad IPA Blocks</h2>
          </div>
        </header>

        <div class="lyrics-grid">
          <div class="lyric-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong style="color:var(--accent-orig); font-size:14px;">1. Suno Pronunciation-Engineered Phonetic Lyrics</strong>
              <button type="button" class="btn-primary" onclick="copyText('lyric-v1', this)">Copy V1 (Suno EN)</button>
            </div>
            <pre class="suno-box" id="lyric-v1">[Intro: Close-Mic Mouth Percussion, Swung 16th-Note Scat Pocket, 103 BPM]
(pff)
thuh-BITCH! camp, brah!
thuh-rup in thuh PANT, thence!
bup-uh-guh-KAH, pump!
thuh-frup in thuh fup-it, at ALLLL!
[Stop]

[Verse 1: Sub-Bass Hum &amp; Syncopated Cork-Pop Scat Groove, 96 BPM]
Mmmmm-mp! (huff)
thuh-cup-uh, thuh-PINK, caaane!
tuh-rip in thuh, KI-'in!
bick in thuh BOW, fen!
tuh-SICK in thuh-kuh-lip in NOWWW!
(deep gasp)

[Chorus: Funk Horn-Stab Call and Response &amp; Falsetto Squeak, 112 BPM]
You know what?!
BOW! buh-BOW! BOW! BOWWW!
You know what, now!
You know what, now!
You know what, then!
You know what, WHENNN?! [High Falsetto Squeak]

[Bridge: 32nd-Note Drum Roll &amp; Double-Tongue Vocal Chopper Fill, 128 BPM]
You know what—
thuh-buh-chuh-kuh-buh-GAHHH!
ski-bi-di-BAHHH!
buh-lip-uh-gih, buh-lep-uh-DAHHH!

[Drop: Heavy Halftime 808 Beatbox Groove &amp; Vocal Hooks, 84 BPM]
FWOOO-BWAHHH!
boo-buh-boo — SHIP it DOWN!
BOOSH! boom-buh-boom — TAKE it DOWN!
Boom, ts, boom-buh-boom — rrr-RIGHT uh-ROUND!
Boom, ts, boom-buh-boom — Hhh-RA-hh-RAAAH! [Turntable Vinyl Scratch]

[Outro: Throat Scrape Breakdown &amp; Staccato Coda Tag]
(kxhh-hrrr)
[1 Second Silence]
Duh-rip-it-NOWWW! (pff-tick)</pre>
          </div>

          <div class="lyric-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong style="color:#fde047; font-size:14px;">2. Pure Narrow IPA (`[ ... ]` Only — Articulatory Transcription)</strong>
              <button type="button" class="btn-primary" onclick="copyText('lyric-v2', this)">Copy V2 (Narrow IPA)</button>
            </div>
            <pre class="suno-box" id="lyric-v2">[p͡f˺]
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
[p˺ t˺]</pre>
          </div>

          <div class="lyric-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong style="color:var(--accent-emerald); font-size:14px;">3. Pure Broad IPA (`/ ... /` Only — Clean Phonemic)</strong>
              <button type="button" class="btn-primary" onclick="copyText('lyric-v3', this)">Copy V3 (Broad IPA)</button>
            </div>
            <pre class="suno-box" id="lyric-v3">/ðə bɪtʃ kæmp bɹɑ/
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
/də ɹɪp ɪt naʊ/</pre>
          </div>

          <div class="lyric-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong style="color:#f472b6; font-size:14px;">4. Tri-Tier Score (`EN` + `Narrow IPA` + `Musical Rhythm`)</strong>
              <button type="button" class="btn-primary" onclick="copyText('lyric-v4', this)">Copy V4 (Tri-Tier)</button>
            </div>
            <pre class="suno-box" id="lyric-v4"># PHRASE 1 (Bars 1–2 | 4/4 @ 103 BPM | Swung 16th Pocket)
EN : [lip-prep] thuh-bitch  camp   brah  | thuh-rup in thuh pant  thence | bup-uh-guh-kah pump
IPA: [p͡f˺]      [ðə ˈbɪtʃ] [ˈkʰæmp̚] [ˈbɹɑː] | [ðə ˈɹʌp̚ ɪn ðə ˈpʰænt̚ ˈðɛns] | [ˈbʌp̚ ə ɡə ˈkʰɑː pʌmp̚]
RHY:  [♪rest]     ♬   ♬      ♬      ♬     |  ♬   ♬·  ♬  ♬   ♪     ♪      |  ♬   ♬ ♬  ♬    ♬

# PHRASE 2 (Bars 3–5 | 2/4 -&gt; 4/4 @ 96 BPM | Sub-Hum &amp; Cork-Pop Groove)
EN : Mmmm!   [breath] | thuh-cup-uh thuh-pink cane  | tuh-rip in thuh ki  'in
IPA: [ˈmːˀp] [h̥ː]     | [ðə ˈkʰʌp̚ ə ðə ˈpʰɪŋk̚ ˈkʰeɪn] | [tʰə ˈɹɪp̚ ɪn ðə ˈkʰɪ ˈʔɪn]
RHY:  ♩—      [♩rest] |  ♬   ♬   ♬  ♬   ♪     ♩     |  ♬   ♬   ♬  ♬  ♪   ♪

# PHRASE 3A–3D (Bars 6–9 | 4/4 @ 112–131 BPM | Horn Stabs &amp; 32nd Chopper)
EN : You know what -&gt; BOW! buh-BOW! BOW! BOWWW! | thuh-buh-chuh-kuh-buh-GAH! | ski-bi-di-BAH!
IPA: [ju ˈnoʊ ˈwʌt̚]  [ˈbaʊ bə ˈbaʊ ˈbaʊ ˈbaʊː] | [ðə  bə  tʃə  kʰə bə ˈɡɑː] | [ˈskɪ bɪ dɪ ˈbɑː]
RHY:  ♬   ♬    ♬      ♪·   ♬   ♪    ♪    ♩      |  ♬   ♬   ♬    ♬   ♬   ♩    |  ♪³  ♪³ ♪³  ♩·

# PHRASE 4–5 (Bars 10–15 | 4/4 @ 83.5 BPM | 808 Beatbox &amp; DJ Scratch)
EN : Boom - ts  - boom - buh - boom | Hhh - RA  - hh - RA!   | Duh - rip - it - NOW!
IPA: [ˈbuːm t͡sʰ   ˈbuːm  bə   ˈbuːm]| [χː   ˈʀæ   χ   ˈʀæː] | [də  ˈɹɪp̚  ˈɪt̚  ˈnaʊ]
RHY:  ♪·    ♬     ♪·     ♬     ♩    |  ♬     ♬    ♬    ♩     |  ♬    ♬     ♬    ♩</pre>
          </div>
        </div>
      </section>
    </div>

    <!-- =================================================================== -->
    <!-- WORKSPACE 4: MUSICAL RHYTHM, SEQUENCER GRID & NARROW IPA GUIDE      -->
    <!-- =================================================================== -->
    <div class="ws-pane" id="pane-rhythm">
      <section class="surface-card">
        <header class="card-header">
          <div>
            <div class="eyebrow-row">
              <span class="window-badge">MUSICAL RHYTHM &amp; DRUM-STAFF ARCHITECTURE</span>
              <span class="window-Range-pill">5 Distinct Rhythmic Feels · 16-Step Sequencer Grid · Formant Vowel Space</span>
            </div>
            <h2 class="card-title">Tempo Curve, Note-Value Census, 16-Step Drum-Machine Grid &amp; Narrow IPA Guide</h2>
          </div>
        </header>

        <div class="figure-frame" onclick="openLightbox('rhy_ov', 'Musical Rhythm Architecture &amp; Tempo Curve')">
          <img id="img-rhy_ov" src="{asset_urls['rhy_ov']}" alt="Musical Rhythm Overview" loading="lazy" />
          <div class="figure-zoom-hint">🔍 Click to expand rhythm architecture</div>
        </div>

        <div class="figure-frame" style="margin-top:14px;" onclick="openLightbox('rhy_seq', '16-Step Drum-Machine Sequencer Grid')">
          <img id="img-rhy_seq" src="{asset_urls['rhy_seq']}" alt="16-Step Sequencer Grid" loading="lazy" />
          <div class="figure-zoom-hint">🔍 Click to expand 16-step sequencer grid</div>
        </div>

        <div class="figure-frame" style="margin-top:14px;" onclick="openLightbox('dash', 'F1-F2 Formant Vowel Space &amp; Drum-Kit Mapping')">
          <img id="img-dash" src="{asset_urls['dash']}" alt="Formant Acoustic Space" loading="lazy" />
          <div class="figure-zoom-hint">🔍 Click to expand formant acoustic space</div>
        </div>

        <div class="section-sublabel" style="margin-top:20px;">🔬 What Is Narrow IPA (`[ ... ]`) vs. Broad IPA (`/ ... /`) in Vocal Percussion?</div>
        <div class="table-scroll">
          <table class="studio-table" style="white-space:normal;">
            <thead>
              <tr>
                <th>Narrow IPA Diacritic</th>
                <th>Linguistic Name</th>
                <th>Vocal-Tract Drum-Machine / Synthesizer Mechanics</th>
                <th>Examples in `IMG_3268`</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code class="ipa-code">[pʰ, tʰ, kʰ]</code> (<code>ʰ</code>)</td>
                <td><strong>Aspirated release</strong></td>
                <td>High-velocity burst of unvoiced air after stop closure → <strong>crisp hi-hat / snare brush transient</strong></td>
                <td><code>[ˈpʰɪŋk̚]</code> (<em>pink</em>), <code>[ˈtʰɪk̚]</code> (<em>take</em>)</td>
              </tr>
              <tr>
                <td><code class="ipa-code">[p̚, t̚, k̚]</code> (<code>̚</code>)</td>
                <td><strong>Unreleased stop (clamp)</strong></td>
                <td>Lips/tongue clamp shut at the end of the syllable without releasing air → <strong>instant noise-gate / choked drum hit</strong></td>
                <td><code>[ˈkʰæmp̚]</code> (<em>camp</em>), <code>[ˈɹɪp̚ ˈɪt̚]</code> (<em>rip it</em>)</td>
              </tr>
              <tr>
                <td><code class="ipa-code">[ʔ]</code></td>
                <td><strong>Glottal stop</strong></td>
                <td>Vocal folds slam shut in <code>2 ms</code> → <strong>dry woodblock / rim click / cork pop</strong></td>
                <td><code>[ˈʔɪn]</code> (<em>'in</em> at <code>08.46s</code>)</td>
              </tr>
              <tr>
                <td><code class="ipa-code">[t͡sʰ, p͡f˺]</code> (<code>͡</code>)</td>
                <td><strong>Affricate tie-bar</strong></td>
                <td>Stop released directly into a narrow sibilant channel → <strong>metallic closed hi-hat (<code>ts</code>)</strong></td>
                <td><code>[t͡sʰ]</code> (<em>ts</em> at <code>28.92s</code>, <code>31.84s</code>)</td>
              </tr>
              <tr>
                <td><code class="ipa-code">[χ, ʀ]</code></td>
                <td><strong>Uvular fricative &amp; trill</strong></td>
                <td>Back of tongue vibrates against uvula while jaw sweeps open → <strong>DJ turntable vinyl record scratch</strong></td>
                <td><code>[χː ˈʀæ]</code> (<em>Hhh-RA!</em> at <code>33.08s</code>)</td>
              </tr>
              <tr>
                <td><code class="ipa-code">[ɪ̃, ↑]</code> (<code>̃, ↑</code>)</td>
                <td><strong>Nasalized vowel &amp; upstep</strong></td>
                <td>Velum lowers while larynx jumps to <code>500 Hz</code> falsetto → <strong>pinched synth lead squeak</strong></td>
                <td><code>[ˈwɪ̃n↑]</code> (<em>WHEN!↑</em> at <code>17.75s</code>)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

    <!-- =================================================================== -->
    <!-- WORKSPACE 5: SEARCHABLE 147-EVENT MASTER CORPUS TABLE               -->
    <!-- =================================================================== -->
    <div class="ws-pane" id="pane-corpus">
      <section class="surface-card">
        <header class="card-header">
          <div>
            <div class="eyebrow-row">
              <span class="window-badge">COMPLETE 147-EVENT ANNOTATED CORPUS</span>
              <span class="window-Range-pill" id="corpusCountLabel">Showing 147 / 147 events</span>
            </div>
            <h2 class="card-title">Interactive Searchable &amp; Filterable Master Event Table</h2>
          </div>
          <div class="card-header-actions">
            <input type="search" class="search-input" id="corpusSearchInput" placeholder="Search syllable, IPA, category, bar..." oninput="applyCorpusFilter()" />
          </div>
        </header>

        <div class="win-filter-bar" style="margin-bottom:14px;">
          {''.join(cat_pills)}
        </div>

        <div class="table-scroll">
          <table class="studio-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Time Range</th>
                <th>Bar · Grid (BPM)</th>
                <th>Rhythm</th>
                <th>English</th>
                <th>Narrow IPA</th>
                <th>Category</th>
                <th>Articulator</th>
                <th>Peak (ATK)</th>
                <th>F0 · F1/F2/F3</th>
                <th>Musical / Percussive Purpose</th>
              </tr>
            </thead>
            <tbody id="masterCorpusBody">
              {''.join(master_rows)}
            </tbody>
          </table>
        </div>
      </section>
    </div>

  </main>
</div>

<!-- Full-Resolution Image Lightbox Modal -->
<div class="lightbox-backdrop" id="lightboxModal" onclick="closeLightbox(event)">
  <div class="lightbox-top" onclick="event.stopPropagation()">
    <strong id="lightboxTitle" style="font-size:15px;">Diagram Preview</strong>
    <button type="button" class="btn-secondary" onclick="closeLightbox()">✕ Close (Esc)</button>
  </div>
  <div class="lightbox-img-wrap" onclick="event.stopPropagation()">
    <img id="lightboxImg" src="" alt="Full resolution preview" />
  </div>
</div>

<script>
const IS_PORTABLE_B64 = {json.dumps(is_portable_b64)};
const EVENTS = {json.dumps(events)};
const WINDOWS = {json.dumps(windows_meta)};
const CAT_COLORS = {json.dumps(CAT_COLORS)};

const media = document.getElementById('mainMedia');
const origAbAudio = document.getElementById('origAbAudio');
const sunoAudio = document.getElementById('sunoAbAudio');

let activeSource = 'video';
let stopAt = null;
let lastSliceStart = 0;
let lastSliceEnd = null;
let loopSlice = false;
let autoScroll = false;
let lastWinId = null;
let currentEventIdx = 1;
let selectedBaseIdx = 0;
let activeCorpusCat = 'ALL';
const activeFlavors = new Set();

// Convert Base64 data URIs to fast in-memory Blob ObjectURLs in portable mode so video/audio seeking has zero lag
function b64DataUriToBlobUrl(dataUri) {{
  if (!dataUri || !dataUri.startsWith('data:')) return dataUri;
  const parts = dataUri.split(',');
  const mimeMatch = parts[0].match(/:(.*?);/);
  const mime = mimeMatch ? mimeMatch[1] : 'application/octet-stream';
  const binStr = atob(parts[1]);
  const len = binStr.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) bytes[i] = binStr.charCodeAt(i);
  return URL.createObjectURL(new Blob([bytes], {{ type: mime }}));
}}

const FAST_URLS = {{
  video: IS_PORTABLE_B64 ? b64DataUriToBlobUrl(media.getAttribute('src')) : media.getAttribute('src'),
  orig: IS_PORTABLE_B64 ? b64DataUriToBlobUrl(origAbAudio.getAttribute('src')) : origAbAudio.getAttribute('src'),
  suno: IS_PORTABLE_B64 ? b64DataUriToBlobUrl(sunoAudio.getAttribute('src')) : sunoAudio.getAttribute('src'),
}};

if (IS_PORTABLE_B64) {{
  media.src = FAST_URLS.video;
  origAbAudio.src = FAST_URLS.orig;
  sunoAudio.src = FAST_URLS.suno;
}}

function switchMonitorSource(srcKey) {{
  const curTime = media.currentTime || 0;
  const wasPlaying = !media.paused;
  activeSource = srcKey;
  document.querySelectorAll('.src-tab').forEach(b => b.classList.remove('active'));
  const tabBtn = document.getElementById('srctab-' + srcKey);
  if (tabBtn) tabBtn.classList.add('active');

  media.src = FAST_URLS[srcKey];
  media.currentTime = Math.min(curTime, srcKey === 'suno' ? 89.0 : 37.8);
  if (wasPlaying) media.play();
}}

function switchWorkspace(paneId, btnEl) {{
  document.body.classList.remove('show-all-panes');
  const showAllBtn = document.getElementById('btnShowAllPanes');
  if (showAllBtn) {{
    showAllBtn.classList.remove('on');
    showAllBtn.textContent = '📑 View All on One Page: OFF';
  }}
  document.querySelectorAll('.ws-pane').forEach(p => p.classList.toggle('active', p.id === paneId));
  document.querySelectorAll('.ws-tab').forEach(b => b.classList.toggle('active', b === btnEl));
  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

function toggleShowAllPanes() {{
  const isAll = document.body.classList.toggle('show-all-panes');
  const btn = document.getElementById('btnShowAllPanes');
  if (btn) {{
    btn.classList.toggle('on', isAll);
    btn.textContent = '📑 View All on One Page: ' + (isAll ? 'ON' : 'OFF');
  }}
}}

function filterZoomWindow(winId, btnEl) {{
  document.querySelectorAll('#pane-microscope .win-filter-pill').forEach(b => b.classList.toggle('active', b === btnEl));
  document.querySelectorAll('.zoom-window-card').forEach(card => {{
    card.style.display = (winId === 'all' || card.id === winId) ? '' : 'none';
  }});
  if (winId !== 'all') {{
    const wObj = WINDOWS.find(w => w.id === winId);
    if (wObj) {{
      stopAt = null;
      media.currentTime = wObj.start;
    }}
  }}
}}

function playSlice(s, e) {{
  origAbAudio.pause();
  sunoAudio.pause();
  if (activeSource === 'suno' && e <= 37.85) {{
    switchMonitorSource('video');
  }}
  lastSliceStart = s;
  lastSliceEnd = e;
  stopAt = e;
  media.currentTime = s;
  media.play();
}}

function playEventByIdx(idx) {{
  const ev = EVENTS.find(x => x.idx === idx);
  if (!ev) return;
  currentEventIdx = idx;
  updateHudFromEvent(ev);
  playSlice(ev.start, ev.end);
}}

function stepEvent(delta) {{
  const nextIdx = Math.max(1, Math.min(EVENTS.length, currentEventIdx + delta));
  playEventByIdx(nextIdx);
}}

function togglePlayPause() {{
  if (media.paused) {{
    stopAt = null;
    media.play();
  }} else {{
    media.pause();
  }}
}}

function setSpeed(rate, btnEl) {{
  media.playbackRate = rate;
  origAbAudio.playbackRate = rate;
  sunoAudio.playbackRate = rate;
  document.querySelectorAll('.speed-btn').forEach(b => b.classList.toggle('active', b === btnEl));
}}

function toggleLoopSlice() {{
  loopSlice = !loopSlice;
  const btn = document.getElementById('btnLoopSlice');
  btn.classList.toggle('on', loopSlice);
  btn.textContent = '🔁 Loop Slice: ' + (loopSlice ? 'ON' : 'OFF');
}}

function toggleAutoScroll() {{
  autoScroll = !autoScroll;
  const btn = document.getElementById('btnScroll');
  btn.classList.toggle('on', autoScroll);
  btn.textContent = '📜 Auto-Follow: ' + (autoScroll ? 'ON' : 'OFF');
}}

let origStopAt = null;
let sunoStopAt = null;

function playOrigAb(s, e) {{
  media.pause();
  sunoAudio.pause();
  origStopAt = e;
  origAbAudio.currentTime = s;
  origAbAudio.play();
}}

function playSunoAb(s, e) {{
  media.pause();
  origAbAudio.pause();
  sunoStopAt = e;
  sunoAudio.currentTime = s;
  sunoAudio.play();
}}

origAbAudio.addEventListener('timeupdate', () => {{
  if (origStopAt !== null && origAbAudio.currentTime >= origStopAt) {{
    origAbAudio.pause();
    origStopAt = null;
  }}
}});

sunoAudio.addEventListener('timeupdate', () => {{
  if (sunoStopAt !== null && sunoAudio.currentTime >= sunoStopAt) {{
    sunoAudio.pause();
    sunoStopAt = null;
  }}
}});

function selectBaseStyle(idx) {{
  selectedBaseIdx = idx;
  for (let i = 0; i < 6; i++) {{
    const el = document.getElementById('scard-' + i);
    if (el) el.classList.toggle('selected', i === idx);
  }}
  updateCombinedPrompt();
}}

function toggleFlavor(chipEl, flavorText) {{
  if (activeFlavors.has(flavorText)) {{
    activeFlavors.delete(flavorText);
    chipEl.classList.remove('on');
  }} else {{
    activeFlavors.add(flavorText);
    chipEl.classList.add('on');
  }}
  updateCombinedPrompt();
}}

function updateCombinedPrompt() {{
  const baseEl = document.getElementById('sprompt-' + selectedBaseIdx);
  const baseText = baseEl ? baseEl.textContent.trim() : '';
  const extras = Array.from(activeFlavors);
  const combined = extras.length ? (baseText + ', ' + extras.join(', ')) : baseText;
  document.getElementById('combinedStyleOut').textContent = combined;
}}

function copyText(elemId, btnEl) {{
  const el = document.getElementById(elemId);
  if (!el) return;
  navigator.clipboard.writeText(el.textContent.trim());
  const old = btnEl.textContent;
  btnEl.textContent = '✓ Copied!';
  setTimeout(() => {{ btnEl.textContent = old; }}, 1400);
}}

function filterCorpusCat(cat, btnEl) {{
  activeCorpusCat = cat;
  document.querySelectorAll('#pane-corpus .win-filter-pill').forEach(b => b.classList.toggle('active', b === btnEl));
  applyCorpusFilter();
}}

function applyCorpusFilter() {{
  const q = (document.getElementById('corpusSearchInput').value || '').trim().toLowerCase();
  let visible = 0;
  document.querySelectorAll('.master-ev-row').forEach(row => {{
    const matchCat = (activeCorpusCat === 'ALL' || row.dataset.cat === activeCorpusCat);
    const matchQ = (!q || row.dataset.search.includes(q));
    const show = matchCat && matchQ;
    row.style.display = show ? '' : 'none';
    if (show) visible++;
  }});
  document.getElementById('corpusCountLabel').textContent = `Showing ${{visible}} / ${{EVENTS.length}} events`;
}}

function openLightbox(imgKey, titleText) {{
  const imgEl = document.getElementById('img-' + imgKey);
  if (!imgEl) return;
  document.getElementById('lightboxImg').src = imgEl.src;
  document.getElementById('lightboxTitle').textContent = titleText;
  document.getElementById('lightboxModal').classList.add('open');
}}

function closeLightbox(ev) {{
  if (ev && ev.target && ev.target.id !== 'lightboxModal') return;
  document.getElementById('lightboxModal').classList.remove('open');
}}

function renderSectionScore(winObj, activeIdx) {{
  const container = document.getElementById('hudSectionScore');
  if (!winObj) return;
  document.getElementById('hudWinLabel').textContent = winObj.id.toUpperCase() + ` (${{winObj.start.toFixed(1)}}–${{winObj.end.toFixed(1)}}s)`;
  const evs = EVENTS.filter(e => winObj.events.includes(e.idx));
  container.innerHTML = evs.map(e => {{
    const isCur = (e.idx === activeIdx);
    const col = CAT_COLORS[e.cat] || '#64748b';
    return `<div class="score-note-pill ${{isCur ? 'current' : ''}}" id="spill-${{e.idx}}" style="border-color:${{isCur ? '#f59e0b' : col}}" onclick="playEventByIdx(${{e.idx}})">
      <span class="sn-rhy">${{e.note_sym}} ${{e.syl}}</span>
      <span class="sn-ipa">[${{e.ipa}}] · ${{e.grid_pos}}</span>
    </div>`;
  }}).join('');
  const activePill = document.getElementById('spill-' + activeIdx);
  if (activePill) {{
    activePill.scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
  }}
}}

function updateHudFromEvent(hit) {{
  const col = CAT_COLORS[hit.cat] || '#38bdf8';
  document.getElementById('hudBar').textContent = `Bar ${{String(hit.bar_num).padStart(2,'0')}} (${{hit.time_sig}} @ ${{hit.local_bpm}} BPM)`;
  document.getElementById('hudGrid').textContent = `Grid: ${{hit.grid_pos}}`;
  document.getElementById('hudCat').textContent = hit.cat;
  document.getElementById('hudCat').style.color = col;
  document.getElementById('hudArt').textContent = hit.art;
  document.getElementById('hudRhyShort').textContent = `${{hit.note_short}} (IOI ${{hit.ioi_ms}}ms)`;
  document.getElementById('hudPkAtk').textContent = `${{hit.pk_db}} dB / ${{hit.atk_ms}}ms`;
  const f0Str = hit.f0 ? `${{Math.round(hit.f0)}}Hz` : 'Unv';
  document.getElementById('hudFormants').textContent = `${{f0Str}} · ${{hit.f1 || '—'}}/${{hit.f2 || '—'}}/${{hit.f3 || '—'}} Hz`;
  document.getElementById('hudNoteSym').textContent = hit.note_sym;
  document.getElementById('hudSyl').textContent = `#${{String(hit.idx).padStart(3,'0')}} ${{hit.syl}}`;
  document.getElementById('hudSyl').style.color = col;
  document.getElementById('hudIpa').textContent = `[${{hit.ipa}}]`;

  const win = WINDOWS.find(w => w.events.includes(hit.idx));
  if (win) renderSectionScore(win, hit.idx);

  document.querySelectorAll('.syl-chip.active, .ev-row.active, .raw-bracket-item.active').forEach(el => el.classList.remove('active'));
  const chip = document.getElementById('chip-' + hit.idx);
  if (chip) chip.classList.add('active');
  const wrow = document.getElementById('wrow-' + hit.idx);
  if (wrow) wrow.classList.add('active');
  const mrow = document.getElementById('mrow-' + hit.idx);
  if (mrow) mrow.classList.add('active');
  const line = document.getElementById('line-' + hit.idx);
  if (line) line.classList.add('active');
}}

media.addEventListener('timeupdate', () => {{
  const t = media.currentTime;
  const dur = media.duration || 37.82;
  document.getElementById('hudTime').textContent = `${{t.toFixed(2)}}s / ${{dur.toFixed(2)}}s`;

  if (stopAt !== null && t >= stopAt) {{
    if (loopSlice && lastSliceEnd !== null) {{
      media.currentTime = lastSliceStart;
      media.play();
      return;
    }} else {{
      media.pause();
      stopAt = null;
    }}
  }}

  const hit = EVENTS.find(x => t >= x.start && t <= x.end);
  if (hit && hit.idx !== currentEventIdx) {{
    currentEventIdx = hit.idx;
    updateHudFromEvent(hit);

    const win = WINDOWS.find(w => t >= w.start && t <= w.end);
    if (autoScroll && win && win.id !== lastWinId) {{
      lastWinId = win.id;
      const el = document.getElementById(win.id);
      if (el && el.offsetParent !== null) {{
        el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      }}
    }}
  }}
}});

// Global Keyboard Shortcuts
document.addEventListener('keydown', (e) => {{
  if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
  if (e.key === 'Escape') {{
    closeLightbox();
    return;
  }}
  if (e.code === 'Space') {{
    e.preventDefault();
    togglePlayPause();
  }} else if (e.key === 'ArrowRight') {{
    e.preventDefault();
    stepEvent(1);
  }} else if (e.key === 'ArrowLeft') {{
    e.preventDefault();
    stepEvent(-1);
  }} else if (e.key === 'l' || e.key === 'L') {{
    toggleLoopSlice();
  }} else if (e.key >= '1' && e.key <= '5') {{
    const idx = parseInt(e.key, 10) - 1;
    const tabs = document.querySelectorAll('.ws-tab');
    if (tabs[idx]) tabs[idx].click();
  }}
}});

// Initialize HUD with Event #1
if (EVENTS.length > 0) {{
  updateHudFromEvent(EVENTS[0]);
}}
</script>
</body>
</html>
"""


def main() -> None:
    events = json.loads((OUT_DIR / "micro_events_138.json").read_text())

    # 1. Write standalone WebVTT file
    vtt_text = build_webvtt(events, ZOOM_WINDOWS)
    vtt_path = OUT_DIR / "IMG_3268_phonetic_rhythm.vtt"
    vtt_path.write_text(vtt_text, encoding="utf-8")
    vtt_b64 = base64.b64encode(vtt_text.encode("utf-8")).decode("ascii")
    print(f"Wrote WebVTT subtitle track ({len(events)} cues) -> {vtt_path.name}")

    # 2. Ensure web-optimized MP4 and burned-in HUD MP4 exist
    web_mp4_path = OUT_DIR / "IMG_3268_web_portable.mp4"
    if not web_mp4_path.exists():
        subprocess.run([
            "ffmpeg", "-y", "-i", str(MP4_PATH),
            "-vf", "scale=-2:720,format=yuv420p",
            "-c:v", "libx264", "-preset", "fast", "-crf", "25",
            "-c:a", "aac", "-b:a", "160k",
            "-movflags", "+faststart",
            str(web_mp4_path)
        ], check=True)
    subtitled_mp4_path = OUT_DIR / "IMG_3268_subtitled_phonetic_rhythm.mp4"

    # Build window metadata
    windows_meta = []
    for z_id, title, zs, ze in ZOOM_WINDOWS:
        ev_sub = [ev for ev in events if ev["start"] >= zs - 0.01 and ev["end"] <= ze + 0.02]
        windows_meta.append({
            "id": z_id,
            "title": title,
            "start": zs,
            "end": ze,
            "events": [ev["idx"] for ev in ev_sub],
        })

    # 3. Build Fast-Loading GitHub Pages `index.html` (relative asset URLs)
    gh_urls = {
        "web_mp4": "./analysis/IMG_3268_web_portable.mp4",
        "vtt": "./analysis/IMG_3268_phonetic_rhythm.vtt",
        "orig_mp3": "./IMG_3268.mp3",
        "suno_mp3": "./IMG_3268%20SUNO.mp3",
        "suno_comp": "./analysis/fig_suno_vs_orig_comparison.png",
        "suno_sheet": "./analysis/IMG_3268_SUNO_sheet.png",
        "orig_sheet": "./analysis/IMG_3268_sheet.png",
        "dash": "./analysis/fig0_phonetic_acoustic_space.png",
        "rhy_ov": "./analysis/fig_rhythm_overview.png",
        "rhy_seq": "./analysis/fig_rhythm_sequencer_grid.png",
    }
    for z_id, _, _, _ in ZOOM_WINDOWS:
        gh_urls[z_id] = f"./analysis/{z_id}.png"

    gh_html = render_html_document(events, windows_meta, gh_urls, is_portable_b64=False)
    index_path = WORKSPACE / "index.html"
    index_path.write_text(gh_html, encoding="utf-8")
    print(f"Wrote fast-loading GitHub Pages app: {index_path} ({index_path.stat().st_size / 1024:.1f} KB)")

    # 4. Build 100% Self-Contained Offline Portable HTML (`analysis/IMG_3268_phonetic_report.html`)
    b64_urls = {
        "web_mp4": "data:video/mp4;base64," + base64.b64encode(web_mp4_path.read_bytes()).decode("ascii"),
        "vtt": "data:text/vtt;base64," + vtt_b64,
        "orig_mp3": "data:audio/mpeg;base64," + base64.b64encode(MP3_PATH.read_bytes()).decode("ascii"),
        "suno_mp3": "data:audio/mpeg;base64," + base64.b64encode(SUNO_MP3_PATH.read_bytes()).decode("ascii"),
        "suno_comp": "data:image/png;base64," + base64.b64encode((OUT_DIR / "fig_suno_vs_orig_comparison.png").read_bytes()).decode("ascii"),
        "suno_sheet": "data:image/png;base64," + base64.b64encode((OUT_DIR / "IMG_3268_SUNO_sheet.png").read_bytes()).decode("ascii"),
        "orig_sheet": "data:image/png;base64," + base64.b64encode((OUT_DIR / "IMG_3268_sheet.png").read_bytes()).decode("ascii"),
        "dash": "data:image/png;base64," + base64.b64encode((OUT_DIR / "fig0_phonetic_acoustic_space.png").read_bytes()).decode("ascii"),
        "rhy_ov": "data:image/png;base64," + base64.b64encode((OUT_DIR / "fig_rhythm_overview.png").read_bytes()).decode("ascii"),
        "rhy_seq": "data:image/png;base64," + base64.b64encode((OUT_DIR / "fig_rhythm_sequencer_grid.png").read_bytes()).decode("ascii"),
    }
    for z_id, _, _, _ in ZOOM_WINDOWS:
        b64_urls[z_id] = "data:image/png;base64," + base64.b64encode((OUT_DIR / f"{z_id}.png").read_bytes()).decode("ascii")

    portable_html = render_html_document(events, windows_meta, b64_urls, is_portable_b64=True)
    portable_path = OUT_DIR / "IMG_3268_phonetic_report.html"
    portable_path.write_text(portable_html, encoding="utf-8")
    print(f"Wrote 100% self-contained portable HTML: {portable_path.name} ({portable_path.stat().st_size / (1024*1024):.2f} MB)")


if __name__ == "__main__":
    main()
