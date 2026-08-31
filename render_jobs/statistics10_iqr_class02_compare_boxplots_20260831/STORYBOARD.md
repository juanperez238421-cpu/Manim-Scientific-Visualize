# Statistics 10 - IQR & Box Plots - Class 2
## From Construction to Interpretation

**Course:** Statistics 10°  
**Institution:** Instituto Jorge Robledo  
**Academic year:** 2026  
**Sequence:** Third Period - IQR / Boxplot  
**Primary scene:** `Statistics10IQRClass02CompareBoxplotsFinal`

## Pedagogical continuity

Class 2 is a direct continuation of the existing Week 1 / Class 1 IQR-boxplot lineage. Class 1 established:

`ORDER DATA -> Q2 -> SPLIT -> Q1/Q3 -> IQR -> BOX -> WHISKERS -> INTERPRET`

Class 2 keeps the same quartile convention and changes the central question from **"How do I construct it?"** to **"What does it tell me?"**

### Quartile convention preserved

- Odd `n`: identify `Q2`, exclude that observation from both halves, then find `Q1` and `Q3` as the medians of the lower and upper halves.
- Even `n`: split the ordered observations into two equal halves, then find the median of each half.
- No software-specific percentile algorithm is substituted.

## Scene map

1. **Opening** - Class 1 route becomes `... -> INTERPRET -> COMPARE`.
2. **Recall** - Q2 = center, IQR = middle 50%, whiskers = extreme regular observations.
3. **Why fences exist** - ordered data `2,3,4,5,6,7,8,20`; visual need before formulas.
4. **Correct whiskers** - formal modified-boxplot distinction: fences are limits, whiskers are real observations.
5. **Worked classification** - IQR, LF, UF, outlier, actual whiskers.
6. **Read one boxplot** - center, middle spread, regular extent, outlier.
7. **Same-scale comparison** - Group A and Group B on one numerical scale.
8. **Compare center** - Group B median `54.5` > Group A median `51`.
9. **Compare IQR** - Group B IQR `5` vs Group A IQR `11.5`.
10. **Compare whiskers** - regular exterior spread.
11. **Inspect asymmetry** - cautious language: clues, not proof.
12. **Inspect outliers** - Group B upper fence `65`, outlier `75`, upper whisker `58`.
13. **Contextual conclusion** - evidence + meaning + qualification.
14. **Common mistakes** - fences as whiskers, connected outliers, unequal scales, vague language.
15. **Student challenge** - new two-group comparison, controlled pause, then reveal.
16. **Exit ticket** - IQR/fences/outlier/interpretation.
17. **Next lesson bridge** - `Q1=P25`, `Q2=P50`, `Q3=P75` as a preview only.

## Numerical truth set

### Formal outlier example

Data: `2,3,4,5,6,7,8,20`

- `Q1 = 3.5`
- `Q2 = 5.5`
- `Q3 = 7.5`
- `IQR = 4`
- `LF = -2.5`
- `UF = 13.5`
- lower whisker = `2`
- upper whisker = `8`
- outlier = `20`

### Comparison groups

**Group A:** `40,44,47,50,52,55,59,63`

- `Q1=45.5`, `Q2=51`, `Q3=57`
- `IQR=11.5`
- whiskers `40` and `63`
- no outliers

**Group B:** `49,52,53,54,55,57,58,75`

- `Q1=52.5`, `Q2=54.5`, `Q3=57.5`
- `IQR=5`
- `LF=45`, `UF=65`
- whiskers `49` and `58`
- upper outlier `75`

## Visual contract

- 1920x1080, 16:9, 30 fps.
- White background.
- Black primary typography and mathematical notation.
- Neutral grays only for hierarchy and secondary structure.
- Large projector-safe text.
- Persistent numbered section header.
- Same numerical scale whenever two boxplots are compared.
- Object-driven construction and highlighting rather than dense slide replacement.
- No decorative color dependency.

## Language

Student-facing language is English. Spanish appears only as concise support when pedagogically useful; mathematical meaning takes priority.

## Final takeaway

**Construct. Read. Compare. Justify.**
