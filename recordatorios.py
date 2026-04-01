print("🔥 recordatorios cargando...")

# ==========================================
# 📦 IMPORTS
# ==========================================

import json
import os
import threading
from datetime import datetime, timezone


# ==========================================
# ⚙️ CONFIGURACIÓN
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MEMORY_DIR = os.path.join(BASE_DIR, "memory")
MEMORY_PATH = os.path.join(MEMORY_DIR, "historial.json")
BACKUP_PATH = os.path.join(MEMORY_DIR, "historial_backup.json")

lock = threading.Lock()
MAX_HISTORIAL = 100

# Asegurar carpeta
os.makedirs(MEMORY_DIR, exist_ok=True)


# ==========================================
# 📥 CARGAR HISTORIAL
# ==========================================

def cargar_historial():
    """
    Carga el historial de forma robusta con fallback.
    """

    if not os.path.exists(MEMORY_PATH):
        return []

    with lock:
        try:

            with open(MEMORY_PATH, "r", encoding="utf-8", errors="replace") as f:
                data = json.load(f)

            if isinstance(data, list):
                return data

            return []

        except Exception:

            print("⚠️ Historial corrupto. Intentando recuperar backup...")

            if os.path.exists(BACKUP_PATH):

                try:
                    with open(BACKUP_PATH, "r", encoding="utf-8", errors="replace") as f:
                        data = json.load(f)

                    if isinstance(data, list):
                        return data

                except Exception:
                    pass

            return []


# ==========================================
# 💾 GUARDAR HISTORIAL (ATÓMICO)
# ==========================================

def guardar_historial(historial):
    """
    Guarda el historial de forma segura y atómica.
    """

    with lock:

        temp_path = MEMORY_PATH + ".tmp"

        # Guardar primero en temporal
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=2, ensure_ascii=False)

        # Backup previo
        if os.path.exists(MEMORY_PATH):
            os.replace(MEMORY_PATH, BACKUP_PATH)

        # Reemplazo atómico
        os.replace(temp_path, MEMORY_PATH)


# ==========================================
# ➕ AGREGAR MENSAJE
# ==========================================

def agregar_mensaje(role, content):
    """
    Agrega un mensaje validado al historial.
    """

    if role not in {"user", "assistant", "system"}:
        raise ValueError("Rol inválido")

    if not isinstance(content, str) or not content.strip():
        raise ValueError("Contenido inválido")

    historial = cargar_historial()

    nuevo = {
        "role": role,
        "content": content.strip(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    historial.append(nuevo)

    # Limitar tamaño
    if len(historial) > MAX_HISTORIAL:
        historial = historial[-MAX_HISTORIAL:]

    guardar_historial(historial)


# ==========================================
# 📤 OBTENER HISTORIAL
# ==========================================

def obtener_historial():
    return cargar_historial()


# ==========================================
# 🧹 LIMPIAR HISTORIAL
# ==========================================

def limpiar_historial():
    guardar_historial([])


# ==========================================
# 🔎 OBTENER ÚLTIMOS MENSAJES
# ==========================================

def obtener_ultimos(n=10):

    historial = cargar_historial()

    if not isinstance(n, int) or n <= 0:
        return []

    return historial[-n:]


print("🔥 recordatorios cargado OK")