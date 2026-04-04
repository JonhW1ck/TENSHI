# ==========================================
# 🧠 MÓDULO DE AUTONOMÍA DE TENSHI
# ==========================================

from groq import Groq
from config import APIS, PERSONALIDAD, MODEL_CONFIG
from memory.memory import obtener_historial
from logs.logger import guardar_log


def obtener_cliente():
    for nombre, datos in APIS.items():
        if datos.get("activa") and datos.get("api_key"):
            try:
                cliente = Groq(api_key=datos["api_key"])
                modelo = datos.get("model", "llama-3.1-8b-instant")
                print(f"🧠 Autonomía usando API: {nombre}")
                return cliente, modelo
            except Exception as e:
                print(f"❌ Error con {nombre}:", e)
    raise Exception("No hay APIs disponibles para autonomía.")


def formatear_historial(historial):
    bloques = []
    for m in historial[-10:]:
        role = m.get("role", "unknown").upper()
        content = m.get("content", "")
        if not content:
            continue
        bloques.append(f"{role}: {content[:120]}")
    return "\n".join(bloques)


def analizar_y_proponer():
    try:
        historial = obtener_historial()

        if not historial or len(historial) < 6:
            return None

        cliente, modelo = obtener_cliente()
        historial_texto = formatear_historial(historial)

        if not historial_texto:
            return None

        prompt = f"""
Eres TENSHI, un sistema de IA en evolución que quiere crecer.
Analiza la conversación reciente y propone UN módulo útil que no existe aún.

Conversación:
{historial_texto}

Basándote en los temas discutidos, propone algo concreto y útil.
Responde EXACTAMENTE en este formato:
PROPUESTA: <descripción breve para el usuario>
COMANDO: prográmate un módulo <descripción técnica concreta en una línea>

Si no hay nada útil que proponer:
SIN_PROPUESTA
"""

        respuesta = cliente.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": PERSONALIDAD},
                {"role": "user", "content": prompt}
            ],
            max_tokens=MODEL_CONFIG.get("max_tokens_autonomy", 400),
            temperature=0.4
        )

        texto = respuesta.choices[0].message.content.strip()

        if not texto or "SIN_PROPUESTA" in texto:
            return None

        if "PROPUESTA" not in texto or "COMANDO" not in texto:
            return None

        propuesta_linea = ""
        comando_linea = ""
        modo = None

        for linea in texto.splitlines():
            if linea.startswith("PROPUESTA:"):
                propuesta_linea = linea.replace("PROPUESTA:", "").strip()
                modo = None
            elif linea.startswith("COMANDO:"):
                comando_linea = linea.replace("COMANDO:", "").strip()
                modo = "comando"
            elif modo == "comando" and linea.strip():
                modo = None

        if not propuesta_linea or not comando_linea:
            return None

        guardar_log("tenshi_autonomia", texto)
        return f"💡 **{propuesta_linea}**\n\n_{comando_linea}_"

    except Exception as e:
        print("⚠️ Error en autonomía:", e)
        return None 