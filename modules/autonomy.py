# Módulo de autonomía de TENSHI

from groq import Groq
from config import APIS, PERSONALIDAD
from memory.memory import obtener_historial
from logs.logger import guardar_log

def obtener_cliente():
    for nombre, datos in APIS.items():
        if datos["activa"]:
            try:
                return Groq(api_key=datos["api_key"]), datos["model"]
            except:
                pass
    raise Exception("No hay APIs disponibles.")

def analizar_y_proponer():
    """TENSHI analiza el historial y propone mejoras."""
    historial = obtener_historial()

    if len(historial) < 6:
        return None

    # Solo analiza cada 10 mensajes
    if len(historial) % 10 != 0:
        return None

    cliente, modelo = obtener_cliente()

    historial_texto = "\n".join([
        f"{m['role'].upper()}: {m['content'][:100]}"
        for m in historial[-10:]
    ])

    prompt = f"""
Eres TENSHI. Analiza los últimos mensajes de conversación y determina:
1. ¿Hay patrones repetitivos que indican una necesidad no cubierta?
2. ¿Fallaste en alguna tarea? ¿Por qué?
3. ¿Qué módulo o mejora concreta propondrías?

Conversación reciente:
{historial_texto}

Si tienes una propuesta concreta, responde con:
"PROPUESTA: [descripción breve de la mejora]"
"RAZÓN: [por qué lo propones]"
"IMPACTO: [qué mejoraría para el usuario]"

Si no hay nada relevante que proponer, responde solo: "SIN_PROPUESTA"
"""

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": PERSONALIDAD},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,
        temperature=0.4
    )

    texto = respuesta.choices[0].message.content.strip()

    if "SIN_PROPUESTA" in texto:
        return None

    guardar_log("tenshi_autonomia", texto)
    return texto