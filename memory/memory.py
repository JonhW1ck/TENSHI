# ==========================================
# 🧠 MÓDULO DE MEMORIA PERSISTENTE DE TENSHI
# ==========================================

# ==========================================
# 📦 IMPORTS
# ==========================================

import json
import os
import tempfile
import shutil
import threading
from typing import List, Dict, Any


# ==========================================
# ⚙️ CONFIGURACIÓN
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIR_MEMORIA = os.path.join(BASE_DIR, "memory")

ARCHIVO_MEMORIA = os.path.join(DIR_MEMORIA, "memoria.json")
ARCHIVO_PENDIENTES = os.path.join(DIR_MEMORIA, "pendientes.json")

MAX_HISTORIAL = 50

os.makedirs(DIR_MEMORIA, exist_ok=True)

LOCK = threading.Lock()


# ==========================================
# 🔒 UTILIDADES DE ESCRITURA SEGURA
# ==========================================

def _escritura_atomica(ruta: str, data: Any):

    try:

        with LOCK:

            fd, tmp_path = tempfile.mkstemp(dir=DIR_MEMORIA)

            with os.fdopen(fd, "w", encoding="utf-8") as tmp:

                json.dump(data, tmp, ensure_ascii=False, indent=2)

            os.replace(tmp_path, ruta)

    except Exception as e:

        print("⚠️ error en escritura atómica:", e)


def _leer_json_seguro(ruta: str, default):

    if not os.path.exists(ruta):

        _escritura_atomica(ruta, default)

        return default

    try:

        with open(ruta, "r", encoding="utf-8") as f:

            return json.load(f)

    except Exception:

        print(f"⚠️ archivo corrupto ({ruta}) — reiniciando")

        _escritura_atomica(ruta, default)

        return default


# ==========================================
# 🧠 HISTORIAL (CHAT)
# ==========================================

ROLES_VALIDOS = {"user", "assistant", "system"}


def _validar_historial(data) -> List[Dict[str, str]]:

    if not isinstance(data, list):

        return []

    limpio = []

    for m in data:

        if isinstance(m, dict):

            role = m.get("role")
            content = m.get("content")

            if role in ROLES_VALIDOS and content:

                limpio.append({
                    "role": str(role),
                    "content": str(content)
                })

    return limpio


historial: List[Dict[str, str]] = _validar_historial(
    _leer_json_seguro(ARCHIVO_MEMORIA, [])
)


def agregar_mensaje(rol: str, contenido: str):

    if not contenido:

        return

    if rol not in ROLES_VALIDOS:

        rol = "user"

    historial.append({
        "role": rol,
        "content": str(contenido)
    })

    limitar_historial()

    guardar_historial()


def obtener_historial():

    return list(historial)


def limitar_historial():

    global historial

    if len(historial) > MAX_HISTORIAL:

        historial = historial[-MAX_HISTORIAL:]


def guardar_historial():

    _escritura_atomica(ARCHIVO_MEMORIA, historial)


def limpiar_historial():

    historial.clear()

    guardar_historial()


# ==========================================
# 📌 PENDIENTES - DELEGADO A database/db_manager
# ==========================================

# ⚠️ IMPORTANTE: Las funciones de pendientes se han movido a:
# database/db_manager.py
# 
# Para mantener consistencia de datos, SIEMPRE usa:
#   from database.db_manager import agregar_pendiente, obtener_pendientes
#
# Este módulo (memory.py) SOLO gestiona el historial de chat
# Los pendientes son responsabilidad de database/db_manager.py