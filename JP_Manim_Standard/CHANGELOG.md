# Changelog

## 1.0.0 — 2026-08-15

- Extracted the JP classroom visual system into an installable package.
- Preserved the 16:9 white/black/gray visual contract and reusable layout helpers.
- Moved pixel resolution/FPS out of the style module so low-quality previews remain low-cost.
- Pinned ManimCE 0.20.1 for reproducibility.
- Enabled Manim caching by default; clean/no-cache modes are explicit.
- Added static style QA, low-quality CI smoke render, manual audited final render, ffprobe/decode verification, QA-frame extraction and SHA-256 packaging.
- Defined separate desktop (`-pqh`) and headless (`-qh`) final profiles.
