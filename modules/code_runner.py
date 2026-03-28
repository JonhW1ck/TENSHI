# Módulo de ejecución de código de TENSHI

import subprocess
import sys
import tempfile
import os

def ejecutar_codigo(codigo):
    """Escribe y ejecuta código Python, devuelve el resultado."""
    try:
        # Crear archivo temporal con el código
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as f:
            f.write(codigo)
            ruta_temp = f.name

        # Ejecutar el archivo temporal
        resultado = subprocess.run(
            [sys.executable, ruta_temp],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Limpiar archivo temporal
        os.unlink(ruta_temp)

        if resultado.returncode == 0:
            return f"✅ Resultado:\n{resultado.stdout}"
        else:
            return f"❌ Error:\n{resultado.stderr}"

    except subprocess.TimeoutExpired:
        return "❌ El código tardó demasiado y fue cancelado."
    except Exception as e:
        return f"❌ Error al ejecutar: {e}"
    