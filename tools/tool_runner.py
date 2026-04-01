# Módulo de herramientas de TENSHI

from ddgs import DDGS
from memory.stats import incrementar

def buscar_en_internet(query, max_resultados=3):
    """Busca en internet y devuelve los resultados."""
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(query, max_results=max_resultados))

        if not resultados:
            return "No encontré resultados para esa búsqueda."

        incrementar("busquedas_internet")

        texto = ""
        for i, r in enumerate(resultados, 1):
            texto += f"{i}. {r['title']}\n{r['body']}\n\n"

        return texto.strip()

    except Exception as e:
        return f"Error al buscar: {e}"

def leer_archivo(ruta):
    """Lee el contenido de un archivo de texto."""
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        
        incrementar("archivos_leidos")
        
        return f"Contenido del archivo '{ruta}':\n\n{contenido}"
    except FileNotFoundError:
        return f"No encontré el archivo '{ruta}'."
    except Exception as e:
        return f"Error al leer el archivo: {e}"

def escribir_archivo(ruta, contenido):
    """Escribe contenido en un archivo de texto."""
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        
        incrementar("archivos_escritos")
        
        return f"✅ Archivo '{ruta}' guardado correctamente."
    except Exception as e:
        return f"Error al escribir el archivo: {e}"

# Registro de herramientas disponibles
HERRAMIENTAS = {
    "buscar": {
        "funcion": buscar_en_internet,
        "descripcion": "Busca información actualizada en internet"
    },
    "leer_archivo": {
        "funcion": leer_archivo,
        "descripcion": "Lee el contenido de un archivo de texto"
    },
    "escribir_archivo": {
        "funcion": escribir_archivo,
        "descripcion": "Escribe contenido en un archivo de texto"
    }
}