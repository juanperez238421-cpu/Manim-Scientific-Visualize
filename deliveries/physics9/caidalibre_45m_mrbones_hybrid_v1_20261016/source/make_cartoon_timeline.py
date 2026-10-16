"""Cartoon-engine timeline for the hybrid video: four clips (prologue, case 1, case 2, case 3,
finale), each opening from and closing to a pure white frame. Release/impact instants come from
shared/derived.json; every impact lands on a drawing (15 drawings/s at 30 fps).
"""
import json, math
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
D = json.loads((HERE / "shared" / "derived.json").read_text())
DPS = 15
ceil_d = lambda t: math.ceil(t * DPS - 1e-9) / DPS
OMEGA = D["sling"]["omega"]; T_UP = 0.8
def sling_T2(dir_):
    sweep = 0.5 * OMEGA * T_UP
    total = math.pi / 2 if dir_ > 0 else 1.5 * math.pi
    while total < sweep + 2 * math.pi: total += 2 * math.pi
    return (total - sweep) / OMEGA
clips, cases = [], []
t = 0.0
# prologue
P = dict(name="B1_prologo", start=0.0, end=16.0)
clips.append(P)
scenes = {"open": [], "close": [], "establish": [1.0, 5.0], "tilt": [1.6, 4.6], "intro": [5.0, 15.0], "hatTip": [5.4, 6.4], "popHead": 6.8, "dataCard": [8.0, 15.0]}
t = 16.0
def add_case(cid, sling):
    global t
    c = D["cases"][str(cid)]
    s = t
    lie = [s + 0.4, s + 1.6]
    if not sling:
        hold = lie[1] + 1.0                       # skull reaches the release point and stays still
        rel_min = hold + 0.6
    else:
        pull = [lie[1] + 0.5, lie[1] + 0.9]
        hang = pull[1] + 0.9
        rel_min = hang + 0.35 + T_UP + sling_T2(1 if c["v0"] > 0 else -1)
    impact = ceil_d(rel_min + c["T"])
    rel = impact - c["T"]
    react0 = impact + 0.8
    rw1 = react0 + 1.0 + c["T"] / 5
    cs = {"id": cid, "v0": c["v0"], "sling": sling, "start": s, "lie": lie, "release": rel, "impact": impact,
          "freeze": [impact, react0], "react": [react0, rw1]}
    if sling:
        cs.update(pull=pull, hang=hang)
        cs["reattach"] = [rw1 + 0.15, rw1 + 0.85]
        gu = [cs["reattach"][1] + 0.15, cs["reattach"][1] + 0.95]
    else:
        cs["holdStill"] = hold
        gu = [rw1 + 0.15, rw1 + 0.95]
    cs["getUp"] = gu
    cs["end"] = ceil_d(gu[1] + 1.2)
    cs["close"] = [cs["end"] - 1.0, cs["end"]]
    cases.append(cs)
    clips.append(dict(name=f"B{1 + cid}_caso{cid}", start=s, end=cs["end"]))
    t = cs["end"]
add_case(1, False)
add_case(2, True)
add_case(3, True)
F = {"start": t, "headBack": [t + 1.0, t + 1.6], "burst": [t + 2.4, t + 3.6], "bow": [t + 4.0, t + 4.8], "close": [t + 5.2, t + 6.2], "end": t + 6.2}
clips.append(dict(name="B5_final", start=t, end=F["end"]))
scenes.update(cases=cases, finale=F)
tl = {"project": {"name": "Mr. Bones · caída libre (híbrido, motor cartoon)", "slug": "caida-libre-hibrido-cartoon", "duration": round(F["end"], 6), "fps": 30,
                  "width": 1920, "height": 1080, "seed": 4510},
      "music": {"bpm": 180, "beatsPerBar": 4, "key": "D minor", "swing": 0.6667, "drawingsPerSecond": DPS},
      "render": {"master": {"crf": 18, "preset": "slow", "tune": "grain"}, "draft": {"scale": 0.5, "fps": 30, "crf": 24, "preset": "veryfast"},
                 "loudness": {"targetLUFS": -16.0, "toleranceLU": 1.0, "maxTruePeakDBTP": -1.5}},
      "clips": clips, "scenes": scenes}
(HERE / "cartoon" / "timeline.json").write_text(json.dumps(tl, indent=1, ensure_ascii=False) + "\n")
for c in clips: print(c)
for c in cases: print(c["id"], "release", round(c["release"], 4), "impact", c["impact"], "frame", c["impact"] * 30)
