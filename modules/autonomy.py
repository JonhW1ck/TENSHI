# ==========================================
# 🧠 MÓDULO DE AUTONOMÍA DE TENSHI
# ==========================================


# ==========================================
# 📦 IMPORTS
# ==========================================

from groq import Groq
from config import APIS, MODELOS, PERSONALIDAD, MODEL_CONFIG

from memory.memory import obtener_historial
from logs.logger import guardar_log


# ==========================================
# 🤖 CLIENTE API
# ==========================================

def obtener_cliente():
    """
    Selecciona una API activa de forma segura.
    """

    for nombre, datos in APIS.items():
        if datos.get("activa"):
            try:
                cliente = Groq(api_key=datos["api_key"])
                modelo = MODELOS["principal"]

                print(f"🧠 Autonomía usando API: {nombre}")

                return cliente, modelo

            except Exception as e:
                print(f"❌ Error con {nombre}:", e)

    raise Exception("No hay APIs disponibles para autonomía.")


# ==========================================
# 📊 FORMATEO DE HISTORIAL
# ==========================================

def formatear_historial(historial):
    """
    Convierte historial en texto compacto y seguro.
    """

    bloques = []

    for m in historial[-10:]:
        role = m.get("role", "unknown").upper()
        content = m.get("content", "")

        if not content:
            continue

        bloques.append(f"{role}: {content[:120]}")

    return "\n".join(bloques)


# ==========================================
# 🧠 ANÁLISIS Y PROPUESTA
# ==========================================

def analizar_y_proponer():
    """
    TENSHI analiza el historial y propone mejoras del sistema.
    """

    try:
        historial = obtener_historial()

        # 🔹 Validación mínima
        if not historial or len(historial) < 6:
            return None

        # 🔹 Frecuencia de análisis (cada 10 mensajes)
        if len(historial) % 10 != 0:
            return None

        cliente, modelo = obtener_cliente()

        historial_texto = formatear_historial(historial)

        if not historial_texto:
            return None


        # ======================================
        # 🧾 PROMPT DE AUTO-MEJORA
        # ======================================

        prompt = f"""
Eres TENSHI, un sistema de IA en evolución.
Analiza ÚNICAMENTE la conversación reciente que se muestra abajo.
NO inventes problemas. NO asumas cosas que no estén explícitamente en el texto.
Solo reporta lo que puedas observar directamente en la conversación.

Detecta SOLO si hay:
1. Una solicitud del usuario que no fue respondida correctamente
2. Un error explícito mencionado por el usuario
3. Una funcionalidad que el usuario pidió y no existe

Conversación:
{historial_texto}

Formato de respuesta:

Si hay algo concreto y observable:
PROPUESTA: ...
RAZÓN: ...
IMPACTO: ...

Si no hay nada concreto y observable:
SIN_PROPUESTA
"""


        # ======================================
        # 🤖 LLAMADA AL MODELO
        # ======================================

        respuesta = cliente.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": PERSONALIDAD},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.4
        )

        texto = respuesta.choices[0].message.content.strip()


        # ======================================
        # 📤 VALIDACIÓN DE RESPUESTA
        # ======================================

        if not texto or "SIN_PROPUESTA" in texto:
            return None

        if "PROPUESTA" not in texto:
            return None

        guardar_log("tenshi_autonomia", texto)

        return texto

    except Exception as e:
        print("⚠️ Error en autonomía:", e)
        return None