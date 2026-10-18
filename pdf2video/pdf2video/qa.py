"""Video QA for a rendered solution video.

Gates:
  technical   h264, 1920x1080, 30 fps, yuv420p, no decode errors, duration > 0
  bookends    first and last frames are blank white (mean > 250, min > 200 on a downscaled frame)
  content     the render log (observed.json) shows: every given chip extracted at a located box,
              every answer value printed in its boxed result, every annotation inside the work area,
              and the spec validation passed
  package     share copy < 30 MB (two-pass if needed), SHA-256 of every deliverable, contact sheet
Writes <outdir>/qa.json and VIDEO_QA.txt.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

from .tools_sheet import sheet


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def probe(path):
    r = _run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
    return json.loads(r.stdout)


def frame_gray(path, t, w=192, h=108):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, t):.3f}", "-i", str(path), "-frames:v", "1", "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                       capture_output=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(h, w) if len(r.stdout) == w * h else None


def share_copy(src, dst, limit_mb=29.0):
    for crf in (23, 25, 27, 29):
        _run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", str(dst)])
        if Path(dst).stat().st_size / 1e6 < limit_mb:
            return crf
    return None


def run_qa(video, observed, validation, outdir, name):
    video, outdir = Path(video), Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rep = {"video": video.name, "checks": {}}
    pr = probe(video)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    dur = float(pr["format"]["duration"])
    dec = _run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"])
    tech = {"codec": v["codec_name"], "size": [v["width"], v["height"]], "fps": v["r_frame_rate"], "pix_fmt": v["pix_fmt"], "duration_s": round(dur, 2),
            "MB": round(video.stat().st_size / 1e6, 2), "decode_errors": dec.stderr.strip()[:300]}
    t_ok = tech["codec"] == "h264" and tech["size"] == [1920, 1080] and tech["fps"] == "30/1" and tech["pix_fmt"] == "yuv420p" and not tech["decode_errors"] and dur > 1
    rep["checks"]["technical"] = {**tech, "pass": bool(t_ok)}
    f0, f1 = frame_gray(video, 0.0), frame_gray(video, dur - 0.1)
    b_ok = f0 is not None and f1 is not None and f0.mean() > 250 and f1.mean() > 250 and f0.min() > 200 and f1.min() > 200
    rep["checks"]["bookends"] = {"first_mean": float(f0.mean()) if f0 is not None else None, "last_mean": float(f1.mean()) if f1 is not None else None, "pass": bool(b_ok)}
    obs = json.loads(Path(observed).read_text())["log"]
    val = json.loads(Path(validation).read_text())
    givens = [o for o in obs if o["kind"] == "given"]
    answers = [o for o in obs if o["kind"] == "answer"]
    anns = [o for o in obs if o["kind"] == "annotation"]
    c_ok = val["pass"] and all(o["boxes"] for o in givens) and all(o["in_tex"] for o in answers) and all(o["in_work_area"] for o in anns) and len(answers) > 0
    rep["checks"]["content"] = {"validation_pass": val["pass"], "givens_extracted": len(givens), "answers_shown": len(answers),
                                "answers_value_in_box": sum(o["in_tex"] for o in answers), "annotations": len(anns),
                                "annotations_in_work_area": sum(o["in_work_area"] for o in anns),
                                "answers": [{"problem": o["problem"], "name": o["name"], "value": o["value"], "shown": o["shown"]} for o in answers], "pass": bool(c_ok)}
    share = outdir / f"{name}_share.mp4"
    crf = share_copy(video, share)
    s_ok = crf is not None
    times = list(np.arange(2.0, dur - 1.0, max(6.0, (dur - 3) / 24)))[:25]
    sheet(video, times, outdir / "contact_sheet.png", 5, 384)
    sums = {p.name: sha256(p) for p in (video, share)}
    (outdir / "SHA256SUMS.txt").write_text("".join(f"{h}  {n}\n" for n, h in sums.items()))
    rep["checks"]["package"] = {"share_MB": round(share.stat().st_size / 1e6, 2), "share_crf": crf, "pass": bool(s_ok)}
    rep["sha256"] = sums
    rep["pass"] = bool(t_ok and b_ok and c_ok and s_ok)
    (outdir / "qa.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False))
    lines = [f"VIDEO QA — {video.name}",
             f"technical: {tech['codec']} {tech['size'][0]}x{tech['size'][1]} {tech['fps']} {tech['pix_fmt']}, {tech['duration_s']} s, {tech['MB']} MB, decode errors: {'none' if not tech['decode_errors'] else tech['decode_errors']}",
             f"bookends: first frame mean {rep['checks']['bookends']['first_mean']:.1f}, last frame mean {rep['checks']['bookends']['last_mean']:.1f} (white)",
             f"content: validation {'PASS' if val['pass'] else 'FAIL'}; {len(givens)} givens extracted at their page boxes; {rep['checks']['content']['answers_value_in_box']}/{len(answers)} answers shown with the recomputed value; "
             f"{rep['checks']['content']['annotations_in_work_area']}/{len(anns)} annotations inside the work area",
             f"share copy: {rep['checks']['package']['share_MB']} MB (crf {crf})",
             f"OVERALL: {'PASS' if rep['pass'] else 'FAIL'}"]
    (outdir / "VIDEO_QA.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return rep
