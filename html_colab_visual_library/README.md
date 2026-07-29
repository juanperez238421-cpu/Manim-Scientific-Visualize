# HTML Colab Visual Library V2

This redesign replaces the previous generic editor/browser split with a continuous Google Colab teaching workflow.

## Visual system

- notebook title and Drive save state;
- File, Edit, View, Insert, Runtime, Tools and Help menus;
- `+ Code` and `+ Text` controls;
- Connect and Share controls;
- left notebook sidebar;
- Markdown explanation cells;
- executable HTML code cells with run button, line numbers and execution count;
- inline browser output;
- camera focus between interface, code and result;
- Robledo Market Lab output based on the real `IJR---Seminario` project.

## Five scenes

1. `HTML01WhatIsHTML`
2. `HTML02HeadAndBody`
3. `HTML03SemanticText`
4. `HTML04LinksListsImages`
5. `HTML05LayoutAndForms`

## Build the single source file

The source is stored in ordered text parts so it can be audited easily.

```bash
python html_colab_visual_library/build_source.py
python -m py_compile html_colab_visual_library/html_colab_visual_library.py
```

## Test and final render

```bash
manim -pql html_colab_visual_library/html_colab_visual_library.py HTML01WhatIsHTML --format=mp4 --disable_caching
manim -pqh html_colab_visual_library/html_colab_visual_library.py HTML01WhatIsHTML --format=mp4 --disable_caching
```

The GitHub Actions workflow renders all five scenes with ManimCE 0.20.1, verifies the resulting MP4 files using `ffprobe` and a full FFmpeg decode, calculates SHA-256 hashes and uploads one delivery artifact.
