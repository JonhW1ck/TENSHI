# ==========================================
# MÓDULO DE EJECUCIÓN DE CÓDIGO — TENSHI
# code_runner.py
# ==========================================
import subprocess
import sys
import tempfile
import os
import json
from memory.stats import incrementar


def ejecutar_codigo(codigo: str) -> dict:
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py",
            delete=False, encoding="utf-8"
        ) as f:
            f.write(codigo)
            ruta_temp = f.name

        resultado = subprocess.run(
            [sys.executable, ruta_temp],
            capture_output=True,
            text=True,
            timeout=10
        )
        os.unlink(ruta_temp)
        incrementar("codigos_ejecutados")

        if resultado.returncode == 0:
            return {
                "exito":  True,
                "output": resultado.stdout.strip() or "(sin output)",
                "error":  "",
                "codigo": codigo,
            }
        else:
            return {
                "exito":  False,
                "output": "",
                "error":  resultado.stderr.strip(),
                "codigo": codigo,
            }

    except subprocess.TimeoutExpired:
        return {"exito": False, "output": "", "error": "Timeout — el código tardó más de 10 segundos.", "codigo": codigo}
    except Exception as e:
        return {"exito": False, "output": "", "error": str(e), "codigo": codigo}


def verificar_output(codigo: str, output: str) -> dict:
    try:
        from groq import Groq
        from config import APIS, PERSONALIDAD, MODEL_CONFIG

        cliente = None
        modelo  = None
        for _, datos in APIS.items():
            if datos.get("activa") and datos.get("api_key"):
                cliente = Groq(api_key=datos["api_key"])
                modelo  = datos["model"]
                break

        if not cliente:
            return {"valido": True, "razon": "No se pudo verificar."}

        prompt = f"""
Eres un verificador de resultados de código Python.

Se ejecutó este código:
{codigo}

Y produjo este output:
{output}

Analiza si el output tiene sentido dado lo que hace el código.
NO uses conocimiento externo, solo analiza si el código podría producir ese output.
Detecta si hay datos inventados, valores imposibles o inconsistencias obvias.

Responde SOLO en este formato JSON sin backticks ni markdown:
{{"valido": true, "razon": "..."}}
"""
        respuesta = cliente.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Eres un verificador de outputs de código Python. Responde solo en JSON puro sin backticks."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=MODEL_CONFIG.get("max_tokens_verify", 200),
            temperature=0.1
        )
        texto = respuesta.choices[0].message.content.strip()

        # Limpiar backticks de forma más robusta
        texto = texto.replace("```json", "").replace("```", "").strip()

        resultado = json.loads(texto)
        return resultado

    except Exception as e:
        print(f"⚠️ Error en verificar_output: {e}")
        return {"valido": True, "razon": "No se pudo verificar."}


def ejecutar_modulo(nombre_modulo: str) -> dict:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(base_dir, "modules", f"{nombre_modulo}.py")

    if not os.path.exists(ruta):
        return {
            "exito": False,
            "output": "",
            "error": f"Módulo '{nombre_modulo}.py' no encontrado en modules/",
            "codigo": "",
        }

    with open(ruta, "r", encoding="utf-8") as f:
        codigo = f.read()

    resultado = ejecutar_codigo(codigo)

    if resultado["exito"] and resultado["output"] != "(sin output)":
        verificacion = verificar_output(codigo, resultado["output"])
        resultado["verificado"] = verificacion["valido"]
        resultado["verificacion_razon"] = verificacion["razon"]
        if not verificacion["valido"]:
            resultado["output"] += f"\n\n⚠️ **Advertencia:** {verificacion['razon']}"
    else:
        resultado["verificado"] = None
        resultado["verificacion_razon"] = ""

    return resultado


def autocorregir(codigo: str, error: str) -> str:
    try:
        from groq import Groq
        from config import APIS, PERSONALIDAD, MODEL_CONFIG

        cliente = None
        modelo  = None
        for _, datos in APIS.items():
            if datos.get("activa") and datos.get("api_key"):
                cliente = Groq(api_key=datos["api_key"])
                modelo  = datos["model"]
                break

        if not cliente:
            return codigo

        prompt = f"""
Eres un experto programador Python.
El siguiente código tiene un error. Corrígelo.

CÓDIGO:
{codigo}

ERROR:
{error}

Devuelve SOLO el código Python corregido.
Sin explicaciones, sin markdown, sin bloques de código.
"""
        respuesta = cliente.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": PERSONALIDAD},
                {"role": "user",   "content": prompt}
            ],
            max_tokens=MODEL_CONFIG.get("max_tokens_code", 4096),
            temperature=0.2
        )
        codigo_corregido = respuesta.choices[0].message.content.strip()

        if codigo_corregido.startswith("```"):
            codigo_corregido = codigo_corregido.split("\n", 1)[1] if "\n" in codigo_corregido else ""
        if codigo_corregido.endswith("```"):
            codigo_corregido = codigo_corregido.rsplit("```", 1)[0]

        return codigo_corregido.strip()

    except Exception as e:
        print(f"⚠️ Error en autocorregir: {e}")
        return codigo


def ejecutar_y_corregir(codigo: str, nombre_modulo: str = "", intentos: int = 2) -> dict:
    codigo_actual = codigo
    corregido     = False

    for intento in range(intentos):
        resultado = ejecutar_codigo(codigo_actual)

        if resultado["exito"]:
            if corregido and nombre_modulo:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                ruta = os.path.join(base_dir, "modules", f"{nombre_modulo}.py")
                try:
                    with open(ruta, "w", encoding="utf-8") as f:
                        f.write(codigo_actual)
                    try:
                        from modules.github_sync import commit_modulo
                        commit_modulo(nombre_modulo, codigo_actual)
                    except Exception:
                        pass
                except Exception:
                    pass

            return {
                "exito":        True,
                "output":       resultado["output"],
                "error":        "",
                "codigo_final": codigo_actual,
                "corregido":    corregido,
                "intentos":     intento + 1,
            }

        if intento < intentos - 1:
            print(f"⚠️ Intento {intento+1} falló, autocorrigiendo...")
            codigo_actual = autocorregir(codigo_actual, resultado["error"])
            corregido     = True

    return {
        "exito":        False,
        "output":       "",
        "error":        resultado["error"],
        "codigo_final": codigo_actual,
        "corregido":    corregido,
        "intentos":     intentos,
    }