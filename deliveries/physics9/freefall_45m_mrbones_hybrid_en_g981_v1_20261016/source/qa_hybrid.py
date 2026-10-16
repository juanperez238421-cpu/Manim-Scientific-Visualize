"""QA + evidence package for the hybrid video (protocol HYBRID-SCIANIM-v1 §9).

- full decode, ffprobe (1920x1080, 30/1, h264, yuv420p, expected duration)
- every clip starts and ends on a #FFFFFF frame (EDL); the cuts between engines are white
- audio: integrated loudness, true peak, clipping; physical cues located by cross-correlation
- contact sheet one frame every 5 s; SHA-256 of every clip and of the deliverables
- GitHub copy < 95 MiB and share copy < 30 MB (two-pass), each with its SHA-256
writes productions/caida-libre-hibrido/qa/{VIDEO_QA.txt, report.json, contact_sheet.png} and SHA256SUMS.txt

usage: .venv/bin/python productions/caida-libre-hibrido/tools/qa_hybrid.py
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "validate"))
import video_qa as V  # noqa: E402

QA = HERE / "qa"
BUILD = ROOT / "build" / "caida-libre-hibrido-en"
EDL = json.loads((QA / "EDL.json").read_text())
FINAL = ROOT / EDL["final"]
NAME = FINAL.stem
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    rep = {"file": str(FINAL.relative_to(ROOT)), "checks": {}}
    ok = True
    pr = V.ffprobe(FINAL)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = [s for s in pr["streams"] if s["codec_type"] == "audio"]
    nf = int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(FINAL)]).stdout.strip())
    exp = round(EDL["total_s"] * 30)
    tech = {"codec": v["codec_name"], "size": [v["width"], v["height"]], "fps": v["r_frame_rate"], "pix_fmt": v["pix_fmt"], "frames": nf, "expected_frames": exp,
            "duration_s": float(pr["format"]["duration"]), "audio": [(s["codec_name"], int(s["sample_rate"]), s["channels"]) for s in a], "bytes": FINAL.stat().st_size}
    dec = run(["ffmpeg", "-v", "error", "-i", str(FINAL), "-f", "null", "-"])
    t_ok = tech["codec"] == "h264" and tech["size"] == [1920, 1080] and tech["fps"] == "30/1" and tech["pix_fmt"] == "yuv420p" and nf == exp and not dec.stderr.strip() and len(a) == 1
    rep["checks"]["technical"] = {**tech, "decode_errors": dec.stderr.strip()[:300], "pass": t_ok}
    ok &= t_ok
    # white bookends at every cut
    wb = [(c["clip"], c["first_white"], c["last_white"]) for c in EDL["clips"]]
    w_ok = all(f and l for _, f, l in wb)
    rep["checks"]["white_cuts"] = {"clips": wb, "pass": w_ok}
    ok &= w_ok
    # audio
    eb = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(FINAL), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    tail = eb[eb.rfind("Summary:"):]
    I = float(re.search(r"I:\s+(-?[\d.]+) LUFS", tail).group(1))
    TP = float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", tail).group(1))
    x = V.decode_audio(FINAL)
    clip = int((np.abs(x) >= 0.9999).sum())
    cues = json.loads((BUILD / "audio" / "cue_sheet.json").read_text())["cues"]
    sync = []
    for c in cues:
        st = np.load(BUILD / "audio" / "stems" / f"{c['id'].replace('@', '_')}.npy")
        tm = V.xcorr_lag(x, 48000, st[: int(0.08 * 48000)], c["t"], search=0.04)
        sync.append({"cue": c["id"], "expected_s": c["t"], "measured_s": round(tm, 6), "offset_ms": round((tm - c["t"]) * 1000, 3)})
    a_ok = abs(I + 16) <= 1.0 and TP <= -1.0 and clip == 0 and all(abs(s["offset_ms"]) <= 5 for s in sync)
    rep["checks"]["audio"] = {"integrated_lufs": I, "true_peak_dbtp": TP, "clipped": clip, "sync": sync, "pass": a_ok}
    ok &= a_ok
    # physics QA (both engines)
    phys = json.loads((QA / "cartoon_physics_qa.json").read_text())
    rep["checks"]["physics_cartoon"] = {"pass": phys["pass"], "checks": phys["checks"]}
    ok &= phys["pass"]
    # contact sheet every 5 s
    times = [t + 2.5 for t in range(0, int(EDL["total_s"]) - 2, 5)]
    V.sheet(FINAL, times, QA / "contact_sheet.png", 8, 300, f"{NAME} — one frame every 5 s")
    # deliverable copies
    gh = ROOT / "output" / "final" / f"{NAME}_github.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(FINAL), "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(gh)])
    share = ROOT / "output" / "final" / f"{NAME}_share.mp4"
    dur = tech["duration_s"]
    vbr = int((28.5 * 8 * 1024 * 1024) / dur - 128_000)  # bits/s for ~28.5 MB total
    for p in (1, 2):
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(FINAL), "-c:v", "libx264", "-preset", "slow", "-b:v", str(vbr), "-pass", str(p), "-passlogfile", str(BUILD / "x264pass"), "-pix_fmt", "yuv420p"]
        cmd += (["-an", "-f", "mp4", "/dev/null"] if p == 1 else ["-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(share)])
        run(cmd)
    sizes = {"final_MiB": FINAL.stat().st_size / 2**20, "github_MiB": gh.stat().st_size / 2**20, "share_MB": share.stat().st_size / 1e6}
    s_ok = sizes["github_MiB"] < 95 and sizes["share_MB"] < 30
    rep["checks"]["sizes"] = {**sizes, "pass": s_ok}
    ok &= s_ok
    sums = {p.name: sha(p) for p in [FINAL, gh, share]}
    sums.update({f"clips/{c['clip']}.mp4": sha(BUILD / "clips" / f"{c['clip']}.mp4") for c in EDL["clips"]})
    (QA / "SHA256SUMS.txt").write_text("".join(f"{h}  {n}\n" for n, h in sums.items()))
    rep["sha256"] = sums
    rep["pass"] = bool(ok)
    (QA / "report.json").write_text(json.dumps(rep, indent=1))
    lines = [f"VIDEO QA — {NAME}", f"technical: {tech}", f"white cuts: {'PASS' if w_ok else 'FAIL'}", f"audio: I={I} LUFS, TP={TP} dBTP, clipped={clip}",
             "sync (ms): " + ", ".join(f"{s['cue']} {s['offset_ms']}" for s in sync), f"physics (cartoon): {'PASS' if phys['pass'] else 'FAIL'}",
             f"sizes: {sizes}", f"OVERALL: {'PASS' if ok else 'FAIL'}"]
    (QA / "VIDEO_QA.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
