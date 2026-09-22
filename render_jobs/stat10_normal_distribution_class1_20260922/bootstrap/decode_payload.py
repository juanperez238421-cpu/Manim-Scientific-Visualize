#!/usr/bin/env python3
from pathlib import Path
import base64, tarfile, sys
job = Path(sys.argv[1])
payload = job / 'bootstrap' / 'payload.tgz.b64'
archive = job / 'bootstrap' / 'payload.tgz'
archive.write_bytes(base64.b64decode(payload.read_text(encoding='ascii')))
with tarfile.open(archive, 'r:gz') as tf:
    tf.extractall(job)
print('decoded:', ', '.join(p.name for p in job.iterdir() if p.is_file()))
