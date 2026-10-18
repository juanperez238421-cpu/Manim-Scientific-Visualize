"""Validate a solution spec against its PDF before anything is rendered.

Gates (all must pass):
  data      every given value and constant is quoted from the document, found on the page (exact on
            text pages, fuzzy on OCR pages), inside its problem block (constants: anywhere on the page),
            and the number in the quote equals the value (or the item is marked implied, e.g. "from rest")
  answers   every answer's expression, evaluated with exact arithmetic, equals the stated value at the
            stated rounding
  steps     every step that carries a `check` holds (numerically, or symbolically when unknowns remain)
  verify    every verification check holds
  visual    the visual module accepts its parameters
Expressions are parsed through an AST whitelist (numbers, names, + - * / **, comparisons, a fixed set
of math/statistics functions): spec text can never execute code.
"""
from __future__ import annotations

import ast
import json
import math
import re
import statistics as st
from pathlib import Path

import sympy as sp

from .ir import Document, norm
from .segment import detect

# ------------------------------------------------------------------ safe expressions
def _q_halves(xs, which):
    xs = sorted(xs); n = len(xs); h = n // 2
    lo, hi = xs[:h], xs[h + (n % 2):]
    return sp.nsimplify(st.median(lo if which == 1 else hi))


def _approx(a, b, tol):
    return sp.Abs(sp.N(a) - sp.N(b)) <= tol


def _flat(a):
    return list(a[0]) if len(a) == 1 and isinstance(a[0], (list, tuple)) else list(a)


def _mean(xs):
    return sp.Add(*xs) / len(xs)


def _pvar(xs):
    m = _mean(xs)
    return sp.Add(*[(x - m) ** 2 for x in xs]) / len(xs)


def _var(xs):
    m = _mean(xs)
    return sp.Add(*[(x - m) ** 2 for x in xs]) / (len(xs) - 1)


def _median(xs):
    xs = sorted(xs, key=lambda v: float(v)); n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def _mode(xs):
    best = max(xs, key=lambda v: (sum(1 for y in xs if y == v), -float(v)))
    return best


def _q_halves(xs, which):
    xs = sorted(xs, key=lambda v: float(v)); n = len(xs); h = n // 2
    lo, hi = xs[:h], xs[h + (n % 2):]
    return _median(lo if which == 1 else hi)


def _approx(a, b, tol):
    return sp.Abs(sp.N(a) - sp.N(b)) <= tol


def _solve(eqs, var, k=0):
    """k-th solution (ascending) of an equation / list of equations (expressions = 0) for var"""
    eqs = list(eqs) if isinstance(eqs, (list, tuple)) else [eqs]
    sol = sp.solve(eqs, dict=True)
    vals = sorted({d[var] for d in sol if var in d}, key=lambda v: float(sp.N(sp.re(v))))
    return vals[int(k)]


def _at(e, *pairs):
    return sp.sympify(e).subs({pairs[i]: pairs[i + 1] for i in range(0, len(pairs), 2)})


FUNCS = {
    "sqrt": sp.sqrt, "Abs": sp.Abs, "abs": sp.Abs, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
    "log": sp.log, "ln": sp.log, "exp": sp.exp, "Rational": sp.Rational, "expand": sp.expand, "factor": sp.factor, "simplify": sp.simplify,
    "deg": lambda x: x * sp.pi / 180, "pi": sp.pi, "E": sp.E,
    "mean": _mean, "median": _median, "mode": _mode, "pvariance": _pvar, "pstdev": lambda xs: sp.sqrt(_pvar(xs)),
    "variance": _var, "stdev": lambda xs: sp.sqrt(_var(xs)), "q1": lambda xs: _q_halves(xs, 1), "q3": lambda xs: _q_halves(xs, 3),
    "max": lambda *a: sp.Max(*_flat(a)), "min": lambda *a: sp.Min(*_flat(a)), "Max": lambda *a: sp.Max(*_flat(a)), "Min": lambda *a: sp.Min(*_flat(a)),
    "sum": lambda xs: sp.Add(*xs), "len": lambda xs: sp.Integer(len(xs)), "approx": _approx, "round": lambda x, d=0: sp.Float(round(float(x), int(d))),
    "solve": _solve, "at": _at,
}
_ALLOWED = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Call, ast.Name, ast.Load, ast.Constant, ast.List, ast.Tuple, ast.Compare,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd, ast.Eq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Mod, ast.FloorDiv)


class UnsafeExpression(ValueError):
    pass


def safe_eval(expr: str, env: dict):
    """evaluate a whitelisted arithmetic expression with sympy semantics"""
    tree = ast.parse(expr.replace("^", "**"), mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED):
            raise UnsafeExpression(f"not allowed: {type(node).__name__} in {expr!r}")
        if isinstance(node, ast.Call) and not (isinstance(node.func, ast.Name) and node.func.id in FUNCS):
            raise UnsafeExpression(f"function not allowed in {expr!r}")
        if isinstance(node, ast.Name) and node.id not in env and node.id not in FUNCS:
            raise UnsafeExpression(f"unknown name {node.id!r} in {expr!r}")
        if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)):
            raise UnsafeExpression(f"constant not allowed in {expr!r}")

    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.Constant): return sp.nsimplify(n.value) if isinstance(n.value, float) else sp.Integer(n.value)
        if isinstance(n, ast.Name): return env[n.id] if n.id in env else FUNCS[n.id]
        if isinstance(n, (ast.List, ast.Tuple)): return [ev(e) for e in n.elts]
        if isinstance(n, ast.UnaryOp): v = ev(n.operand); return -v if isinstance(n.op, ast.USub) else v
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            return {ast.Add: lambda: a + b, ast.Sub: lambda: a - b, ast.Mult: lambda: a * b, ast.Div: lambda: a / b, ast.Pow: lambda: a ** b,
                    ast.Mod: lambda: a % b, ast.FloorDiv: lambda: a // b}[type(n.op)]()
        if isinstance(n, ast.Call):
            f = FUNCS[n.func.id]
            return f(*[ev(a) for a in n.args])
        if isinstance(n, ast.Compare):
            a = ev(n.left)
            res = True
            for op, c in zip(n.ops, n.comparators):
                b = ev(c)
                if isinstance(op, ast.Eq): res = res and _equal(a, b)
                elif isinstance(op, ast.Lt): res = res and bool(sp.N(a) < sp.N(b))
                elif isinstance(op, ast.LtE): res = res and bool(sp.N(a) <= sp.N(b))
                elif isinstance(op, ast.Gt): res = res and bool(sp.N(a) > sp.N(b))
                elif isinstance(op, ast.GtE): res = res and bool(sp.N(a) >= sp.N(b))
                a = b
            return res
        raise UnsafeExpression(type(n).__name__)
    return ev(tree)


def _equal(a, b, tol=1e-9):
    if isinstance(a, list) or isinstance(b, list):
        return isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and all(_equal(x, y) for x, y in zip(a, b))
    d = sp.simplify(sp.sympify(a) - sp.sympify(b))
    if d == 0:
        return True
    if d.free_symbols:
        return False
    return abs(float(sp.N(d))) <= tol * max(1.0, abs(float(sp.N(a))))


def numbers_in(s: str):
    return [float(x.replace(",", "")) for x in re.findall(r"(?<![\w.])-?\d+(?:,\d{3})*(?:\.\d+)?", norm(s))]


def fmt_value(v, decimals):
    if decimals is None:
        f = float(v)
        return str(int(f)) if abs(f - round(f)) < 1e-12 else f"{f:g}"
    return f"{float(v):.{decimals}f}"


# ------------------------------------------------------------------ the validator
def validate(spec_path, workdir=None, verbose=True):
    spec_path = Path(spec_path)
    S = json.loads(spec_path.read_text())
    pdf = (spec_path.parent / S["document"]).resolve()
    doc = Document(pdf, workdir or spec_path.parent / ".p2v_work")
    probs = {p.id: p for p in detect(doc)}
    rep = {"spec": spec_path.name, "document": pdf.name, "sha256": doc.sha256, "pages": len(doc.pages), "source": [P.source for P in doc.pages],
           "problems": [], "pass": True}
    if S.get("sha256") and S["sha256"] != doc.sha256:
        rep["pass"] = False; rep["error"] = "document sha256 differs from the spec"
    env_c, located_c = {}, []
    for c in S.get("constants", []):
        page = c.get("page", 1)
        m = doc.find(page, c["quote"])
        ok_num = c.get("implied") or any(abs(x - c["value"]) < 1e-9 for x in numbers_in(c["quote"]))
        located_c.append({"name": c["name"], "quote": c["quote"], "found": bool(m), "box": m.box if m else None, "score": m.score if m else 0, "number_in_quote": bool(ok_num)})
        env_c[c["name"]] = sp.nsimplify(c["value"])
        if not (m and ok_num):
            rep["pass"] = False
    rep["constants"] = located_c
    for P in S["problems"]:
        r = {"id": P["id"], "checks": [], "pass": True}
        det = probs.get(P["id"])
        if det is None:
            r["pass"] = False; r["error"] = f"problem {P['id']} not found on the page"; rep["problems"].append(r); rep["pass"] = False; continue
        region = det.box
        env = dict(env_c)
        for s in P.get("symbols", []):
            env[s] = sp.Symbol(s)
        # data
        for g in P.get("given", []):
            quotes = g["quote"] if isinstance(g["quote"], list) else [g["quote"]]
            ms = [doc.find(det.page, q, region, nth=g.get("nth", 0)) for q in quotes]
            found = all(ms)
            qnums = [x for q in quotes for x in numbers_in(q)]
            if g.get("equation") is not None:
                env[g["name"]] = safe_eval(g["equation"], env)
                eq_nums = [abs(x) for x in numbers_in(g["equation"].replace("**", "^").replace("*", " "))]
                ok_num = all(abs(x) in eq_nums for x in qnums if x != 0)
            elif g.get("list") is not None:
                vals = g["list"]
                ok_num = all(any(abs(x - v) < 1e-9 for x in qnums) for v in vals)
                env[g["name"]] = [sp.nsimplify(v) for v in vals]
            else:
                ok_num = g.get("implied") or any(abs(x - g["value"]) < 1e-9 for x in qnums)
                env[g["name"]] = sp.nsimplify(g["value"])
            ok = bool(found) and bool(ok_num)
            boxes = [m.box for m in ms if m]
            r["checks"].append({"kind": "data", "name": g["name"], "quote": g["quote"], "found": bool(found), "score": min((m.score for m in ms if m), default=0),
                                "box": boxes[0] if boxes else None, "boxes": boxes, "number_in_quote": bool(ok_num), "pass": ok})
            r["pass"] &= ok
        # table data (cells read from the PDF table)
        for tq in P.get("table", []):
            pg = doc.page(det.page)
            cells = [c["text"] for t in pg.tables for row in t["rows"] for c in row if c]
            ok = all(str(v) in cells for v in tq["values"])
            r["checks"].append({"kind": "table", "name": tq["name"], "pass": ok})
            r["pass"] &= ok
        # answers (in order; later ones may use earlier ones)
        for a in P.get("answers", []):
            try:
                val = safe_eval(a["expr"], env)
                d = a.get("decimals")
                shown = fmt_value(val, d)
                ok = abs(float(sp.N(val)) - float(a["value"])) <= (0.5 * 10 ** -d + 1e-12 if d is not None else 1e-9 * max(1, abs(float(a["value"]))))
                env[a["name"]] = val
                r["checks"].append({"kind": "answer", "name": a["name"], "expr": a["expr"], "computed": float(sp.N(val)), "stated": a["value"], "shown": shown, "pass": bool(ok)})
                r["pass"] &= bool(ok)
            except Exception as e:  # noqa: BLE001
                r["checks"].append({"kind": "answer", "name": a.get("name"), "error": str(e), "pass": False}); r["pass"] = False
        # steps and verification
        for kind, items in (("step", P.get("steps", [])), ("verify", P.get("verify", []))):
            for k, s in enumerate(items):
                if not s.get("check"):
                    continue
                try:
                    ok = bool(safe_eval(s["check"], env))
                except Exception as e:  # noqa: BLE001
                    ok = False; s = {**s, "error": str(e)}
                r["checks"].append({"kind": kind, "index": k, "check": s["check"], "pass": ok, **({"error": s["error"]} if "error" in s else {})})
                r["pass"] &= ok
        if not P.get("verify"):
            r["checks"].append({"kind": "verify", "note": "no independent verification given", "pass": False}); r["pass"] = False
        # visual
        if P.get("visual"):
            from .render.visuals import check_params
            try:
                check_params(P["visual"], env)
                r["checks"].append({"kind": "visual", "type": P["visual"]["type"], "pass": True})
            except Exception as e:  # noqa: BLE001
                r["checks"].append({"kind": "visual", "type": P["visual"].get("type"), "error": str(e), "pass": False}); r["pass"] = False
        r["region"] = region; r["statement"] = det.statement; r["work"] = det.work; r["page"] = det.page
        rep["problems"].append(r)
        rep["pass"] &= r["pass"]
    if verbose:
        for r in rep["problems"]:
            bad = [c for c in r["checks"] if not c["pass"]]
            print(f"  problem {r['id']}: {'PASS' if r['pass'] else 'FAIL'}  ({len(r['checks'])} checks)" + ("" if not bad else "  -> " + "; ".join(json.dumps(b)[:160] for b in bad)))
        print(f"VALIDATION {'PASS' if rep['pass'] else 'FAIL'}: {spec_path.name}")
    return rep, doc, S
