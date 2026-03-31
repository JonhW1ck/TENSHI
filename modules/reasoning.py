# Módulo de razonamiento de TENSHI

def construir_razonamiento(mensaje_usuario):
    """Genera un prompt de razonamiento paso a paso."""
    return f"""
Antes de responder, analiza internamente:
1. ¿Qué está pidiendo exactamente el usuario?
2. ¿Necesito buscar en internet, leer archivos, ejecutar código o analizar una imagen?
3. ¿Cuál es la forma más precisa y completa de responder?
4. ¿Hay algo ambiguo que deba aclarar?

Mensaje del usuario: {mensaje_usuario}

Ahora responde de forma directa, precisa y completa.
"""