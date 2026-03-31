# Planner de TENSHI
# Decide qué estrategia usar antes de responder

def analizar_intencion(mensaje):
    """
    Analiza el mensaje del usuario y detecta qué tipo de tarea es.
    """

    mensaje = mensaje.lower()

    if any(p in mensaje for p in ["investiga", "analiza", "profundiza", "explica a fondo"]):
        return "analisis_profundo"

    if any(p in mensaje for p in ["paso a paso", "guíame", "enseña", "aprende"]):
        return "modo_enseñanza"

    if any(p in mensaje for p in ["programa", "código", "script", "python", "función"]):
        return "programacion"

    if any(p in mensaje for p in ["busca", "internet", "noticias", "precio", "actualmente"]):
        return "busqueda"

    if any(p in mensaje for p in ["resume", "resumen", "simplifica"]):
        return "resumen"

    return "respuesta_normal"


def construir_plan(mensaje):
    """
    Construye un pequeño plan interno antes de responder.
    """

    tipo = analizar_intencion(mensaje)

    if tipo == "analisis_profundo":
        return """
PLAN:
1. Descomponer el problema
2. Analizar cada parte
3. Explicar conclusiones claras
"""

    if tipo == "modo_enseñanza":
        return """
PLAN:
1. Explicar concepto
2. Dar ejemplo
3. Dar analogía simple
"""

    if tipo == "programacion":
        return """
PLAN:
1. Entender problema técnico
2. Diseñar solución
3. Escribir código claro
"""

    if tipo == "busqueda":
        return """
PLAN:
1. Obtener información externa
2. Verificar relevancia
3. Responder usando los datos
"""

    if tipo == "resumen":
        return """
PLAN:
1. Identificar ideas clave
2. Eliminar redundancia
3. Resumir claramente
"""

    return """
PLAN:
Responder de forma clara y directa
"""