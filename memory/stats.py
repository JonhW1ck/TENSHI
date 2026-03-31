# Módulo de estadísticas de TENSHI

import json
import os

ARCHIVO_STATS = "memory/stats.json"

# Crear carpeta memory si no existe
os.makedirs("memory", exist_ok=True)

def cargar_stats():
    if os.path.exists(ARCHIVO_STATS):
        try:
            with open(ARCHIVO_STATS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass

    return {
        "mensajes_totales": 0,
        "busquedas_internet": 0,
        "archivos_leidos": 0,
        "archivos_escritos": 0,
        "codigos_ejecutados": 0,
        "imagenes_analizadas": 0
    }

# Stats en memoria RAM
stats = cargar_stats()

def guardar_stats():
    with open(ARCHIVO_STATS, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def incrementar(clave):
    if clave in stats:
        stats[clave] += 1
        guardar_stats()

def obtener_stats():
    return stats