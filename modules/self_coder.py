# ==========================================
# MÓDULO DE AUTO-PROGRAMACIÓN DE TENSHI
# self_coder.py
# ==========================================
import os
import re
import json
import importlib.util
from datetime import datetime
from groq import Groq
from config import APIS, PERSONALIDAD, BASE_DIR, MODEL_CONFIG


# ==========================================
# OBTENER CLIENTE
# ==========================================
def obtener_cliente():
    for nombre, datos in APIS.items():
        if datos.get("activa") and datos.get("api_key"):
            return Groq(api_key=datos["api_key"]), datos["model"]
    raise Exception("No hay APIs disponibles.")


# ==========================================
# LIMPIAR CÓDIGO — backticks y dunders
# ==========================================
def limpiar_codigo(codigo: str) -> str:
    # Quitar backticks si el modelo los incluyó
    if codigo.startswith("```"):
        codigo = codigo.split("\n", 1)[1] if "\n" in codigo else ""
    if codigo.endswith("```"):
        codigo = codigo.rsplit("```", 1)[0]
    codigo = codigo.strip()

    # Corregir dunders mal escritos por Groq (_name_ → __name__)
    dunders = [
        "name", "main", "init", "dict", "str", "repr",
        "len", "call", "class", "doc", "file", "all",
        "iter", "next", "enter", "exit", "get", "set",
    ]
    for d in dunders:
        # Solo reemplaza si tiene exactamente UN guión a cada lado
        codigo = re.sub(rf'(?<![_])_{d}_(?![_])', f'__{d}__', codigo)

    return codigo


# ==========================================
# GENERAR CÓDIGO CON GROQ
# ==========================================
def generar_codigo(instruccion: str) -> str:
    cliente, modelo = obtener_cliente()
    prompt = f"""
Eres un experto programador Python. El usuario quiere que TENSHI se auto-programe.

Instrucción: {instruccion}

Genera un módulo Python completo, funcional y bien comentado.
El módulo debe:
- Tener funciones claras con nombres descriptivos en español
- Incluir manejo de errores con try/except
- Ser compatible con el resto del proyecto TENSHI
- No usar librerías externas que no estén en requirements.txt
- Incluir un bloque if __name__ == "__main__" con ejemplos de uso
- Usar SIEMPRE doble guión bajo en métodos especiales: __init__, __main__, __name__, __dict__

Responde SOLO con el código Python puro. Sin explicaciones, sin markdown, sin bloques de código.
"""
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": PERSONALIDAD},
            {"role": "user",   "content": prompt}
        ],
        max_tokens=MODEL_CONFIG.get("max_tokens_code", 4096),
        temperature=0.3
    )
    codigo = respuesta.choices[0].message.content.strip()
    return limpiar_codigo(codigo)


# ==========================================
# EXTRAER NOMBRE DEL MÓDULO
# ==========================================
def extraer_nombre_modulo(instruccion: str) -> str:
    cliente, modelo = obtener_cliente()
    prompt = f"""
De esta instrucción: "{instruccion}"
Extrae un nombre corto en snake_case para el archivo Python.
Ejemplo: "módulo de búsqueda web" → "buscador_web"
Responde SOLO con el nombre sin extensión .py
"""
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=30,
        temperature=0.1
    )
    nombre = respuesta.choices[0].message.content.strip()
    nombre = "".join(c for c in nombre if c.isalnum() or c == "_")
    return nombre or "modulo_nuevo"


# ==========================================
# GUARDAR LOG DE AUTO-MEJORAS
# ==========================================
def guardar_log_mejora(nombre: str, instruccion: str, estado: str):
    ruta_log = os.path.join(BASE_DIR, "logs", "self_improvements.json")
    try:
        if os.path.exists(ruta_log):
            with open(ruta_log, "r", encoding="utf-8") as f:
                log = json.load(f)
        else:
            log = []
        log.append({
            "fecha":       datetime.now().isoformat(),
            "nombre":      nombre,
            "instruccion": instruccion,
            "estado":      estado,
        })
        with open(ruta_log, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ Error guardando log: {e}")


# ==========================================
# GUARDAR E IMPORTAR MÓDULO + COMMIT GITHUB
# ==========================================
def guardar_modulo(nombre: str, codigo: str) -> str:
    ruta = os.path.join(BASE_DIR, "modules", f"{nombre}.py")
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(codigo)

        spec = importlib.util.spec_from_file_location(nombre, ruta)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)

        try:
            from modules.github_sync import commit_modulo
            resultado_git = commit_modulo(nombre, codigo)
            git_msg = resultado_git.get("mensaje", "")
        except Exception as e:
            git_msg = f"⚠️ GitHub sync falló: {e}"

        guardar_log_mejora(nombre, nombre, "guardado_ok")
        return (
            f"✅ Módulo '{nombre}.py' creado e importado correctamente.\n"
            f"{git_msg}"
        )
    except Exception as e:
        guardar_log_mejora(nombre, nombre, f"error: {str(e)}")
        return f"⚠️ Módulo guardado pero hubo error al importarlo: {e}"


# ==========================================
# FUNCIÓN PRINCIPAL
# ==========================================
def auto_programar(instruccion: str) -> dict:
    try:
        print(f"\n🤖 [self_coder] Procesando: {instruccion}")
        nombre = extraer_nombre_modulo(instruccion)
        codigo = generar_codigo(instruccion)
        guardar_log_mejora(nombre, instruccion, "pendiente_confirmacion")
        return {
            "nombre":                 nombre,
            "codigo":                 codigo,
            "pendiente_confirmacion": True,
        }
    except Exception as e:
        return {
            "nombre":                 "error",
            "codigo":                 "",
            "pendiente_confirmacion": False,
            "error":                  str(e),
        }


def confirmar_guardado(nombre: str, codigo: str) -> str:
    return guardar_modulo(nombre, codigo)

