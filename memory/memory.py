# Módulo de memoria persistente de TENSHI

import json
import os

ARCHIVO_MEMORIA = "memory/memoria.json"
ARCHIVO_PENDIENTES = "memory/pendientes.json"

MAX_HISTORIAL = 50

os.makedirs("memory", exist_ok=True)

# ==============================
# 🧠 HISTORIAL (CHAT)
# ==============================

def cargar_historial():
    if not os.path.exists(ARCHIVO_MEMORIA):
        with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

    try:
        with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        print("⚠️ memoria corrupta — reiniciando")
        with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

historial = cargar_historial()

def agregar_mensaje(rol, contenido):
    historial.append({"role": rol, "content": contenido})
    limitar_historial()
    guardar_historial()

def obtener_historial():
    return historial

def limitar_historial():
    global historial
    if len(historial) > MAX_HISTORIAL:
        historial = historial[-MAX_HISTORIAL:]

def guardar_historial():
    try:
        with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
            json.dump(historial, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("⚠️ error guardando memoria:", e)

def limpiar_historial():
    historial.clear()
    guardar_historial()

# ==============================
# 📌 PENDIENTES
# ==============================

def cargar_pendientes():
    if not os.path.exists(ARCHIVO_PENDIENTES):
        with open(ARCHIVO_PENDIENTES, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

    try:
        with open(ARCHIVO_PENDIENTES, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        print("⚠️ pendientes corruptos — reiniciando")
        with open(ARCHIVO_PENDIENTES, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

pendientes = cargar_pendientes()

def guardar_pendientes():
    try:
        with open(ARCHIVO_PENDIENTES, "w", encoding="utf-8") as f:
            json.dump(pendientes, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("⚠️ error guardando pendientes:", e)

# ✅ FUNCIÓN CORRECTA
def agregar_pendiente(pendiente):
    """
    Recibe un dict como:
    {
        "texto": "Comprar pan",
        "fecha": "2026-04-01" o None,
        "completado": False
    }
    """
    if not isinstance(pendiente, dict):
        print("⚠️ pendiente inválido")
        return

    pendientes.append({
        "texto": pendiente.get("texto", ""),
        "fecha": pendiente.get("fecha"),
        "completado": pendiente.get("completado", False)
    })

    guardar_pendientes()

def obtener_pendientes():
    return pendientes

def completar_pendiente(index):
    if 0 <= index < len(pendientes):
        pendientes[index]["completado"] = True
        guardar_pendientes()

def eliminar_pendiente(index):
    if 0 <= index < len(pendientes):
        pendientes.pop(index)
        guardar_pendientes()

def limpiar_pendientes():
    pendientes.clear()
    guardar_pendientes()