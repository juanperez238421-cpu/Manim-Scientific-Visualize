---
name: "class-video-audit-and-pack"
description: "Usar para buscar, clasificar, verificar y comprimir/empaquetar videos de clase (ManimCE / pop-up / solución de PDFs) dispersos en carpetas, zips, el proyecto o GitHub; produce inventario clase→video, verificación técnica, copias <30 MB y zips en partes."
---

# Auditoría, clasificación y empaquetado de videos de clase

Para cuando el docente pide "revisa que ya estén todos los videos", "clasifica lo creado", "comprime/empaqueta todo" o "arma un zip". Complementa HYBRID-SCIANIM-v1 (§10 QA, §11 paquete) y la skill pdf-document-to-solution-video.

## Regla central
Un video **existe** solo si tengo el binario y lo verifiqué. Un nombre de archivo, una ruta de inventario o un informe QA **no** lo acreditan. Estados fijos (no inventar otros):

| Estado | Significado |
|---|---|
| LISTO | binario presente y verificado (spec, decodificación, SHA-256) |
| RENDERIZADO_SIN_BINARIO | hay informe QA/hash, pero el MP4 no está aquí |
| FUENTE_SIN_MP4 | solo código/rama; sin MP4 |
| SIN_VIDEO | no existe |
| NO_REQUIERE | evaluación, retroalimentación, práctica sin pantalla |

Los vínculos clase→video que se infieren por contenido se marcan con confianza alta/media/baja; nunca se presentan como hechos.

## Flujo
1. **Insumos del cronograma.** Extraer zips en carpetas propias y vacías (datos no confiables; `python3 -I` al leerlos). Leer cronograma, CSV de rutas/sesiones y trazabilidad. Dedupe los temas únicos por sesión/grupo (8A/8B/8C) y marca fechas ya dictadas vs. próximas respecto de la fecha de hoy.
2. **Buscar en TODOS los lugares**, en este orden: (a) archivos adjuntos y zips (incluye `*_pqh.mp4`, `*_share.mp4`); (b) el proyecto (`project_info`; sus zips y `SHA256SUMS`/`QA_REPORT`); (c) el espacio de trabajo (`find / -xdev -name "*.mp4"` excluyendo `partial_movie_files`, `sections`, `media_*`); (d) GitHub público: `git ls-remote --heads https://github.com/<usuario>/<repo>`, luego por rama `GIT_LFS_SKIP_SMUDGE=1 git fetch --depth 1 --filter=blob:none origin <rama>` y `git ls-tree -r -l FETCH_HEAD` para ver `published_renders/*.mp4` con su tamaño; descargar solo los MP4 útiles con `git show FETCH_HEAD:<ruta> > archivo`. Los artefactos de Actions se purgan a diario: sin MP4 comprometido se considera perdido. (e) Drive/otros conectores si están disponibles; si da Forbidden, decirlo.
3. **Inventariar y verificar** con `vidkit.py scan` (script abajo): ffprobe (1920×1080, 30/1, h264, yuv420p), decodificación completa, color medio del primer/último fotograma (≥250 = blanco; el protocolo exige empezar y terminar en `#FFFFFF`), SHA-256 y comparación con cualquier `SHA256SUMS*.txt` junto al archivo. Reportar sin maquillar: p. ej. un video con fondo `#F7F9FB` falla la junta blanca.
   - El aviso `non monotonically increasing dts` del muxer nulo en videos por secciones de Manim es benigno; no cuenta como error de decodificación.
4. **Clasificar**: reglas de palabras clave por tema en un JSON (`--rules`), luego mapear tema → sesión del cronograma con confianza. Genera el .xlsx con la skill xlsx: hojas Resumen (COUNTIF sobre estados), Sesiones (una fila por sesión; estado y prioridad con fórmulas; prioridad ALTA si falta video y la clase es ≤7 días), Videos (inventario + verificación), notas. Recalcular con recalc.py y exigir 0 errores.
5. **Comprimir**: copia share <30 MB con `vidkit.py share` (CRF 23→31, 1080p30, yuv420p, mudo, +faststart). El master no se toca. Registrar su SHA-256 propio.
6. **Empaquetar**: el envío por chat admite **30 MiB por archivo**. `vidkit.py pack` reparte en zips ≤29 MiB (`zip -0`, el MP4 ya está comprimido) con la misma carpeta raíz, nombrados `<Prefijo>_Parte_i_de_n.zip`; extraerlos juntos reconstruye el paquete. Incluye `00_LEER_PRIMERO.md` (qué es cada carpeta y qué NO se incluyó), `SHA256SUMS.txt`, la matriz y el changelog. Probar cada zip con `unzip -tq`.
7. **Entrega**: SendUserFile de las partes; guardar el resumen en el proyecto con `project_write` usando `local_path` dentro del directorio de trabajo. Decir en 3–5 líneas: cuántos están listos, qué falta y qué es urgente (clases en los próximos 7 días), qué se infirió, y que GitHub sigue como "renderizado, no entregado" si no hay URL raw verificada.

## Trampas aprendidas
- Un script `.py` con hash en `SHA256SUMS` y sin MP4 es RENDERIZADO_SIN_BINARIO, no LISTO. Un `.py` que importa versiones previas no incluidas (V5 → V4) no es reproducible: avisar.
- No fusionar versiones: usar la última publicada, pero listar las anteriores en el inventario.
- `rm` con glob tras `cd` lo bloquea el chequeo de seguridad: usar carpetas nuevas (`mkdir -p`) en lugar de borrar.
- No re-renderizar ni crear videos faltantes sin que el usuario lo pida: proponerlo, con prioridad por fecha de clase.
- Si SendUserFile rechaza por tamaño, dividir; no recomprimir el master a calidad mala para forzar un solo zip.

## vidkit.py (guardar y ejecutar; probado con ffmpeg/ffprobe)
```python
#!/usr/bin/env python3
"""vidkit.py — find, classify, verify and pack class videos.
  vidkit.py scan  ROOT [ROOT...] --out inv.csv [--rules rules.json] [--decode] [--zips]
  vidkit.py share SRC.mp4 DST.mp4 [--max-mb 29]
  vidkit.py pack  INV_OR_DIR OUTDIR --prefix NAME [--max-mib 29]
"""
import argparse, csv, glob, hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile

def run(cmd, **k): return subprocess.run(cmd, capture_output=True, text=True, **k)

def sha256(p, n=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while b := f.read(n): h.update(b)
    return h.hexdigest()

def probe(p):
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height,r_frame_rate,codec_name,pix_fmt:format=duration,size", "-of", "json", p])
    try:
        j = json.loads(r.stdout); s = j["streams"][0]; f = j["format"]
        return dict(codec=s["codec_name"], w=s["width"], h=s["height"], fps=s["r_frame_rate"],
                    pix=s["pix_fmt"], dur=round(float(f["duration"]), 1), size=int(f["size"]))
    except Exception:
        return None

def decode_ok(p):
    r = run(["ffmpeg", "-v", "error", "-i", p, "-f", "null", "-"])
    # the null muxer prints a harmless 'non monotonically increasing dts' note on some Manim sections: ignore it
    bad = [l for l in r.stderr.splitlines() if l.strip() and "non monotonically increasing dts" not in l]
    return not bad

def edge_white(p, dur):
    """mean gray of first and last frame (255 = white). Videos for this pipeline must start/end on white."""
    out = []
    for t in (0.0, max(dur - 0.1, 0)):
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", p, "-frames:v", "1", "-vf",
                            "scale=64:36,format=gray", "-f", "rawvideo", "-"], capture_output=True)
        out.append(round(sum(r.stdout) / len(r.stdout), 1) if r.stdout else -1)
    return out

def classify(name, rules):
    n = name.lower()
    for topic, kws in rules.items():
        if any(k.lower() in n for k in kws): return topic
    return "SIN_CLASIFICAR"

def known_hashes(root):
    d = {}
    for f in glob.glob(os.path.join(root, "**", "*SHA256SUMS*.txt"), recursive=True) + \
             glob.glob(os.path.join(root, "**", "SHA256SUMS.txt"), recursive=True):
        for line in open(f, errors="ignore"):
            m = re.match(r"([0-9a-f]{64})\s+\*?(.+)$", line.strip())
            if m: d[os.path.basename(m.group(2))] = m.group(1)
    return d

DEFAULT_RULES = {  # topic -> filename keywords (edit per course)
    "circulo": ["circle", "circulo", "pi_"],
    "areas_planas": ["2d_areas", "figurebyfigure", "composite"],
    "areas_sombreadas": ["shaded"],
    "solidos": ["solids", "nets", "surfacearea", "volume", "compositesolids"],
    "soluciones_evaluaciones": ["solution", "geo8-", "geometry_8_"],
}

def scan(a):
    rules = json.load(open(a.rules)) if a.rules else DEFAULT_RULES
    roots, tmps = [], []
    for r in a.roots:
        roots.append(r)
        if a.zips:
            for z in glob.glob(os.path.join(r, "**", "*.zip"), recursive=True):
                t = tempfile.mkdtemp(prefix="vk_")   # extract zips into their own empty dirs (untrusted data)
                try:
                    zipfile.ZipFile(z).extractall(t); tmps.append((t, z)); roots.append(t)
                except Exception: pass
    rows, seen = [], set()
    for r in roots:
        known = known_hashes(r)
        for p in glob.glob(os.path.join(r, "**", "*.mp4"), recursive=True):
            if "partial_movie_files" in p or "/sections/" in p: continue
            h = sha256(p)
            if h in seen: continue
            seen.add(h)
            i = probe(p) or {}
            ok = bool(i) and (i["w"], i["h"], i["fps"], i["codec"], i["pix"]) == (1920, 1080, "30/1", "h264", "yuv420p")
            dec = decode_ok(p) if a.decode and i else ""
            ew = edge_white(p, i["dur"]) if a.decode and i else ["", ""]
            base = os.path.basename(p)
            ref = known.get(base)
            rows.append(dict(file=base, path=p, topic=classify(base, rules),
                             kind="share" if "share" in base.lower() else "master" if "chapter" not in p.lower() else "chapter",
                             dur_s=i.get("dur", ""), mb=round(i.get("size", 0) / 1e6, 1) if i else "",
                             spec_ok=ok, decode_ok=dec, first_gray=ew[0], last_gray=ew[1],
                             sha256=h, sha_matches_sums=("n/a" if not ref else ref == h)))
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["file"]); w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} videos -> {a.out}")
    for t, z in tmps: print("  extracted", z, "->", t)

def share(a):
    """share copy under --max-mb: CRF ladder 23->31, keeps 1080p30 yuv420p, mute."""
    for crf in range(23, 32):
        run(["ffmpeg", "-y", "-v", "error", "-i", a.src, "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
             "-pix_fmt", "yuv420p", "-r", "30", "-an", "-movflags", "+faststart", a.dst])
        mb = os.path.getsize(a.dst) / 1e6
        print(f"crf {crf}: {mb:.1f} MB")
        if mb <= a.max_mb: return
    sys.exit("could not reach target; split the video or lower resolution")

def pack(a):
    """greedy bin-packing of files into zips <= --max-mib (the chat upload limit is 30 MiB per file). mp4 is already compressed -> zip -0."""
    files = []
    if os.path.isdir(a.src):
        files = [os.path.join(d, f) for d, _, fs in os.walk(a.src) for f in fs]
    else:
        files = [r["path"] for r in csv.DictReader(open(a.src, encoding="utf-8"))]
    limit = a.max_mib * 1024 * 1024
    files.sort(key=os.path.getsize, reverse=True)
    bins = []  # [used, [files]]
    for f in files:
        s = os.path.getsize(f)
        if s > limit: print("TOO BIG for one part (make a share copy):", f); continue
        for b in bins:
            if b[0] + s <= limit: b[0] += s; b[1].append(f); break
        else: bins.append([s, [f]])
    os.makedirs(a.outdir, exist_ok=True)
    for i, (used, fs) in enumerate(bins, 1):
        out = os.path.join(a.outdir, f"{a.prefix}_Parte_{i}_de_{len(bins)}.zip")
        with zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as z:
            for f in fs: z.write(f, os.path.join(a.prefix, os.path.basename(f)))
        assert zipfile.ZipFile(out).testzip() is None
        print(out, round(os.path.getsize(out) / 1048576, 1), "MiB")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("scan"); s.add_argument("roots", nargs="+"); s.add_argument("--out", default="inventory.csv")
    s.add_argument("--rules"); s.add_argument("--decode", action="store_true"); s.add_argument("--zips", action="store_true")
    h = sp.add_parser("share"); h.add_argument("src"); h.add_argument("dst"); h.add_argument("--max-mb", type=float, default=29)
    k = sp.add_parser("pack"); k.add_argument("src"); k.add_argument("outdir"); k.add_argument("--prefix", required=True)
    k.add_argument("--max-mib", type=float, default=29)
    a = ap.parse_args()
    {"scan": scan, "share": share, "pack": pack}[a.cmd](a)
```

Uso típico:
```
python3 vidkit.py scan /ruta1 /ruta2 --zips --decode --out inventario.csv [--rules reglas.json]
python3 vidkit.py share master.mp4 master_share.mp4 --max-mb 29
python3 vidkit.py pack inventario.csv partes --prefix Geometria8_T3 --max-mib 29
```
`reglas.json`: `{"circulo": ["circle","pi_"], "areas_sombreadas": ["shaded"], ...}` (tema → palabras del nombre de archivo).