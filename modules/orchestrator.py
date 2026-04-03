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
import re, os, json as _json, glob as _glob
from datetime import datetime, timedelta

def limpiar_texto(texto):
    if not texto: return ""
    texto_limpio = texto.lower().strip()
    for patron in [r"recuérdame\s*",r"recuerda\s+me\s*",r"recordarme\s*",r"guardame\s*",r"guarda\s+me\s*",r"guarda\s*",r"que\s+me\s+guarde\s*",r"que\s+mañana\s*",r"para\s+mañana\s*",r"que\s+tengo\s+que\s*",r"que\s+",r"tengo\s+que\s*",r"^para\s+",r"^necesito\s+"]:
        texto_limpio = re.sub(patron, "", texto_limpio, flags=re.IGNORECASE).strip()
    texto_limpio = re.sub(r"\s*mañana\s*$", "", texto_limpio).strip()
    return re.sub(r"\s+", " ", texto_limpio).strip()

def textos_similares(t1, t2):
    a, b = t1.lower().strip(), t2.lower().strip()
    return a == b or a in b or b in a

def detectar_intencion(texto):
    if not texto: return "general"
    tl = texto.lower()

    if tl.startswith("confirmar "):
        return "confirmar_modulo"

    autoprog = ["prográmate","programate","crea módulo","crea modulo","agrégarte","agregarte","impleméntate","implementate","escríbete","escribete","añádete","anadete","auto programa","auto-programa","genera módulo","genera modulo","nueva función","nueva funcion","nueva herramienta","self code","self-code"]
    if any(p in tl for p in autoprog):
        return "autoprogramacion"

    ejecutar = ["ejecuta","ejecutar","corre","correr","prueba el módulo","prueba el modulo","run","lanza","lanzar","testea","testear"]
    if any(p in tl for p in ejecutar):
        return "ejecutar"

    memoria = ["recuérdame","recuerdame","recordarme","guardame","guarda","pendiente para"]
    if any(p in tl for p in memoria):
        return "memoria"

    pendientes = ["pendientes","qué pendientes","mis pendientes","qué tengo pendiente","lista de pendientes","cuales son","cuales son mis","tengo pendiente","qué me falta","que falta","tareas"]
    if any(p in tl for p in pendientes):
        return "consultar_pendientes"

    busqueda = ["busca","buscar","internet","noticias","precio","actualmente","qué es","que es","explica","define","wikipedia"]
    if any(p in tl for p in busqueda):
        return "busqueda"

    return "general"

def obtener_cliente():
    for _, datos in APIS.items():
        if datos.get("activa") and datos.get("api_key"):
            try:
                cliente = Groq(api_key=datos["api_key"])
                modelo = datos.get("model")
                if not modelo: raise Exception("Modelo no configurado")
                return cliente, modelo
            except Exception as e:
                print(f"⚠️ Error API: {e}")
    raise Exception("No hay APIs disponibles.")

def generar_respuesta_ia(mensaje_usuario, cliente, modelo):
    historial = obtener_historial()[-10:]
    mensajes = [{"role":"system","content":PERSONALIDAD}]
    for m in historial:
        if m.get("role") in ["user","assistant"] and m.get("content"):
            mensajes.append({"role":m["role"],"content":m["content"]})
    mensajes.append({"role":"user","content":mensaje_usuario})
    respuesta = cliente.chat.completions.create(model=modelo,messages=mensajes,max_tokens=MODEL_CONFIG.get("max_tokens",512),temperature=MODEL_CONFIG.get("temperature",0.7))
    try:
        texto = respuesta.choices[0].message.content.strip()
        return texto if texto else "⚠️ No recibí respuesta."
    except:
        return "⚠️ Error interpretando respuesta."

def _extraer_nombre_modulo(texto):
    tl = texto.lower()
    match = re.search(r'(\w+)\.py', tl)
    if match:
        return match.group(1)
    triggers = ["ejecuta","ejecutar","corre","prueba","testea","lanza"]
    skip = {"el","la","los","las","un","una","módulo","modulo"}
    palabras = tl.split()
    for i, w in enumerate(palabras):
        if w in triggers:
            for j in range(i+1, len(palabras)):
                if palabras[j] not in skip:
                    return palabras[j].replace(".py","")
    return None

def responder(mensaje_usuario):
    try:
        if not mensaje_usuario:
            return "⚠️ No recibí ningún mensaje."

        incrementar("mensajes_totales")
        intencion = detectar_intencion(mensaje_usuario)
        print(f"✅ Intención: {intencion}")

        imagen_path = None
        if "temp_" in mensaje_usuario or "sandbox" in mensaje_usuario:
            for parte in mensaje_usuario.split():
                if parte.startswith("temp_") or "sandbox" in parte:
                    imagen_path = parte
                    mensaje_usuario = mensaje_usuario.replace(f" {imagen_path}","").strip()
                    break

        # 1️⃣ CONFIRMAR MÓDULO
        if intencion == "confirmar_modulo":
            nombre_pedido = mensaje_usuario.lower().replace("confirmar","").strip()
            patron = os.path.join(os.path.dirname(__file__),"..","logs",f"_pending_{nombre_pedido}.json")
            candidatos = _glob.glob(patron) or _glob.glob(os.path.join(os.path.dirname(__file__),"..","logs","_pending_*.json"))
            if candidatos:
                with open(candidatos[0],"r",encoding="utf-8") as f:
                    resultado = _json.load(f)
                nombre = resultado.get("nombre","modulo_nuevo")
                codigo = resultado.get("codigo","")
                from modules.self_coder import confirmar_guardado
                respuesta = confirmar_guardado(nombre, codigo)
                os.remove(candidatos[0])
            else:
                respuesta = "⚠️ No encontré ningún módulo pendiente de confirmar."
            agregar_mensaje("user",mensaje_usuario); agregar_mensaje("assistant",respuesta)
            guardar_log("usuario",mensaje_usuario); guardar_log("tenshi",respuesta)
            return respuesta

        # 2️⃣ AUTO-PROGRAMACIÓN
        if intencion == "autoprogramacion":
            try:
                resultado = auto_programar(mensaje_usuario)
                nombre = resultado.get("nombre","módulo_nuevo")
                codigo = resultado.get("codigo","")
                pendiente = resultado.get("pendiente_confirmacion",False)
                error = resultado.get("error","")
                if error and nombre == "error":
                    respuesta = f"❌ Error al auto-programarme: {error}"
                elif pendiente:
                    respuesta = (f"🤖 **Módulo generado:** `{nombre}.py`\n\n```python\n{codigo[:800]}{'...' if len(codigo)>800 else ''}\n```\n\n¿Confirmas que lo guarde? Escribe: **confirmar {nombre}**")
                    tmp_path = os.path.join(os.path.dirname(__file__),"..","logs",f"_pending_{nombre}.json")
                    with open(tmp_path,"w",encoding="utf-8") as f:
                        _json.dump(resultado,f,ensure_ascii=False,indent=2)
                else:
                    respuesta = "❌ Resultado inesperado."
                incrementar("autoprogramaciones")
            except Exception as e:
                respuesta = f"❌ Error en auto-programación: {e}"
            agregar_mensaje("user",mensaje_usuario); agregar_mensaje("assistant",respuesta)
            guardar_log("usuario",mensaje_usuario); guardar_log("tenshi",respuesta)
            return respuesta

        # 3️⃣ EJECUTAR CÓDIGO
        if intencion == "ejecutar":
            from modules.code_runner import ejecutar_modulo, ejecutar_y_corregir
            nombre_modulo = _extraer_nombre_modulo(mensaje_usuario)
            if nombre_modulo:
                print(f"▶️ Ejecutando módulo: {nombre_modulo}")
                resultado = ejecutar_modulo(nombre_modulo)
                if resultado["exito"]:
                    verificacion = ""
                    if resultado.get("verificado") == True:
                        verificacion = f"\n\n✅ **Verificado:** {resultado.get('verificacion_razon','')}"
                    elif resultado.get("verificado") == False:
                        verificacion = f"\n\n⚠️ **Advertencia:** {resultado.get('verificacion_razon','')}"
                    respuesta = f"▶️ **{nombre_modulo}.py** ejecutado:\n```\n{resultado['output']}\n```{verificacion}"
                else:
                    print("⚠️ Error detectado, autocorrigiendo...")
                    ruta_modulo = os.path.join(os.path.dirname(__file__), f"{nombre_modulo}.py")
                    with open(ruta_modulo,"r",encoding="utf-8") as f:
                        codigo = f.read()
                    resultado2 = ejecutar_y_corregir(codigo, nombre_modulo)
                    if resultado2["exito"]:
                        estado = "✅ Autocorregido y " if resultado2["corregido"] else ""
                        respuesta = (f"🔧 **Error detectado y corregido automáticamente.**\n\n"f"▶️ {estado}ejecutado:\n```\n{resultado2['output']}\n```")
                    else:
                        respuesta = (f"❌ No pude corregir el error en `{nombre_modulo}.py`:\n```\n{resultado2['error']}\n```")
            else:
                respuesta = "⚠️ No entendí qué módulo ejecutar. Escribe: **ejecuta nombre_modulo.py**"
            agregar_mensaje("user",mensaje_usuario); agregar_mensaje("assistant",respuesta)
            guardar_log("usuario",mensaje_usuario); guardar_log("tenshi",respuesta)
            return respuesta

        # 4️⃣ MEMORIA
        if intencion == "memoria":
            texto_limpio = limpiar_texto(mensaje_usuario)
            fecha = (datetime.now().date()+timedelta(days=1)).isoformat() if "mañana" in mensaje_usuario.lower() else None
            lista = obtener_pendientes() or []
            if any(textos_similares(p.get("texto",""),texto_limpio) for p in lista):
                respuesta = "⚠️ Ya tienes ese pendiente."
            else:
                agregar_pendiente(texto_limpio, fecha)
                respuesta = "📌 Guardado como pendiente."
            agregar_mensaje("user",mensaje_usuario); agregar_mensaje("assistant",respuesta)
            guardar_log("usuario",mensaje_usuario); guardar_log("tenshi",respuesta)
            return respuesta

        # 5️⃣ CONSULTAR PENDIENTES
        if intencion == "consultar_pendientes":
            lista = obtener_pendientes() or []
            if not lista:
                respuesta = "📭 No tienes pendientes."
            else:
                respuesta = "📋 **Tus pendientes:**\n\n"
                for i,p in enumerate(lista,1):
                    emoji = "⏳" if p.get("estado","pendiente")=="pendiente" else "✅"
                    respuesta += f"{i}. {emoji} **{p.get('texto','Sin descripción')}** ({p.get('fecha','Sin fecha')})\n"
            agregar_mensaje("user",mensaje_usuario); agregar_mensaje("assistant",respuesta)
            guardar_log("usuario",mensaje_usuario); guardar_log("tenshi",respuesta)
            return respuesta

        # 6️⃣ BÚSQUEDA
        if intencion == "busqueda":
            try:
                resultado = buscar_en_internet(mensaje_usuario, max_resultados=3)
                incrementar("busquedas_internet")
                agregar_mensaje("user",mensaje_usuario); agregar_mensaje("assistant",resultado)
                guardar_log("usuario",mensaje_usuario); guardar_log("tenshi",resultado)
                return resultado
            except Exception as e:
                respuesta = f"❌ Error en búsqueda: {e}"
                agregar_mensaje("user",mensaje_usuario); agregar_mensaje("assistant",respuesta)
                return respuesta

        # 7️⃣ GENERAL
        cliente, modelo = obtener_cliente()
        razonamiento = construir_razonamiento(mensaje_usuario)
        texto = generar_respuesta_ia(razonamiento, cliente, modelo)
        agregar_mensaje("user",mensaje_usuario); agregar_mensaje("assistant",texto)
        guardar_log("usuario",mensaje_usuario); guardar_log("tenshi",texto)
        return texto

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"ERROR REAL: {str(e)}"