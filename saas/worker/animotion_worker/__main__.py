"""python -m animotion_worker [run|once|check]"""
from __future__ import annotations

import sys
import threading

from .api import WorkerApi
from .config import WorkerSettings
from .service import Worker


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "run"
    s = WorkerSettings.from_env()
    errs = s.validate()
    if cmd == "check":
        print("OK" if not errs else "PROBLEMAS:\n - " + "\n - ".join(errs))
        return 0 if not errs else 2
    if errs:
        print("Configuración inválida:\n - " + "\n - ".join(errs), file=sys.stderr)
        return 2
    w = Worker(s, WorkerApi(s.api_url, s.worker_token, s.worker_id))
    if cmd == "once":
        return 0 if w.run_once() else 1
    stop = threading.Event()
    try:
        w.run_forever(stop)
    except KeyboardInterrupt:
        stop.set()
    return 0


if __name__ == "__main__":
    sys.exit(main())
