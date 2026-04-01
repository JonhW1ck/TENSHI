# ==========================================
# 📊 MÓDULO DE ESTADÍSTICAS DE TENSHI
# ==========================================


# ==========================================
# 📦 IMPORTS
# ==========================================

import json
import os
import tempfile
import shutil
from typing import Dict


# ==========================================
# ⚙️ CONFIGURACIÓN
# ==========================================

DIR_MEMORIA = "memory"
ARCHIVO_STATS = os.path.join(DIR_MEMORIA, "stats.json")

os.makedirs(DIR_MEMORIA, exist_ok=True)


# ==========================================
# 🔒 UTILIDADES SEGURAS
# ==========================================

def _escritura_atomica(ruta: str, data: Dict):
    """
    Escritura atómica para evitar corrupción.
    """
    try:
        fd, tmp_path = tempfile.mkstemp(dir=DIR_MEMORIA)
        with os.fdopen(fd, "w", encoding="utf-8") as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
        shutil.replace(tmp_path, ruta)
    except Exception as e:
        print("⚠️ error escritura stats:", e)


def _leer_json_seguro(ruta: str, default: Dict):
    """
    Lectura robusta con recuperación.
    """
    if not os.path.exists(ruta):
        _escritura_atomica(ruta, default)
        return default

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("⚠️ stats corruptos — reiniciando")
        _escritura_atomica(ruta, default)
        return default


# ==========================================
# 📊 ESTRUCTURA BASE
# ==========================================

def _estructura_base():
    return {
        "mensajes_totales": 0,
        "busquedas_internet": 0,
        "archivos_leidos": 0,
        "archivos_escritos": 0,
        "codigos_ejecutados": 0,
        "imagenes_analizadas": 0
    }


def _validar_stats(data: Dict) -> Dict:
    """
    Garantiza integridad de claves.
    """
    base = _estructura_base()

    if not isinstance(data, dict):
        return base

    for k in base:
        if k in data and isinstance(data[k], int):
            base[k] = data[k]

    return base


# ==========================================
# 📊 CARGA EN MEMORIA
# ==========================================

stats: Dict = _validar_stats(
    _leer_json_seguro(ARCHIVO_STATS, _estructura_base())
)


# ==========================================
# 💾 GUARDADO
# ==========================================

def guardar_stats():
    try:
        _escritura_atomica(ARCHIVO_STATS, stats)
    except Exception as e:
        print("⚠️ error guardando stats:", e)


# ==========================================
# ➕ OPERACIONES
# ==========================================

def incrementar(clave: str, valor: int = 1):
    """
    Incrementa una métrica de forma segura.
    """
    if clave not in stats:
        print(f"⚠️ clave desconocida en stats: {clave}")
        return

    if not isinstance(valor, int):
        return

    stats[clave] += valor
    guardar_stats()


def obtener_stats() -> Dict:
    """
    Devuelve copia segura.
    """
    return dict(stats)


def resetear_stats():
    """
    Reinicia estadísticas.
    """
    global stats
    stats = _estructura_base()
    guardar_stats()

