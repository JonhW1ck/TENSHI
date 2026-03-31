# Interfaz gráfica de TENSHI — Streamlit

import streamlit as st
from modules.orchestrator import responder
from memory.memory import limpiar_historial
from memory.stats import obtener_stats
import os
import glob

st.set_page_config(
    page_title="TENSHI · NHRX LABS",
    page_icon="⚔️",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif !important;
    background-color: #080808 !important;
    color: #ffffff !important;
}

.stApp { background-color: #080808 !important; }

.nav-bar {
    display: flex; justify-content: space-between; align-items: center;
    padding: 14px 0; border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 24px;
}
.nav-kanji { font-size: 16px; color: rgba(204,34,0,0.8); letter-spacing: 3px; }
.nav-status { font-family: 'Share Tech Mono', monospace; font-size: 10px;
    color: rgba(255,255,255,0.3); letter-spacing: 2px; }

.msg-tenshi {
    background: #0f0f0f; border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px; padding: 12px 16px; margin: 8px 0;
    font-size: 15px; line-height: 1.7; color: rgba(255,255,255,0.85);
}
.msg-user {
    background: rgba(204,34,0,0.08); border: 1px solid rgba(204,34,0,0.2);
    border-radius: 8px; padding: 12px 16px; margin: 8px 0;
    font-size: 15px; line-height: 1.7; color: rgba(255,255,255,0.8);
    text-align: right;
}
.msg-label-tenshi {
    font-family: 'Share Tech Mono', monospace; font-size: 9px;
    letter-spacing: 3px; color: rgba(204,34,0,0.6); margin-bottom: 6px;
}
.msg-label-user {
    font-family: 'Share Tech Mono', monospace; font-size: 9px;
    letter-spacing: 3px; color: rgba(255,255,255,0.2);
    text-align: right; margin-bottom: 6px;
}
.tool-badge {
    display: inline-block; font-family: 'Share Tech Mono', monospace;
    font-size: 10px; color: rgba(204,34,0,0.6);
    border: 1px solid rgba(204,34,0,0.2); padding: 2px 8px;
    border-radius: 3px; margin-bottom: 8px;
}
.footer-bar {
    display: flex; justify-content: space-between;
    border-top: 1px solid rgba(255,255,255,0.04);
    padding: 10px 0; margin-top: 24px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px; color: rgba(255,255,255,0.12); letter-spacing: 2px;
}

/* Input styling */
.stTextInput > div > div > input {
    background: #0f0f0f !important; border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 6px !important; color: #fff !important;
    font-family: 'Rajdhani', sans-serif !important; font-size: 15px !important;
}
.stButton > button {
    background: rgba(204,34,0,0.8) !important; border: none !important;
    color: #fff !important; font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important; letter-spacing: 2px !important;
    border-radius: 6px !important; width: 100%;
}
.stButton > button:hover { background: #ff2900 !important; }
</style>
""", unsafe_allow_html=True)

# Navbar
st.markdown("""
<div class="nav-bar">
    <span class="nav-kanji">創造天使 · TENSHI</span>
    <span class="nav-status">⬤ GROQ · LLAMA-3.1 · ACTIVA</span>
</div>
""", unsafe_allow_html=True)

# Panel de estadísticas
stats = obtener_stats()
col_a, col_b, col_c, col_d, col_e = st.columns(5)
col_a.metric("💬 Mensajes", stats["mensajes_totales"])
col_b.metric("🔍 Búsquedas", stats["busquedas_internet"])
col_c.metric("🧮 Códigos", stats["codigos_ejecutados"])
col_d.metric("👁️ Imágenes", stats["imagenes_analizadas"])
col_e.metric("📁 Archivos", stats["archivos_leidos"])
st.markdown("<hr style='border:1px solid rgba(255,255,255,0.06);margin:0 0 16px;'>", unsafe_allow_html=True)

# Inicializar historial visual
if "mensajes_ui" not in st.session_state:
    st.session_state.mensajes_ui = []
    st.session_state.mensajes_ui.append({
        "rol": "tenshi",
        "texto": "Hola. Soy TENSHI. ¿En qué trabajamos hoy?"
    })

# Mostrar mensajes
for msg in st.session_state.mensajes_ui:
    if msg["rol"] == "tenshi":
        st.markdown(f'<div class="msg-label-tenshi">TENSHI</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="msg-tenshi">{msg["texto"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg-label-user">TÚ</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="msg-user">{msg["texto"]}</div>', unsafe_allow_html=True)

# Subir imagen
imagen_subida = st.file_uploader("", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")
if imagen_subida:
    ruta_imagen_temp = f"temp_{imagen_subida.name}"
    with open(ruta_imagen_temp, "wb") as f:
        f.write(imagen_subida.getbuffer())
    st.image(imagen_subida, width=200)
    st.session_state["imagen_path"] = ruta_imagen_temp
else:
    if "imagen_path" in st.session_state:
        del st.session_state["imagen_path"]

# Input
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    entrada = st.text_input("", placeholder="Escribe algo a TENSHI...", label_visibility="collapsed", key="input")
with col2:
    enviar = st.button("→ ENVIAR")

col3, col4 = st.columns([5, 1])
with col3:
    pass
with col4:
    if st.button("LIMPIAR"):
        limpiar_historial()
        st.session_state.mensajes_ui = []
        st.rerun()

# Procesar respuesta
if enviar and entrada.strip():
    mensaje = entrada
    if "imagen_path" in st.session_state:
        mensaje = f"{entrada} {st.session_state['imagen_path']}"
    st.session_state.mensajes_ui.append({"rol": "usuario", "texto": entrada})
    with st.spinner("TENSHI pensando..."):
        respuesta = responder(mensaje)
    st.session_state.mensajes_ui.append({"rol": "tenshi", "texto": respuesta})
    st.rerun()
# Historial de conversaciones
with st.expander("📅 HISTORIAL DE CONVERSACIONES"):
    archivos_log = sorted(glob.glob("logs/tenshi_*.txt"), reverse=True)
    if not archivos_log:
        st.markdown("<span style='color:rgba(255,255,255,0.3);font-size:13px;'>No hay conversaciones guardadas.</span>", unsafe_allow_html=True)
    else:
        fechas = [os.path.basename(f).replace("tenshi_","").replace(".txt","") for f in archivos_log]
        fecha_sel = st.selectbox("Selecciona una fecha", fechas, label_visibility="collapsed")
        archivo_sel = f"logs/tenshi_{fecha_sel}.txt"
        with open(archivo_sel, "r", encoding="utf-8-sig") as f:
            contenido = f.read()
        st.markdown(f"""
        <div style='background:#0f0f0f;border:1px solid rgba(255,255,255,0.06);
        border-radius:8px;padding:16px;font-family:Share Tech Mono,monospace;
        font-size:12px;color:rgba(255,255,255,0.6);white-space:pre-wrap;
        max-height:300px;overflow-y:auto;'>
        {contenido}
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-bar">
    <span>© 2026 NHRX LABS · TENSHI v1.0</span>
    <span>MEMORIA ACTIVA · LOGS ON</span>
</div>
""", unsafe_allow_html=True)