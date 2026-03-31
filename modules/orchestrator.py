# Orquestador de TENSHI (CEREBRO REAL)

from groq import Groq
from config import APIS, MODELOS, MODEL_CONFIG, PERSONALIDAD

from memory.memory import (
    agregar_mensaje,
    obtener_historial,
    agregar_pendiente,
    obtener_pendientes
)

from logs.logger import guardar_log
from memory.stats import incrementar

from tools.tool_runner import buscar_en_internet, leer_archivo, escribir_archivo
from modules.code_runner import ejecutar_codigo
from modules.vision import analizar_imagen
from modules.planner import construir_plan
from modules.reasoning import construir_razonamiento

MAX_HISTORY = 8


# ==========================================
# CLIENTE API
# ==========================================

def obtener_cliente():
    for nombre, datos in APIS.items():
        if datos["activa"]:
            try:
                cliente = Groq(api_key=datos["api_key"])
                modelo = MODELOS["principal"]
                print(f"✅ API: {nombre} | modelo {modelo}")
                return cliente, modelo
            except Exception as e:
                print(f"❌ {nombre} falló:", e)
    raise Exception("No hay APIs disponibles")


# ==========================================
# INTENCIÓN (CEREBRO)
# ==========================================

def detectar_intencion(mensaje):
    m = mensaje.lower()

    # VIDA REAL
    if any(p in m for p in ["pendiente","tarea","recuerda","recordar"]):
        return "memoria"

    if any(p in m for p in ["qué tengo que hacer","mis pendientes","tareas"]):
        return "consultar_pendientes"

    # SISTEMA
    if any(ext in m for ext in [".jpg",".png",".jpeg",".webp",".gif"]):
        return "vision"

    if any(p in m for p in ["busca","investiga","noticias","precio","clima"]):
        return "internet"

    if any(ext in m for ext in [".txt",".py",".json",".csv",".md"]):
        if any(p in m for p in ["lee","abre","muestra"]):
            return "leer_archivo"
        if any(p in m for p in ["guarda","crear","escribe"]):
            return "escribir_archivo"

    if any(p in m for p in ["codigo","script","programa","ejecuta"]):
        return "codigo"

    return "chat"


# ==========================================
# EXTRACTORES
# ==========================================

def extraer_ruta(mensaje):
    for p in mensaje.split():
        if any(ext in p for ext in [".txt",".py",".json",".csv",".md"]):
            return p.strip("\"',")
    return None


def extraer_imagen(mensaje):
    for p in mensaje.split():
        if any(ext in p for ext in [".jpg",".png",".jpeg",".webp",".gif"]):
            return p.strip("\"',")
    return None


# ==========================================
# RESPUESTA PRINCIPAL
# ==========================================

def responder(mensaje_usuario):

    cliente, modelo = obtener_cliente()
    intencion = detectar_intencion(mensaje_usuario)

    # ======================================
    # MEMORIA INTELIGENTE
    # ======================================

    if intencion == "memoria":

        agregar_pendiente(mensaje_usuario)

        respuesta = "📌 Guardado como pendiente."

        agregar_mensaje("assistant", respuesta)

        guardar_log("tenshi", respuesta)

        return respuesta


    if intencion == "consultar_pendientes":

        pendientes = obtener_pendientes()

        if not pendientes:
            return "📋 No tienes pendientes registrados."

        texto = "📋 Tus pendientes:\n\n"

        for i, p in enumerate(pendientes, 1):
            estado = "✅" if p.get("completado") else "⏳"
            texto += f"{i}. {estado} {p['texto']}\n"

        agregar_mensaje("assistant", texto)

        return texto


    mensajes = [{"role":"system","content":PERSONALIDAD}]

    # ======================================
    # EJECUCIÓN DIRECTA
    # ======================================

    if intencion == "vision":
        ruta = extraer_imagen(mensaje_usuario)
        if ruta:
            resultado = analizar_imagen(
                ruta,
                mensaje_usuario,
                cliente,
                "meta-llama/llama-4-scout-17b-16e-instruct"
            )
            agregar_mensaje("user", mensaje_usuario)
            agregar_mensaje("assistant", resultado)
            incrementar("imagenes_analizadas")
            return resultado


    if intencion == "internet":
        resultados = buscar_en_internet(mensaje_usuario)
        mensajes.append({"role":"system","content":f"Info:\n{resultados}"})
        incrementar("busquedas_internet")


    if intencion == "leer_archivo":
        ruta = extraer_ruta(mensaje_usuario)
        if ruta:
            contenido = leer_archivo(ruta)
            mensajes.append({"role":"system","content":contenido})
            incrementar("archivos_leidos")


    # ======================================
    # HISTORIAL
    # ======================================

    historial = obtener_historial()[-MAX_HISTORY:]
    mensajes += historial


    # ======================================
    # PLAN
    # ======================================

    if intencion in ["chat","codigo"]:
        plan = construir_plan(mensaje_usuario)
        mensajes.append({"role":"system","content":f"Estrategia:\n{plan}"})


    # ======================================
    # RAZONAMIENTO
    # ======================================

    mensajes.append({
        "role":"user",
        "content": construir_razonamiento(mensaje_usuario)
    })


    # ======================================
    # LLAMADA IA
    # ======================================

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        max_tokens=MODEL_CONFIG["max_tokens"],
        temperature=MODEL_CONFIG["temperature"]
    )

    texto = respuesta.choices[0].message.content


    # ======================================
    # MEMORIA
    # ======================================

    agregar_mensaje("user", mensaje_usuario)
    agregar_mensaje("assistant", texto)

    guardar_log("usuario", mensaje_usuario)
    guardar_log("tenshi", texto)

    incrementar("mensajes_totales")


    # ======================================
    # CÓDIGO
    # ======================================

    if intencion == "codigo" and "```python" in texto:
        codigo = texto.split("```python")[1].split("```")[0]
        resultado = ejecutar_codigo(codigo)
        texto += f"\n\nResultado:\n{resultado}"
        incrementar("codigos_ejecutados")


    # ======================================
    # ARCHIVO
    # ======================================

    if intencion == "escribir_archivo":
        ruta = extraer_ruta(mensaje_usuario)
        if ruta:
            escribir_archivo(ruta, texto)
            print("💾 Guardado:", ruta)


    return texto