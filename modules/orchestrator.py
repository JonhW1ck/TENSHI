# Orquestador de TENSHI

from groq import Groq
from config import APIS, MODELOS, MODEL_CONFIG, PERSONALIDAD

from memory.memory import agregar_mensaje, obtener_historial
from tools.tool_runner import buscar_en_internet, leer_archivo, escribir_archivo
from logs.logger import guardar_log
from memory.stats import incrementar

from modules.code_runner import ejecutar_codigo
from modules.vision import analizar_imagen
from modules.reasoning import construir_razonamiento
from modules.planner import construir_plan


# ==========================================
# CONFIG
# ==========================================

MAX_HISTORY = 10


# ==========================================
# CLIENTE API
# ==========================================

def obtener_cliente():

    for nombre, datos in APIS.items():

        if datos["activa"]:

            try:

                cliente = Groq(api_key=datos["api_key"])
                modelo = MODELOS["principal"]

                print(f"✅ API conectada: {nombre} | modelo {modelo}")

                return cliente, modelo

            except Exception as e:

                print(f"❌ API {nombre} falló:", e)

    raise Exception("No hay APIs disponibles")


# ==========================================
# DETECTORES
# ==========================================

def contiene(mensaje, palabras):

    mensaje = mensaje.lower()

    return any(p in mensaje for p in palabras)


def necesita_busqueda(mensaje):

    palabras = [
        "busca","buscar","investiga","googlea",
        "noticias","precio","clima","temperatura",
        "actualmente","reciente","últimas",
        "quién es","qué es","dónde está"
    ]

    return contiene(mensaje, palabras)


def necesita_leer_archivo(mensaje):

    palabras = ["lee","leer","abre","abrir","mostrar"]

    extensiones = [".txt",".csv",".py",".json",".md"]

    return contiene(mensaje, palabras) or contiene(mensaje, extensiones)


def necesita_escribir_archivo(mensaje):

    palabras = ["guardar","guarda","crear","genera","escribe"]

    extensiones = [".txt",".csv",".py",".json",".md"]

    return contiene(mensaje, palabras) and contiene(mensaje, extensiones)


def necesita_codigo(mensaje):

    palabras = ["codigo","script","programa","ejecuta","calcula"]

    return contiene(mensaje, palabras)


def necesita_vision(mensaje):

    extensiones = [".jpg",".jpeg",".png",".webp",".gif"]

    return contiene(mensaje, extensiones)


# ==========================================
# EXTRACTORES
# ==========================================

def extraer_ruta(mensaje):

    palabras = mensaje.split()

    extensiones = [".txt",".csv",".py",".json",".md"]

    for p in palabras:

        if any(ext in p for ext in extensiones):

            return p.strip("\"',")

    return None


def extraer_imagen(mensaje):

    palabras = mensaje.split()

    extensiones = [".jpg",".jpeg",".png",".webp",".gif"]

    for p in palabras:

        if any(ext in p for ext in extensiones):

            return p.strip("\"',")

    return None


# ==========================================
# RESPUESTA PRINCIPAL
# ==========================================

def responder(mensaje_usuario):

    cliente, modelo = obtener_cliente()

    mensajes = []

    mensajes.append({
        "role": "system",
        "content": PERSONALIDAD
    })

    # ======================================
    # VISION
    # ======================================

    if necesita_vision(mensaje_usuario):

        ruta = extraer_imagen(mensaje_usuario)

        if ruta:

            print("👁️ Analizando imagen:", ruta)

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


    # ======================================
    # BUSQUEDA INTERNET
    # ======================================

    if necesita_busqueda(mensaje_usuario):

        print("🔎 búsqueda internet")

        resultados = buscar_en_internet(mensaje_usuario)

        mensajes.append({
            "role": "system",
            "content": f"Información encontrada en internet:\n{resultados}"
        })

        incrementar("busquedas_internet")


    # ======================================
    # LEER ARCHIVO
    # ======================================

    if necesita_leer_archivo(mensaje_usuario):

        ruta = extraer_ruta(mensaje_usuario)

        if ruta:

            print("📂 leyendo archivo:", ruta)

            contenido = leer_archivo(ruta)

            mensajes.append({
                "role": "system",
                "content": f"Contenido del archivo:\n{contenido}"
            })

            incrementar("archivos_leidos")


    # ======================================
    # HISTORIAL
    # ======================================

    historial = obtener_historial()[-MAX_HISTORY:]

    mensajes += historial


    # ======================================
    # PLAN
    # ======================================

    plan = construir_plan(mensaje_usuario)

    mensajes.append({
        "role": "system",
        "content": f"Estrategia interna:\n{plan}"
    })


    # ======================================
    # RAZONAMIENTO
    # ======================================

    mensajes.append({
        "role": "user",
        "content": construir_razonamiento(mensaje_usuario)
    })


    # ======================================
    # LLAMADA AL MODELO
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
    # EJECUTAR CODIGO
    # ======================================

    if necesita_codigo(mensaje_usuario):

        if "```python" in texto:

            codigo = texto.split("```python")[1].split("```")[0]

            resultado = ejecutar_codigo(codigo)

            texto += f"\n\nResultado ejecución:\n{resultado}"

            incrementar("codigos_ejecutados")


    # ======================================
    # GUARDAR ARCHIVO
    # ======================================

    if necesita_escribir_archivo(mensaje_usuario):

        ruta = extraer_ruta(mensaje_usuario)

        if ruta:

            escribir_archivo(ruta, texto)

            print("💾 archivo guardado:", ruta)


    return texto