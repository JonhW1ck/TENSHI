# ==========================================
# 📜 MÓDULO DE LOGS DE TENSHI (ROBUSTO)
# ==========================================

import os
import threading
from datetime import datetime


# ==========================================
# ⚙️ CONFIGURACIÓN
# ==========================================

CARPETA_LOGS = "logs"
os.makedirs(CARPETA_LOGS, exist_ok=True)

_lock = threading.Lock()

# Tamaño máximo del archivo (1 MB)
MAX_LOG_SIZE = 1_000_000


# ==========================================
# 🔧 UTILIDADES
# ==========================================

def _sanitizar(texto: str) -> str:
    if texto is None:
        return ""

    texto = str(texto)
    texto = texto.replace("\n", " ").replace("\r", " ")

    return texto.strip()


def _obtener_archivo_log() -> str:
    hoy = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(CARPETA_LOGS, f"tenshi_{hoy}.txt")


def _rotar_log_si_necesario(ruta):
    """
    Evita que el log crezca indefinidamente.
    """

    if os.path.exists(ruta) and os.path.getsize(ruta) > MAX_LOG_SIZE:
        nuevo_nombre = ruta.replace(".txt", "_old.txt")
        os.rename(ruta, nuevo_nombre)


# ==========================================
# 💾 FUNCIÓN PRINCIPAL
# ==========================================

def guardar_log(rol: str, mensaje: str, nivel="INFO"):
    """
    Guarda un log estructurado.

    Formato:
    [HH:MM:SS] [NIVEL] ROL: mensaje
    """

    try:
        archivo = _obtener_archivo_log()
        hora = datetime.now().strftime("%H:%M:%S")

        rol = _sanitizar(rol).upper()
        mensaje = _sanitizar(mensaje)
        nivel = _sanitizar(nivel).upper()

        linea = f"[{hora}] [{nivel}] {rol}: {mensaje}\n"
        separador = "-" * 60 + "\n"

        with _lock:
            _rotar_log_si_necesario(archivo)

            with open(archivo, "a", encoding="utf-8") as f:
                f.write(linea)
                f.write(separador)

    except Exception as e:
        print("⚠️ error guardando log:", e)