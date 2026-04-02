# ==========================================
# 🧠 ORCHESTRATOR DE TENSHI (ROBUSTO v3)
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
from modules.self_coder import auto_programar

import re
import os
import json as _json
import glob as _glob
from datetime import datetime, timedelta


# ==========================================
# 🧹 LIMPIAR TEXTO DE PALABRAS CLAVE
# ==========================================

def limpiar_texto(texto):
    if not texto:
        return ""
    texto_limpio = texto.lower().strip()
    palabras_clave = [
        r"recuérdame\s*", r"recuerda\s+me\s*", r"recordarme\s*",
        r"guardame\s*", r"guarda\s+me\s*", r"guarda\s*",
        r"que\s+me\s+guarde\s*", r"que\s+mañana\s*", r"para\s+mañana\s*",
        r"que\s+tengo\s+que\s*", r"que\s+", r"tengo\s+que\s*",
        r"^para\s+", r"^necesito\s+",
    ]
    for patron in palabras_clave:
        texto_limpio = re.sub(patron, "", texto_limpio, flags=re.IGNORECASE).strip()
    texto_limpio = re.sub(r"\s*mañana\s*$", "", texto_limpio).strip()
    texto_limpio = re.sub(r"\s+", " ", texto_limpio).strip()
    return texto_limpio


def textos_similares(texto1, texto2):
    t1 = texto1.lower().strip()
    t2 = texto2.lower().strip()
    return t1 == t2 or t1 in t2 or t2 in t1


# ==========================================
# 🔎 DETECCIÓN DE INTENCIÓN
# Orden de prioridad (de mayor a menor):
#   1. confirmar_modulo
#   2. autoprogramacion   ← ANTES que memoria para evitar falsos positivos
#   3. memoria
#   4. consultar_pendientes
#   5. busqueda
#   6. general
# ==========================================

def detectar_intencion(texto):
    if not texto:
        return "general"

    texto_lower = texto.lower()

    # 1️⃣ CONFIRMAR MÓDULO — siempre primero
    if texto_lower.startswith("confirmar "):
        print("🔎 Intención detectada: CONFIRMAR_MODULO")
        return "confirmar_modulo"

    # 2️⃣ AUTO-PROGRAMACIÓN — antes que memoria para evitar que
    #    palabras como "guarda" en el prompt disparen la rama equivocada
    palabras_autoprog = [
        "prográmate", "programate", "crea módulo", "crea modulo",
        "agrégarte", "agregarte", "impleméntate", "implementate",
        "escríbete", "escribete", "añádete", "anadete",
        "auto programa", "auto-programa", "genera módulo", "genera modulo",
        "nueva función", "nueva funcion", "nueva herramienta",
        "self code", "self-code",
    ]
    if any(p in texto_lower for p in palabras_autoprog):
        print("🔎 Intención detectada: AUTOPROGRAMACION")
        return "autoprogramacion"

    # 3️⃣ MEMORIA — guardar pendiente
    palabras_memoria = [
        "recuérdame", "recuerdame", "recordarme",
        "guardame", "guarda", "pendiente para"
    ]
    if any(p in texto_lower for p in palabras_memoria):
        print("🔎 Intención detectada: MEMORIA")
        return "memoria"

    # 4️⃣ CONSULTAR PENDIENTES
    palabras_pendientes = [
        "pendientes", "qué pendientes", "mis pendientes",
        "qué tengo pendiente", "lista de pendientes", "cuales son",
        "cuales son mis", "tengo pendiente", "qué me falta",
        "que falta", "tareas"
    ]
    if any(p in texto_lower for p in palabras_pendientes):
        print("🔎 Intención detectada: CONSULTAR_PENDIENTES")
        return "consultar_pendientes"

    # 5️⃣ BÚSQUEDA
    palabras_busqueda = [
        "busca", "buscar", "internet", "noticias", "precio",
        "actualmente", "qué es", "que es", "explica", "define", "wikipedia"
    ]
    if any(p in texto_lower for p in palabras_busqueda):
        print("🔎 Intención detectada: BUSQUEDA")
        return "busqueda"

    print("🔎 Intención detectada: GENERAL")
    return "general"


# ==========================================
# 🔌 CLIENTE IA
# ==========================================

def obtener_cliente():
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
# 🤖 RESPUESTA IA
# ==========================================

def generar_respuesta_ia(mensaje_usuario, cliente, modelo):
    historial = obtener_historial()[-10:]
    mensajes = [{"role": "system", "content": PERSONALIDAD}]
    for m in historial:
        role = m.get("role")
        content = m.get("content")
        if role in ["user", "assistant"] and content:
            mensajes.append({"role": role, "content": content})
    mensajes.append({"role": "user", "content": mensaje_usuario})
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
# 🚀 RESPUESTA PRINCIPAL
# ==========================================

def responder(mensaje_usuario):
    try:
        if not mensaje_usuario:
            return "⚠️ No recibí ningún mensaje."

        print(f"\n{'='*60}")
        print(f"📥 MENSAJE: {mensaje_usuario}")
        print(f"{'='*60}")

        incrementar("mensajes_totales")

        intencion = detectar_intencion(mensaje_usuario)
        print(f"✅ Intención: {intencion}")

        plan = construir_plan(mensaje_usuario)
        print(f"📋 Plan: {plan}")

        # ── Detectar imagen adjunta ──────────────────────────────
        imagen_path = None
        if "temp_" in mensaje_usuario or "sandbox" in mensaje_usuario:
            for parte in mensaje_usuario.split():
                if parte.startswith("temp_") or "sandbox" in parte:
                    imagen_path = parte
                    mensaje_usuario = mensaje_usuario.replace(f" {imagen_path}", "").strip()
                    print(f"🖼️ Imagen detectada: {imagen_path}")
                    break

        # ==========================================
        # 1️⃣ CONFIRMAR MÓDULO
        # ==========================================
        if intencion == "confirmar_modulo":
            print("\n✅ Procesando: CONFIRMAR MÓDULO")

            nombre_pedido = mensaje_usuario.lower().replace("confirmar", "").strip()
            patron = os.path.join(os.path.dirname(__file__), "..", "logs", f"_pending_{nombre_pedido}.json")
            candidatos = _glob.glob(patron)

            if not candidatos:
                candidatos = _glob.glob(
                    os.path.join(os.path.dirname(__file__), "..", "logs", "_pending_*.json")
                )

            if candidatos:
                with open(candidatos[0], "r", encoding="utf-8") as f:
                    resultado = _json.load(f)
                nombre = resultado.get("nombre", "modulo_nuevo")
                codigo = resultado.get("codigo", "")
                from modules.self_coder import confirmar_guardado
                respuesta = confirmar_guardado(nombre, codigo)
                os.remove(candidatos[0])
            else:
                respuesta = "⚠️ No encontré ningún módulo pendiente de confirmar."

            agregar_mensaje("user", mensaje_usuario)
            agregar_mensaje("assistant", respuesta)
            guardar_log("usuario", mensaje_usuario)
            guardar_log("tenshi", respuesta)
            return respuesta

        # ==========================================
        # 2️⃣ AUTO-PROGRAMACIÓN
        # ==========================================
        if intencion == "autoprogramacion":
            print("\n🤖 Procesando: AUTO-PROGRAMACIÓN")
            try:
                resultado = auto_programar(mensaje_usuario)
                nombre   = resultado.get("nombre", "módulo_nuevo")
                codigo   = resultado.get("codigo", "")
                pendiente = resultado.get("pendiente_confirmacion", False)
                error    = resultado.get("error", "")

                if error and nombre == "error":
                    respuesta = f"❌ Error al auto-programarme: {error}"
                elif pendiente:
                    respuesta = (
                        f"🤖 **Módulo generado:** `{nombre}.py`\n\n"
                        f"```python\n{codigo[:800]}{'...' if len(codigo) > 800 else ''}\n```\n\n"
                        f"¿Confirmas que lo guarde? Escribe: **confirmar {nombre}**"
                    )
                    tmp_path = os.path.join(os.path.dirname(__file__), "..", "logs", f"_pending_{nombre}.json")
                    with open(tmp_path, "w", encoding="utf-8") as f:
                        _json.dump(resultado, f, ensure_ascii=False, indent=2)
                else:
                    respuesta = "❌ Resultado inesperado del auto-programador."

                incrementar("autoprogramaciones")

            except Exception as e:
                respuesta = f"❌ Error en auto-programación: {e}"

            agregar_mensaje("user", mensaje_usuario)
            agregar_mensaje("assistant", respuesta)
            guardar_log("usuario", mensaje_usuario)
            guardar_log("tenshi", respuesta)
            print(f"✅ RESPUESTA AUTO-PROG: {respuesta[:100]}...\n")
            return respuesta

        # ==========================================
        # 3️⃣ GUARDAR PENDIENTE
        # ==========================================
        if intencion == "memoria":
            print("\n🔄 Procesando: GUARDAR PENDIENTE")

            texto_limpio = limpiar_texto(mensaje_usuario)
            print(f"   Texto limpiado: '{texto_limpio}'")

            fecha = None
            if "mañana" in mensaje_usuario.lower():
                fecha = (datetime.now().date() + timedelta(days=1)).isoformat()

            lista = obtener_pendientes() or []
            ya_existe = any(textos_similares(p.get("texto", ""), texto_limpio) for p in lista)

            if ya_existe:
                respuesta = "⚠️ Ya tienes ese pendiente."
            else:
                agregar_pendiente(texto_limpio, fecha)
                respuesta = "📌 Guardado como pendiente."

            agregar_mensaje("user", mensaje_usuario)
            agregar_mensaje("assistant", respuesta)
            guardar_log("usuario", mensaje_usuario)
            guardar_log("tenshi", respuesta)
            return respuesta

        # ==========================================
        # 4️⃣ CONSULTAR PENDIENTES
        # ==========================================
        if intencion == "consultar_pendientes":
            print("\n🔄 Procesando: CONSULTAR PENDIENTES")

            lista = obtener_pendientes() or []

            if not lista:
                respuesta = "📭 No tienes pendientes."
            else:
                respuesta = "📋 **Tus pendientes:**\n\n"
                for i, p in enumerate(lista, 1):
                    texto = p.get("texto", "Sin descripción")
                    fecha = p.get("fecha", "Sin fecha")
                    estado = p.get("estado", "pendiente")
                    emoji = "⏳" if estado == "pendiente" else "✅"
                    respuesta += f"{i}. {emoji} **{texto}** ({fecha})\n"

            agregar_mensaje("user", mensaje_usuario)
            agregar_mensaje("assistant", respuesta)
            guardar_log("usuario", mensaje_usuario)
            guardar_log("tenshi", respuesta)
            return respuesta

        # ==========================================
        # 5️⃣ BÚSQUEDA EN INTERNET
        # ==========================================
        if intencion == "busqueda":
            print("\n🔄 Procesando: BÚSQUEDA EN INTERNET")
            try:
                resultado = buscar_en_internet(mensaje_usuario, max_resultados=3)
                incrementar("busquedas_internet")
                agregar_mensaje("user", mensaje_usuario)
                agregar_mensaje("assistant", resultado)
                guardar_log("usuario", mensaje_usuario)
                guardar_log("tenshi", resultado)
                return resultado
            except Exception as e:
                respuesta = f"❌ Error en búsqueda: {e}"
                agregar_mensaje("user", mensaje_usuario)
                agregar_mensaje("assistant", respuesta)
                return respuesta

        # ==========================================
        # 6️⃣ RESPUESTA IA GENERAL
        # ==========================================
        print("\n🔄 Procesando: RESPUESTA IA GENERAL")

        cliente, modelo = obtener_cliente()
        razonamiento = construir_razonamiento(mensaje_usuario)
        texto = generar_respuesta_ia(razonamiento, cliente, modelo)

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