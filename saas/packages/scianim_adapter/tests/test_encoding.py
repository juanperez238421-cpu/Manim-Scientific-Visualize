"""Regresion de codificacion (Windows cp1252 vs UTF-8). Causa raiz: el motor escribia el IR con Path.write_text()
sin encoding; en Windows eso produce cp1252 ('·' -> 0xB7) y el adaptador lo leia como UTF-8 estricto."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from scianim_adapter import JobConfig
from scianim_adapter import runner as R

TTF = [p for p in (r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\segoeui.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf") if os.path.exists(p)]
WIDE = "pi = 3,14 · mu · Δx ≈ 2 · (−5) · ñ · 25 °C · v² · ½"      # incluye caracteres fuera de cp1252 (π, Δ, ≈, −, ½ ...)


@pytest.fixture()
def unicode_pdf(tmp_path):
    import pymupdf
    doc = pymupdf.open()
    page = doc.new_page()
    if TTF:
        page.insert_font(fontname="uf", fontfile=TTF[0])
        fn = "uf"
        text = "Física y Química · 4.º ESO · π μ ñ ° ≈ −"
        prob = "1. Calcula Δx ≈ 2·π · 3 °C con v² = 4 m/s² · ½ μ (ñ)."
    else:
        fn, text, prob = "helv", "Física y Química · 4.º ESO · ñ °", "1. Calcula x = 2 · 3 m con v = 4 m/s · ñ."
    page.insert_text((50, 60), text, fontname=fn, fontsize=11)
    page.insert_text((50, 100), prob, fontname=fn, fontsize=11)
    page.insert_text((50, 130), "______________________________", fontname=fn, fontsize=11)
    p = tmp_path / "unicode.pdf"
    doc.save(p); doc.close()
    return p


def test_adapter_forces_utf8_in_child_env(monkeypatch, tmp_path, cfg):
    seen = {}

    def fake(cmd, **kw):
        seen.update(kw)
        return subprocess.CompletedProcess(cmd, 0, "", "")
    monkeypatch.setattr(R.subprocess, "run", fake)
    R._run(cfg, ["analyze", "x.pdf"], 5, tmp_path)
    assert seen["env"]["PYTHONUTF8"] == "1" and seen["env"]["PYTHONIOENCODING"] == "utf-8"
    assert seen["encoding"] == "utf-8" and seen["errors"] == "strict"   # nunca 'ignore'/'replace'


def test_ir_json_is_strict_utf8_and_keeps_characters(tmp_path, cfg, unicode_pdf):
    out = tmp_path / "an"
    r = R._run(cfg, ["analyze", str(unicode_pdf), "--out", str(out)], 180, tmp_path)
    assert r.returncode == 0, r.stderr[-400:]
    raw = (out / "ir.json").read_bytes()
    text = raw.decode("utf-8")                 # estricto: lanza si hubiese un 0xB7 suelto
    assert b"\xb7" not in raw.replace(b"\xc2\xb7", b"")          # ningun 0xB7 aislado (cp1252)
    assert "\ufffd" not in text                                     # sin caracteres de sustitucion
    ir = json.loads(text)
    assert ir["pages"][0]["lines"]
    # Verdad de referencia: los caracteres que la capa de texto del PDF contiene realmente (depende de la fuente).
    import pymupdf
    with pymupdf.open(unicode_pdf) as d:
        truth = d[0].get_text()
    expected = [ch for ch in "·ñ°ºπμΔ≈−½²" if ch in truth]
    assert "·" in expected, f"el PDF de prueba no contiene '·' en su capa de texto; fuente={TTF[:1]}"
    missing = [ch for ch in expected if ch not in text]
    sample = [ln["text"] for ln in ir["pages"][0]["lines"]][:3]
    assert not missing, f"caracteres perdidos en el IR: {missing!r}; PDF={truth[:90]!r}; IR={sample!r}"


def test_engine_has_no_locale_dependent_file_io(tmp_path, cfg, unicode_pdf, physics):
    """Aun sin PYTHONUTF8, el motor parcheado no depende de la pagina de codigos: cualquier open()/write_text()
    sin encoding en pdf2video.* lanzaria EncodingWarning (convertido en error). Independiente del SO."""
    code = ("import runpy, sys, warnings\n"
            "warnings.filterwarnings('error', category=EncodingWarning, module=r'pdf2video(\\..*)?$')\n"
            "sys.argv = ['p2v'] + sys.argv[1:]\n"
            "runpy.run_module('pdf2video', run_name='__main__')\n")
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONUTF8", "PYTHONIOENCODING")}
    env.update(PYTHONUTF8="0", PYTHONDONTWRITEBYTECODE="1")

    def run(*args):
        return subprocess.run([sys.executable, "-X", "warn_default_encoding", "-c", code, *args], cwd=cfg.engine_root,
                              env=env, capture_output=True, text=True, encoding="utf-8", timeout=300)
    a = run("analyze", str(unicode_pdf), "--out", str(tmp_path / "an2"))
    assert a.returncode == 0 and "EncodingWarning" not in a.stderr, a.stderr[-600:]
    spec = tmp_path / "spec.json"
    spec.write_text(json.dumps(physics[1], ensure_ascii=False), encoding="utf-8")
    v = run("validate", str(spec), "--name", "enc_probe")
    try:
        assert "EncodingWarning" not in v.stderr and "UnicodeDecodeError" not in v.stderr, v.stderr[-600:]
    finally:
        import shutil
        shutil.rmtree(Path(cfg.engine_root) / "build" / "enc_probe", ignore_errors=True)
