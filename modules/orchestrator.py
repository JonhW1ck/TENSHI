# Orquestador de TENSHI (CEREBRO REAL)

from groq import Groq
from config import APIS, MODELOS, MODEL_CONFIG, PERSONALIDAD

from memory.memory import (
    agregar_mensaje,
    obtener_historial,
    agregar_pendiente,
    obtener_pendientes,
    guardar_pendientes
)

from logs.logger import guardar_log
from memory.stats import incrementar

from datetime import datetime, timedelta
import re

MAX_HISTORY = 8


# ==========================================
# CLIENTE API
# ==========================================

def obtener_cliente():
    for nombre, datos in APIS.items():
        if datos["activa"]:
            try:
                cliente = Groq(api_key=datos["api_key"])
                modelo = MODELOS["principal"]
                print(f"✅ API: {nombre} | modelo {modelo}")
                return cliente, modelo
            except Exception as e:
                print(f"❌ {nombre} falló:", e)
    raise Exception("No hay APIs disponibles")


# ==========================================
# DETECCIÓN DE INTENCIÓN
# ==========================================

def detectar_intencion(mensaje):
    m = mensaje.lower()

    if any(p in m for p in [
        "qué pendientes tengo","cuales son mis pendientes",
        "mis pendientes","lista de pendientes","ver pendientes"
    ]):
        return "consultar_pendientes"

    if any(p in m for p in [
        "recuerda","recordar","guarda","anota",
        "tengo que","no olvides","recuérdame"
    ]):
        return "memoria"

    return "chat"


# ==========================================
# FECHA
# ==========================================

def extraer_fecha(mensaje):
    m = mensaje.lower()
    hoy = datetime.now()

    if "mañana" in m:
        return (hoy + timedelta(days=1)).strftime("%Y-%m-%d")

    if "hoy" in m:
        return hoy.strftime("%Y-%m-%d")

    match = re.search(r"(en|dentro de)\s+(\d+)\s+d[ií]as", m)
    if match:
        dias = int(match.group(2))
        return (hoy + timedelta(days=dias)).strftime("%Y-%m-%d")

    return None


# ==========================================
# LIMPIAR TEXTO
# ==========================================

def limpiar_texto(mensaje):
    texto = mensaje.lower()

    palabras_basura = [
        "guarda","recuerda","recordar","recuérdame","recuerdame",
        "anota","apunta","por favor"
    ]

    for palabra in palabras_basura:
        texto = texto.replace(palabra, "")

    texto = re.sub(r"\b(hoy|mañana)\b", "", texto)
    texto = re.sub(r"(en|dentro de)\s+\d+\s+d[ií]as", "", texto)
    texto = re.sub(r"\d+", "", texto)

    texto = " ".join(texto.split())

    # 🔥 LIMPIEZA EXTRA NATURAL
    if texto.startswith("que "):
        texto = texto[4:]

    if texto.startswith("tengo que "):
        texto = texto[10:]

    return texto.capitalize()


# ==========================================
# EVITAR DUPLICADOS
# ==========================================

def pendiente_ya_existe(texto, fecha, lista):
    for p in lista:
        if p["texto"] == texto and p.get("fecha") == fecha:
            return True
    return False


def limpiar_duplicados():
    lista = obtener_pendientes()
    vistos = set()
    nueva = []

    for p in lista:
        clave = (p["texto"], p.get("fecha"))
        if clave not in vistos:
            vistos.add(clave)
            nueva.append(p)

    from memory.memory import pendientes
    pendientes.clear()
    pendientes.extend(nueva)
    guardar_pendientes()


# ==========================================
# RESPUESTA PRINCIPAL
# ==========================================

def responder(mensaje_usuario):

    cliente, modelo = obtener_cliente()
    intencion = detectar_intencion(mensaje_usuario)

    # ==========================
    # MEMORIA
    # ==========================

    if intencion == "memoria":

        texto_limpio = limpiar_texto(mensaje_usuario)
        fecha = extraer_fecha(mensaje_usuario)

        lista = obtener_pendientes()

        if pendiente_ya_existe(texto_limpio, fecha, lista):
            return "⚠️ Ese pendiente ya existe."

        agregar_pendiente({
            "texto": texto_limpio,
            "fecha": fecha,
            "completado": False
        })

        limpiar_duplicados()

        agregar_mensaje("user", mensaje_usuario)

        respuesta = "📌 Guardado como pendiente."

        agregar_mensaje("assistant", respuesta)
        guardar_log("usuario", mensaje_usuario)
        guardar_log("tenshi", respuesta)

        return respuesta

    # ==========================
    # CONSULTAR PENDIENTES
    # ==========================

    if intencion == "consultar_pendientes":

        limpiar_duplicados()
        pendientes = obtener_pendientes()

        if not pendientes:
            return "📋 No tienes pendientes registrados."

        texto = "📋 Tus pendientes:\n\n"

        for i, p in enumerate(pendientes, 1):
            estado = "✅" if p.get("completado") else "⏳"
            fecha = f" ({p['fecha']})" if p.get("fecha") else ""
            texto += f"{i}. {estado} {p['texto']}{fecha}\n"

        agregar_mensaje("assistant", texto)
        return texto

    # ==========================
    # IA NORMAL
    # ==========================

    mensajes = [{"role": "system", "content": PERSONALIDAD}]
    historial = obtener_historial()[-MAX_HISTORY:]
    mensajes += historial

    mensajes.append({
        "role": "user",
        "content": mensaje_usuario
    })

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        max_tokens=MODEL_CONFIG["max_tokens"],
        temperature=MODEL_CONFIG["temperature"]
    )

    texto = respuesta.choices[0].message.content

    agregar_mensaje("user", mensaje_usuario)
    agregar_mensaje("assistant", texto)

    guardar_log("usuario", mensaje_usuario)
    guardar_log("tenshi", texto)

    incrementar("mensajes_totales")

    return texto