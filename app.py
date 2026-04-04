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
# ⚙️ CONFIG STREAMLIT — debe ir primero
# ==========================================

st.set_page_config(
    page_title="TENSHI · NHRX LABS",
    page_icon="⚔️",
    layout="centered"
)

# ==========================================
# 📱 PWA MANIFEST
# ==========================================

st.markdown("""
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#b8960c">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="TENSHI">
""", unsafe_allow_html=True)

# ==========================================
# 🎨 CSS — estética TorreIA
# ==========================================

def inyectar_css(ac: str, bg: str, modo: str):
    texto = "#111111" if modo == "dia" else "rgba(255,255,255,0.85)"
    superficie = "rgba(255,255,255,0.06)" if modo == "noche" else "rgba(0,0,0,0.04)"
    borde = "rgba(255,255,255,0.08)" if modo == "noche" else "rgba(0,0,0,0.08)"
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600&family=Noto+Serif+JP:wght@300;400&family=Share+Tech+Mono&display=swap');

    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {bg} !important;
        font-family: 'Rajdhani', sans-serif !important;
    }}
    [data-testid="stHeader"] {{ background: transparent !important; }}
    [data-testid="stMainBlockContainer"] {{ padding-top: 1rem !important; }}

    .tenshi-nav {{
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0; margin-bottom: 12px;
        border-bottom: 1px solid {borde};
    }}
    .tenshi-marca {{
        display: flex; align-items: center; gap: 10px;
    }}
    .tenshi-kanji {{
        font-family: 'Noto Serif JP', serif;
        font-size: 20px; color: {ac};
    }}
    .tenshi-nombre {{
        font-size: 14px; letter-spacing: 4px;
        color: {texto}; font-weight: 500;
    }}

    [data-testid="metric-container"] {{
        background: {superficie};
        border: 1px solid {borde};
        border-radius: 6px;
        padding: 8px 10px;
        text-align: center;
    }}
    [data-testid="stMetricValue"] {{
        font-family: 'Share Tech Mono', monospace !important;
        color: {ac} !important;
        font-size: 20px !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 9px !important;
        letter-spacing: 2px !important;
        color: {texto} !important;
        opacity: 0.4;
    }}

    .msg-tenshi {{
        background: {superficie};
        border: 1px solid {borde};
        border-radius: 0 10px 10px 10px;
        padding: 10px 14px;
        margin: 6px 0;
        font-size: 15px;
        color: {texto};
        line-height: 1.6;
    }}
    .msg-tenshi-label {{
        font-family: 'Share Tech Mono', monospace;
        font-size: 9px; letter-spacing: 3px;
        color: {ac}; margin-bottom: 4px;
    }}
    .msg-user {{
        background: {ac};
        border-radius: 10px 0 10px 10px;
        padding: 10px 14px;
        margin: 6px 0 6px auto;
        font-size: 15px;
        color: #fff;
        line-height: 1.6;
        text-align: right;
        max-width: 85%;
    }}

    [data-testid="stTextInput"] input {{
        background: {superficie} !important;
        border: 1px solid {borde} !important;
        border-radius: 6px !important;
        color: {texto} !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 15px !important;
    }}

    [data-testid="stButton"] button {{
        background: transparent !important;
        border: 1px solid {borde} !important;
        border-radius: 6px !important;
        color: {texto} !important;
        font-family: 'Rajdhani', sans-serif !important;
        letter-spacing: 1px !important;
        transition: all 0.2s !important;
    }}
    [data-testid="stButton"] button:hover {{
        border-color: {ac} !important;
        color: {ac} !important;
    }}

    [data-testid="stExpander"] {{
        background: {superficie} !important;
        border: 1px solid {borde} !important;
        border-radius: 6px !important;
    }}

    ::-webkit-scrollbar {{ width: 4px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: {ac}; border-radius: 2px; opacity: 0.5; }}

    .tenshi-footer {{
        text-align: center;
        font-size: 10px;
        letter-spacing: 3px;
        color: {texto};
        opacity: 0.2;
        margin-top: 20px;
        padding: 10px 0;
        border-top: 1px solid {borde};
    }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🎨 SESSION STATE — colores y modo
# ==========================================

if "color_acento" not in st.session_state:
    st.session_state.color_acento = "#cc2200"
if "color_fondo" not in st.session_state:
    st.session_state.color_fondo = "#080808"
if "modo" not in st.session_state:
    st.session_state.modo = "noche"
if "propuesta_pendiente" not in st.session_state:
    st.session_state.propuesta_pendiente = None

inyectar_css(
    st.session_state.color_acento,
    st.session_state.color_fondo,
    st.session_state.modo
)

# ==========================================
# 🔐 AUTENTICACIÓN
# ==========================================

def check_password():
    try:
        password_correcta = st.secrets.get("PASSWORD", "tenshi2026")
    except Exception:
        password_correcta = "tenshi2026"

    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.markdown("""
        <div style='text-align:center;padding:40px 0 20px;'>
            <span style='font-family:Noto Serif JP,serif;font-size:48px;'>⚔️</span>
            <h1 style='font-family:Rajdhani,sans-serif;letter-spacing:6px;margin:8px 0 4px;'>TENSHI</h1>
            <p style='font-size:10px;letter-spacing:4px;opacity:0.3;'>NHRX LABS · 創造天使</p>
        </div>
        """, unsafe_allow_html=True)
        pwd = st.text_input("Contraseña", type="password", placeholder="···")
        if st.button("ENTRAR →"):
            if pwd == password_correcta:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        st.stop()

check_password()

# ==========================================
# 🧹 LIMPIAR TEMPORALES
# ==========================================

def limpiar_temp_files():
    try:
        memory_dir = os.path.join(os.path.dirname(__file__), "memory")
        for archivo in os.listdir(memory_dir):
            if archivo.startswith("tmp"):
                ruta_tmp = os.path.join(memory_dir, archivo)
                if os.path.isfile(ruta_tmp):
                    os.remove(ruta_tmp)
    except Exception:
        pass

if "temp_cleaned" not in st.session_state:
    limpiar_temp_files()
    st.session_state.temp_cleaned = True

# ==========================================
# 🔔 HILO RECORDATORIOS
# ==========================================

if "hilo_recordatorios_iniciado" not in st.session_state:
    try:
        hilo = threading.Thread(target=recordatorios.revisar_recordatorios, daemon=True)
        hilo.start()
    except Exception as e:
        print("⚠️ Error iniciando hilo:", e)
    st.session_state.hilo_recordatorios_iniciado = True

# ==========================================
# 🧠 SESSION STATE — chat
# ==========================================

if "mensajes_ui" not in st.session_state:
    st.session_state.mensajes_ui = [
        {"rol": "assistant", "texto": "Hola. Soy TENSHI. ¿En qué trabajamos hoy?"}
    ]
if "procesando" not in st.session_state:
    st.session_state.procesando = False

# ==========================================
# 🏠 NAV BAR
# ==========================================

st.markdown("""
<div class='tenshi-nav'>
    <div class='tenshi-marca'>
        <span class='tenshi-kanji'>⚔</span>
        <span class='tenshi-nombre'>TENSHI</span>
    </div>
    <span style='font-family:Share Tech Mono,monospace;font-size:10px;letter-spacing:2px;opacity:0.3;'>NHRX LABS · 創造天使</span>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 📊 STATS
# ==========================================

try:
    stats = obtener_stats()
except Exception:
    stats = {
        "mensajes_totales": 0, "busquedas_internet": 0,
        "codigos_ejecutados": 0, "imagenes_analizadas": 0,
        "archivos_leidos": 0, "autoprogramaciones": 0,
    }

c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("MSGS",    stats.get("mensajes_totales",   0))
c2.metric("SEARCH",  stats.get("busquedas_internet", 0))
c3.metric("CODE",    stats.get("codigos_ejecutados", 0))
c4.metric("IMG",     stats.get("imagenes_analizadas",0))
c5.metric("FILES",   stats.get("archivos_leidos",    0))
c6.metric("AUTOPROG",stats.get("autoprogramaciones", 0))

st.markdown("<div style='margin:8px 0;'></div>", unsafe_allow_html=True)

# ==========================================
# 💬 CHAT
# ==========================================

MAX_UI_HISTORY = 40
st.session_state.mensajes_ui = st.session_state.mensajes_ui[-MAX_UI_HISTORY:]

for msg in st.session_state.mensajes_ui:
    if msg["rol"] == "assistant":
        st.markdown(f"""
        <div class='msg-tenshi'>
            <div class='msg-tenshi-label'>TENSHI</div>
            {msg['texto']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='msg-user'>{msg['texto']}</div>
        """, unsafe_allow_html=True)

# ==========================================
# 🖼️ IMAGEN
# ==========================================

imagen_subida = st.file_uploader(
    "", type=["jpg","jpeg","png","webp"],
    label_visibility="collapsed"
)
if imagen_subida:
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
        "", placeholder="Escribe algo a TENSHI...",
        label_visibility="collapsed"
    )
with colB:
    enviar = st.button("→", disabled=st.session_state.procesando)

colC, colD = st.columns([1,1])
with colC:
    if st.button("LIMPIAR"):
        limpiar_historial()
        st.session_state.mensajes_ui = [
            {"rol": "assistant", "texto": "Hola. Soy TENSHI. ¿En qué trabajamos hoy?"}
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

    st.session_state.mensajes_ui.append({"rol": "user", "texto": entrada})

    try:
        with st.spinner("···"):
            respuesta = responder(mensaje)
    except Exception:
        traceback.print_exc()
        respuesta = "⚠️ Error interno."

    st.session_state.mensajes_ui.append({"rol": "assistant", "texto": respuesta})

    try:
        propuesta = analizar_y_proponer()
        if propuesta:
            st.session_state.propuesta_pendiente = propuesta
    except Exception:
        pass

    if "imagen_path" in st.session_state:
        try:
            os.remove(st.session_state["imagen_path"])
        except Exception:
            pass
        del st.session_state["imagen_path"]

    st.session_state.procesando = False
    st.rerun()

# ==========================================
# 🤖 PROPUESTA AUTÓNOMA DE CRECIMIENTO
# ==========================================

if st.session_state.propuesta_pendiente:
    propuesta = st.session_state.propuesta_pendiente
    st.markdown(f"""
    <div class='msg-tenshi'>
        <div class='msg-tenshi-label'>TENSHI · PROPUESTA AUTÓNOMA</div>
        {propuesta}
    </div>
    """, unsafe_allow_html=True)
    col_ap, col_ig = st.columns([1,1])
    with col_ap:
        if st.button("✅ Aprobar"):
            st.session_state.mensajes_ui.append({"rol": "user", "texto": propuesta})
            with st.spinner("···"):
                respuesta = responder(propuesta)
            st.session_state.mensajes_ui.append({"rol": "assistant", "texto": respuesta})
            st.session_state.propuesta_pendiente = None
            st.rerun()
    with col_ig:
        if st.button("❌ Ignorar"):
            st.session_state.propuesta_pendiente = None
            st.rerun()

# ==========================================
# 🎨 PANEL DE PERSONALIZACIÓN
# ==========================================

with st.expander("🎨 Personalizar"):
    col_a, col_b, col_c = st.columns([1,1,1])
    with col_a:
        nuevo_acento = st.color_picker("Color acento", st.session_state.color_acento)
    with col_b:
        nuevo_fondo = st.color_picker("Color fondo", st.session_state.color_fondo)
    with col_c:
        modo_label = "🌙 Noche" if st.session_state.modo == "noche" else "☀️ Día"
        if st.button(modo_label):
            st.session_state.modo = "dia" if st.session_state.modo == "noche" else "noche"
            if st.session_state.modo == "dia":
                st.session_state.color_fondo = "#f5f5f0"
            else:
                st.session_state.color_fondo = "#080808"
            st.rerun()

    if nuevo_acento != st.session_state.color_acento or nuevo_fondo != st.session_state.color_fondo:
        st.session_state.color_acento = nuevo_acento
        st.session_state.color_fondo  = nuevo_fondo
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
# 📜 HISTORIAL
# ==========================================

with st.expander("📅 Historial"):
    archivos = sorted(glob.glob("logs/tenshi_*.txt"), reverse=True)
    if archivos:
        fechas = [os.path.basename(f).replace("tenshi_","").replace(".txt","") for f in archivos]
        fecha  = st.selectbox("Fecha", fechas)
        with open(f"logs/tenshi_{fecha}.txt", "r", encoding="utf-8") as f:
            st.text(f.read())
    else:
        st.write("No hay registros.")

# ==========================================
# 🧾 FOOTER
# ==========================================

st.markdown("<div class='tenshi-footer'>© 2026 NHRX LABS · TENSHI · 創造天使</div>", unsafe_allow_html=True)