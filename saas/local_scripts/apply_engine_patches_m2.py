"""Parches idempotentes M2 al motor pdf2video (se aplican DESPUES de apply_engine_patches.py):

  1. Espanol en el render (render/i18n.py + textos fijos de scene.py segun spec["language"]).
  2. Coma decimal / miles con espacio en el validador (numbers_in): 9,8 -> 9.8 ; 18 000 -> 18000.
  3. Perfiles de video y QA diferenciados mediante P2V_PROFILE: preview480 | dev720 | delivery1080.

Uso:  python scripts/apply_engine_patches_m2.py [ruta/al/pdf2video]   (por defecto engine/pdf2video)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
eng = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "engine" / "pdf2video"
PKG = eng / "pdf2video"

NUMBERS_OLD = r'''    return [float(x.replace(",", "")) for x in re.findall(r"(?<![\w.])-?\d+(?:,\d{3})*(?:\.\d+)?", norm(s))]
'''
NUMBERS_NEW = r'''    """Numeros impresos en `s`. Ademas de la lectura inglesa (1,000 = 1000; 9.8) devuelve la lectura espanola/SI:
    coma decimal (9,8 -> 9.8) y miles separados por espacio (18 000 -> 18000). Los candidatos extra solo facilitan casar
    una cita con un valor; la cita localizada en la pagina sigue siendo obligatoria."""
    t = norm(s)
    out = [float(x.replace(",", "")) for x in re.findall(r"(?<![\w.])-?\d+(?:,\d{3})*(?:\.\d+)?", t)]
    out += [float(f"{m.group(1)}.{m.group(2)}") for m in re.finditer(r"(?<![\w.,])(-?\d+),(\d+)(?!\d)", t)]
    out += [float(re.sub(r"[   ]", "", m.group(0))) for m in re.finditer(r"(?<![\w.,])-?\d{1,3}(?:[   ]\d{3})+(?![\d])", t)]
    return out
'''

PATCHES = [
    # ---- i18n del render
    ("render/scene.py", "from pdf2video.validate import fmt_value, validate  # noqa: E402\n",
     "from pdf2video.validate import fmt_value, validate  # noqa: E402\nfrom pdf2video.render.i18n import strings  # noqa: E402\n"),
    ("render/scene.py", '        self.rep, self.doc, self.S = validate(spec, workdir=self.out / "work", verbose=False)\n',
     '        self.rep, self.doc, self.S = validate(spec, workdir=self.out / "work", verbose=False)\n        self.L = strings(self.S.get("language"))\n'),
    ("render/scene.py", 'head = T((stage.upper() + ("  ·  " + note if note else "")), 15, MUTED)',
     'head = T((self.L["stage"].get(stage, stage).upper() + ("  ·  " + note if note else "")), 15, MUTED)'),
    ("render/scene.py", """meta = fit(T(f"{self.doc.path.name}  ·  {len(probs)} problem{'s' if len(probs) != 1 else ''}  ·  every value checked", 17, MUTED), 7.4)""",
     """meta = fit(T(self.L["meta"].format(doc=self.doc.path.name, n=len(probs), s="s" if len(probs) != 1 else ""), 17, MUTED), 7.4)"""),
    ("render/scene.py", "        for i, s in enumerate(STAGES):\n            stages.add(T(s, 19, INK))\n            if i < len(STAGES) - 1:",
     '        for i, s in enumerate(self.L["stages"]):\n            stages.add(T(s, 19, INK))\n            if i < len(self.L["stages"]) - 1:'),
    ("render/scene.py", """for col, lab in ((C_VEL, "data from the page"), (C_ACC, "condition / sign"), (C_POS, "result"), (C_GAL, "verified")):""",
     """for col, lab in zip((C_VEL, C_ACC, C_POS, C_GAL), self.L["legend"]):"""),
    ("render/scene.py", """T(f"PROBLEM {P['id']}", 22, C_POS, weight=BOLD)""", """T(f"{self.L['problem_up']} {P['id']}", 22, C_POS, weight=BOLD)"""),
    ("render/scene.py", """T(f"Problem {P['id']}", 24, C_POS, weight=BOLD)""", """T(f"{self.L['problem']} {P['id']}", 24, C_POS, weight=BOLD)"""),
    ("render/scene.py", 'head = T("MODEL", 15, MUTED)', 'head = T(self.L["model"], 15, MUTED)'),
    ("render/scene.py", """"in_tex": shown.replace(" ", "") in a["tex"].replace(" ", "").replace("{,}", "")})""",
     """"in_tex": (lambda t, sh: sh in t.replace("{,}", "") or sh in t.replace("{,}", ".") or sh.replace(".", ",") in t.replace("{,}", ","))(a["tex"].replace(" ", ""), shown.replace(" ", ""))})"""),
    ("render/scene.py", 'T("CHECKED", 20, BG, weight=BOLD)', 'T(self.L["checked"], 20, BG, weight=BOLD)'),
    ("render/scene.py", 'col = VGroup(T("Answers", 36, INK, weight=BOLD))', 'col = VGroup(T(self.L["answers"], 36, INK, weight=BOLD))'),
    ("render/scene.py", """items = VGroup(T(f"Problem {p['id']}  ·  {p.get('title', '')}", 21, C_POS, weight=BOLD))""",
     """items = VGroup(T(f"{self.L['problem']} {p['id']}  ·  {p.get('title', '')}", 21, C_POS, weight=BOLD))"""),
    ("render/scene.py", 'T("EVERY VALUE QUOTED FROM THE PAGE · EVERY ANSWER RECOMPUTED (SymPy)", 15, BG, weight=BOLD)',
     'T(self.L["closing"], 15, BG, weight=BOLD)'),
    # ---- coma decimal
    ("validate.py", NUMBERS_OLD, NUMBERS_NEW),
    # ---- perfiles de video / QA
    ("qa.py", "import json\nimport subprocess\n", "import json\nimport os\nimport subprocess\n"),
    ("qa.py", "def share_copy(src, dst, limit_mb=29.0):",
     "# Perfiles: (resolucion esperada, fps esperados). preview = borrador rapido; dev = desarrollo; delivery = entrega final.\n"
     'PROFILES = {"preview480": ([854, 480], "15/1"), "dev720": ([1280, 720], "30/1"), "delivery1080": ([1920, 1080], "30/1")}\n\n\n'
     "def share_copy(src, dst, limit_mb=29.0):"),
    ("qa.py",
     '    t_ok = tech["codec"] == "h264" and tech["size"] == [1920, 1080] and tech["fps"] == "30/1" and tech["pix_fmt"] == "yuv420p" and not tech["decode_errors"] and dur > 1',
     '    profile = os.environ.get("P2V_PROFILE", "delivery1080")\n'
     "    if profile not in PROFILES:\n"
     '        raise SystemExit(f"unknown P2V_PROFILE {profile!r}; expected one of {sorted(PROFILES)}")\n'
     "    want_size, want_fps = PROFILES[profile]\n"
     '    tech["profile"] = profile\n'
     '    t_ok = tech["codec"] == "h264" and tech["size"] == want_size and tech["fps"] == want_fps and tech["pix_fmt"] == "yuv420p" and not tech["decode_errors"] and dur > 1'),
    # ---- anotaciones: si la hoja no tiene hueco suficiente, NO se escribe fuera del area de trabajo (la respuesta sigue
    #      mostrandose y verificandose); se registra como annotation_skipped en vez de fallar el QA por falta de espacio.
    ("render/scene.py", '            ann = self.annotation(a["annotation"], x, y)\n',
     '            if not (band[1] <= y <= band[3]):\n'
     '                self.log.append({"problem": P["id"], "kind": "annotation_skipped", "name": a["name"], "reason": "no room in work area"})\n'
     '                continue\n'
     '            ann = self.annotation(a["annotation"], x, y)\n'),
    ("qa.py", '"annotations_in_work_area": sum(o["in_work_area"] for o in anns),',
     '"annotations_in_work_area": sum(o["in_work_area"] for o in anns), "annotations_skipped_no_room": sum(1 for o in obs if o["kind"] == "annotation_skipped"),'),
]

NEW_FILES = {"render/i18n.py": ROOT / "scripts" / "engine_files" / "i18n.py"}

changed = ok = 0
for rel, src in NEW_FILES.items():
    dst = PKG / rel
    data = src.read_text(encoding="utf-8")
    if dst.exists() and dst.read_text(encoding="utf-8") == data:
        ok += 1
    else:
        dst.write_text(data, encoding="utf-8")
        changed += 1
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
print(f"parches M2 aplicados: {changed}, ya presentes: {ok}")
