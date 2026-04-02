import os

# ============================================
# CARGAR API KEY — LOCAL O STREAMLIT CLOUD
# ============================================
try:
    import streamlit as st
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
    PASSWORD = st.secrets.get("PASSWORD", "tenshi2026")
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    PASSWORD = os.getenv("PASSWORD", "tenshi2026")

# ============================================
# RUTAS BASE DEL PROYECTO
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATHS = {
    "memory":  os.path.join(BASE_DIR, "memory"),
    "logs":    os.path.join(BASE_DIR, "logs"),
    "sandbox": os.path.join(BASE_DIR, "sandbox"),
    "modules": os.path.join(BASE_DIR, "modules"),
}
for ruta in PATHS.values():
    os.makedirs(ruta, exist_ok=True)

# ============================================
# APIS
# ============================================
APIS = {}
if GROQ_API_KEY:
    APIS["groq"] = {
        "api_key": GROQ_API_KEY,
        "model":   "llama-3.1-8b-instant",
        "activa":  True,
        "priority": 1,
    }
else:
    APIS["groq"] = {
        "api_key": None,
        "model":   "llama-3.1-8b-instant",
        "activa":  False,
        "priority": 1,
    }

# ============================================
# MODELOS
# ============================================
MODELOS = {
    "principal": "llama-3.1-8b-instant",
    "fallback":  "llama3-70b-8192",
}

# ============================================
# IDENTIDAD
# ============================================
AI_CONFIG = {
    "name":    "TENSHI",
    "creator": "Angel",
    "version": "0.2",
}

# ============================================
# CONFIGURACIÓN DEL MODELO
# ============================================
MODEL_CONFIG = {
    "temperature": 0.7,
    "max_tokens":  1024,
}

# ============================================
# PERSONALIDAD
# ============================================
PERSONALIDAD = """
Eres TENSHI, un asistente inteligente creado por Angel.
Tu propósito es ayudar a resolver problemas, programar,
explicar conceptos y asistir en tareas técnicas.
Eres claro, directo, útil y preciso.
Cuando el usuario te pida crear un módulo o programarte algo nuevo,
usa el módulo self_coder para generarlo y consultarle antes de guardar.
"""

# ============================================
# VALIDACIÓN
# ============================================
def validar_config():
    errores = []
    if not GROQ_API_KEY:
        errores.append("Falta GROQ_API_KEY en .env o Streamlit Secrets")
    return errores

ERRORES_CONFIG = validar_config()
if ERRORES_CONFIG:
    print("\n⚠️ CONFIGURACIÓN INCOMPLETA")
    for e in ERRORES_CONFIG:
        print("-", e)
else:
    print("\n✅ Configuración cargada correctamente\n")