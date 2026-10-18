"""Parches idempotentes al motor pdf2video (carpeta engine/pdf2video) para E/S UTF-8 explicita.

Causa raiz: el motor escribe/lee JSON con Path.write_text()/read_text() SIN encoding. En Windows eso usa la
pagina de codigos ANSI (cp1252): '.' (U+00B7) se guardaba como el byte 0xB7 y el consumidor lo leia como UTF-8
estricto (UnicodeDecodeError); caracteres fuera de cp1252 (pi, mu, Delta, menos U+2212...) ni siquiera se podian escribir.
Uso:  python scripts/apply_engine_patches.py [ruta/al/pdf2video]   (por defecto engine/pdf2video)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
eng = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "engine" / "pdf2video"
PKG = eng / "pdf2video"

PATCHES = [
    ("ir.py", 'Path(path).write_text(json.dumps(self.to_json(problems), indent=1, ensure_ascii=False))',
              'Path(path).write_text(json.dumps(self.to_json(problems), indent=1, ensure_ascii=False), encoding="utf-8")'),
    ("cli.py", '(out / "validation.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=str))',
               '(out / "validation.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=str), encoding="utf-8")'),
    ("cli.py", 'with open(out / "render.log", "w") as log:', 'with open(out / "render.log", "w", encoding="utf-8") as log:'),
    ("render/scene.py", '(self.out / "observed.json").write_text(json.dumps({"spec": self.S.get("title"), "log": self.log}, indent=1, ensure_ascii=False))',
                        '(self.out / "observed.json").write_text(json.dumps({"spec": self.S.get("title"), "log": self.log}, indent=1, ensure_ascii=False), encoding="utf-8")'),
    ("qa.py", 'return subprocess.run(cmd, capture_output=True, text=True)', 'return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")'),
    ("qa.py", 'obs = json.loads(Path(observed).read_text())["log"]', 'obs = json.loads(Path(observed).read_text(encoding="utf-8"))["log"]'),
    ("qa.py", 'val = json.loads(Path(validation).read_text())', 'val = json.loads(Path(validation).read_text(encoding="utf-8"))'),
    ("qa.py", '(outdir / "SHA256SUMS.txt").write_text("".join(f"{h}  {n}\\n" for n, h in sums.items()))',
              '(outdir / "SHA256SUMS.txt").write_text("".join(f"{h}  {n}\\n" for n, h in sums.items()), encoding="utf-8")'),
    ("qa.py", '(outdir / "qa.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False))', '(outdir / "qa.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")'),
    ("qa.py", '(outdir / "VIDEO_QA.txt").write_text("\\n".join(lines) + "\\n")', '(outdir / "VIDEO_QA.txt").write_text("\\n".join(lines) + "\\n", encoding="utf-8")'),
    ("validate.py", 'S = json.loads(spec_path.read_text())', 'S = json.loads(spec_path.read_text(encoding="utf-8"))'),
    ("__main__.py", "from .cli import main\n",
                    "from .cli import main\n\nfor _s in (sys.stdout, sys.stderr):  # salida UTF-8 aunque la consola/tuberia use cp1252\n    if hasattr(_s, \"reconfigure\"):\n        _s.reconfigure(encoding=\"utf-8\")\n"),
]

changed = ok = 0
for rel, old, new in PATCHES:
    f = PKG / rel
    s = f.read_text(encoding="utf-8")
    if new in s:
        ok += 1
        continue
    if s.count(old) != 1:
        sys.exit(f"ERROR: {rel}: patron no encontrado exactamente una vez; el motor cambio, revisa a mano:\n  {old[:90]}")
    f.write_text(s.replace(old, new), encoding="utf-8")
    changed += 1
print(f"parches aplicados: {changed}, ya presentes: {ok}")
