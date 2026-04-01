# ==========================================
# 🧠 ORCHESTRATOR DE TENSHI (ROBUSTO v2)
# ==========================================

from groq import Groq
from config import APIS, PERSONALIDAD, MODEL_CONFIG

from memory.memory import agregar_mensaje, obtener_historial
from memory.stats import incrementar
from logs.logger import guardar_log

from database.db_manager import agregar_pendiente, obtener_pendientes

from modules.planner import construir_plan
from modules.reasoning import construir_razonamiento, evaluar_respuesta
from modules.vision import analizar_imagen
from tools.tool_runner import buscar_en_internet, leer_archivo, escribir_archivo
from modules.background import ejecutar_en_segundo_plano

import re
import os
from datetime import datetime, timedelta


# ==========================================
# 🧹 LIMPIAR TEXTO DE PALABRAS CLAVE
# ==========================================

def limpiar_texto(texto):
    """
    Elimina palabras clave y frases comunes al guardar pendientes.
    Ejemplo: 'recuérdame que mañana tengo que comprar pan' → 'comprar pan'
    """
    
    if not texto:
        return ""
    
    texto_limpio = texto.lower().strip()
    
    # Lista completa de palabras y frases a eliminar
    palabras_clave = [
        # Verbos principales
        r"recuérdame\s*",
        r"recuerda\s+me\s*",
        r"recordarme\s*",
        r"guardame\s*",
        r"guarda\s+me\s*",
        r"guarda\s*",
        r"que\s+me\s+guarde\s*",
        # Palabras temporales (pero SIN "mañana" - se maneja aparte)
        r"que\s+mañana\s*",
        r"para\s+mañana\s*",
        # Palabras conectivas
        r"que\s+tengo\s+que\s*",
        r"que\s+",
        r"tengo\s+que\s*",
        # Al inicio
        r"^para\s+",
        r"^necesito\s+",
    ]
    
    for patron in palabras_clave:
        texto_limpio = re.sub(patron, "", texto_limpio, flags=re.IGNORECASE).strip()
    
    # Remover "mañana" solo si está al final
    texto_limpio = re.sub(r"\s*mañana\s*$", "", texto_limpio).strip()
    
    # Limpiar espacios múltiples
    texto_limpio = re.sub(r"\s+", " ", texto_limpio).strip()
    
    return texto_limpio


def textos_similares(texto1, texto2):
    """
    Verifica si dos textos son similares usando substring matching.
    Retorna True si uno está contenido en el otro o son iguales.
    """
    t1 = texto1.lower().strip()
    t2 = texto2.lower().strip()
    
    return t1 == t2 or t1 in t2 or t2 in t1


# ==========================================
# 🔎 DETECCIÓN DE INTENCIÓN (MEJORADA)
# ==========================================

def detectar_intencion(texto):
    """
    Detecta la intención del usuario con múltiples palabras clave.
    Retorna: 'memoria', 'consultar_pendientes', 'busqueda' o 'general'
    """
    
    if not texto:
        return "general"
    
    texto_lower = texto.lower()
    
    # 📌 MEMORIA - Guardar pendiente
    palabras_memoria = ["recuérdame", "recuerdame", "recordarme", "guardame", "guarda", "pendiente para"]
    if any(palabra in texto_lower for palabra in palabras_memoria):
        print(f"🔎 Intención detectada: MEMORIA")
        return "memoria"
    
    # 📋 CONSULTAR PENDIENTES - Leer pendientes
    palabras_pendientes = ["pendientes", "qué pendientes", "mis pendientes", "qué tengo pendiente",
                          "lista de pendientes", "cuales son", "cuales son mis", "tengo pendiente",
                          "qué me falta", "que falta", "tareas"]
    if any(palabra in texto_lower for palabra in palabras_pendientes):
        print(f"🔎 Intención detectada: CONSULTAR_PENDIENTES")
        return "consultar_pendientes"
    
    # 🔍 BÚSQUEDAS
    palabras_busqueda = ["busca", "buscar", "internet", "noticias", "precio", "actualmente",
                        "qué es", "que es", "explica", "define", "wikipedia"]
    if any(palabra in texto_lower for palabra in palabras_busqueda):
        print(f"🔎 Intención detectada: BUSQUEDA")
        return "busqueda"
    
    print(f"🔎 Intención detectada: GENERAL")
    return "general"


# ==========================================
# 🔌 CLIENTE IA
# ==========================================

def obtener_cliente():
    """
    Obtiene cliente disponible de IA
    """

    for nombre, datos in APIS.items():

        if datos.get("activa") and datos.get("api_key"):

            try:

                cliente = Groq(api_key=datos["api_key"])

                modelo = datos.get("model")

                if not modelo:
                    raise Exception("Modelo no configurado")

                return cliente, modelo

            except Exception as e:

                print(f"⚠️ Error inicializando API {nombre}: {e}")

    raise Exception("No hay APIs disponibles.")


# ==========================================
#  RESPUESTA IA
# ==========================================

def generar_respuesta_ia(mensaje_usuario, cliente, modelo):

    historial = obtener_historial()[-10:]

    mensajes = [
        {
            "role": "system",
            "content": PERSONALIDAD
        }
    ]

    for m in historial:

        role = m.get("role")
        content = m.get("content")

        if role in ["user", "assistant"] and content:
            mensajes.append({
                "role": role,
                "content": content
            })

    mensajes.append({
        "role": "user",
        "content": mensaje_usuario
    })

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        max_tokens=MODEL_CONFIG.get("max_tokens", 512),
        temperature=MODEL_CONFIG.get("temperature", 0.7)
    )

    try:

        texto = respuesta.choices[0].message.content.strip()

        if not texto:
            texto = "⚠️ No recibí respuesta del modelo."

    except Exception:

        texto = "⚠️ Error interpretando respuesta del modelo."

    return texto


# ==========================================
# 🤖 RESPUESTA PRINCIPAL (MEJORADA)
# ==========================================

def responder(mensaje_usuario):

    try:

        if not mensaje_usuario:
            return "⚠️ No recibí ningún mensaje."

        print(f"\n{'='*60}")
        print(f"📥 MENSAJE: {mensaje_usuario}")
        print(f"{'='*60}")

        # 📊 Incrementar stats
        incrementar("mensajes_totales")

        # 🔎 Detectar intención MEJORADA
        intencion = detectar_intencion(mensaje_usuario)
        print(f"✅ Intención: {intencion}")

        # 🧾 Construir plan de respuesta
        plan = construir_plan(mensaje_usuario)
        print(f"📋 Plan: {plan}")

        # ==========================================
        # 👁️ DETECTAR Y ANALIZAR IMÁGENES
        # ==========================================
        
        imagen_path = None
        if "temp_" in mensaje_usuario or "sandbox" in mensaje_usuario:
            partes = mensaje_usuario.split()
            for parte in partes:
                if parte.startswith("temp_") or "sandbox" in parte:
                    imagen_path = parte
                    mensaje_usuario = mensaje_usuario.replace(f" {imagen_path}", "").strip()
                    print(f"🖼️ Imagen detectada: {imagen_path}")
                    break

        # ==========================================
        # 📌 GUARDAR PENDIENTE
        # ==========================================
        
        if intencion == "memoria":
            
            print(f"\n🔄 Procesando: GUARDAR PENDIENTE")

            # 🧹 Limpiar texto de palabras clave
            texto_limpio = limpiar_texto(mensaje_usuario)
            print(f"   Texto limpiado: '{texto_limpio}'")

            # 📅 Detectar fecha (mañana o hoy)
            fecha = None
            if "mañana" in mensaje_usuario.lower():
                fecha = (datetime.now().date() + timedelta(days=1)).isoformat()
                print(f"   Fecha: {fecha} (MAÑANA)")
            else:
                print(f"   Fecha: Sin especificar (HOY)")

            # ⚠️ IMPORTANTE: Leer SIEMPRE de db_manager
            lista = obtener_pendientes() or []
            print(f"   Pendientes actuales en DB: {len(lista)}")
            for p in lista:
                print(f"      - {p.get('texto')} | {p.get('fecha')}")

            # 🔍 Verificar duplicados con matching inteligente
            ya_existe = False
            for p in lista:
                if textos_similares(p.get("texto"), texto_limpio):
                    ya_existe = True
                    print(f"   ⚠️ DUPLICADO DETECTADO: '{p.get('texto')}'")
                    break

            if ya_existe:
                respuesta = "⚠️ Ya tienes ese pendiente."
            else:
                agregar_pendiente(texto_limpio, fecha)
                print(f"   ✅ GUARDADO EN DB")
                
                # Verificar que se guardó
                lista_nueva = obtener_pendientes() or []
                print(f"   Pendientes DESPUÉS de guardar: {len(lista_nueva)}")
                for p in lista_nueva:
                    print(f"      - {p.get('texto')} | {p.get('fecha')}")
                
                respuesta = "📌 Guardado como pendiente."

            agregar_mensaje("user", mensaje_usuario)
            agregar_mensaje("assistant", respuesta)

            guardar_log("usuario", mensaje_usuario)
            guardar_log("tenshi", respuesta)

            print(f"📤 RESPUESTA: {respuesta}\n")
            return respuesta

        # ==========================================
        # 📋 CONSULTAR PENDIENTES
        # ==========================================

        if intencion == "consultar_pendientes":
            
            print(f"\n🔄 Procesando: CONSULTAR PENDIENTES")

            # ⚠️ IMPORTANTE: Leer SIEMPRE de db_manager
            lista = obtener_pendientes() or []
            
            print(f"   📂 Leyendo de: database/db_manager.py")
            print(f"   📊 Total de pendientes encontrados: {len(lista)}")
            
            for i, p in enumerate(lista, 1):
                print(f"      {i}. {p.get('texto')} | Estado: {p.get('estado')} | Fecha: {p.get('fecha')}")

            if not lista:
                respuesta = "📭 No tienes pendientes."
                print(f"   ⚠️ LISTA VACÍA")
            else:
                respuesta = "📋 **Tus pendientes:**\n\n"

                for i, p in enumerate(lista, 1):
                    texto = p.get("texto", "Sin descripción")
                    fecha = p.get("fecha", "Sin fecha")
                    estado = p.get("estado", "pendiente")
                    
                    emoji = "⏳" if estado == "pendiente" else "✅"
                    respuesta += f"{i}. {emoji} **{texto}** ({fecha})\n"
                
                print(f"   ✅ FORMATEADO PARA USUARIO")

            agregar_mensaje("user", mensaje_usuario)
            agregar_mensaje("assistant", respuesta)

            guardar_log("usuario", mensaje_usuario)
            guardar_log("tenshi", respuesta)

            print(f"📤 RESPUESTA: {respuesta}\n")
            return respuesta

        # ==========================================
        # 🔍 BÚSQUEDAS EN INTERNET
        # ==========================================

        if intencion == "busqueda":
            
            print(f"\n🔄 Procesando: BÚSQUEDA EN INTERNET")
            
            try:
                print(f"   🌐 Buscando: {mensaje_usuario}")
                
                resultado = buscar_en_internet(mensaje_usuario, max_resultados=3)
                
                incrementar("busquedas_internet")
                print(f"   ✅ BÚSQUEDA COMPLETADA")

                agregar_mensaje("user", mensaje_usuario)
                agregar_mensaje("assistant", resultado)

                guardar_log("usuario", mensaje_usuario)
                guardar_log("tenshi", resultado)

                print(f"📤 RESPUESTA: {resultado[:100]}...\n")
                return resultado

            except Exception as e:
                print(f"   ❌ Error en búsqueda: {e}")
                respuesta = f"❌ Error en búsqueda: {e}"
                
                agregar_mensaje("user", mensaje_usuario)
                agregar_mensaje("assistant", respuesta)
                
                print(f"📤 RESPUESTA: {respuesta}\n")
                return respuesta

        # ==========================================
        # 🤖 RESPUESTA IA CON RAZONAMIENTO (GENERAL)
        # ==========================================

        print(f"\n🔄 Procesando: RESPUESTA IA GENERAL")

        cliente, modelo = obtener_cliente()

        # Construir razonamiento interno (no mostrado)
        razonamiento = construir_razonamiento(mensaje_usuario)
        print(f"   🧠 Razonamiento construido")

        # Generar respuesta con razonamiento
        texto = generar_respuesta_ia(razonamiento, cliente, modelo)
        print(f"   ✅ RESPUESTA GENERADA")

        # Guardar en memoria
        agregar_mensaje("user", mensaje_usuario)
        agregar_mensaje("assistant", texto)

        guardar_log("usuario", mensaje_usuario)
        guardar_log("tenshi", texto)

        print(f"📤 RESPUESTA: {texto[:100]}...\n")
        return texto


    except Exception as e:

        import traceback

        print("\n" + "="*60)
        print("🔥 ERROR REAL TENSHI 🔥")
        print("="*60)
        traceback.print_exc()
        print(f"MENSAJE: {str(e)}")
        print("="*60 + "\n")

        return f"ERROR REAL: {str(e)}"