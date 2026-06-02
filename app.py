import streamlit as st
import pandas as pd
from datetime import date, datetime
import json
import os
import sqlite3
import folium
import base64
import hashlib
import smtplib
import re
import requests
from PIL import Image as PILImage
import pdfplumber
import pytesseract

# ─────────────────────────────────────────────
# TESSERACT — caminho para Windows
# ─────────────────────────────────────────────
import platform
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from reportlab.platypus import PageBreak
from streamlit_js_eval import get_geolocation
from streamlit_folium import st_folium
from folium.plugins import Draw
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ─────────────────────────────────────────────
# CORREÇÃO 1: função sem recursão infinita
# ─────────────────────────────────────────────
def adicionar_logo_fundo():
    if not os.path.exists("IAAgrologo.jpeg"):
        return
    with open("IAAgrologo.jpeg", "rb") as imagem:
        encoded = base64.b64encode(imagem.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                linear-gradient(rgba(7, 18, 35, 0.88), rgba(11, 26, 46, 0.88)),
                url("data:image/jpeg;base64,{encoded}") !important;
            background-repeat: no-repeat !important;
            background-position: center center !important;
            background-size: cover !important;
            background-attachment: fixed !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

adicionar_logo_fundo()

# ─────────────────────────────────────────────
# CSS UNIFICADO (sem conflitos e sem duplicatas)
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ══════════════════════════════════════════
   RESET GERAL — evita fundo branco do Streamlit
══════════════════════════════════════════ */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="block-container"],
.main, .stApp {
    background-color: #0d2137 !important;
    color: #f1f5f9 !important;
}

/* ── FUNDO GERAL ── */
.stApp {
    background: linear-gradient(160deg, #0d2137 0%, #123354 50%, #1a4a73 100%) !important;
}

/* ── TEXTO GERAL ── */
p, span, div, li, label,
.stMarkdown p, .stMarkdown li,
[data-testid="stText"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] {
    color: #f1f5f9 !important;
}

/* ── TÍTULOS ── */
h1, h2, h3, h4, h5, h6 {
    color: #6ee7b7 !important;
    font-weight: 800 !important;
}

/* ── LABELS DE CAMPOS ── */
label, .stTextInput label, .stNumberInput label,
.stSelectbox label, .stTextArea label,
.stDateInput label, .stSlider label,
.stFileUploader label, .stRadio label,
.stCheckbox label, .stMultiSelect label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] {
    color: #6ee7b7 !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}

/* ── INPUTS TEXT / NUMBER ── */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: #0f3460 !important;
    color: #ffffff !important;
    border: 2px solid #22c55e !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}
.stTextInput input::placeholder,
.stNumberInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #64748b !important;
}

/* ── SELECTBOX ── */
.stSelectbox [data-baseweb="select"] > div {
    background: #0f3460 !important;
    color: #ffffff !important;
    border: 2px solid #22c55e !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}
.stSelectbox [data-baseweb="select"] span,
.stSelectbox [data-baseweb="select"] div,
.stSelectbox [data-baseweb="select"] * {
    color: #ffffff !important;
}
[data-baseweb="popover"] li,
[data-baseweb="menu"] li {
    color: #0f172a !important;
    background: #f8fafc !important;
    font-weight: 600 !important;
}
[data-baseweb="popover"] li:hover,
[data-baseweb="menu"] li:hover {
    background: #bbf7d0 !important;
}

/* ── DATE INPUT ── */
.stDateInput input {
    background: #0f3460 !important;
    color: #ffffff !important;
    border: 2px solid #22c55e !important;
    border-radius: 10px !important;
}

/* ── TEXTAREA ── */
.stTextArea textarea {
    background: #0f3460 !important;
    color: #ffffff !important;
    border: 2px solid #22c55e !important;
    border-radius: 10px !important;
}

/* ── NÚMERO (botões +/-) ── */
.stNumberInput button {
    background: #1a4a73 !important;
    color: #ffffff !important;
    border: 1px solid #60a5fa !important;
    border-radius: 6px !important;
}

/* ── BOTÕES ── */
.stButton > button {
    background: linear-gradient(135deg, #00c853, #16a34a) !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    font-size: 16px !important;
    font-weight: bold !important;
    padding: 10px 22px !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00e676, #15803d) !important;
}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background-color: #16a34a !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 12px 20px !important;
    font-size: 16px !important;
    font-weight: bold !important;
    width: 100% !important;
}

/* ── MÉTRICAS ── */
div[data-testid="stMetric"] {
    background: #1a4a73 !important;
    border-radius: 16px !important;
    padding: 16px !important;
    border: 1px solid #60a5fa !important;
}
div[data-testid="stMetric"] * { color: #f1f5f9 !important; }
div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 900 !important;
    font-size: 26px !important;
}
div[data-testid="stMetricLabel"] {
    color: #93c5fd !important;
    font-weight: 700 !important;
    font-size: 13px !important;
}

/* ── DATAFRAMES ── */
[data-testid="stDataFrame"] {
    background: #ffffff !important;
    border-radius: 12px !important;
    border: 2px solid #3b82f6 !important;
}
[data-testid="stDataFrame"] * { color: #0f172a !important; }
[data-testid="stDataFrame"] th {
    color: #0f172a !important;
    background: #bfdbfe !important;
    font-weight: 800 !important;
    font-size: 13px !important;
}
[data-testid="stDataFrame"] td {
    color: #0f172a !important;
    background: #f8fafc !important;
    font-size: 13px !important;
}

/* ── ALERTAS ── */
.stAlert {
    border-radius: 12px !important;
    font-weight: 600 !important;
}
.stAlert *, .stAlert p, .stAlert div, .stAlert span {
    color: #0f172a !important;
    font-weight: 600 !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid #1e3a5f !important;
}
.stTabs [data-baseweb="tab"] {
    color: #93c5fd !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #6ee7b7 !important;
    border-bottom: 3px solid #6ee7b7 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader,
[data-testid="stExpander"] summary {
    color: #6ee7b7 !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    background: #0f3460 !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] {
    background: #0f3460 !important;
    border: 1px solid #1e5799 !important;
    border-radius: 10px !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: #0a1f35 !important;
}
[data-testid="stSidebar"] * { color: #f1f5f9 !important; }
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] label {
    color: #6ee7b7 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

/* ── PROGRESS BAR ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #00c853, #16a34a) !important;
    border-radius: 10px !important;
}
.stProgress > div {
    background: #1a4a73 !important;
    border-radius: 10px !important;
}

/* ── UPLOAD ── */
section[data-testid="stFileUploader"] { background: transparent !important; }
div[data-testid="stFileUploaderDropzone"] {
    background: #0f3460 !important;
    border: 2px solid #22c55e !important;
    border-radius: 12px !important;
    padding: 20px !important;
}
div[data-testid="stFileUploaderDropzone"] * {
    color: #ffffff !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}
/* Texto "Drag and drop" e instruções */
div[data-testid="stFileUploaderDropzone"] span,
div[data-testid="stFileUploaderDropzone"] p,
div[data-testid="stFileUploaderDropzone"] small {
    color: #ffffff !important;
    font-size: 14px !important;
}
/* Botão Browse/Upload */
div[data-testid="stFileUploaderDropzone"] button,
div[data-testid="stFileUploaderDropzone"] [data-testid="baseButton-secondary"] {
    background: linear-gradient(135deg, #16a34a, #15803d) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 8px 18px !important;
}
div[data-testid="stFileUploaderDropzone"] button:hover {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
}
/* Ícone de upload */
div[data-testid="stFileUploaderDropzone"] svg {
    fill: #22c55e !important;
    stroke: #22c55e !important;
}

/* ── INFO BOX dentro do st.info ── */
[data-testid="stNotification"] * { color: #0f172a !important; }

/* ── DIVIDER ── */
hr { border-color: #1e3a5f !important; }

/* ── RADIO ── */
.stRadio > div { background: transparent !important; }
.stRadio [data-testid="stWidgetLabel"] p { color: #6ee7b7 !important; }

/* ── CHECKBOX ── */
.stCheckbox label p { color: #f1f5f9 !important; }

/* ── MULTISELECT ── */
/* Campo principal */
.stMultiSelect [data-baseweb="select"] > div {
    background: #0f3460 !important;
    border: 2px solid #22c55e !important;
    border-radius: 10px !important;
    color: #ffffff !important;
}
/* Tags selecionadas */
.stMultiSelect [data-baseweb="tag"] {
    background: #1a4a73 !important;
    color: #ffffff !important;
    border-radius: 6px !important;
}
.stMultiSelect [data-baseweb="tag"] span {
    color: #ffffff !important;
}
/* Placeholder */
.stMultiSelect [data-baseweb="select"] input {
    color: #ffffff !important;
}
/* Dropdown aberto — fundo e texto dos itens */
[data-baseweb="popover"] [role="option"],
[data-baseweb="menu"] [role="option"],
[data-baseweb="popover"] ul li,
[data-baseweb="menu"] ul li,
[data-baseweb="popover"] li,
[data-baseweb="menu"] li {
    background: #0f2744 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}
/* Hover dos itens */
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="menu"] [role="option"]:hover,
[data-baseweb="popover"] li:hover,
[data-baseweb="menu"] li:hover {
    background: #1a4a73 !important;
    color: #6ee7b7 !important;
}
/* Item selecionado/ativo */
[data-baseweb="popover"] [aria-selected="true"],
[data-baseweb="menu"] [aria-selected="true"] {
    background: #14532d !important;
    color: #ffffff !important;
}
/* "Selecionar todos" */
[data-baseweb="popover"] [role="option"]:first-child,
[data-baseweb="menu"] [role="option"]:first-child {
    background: #1e3a5f !important;
    color: #93c5fd !important;
    font-weight: 700 !important;
    border-bottom: 1px solid #3b82f6 !important;
}
/* Fundo do container do dropdown */
[data-baseweb="popover"] > div,
[data-baseweb="menu"] > div {
    background: #0f2744 !important;
    border: 1px solid #3b82f6 !important;
    border-radius: 10px !important;
}
/* "Sem resultados" quando todos selecionados */
[data-baseweb="popover"] [role="listbox"] > div,
[data-baseweb="menu"] [role="listbox"] > div,
[data-baseweb="popover"] ul,
[data-baseweb="menu"] ul {
    background: #0f2744 !important;
}
[data-baseweb="popover"] p,
[data-baseweb="menu"] p,
[data-baseweb="popover"] span:not([data-baseweb="tag"] span),
[data-baseweb="popover"] div > p {
    color: #93c5fd !important;
    background: #0f2744 !important;
}
/* Texto "Sem resultados" */
[data-baseweb="popover"] [role="listbox"]:empty::after,
[data-baseweb="popover"] ul:empty::after {
    content: "✅ Todos selecionados" !important;
    color: #6ee7b7 !important;
    display: block !important;
    padding: 12px 18px !important;
    font-weight: 600 !important;
}
/* Garante fundo escuro em qualquer div filho do popover */
[data-baseweb="popover"] * {
    background-color: transparent !important;
}
[data-baseweb="popover"] > div > div {
    background: #0f2744 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS DE NOTIFICAÇÃO — garantem legibilidade
# ─────────────────────────────────────────────
def info_box(msg):
    st.markdown(f'<div style="background:#1e3a5f;color:#ffffff;padding:13px 18px;border-radius:10px;'
                f'border-left:5px solid #3b82f6;font-weight:600;font-size:15px;margin:6px 0;">'
                f'ℹ️ {msg}</div>', unsafe_allow_html=True)

def success_box(msg):
    st.markdown(f'<div style="background:#14532d;color:#ffffff;padding:13px 18px;border-radius:10px;'
                f'border-left:5px solid #22c55e;font-weight:600;font-size:15px;margin:6px 0;">'
                f'✅ {msg}</div>', unsafe_allow_html=True)

def warning_box(msg):
    st.markdown(f'<div style="background:#78350f;color:#ffffff;padding:13px 18px;border-radius:10px;'
                f'border-left:5px solid #f59e0b;font-weight:600;font-size:15px;margin:6px 0;">'
                f'⚠️ {msg}</div>', unsafe_allow_html=True)

def error_box(msg):
    st.markdown(f'<div style="background:#7f1d1d;color:#ffffff;padding:13px 18px;border-radius:10px;'
                f'border-left:5px solid #ef4444;font-weight:600;font-size:15px;margin:6px 0;">'
                f'❌ {msg}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ARQUIVOS DE PERSISTÊNCIA
# ─────────────────────────────────────────────
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_ESTOQUE  = "estoque.json"
ARQUIVO_AREAS    = "areas.json"
ARQUIVO_DADOS_IAAGRO = "dados_iaagro.json"
DB_FILE              = "iaagro.db"

# ─────────────────────────────────────────────
# CORREÇÃO 9: senhas com hash (hashlib)
# ─────────────────────────────────────────────
def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    return hash_senha(senha) == hash_armazenado

# ─────────────────────────────────────────────
# BANCO DE DADOS SQLITE — histórico de solo
# ─────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS historico_solo ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "id_area TEXT, data TEXT,"
        "ph REAL, fosforo REAL, potassio REAL, materia_organica REAL,"
        "calcio REAL, magnesio REAL, aluminio REAL, enxofre REAL,"
        "ctc REAL, argila REAL, nota INTEGER, score INTEGER, classe TEXT)"
    )
    conn.commit()
    conn.close()

def salvar_analise_solo_db(id_area, dados, nota, score, classe):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(
            "INSERT INTO historico_solo "
            "(id_area,data,ph,fosforo,potassio,materia_organica,calcio,magnesio,"
            "aluminio,enxofre,ctc,argila,nota,score,classe) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (id_area, str(date.today()),
             dados.get("ph",0), dados.get("fosforo",0), dados.get("potassio",0),
             dados.get("materia_organica",0), dados.get("calcio",0),
             dados.get("magnesio",0), dados.get("aluminio",0),
             dados.get("enxofre",0), dados.get("ctc",0),
             dados.get("argila",0), nota, score, classe))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def carregar_historico_solo_db(id_area):
    try:
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql_query(
            "SELECT * FROM historico_solo WHERE id_area=? ORDER BY data DESC",
            conn, params=(id_area,))
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

# ─────────────────────────────────────────────
# VALIDAÇÃO DE CAMPOS
# ─────────────────────────────────────────────
def validar_ph(v):
    return 3.5 <= v <= 9.0

def validar_email_fmt(email):
    return bool(re.match(r'^[^@]+@[^@]+\.[^@]+$', email))

# ─────────────────────────────────────────────
# EXPORTAR XLSX
# ─────────────────────────────────────────────
def exportar_excel(dados_dict: dict):
    output = BytesIO()
    try:
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for aba, dados in dados_dict.items():
                if dados:
                    rows = dados if isinstance(dados, list) else [dados]
                    pd.DataFrame(rows).to_excel(writer, sheet_name=aba[:31], index=False)
        return output.getvalue()
    except Exception as e:
        return None

# ─────────────────────────────────────────────
# BACKUP / RESTORE
# ─────────────────────────────────────────────
def gerar_backup():
    dados = {
        "usuarios":  st.session_state.get("usuarios", {}),
        "dados":     st.session_state.get("dados", {}),
        "areas":     st.session_state.get("areas", []),
        "estoque":   st.session_state.get("estoque", []),
        "aplicacoes":st.session_state.get("aplicacoes", []),
        "historico_produtividade": st.session_state.get("historico_produtividade", []),
        "pluviometro":        st.session_state.get("pluviometro", []),
        "carencia_registros": st.session_state.get("carencia_registros", []),
        "dre_registros":      st.session_state.get("dre_registros", []),
        "calendario_eventos": st.session_state.get("calendario_eventos", []),
        "backup_data": str(datetime.now())
    }
    return json.dumps(dados, ensure_ascii=False, indent=2).encode("utf-8")

def restaurar_backup(arquivo):
    try:
        dados = json.loads(arquivo.read().decode("utf-8"))
        st.session_state.usuarios = dados.get("usuarios", {})
        st.session_state.dados    = dados.get("dados", {})
        st.session_state.areas    = dados.get("areas", [])
        st.session_state.estoque  = dados.get("estoque", [])
        st.session_state.aplicacoes = dados.get("aplicacoes", [])
        st.session_state.historico_produtividade = dados.get("historico_produtividade", [])
        st.session_state.pluviometro        = dados.get("pluviometro", [])
        st.session_state.carencia_registros  = dados.get("carencia_registros", [])
        st.session_state.dre_registros       = dados.get("dre_registros", [])
        st.session_state.calendario_eventos  = dados.get("calendario_eventos", [])
        salvar_dados_iaagro()
        salvar_usuarios(st.session_state.usuarios)
        return True, f"Backup de {dados.get('backup_data','?')} restaurado!"
    except Exception as e:
        return False, f"Erro ao restaurar: {e}"

# ─────────────────────────────────────────────
# EMAIL SMTP — alertas de estoque
# ─────────────────────────────────────────────
def enviar_email_alerta(destinatario, assunto, corpo):
    try:
        cfg = st.session_state.get("email_config", {})
        if not cfg.get("ativo") or not cfg.get("remetente"):
            return False
        msg = MIMEMultipart()
        msg["From"]    = cfg["remetente"]
        msg["To"]      = destinatario
        msg["Subject"] = assunto
        msg.attach(MIMEText(corpo, "html"))
        with smtplib.SMTP(cfg.get("smtp","smtp.gmail.com"), int(cfg.get("porta",587))) as s:
            s.starttls()
            s.login(cfg["remetente"], cfg.get("senha",""))
            s.send_message(msg)
        return True
    except Exception:
        return False

def checar_alertas_estoque():
    cfg = st.session_state.get("email_config", {})
    if not cfg.get("ativo") or not cfg.get("email_destino"):
        return
    zerados = [i for i in st.session_state.estoque if i.get("Quantidade",0) <= 0]
    baixos  = [i for i in st.session_state.estoque
               if 0 < i.get("Quantidade",0) <= i.get("Estoque Mínimo",0)]
    if zerados or baixos:
        corpo = "<h2>⚠️ IAAgro Pro — Alerta de Estoque</h2><ul>"
        for i in zerados:
            corpo += f"<li>❌ <b>{i['Insumo']}</b>: estoque ZERADO</li>"
        for i in baixos:
            corpo += f"<li>⚠️ <b>{i['Insumo']}</b>: {i['Quantidade']:.1f} (mín: {i['Estoque Mínimo']:.1f})</li>"
        corpo += "</ul><p>Acesse o IAAgro Pro para repor o estoque.</p>"
        enviar_email_alerta(cfg["email_destino"], "⚠️ IAAgro — Alerta de Estoque", corpo)


# ─────────────────────────────────────────────
# CLIMA EM TEMPO REAL — Open-Meteo (gratuito, sem API key)
# ─────────────────────────────────────────────
def buscar_clima(lat, lon):
    """Busca clima atual via Open-Meteo API (gratuita, sem chave)."""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,precipitation,"
            f"windspeed_10m,weathercode"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
            f"windspeed_10m_max"
            f"&timezone=America%2FSao_Paulo&forecast_days=7"
        )
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None

def codigo_clima_emoji(code):
    """Converte weathercode Open-Meteo em emoji + descrição."""
    mapa = {
        0: ("☀️", "Céu limpo"), 1: ("🌤️", "Principalmente limpo"),
        2: ("⛅", "Parcialmente nublado"), 3: ("☁️", "Nublado"),
        45: ("🌫️", "Névoa"), 48: ("🌫️", "Névoa com geada"),
        51: ("🌦️", "Garoa leve"), 53: ("🌦️", "Garoa moderada"),
        55: ("🌧️", "Garoa intensa"), 61: ("🌧️", "Chuva leve"),
        63: ("🌧️", "Chuva moderada"), 65: ("🌧️", "Chuva intensa"),
        71: ("🌨️", "Neve leve"), 73: ("🌨️", "Neve moderada"),
        75: ("❄️", "Neve intensa"), 80: ("🌦️", "Chuva rápida leve"),
        81: ("🌧️", "Chuva rápida moderada"), 82: ("⛈️", "Chuva rápida intensa"),
        95: ("⛈️", "Trovoada"), 96: ("⛈️", "Trovoada com granizo"),
        99: ("⛈️", "Trovoada intensa"),
    }
    return mapa.get(code, ("🌡️", "Desconhecido"))

def alerta_clima_aplicacao(codigo_clima, velocidade_vento, precipitacao):
    """Retorna alerta se o clima não é ideal para aplicação."""
    alertas = []
    if precipitacao > 0:
        alertas.append("🌧️ Chuva detectada — evite aplicações!")
    if velocidade_vento > 15:
        alertas.append(f"💨 Vento alto ({velocidade_vento:.1f} km/h) — risco de deriva!")
    if codigo_clima in [95, 96, 99]:
        alertas.append("⛈️ Trovoada — NÃO faça aplicações!")
    return alertas

# ─────────────────────────────────────────────
# PREÇOS DE COMMODITIES — CEPEA/ESALQ via scraping
# ─────────────────────────────────────────────
def buscar_precos_commodities():
    """Busca preços simulados com fallback para dados estáticos."""
    try:
        # Tenta API pública de grãos (HG Brasil)
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(
            "https://api.hgbrasil.com/finance/stock_price?key=demo&symbol=SOJA3,MILH3",
            headers=headers, timeout=6
        )
        if r.status_code == 200:
            dados = r.json()
            return dados
    except Exception:
        pass
    # Fallback: retorna referência CEPEA aproximada
    return {
        "soja_sc":  {"preco": 135.0, "fonte": "Referência CEPEA (offline)"},
        "milho_sc": {"preco": 68.0,  "fonte": "Referência CEPEA (offline)"},
        "trigo_sc": {"preco": 95.0,  "fonte": "Referência CEPEA (offline)"},
        "dolar":    {"preco": 5.15,  "fonte": "Referência BRL (offline)"},
    }

# ─────────────────────────────────────────────
# OCR DE LAUDO DE SOLO — PDF e Imagem
# ─────────────────────────────────────────────
def extrair_texto_pdf(arquivo_pdf):
    """Extrai texto de PDF de laudo de solo."""
    try:
        texto_total = ""
        with pdfplumber.open(arquivo_pdf) as pdf:
            for page in pdf.pages:
                texto_total += page.extract_text() or ""
        return texto_total.strip()
    except Exception as e:
        return f"Erro ao ler PDF: {e}"

def extrair_texto_imagem(arquivo_img):
    """Extrai texto de imagem de laudo via OCR (pytesseract)."""
    try:
        img = PILImage.open(arquivo_img)
        texto = pytesseract.image_to_string(img, lang="por")
        return texto.strip()
    except Exception as e:
        return f"Erro no OCR: {e}"

def parsear_laudo_ocr(texto):
    """Tenta extrair valores de análise de solo do texto OCR."""
    resultado = {}
    padroes = {
        "ph":              r"pH[:\s]+([0-9]+[.,][0-9]+)",
        "fosforo":         r"(?:Fósforo|Fosforo|P)[:\s]+([0-9]+[.,][0-9]+)",
        "potassio":        r"(?:Potássio|Potassio|K)[:\s]+([0-9]+[.,][0-9]+)",
        "calcio":          r"(?:Cálcio|Calcio|Ca)[:\s]+([0-9]+[.,][0-9]+)",
        "magnesio":        r"(?:Magnésio|Magnesio|Mg)[:\s]+([0-9]+[.,][0-9]+)",
        "aluminio":        r"(?:Alumínio|Aluminio|Al)[:\s]+([0-9]+[.,][0-9]+)",
        "enxofre":         r"(?:Enxofre|S)[:\s]+([0-9]+[.,][0-9]+)",
        "materia_organica":r"(?:Matéria Orgânica|M\.O\.|MO)[:\s]+([0-9]+[.,][0-9]+)",
        "ctc":             r"(?:CTC|T)[:\s]+([0-9]+[.,][0-9]+)",
        "argila":          r"(?:Argila)[:\s]+([0-9]+[.,][0-9]+)",
    }
    for campo, padrao in padroes.items():
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            try:
                resultado[campo] = float(match.group(1).replace(",", "."))
            except ValueError:
                pass
    return resultado


# ─────────────────────────────────────────────
# CORREÇÃO 3: funções sem duplicatas
# ─────────────────────────────────────────────
def carregar_dados_iaagro():
    if os.path.exists(ARQUIVO_DADOS_IAAGRO):
        with open(ARQUIVO_DADOS_IAAGRO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return {"dados": {}, "areas": [], "estoque": [], "aplicacoes": [],
            "historico_produtividade": [], "pluviometro": [],
            "carencia_registros": [], "dre_registros": [], "calendario_eventos": []}

def salvar_dados_iaagro():
    dados_salvos = {
        "dados": st.session_state.dados,
        "areas": st.session_state.areas,
        "estoque": st.session_state.estoque,
        "aplicacoes": st.session_state.aplicacoes,
        "historico_produtividade": st.session_state.historico_produtividade,
        "pluviometro": st.session_state.pluviometro,
        "carencia_registros": st.session_state.get("carencia_registros", []),
        "dre_registros":      st.session_state.get("dre_registros", []),
        "calendario_eventos": st.session_state.get("calendario_eventos", []),
    }
    with open(ARQUIVO_DADOS_IAAGRO, "w", encoding="utf-8") as arquivo:
        json.dump(dados_salvos, arquivo, indent=4, ensure_ascii=False)

def carregar_areas():
    if os.path.exists(ARQUIVO_AREAS):
        with open(ARQUIVO_AREAS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return []

def salvar_areas(areas):
    with open(ARQUIVO_AREAS, "w", encoding="utf-8") as arquivo:
        json.dump(areas, arquivo, indent=4, ensure_ascii=False)

# CORREÇÃO 2: carregar_area_por_id movida para escopo global
def carregar_area_por_id(id_area):
    for area in st.session_state.areas:
        if area.get("ID") == id_area:
            st.session_state.dados = area.get("Dados", {}).copy()
            st.session_state.aplicacoes = area.get("Aplicacoes", []).copy()
            st.session_state.estoque = area.get("Estoque", []).copy()
            return True
    return False

def carregar_estoque():
    if os.path.exists(ARQUIVO_ESTOQUE):
        with open(ARQUIVO_ESTOQUE, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return []

def salvar_estoque(estoque):
    with open(ARQUIVO_ESTOQUE, "w", encoding="utf-8") as arquivo:
        json.dump(estoque, arquivo, indent=4, ensure_ascii=False)

def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return {}

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

# ─────────────────────────────────────────────
# SESSION STATE – LOGIN
# ─────────────────────────────────────────────
if "usuarios" not in st.session_state:
    st.session_state.usuarios = carregar_usuarios()

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario_atual" not in st.session_state:
    st.session_state.usuario_atual = ""

# ─────────────────────────────────────────────
# TELA DE LOGIN
# ─────────────────────────────────────────────
def tela_login():
    # Logo centralizada na tela de login
    if os.path.exists("IAAgrologo.jpeg"):
        import base64 as _b64
        with open("IAAgrologo.jpeg", "rb") as _f:
            _logo = _b64.b64encode(_f.read()).decode()
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;margin-bottom:10px;">
            <img src="data:image/jpeg;base64,{_logo}"
                 style="width:180px;border-radius:20px;
                        box-shadow:0 4px 24px rgba(0,200,83,0.35);
                        margin-bottom:14px;" />
            <h1 style="color:#6ee7b7;font-size:2.2rem;font-weight:900;
                       letter-spacing:2px;margin:0;">IAAgro Pro</h1>
            <p style="color:#93c5fd;font-size:1rem;font-weight:600;
                      margin:4px 0 0 0;letter-spacing:1px;">
                Gestão agrícola inteligente
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;margin-bottom:16px;">
            <h1 style="color:#6ee7b7;font-size:2.2rem;font-weight:900;">🌱 IAAgro Pro</h1>
            <p style="color:#93c5fd;font-size:1rem;font-weight:600;">Gestão agrícola inteligente</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h3 style='color:#f1f5f9;text-align:center;margin-bottom:18px;'>Acesse sua conta</h3>",
                unsafe_allow_html=True)

    aba_login, aba_cadastro, aba_recuperar = st.tabs(
        ["Entrar", "Criar conta", "Recuperar senha"]
    )

    with aba_login:
        usuario = st.text_input("Usuário", key="login_usuario")
        senha   = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar"):
            u = st.session_state.usuarios.get(usuario)
            if u and verificar_senha(senha, u["senha"]):
                st.session_state.logado = True
                st.session_state.usuario_atual = usuario
                st.success("Login realizado com sucesso.")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    with aba_cadastro:
        novo_nome     = st.text_input("Nome completo")
        novo_email    = st.text_input("Email de recuperação")
        novo_usuario  = st.text_input("Criar usuário")
        nova_senha    = st.text_input("Criar senha", type="password")
        confirmar_senha = st.text_input("Confirmar senha", type="password")

        if st.button("Cadastrar"):
            if novo_nome.strip() == "":
                st.error("Digite seu nome.")
            elif novo_email.strip() == "" or "@" not in novo_email or "." not in novo_email:
                st.error("Digite um email válido.")
            elif novo_usuario.strip() == "":
                st.error("Digite um usuário.")
            elif len(nova_senha) < 6:
                st.error("A senha precisa ter pelo menos 6 caracteres.")
            elif nova_senha != confirmar_senha:
                st.error("As senhas não conferem.")
            elif novo_usuario in st.session_state.usuarios:
                st.error("Esse usuário já existe.")
            else:
                st.session_state.usuarios[novo_usuario] = {
                    "nome":  novo_nome,
                    "email": novo_email,
                    "senha": hash_senha(nova_senha)   # CORREÇÃO 9: hash
                }
                # CORREÇÃO 8: salvar após cadastro
                salvar_usuarios(st.session_state.usuarios)
                st.success("Conta criada com sucesso. Agora faça login.")

    with aba_recuperar:
        st.write("Recupere sua senha usando usuário e email cadastrado.")

        usuario_recuperar      = st.text_input("Usuário cadastrado", key="rec_usuario")
        email_recuperar        = st.text_input("Email de recuperação", key="rec_email")
        nova_senha_rec         = st.text_input("Nova senha", type="password", key="rec_nova_senha")
        confirmar_nova_senha_rec = st.text_input("Confirmar nova senha", type="password", key="rec_confirmar_senha")

        if st.button("Redefinir senha"):
            if not usuario_recuperar.strip():
                st.error("Digite o usuário cadastrado.")
            elif usuario_recuperar not in st.session_state.usuarios:
                st.error("Usuário não encontrado.")
            elif st.session_state.usuarios[usuario_recuperar].get("email", "") != email_recuperar:
                st.error("Email de recuperação não confere.")
            elif len(nova_senha_rec) < 6:
                st.error("A nova senha precisa ter pelo menos 6 caracteres.")
            elif nova_senha_rec != confirmar_nova_senha_rec:
                st.error("As senhas não conferem.")
            else:
                st.session_state.usuarios[usuario_recuperar]["senha"] = hash_senha(nova_senha_rec)
                salvar_usuarios(st.session_state.usuarios)
                st.success("Senha redefinida com sucesso. Agora faça login.")


if not st.session_state.logado:
    tela_login()
    st.stop()

# ─────────────────────────────────────────────
# SPLASH SCREEN (apenas 1x por sessão)
# ─────────────────────────────────────────────
if "app_loaded" not in st.session_state:
    _ph = st.empty()
    if os.path.exists("IAAgrologo.jpeg"):
        import base64 as _b64x, time as _tx
        with open("IAAgrologo.jpeg","rb") as _fx:
            _ls = _b64x.b64encode(_fx.read()).decode()
        _ph.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;
                    justify-content:center;padding:80px 0;">
            <img src="data:image/jpeg;base64,{_ls}"
                 style="width:150px;border-radius:18px;
                        box-shadow:0 4px 30px rgba(0,200,83,0.5);" />
            <h2 style="color:#6ee7b7;margin-top:20px;font-weight:900;">Carregando IAAgro Pro...</h2>
            <p style="color:#93c5fd;font-size:1rem;">Sistema de gestão agrícola inteligente</p>
        </div>""", unsafe_allow_html=True)
        _tx.sleep(1.2)
    _ph.empty()
    st.session_state.app_loaded = True

# ─────────────────────────────────────────────
# BARRA LATERAL
# ─────────────────────────────────────────────
st.sidebar.markdown(
    f'<div style="background:#1a4a73;color:#ffffff;padding:10px 14px;border-radius:8px;'
    f'font-weight:700;font-size:14px;margin-bottom:8px;">👤 {st.session_state.usuario_atual}</div>',
    unsafe_allow_html=True
)
if st.sidebar.button("Sair", key="botao_sair"):
    st.session_state.logado = False
    st.session_state.usuario_atual = ""
    st.rerun()


# ─────────────────────────────────────────────
# SESSION STATE – DADOS
# ─────────────────────────────────────────────
dados_carregados = carregar_dados_iaagro()

if "dados"   not in st.session_state:
    st.session_state.dados   = dados_carregados.get("dados", {})
if "areas"   not in st.session_state:
    st.session_state.areas   = dados_carregados.get("areas", [])
if "contador_area" not in st.session_state:
    st.session_state.contador_area = max(
        (int(a["ID"].split("-")[-1]) for a in dados_carregados.get("areas", []) if "ID" in a),
        default=0
    ) + 1
if "area_selecionada" not in st.session_state:
    st.session_state.area_selecionada = None
if "estoque" not in st.session_state:
    st.session_state.estoque = dados_carregados.get("estoque", [])
if "aplicacoes" not in st.session_state:
    st.session_state.aplicacoes = dados_carregados.get("aplicacoes", [])
if "historico_produtividade" not in st.session_state:
    st.session_state.historico_produtividade = dados_carregados.get("historico_produtividade", [])
if "pluviometro" not in st.session_state:
    st.session_state.pluviometro = dados_carregados.get("pluviometro", [])
if "carencia_registros" not in st.session_state:
    st.session_state.carencia_registros = dados_carregados.get("carencia_registros", [])
if "dre_registros" not in st.session_state:
    st.session_state.dre_registros = dados_carregados.get("dre_registros", [])
if "calendario_eventos" not in st.session_state:
    st.session_state.calendario_eventos = dados_carregados.get("calendario_eventos", [])

# ─────────────────────────────────────────────
# FUNÇÕES UTILITÁRIAS
# ─────────────────────────────────────────────
def classificar(valor, baixo, medio):
    if valor < baixo:   return "Baixo"
    elif valor < medio: return "Médio"
    return "Alto"


def atualizar_area_atual():
    id_area = st.session_state.dados.get("id_area")
    if not id_area:
        return
    for i, area in enumerate(st.session_state.areas):
        if area.get("ID") == id_area:
            st.session_state.areas[i]["Dados"] = st.session_state.dados.copy()
            st.session_state.areas[i]["Aplicacoes"] = [
                app for app in st.session_state.aplicacoes
                if app.get("ID Área", id_area) == id_area
            ]
            st.session_state.areas[i]["Estoque"] = st.session_state.estoque.copy()
            break
    salvar_dados_iaagro()


def calcular_calcario_por_ph(ph, area):
    if   ph < 4.8: dose = 4.0
    elif ph < 5.2: dose = 3.0
    elif ph < 5.5: dose = 2.0
    elif ph < 5.8: dose = 1.0
    else:          dose = 0.0
    return dose, dose * area


def calcular_gesso(d):
    precisa = False
    motivos = []
    aluminio = d.get("aluminio", 0)
    calcio   = d.get("calcio", 0)
    enxofre  = d.get("enxofre", 0)
    ctc      = d.get("ctc", 0)
    argila   = d.get("argila", 35)
    area     = d.get("area", 0)
    if aluminio > 0.3:
        precisa = True; motivos.append("Alumínio elevado")
    if calcio < 3:
        precisa = True; motivos.append("Cálcio baixo")
    if enxofre < 8:
        precisa = True; motivos.append("Enxofre baixo")
    if ctc < 6 and aluminio > 0.2:
        precisa = True; motivos.append("CTC baixa com alumínio presente")
    if precisa:
        if   argila < 20: dose = 0.7
        elif argila < 40: dose = 1.2
        elif argila < 60: dose = 1.8
        else:             dose = 2.2
    else:
        dose = 0.0
    return precisa, dose, dose * area, motivos


def calcular_nota(d):
    nota = 100
    if d.get("ph", 7) < 5.5:             nota -= 20
    if d.get("fosforo", 99) < 15:        nota -= 15
    if d.get("potassio", 999) < 120:     nota -= 15
    if d.get("materia_organica", 99) < 3: nota -= 10
    if d.get("calcio", 99) < 3:          nota -= 10
    if d.get("magnesio", 99) < 1:        nota -= 10
    if d.get("enxofre", 99) < 8:         nota -= 5
    if d.get("aluminio", 0) > 0.3:       nota -= 15
    if d.get("ctc", 99) < 6:             nota -= 10
    return max(nota, 0)


def prioridade(nota):
    if nota < 50:   return "Alta"
    elif nota < 75: return "Média"
    return "Baixa"


def estimar_producao(meta, nota):
    fator = nota / 100
    if   fator >= 0.85: return meta
    elif fator >= 0.70: return meta * 0.85
    elif fator >= 0.50: return meta * 0.70
    return meta * 0.55


def recomendacao_npk(cultura, produtividade, fosforo, potassio, materia_organica, argila=50, ph=5.5):
    n = p2o5 = k2o = 0
    if cultura == "Soja":
        n = 0
        if   fosforo < 10:  p2o5 = 120
        elif fosforo < 20:  p2o5 = 90
        elif fosforo < 35:  p2o5 = 60
        else:               p2o5 = 30
        if   potassio < 80:  k2o = 140
        elif potassio < 150: k2o = 100
        elif potassio < 250: k2o = 70
        else:                k2o = 40
        if produtividade > 70: p2o5 += 20; k2o += 20
    elif cultura == "Milho":
        n = produtividade * 2.2
        if   fosforo < 10:  p2o5 = 140
        elif fosforo < 20:  p2o5 = 100
        elif fosforo < 35:  p2o5 = 70
        else:               p2o5 = 40
        k2o = produtividade * 1.8
        if potassio < 120:  k2o += 50
    elif cultura == "Trigo":
        n = produtividade * 1.8
        if   fosforo < 10:  p2o5 = 100
        elif fosforo < 20:  p2o5 = 70
        else:               p2o5 = 40
        k2o = produtividade * 1.4
    # Ajustes solo
    if argila < 25:        k2o += 20
    elif argila > 60:      k2o -= 10
    if materia_organica >= 4: n *= 0.85
    if ph < 5.2:           p2o5 += 15
    return round(n, 1), round(p2o5, 1), round(k2o, 1)


def score_solo(d):
    score   = 100
    alertas = []
    ph              = d.get("ph", 0)
    fosforo         = d.get("fosforo", 0)
    potassio        = d.get("potassio", 0)
    calcio          = d.get("calcio", 0)
    magnesio        = d.get("magnesio", 0)
    aluminio        = d.get("aluminio", 0)
    materia_organica = d.get("materia_organica", 0)
    if ph < 5.0:    score -= 20; alertas.append("pH baixo")
    elif ph < 5.5:  score -= 10; alertas.append("pH abaixo do ideal")
    if fosforo < 10: score -= 20; alertas.append("Fósforo muito baixo")
    elif fosforo < 20: score -= 10; alertas.append("Fósforo baixo")
    if potassio < 80:  score -= 15; alertas.append("Potássio baixo")
    elif potassio < 120: score -= 8; alertas.append("Potássio médio/baixo")
    if calcio < 3:   score -= 15; alertas.append("Cálcio baixo")
    if magnesio < 1: score -= 10; alertas.append("Magnésio baixo")
    if aluminio > 0.5: score -= 20; alertas.append("Alumínio elevado")
    if materia_organica < 2.5: score -= 10; alertas.append("Matéria orgânica baixa")
    score = max(0, min(100, score))
    if   score >= 85: classe = "Excelente"
    elif score >= 70: classe = "Boa"
    elif score >= 50: classe = "Média"
    elif score >= 30: classe = "Fraca"
    else:             classe = "Crítica"
    return score, classe, alertas


def baixar_estoque(nome_insumo, quantidade_usada):
    for item in st.session_state.estoque:
        if item["Insumo"] == nome_insumo:
            if item["Quantidade"] >= quantidade_usada:
                item["Quantidade"] -= quantidade_usada
                item["Valor Total R$"] = item["Quantidade"] * item["Valor Unitário R$"]
                return True, "Baixa realizada com sucesso."
            return False, "Estoque insuficiente."
    return False, "Insumo não encontrado."


# ─────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────
menu = st.sidebar.radio(
    "📋 Menu",
    [
        "Início",
        "Cadastro da Área",
        "Áreas Cadastradas",
        "Histórico de Produtividade",
        "Pluviômetro",
        "Mapa de Fertilidade",
        "Análise de Solo",
        "Diagnóstico Completo",
        "Adubação",
        "Custos",
        "Estoque de Insumos",
        "Aplicações",
        "Relatório Final",
        "🌤️ Clima & Alertas",
        "💰 Preços de Mercado",
        "📄 OCR Laudo de Solo",
        "⏱️ Prazo de Carência",
        "📋 Ordem de Serviço",
        "💹 Dashboard Financeiro",
        "📅 Calendário Agrícola",
        "⚙️ Configurações"
    ]
)

# ── Backup rápido na sidebar ──
st.sidebar.divider()
backup_bytes = gerar_backup()
st.sidebar.download_button(
    "💾 Baixar Backup",
    data=backup_bytes,
    file_name=f"iaagro_backup_{date.today()}.json",
    mime="application/json",
    use_container_width=True
)

if st.session_state.area_selecionada:
    st.sidebar.markdown(f'<div style="background:#14532d;color:#fff;padding:8px 12px;border-radius:8px;font-weight:700;font-size:13px;margin-top:6px;">🌾 Área ativa: {st.session_state.area_selecionada}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MENU: INÍCIO
# ─────────────────────────────────────────────
if menu == "Início":
    st.markdown("## 🚜 IAAgro Pro V9")
    st.markdown("**Gestão agrícola inteligente**")

    total_areas      = len(st.session_state.areas)
    total_estoque    = len(st.session_state.estoque)
    total_aplicacoes = len(st.session_state.aplicacoes)
    area_total       = sum(area.get("Hectares", 0) for area in st.session_state.areas)

    produtividade_media = 0
    if total_areas > 0:
        produtividade_media = sum(
            area.get("Meta Produtividade", 0) for area in st.session_state.areas
        ) / total_areas

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌾 Áreas",       total_areas)
    col2.metric("📦 Estoque",     total_estoque)
    col3.metric("🚜 Aplicações",  total_aplicacoes)
    col4.metric("📍 Área Total",  f"{area_total:.1f} ha")

    st.divider()

    col5, col6 = st.columns(2)
    with col5:
        st.subheader("📈 Produtividade Média")
        st.metric("Média", f"{produtividade_media:.1f} sc/ha")
    with col6:
        st.subheader("⚠️ Alertas de Estoque")
        estoque_baixo = [item for item in st.session_state.estoque if item.get("Quantidade", 0) < 10]
        if len(estoque_baixo) == 0:
            st.markdown('<div style="background:#166534;color:#ffffff;padding:12px 18px;border-radius:10px;font-weight:700;font-size:15px;">✅ Nenhum alerta de estoque.</div>', unsafe_allow_html=True)
        else:
            for item in estoque_baixo:
                nome = item.get("Insumo", item.get("Produto", "Produto"))
                st.markdown(f'<div style="background:#92400e;color:#ffffff;padding:12px 18px;border-radius:10px;font-weight:700;font-size:15px;">⚠️ {nome} com estoque baixo.</div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("📋 Resumo das Áreas")

    if total_areas == 0:
        st.markdown('<div style="background:#1e3a5f;color:#ffffff;padding:14px 18px;border-radius:10px;font-weight:600;font-size:15px;">ℹ️ Nenhuma área cadastrada.</div>', unsafe_allow_html=True)
    else:
        tabela_dashboard = []
        for area in st.session_state.areas:
            tabela_dashboard.append({
                "Fazenda":    area.get("Fazenda", ""),
                "Talhão":    area.get("Talhão", ""),
                "Cultura":   area.get("Cultura", ""),
                "Área ha":   area.get("Hectares", 0),
                "Meta sc/ha": area.get("Meta Produtividade", 0)
            })
        df_areas = pd.DataFrame(tabela_dashboard)
        st.dataframe(df_areas, use_container_width=True)
        st.divider()
        st.subheader("📊 Gráfico de Produtividade por Talhão")
        st.bar_chart(df_areas.set_index("Talhão")["Meta sc/ha"])

    if total_estoque > 0:
        df_estoque = pd.DataFrame(st.session_state.estoque)
        if "Insumo" in df_estoque.columns and "Quantidade" in df_estoque.columns:
            st.divider()
            st.subheader("📦 Gráfico de Estoque")
            st.bar_chart(df_estoque.set_index("Insumo")["Quantidade"])


# ─────────────────────────────────────────────
# MENU: ÁREAS CADASTRADAS
# ─────────────────────────────────────────────
elif menu == "Áreas Cadastradas":
    st.header("Áreas Cadastradas")

    if len(st.session_state.areas) == 0:
        st.markdown('<div style="background:#1e3a5f;color:#ffffff;padding:14px 18px;border-radius:10px;font-weight:600;font-size:15px;border:1px solid #3b82f6;">ℹ️ Nenhuma área cadastrada ainda.</div>', unsafe_allow_html=True)
    else:
        tabela_areas = pd.DataFrame([
            {
                "ID":               a["ID"],
                "Fazenda":          a["Fazenda"],
                "Talhão":          a["Talhão"],
                "Matricula":        a.get("Matricula", ""),
                "Cidade/Estado":    a["Cidade/Estado"],
                "Hectares":         a["Hectares"],
                "Cultura":          a["Cultura"],
                "Meta Produtividade": a["Meta Produtividade"]
            }
            for a in st.session_state.areas
        ])
        st.dataframe(tabela_areas, use_container_width=True)

        opcoes = [f"{area['ID']} - {area['Talhão']} - {area['Cultura']}" for area in st.session_state.areas]
        escolha = st.selectbox("Selecionar área para trabalhar", opcoes)

        if st.button("Carregar Área Selecionada"):
            indice = opcoes.index(escolha)
            area   = st.session_state.areas[indice]
            st.session_state.id_area          = area["ID"]
            st.session_state.area_selecionada = area["ID"]
            st.session_state.dados            = area.get("Dados", area.get("dados", {})).copy()
            if "id_area" not in st.session_state.dados:
                st.session_state.dados["id_area"] = area["ID"]
            st.session_state.aplicacoes = area.get("Aplicacoes", []).copy()
            st.session_state.estoque    = area.get("Estoque", []).copy()
            salvar_dados_iaagro()
            success_box(f"Área {area['ID']} carregada com sucesso.")

        st.divider()
        st.subheader("Excluir Área Individual")
        opcao_excluir = st.selectbox(
            "Escolha a área para excluir",
            [f"{area['ID']} - {area['Talhão']} - {area['Cultura']}" for area in st.session_state.areas],
            key="excluir_area_select"
        )
        if st.button("Excluir Área Selecionada", key="excluir_area_btn"):
            indice_excluir = [
                f"{area['ID']} - {area['Talhão']} - {area['Cultura']}"
                for area in st.session_state.areas
            ].index(opcao_excluir)
            area_excluida = st.session_state.areas[indice_excluir]["ID"]
            st.session_state.areas.pop(indice_excluir)
            if st.session_state.area_selecionada == area_excluida:
                st.session_state.area_selecionada = None
                st.session_state.dados = {}
            salvar_dados_iaagro()
            success_box(f"Área {area_excluida} excluída com sucesso.")
            st.rerun()

        if st.button("Apagar Todas as Áreas"):
            st.session_state.areas = []
            st.session_state.dados = {}
            st.session_state.area_selecionada = None
            salvar_dados_iaagro()
            warning_box("Todas as áreas foram apagadas.")

# ─────────────────────────────────────────────
# MENU: CADASTRO DA ÁREA
# ─────────────────────────────────────────────
elif menu == "Cadastro da Área":
    st.header("Cadastro da Área")

    fazenda   = st.text_input("Nome da fazenda",  st.session_state.dados.get("fazenda", ""))
    talhao    = st.text_input("Nome do talhão",   st.session_state.dados.get("talhao", ""))
    matricula = st.text_input("Matrícula da Área", st.session_state.dados.get("matricula", ""))
    cidade    = st.text_input("Cidade / Estado",   st.session_state.dados.get("cidade", ""))
    area      = st.number_input("Área do talhão em hectares", min_value=0.0,
                                value=float(st.session_state.dados.get("area", 10.0)))

    culturas_disponiveis = [
        "Soja","Milho","Trigo","Feijão","Canola","Aveia","Cana-de-açúcar",
        "Arroz","Sorgo","Girassol","Cevada","Pastagem","Algodão","Café",
        "Tabaco","Mandioca","Batata","Tomate","Cebola","Alho","Uva",
        "Maçã","Laranja","Banana","Eucalipto","Pinus"
    ]
    config_culturas = {
        "Soja":          {"ph_ideal":"5.8 - 6.5","chuva_ideal":"450 - 800 mm","produtividade_media":65,"nutriente_principal":"Potássio"},
        "Milho":         {"ph_ideal":"5.5 - 6.8","chuva_ideal":"500 - 800 mm","produtividade_media":180,"nutriente_principal":"Nitrogênio"},
        "Trigo":         {"ph_ideal":"5.5 - 6.2","chuva_ideal":"350 - 600 mm","produtividade_media":55,"nutriente_principal":"Nitrogênio"},
        "Feijão":        {"ph_ideal":"5.8 - 6.5","chuva_ideal":"300 - 500 mm","produtividade_media":45,"nutriente_principal":"Fósforo"},
        "Canola":        {"ph_ideal":"5.5 - 6.2","chuva_ideal":"400 - 700 mm","produtividade_media":40,"nutriente_principal":"Enxofre"},
        "Aveia":         {"ph_ideal":"5.2 - 6.0","chuva_ideal":"300 - 550 mm","produtividade_media":70,"nutriente_principal":"Nitrogênio"},
        "Cana-de-açúcar":{"ph_ideal":"5.5 - 6.5","chuva_ideal":"1200 - 1800 mm","produtividade_media":90,"nutriente_principal":"Potássio"},
        "Arroz":         {"ph_ideal":"5.0 - 6.0","chuva_ideal":"900 - 1300 mm","produtividade_media":160,"nutriente_principal":"Nitrogênio"},
        "Sorgo":         {"ph_ideal":"5.5 - 6.5","chuva_ideal":"350 - 650 mm","produtividade_media":120,"nutriente_principal":"Nitrogênio"},
        "Girassol":      {"ph_ideal":"5.5 - 6.8","chuva_ideal":"400 - 700 mm","produtividade_media":35,"nutriente_principal":"Boro"},
        "Cevada":        {"ph_ideal":"5.5 - 6.5","chuva_ideal":"350 - 600 mm","produtividade_media":60,"nutriente_principal":"Nitrogênio"},
        "Pastagem":      {"ph_ideal":"5.0 - 6.5","chuva_ideal":"500 - 1200 mm","produtividade_media":0,"nutriente_principal":"Nitrogênio"},
        "Algodão":       {"ph_ideal":"5.5 - 6.5","chuva_ideal":"700 - 1300 mm","produtividade_media":300,"nutriente_principal":"Potássio"},
        "Café":          {"ph_ideal":"5.5 - 6.5","chuva_ideal":"1200 - 1800 mm","produtividade_media":35,"nutriente_principal":"Nitrogênio"},
        "Tabaco":        {"ph_ideal":"5.2 - 6.2","chuva_ideal":"600 - 1000 mm","produtividade_media":2500,"nutriente_principal":"Potássio"},
        "Mandioca":      {"ph_ideal":"5.0 - 6.5","chuva_ideal":"800 - 1500 mm","produtividade_media":25,"nutriente_principal":"Potássio"},
        "Batata":        {"ph_ideal":"5.0 - 6.0","chuva_ideal":"500 - 700 mm","produtividade_media":35,"nutriente_principal":"Potássio"},
        "Tomate":        {"ph_ideal":"5.5 - 6.8","chuva_ideal":"400 - 800 mm","produtividade_media":80,"nutriente_principal":"Potássio"},
        "Cebola":        {"ph_ideal":"6.0 - 6.8","chuva_ideal":"350 - 650 mm","produtividade_media":40,"nutriente_principal":"Potássio"},
        "Alho":          {"ph_ideal":"6.0 - 7.0","chuva_ideal":"300 - 500 mm","produtividade_media":12,"nutriente_principal":"Enxofre"},
        "Uva":           {"ph_ideal":"5.5 - 6.5","chuva_ideal":"500 - 900 mm","produtividade_media":25,"nutriente_principal":"Potássio"},
        "Maçã":          {"ph_ideal":"5.5 - 6.5","chuva_ideal":"700 - 1200 mm","produtividade_media":45,"nutriente_principal":"Cálcio"},
        "Laranja":       {"ph_ideal":"5.5 - 6.5","chuva_ideal":"1000 - 1500 mm","produtividade_media":35,"nutriente_principal":"Potássio"},
        "Banana":        {"ph_ideal":"5.5 - 7.0","chuva_ideal":"1200 - 2000 mm","produtividade_media":45,"nutriente_principal":"Potássio"},
        "Eucalipto":     {"ph_ideal":"5.0 - 6.5","chuva_ideal":"800 - 1500 mm","produtividade_media":40,"nutriente_principal":"Fósforo"},
        "Pinus":         {"ph_ideal":"4.5 - 6.0","chuva_ideal":"700 - 1400 mm","produtividade_media":35,"nutriente_principal":"Fósforo"},
    }

    cultura_atual = st.session_state.dados.get("cultura", "Soja")
    idx_cultura   = culturas_disponiveis.index(cultura_atual) if cultura_atual in culturas_disponiveis else 0
    cultura       = st.selectbox("Cultura", culturas_disponiveis, index=idx_cultura, key="cultura_area")

    info = config_culturas.get(cultura, {"ph_ideal":"Não definido","chuva_ideal":"Não definido","produtividade_media":0,"nutriente_principal":"Não definido"})
    st.markdown(f"""
    <div style="background:#0f3460;color:#ffffff;padding:14px 18px;border-radius:12px;
                border:1px solid #3b82f6;font-size:15px;font-weight:600;line-height:2;">
        🌱 <b>Cultura:</b> {cultura} &nbsp;|&nbsp;
        🧪 <b>pH ideal:</b> {info['ph_ideal']} &nbsp;|&nbsp;
        🌧️ <b>Chuva ideal:</b> {info['chuva_ideal']}<br>
        📈 <b>Produtividade média:</b> {info['produtividade_media']} &nbsp;|&nbsp;
        🧬 <b>Nutriente principal:</b> {info['nutriente_principal']}
    </div>
    """, unsafe_allow_html=True)

    produtividade = st.number_input("Meta de produtividade em sacas/ha", min_value=0.0,
                                    value=float(st.session_state.dados.get("produtividade", 60.0)))

    # CORREÇÃO: latitude/longitude com geolocalização ou padrão (eram usadas sem definição neste menu)
    geo = get_geolocation()
    if geo:
        latitude  = geo["coords"]["latitude"]
        longitude = geo["coords"]["longitude"]
    else:
        latitude  = st.session_state.dados.get("latitude", -26.88)
        longitude = st.session_state.dados.get("longitude", -52.40)

    if st.button("Salvar Nova Área"):
        id_area  = f"AREA-{st.session_state.contador_area:03d}"
        nova_area = {
            "ID": id_area,
            "Fazenda": fazenda, "Talhão": talhao, "Matricula": matricula,
            "Cidade/Estado": cidade, "Hectares": area,
            "Latitude": latitude, "Longitude": longitude,
            "Cultura": cultura, "Meta Produtividade": produtividade,
            "pH":              st.session_state.dados.get("ph", 0),
            "Fósforo":         st.session_state.dados.get("fosforo", 0),
            "Potássio":        st.session_state.dados.get("potassio", 0),
            "Matéria Orgânica": st.session_state.dados.get("materia_organica", 0),
            "Saturação Base":  st.session_state.dados.get("saturacao_bases", 0),
            "Calcário t/ha":   st.session_state.dados.get("dose_calcario", 0),
            "Gesso t/ha":      st.session_state.dados.get("dose_gesso", 0),
            "Prioridade":      st.session_state.dados.get("prioridade", "Média"),
            "Zona":            st.session_state.dados.get("zona_produtividade", "Média"),
            "Nota Solo":       st.session_state.dados.get("nota_solo", 0),
        }
        st.session_state.areas.append(nova_area)
        st.session_state.contador_area += 1
        st.session_state.area_selecionada = id_area
        st.session_state.dados = {
            "id_area": id_area, "fazenda": fazenda, "talhao": talhao,
            "cidade": cidade, "area": area, "cultura": cultura,
            "produtividade": produtividade, "latitude": latitude, "longitude": longitude
        }
        atualizar_area_atual()
        salvar_dados_iaagro()
        success_box(f"Área cadastrada com sucesso. ID gerado: {id_area}")

    if st.session_state.area_selecionada:
        if st.button("Atualizar Área Ativa"):
            st.session_state.dados.update({
                "fazenda": fazenda, "talhao": talhao, "cidade": cidade,
                "area": area, "cultura": cultura, "produtividade": produtividade
            })
            for a in st.session_state.areas:
                if a["ID"] == st.session_state.area_selecionada:
                    a["Fazenda"] = fazenda; a["Talhão"] = talhao
                    a["Cidade/Estado"] = cidade; a["Hectares"] = area
                    a["Cultura"] = cultura; a["Meta Produtividade"] = produtividade
                    a["Dados"] = st.session_state.dados.copy()
            salvar_dados_iaagro()
            success_box("Área ativa atualizada com sucesso.")

# ─────────────────────────────────────────────
# MENU: HISTÓRICO DE PRODUTIVIDADE
# ─────────────────────────────────────────────
elif menu == "Histórico de Produtividade":
    st.header("📈 Histórico de Produtividade")

    if len(st.session_state.areas) == 0:
        warning_box("Cadastre uma área primeiro.")
    else:
        lista_areas = [f"{a['ID']} - {a['Talhão']}" for a in st.session_state.areas]
        area_escolhida     = st.selectbox("Selecione a Área", lista_areas)
        safra              = st.text_input("Safra", placeholder="2024/2025")
        produtividade_real = st.number_input("Produtividade Real (sc/ha)", min_value=0.0, value=60.0)
        custo_total        = st.number_input("Custo Total por hectare (R$)", min_value=0.0, value=0.0)
        observacoes        = st.text_area("Observações da Safra")

        if st.button("Salvar Histórico"):
            st.session_state.historico_produtividade.append({
                "Área": area_escolhida, "Safra": safra,
                "Produtividade": produtividade_real,
                "Custo": custo_total, "Observações": observacoes
            })
            salvar_dados_iaagro()
            success_box("Histórico salvo com sucesso!")

        if len(st.session_state.historico_produtividade) > 0:
            df_hist = pd.DataFrame(st.session_state.historico_produtividade)
            st.dataframe(df_hist, use_container_width=True)
            st.subheader("📊 Evolução Produtiva")
            area_filtro = st.selectbox("Filtrar gráfico por área", df_hist["Área"].unique())
            df_area     = df_hist[df_hist["Área"] == area_filtro]
            grafico     = df_area.pivot_table(index="Safra", values="Produtividade", aggfunc="mean")
            st.line_chart(grafico)
            media_prod  = df_hist["Produtividade"].mean()
            melhor_prod = df_hist["Produtividade"].max()
            custo_medio = df_hist["Custo"].mean()
            col1, col2, col3 = st.columns(3)
            col1.metric("📈 Média Produtiva", f"{media_prod:.1f} sc/ha")
            col2.metric("🏆 Melhor Safra",    f"{melhor_prod:.1f} sc/ha")
            col3.metric("💰 Custo Médio",      f"R$ {custo_medio:.2f}")


# ─────────────────────────────────────────────
# MENU: PLUVIÔMETRO
# ─────────────────────────────────────────────
elif menu == "Pluviômetro":
    st.header("🌧️ Pluviômetro Inteligente")

    if len(st.session_state.areas) == 0:
        warning_box("Cadastre uma área primeiro.")
    else:
        lista_areas  = [f"{a['ID']} - {a['Talhão']}" for a in st.session_state.areas]
        area_chuva   = st.selectbox("Selecione a Área", lista_areas)
        id_area_chuva = area_chuva.split(" - ")[0]
        area_obj      = next((a for a in st.session_state.areas if a["ID"] == id_area_chuva), {})
        cultura_chuva = area_obj.get("Cultura", "Soja")

        chuva_ideal_padrao = {
            "Soja":120.0,"Milho":140.0,"Trigo":90.0,"Feijão":100.0,"Canola":90.0,
            "Aveia":80.0,"Cana-de-açúcar":180.0,"Arroz":180.0,"Sorgo":90.0,
            "Girassol":90.0,"Cevada":80.0,"Pastagem":120.0,"Algodão":130.0,
            "Café":140.0,"Tabaco":110.0,"Mandioca":100.0,"Batata":100.0,
            "Tomate":120.0,"Cebola":80.0,"Alho":70.0,"Uva":80.0,"Maçã":100.0,
            "Laranja":130.0,"Banana":180.0,"Eucalipto":120.0,"Pinus":100.0
        }
        chuva_ideal_auto = chuva_ideal_padrao.get(cultura_chuva, 120.0)
        st.markdown(f'<div style="background:#0f3460;color:#ffffff;padding:12px 18px;border-radius:10px;font-weight:600;font-size:15px;border:1px solid #3b82f6;">🌱 <b>Cultura:</b> {cultura_chuva} &nbsp;|&nbsp; 🌧️ <b>Chuva ideal estimada:</b> {chuva_ideal_auto} mm</div>', unsafe_allow_html=True)

        mes        = st.selectbox("Mês", ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
                                          "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"])
        chuva_real = st.number_input("Chuva acumulada (mm)", min_value=0.0, value=0.0)
        chuva_ideal = st.number_input("Chuva ideal da cultura (mm)", min_value=0.0, value=chuva_ideal_auto)

        if chuva_real < chuva_ideal * 0.7:
            perda  = round((chuva_ideal - chuva_real) * 0.15, 1)
            status = "⚠️ Déficit hídrico"
        elif chuva_real > chuva_ideal * 1.3:
            perda  = round((chuva_real - chuva_ideal) * 0.08, 1)
            status = "⚠️ Excesso de chuva"
        else:
            perda  = 0
            status = "✅ Chuva adequada"

        percentual = min(chuva_real / chuva_ideal, 1.0) if chuva_ideal > 0 else 0.0
        st.subheader("🌧️ Nível de Chuva")
        st.progress(percentual)
        st.write(f"{round(percentual * 100)}% da chuva ideal atingida")
        st.subheader("📊 Diagnóstico Climático")
        st.metric("Perda estimada", f"{perda}%")
        info_box(status)

        if st.button("Salvar Registro de Chuva"):
            st.session_state.pluviometro.append({
                "Área": area_chuva, "Mês": mes,
                "Chuva Real": chuva_real, "Chuva Ideal": chuva_ideal,
                "Perda Estimada": perda, "Status": status
            })
            salvar_dados_iaagro()
            success_box("Registro salvo com sucesso!")

        if len(st.session_state.pluviometro) > 0:
            df_chuva      = pd.DataFrame(st.session_state.pluviometro)
            st.subheader("📋 Histórico de Chuvas")
            st.dataframe(df_chuva, use_container_width=True)
            st.subheader("📈 Chuva Real x Chuva Ideal")
            df_chuva_area = df_chuva[df_chuva["Área"] == area_chuva]
            grafico_chuva = df_chuva_area.set_index("Mês")[["Chuva Real","Chuva Ideal"]]
            st.line_chart(grafico_chuva)
            st.subheader("🤖 Previsão IAAgro de Quebra de Safra")
            perda_media       = df_chuva_area["Perda Estimada"].mean()
            chuva_total       = df_chuva_area["Chuva Real"].sum()
            chuva_ideal_total = df_chuva_area["Chuva Ideal"].sum()
            if perda_media >= 15:
                risco_safra = "🔴 Alto risco de quebra produtiva"
                recomendacao_ia = "Reavaliar meta produtiva, reforçar monitoramento da lavoura e ajustar investimento."
            elif perda_media >= 7:
                risco_safra = "🟡 Risco moderado de quebra produtiva"
                recomendacao_ia = "Acompanhar fases críticas da cultura e observar estresse hídrico."
            else:
                risco_safra = "🟢 Baixo risco climático até o momento"
                recomendacao_ia = "Condição hídrica dentro de faixa aceitável."
            col1, col2, col3 = st.columns(3)
            col1.metric("🌧️ Chuva Total",  f"{chuva_total:.1f} mm")
            col2.metric("🎯 Ideal Total",  f"{chuva_ideal_total:.1f} mm")
            col3.metric("📉 Perda Média",  f"{perda_media:.1f}%")
            info_box(risco_safra)
            warning_box(recomendacao_ia)


# ─────────────────────────────────────────────
# MENU: MAPA DE FERTILIDADE
# ─────────────────────────────────────────────
elif menu == "Mapa de Fertilidade":
    st.header("🗺️ Mapa de Fertilidade por Cores")
    st.subheader("🌦️ Mapa Climático dos Talhões")

    if len(st.session_state.areas) == 0:
        st.markdown('<div style="background:#1e3a5f;color:#ffffff;padding:14px 18px;border-radius:10px;font-weight:600;font-size:15px;border:1px solid #3b82f6;">ℹ️ Nenhuma área cadastrada.</div>', unsafe_allow_html=True)
    else:
        mapa_dados = []
        for area in st.session_state.areas:
            dados_area = area.get("Dados", area.get("dados", {}))
            media_hist = 0
            historicos_area = [h for h in st.session_state.historico_produtividade if h["Área"].startswith(area["ID"])]
            if len(historicos_area) > 0:
                media_hist = sum(h["Produtividade"] for h in historicos_area) / len(historicos_area)
            if dados_area and "ph" in dados_area:
                score, classe, alertas = score_solo(dados_area)
            else:
                score = 0; classe = "Sem análise"; alertas = ["Sem análise de solo"]
            if   score >= 85: cor = "🟢 Verde"
            elif score >= 70: cor = "🟡 Amarelo"
            elif score >= 50: cor = "🟠 Laranja"
            else:             cor = "🔴 Vermelho"
            registros_area = [r for r in st.session_state.pluviometro if r["Área"] == area.get("ID","")]
            if len(registros_area) > 0:
                perda_media_clima = sum(r["Perda Estimada"] for r in registros_area) / len(registros_area)
                if   perda_media_clima <= 5:  clima_cor = "🟢 Ideal"
                elif perda_media_clima <= 12: clima_cor = "🟡 Atenção"
                else:                         clima_cor = "🔴 Crítico"
            else:
                clima_cor = "⚪ Sem dados"
            mapa_dados.append({
                "ID": area.get("ID",""), "Fazenda": area.get("Fazenda",""),
                "Talhão": area.get("Talhão",""), "Clima": clima_cor,
                "Cultura": area.get("Cultura",""), "Área ha": area.get("Hectares",0),
                "Score": score, "Classe": classe, "Cor": cor,
                "Alertas": ", ".join(alertas)
            })
        df_mapa = pd.DataFrame(mapa_dados)
        st.subheader("📍 Visão geral dos talhões")
        st.dataframe(df_mapa, use_container_width=True)
        st.subheader("🎨 Legenda")
        st.write("🟢 Verde = solo excelente | 🟡 Amarelo = solo bom | 🟠 Laranja = solo médio | 🔴 Vermelho = solo crítico")
        st.subheader("🛰️ Mapa Visual dos Talhões")
        cols = st.columns(3)
        for i, linha in df_mapa.iterrows():
            cor_str = linha["Cor"]
            if "Verde"   in cor_str: fundo = "#16a34a"
            elif "Amarelo" in cor_str: fundo = "#eab308"
            elif "Laranja" in cor_str: fundo = "#f97316"
            else:                      fundo = "#dc2626"
            with cols[i % 3]:
                st.markdown(
                    f"""<div style="background-color:{fundo};padding:18px;border-radius:18px;
                    margin-bottom:15px;color:white;font-weight:bold;box-shadow:0 4px 12px rgba(0,0,0,0.25);">
                    <h3>{linha['Talhão']}</h3><p>ID: {linha['ID']}</p>
                    <p>Cultura: {linha['Cultura']}</p><p>Área: {linha['Área ha']} ha</p>
                    <p>Classe: {linha['Classe']}</p><p>Score: {linha['Score']}</p>
                    <p>{linha['Alertas']}</p></div>""",
                    unsafe_allow_html=True
                )
        st.subheader("🌡️ Heatmap de Fertilidade")
        df_heatmap = df_mapa[["Talhão","Score"]].copy()
        st.write("Quanto mais alto o score, melhor a fertilidade do talhão.")
        st.dataframe(df_heatmap.style.background_gradient(cmap="RdYlGn", subset=["Score"]), use_container_width=True)
        st.subheader("📊 Ranking de Fertilidade")
        st.bar_chart(df_mapa.set_index("Talhão")["Score"])
        st.subheader("🛰️ Mapa GPS dos Talhões")
        geo = get_geolocation()
        if geo:
            latitude  = geo["coords"]["latitude"]
            longitude = geo["coords"]["longitude"]
        else:
            latitude  = -26.88
            longitude = -52.40
        mapa_folium = folium.Map(location=[latitude, longitude], zoom_start=13, tiles=None)
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri", name="Satélite", control=True
        ).add_to(mapa_folium)
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
            attr="Esri", name="Nomes e locais", overlay=True, control=True
        ).add_to(mapa_folium)
        folium.LayerControl(position="topright", collapsed=False).add_to(mapa_folium)
        Draw(
            draw_options={"polyline":False,"rectangle":True,"circle":False,"marker":False,"circlemarker":False,"polygon":True},
            edit_options={"edit":True,"remove":True}
        ).add_to(mapa_folium)
        folium.Marker(location=[latitude, longitude], popup="Minha localização",
                      tooltip="Local atual", icon=folium.Icon(color="darkgreen", icon="leaf")
        ).add_to(mapa_folium)
        dados_mapa_folium = st_folium(mapa_folium, width=900, height=500)
        st.subheader("💾 Salvar Desenho do Talhão")
        if dados_mapa_folium and dados_mapa_folium.get("last_active_drawing"):
            desenho = dados_mapa_folium["last_active_drawing"]
            coords  = desenho["geometry"]["coordinates"][0]
            def calcular_area_ha(coords):
                area_val = 0
                for i in range(len(coords) - 1):
                    x1, y1 = coords[i]; x2, y2 = coords[i + 1]
                    area_val += (x1 * y2) - (x2 * y1)
                return abs(area_val) / 2 * 111139 * 111139 / 10000
            area_calculada = calcular_area_ha(coords)
            success_box(f"Área calculada automaticamente: {area_calculada:.2f} ha")
            if st.button("Salvar desenho no talhão", key="salvar_desenho_talhao"):
                st.session_state.dados["desenho_talhao"] = desenho
                salvar_dados_iaagro()
                success_box("Desenho do talhão salvo com sucesso!")
        else:
            info_box("Desenhe um polígono no mapa para salvar.")

# ─────────────────────────────────────────────
# MENU: ANÁLISE DE SOLO
# ─────────────────────────────────────────────
elif menu == "Análise de Solo":
    st.header("Análise de Solo")

    # Injeta estilo escuro no componente de upload via JS
    st.markdown("""
    <style>
    /* Força fundo escuro no dropzone do upload */
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploader"] section > div,
    [data-testid="stFileUploaderDropzone"],
    [data-testid="stFileUploaderDropzone"] > div {
        background-color: #0f3460 !important;
        border: 2px solid #22c55e !important;
        border-radius: 12px !important;
    }
    /* Botão Upload */
    [data-testid="stFileUploaderDropzone"] button {
        background-color: #16a34a !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    [data-testid="stFileUploaderDropzone"] button span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    /* Texto de instrução */
    [data-testid="stFileUploaderDropzone"] span,
    [data-testid="stFileUploaderDropzone"] p,
    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploaderDropzone"] div {
        color: #ffffff !important;
        opacity: 1 !important;
    }
    /* Ícone */
    [data-testid="stFileUploaderDropzone"] svg path {
        fill: #22c55e !important;
        stroke: #22c55e !important;
    }
    </style>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📄 Upload análise de solo", type=["xlsx","csv"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df_upload = pd.read_csv(uploaded_file)
        else:
            df_upload = pd.read_excel(uploaded_file)
        success_box("✅ Análise carregada com sucesso!")
        st.dataframe(df_upload)

    if not st.session_state.area_selecionada:
        warning_box("Cadastre ou carregue uma área primeiro.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            ph       = st.number_input("pH do solo", min_value=3.5, max_value=8.0, value=float(st.session_state.dados.get("ph", 5.5)))
            fosforo  = st.number_input("Fósforo P", min_value=0.0, value=float(st.session_state.dados.get("fosforo", 10.0)))
            potassio = st.number_input("Potássio K", min_value=0.0, value=float(st.session_state.dados.get("potassio", 100.0)))
        with col2:
            materia_organica = st.number_input("Matéria orgânica %", min_value=0.0, value=float(st.session_state.dados.get("materia_organica", 2.5)))
            calcio   = st.number_input("Cálcio Ca", min_value=0.0, value=float(st.session_state.dados.get("calcio", 3.0)))
            magnesio = st.number_input("Magnésio Mg", min_value=0.0, value=float(st.session_state.dados.get("magnesio", 1.0)))
        with col3:
            aluminio = st.number_input("Alumínio Al", min_value=0.0, value=float(st.session_state.dados.get("aluminio", 0.2)))
            enxofre  = st.number_input("Enxofre S", min_value=0.0, value=float(st.session_state.dados.get("enxofre", 8.0)))
            ctc      = st.number_input("CTC", min_value=0.0, value=float(st.session_state.dados.get("ctc", 8.0)))

        st.subheader("Micronutrientes")
        col4, col5, col6 = st.columns(3)
        with col4:
            boro  = st.number_input("Boro B", min_value=0.0, value=float(st.session_state.dados.get("boro", 0.3)))
            zinco = st.number_input("Zinco Zn", min_value=0.0, value=float(st.session_state.dados.get("zinco", 1.0)))
        with col5:
            manganes = st.number_input("Manganês Mn", min_value=0.0, value=float(st.session_state.dados.get("manganes", 5.0)))
            cobre    = st.number_input("Cobre Cu", min_value=0.0, value=float(st.session_state.dados.get("cobre", 0.5)))
        with col6:
            argila = st.number_input("Argila %", min_value=0.0, max_value=100.0, value=float(st.session_state.dados.get("argila", 35.0)))

        # Validação de campos
        erros_val = []
        if not validar_ph(ph):
            erros_val.append("pH deve estar entre 3.5 e 9.0")
        if ph == 0:
            erros_val.append("pH não pode ser zero")

        if erros_val:
            for e in erros_val:
                st.markdown(f'''<div style="background:#7f1d1d;color:#fff;padding:10px 16px;
                border-radius:10px;border-left:5px solid #ef4444;font-weight:600;margin:4px 0;">
                ❌ {e}</div>''', unsafe_allow_html=True)

        if st.button("Salvar Análise"):
            if erros_val:
                st.markdown('''<div style="background:#7f1d1d;color:#fff;padding:10px 16px;
                border-radius:10px;border-left:5px solid #ef4444;font-weight:600;">
                ❌ Corrija os erros antes de salvar.</div>''', unsafe_allow_html=True)
            else:
                st.session_state.dados.update({
                    "ph": ph, "fosforo": fosforo, "potassio": potassio,
                    "materia_organica": materia_organica, "calcio": calcio, "magnesio": magnesio,
                    "aluminio": aluminio, "enxofre": enxofre, "ctc": ctc,
                    "boro": boro, "zinco": zinco, "manganes": manganes, "cobre": cobre, "argila": argila
                })
                atualizar_area_atual()
                salvar_dados_iaagro()
                # Salvar no banco histórico
                nota_s  = calcular_nota(st.session_state.dados)
                score_s, classe_s, _ = score_solo(st.session_state.dados)
                id_area_atual = st.session_state.dados.get("id_area","")
                if id_area_atual:
                    salvar_analise_solo_db(id_area_atual, st.session_state.dados, nota_s, score_s, classe_s)
                # Checar alertas de estoque por email
                checar_alertas_estoque()
                success_box("Análise salva na área ativa e registrada no histórico!")

        # ── Foto do talhão ──
        st.divider()
        st.subheader("📷 Foto do Talhão")
        foto = st.file_uploader("Adicionar foto do talhão (JPG, PNG)", type=["jpg","jpeg","png"],
                                key="foto_talhao")
        if foto:
            import base64 as _b64
            foto_bytes = foto.read()
            foto_b64   = _b64.b64encode(foto_bytes).decode()
            ext        = foto.name.split(".")[-1].lower()
            st.session_state.dados["foto_talhao_b64"] = foto_b64
            st.session_state.dados["foto_talhao_ext"] = ext
            salvar_dados_iaagro()
            success_box("Foto salva com sucesso!")

        if st.session_state.dados.get("foto_talhao_b64"):
            import base64 as _b64
            foto_b64 = st.session_state.dados["foto_talhao_b64"]
            ext      = st.session_state.dados.get("foto_talhao_ext","jpg")
            st.markdown(f'''<div style="text-align:center;margin:16px 0;">
                <img src="data:image/{ext};base64,{foto_b64}"
                     style="max-width:100%;border-radius:14px;
                            border:2px solid #22c55e;box-shadow:0 4px 20px rgba(0,200,83,0.3);" />
            </div>''', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MENU: DIAGNÓSTICO COMPLETO
# ─────────────────────────────────────────────
elif menu == "Diagnóstico Completo":
    st.header("Diagnóstico Completo")
    d = st.session_state.dados

    if "ph" not in d:
        warning_box("Preencha primeiro a análise de solo.")
    else:
        nota           = calcular_nota(d)
        score, classe_score, alertas_score = score_solo(d)
        prioridade_final = prioridade(nota)
        dose_calcario, total_calcario = calcular_calcario_por_ph(d["ph"], d["area"])
        precisa_gesso, dose_gesso, total_gesso, motivos_gesso = calcular_gesso(d)
        producao_estimada = estimar_producao(d["produtividade"], nota)

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Nota",              f"{nota}/100")
        col2.metric("Prioridade",        prioridade_final)
        col3.metric("Calcário",          f"{dose_calcario} t/ha")
        col4.metric("Gesso",             f"{dose_gesso} t/ha")
        col5.metric("Produção Estimada", f"{producao_estimada:.1f} sc/ha")

        st.subheader("🧠 Score Inteligente do Solo")
        col1, col2 = st.columns(2)
        col1.metric("Score do Solo",   f"{score}/100")
        col2.metric("Classificação",   classe_score)
        if alertas_score:
            warning_box(" | ".join(alertas_score))
        else:
            success_box("Solo em boas condições gerais.")

        indice_produtivo  = score * 1.15
        produtividade_ia  = producao_estimada * (indice_produtivo / 100)
        if   indice_produtivo >= 85: status_ia = "ALTO"
        elif indice_produtivo >= 65: status_ia = "MÉDIO"
        else:                        status_ia = "BAIXO"

        st.subheader("🤖 Inteligência Artificial Produtiva")
        st.markdown(f'''<div style="background:#1e3a5f;color:#ffffff;padding:15px 18px;border-radius:12px;
        border-left:5px solid #3b82f6;font-size:15px;font-weight:600;line-height:2.0;margin:8px 0;">
        🤖 <b>Potencial estimado:</b> {status_ia}<br>
        📈 <b>Produtividade prevista pela IA:</b> {produtividade_ia:.1f} sc/ha<br>
        📊 <b>Índice produtivo do talhão:</b> {indice_produtivo:.1f}/100
        </div>''', unsafe_allow_html=True)

        st.subheader("💰 Inteligência Econômica")
        area          = float(d["area"])
        preco_soja    = 135
        custo_base    = 3200
        receita_estimada = produtividade_ia * preco_soja * area
        lucro_estimado   = receita_estimada - (custo_base * area)
        if   lucro_estimado > 50000: risco = "BAIXO"
        elif lucro_estimado > 20000: risco = "MÉDIO"
        else:                         risco = "ALTO"
        st.markdown(f'''<div style="background:#14532d;color:#ffffff;padding:15px 18px;border-radius:12px;
        border-left:5px solid #22c55e;font-size:15px;font-weight:600;line-height:2.0;margin:8px 0;">
        💰 <b>Receita estimada:</b> R$ {receita_estimada:,.2f}<br>
        💵 <b>Lucro potencial:</b> R$ {lucro_estimado:,.2f}<br>
        📊 <b>Risco econômico:</b> {risco}
        </div>''', unsafe_allow_html=True)

        st.subheader("Calcário")
        st.write(f"Dose estimada: {dose_calcario} t/ha")
        st.write(f"Total estimado: {total_calcario:.1f} toneladas")

        st.subheader("Gesso Agrícola")
        if precisa_gesso:
            warning_box(f"Indicação inicial de gesso: {dose_gesso} t/ha")
            st.write(f"Total estimado: {total_gesso:.1f} toneladas")
            for motivo in motivos_gesso:
                st.write(f"- {motivo}")
        else:
            success_box("Sem indicação inicial forte para gesso.")

        tabela = pd.DataFrame({
            "Indicador": ["pH","Fósforo","Potássio","Matéria Orgânica","Cálcio","Magnésio","Enxofre","Alumínio","CTC","Argila"],
            "Valor": [d["ph"],d["fosforo"],d["potassio"],d["materia_organica"],d["calcio"],d["magnesio"],d["enxofre"],d["aluminio"],d["ctc"],d["argila"]],
            "Classificação": [
                "Baixo" if d["ph"] < 5.5 else "Adequado",
                classificar(d["fosforo"],15,30), classificar(d["potassio"],120,200),
                classificar(d["materia_organica"],3,5), classificar(d["calcio"],3,6),
                classificar(d["magnesio"],1,2), classificar(d["enxofre"],8,15),
                "Alto" if d["aluminio"] > 0.3 else "Seguro",
                classificar(d["ctc"],6,10), classificar(d["argila"],20,40)
            ]
        })
        st.dataframe(tabela, use_container_width=True)


# ─────────────────────────────────────────────
# MENU: ADUBAÇÃO
# ─────────────────────────────────────────────
elif menu == "Adubação":
    st.header("🌱 Adubação Inteligente")
    d = st.session_state.dados

    if "ph" not in d:
        warning_box("Preencha primeiro o Cadastro da Área e a Análise de Solo.")
    else:
        cultura      = d.get("cultura", "Soja")
        area         = d.get("area", 0)
        produtividade = d.get("produtividade", 0)
        fosforo      = d.get("fosforo", 0)
        potassio     = d.get("potassio", 0)
        ph           = d.get("ph", 0)
        materia_organica = d.get("materia_organica", 0)

        st.subheader("🤖 IA Recomendando Adubação")

        # Recomendação por cultura
        n = p2o5 = k2o = 0
        if cultura == "Soja":
            if fosforo < 8:    p2o5 = 120
            elif fosforo < 15: p2o5 = 90
            else:              p2o5 = 60
            if potassio < 0.20:    k2o = 140
            elif potassio < 0.35:  k2o = 100
            else:                  k2o = 70
            n = 0
        elif cultura == "Milho":
            if fosforo < 10:   p2o5 = 140
            elif fosforo < 18: p2o5 = 100
            else:              p2o5 = 70
            if potassio < 0.25:    k2o = 120
            elif potassio < 0.40:  k2o = 90
            else:                  k2o = 60
            n = 160
        elif cultura == "Trigo":
            p2o5 = 100 if fosforo < 10 else 70
            k2o  = 80  if potassio < 0.30 else 50
            n    = 120
        elif cultura == "Feijão":
            p2o5 = 110 if fosforo < 10 else 80
            k2o  = 90  if potassio < 0.30 else 60
            n    = 40
        elif cultura == "Canola":
            p2o5 = 80; k2o = 70; n = 150
        elif cultura == "Aveia":
            p2o5 = 50; k2o = 40; n = 90
        elif cultura == "Cana-de-açúcar":
            p2o5 = 100; k2o = 180; n = 140
        else:
            p2o5 = 60; k2o = 60; n = 80

        st.markdown(f'''<div style="background:#14532d;color:#ffffff;padding:15px 18px;border-radius:12px;
        border-left:5px solid #22c55e;font-size:15px;font-weight:600;line-height:2.0;margin:8px 0;">
        🌱 <b>Recomendação IAAgro</b><br>
        🧪 Nitrogênio (N): {n} kg/ha<br>
        🧪 Fósforo (P2O5): {p2o5} kg/ha<br>
        🧪 Potássio (K2O): {k2o} kg/ha
        </div>''', unsafe_allow_html=True)

        st.subheader("📍 Taxa Variável Inteligente")
        zona = st.selectbox("Zona do talhão", ["Baixa Produtividade","Média Produtividade","Alta Produtividade"])
        fator_zona = 0.85 if zona == "Baixa Produtividade" else (1.15 if zona == "Alta Produtividade" else 1.0)
        produtividade_ajustada = produtividade * fator_zona
        n    *= fator_zona
        p2o5 *= fator_zona
        k2o  *= fator_zona

        st.subheader("Dados da Área")
        col1, col2, col3 = st.columns(3)
        col1.metric("Cultura", cultura)
        col2.metric("Área", f"{area:.2f} ha")
        col3.metric("Meta Produtividade", f"{produtividade_ajustada:.1f} sc/ha")
        st.divider()

        st.subheader("Recomendação Base")
        if cultura == "Soja":
            n_ha    = 0
            p2o5_ha = max(40, 100 - fosforo * 2)
            k2o_ha  = max(40, 120 - potassio * 0.5)
        elif cultura == "Milho":
            n_ha    = max(80, produtividade * 3)
            p2o5_ha = max(50, 120 - fosforo * 2)
            k2o_ha  = max(50, 140 - potassio * 0.5)
        else:
            n_ha    = max(60, produtividade * 2.5)
            p2o5_ha = max(40, 100 - fosforo * 2)
            k2o_ha  = max(40, 120 - potassio * 0.5)
        if materia_organica >= 4:
            n_ha *= 0.85

        map_ha   = p2o5_ha / 0.52
        kcl_ha   = k2o_ha  / 0.60
        ureia_ha = n_ha    / 0.45 if n_ha > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Nitrogênio", f"{n:.1f} kg/ha", delta=f"{((fator_zona-1)*100):+.0f}%")
        col2.metric("P₂O₅",      f"{p2o5:.1f} kg/ha", delta=f"{((fator_zona-1)*100):+.0f}%")
        col3.metric("K₂O",       f"{k2o:.1f} kg/ha", delta=f"{((fator_zona-1)*100):+.0f}%")
        st.divider()

        st.subheader("Produtos Recomendados")
        map_ha_ajustado  = map_ha  * fator_zona
        kcl_ha_ajustado  = kcl_ha  * fator_zona
        ureia_ha_ajustado = ureia_ha * fator_zona
        col1, col2, col3 = st.columns(3)
        col1.metric("MAP 11-52-00", f"{map_ha_ajustado:.1f} kg/ha")
        col2.metric("KCl 00-00-60", f"{kcl_ha_ajustado:.1f} kg/ha")
        col3.metric("Ureia 45% N",  f"{ureia_ha_ajustado:.1f} kg/ha")

        st.subheader("Total para a Área")
        total_map  = map_ha_ajustado  * area
        total_kcl  = kcl_ha_ajustado  * area
        total_ureia = ureia_ha_ajustado * area
        col1, col2, col3 = st.columns(3)
        col1.metric("MAP Total",   f"{total_map:.1f} kg")
        col2.metric("KCl Total",   f"{total_kcl:.1f} kg")
        col3.metric("Ureia Total", f"{total_ureia:.1f} kg")

        st.subheader("🚜 Enviar Recomendação para Aplicação")
        if st.button("Gerar Aplicação com Recomendação IA", key="gerar_aplicacao_ia"):
            nova_aplicacao = {
                "Data": str(date.today()),
                "ID Área": st.session_state.dados.get("id_area",""),
                "Talhão": st.session_state.dados.get("talhao",""),
                "Cultura": cultura, "Tipo": "Adubação IA", "Área ha": area,
                "Produtos": [
                    {"Insumo":"MAP 11-52-00","Dose ha":map_ha_ajustado,"Quantidade usada":total_map,"Unidade":"kg"},
                    {"Insumo":"KCL 00-00-60","Dose ha":kcl_ha_ajustado,"Quantidade usada":total_kcl,"Unidade":"kg"},
                    {"Insumo":"Ureia 45% N", "Dose ha":ureia_ha_ajustado,"Quantidade usada":total_ureia,"Unidade":"kg"},
                ]
            }
            st.session_state.aplicacoes.append(nova_aplicacao)
            salvar_dados_iaagro()
            success_box("Aplicação de adubação IA enviada para o histórico!")
            st.subheader("🚨 Alerta Inteligente de Estoque")
            for prod in [{"Insumo":"MAP 11-52-00","Necessario":total_map},
                         {"Insumo":"KCL 00-00-60","Necessario":total_kcl},
                         {"Insumo":"Ureia 45% N","Necessario":total_ureia}]:
                nome       = prod["Insumo"]
                necessario = prod["Necessario"]
                estoque_item = next((item for item in st.session_state.estoque if item["Insumo"] == nome), None)
                if estoque_item is None:
                    error_box(f"❌ {nome}: não cadastrado no estoque.")
                elif necessario <= 0:
                    info_box(f"ℹ️ {nome}: não necessário nesta recomendação.")
                elif estoque_item.get("Quantidade",0) >= necessario:
                    sobra = estoque_item["Quantidade"] - necessario
                    success_box(f"✅ {nome}: estoque suficiente. Necessário: {necessario:.1f} | Sobra: {sobra:.1f} kg")
                else:
                    falta     = necessario - estoque_item["Quantidade"]
                    cobertura = (estoque_item["Quantidade"] / necessario) * 100
                    warning_box(f"⚠️ {nome}: estoque insuficiente. Falta: {falta:.1f} kg | Cobertura: {cobertura:.0f}%")

        st.divider()
        st.subheader("Micronutrientes")
        recomendacoes_micro = []
        if d.get("boro",   0) < 0.3: recomendacoes_micro.append("Boro baixo: considerar aplicação de B.")
        if d.get("zinco",  0) < 1.0: recomendacoes_micro.append("Zinco baixo: considerar aplicação de Zn.")
        if d.get("manganes",0) < 5:  recomendacoes_micro.append("Manganês baixo: monitorar Mn.")
        if d.get("cobre",  0) < 0.5: recomendacoes_micro.append("Cobre baixo: considerar aplicação de Cu.")
        if recomendacoes_micro:
            for rec in recomendacoes_micro: warning_box(rec)
        else:
            success_box("Micronutrientes em faixa aceitável.")

        st.divider()
        st.subheader("Salvar Recomendação")
        recomendacao_adubacao = {
            "Cultura": cultura, "Área ha": area, "Produtividade alvo": produtividade,
            "N kg/ha": n_ha, "P2O5 kg/ha": p2o5_ha, "K2O kg/ha": k2o_ha,
            "MAP kg/ha": map_ha, "KCl kg/ha": kcl_ha, "Ureia kg/ha": ureia_ha,
            "MAP total kg": total_map, "KCl total kg": total_kcl, "Ureia total kg": total_ureia,
            "Micronutrientes": recomendacoes_micro
        }
        if st.button("Salvar Recomendação de Adubação", key="salvar_adubacao_inteligente"):
            st.session_state.dados["adubacao"] = recomendacao_adubacao
            atualizar_area_atual()
            salvar_dados_iaagro()
            success_box("Recomendação de adubação salva com sucesso.")

# ─────────────────────────────────────────────
# MENU: CUSTOS
# ─────────────────────────────────────────────
elif menu == "Custos":
    st.header("Custos Estimados")
    d = st.session_state.dados

    if "ph" not in d:
        warning_box("Preencha primeiro Cadastro da Área e Análise de Solo.")
    else:
        dose_calcario, total_calcario = calcular_calcario_por_ph(d["ph"], d["area"])
        precisa_gesso, dose_gesso, total_gesso, _ = calcular_gesso(d)

        preco_calcario    = st.number_input("Preço calcário R$/t",     min_value=0.0, value=180.0)
        frete_calcario    = st.number_input("Frete calcário R$/t",     min_value=0.0, value=50.0)
        aplicacao_calcario = st.number_input("Aplicação calcário R$/ha", min_value=0.0, value=80.0)
        preco_gesso       = st.number_input("Preço gesso R$/t",        min_value=0.0, value=120.0)
        frete_gesso       = st.number_input("Frete gesso R$/t",        min_value=0.0, value=50.0)
        aplicacao_gesso   = st.number_input("Aplicação gesso R$/ha",   min_value=0.0, value=70.0)

        custo_total_calcario = (total_calcario * preco_calcario
                                + total_calcario * frete_calcario
                                + d["area"] * aplicacao_calcario)
        custo_total_gesso    = (total_gesso * preco_gesso
                                + total_gesso * frete_gesso
                                + d["area"] * aplicacao_gesso)

        st.divider()
        st.subheader("💰 Custos Complementares")
        custo_semente      = st.number_input("Custo sementes R$/ha",       min_value=0.0, step=1.0)
        custo_fertilizante = st.number_input("Custo fertilizantes R$/ha",  min_value=0.0, step=1.0)
        custo_defensivos   = st.number_input("Custo defensivos R$/ha",     min_value=0.0, step=1.0)
        custo_diesel       = st.number_input("Custo diesel/máquinas R$/ha", min_value=0.0, step=1.0)
        outros_custos      = st.number_input("Outros custos R$/ha",        min_value=0.0, step=1.0)

        custo_operacional_total = (custo_semente + custo_fertilizante + custo_defensivos + custo_diesel + outros_custos) * d["area"]
        custo_total_safra       = custo_total_calcario + custo_total_gesso + custo_operacional_total
        custo_por_hectare       = custo_total_safra / d["area"] if d["area"] > 0 else 0

        st.divider()
        st.subheader("📊 Resumo Financeiro")
        st.metric("Custo Total Safra",    f"R$ {custo_total_safra:,.2f}")
        st.metric("Custo por Hectare",    f"R$ {custo_por_hectare:,.2f}/ha")

        if "produtividade" in d:
            preco_saca   = st.number_input("Preço da saca R$", min_value=0.0, step=1.0)
            faturamento  = d["produtividade"] * preco_saca * d["area"]
            lucro        = faturamento - custo_total_safra
            margem       = (lucro / faturamento * 100) if faturamento > 0 else 0
            st.metric("Faturamento Estimado", f"R$ {faturamento:,.2f}")
            st.metric("Lucro Estimado",       f"R$ {lucro:,.2f}")
            st.metric("Margem Estimada",      f"{margem:.1f}%")


# ─────────────────────────────────────────────
# MENU: ESTOQUE DE INSUMOS
# ─────────────────────────────────────────────
elif menu == "Estoque de Insumos":
    st.header("Estoque de Insumos")
    st.subheader("Cadastrar Produto")

    col1, col2, col3 = st.columns(3)
    with col1:
        nome_insumo = st.text_input("Nome do produto / insumo")
        categoria   = st.selectbox("Categoria", [
            "Fertilizante","Cloreto de Potássio","Ureia","Fungicida","Inseticida",
            "Herbicida","Biológico","Foliar","Semente","Calcário","Gesso Agrícola","Adjuvante","Outro"
        ])
        cultura     = st.selectbox("Cultura", ["Soja","Milho","Ambos"], key="cultura_estoque")
        dose_ha     = st.number_input("Dose por hectare", min_value=0.0, value=0.0, key="dose_ha_estoque")
        litros_ha   = st.number_input("Litros de calda por hectare", min_value=0.0, value=75.0, key="litros_ha_estoque")
        capacidade_tanque = st.number_input("Capacidade do tanque (L)", min_value=0, value=2000, key="tanque_estoque")
    with col2:
        quantidade   = st.number_input("Quantidade em estoque", min_value=0.0, value=0.0)
        unidade      = st.selectbox("Unidade do estoque", ["kg","ton","litros","sacos","galões","unidades"])
    with col3:
        valor_unitario  = st.number_input("Valor unitário R$", min_value=0.0, value=0.0)
        estoque_minimo  = st.number_input("Estoque mínimo", min_value=0.0, value=0.0)

    observacao = st.text_area("Observação")

    if st.button("Adicionar Produto ao Estoque"):
        if nome_insumo.strip() == "":
            error_box("Digite o nome do produto.")
        else:
            novo_item = {
                "Insumo": nome_insumo, "Categoria": categoria,
                "Quantidade": quantidade, "Unidade": unidade,
                "Valor Unitário R$": valor_unitario,
                "Valor Total R$": quantidade * valor_unitario,
                "Estoque Mínimo": estoque_minimo,
                "Observação": observacao, "Cultura": cultura,
                "Dose ha": dose_ha, "Litros ha": litros_ha,
                "Tanque litros": capacidade_tanque,
            }
            st.session_state.estoque.append(novo_item)
            salvar_dados_iaagro()
            success_box("Produto adicionado ao estoque.")

    st.subheader("Estoque Atual")
    if len(st.session_state.estoque) == 0:
        info_box("Nenhum produto cadastrado ainda.")
    else:
        tabela_estoque = pd.DataFrame(st.session_state.estoque)

        st.markdown("### 🗑️ Excluir Produto")
        produto_excluir = st.selectbox(
            "Selecione o produto",
            [item["Insumo"] for item in st.session_state.estoque],
            key="produto_excluir_estoque"
        )
        if st.button("❌ Excluir Produto", key="btn_excluir_produto"):
            st.session_state.estoque = [i for i in st.session_state.estoque if i["Insumo"] != produto_excluir]
            salvar_dados_iaagro()
            success_box(f"{produto_excluir} removido do estoque.")
            st.rerun()

        tabela_estoque["Status"] = tabela_estoque.apply(
            lambda linha: "Estoque baixo" if linha["Quantidade"] <= linha["Estoque Mínimo"] else "OK", axis=1
        )
        st.dataframe(tabela_estoque, use_container_width=True)

        st.subheader("🚨 Alertas Inteligentes")
        for item in st.session_state.estoque:
            qtd  = item.get("Quantidade", 0)
            nome = item.get("Insumo", "Produto")
            if   qtd <= 0:   error_box(f"❌ {nome}: estoque zerado!")
            elif qtd <= 500: warning_box(f"⚠️ {nome}: estoque baixo ({qtd:.1f} kg/L)")
            else:            success_box(f"✅ {nome}: estoque OK ({qtd:.1f} kg/L)")

        col4, col5, col6 = st.columns(3)
        col4.metric("Itens cadastrados",      len(tabela_estoque))
        col5.metric("Valor total em estoque", f"R$ {tabela_estoque['Valor Total R$'].sum():,.2f}")
        col6.metric("Itens com estoque baixo", len(tabela_estoque[tabela_estoque["Status"] == "Estoque baixo"]))

# ─────────────────────────────────────────────
# MENU: APLICAÇÕES
# CORREÇÕES:
#   - operador/pulverizador/velocidade/pressao/clima movidos para fora do loop
#   - loop aninhado duplicado removido
#   - key duplicada no botão corrigida com índice único
# ─────────────────────────────────────────────
elif menu == "Aplicações":
    st.header("🚜 Aplicações Agrícolas")

    if "aplicacoes" not in st.session_state:
        st.session_state.aplicacoes = []

    if len(st.session_state.estoque) == 0:
        warning_box("Cadastre produtos no estoque antes de registrar aplicações.")
    else:
        tipos_aplicacao = [
            "Pré-plantio","Pós-plantio","V0","Herbicida seletivo",
            "1ª Fungicida","2ª Fungicida","3ª Fungicida","4ª Fungicida",
            "5ª Fungicida","6ª Fungicida","Outra"
        ]
        tipo_aplicacao = st.selectbox("Tipo de aplicação", tipos_aplicacao)
        nome_aplicacao = st.text_input("Nome da aplicação", placeholder="Ex: Aplicação de inseticida") if tipo_aplicacao == "Outra" else tipo_aplicacao

        col_a, col_b, col_c = st.columns(3)
        with col_a: data_aplicacao = st.date_input("Data da aplicação")
        with col_b: area_aplicada  = st.number_input("Área aplicada em hectares", min_value=0.0, value=float(st.session_state.dados.get("area", 0.0)))
        with col_c: litros_por_hectare = st.number_input("Volume de calda L/ha", min_value=0.0, value=75.0)

        capacidade_tanque  = st.number_input("Capacidade do tanque em litros", min_value=0.0, value=3000.0)
        area_por_tanque    = (capacidade_tanque / litros_por_hectare) if litros_por_hectare > 0 else 0
        numero_tanques     = (area_aplicada / area_por_tanque) if area_por_tanque > 0 else 0

        col_t1, col_t2 = st.columns(2)
        col_t1.metric("Área por tanque",            f"{area_por_tanque:.2f} ha")
        col_t2.metric("Número estimado de tanques", f"{numero_tanques:.2f}")

        # CORREÇÃO 6: campos do operador fora do loop de produtos
        st.subheader("🧑‍🌾 Dados do Operador")
        operador         = st.text_input("Operador da aplicação")
        pulverizador     = st.text_input("Pulverizador / Máquina")
        velocidade       = st.number_input("Velocidade de aplicação (km/h)", min_value=0.0, value=0.0)
        pressao          = st.number_input("Pressão de trabalho (bar)", min_value=0.0, value=0.0)
        clima_aplicacao  = st.selectbox("Condição climática", ["Adequada","Vento alto","Muito seco","Chuva próxima","Muito quente"])

        quantidade_produtos = st.number_input("Quantidade de produtos usados", min_value=1, max_value=10, value=1)
        produtos_usados = []

        for i in range(quantidade_produtos):
            st.markdown(f"### Produto {i + 1}")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                produto = st.selectbox(f"Produto {i+1}", [item["Insumo"] for item in st.session_state.estoque], key=f"produto_aplicacao_{i}")
            with col2:
                dose_ha = st.number_input(f"Dose por hectare {i+1}", min_value=0.0, value=0.0, key=f"dose_ha_aplicacao_{i}")
            with col3:
                unidade = st.selectbox(f"Unidade {i+1}", ["litros/ha","ml/ha","kg/ha","g/ha"], key=f"unidade_aplicacao_{i}")
            with col4:
                obs_produto = st.text_input(f"Observação {i+1}", key=f"obs_produto_aplicacao_{i}")
            produto_por_tanque = dose_ha * area_por_tanque
            produto_total      = dose_ha * area_aplicada
            info_box(f"{produto}: {produto_por_tanque:.2f} {unidade.replace('/ha','')} por tanque | Total na área: {produto_total:.2f} {unidade.replace('/ha','')}")
            produtos_usados.append({
                "Produto": produto, "Dose por ha": dose_ha, "Unidade": unidade,
                "Produto por tanque": produto_por_tanque, "Total usado": produto_total, "Observação": obs_produto
            })

        if st.button("Salvar Aplicação", key="salvar_aplicacao_modelada"):
            erro = False
            if nome_aplicacao.strip() == "": error_box("Informe o nome da aplicação."); erro = True
            if area_aplicada <= 0:           error_box("Informe a área aplicada."); erro = True
            if litros_por_hectare <= 0:      error_box("Informe o volume de calda em L/ha."); erro = True
            if capacidade_tanque <= 0:       error_box("Informe a capacidade do tanque."); erro = True
            for p in produtos_usados:
                if p["Dose por ha"] <= 0: error_box(f"Informe dose maior que zero para {p['Produto']}."); erro = True
            if not erro:
                for p in produtos_usados:
                    sucesso, mensagem = baixar_estoque(p["Produto"], p["Total usado"])
                    if not sucesso: error_box(f"{p['Produto']}: {mensagem}"); erro = True
            if not erro:
                st.session_state.aplicacoes.append({
                    "ID Área":            st.session_state.dados.get("id_area",""),
                    "Aplicação":          nome_aplicacao,
                    "Data":               str(data_aplicacao),
                    "Área aplicada ha":   area_aplicada,
                    "Volume calda L/ha":  litros_por_hectare,
                    "Capacidade tanque L": capacidade_tanque,
                    "Área por tanque ha": area_por_tanque,
                    "Número tanques":     numero_tanques,
                    "Operador":           operador,
                    "Pulverizador":       pulverizador,
                    "Velocidade km/h":    velocidade,
                    "Pressão bar":        pressao,
                    "Clima aplicação":    clima_aplicacao,
                    "Produtos":           produtos_usados
                })
                atualizar_area_atual()
                salvar_dados_iaagro()
                success_box(f"{nome_aplicacao} salva com sucesso.")

        # ── Histórico
        st.divider()
        st.subheader("📋 Histórico de Aplicações")
        if len(st.session_state.aplicacoes) == 0:
            info_box("Nenhuma aplicação registrada ainda.")
        else:
            ordem = {"Pré-plantio":1,"Pós-plantio":2,"V0":3,"Herbicida seletivo":4,
                     "1ª Fungicida":5,"2ª Fungicida":6,"3ª Fungicida":7,"4ª Fungicida":8,"5ª Fungicida":9,"6ª Fungicida":10}
            aplicacoes_ordenadas = sorted(st.session_state.aplicacoes, key=lambda x: ordem.get(x.get("Aplicação",""), 99))

            for aplicacao in aplicacoes_ordenadas:
                with st.expander(f"{aplicacao.get('Aplicação','Sem nome')} - {aplicacao.get('Data','Sem data')}"):
                    st.write(f"Área aplicada: {aplicacao.get('Área aplicada ha', 0)} ha")
                    st.write(f"Volume de calda: {aplicacao.get('Volume calda L/ha', 0)} L/ha")
                    st.write(f"Capacidade do tanque: {aplicacao.get('Capacidade tanque L', 0)} L")
                    st.write(f"Área por tanque: {aplicacao.get('Área por tanque ha', 0):.2f} ha")
                    st.write(f"Número estimado de tanques: {aplicacao.get('Número tanques', 0):.2f}")
                    tabela_ap = pd.DataFrame(aplicacao.get("Produtos", []))
                    st.dataframe(tabela_ap, use_container_width=True)

            st.divider()
            st.subheader("🗑️ Gerenciar Aplicações")
            for i, app in enumerate(st.session_state.aplicacoes):
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.write(f"{app.get('Aplicação','Sem nome')} | {app.get('Data','Sem data')} | {app.get('Área aplicada ha', 0)} ha")
                with col2:
                    if st.button("Apagar", key=f"apagar_app_{i}"):
                        st.session_state.aplicacoes.pop(i)
                        salvar_dados_iaagro()
                        success_box("Aplicação removida com sucesso!")
                        st.rerun()

            # ── Folha técnica
            st.divider()
            st.subheader("🖨️ Folha Técnica de Aplicação")
            for aplicacao in aplicacoes_ordenadas:
                with st.container():
                    st.markdown(f"""
                    ### 🚜 {aplicacao.get('Aplicação','Sem nome')}
                    📅 **Data:** {aplicacao.get('Data','Sem data')}
                    👨‍🌾 **Operador:** {aplicacao.get('Operador','Não informado')}
                    🚜 **Pulverizador:** {aplicacao.get('Pulverizador','Não informado')}
                    ⚙️ **Velocidade:** {aplicacao.get('Velocidade km/h', 0)} km/h
                    🧭 **Pressão:** {aplicacao.get('Pressão bar', 0)} bar
                    🌦️ **Condição Climática:** {aplicacao.get('Clima aplicação','Não informado')}
                    📍 **Área Aplicada:** {aplicacao.get('Área aplicada ha', 0)} ha
                    💧 **Volume de Calda:** {aplicacao.get('Volume calda L/ha', 0)} L/ha
                    🚛 **Capacidade do Tanque:** {aplicacao.get('Capacidade tanque L', 0)} L
                    🌱 **Área por Tanque:** {aplicacao.get('Área por tanque ha', 0):.2f} ha
                    🔄 **Número de Tanques:** {aplicacao.get('Número tanques', 0):.2f}
                    """)
                    produtos = aplicacao.get("Produtos", [])
                    if produtos:
                        tab = pd.DataFrame(produtos).rename(columns={
                            "Dose por ha":"Dose/ha","Produto por tanque":"Por tanque","Total usado":"Total"
                        })
                        st.dataframe(tab, use_container_width=True, hide_index=True)
                    st.markdown("---")

            # ── Montagem Automática (Relatório Final chama isso também)
            st.divider()
            st.subheader("🚜 Montagem Automática da Aplicação")

            if len(st.session_state.estoque) > 0:
                cultura_aplicacao = st.selectbox("Cultura da aplicação", ["Soja","Milho"])
                produtos_filtrados = [
                    item for item in st.session_state.estoque
                    if item["Cultura"] == cultura_aplicacao or item["Cultura"] == "Ambos"
                ]
                area_aplicacao = st.number_input("Área da aplicação (ha)", min_value=0.1, value=10.0, key="area_aplicacao_tanque")

                st.write("Produtos disponíveis para aplicação:")

                for produto in produtos_filtrados:
                    st.markdown(
                        f'<div style="background:#14532d;color:#fff;padding:10px 16px;'
                        f'border-radius:10px;border-left:5px solid #22c55e;'
                        f'font-weight:600;margin:4px 0;">'
                        f'✅ {produto["Insumo"]} | Dose: {produto["Dose ha"]} ha | Tanque: {produto["Tanque litros"]}L'
                        f'</div>', unsafe_allow_html=True
                    )

                st.subheader("🧪 Cálculo Automático por Tanque")
                for produto in produtos_filtrados:
                    dose             = produto["Dose ha"]
                    litros_ha_p      = produto["Litros ha"]
                    tanque           = produto["Tanque litros"]
                    hectares_por_tanque    = tanque / litros_ha_p if litros_ha_p > 0 else 0
                    quantidade_produto_tanque = dose * hectares_por_tanque
                    total_necessario   = dose * area_aplicacao
                    st.markdown(f'''<div style="background:#1e3a5f;color:#fff;padding:14px 18px;
                    border-radius:12px;border-left:5px solid #3b82f6;
                    font-size:14px;font-weight:600;line-height:2.0;margin:6px 0;">
                    🌱 <b>Produto:</b> {produto['Insumo']}<br>
                    🚜 <b>Dose/ha:</b> {dose}<br>
                    💧 <b>Litros/ha:</b> {litros_ha_p}<br>
                    🛢️ <b>Tanque:</b> {tanque} L<br>
                    📐 <b>Ha por tanque:</b> {hectares_por_tanque:.2f}<br>
                    🧪 <b>Produto por tanque:</b> {quantidade_produto_tanque:.2f}<br>
                    📦 <b>Total para {area_aplicacao:.1f} ha:</b> {total_necessario:.2f}
                    </div>''', unsafe_allow_html=True)

                # CORREÇÃO 4: key única por produto para evitar DuplicateWidgetID
                if st.button("Salvar Aplicação Automática", key="salvar_aplicacao_auto_geral"):
                    nova_aplicacao = {
                        "Data":            str(date.today()),
                        "ID Área":         st.session_state.get("dados", {}).get("id_area",""),
                        "Talhão":          st.session_state.get("dados", {}).get("talhao",""),
                        "Cultura":         cultura_aplicacao,
                        "Aplicação":       "Aplicação Automática",
                        "Tipo":            "Aplicação Automática",
                        "Operador":        "",
                        "Pulverizador":    "",
                        "Velocidade km/h": 0,
                        "Pressão bar":     0,
                        "Clima aplicação": "Não informado",
                        "Área ha":         area_aplicacao,
                        "Produtos":        produtos_filtrados
                    }
                    for produto_aplicado in produtos_filtrados:
                        nome_produto    = produto_aplicado["Insumo"]
                        quantidade_usada = produto_aplicado["Dose ha"] * area_aplicacao
                        for item_estoque in st.session_state.estoque:
                            if item_estoque["Insumo"] == nome_produto:
                                item_estoque["Quantidade"] = max(0, item_estoque["Quantidade"] - quantidade_usada)
                    st.session_state.aplicacoes.append(nova_aplicacao)
                    salvar_dados_iaagro()
                    success_box("Aplicação automática salva com sucesso!")

                    if len(produtos_filtrados) > 0:
                        ficha_linhas = []
                        for produto in produtos_filtrados:
                            d_p  = produto["Dose ha"]
                            l_ha = produto["Litros ha"]
                            tnq  = produto["Tanque litros"]
                            v_u  = produto.get("Valor Unitário R$", 0)
                            hpt  = tnq / l_ha if l_ha > 0 else 0
                            ficha_linhas.append({
                                "Produto": produto["Insumo"],
                                "Dose/ha": d_p, "Litros/ha": l_ha, "Tanque L": tnq,
                                "Ha por tanque": round(hpt, 2),
                                "Produto por tanque": round(d_p * hpt, 2),
                                "Total na área": round(d_p * area_aplicacao, 2)
                            })
                        df_ficha = pd.DataFrame(ficha_linhas)
                        st.dataframe(df_ficha, use_container_width=True)
                        st.download_button(
                            "📥 Baixar ficha CSV",
                            data=df_ficha.to_csv(index=False).encode("utf-8"),
                            file_name=f"ficha_aplicacao_{cultura_aplicacao}.csv",
                            mime="text/csv"
                        )

        # ── Histórico completo de aplicações (tabela)
        st.divider()
        st.subheader("Aplicações Registradas")
        if len(st.session_state.aplicacoes) == 0:
            info_box("Nenhuma aplicação registrada.")
        else:
            historico_linhas = []
            for aplicacao in st.session_state.aplicacoes:
                for prod in aplicacao.get("Produtos", []):
                    historico_linhas.append({
                        "Data":             aplicacao.get("Data",""),
                        "ID Área":          aplicacao.get("ID Área",""),
                        "Talhão":           aplicacao.get("Talhão",""),
                        "Tipo":             aplicacao.get("Tipo",""),
                        "Produto":          prod.get("Insumo", prod.get("Produto","")),
                        "Dose/ha":          prod.get("Dose por ha", prod.get("Dose ha","")),
                        "Quantidade usada": prod.get("Total usado", prod.get("Quantidade usada","")),
                        "Unidade":          prod.get("Unidade",""),
                        "Custo/ha":         prod.get("Custo_ha", 0),
                        "Custo Total":      prod.get("Custo Total", 0),
                    })
            st.dataframe(pd.DataFrame(historico_linhas), use_container_width=True)

# ─────────────────────────────────────────────
# MENU: RELATÓRIO FINAL
# ─────────────────────────────────────────────
elif menu == "Relatório Final":
    st.header("Relatório Final IAAgro")

    def gerar_pdf_relatorio(dados):
        buffer = BytesIO()
        doc    = SimpleDocTemplate(buffer, pagesize=A4,
                                   rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
        styles    = getSampleStyleSheet()
        elementos = []

        # Logo (com fallback se arquivo não existir)
        if os.path.exists("IAAgrologo.jpeg"):
            logo = Image("IAAgrologo.jpeg", width=140, height=70)
            elementos.append(logo)
        elementos.append(Spacer(1, 20))

        elementos.append(Paragraph(
            f"<b>Relatório Técnico IAAgro</b><br/>Data: {date.today()}<br/>Sistema Inteligente de Agricultura de Precisão",
            styles['BodyText']
        ))
        elementos.append(Spacer(1, 15))
        elementos.append(Paragraph("<b>IAAgro Pro V9 - Relatório Técnico</b>", styles['Title']))

        dados_tabela = [["Campo","Valor"]]
        for chave, valor in dados.items():
            dados_tabela.append([str(chave), str(valor)])

        tabela = Table(dados_tabela, colWidths=[180, 280])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkgreen),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('GRID',       (0,0), (-1,-1), 1, colors.black),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME',   (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE',   (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ]))
        elementos.append(tabela)
        elementos.append(Spacer(1, 20))

        if   dados.get("ph",0) >= 5.5 and dados.get("materia_organica",0) >= 2:
            classificacao     = "ALTO POTENCIAL PRODUTIVO"
            cor_classificacao = colors.green
        elif dados.get("ph",0) >= 5.0:
            classificacao     = "POTENCIAL MÉDIO"
            cor_classificacao = colors.orange
        else:
            classificacao     = "SOLO COM LIMITAÇÕES"
            cor_classificacao = colors.red

        class_box = Table([["Classificação IAAgro", classificacao]], colWidths=[220, 240])
        class_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.darkgreen),
            ('BACKGROUND', (1,0), (1,0), cor_classificacao),
            ('TEXTCOLOR',  (0,0), (-1,-1), colors.white),
            ('FONTNAME',   (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,-1), 12),
            ('GRID',       (0,0), (-1,-1), 1, colors.black),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        elementos.append(class_box)
        elementos.append(Spacer(1, 20))
        elementos.append(Paragraph(
            """<b>Recomendação Inteligente IAAgro:</b><br/><br/>
            • Solo com potencial produtivo médio/alto.<br/>
            • Recomendado monitoramento de fósforo e matéria orgânica.<br/>
            • Ajustar manejo conforme produtividade esperada.<br/>
            • Realizar acompanhamento de micronutrientes durante o ciclo.<br/>
            • Sistema gerado automaticamente pela IA do IAAgro.""",
            styles['BodyText']
        ))
        elementos.append(PageBreak())
        elementos.append(Paragraph("<b>Mapa GPS do Talhão</b>", styles['Title']))
        elementos.append(Spacer(1, 20))
        elementos.append(Paragraph("Imagem do mapa GPS do talhão será inserida aqui.", styles["BodyText"]))
        doc.build(elementos)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    d = st.session_state.dados

    if "ph" not in d or "fazenda" not in d:
        warning_box("Preencha os dados antes de gerar relatório.")
    else:
        nota             = calcular_nota(d)
        prioridade_final = prioridade(nota)
        dose_calcario, total_calcario = calcular_calcario_por_ph(d["ph"], d["area"])
        precisa_gesso, dose_gesso, total_gesso, motivos_gesso = calcular_gesso(d)
        producao_estimada = estimar_producao(d["produtividade"], nota)

        # IA de previsão
        indice_produtivo = 0
        score_rel        = 75
        indice_produtivo += score_rel * 0.45
        if 5.8 <= d["ph"] <= 6.5:               indice_produtivo += 15
        if d["fosforo"] >= 12:                   indice_produtivo += 10
        if d["potassio"] >= 0.35:                indice_produtivo += 10
        if d["materia_organica"] >= 3:           indice_produtivo += 10
        if d.get("argila", 0) >= 35:             indice_produtivo += 5
        indice_produtivo = min(indice_produtivo, 100)
        produtividade_ia = d["produtividade"] * (indice_produtivo / 100)

        if   produtividade_ia >= d["produtividade"] * 0.9: status_ia = "🟢 Alto Potencial"
        elif produtividade_ia >= d["produtividade"] * 0.7: status_ia = "🟡 Médio Potencial"
        else:                                               status_ia = "🔴 Baixo Potencial"

        n, p2o5, k2o = recomendacao_npk(
            d["cultura"], d["produtividade"], d["fosforo"], d["potassio"], d["materia_organica"]
        )

        st.subheader("Resumo da Área")
        st.write(f"ID da área: {d.get('id_area','')}")
        st.write(f"Fazenda: {d['fazenda']}")
        st.write(f"Talhão: {d['talhao']}")
        st.write(f"Cidade/Estado: {d['cidade']}")
        st.write(f"Área: {d['area']} hectares")
        st.write(f"Cultura: {d['cultura']}")
        st.write(f"Meta de produtividade: {d['produtividade']} sacas/ha")

        st.subheader("Resultado Geral")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Nota",              f"{nota}/100")
        col2.metric("Prioridade",        prioridade_final)
        col3.metric("Produção Estimada", f"{producao_estimada:.1f} sc/ha")
        col4.metric("Calcário",          f"{dose_calcario} t/ha")
        col5.metric("Gesso",             f"{dose_gesso} t/ha")
        col6.metric("IA Produtividade",  f"{produtividade_ia:.1f} sc/ha")

        st.subheader("Correção")
        st.write(f"Dose estimada de calcário: {dose_calcario} t/ha")
        st.write(f"Total estimado de calcário: {total_calcario:.1f} toneladas")
        st.write(f"Dose estimada de gesso: {dose_gesso} t/ha")
        st.write(f"Total estimado de gesso: {total_gesso:.1f} toneladas")

        st.subheader("Adubação NPK")
        tabela_npk = pd.DataFrame({
            "Nutriente":          ["N","P2O5","K2O"],
            "Dose kg/ha":         [n, p2o5, k2o],
            "Total no talhão kg": [n * d["area"], p2o5 * d["area"], k2o * d["area"]]
        })
        st.dataframe(tabela_npk, use_container_width=True)

        st.subheader("Estoque Atual")
        if len(st.session_state.estoque) == 0:
            info_box("Nenhum produto cadastrado.")
        else:
            st.dataframe(pd.DataFrame(st.session_state.estoque), use_container_width=True)

        st.subheader("Aplicações Registradas")
        if len(st.session_state.aplicacoes) == 0:
            info_box("Nenhuma aplicação registrada.")
        else:
            historico_linhas = []
            for aplicacao in st.session_state.aplicacoes:
                for prod in aplicacao.get("Produtos", []):
                    historico_linhas.append({
                        "Data":    aplicacao.get("Data",""),
                        "ID Área": aplicacao.get("ID Área",""),
                        "Talhão":  aplicacao.get("Talhão",""),
                        "Tipo":    aplicacao.get("Tipo",""),
                        "Produto": prod.get("Insumo", prod.get("Produto","")),
                        "Dose/ha": prod.get("Dose por ha", prod.get("Dose ha","")),
                        "Quantidade usada": prod.get("Total usado", prod.get("Quantidade usada","")),
                        "Unidade": prod.get("Unidade",""),
                    })
            st.dataframe(pd.DataFrame(historico_linhas), use_container_width=True)

        st.subheader("Parecer IAAgro")
        st.markdown(f'''<div style="background:#1e3a5f;color:#fff;padding:15px 18px;
        border-radius:12px;border-left:5px solid #3b82f6;
        font-size:15px;font-weight:600;line-height:2.0;margin:8px 0;">
        📋 A área <b>{d.get('id_area','')}</b> apresenta prioridade de correção <b>{prioridade_final}</b>.<br>
        📈 Produtividade estimada: <b>{producao_estimada:.1f} sacas/ha</b><br>
        🧪 O sistema avaliou calcário, gesso, adubação, estoque e aplicações.<br>
        🗂️ Cada área possui ID próprio e pode ser carregada pela aba Áreas Cadastradas.
        </div>''', unsafe_allow_html=True)
        st.divider()

        pdf_relatorio = gerar_pdf_relatorio(d)
        st.download_button(
            label="📄 Baixar Relatório PDF",
            data=pdf_relatorio,
            file_name="relatorio_iaagro.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# ─────────────────────────────────────────────
# MENU: CLIMA & ALERTAS
# ─────────────────────────────────────────────
elif menu == "🌤️ Clima & Alertas":
    st.header("🌤️ Clima em Tempo Real & Alertas de Aplicação")

    # Geolocalização
    geo = get_geolocation()
    if geo:
        lat = geo["coords"]["latitude"]
        lon = geo["coords"]["longitude"]
    else:
        lat = st.session_state.dados.get("latitude", -26.88)
        lon = st.session_state.dados.get("longitude", -52.40)

    st.markdown(f'''<div style="background:#0f3460;color:#fff;padding:12px 18px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
    📍 Localização: {lat:.4f}, {lon:.4f}</div>''', unsafe_allow_html=True)

    if st.button("🔄 Atualizar Clima", key="btn_clima"):
        st.session_state.clima_data = buscar_clima(lat, lon)

    dados_clima = st.session_state.get("clima_data") or buscar_clima(lat, lon)

    if dados_clima:
        current = dados_clima.get("current", {})
        daily   = dados_clima.get("daily", {})

        temp      = current.get("temperature_2m", 0)
        umidade   = current.get("relative_humidity_2m", 0)
        chuva     = current.get("precipitation", 0)
        vento     = current.get("windspeed_10m", 0)
        wcode     = current.get("weathercode", 0)
        emoji_c, desc_c = codigo_clima_emoji(wcode)

        # Cards clima atual
        st.subheader(f"{emoji_c} Condição Atual — {desc_c}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🌡️ Temperatura",  f"{temp:.1f} °C")
        col2.metric("💧 Umidade",       f"{umidade:.0f}%")
        col3.metric("🌧️ Precipitação", f"{chuva:.1f} mm")
        col4.metric("💨 Vento",         f"{vento:.1f} km/h")

        # Alerta de aplicação
        st.divider()
        st.subheader("🚜 Condição para Aplicação de Defensivos")
        alertas_ap = alerta_clima_aplicacao(wcode, vento, chuva)
        if alertas_ap:
            for a in alertas_ap:
                st.markdown(f'''<div style="background:#7f1d1d;color:#fff;padding:12px 18px;
                border-radius:10px;border-left:5px solid #ef4444;font-weight:700;margin:6px 0;">
                {a}</div>''', unsafe_allow_html=True)
        else:
            st.markdown('''<div style="background:#14532d;color:#fff;padding:12px 18px;
            border-radius:10px;border-left:5px solid #22c55e;font-weight:700;margin:6px 0;">
            ✅ Condições adequadas para aplicação!</div>''', unsafe_allow_html=True)

        # Condições ideais por parâmetro
        st.divider()
        st.subheader("📋 Janela Ideal de Aplicação")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            ok_temp = 10 <= temp <= 30
            st.markdown(f'''<div style="background:{'#14532d' if ok_temp else '#78350f'};color:#fff;
            padding:12px;border-radius:10px;text-align:center;font-weight:700;">
            🌡️ Temperatura<br><b>{temp:.1f}°C</b><br>{"✅ Ideal" if ok_temp else "⚠️ Fora do ideal (10-30°C)"}</div>''',
            unsafe_allow_html=True)
        with col_b:
            ok_vento = vento <= 10
            st.markdown(f'''<div style="background:{'#14532d' if ok_vento else '#78350f'};color:#fff;
            padding:12px;border-radius:10px;text-align:center;font-weight:700;">
            💨 Vento<br><b>{vento:.1f} km/h</b><br>{"✅ Ideal" if ok_vento else "⚠️ Alto (max 10 km/h)"}</div>''',
            unsafe_allow_html=True)
        with col_c:
            ok_chuva = chuva == 0
            st.markdown(f'''<div style="background:{'#14532d' if ok_chuva else '#7f1d1d'};color:#fff;
            padding:12px;border-radius:10px;text-align:center;font-weight:700;">
            🌧️ Chuva<br><b>{chuva:.1f} mm</b><br>{"✅ Sem chuva" if ok_chuva else "❌ Aguarde a chuva passar"}</div>''',
            unsafe_allow_html=True)

        # Previsão 7 dias
        st.divider()
        st.subheader("📅 Previsão para os Próximos 7 Dias")
        if daily and "temperature_2m_max" in daily:
            datas       = daily.get("time", [])
            temp_max    = daily.get("temperature_2m_max", [])
            temp_min    = daily.get("temperature_2m_min", [])
            chuva_d     = daily.get("precipitation_sum", [])
            vento_d     = daily.get("windspeed_10m_max", [])

            df_prev = pd.DataFrame({
                "Data":       datas,
                "Temp Máx °C": temp_max,
                "Temp Mín °C": temp_min,
                "Chuva mm":   chuva_d,
                "Vento km/h": vento_d,
            })
            df_prev["Aplicar?"] = df_prev.apply(
                lambda r: "✅ Sim" if r["Chuva mm"] == 0 and r["Vento km/h"] <= 10
                          else "❌ Não", axis=1
            )
            st.dataframe(df_prev, use_container_width=True)
            st.line_chart(df_prev.set_index("Data")[["Temp Máx °C","Temp Mín °C","Chuva mm"]])

            # Melhor janela de aplicação
            dias_bons = df_prev[df_prev["Aplicar?"] == "✅ Sim"]
            if not dias_bons.empty:
                st.markdown(f'''<div style="background:#14532d;color:#fff;padding:13px 18px;
                border-radius:10px;border-left:5px solid #22c55e;font-weight:700;margin:8px 0;">
                📅 Melhores dias para aplicação: {", ".join(dias_bons["Data"].tolist())}
                </div>''', unsafe_allow_html=True)
    else:
        st.markdown('''<div style="background:#78350f;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #f59e0b;font-weight:600;">
        ⚠️ Não foi possível buscar dados climáticos. Verifique sua conexão com a internet.
        </div>''', unsafe_allow_html=True)

        # Modo offline — entrada manual
        st.subheader("✍️ Inserir Condições Manualmente")
        col1, col2, col3 = st.columns(3)
        with col1: temp_m    = st.number_input("Temperatura °C", 0.0, 50.0, 25.0)
        with col2: vento_m   = st.number_input("Vento km/h", 0.0, 100.0, 8.0)
        with col3: chuva_m   = st.number_input("Precipitação mm", 0.0, 200.0, 0.0)
        alertas_m = alerta_clima_aplicacao(0, vento_m, chuva_m)
        if alertas_m:
            for a in alertas_m:
                st.markdown(f'''<div style="background:#7f1d1d;color:#fff;padding:12px 18px;
                border-radius:10px;border-left:5px solid #ef4444;font-weight:700;">{a}</div>''',
                unsafe_allow_html=True)
        else:
            st.markdown('''<div style="background:#14532d;color:#fff;padding:12px 18px;
            border-radius:10px;border-left:5px solid #22c55e;font-weight:700;">
            ✅ Condições adequadas para aplicação!</div>''', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MENU: PREÇOS DE MERCADO
# ─────────────────────────────────────────────
elif menu == "💰 Preços de Mercado":
    st.header("💰 Preços de Commodities & Análise de Rentabilidade")

    if st.button("🔄 Atualizar Preços", key="btn_precos"):
        st.session_state.precos_data = buscar_precos_commodities()

    precos = st.session_state.get("precos_data") or buscar_precos_commodities()

    # Exibe preços atuais
    st.subheader("📊 Preços de Referência (sc/60kg)")
    soja_p  = precos.get("soja_sc",  {}).get("preco", 135.0)
    milho_p = precos.get("milho_sc", {}).get("preco", 68.0)
    trigo_p = precos.get("trigo_sc", {}).get("preco", 95.0)
    dolar_p = precos.get("dolar",    {}).get("preco", 5.15)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌱 Soja",    f"R$ {soja_p:.2f}/sc")
    col2.metric("🌽 Milho",   f"R$ {milho_p:.2f}/sc")
    col3.metric("🌾 Trigo",   f"R$ {trigo_p:.2f}/sc")
    col4.metric("💵 Dólar",   f"R$ {dolar_p:.2f}")

    fonte = precos.get("soja_sc", {}).get("fonte", "")
    if fonte:
        st.markdown(f'''<div style="background:#1e3a5f;color:#93c5fd;padding:8px 14px;
        border-radius:8px;font-size:13px;margin:6px 0;">ℹ️ Fonte: {fonte}</div>''',
        unsafe_allow_html=True)

    st.divider()

    # Simulador de rentabilidade por área
    st.subheader("🧮 Simulador de Rentabilidade por Talhão")
    d = st.session_state.dados

    if not d.get("area"):
        st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;">
        ℹ️ Cadastre uma área primeiro para usar o simulador.</div>''', unsafe_allow_html=True)
    else:
        cultura_sim   = d.get("cultura", "Soja")
        area_sim      = float(d.get("area", 10))
        produt_sim    = float(d.get("produtividade", 60))

        preco_map = {"Soja": soja_p, "Milho": milho_p, "Trigo": trigo_p}
        preco_sim = preco_map.get(cultura_sim, soja_p)

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            produt_real   = st.number_input("Produtividade esperada (sc/ha)", 0.0, 500.0, produt_sim)
            preco_custom  = st.number_input("Preço da saca (R$)", 0.0, 1000.0, preco_sim)
        with col_s2:
            custo_ha      = st.number_input("Custo total por hectare (R$)", 0.0, 50000.0, 3200.0)
            area_calc     = st.number_input("Área (ha)", 0.1, 100000.0, area_sim)

        receita       = produt_real * preco_custom * area_calc
        custo_total   = custo_ha * area_calc
        lucro         = receita - custo_total
        margem        = (lucro / receita * 100) if receita > 0 else 0
        breakeven     = custo_ha / preco_custom if preco_custom > 0 else 0
        preco_min     = custo_ha / produt_real if produt_real > 0 else 0

        st.divider()
        col_r1, col_r2, col_r3 = st.columns(3)
        col_r1.metric("💰 Receita Total",  f"R$ {receita:,.0f}")
        col_r2.metric("💸 Custo Total",    f"R$ {custo_total:,.0f}")
        col_r3.metric("💵 Lucro Líquido",  f"R$ {lucro:,.0f}")

        col_r4, col_r5, col_r6 = st.columns(3)
        col_r4.metric("📊 Margem",           f"{margem:.1f}%")
        col_r5.metric("⚖️ Break-even sc/ha", f"{breakeven:.1f} sc")
        col_r6.metric("💲 Preço mín R$/sc",  f"R$ {preco_min:.2f}")

        if lucro > 0:
            st.markdown(f'''<div style="background:#14532d;color:#fff;padding:13px 18px;
            border-radius:10px;border-left:5px solid #22c55e;font-weight:700;font-size:16px;margin:10px 0;">
            ✅ Operação LUCRATIVA — Lucro de R$ {lucro:,.2f} com margem de {margem:.1f}%
            </div>''', unsafe_allow_html=True)
        else:
            st.markdown(f'''<div style="background:#7f1d1d;color:#fff;padding:13px 18px;
            border-radius:10px;border-left:5px solid #ef4444;font-weight:700;font-size:16px;margin:10px 0;">
            ❌ Operação no PREJUÍZO — Revise custos ou produtividade esperada.
            </div>''', unsafe_allow_html=True)

        # Análise de sensibilidade — variação de preço
        st.divider()
        st.subheader("📈 Análise de Sensibilidade — Variação de Preço")
        precos_range  = [preco_custom * f for f in [0.7,0.8,0.9,1.0,1.1,1.2,1.3]]
        lucros_range  = [(p * produt_real * area_calc - custo_total) for p in precos_range]
        df_sens = pd.DataFrame({
            "Preço R$/sc": [f"R$ {p:.0f}" for p in precos_range],
            "Lucro R$":    [round(l, 2) for l in lucros_range]
        })
        st.dataframe(df_sens, use_container_width=True)
        st.bar_chart(pd.Series(lucros_range, index=[f"R${p:.0f}" for p in precos_range]))

        # Comparativo entre culturas
        st.divider()
        st.subheader("🔄 Comparativo Entre Culturas")
        comp_data = []
        for cult, preco_c in [("Soja", soja_p), ("Milho", milho_p), ("Trigo", trigo_p)]:
            prod_c = {"Soja": 65, "Milho": 180, "Trigo": 55}[cult]
            rec_c  = prod_c * preco_c * area_calc
            luc_c  = rec_c - custo_total
            comp_data.append({
                "Cultura": cult, "Produt. média sc/ha": prod_c,
                "Preço R$/sc": preco_c,
                "Receita R$": round(rec_c, 2),
                "Lucro R$":   round(luc_c, 2),
                "Margem %":   round((luc_c/rec_c*100) if rec_c > 0 else 0, 1)
            })
        st.dataframe(pd.DataFrame(comp_data), use_container_width=True)


# ─────────────────────────────────────────────
# MENU: OCR LAUDO DE SOLO
# ─────────────────────────────────────────────
elif menu == "📄 OCR Laudo de Solo":
    st.header("📄 Leitura Automática de Laudo de Solo")
    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
    ℹ️ Faça upload do seu laudo de solo (PDF ou imagem JPG/PNG) e o sistema tentará
    extrair os valores automaticamente usando OCR e preenchê-los na análise de solo.
    </div>''', unsafe_allow_html=True)

    tipo_arquivo = st.radio("Tipo de arquivo", ["📄 PDF", "🖼️ Imagem (JPG/PNG)"],
                            horizontal=True, key="ocr_tipo")

    st.markdown("""
    <style>
    [data-testid="stFileUploaderDropzone"],
    [data-testid="stFileUploaderDropzone"] > div {
        background-color: #0f3460 !important;
        border: 2px solid #22c55e !important;
        border-radius: 12px !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background-color: #16a34a !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }
    [data-testid="stFileUploaderDropzone"] span,
    [data-testid="stFileUploaderDropzone"] p,
    [data-testid="stFileUploaderDropzone"] div,
    [data-testid="stFileUploaderDropzone"] button span {
        color: #ffffff !important; opacity: 1 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    texto_ocr    = ""
    campos_ocr   = {}

    if tipo_arquivo == "📄 PDF":
        arquivo_laudo = st.file_uploader("Upload do laudo PDF", type=["pdf"], key="ocr_pdf")
        if arquivo_laudo:
            with st.spinner("🔍 Lendo PDF..."):
                texto_ocr = extrair_texto_pdf(arquivo_laudo)
    else:
        arquivo_laudo = st.file_uploader("Upload da imagem do laudo", type=["jpg","jpeg","png"], key="ocr_img")
        if arquivo_laudo:
            img_pil = PILImage.open(arquivo_laudo)
            st.image(img_pil, caption="Laudo enviado", use_container_width=True)
            with st.spinner("🔍 Aplicando OCR..."):
                texto_ocr = extrair_texto_imagem(arquivo_laudo)

    if texto_ocr:
        with st.expander("📝 Texto extraído (clique para ver)"):
            st.text(texto_ocr[:3000])

        campos_ocr = parsear_laudo_ocr(texto_ocr)

        if campos_ocr:
            st.subheader("✅ Valores detectados automaticamente")
            df_ocr = pd.DataFrame([{
                "Campo": k.replace("_"," ").title(),
                "Valor detectado": v
            } for k, v in campos_ocr.items()])
            st.dataframe(df_ocr, use_container_width=True)

            st.subheader("✏️ Confirme ou ajuste os valores")
            cols_ocr = st.columns(3)
            campos_editados = {}
            campos_lista = list(campos_ocr.items())
            for i, (campo, val) in enumerate(campos_lista):
                with cols_ocr[i % 3]:
                    campos_editados[campo] = st.number_input(
                        campo.replace("_"," ").title(),
                        value=float(val),
                        key=f"ocr_{campo}"
                    )

            if st.button("📥 Importar valores para Análise de Solo", key="btn_importar_ocr"):
                if not st.session_state.area_selecionada:
                    st.markdown('''<div style="background:#7f1d1d;color:#fff;padding:12px 18px;
                    border-radius:10px;border-left:5px solid #ef4444;font-weight:700;">
                    ❌ Carregue uma área primeiro em "Áreas Cadastradas".</div>''',
                    unsafe_allow_html=True)
                else:
                    st.session_state.dados.update(campos_editados)
                    atualizar_area_atual()
                    salvar_dados_iaagro()
                    st.markdown(f'''<div style="background:#14532d;color:#fff;padding:13px 18px;
                    border-radius:10px;border-left:5px solid #22c55e;font-weight:700;">
                    ✅ {len(campos_editados)} campos importados para a área ativa!
                    Acesse "Análise de Solo" para conferir.</div>''', unsafe_allow_html=True)
        else:
            st.markdown('''<div style="background:#78350f;color:#fff;padding:13px 18px;
            border-radius:10px;border-left:5px solid #f59e0b;font-weight:600;margin:8px 0;">
            ⚠️ Não foi possível detectar valores automaticamente. Verifique se o laudo
            está legível e tente novamente. Você também pode inserir os dados manualmente
            na aba "Análise de Solo".</div>''', unsafe_allow_html=True)

            with st.expander("💡 Dicas para melhor resultado"):
                st.markdown("""
                - Use laudos com texto digital (não escaneados em baixa resolução)
                - Laudos da EMBRAPA, IAC e laboratórios com formato padrão funcionam melhor
                - Para imagens, tire a foto com boa iluminação e sem sombras
                - O OCR reconhece nomes como: pH, Fósforo, Potássio, Cálcio, Magnésio, Alumínio, Argila, CTC, MO
                """)

# ─────────────────────────────────────────────
# MENU: PRAZO DE CARÊNCIA
# ─────────────────────────────────────────────
elif menu == "⏱️ Prazo de Carência":
    st.header("⏱️ Controle de Prazo de Carência e Reentrada")
    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
    ℹ️ Registre os defensivos aplicados e acompanhe automaticamente os prazos de
    carência (colheita) e reentrada (entrada segura na lavoura).
    </div>''', unsafe_allow_html=True)

    # Init storage
    if "carencia_registros" not in st.session_state:
        st.session_state.carencia_registros = []

    # ── Cadastrar nova aplicação com carência ──
    st.subheader("➕ Registrar Aplicação com Carência")
    col1, col2, col3 = st.columns(3)
    with col1:
        car_produto    = st.text_input("Nome do produto/defensivo", key="car_produto")
        car_cultura    = st.selectbox("Cultura", ["Soja","Milho","Trigo","Feijão","Outra"], key="car_cultura")
        car_data_aplic = st.date_input("Data da aplicação", key="car_data")
    with col2:
        car_carencia   = st.number_input("Prazo de carência (dias)", min_value=0, value=14, key="car_carencia",
                                          help="Dias após aplicação até a colheita segura")
        car_reentrada  = st.number_input("Prazo de reentrada (horas)", min_value=0, value=48, key="car_reentrada",
                                          help="Horas após aplicação para entrar na lavoura com segurança")
        car_dose       = st.text_input("Dose aplicada", placeholder="Ex: 0.5 L/ha", key="car_dose")
    with col3:
        car_talhao     = st.text_input("Talhão/Área", key="car_talhao")
        car_epi        = st.multiselect("EPI necessário", 
                                         ["Máscara","Luvas","Óculos","Macacão","Botas","Protetor Auricular"],
                                         key="car_epi")
        car_obs        = st.text_area("Observações", key="car_obs", height=80)

    if st.button("💾 Salvar Registro de Carência", key="btn_salvar_carencia"):
        if not car_produto.strip():
            error_box("Digite o nome do produto.")
        else:
            from datetime import timedelta
            data_colheita_seg = car_data_aplic + timedelta(days=int(car_carencia))
            data_reentrada    = datetime.combine(car_data_aplic, datetime.min.time()) + timedelta(hours=int(car_reentrada))
            st.session_state.carencia_registros.append({
                "Produto":          car_produto,
                "Cultura":          car_cultura,
                "Talhão":           car_talhao,
                "Data Aplicação":   str(car_data_aplic),
                "Carência dias":    car_carencia,
                "Data Colheita Segura": str(data_colheita_seg),
                "Reentrada horas":  car_reentrada,
                "Data Reentrada":   str(data_reentrada.date()),
                "Dose":             car_dose,
                "EPI":              ", ".join(car_epi),
                "Observações":      car_obs,
            })
            salvar_dados_iaagro()
            success_box(f"Registro de {car_produto} salvo! Carência até: {data_colheita_seg} | Reentrada: {data_reentrada.strftime('%d/%m/%Y %H:%M')}")

    # ── Painel de situação ──
    if st.session_state.carencia_registros:
        st.divider()
        st.subheader("📊 Situação dos Prazos")

        hoje = date.today()
        registros_status = []
        for r in st.session_state.carencia_registros:
            data_colh  = date.fromisoformat(r["Data Colheita Segura"])
            data_reent = date.fromisoformat(r["Data Reentrada"])
            dias_colh  = (data_colh - hoje).days
            dias_reent = (data_reent - hoje).days

            if dias_colh < 0:
                status_colh = "✅ Liberado para colheita"
            elif dias_colh == 0:
                status_colh = "⚠️ Liberado hoje"
            else:
                status_colh = f"🔴 {dias_colh} dias para colheita segura"

            if dias_reent < 0:
                status_reent = "✅ Reentrada liberada"
            elif dias_reent == 0:
                status_reent = "⚠️ Reentrada liberada hoje"
            else:
                status_reent = f"🔴 Aguardar {dias_reent} dia(s) para reentrada"

            registros_status.append({
                "Produto":         r["Produto"],
                "Cultura":         r["Cultura"],
                "Talhão":          r["Talhão"],
                "Aplicação":       r["Data Aplicação"],
                "Colheita Segura": r["Data Colheita Segura"],
                "Status Colheita": status_colh,
                "Status Reentrada":status_reent,
                "EPI":             r["EPI"],
            })

        df_car = pd.DataFrame(registros_status)
        st.dataframe(df_car, use_container_width=True)

        # Alertas visuais
        st.divider()
        st.subheader("🚨 Alertas Ativos")
        alertas_ativos = False
        for r in registros_status:
            if "🔴" in r["Status Colheita"]:
                st.markdown(f'''<div style="background:#7f1d1d;color:#fff;padding:12px 18px;
                border-radius:10px;border-left:5px solid #ef4444;font-weight:700;margin:4px 0;">
                🌾 {r["Produto"]} — {r["Talhão"]}: {r["Status Colheita"]}</div>''',
                unsafe_allow_html=True)
                alertas_ativos = True
            if "🔴" in r["Status Reentrada"]:
                st.markdown(f'''<div style="background:#78350f;color:#fff;padding:12px 18px;
                border-radius:10px;border-left:5px solid #f59e0b;font-weight:700;margin:4px 0;">
                ⛔ {r["Produto"]} — {r["Talhão"]}: {r["Status Reentrada"]} | EPI: {r["EPI"]}</div>''',
                unsafe_allow_html=True)
                alertas_ativos = True
        if not alertas_ativos:
            success_box("Nenhum prazo de carência ou reentrada pendente no momento!")

        # Excluir registro
        st.divider()
        opcoes_del = [f"{r['Produto']} — {r['Talhão']} ({r['Data Aplicação']})"
                      for r in st.session_state.carencia_registros]
        del_choice = st.selectbox("Excluir registro", opcoes_del, key="del_carencia")
        if st.button("🗑️ Excluir", key="btn_del_carencia"):
            idx = opcoes_del.index(del_choice)
            st.session_state.carencia_registros.pop(idx)
            salvar_dados_iaagro()
            success_box("Registro removido.")
            st.rerun()


# ─────────────────────────────────────────────
# MENU: ORDEM DE SERVIÇO
# ─────────────────────────────────────────────
elif menu == "📋 Ordem de Serviço":
    st.header("📋 Ordem de Serviço")
    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
    ℹ️ Gere uma Ordem de Serviço completa para o operador ir ao campo. Pode ser impressa ou salva em PDF.
    </div>''', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        os_numero     = st.text_input("Número da OS", value=f"OS-{datetime.now().strftime('%Y%m%d%H%M')}")
        os_data       = st.date_input("Data da OS", value=date.today())
        os_fazenda    = st.text_input("Fazenda", value=st.session_state.dados.get("fazenda",""))
        os_talhao     = st.text_input("Talhão", value=st.session_state.dados.get("talhao",""))
        os_area       = st.number_input("Área (ha)", value=float(st.session_state.dados.get("area",0)))
        os_cultura    = st.text_input("Cultura", value=st.session_state.dados.get("cultura",""))
    with col2:
        os_operador   = st.text_input("Operador responsável")
        os_maquina    = st.text_input("Máquina / Pulverizador")
        os_velocidade = st.number_input("Velocidade (km/h)", value=6.0)
        os_pressao    = st.number_input("Pressão de trabalho (bar)", value=2.5)
        os_volume     = st.number_input("Volume de calda (L/ha)", value=100.0)
        os_inicio     = st.text_input("Horário previsto de início", placeholder="Ex: 06:30")

    st.subheader("🧪 Produtos da OS")
    os_qtd_produtos = st.number_input("Quantidade de produtos", min_value=1, max_value=10, value=1, key="os_qtd")
    os_produtos = []
    for i in range(int(os_qtd_produtos)):
        c1, c2, c3, c4 = st.columns(4)
        with c1: p_nome  = st.text_input(f"Produto {i+1}", key=f"os_prod_{i}")
        with c2: p_dose  = st.text_input(f"Dose/ha {i+1}", key=f"os_dose_{i}")
        with c3: p_total = st.text_input(f"Total {i+1}", key=f"os_total_{i}")
        with c4: p_obs   = st.text_input(f"Obs {i+1}", key=f"os_obs_{i}")
        if p_nome:
            os_produtos.append({"Produto": p_nome, "Dose/ha": p_dose,
                                 "Total": p_total, "Obs": p_obs})

    os_epi     = st.multiselect("EPI obrigatório", 
                                 ["Máscara com filtro","Luvas nitrílicas","Óculos de proteção",
                                  "Macacão impermeável","Botas de borracha","Protetor auricular","Avental"],
                                 key="os_epi")
    os_obs_geral = st.text_area("Observações gerais", key="os_obs_geral")

    if st.button("📄 Gerar Ordem de Serviço (PDF)", key="btn_gerar_os"):
        from reportlab.lib.units import cm
        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                rightMargin=1.5*cm, leftMargin=1.5*cm,
                                topMargin=1.5*cm, bottomMargin=1.5*cm)
        styles = getSampleStyleSheet()
        el = []

        # Cabeçalho
        if os.path.exists("IAAgrologo.jpeg"):
            el.append(Image("IAAgrologo.jpeg", width=3*cm, height=1.5*cm))
        el.append(Spacer(1, 6))

        # Título
        titulo_style = styles["Title"]
        el.append(Paragraph(f"<b>ORDEM DE SERVIÇO — {os_numero}</b>", titulo_style))
        el.append(Paragraph(f"Data: {os_data} | Fazenda: {os_fazenda} | Talhão: {os_talhao}", styles["Normal"]))
        el.append(Spacer(1, 12))

        # Dados gerais
        dados_os = [
            ["Campo","Informação","Campo","Informação"],
            ["Fazenda", os_fazenda, "Operador", os_operador],
            ["Talhão",  os_talhao,  "Máquina",  os_maquina],
            ["Área",    f"{os_area} ha", "Cultura", os_cultura],
            ["Volume calda", f"{os_volume} L/ha", "Velocidade", f"{os_velocidade} km/h"],
            ["Pressão", f"{os_pressao} bar", "Início previsto", os_inicio],
        ]
        t_dados = Table(dados_os, colWidths=[3.5*cm,6*cm,3.5*cm,5.5*cm])
        t_dados.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0), colors.HexColor("#1e3a5f")),
            ("TEXTCOLOR", (0,0),(-1,0), colors.white),
            ("BACKGROUND",(0,1),(0,-1), colors.HexColor("#e8f5e9")),
            ("BACKGROUND",(2,1),(2,-1), colors.HexColor("#e8f5e9")),
            ("FONTNAME",  (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTNAME",  (0,1),(-1,-1),"Helvetica"),
            ("FONTSIZE",  (0,0),(-1,-1), 9),
            ("GRID",      (0,0),(-1,-1), 0.5, colors.grey),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#f0f9ff")]),
        ]))
        el.append(t_dados)
        el.append(Spacer(1, 12))

        # Produtos
        el.append(Paragraph("<b>PRODUTOS A APLICAR</b>", styles["Heading2"]))
        if os_produtos:
            prod_data = [["Produto","Dose/ha","Total","Observação"]] +                         [[p["Produto"],p["Dose/ha"],p["Total"],p["Obs"]] for p in os_produtos]
            t_prod = Table(prod_data, colWidths=[5.5*cm,3*cm,3*cm,7*cm])
            t_prod.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,0), colors.HexColor("#14532d")),
                ("TEXTCOLOR", (0,0),(-1,0), colors.white),
                ("FONTNAME",  (0,0),(-1,0), "Helvetica-Bold"),
                ("FONTSIZE",  (0,0),(-1,-1), 9),
                ("GRID",      (0,0),(-1,-1), 0.5, colors.grey),
                ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#f0fdf4")]),
            ]))
            el.append(t_prod)
        el.append(Spacer(1, 12))

        # EPI
        if os_epi:
            el.append(Paragraph("<b>EPI OBRIGATÓRIO:</b> " + " | ".join(os_epi), styles["Normal"]))
            el.append(Spacer(1, 8))

        # Observações
        if os_obs_geral:
            el.append(Paragraph(f"<b>Observações:</b> {os_obs_geral}", styles["Normal"]))
            el.append(Spacer(1, 16))

        # Assinaturas
        assin = Table([
            ["_"*35, " ", "_"*35],
            ["Operador / Data", " ", "Responsável Técnico / Data"],
        ], colWidths=[7*cm, 4*cm, 7*cm])
        assin.setStyle(TableStyle([
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("FONTSIZE",(0,0),(-1,-1),9),
        ]))
        el.append(assin)

        doc.build(el)
        pdf_os = buf.getvalue()
        buf.close()

        st.download_button(
            "📥 Baixar Ordem de Serviço PDF",
            data=pdf_os,
            file_name=f"OS_{os_numero}_{os_data}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        success_box(f"OS {os_numero} gerada com sucesso!")


# ─────────────────────────────────────────────
# MENU: DASHBOARD FINANCEIRO
# ─────────────────────────────────────────────
elif menu == "💹 Dashboard Financeiro":
    st.header("💹 Dashboard Financeiro — DRE por Safra")

    if "dre_registros" not in st.session_state:
        st.session_state.dre_registros = []

    tab_dre, tab_novo, tab_grafico = st.tabs([
        "📊 DRE & Resultados",
        "➕ Lançar Receita/Custo",
        "📈 Evolução por Safra"
    ])

    with tab_novo:
        st.subheader("➕ Novo Lançamento Financeiro")
        col1, col2, col3 = st.columns(3)
        with col1:
            dre_safra    = st.text_input("Safra", placeholder="2024/2025", key="dre_safra")
            dre_tipo     = st.selectbox("Tipo", ["Receita","Custo Variável","Custo Fixo"], key="dre_tipo")
            dre_categ    = st.selectbox("Categoria", [
                "Venda de grãos","Venda de outros","Semente","Fertilizante",
                "Defensivo","Diesel e lubrificantes","Mão de obra","Aluguel de máquinas",
                "Arrendamento","Seguro","Transporte","Armazenagem","Outros"
            ], key="dre_categ")
        with col2:
            dre_descricao = st.text_input("Descrição", key="dre_desc")
            dre_valor     = st.number_input("Valor R$", min_value=0.0, key="dre_valor")
            dre_area_ha   = st.number_input("Área referente (ha)", min_value=0.0,
                                             value=float(st.session_state.dados.get("area",0)),
                                             key="dre_area")
        with col3:
            dre_data_lanc = st.date_input("Data", key="dre_data")
            dre_talhao    = st.text_input("Talhão/Área", key="dre_talhao")
            dre_cultura   = st.text_input("Cultura", value=st.session_state.dados.get("cultura",""), key="dre_cultura")

        if st.button("💾 Salvar Lançamento", key="btn_salvar_dre"):
            if not dre_safra.strip():
                error_box("Informe a safra.")
            elif dre_valor <= 0:
                error_box("Informe um valor maior que zero.")
            else:
                st.session_state.dre_registros.append({
                    "Safra":      dre_safra,
                    "Tipo":       dre_tipo,
                    "Categoria":  dre_categ,
                    "Descrição":  dre_descricao,
                    "Valor R$":   dre_valor,
                    "Área ha":    dre_area_ha,
                    "Valor/ha":   round(dre_valor / dre_area_ha, 2) if dre_area_ha > 0 else 0,
                    "Data":       str(dre_data_lanc),
                    "Talhão":     dre_talhao,
                    "Cultura":    dre_cultura,
                })
                salvar_dados_iaagro()
                success_box(f"Lançamento salvo! R$ {dre_valor:,.2f} — {dre_categ}")

    with tab_dre:
        if not st.session_state.dre_registros:
            info_box("Nenhum lançamento financeiro ainda. Use a aba 'Lançar Receita/Custo'.")
        else:
            df_dre = pd.DataFrame(st.session_state.dre_registros)
            safras_disp = sorted(df_dre["Safra"].unique().tolist(), reverse=True)
            safra_sel   = st.selectbox("Selecione a safra", safras_disp, key="dre_sel_safra")
            df_safra    = df_dre[df_dre["Safra"] == safra_sel]

            receita      = df_safra[df_safra["Tipo"]=="Receita"]["Valor R$"].sum()
            custo_var    = df_safra[df_safra["Tipo"]=="Custo Variável"]["Valor R$"].sum()
            custo_fix    = df_safra[df_safra["Tipo"]=="Custo Fixo"]["Valor R$"].sum()
            custo_total  = custo_var + custo_fix
            lucro_bruto  = receita - custo_var
            lucro_liq    = receita - custo_total
            margem       = (lucro_liq / receita * 100) if receita > 0 else 0
            area_safra   = df_safra["Área ha"].max() if not df_safra.empty else 1
            receita_ha   = receita / area_safra if area_safra > 0 else 0
            custo_ha     = custo_total / area_safra if area_safra > 0 else 0
            lucro_ha     = lucro_liq / area_safra if area_safra > 0 else 0
            breakeven    = custo_total / area_safra if area_safra > 0 else 0

            st.subheader(f"📊 DRE — Safra {safra_sel}")
            col1,col2,col3,col4 = st.columns(4)
            col1.metric("💰 Receita Total",   f"R$ {receita:,.0f}")
            col2.metric("💸 Custo Total",     f"R$ {custo_total:,.0f}")
            col3.metric("💵 Lucro Líquido",   f"R$ {lucro_liq:,.0f}")
            col4.metric("📊 Margem",          f"{margem:.1f}%")

            col5,col6,col7,col8 = st.columns(4)
            col5.metric("💰 Receita/ha",  f"R$ {receita_ha:,.0f}")
            col6.metric("💸 Custo/ha",    f"R$ {custo_ha:,.0f}")
            col7.metric("💵 Lucro/ha",    f"R$ {lucro_ha:,.0f}")
            col8.metric("⚖️ Break-even",  f"R$ {breakeven:,.0f}/ha")

            # DRE formatado
            st.divider()
            st.subheader("📋 Demonstrativo de Resultado (DRE)")
            dre_lines = [
                {"Item": "RECEITA BRUTA",            "Valor R$": receita,      "Tipo": ""},
                {"Item": "(-) Custos Variáveis",     "Valor R$": -custo_var,   "Tipo": ""},
                {"Item": "= LUCRO BRUTO",             "Valor R$": lucro_bruto,  "Tipo": ""},
                {"Item": "(-) Custos Fixos",          "Valor R$": -custo_fix,   "Tipo": ""},
                {"Item": "= LUCRO LÍQUIDO",           "Valor R$": lucro_liq,    "Tipo": ""},
                {"Item": f"  Margem Líquida",         "Valor R$": margem,       "Tipo": "%"},
            ]
            df_dre_fmt = pd.DataFrame(dre_lines)
            st.dataframe(df_dre_fmt, use_container_width=True, hide_index=True)

            # Lançamentos detalhados
            st.divider()
            st.subheader("📝 Lançamentos Detalhados")
            st.dataframe(df_safra[["Data","Tipo","Categoria","Descrição","Valor R$","Valor/ha","Talhão"]],
                         use_container_width=True, hide_index=True)

            # Composição de custos
            st.divider()
            st.subheader("🥧 Composição de Custos")
            df_custos = df_safra[df_safra["Tipo"].isin(["Custo Variável","Custo Fixo"])]
            if not df_custos.empty:
                df_comp = df_custos.groupby("Categoria")["Valor R$"].sum().reset_index()
                st.bar_chart(df_comp.set_index("Categoria")["Valor R$"])

            # Exportar DRE
            st.divider()
            xlsx_dre = exportar_excel({
                f"DRE {safra_sel}": dre_lines,
                "Lançamentos":      st.session_state.dre_registros
            })
            if xlsx_dre:
                st.download_button(
                    "📥 Exportar DRE Excel",
                    data=xlsx_dre,
                    file_name=f"DRE_{safra_sel.replace('/','_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

    with tab_grafico:
        if len(st.session_state.dre_registros) < 2:
            info_box("Lançe dados de pelo menos 2 safras para ver a evolução.")
        else:
            df_all  = pd.DataFrame(st.session_state.dre_registros)
            df_evo  = df_all.groupby(["Safra","Tipo"])["Valor R$"].sum().unstack(fill_value=0).reset_index()
            st.subheader("📈 Evolução Financeira por Safra")
            st.dataframe(df_evo, use_container_width=True)
            st.line_chart(df_evo.set_index("Safra"))

            # Lucratividade por safra
            df_lucro = df_all.groupby("Safra").apply(
                lambda x: pd.Series({
                    "Receita":     x[x["Tipo"]=="Receita"]["Valor R$"].sum(),
                    "Custo Total": x[x["Tipo"].isin(["Custo Variável","Custo Fixo"])]["Valor R$"].sum(),
                })
            ).reset_index()
            df_lucro["Lucro"] = df_lucro["Receita"] - df_lucro["Custo Total"]
            df_lucro["Margem %"] = (df_lucro["Lucro"] / df_lucro["Receita"] * 100).round(1)
            st.subheader("💰 Lucratividade por Safra")
            st.dataframe(df_lucro, use_container_width=True)
            st.bar_chart(df_lucro.set_index("Safra")["Lucro"])


# ─────────────────────────────────────────────
# MENU: CALENDÁRIO AGRÍCOLA
# ─────────────────────────────────────────────
elif menu == "📅 Calendário Agrícola":
    st.header("📅 Calendário Agrícola")

    if "calendario_eventos" not in st.session_state:
        st.session_state.calendario_eventos = []

    tab_cal, tab_novo_ev, tab_plantio = st.tabs([
        "📅 Calendário do Mês",
        "➕ Novo Evento",
        "🌱 Cronograma de Plantio"
    ])

    with tab_novo_ev:
        st.subheader("➕ Cadastrar Evento Agrícola")
        col1, col2 = st.columns(2)
        with col1:
            ev_tipo   = st.selectbox("Tipo de evento", [
                "🌱 Plantio","🌿 Emergência","🚜 Aplicação","✂️ Poda/Desbaste",
                "💧 Irrigação","🌾 Colheita","🧪 Análise de Solo","📦 Recebimento de insumos",
                "🔧 Manutenção de equipamentos","📋 Vistoria","🌦️ Evento climático","📝 Outro"
            ], key="ev_tipo")
            ev_data   = st.date_input("Data do evento", key="ev_data")
            ev_talhao = st.text_input("Talhão/Área", key="ev_talhao")
        with col2:
            ev_cultura = st.text_input("Cultura", value=st.session_state.dados.get("cultura",""), key="ev_cultura")
            ev_resp    = st.text_input("Responsável", key="ev_resp")
            ev_status  = st.selectbox("Status", ["⏳ Planejado","✅ Realizado","⚠️ Atrasado","❌ Cancelado"], key="ev_status")
        ev_descricao = st.text_area("Descrição / Observações", key="ev_desc")

        if st.button("💾 Salvar Evento", key="btn_salvar_ev"):
            if not ev_tipo:
                error_box("Selecione o tipo de evento.")
            else:
                st.session_state.calendario_eventos.append({
                    "Tipo":        ev_tipo,
                    "Data":        str(ev_data),
                    "Talhão":      ev_talhao,
                    "Cultura":     ev_cultura,
                    "Responsável": ev_resp,
                    "Status":      ev_status,
                    "Descrição":   ev_descricao,
                })
                salvar_dados_iaagro()
                success_box(f"Evento '{ev_tipo}' em {ev_data} salvo!")

    with tab_cal:
        if not st.session_state.calendario_eventos:
            info_box("Nenhum evento cadastrado. Use a aba 'Novo Evento'.")
        else:
            df_ev = pd.DataFrame(st.session_state.calendario_eventos)
            df_ev["Data"] = pd.to_datetime(df_ev["Data"])

            # Filtros
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                mes_sel = st.selectbox("Mês", range(1,13),
                                        index=date.today().month-1,
                                        format_func=lambda m: ["Jan","Fev","Mar","Abr","Mai","Jun",
                                                                "Jul","Ago","Set","Out","Nov","Dez"][m-1],
                                        key="cal_mes")
            with col_f2:
                ano_sel = st.selectbox("Ano", sorted(df_ev["Data"].dt.year.unique().tolist(), reverse=True),
                                        key="cal_ano")
            with col_f3:
                status_fil = st.multiselect("Status", df_ev["Status"].unique().tolist(),
                                             default=df_ev["Status"].unique().tolist(),
                                             key="cal_status")

            df_mes = df_ev[
                (df_ev["Data"].dt.month == mes_sel) &
                (df_ev["Data"].dt.year  == ano_sel) &
                (df_ev["Status"].isin(status_fil))
            ].sort_values("Data")

            if df_mes.empty:
                warning_box("Nenhum evento neste mês com os filtros selecionados.")
            else:
                st.subheader(f"📅 Eventos — {['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'][mes_sel-1]}/{ano_sel}")

                for _, ev in df_mes.iterrows():
                    cor = {"✅ Realizado":"#14532d","⏳ Planejado":"#1e3a5f",
                           "⚠️ Atrasado":"#78350f","❌ Cancelado":"#7f1d1d"}.get(ev["Status"],"#1e3a5f")
                    borda = {"✅ Realizado":"#22c55e","⏳ Planejado":"#3b82f6",
                             "⚠️ Atrasado":"#f59e0b","❌ Cancelado":"#ef4444"}.get(ev["Status"],"#3b82f6")
                    st.markdown(f'''<div style="background:{cor};color:#fff;padding:12px 18px;
                    border-radius:10px;border-left:5px solid {borda};
                    font-weight:600;margin:6px 0;font-size:14px;">
                    {ev["Tipo"]} &nbsp;|&nbsp; <b>{ev["Data"].strftime("%d/%m/%Y")}</b>
                    &nbsp;|&nbsp; {ev["Talhão"]} &nbsp;|&nbsp; {ev["Cultura"]}
                    &nbsp;|&nbsp; {ev["Status"]}<br>
                    <span style="font-weight:400;font-size:13px;">{ev["Descrição"]}</span>
                    </div>''', unsafe_allow_html=True)

            # Próximos eventos
            st.divider()
            st.subheader("⏰ Próximos Eventos (7 dias)")
            hoje_ts = pd.Timestamp(date.today())
            df_prox = df_ev[
                (df_ev["Data"] >= hoje_ts) &
                (df_ev["Data"] <= hoje_ts + pd.Timedelta(days=7)) &
                (df_ev["Status"] == "⏳ Planejado")
            ].sort_values("Data")
            if df_prox.empty:
                info_box("Nenhum evento planejado nos próximos 7 dias.")
            else:
                for _, ev in df_prox.iterrows():
                    dias_rest = (ev["Data"].date() - date.today()).days
                    st.markdown(f'''<div style="background:#1e3a5f;color:#fff;padding:10px 16px;
                    border-radius:10px;border-left:5px solid #3b82f6;font-weight:700;margin:4px 0;">
                    {ev["Tipo"]} — {ev["Talhão"]} em {ev["Data"].strftime("%d/%m/%Y")}
                    {"(hoje)" if dias_rest==0 else f"(em {dias_rest} dia{'s' if dias_rest>1 else ''})"}
                    </div>''', unsafe_allow_html=True)

            # Excluir evento
            st.divider()
            opcoes_ev = [f"{e['Tipo']} — {e['Talhão']} ({e['Data'].strftime('%d/%m/%Y')})"
                          for _, e in df_mes.iterrows()]
            if opcoes_ev:
                del_ev = st.selectbox("Excluir evento", opcoes_ev, key="del_ev_sel")
                if st.button("🗑️ Excluir Evento", key="btn_del_ev"):
                    idx_del = opcoes_ev.index(del_ev)
                    data_del = df_mes.iloc[idx_del]["Data"]
                    tipo_del = df_mes.iloc[idx_del]["Tipo"]
                    st.session_state.calendario_eventos = [
                        e for e in st.session_state.calendario_eventos
                        if not (e["Tipo"]==tipo_del and e["Data"]==str(data_del.date()))
                    ]
                    salvar_dados_iaagro()
                    success_box("Evento removido.")
                    st.rerun()

    with tab_plantio:
        st.subheader("🌱 Cronograma de Plantio por Cultura")
        cronograma = {
            "Soja":    {"plantio":["Out","Nov"],"floração":["Dez","Jan"],"colheita":["Mar","Abr"],"ciclo":"120-140 dias"},
            "Milho":   {"plantio":["Set","Out","Nov"],"floração":["Dez","Jan"],"colheita":["Fev","Mar","Abr"],"ciclo":"120-150 dias"},
            "Trigo":   {"plantio":["Abr","Mai","Jun"],"floração":["Jul","Ago"],"colheita":["Set","Out"],"ciclo":"100-130 dias"},
            "Feijão":  {"plantio":["Jan","Jul","Out"],"floração":["Fev","Ago","Nov"],"colheita":["Mar","Set","Dez"],"ciclo":"70-90 dias"},
            "Canola":  {"plantio":["Abr","Mai"],"floração":["Jun","Jul"],"colheita":["Set","Out"],"ciclo":"120-150 dias"},
            "Aveia":   {"plantio":["Abr","Mai","Jun"],"floração":["Jul","Ago"],"colheita":["Set","Out"],"ciclo":"100-120 dias"},
        }
        cultura_cron = st.selectbox("Selecione a cultura", list(cronograma.keys()), key="cron_cultura")
        cron = cronograma[cultura_cron]
        col1,col2,col3,col4 = st.columns(4)
        col1.metric("🌱 Plantio",    ", ".join(cron["plantio"]))
        col2.metric("🌸 Floração",   ", ".join(cron["floração"]))
        col3.metric("🌾 Colheita",   ", ".join(cron["colheita"]))
        col4.metric("⏱️ Ciclo",      cron["ciclo"])

        meses_abrev = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
        fases_linha = []
        for mes in meses_abrev:
            if mes in cron["plantio"]:   fase = "🌱 Plantio"
            elif mes in cron["floração"]: fase = "🌸 Floração"
            elif mes in cron["colheita"]: fase = "🌾 Colheita"
            else:                         fase = "—"
            fases_linha.append({"Mês": mes, "Fase": fase})
        df_cron = pd.DataFrame(fases_linha)
        st.dataframe(df_cron.T, use_container_width=True)

        st.markdown('''<div style="background:#14532d;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #22c55e;font-weight:600;margin:10px 0;">
        💡 Use a aba "Novo Evento" para lançar as datas reais do seu plantio e acompanhar
        o andamento da safra no calendário.
        </div>''', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MENU: CONFIGURAÇÕES
# ─────────────────────────────────────────────
elif menu == "⚙️ Configurações":
    st.header("⚙️ Configurações do Sistema")

    tab1, tab2, tab3, tab4 = st.tabs([
        "💾 Backup & Restore",
        "📧 Email & Alertas",
        "📊 Histórico do Solo",
        "📤 Exportar Excel"
    ])

    # ── TAB 1: BACKUP & RESTORE ──
    with tab1:
        st.subheader("💾 Backup de Dados")
        st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
        ℹ️ O backup salva todos os dados: áreas, estoque, aplicações, histórico e pluviômetro.
        </div>''', unsafe_allow_html=True)

        backup_data = gerar_backup()
        st.download_button(
            "📥 Baixar Backup Completo (.json)",
            data=backup_data,
            file_name=f"iaagro_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )

        st.divider()
        st.subheader("📂 Restaurar Backup")
        st.markdown('''<div style="background:#78350f;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #f59e0b;font-weight:600;margin:8px 0;">
        ⚠️ A restauração substituirá TODOS os dados atuais pelo backup selecionado.
        </div>''', unsafe_allow_html=True)

        st.markdown("""
        <style>
        [data-testid="stFileUploader"] section,
        [data-testid="stFileUploaderDropzone"],
        [data-testid="stFileUploaderDropzone"] > div {
            background-color: #0f3460 !important;
            border: 2px solid #22c55e !important;
            border-radius: 12px !important;
        }
        [data-testid="stFileUploaderDropzone"] button {
            background-color: #16a34a !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
        }
        [data-testid="stFileUploaderDropzone"] button span,
        [data-testid="stFileUploaderDropzone"] span,
        [data-testid="stFileUploaderDropzone"] p,
        [data-testid="stFileUploaderDropzone"] small,
        [data-testid="stFileUploaderDropzone"] div {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        [data-testid="stFileUploaderDropzone"] svg path {
            fill: #22c55e !important;
        }
        </style>
        """, unsafe_allow_html=True)
        arquivo_restore = st.file_uploader("Selecione o arquivo de backup (.json)", type=["json"])
        if arquivo_restore:
            if st.button("🔄 Restaurar Backup Agora", key="btn_restore"):
                ok, msg = restaurar_backup(arquivo_restore)
                if ok:
                    st.markdown(f'''<div style="background:#14532d;color:#fff;padding:13px 18px;
                    border-radius:10px;border-left:5px solid #22c55e;font-weight:600;">
                    ✅ {msg}</div>''', unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.markdown(f'''<div style="background:#7f1d1d;color:#fff;padding:13px 18px;
                    border-radius:10px;border-left:5px solid #ef4444;font-weight:600;">
                    ❌ {msg}</div>''', unsafe_allow_html=True)

    # ── TAB 2: EMAIL & ALERTAS ──
    with tab2:
        st.subheader("📧 Configuração de Email para Alertas")
        st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
        ℹ️ Configure um email para receber alertas automáticos quando o estoque estiver baixo.
        Use Gmail com senha de app (configurações → segurança → senhas de app).
        </div>''', unsafe_allow_html=True)

        if "email_config" not in st.session_state:
            st.session_state.email_config = {
                "ativo": False, "remetente": "", "senha": "",
                "email_destino": "", "smtp": "smtp.gmail.com", "porta": 587
            }

        cfg = st.session_state.email_config
        col1, col2 = st.columns(2)
        with col1:
            cfg["remetente"]     = st.text_input("Email remetente (Gmail)", value=cfg.get("remetente",""))
            cfg["senha"]         = st.text_input("Senha de app Gmail", type="password", value=cfg.get("senha",""))
        with col2:
            cfg["email_destino"] = st.text_input("Email destino dos alertas", value=cfg.get("email_destino",""))
            cfg["porta"]         = st.number_input("Porta SMTP", value=int(cfg.get("porta",587)), min_value=1)

        cfg["smtp"] = st.text_input("Servidor SMTP", value=cfg.get("smtp","smtp.gmail.com"))
        cfg["ativo"] = st.checkbox("✅ Ativar alertas por email", value=cfg.get("ativo", False))

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💾 Salvar Configurações de Email"):
                st.session_state.email_config = cfg
                st.markdown('''<div style="background:#14532d;color:#fff;padding:12px 18px;
                border-radius:10px;border-left:5px solid #22c55e;font-weight:600;">
                ✅ Configurações salvas!</div>''', unsafe_allow_html=True)
        with col_b:
            if st.button("📧 Testar Envio de Email"):
                ok = enviar_email_alerta(
                    cfg.get("email_destino",""),
                    "✅ IAAgro Pro — Teste de Email",
                    "<h2>✅ Email configurado com sucesso!</h2><p>Você receberá alertas de estoque aqui.</p>"
                )
                if ok:
                    st.markdown('''<div style="background:#14532d;color:#fff;padding:12px 18px;
                    border-radius:10px;border-left:5px solid #22c55e;font-weight:600;">
                    ✅ Email de teste enviado com sucesso!</div>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<div style="background:#7f1d1d;color:#fff;padding:12px 18px;
                    border-radius:10px;border-left:5px solid #ef4444;font-weight:600;">
                    ❌ Falha ao enviar. Verifique as configurações.</div>''', unsafe_allow_html=True)

        if cfg.get("ativo"):
            st.divider()
            if st.button("🔔 Verificar Alertas de Estoque Agora"):
                checar_alertas_estoque()
                st.markdown('''<div style="background:#14532d;color:#fff;padding:12px 18px;
                border-radius:10px;border-left:5px solid #22c55e;font-weight:600;">
                ✅ Verificação concluída!</div>''', unsafe_allow_html=True)

    # ── TAB 3: HISTÓRICO DO SOLO ──
    with tab3:
        st.subheader("📊 Evolução da Fertilidade do Solo")
        if not st.session_state.areas:
            st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
            border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;">
            ℹ️ Cadastre e analise áreas para ver o histórico.</div>''', unsafe_allow_html=True)
        else:
            opcoes_area = [f"{a['ID']} - {a['Talhão']}" for a in st.session_state.areas]
            area_hist   = st.selectbox("Selecione a área", opcoes_area, key="hist_solo_area")
            id_area_sel = area_hist.split(" - ")[0]

            df_hist = carregar_historico_solo_db(id_area_sel)
            if df_hist.empty:
                st.markdown('''<div style="background:#78350f;color:#fff;padding:13px 18px;
                border-radius:10px;border-left:5px solid #f59e0b;font-weight:600;">
                ⚠️ Nenhuma análise salva no banco ainda. Salve uma análise na aba "Análise de Solo".</div>''',
                unsafe_allow_html=True)
            else:
                st.dataframe(df_hist[["data","ph","fosforo","potassio","materia_organica",
                                       "calcio","magnesio","nota","score","classe"]],
                             use_container_width=True)
                st.subheader("📈 Evolução do Score e Nota")
                col1, col2 = st.columns(2)
                with col1:
                    st.line_chart(df_hist.set_index("data")[["score","nota"]])
                with col2:
                    st.line_chart(df_hist.set_index("data")[["ph","fosforo","potassio"]])

    # ── TAB 4: EXPORTAR EXCEL ──
    with tab4:
        st.subheader("📤 Exportar Dados para Excel")
        st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
        ℹ️ Gera um arquivo Excel com múltiplas abas contendo todos os dados do sistema.
        </div>''', unsafe_allow_html=True)

        if st.button("📊 Gerar Relatório Excel Completo"):
            dados_export = {
                "Áreas":     st.session_state.areas,
                "Estoque":   st.session_state.estoque,
                "Aplicações":[
                    {**{k:v for k,v in ap.items() if k != "Produtos"},
                     "Produtos": str(ap.get("Produtos",[]))}
                    for ap in st.session_state.aplicacoes
                ],
                "Hist Produt": st.session_state.historico_produtividade,
                "Pluviômetro": st.session_state.pluviometro,
                "Análise Solo":[st.session_state.dados] if st.session_state.dados else []
            }
            xlsx = exportar_excel(dados_export)
            if xlsx:
                st.download_button(
                    "📥 Baixar Excel Completo",
                    data=xlsx,
                    file_name=f"iaagro_relatorio_{date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            else:
                st.markdown('''<div style="background:#7f1d1d;color:#fff;padding:12px 18px;
                border-radius:10px;border-left:5px solid #ef4444;font-weight:600;">
                ❌ Erro ao gerar Excel. Verifique se openpyxl está instalado: pip install openpyxl
                </div>''', unsafe_allow_html=True)
