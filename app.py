# ==========================================
# 📦 IMPORTS
# ==========================================

import streamlit as st
import os
import glob
import threading
import traceback

from modules.orchestrator import responder
from modules.autonomy import analizar_y_proponer

from memory.memory import limpiar_historial
from memory.stats import obtener_stats, incrementar

import recordatorios


# ==========================================
# 🧹 LIMPIAR ARCHIVOS TEMPORALES AL INICIO
# ==========================================

def limpiar_temp_files():
    """Limpia archivos temporales de memory/ al iniciar"""
    try:
        memory_dir = os.path.join(os.path.dirname(__file__), "memory")
        for archivo in os.listdir(memory_dir):
            if archivo.startswith("tmp"):
                ruta_tmp = os.path.join(memory_dir, archivo)
                try:
                    if os.path.isfile(ruta_tmp):
                        os.remove(ruta_tmp)
                        print(f"🧹 Eliminado: {archivo}")
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar {archivo}: {e}")
    except Exception as e:
        print(f"⚠️ Error limpiando temp files: {e}")


# Ejecutar una vez al iniciar
if "temp_cleaned" not in st.session_state:
    limpiar_temp_files()
    st.session_state.temp_cleaned = True


# ==========================================
# ⚙️ CONFIG STREAMLIT
# ==========================================

st.set_page_config(
    page_title="TENSHI · NHRX LABS",
    page_icon="⚔️",
    layout="centered"
)


# ==========================================
# 🔔 HILO RECORDATORIOS
# ==========================================

def iniciar_hilo_recordatorios():

    try:

        hilo = threading.Thread(
            target=recordatorios.revisar_recordatorios,
            daemon=True
        )

        hilo.start()

    except Exception as e:

        print("⚠️ Error iniciando hilo:", e)


if "hilo_recordatorios_iniciado" not in st.session_state:

    iniciar_hilo_recordatorios()
    st.session_state.hilo_recordatorios_iniciado = True


# ==========================================
# 🧠 SESSION STATE
# ==========================================

if "mensajes_ui" not in st.session_state:

    st.session_state.mensajes_ui = [
        {
            "rol": "assistant",
            "texto": "Hola. Soy TENSHI. ¿En qué trabajamos hoy?"
        }
    ]

if "procesando" not in st.session_state:
    st.session_state.procesando = False


# ==========================================
# 📊 STATS
# ==========================================

try:

    stats = obtener_stats()

except Exception:

    stats = {
        "mensajes_totales": 0,
        "busquedas_internet": 0,
        "codigos_ejecutados": 0,
        "imagenes_analizadas": 0,
        "archivos_leidos": 0
    }


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💬 Mensajes", stats.get("mensajes_totales", 0))
col2.metric("🔍 Búsquedas", stats.get("busquedas_internet", 0))
col3.metric("🧮 Código", stats.get("codigos_ejecutados", 0))
col4.metric("👁️ Imágenes", stats.get("imagenes_analizadas", 0))
col5.metric("📁 Archivos", stats.get("archivos_leidos", 0))

st.markdown("<hr>", unsafe_allow_html=True)


# ==========================================
# 💬 CHAT UI
# ==========================================

MAX_UI_HISTORY = 40

st.session_state.mensajes_ui = st.session_state.mensajes_ui[-MAX_UI_HISTORY:]


for msg in st.session_state.mensajes_ui:

    if msg["rol"] == "assistant":

        st.markdown(f"**TENSHI:** {msg['texto']}")

    else:

        st.markdown(f"**TÚ:** {msg['texto']}")


# ==========================================
# 🖼️ SUBIR IMAGEN
# ==========================================

imagen_subida = st.file_uploader(
    "",
    type=["jpg","jpeg","png","webp"],
    label_visibility="collapsed"
)

if imagen_subida:

    # Crear carpeta sandbox si no existe
    sandbox_dir = os.path.join(os.path.dirname(__file__), "sandbox")
    os.makedirs(sandbox_dir, exist_ok=True)

    ruta = os.path.join(sandbox_dir, imagen_subida.name)

    with open(ruta, "wb") as f:
        f.write(imagen_subida.getbuffer())

    st.image(imagen_subida, width=200)

    st.session_state["imagen_path"] = ruta
    
    incrementar("imagenes_analizadas")


# ==========================================
# ⌨️ INPUT
# ==========================================

colA, colB = st.columns([5,1])

with colA:

    entrada = st.text_input(
        "",
        placeholder="Escribe algo a TENSHI...",
        label_visibility="collapsed"
    )

with colB:

    enviar = st.button(
        "→",
        disabled=st.session_state.procesando
    )


# ==========================================
# 🧹 LIMPIAR CHAT
# ==========================================

if st.button("LIMPIAR"):

    limpiar_historial()

    st.session_state.mensajes_ui = [
        {
            "rol": "assistant",
            "texto": "Hola. Soy TENSHI. ¿En qué trabajamos hoy?"
        }
    ]

    st.rerun()


# ==========================================
# ⚙️ PROCESAR MENSAJE
# ==========================================

if enviar and entrada.strip() and not st.session_state.procesando:

    st.session_state.procesando = True

    mensaje = entrada

    if "imagen_path" in st.session_state:

        mensaje += f" {st.session_state['imagen_path']}"

    st.session_state.mensajes_ui.append({
        "rol": "user",
        "texto": entrada
    })

    try:

        with st.spinner("TENSHI pensando..."):

            respuesta = responder(mensaje)

    except Exception:

        traceback.print_exc()
        respuesta = "⚠️ Error interno."

    st.session_state.mensajes_ui.append({
        "rol": "assistant",
        "texto": respuesta
    })


    # 🤖 AUTONOMÍA
    try:

        propuesta = analizar_y_proponer()

        if propuesta:

            st.session_state.mensajes_ui.append({
                "rol": "assistant",
                "texto": f"💡 {propuesta}"
            })

    except Exception:
        pass


    # 🧹 LIMPIAR IMAGEN
    if "imagen_path" in st.session_state:

        try:
            os.remove(st.session_state["imagen_path"])
        except Exception:
            pass

        del st.session_state["imagen_path"]


    st.session_state.procesando = False

    st.rerun()


# ==========================================
# 🔔 RECORDATORIOS
# ==========================================

with st.expander("🔔 Recordatorios"):

    if st.button("Ver recordatorios"):

        try:

            st.write(recordatorios.ver_recordatorios())

        except Exception as e:

            st.error(f"Error: {e}")


# ==========================================
# 📜 HISTORIAL LOGS
# ==========================================

with st.expander("📅 Historial"):

    archivos = sorted(
        glob.glob("logs/tenshi_*.txt"),
        reverse=True
    )

    if archivos:

        fechas = [
            os.path.basename(f)
            .replace("tenshi_","")
            .replace(".txt","")
            for f in archivos
        ]

        fecha = st.selectbox("Selecciona fecha", fechas)

        with open(
            f"logs/tenshi_{fecha}.txt",
            "r",
            encoding="utf-8"
        ) as f:

            st.text(f.read())

    else:

        st.write("No hay registros.")


# ==========================================
# 🧾 FOOTER
# ==========================================

st.markdown("© 2026 NHRX LABS · TENSHI")