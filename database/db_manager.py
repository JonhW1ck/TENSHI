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

        os.replace(tmp_path, ruta)

    except Exception as e:

        print("⚠️ Error en escritura atómica:", e)


# ==========================================
# � CARGAR DATOS
# ==========================================

def cargar_pendientes():
    """
    Carga los recordatorios de forma segura.
    ⚠️ SIEMPRE LEE DEL ARCHIVO - NO USA CACHÉ EN MEMORIA
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
    """
    Agrega un nuevo pendiente al archivo.
    ⚠️ SIEMPRE LEE ANTES Y DESPUÉS para garantizar consistencia
    """

    texto = str(texto).strip()

    if not texto:
        return

    # 🔍 DEBUG: Antes de guardar
    print(f"\n{'='*70}")
    print(f"📝 [db_manager.agregar_pendiente()]")
    print(f"   Texto: '{texto}'")
    print(f"   Fecha: {fecha}")
    
    # Leer estado actual
    pendientes = cargar_pendientes()
    print(f"   Pendientes ANTES de agregar: {len(pendientes)}")

    nuevo = {
        "id": str(uuid.uuid4()),
        "texto": texto,
        "fecha": fecha,
        "estado": "pendiente",
        "creado_en": datetime.now().isoformat()
    }

    pendientes.append(nuevo)
    print(f"   ✅ Agregado a lista (ID: {nuevo['id']})")

    # Guardar al archivo
    guardar_pendientes(pendientes)
    print(f"   💾 Guardado en: {os.path.abspath(DB_PATH)}")

    # Verificar que se guardó
    pendientes_verificacion = cargar_pendientes()
    print(f"   ✓ Verificación DESPUÉS de guardar: {len(pendientes_verificacion)}")
    print(f"{'='*70}\n")
    
    return nuevo


# ==========================================
# 📤 OBTENER PENDIENTES ACTIVOS
# ==========================================

def obtener_pendientes():
    """
    Obtiene SOLO los pendientes activos del archivo.
    ⚠️ SIEMPRE LEE DEL ARCHIVO - NO USA CACHÉ
    """

    pendientes = cargar_pendientes()
    
    # 🔍 DEBUG: Mostrar ruta exacta y contenido
    print(f"\n{'='*70}")
    print(f"📂 [db_manager.obtener_pendientes()]")
    print(f"   📁 Ruta absoluta: {os.path.abspath(DB_PATH)}")
    print(f"   📊 Total en archivo: {len(pendientes)}")
    print(f"   📋 Contenido:")
    for i, p in enumerate(pendientes, 1):
        estado = p.get("estado", "?")
        texto = p.get("texto", "?")
        fecha = p.get("fecha", "sin fecha")
        print(f"      {i}. [{estado}] {texto} (fecha: {fecha})")
    
    # Filtrar solo pendientes activos
    resultado = [
        p for p in pendientes
        if p.get("estado") == "pendiente"
    ]
    
    print(f"   ✅ Pendientes activos: {len(resultado)}")
    print(f"{'='*70}\n")
    
    return resultado


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


# ==========================================
# 🧪 LIMPIAR DATOS DE PRUEBA
# ==========================================

def limpiar_test_data():
    """
    Elimina pendientes con texto de prueba (TEST, Hacer tareas, etc.)
    """
    
    pendientes = cargar_pendientes()
    
    # Palabras que indican datos de prueba
    palabras_test = ["TEST", "PRUEBA", "Hacer tareas"]
    
    # Filtrar pendientes que NO sean de prueba
    activos = [
        p for p in pendientes
        if not any(palabra in p.get("texto", "") for palabra in palabras_test)
    ]
    
    if len(activos) < len(pendientes):
        print(f"\n🧹 Limpieza de datos de prueba:")
        print(f"   Antes: {len(pendientes)} pendientes")
        print(f"   Después: {len(activos)} pendientes")
        print(f"   Eliminados: {len(pendientes) - len(activos)}")
        guardar_pendientes(activos)
        print(f"✅ Datos de prueba limpiados\n")
    else:
        print(f"\n✅ No hay datos de prueba para limpiar\n")