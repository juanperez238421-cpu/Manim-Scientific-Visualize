# Statistics — Data Types in Google Colab

ManimCE classroom presentation connecting Python/Colab data types with statistical variable types.

## Scene
`StatisticsColabDataTypes`

## Lesson sequence
1. Why data types matter
2. `int`, `float`, `str`, `bool`, `None`
3. Lists and dictionaries
4. `type()` and explicit conversion
5. pandas `DataFrame` and `df.dtypes`
6. Python types vs statistical variable types
7. Reusable workflow before statistical analysis

## Statistical bridge
The presentation distinguishes programming storage types from statistical meaning:
- discrete quantitative → commonly `int`
- continuous quantitative → commonly `float`
- nominal qualitative → commonly `str` / pandas category
- binary variables → commonly `bool`
- missing values → `None` / `NaN`

## Render
The GitHub Actions workflow reconstructs the canonical JP classroom style, runs `py_compile`, renders an accelerated `-pql` gate, then a literal `-pqh` final at 1920×1080 and 30 fps.

Local commands once `jp_classroom_style.py` is beside the scene:
```bash
manim -pql Statistics_Colab_Data_Types.py StatisticsColabDataTypes --disable_caching
manim -pqh Statistics_Colab_Data_Types.py StatisticsColabDataTypes --disable_caching
```
