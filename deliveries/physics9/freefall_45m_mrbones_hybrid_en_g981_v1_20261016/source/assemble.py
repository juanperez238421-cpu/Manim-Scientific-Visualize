"""Assemble the hybrid video: cartoon clips (engine B) + ManimCE sections (engine A).

1. cut the cartoon master into its five clips at their exact frame boundaries (white frames)
2. check every clip starts and ends on a #FFFFFF frame; normalise all clips (1920x1080, 30 fps,
   H.264 yuv420p) and concatenate in the narrative order
3. synthesise the soundtrack on the final timeline: the band under the cartoon (stops for each fall),
   sound effects at the exact physical instants (sling whoosh at every turn, release click, a whistle
   whose pitch follows |v|, thud at impact), a quiet bed under the lesson; master to -16 LUFS
4. mux, write the edit decision list (EDL) with every clip's offset in the final video

usage: .venv/bin/python productions/caida-libre-hibrido/tools/assemble.py
"""
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
BUILD = ROOT / "build" / "caida-libre-hibrido-en"
OUT = ROOT / "output" / "final"
TL = json.loads((HERE / "cartoon" / "timeline.json").read_text())
D = json.loads((HERE / "shared" / "derived.json").read_text())
FPS = 30
SR = 48000
MANIM = BUILD / "manim" / "videos" / "freefall_lesson_en" / "1080p30"
ORDER = ["B1_prologo", "A1Pregunta", "B2_caso1", "A2NumerosPrimero", "A3Ecuacion", "B3_caso2", "A4Honda", "B4_caso3",
         "A5TresCasos", "A6PuntoAlto", "A7Excepciones", "B5_final", "A8Sintesis"]
NAME = "Physics9_FreeFall45m_MrBones_HYBRID_EN_g981_V1_SENIOR_FINAL_pqh"


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        raise SystemExit(f"command failed: {' '.join(map(str, cmd))}\n{r.stderr[-2000:]}")
    return r


def probe(f):
    r = run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames,width,height,r_frame_rate,pix_fmt", "-of", "json", str(f)])
    return json.loads(r.stdout)["streams"][0]


def frame_rgb(f, idx):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-vf", f"select=eq(n\\,{idx})", "-vframes", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "192x108", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.uint8)


def main():
    clipdir = BUILD / "clips"
    clipdir.mkdir(parents=True, exist_ok=True)
    master = BUILD / "cartoon_master.mp4"
    clips = {}
    # 1. cartoon clips at exact frames
    for c in TL["clips"]:
        f0, f1 = round(c["start"] * FPS), round(c["end"] * FPS)
        out = clipdir / f"{c['name']}.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(master), "-vf", f"select=between(n\\,{f0}\\,{f1 - 1}),setpts=N/{FPS}/TB", "-r", str(FPS), "-an",
             "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)])
        clips[c["name"]] = {"file": out, "engine": "B (cartoon)", "cartoon_start": c["start"], "frames": f1 - f0}
    # 2. manim clips, normalised
    for n in ORDER:
        if n.startswith("A"):
            src = MANIM / f"{n}.mp4"
            out = clipdir / f"{n}.mp4"
            run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-an", "-r", str(FPS), "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)])
            clips[n] = {"file": out, "engine": "A (ManimCE)"}
    edl, t = [], 0.0
    for n in ORDER:
        p = probe(clips[n]["file"])
        nf = int(p["nb_read_frames"])
        first, last = frame_rgb(clips[n]["file"], 0), frame_rgb(clips[n]["file"], nf - 1)
        white = lambda a: bool(a.size and a.min() >= 250)
        edl.append({"clip": n, "engine": clips[n]["engine"], "offset_s": round(t, 6), "frames": nf, "duration_s": nf / FPS, "first_white": white(first), "last_white": white(last),
                    "size": [p["width"], p["height"]], "fps": p["r_frame_rate"], "pix_fmt": p["pix_fmt"], **({"cartoon_start": clips[n]["cartoon_start"]} if "cartoon_start" in clips[n] else {})})
        t += nf / FPS
    total = t
    lst = clipdir / "concat.txt"
    lst.write_text("".join(f"file '{clips[n]['file'].name}'\n" for n in ORDER))
    silent = BUILD / "hybrid_silent.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(silent)], cwd=clipdir)
    # 3. soundtrack
    audio = soundtrack(edl, total)
    # 4. mux
    OUT.mkdir(parents=True, exist_ok=True)
    final = OUT / f"{NAME}.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(audio), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(final)])
    (HERE / "qa").mkdir(exist_ok=True)
    (HERE / "qa" / "EDL.json").write_text(json.dumps({"order": ORDER, "clips": edl, "total_s": total, "final": str(final.relative_to(ROOT))}, indent=1))
    print(json.dumps({"total_s": round(total, 3), "clips": [(e["clip"], round(e["duration_s"], 2), e["first_white"], e["last_white"]) for e in edl]}, indent=1))


# ------------------------------------------------------------------ soundtrack
def soundtrack(edl, total):
    spec = importlib.util.spec_from_file_location("hh", ROOT / "productions" / "halloween-hop" / "audio" / "score.py")
    hh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hh)
    N = int(math.ceil(total * SR)) + SR
    x = np.zeros(N)
    cues = []

    def add(t, sig, gain=1.0, cue=None):
        i = int(round(t * SR))
        if i < 0 or i >= N:
            return
        seg = sig[: N - i]
        x[i:i + len(seg)] += gain * seg
        if cue:
            cues.append({"id": cue, "t": round(t, 6), "frame": round(t * FPS, 3)})
            stems[cue] = gain * sig[: int(0.25 * SR)]

    stems = {}
    m, hz = hh.m, hh.hz
    spb = 60 / 180
    S = TL["scenes"]
    G = D["constants"]["g"]
    omega = D["sling"]["omega"]
    for e in edl:
        off, dur = e["offset_s"], e["duration_s"]
        if e["engine"].startswith("A"):
            # quiet bed: sustained organ chord + a celesta figure every 4 bars
            chords = [[m("D3"), m("A3"), m("F4")], [m("G2"), m("D3"), m("Bb3")], [m("A2"), m("E3"), m("C#4")], [m("D3"), m("A3"), m("F4")]]
            k = 0
            tt = off + 0.4
            while tt < off + dur - 1.5:
                ln = min(8 * 4 * spb, off + dur - 0.6 - tt)
                add(tt, hh.organ(chords[k % 4], ln, 0.35), 0.5)
                for j, nt in enumerate(["D5", "F5", "A5", "D6"]):
                    add(tt + 2 * spb * j, hh.celesta(hz(m(nt))), 0.18)
                tt += 8 * 4 * spb
                k += 1
            continue
        c0 = e["cartoon_start"]
        to_final = lambda tc: off + (tc - c0)
        name = e["clip"]
        if name == "B1_prologo":
            hh.rhythm_t = None
            for b in range(0, int(dur / spb) - 4, 4):
                for j, (bb, ch) in enumerate([(0, "Dm"), (2, "A7")]):
                    pass
            # theme on the band through the prologue
            for k, (b, d, nt) in enumerate(hh.THEME):
                if b * spb < dur - 1.5:
                    add(off + 0.5 + b * spb, hh.trumpet(hz(m(nt)), d * spb * 0.95), 0.8)
            for b in range(0, int((dur - 1.0) / spb), 2):
                root = [m("D2"), m("A1")][(b // 2) % 2]
                add(off + 0.5 + b * spb, hh.tuba(hz(root), 0.9 * spb, 0.7))
                add(off + 0.5 + (b + 1) * spb, hh.banjo_strum([m("D4"), m("F4"), m("A4")], 0.8 * spb, 0.8))
            add(to_final(S["popHead"]), hh.boing(200, 0.5), 1.0, cue="pop-cabeza")
            add(to_final(S["popHead"]), hh.woodblock(1500, 1.0), 0.8)
            continue
        if name == "B5_final":
            F = S["finale"]
            add(to_final(F["headBack"][1]), hh.woodblock(1300, 1.0), 0.8, cue="cabeza-en-su-sitio")
            add(to_final(F["burst"][0]), hh.cymbal(0.7, 1.0), 1.0)
            for j, nt in enumerate(["D5", "A4", "A4", "B4", "A4", "C#5", "D5"]):
                tb = to_final(F["bow"][0]) - 1.6 + [0, 1, 1.5, 2, 3, 5, 6][j] * spb * 0.9
                add(tb, hh.trumpet(hz(m(nt)), 0.5 * spb, 1.1, wah=False), 0.9)
                add(tb, hh.xylophone(hz(m(nt))), 0.4)
            continue
        # a case clip
        cs = next(c for c in S["cases"] if f"B{1 + c['id']}_caso{c['id']}" == name)
        rel, imp, v0 = cs["release"], cs["impact"], cs["v0"]
        Tf = imp - rel
        # light vamp until the release, then the band stops
        tt = cs["start"] + 0.6
        while tt < rel - 0.4:
            add(to_final(tt), hh.tuba(hz(m("D2") if int((tt - cs['start']) / (2 * spb)) % 2 == 0 else m("A1")), 0.9 * spb, 0.55))
            add(to_final(tt + spb), hh.banjo_strum([m("D4"), m("F4"), m("A4")], 0.8 * spb, 0.5))
            tt += 2 * spb
        if cs["sling"]:
            add(to_final(cs["pull"][1]), hh.woodblock(600, 1.2), 1.0, cue=f"caso{cs['id']}-clac")
            # whoosh every time the skull passes the bottom of the circle (θ ≡ −π/2), from the JS schedule
            dirn = 1 if v0 > 0 else -1
            T_UP = 0.8
            sweep = 0.5 * omega * T_UP
            tot = math.pi / 2 if dirn > 0 else 1.5 * math.pi
            while tot < sweep + 2 * math.pi:
                tot += 2 * math.pi
            T2 = (tot - sweep) / omega
            tS = rel - T_UP - T2
            alpha = omega / T_UP
            nturn = 1
            while True:
                ang = 2 * math.pi * nturn  # angle swept to pass the bottom again
                if ang <= sweep:
                    tb = tS + math.sqrt(2 * ang / alpha)
                elif ang <= tot:
                    tb = tS + T_UP + (ang - sweep) / omega
                else:
                    break
                add(to_final(tb), hh.whoosh(0.18, up=True, vel=0.6), 0.9)
                nturn += 1
        add(to_final(rel), hh.woodblock(1800, 0.9), 0.7, cue=f"caso{cs['id']}-suelta")
        n = int(Tf * SR)
        tv = np.arange(n) / SR
        f = 380 + 26 * np.abs(v0 - G * tv)
        env = np.minimum(1, tv / 0.03) * np.minimum(1, (Tf - tv) / 0.01)
        add(to_final(rel), 0.24 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env, 1.0)
        add(to_final(rel), hh.roll(Tf, 0.7), 1.0)
        add(to_final(imp), hh.thud(1.2), 1.0, cue=f"caso{cs['id']}-impacto")
        add(to_final(imp), hh.cymbal(1.0, 1.6), 0.9)
        add(to_final(imp), hh.woodblock(700, 1.0), 0.8)
        k0 = cs["react"][0]
        rng = np.random.default_rng(4510 + cs["id"])
        for j in range(16):
            add(to_final(k0 + 0.04 * j + 0.01 * rng.uniform()), hh.woodblock(float(rng.uniform(900, 2600)), 0.5), 0.4)
        rw0 = k0 + 1.0
        add(to_final(rw0), hh.slide_whistle(1400, 420, Tf / 5), 0.6)
        if cs["sling"]:
            add(to_final(cs["reattach"][1]), hh.woodblock(2200, 1.0), 0.7, cue=f"caso{cs['id']}-clic")
    y = hh.period_chain(x[: int(total * SR)], crackle=False)
    y = y / max(1e-9, np.abs(y).max()) * 0.5
    out = BUILD / "audio"
    out.mkdir(exist_ok=True)
    g = 1.0
    hist = []
    for it in range(6):
        z, gr = hh.limiter(np.stack([y * g, y * g], axis=1), -2.0)
        hh.write_wav(out / "mix.wav", z)
        mm = hh.measure(out / "mix.wav")
        hist.append({"gain": g, **mm})
        err = -16.0 - mm["integrated_lufs"]
        if abs(err) <= 0.2:
            break
        g *= 10 ** (err / 20)
    (out / "stems").mkdir(exist_ok=True)
    for cid, sig in stems.items():
        s = np.zeros(int(0.25 * SR)); s[: len(sig)] = sig
        np.save(out / "stems" / f"{cid.replace('@', '_')}.npy", hh.period_chain(s, crackle=False))
    (out / "cue_sheet.json").write_text(json.dumps({"cues": cues, "loudness": hist[-1]}, indent=1))
    return out / "mix.wav"


if __name__ == "__main__":
    main()
