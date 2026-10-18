"""Find the problems on each page: numbered items ("1.", "2)", "Problem 3", "Exercise 4",
"Question 5", "Ejercicio 6", "Problema 7", "Pregunta 8"...). Each problem gets:
  box        the whole block (statement + work area + any table/figure), page width
  statement  the box of the statement text only (the lines before the first big vertical gap)
  work       blank bands inside the block, where the answers are written back
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

LABEL = re.compile(r"^(?:(?:problem|exercise|question|ejercicio|problema|pregunta|item|task)\s*)?(\d{1,2})\s*[.):]?$", re.I)
LABEL_INLINE = re.compile(r"^(?:(?:problem|exercise|question|ejercicio|problema|pregunta)\s+)(\d{1,2})\b", re.I)


@dataclass
class Problem:
    id: str
    page: int
    box: list
    statement: list
    text: str
    work: list = field(default_factory=list)
    graphics: list = field(default_factory=list)


def detect(doc, footer_margin=48, header_skip=0.12):
    probs = []
    for P in doc.pages:
        lines = doc.lines(P.n)
        left = min((L.box[0] for L in lines), default=0)
        starts = []
        for L in lines:
            if L.box[1] < P.height * header_skip:
                continue
            first = L.words[0].text.strip()
            m = LABEL.match(first) or LABEL_INLINE.match(L.text)
            two = " ".join(w.text for w in L.words[:2])
            m2 = LABEL.match(two) if not m else None
            mm = m or m2
            if mm and L.box[0] < left + P.width * 0.12:
                n = int(mm.group(1))
                if not starts or n == starts[-1][0] + 1 or (n == 1 and not starts):
                    starts.append((n, L))
        bottom_limit = P.height - footer_margin
        foot = [L for L in lines if L.box[1] > bottom_limit]
        for k, (n, L) in enumerate(starts):
            y0 = L.box[1] - 4
            y1 = (starts[k + 1][1].box[1] - 6) if k + 1 < len(starts) else (min((f.box[1] for f in foot), default=bottom_limit) - 4)
            box = [max(0, left - 6), y0, P.width - left + 6 if left < P.width / 2 else P.width, y1]
            blk = doc.lines(P.n, box)
            # statement: consecutive lines until a vertical gap larger than 2.2 line heights
            st = [blk[0]] if blk else []
            for a, b in zip(blk, blk[1:]):
                h = max(8.0, a.box[3] - a.box[1])
                if b.box[1] - a.box[3] > 2.2 * h:
                    break
                st.append(b)
            sbox = [min(x.box[0] for x in st), min(x.box[1] for x in st), max(x.box[2] for x in st), max(x.box[3] for x in st)] if st else box
            text = " ".join(x.text for x in st)
            gfx = [g for g in P.graphics if g[1] >= y0 - 1 and g[3] <= y1 + 1 and (g[2] - g[0]) * (g[3] - g[1]) > 50]
            work = doc.blank_bands(P.n, [box[0] + 20, sbox[3] + 4, box[2] - 20, y1], min_h=36)
            probs.append(Problem(str(n), P.n, [round(v, 1) for v in box], [round(v, 1) for v in sbox], text, [[round(v, 1) for v in b] for b in work], gfx))
    return probs
