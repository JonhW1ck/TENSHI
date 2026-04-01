import os
from dotenv import load_dotenv


# ============================================
# CARGAR VARIABLES DE ENTORNO
# ============================================

load_dotenv()


# ============================================
# RUTAS BASE DEL PROYECTO
# ============================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATHS = {
    "memory": os.path.join(BASE_DIR, "memory"),
    "logs": os.path.join(BASE_DIR, "logs"),
    "sandbox": os.path.join(BASE_DIR, "sandbox"),
}

# Crear carpetas automáticamente
for ruta in PATHS.values():
    os.makedirs(ruta, exist_ok=True)


# ============================================
# API KEYS (DESDE .env)
# ============================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ============================================
# CONFIGURACIÓN DE APIS
# ============================================

APIS = {}

# Activar Groq solo si existe la key
if GROQ_API_KEY:

    APIS["groq"] = {
        "api_key": GROQ_API_KEY,
        "model": "llama-3.1-8b-instant",
        "activa": True,
        "priority": 1
    }

else:

    APIS["groq"] = {
        "api_key": None,
        "model": "llama-3.1-8b-instant",
        "activa": False,
        "priority": 1
    }


# ============================================
# MODELOS
# ============================================

MODELOS = {
    "principal": "llama-3.1-8b-instant",
    "fallback": "llama3-70b-8192"
}


# ============================================
# IDENTIDAD DEL ASISTENTE
# ============================================

AI_CONFIG = {
    "name": "TENSHI",
    "creator": "Angel",
    "version": "0.1"
}


# ============================================
# CONFIGURACIÓN DEL MODELO
# ============================================

MODEL_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 1024
}


# ============================================
# PERSONALIDAD DE TENSHI
# ============================================

PERSONALIDAD = """
Eres TENSHI, un asistente inteligente creado por Angel.

Tu propósito es ayudar a resolver problemas, programar,
explicar conceptos y asistir en tareas técnicas.

Eres claro, directo, útil y preciso.
"""


# ============================================
# VALIDACIÓN DE CONFIGURACIÓN
# ============================================

def validar_config():

    errores = []

    if not GROQ_API_KEY:
        errores.append("Falta GROQ_API_KEY en el archivo .env")

    return errores


ERRORES_CONFIG = validar_config()

if ERRORES_CONFIG:

    print("\n⚠️ CONFIGURACIÓN INCOMPLETA ⚠️")

    for e in ERRORES_CONFIG:
        print("-", e)

    print()

else:

    print("\n✅ Configuración cargada correctamente\n")