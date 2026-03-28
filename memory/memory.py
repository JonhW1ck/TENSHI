# Módulo de memoria persistente de TENSHI

import json
import os

ARCHIVO_MEMORIA = "memory/memoria.json"

# Cargar historial desde archivo al iniciar
def cargar_historial():
    if os.path.exists(ARCHIVO_MEMORIA):
        try:
            with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# Historial en memoria RAM (cargado desde archivo)
historial = cargar_historial()

def agregar_mensaje(rol, contenido):
    historial.append({
        "role": rol,
        "content": contenido
    })
    guardar_historial()

def obtener_historial():
    return historial

def guardar_historial():
    """Guarda el historial en disco."""
    with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

def limpiar_historial():
    historial.clear()
    guardar_historial()
    print("🧹 Memoria limpiada.")