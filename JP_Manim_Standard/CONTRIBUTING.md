# Contributing to JP Manim Classroom Standard

1. Create a feature branch.
2. Keep lesson content separate from the visual library.
3. Do not hard-code `pixel_width`, `pixel_height` or `frame_rate` in lesson files.
4. Run `python tools/check_style.py <lesson.py>`.
5. Run the low-quality smoke render.
6. For changes to the visual library, render at least one representative figure/equation lesson, one table-heavy lesson and one 3D lesson before merge.
7. Do not upgrade ManimCE in the same PR as unrelated visual changes.
8. Update `CHANGELOG.md` for user-visible standard changes.
