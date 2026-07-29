# Visual Studio Code and HTML Basics Tutorial Series

This folder contains an English ManimCE 0.20.1 tutorial series that recreates a Visual Studio Code dark workspace and teaches a complete first HTML workflow.

## Lessons

1. `VSCode01_InterfaceTour`
2. `VSCode02_CreateProjectFolder`
3. `VSCode03_CreateIndexFile`
4. `VSCode04_HTMLSkeleton`
5. `VSCode05_HelloWorldAndPreview`
6. `VSCode06_HTMLLogicAndPractice`

## Build source

```bash
python vscode_html_tutorial/build_source.py
python -m py_compile vscode_html_tutorial/vscode_html_tutorial.py
```

## Render one lesson

```bash
manim -pql vscode_html_tutorial/vscode_html_tutorial.py VSCode01_InterfaceTour --format=mp4 --disable_caching
manim -pqh vscode_html_tutorial/vscode_html_tutorial.py VSCode01_InterfaceTour --format=mp4 --disable_caching
```

The GitHub Actions workflow renders all six lessons in parallel, normalizes every video to H.264/yuv420p at 1920×1080 and 30 fps, performs a complete frame decode, and creates one concatenated full-series MP4.

The pull request is kept isolated until the rendered artifact passes visual frame inspection.
