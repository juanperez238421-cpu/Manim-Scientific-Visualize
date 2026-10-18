"""Generic solution-video scene: one ManimCE scene renders any validated spec.

  P2V_SPEC=path/to/spec.json [P2V_PROBLEMS=1,3] [P2V_OUT=dir] manim -qh --fps 30 scene.py SolutionVideo

Lifecycle per problem (the page is the visual authority, it is never retyped):
  page      full page, the problem block outlined, constants from the instructions picked up as chips
  zoom      the page scales so the problem fills the frame; a pixel-identical 300 dpi crop is lifted on top
  read      every given value is highlighted at its real box on the page and flies into a data chip
  thumb     the statement shrinks to a thumbnail (top left); chips line up below it
  derive    right panel: Find / Model / Equation / Substitute / Solve rows (one operation per row, with a note)
  visual    lower-left zone: topic figure (motion, plot, statistics, geometry, conversion chain)
  answers   boxed answers, independent verification, CHECKED badge
  return    the statement returns to the page, the page zooms to the work area and the answers are written
            there (blue, green tick); zoom out; annotations stay on the page for the rest of the video
Opening (title, pages, stages, colour legend) and closing (all answers, checked badge) frame the video,
which starts and ends on a blank white frame.
"""
from __future__ import annotations

import json
import os
import sys
import textwrap
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import (DOWN, LEFT, ORIGIN, RIGHT, UL, UP, UR, Create, FadeIn, FadeOut, Group, ImageMobject, Rectangle,  # noqa: E402
                   RoundedRectangle, Scene, SurroundingRectangle, TransformFromCopy, VGroup, Write, config, smooth, Line, Indicate)

from pdf2video.render import visuals  # noqa: E402
from pdf2video.render.theme import (BG, BOLD, C_ACC, C_GAL, C_POS, C_VEL, FILL, HILITE, INK, ITALIC, MUTED, RULE, P_BEAT, P_LONG,  # noqa: E402
                                     P_MED, P_SHORT, TS, XL, XR, YB, YT, M, T, fit, read_time)
from pdf2video.validate import fmt_value, validate  # noqa: E402

config.background_color = BG
PX_PER_UNIT = 1920 / 14.222
STAGES = ["Read", "Model", "Equation", "Substitute", "Solve", "Verify"]


def wrap(s, width):
    return "\n".join(textwrap.wrap(str(s), width))


class SolutionVideo(Scene):
    # ------------------------------------------------------------------ setup
    def setup(self):
        spec = os.environ["P2V_SPEC"]
        self.out = Path(os.getenv("P2V_OUT", Path(spec).parent / "build"))
        self.out.mkdir(parents=True, exist_ok=True)
        self.rep, self.doc, self.S = validate(spec, workdir=self.out / "work", verbose=False)
        if not self.rep["pass"]:
            raise SystemExit("spec does not validate: run `p2v validate` first")
        only = os.getenv("P2V_PROBLEMS")
        self.only = set(only.split(",")) if only else None
        self.reports = {r["id"]: r for r in self.rep["problems"]}
        self.ann = {}  # page -> list of annotation mobjects (kept on the page)
        self.pg = None  # current page group: Group(image, *annotations)
        self.cur_page = None
        self.log = []
        self.rows = []

    def w(self, s):
        self.wait(max(0.05, s * TS))

    # ------------------------------------------------------------------ images (LOD: resampled to on-screen size)
    def lod(self, path, px_w):
        px_w = max(16, int(round(px_w)))
        im = Image.open(path)
        if im.width <= px_w * 1.05:
            return str(path)
        out = self.out / "work" / f"{Path(path).stem}_w{px_w}.png"
        if not out.exists():
            im.resize((px_w, round(im.height * px_w / im.width)), Image.LANCZOS).save(out)
        return str(out)

    def img(self, path, width_units):
        m = ImageMobject(self.lod(path, width_units * PX_PER_UNIT))
        m.scale_to_fit_width(width_units)
        return m

    # ------------------------------------------------------------------ page mapping
    def P(self, n):
        return self.doc.page(n)

    def mapping(self):
        im = self.pg[0]
        P = self.P(self.cur_page)
        return im.get_corner(UL), im.height / P.height

    def to_xy(self, x, y):
        ul, s = self.mapping()
        return ul + np.array([x * s, -y * s, 0])

    def box_rect(self, box, pad=1.5, **kw):
        a, b = self.to_xy(box[0] - pad, box[1] - pad), self.to_xy(box[2] + pad, box[3] + pad)
        r = Rectangle(width=b[0] - a[0], height=a[1] - b[1], **kw)
        r.move_to((a + b) / 2)
        return r

    def full_target(self, n):
        P = self.P(n)
        h = 7.7
        return h / P.height, np.array([0.0, 0.0, 0]) + np.array([-P.width / 2 * h / P.height, P.height / 2 * h / P.height, 0])

    def fit_target(self, n, box, maxw=13.4, maxh=6.1, center=(0, 0.5)):
        s = min(maxw / (box[2] - box[0]), maxh / (box[3] - box[1]))
        c = np.array([center[0], center[1], 0])
        ul = c - np.array([(box[0] + box[2]) / 2 * s, -(box[1] + box[3]) / 2 * s, 0])
        return s, ul

    def move_page(self, s1, ul1, extra=(), run_time=1.6, also=()):
        ul0, s0 = self.mapping()
        k = s1 / s0
        anims = list(also)
        for m in (self.pg, *extra):
            anims.append(m.animate.scale(k, about_point=ul0).shift(ul1 - ul0))
        self.play(*anims, run_time=run_time, rate_func=smooth)

    def show_page(self, n, target=None, run_time=1.0):
        P = self.P(n)
        s, ul = target or self.full_target(n)
        im = self.img(P.image, P.width * s)
        im.scale_to_fit_height(P.height * s)
        im.move_to(ul + np.array([P.width * s / 2, -P.height * s / 2, 0]))
        frame = Rectangle(width=im.width, height=im.height, stroke_color=RULE, stroke_width=1.2).move_to(im)
        old = self.pg
        self.cur_page = n
        self.pg = Group(im, frame)
        for a in self.ann.get(n, []):
            self.pg.add(a["mob"])
        self._place_annotations(n)
        anims = [FadeIn(self.pg)]
        if old is not None:
            anims.append(FadeOut(old))
        self.play(*anims, run_time=run_time)

    def crop(self, box, pad=4):
        path, cbox = self.doc.crop(self.cur_page, box, pad=pad)
        ul, s = self.mapping()
        w = (cbox[2] - cbox[0]) * s
        m = ImageMobject(self.lod(path, w * PX_PER_UNIT))
        m.scale_to_fit_width(w)
        m.move_to(self.to_xy((cbox[0] + cbox[2]) / 2, (cbox[1] + cbox[3]) / 2))
        return m, cbox

    # ------------------------------------------------------------------ annotations (teacher ink at real page positions)
    def _place_annotations(self, n):
        for a in self.ann.get(n, []):
            self._fit_ann(a)

    def _fit_ann(self, a):
        ul, s = self.mapping()
        m = a["mob"]
        m.scale_to_fit_height(a["h_pt"] * s)
        m.move_to(self.to_xy(a["x"], a["y"]), aligned_edge=LEFT)

    def annotation(self, text, x, y, size_pt=12.5):
        ref = T("Hg", 26, C_POS, slant=ITALIC)
        txt = T(text, 26, C_POS, slant=ITALIC)
        tick = M(r"\checkmark", 30, C_GAL)
        tick.scale_to_fit_height(ref.height * 0.8)
        g = VGroup(txt, tick).arrange(RIGHT, buff=ref.height * 0.5, aligned_edge=DOWN)
        h_pt = size_pt * g.height / ref.height
        a = {"mob": g, "x": x, "y": y, "h_pt": h_pt, "text": text}
        self._fit_ann(a)
        return a

    # ------------------------------------------------------------------ right panel (derivation rows, scrolling)
    PANEL_X0, PANEL_X1 = 0.05, XR

    def panel_add(self, row, anim="write", run_time=0.9):
        row.align_to(np.array([self.PANEL_X0, 0, 0]), LEFT)
        top = (self.rows[-1].get_bottom()[1] - 0.24) if self.rows else self.panel_top
        row.move_to([row.get_center()[0], top - row.height / 2, 0])
        over = (YB + 0.05) - row.get_bottom()[1]
        if over > 0:
            vis = [r for r in self.rows]
            gone = [r for r in vis if r.get_top()[1] + over > self.panel_top + 0.02]
            self.play(*[r.animate.shift(UP * over) for r in vis if r not in gone], *[FadeOut(r, shift=UP * over) for r in gone], run_time=0.6)
            self.rows = [r for r in self.rows if r not in gone]
            row.shift(UP * over)
        self.rows.append(row)
        if anim == "write":
            self.play(Write(row), run_time=run_time)
        else:
            self.play(FadeIn(row, shift=UP * 0.15), run_time=run_time)

    def step_row(self, stage, note, tex, col=INK, size=32):
        head = T((stage.upper() + ("  ·  " + note if note else "")), 15, MUTED)
        fit(head, self.PANEL_X1 - self.PANEL_X0)
        if stage.upper() in ("VERIFY",):
            head.set_color(C_GAL)
        math = fit(M(tex, size, col), self.PANEL_X1 - self.PANEL_X0 - 0.1, 1.3)
        return VGroup(head, math).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

    # ------------------------------------------------------------------ construct
    def construct(self):
        S = self.S
        probs = [p for p in S["problems"] if self.only is None or p["id"] in self.only]
        self.w(0.3)
        self.opening(probs)
        for k, P in enumerate(probs):
            self.problem(P, self.reports[P["id"]], k, len(probs))
        self.closing(probs)
        (self.out / "observed.json").write_text(json.dumps({"spec": self.S.get("title"), "log": self.log}, indent=1, ensure_ascii=False))

    # ------------------------------------------------------------------ opening
    def opening(self, probs):
        S = self.S
        title = fit(T(S.get("title", "Solutions"), 40, INK, weight=BOLD), 7.4)
        sub = fit(T(S.get("subject", ""), 22, MUTED), 7.4)
        meta = fit(T(f"{self.doc.path.name}  ·  {len(probs)} problem{'s' if len(probs) != 1 else ''}  ·  every value checked", 17, MUTED), 7.4)
        stages = VGroup()
        for i, s in enumerate(STAGES):
            stages.add(T(s, 19, INK))
            if i < len(STAGES) - 1:
                stages.add(T("→", 19, MUTED))
        stages.arrange(RIGHT, buff=0.14)
        fit(stages, 7.4)
        legend = VGroup()
        for col, lab in ((C_VEL, "data from the page"), (C_ACC, "condition / sign"), (C_POS, "result"), (C_GAL, "verified")):
            legend.add(VGroup(RoundedRectangle(corner_radius=0.04, width=0.36, height=0.2, fill_color=col, fill_opacity=1, stroke_width=0), T(lab, 16, INK)).arrange(RIGHT, buff=0.12))
        legend.arrange_in_grid(rows=2, cols=2, buff=(0.5, 0.18), col_alignments="ll")
        col = VGroup(title, sub, meta, stages, legend).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        col[3].shift(DOWN * 0.25); col[4].shift(DOWN * 0.35)
        col.move_to([-2.6, 0.1, 0])
        pages = sorted({self.reports[p["id"]]["page"] for p in probs})
        n0 = pages[0]
        P0 = self.P(n0)
        h = 6.6
        thumb = self.img(P0.image, P0.width * h / P0.height)
        thumb.scale_to_fit_height(h).move_to([4.15, 0, 0])
        tframe = Rectangle(width=thumb.width, height=thumb.height, stroke_color=RULE, stroke_width=1.2).move_to(thumb)
        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(sub), FadeIn(meta), FadeIn(thumb), FadeIn(tframe), run_time=0.9)
        self.play(FadeIn(stages, lag_ratio=0.1), run_time=1.0)
        self.play(FadeIn(legend), run_time=0.6)
        self.w(P_LONG)
        self.play(FadeOut(col), FadeOut(thumb), FadeOut(tframe), run_time=0.7)
        self.show_page(n0, run_time=0.8)

    # ------------------------------------------------------------------ one problem
    def lift_box(self, r):
        """statement + figures/tables of the block (not the empty work box)"""
        box = list(r["region"])
        parts = [r["statement_box"]] if "statement_box" in r else []
        sb = self._statement_box(r)
        parts = [sb]
        bw, bh = box[2] - box[0], box[3] - box[1]
        for L in self.doc.lines(r["page"], box):
            parts.append(L.box)
        for g in self.doc.page(r["page"]).graphics:
            if g[1] >= box[1] - 1 and g[3] <= box[3] + 1 and not ((g[2] - g[0]) > 0.75 * bw and (g[3] - g[1]) > 0.35 * bh):
                if (g[2] - g[0]) * (g[3] - g[1]) > 30:
                    parts.append(g)
        u = [min(p[0] for p in parts), min(p[1] for p in parts), max(p[2] for p in parts), max(p[3] for p in parts)]
        return [u[0] - 2, u[1] - 2, u[2] + 2, u[3] + 2]

    def _statement_box(self, r):
        from pdf2video.segment import detect
        if not hasattr(self, "_det"):
            self._det = {p.id: p for p in detect(self.doc)}
        return self._det[r["id"]].statement

    def chip(self, tex, col=C_VEL):
        m = M(tex, 26, INK)
        b = RoundedRectangle(corner_radius=0.08, width=m.width + 0.28, height=max(0.5, m.height + 0.2), stroke_color=col, stroke_width=2, fill_color=FILL, fill_opacity=1)
        m.move_to(b)
        return VGroup(b, m)

    def problem(self, P, r, k, n_total):
        n = r["page"]
        if self.cur_page != n:
            self.show_page(n)
        # -- page: outline the block, problem tag in the margin
        blk = self.box_rect(r["region"], pad=0, stroke_color=C_POS, stroke_width=2.5)
        tag = VGroup(T(f"PROBLEM {P['id']}", 22, C_POS, weight=BOLD), fit(T(wrap(P.get("title", ""), 18), 18, INK), 3.0)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        tag.move_to([XL + tag.width / 2, 2.6, 0])
        self.play(Create(blk), FadeIn(tag, shift=RIGHT * 0.2), run_time=0.9)
        # constants used by this problem (from the instructions): highlight on the page, park as chips
        consts = [c for c in self.S.get("constants", []) if c["name"] in P.get("uses", [])]
        cchips = []
        for c in consts:
            m = next((x for x in self.rep["constants"] if x["name"] == c["name"]), None)
            hl = self.box_rect(m["box"], pad=1.5, stroke_color=C_VEL, stroke_width=2, fill_color=HILITE, fill_opacity=0.55)
            ch = self.chip(c["chip"])
            ch.move_to([XR - ch.width / 2, 2.6 - 0.7 * len(cchips), 0])
            self.play(FadeIn(hl), run_time=0.5)
            self.play(TransformFromCopy(hl, ch, path_arc=-0.5), run_time=0.9)
            self.log.append({"problem": P["id"], "kind": "constant", "name": c["name"], "chip": c["chip"], "box": m["box"]})
            self.play(FadeOut(hl), run_time=0.3)
            cchips.append(ch)
        self.w(P_BEAT)
        # -- zoom to the statement (+ figure/table) and lift a crisp crop
        lb = self.lift_box(r)
        s1, ul1 = self.fit_target(n, lb)
        self.play(FadeOut(tag), run_time=0.4)
        self.pg.add(blk)
        also = []
        if cchips:
            row = VGroup(*[c.copy() for c in cchips]).arrange(RIGHT, buff=0.2)
            row.move_to([XL + row.width / 2, -3.2, 0])
            also = [c.animate.move_to(t.get_center()) for c, t in zip(cchips, row)]
        self.move_page(s1, ul1, run_time=1.6, also=also)
        self.pg.remove(blk); self.remove(blk)
        crop, cbox = self.crop(lb, pad=2)
        veil = Rectangle(width=14.4, height=8.2, stroke_width=0, fill_color=BG, fill_opacity=0.8)
        self.play(FadeIn(veil), FadeIn(crop), run_time=0.5)
        self.w(read_time(r["statement"], base=2.0, per_word=0.12, cap=5.0))
        # -- read: highlight each given at its real box and turn it into a chip (bottom band)
        chips = list(cchips)
        x_cursor = (chips[-1].get_right()[0] + 0.2) if chips else XL
        hls = []
        for g in P.get("given", []):
            chk = next(c for c in r["checks"] if c["kind"] == "data" and c["name"] == g["name"])
            if not g.get("chip"):
                continue
            hl = VGroup(*[self.box_rect(b, pad=1.5, stroke_color=C_VEL, stroke_width=2.5, fill_color=HILITE, fill_opacity=0.45) for b in chk["boxes"]])
            self.play(FadeIn(hl), run_time=0.45)
            ch = self.chip(g["chip"])
            fit(ch, 6.2)
            if x_cursor + ch.width > XR:
                x_cursor = XL  # second row: shift the first row up
                for c in chips:
                    c.shift(UP * 0.62)
            ch.move_to([x_cursor + ch.width / 2, -3.2, 0])
            x_cursor += ch.width + 0.2
            self.play(TransformFromCopy(hl, ch, path_arc=-0.6), hl.animate.set_fill(opacity=0.25), run_time=0.9)
            self.log.append({"problem": P["id"], "kind": "given", "name": g["name"], "chip": g["chip"], "quote": g["quote"], "boxes": chk["boxes"], "score": chk["score"]})
            chips.append(ch)
            hls.append(hl)
            self.w(0.35)
        self.w(P_SHORT)
        # -- thumbnail + chips below it + panel header
        self.play(*[FadeOut(h) for h in hls], FadeOut(self.pg), FadeOut(veil), run_time=0.5)
        tw, th = 6.2, 2.05
        sc = min(tw / crop.width, th / crop.height)
        crop_t = crop.copy().scale(sc)
        crop_t.move_to([XL + crop_t.width / 2, YT - crop_t.height / 2, 0])
        thumb_frame = Rectangle(width=crop_t.width + 0.08, height=crop_t.height + 0.08, stroke_color=RULE, stroke_width=1.2).move_to(crop_t)
        # chips: rows of max width 6.2 under the thumbnail
        rows_, cur, wsum = [], [], 0
        for c in chips:
            if cur and wsum + c.width > 6.3:
                rows_.append(cur); cur, wsum = [], 0
            cur.append(c); wsum += c.width + 0.18
        if cur:
            rows_.append(cur)
        targets = []
        y = crop_t.get_bottom()[1] - 0.2
        for rw in rows_:
            g = VGroup(*[c.copy() for c in rw]).arrange(RIGHT, buff=0.18)
            fit(g, 6.3)
            g.move_to([XL + g.width / 2, y - g.height / 2, 0])
            y -= g.height + 0.14
            targets += list(g)
        self.play(crop.animate.scale(sc).move_to(crop_t), FadeIn(thumb_frame),
                  *[c.animate.become(t) for c, t in zip(chips, targets)], run_time=1.3)
        chips_bottom = min((t.get_bottom()[1] for t in targets), default=crop_t.get_bottom()[1])
        zone = (XL, chips_bottom - 0.3, -0.45, YB)
        header = VGroup(T(f"Problem {P['id']}", 24, C_POS, weight=BOLD), fit(T(P.get("title", ""), 22, INK), 5.0)).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        header.move_to([self.PANEL_X0 + header.width / 2, YT - header.height / 2, 0])
        rule = Line([self.PANEL_X0, header.get_bottom()[1] - 0.12, 0], [XR, header.get_bottom()[1] - 0.12, 0], color=RULE, stroke_width=1.5)
        self.play(FadeIn(header), Create(rule), run_time=0.6)
        self.panel_top = rule.get_center()[1] - 0.18
        self.rows = []
        # -- find / model
        if P.get("find"):
            self.panel_add(self.step_row("Find", "", P["find"], C_ACC, 30), anim="fade")
            self.w(P_SHORT)
        if P.get("model"):
            mt = fit(T(wrap(P["model"], 58), 17, INK), self.PANEL_X1 - self.PANEL_X0)
            head = T("MODEL", 15, MUTED)
            self.panel_add(VGroup(head, mt).arrange(DOWN, aligned_edge=LEFT, buff=0.08), anim="fade")
            self.w(read_time(P["model"]))
        # -- steps (+ visual at the requested point)
        V = P.get("visual") or {"type": "none"}
        after = V.get("after", len(P.get("steps", [])))
        env = self._env(P)
        vis = None
        steps = P.get("steps", [])
        for i, s in enumerate(steps):
            row = self.step_row(s.get("stage", ""), s.get("note", ""), s["tex"])
            self.panel_add(row)
            self.w(max(1.4, read_time(s.get("note", ""), base=1.4, per_word=0.25, cap=3.2)))
            if i + 1 == after and vis is None:
                vis = visuals.build(self, V, env, zone)
        if vis is None:
            vis = visuals.build(self, V, env, zone)
        # -- answers (boxed) and verification
        for a in P.get("answers", []):
            row = self.step_row("Answer", a.get("label", ""), a["tex"], C_POS, 34)
            row[1].shift(DOWN * 0.12)  # room for the box frame under the header
            self.panel_add(row, anim="fade")
            box = SurroundingRectangle(row[1], color=C_POS, buff=0.1, stroke_width=2.5)
            self.play(Create(box), run_time=0.5)
            self.remove(box)
            row.add(box)
            shown = fmt_value(a["value"], a.get("decimals"))
            self.log.append({"problem": P["id"], "kind": "answer", "name": a["name"], "tex": a["tex"], "value": a["value"], "shown": shown,
                             "in_tex": shown.replace(" ", "") in a["tex"].replace(" ", "").replace("{,}", "")})
            self.w(P_BEAT)
        for v in P.get("verify", []):
            self.panel_add(self.step_row("Verify", v.get("note", ""), v["tex"], C_GAL, 30))
            self.w(max(1.4, read_time(v.get("note", ""), base=1.4, per_word=0.25, cap=3.0)))
        badge = VGroup(M(r"\checkmark", 30, BG), T("CHECKED", 20, BG, weight=BOLD)).arrange(RIGHT, buff=0.12)
        bb = RoundedRectangle(corner_radius=0.1, width=badge.width + 0.4, height=badge.height + 0.22, fill_color=C_GAL, fill_opacity=1, stroke_width=0)
        badge.move_to(bb); badge = VGroup(bb, badge)
        last = self.rows[-1] if self.rows else None
        if last is not None and last[1].get_right()[0] + badge.width + 0.25 < XR:
            badge.move_to([XR - badge.width / 2, last[1].get_center()[1], 0])
        else:
            self.panel_add(VGroup(badge.copy().set_opacity(0)), anim="fade", run_time=0.05)
            badge.move_to([XR - badge.width / 2, self.rows[-1].get_center()[1], 0])
        self.play(FadeIn(badge, scale=1.2), run_time=0.6)
        if P.get("interpretation"):
            it = fit(T(wrap(P["interpretation"], 60), 16, INK), self.PANEL_X1 - self.PANEL_X0 - 0.3)
            ib = RoundedRectangle(corner_radius=0.08, width=it.width + 0.3, height=it.height + 0.24, stroke_color=C_POS, stroke_width=1.5, fill_color=FILL, fill_opacity=1)
            it.move_to(ib)
            self.panel_add(VGroup(ib, it), anim="fade")
            self.w(read_time(P["interpretation"]))
        self.w(P_MED)
        # -- return to the page: the statement goes back, the page zooms to the work area, answers are written there
        self.play(*[FadeOut(m) for m in (*self.rows, header, rule, badge, thumb_frame, *chips)], FadeOut(vis), run_time=0.7)
        self.rows = []
        self.play(crop.animate.scale(1 / sc).move_to(self.to_xy((cbox[0] + cbox[2]) / 2, (cbox[1] + cbox[3]) / 2)), FadeIn(self.pg), run_time=1.2)
        s2, ul2 = self.fit_target(n, r["region"], maxh=7.2, center=(0, 0))
        self.move_page(s2, ul2, extra=[crop], run_time=1.4)
        full, _ = self.crop(r["region"], pad=2)
        self.play(FadeIn(full), run_time=0.3)
        self.remove(crop)
        band = (r["work"][0] if r["work"] else [r["region"][0] + 20, self._statement_box(r)[3] + 6, r["region"][2] - 20, r["region"][3]])
        x, y = band[0] + 12, band[1] + 16
        new_anns = []
        for a in P.get("answers", []):
            if not a.get("annotation"):
                continue
            ann = self.annotation(a["annotation"], x, y)
            self.play(Write(ann["mob"]), run_time=1.0)
            self.remove(ann["mob"])
            self.pg.add(ann["mob"])
            self.ann.setdefault(n, []).append(ann)
            new_anns.append(ann)
            self.log.append({"problem": P["id"], "kind": "annotation", "name": a["name"], "text": a["annotation"], "at_pt": [round(x, 1), round(y, 1)],
                             "in_work_area": bool(band[0] <= x <= band[2] and band[1] <= y <= band[3])})
            y += 19
            self.w(0.4)
        self.w(P_SHORT)
        self.play(FadeOut(full), run_time=0.3)
        s0, ul0 = self.full_target(n)
        self.move_page(s0, ul0, run_time=1.6)
        self.w(P_SHORT if k < n_total - 1 else P_BEAT)

    def _env(self, P):
        import sympy as sp
        from pdf2video.validate import safe_eval
        env = {c["name"]: sp.nsimplify(c["value"]) for c in self.S.get("constants", [])}
        for s in P.get("symbols", []):
            env[s] = sp.Symbol(s)
        for g in P.get("given", []):
            if g.get("equation") is not None:
                env[g["name"]] = safe_eval(g["equation"], env)
            else:
                env[g["name"]] = [sp.nsimplify(v) for v in g["list"]] if g.get("list") is not None else sp.nsimplify(g["value"])
        for a in P.get("answers", []):
            env[a["name"]] = safe_eval(a["expr"], env)
        return env

    # ------------------------------------------------------------------ closing
    def closing(self, probs):
        n = self.cur_page
        P = self.P(n)
        h = 7.2
        s = h / P.height
        ul = np.array([XL, h / 2, 0])
        self.move_page(s, ul, run_time=1.2)
        col = VGroup(T("Answers", 36, INK, weight=BOLD))
        for p in probs:
            items = VGroup(T(f"Problem {p['id']}  ·  {p.get('title', '')}", 21, C_POS, weight=BOLD))
            for a in p.get("answers", []):
                items.add(fit(M(a["tex"], 36, INK), 6.6))
            items.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            col.add(items)
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        fit(col, 7.6, 6.3)
        x0 = XL + P.width * s + 0.6
        col.move_to([x0 + col.width / 2, 0.45, 0])
        badge = VGroup(M(r"\checkmark", 28, BG), T("EVERY VALUE QUOTED FROM THE PAGE · EVERY ANSWER RECOMPUTED (SymPy)", 15, BG, weight=BOLD)).arrange(RIGHT, buff=0.12)
        fit(badge, XR - x0 - 0.4)
        bb = RoundedRectangle(corner_radius=0.1, width=badge.width + 0.36, height=badge.height + 0.22, fill_color=C_GAL, fill_opacity=1, stroke_width=0)
        badge.move_to(bb)
        badge = VGroup(bb, badge)
        badge.move_to([x0 + badge.width / 2, YB + badge.height / 2 + 0.05, 0])
        self.play(FadeIn(col, lag_ratio=0.15), run_time=1.6)
        self.play(FadeIn(badge, scale=1.1), run_time=0.6)
        self.w(P_LONG + 1.5)
        self.play(FadeOut(col), FadeOut(badge), FadeOut(self.pg), run_time=0.8)
        self.w(0.5)
