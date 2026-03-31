# Orquestador de TENSHI - decide cómo responder

from groq import Groq
from config import APIS, NOMBRE_IA, MAX_TOKENS, TEMPERATURA, PERSONALIDAD
from memory.memory import agregar_mensaje, obtener_historial
from tools.tool_runner import buscar_en_internet, leer_archivo, escribir_archivo
from logs.logger import guardar_log
from modules.code_runner import ejecutar_codigo
from modules.vision import analizar_imagen
from memory.stats import incrementar

def obtener_cliente():
    """Intenta conectarse a la API disponible."""
    for nombre, datos in APIS.items():
        if datos["activa"]:
            try:
                cliente = Groq(api_key=datos["api_key"])
                print(f"✅ Conectado a {nombre}")
                return cliente, datos["model"]
            except Exception as e:
                print(f"❌ Falló {nombre}: {e}")
    raise Exception("No hay APIs disponibles.")

def necesita_busqueda(mensaje):
    """Detecta si el mensaje requiere buscar en internet."""
    palabras_clave = [
        "busca", "buscar", "busca en internet", "investiga", "googlea",
        "noticias", "precio", "clima", "temperatura", "hoy", "hoy en día",
        "actualmente", "últimas", "reciente", "ahora mismo",
        "2024", "2025", "2026",
        "quién es", "qué es", "dónde está", "cuándo fue", "cómo funciona",
        "cuánto cuesta", "cuánto vale", "cuál es el",
        "dólar", "euro", "bitcoin", "crypto", "bolsa", "acciones",
        "partido", "resultado", "elecciones", "guerra", "terremoto",
        "estreno", "lanzamiento", "nuevo", "última versión"
    ]
    mensaje_lower = mensaje.lower()
    return any(palabra in mensaje_lower for palabra in palabras_clave)

def necesita_leer_archivo(mensaje):
    """Detecta si el mensaje pide leer un archivo."""
    palabras_clave = ["lee", "leer", "abre", "abrir", "muestra", "mostrar"]
    extensiones = [".txt", ".csv", ".py", ".json", ".md"]
    mensaje_lower = mensaje.lower()
    tiene_palabra = any(p in mensaje_lower for p in palabras_clave)
    tiene_extension = any(e in mensaje_lower for e in extensiones)
    return tiene_palabra or tiene_extension

def necesita_ejecutar_codigo(mensaje):
    """Detecta si el mensaje requiere ejecutar código Python."""
    palabras_clave = [
        "ejecuta", "ejecutar", "corre", "correr", "calcula", "calcular",
        "programa", "programar", "código", "codigo", "script",
        "resuelve", "resolver", "computa", "computar"
    ]
    mensaje_lower = mensaje.lower()
    return any(palabra in mensaje_lower for palabra in palabras_clave)

def necesita_vision(mensaje):
    """Detecta si el mensaje incluye una imagen para analizar."""
    palabras_clave = [
        "imagen", "foto", "fotografía", "picture", "analiza", "analizar",
        "mira", "mirar", "observa", "observar", "describe", "describir",
        "qué ves", "qué hay", "qué muestra"
    ]
    extensiones = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    mensaje_lower = mensaje.lower()
    tiene_palabra = any(p in mensaje_lower for p in palabras_clave)
    tiene_extension = any(e in mensaje_lower for e in extensiones)
    return tiene_palabra or tiene_extension

def extraer_ruta_imagen(mensaje):
    """Extrae la ruta de la imagen del mensaje."""
    palabras = mensaje.split()
    extensiones = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    for palabra in palabras:
        if any(ext in palabra.lower() for ext in extensiones):
            return palabra.strip("\"'.,")
    return None

def necesita_escribir_archivo(mensaje):
    """Detecta si el mensaje pide escribir o guardar un archivo."""
    palabras_clave = ["guarda", "guardar", "escribe", "escribir", "crea", "crear", "genera", "generar"]
    extensiones = [".txt", ".csv", ".py", ".json", ".md"]
    mensaje_lower = mensaje.lower()
    tiene_palabra = any(p in mensaje_lower for p in palabras_clave)
    tiene_extension = any(e in mensaje_lower for e in extensiones)
    return tiene_palabra and tiene_extension

def extraer_ruta(mensaje):
    """Extrae la ruta del archivo mencionado en el mensaje."""
    palabras = mensaje.split()
    extensiones = [".txt", ".csv", ".py", ".json", ".md"]
    for palabra in palabras:
        if any(ext in palabra for ext in extensiones):
            return palabra.strip("\"'.,")
    return None

def responder(mensaje_usuario):
    """Recibe un mensaje y devuelve la respuesta de TENSHI."""

    # Obtener cliente y modelo
    cliente, modelo = obtener_cliente()

    # Construir lista de mensajes
    mensajes = [
       {"role": "system", "content": PERSONALIDAD}
    ]

    # Herramienta: visión (tiene prioridad, responde directo)
    if necesita_vision(mensaje_usuario):
        ruta_imagen = extraer_ruta_imagen(mensaje_usuario)
        if ruta_imagen:
            print(f"👁️ Analizando imagen: {ruta_imagen}")
            incrementar("imagenes_analizadas")
            resultado_vision = analizar_imagen(ruta_imagen, mensaje_usuario, cliente, "meta-llama/llama-4-scout-17b-16e-instruct")
            agregar_mensaje("user", mensaje_usuario)
            agregar_mensaje("assistant", resultado_vision)
            guardar_log("usuario", mensaje_usuario)
            guardar_log("tenshi", resultado_vision)
            return resultado_vision

    # Herramienta: buscar en internet
    if necesita_busqueda(mensaje_usuario):
        print("🔍 Buscando en internet...")
        incrementar("busquedas_internet")
        resultados = buscar_en_internet(mensaje_usuario)
        mensajes.append({"role": "user", "content": f"Resultados reales de internet:\n\n{resultados}"})
        mensajes.append({"role": "assistant", "content": "Entendido, usaré esa información para responder."})

    # Herramienta: leer archivo
    if necesita_leer_archivo(mensaje_usuario):
        ruta = extraer_ruta(mensaje_usuario)
        if ruta:
            print(f"📂 Leyendo archivo: {ruta}")
            incrementar("archivos_leidos")
            contenido = leer_archivo(ruta)
            mensajes.append({"role": "user", "content": contenido})
            mensajes.append({"role": "assistant", "content": "Entendido, tengo el contenido del archivo."})

    # Agregar historial y mensaje actual
    mensajes += obtener_historial()
    mensajes.append({"role": "user", "content": mensaje_usuario})

    # Llamar a la API
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURA
    )

    # Extraer texto
    texto = respuesta.choices[0].message.content

    # Guardar en memoria y log
    incrementar("mensajes_totales")
    agregar_mensaje("user", mensaje_usuario)
    agregar_mensaje("assistant", texto)
    guardar_log("usuario", mensaje_usuario)
    guardar_log("tenshi", texto)

    # Herramienta: ejecutar código
    if necesita_ejecutar_codigo(mensaje_usuario):
        if "```python" in texto:
            print("🧮 Ejecutando código...")
            codigo = texto.split("```python")[1].split("```")[0].strip()
            resultado = ejecutar_codigo(codigo)
            print(resultado)
            texto += f"\n\n{resultado}"
            agregar_mensaje("assistant", resultado)
            guardar_log("tenshi", resultado)

    # Herramienta: escribir archivo
    if necesita_escribir_archivo(mensaje_usuario):
        ruta = extraer_ruta(mensaje_usuario)
        if ruta:
            print(f"💾 Guardando archivo: {ruta}")
            escribir_archivo(ruta, texto)

    return texto