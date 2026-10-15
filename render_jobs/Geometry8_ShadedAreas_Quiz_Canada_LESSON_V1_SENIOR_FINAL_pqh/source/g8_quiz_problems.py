#!/usr/bin/env python3
"""Geometry 8 · Shaded Areas Quiz (Canada) — problem DATA + integrity checks.

Problems are data: every number, formula line and sentence that the student
sees is generated here from the same model-unit (cm) geometry that the scene
draws.  Nothing in the scene file types a number by hand.

Run `python3 g8_quiz_problems.py` to execute every integrity check
(Gate A of the G8 production protocol).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction

from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

QUAD = 256          # shapely circle resolution (area error < 0.003 %)
CLEARANCE = 0.25    # cm, minimum gap-to-gap and gap-to-silhouette distance
TAG_CLEAR = 0.8     # cm, positive-part tags must be this far from any gap


# ----------------------------------------------------------------------------
# Exact numbers  a + b·π  (rational a, b)
# ----------------------------------------------------------------------------
@dataclass(frozen=True)
class Exact:
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)      # coefficient of π

    @staticmethod
    def of(a=0, pi=0) -> "Exact":
        return Exact(Fraction(a), Fraction(pi))

    def __add__(self, o: "Exact") -> "Exact":
        return Exact(self.a + o.a, self.b + o.b)

    def __sub__(self, o: "Exact") -> "Exact":
        return Exact(self.a - o.a, self.b - o.b)

    def __mul__(self, k) -> "Exact":
        return Exact(self.a * k, self.b * k)

    @property
    def value(self) -> float:
        return float(self.a) + float(self.b) * math.pi

    @property
    def n_terms(self) -> int:
        return int(self.a != 0) + int(self.b != 0)

    def latex(self) -> str:
        parts = []
        if self.a != 0:
            parts.append(num(self.a))
        if self.b != 0:
            coef = "" if abs(self.b) == 1 else num(abs(self.b))
            term = f"{coef}\\pi"
            if not parts:
                parts.append(("-" if self.b < 0 else "") + term)
            else:
                parts.append(("-" if self.b < 0 else "+") + term)
        return "".join(parts) if parts else "0"

    def plain(self) -> str:
        """Unicode version for Text (answer key)."""
        return self.latex().replace("\\pi", "π").replace("-", " − ").replace("+", " + ")

    def approx(self) -> str:
        return f"{self.value:.2f}"


def num(x) -> str:
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{float(x):g}"


# ----------------------------------------------------------------------------
# Shapes in model units (cm)
# ----------------------------------------------------------------------------
@dataclass(frozen=True)
class Shape:
    kind: str                 # rect | tri | circle | semicircle | poly
    params: tuple             # kind-specific (see poly())

    def poly(self) -> Polygon:
        k, p = self.kind, self.params
        if k == "rect":       # (x0, y0, x1, y1)
            return box(*p)
        if k in ("tri", "poly"):  # vertices
            return Polygon(p)
        if k == "circle":     # (cx, cy, r)
            cx, cy, r = p
            return Point(cx, cy).buffer(r, quad_segs=QUAD)
        if k == "semicircle":  # (cx, cy, r, start_deg)  — 180° sector
            cx, cy, r, start = p
            pts = [(cx, cy)]
            for i in range(721):
                t = math.radians(start + 180 * i / 720)
                pts.append((round(cx + r * math.cos(t), 9), round(cy + r * math.sin(t), 9)))
            return Polygon(pts)
        raise ValueError(k)


@dataclass(frozen=True)
class Part:
    key: str                  # "A1"
    name: str                 # "rectangle"
    sign: int                 # +1 whole / −1 gap
    formula: str              # rect | tri | square | rhombus | circle | semicircles
    dims: dict                # numbers used by the formula
    shapes: tuple             # Shape(s) that are drawn
    tag_at: tuple             # (x, y) model point where the A-tag sits
    describe: str             # plan-card description (unicode)

    # --- exact area from the formula (never from the drawing) ---------------
    @property
    def value(self) -> Exact:
        d, f = self.dims, self.formula
        if f == "rect":
            return Exact.of(d["b"] * d["h"])
        if f == "square":
            return Exact.of(d["s"] ** 2)
        if f == "tri":
            return Exact.of(Fraction(d["b"] * d["h"], 2))
        if f == "rhombus":
            return Exact.of(Fraction(d["D"] * d["d"], 2))
        if f == "circle":
            return Exact.of(pi=d["r"] ** 2)
        if f == "semicircles":
            r = Fraction(d["diameter"], 2)
            return Exact.of(pi=d["n"] * r * r / 2)
        raise ValueError(f)

    # --- step-by-step LaTeX lines, generated from the same numbers ----------
    def calc_lines(self) -> list[str]:
        d, f, i = self.dims, self.formula, self.key[1:]
        A = f"A_{{{i}}}"
        unit = r"\ \text{cm}^2"
        res = f"{A}={self.value.latex()}{unit}"
        if f == "rect":
            return [rf"{A}=b\times h", rf"{A}={d['b']}\times {d['h']}", res]
        if f == "square":
            return [rf"{A}=s^2", rf"{A}={d['s']}^2={d['s']}\times {d['s']}", res]
        if f == "tri":
            return [rf"{A}=\frac{{b\times h}}{{2}}",
                    rf"{A}=\frac{{{d['b']}\times {d['h']}}}{{2}}="
                    rf"\frac{{{d['b'] * d['h']}}}{{2}}", res]
        if f == "rhombus":
            return [rf"{A}=\frac{{D\times d}}{{2}}",
                    rf"{A}=\frac{{{d['D']}\times {d['d']}}}{{2}}="
                    rf"\frac{{{d['D'] * d['d']}}}{{2}}", res]
        if f == "circle":
            return [rf"{A}=\pi r^2", rf"{A}=\pi({d['r']})^2=\pi\times {d['r'] ** 2}", res]
        if f == "semicircles":
            r = num(Fraction(d["diameter"], 2))
            n = d["n"]
            return [rf"r={d['diameter']}\div 2={r}\ \text{{cm}}",
                    rf"{A}={n}\times\frac{{\pi r^2}}{{2}}=\pi r^2" if n == 2 else
                    rf"{A}={n}\times\frac{{\pi r^2}}{{2}}",
                    rf"{A}=\pi({r})^2" if n == 2 else rf"{A}={n}\times\frac{{\pi({r})^2}}{{2}}",
                    res]
        raise ValueError(f)


@dataclass
class Dim:
    """A dimension annotation in model units."""
    kind: str        # arrow | text | radius
    p1: tuple
    p2: tuple = (0, 0)
    text: str = ""
    offset: tuple = (0, 0)     # label offset in FRAME units (labels keep their size)
    rotate: bool = False


@dataclass
class Problem:
    number: int
    slug: str
    title: str
    level: str
    statement: str
    parts: list[Part]
    seams: list[tuple]                 # internal boundaries ((x0,y0),(x1,y1))
    dims: list[Dim]
    checks: list[str] = field(default_factory=list)

    @property
    def positives(self):
        return [p for p in self.parts if p.sign > 0]

    @property
    def negatives(self):
        return [p for p in self.parts if p.sign < 0]

    @property
    def pos_total(self) -> Exact:
        t = Exact()
        for p in self.positives:
            t = t + p.value
        return t

    @property
    def neg_total(self) -> Exact:
        t = Exact()
        for p in self.negatives:
            t = t + p.value
        return t

    @property
    def answer(self) -> Exact:
        return self.pos_total - self.neg_total

    @property
    def n_figures(self) -> int:
        return sum(len(p.shapes) for p in self.parts)

    # --- combination lines --------------------------------------------------
    def plan_latex(self) -> str:
        s = "A_s=" + "+".join(f"A_{{{p.key[1:]}}}" for p in self.positives)
        s += "".join(f"-A_{{{p.key[1:]}}}" for p in self.negatives)
        return s

    def combine_lines(self) -> list[str]:
        unit = r"\ \text{cm}^2"
        pos = "+".join(p.value.latex() for p in self.positives)
        neg = "+".join(p.value.latex() for p in self.negatives)
        lines = [
            "A_s=(" + "+".join(f"A_{{{p.key[1:]}}}" for p in self.positives)
            + ")-(" + "+".join(f"A_{{{p.key[1:]}}}" for p in self.negatives) + ")",
            f"A_s=({pos})-({neg})",
        ]
        nt = self.neg_total
        neg_s = nt.latex() if nt.n_terms == 1 else f"({nt.latex()})"
        lines.append(f"A_s={self.pos_total.latex()}-{neg_s}")
        if self.answer.b == 0:
            lines.append(rf"A_s=\boxed{{{self.answer.latex()}{unit}}}")
        else:
            lines.append(f"A_s={self.answer.latex()}{unit}")
            lines.append(rf"A_s\approx\boxed{{{self.answer.approx()}{unit}}}")
        return lines

    @property
    def find_text(self) -> str:
        if self.answer.b == 0:
            return "Find the shaded area (cm²)."
        return "Give the exact answer (with π), then round to 2 decimal places."

    def answer_plain(self) -> str:
        if self.answer.b == 0:
            return f"{self.answer.plain()} cm²"
        return f"{self.answer.plain()} ≈ {self.answer.approx()} cm²"

    # --- integrity checks -----------------------------------------------------
    def verify(self) -> list[str]:
        log = []
        # 1. figure count rule of the request: 3..5 figures
        assert 3 <= self.n_figures <= 5, f"P{self.number}: {self.n_figures} figures"
        log.append(f"P{self.number}: {self.n_figures} figures (3–5) ✓")
        # 2. drawn area == formula area (±0.2 %)
        for p in self.parts:
            drawn = sum(s.poly().area for s in p.shapes)
            exact = p.value.value
            err = abs(drawn - exact) / exact
            assert err < 0.002, f"{p.key} drawn {drawn} vs {exact}"
            log.append(f"  {p.key} {p.name}: drawn {drawn:.4f} vs formula {exact:.4f} "
                       f"(err {err * 100:.4f} %) ✓")
        pos_polys = [s.poly() for p in self.positives for s in p.shapes]
        neg_polys = [s.poly() for p in self.negatives for s in p.shapes]
        silhouette = unary_union(pos_polys)
        # 3. positive parts pairwise disjoint (only shared edges)
        for i in range(len(pos_polys)):
            for j in range(i + 1, len(pos_polys)):
                ov = pos_polys[i].intersection(pos_polys[j]).area
                assert ov < 1e-6, f"P{self.number}: positives overlap {ov}"
        assert abs(silhouette.area - sum(q.area for q in pos_polys)) < 1e-4
        log.append("  positive parts disjoint (no region added twice) ✓")
        # 4. every gap inside the silhouette with clearance
        shrunk = silhouette.buffer(-CLEARANCE)
        for p in self.negatives:
            for s in p.shapes:
                assert shrunk.contains(s.poly()), f"{p.key} not inside with clearance"
        log.append(f"  every gap inside the silhouette (clearance ≥ {CLEARANCE} cm) ✓")
        # 5. gaps pairwise disjoint with clearance
        for i in range(len(neg_polys)):
            for j in range(i + 1, len(neg_polys)):
                dist = neg_polys[i].distance(neg_polys[j])
                assert dist >= CLEARANCE, f"gaps too close {dist}"
        log.append("  gaps pairwise separated (no region subtracted twice) ✓")
        # 6. tags on their own region, away from gaps
        for p in self.parts:
            pt = Point(p.tag_at)
            own = unary_union([s.poly() for s in p.shapes])
            assert own.contains(pt), f"{p.key} tag outside its region"
            if p.sign > 0:
                for g in neg_polys:
                    assert g.distance(pt) >= TAG_CLEAR, f"{p.key} tag too close to a gap"
        log.append("  tags sit on their own region ✓")
        # 7. sum of signed parts == answer; shapely cross-check
        shaded = silhouette.difference(unary_union(neg_polys)).area
        assert abs(shaded - self.answer.value) / self.answer.value < 0.002
        log.append(f"  shaded region measured {shaded:.4f} vs answer "
                   f"{self.answer.value:.4f} ✓")
        assert f"{self.answer.value:.2f}" == self.answer.approx()
        log.append(f"  answer = {self.answer.latex()} ≈ {self.answer.approx()} cm² ✓")
        return log

    def bounds(self):
        """Model-unit bounding box of the shapes."""
        allp = unary_union([s.poly() for p in self.parts for s in p.shapes])
        return allp.bounds


# ============================================================================
# THE THREE QUIZ PROBLEMS
# ============================================================================
def problem_1() -> Problem:
    L, H = 10, 6             # rectangle
    TH = 4                   # triangle height (horizontal tip)
    S = 3                    # square hole
    sq_c = (L / 2, H / 2)
    parts = [
        Part("A1", "rectangle", +1, "rect", {"b": L, "h": H},
             (Shape("rect", (0, 0, L, H)),), (1.6, 4.7),
             f"rectangle  {L} cm × {H} cm"),
        Part("A2", "triangle", +1, "tri", {"b": H, "h": TH},
             (Shape("tri", ((L, 0), (L, H), (L + TH, H / 2))),), (L + 1.25, H / 2),
             f"triangle  b = {H} cm, h = {TH} cm"),
        Part("A3", "square hole", -1, "square", {"s": S},
             (Shape("rect", (sq_c[0] - S / 2, sq_c[1] - S / 2,
                             sq_c[0] + S / 2, sq_c[1] + S / 2)),),
             (sq_c[0], sq_c[1] + 0.55),
             f"square hole  side {S} cm"),
    ]
    statement = (
        f"A hiking-trail sign in a Canadian park is shaped like an arrow: "
        f"a rectangle {L} cm long and {H} cm tall with a triangle attached to its "
        f"right side. The triangle's base is the {H} cm side and its height is "
        f"{TH} cm. A square hole with sides of {S} cm is cut out of the sign. "
        f"Find the area of the shaded region."
    )
    dims = [
        Dim("arrow", (0, -1.0), (L, -1.0), f"{L} cm", (0, -0.32)),
        Dim("arrow", (L, -1.0), (L + TH, -1.0), f"{TH} cm", (0, -0.32)),
        Dim("arrow", (-1.0, 0), (-1.0, H), f"{H} cm", (-0.55, 0)),
        Dim("text", (sq_c[0], sq_c[1] - 0.6), text=f"{S} cm"),
    ]
    p = Problem(1, "trail_sign", "TRAIL SIGN", "LEVEL 1 · 3 FIGURES", statement,
                parts, seams=[((L, 0), (L, H))], dims=dims)
    p.checks = [
        f"{p.answer.plain()} < {p.pos_total.plain()}: the hole was removed ✓",
        "Triangle area = base × height ÷ 2 ✓",
        "Units: cm × cm = cm² ✓",
    ]
    return p


def problem_2() -> Problem:
    L, W = 20, 10            # rectangle (W = diameter of each semicircle)
    R = Fraction(W, 2)
    RC = 3                   # centre circle radius
    r = float(R)
    parts = [
        Part("A1", "rectangle", +1, "rect", {"b": L, "h": W},
             (Shape("rect", (-L / 2, -W / 2, L / 2, W / 2)),), (6.2, 2.4),
             f"rectangle  {L} cm × {W} cm"),
        Part("A2", "two semicircles", +1, "semicircles", {"n": 2, "diameter": W},
             (Shape("semicircle", (-L / 2, 0, r, 90)),
              Shape("semicircle", (L / 2, 0, r, -90))),
             (-L / 2 - 2.2, 0),
             f"two semicircles  diameter {W} cm"),
        Part("A3", "centre circle", -1, "circle", {"r": RC},
             (Shape("circle", (0, 0, RC)),), (0, -1.3),
             f"centre circle  r = {RC} cm"),
    ]
    statement = (
        f"A table-hockey board is a rectangle {L} cm long and {W} cm wide with a "
        f"semicircle on each short side. The white centre circle, with a radius "
        f"of {RC} cm, is not painted. Find the area of the shaded (painted) part."
    )
    dims = [
        Dim("arrow", (-L / 2, W / 2 + 1.3), (L / 2, W / 2 + 1.3), f"{L} cm", (0, 0.30)),
        Dim("arrow", (-L / 2 + 1.2, -W / 2), (-L / 2 + 1.2, W / 2), f"{W} cm",
            (0.24, 0), rotate=True),
        Dim("radius", (0, 0), (RC, 0), f"r = {RC}", (1.08, 0)),
    ]
    p = Problem(2, "hockey_rink", "HOCKEY RINK", "LEVEL 2 · 4 FIGURES", statement,
                parts, seams=[((-L / 2, -W / 2), (-L / 2, W / 2)),
                              ((L / 2, -W / 2), (L / 2, W / 2))], dims=dims)
    p.checks = [
        f"2 semicircles = 1 circle, r = {num(R)} cm ✓",
        f"{p.answer.approx()} < {p.pos_total.approx()} (positive total) ✓",
        "π kept exact until the last line ✓",
    ]
    return p


def problem_3() -> Problem:
    L, H = 14, 8             # wall
    RH = 6                   # roof height
    S = 3                    # square window
    D, d = 4, 3              # rhombus diagonals
    RC = 2                   # round roof window
    sq = (-4.0, 4.5)
    rh = (4.0, 4.5)
    cc = (0.0, 10.6)
    parts = [
        Part("A1", "rectangle", +1, "rect", {"b": L, "h": H},
             (Shape("rect", (-L / 2, 0, L / 2, H)),), (0, 1.3),
             f"wall rectangle  {L} cm × {H} cm"),
        Part("A2", "triangle", +1, "tri", {"b": L, "h": RH},
             (Shape("tri", ((-L / 2, H), (L / 2, H), (0, H + RH))),), (-3.6, 9.1),
             f"roof triangle  b = {L} cm, h = {RH} cm"),
        Part("A3", "square window", -1, "square", {"s": S},
             (Shape("rect", (sq[0] - S / 2, sq[1] - S / 2, sq[0] + S / 2, sq[1] + S / 2)),),
             (sq[0], sq[1] + 0.55),
             f"square window  side {S} cm"),
        Part("A4", "rhombus window", -1, "rhombus", {"D": D, "d": d},
             (Shape("poly", ((rh[0] - D / 2, rh[1]), (rh[0], rh[1] + d / 2),
                             (rh[0] + D / 2, rh[1]), (rh[0], rh[1] - d / 2))),),
             (rh[0], rh[1] + 0.35),
             f"rhombus window  D = {D} cm, d = {d} cm"),
        Part("A5", "round window", -1, "circle", {"r": RC},
             (Shape("circle", (cc[0], cc[1], RC)),), (cc[0], cc[1] + 0.6),
             f"round window  r = {RC} cm"),
    ]
    statement = (
        f"The front of a mountain lodge is a {L} cm × {H} cm rectangle with a "
        f"triangular roof (base {L} cm, height {RH} cm). It has three white windows: "
        f"a square of side {S} cm, a rhombus with diagonals {D} cm and {d} cm, and a "
        f"circle of radius {RC} cm. Find the area of the shaded region."
    )
    dims = [
        Dim("arrow", (-L / 2, -1.0), (L / 2, -1.0), f"{L} cm", (0, -0.32)),
        Dim("arrow", (-L / 2 - 1.0, 0), (-L / 2 - 1.0, H), f"{H} cm", (-0.55, 0)),
        Dim("arrow", (L / 2 + 1.0, H), (L / 2 + 1.0, H + RH), f"{RH} cm", (0.55, 0)),
        Dim("text", (sq[0], sq[1] - 0.6), text=f"{S} cm"),
        Dim("text", (rh[0], rh[1] - d / 2 - 0.75), text=f"D = {D}, d = {d}"),
        Dim("radius", cc, (cc[0] + RC, cc[1]), f"r = {RC}", (0.30, -0.28)),
    ]
    p = Problem(3, "mountain_lodge", "MOUNTAIN LODGE", "LEVEL 3 · 5 FIGURES", statement,
                parts, seams=[((-L / 2, H), (L / 2, H))], dims=dims)
    p.checks = [
        "Each window is subtracted exactly once ✓",
        f"{p.answer.approx()} < {p.pos_total.plain()} (positive total) ✓",
        "Rhombus uses diagonals, not sides ✓",
    ]
    return p


PROBLEMS = [problem_1(), problem_2(), problem_3()]


def verify_all() -> list[str]:
    log = []
    for p in PROBLEMS:
        log += p.verify()
    return log


if __name__ == "__main__":
    for line in verify_all():
        print(line)
    print()
    for p in PROBLEMS:
        print(f"P{p.number} {p.title}: {p.answer_plain()}")
        for part in p.parts:
            print("   ", part.key, part.calc_lines())
        for line in p.combine_lines():
            print("   ", line)
    print("\nALL INTEGRITY CHECKS PASSED")
