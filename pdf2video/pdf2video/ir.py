"""Document IR: every word of a PDF with its exact box, for any PDF.

- Text PDFs: words from the text layer (pdfplumber), boxes in PDF points, origin top-left.
- Scanned / image-only pages: OCR (Tesseract) on a 300 dpi render, boxes mapped back to points,
  with a per-word confidence. The page image is always the visual authority.
- Pages are rendered once at 300 dpi (PyMuPDF) and cached; crops are pixel-identical cut-outs.
- `find()` locates a quoted phrase on a page (exact first, then fuzzy for OCR), returning the union
  box of the matched words: that is where the video highlights the data.

PDFs are untrusted input: nothing here executes content from the file.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import re
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path

import pdfplumber
import pymupdf
from PIL import Image

DPI = 300
_SUBS = {"−": "-", "–": "-", "—": "-", "×": "x", "·": ".", " ": " ", "’": "'", "‘": "'", "“": '"', "”": '"', "²": "2", "³": "3", "°": "o",
         "₀": "0", "₁": "1", "₂": "2", "₃": "3", "ﬁ": "fi", "ﬂ": "fl"}


def norm(s: str) -> str:
    """normalise text for matching: unicode-fold, unify dashes/marks, lower case"""
    s = unicodedata.normalize("NFKC", s)
    for a, b in _SUBS.items():
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().lower()


@dataclass
class Word:
    text: str
    x0: float
    top: float
    x1: float
    bottom: float
    size: float = 0.0
    src: str = "text"  # 'text' | 'ocr'
    conf: float = 100.0


@dataclass
class Line:
    text: str
    box: list
    words: list = field(default_factory=list)


@dataclass
class Page:
    n: int
    width: float
    height: float
    words: list
    image: str
    source: str  # 'text' | 'ocr'
    tables: list = field(default_factory=list)
    graphics: list = field(default_factory=list)  # boxes of drawn rectangles/curves (figures, tables, work boxes)


@dataclass
class Match:
    box: list
    score: float
    text: str
    words: list


def union(boxes):
    return [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)]


class Document:
    def __init__(self, path, workdir, ocr_lang="eng", min_words=8):
        self.path = Path(path)
        self.work = Path(workdir)
        self.work.mkdir(parents=True, exist_ok=True)
        self.sha256 = hashlib.sha256(self.path.read_bytes()).hexdigest()
        self.ocr_lang = ocr_lang
        self.pages: list[Page] = []
        mu = pymupdf.open(str(self.path))
        with pdfplumber.open(str(self.path)) as pl:
            for i, (mp, pp) in enumerate(zip(mu, pl.pages)):
                img = self.work / f"page{i + 1}_{DPI}.png"
                if not img.exists():
                    mp.get_pixmap(dpi=DPI, alpha=False).save(str(img))
                words = [Word(w["text"], w["x0"], w["top"], w["x1"], w["bottom"], round(w.get("size", 0), 2))
                         for w in pp.extract_words(extra_attrs=["size"], keep_blank_chars=False)]
                source = "text"
                if len(words) < min_words:
                    words = self._ocr(img, pp.width, pp.height)
                    source = "ocr"
                graphics = [[r["x0"], r["top"], r["x1"], r["bottom"]] for r in pp.rects] + [[c["x0"], c["top"], c["x1"], c["bottom"]] for c in pp.curves]
                tables = []
                if source == "text":
                    for t in pp.find_tables():
                        rows = []
                        for r in t.rows:
                            rows.append([None if c is None else {"box": list(c), "text": (pp.crop(c).extract_text() or "").strip()} for c in r.cells])
                        tables.append({"box": list(t.bbox), "rows": rows})
                self.pages.append(Page(i + 1, pp.width, pp.height, words, str(img), source, tables, graphics))

    # ------------------------------------------------------------------ OCR
    def _ocr(self, img, W, H):
        import pytesseract
        im = Image.open(img)
        d = pytesseract.image_to_data(im, lang=self.ocr_lang, output_type=pytesseract.Output.DICT, config="--psm 3")
        k = 72.0 / DPI
        out = []
        for i, t in enumerate(d["text"]):
            t = (t or "").strip()
            if not t or float(d["conf"][i]) < 0:
                continue
            x, y, w, h = d["left"][i], d["top"][i], d["width"][i], d["height"][i]
            out.append(Word(t, x * k, y * k, (x + w) * k, (y + h) * k, round(h * k, 2), "ocr", float(d["conf"][i])))
        return out

    # ------------------------------------------------------------------ geometry helpers
    def page(self, n) -> Page:
        return self.pages[n - 1]

    def lines(self, n, region=None):
        """words grouped into reading lines (vertical overlap clustering), optionally inside a region"""
        P = self.page(n)
        ws = [w for w in P.words if region is None or (w.x0 >= region[0] - 1 and w.x1 <= region[2] + 1 and w.top >= region[1] - 1 and w.bottom <= region[3] + 1)]
        ws.sort(key=lambda w: (w.top, w.x0))
        lines = []
        for w in ws:
            h = w.bottom - w.top
            best = None
            for L in lines[-8:]:
                a, b = L.box[1], L.box[3]
                ov = min(b, w.bottom) - max(a, w.top)
                if ov > 0.45 * min(h, b - a):
                    best = L
                    break
            if best is None:
                lines.append(Line("", [w.x0, w.top, w.x1, w.bottom], [w]))
            else:
                best.words.append(w)
                best.box = [min(best.box[0], w.x0), min(best.box[1], w.top), max(best.box[2], w.x1), max(best.box[3], w.bottom)]
        for L in lines:
            L.words.sort(key=lambda w: w.x0)
            L.text = " ".join(w.text for w in L.words)
        lines.sort(key=lambda L: (L.box[1], L.box[0]))
        return lines

    def text(self, n, region=None):
        return "\n".join(L.text for L in self.lines(n, region))

    def find(self, n, quote, region=None, nth=0, fuzzy=None) -> Match | None:
        """locate a quoted phrase (case/space/unicode-insensitive); fuzzy for OCR pages"""
        P = self.page(n)
        ws = [w for L in self.lines(n, [region[0] - 2, region[1] - 2, region[2] + 2, region[3] + 2] if region else None) for w in L.words]
        stream, owner, starts = [], [], set()
        for k, w in enumerate(ws):
            t = norm(w.text).replace(" ", "")
            starts.add(len(owner))
            stream.append(t); owner += [k] * len(t)
        S = "".join(stream)
        q = norm(quote).replace(" ", "")
        if not q or not S:
            return None
        # a phrase must start where a word starts ('5 m/s' is not inside '2.5 m/s')
        hits = [m.start() for m in re.finditer(re.escape(q), S) if m.start() in starts]
        if len(hits) > nth:
            i = hits[nth]
            ks = sorted(set(owner[i:i + len(q)]))
            return Match(union([[ws[k].x0, ws[k].top, ws[k].x1, ws[k].bottom] for k in ks]), 1.0, " ".join(ws[k].text for k in ks), ks)
        if fuzzy is None:
            fuzzy = P.source == "ocr"
        if not fuzzy:
            return None
        best = (0.0, None)
        L = len(q)
        for i in sorted(starts):
            for dl in (-2, -1, 0, 1, 2):
                seg = S[i:i + L + dl]
                if not seg:
                    continue
                r = difflib.SequenceMatcher(None, q, seg).ratio()
                if r > best[0]:
                    best = (r, (i, i + L + dl))
        if best[0] < 0.8:
            return None
        a, b = best[1]
        ks = sorted(set(owner[a:b]))
        return Match(union([[ws[k].x0, ws[k].top, ws[k].x1, ws[k].bottom] for k in ks]), round(best[0], 3), " ".join(ws[k].text for k in ks), ks)

    def crop(self, n, box, pad=4, name=None):
        """pixel-identical crop of the 300 dpi page render (box in points)"""
        P = self.page(n)
        k = DPI / 72.0
        im = Image.open(P.image)
        x0, y0 = max(0, int((box[0] - pad) * k)), max(0, int((box[1] - pad) * k))
        x1, y1 = min(im.width, int((box[2] + pad) * k)), min(im.height, int((box[3] + pad) * k))
        out = self.work / (name or f"crop_p{n}_{int(box[0])}_{int(box[1])}_{int(box[2])}_{int(box[3])}.png")
        im.crop((x0, y0, x1, y1)).save(out)
        return str(out), [x0 / k, y0 / k, x1 / k, y1 / k]

    def blank_bands(self, n, region, min_h=30):
        """empty horizontal bands inside a region (where answers can be written back)"""
        Ls = self.lines(n, region)
        ys = [region[1]] + [v for L in Ls for v in (L.box[1], L.box[3])] + [region[3]]
        occupied = sorted([(L.box[1], L.box[3]) for L in Ls])
        bands, y = [], region[1]
        for a, b in occupied:
            if a - y >= min_h:
                bands.append([region[0], y, region[2], a])
            y = max(y, b)
        if region[3] - y >= min_h:
            bands.append([region[0], y, region[2], region[3]])
        void = ys
        return bands

    # ------------------------------------------------------------------ export (what the spec author reads)
    def to_json(self, problems=None):
        return {
            "file": self.path.name, "sha256": self.sha256,
            "pages": [{"n": P.n, "width": P.width, "height": P.height, "source": P.source,
                       "lines": [{"text": L.text, "box": [round(v, 1) for v in L.box]} for L in self.lines(P.n)],
                       "tables": [{"box": t["box"], "cells": [[c["text"] if c else None for c in r] for r in t["rows"]]} for t in P.tables]}
                      for P in self.pages],
            "problems": [asdict(p) for p in (problems or [])],
        }

    def save_json(self, path, problems=None):
        Path(path).write_text(json.dumps(self.to_json(problems), indent=1, ensure_ascii=False))
