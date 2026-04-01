# ==========================================
# 🧠 ORCHESTRATOR DE TENSHI (ROBUSTO v2)
# ==========================================

from groq import Groq
from config import APIS, PERSONALIDAD

from memory.memory import agregar_mensaje, obtener_historial
from logs.logger import guardar_log

from database.db_manager import agregar_pendiente, obtener_pendientes

import re
from datetime import datetime


# ==========================================
# 🔌 CLIENTE IA
# ==========================================

def obtener_cliente():
    """
    Obtiene cliente disponible de IA
    """

    for nombre, datos in APIS.items():

        if datos.get("activa") and datos.get("api_key"):

            try:

                cliente = Groq(api_key=datos["api_key"])

                modelo = datos.get("model")

                if not modelo:
                    raise Exception("Modelo no configurado")

                return cliente, modelo

            except Exception as e:

                print(f"⚠️ Error inicializando API {nombre}: {e}")

    raise Exception("No hay APIs disponibles.")


# ==========================================
# 🧠 DETECCIÓN DE INTENCIÓN
# ==========================================

def detectar_intencion(texto):

    if not texto:
        return "general"

    texto = texto.lower()

    if "recuérdame" in texto or "recuerdame" in texto:
        return "memoria"

    if "pendientes" in texto:
        return "consultar_pendientes"

    return "general"


# ==========================================
# 🧹 LIMPIAR TEXTO
# ==========================================

def limpiar_texto(texto):

    texto = texto.lower()

    texto = re.sub(r"recu[eé]rdame", "", texto)

    texto = texto.strip()

    return texto


# ==========================================
# 📅 EXTRAER FECHA
# ==========================================

def extraer_fecha(texto):

    texto = texto.lower()

    if "mañana" in texto:
        return datetime.now().date().isoformat()

    return None


# ==========================================
# 🔁 DETECTAR DUPLICADOS
# ==========================================

def pendiente_ya_existe(texto, fecha, lista):

    for p in lista:

        if (
            p.get("texto") == texto
            and p.get("fecha") == fecha
        ):
            return True

    return False


# ==========================================
# 🧠 CONSTRUIR MENSAJES PARA IA
# ==========================================

def construir_mensajes(historial, mensaje_usuario):

    mensajes = [
        {
            "role": "system",
            "content": PERSONALIDAD
        }
    ]

    for m in historial:

        role = m.get("role")
        content = m.get("content")

        if role in ["user", "assistant"] and content:
            mensajes.append({
                "role": role,
                "content": content
            })

    mensajes.append({
        "role": "user",
        "content": mensaje_usuario
    })

    return mensajes


# ==========================================
# 🤖 RESPUESTA IA
# ==========================================

def generar_respuesta_ia(mensaje_usuario):

    cliente, modelo = obtener_cliente()

    historial = obtener_historial()[-10:]

    mensajes = construir_mensajes(historial, mensaje_usuario)

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        max_tokens=512,
        temperature=0.7
    )

    try:

        texto = respuesta.choices[0].message.content.strip()

        if not texto:
            texto = "⚠️ No recibí respuesta del modelo."

    except Exception:

        texto = "⚠️ Error interpretando respuesta del modelo."

    return texto


# ==========================================
# 🧠 RESPUESTA PRINCIPAL
# ==========================================

def responder(mensaje_usuario):

    try:

        if not mensaje_usuario:
            return "⚠️ No recibí ningún mensaje."

        # 🔎 detectar intención
        intencion = detectar_intencion(mensaje_usuario)

        # ==========================================
        # 📌 GUARDAR PENDIENTE
        # ==========================================

        if intencion == "memoria":

            texto_limpio = limpiar_texto(mensaje_usuario)

            fecha = extraer_fecha(mensaje_usuario)

            lista = obtener_pendientes() or []

            if pendiente_ya_existe(texto_limpio, fecha, lista):

                return "⚠️ Ese pendiente ya existe."

            agregar_pendiente(texto_limpio, fecha)

            respuesta = "📌 Guardado como pendiente."

            agregar_mensaje("user", mensaje_usuario)
            agregar_mensaje("assistant", respuesta)

            guardar_log("usuario", mensaje_usuario)
            guardar_log("tenshi", respuesta)

            return respuesta


        # ==========================================
        # 📋 CONSULTAR PENDIENTES
        # ==========================================

        if intencion == "consultar_pendientes":

            lista = obtener_pendientes() or []

            if not lista:
                return "📭 No tienes pendientes."

            respuesta = "📋 Tus pendientes:\n"

            for i, p in enumerate(lista, 1):

                texto = p.get("texto", "Sin descripción")
                fecha = p.get("fecha", "Sin fecha")

                respuesta += f"{i}. ⏳ {texto} ({fecha})\n"

            guardar_log("usuario", mensaje_usuario)
            guardar_log("tenshi", respuesta)

            return respuesta


        # ==========================================
        # 🤖 RESPUESTA IA
        # ==========================================

        texto = generar_respuesta_ia(mensaje_usuario)

        agregar_mensaje("user", mensaje_usuario)
        agregar_mensaje("assistant", texto)

        guardar_log("usuario", mensaje_usuario)
        guardar_log("tenshi", texto)

        return texto


    except Exception as e:

        import traceback

        print("\n🔥 ERROR REAL TENSHI 🔥")
        traceback.print_exc()
        print("MENSAJE:", str(e))
        print()

        return f"ERROR REAL: {str(e)}"