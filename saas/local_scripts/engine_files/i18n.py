"""Fixed on-screen strings of the generic scene, by spec language (default English).

Only the words the renderer itself writes live here; everything else (titles, notes, models, captions)
comes from the spec in the document's own language.
"""
STRINGS = {
    "en": {
        "stages": ["Read", "Model", "Equation", "Substitute", "Solve", "Verify"],
        "stage": {"Find": "Find", "Model": "Model", "Equation": "Equation", "Substitute": "Substitute",
                  "Solve": "Solve", "Verify": "Verify", "Answer": "Answer", "Read": "Read"},
        "meta": "{doc}  ·  {n} problem{s}  ·  every value checked",
        "legend": ["data from the page", "condition / sign", "result", "verified"],
        "model": "MODEL", "problem": "Problem", "problem_up": "PROBLEM", "checked": "CHECKED",
        "answers": "Answers",
        "closing": "EVERY VALUE QUOTED FROM THE PAGE · EVERY ANSWER RECOMPUTED (SymPy)",
    },
    "es": {
        "stages": ["Leer", "Modelar", "Ecuación", "Sustituir", "Resolver", "Verificar"],
        "stage": {"Find": "Se pide", "Model": "Modelo", "Equation": "Ecuación", "Substitute": "Sustituir",
                  "Solve": "Resolver", "Verify": "Verificar", "Answer": "Respuesta", "Read": "Leer"},
        "meta": "{doc}  ·  {n} problema{s}  ·  cada valor verificado",
        "legend": ["dato de la hoja", "condición / signo", "resultado", "verificado"],
        "model": "MODELO", "problem": "Problema", "problem_up": "PROBLEMA", "checked": "VERIFICADO",
        "answers": "Respuestas",
        "closing": "CADA VALOR CITADO DE LA HOJA · CADA RESPUESTA RECALCULADA (SymPy)",
    },
}


def strings(lang):
    return STRINGS.get((lang or "en")[:2].lower(), STRINGS["en"])
