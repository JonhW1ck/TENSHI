# ==========================================
# 📦 IMPORTS
# ==========================================

import json
import os
import uuid
import threading
import tempfile
import shutil
from datetime import datetime


# ==========================================
# ⚙️ CONFIGURACIÓN
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEMORY_DIR = os.path.join(BASE_DIR, "memory")
os.makedirs(MEMORY_DIR, exist_ok=True)

DB_PATH = os.path.join(MEMORY_DIR, "pendientes.json")

# 🔒 Control de concurrencia
lock = threading.Lock()


# ==========================================
# 🔒 ESCRITURA ATÓMICA
# ==========================================

def escritura_atomica(ruta, data):

    try:

        fd, tmp_path = tempfile.mkstemp(dir=MEMORY_DIR)

        with os.fdopen(fd, "w", encoding="utf-8") as tmp:

            json.dump(data, tmp, indent=4, ensure_ascii=False)

        shutil.replace(tmp_path, ruta)

    except Exception as e:

        print("⚠️ Error en escritura atómica:", e)


# ==========================================
# 📥 CARGAR DATOS
# ==========================================

def cargar_pendientes():
    """
    Carga los recordatorios de forma segura.
    """

    with lock:

        if not os.path.exists(DB_PATH):

            escritura_atomica(DB_PATH, [])
            return []

        try:

            with open(DB_PATH, "r", encoding="utf-8") as f:

                data = json.load(f)

                if isinstance(data, list):
                    return data

                return []

        except json.JSONDecodeError:

            print("⚠️ JSON corrupto — reiniciando pendientes")

            escritura_atomica(DB_PATH, [])

            return []


# ==========================================
# 💾 GUARDAR DATOS
# ==========================================

def guardar_pendientes(lista):

    with lock:

        escritura_atomica(DB_PATH, lista)


# ==========================================
# ➕ AGREGAR RECORDATORIO
# ==========================================

def agregar_pendiente(texto, fecha=None):

    texto = str(texto).strip()

    if not texto:
        return

    pendientes = cargar_pendientes()

    nuevo = {

        "id": str(uuid.uuid4()),

        "texto": texto,

        "fecha": fecha,

        "estado": "pendiente",

        "creado_en": datetime.now().isoformat()

    }

    pendientes.append(nuevo)

    guardar_pendientes(pendientes)


# ==========================================
# 📤 OBTENER PENDIENTES ACTIVOS
# ==========================================

def obtener_pendientes():

    pendientes = cargar_pendientes()

    return [

        p for p in pendientes

        if p.get("estado") == "pendiente"

    ]


# ==========================================
# 📋 OBTENER TODOS
# ==========================================

def obtener_todos():

    return cargar_pendientes()


# ==========================================
# ✅ MARCAR COMO HECHO
# ==========================================

def marcar_como_hecho(recordatorio_id):

    pendientes = cargar_pendientes()

    for p in pendientes:

        if p.get("id") == recordatorio_id:

            p["estado"] = "hecho"

            p["completado_en"] = datetime.now().isoformat()

    guardar_pendientes(pendientes)


# ==========================================
# ❌ ELIMINAR RECORDATORIO
# ==========================================

def eliminar_pendiente(recordatorio_id):

    pendientes = cargar_pendientes()

    pendientes = [

        p for p in pendientes

        if p.get("id") != recordatorio_id

    ]

    guardar_pendientes(pendientes)


# ==========================================
# 🧹 LIMPIAR COMPLETADOS
# ==========================================

def limpiar_completados():

    pendientes = cargar_pendientes()

    activos = [

        p for p in pendientes

        if p.get("estado") != "hecho"

    ]

    guardar_pendientes(activos)