"""ffprobe + hash del MP4 final (el worker verifica lo que entrega; la API vuelve a comprobar el tamaño)."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def probe(path) -> dict:
    exe = shutil.which("ffprobe")
    if not exe:
        raise RuntimeError("ffprobe no está instalado")
    r = subprocess.run([exe, "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(path)],
                       capture_output=True, text=True, encoding="utf-8", timeout=60)
    if r.returncode:
        raise RuntimeError(f"ffprobe falló: {r.stderr[-200:]}")
    j = json.loads(r.stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    num, den = v["r_frame_rate"].split("/")
    return {"codec": v["codec_name"], "width": int(v["width"]), "height": int(v["height"]),
            "fps": round(int(num) / int(den)), "pix_fmt": v["pix_fmt"], "duration_seconds": float(j["format"]["duration"]),
            "size_bytes": int(j["format"]["size"])}


def full_decode_errors(path) -> str:
    """Decodifica TODO el archivo; cadena vacía = sin errores."""
    exe = shutil.which("ffmpeg")
    if not exe:
        raise RuntimeError("ffmpeg no está instalado")
    r = subprocess.run([exe, "-v", "error", "-i", str(path), "-f", "null", "-"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=600)
    return (r.stderr or "").strip()[:300]
