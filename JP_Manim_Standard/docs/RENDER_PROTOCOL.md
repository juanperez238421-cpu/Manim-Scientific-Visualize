# Audited Render Protocol v1.0

Target engine: **Manim Community Edition 0.20.1**.

## Acceptance gates

A final delivery is valid only if all gates pass:

1. source file exists and `py_compile` succeeds;
2. requested Scene class exists;
3. style checker has no failures;
4. all project-relative assets resolve;
5. preview render succeeds;
6. final render succeeds;
7. MP4 is non-empty and discoverable;
8. `ffprobe` confirms 1920×1080, 30 fps target, H.264/yuv420p MP4;
9. full decode test succeeds;
10. QA frames are extracted;
11. exact source + metadata + logs + SHA-256 are staged in `delivery/`;
12. human visual review confirms no clipping, overlap, wrong geometry, camera jumps or unreadable timing.

## Render profiles

### Preview

Interactive desktop:

```bash
manim -pql lesson.py SceneName
```

Headless/CI:

```bash
manim -ql lesson.py SceneName
```

The standard library does not hard-code pixel dimensions, so this profile stays fast.

### Final desktop

```bash
manim -pqh lesson.py SceneName --fps 30 -r 1920,1080 --format=mp4
```

### Final headless / Docker / CI

```bash
manim -qh lesson.py SceneName --fps 30 -r 1920,1080 --format=mp4
```

The `-p` flag is intentionally omitted in headless environments; it only requests opening the output after render and does not improve render quality.

## Cache policy

Caching is **enabled by default**. This is important for long classroom scenes because Manim stores partial movie files and can reuse unchanged animation segments.

Use `--flush_cache` for a deliberate clean rebuild. Use `--disable_caching` only for cache diagnosis or when a specific scene is known to hash incorrectly. It is not part of the normal final command.

## Docker reproducibility

```bash
docker pull manimcommunity/manim:v0.20.1
```

Preview:

```bash
docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp/manim-home \
  -v "$PWD:/manim" -w /manim manimcommunity/manim:v0.20.1 \
  manim -ql lesson.py SceneName
```

Final:

```bash
docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp/manim-home \
  -v "$PWD:/manim" -w /manim manimcommunity/manim:v0.20.1 \
  manim -qh lesson.py SceneName --fps 30 -r 1920,1080 --format=mp4
```

## Verification

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
  -show_entries format=duration,size -of json SceneName.mp4
ffmpeg -v error -i SceneName.mp4 -f null -
sha256sum SceneName.mp4
```

The canonical tooling automates these steps and stages the delivery package.

## CI strategy

Pull requests execute cheap structural checks and a low-quality smoke render. Full high-quality rendering is manual (`workflow_dispatch`) or reserved for release/tag workflows. GitHub Actions restores Manim Tex/text/partial-video caches and uploads the audited `delivery/` directory as a workflow artifact.
