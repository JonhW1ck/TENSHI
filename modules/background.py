# Módulo de tareas en segundo plano de TENSHI

import threading
import time

tareas_activas = {}

def ejecutar_en_segundo_plano(nombre_tarea, funcion, *args):
    """Ejecuta una función en un hilo separado."""

    resultado = {"estado": "ejecutando", "resultado": None, "error": None}
    tareas_activas[nombre_tarea] = resultado

    def hilo():
        try:
            print(f"⚙️ Tarea '{nombre_tarea}' iniciada...")
            resultado["resultado"] = funcion(*args)
            resultado["estado"] = "completada"
            print(f"✅ Tarea '{nombre_tarea}' completada.")
        except Exception as e:
            resultado["estado"] = "error"
            resultado["error"] = str(e)
            print(f"❌ Tarea '{nombre_tarea}' falló: {e}")

    hilo_thread = threading.Thread(target=hilo, daemon=True)
    hilo_thread.start()
    return nombre_tarea

def obtener_estado(nombre_tarea):
    """Consulta el estado de una tarea."""
    if nombre_tarea in tareas_activas:
        return tareas_activas[nombre_tarea]
    return {"estado": "no encontrada", "resultado": None, "error": None}

def listar_tareas():
    """Lista todas las tareas activas."""
    return {k: v["estado"] for k, v in tareas_activas.items()}