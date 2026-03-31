# Módulo de razonamiento de TENSHI

def construir_razonamiento(mensaje_usuario):
    """Genera un prompt de razonamiento paso a paso."""
    return f"""
Antes de responder, analiza internamente (no muestres este análisis al usuario):
1. ¿Qué está pidiendo exactamente el usuario?
2. ¿Necesito buscar en internet, leer archivos, ejecutar código o analizar una imagen?
3. ¿Cuál es la forma más precisa y completa de responder?
4. ¿Hay algo ambiguo que deba aclarar?

Mensaje del usuario: {mensaje_usuario}

Ahora responde de forma directa, precisa y completa. Sin mostrar el análisis interno.
"""

def evaluar_respuesta(mensaje_usuario, respuesta):
    """Genera un prompt para que TENSHI evalúe su propia respuesta."""
    return f"""
Evalúa tu propia respuesta con estos criterios:
1. ¿Respondiste exactamente lo que se pidió? (sí/no)
2. ¿La respuesta es completa o le falta información? (completa/incompleta)
3. ¿Usaste las herramientas correctas? (sí/no)
4. Puntuación del 1 al 10

Pregunta original: {mensaje_usuario}
Tu respuesta: {respuesta}

Si la puntuación es menor a 7, escribe "MEJORAR:" seguido de la respuesta mejorada.
Si la puntuación es 7 o mayor, escribe "APROBADA:" seguido de la respuesta sin cambios.
"""