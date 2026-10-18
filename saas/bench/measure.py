"""Portable resource meter (Windows/Linux/macOS).

    python measure.py --out run.json [--interval 1.0] -- <command> [args...]

Runs the command, samples every `interval` seconds the CPU%, RSS and thread count of the WHOLE process
tree (manim spawns latex/dvisvgm/ffmpeg children), plus NVIDIA GPU utilisation / VRAM when `nvidia-smi`
is on PATH. Writes a JSON record and prints a one-line summary. Nothing is estimated: fields that could
not be measured are null.
"""
from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
import time

import psutil


def _gpu_sample():
    exe = shutil.which("nvidia-smi")
    if not exe:
        return None
    try:
        out = subprocess.run([exe, "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=5).stdout.strip().splitlines()[0]
        u, m, t = (float(x) for x in out.split(","))
        return u, m, t
    except Exception:  # noqa: BLE001
        return None


def _tree(p: psutil.Process):
    try:
        return [p, *p.children(recursive=True)]
    except psutil.Error:
        return []


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--interval", type=float, default=1.0)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args(argv)
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    if not cmd:
        ap.error("command required after --")

    ncpu = psutil.cpu_count(logical=True)
    t0 = time.time()
    proc = subprocess.Popen(cmd)
    root = psutil.Process(proc.pid)
    cpu_samples, rss_samples, thr, gpu_u, gpu_m, seen = [], [], [], [], [], {}
    gpu_total = None
    while proc.poll() is None:
        procs = _tree(root)
        cpu = rss = th = 0
        for p in procs:
            try:
                seen.setdefault(p.pid, p)
                cpu += p.cpu_percent(interval=None)
                rss += p.memory_info().rss
                th += p.num_threads()
            except psutil.Error:
                pass
        cpu_samples.append(cpu / ncpu)              # % of the whole machine (all logical CPUs)
        rss_samples.append(rss / 2**20)
        thr.append(th)
        g = _gpu_sample()
        if g:
            gpu_u.append(g[0]); gpu_m.append(g[1]); gpu_total = g[2]
        time.sleep(a.interval)
    wall = time.time() - t0
    # the first cpu_percent() of each new process is 0.0 by construction; drop the first sample
    cpu_used = cpu_samples[1:] or cpu_samples

    def mx(x): return round(max(x), 1) if x else None
    def avg(x): return round(sum(x) / len(x), 1) if x else None

    rec = {
        "cmd": cmd, "exit": proc.returncode, "wall_s": round(wall, 2), "samples": len(rss_samples),
        "interval_s": a.interval,
        "cpu_pct_machine_avg": avg(cpu_used), "cpu_pct_machine_max": mx(cpu_used),
        "rss_mb_max": mx(rss_samples), "threads_max": max(thr) if thr else None,
        "gpu": None if not gpu_u else {"util_pct_avg": avg(gpu_u), "util_pct_max": mx(gpu_u),
                                       "vram_mb_max": mx(gpu_m), "vram_mb_total": gpu_total},
        "host": {"platform": platform.platform(), "machine": platform.machine(), "logical_cpus": ncpu,
                 "physical_cpus": psutil.cpu_count(logical=False), "ram_gb": round(psutil.virtual_memory().total / 2**30, 1),
                 "python": sys.version.split()[0]},
        "started_epoch": t0,
    }
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1)
    print(json.dumps({k: rec[k] for k in ("exit", "wall_s", "cpu_pct_machine_avg", "cpu_pct_machine_max", "rss_mb_max", "gpu")}))
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
