"""Every number shown in the hybrid video, computed once with asserts.
Writes shared/derived.json, which the ManimCE lesson imports (the cartoon engine computes the
same closed forms in JS and tools/cross_check.mjs compares both against this file).

usage: .venv/bin/python productions/caida-libre-hibrido/verify_caida_libre.py
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
C = json.loads((HERE / "shared" / "constants.json").read_text())
H, G = C["H"], C["g"]


def close(a, b, tol=1e-9, label=""):
    assert abs(a - b) <= tol, f"{label}: {a} != {b}"


def case(v0, g=G, h=H):
    disc = v0 * v0 + 2 * g * h
    T = (v0 + math.sqrt(disc)) / g          # positive root of 0 = h + v0 T - g T^2 / 2
    v = v0 - g * T
    out = {"v0": v0, "T": T, "v_impact": v, "speed_impact": math.sqrt(disc), "disc": disc}
    close(h + v0 * T - 0.5 * g * T * T, 0.0, 1e-9, "y(T)=0")
    close(v * v, v0 * v0 + 2 * g * h, 1e-9, "v^2 = v0^2 + 2gh")
    if v0 > 0:
        out.update(t_apex=v0 / g, y_apex=h + v0 * v0 / (2 * g), t_back=2 * v0 / g, v_back=-v0)
        close(v0 - g * out["t_apex"], 0, 1e-12, "v(apex)=0")
    return out


cases = {k: case(v0) for k, v0 in C["v0"].items()}
# exact forms quoted on screen (g = 9.81): t = (v0 + sqrt(v0^2 + 2 g h)) / g
for k, v0 in C["v0"].items():
    close(cases[k]["T"], (v0 + math.sqrt(v0 * v0 + 2 * G * H)) / G, 1e-12, f"case {k} T")
close(cases["2"]["speed_impact"], cases["3"]["speed_impact"], 1e-12, "equal speeds +-v0")
close(cases["3"]["y_apex"], H + 100 / (2 * G), 1e-12, "apex")
# numbers-first table for case 1: drop each second and its increments (1 : 3 : 5)
drop = [0.5 * G * t * t for t in range(4)]
incr = [drop[i + 1] - drop[i] for i in range(3)]
for i, r in enumerate((1, 3, 5)):
    close(incr[i] / incr[0], r, 1e-12, "1:3:5")
vel = [G * t for t in range(4)]
avg_speed = [incr[i] / 1.0 for i in range(3)]          # average speed in each 1-s interval
mid_speed = [G * (i + 0.5) for i in range(3)]          # = speed at the middle of the interval
for a, b in zip(avg_speed, mid_speed):
    close(a, b, 1e-12, "avg speed = mid-interval speed")
# the sling: v0 = omega R; release where the radius is horizontal (velocity vertical)
R = C["sling"]["R_u"] / C["rig_u_per_m"]
omega = 10.0 / R
sling = {"R": R, "omega": omega, "rev_per_s": omega / (2 * math.pi), "centripetal_acc": omega * omega * R, "centripetal_in_g": omega * omega * R / G}
# real-world: g = 9.81
real = {k: case(v0, g=C["g_rounded"]) for k, v0 in C["v0"].items()}  # comparison: g rounded to 10
# air drag (quadratic) for a real skull: v_t = sqrt(2 m g / (rho Cd A)); RK4 integration
a = C["air"]
A = math.pi * (a["diameter_m"] / 2) ** 2
vt = math.sqrt(2 * a["mass_kg"] * C["g_real"] / (a["rho"] * a["Cd"] * A))
k = a["rho"] * a["Cd"] * A / (2 * a["mass_kg"])


def drag_fall(v0, g=C["g_real"], dt=1e-5):
    y, v, t = H, v0, 0.0
    f = lambda vv: -g - k * vv * abs(vv)
    while True:
        k1 = f(v); k2 = f(v + 0.5 * dt * k1); k3 = f(v + 0.5 * dt * k2); k4 = f(v + dt * k3)
        dv = dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        yn = y + dt * (v + 0.5 * dv)  # trapezoid-consistent position step
        if yn <= 0:
            frac = y / (y - yn)
            return t + frac * dt, v + frac * dv
        y, v, t = yn, v + dv, t + dt


drag = {kk: dict(zip(("T", "v_impact"), drag_fall(v0))) for kk, v0 in C["v0"].items()}
# closed form check for the drop: T = (vt/g) arccosh(exp(g H / vt^2))
T1 = vt / C["g_real"] * math.acosh(math.exp(C["g_real"] * H / vt ** 2))
close(drag["1"]["T"], T1, 2e-4, "drag closed form")
out = {"constants": C, "cases": cases, "numbers_first": {"t": [0, 1, 2, 3], "drop": drop, "increments": incr, "v": vel, "avg_speed": avg_speed},
       "sling": sling, "rounded_g": real, "drag": {"v_terminal": vt, "A": A, "k": k, "cases": drag}}
(HERE / "shared" / "derived.json").write_text(json.dumps(out, indent=1))
print(json.dumps({"T": {k: round(v["T"], 4) for k, v in cases.items()}, "sling": sling, "rounded_T": {k: round(v["T"], 3) for k, v in real.items()},
                  "drag": {"vt": round(vt, 2), **{k: (round(v["T"], 3), round(v["v_impact"], 2)) for k, v in drag.items()}}}, indent=1))
