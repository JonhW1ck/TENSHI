# ==========================================
# MÓDULO DE SINCRONIZACIÓN CON GITHUB
# github_sync.py
# ==========================================
import os
import base64
import json
from datetime import datetime

try:
    import requests
except ImportError:
    requests = None


def _obtener_config():
    """Lee token y repo desde secrets de Streamlit o variables de entorno."""
    try:
        import streamlit as st
        token = st.secrets.get("GITHUB_TOKEN", "")
        repo  = st.secrets.get("GITHUB_REPO", "")
    except Exception:
        token = os.getenv("GITHUB_TOKEN", "")
        repo  = os.getenv("GITHUB_REPO", "")
    return token, repo


def _headers(token: str) -> dict:
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }


def _obtener_sha(token: str, repo: str, ruta_archivo: str) -> str | None:
    """Obtiene el SHA del archivo si ya existe en el repo (necesario para actualizar)."""
    url = f"https://api.github.com/repos/{repo}/contents/{ruta_archivo}"
    resp = requests.get(url, headers=_headers(token))
    if resp.status_code == 200:
        return resp.json().get("sha")
    return None


def commit_modulo(nombre_modulo: str, codigo: str, carpeta: str = "modules") -> dict:
    """
    Sube o actualiza un módulo Python al repositorio de GitHub.

    Args:
        nombre_modulo: nombre sin extensión (ej: 'calculadora_cientifica')
        codigo: contenido del archivo Python
        carpeta: carpeta destino dentro del repo (default: 'modules')

    Returns:
        dict con 'exito', 'mensaje' y 'url' del archivo en GitHub
    """
    if requests is None:
        return {"exito": False, "mensaje": "Librería 'requests' no disponible."}

    token, repo = _obtener_config()

    if not token or not repo:
        return {"exito": False, "mensaje": "GITHUB_TOKEN o GITHUB_REPO no configurados en secrets."}

    ruta_archivo = f"{carpeta}/{nombre_modulo}.py"
    url          = f"https://api.github.com/repos/{repo}/contents/{ruta_archivo}"
    contenido_b64 = base64.b64encode(codigo.encode("utf-8")).decode("utf-8")
    fecha         = datetime.now().strftime("%Y-%m-%d %H:%M")
    mensaje_commit = f"feat: módulo {nombre_modulo} generado por TENSHI [{fecha}]"

    payload = {
        "message": mensaje_commit,
        "content": contenido_b64,
    }

    # Si el archivo ya existe hay que incluir su SHA para actualizarlo
    sha = _obtener_sha(token, repo, ruta_archivo)
    if sha:
        payload["sha"] = sha

    resp = requests.put(url, headers=_headers(token), data=json.dumps(payload))

    if resp.status_code in (200, 201):
        html_url = resp.json().get("content", {}).get("html_url", "")
        accion   = "actualizado" if sha else "creado"
        return {
            "exito":   True,
            "mensaje": f"✅ Módulo '{nombre_modulo}.py' {accion} en GitHub.",
            "url":     html_url,
        }
    else:
        return {
            "exito":   False,
            "mensaje": f"❌ Error GitHub {resp.status_code}: {resp.text[:200]}",
        }


def listar_modulos_remotos(carpeta: str = "modules") -> list:
    """
    Lista los archivos .py que existen en la carpeta del repo remoto.
    """
    if requests is None:
        return []

    token, repo = _obtener_config()
    if not token or not repo:
        return []

    url  = f"https://api.github.com/repos/{repo}/contents/{carpeta}"
    resp = requests.get(url, headers=_headers(token))

    if resp.status_code == 200:
        archivos = resp.json()
        return [a["name"] for a in archivos if a["name"].endswith(".py")]
    return []