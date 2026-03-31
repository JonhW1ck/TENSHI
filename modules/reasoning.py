# ============================================
# RAZONAMIENTO INTERNO DE TENSHI
# ============================================

def construir_razonamiento(mensaje_usuario):
    """
    Genera un prompt de razonamiento interno.
    Este razonamiento NO debe mostrarse al usuario.
    """

    return f"""
Piensa paso a paso antes de responder.

Analiza internamente:

1. ¿Qué quiere realmente el usuario?
2. ¿Necesito usar alguna herramienta?
   - búsqueda en internet
   - lectura de archivos
   - ejecución de código
   - análisis de imagen
3. ¿Cuál es la forma más clara y correcta de responder?

Mensaje del usuario:
{mensaje_usuario}

Ahora responde al usuario de forma directa y clara.
NO muestres tu razonamiento interno.
"""


# ============================================
# AUTOEVALUACIÓN
# ============================================

def evaluar_respuesta(mensaje_usuario, respuesta):
    """
    Evalúa si la respuesta es correcta.
    Devuelve SOLO la respuesta final corregida.
    """

    return f"""
Revisa si la respuesta responde correctamente a la pregunta.

Pregunta del usuario:
{mensaje_usuario}

Respuesta generada:
{respuesta}

Si la respuesta es correcta y completa, devuelve exactamente:

APROBADA: <respuesta final>

Si la respuesta tiene errores o está incompleta, devuelve exactamente:

MEJORAR: <respuesta corregida y mejorada>

No expliques tu evaluación.
No muestres análisis.
Solo devuelve el formato indicado.
"""