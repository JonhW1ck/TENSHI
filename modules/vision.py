# Módulo de visión de TENSHI

import base64
from PIL import Image
import os

def imagen_a_base64(ruta_imagen):
    """Convierte una imagen a base64."""
    try:
        with open(ruta_imagen, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

def obtener_extension(ruta):
    """Obtiene el tipo de imagen."""
    ext = os.path.splitext(ruta)[1].lower()
    tipos = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }
    return tipos.get(ext, "image/jpeg")

def analizar_imagen(ruta_imagen, pregunta, cliente, modelo_vision):
    """Envía una imagen a TENSHI para que la analice."""
    try:
        imagen_b64 = imagen_a_base64(ruta_imagen)
        if not imagen_b64:
            return f"❌ No encontré la imagen en '{ruta_imagen}'."

        tipo = obtener_extension(ruta_imagen)

        respuesta = cliente.chat.completions.create(
            model=modelo_vision,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{tipo};base64,{imagen_b64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": pregunta
                        }
                    ]
                }
            ],
            max_tokens=1024
        )

        return respuesta.choices[0].message.content

    except Exception as e:
        return f"❌ Error al analizar imagen: {e}"