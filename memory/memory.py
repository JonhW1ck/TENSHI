# Módulo de memoria persistente de TENSHI

import json
import os

ARCHIVO_MEMORIA = "memory/memoria.json"

MAX_HISTORIAL = 50


# ==========================================
# CREAR CARPETA SI NO EXISTE
# ==========================================

os.makedirs("memory", exist_ok=True)


# ==========================================
# CARGAR HISTORIAL
# ==========================================

def cargar_historial():

    if not os.path.exists(ARCHIVO_MEMORIA):

        with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
            json.dump([], f)

        return []

    try:

        with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:

            data = json.load(f)

            if isinstance(data, list):

                return data

            return []

    except Exception:

        print("⚠️ memoria corrupta — reiniciando")

        with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
            json.dump([], f)

        return []


# ==========================================
# MEMORIA EN RAM
# ==========================================

historial = cargar_historial()


# ==========================================
# AGREGAR MENSAJE
# ==========================================

def agregar_mensaje(rol, contenido):

    historial.append({
        "role": rol,
        "content": contenido
    })

    limitar_historial()

    guardar_historial()


# ==========================================
# OBTENER HISTORIAL
# ==========================================

def obtener_historial():

    return historial


# ==========================================
# LIMITAR HISTORIAL
# ==========================================

def limitar_historial():

    global historial

    if len(historial) > MAX_HISTORIAL:

        historial = historial[-MAX_HISTORIAL:]


# ==========================================
# GUARDAR
# ==========================================

def guardar_historial():

    try:

        with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:

            json.dump(historial, f, ensure_ascii=False, indent=2)

    except Exception as e:

        print("⚠️ error guardando memoria:", e)


# ==========================================
# LIMPIAR
# ==========================================

def limpiar_historial():

    historial.clear()

    guardar_historial()

    print("🧹 memoria limpiada")