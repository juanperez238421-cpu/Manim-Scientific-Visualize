"""Topic visual modules drawn in the lower-left zone of the solution layout.

Every module is declarative: the spec gives a type and parameters; numeric parameters are
expressions evaluated through the validator's safe evaluator against the problem's names
(givens, constants, answers). Modules never read code from the spec.

  motion_1d      agents on a number line (horizontal) or a height axis (vertical, free fall),
                 animated with a ValueTracker, live t/x/v readout, freeze at the event
  function_plot  curves y = f(x), marked points (intersections, roots, given points)
  stats          dot plot with mean / median / +-1 SD band, or box plot (Q1, median, Q3)
  geometry       rect_semicircle (composite area) | right_triangle (squares on the sides)
  chain          conversion chain: boxes joined by labelled arrows (stoichiometry, units)
  none           no figure: the zone repeats the key relation
"""
from __future__ import annotations

import numpy as np
import sympy as sp
from manim import (DOWN, LEFT, RIGHT, UP, Annulus, Arc, Arrow, Axes, Create, DashedLine, DecimalNumber, Dot, FadeIn, GrowArrow,
                   Line, NumberLine, Polygon, Rectangle, RoundedRectangle, Sector, Square, Text, Transform, ValueTracker, VGroup,
                   Write, always_redraw, linear, smooth, LaggedStart)

from .theme import (C_ACC, C_GAL, C_POS, C_VEL, FILL, INK, MUTED, RULE, P_BEAT, P_SHORT, P_MED, M, T, color, fit)

TYPES = ("motion_1d", "function_plot", "stats", "geometry", "chain", "none")


def _ev(expr, env):
    from ..validate import safe_eval
    if isinstance(expr, (int, float)):
        return float(expr)
    v = safe_eval(str(expr), env)
    return [float(sp.N(x)) for x in v] if isinstance(v, list) else float(sp.N(v))


def _ev_list(expr, env):
    from ..validate import safe_eval
    if isinstance(expr, list):
        return [float(x) if isinstance(x, (int, float)) else _ev(x, env) for x in expr]
    v = safe_eval(str(expr), env)
    return [float(sp.N(x)) for x in v]


def _fn(expr, env):
    from ..validate import safe_eval
    x = sp.Symbol("x")
    e = safe_eval(str(expr), {**env, "x": x})
    return sp.lambdify(x, e, "numpy")


# ------------------------------------------------------------------ parameter checks (used by validate)
def check_params(V, env):
    t = V.get("type")
    if t not in TYPES:
        raise ValueError(f"unknown visual type {t!r}")
    if t == "motion_1d":
        ax = V["axis"]
        lo, hi = _ev(ax["min"], env), _ev(ax["max"], env)
        assert hi > lo, "axis max must exceed min"
        assert 1 <= len(V["agents"]) <= 3, "1 to 3 agents"
        T_end = _ev(V["t_end"], env)
        assert T_end > 0
        for a in V["agents"]:
            for k in ("x0", "v0", "a"):
                _ev(a.get(k, 0), env)
            x_end = _x(a, T_end, env)
            assert lo - 1e-6 <= x_end <= hi + 1e-6, f"agent {a.get('label')} leaves the axis ({x_end})"
        if V.get("event"):
            assert 0 < _ev(V["event"]["t"], env) <= T_end + 1e-9
    elif t == "function_plot":
        xr, yr = V["x_range"], V["y_range"]
        assert xr[1] > xr[0] and yr[1] > yr[0]
        for c in V["curves"]:
            f = _fn(c["expr"], env)
            float(np.asarray(f(np.float64((xr[0] + xr[1]) / 2))))
        for p in V.get("points", []):
            x, y = _ev(p["x"], env), _ev(p["y"], env)
            assert xr[0] <= x <= xr[1] and yr[0] <= y <= yr[1], f"point {p.get('label')} outside the axes"
            if p.get("on"):
                for k in p["on"]:
                    f = _fn(V["curves"][k]["expr"], env)
                    assert abs(float(f(x)) - y) < 1e-6, f"point {p.get('label')} is not on curve {k}"
    elif t == "stats":
        data = _ev_list(V["data"], env)
        assert len(data) >= 2
        lo, hi = V["axis"][0], V["axis"][1]
        assert lo <= min(data) and max(data) <= hi, "data outside the axis"
        assert V.get("kind", "dot") in ("dot", "box")
    elif t == "geometry":
        fig = V["figure"]
        assert fig in ("rect_semicircle", "right_triangle")
        for k, e in V["params"].items():
            assert _ev(e, env) > 0, f"{k} must be positive"
    elif t == "chain":
        assert len(V["nodes"]) >= 2 and len(V["edges"]) == len(V["nodes"]) - 1
    return True


def _x(a, t, env):
    x0, v0, acc = (_ev(a.get(k, 0), env) for k in ("x0", "v0", "a"))
    return x0 + v0 * t + 0.5 * acc * t * t


def _v(a, t, env):
    v0, acc = (_ev(a.get(k, 0), env) for k in ("v0", "a"))
    return v0 + acc * t


def _fmt(v, d=1):
    s = f"{v:.{d}f}"
    return s[1:] if s.startswith("-0") and float(s) == 0 else s


# ------------------------------------------------------------------ builders
def build(scene, V, env, zone):
    """draw + animate inside zone=(x0, y0, x1, y1) (frame units, y0 top); returns mobjects to clear"""
    t = V.get("type", "none")
    fn = {"motion_1d": _motion, "function_plot": _plot, "stats": _stats, "geometry": _geometry, "chain": _chain}.get(t)
    if fn is None:
        return VGroup()
    return fn(scene, V, env, zone)


def _cap(scene, V, zone):
    if not V.get("caption"):
        return VGroup()
    c = fit(T(V["caption"], 17, MUTED), zone[2] - zone[0])
    c.move_to([(zone[0] + zone[2]) / 2, zone[1] - c.height / 2, 0])
    scene.play(FadeIn(c), run_time=0.5)
    return c


def _motion(scene, V, env, zone):
    x0z, y0z, x1z, y1z = zone
    cap = _cap(scene, V, zone)
    top = y0z - (cap.height + 0.15 if len(cap) or isinstance(cap, Text) else 0)
    ax = V["axis"]
    lo, hi, step = _ev(ax["min"], env), _ev(ax["max"], env), _ev(ax.get("step", (_ev(ax["max"], env) - _ev(ax["min"], env)) / 5), env)
    T_end = _ev(V["t_end"], env)
    vertical = V.get("orientation") == "vertical"
    agents = V["agents"]
    tt = ValueTracker(0.0)
    cols = [color(a.get("color"), [C_POS, C_ACC, C_VEL][i % 3]) for i, a in enumerate(agents)]
    unit = ax.get("unit", "m")
    if vertical:
        h = top - y1z - 1.05
        nl = NumberLine(x_range=[lo, hi + step, step], length=h, rotation=np.pi / 2, color=INK, include_numbers=True, font_size=20, decimal_number_config={"color": INK, "num_decimal_places": 0},
                        numbers_to_exclude=[hi + step], label_direction=LEFT, stroke_width=2)
        nl.move_to([x0z + 0.9, y1z + 1.05 + h / 2, 0])
        lab = T(f"{ax.get('label', 'y')} ({unit})", 17, MUTED).next_to(nl.n2p(hi + step), UP, buff=0.08)
        ground = Line(nl.n2p(lo) + LEFT * 0.4, nl.n2p(lo) + RIGHT * 3.2, color=STROKE_C, stroke_width=3)
    else:
        w = x1z - x0z - 0.4
        nl = NumberLine(x_range=[lo, hi + step, step], length=w, color=INK, include_numbers=True, font_size=20, decimal_number_config={"color": INK, "num_decimal_places": 0}, numbers_to_exclude=[hi + step], stroke_width=2)
        nl.move_to([(x0z + x1z) / 2, (top + y1z) / 2 + 0.25, 0])
        lab = T(f"{ax.get('label', 'x')} ({unit})", 17, MUTED).next_to(nl.n2p(hi + step), DOWN, buff=0.32).shift(LEFT * 0.1)
        ground = VGroup()
    scene.play(Create(nl), FadeIn(lab), FadeIn(ground), run_time=1.0)

    def pos(i):
        x = _x(agents[i], tt.get_value(), env)
        if vertical:
            return nl.n2p(x) + RIGHT * (1.2 + 0.9 * i)
        return nl.n2p(x) + UP * (0.32 + 0.0 * i)

    dots, tags = VGroup(), VGroup()
    for i, a in enumerate(agents):
        d = always_redraw(lambda i=i: Dot(pos(i), radius=0.11, color=cols[i]))
        tg = always_redraw(lambda i=i: fit(T(agents[i].get("label", ""), 16, cols[i]), 1.6).next_to(pos(i), UP if not vertical else RIGHT, buff=0.12 if not vertical else 0.18))
        dots.add(d); tags.add(tg)
        if not vertical:
            ghost = DashedLine(nl.n2p(_x(a, 0, env)) + DOWN * 0.15, nl.n2p(_x(a, 0, env)) + UP * 0.15, color=cols[i], stroke_width=2)
            scene.add(ghost); tags.add(ghost)
    scene.play(*[FadeIn(d) for d in dots], *[FadeIn(t) for t in tags], run_time=0.6)
    # live readout strip (fixed width)
    ro = VGroup()
    nums = []

    def field(label, col, getter, unit_s, widest, d):
        lab_ = T(label, 18, col)
        num = DecimalNumber(widest, num_decimal_places=d, font_size=26, color=col)
        u_ = T(unit_s, 18, col)
        g_ = VGroup(lab_, num, u_).arrange(RIGHT, buff=0.1)
        nums.append((num, u_, getter))
        return g_

    ro.add(field("t =", INK, lambda: tt.get_value(), "s", T_end, 2))
    for i, a in enumerate(agents[:2]):
        xs = [_x(a, T_end * k / 20, env) for k in range(21)]
        ro.add(field(f"{agents[i].get('short', ax.get('label', 'x'))} =", cols[i], (lambda i=i: _x(agents[i], tt.get_value(), env)), unit,
                     max(xs, key=lambda v: len(f"{v:.1f}")), 1))
        if V.get("show_v", True):
            vs = [abs(_v(a, T_end * k / 20, env)) if V.get("speed") else _v(a, T_end * k / 20, env) for k in range(21)]
            ro.add(field("v =", C_VEL, (lambda i=i: abs(_v(agents[i], tt.get_value(), env)) if V.get("speed") else _v(agents[i], tt.get_value(), env)),
                         ax.get("v_unit", "m/s"), max(vs, key=lambda v: len(f"{v:.1f}")), 1))
    ro.arrange(RIGHT, buff=0.45)
    fit(ro, x1z - x0z - 0.2)
    frame = RoundedRectangle(corner_radius=0.08, width=x1z - x0z, height=0.62, stroke_color=RULE, stroke_width=1.5, fill_color=FILL, fill_opacity=1)
    frame.move_to([(x0z + x1z) / 2, y1z + 0.31, 0])
    ro.move_to(frame)
    slow = V.get("time_note", "")
    note = T(slow, 15, MUTED).next_to(frame, UP, buff=0.06).align_to(frame, RIGHT) if slow else VGroup()
    for num, u_, getter in nums:
        num.set_value(getter())
        num.add_updater(lambda m, g=getter: m.set_value(g()))
        u_.add_updater(lambda m, n=num: m.next_to(n, RIGHT, buff=0.1))
    scene.play(FadeIn(frame), FadeIn(ro), FadeIn(note), run_time=0.6)
    run = float(V.get("run_time", 5.0))
    ev = V.get("event")
    scene.play(tt.animate.set_value(T_end), run_time=run, rate_func=linear)
    extra = VGroup()
    if ev:
        te = _ev(ev["t"], env)
        p = pos(0)
        if vertical:
            mk = VGroup(Line(p + LEFT * 0.45, p + RIGHT * 0.45, color=C_GAL, stroke_width=4))
            lab_e = fit(T(ev.get("label", ""), 17, C_GAL), 3.0).next_to(mk, RIGHT, buff=0.15).shift(UP * 0.3)
        else:
            mk = VGroup(Line(p + DOWN * 0.55, p + UP * 0.55, color=C_GAL, stroke_width=4))
            lab_e = fit(T(ev.get("label", ""), 17, C_GAL), 3.0).next_to(mk, UP, buff=0.05)
        extra.add(mk, lab_e)
        scene.play(Create(mk), FadeIn(lab_e), run_time=0.6)
    for m in ro:
        for k in m:
            k.clear_updaters()
    scene.wait(P_BEAT)
    return VGroup(cap, nl, lab, ground, dots, tags, frame, ro, note, extra)


STROKE_C = "#3C3C3C"


def _plot(scene, V, env, zone):
    x0z, y0z, x1z, y1z = zone
    cap = _cap(scene, V, zone)
    top = y0z - (cap.height + 0.12 if len(cap) or isinstance(cap, Text) else 0)
    xr, yr = V["x_range"], V["y_range"]
    w, h = x1z - x0z - 0.6, top - y1z - 0.35
    axes = Axes(x_range=xr, y_range=yr, x_length=w, y_length=h, tips=True,
                axis_config={"color": INK, "stroke_width": 2, "include_numbers": True, "font_size": 18, "tip_length": 0.16, "decimal_number_config": {"color": INK, "num_decimal_places": 0}},
                x_axis_config={"numbers_to_exclude": [0]}, y_axis_config={"numbers_to_exclude": [0]})
    axes.move_to([(x0z + x1z) / 2 + 0.1, (top + y1z) / 2, 0])
    xl = T("x", 18, MUTED).next_to(axes.x_axis.get_end(), RIGHT, buff=0.08)
    yl = T("y", 18, MUTED).next_to(axes.y_axis.get_end(), UP, buff=0.05)
    scene.play(Create(axes), FadeIn(xl), FadeIn(yl), run_time=1.0)
    out = VGroup(cap, axes, xl, yl)
    for k, c in enumerate(V["curves"]):
        f = _fn(c["expr"], env)
        col = color(c.get("color"), [C_POS, C_ACC, C_VEL][k % 3])
        rng = c.get("x_range", xr[:2])
        # keep the longest x interval where the curve stays inside the visible y range
        xs = np.linspace(rng[0], rng[1], 801)
        ys = np.array([float(f(x)) for x in xs])
        ok = (ys >= yr[0]) & (ys <= yr[1])
        best, cur = (0, 0), None
        for i, flag in enumerate(ok):
            if flag and cur is None:
                cur = i
            if (not flag or i == len(ok) - 1) and cur is not None:
                j = i if flag else i - 1
                if j - cur > best[1] - best[0]:
                    best = (cur, j)
                cur = None
        a_, b_ = xs[best[0]], xs[best[1]]
        rng = [a_, b_]
        g = axes.plot(lambda x, f=f: float(f(x)), x_range=[a_, b_, (b_ - a_) / 200], color=col, stroke_width=3.5)
        scene.play(Create(g), run_time=1.2)
        out.add(g)
        if c.get("label"):
            lx = c.get("label_x", rng[1] - (rng[1] - rng[0]) * 0.18)
            ly = float(np.clip(f(lx), yr[0], yr[1]))
            lab = fit(M(c["label"], 22, col), 2.6)
            lab.next_to(axes.c2p(lx, ly), UP if c.get("label_side", "up") == "up" else DOWN, buff=0.12)
            scene.play(FadeIn(lab), run_time=0.4)
            out.add(lab)
    for p in V.get("points", []):
        x, y = _ev(p["x"], env), _ev(p["y"], env)
        col = color(p.get("color"), C_GAL)
        d = Dot(axes.c2p(x, y), radius=0.085, color=col)
        guides = VGroup(DashedLine(axes.c2p(x, 0), axes.c2p(x, y), color=MUTED, stroke_width=1.5), DashedLine(axes.c2p(0, y), axes.c2p(x, y), color=MUTED, stroke_width=1.5)) if p.get("guides", True) and y != 0 else VGroup()
        lab = fit(M(p.get("label", f"({x:g},\\ {y:g})"), 22, col), 2.4)
        lab.next_to(d, {"ur": UP + RIGHT, "ul": UP + LEFT, "dr": DOWN + RIGHT, "dl": DOWN + LEFT, "u": UP, "d": DOWN, "r": RIGHT, "l": LEFT}[p.get("side", "ur")], buff=0.08)
        scene.play(Create(guides), FadeIn(d, scale=0.5), FadeIn(lab), run_time=0.7)
        out.add(guides, d, lab)
    for s in V.get("slope_triangles", []):
        (xa, ya), (xb, yb) = [(_ev(a, env), _ev(b, env)) for a, b in s["points"]]
        corner = axes.c2p(xb, ya)
        run_l = Line(axes.c2p(xa, ya), corner, color=C_VEL, stroke_width=3)
        rise_l = Line(corner, axes.c2p(xb, yb), color=C_VEL, stroke_width=3)
        lr = M(rf"\Delta x = {xb - xa:g}", 20, C_VEL).next_to(run_l, DOWN, buff=0.08)
        ll = M(rf"\Delta y = {yb - ya:g}", 20, C_VEL).next_to(rise_l, RIGHT, buff=0.08)
        scene.play(Create(run_l), FadeIn(lr), run_time=0.6)
        scene.play(Create(rise_l), FadeIn(ll), run_time=0.6)
        out.add(run_l, rise_l, lr, ll)
    scene.wait(P_BEAT)
    return out


def _stats(scene, V, env, zone):
    x0z, y0z, x1z, y1z = zone
    cap = _cap(scene, V, zone)
    top = y0z - (cap.height + 0.12 if len(cap) or isinstance(cap, Text) else 0)
    data = _ev_list(V["data"], env)
    lo, hi, st_ = V["axis"]
    w = x1z - x0z - 0.5
    nl = NumberLine(x_range=[lo, hi, st_], length=w, color=INK, include_numbers=True, font_size=20, decimal_number_config={"color": INK, "num_decimal_places": 0}, stroke_width=2)
    base_y = y1z + 0.55
    nl.move_to([(x0z + x1z) / 2, base_y, 0])
    unit = V.get("unit", "")
    lab = T(unit, 16, MUTED).next_to(nl, RIGHT, buff=0.08).shift(UP * 0.05) if unit else VGroup()
    scene.play(Create(nl), FadeIn(lab), run_time=0.8)
    out = VGroup(cap, nl, lab)
    kind = V.get("kind", "dot")
    avail = top - base_y - 0.35
    import statistics as stx
    if kind == "dot":
        counts = {}
        dots = VGroup()
        r = min(0.13, avail / (2.2 * max(1, max(data.count(v) for v in data))))
        for v in data:
            k = counts.get(v, 0); counts[v] = k + 1
            dots.add(Dot(nl.n2p(v) + UP * (0.25 + r + 2.15 * r * k), radius=r, color=C_POS))
        scene.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in dots], lag_ratio=0.12), run_time=1.6)
        out.add(dots)
        ytop = max(d.get_top()[1] for d in dots) + 0.25
        marks = V.get("show", ["mean", "median"])
        if "sd" in marks:
            m = stx.mean(data); s = stx.pstdev(data)
            band = Rectangle(width=nl.n2p(m + s)[0] - nl.n2p(m - s)[0], height=ytop - base_y - 0.05, stroke_width=0, fill_color=C_VEL, fill_opacity=0.15)
            band.move_to([(nl.n2p(m + s)[0] + nl.n2p(m - s)[0]) / 2, (ytop + base_y) / 2, 0])
            bl = M(r"\bar{x}\pm\sigma", 20, C_VEL).next_to(band, UP, buff=0.05).shift(RIGHT * 0.9)
            scene.play(FadeIn(band), FadeIn(bl), run_time=0.8)
            out.add(band, bl)
        for name, val, col, side in (("mean", stx.mean(data), C_ACC, UP), ("median", stx.median(data), C_GAL, UP)):
            if name not in marks:
                continue
            ln = DashedLine(nl.n2p(val) + UP * 0.05, nl.n2p(val) + UP * (ytop - base_y), color=col, stroke_width=3)
            tx = fit(M((r"\bar{x}" if name == "mean" else r"\mathrm{Med}") + f" = {_fmt(val, 2) if abs(val - round(val)) > 1e-9 else int(round(val))}", 20, col), 2.6)
            tx.next_to(ln, UP, buff=0.05)
            if name == "median" and "mean" in marks and abs(stx.mean(data) - val) < (hi - lo) * 0.12:
                tx.shift(LEFT * (tx.width / 2 + 0.1));
            if name == "mean" and "median" in marks and abs(stx.median(data) - val) < (hi - lo) * 0.12:
                tx.shift(RIGHT * (tx.width / 2 + 0.1))
            scene.play(Create(ln), FadeIn(tx), run_time=0.7)
            out.add(ln, tx)
    else:
        from ..validate import _q_halves
        q1, q3 = float(_q_halves(data, 1)), float(_q_halves(data, 3))
        med = stx.median(data)
        dots = VGroup(*[Dot(nl.n2p(v) + UP * 0.3, radius=0.08, color=C_POS) for v in data])
        scene.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in dots], lag_ratio=0.1), run_time=1.2)
        yb = base_y + 0.3 + min(1.4, avail * 0.55)
        bh = min(0.9, avail * 0.4)
        box = Rectangle(width=nl.n2p(q3)[0] - nl.n2p(q1)[0], height=bh, stroke_color=C_POS, stroke_width=3, fill_color=C_POS, fill_opacity=0.12)
        box.move_to([(nl.n2p(q1)[0] + nl.n2p(q3)[0]) / 2, yb, 0])
        mline = Line([nl.n2p(med)[0], yb - bh / 2, 0], [nl.n2p(med)[0], yb + bh / 2, 0], color=C_GAL, stroke_width=4)
        wl = Line([nl.n2p(min(data))[0], yb, 0], box.get_left(), color=INK, stroke_width=2)
        wr = Line(box.get_right(), [nl.n2p(max(data))[0], yb, 0], color=INK, stroke_width=2)
        caps = VGroup(*[Line([nl.n2p(v)[0], yb - 0.15, 0], [nl.n2p(v)[0], yb + 0.15, 0], color=INK, stroke_width=2) for v in (min(data), max(data))])
        scene.play(Create(wl), Create(wr), Create(caps), run_time=0.6)
        scene.play(Create(box), run_time=0.6)
        scene.play(Create(mline), run_time=0.4)
        labs = VGroup(M(f"Q_1 = {q1:g}", 19, C_POS).next_to(box.get_corner(DOWN + LEFT), DOWN, buff=0.08),
                      M(f"Q_3 = {q3:g}", 19, C_POS).next_to(box.get_corner(DOWN + RIGHT), DOWN, buff=0.08),
                      M(rf"\mathrm{{Med}} = {med:g}", 19, C_GAL).next_to(mline, UP, buff=0.06))
        iqr = VGroup(DashedLine(box.get_corner(UP + LEFT) + UP * 0.12, box.get_corner(UP + RIGHT) + UP * 0.12, color=C_VEL, stroke_width=2))
        scene.play(FadeIn(labs), run_time=0.6)
        out.add(dots, box, mline, wl, wr, caps, labs)
    scene.wait(P_BEAT)
    return out


def _geometry(scene, V, env, zone):
    x0z, y0z, x1z, y1z = zone
    cap = _cap(scene, V, zone)
    top = y0z - (cap.height + 0.12 if len(cap) or isinstance(cap, Text) else 0)
    P = {k: _ev(e, env) for k, e in V["params"].items()}
    u = V.get("unit", "cm")
    cx, cy = (x0z + x1z) / 2, (top + y1z) / 2
    out = VGroup(cap)
    if V["figure"] == "rect_semicircle":
        w, h = P["w"], P["h"]
        r = h / 2
        k = min((x1z - x0z - 1.2) / (w + r), (top - y1z - 0.9) / h)
        W, H, R = w * k, h * k, r * k
        left = cx - (W + R) / 2
        rect = Rectangle(width=W, height=H, stroke_color=INK, stroke_width=3, fill_color=C_POS, fill_opacity=0.18).move_to([left + W / 2, cy, 0])
        semi = Sector(radius=R, start_angle=-np.pi / 2, angle=np.pi, stroke_color=INK, stroke_width=3, fill_color=C_VEL, fill_opacity=0.25)
        semi.move_to(rect.get_right() + RIGHT * R / 2)
        dia = DashedLine(rect.get_corner(UP + RIGHT), rect.get_corner(DOWN + RIGHT), color=MUTED, stroke_width=2)
        lw = M(f"{w:g}\\ \\mathrm{{{u}}}", 22, INK).next_to(rect, DOWN, buff=0.1)
        lh = M(f"{h:g}\\ \\mathrm{{{u}}}", 22, INK).next_to(rect, LEFT, buff=0.1)
        lr = M(f"r = {r:g}", 20, C_VEL).next_to(semi, UP, buff=0.05)
        scene.play(Create(rect), FadeIn(lw), FadeIn(lh), run_time=1.0)
        scene.play(Create(dia), Create(semi), FadeIn(lr), run_time=1.0)
        a1 = M(V.get("label_a", f"{w*h:g}"), 22, C_POS).move_to(rect)
        a2 = fit(M(V.get("label_b", r"\tfrac{1}{2}\pi r^2"), 20, C_VEL), R * 0.95).move_to(semi.get_center() + RIGHT * R * 0.12)
        scene.play(FadeIn(a1), FadeIn(a2), run_time=0.6)
        out.add(rect, semi, dia, lw, lh, lr, a1, a2)
    else:  # right_triangle with squares on the sides
        a, b = P["a"], P["b"]
        c = (a * a + b * b) ** 0.5
        span_w, span_h = a + b + c * 0.0, b + a  # rough bounding of figure with squares
        k = min((x1z - x0z - 0.6) / (a + b + 0.2), (top - y1z - 0.4) / (a + b + 0.2)) * 0.95
        A = np.array([cx - (a * k) / 2 + (b * k) * 0.1, cy - (b * k) / 2 + (a * k) * 0.0, 0])
        # right angle at C0; legs along +x (a) and +y (b)
        C0 = np.array([cx - a * k * 0.25, cy - b * k * 0.15, 0])
        Pa = C0 + RIGHT * a * k
        Pb = C0 + UP * b * k
        tri = Polygon(C0, Pa, Pb, stroke_color=INK, stroke_width=3, fill_color=C_POS, fill_opacity=0.15)
        ra = Square(0.18, stroke_color=INK, stroke_width=2).move_to(C0 + np.array([0.09, 0.09, 0]))
        sq_a = Polygon(C0, Pa, Pa + DOWN * a * k, C0 + DOWN * a * k, stroke_color=C_VEL, stroke_width=2, fill_color=C_VEL, fill_opacity=0.15)
        sq_b = Polygon(C0, C0 + LEFT * b * k, Pb + LEFT * b * k, Pb, stroke_color=C_VEL, stroke_width=2, fill_color=C_VEL, fill_opacity=0.15)
        d = (Pb - Pa); n = np.array([d[1], -d[0], 0])  # outward normal (away from C0)
        sq_c = Polygon(Pa, Pb, Pb + n, Pa + n, stroke_color=C_GAL, stroke_width=2, fill_color=C_GAL, fill_opacity=0.12)
        grp = VGroup(tri, ra, sq_a, sq_b, sq_c)
        # fit whole figure into zone
        s = min((x1z - x0z - 0.3) / grp.width, (top - y1z - 0.2) / grp.height, 1.0)
        grp.scale(s).move_to([cx, (top + y1z) / 2, 0])
        la = M(f"{a:g}", 22, INK).next_to(Line(grp[0].get_vertices()[0], grp[0].get_vertices()[1]), UP, buff=0.06)
        lb = M(f"{b:g}", 22, INK).next_to(Line(grp[0].get_vertices()[0], grp[0].get_vertices()[2]), RIGHT, buff=0.06)
        lc = M("c", 24, C_GAL).move_to((grp[0].get_vertices()[1] + grp[0].get_vertices()[2]) / 2 + 0.22 * (n / np.linalg.norm(n)) * -1)
        scene.play(Create(tri), Create(ra), FadeIn(la), FadeIn(lb), FadeIn(lc), run_time=1.0)
        aa = M(f"{a*a:g}", 22, C_VEL).move_to(grp[2]); ab = M(f"{b*b:g}", 22, C_VEL).move_to(grp[3]); ac = M(f"{c*c:g}", 24, C_GAL).move_to(grp[4])
        scene.play(Create(grp[2]), FadeIn(aa), run_time=0.6)
        scene.play(Create(grp[3]), FadeIn(ab), run_time=0.6)
        scene.play(Create(grp[4]), FadeIn(ac), run_time=0.8)
        out.add(grp, la, lb, lc, aa, ab, ac)
    scene.wait(P_BEAT)
    return out


def _chain(scene, V, env, zone):
    x0z, y0z, x1z, y1z = zone
    cap = _cap(scene, V, zone)
    top = y0z - (cap.height + 0.12 if len(cap) or isinstance(cap, Text) else 0)
    nodes = [M(n, 24, C_POS if k == len(V["nodes"]) - 1 else INK) for k, n in enumerate(V["nodes"])]
    boxes = [RoundedRectangle(corner_radius=0.1, width=m.width + 0.3, height=m.height + 0.26, stroke_color=(C_POS if k == len(nodes) - 1 else STROKE_C), stroke_width=2,
                              fill_color=FILL, fill_opacity=1) for k, m in enumerate(nodes)]
    items = [VGroup(b, m) for b, m in zip(boxes, nodes)]
    for b, m in items:
        m.move_to(b)
    edges = [M(e, 20, C_VEL) for e in V["edges"]]
    # layout: two columns zig-zag, top to bottom
    W = x1z - x0z
    n = len(items)
    rows = (n + 1) // 2
    rh = (top - y1z) / rows
    pos = []
    for k in range(n):
        r, c = k // 2, k % 2
        if r % 2 == 1:
            c = 1 - c
        pos.append([x0z + W * (0.26 + 0.48 * c), top - rh * (r + 0.5), 0])
    for it, p in zip(items, pos):
        fit(it, W * 0.44, rh * 0.62)
        it.move_to(p)
    scene.play(FadeIn(items[0]), run_time=0.5)
    out = VGroup(cap, *items)
    for k in range(1, n):
        a, b = items[k - 1], items[k]
        if abs(a.get_center()[1] - b.get_center()[1]) < 1e-3:
            s, e = (a.get_right(), b.get_left()) if a.get_center()[0] < b.get_center()[0] else (a.get_left(), b.get_right())
        else:
            s, e = a.get_bottom(), b.get_top()
        ar = Arrow(s, e, buff=0.08, color=C_VEL, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        el = fit(edges[k - 1], W * 0.42, rh * 0.36)
        if abs(s[1] - e[1]) < 1e-3:
            el.next_to(ar, UP, buff=0.04)
        else:
            el.next_to(ar, RIGHT if ar.get_center()[0] < (x0z + x1z) / 2 else LEFT, buff=0.08)
        scene.play(GrowArrow(ar), FadeIn(el), run_time=0.6)
        scene.play(FadeIn(b, shift=(e - s) / np.linalg.norm(e - s) * 0.2), run_time=0.5)
        out.add(ar, el)
    scene.wait(P_BEAT)
    return out
