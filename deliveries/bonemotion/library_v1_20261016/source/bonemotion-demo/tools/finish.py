"""Finish the demo reel: mux the silent 60 fps master with the soundtrack, cut one clip per animation,
make the share / GitHub copies, and run the video QA.

  - technical: h264, 1920x1080, 60/1, yuv420p, frame count = duration x 60, no decode errors, one AAC track
  - audio: -16 LUFS +-1, true peak <= -1 dBTP, no clipping; sync cues located by cross-correlation (<= 5 ms)
  - per-animation clips: every segment cut frame-accurately (re-encoded), with its sound
  - contact sheet: two frames per animation
  - share copy < 30 MB (two-pass), GitHub copy < 95 MiB; SHA-256 of every deliverable
writes productions/bonemotion-demo/qa/{VIDEO_QA.txt, report.json, contact_sheet.png} and SHA256SUMS.txt

usage: .venv/bin/python productions/bonemotion-demo/tools/finish.py
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

BUILD = ROOT / "build" / "bonemotion-demo"
QA = HERE / "qa"
QA.mkdir(exist_ok=True)
OUTD = ROOT / "output" / "final" / "bonemotion"
OUTD.mkdir(parents=True, exist_ok=True)
NAME = "bonemotion_demo_reel_1080p60"
CUES = json.loads((BUILD / "cues.json").read_text())
FPS = 60
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2000:])
    return r


def main():
    master = BUILD / "master_silent.mp4"
    mix = BUILD / "audio" / "mix.wav"
    final = OUTD / f"{NAME}.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(master), "-i", str(mix), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-af", "apad", "-t", f"{round(CUES['total'] * FPS) / FPS:.6f}", "-movflags", "+faststart", str(final)])
    rep = {"file": str(final.relative_to(ROOT)), "checks": {}}
    ok = True
    pr = V.ffprobe(final)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = [s for s in pr["streams"] if s["codec_type"] == "audio"]
    nf = int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(final)]).stdout.strip())
    exp = round(CUES["total"] * FPS)
    dec = run(["ffmpeg", "-v", "error", "-i", str(final), "-f", "null", "-"])
    tech = {"codec": v["codec_name"], "size": [v["width"], v["height"]], "fps": v["r_frame_rate"], "pix_fmt": v["pix_fmt"], "frames": nf, "expected_frames": exp,
            "duration_s": float(pr["format"]["duration"]), "audio": [(s["codec_name"], int(s["sample_rate"]), s["channels"]) for s in a], "bytes": final.stat().st_size}
    t_ok = tech["codec"] == "h264" and tech["size"] == [1920, 1080] and tech["fps"] == "60/1" and tech["pix_fmt"] == "yuv420p" and abs(nf - exp) <= 1 and not dec.stderr.strip() and len(a) == 1
    rep["checks"]["technical"] = {**tech, "decode_errors": dec.stderr.strip()[:300], "pass": t_ok}
    ok &= t_ok
    # audio
    eb = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(final), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    tail = eb[eb.rfind("Summary:"):]
    I = float(re.search(r"I:\s+(-?[\d.]+) LUFS", tail).group(1))
    TP = float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", tail).group(1))
    x = V.decode_audio(final)
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
    # library QA (motion + neural) is part of the evidence
    mq = json.loads((ROOT / "packages" / "bonemotion" / "qa" / "motion_qa.json").read_text())
    nq = json.loads((ROOT / "packages" / "bonemotion" / "qa" / "neural_qa.json").read_text())
    rep["checks"]["motion_qa"] = {"clips": len(mq["clips"]), "pass": mq["pass"]}
    rep["checks"]["neural_qa"] = {"checks": nq["checks"], "pass": nq["pass"]}
    ok &= mq["pass"] and nq["pass"]
    # one clip per animation (frame-accurate cut, re-encoded)
    clips = []
    for s in CUES["segments"]:
        f0, f1 = round(s["t0"] * FPS), round((s["t0"] + s["dur"]) * FPS)
        out = OUTD / f"{s['num']}_{s['id']}.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(final), "-vf", f"trim=start_frame={f0}:end_frame={f1},setpts=PTS-STARTPTS",
             "-af", f"atrim=start={f0 / FPS}:end={f1 / FPS},asetpts=PTS-STARTPTS", "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)])
        n = int(run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(out)]).stdout.strip() or 0)
        clips.append({"file": out.name, "title": s["title"], "frames": n, "expected": f1 - f0, "MB": round(out.stat().st_size / 1e6, 2), "pass": n == f1 - f0})
    c_ok = all(c["pass"] for c in clips)
    rep["checks"]["clips"] = {"clips": clips, "pass": c_ok}
    ok &= c_ok
    # contact sheet: two frames per animation
    times = []
    for s in CUES["segments"]:
        times += [s["t0"] + 0.35 * s["dur"], s["t0"] + 0.7 * s["dur"]]
    V.sheet(final, times, QA / "contact_sheet.png", 7, 340, f"{NAME} — dos fotogramas por animación")
    # share + GitHub copies
    gh = OUTD / f"{NAME}_github.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(final), "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(gh)])
    share = OUTD / f"{NAME}_share.mp4"
    dur = tech["duration_s"]
    vbr = int((28.5 * 8 * 1024 * 1024) / dur - 128_000)
    for p in (1, 2):
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(final), "-c:v", "libx264", "-preset", "slow", "-b:v", str(vbr), "-pass", str(p), "-passlogfile", str(BUILD / "x264pass"), "-pix_fmt", "yuv420p"]
        cmd += (["-an", "-f", "mp4", "/dev/null"] if p == 1 else ["-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(share)])
        run(cmd)
    sizes = {"final_MiB": final.stat().st_size / 2**20, "github_MiB": gh.stat().st_size / 2**20, "share_MB": share.stat().st_size / 1e6}
    s_ok = sizes["github_MiB"] < 95 and sizes["share_MB"] < 30
    rep["checks"]["sizes"] = {**sizes, "pass": s_ok}
    ok &= s_ok
    sums = {p.name: sha(p) for p in [final, gh, share] + [OUTD / c["file"] for c in clips]}
    (QA / "SHA256SUMS.txt").write_text("".join(f"{h}  {n}\n" for n, h in sums.items()))
    rep["sha256"] = sums
    rep["pass"] = bool(ok)
    (QA / "report.json").write_text(json.dumps(rep, indent=1))
    lines = [f"VIDEO QA — {NAME}", f"technical: {tech}", f"audio: I={I} LUFS, TP={TP} dBTP, clipped={clip}",
             "sync (ms): " + ", ".join(f"{s['cue']} {s['offset_ms']}" for s in sync),
             f"motion QA: {'PASS' if mq['pass'] else 'FAIL'} ({len(mq['clips'])} clips)  neural QA: {'PASS' if nq['pass'] else 'FAIL'}",
             f"clips: {len(clips)} cut, frame counts {'exact' if c_ok else 'MISMATCH'}", f"sizes: {sizes}", f"OVERALL: {'PASS' if ok else 'FAIL'}"]
    (QA / "VIDEO_QA.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
