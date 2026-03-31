# Interfaz gráfica de TENSHI — Streamlit

import streamlit as st
import os
import glob
from datetime import datetime

from modules.orchestrator import responder
from modules.autonomy import analizar_y_proponer

from memory.memory import limpiar_historial
from memory.stats import obtener_stats

from logs.logger import guardar_log


# ==========================================
# CONFIGURACIÓN STREAMLIT
# ==========================================

st.set_page_config(
    page_title="TENSHI · NHRX LABS",
    page_icon="⚔️",
    layout="centered"
)


# ==========================================
# ESTADO DE SESIÓN
# ==========================================

if "mensajes_ui" not in st.session_state:
    st.session_state.mensajes_ui = [{
        "rol": "tenshi",
        "texto": "Hola. Soy TENSHI. ¿En qué trabajamos hoy?"
    }]

if "procesando" not in st.session_state:
    st.session_state.procesando = False


# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
font-family: 'Rajdhani', sans-serif !important;
background-color: #080808 !important;
color: #ffffff !important;
}

.nav-bar {
display:flex;
justify-content:space-between;
align-items:center;
padding:14px 0;
border-bottom:1px solid rgba(255,255,255,0.06);
margin-bottom:24px;
}

.nav-kanji {
font-size:16px;
color:rgba(204,34,0,0.8);
letter-spacing:3px;
}

.nav-status {
font-family:'Share Tech Mono', monospace;
font-size:10px;
color:rgba(255,255,255,0.3);
letter-spacing:2px;
}

.msg-tenshi {
background:#0f0f0f;
border:1px solid rgba(255,255,255,0.06);
border-radius:8px;
padding:12px 16px;
margin:8px 0;
font-size:15px;
line-height:1.7;
color:rgba(255,255,255,0.85);
}

.msg-user {
background:rgba(204,34,0,0.08);
border:1px solid rgba(204,34,0,0.2);
border-radius:8px;
padding:12px 16px;
margin:8px 0;
font-size:15px;
line-height:1.7;
color:rgba(255,255,255,0.8);
text-align:right;
}

.msg-label-tenshi {
font-family:'Share Tech Mono', monospace;
font-size:9px;
letter-spacing:3px;
color:rgba(204,34,0,0.6);
margin-bottom:6px;
}

.msg-label-user {
font-family:'Share Tech Mono', monospace;
font-size:9px;
letter-spacing:3px;
color:rgba(255,255,255,0.2);
text-align:right;
margin-bottom:6px;
}

.footer-bar {
display:flex;
justify-content:space-between;
border-top:1px solid rgba(255,255,255,0.04);
padding:10px 0;
margin-top:24px;
font-family:'Share Tech Mono', monospace;
font-size:9px;
color:rgba(255,255,255,0.12);
letter-spacing:2px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# NAVBAR
# ==========================================

st.markdown("""
<div class="nav-bar">
<span class="nav-kanji">創造天使 · TENSHI</span>
<span class="nav-status">⬤ GROQ · ACTIVA</span>
</div>
""", unsafe_allow_html=True)


# ==========================================
# ESTADÍSTICAS
# ==========================================

stats = obtener_stats()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💬 Mensajes", stats["mensajes_totales"])
col2.metric("🔍 Búsquedas", stats["busquedas_internet"])
col3.metric("🧮 Código", stats["codigos_ejecutados"])
col4.metric("👁️ Imágenes", stats["imagenes_analizadas"])
col5.metric("📁 Archivos", stats["archivos_leidos"])

st.markdown("<hr>", unsafe_allow_html=True)


# ==========================================
# MOSTRAR CHAT
# ==========================================

MAX_UI_HISTORY = 40
st.session_state.mensajes_ui = st.session_state.mensajes_ui[-MAX_UI_HISTORY:]

for msg in st.session_state.mensajes_ui:

    if msg["rol"] == "tenshi":

        st.markdown('<div class="msg-label-tenshi">TENSHI</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="msg-tenshi">{msg["texto"]}</div>', unsafe_allow_html=True)

    else:

        st.markdown('<div class="msg-label-user">TÚ</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="msg-user">{msg["texto"]}</div>', unsafe_allow_html=True)


# ==========================================
# SUBIR IMAGEN
# ==========================================

imagen_subida = st.file_uploader("", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")

if imagen_subida:

    ruta_imagen_temp = f"temp_{imagen_subida.name}"

    with open(ruta_imagen_temp, "wb") as f:
        f.write(imagen_subida.getbuffer())

    st.image(imagen_subida, width=200)

    st.session_state["imagen_path"] = ruta_imagen_temp


# ==========================================
# INPUT
# ==========================================

colA, colB = st.columns([5,1])

with colA:
    entrada = st.text_input(
        "",
        placeholder="Escribe algo a TENSHI...",
        label_visibility="collapsed"
    )

with colB:
    enviar = st.button("→", disabled=st.session_state.procesando)


# ==========================================
# LIMPIAR CHAT
# ==========================================

colC, colD = st.columns([5,1])

with colD:

    if st.button("LIMPIAR"):

        limpiar_historial()
        st.session_state.mensajes_ui = []
        st.rerun()


# ==========================================
# PROCESAR MENSAJE
# ==========================================

if enviar and entrada.strip() and not st.session_state.procesando:

    st.session_state.procesando = True

    mensaje = entrada

    if "imagen_path" in st.session_state:
        mensaje = f"{entrada} {st.session_state['imagen_path']}"

    st.session_state.mensajes_ui.append({
        "rol": "user",
        "texto": entrada
    })

    try:

        with st.spinner("TENSHI pensando..."):

            respuesta = responder(mensaje)

    except Exception as e:

        respuesta = f"⚠️ Error interno:\n\n{str(e)}"

    st.session_state.mensajes_ui.append({
        "rol": "tenshi",
        "texto": respuesta
    })

    guardar_log(entrada, respuesta)


    # ======================================
    # AUTONOMÍA
    # ======================================

    try:

        propuesta = analizar_y_proponer()

        if propuesta:

            st.session_state.mensajes_ui.append({
                "rol": "tenshi",
                "texto": f"💡 Propuesta de mejora:\n\n{propuesta}\n\nResponde **SI** para aprobar o **NO** para ignorar."
            })

    except:
        pass


    # ======================================
    # LIMPIAR IMAGEN
    # ======================================

    if "imagen_path" in st.session_state:

        try:
            os.remove(st.session_state["imagen_path"])
        except:
            pass

        del st.session_state["imagen_path"]

    st.session_state.procesando = False

    st.rerun()


# ==========================================
# HISTORIAL LOGS
# ==========================================

with st.expander("📅 HISTORIAL DE CONVERSACIONES"):

    archivos = sorted(glob.glob("logs/tenshi_*.txt"), reverse=True)

    if not archivos:

        st.write("No hay conversaciones guardadas.")

    else:

        fechas = [os.path.basename(f).replace("tenshi_","").replace(".txt","") for f in archivos]

        fecha = st.selectbox("Selecciona fecha", fechas)

        archivo = f"logs/tenshi_{fecha}.txt"

        with open(archivo,"r",encoding="utf-8-sig") as f:
            contenido = f.read()

        st.text(contenido)


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer-bar">
<span>© 2026 NHRX LABS · TENSHI</span>
<span>MEMORIA ACTIVA</span>
</div>
""", unsafe_allow_html=True)