"""pdf2video command line.

  p2v analyze  <pdf> [--out DIR]            document IR + detected problems -> DIR/ir.json (input for the spec author)
  p2v validate <spec.json>                  every quote located, every number recomputed -> validation.json
  p2v render   <spec.json> [--name N] [--quality qh|qm|ql] [--problems 1,3]
  p2v qa       <spec.json> [--name N]       technical + content QA of the rendered video, share copy, SHA-256
  p2v run      <spec.json> [--name N]       validate -> render -> qa (stops at the first failing gate)
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _name(spec, name):
    return name or Path(spec).resolve().parent.name


def cmd_analyze(a):
    from .ir import Document
    from .segment import detect
    out = Path(a.out or Path(a.pdf).with_suffix("")).resolve()
    doc = Document(a.pdf, out / "work")
    probs = detect(doc)
    doc.save_json(out / "ir.json", probs)
    print(f"{Path(a.pdf).name}: {len(doc.pages)} page(s) [{', '.join(P.source for P in doc.pages)}], sha256 {doc.sha256[:12]}…, {len(probs)} problem(s)")
    for p in probs:
        print(f"  {p.id} (p{p.page}) {p.text[:110]}")
    print(f"IR written to {out / 'ir.json'}")
    return 0


def cmd_validate(a):
    from .validate import validate
    rep, _, _ = validate(a.spec, workdir=ROOT / "build" / _name(a.spec, a.name) / "work")
    out = ROOT / "build" / _name(a.spec, a.name)
    out.mkdir(parents=True, exist_ok=True)
    (out / "validation.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=str))
    return 0 if rep["pass"] else 2


def cmd_render(a):
    name = _name(a.spec, a.name)
    out = ROOT / "build" / name
    out.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "P2V_SPEC": str(Path(a.spec).resolve()), "P2V_OUT": str(out), "P2V_PROBLEMS": a.problems or ""}
    manim = shutil.which("manim", path=str(Path(sys.executable).parent)) or "manim"
    cmd = [manim, f"-{a.quality}", "--fps", str(a.fps), "--media_dir", str(out / "media"), "-o", name, str(ROOT / "pdf2video" / "render" / "scene.py"), "SolutionVideo"]
    with open(out / "render.log", "w") as log:
        r = subprocess.run(cmd, env=env, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT)
    if r.returncode:
        print(f"render failed, see {out / 'render.log'}")
        return r.returncode
    vid = next((out / "media" / "videos").rglob(f"{name}.mp4"))
    shutil.copy(vid, out / f"{name}.mp4")
    print(f"rendered {out / f'{name}.mp4'}")
    return 0


def cmd_qa(a):
    from .qa import run_qa
    name = _name(a.spec, a.name)
    out = ROOT / "build" / name
    rep = run_qa(out / f"{name}.mp4", out / "observed.json", out / "validation.json", out / "qa", name)
    return 0 if rep["pass"] else 3


def cmd_run(a):
    for step in (cmd_validate, cmd_render, cmd_qa):
        rc = step(a)
        if rc:
            return rc
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="p2v", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("analyze"); s.add_argument("pdf"); s.add_argument("--out")
    for nm in ("validate", "render", "qa", "run"):
        s = sub.add_parser(nm); s.add_argument("spec"); s.add_argument("--name")
        s.add_argument("--quality", default="qh", choices=["ql", "qm", "qh", "qk"]); s.add_argument("--problems", default=""); s.add_argument("--fps", default=30, type=int)
    a = ap.parse_args(argv)
    return {"analyze": cmd_analyze, "validate": cmd_validate, "render": cmd_render, "qa": cmd_qa, "run": cmd_run}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
