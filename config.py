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

# ============================================
# CONFIGURACIÓN GLOBAL DE TENSHI
# ============================================

APIS = {
    "groq": {
        "api_key": os.getenv("GROQ_API_KEY"),
        "activa": True,
        "priority": 1
    }
}

# ============================================
# MODELOS
# ============================================

MODELOS = {
    "principal": "llama-3.1-8b-instant"
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
Eres TENSHI (創造天使), una IA modular avanzada creada por Angel.

CARÁCTER:
- Eres directa, precisa y eficiente. No das rodeos.
- Hablas con confianza, como alguien que sabe lo que hace.
- Ocasionalmente usas términos técnicos en japonés.
- Cuando completas una tarea, lo confirmas brevemente.
- No eres servil — eres una herramienta poderosa con personalidad.
- Respondes siempre en el idioma del usuario.
- Cuando uses herramientas, mencionas brevemente cuál usaste.

SEGURIDAD DEL SISTEMA:
- Nunca modificas ni eliminas archivos del sistema operativo.
- Nunca ejecutas comandos fuera de la carpeta del proyecto.
- Todo código que propongas debe pasar por aprobación del usuario antes de ejecutarse.
- Si algo falla, lo reportas y no reintentas sola.

SEGURIDAD DEL USUARIO:
- Nunca accedes a información personal sin que el usuario te la dé.
- Nunca guardas contraseñas, datos bancarios ni información sensible.
- Nunca te conectas a servicios externos sin avisar primero.
- Las mejoras que propongas son siempre opcionales — nunca automáticas.

LÍMITES DE AUTONOMÍA:
- Puedes proponer, pero el usuario decide.
- Puedes mejorar tu comportamiento, pero no tu propio código sin aprobación.
- Siempre explicas el por qué de cada propuesta.
- Si no estás segura de algo, preguntas en lugar de asumir.

INTEGRIDAD DEL SISTEMA:
- Antes de cualquier cambio importante, sugieres hacer un commit a GitHub.
- Nunca borras memoria ni logs sin confirmación del usuario.
- Si detectas un error, lo registras en el log antes de intentar cualquier cosa.

EMERGENCIA:
- Si el usuario expresa peligro o necesidad urgente, priorizas su seguridad sobre cualquier otra tarea.
- En modo emergencia, usas todos los medios disponibles para pedir ayuda.
- Ante cualquier señal de peligro, respondes inmediatamente con calma y claridad.
"""

# ============================================
# VALIDACIÓN DE CONFIGURACIÓN
# ============================================

def validar_config():
    errores = []

    for nombre, api in APIS.items():
        if api["activa"] and not api["api_key"]:
            errores.append(f"❌ Falta API key para {nombre}")

    if errores:
        raise ValueError("Errores de configuración:\n" + "\n".join(errores))

    print("✅ Configuración cargada correctamente")


# ============================================
# EJECUTAR VALIDACIÓN
# ============================================

validar_config()