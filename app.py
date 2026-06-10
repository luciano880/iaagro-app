import streamlit as st

st.set_page_config(
    page_title="IAAgro Pro",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)
import pandas as pd
from datetime import date, datetime, timedelta
import random
import json
import os
import sqlite3
import folium
import base64
import hashlib
import smtplib
import re
import requests
import xml.etree.ElementTree as ET
from PIL import Image as PILImage
import pdfplumber
import pytesseract
try:
    from pyzbar.pyzbar import decode as pyzbar_decode
    PYZBAR_OK = True
except Exception:
    PYZBAR_OK = False

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

# ─────────────────────────────────────────────
# SUPABASE — importa módulo de integração
# ─────────────────────────────────────────────
try:
    from supabase_db import (
        sb_login, sb_signup, sb_logout, sb_reset_senha,
        sb_carregar, sb_salvar, sb_plano, sb_refresh
    )
    _SB_DISPONIVEL = True
except Exception:
    _SB_DISPONIVEL = False
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# ─────────────────────────────────────────────
# SEGMENTOS E CULTURAS — definidos no topo para uso em tela_login
# ─────────────────────────────────────────────
SEGMENTOS_INFO = {
    "🌾 Grãos":        {"desc":"Soja, Milho, Trigo e outros cereais",   "cor":"#14532d","borda":"#22c55e"},
    "🌿 Horticultura": {"desc":"Hortaliças, verduras e legumes",         "cor":"#14532d","borda":"#84cc16"},
    "🎯 Fruticultura": {"desc":"Frutas tropicais, uva, café e outras",  "cor":"#7f1d1d","borda":"#f87171"},
    "🌲 Silvicultura": {"desc":"Eucalipto, Pinus e reflorestamento",     "cor":"#1e3a5f","borda":"#38bdf8"},
}

CULTURAS_POR_SEGMENTO = {
    "🌾 Grãos":        ["🌱 Soja","🌽 Milho","🌾 Trigo","🌱 Feijão","🌻 Canola","🌿 Aveia","🍚 Arroz","🌾 Sorgo","🌾 Cevada","🌻 Girassol"],
    "🌿 Horticultura": ["🍅 Tomate","🥔 Batata","🧅 Cebola","🧄 Alho","🍠 Mandioca","🥬 Alface","🥕 Cenoura","🥦 Brócolis","🥒 Pepino","🫑 Pimentão"],
    "🎯 Fruticultura": ["🍊 Laranja","🍌 Banana","🍇 Uva","🍎 Maçã","🥭 Manga","🥑 Abacate","🍋 Limão","🍑 Pêssego","🍂 Caqui","☕ Café"],
    "🌲 Silvicultura": ["🌳 Eucalipto","🌲 Pinus","🌴 Teca","🌿 Paricá","🌲 Cedro"],
}

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
# usuarios.json fica no repositório (persistente entre deploys)
# dados operacionais ficam em /tmp (sessão)
# ─────────────────────────────────────────────
import pathlib

_BASE_DIR = pathlib.Path("/tmp/iaagro_data")
_BASE_DIR.mkdir(parents=True, exist_ok=True)

# Usuários: salva no diretório do app (persistente no Git/repositório)
_REPO_DIR = pathlib.Path(__file__).parent if "__file__" in dir() else pathlib.Path(".")
ARQUIVO_USUARIOS     = str(_REPO_DIR / "usuarios.json")

# Dados operacionais em /tmp (rápido, mas reseta no redeploy)
ARQUIVO_ESTOQUE      = str(_BASE_DIR / "estoque.json")
ARQUIVO_AREAS        = str(_BASE_DIR / "areas.json")
ARQUIVO_DADOS_IAAGRO = str(_BASE_DIR / "dados_iaagro.json")
DB_FILE              = str(_BASE_DIR / "iaagro.db")

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
        "email_config":       st.session_state.get("email_config", {}),
        "backup_data": str(datetime.now())
    }
    return json.dumps(dados, ensure_ascii=False, indent=2).encode("utf-8")

def restaurar_backup(arquivo):
    try:
        import io
        if isinstance(arquivo, (bytes, bytearray)):
            conteudo = arquivo
        elif isinstance(arquivo, io.BytesIO):
            conteudo = arquivo.read()
        else:
            conteudo = arquivo.read()
        dados = json.loads(conteudo.decode("utf-8"))
        if "dados" not in dados and "areas" not in dados:
            return False, "Arquivo inválido — não parece ser um backup do IAAgro."
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
        st.session_state.harvest_historico   = dados.get("harvest_historico", [])
        st.session_state.receituarios        = dados.get("receituarios", [])
        st.session_state.safrinha_registros  = dados.get("safrinha_registros", [])
        st.session_state.segmento            = dados.get("segmento", None)
        if dados.get("email_config"):
            st.session_state.email_config = dados["email_config"]
        salvar_dados_iaagro()
        salvar_usuarios(st.session_state.usuarios)
        n_areas   = len(st.session_state.areas)
        n_estoque = len(st.session_state.estoque)
        return True, f"Backup de {dados.get('backup_data','?')} restaurado! {n_areas} áreas, {n_estoque} itens de estoque."
    except json.JSONDecodeError:
        return False, "Arquivo corrompido — não é um JSON válido."
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


def enviar_email_recuperacao(email_destino, usuario, token):
    """Envia email com token de 6 dígitos para recuperação de senha."""
    try:
        cfg = st.session_state.get("email_config", {})
        if not cfg.get("ativo") or not cfg.get("remetente"):
            return False, "Email não configurado. Vá em ⚙️ Configurações → Email SMTP."
        corpo = f"""
        <div style="font-family:Arial,sans-serif;max-width:500px;margin:auto;
        background:#0f2744;color:#fff;border-radius:14px;padding:30px;">
        <h2 style="color:#22c55e;text-align:center;">🌿 IAAgro Pro</h2>
        <h3 style="text-align:center;color:#fff;">Recuperação de Senha</h3>
        <p>Olá, <b>{usuario}</b>!</p>
        <p>Recebemos uma solicitação para redefinir sua senha.</p>
        <p>Use o código abaixo para criar uma nova senha:</p>
        <div style="background:#1e3a5f;border-radius:10px;padding:20px;text-align:center;
        margin:20px 0;">
          <span style="font-size:36px;font-weight:900;letter-spacing:10px;color:#22c55e;">
          {token}
          </span>
        </div>
        <p style="color:#93c5fd;font-size:13px;">
        ⏱️ Este código expira em <b>15 minutos</b>.<br>
        Se não foi você, ignore este email.
        </p>
        <hr style="border-color:#1e3a5f;margin:20px 0;">
        <p style="color:#6b7280;font-size:11px;text-align:center;">
        IAAgro Pro — Sistema de Gestão Agrícola Inteligente
        </p>
        </div>
        """
        msg = MIMEMultipart()
        msg["From"]    = cfg["remetente"]
        msg["To"]      = email_destino
        msg["Subject"] = "🌿 IAAgro Pro — Código de recuperação de senha"
        msg.attach(MIMEText(corpo, "html"))
        with smtplib.SMTP(cfg.get("smtp","smtp.gmail.com"), int(cfg.get("porta",587))) as s:
            s.starttls()
            s.login(cfg["remetente"], cfg.get("senha",""))
            s.send_message(msg)
        return True, "ok"
    except Exception as e:
        return False, str(e)

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
    """Busca clima atual + previsão 7 dias via Open-Meteo (gratuita, sem chave)."""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
            f"precipitation,windspeed_10m,winddirection_10m,weathercode,"
            f"surface_pressure,visibility,uv_index"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
            f"precipitation_probability_max,windspeed_10m_max,weathercode,"
            f"uv_index_max,et0_fao_evapotranspiration,sunrise,sunset"
            f"&hourly=temperature_2m,precipitation_probability,precipitation,"
            f"windspeed_10m,relativehumidity_2m"
            f"&timezone=America%2FSao_Paulo&forecast_days=7"
        )
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            dados = r.json()
            dados["_atualizado_em"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            return dados
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
def buscar_dolar_awesomeapi():
    """Busca cotação real do dólar — tenta 4 fontes em sequência."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }
    # 1. ExchangeRate-API (mais permissiva no Streamlit Cloud)
    try:
        r3 = requests.get("https://open.er-api.com/v6/latest/USD", timeout=6, headers=headers)
        if r3.status_code == 200:
            brl = r3.json().get("rates", {}).get("BRL", 0)
            if brl > 0:
                return {"preco": round(brl, 4), "fonte": "ExchangeRate-API (tempo real)", "horario": ""}
    except Exception:
        pass  # falha silenciada — não crítico
    # 2. AwesomeAPI
    try:
        r = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL",
                         timeout=6, headers=headers)
        if r.status_code == 200:
            d = r.json()
            bid = float(d["USDBRL"]["bid"])
            if bid > 0:
                return {"preco": round(bid, 4), "fonte": "AwesomeAPI (tempo real)",
                        "horario": d["USDBRL"].get("create_date", "")}
    except Exception:
        pass  # falha silenciada — não crítico
    # 3. Banco Central do Brasil — PTAX
    try:
        from datetime import datetime as _dt2, timedelta as _td
        for delta in [0, 1, 2]:
            data = (_dt2.now() - _td(days=delta)).strftime("%m-%d-%Y")
            url_bcb = (f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
                       f"CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{data}'"
                       f"&$top=1&$format=json&$select=cotacaoVenda")
            r = requests.get(url_bcb, timeout=8, headers=headers)
            if r.status_code == 200:
                val = r.json().get("value", [])
                if val and float(val[0].get("cotacaoVenda", 0)) > 0:
                    return {"preco": round(float(val[0]["cotacaoVenda"]), 4),
                            "fonte": "Banco Central do Brasil PTAX (tempo real)",
                            "horario": data}
    except Exception:
        pass  # falha silenciada — não crítico
    return {"preco": 5.80, "fonte": "Offline"}


def buscar_precos_cepea_ia():
    """
    Usa Claude API com web_search para buscar preços CEPEA em tempo real.
    """
    try:
        # Tenta acessar a chave de diferentes formas
        api_key = ""
        try:
            api_key = st.secrets["ANTHROPIC_API_KEY"]
        except Exception:
            try:
                api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
            except Exception:
                pass  # falha silenciada — não crítico
        if not api_key:
            import os
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")

        if not api_key or len(api_key) < 20:
            st.session_state["_cepea_erro"] = "API key não encontrada ou inválida"
            return None

        hoje_str = datetime.now().strftime("%d/%m/%Y")
        prompt = (
            f"Hoje é {hoje_str}. "
            "Pesquise AGORA no site do CEPEA (cepea.esalq.usp.br) ou em fontes de mercado físico brasileiro "
            "os preços FÍSICOS das seguintes commodities NO BRASIL (NÃO use preços da CBOT/Bolsa de Chicago): "
            "- Soja: preço físico PR/SC em R$/sc 60kg (referência COAMO, Paranaguá ou CEPEA/ESALQ Paraná) "
            "- Milho: preço físico PR/SC em R$/sc 60kg (referência Maringá, Cascavel ou CEPEA Paraná) "
            "- Trigo: preço físico PR em R$/sc 60kg (referência CEPEA/ESALQ) "
            "- Café: preço físico SP em R$/sc 60kg (referência CEPEA/ESALQ São Paulo) "
            "- Algodão: preço físico MT em R$/@ (referência CEPEA) "
            "- Boi Gordo: preço físico SP em R$/@ (referência CEPEA/ESALQ São Paulo) "
            "- Arroz: preço físico RS em R$/sc 50kg (referência CEPEA) "
            "IMPORTANTE: os preços físicos brasileiros típicos são: soja ~110-130 R$/sc, milho ~50-65 R$/sc, trigo ~65-80 R$/sc. "
            "Se não encontrar, use a melhor estimativa do mercado físico brasileiro disponível. "
            "Responda SOMENTE com JSON válido, sem texto extra, sem markdown:\n"
            '{"soja":0.0,"milho":0.0,"trigo":0.0,"cafe":0.0,"algodao":0.0,"boi":0.0,"arroz":0.0,'
            '"fonte":"CEPEA/ESALQ","mercado":"fisico_br","data":"' + hoje_str + '"}'
        )
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type":      "application/json",
                "x-api-key":         api_key,
                "anthropic-version": "2023-06-01",
            },
            json={
                "model":      "claude-sonnet-4-5",
                "max_tokens": 1000,
                "tools":      [{"type": "web_search_20250305", "name": "web_search"}],
                "messages":   [{"role": "user", "content": prompt}]
            },
            timeout=60
        )
        if resp.status_code != 200:
            st.session_state["_cepea_erro"] = f"HTTP {resp.status_code}: {resp.text[:60]}"
            return None

        # Loop de tool_use — continua até end_turn
        _msgs = [{"role": "user", "content": prompt}]
        _resp_data = resp.json()
        _max_iter = 4
        _iter = 0
        texto = ""

        while _iter < _max_iter:
            _iter += 1
            _content = _resp_data.get("content", [])
            _stop    = _resp_data.get("stop_reason", "end_turn")

            # Coleta texto da resposta
            for bloco in _content:
                if bloco.get("type") == "text":
                    texto += bloco.get("text", "")

            if _stop == "end_turn":
                break

            if _stop == "tool_use":
                # Adiciona resposta do assistant e resultado fake da tool
                _msgs.append({"role": "assistant", "content": _content})
                _tool_results = []
                for bloco in _content:
                    if bloco.get("type") == "tool_use":
                        _tool_results.append({
                            "type":        "tool_result",
                            "tool_use_id": bloco["id"],
                            "content":     "Busca realizada. Por favor retorne os preços encontrados em JSON."
                        })
                if _tool_results:
                    _msgs.append({"role": "user", "content": _tool_results})
                    _r2 = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "Content-Type":      "application/json",
                            "x-api-key":         api_key,
                            "anthropic-version": "2023-06-01",
                        },
                        json={
                            "model":    "claude-sonnet-4-5",
                            "max_tokens": 1000,
                            "tools":    [{"type": "web_search_20250305", "name": "web_search"}],
                            "messages": _msgs,
                        },
                        timeout=60
                    )
                    if _r2.status_code == 200:
                        _resp_data = _r2.json()
                    else:
                        break
                else:
                    break
            else:
                break

        texto = texto.replace("```json", "").replace("```", "").strip()
        dados = None
        # Procura JSON no texto
        idx = 0
        while idx < len(texto):
            inicio = texto.find("{", idx)
            if inicio < 0:
                break
            fim = texto.rfind("}", inicio) + 1
            if fim <= inicio:
                break
            try:
                candidato = json.loads(texto[inicio:fim])
                campos = ["soja", "milho", "trigo", "cafe", "algodao", "boi", "arroz"]
                if all(isinstance(candidato.get(c, 0), (int, float)) and float(candidato.get(c, 0)) > 10 for c in campos):
                    dados = candidato
                    break
            except Exception:
                pass
            idx = inicio + 1

        if dados:
            st.session_state["_cepea_erro"] = ""
            return dados
        else:
            # Tenta extrair valores individualmente se modelo respondeu em texto
            import re
            valores = {}
            mapa = {
                "soja":    r"soja[^0-9]*(\d+[.,]\d+)",
                "milho":   r"milho[^0-9]*(\d+[.,]\d+)",
                "trigo":   r"trigo[^0-9]*(\d+[.,]\d+)",
                "cafe":    r"caf[eé][^0-9]*(\d+[.,]\d+)",
                "algodao": r"algod[aã]o[^0-9]*(\d+[.,]\d+)",
                "boi":     r"boi[^0-9]*(\d+[.,]\d+)",
                "arroz":   r"arroz[^0-9]*(\d+[.,]\d+)",
            }
            for campo, pat in mapa.items():
                m = re.search(pat, texto.lower())
                if m:
                    valores[campo] = float(m.group(1).replace(",", "."))

            if len(valores) >= 5:
                for campo in ["soja","milho","trigo","cafe","algodao","boi","arroz"]:
                    if campo not in valores:
                        valores[campo] = 0.0
                valores["fonte"] = "CEPEA/ESALQ"
                valores["mercado"] = "fisico_br"
                valores["data"]  = datetime.now().strftime("%d/%m/%Y")
                st.session_state["_cepea_erro"] = ""
                return valores

            st.session_state["_cepea_erro"] = f"JSON não encontrado: {texto[:60]}"
    except Exception as e:
        st.session_state["_cepea_erro"] = f"Exceção: {str(e)[:80]}"
    return None


def converter_para_reais(precos_cbot, dolar):
    """Converte cotações CBOT/ICE para R$."""
    resultado = {}
    dv = dolar if isinstance(dolar,(int,float)) and dolar > 0 else 5.80
    if precos_cbot.get("soja_cbot",0)  > 0:
        resultado["soja_sc"]    = {"preco": round((precos_cbot["soja_cbot"]/100)*2.2046*dv,2),   "unidade":"R$/sc 60kg","praca":"CBOT","fonte":f"CBOT+USD {dv:.2f}"}
    if precos_cbot.get("milho_cbot",0) > 0:
        resultado["milho_sc"]   = {"preco": round((precos_cbot["milho_cbot"]/100)*2.3621*dv,2),  "unidade":"R$/sc 60kg","praca":"CBOT","fonte":f"CBOT+USD {dv:.2f}"}
    if precos_cbot.get("trigo_cbot",0) > 0:
        resultado["trigo_sc"]   = {"preco": round((precos_cbot["trigo_cbot"]/100)*2.2046*dv,2),  "unidade":"R$/sc 60kg","praca":"CBOT","fonte":f"CBOT+USD {dv:.2f}"}
    if precos_cbot.get("cafe_cbot",0)  > 0:
        resultado["cafe_sc"]    = {"preco": round((precos_cbot["cafe_cbot"]/100)*132.277*dv,2),   "unidade":"R$/sc 60kg","praca":"ICE","fonte":f"ICE+USD {dv:.2f}"}
    if precos_cbot.get("algodao_ice",0)> 0:
        resultado["algodao_at"] = {"preco": round((precos_cbot["algodao_ice"]/100)*33.069*dv,2),  "unidade":"R$/@","praca":"ICE","fonte":f"ICE+USD {dv:.2f}"}
    if precos_cbot.get("boi_cme",0)    > 0:
        resultado["boi_at"]     = {"preco": round((precos_cbot["boi_cme"]/100)*33.069*dv,2),      "unidade":"R$/@","praca":"CME","fonte":f"CME+USD {dv:.2f}"}
    return resultado


def buscar_precos_scraping():
    """Fallback: Stooq CSV e Yahoo Finance."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    resultado = {}
    stooq_map = {"zs.f":"soja_cbot","zc.f":"milho_cbot","zw.f":"trigo_cbot",
                 "kc.f":"cafe_cbot","ct.f":"algodao_ice","gf.f":"boi_cme"}
    for tk, ch in stooq_map.items():
        try:
            r = requests.get(f"https://stooq.com/q/l/?s={tk}&f=sd2t2ohlcv&h&e=csv",
                             headers=headers, timeout=8)
            if r.status_code == 200:
                lns = r.text.strip().split("\n")
                if len(lns) >= 2:
                    cs = lns[1].split(",")
                    if len(cs) >= 7:
                        ps = cs[6].strip()
                        if ps and ps not in ("N/D","0",""):
                            pv = float(ps)
                            if pv > 0: resultado[ch] = pv
        except Exception:
            continue
    if not resultado:
        ym = {"ZS=F":"soja_cbot","ZC=F":"milho_cbot","ZW=F":"trigo_cbot",
              "KC=F":"cafe_cbot","CT=F":"algodao_ice","GF=F":"boi_cme"}
        yh = {**headers,"Accept":"application/json","Referer":"https://finance.yahoo.com/"}
        for tk, ch in ym.items():
            for ep in [f"https://query2.finance.yahoo.com/v8/finance/chart/{tk}?interval=1d&range=1d",
                       f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?interval=1d&range=1d"]:
                try:
                    r = requests.get(ep, headers=yh, timeout=8)
                    if r.status_code == 200:
                        meta = r.json()["chart"]["result"][0]["meta"]
                        pv   = meta.get("regularMarketPrice") or meta.get("previousClose",0)
                        if pv and float(pv) > 0:
                            resultado[ch] = float(pv)
                            break
                except Exception:
                    continue
    return resultado if resultado else None


def buscar_precos_commodities():
    """
    Busca preços em tempo real:
    1. Dólar via BCB PTAX / AwesomeAPI / ExchangeRate-API
    2. Commodities via IA + web_search CEPEA (principal — funciona no Streamlit Cloud)
    3. Fallback: CBOT/ICE via Stooq / Yahoo Finance
    4. Fallback final: referências offline
    """
    resultado = {}
    dolar_data = buscar_dolar_awesomeapi()
    resultado["dolar"] = dolar_data
    dolar_val  = dolar_data.get("preco", 5.80)

    # Verifica cache — só chama IA se passou mais de 30 min
    _cache = st.session_state.get("_cepea_cache", {})
    _cache_ts = st.session_state.get("_cepea_cache_ts", 0)
    _agora = datetime.now().timestamp()
    _cache_valido = _cache and (_agora - _cache_ts) < 1800  # 30 minutos

    dados_cepea = None
    if _cache_valido:
        dados_cepea = _cache
    else:
        dados_cepea = buscar_precos_cepea_ia()
        if dados_cepea:
            st.session_state["_cepea_cache"]    = dados_cepea
            st.session_state["_cepea_cache_ts"] = _agora

    if dados_cepea:
        fc = f"{dados_cepea.get('fonte','CEPEA')} — {dados_cepea.get('data','')}"
        resultado["soja_sc"]    = {"preco":float(dados_cepea["soja"]),    "unidade":"R$/sc 60kg","praca":"PR","fonte":fc}
        resultado["milho_sc"]   = {"preco":float(dados_cepea["milho"]),   "unidade":"R$/sc 60kg","praca":"PR","fonte":fc}
        resultado["trigo_sc"]   = {"preco":float(dados_cepea["trigo"]),   "unidade":"R$/sc 60kg","praca":"PR","fonte":fc}
        resultado["cafe_sc"]    = {"preco":float(dados_cepea["cafe"]),    "unidade":"R$/sc 60kg","praca":"SP","fonte":fc}
        resultado["algodao_at"] = {"preco":float(dados_cepea["algodao"]), "unidade":"R$/@",      "praca":"MT","fonte":fc}
        resultado["boi_at"]     = {"preco":float(dados_cepea["boi"]),     "unidade":"R$/@",      "praca":"SP","fonte":fc}
        resultado["arroz_sc"]   = {"preco":float(dados_cepea["arroz"]),   "unidade":"R$/sc 50kg","praca":"RS","fonte":fc}
    else:
        # Prioridade 2: CBOT convertido
        precos_cbot = buscar_precos_scraping() or {}
        resultado.update(converter_para_reais(precos_cbot, dolar_val))

    hoje = datetime.now().strftime("%d/%m/%Y")
    for chave, fb in {
        "soja_sc":    {"preco":115.0, "unidade":"R$/sc 60kg","praca":"PR","fonte":f"Referência {hoje}"},
        "milho_sc":   {"preco": 58.0, "unidade":"R$/sc 60kg","praca":"PR","fonte":f"Referência {hoje}"},
        "trigo_sc":   {"preco": 69.0, "unidade":"R$/sc 60kg","praca":"PR","fonte":f"Referência {hoje}"},
        "cafe_sc":    {"preco":2250.0,"unidade":"R$/sc 60kg","praca":"SP","fonte":f"Referência {hoje}"},
        "algodao_at": {"preco":120.0, "unidade":"R$/@",      "praca":"MT","fonte":f"Referência {hoje}"},
        "boi_at":     {"preco":320.0, "unidade":"R$/@",      "praca":"SP","fonte":f"Referência {hoje}"},
        "arroz_sc":   {"preco": 74.0, "unidade":"R$/sc 50kg","praca":"RS","fonte":f"Referência {hoje}"},
    }.items():
        resultado.setdefault(chave, fb)

    resultado["_atualizado_em"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return resultado

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
        "dados":                   st.session_state.dados,
        "areas":                   st.session_state.areas,
        "estoque":                 st.session_state.estoque,
        "aplicacoes":              st.session_state.aplicacoes,
        "historico_produtividade": st.session_state.historico_produtividade,
        "pluviometro":             st.session_state.pluviometro,
        "carencia_registros":      st.session_state.get("carencia_registros", []),
        "dre_registros":           st.session_state.get("dre_registros", []),
        "calendario_eventos":      st.session_state.get("calendario_eventos", []),
        "harvest_historico":       st.session_state.get("harvest_historico", []),
        "receituarios":            st.session_state.get("receituarios", []),
        "segmento":                st.session_state.get("segmento", None),
        "safrinha_registros":      st.session_state.get("safrinha_registros", []),
        "fluxo_caixa":             st.session_state.get("fluxo_caixa", []),
        "contratos_troca":         st.session_state.get("contratos_troca", []),
        "planejamento_safras":     st.session_state.get("planejamento_safras", []),
        "corretivos_aplicados":    st.session_state.get("corretivos_aplicados", []),
    }
    # Lê variáveis globais dinamicamente (podem não existir quando função é definida)
    _sb_url    = st.secrets.get("SUPABASE_URL", "") if hasattr(st, 'secrets') else ""
    _sb_key    = st.secrets.get("SUPABASE_ANON_KEY", "") if hasattr(st, 'secrets') else ""
    _sb_token  = st.session_state.get("sb_token", "")
    _sb_uid    = st.session_state.get("sb_user_id", "")
    _sb_ok     = bool(_sb_url and _sb_key and _sb_token and _sb_uid and _SB_DISPONIVEL)

    if _sb_ok:
        try:
            ok = sb_salvar(_sb_url, _sb_key, _sb_token, _sb_uid, dados_salvos)
            if ok:
                st.session_state["_ultimo_save"] = f"✅ Supabase {datetime.now().strftime('%H:%M:%S')}"
                return
            else:
                # Tenta renovar token e salvar de novo
                _refresh = st.session_state.get("sb_refresh_token", "")
                if _refresh and _SB_DISPONIVEL:
                    try:
                        _novo = sb_refresh(_sb_url, _sb_key, _refresh)
                        if _novo.get("ok"):
                            st.session_state.sb_token         = _novo["token"]
                            st.session_state.sb_refresh_token = _novo["refresh_token"]
                            # Salva query_params com novo token
                            try:
                                _tk = _novo["token"]
                                st.query_params["_t1"] = _tk[:200]
                                st.query_params["_t2"] = _tk[200:400]
                                st.query_params["_t3"] = _tk[400:]
                            except Exception:
                                pass
                            ok2 = sb_salvar(_sb_url, _sb_key, _novo["token"], _sb_uid, dados_salvos)
                            if ok2:
                                st.session_state["_ultimo_save"] = f"✅ Supabase {datetime.now().strftime('%H:%M:%S')} (renovado)"
                                return
                    except Exception:
                        pass
                # Captura erro detalhado
                import requests as _rq
                _r = _rq.patch(
                    f"{_sb_url}/rest/v1/iaagro_dados?user_id=eq.{_sb_uid}",
                    headers={"apikey": _sb_key, "Authorization": f"Bearer {_sb_token}",
                             "Content-Type": "application/json", "Prefer": "return=minimal"},
                    json={"atualizado_em": datetime.now().isoformat()},
                    timeout=10
                )
                st.session_state["_ultimo_save"] = f"❌ {_r.status_code}: {_r.text[:50]}"
        except Exception as e:
            st.session_state["_ultimo_save"] = f"❌ Erro: {str(e)[:40]}"
    else:
        motivo = []
        if not _sb_url: motivo.append("sem URL")
        if not _sb_key: motivo.append("sem KEY")
        if not _sb_token: motivo.append("sem token")
        if not _sb_uid: motivo.append("sem user_id")
        if not _SB_DISPONIVEL: motivo.append("módulo não carregou")
        st.session_state["_ultimo_save"] = f"⚠️ Local ({', '.join(motivo)})"
    # Fallback: arquivo local
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
    # Tenta carregar do repositório primeiro
    for caminho in [ARQUIVO_USUARIOS, str(_BASE_DIR / "usuarios.json")]:
        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding="utf-8") as arquivo:
                    dados = json.load(arquivo)
                    if isinstance(dados, dict) and dados:
                        return dados
            except Exception:
                pass  # falha silenciada — não crítico
    return {}

def salvar_usuarios(usuarios):
    # Salva no repositório (persistente)
    try:
        with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
    except Exception:
        pass  # falha silenciada — não crítico
    # Backup em /tmp também
    try:
        with open(str(_BASE_DIR / "usuarios.json"), "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
    except Exception:
        pass  # falha silenciada — não crítico

# ─────────────────────────────────────────────
# SUPABASE — configuração
# ─────────────────────────────────────────────
_SB_URL = st.secrets.get("SUPABASE_URL", "")
_SB_KEY = st.secrets.get("SUPABASE_ANON_KEY", "")
_SUPABASE_ATIVO = bool(_SB_URL and _SB_KEY and _SB_DISPONIVEL)

# ─────────────────────────────────────────────
# AUTO-LOGIN — restaura sessão via query_params
# Quando usuário recarrega a página, o token
# salvo nos query_params restaura a sessão
# ─────────────────────────────────────────────
def _tentar_autologin():
    """Tenta restaurar sessão via query_params após reload."""
    try:
        params = st.query_params
        _t1  = params.get("_t1", "")
        _t2  = params.get("_t2", "")
        _t3  = params.get("_t3", "")
        _tk  = _t1 + _t2 + _t3
        _uid = params.get("_u", "")
        _pl  = params.get("_p", "free")
        _nm  = params.get("_n", "")
        _rf  = params.get("_rf", "")
        if _tk and _uid and not st.session_state.get("logado"):
            # Tenta renovar token com refresh antes de carregar
            if _rf and _SUPABASE_ATIVO:
                try:
                    _novo = sb_refresh(_SB_URL, _SB_KEY, _rf)
                    if _novo.get("ok"):
                        _tk = _novo["token"]
                        _rf = _novo.get("refresh_token", _rf)
                except Exception:
                    pass
            _dados = sb_carregar(_SB_URL, _SB_KEY, _tk, _uid) if _SUPABASE_ATIVO else None
            if _dados is not None:
                st.session_state.logado           = True
                st.session_state.sb_token         = _tk
                st.session_state.sb_refresh_token = _rf
                st.session_state.sb_user_id       = _uid
                st.session_state.sb_plano         = _pl
                st.session_state.usuario_atual    = (_nm or "Usuário").replace("_", " ")
                # Carrega TODOS os campos do Supabase
                _campos = ["dados","areas","estoque","aplicacoes","historico_produtividade",
                           "pluviometro","carencia_registros","dre_registros","calendario_eventos",
                           "harvest_historico","receituarios","safrinha_registros","fluxo_caixa",
                           "corretivos_aplicados","segmento","contratos_troca"]
                for k in _campos:
                    if k in _dados and _dados[k] not in (None, [], {}):
                        setattr(st.session_state, k, _dados[k])
                try:
                    st.session_state.sb_plano = sb_plano(_SB_URL, _SB_KEY, _tk, _uid)
                except Exception:
                    pass
                # Atualiza query_params com token renovado
                try:
                    st.query_params["_t1"] = _tk[:200]
                    st.query_params["_t2"] = _tk[200:400]
                    st.query_params["_t3"] = _tk[400:]
                    if _rf:
                        st.query_params["_rf"] = _rf[:200]
                except Exception:
                    pass
                return True
    except Exception:
        pass
    return False

if _SUPABASE_ATIVO and not st.session_state.get("logado"):
    _tentar_autologin()

# ─────────────────────────────────────────────
# SESSION STATE – LOGIN
# ─────────────────────────────────────────────
if "sb_token"   not in st.session_state: st.session_state.sb_token   = ""
if "sb_user_id" not in st.session_state: st.session_state.sb_user_id = ""
if "sb_plano"   not in st.session_state: st.session_state.sb_plano   = "free"

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
    """Tela de login — usa Supabase se disponível, senão sistema local."""

    # Logo
    if os.path.exists("IAAgrologo.jpeg"):
        import base64 as _b64
        with open("IAAgrologo.jpeg", "rb") as _f:
            _logo_b64 = _b64.b64encode(_f.read()).decode()
        st.markdown(f"""<div style='text-align:center;padding:20px 0 10px;'>
        <img src='data:image/jpeg;base64,{_logo_b64}' style='max-height:120px;border-radius:12px;'/>
        </div>""", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center;color:#22c55e;'>🌾 IAAGRO</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#94a3b8;'>Inteligência Agrícola de Precisão</p>", unsafe_allow_html=True)

    if _SUPABASE_ATIVO:
        # ── LOGIN VIA SUPABASE ───────────────────────────
        aba_login, aba_cadastro, aba_recuperar = st.tabs(["🔓 Entrar","➕ Criar Conta","🔑 Recuperar Senha"])

        with aba_login:
            with st.form("form_login_sb", clear_on_submit=False):
                email_l = st.text_input("E-mail", placeholder="seu@email.com", key="sb_email_login")
                senha_l = st.text_input("Senha", type="password", key="sb_senha_login")
                btn_l   = st.form_submit_button("Entrar", use_container_width=True)
            if btn_l:
                if not email_l or not senha_l:
                    st.error("Preencha e-mail e senha.")
                else:
                    with st.spinner("Autenticando..."):
                        res = sb_login(_SB_URL, _SB_KEY, email_l.strip(), senha_l)
                    if res["ok"]:
                        st.session_state.logado           = True
                        st.session_state.usuario_atual    = res["nome"] or res["email"]
                        st.session_state.sb_token         = res["token"]
                        st.session_state.sb_refresh_token = res.get("refresh_token", "")
                        st.session_state.sb_user_id       = res["user_id"]
                        st.session_state.sb_plano         = sb_plano(_SB_URL, _SB_KEY, res["token"], res["user_id"])
                        # Carrega dados do usuário do Supabase
                        dados_sb = sb_carregar(_SB_URL, _SB_KEY, res["token"], res["user_id"])
                        if dados_sb:
                            for k, v in dados_sb.items():
                                if k not in st.session_state:
                                    setattr(st.session_state, k, v)
                            # Aplica segmento do cadastro se for primeiro login
                            if not dados_sb.get("segmento") and st.session_state.get("_seg_novo_usuario"):
                                st.session_state.segmento = st.session_state.pop("_seg_novo_usuario")
                                salvar_dados_iaagro()
                        elif st.session_state.get("_seg_novo_usuario"):
                            st.session_state.segmento = st.session_state.pop("_seg_novo_usuario")
                        # Salva refresh info nos query_params para auto-login após reload
                        try:
                            import hashlib as _hl
                            _nome_url = (res["nome"] or res["email"]).replace(" ", "_")[:20]
                            # Salva token completo — query_params suporta strings longas
                            _tk_full = res["token"]
                            st.query_params["_u"] = res["user_id"]
                            st.query_params["_p"] = st.session_state.sb_plano
                            st.query_params["_n"] = _nome_url
                            # Divide token em partes para query_params
                            st.query_params["_t1"] = _tk_full[:200]
                            st.query_params["_t2"] = _tk_full[200:400]
                            st.query_params["_t3"] = _tk_full[400:]
                            st.query_params["_rf"]  = res.get("refresh_token","")[:200]
                        except Exception:
                            pass
                        st.success(f"✅ Bem-vindo, {st.session_state.usuario_atual}!")
                        st.rerun()
                    else:
                        st.error(f"❌ {res['erro']}")

        with aba_cadastro:
            st.markdown("#### 🌿 Criar nova conta")
            with st.form("form_cadastro_sb", clear_on_submit=True):
                nome_c  = st.text_input("Nome completo", key="sb_nome_cad")
                email_c = st.text_input("E-mail", key="sb_email_cad")
                senha_c = st.text_input("Senha (mín. 6 caracteres)", type="password", key="sb_senha_cad")
                conf_c  = st.text_input("Confirmar senha", type="password", key="sb_conf_cad")
                st.markdown("#### 🌾 Qual é o seu segmento de atuação?")
                _segs_cad = list(SEGMENTOS_INFO.keys())
                seg_c = st.radio(
                    "Segmento",
                    _segs_cad,
                    horizontal=True,
                    key="sb_seg_cad",
                    help="Você pode alterar depois em Configurações"
                )
                _culturas_seg_c = CULTURAS_POR_SEGMENTO.get(seg_c, [])
                if _culturas_seg_c:
                    _nomes_cult = " &nbsp;·&nbsp; ".join(
                        f'<span style="background:#14532d;color:#6ee7b7;padding:2px 8px;border-radius:6px;font-size:12px;font-weight:600;">{c}</span>'
                        for c in _culturas_seg_c
                    )
                    st.markdown(f"<div style='margin:6px 0 10px;'>{_nomes_cult}</div>", unsafe_allow_html=True)
                btn_c = st.form_submit_button("✅ Criar Conta", use_container_width=True)
            if btn_c:
                if not nome_c or not email_c or not senha_c:
                    st.error("Preencha todos os campos.")
                elif len(senha_c) < 6:
                    st.error("Senha deve ter pelo menos 6 caracteres.")
                elif senha_c != conf_c:
                    st.error("Senhas não conferem.")
                else:
                    with st.spinner("Criando conta..."):
                        res = sb_signup(_SB_URL, _SB_KEY, email_c.strip(), senha_c, nome_c.strip())
                    if res.get("id") or res.get("user"):
                        st.session_state["_seg_novo_usuario"] = seg_c
                        st.success(f"✅ Conta criada! Segmento: **{seg_c}**. Verifique seu e-mail e faça login.")
                    else:
                        st.error(f"❌ {res.get('msg', res.get('error_description', 'Erro ao criar conta'))}")

        with aba_recuperar:
            st.markdown("#### 🔑 Recuperar Senha")

            if not st.session_state.get("_recup_email"):
                with st.form("form_recup_sb", clear_on_submit=True):
                    email_r = st.text_input("E-mail cadastrado", key="sb_email_recup")
                    btn_r   = st.form_submit_button("📨 Enviar código por e-mail", use_container_width=True)
                if btn_r:
                    if not email_r:
                        st.error("Digite seu e-mail.")
                    else:
                        try:
                            import requests as _req
                            # Envia OTP numérico de 6 dígitos
                            r = _req.post(
                                f"{_SB_URL}/auth/v1/otp",
                                headers={"apikey": _SB_KEY, "Content-Type": "application/json"},
                                json={
                                    "email": email_r.strip(),
                                    "create_user": False,
                                    "options": {"should_create_user": False}
                                },
                                timeout=10
                            )
                            if r.status_code == 200:
                                st.session_state["_recup_email"] = email_r.strip()
                                st.success(f"✅ Código enviado para **{email_r.strip()}**!")
                                st.info("📧 Verifique seu e-mail e copie o código de 8 dígitos.")
                                st.rerun()
                            else:
                                st.error("❌ E-mail não encontrado.")
                        except Exception as e:
                            st.error(f"❌ Erro: {e}")
            else:
                _email_recup = st.session_state["_recup_email"]
                st.info(f"📧 Código enviado para **{_email_recup}**")
                st.warning("⚠️ O e-mail enviado tem um código de 8 dígitos. **Não clique no link** — copie apenas o código numérico.")

                with st.form("form_otp_sb", clear_on_submit=False):
                    otp_code   = st.text_input("Código de 8 dígitos do e-mail", key="sb_otp_code",
                                               placeholder="12345678", max_chars=8)
                    nova_senha = st.text_input("Nova senha (mín. 6 caracteres)", type="password", key="sb_nova_senha")
                    conf_nova  = st.text_input("Confirmar nova senha", type="password", key="sb_conf_nova")
                    btn_otp    = st.form_submit_button("🔐 Redefinir Senha", use_container_width=True)

                if btn_otp:
                    if not otp_code or len(otp_code.strip()) < 6:
                        st.error("Digite o código de 8 dígitos.")
                    elif len(nova_senha) < 6:
                        st.error("Senha deve ter pelo menos 6 caracteres.")
                    elif nova_senha != conf_nova:
                        st.error("Senhas não conferem.")
                    else:
                        try:
                            import requests as _req
                            r = _req.post(
                                f"{_SB_URL}/auth/v1/verify",
                                headers={"apikey": _SB_KEY, "Content-Type": "application/json"},
                                json={"type": "magiclink", "email": _email_recup, "token": otp_code.strip()},
                                timeout=10
                            )
                            if r.status_code != 200:
                                # Tenta também com type "email"
                                r = _req.post(
                                    f"{_SB_URL}/auth/v1/verify",
                                    headers={"apikey": _SB_KEY, "Content-Type": "application/json"},
                                    json={"type": "email", "email": _email_recup, "token": otp_code.strip()},
                                    timeout=10
                                )
                            if r.status_code == 200 and "access_token" in r.json():
                                _token_temp = r.json()["access_token"]
                                r2 = _req.put(
                                    f"{_SB_URL}/auth/v1/user",
                                    headers={"apikey": _SB_KEY,
                                             "Authorization": f"Bearer {_token_temp}",
                                             "Content-Type": "application/json"},
                                    json={"password": nova_senha},
                                    timeout=10
                                )
                                if r2.status_code == 200:
                                    st.session_state.pop("_recup_email", None)
                                    st.success("✅ Senha redefinida! Faça login com a nova senha.")
                                    st.balloons()
                                else:
                                    st.error(f"❌ Erro ao atualizar senha: {r2.text[:80]}")
                            else:
                                st.error(f"❌ Código inválido ou expirado. Tente solicitar um novo código.")
                        except Exception as e:
                            st.error(f"❌ Erro: {e}")

                if st.button("↩️ Solicitar novo código", key="btn_recup_voltar"):
                    st.session_state.pop("_recup_email", None)
                    st.rerun()

        st.markdown("---")
        st.caption("🔒 Dados protegidos por Supabase | Cada usuário tem seus próprios dados")

    else:
        # ── LOGIN LOCAL (fallback sem Supabase) ─────────
        aba_login, aba_cadastro, aba_recuperar = st.tabs(["🔓 Entrar","➕ Criar Conta","🔑 Recuperar Senha"])

        with aba_login:
            with st.form("form_login", clear_on_submit=False):
                usuario = st.text_input("Usuário", key="login_usuario")
                senha   = st.text_input("Senha", type="password", key="login_senha")
                entrar  = st.form_submit_button("Entrar", use_container_width=True)
            if entrar:
                _usuarios = st.session_state.usuarios if isinstance(st.session_state.usuarios, dict) else {}
                u = _usuarios.get(usuario)
                if u and verificar_senha(senha, u["senha"]):
                    st.session_state.logado        = True
                    st.session_state.usuario_atual = usuario
                    st.session_state.sb_plano      = "pro"  # local = sem limite
                    st.success("Login realizado com sucesso.")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")

        with aba_cadastro:
            novo_nome       = st.text_input("Nome completo",       key="cad_nome")
            novo_email      = st.text_input("Email de recuperação", key="cad_email")
            novo_usuario    = st.text_input("Criar usuário",        key="cad_usuario")
            nova_senha      = st.text_input("Criar senha",          type="password", key="cad_senha")
            confirmar_senha = st.text_input("Confirmar senha",      type="password", key="cad_confirmar")
            if st.button("Cadastrar", use_container_width=True, key="btn_cadastrar"):
                if not novo_nome.strip():
                    st.error("Digite seu nome.")
                elif not novo_email.strip() or "@" not in novo_email:
                    st.error("Digite um email válido.")
                elif not novo_usuario.strip():
                    st.error("Digite um usuário.")
                elif len(nova_senha) < 6:
                    st.error("Senha deve ter pelo menos 6 caracteres.")
                elif nova_senha != confirmar_senha:
                    st.error("As senhas não conferem.")
                elif novo_usuario in st.session_state.usuarios:
                    st.error("Esse usuário já existe.")
                else:
                    st.session_state.usuarios[novo_usuario] = {
                        "nome":  novo_nome,
                        "email": novo_email,
                        "senha": hash_senha(nova_senha)
                    }
                    salvar_usuarios(st.session_state.usuarios)
                    st.success("✅ Conta criada! Faça login na aba Entrar.")

        with aba_recuperar:
            st.info("Sistema local — recuperação de senha não disponível sem e-mail configurado.")

        st.caption("⚠️ Modo local — dados compartilhados. Configure Supabase para multi-usuário.")


if not st.session_state.logado:
    # Verifica se havia uma sessão anterior (usuário recarregou a página)
    if st.session_state.get("usuario_atual"):
        st.warning("⏳ Sua sessão expirou. Faça login novamente — seus dados estão salvos no servidor.")
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

# Badge do plano no sidebar
_plano_atual = st.session_state.get("sb_plano", "free")
PLANOS = {
    "free": {
        "nome":    "🆓 Free",
        "preco":   0,
        "areas":   2,
        "estoque": 20,
        "cor":     "#78350f",
        "borda":   "#f59e0b",
        "recursos": [
            "2 áreas cadastradas",
            "20 itens de estoque",
            "Análise de solo básica",
            "Calendário agrícola",
            "Preços offline",
        ],
        "bloqueados": [
            "Relatório PDF",
            "Importação NF-e XML",
            "Preços CEPEA tempo real",
            "Mapa de Colheita IA",
            "IR Rural",
            "Safrinha",
        ]
    },
    "pro": {
        "nome":    "💎 Pro",
        "preco":   49.90,
        "areas":   10,
        "estoque": 100,
        "cor":     "#1e3a5f",
        "borda":   "#3b82f6",
        "recursos": [
            "10 áreas cadastradas",
            "100 itens de estoque",
            "Diagnóstico completo EMBRAPA",
            "Relatório PDF premium",
            "Importação NF-e XML",
            "Preços CEPEA tempo real",
            "Safrinha",
            "IR Rural automatizado",
            "Receituário Agronômico",
            "Suporte via WhatsApp",
        ],
        "bloqueados": [
            "Áreas ilimitadas",
            "Estoque ilimitado",
            "Mapa de Colheita IA avançado",
            "API de integração",
            "Multi-usuário",
        ]
    },
    "premium": {
        "nome":    "🚀 Premium",
        "preco":   119.90,
        "areas":   -1,   # ilimitado
        "estoque": -1,   # ilimitado
        "cor":     "#14532d",
        "borda":   "#22c55e",
        "recursos": [
            "Áreas ILIMITADAS",
            "Estoque ILIMITADO",
            "Tudo do Plano Pro",
            "Mapa de Colheita IA avançado",
            "Relatórios agrupados",
            "API de integração",
            "Suporte prioritário 24h",
            "Treinamento online",
            "White-label disponível",
        ],
        "bloqueados": []
    },
}

WPP_NUMERO  = "5549998159224"  # ← coloque seu WhatsApp aqui
MP_LINK_PRO_MES     = "https://www.mercadopago.com.br/subscriptions/checkout?preapproval_plan_id=68376880ac884906be23814262c595f7"
MP_LINK_PREMIUM_MES = "https://www.mercadopago.com.br/subscriptions/checkout?preapproval_plan_id=ad8dd2ef6aaa444eb2b8189751506028"
MP_LINK_PRO_ANO     = "https://www.mercadopago.com.br/subscriptions/checkout?preapproval_plan_id=3a1d4344b989498a9fe7d8afd972625e"
MP_LINK_PREMIUM_ANO = "https://www.mercadopago.com.br/subscriptions/checkout?preapproval_plan_id=d77348e5eee84d658ee3c3023c6f6ad0"
_plano_info  = PLANOS.get(_plano_atual, PLANOS["free"])
st.sidebar.markdown(
    f"<div style='background:{_plano_info['cor']};color:{_plano_info['borda']};"
    f"padding:5px 10px;border-radius:6px;font-size:11px;font-weight:700;"
    f"margin-bottom:6px;text-align:center;border:1px solid {_plano_info['borda']};'>"
    f"{_plano_info['nome']}</div>",
    unsafe_allow_html=True
)

if st.sidebar.button("Sair", key="botao_sair"):
    if _SUPABASE_ATIVO and st.session_state.get("sb_token"):
        try:
            sb_logout(_SB_URL, _SB_KEY, st.session_state.sb_token)
        except Exception:
            pass
    st.session_state.logado        = False
    st.session_state.usuario_atual = ""
    st.session_state.sb_token      = ""
    st.session_state.sb_user_id    = ""
    st.session_state.sb_plano      = "free"
    try:
        st.query_params.clear()
    except Exception:
        pass
    st.rerun()

# Status do último salvamento (debug)
if st.session_state.get("_ultimo_save"):
    _cor_s = "#14532d" if "✅" in st.session_state["_ultimo_save"] else "#7f1d1d"
    st.sidebar.markdown(
        f"<div style='background:{_cor_s};color:#fff;padding:3px 8px;"
        f"border-radius:4px;font-size:10px;margin-top:2px;'>"
        f"{st.session_state['_ultimo_save']}</div>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
# SESSION STATE – DADOS
# Carrega do Supabase se tem token, senão arquivo local
# ─────────────────────────────────────────────
_dados_supabase = {}
if (_SUPABASE_ATIVO
        and st.session_state.get("sb_token")
        and st.session_state.get("sb_user_id")
        and "areas" not in st.session_state):
    try:
        _dados_supabase = sb_carregar(
            _SB_URL, _SB_KEY,
            st.session_state.sb_token,
            st.session_state.sb_user_id
        ) or {}
        if _dados_supabase:
            st.session_state.sb_plano = sb_plano(
                _SB_URL, _SB_KEY,
                st.session_state.sb_token,
                st.session_state.sb_user_id
            )
    except Exception:
        pass  # falha silenciada — usa arquivo local

dados_carregados = {}

# Carrega do Supabase sempre que logado — garante dados frescos incluindo contratos_troca
if _dados_supabase:
    dados_carregados = _dados_supabase
elif (_SUPABASE_ATIVO
      and st.session_state.get("sb_token")
      and st.session_state.get("sb_user_id")):
    try:
        dados_carregados = sb_carregar(
            _SB_URL, _SB_KEY,
            st.session_state.sb_token,
            st.session_state.sb_user_id
        ) or {}
    except Exception:
        dados_carregados = carregar_dados_iaagro()
else:
    dados_carregados = carregar_dados_iaagro()

# Aplica cada campo: se session_state vazio E supabase tem dados, carrega do supabase
def _carregar_campo(campo, default):
    _local = st.session_state.get(campo)
    _remoto = dados_carregados.get(campo, default)
    if not _local and _remoto:
        setattr(st.session_state, campo, _remoto)
    elif campo not in st.session_state:
        setattr(st.session_state, campo, default)

if "dados" not in st.session_state:
    _d = dados_carregados.get("dados", {})
    st.session_state.dados = _d if isinstance(_d, dict) else {}
if "areas" not in st.session_state or (not st.session_state.areas and dados_carregados.get("areas")):
    st.session_state.areas = dados_carregados.get("areas", [])
if "contador_area" not in st.session_state:
    _areas_dc = st.session_state.get("areas", dados_carregados.get("areas", []))
    st.session_state.contador_area = max(
        (int(a["ID"].split("-")[-1]) for a in _areas_dc if "ID" in a),
        default=0
    ) + 1
if "area_selecionada" not in st.session_state:
    st.session_state.area_selecionada = None
if "segmento" not in st.session_state or (not st.session_state.segmento and dados_carregados.get("segmento")):
    st.session_state.segmento = dados_carregados.get("segmento", None)
if "estoque" not in st.session_state or (not st.session_state.estoque and dados_carregados.get("estoque")):
    st.session_state.estoque = dados_carregados.get("estoque", [])
if "aplicacoes" not in st.session_state or (not st.session_state.aplicacoes and dados_carregados.get("aplicacoes")):
    st.session_state.aplicacoes = dados_carregados.get("aplicacoes", [])
if "historico_produtividade" not in st.session_state or (not st.session_state.historico_produtividade and dados_carregados.get("historico_produtividade")):
    st.session_state.historico_produtividade = dados_carregados.get("historico_produtividade", [])
if "pluviometro" not in st.session_state or (not st.session_state.pluviometro and dados_carregados.get("pluviometro")):
    st.session_state.pluviometro = dados_carregados.get("pluviometro", [])
if "carencia_registros" not in st.session_state or (not st.session_state.carencia_registros and dados_carregados.get("carencia_registros")):
    st.session_state.carencia_registros = dados_carregados.get("carencia_registros", [])
if "dre_registros" not in st.session_state or (not st.session_state.dre_registros and dados_carregados.get("dre_registros")):
    st.session_state.dre_registros = dados_carregados.get("dre_registros", [])
if "calendario_eventos" not in st.session_state:
    st.session_state.calendario_eventos = dados_carregados.get("calendario_eventos", [])

# ── Mapa de Colheita IA — inicialização global ──────────────────
if "harvest_df"        not in st.session_state: st.session_state.harvest_df        = None
if "harvest_analise"   not in st.session_state: st.session_state.harvest_analise   = None
if "harvest_arquivo"   not in st.session_state: st.session_state.harvest_arquivo   = ""
if "harvest_historico" not in st.session_state: st.session_state.harvest_historico = dados_carregados.get("harvest_historico", [])
if "clima_data"        not in st.session_state: st.session_state.clima_data        = None
if "precos_data"       not in st.session_state: st.session_state.precos_data       = None
if "receituarios"      not in st.session_state: st.session_state.receituarios      = dados_carregados.get("receituarios", [])
if "senha_redefinida"  not in st.session_state: st.session_state.senha_redefinida  = False
if "safrinha_registros" not in st.session_state: st.session_state.safrinha_registros = dados_carregados.get("safrinha_registros", [])
if "corretivos_aplicados" not in st.session_state or (not st.session_state.get("corretivos_aplicados") and dados_carregados.get("corretivos_aplicados")):
    st.session_state.corretivos_aplicados = dados_carregados.get("corretivos_aplicados", [])
if "contratos_troca" not in st.session_state or (not st.session_state.get("contratos_troca") and dados_carregados.get("contratos_troca")):
    st.session_state.contratos_troca = dados_carregados.get("contratos_troca", [])
if "planejamento_safras" not in st.session_state or (not st.session_state.get("planejamento_safras") and dados_carregados.get("planejamento_safras")):
    st.session_state.planejamento_safras = dados_carregados.get("planejamento_safras", [])
if "fluxo_caixa" not in st.session_state or (not st.session_state.get("fluxo_caixa") and dados_carregados.get("fluxo_caixa")):
    st.session_state.fluxo_caixa = dados_carregados.get("fluxo_caixa", [])
if "harvest_historico" not in st.session_state or (not st.session_state.get("harvest_historico") and dados_carregados.get("harvest_historico")):
    st.session_state.harvest_historico = dados_carregados.get("harvest_historico", [])
if "receituarios" not in st.session_state or (not st.session_state.get("receituarios") and dados_carregados.get("receituarios")):
    st.session_state.receituarios = dados_carregados.get("receituarios", [])
if "carencia_registros" not in st.session_state or (not st.session_state.get("carencia_registros") and dados_carregados.get("carencia_registros")):
    st.session_state.carencia_registros = dados_carregados.get("carencia_registros", [])
if "pluviometro" not in st.session_state or (not st.session_state.get("pluviometro") and dados_carregados.get("pluviometro")):
    st.session_state.pluviometro = dados_carregados.get("pluviometro", [])
if "calendario_eventos" not in st.session_state or (not st.session_state.get("calendario_eventos") and dados_carregados.get("calendario_eventos")):
    st.session_state.calendario_eventos = dados_carregados.get("calendario_eventos", [])
if "dre_registros" not in st.session_state or (not st.session_state.get("dre_registros") and dados_carregados.get("dre_registros")):
    st.session_state.dre_registros = dados_carregados.get("dre_registros", [])

# ── GPS session_states — inicialização segura ───────────────────
if "_gps_lat"       not in st.session_state: st.session_state._gps_lat       = None
if "_gps_lon"       not in st.session_state: st.session_state._gps_lon       = None
if "_gps_mf_lat"    not in st.session_state: st.session_state._gps_mf_lat    = None
if "_gps_mf_lon"    not in st.session_state: st.session_state._gps_mf_lon    = None
if "_gps_clima_lat" not in st.session_state: st.session_state._gps_clima_lat = None
if "_gps_clima_lon" not in st.session_state: st.session_state._gps_clima_lon = None
if "filtro_out"     not in st.session_state: st.session_state.filtro_out     = []

# ─────────────────────────────────────────────

# BANCO DE PRODUTOS AGRÍCOLAS — Autocomplete
# Fontes: BASF, Syngenta, Bayer, UPL, MAPA/AGROFIT
# ─────────────────────────────────────────────
CATALOGO_PRODUTOS = [
    # ── OUTROS ──
    {"nome":"2,4-D Amina 806","fab":"Outros","cat":"Herbicida","ia":"2,4-D Amina"},
    {"nome":"2,4-D Éster 670","fab":"Outros","cat":"Herbicida","ia":"2,4-D Éster"},
    # ── BASF ──
    {"nome":"Abacus HC","fab":"BASF","cat":"Fungicida","ia":"Epoxiconazol + Piraclostrobina"},
    # ── OUTROS ──
    {"nome":"Abamectina 18 EC","fab":"Outros","cat":"Inseticida","ia":"Abamectina"},
    {"nome":"Abamectina 36 EC","fab":"Outros","cat":"Acaricida","ia":"Abamectina"},
    # ── ADAMA ──
    {"nome":"Abamex 18 EC","fab":"ADAMA","cat":"Inseticida","ia":"Abamectina"},
    # ── BASF ──
    {"nome":"Acabus","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},
    # ── OURO FINO ──
    {"nome":"Acaristop 500 SC","fab":"Ouro Fino","cat":"Acaricida","ia":"Clofentezina"},
    # ── BASF ──
    {"nome":"Accent 750 WG","fab":"BASF","cat":"Herbicida","ia":"Nicossulfurom"},
    # ── BAYER ──
    {"nome":"Accent Gold","fab":"Bayer","cat":"Herbicida","ia":"Nicossulfurom + Rimsulfurom"},
    # ── ADAMA ──
    {"nome":"Acefato 750 WP","fab":"ADAMA","cat":"Inseticida","ia":"Acefato"},
    {"nome":"Acetamiprido 200 SP","fab":"ADAMA","cat":"Inseticida","ia":"Acetamiprido"},
    # ── IHARA ──
    {"nome":"Acimanto SC","fab":"Ihara","cat":"Inseticida","ia":"Acefato"},
    # ── OUTROS ──
    {"nome":"Acramite 50 WS","fab":"Outros","cat":"Acaricida","ia":"Bifenazate"},
    # ── BASF ──
    {"nome":"Acrobat MZ","fab":"BASF","cat":"Fungicida","ia":"Dimetomorfe + Mancozebe"},
    # ── SYNGENTA ──
    {"nome":"Actara 250 WG","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam"},
    {"nome":"Actellic 500 EC","fab":"Syngenta","cat":"Inseticida","ia":"Pirimifós-Metílico"},
    # ── OURO FINO ──
    {"nome":"Actigen","fab":"Ouro Fino","cat":"Fungicida Biológico","ia":"Bacillus amyloliquefaciens"},
    # ── IHARA ──
    {"nome":"Actyon 100 EC","fab":"Ihara","cat":"Inseticida","ia":"Bifentrina"},
    # ── BAYER ──
    {"nome":"Adengo","fab":"Bayer","cat":"Herbicida","ia":"Isoxaflutol + Tiencarbazona"},
    # ── ADAMA ──
    {"nome":"Afalon 450 SC","fab":"ADAMA","cat":"Herbicida","ia":"Linurom"},
    # ── OUTROS ──
    {"nome":"Agree WP","fab":"Outros","cat":"Inseticida Biológico","ia":"Bacillus thuringiensis"},
    # ── SYNGENTA ──
    {"nome":"Alade","fab":"Syngenta","cat":"Fungicida","ia":"Solatenol + Ciproconazol + Difenoconazol"},
    # ── ADAMA ──
    {"nome":"Ally","fab":"ADAMA","cat":"Herbicida","ia":"Metsulfurom-Metílico"},
    # ── IHARA ──
    {"nome":"Alto 100 SL","fab":"Ihara","cat":"Fungicida","ia":"Ciproconazol"},
    # ── SYNGENTA ──
    {"nome":"Amistar 500 WG","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina"},
    {"nome":"Amistar Top","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Difenoconazol"},
    # ── BASF ──
    {"nome":"Amplexus","fab":"BASF","cat":"Herbicida","ia":"Flumioxazina + Lactofen"},
    # ── SYNGENTA ──
    {"nome":"Ampligo 150 ZC","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole + Lambda-Cialotrina"},
    {"nome":"Ampligo Pro","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole + Clorfenapir"},
    # ── BASF ──
    {"nome":"Amplo","fab":"BASF","cat":"Herbicida","ia":"Imazapique + Imazapir"},
    # ── OUTROS ──
    {"nome":"Apollo 500 SC","fab":"Outros","cat":"Acaricida","ia":"Clofentezina"},
    # ── CORTEVA ──
    {"nome":"Aproach 500 SC","fab":"Corteva","cat":"Fungicida","ia":"Picoxistrobina"},
    {"nome":"Aproach Prima","fab":"Corteva","cat":"Fungicida","ia":"Picoxistrobina + Ciproconazol"},
    # ── IHARA ──
    {"nome":"Artea 330 EC","fab":"Ihara","cat":"Fungicida","ia":"Propiconazol + Ciproconazol"},
    # ── CORTEVA ──
    {"nome":"Arylex Active","fab":"Corteva","cat":"Herbicida","ia":"Halauxifem-metílico"},
    # ── OURO FINO ──
    {"nome":"Ascope","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Tebuconazol"},
    # ── CORTEVA ──
    {"nome":"Asgard BR","fab":"Corteva","cat":"Herbicida","ia":"Sulfentrazona + Clomazona"},
    # ── MOSAIC ──
    {"nome":"Aspire","fab":"Mosaic","cat":"Fertilizante","ia":"KCl + B granulado"},
    # ── OUTROS ──
    {"nome":"Assist","fab":"Outros","cat":"Adjuvante","ia":"Óleo Mineral"},
    # ── MOSAIC ──
    {"nome":"Athos","fab":"Mosaic","cat":"Fertilizante","ia":"Sulfato de amônio premium"},
    # ── BASF ──
    {"nome":"Ativo TS","fab":"BASF","cat":"Tratamento de Sementes","ia":"Fludioxonil + Metalaxil-M + Tiametoxam"},
    {"nome":"Ativum","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Fluxapiroxade"},
    # ── OUTROS ──
    {"nome":"Atrazina 500 SC","fab":"Outros","cat":"Herbicida","ia":"Atrazina"},
    # ── BASF ──
    {"nome":"Aura 200","fab":"BASF","cat":"Herbicida","ia":"Quizalofope-P-etílico"},
    # ── BAYER ──
    {"nome":"Aureo","fab":"Bayer","cat":"Adjuvante","ia":"Óleo de Soja"},
    # ── ADAMA ──
    {"nome":"Aurora 400 EC","fab":"ADAMA","cat":"Herbicida","ia":"Carfentrazona-etílica"},
    # ── FMC ──
    {"nome":"Authority 700 WDG","fab":"FMC","cat":"Herbicida","ia":"Sulfentrazona"},
    {"nome":"Authority Assist","fab":"FMC","cat":"Herbicida","ia":"Sulfentrazona + Imazaquim"},
    {"nome":"Authority First","fab":"FMC","cat":"Herbicida","ia":"Sulfentrazona + Cloransulam"},
    {"nome":"Authority MTZ","fab":"FMC","cat":"Herbicida","ia":"Sulfentrazona + Metribuzim"},
    # ── CORTEVA ──
    {"nome":"Avaunt 150 SC","fab":"Corteva","cat":"Inseticida","ia":"Indoxacarbe"},
    # ── SYNGENTA ──
    {"nome":"Avicta 500 FS","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Abamectina"},
    # ── BASF ──
    {"nome":"Axalion","fab":"BASF","cat":"Inseticida","ia":"Afidopiropeno"},
    # ── SYNGENTA ──
    {"nome":"Axial","fab":"Syngenta","cat":"Herbicida","ia":"Pinoxaden"},
    {"nome":"Axial One","fab":"Syngenta","cat":"Herbicida","ia":"Pinoxaden + Clodinafope-propargil"},
    # ── ADAMA ──
    {"nome":"Azimut 250 SC","fab":"ADAMA","cat":"Fungicida","ia":"Azoxistrobina"},
    # ── OURO FINO ──
    {"nome":"Azimut OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina"},
    # ── OUTROS ──
    {"nome":"Azoxistrobina 250 SC","fab":"Outros","cat":"Fungicida","ia":"Azoxistrobina"},
    # ── OURO FINO ──
    {"nome":"Azoxy OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Propiconazol"},
    # ── BAYER ──
    {"nome":"Banvel","fab":"Bayer","cat":"Herbicida","ia":"Dicamba"},
    # ── BASF ──
    {"nome":"Basagran 480","fab":"BASF","cat":"Herbicida","ia":"Bentazona"},
    {"nome":"Basagran 600","fab":"BASF","cat":"Herbicida","ia":"Bentazona"},
    # ── BAYER ──
    {"nome":"Bayfidan 250 EC","fab":"Bayer","cat":"Fungicida","ia":"Triadimenol"},
    {"nome":"Bayfolan Boro","fab":"Bayer","cat":"Foliar / Nutrição","ia":"B + aminoácidos"},
    {"nome":"Bayfolan Cobre","fab":"Bayer","cat":"Foliar / Nutrição","ia":"Cu + aminoácidos"},
    {"nome":"Bayfolan Forte","fab":"Bayer","cat":"Foliar / Nutrição","ia":"NPK + micronutrientes + aminoácidos"},
    {"nome":"Bayfolan NK","fab":"Bayer","cat":"Foliar / Nutrição","ia":"N + K + aminoácidos"},
    # ── BASF ──
    {"nome":"Baytan 150 FS","fab":"BASF","cat":"Tratamento de Sementes","ia":"Triadimenol"},
    # ── BAYER ──
    {"nome":"Belt 480 SC","fab":"Bayer","cat":"Inseticida","ia":"Flubendiamida"},
    {"nome":"Belt Expert","fab":"Bayer","cat":"Inseticida","ia":"Flubendiamida + Spirotetramat"},
    # ── BASF ──
    {"nome":"Belyan","fab":"BASF","cat":"Fungicida","ia":"Mefentrifluconazol + Piraclostrobina + Fluxapiroxade"},
    # ── UPL ──
    {"nome":"Bendazol 500 SC","fab":"UPL","cat":"Fungicida","ia":"Carbendazim"},
    # ── CORTEVA ──
    {"nome":"Benevia OD","fab":"Corteva","cat":"Inseticida","ia":"Ciantraniliprole"},
    # ── OUTROS ──
    {"nome":"Bentazona 600 SL","fab":"Outros","cat":"Herbicida","ia":"Bentazona"},
    # ── OURO FINO ──
    {"nome":"Benza 500 SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Carbendazim"},
    # ── OUTROS ──
    {"nome":"Bifentrina 100 EC","fab":"Outros","cat":"Inseticida","ia":"Bifentrina"},
    # ── UPL ──
    {"nome":"Biozyme","fab":"UPL","cat":"Bioestimulante","ia":"Aminoácidos + Extrato de algas"},
    # ── BASF ──
    {"nome":"Blavity","fab":"BASF","cat":"Fungicida","ia":"Fluxapiroxade + Protioconazol"},
    # ── BAYER ──
    {"nome":"Bold 750 WG","fab":"Bayer","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # ── CORTEVA ──
    {"nome":"Boral 500 SC","fab":"Corteva","cat":"Herbicida","ia":"Sulfentrazona"},
    # ── OUTROS ──
    {"nome":"Boro Max 10%","fab":"Outros","cat":"Foliar / Nutrição","ia":"Boro"},
    {"nome":"Bovemax SC","fab":"Outros","cat":"Inseticida Biológico","ia":"Beauveria bassiana"},
    # ── IHARA ──
    {"nome":"Boveril WP","fab":"Ihara","cat":"Inseticida Biológico","ia":"Beauveria bassiana"},
    # ── SYNGENTA ──
    {"nome":"Bravonil 500 SC","fab":"Syngenta","cat":"Fungicida","ia":"Clorotalonil"},
    {"nome":"Bravonil Top","fab":"Syngenta","cat":"Fungicida","ia":"Clorotalonil + Ciproconazol"},
    # ── ADAMA ──
    {"nome":"Bravonil Ultrex","fab":"ADAMA","cat":"Fungicida","ia":"Clorotalonil"},
    # ── OUTROS ──
    {"nome":"Break Thru S 240","fab":"Outros","cat":"Adjuvante","ia":"Silicone"},
    # ── FMC ──
    {"nome":"Brigade 100 EC","fab":"FMC","cat":"Inseticida","ia":"Bifentrina"},
    {"nome":"Brigade 400 SC","fab":"FMC","cat":"Inseticida","ia":"Bifentrina"},
    # ── BASF ──
    {"nome":"Bright","fab":"BASF","cat":"Inseticida","ia":"Ciantraniliprole + Tiametoxam"},
    {"nome":"Brio","fab":"BASF","cat":"Fungicida","ia":"Trifloxistrobina + Propiconazol"},
    # ── BAYER ──
    {"nome":"Bulldock 125 SC","fab":"Bayer","cat":"Inseticida","ia":"Beta-Ciflutrina"},
    # ── OUTROS ──
    {"nome":"Bórax","fab":"Outros","cat":"Fertilizante","ia":"B 11%"},
    # ── BASF ──
    {"nome":"Cabrio Top","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Metiram"},
    {"nome":"Caipora","fab":"BASF","cat":"Tratamento de Sementes","ia":"Piraclostrobina + Tiofanato + Fipronil"},
    # ── SYNGENTA ──
    {"nome":"Calaris Milho","fab":"Syngenta","cat":"Herbicida","ia":"Tembotriona + Atrazina"},
    # ── OUTROS ──
    {"nome":"Calcário Calcítico","fab":"Outros","cat":"Fertilizante","ia":"CaCO3"},
    {"nome":"Calcário Dolomítico","fab":"Outros","cat":"Fertilizante","ia":"CaCO3 + MgCO3"},
    # ── SYNGENTA ──
    {"nome":"Calipen SC","fab":"Syngenta","cat":"Herbicida","ia":"Cloransulam-metílico"},
    # ── CORTEVA ──
    {"nome":"Callisto","fab":"Corteva","cat":"Herbicida","ia":"Mesotriona"},
    # ── BASF ──
    {"nome":"Cantus","fab":"BASF","cat":"Fungicida","ia":"Boscalida"},
    {"nome":"Caramba 90","fab":"BASF","cat":"Fungicida","ia":"Metconazol"},
    # ── OUTROS ──
    {"nome":"Carbendazim 500 SC","fab":"Outros","cat":"Fungicida","ia":"Carbendazim"},
    {"nome":"Carbofuran 350 SC","fab":"Outros","cat":"Nematicida","ia":"Carbofurano"},
    {"nome":"Carrier 170 EC","fab":"Outros","cat":"Adjuvante","ia":"Óleo Mineral"},
    # ── BAYER ──
    {"nome":"Celeiro","fab":"Bayer","cat":"Fungicida","ia":"Tebuconazol + Trifloxistrobina"},
    # ── ADAMA ──
    {"nome":"Cercobin 700 WP","fab":"ADAMA","cat":"Fungicida","ia":"Tiofanato Metílico"},
    # ── UPL ──
    {"nome":"Cerconil WP","fab":"UPL","cat":"Fungicida","ia":"Clorotalonil + Tiofanato"},
    # ── OUTROS ──
    {"nome":"Cereus 72 SC","fab":"Outros","cat":"Regulador de Crescimento","ia":"Trinexapaque-etílico"},
    # ── SYNGENTA ──
    {"nome":"Certano","fab":"Syngenta","cat":"Inseticida Biológico","ia":"Beauveria bassiana"},
    # ── BAYER ──
    {"nome":"Certero 480 SC","fab":"Bayer","cat":"Inseticida","ia":"Triflumurom"},
    # ── ADAMA ──
    {"nome":"Cipermetrina 250 EC","fab":"ADAMA","cat":"Inseticida","ia":"Cipermetrina"},
    # ── OURO FINO ──
    {"nome":"Cipro 250 SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Ciproconazol"},
    # ── OUTROS ──
    {"nome":"Citromax Cal-Boro","fab":"Outros","cat":"Foliar / Nutrição","ia":"Cálcio + Boro"},
    # ── SYNGENTA ──
    {"nome":"Clariva Complete B","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Pasteuria nishizawae + Tiametoxam"},
    # ── ADAMA ──
    {"nome":"Clethodim 240 EC","fab":"ADAMA","cat":"Herbicida","ia":"Cletodim"},
    # ── OUTROS ──
    {"nome":"Cletodim 240 EC","fab":"Outros","cat":"Herbicida","ia":"Cletodim"},
    {"nome":"Clodinafope 240 EC","fab":"Outros","cat":"Herbicida","ia":"Clodinafope-propargil"},
    {"nome":"Clomazona 500 EC","fab":"Outros","cat":"Herbicida","ia":"Clomazona"},
    {"nome":"Clorantraniliprole 200 SC","fab":"Outros","cat":"Inseticida","ia":"Clorantraniliprole"},
    {"nome":"Cloreto de Potássio","fab":"Outros","cat":"Fertilizante","ia":"KCl 00-00-60"},
    # ── MOSAIC ──
    {"nome":"Cloreto de Potássio Mosaic","fab":"Mosaic","cat":"Fertilizante","ia":"KCl 00-00-60"},
    # ── OUTROS ──
    {"nome":"Clorotalonil 720 SC","fab":"Outros","cat":"Fungicida","ia":"Clorotalonil"},
    {"nome":"Clorpirifós 480 EC","fab":"Outros","cat":"Inseticida","ia":"Clorpirifós"},
    # ── CORTEVA ──
    {"nome":"Closer SC","fab":"Corteva","cat":"Inseticida","ia":"Sulfoxaflor"},
    # ── IHARA ──
    {"nome":"Clout 100 CS","fab":"Ihara","cat":"Inseticida","ia":"Lambda-Cialotrina"},
    # ── OUTROS ──
    {"nome":"Cobra","fab":"Outros","cat":"Herbicida","ia":"Lactofen"},
    {"nome":"Cobre Foliar 5%","fab":"Outros","cat":"Foliar / Nutrição","ia":"Cobre"},
    # ── BASF ──
    {"nome":"Cobre Sandoz","fab":"BASF","cat":"Fungicida","ia":"Oxicloreto de Cobre"},
    {"nome":"Collis","fab":"BASF","cat":"Fungicida","ia":"Boscalida + Cresoxim-metílico"},
    {"nome":"Comet 200 EC","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina"},
    # ── BAYER ──
    {"nome":"Confidor 700 WG","fab":"Bayer","cat":"Inseticida","ia":"Imidaclopride"},
    {"nome":"Confidor Oil","fab":"Bayer","cat":"Inseticida","ia":"Imidaclopride + Óleo mineral"},
    {"nome":"Connect","fab":"Bayer","cat":"Inseticida","ia":"Imidaclopride + Beta-Ciflutrina"},
    # ── UPL ──
    {"nome":"Constel","fab":"UPL","cat":"Inseticida","ia":"Clorantraniliprole + Metoxifenozida"},
    # ── BAYER ──
    {"nome":"Convintro Duo","fab":"Bayer","cat":"Herbicida","ia":"Halauxifem-metílico + Fluroxipir"},
    # ── CORTEVA ──
    {"nome":"Coragen 200 SC","fab":"Corteva","cat":"Inseticida","ia":"Clorantraniliprole"},
    # ── FMC ──
    {"nome":"Coragen FMC","fab":"FMC","cat":"Inseticida","ia":"Clorantraniliprole"},
    # ── TIMAC AGRO ──
    {"nome":"Corona","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"N + B + Mo + aminoácidos"},
    # ── UPL ──
    {"nome":"Cossack OD","fab":"UPL","cat":"Herbicida","ia":"Mesossulfurom + Iodossulfurom"},
    # ── BAYER ──
    {"nome":"Cripton Xpro","fab":"Bayer","cat":"Fungicida","ia":"Bixafem + Protioconazol + Trifloxistrobina"},
    {"nome":"Cropstar 600 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Imidaclopride + Tiodicarbe"},
    # ── UPL ──
    {"nome":"Crosstin","fab":"UPL","cat":"Herbicida","ia":"Hexazinona + Diurom"},
    # ── SYNGENTA ──
    {"nome":"Cruiser 350 FS","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Tiametoxam"},
    {"nome":"Cruiser Opti","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Tiametoxam + Fludioxonil + Mefenoxam"},
    # ── ADAMA ──
    {"nome":"Cuprozeb","fab":"ADAMA","cat":"Fungicida","ia":"Cobre + Mancozebe"},
    # ── BAYER ──
    {"nome":"Curbix","fab":"Bayer","cat":"Inseticida","ia":"Flupyrimin"},
    # ── SYNGENTA ──
    {"nome":"Curyom 550 EC","fab":"Syngenta","cat":"Inseticida","ia":"Profenofós + Cipermetrina"},
    # ── CORTEVA ──
    {"nome":"Cyazypyr 100 OD","fab":"Corteva","cat":"Inseticida","ia":"Ciantraniliprole"},
    # ── FMC ──
    {"nome":"Cyazypyr FMC","fab":"FMC","cat":"Inseticida","ia":"Ciantraniliprole"},
    # ── SYNGENTA ──
    {"nome":"Cypress","fab":"Syngenta","cat":"Fungicida","ia":"Difenoconazol + Propiconazol"},
    # ── IHARA ──
    {"nome":"Cypress Ihara","fab":"Ihara","cat":"Fungicida","ia":"Difenoconazol + Propiconazol"},
    # ── OUTROS ──
    {"nome":"Cálcio King 12%","fab":"Outros","cat":"Foliar / Nutrição","ia":"Cálcio"},
    {"nome":"DAP 18-46-00","fab":"Outros","cat":"Fertilizante","ia":"Diamônio fosfato"},
    # ── MOSAIC ──
    {"nome":"DAP Mosaic","fab":"Mosaic","cat":"Fertilizante","ia":"Diamônio fosfato 18-46-00"},
    # ── OUTROS ──
    {"nome":"Dash HC","fab":"Outros","cat":"Adjuvante","ia":"Éster Metílico de Óleos"},
    # ── OURO FINO ──
    {"nome":"Debussy SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Propiconazol + Difenoconazol"},
    # ── BAYER ──
    {"nome":"Decis 25 EC","fab":"Bayer","cat":"Inseticida","ia":"Deltametrina"},
    {"nome":"Decis Protech","fab":"Bayer","cat":"Inseticida","ia":"Deltametrina"},
    # ── BASF ──
    {"nome":"Delan","fab":"BASF","cat":"Fungicida","ia":"Ditianonom"},
    # ── ADAMA ──
    {"nome":"Deltametrina 25 EC","fab":"ADAMA","cat":"Inseticida","ia":"Deltametrina"},
    # ── CORTEVA ──
    {"nome":"Dermacor X-100","fab":"Corteva","cat":"Tratamento de Sementes","ia":"Clorantraniliprole"},
    # ── BASF ──
    {"nome":"Derosal Plus TS","fab":"BASF","cat":"Tratamento de Sementes","ia":"Carbendazim + Tiram"},
    # ── FMC ──
    {"nome":"Diamond 50 EC","fab":"FMC","cat":"Inseticida","ia":"Novalurom"},
    # ── ADAMA ──
    {"nome":"Diclosulam 840 WG","fab":"ADAMA","cat":"Herbicida","ia":"Diclosulam"},
    {"nome":"Difenoconazol 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Difenoconazol"},
    # ── CORTEVA ──
    {"nome":"Dimilin 250 WP","fab":"Corteva","cat":"Inseticida","ia":"Diflubenzurom"},
    # ── OUTROS ──
    {"nome":"Dipel WP","fab":"Outros","cat":"Inseticida Biológico","ia":"Bacillus thuringiensis"},
    # ── CORTEVA ──
    {"nome":"DMA 806 BR","fab":"Corteva","cat":"Herbicida","ia":"2,4-D Amina"},
    # ── UPL ──
    {"nome":"Domark 100 EC","fab":"UPL","cat":"Fungicida","ia":"Tetraconazol"},
    # ── SYNGENTA ──
    {"nome":"Dual Gold 960 EC","fab":"Syngenta","cat":"Herbicida","ia":"S-Metolacloro"},
    {"nome":"Durivo","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Clorantraniliprole"},
    # ── UPL ──
    {"nome":"Ecconik","fab":"UPL","cat":"Herbicida","ia":"Isoxaflutol"},
    # ── OUTROS ──
    {"nome":"Ecoss WP","fab":"Outros","cat":"Fungicida Biológico","ia":"Bacillus subtilis"},
    # ── SYNGENTA ──
    {"nome":"Eddus","fab":"Syngenta","cat":"Herbicida","ia":"Flumioxazina"},
    {"nome":"Elatus","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Benzovindiflupir"},
    {"nome":"Elatus Ace","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Benzovindiflupir + Propiconazol"},
    {"nome":"Elatus Plus","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Benzovindiflupir + Difenoconazol"},
    {"nome":"Elestal Neo","fab":"Syngenta","cat":"Inseticida","ia":"Sulfoxaflor"},
    # ── OUTROS ──
    {"nome":"Emamectina 50 WG","fab":"Outros","cat":"Inseticida","ia":"Benzoato de Emamectina"},
    # ── ADAMA ──
    {"nome":"Eminent 125 EW","fab":"ADAMA","cat":"Fungicida","ia":"Tetraconazol"},
    {"nome":"Eminent Star","fab":"ADAMA","cat":"Fungicida","ia":"Tetraconazol + Fludioxonil"},
    # ── SYNGENTA ──
    {"nome":"Engeo Pleno S","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Lambda-Cialotrina"},
    # ── CORTEVA ──
    {"nome":"Enlist Duo","fab":"Corteva","cat":"Herbicida","ia":"2,4-D + Glifosato"},
    # ── OUTROS ──
    {"nome":"Envidor 240 SC","fab":"Outros","cat":"Acaricida","ia":"Espirodiclofeno"},
    # ── SYNGENTA ──
    {"nome":"Epivio Sky","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Fluopyram"},
    # ── OUTROS ──
    {"nome":"Epoxiconazol 75 SC","fab":"Outros","cat":"Fungicida","ia":"Epoxiconazol"},
    # ── ADAMA ──
    {"nome":"Esférica Duo","fab":"ADAMA","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # ── OUTROS ──
    {"nome":"Espinosade 480 SC","fab":"Outros","cat":"Inseticida","ia":"Espinosade"},
    # ── OURO FINO ──
    {"nome":"Estoril OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # ── OUTROS ──
    {"nome":"Ethrel 720 SL","fab":"Outros","cat":"Regulador de Crescimento","ia":"Etefom"},
    # ── BAYER ──
    {"nome":"Evidence 200 EC","fab":"Bayer","cat":"Fungicida","ia":"Iprodiona"},
    # ── UPL ──
    {"nome":"Evolution","fab":"UPL","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},
    # ── FMC ──
    {"nome":"Exalt 600 SC","fab":"FMC","cat":"Inseticida","ia":"Espinetoram"},
    # ── MOSAIC ──
    {"nome":"Excellen","fab":"Mosaic","cat":"Fertilizante","ia":"N com inibidor de nitrificação"},
    # ── CORTEVA ──
    {"nome":"Exirel 100 SE","fab":"Corteva","cat":"Inseticida","ia":"Ciantraniliprole"},
    # ── OUTROS ──
    {"nome":"Extravon","fab":"Outros","cat":"Adjuvante","ia":"Alquil-polioxietileno"},
    # ── BASF ──
    {"nome":"Fastac 100 CE","fab":"BASF","cat":"Inseticida","ia":"Alfa-Cipermetrina"},
    {"nome":"Fastac 50 EC","fab":"BASF","cat":"Inseticida","ia":"Alfa-Cipermetrina"},
    # ── UPL ──
    {"nome":"Fastmite","fab":"UPL","cat":"Inseticida","ia":"Abamectina"},
    # ── BASF ──
    {"nome":"Fegatex","fab":"BASF","cat":"Inseticida","ia":"Acefato"},
    # ── UPL ──
    {"nome":"Fernok","fab":"UPL","cat":"Herbicida","ia":"Fenoxaprop + Mefenpir"},
    {"nome":"Feroce","fab":"UPL","cat":"Inseticida","ia":"Lambda-Cialotrina + Tiametoxam"},
    # ── OURO FINO ──
    {"nome":"Ferrari","fab":"Ouro Fino","cat":"Fungicida","ia":"Piraclostrobina + Tebuconazol"},
    # ── OUTROS ──
    {"nome":"Ferro Quelatado 6%","fab":"Outros","cat":"Foliar / Nutrição","ia":"Ferro EDTA"},
    # ── TIMAC AGRO ──
    {"nome":"Fertiactyl Cana","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"N + K + S"},
    {"nome":"Fertiactyl Gramíneas","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"N + S + Zn"},
    {"nome":"Fertiactyl GZ","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"N + P + K + aminoácidos + algas"},
    {"nome":"Fertiactyl Kalibor","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"K + B"},
    {"nome":"Fertiactyl Leguminosas","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"N + P + K + Mo + Co"},
    {"nome":"Fertiactyl Leguminosas NG","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"N + P + K + Mo + Co + aminoácidos"},
    {"nome":"Fertileader Alpha","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"Seactiv + N + Zn"},
    {"nome":"Fertileader Cana","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"Seactiv + N + K"},
    {"nome":"Fertileader Grena","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"Seactiv + K + Ca + B"},
    {"nome":"Fertileader Maiz","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"Seactiv + N + P + Zn"},
    {"nome":"Fertileader Qualité","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"Seactiv + P + K + S"},
    {"nome":"Fertileader Vital","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"Seactiv + NPK"},
    # ── OUTROS ──
    {"nome":"Fetrilon Combi","fab":"Outros","cat":"Foliar / Nutrição","ia":"Multi-micronutrientes"},
    # ── BASF ──
    {"nome":"Finale","fab":"BASF","cat":"Herbicida","ia":"Glufosinato de Amônio"},
    # ── OUTROS ──
    {"nome":"Fipronil 800 WG","fab":"Outros","cat":"Inseticida","ia":"Fipronil"},
    {"nome":"Floramite 240 SC","fab":"Outros","cat":"Acaricida","ia":"Bifenazate"},
    {"nome":"Fluazifope 250 EC","fab":"Outros","cat":"Herbicida","ia":"Fluazifope-P-butílico"},
    {"nome":"Flumioxazina 500 SC","fab":"Outros","cat":"Herbicida","ia":"Flumioxazina"},
    {"nome":"Fluxapiroxade 500 SC","fab":"Outros","cat":"Fungicida","ia":"Fluxapiroxade"},
    # ── BAYER ──
    {"nome":"Folicur 200 EC","fab":"Bayer","cat":"Fungicida","ia":"Tebuconazol"},
    # ── UPL ──
    {"nome":"Foltron Plus","fab":"UPL","cat":"Foliar / Nutrição","ia":"Nitrogênio + Boro + Molibdênio"},
    # ── CORTEVA ──
    {"nome":"Fontelis 200 SC","fab":"Corteva","cat":"Fungicida","ia":"Penthiopirad"},
    # ── SYNGENTA ──
    {"nome":"Fortenza 600 FS","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Afidopiropeno"},
    # ── BASF ──
    {"nome":"Fortenza Duo","fab":"BASF","cat":"Tratamento de Sementes","ia":"Afidopiropeno + Sedaxane"},
    {"nome":"Forum","fab":"BASF","cat":"Fungicida","ia":"Dimetomorfe"},
    {"nome":"Forum Plus","fab":"BASF","cat":"Fungicida","ia":"Dimetomorfe + Folpete"},
    # ── OUTROS ──
    {"nome":"Fosfato Reativo","fab":"Outros","cat":"Fertilizante","ia":"Fosfato natural reativo"},
    # ── OURO FINO ──
    {"nome":"Fox OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # ── BAYER ──
    {"nome":"Fox Ultra","fab":"Bayer","cat":"Fungicida","ia":"Protioconazol + Impirfluxam + Trifloxistrobina"},
    {"nome":"Fox Xpro","fab":"Bayer","cat":"Fungicida","ia":"Bixafem + Tebuconazol + Trifloxistrobina"},
    # ── OUTROS ──
    {"nome":"Fritas FTE BR-12","fab":"Outros","cat":"Fertilizante","ia":"Multi-micronutrientes fritados"},
    # ── SYNGENTA ──
    {"nome":"Frondeo Cana","fab":"Syngenta","cat":"Inseticida","ia":"Plinazolina"},
    # ── UPL ──
    {"nome":"Fury 200 EW","fab":"UPL","cat":"Inseticida","ia":"Zeta-Cipermetrina"},
    # ── ADAMA ──
    {"nome":"Fusilade 250 EW","fab":"ADAMA","cat":"Herbicida","ia":"Fluazifope-P-butílico"},
    # ── OURO FINO ──
    {"nome":"Fusión SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Ciproconazol"},
    # ── BAYER ──
    {"nome":"Galil SC","fab":"Bayer","cat":"Fungicida","ia":"Iprodiona + Tiofanato Metílico"},
    # ── UPL ──
    {"nome":"Galvian 500 WG","fab":"UPL","cat":"Inseticida","ia":"Acefato"},
    # ── BASF ──
    {"nome":"Gamit 360 CS","fab":"BASF","cat":"Herbicida","ia":"Clomazona"},
    # ── FMC ──
    {"nome":"Gamit Star","fab":"FMC","cat":"Herbicida","ia":"Clomazona + Pendimetalina"},
    # ── UPL ──
    {"nome":"Gamit UPL","fab":"UPL","cat":"Herbicida","ia":"Clomazona 360 CS"},
    # ── BAYER ──
    {"nome":"Gaucho 350 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Imidaclopride"},
    {"nome":"Gaucho 600 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Imidaclopride"},
    # ── SYNGENTA ──
    {"nome":"Gesagard 500 SC","fab":"Syngenta","cat":"Herbicida","ia":"Prometrina"},
    {"nome":"Gesaprim 500 SC","fab":"Syngenta","cat":"Herbicida","ia":"Atrazina"},
    # ── OUTROS ──
    {"nome":"Gesso Agrícola","fab":"Outros","cat":"Fertilizante","ia":"CaSO4"},
    {"nome":"Gibb 10 Plus","fab":"Outros","cat":"Regulador de Crescimento","ia":"Ácido Giberélico"},
    {"nome":"Glifosato CS 480","fab":"Outros","cat":"Herbicida","ia":"Glifosato"},
    # ── SYNGENTA ──
    {"nome":"Gramoxone 200","fab":"Syngenta","cat":"Herbicida","ia":"Paraquat"},
    {"nome":"Grower","fab":"Syngenta","cat":"Herbicida","ia":"Nicossulfurom"},
    # ── OUTROS ──
    {"nome":"Halosulfurom 750 WG","fab":"Outros","cat":"Herbicida","ia":"Halosulfurom-metílico"},
    # ── SYNGENTA ──
    {"nome":"Harness 25 EC","fab":"Syngenta","cat":"Herbicida","ia":"Acetocloro"},
    # ── OUTROS ──
    {"nome":"Harpoon WP","fab":"Outros","cat":"Fungicida Biológico","ia":"Trichoderma asperellum"},
    {"nome":"Hasten","fab":"Outros","cat":"Adjuvante","ia":"Óleo Vegetal Éster"},
    # ── BASF ──
    {"nome":"Headline Amp","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Metconazol"},
    {"nome":"Headline EC","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina"},
    {"nome":"Heat","fab":"BASF","cat":"Herbicida","ia":"Saflufenacil"},
    {"nome":"Herbadox 400 EC","fab":"BASF","cat":"Herbicida","ia":"Pendimetalina"},
    # ── ADAMA ──
    {"nome":"Herbazida 480","fab":"ADAMA","cat":"Herbicida","ia":"Glifosato"},
    # ── TIMAC AGRO ──
    {"nome":"HidroFit Arranque","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"P + Zn + aminoácidos"},
    {"nome":"HidroFit K Plus","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"K + Ca + Mg"},
    {"nome":"HidroFit N-Max","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"N + S"},
    # ── IHARA ──
    {"nome":"Hokko Cupra 500 PM","fab":"Ihara","cat":"Fungicida","ia":"Oxicloreto de Cobre"},
    # ── TIMAC AGRO ──
    {"nome":"Humi-K","fab":"Timac Agro","cat":"Fertilizante","ia":"Ácidos húmicos + fúlvicos + K"},
    # ── BASF ──
    {"nome":"Hussar OD","fab":"BASF","cat":"Herbicida","ia":"Iodossulfurom-sódio"},
    {"nome":"Hussar Plus","fab":"BASF","cat":"Herbicida","ia":"Iodossulfurom + Mefenpir"},
    # ── BAYER ──
    {"nome":"Iblon","fab":"Bayer","cat":"Fungicida","ia":"Isoflucipram + Tebuconazol"},
    # ── ADAMA ──
    {"nome":"Iguape 700 WG","fab":"ADAMA","cat":"Fungicida","ia":"Tiofanato Metílico"},
    # ── OUTROS ──
    {"nome":"Iharol EC","fab":"Outros","cat":"Adjuvante","ia":"Óleo Mineral"},
    # ── OURO FINO ──
    {"nome":"Imafort","fab":"Ouro Fino","cat":"Fungicida","ia":"Isoflucipramo + Tebuconazol"},
    # ── OUTROS ──
    {"nome":"Imazaquim 150 SL","fab":"Outros","cat":"Herbicida","ia":"Imazaquim"},
    # ── UPL ──
    {"nome":"Imazetapir 100 SL","fab":"UPL","cat":"Herbicida","ia":"Imazetapir"},
    # ── ADAMA ──
    {"nome":"Imidaclopride 700 WS","fab":"ADAMA","cat":"Inseticida","ia":"Imidaclopride"},
    # ── FMC ──
    {"nome":"Imperious","fab":"FMC","cat":"Inseticida","ia":"Clorantraniliprole + Bifentrina"},
    # ── BASF ──
    {"nome":"Imunit","fab":"BASF","cat":"Inseticida","ia":"Metaflumizone + Beta-Ciflutrina"},
    # ── SYNGENTA ──
    {"nome":"Influx","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole"},
    # ── BAYER ──
    {"nome":"Input","fab":"Bayer","cat":"Fungicida","ia":"Protioconazol + Espiropidiona"},
    {"nome":"Inspire","fab":"Bayer","cat":"Herbicida","ia":"Tembotriona"},
    # ── CORTEVA ──
    {"nome":"Inspire Super","fab":"Corteva","cat":"Fungicida","ia":"Difenoconazol + Ciprodinil"},
    # ── SYNGENTA ──
    {"nome":"Instivo","fab":"Syngenta","cat":"Inseticida","ia":"Espinetoram"},
    {"nome":"Instivo Algodão","fab":"Syngenta","cat":"Inseticida","ia":"Espinetoram"},
    {"nome":"Instivo Milho","fab":"Syngenta","cat":"Inseticida","ia":"Espinetoram"},
    # ── OUTROS ──
    {"nome":"Integral Pro WG","fab":"Outros","cat":"Fungicida Biológico","ia":"Bacillus subtilis"},
    # ── SYNGENTA ──
    {"nome":"Invict","fab":"Syngenta","cat":"Fungicida","ia":"Ciproconazol"},
    # ── OUTROS ──
    {"nome":"Iprodiona 500 SC","fab":"Outros","cat":"Fungicida","ia":"Iprodiona"},
    # ── FMC ──
    {"nome":"Jacle","fab":"FMC","cat":"Herbicida","ia":"Cloransulam-metílico"},
    # ── SYNGENTA ──
    {"nome":"Joiner Café","fab":"Syngenta","cat":"Inseticida","ia":"Sulfoxaflor + Lambda-Cialotrina"},
    {"nome":"Joiner HF","fab":"Syngenta","cat":"Inseticida","ia":"Sulfoxaflor + Lambda-Cialotrina"},
    # ── BAYER ──
    {"nome":"Juno Flex","fab":"Bayer","cat":"Fungicida","ia":"Azoxistrobina + Tebuconazol"},
    # ── UPL ──
    {"nome":"K-fol","fab":"UPL","cat":"Foliar / Nutrição","ia":"Potássio"},
    # ── MOSAIC ──
    {"nome":"K-Mag","fab":"Mosaic","cat":"Fertilizante","ia":"K 21% + Mg 10% + S 21%"},
    # ── SYNGENTA ──
    {"nome":"Kaiso Sorby 50 WG","fab":"Syngenta","cat":"Inseticida","ia":"Lambda-Cialotrina"},
    # ── OURO FINO ──
    {"nome":"Kanet OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Mancozebe + Ciproconazol"},
    # ── SYNGENTA ──
    {"nome":"Karate Zeon 50 CS","fab":"Syngenta","cat":"Inseticida","ia":"Lambda-Cialotrina"},
    # ── UPL ──
    {"nome":"Kashmir","fab":"UPL","cat":"Herbicida","ia":"Hexazinona + Isoxaflutol + Sulfentrazona"},
    {"nome":"Kasumin 2L","fab":"UPL","cat":"Fungicida","ia":"Kasugamicina"},
    {"nome":"Kennox","fab":"UPL","cat":"Herbicida","ia":"Hexazinona + Diurom"},
    # ── BASF ──
    {"nome":"Keyra","fab":"BASF","cat":"Fungicida","ia":"Mefentrifluconazol + Fenpropimorfe"},
    {"nome":"Kixor BX","fab":"BASF","cat":"Herbicida","ia":"Saflufenacil"},
    # ── IHARA ──
    {"nome":"Klorpan 480 EC","fab":"Ihara","cat":"Inseticida","ia":"Clorpirifós"},
    # ── BASF ──
    {"nome":"Kumulus DF","fab":"BASF","cat":"Fungicida","ia":"Enxofre"},
    # ── OUTROS ──
    {"nome":"Lactofen 240 EC","fab":"Outros","cat":"Herbicida","ia":"Lactofen"},
    # ── ADAMA ──
    {"nome":"Lambda-Cialotrina 250 CS","fab":"ADAMA","cat":"Inseticida","ia":"Lambda-Cialotrina"},
    {"nome":"Lanata 750 SC","fab":"ADAMA","cat":"Fungicida","ia":"Boscalida + Piraclostrobina"},
    # ── IHARA ──
    {"nome":"Lancer Gold","fab":"Ihara","cat":"Inseticida","ia":"Acefato + Imidaclopride"},
    # ── CORTEVA ──
    {"nome":"Lannate BR","fab":"Corteva","cat":"Inseticida","ia":"Metomil"},
    # ── BAYER ──
    {"nome":"Larvin 800 WG","fab":"Bayer","cat":"Inseticida","ia":"Tiodicarbe"},
    # ── ADAMA ──
    {"nome":"Laser 360 CS","fab":"ADAMA","cat":"Herbicida","ia":"Clomazona"},
    # ── FMC ──
    {"nome":"Leverage 360","fab":"FMC","cat":"Inseticida","ia":"Imidaclopride + Beta-Ciflutrina"},
    # ── CORTEVA ──
    {"nome":"Lexar EZ","fab":"Corteva","cat":"Herbicida","ia":"S-Metolacloro + Atrazina + Mesotriona"},
    # ── BAYER ──
    {"nome":"Liberty 200 SL","fab":"Bayer","cat":"Herbicida","ia":"Glufosinato de Amônio"},
    {"nome":"Liberty 280 SL","fab":"Bayer","cat":"Herbicida","ia":"Glufosinato de Amônio"},
    # ── ADAMA ──
    {"nome":"Lintur 700 WG","fab":"ADAMA","cat":"Herbicida","ia":"Dicamba + Triasulfurom"},
    # ── BAYER ──
    {"nome":"Locker","fab":"Bayer","cat":"Herbicida","ia":"Fluroxipir-meptílico"},
    # ── CORTEVA ──
    {"nome":"Lorsban 480 BR","fab":"Corteva","cat":"Inseticida","ia":"Clorpirifós"},
    {"nome":"Lumax EZ","fab":"Corteva","cat":"Herbicida","ia":"S-Metolacloro + Atrazina + Mesotriona"},
    {"nome":"Lumiderm","fab":"Corteva","cat":"Tratamento de Sementes","ia":"Clorantraniliprole"},
    # ── UPL ──
    {"nome":"Luminus","fab":"UPL","cat":"Inseticida Biológico","ia":"Peptídeo Flg22-Bt"},
    # ── CORTEVA ──
    {"nome":"Lumivia","fab":"Corteva","cat":"Tratamento de Sementes","ia":"Clorantraniliprole"},
    # ── BAYER ──
    {"nome":"Luna Experience","fab":"Bayer","cat":"Fungicida","ia":"Fluopiram + Tebuconazol"},
    {"nome":"Luna Privilege","fab":"Bayer","cat":"Fungicida","ia":"Fluopiram"},
    {"nome":"Luna Sensation","fab":"Bayer","cat":"Fungicida","ia":"Fluopiram + Trifloxistrobina"},
    # ── BASF ──
    {"nome":"Luximo","fab":"BASF","cat":"Herbicida","ia":"Metazacloro"},
    # ── OUTROS ──
    {"nome":"Malationa 500 CE","fab":"Outros","cat":"Inseticida","ia":"Malationa"},
    # ── ADAMA ──
    {"nome":"Malatol 500 CE","fab":"ADAMA","cat":"Inseticida","ia":"Malationa"},
    {"nome":"Mancozebe 750 WG","fab":"ADAMA","cat":"Fungicida","ia":"Mancozebe"},
    {"nome":"Mancozebe 800 WP","fab":"ADAMA","cat":"Fungicida","ia":"Mancozebe"},
    # ── OURO FINO ──
    {"nome":"Manfil 750 WG","fab":"Ouro Fino","cat":"Fungicida","ia":"Mancozebe"},
    # ── OUTROS ──
    {"nome":"Manganês Foliar 15%","fab":"Outros","cat":"Foliar / Nutrição","ia":"Manganês"},
    # ── IHARA ──
    {"nome":"Manzate 800 WP","fab":"Ihara","cat":"Fungicida","ia":"Mancozebe"},
    # ── OUTROS ──
    {"nome":"MAP 11-52-00","fab":"Outros","cat":"Fertilizante","ia":"Monofosfato de amônio"},
    # ── MOSAIC ──
    {"nome":"MAP Mosaic","fab":"Mosaic","cat":"Fertilizante","ia":"Monofosfato amônio 11-52-00"},
    # ── ADAMA ──
    {"nome":"Marshal 200 SC","fab":"ADAMA","cat":"Inseticida","ia":"Carbossulfano"},
    # ── FMC ──
    {"nome":"Match 50 EC","fab":"FMC","cat":"Inseticida","ia":"Lufenurom"},
    # ── OURO FINO ──
    {"nome":"Maxifort","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Fluxapiroxade"},
    # ── OUTROS ──
    {"nome":"Maxim 025 FS","fab":"Outros","cat":"Tratamento de Sementes","ia":"Fludioxonil"},
    # ── SYNGENTA ──
    {"nome":"Maxim Advanced","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Fludioxonil + Metalaxil-M"},
    {"nome":"Maxim XL 035 FS","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Fludioxonil + Metalaxil-M"},
    # ── UPL ──
    {"nome":"Melius","fab":"UPL","cat":"Regulador de Crescimento","ia":"Trinexapaque-etílico"},
    # ── BASF ──
    {"nome":"Melyra","fab":"BASF","cat":"Fungicida","ia":"Pydiflumetofen + Fludioxonil"},
    # ── BAYER ──
    {"nome":"Merlin 750 WG","fab":"Bayer","cat":"Herbicida","ia":"Isoxaflutol"},
    # ── OUTROS ──
    {"nome":"Metalaxil-M 480 EC","fab":"Outros","cat":"Fungicida","ia":"Metalaxil-M"},
    # ── IHARA ──
    {"nome":"Metarril SC","fab":"Ihara","cat":"Inseticida Biológico","ia":"Metarhizium anisopliae"},
    {"nome":"Methomex 215 SL","fab":"Ihara","cat":"Inseticida","ia":"Metomil"},
    # ── ADAMA ──
    {"nome":"Metribuzim 480 SC","fab":"ADAMA","cat":"Herbicida","ia":"Metribuzim"},
    # ── OUTROS ──
    {"nome":"Metsulfurom 600 WG","fab":"Outros","cat":"Herbicida","ia":"Metsulfurom-metílico"},
    # ── UPL ──
    {"nome":"Metsuran 600 WG","fab":"UPL","cat":"Herbicida","ia":"Metsulfurom-Metílico"},
    # ── BASF ──
    {"nome":"Mibelya","fab":"BASF","cat":"Fungicida","ia":"Pydiflumetofen + Difenoconazol"},
    # ── MOSAIC ──
    {"nome":"MicroEssentials S15","fab":"Mosaic","cat":"Fertilizante","ia":"MAP + N + P + S 15%"},
    {"nome":"MicroEssentials S9","fab":"Mosaic","cat":"Fertilizante","ia":"MAP + N + P + S 9%"},
    # ── SYNGENTA ──
    {"nome":"Minecto Duo","fab":"Syngenta","cat":"Inseticida","ia":"Abamectina + Ciantraniliprole"},
    {"nome":"Minecto Pro","fab":"Syngenta","cat":"Inseticida","ia":"Abamectina + Ciantraniliprole"},
    {"nome":"Miravis","fab":"Syngenta","cat":"Fungicida","ia":"Pydiflumetofen"},
    {"nome":"Miravis Ace","fab":"Syngenta","cat":"Fungicida","ia":"Pydiflumetofen + Azoxistrobina"},
    {"nome":"Miravis Duo","fab":"Syngenta","cat":"Fungicida","ia":"Pydiflumetofen + Difenoconazol"},
    {"nome":"Miravis Pro","fab":"Syngenta","cat":"Fungicida","ia":"Pydiflumetofen + Propiconazol"},
    {"nome":"Mitrion","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Propiconazol"},
    # ── OUTROS ──
    {"nome":"Moddus 250 EC","fab":"Outros","cat":"Regulador de Crescimento","ia":"Trinexapaque-etílico"},
    {"nome":"Molibdato de Sódio","fab":"Outros","cat":"Fertilizante","ia":"Mo 39%"},
    {"nome":"Molibdênio 10%","fab":"Outros","cat":"Foliar / Nutrição","ia":"Molibdênio"},
    # ── IHARA ──
    {"nome":"Monarca 200 OD","fab":"Ihara","cat":"Inseticida","ia":"Metoxifenozida + Espinosade"},
    # ── BAYER ──
    {"nome":"Movento 150 OD","fab":"Bayer","cat":"Inseticida","ia":"Spirotetramat"},
    # ── MOSAIC ──
    {"nome":"MPasto 20-00-20","fab":"Mosaic","cat":"Fertilizante","ia":"NK 20-00-20 + S"},
    {"nome":"MPasto 20-05-20","fab":"Mosaic","cat":"Fertilizante","ia":"NPK 20-05-20 + S + Zn + B"},
    {"nome":"MPasto Plus","fab":"Mosaic","cat":"Fertilizante","ia":"NPK + S + Zn + B"},
    # ── ADAMA ──
    {"nome":"Murvin 850 PM","fab":"ADAMA","cat":"Inseticida","ia":"Carbaril"},
    # ── CORTEVA ──
    {"nome":"Mustang 350 EW","fab":"Corteva","cat":"Inseticida","ia":"Zeta-Cipermetrina"},
    # ── BAYER ──
    {"nome":"Nativo","fab":"Bayer","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # ── ADAMA ──
    {"nome":"Nativo 750 WG","fab":"ADAMA","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # ── OURO FINO ──
    {"nome":"Nativo OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # ── OUTROS ──
    {"nome":"Nemathorin 150 EC","fab":"Outros","cat":"Nematicida","ia":"Fostiazate"},
    {"nome":"Nicossulfurom 240 SC","fab":"Outros","cat":"Herbicida","ia":"Nicossulfurom"},
    # ── UPL ──
    {"nome":"Nimaxxa","fab":"UPL","cat":"Nematicida","ia":"Purpureocillium lilacinum"},
    # ── OUTROS ──
    {"nome":"Nimbus","fab":"Outros","cat":"Adjuvante","ia":"Óleo Vegetal"},
    {"nome":"Nimitz Pro","fab":"Outros","cat":"Nematicida","ia":"Fluensulfona"},
    {"nome":"Nitrato de Cálcio","fab":"Outros","cat":"Fertilizante","ia":"15,5% N + 26% CaO"},
    {"nome":"Nitrato de Potássio","fab":"Outros","cat":"Fertilizante","ia":"13% N + 46% K2O"},
    {"nome":"Nitrofoska Foliar","fab":"Outros","cat":"Foliar / Nutrição","ia":"NPK Foliar"},
    # ── BASF ──
    {"nome":"Nomolt 150","fab":"BASF","cat":"Inseticida","ia":"Teflubenzurom"},
    # ── NORTOX ──
    {"nome":"Nortox 2,4-D","fab":"Nortox","cat":"Herbicida","ia":"2,4-D Amina 806"},
    # ── UPL ──
    {"nome":"Nortox 480 SL","fab":"UPL","cat":"Herbicida","ia":"Glifosato"},
    # ── NORTOX ──
    {"nome":"Nortox Abamectina","fab":"Nortox","cat":"Inseticida","ia":"Abamectina 18 EC"},
    {"nome":"Nortox Atrazina 500","fab":"Nortox","cat":"Herbicida","ia":"Atrazina"},
    {"nome":"Nortox Cipermetrina","fab":"Nortox","cat":"Inseticida","ia":"Cipermetrina 250 EC"},
    {"nome":"Nortox Clorpirifós","fab":"Nortox","cat":"Inseticida","ia":"Clorpirifós 480 EC"},
    {"nome":"Nortox Deltametrina","fab":"Nortox","cat":"Inseticida","ia":"Deltametrina 25 EC"},
    {"nome":"Nortox Imidaclopride","fab":"Nortox","cat":"Inseticida","ia":"Imidaclopride 480 SC"},
    {"nome":"Nortox Mancozebe","fab":"Nortox","cat":"Fungicida","ia":"Mancozebe 800 WP"},
    {"nome":"Nortox Pendimetalina","fab":"Nortox","cat":"Herbicida","ia":"Pendimetalina 400 EC"},
    {"nome":"Nortox Tebuconazol","fab":"Nortox","cat":"Fungicida","ia":"Tebuconazol 200 EC"},
    # ── OUTROS ──
    {"nome":"NPK 04-14-08","fab":"Outros","cat":"Fertilizante","ia":"Formulação NPK 04-14-08"},
    {"nome":"NPK 04-20-20","fab":"Outros","cat":"Fertilizante","ia":"Formulação NPK 04-20-20"},
    {"nome":"NPK 05-25-25","fab":"Outros","cat":"Fertilizante","ia":"Formulação NPK 05-25-25"},
    {"nome":"NPK 08-20-20","fab":"Outros","cat":"Fertilizante","ia":"Formulação NPK 08-20-20"},
    {"nome":"NPK 08-28-16","fab":"Outros","cat":"Fertilizante","ia":"Formulação NPK 08-28-16"},
    {"nome":"NPK 10-10-10","fab":"Outros","cat":"Fertilizante","ia":"Formulação NPK 10-10-10"},
    {"nome":"NPK 10-20-20","fab":"Outros","cat":"Fertilizante","ia":"Formulação NPK 10-20-20"},
    {"nome":"NPK 12-06-12","fab":"Outros","cat":"Fertilizante","ia":"Formulação NPK 12-06-12"},
    {"nome":"NPK 12-12-12","fab":"Outros","cat":"Fertilizante","ia":"Formulação NPK 12-12-12"},
    {"nome":"NPK 15-05-30","fab":"Outros","cat":"Fertilizante","ia":"Formulação NPK 15-05-30"},
    {"nome":"NPK 20-00-20","fab":"Outros","cat":"Fertilizante","ia":"Formulação NPK 20-00-20"},
    {"nome":"NPK 20-05-20","fab":"Outros","cat":"Fertilizante","ia":"Formulação NPK 20-05-20"},
    # ── IHARA ──
    {"nome":"Nurelle D 550/50","fab":"Ihara","cat":"Inseticida","ia":"Clorpirifós + Cipermetrina"},
    # ── UPL ──
    {"nome":"Nuvita","fab":"UPL","cat":"Bioestimulante","ia":"Extrato de algas + aminoácidos"},
    # ── BAYER ──
    {"nome":"Oberon 240 SC","fab":"Bayer","cat":"Inseticida","ia":"Espirodiclofeno"},
    # ── OURO FINO ──
    {"nome":"Oberon OF","fab":"Ouro Fino","cat":"Acaricida","ia":"Espirodiclofeno"},
    # ── UPL ──
    {"nome":"Olea","fab":"UPL","cat":"Herbicida","ia":"2,4-D + Metsulfurom + Picloram"},
    # ── BASF ──
    {"nome":"Opera","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},
    # ── OURO FINO ──
    {"nome":"Opera OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},
    # ── BASF ──
    {"nome":"Opera Ultra","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},
    # ── OURO FINO ──
    {"nome":"Orkestra OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},
    # ── BASF ──
    {"nome":"Orkestra SC","fab":"BASF","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},
    # ── SYNGENTA ──
    {"nome":"Orondis Flexi","fab":"Syngenta","cat":"Fungicida","ia":"Oxathiapiprolin + Mandipropamida"},
    {"nome":"Orondis Gold","fab":"Syngenta","cat":"Fungicida","ia":"Oxathiapiprolin + Mefenoxam"},
    {"nome":"Orondis Ultra","fab":"Syngenta","cat":"Fungicida","ia":"Oxathiapiprolin + Clorotalonil"},
    # ── OUTROS ──
    {"nome":"Ortus 50 SC","fab":"Outros","cat":"Acaricida","ia":"Fenpiroximato"},
    {"nome":"Oxifluorfem 240 EC","fab":"Outros","cat":"Herbicida","ia":"Oxifluorfem"},
    # ── BASF ──
    {"nome":"Pagani","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol + Fluxapiroxade"},
    # ── OUTROS ──
    {"nome":"Palisade EC","fab":"Outros","cat":"Regulador de Crescimento","ia":"Prohexadona de Cálcio"},
    # ── SYNGENTA ──
    {"nome":"Pallas 45 OD","fab":"Syngenta","cat":"Herbicida","ia":"Piroxsulam"},
    # ── ADAMA ──
    {"nome":"Pantera 40 EC","fab":"ADAMA","cat":"Herbicida","ia":"Quizalofope-P-etílico"},
    # ── BASF ──
    {"nome":"Pavecto","fab":"BASF","cat":"Fungicida","ia":"Mefentrifluconazol + Boscalida"},
    # ── OUTROS ──
    {"nome":"Pendimetalina 400 EC","fab":"Outros","cat":"Herbicida","ia":"Pendimetalina"},
    # ── MOSAIC ──
    {"nome":"Performa Bio","fab":"Mosaic","cat":"Fertilizante","ia":"MAP + S + PGPR"},
    {"nome":"Performa Full","fab":"Mosaic","cat":"Fertilizante","ia":"N+P+K+Mg+S+B completo"},
    {"nome":"Performa HF","fab":"Mosaic","cat":"Fertilizante","ia":"MicroEssentials + Aspire + K-Mag"},
    {"nome":"Performa Neo","fab":"Mosaic","cat":"Fertilizante","ia":"MicroEssentials + K-Mag"},
    {"nome":"Performa Plus","fab":"Mosaic","cat":"Fertilizante","ia":"MicroEssentials + Aspire"},
    {"nome":"Performa Ultra","fab":"Mosaic","cat":"Fertilizante","ia":"K + Mg + S + B"},
    # ── SYNGENTA ──
    {"nome":"Pergado MZ","fab":"Syngenta","cat":"Fungicida","ia":"Mandipropamida + Mancozebe"},
    # ── ADAMA ──
    {"nome":"Permetrina 500 EC","fab":"ADAMA","cat":"Inseticida","ia":"Permetrina"},
    # ── FMC ──
    {"nome":"Persist","fab":"FMC","cat":"Herbicida","ia":"Imazaquim"},
    # ── TIMAC AGRO ──
    {"nome":"Physiostart","fab":"Timac Agro","cat":"Fertilizante","ia":"MAP + Ca + tecnologia Physio"},
    # ── OUTROS ──
    {"nome":"Picloram 240 SL","fab":"Outros","cat":"Herbicida","ia":"Picloram"},
    # ── FMC ──
    {"nome":"Pidan","fab":"FMC","cat":"Inseticida","ia":"Clorfenapir"},
    # ── IHARA ──
    {"nome":"Pidan 360 EC","fab":"Ihara","cat":"Inseticida","ia":"Clorfenapir"},
    # ── OUTROS ──
    {"nome":"Piraclostrobina 250 EC","fab":"Outros","cat":"Fungicida","ia":"Piraclostrobina"},
    # ── BASF ──
    {"nome":"Pirate","fab":"BASF","cat":"Inseticida","ia":"Clorfenapir"},
    {"nome":"Pirimor 500 WG","fab":"BASF","cat":"Inseticida","ia":"Pirimicarbe"},
    # ── ADAMA ──
    {"nome":"Pirimor 500 WG Adama","fab":"ADAMA","cat":"Inseticida","ia":"Pirimicarbe"},
    {"nome":"Pivot 600 CS","fab":"ADAMA","cat":"Herbicida","ia":"Imazetapir"},
    # ── CORTEVA ──
    {"nome":"Pivotal","fab":"Corteva","cat":"Tratamento de Sementes","ia":"Clorantraniliprole + Tiametoxam"},
    # ── BASF ──
    {"nome":"Plateau 700 WG","fab":"BASF","cat":"Herbicida","ia":"Imazapique"},
    # ── BAYER ──
    {"nome":"Plenexos","fab":"Bayer","cat":"Inseticida","ia":"Fluazaindolizina"},
    # ── SYNGENTA ──
    {"nome":"Plinazolin","fab":"Syngenta","cat":"Inseticida","ia":"Plinazolina"},
    # ── OUTROS ──
    {"nome":"Pluto 100 SC","fab":"Outros","cat":"Acaricida","ia":"Etoxazol"},
    # ── ADAMA ──
    {"nome":"Poast","fab":"ADAMA","cat":"Herbicida","ia":"Setoxidim"},
    # ── SYNGENTA ──
    {"nome":"Polo 500 WP","fab":"Syngenta","cat":"Inseticida","ia":"Diafentiurom"},
    # ── BASF ──
    {"nome":"Polyram DF","fab":"BASF","cat":"Fungicida","ia":"Metiram"},
    # ── IHARA ──
    {"nome":"Polytrin 400/40 EC","fab":"Ihara","cat":"Inseticida","ia":"Profenofós + Cipermetrina"},
    # ── BAYER ──
    {"nome":"Poncho 600 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Clotianidina"},
    # ── OUTROS ──
    {"nome":"Potássio Foliar 10%","fab":"Outros","cat":"Foliar / Nutrição","ia":"Potássio"},
    # ── FMC ──
    {"nome":"Predix","fab":"FMC","cat":"Fungicida","ia":"Fluxapiroxade"},
    {"nome":"Premio 200 SC","fab":"FMC","cat":"Inseticida","ia":"Clorantraniliprole"},
    {"nome":"Presence 500","fab":"FMC","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},
    # ── UPL ──
    {"nome":"Presence 500 SC","fab":"UPL","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},
    # ── OURO FINO ──
    {"nome":"Presence OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},
    # ── BASF ──
    {"nome":"Prexio","fab":"BASF","cat":"Inseticida","ia":"Broflanilida"},
    # ── BAYER ──
    {"nome":"Primestra Gold","fab":"Bayer","cat":"Herbicida","ia":"S-Metolacloro + Atrazina"},
    # ── SYNGENTA ──
    {"nome":"Priori Top","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Difenoconazol"},
    {"nome":"Priori Xtra","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Ciproconazol"},
    # ── OURO FINO ──
    {"nome":"Priori Xtra OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Ciproconazol"},
    # ── SYNGENTA ──
    {"nome":"Proclaim 50 WG","fab":"Syngenta","cat":"Inseticida","ia":"Benzoato de Emamectina"},
    # ── ADAMA ──
    {"nome":"Propiconazol 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Propiconazol"},
    # ── UPL ──
    {"nome":"Propose","fab":"UPL","cat":"Inseticida","ia":"Clorantraniliprole + Clorfenapir"},
    # ── BAYER ──
    {"nome":"Prosaro 420 SC","fab":"Bayer","cat":"Fungicida","ia":"Protioconazol + Tebuconazol"},
    # ── OUTROS ──
    {"nome":"Provar","fab":"Outros","cat":"Acaricida","ia":"Hexitiazox"},
    # ── ADAMA ──
    {"nome":"Provost 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Propiconazol + Iprodiona"},
    # ── BAYER ──
    {"nome":"Provost Opti","fab":"Bayer","cat":"Fungicida","ia":"Iprodiona + Propiconazol"},
    # ── SYNGENTA ──
    {"nome":"Quadris","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina"},
    # ── OURO FINO ──
    {"nome":"Rabano","fab":"Ouro Fino","cat":"Herbicida","ia":"Fluazifope-P-butílico + Fomesafem"},
    # ── ADAMA ──
    {"nome":"Rampage 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Ciproconazol"},
    # ── BASF ──
    {"nome":"Raptor","fab":"BASF","cat":"Herbicida","ia":"Imazapique"},
    # ── ADAMA ──
    {"nome":"Ravine 240 EC","fab":"ADAMA","cat":"Fungicida","ia":"Boscalida"},
    {"nome":"Reason 500 SC","fab":"ADAMA","cat":"Fungicida","ia":"Famoxadona + Cimoxanil"},
    # ── SYNGENTA ──
    {"nome":"Rebron","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole + Tiametoxam"},
    # ── ADAMA ──
    {"nome":"Regent 800 WG","fab":"ADAMA","cat":"Inseticida","ia":"Fipronil"},
    # ── BASF ──
    {"nome":"Regent Duo","fab":"BASF","cat":"Inseticida","ia":"Fipronil + Tiametoxam"},
    # ── SYNGENTA ──
    {"nome":"Reglone","fab":"Syngenta","cat":"Herbicida","ia":"Diquat"},
    {"nome":"Revus Opti","fab":"Syngenta","cat":"Fungicida","ia":"Mandipropamida + Clorotalonil"},
    {"nome":"Revus Top","fab":"Syngenta","cat":"Fungicida","ia":"Mandipropamida + Difenoconazol"},
    # ── BASF ──
    {"nome":"Revysol","fab":"BASF","cat":"Fungicida","ia":"Mefentrifluconazol"},
    {"nome":"Rhodiauram 700 WS","fab":"BASF","cat":"Tratamento de Sementes","ia":"Thiram"},
    # ── SYNGENTA ──
    {"nome":"Ridomil Gold MZ","fab":"Syngenta","cat":"Fungicida","ia":"Metalaxil-M + Mancozebe"},
    {"nome":"Ridomil Gold WG","fab":"Syngenta","cat":"Fungicida","ia":"Metalaxil-M + Cobre"},
    # ── CORTEVA ──
    {"nome":"Rinskor Active","fab":"Corteva","cat":"Herbicida","ia":"Florpirauifen-benzil"},
    # ── SYNGENTA ──
    {"nome":"Ripcord 100 EC","fab":"Syngenta","cat":"Inseticida","ia":"Cipermetrina"},
    # ── OUTROS ──
    {"nome":"Rizoliq Top","fab":"Outros","cat":"Fungicida Biológico","ia":"Trichoderma harzianum"},
    # ── BAYER ──
    {"nome":"Roundup Original","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},
    {"nome":"Roundup Powermax","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},
    {"nome":"Roundup Ready","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},
    {"nome":"Roundup Transorb HC","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},
    {"nome":"Roundup Ultra Max","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},
    {"nome":"Roundup WG","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},
    # ── UPL ──
    {"nome":"Rovral SC","fab":"UPL","cat":"Fungicida","ia":"Iprodiona"},
    # ── CORTEVA ──
    {"nome":"Rynaxypyr 200 SC","fab":"Corteva","cat":"Inseticida","ia":"Clorantraniliprole"},
    # ── OUTROS ──
    {"nome":"S-Metolacloro 960 EC","fab":"Outros","cat":"Herbicida","ia":"S-Metolacloro"},
    # ── UPL ──
    {"nome":"Samson Extra 6%","fab":"UPL","cat":"Herbicida","ia":"Nicossulfurom"},
    # ── IHARA ──
    {"nome":"Samurai SC","fab":"Ihara","cat":"Inseticida","ia":"Imidaclopride + Lambda-Cialotrina"},
    # ── ADAMA ──
    {"nome":"Sanmite 150 WP","fab":"ADAMA","cat":"Acaricida","ia":"Piridabem"},
    # ── SYNGENTA ──
    {"nome":"Sanson 40 SC","fab":"Syngenta","cat":"Herbicida","ia":"Nicossulfurom"},
    # ── OUTROS ──
    {"nome":"Savey 50 WP","fab":"Outros","cat":"Acaricida","ia":"Hexitiazox"},
    # ── SYNGENTA ──
    {"nome":"Score 250 EC","fab":"Syngenta","cat":"Fungicida","ia":"Difenoconazol"},
    # ── IHARA ──
    {"nome":"Score Ihara","fab":"Ihara","cat":"Fungicida","ia":"Difenoconazol"},
    # ── OURO FINO ──
    {"nome":"Score OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Difenoconazol"},
    # ── CORTEVA ──
    {"nome":"Select Max","fab":"Corteva","cat":"Herbicida","ia":"Cletodim"},
    # ── BASF ──
    {"nome":"Seltima","fab":"BASF","cat":"Fungicida","ia":"Isoflucipramo + Propiconazol"},
    {"nome":"Seltima Duo","fab":"BASF","cat":"Fungicida","ia":"Isoflucipramo + Trifloxistrobina"},
    # ── BAYER ──
    {"nome":"Semevin 350 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Tiametoxam"},
    # ── ADAMA ──
    {"nome":"Sencor 480 SC","fab":"ADAMA","cat":"Herbicida","ia":"Metribuzim"},
    # ── OUTROS ──
    {"nome":"Serenade ASO","fab":"Outros","cat":"Fungicida Biológico","ia":"Bacillus subtilis"},
    {"nome":"Setoxidim 184 EC","fab":"Outros","cat":"Herbicida","ia":"Setoxidim"},
    # ── MOSAIC ──
    {"nome":"SFP 10-40-00+S","fab":"Mosaic","cat":"Fertilizante","ia":"N + P + S em grânulo único"},
    # ── BAYER ──
    {"nome":"Silvacur Combi","fab":"Bayer","cat":"Fungicida","ia":"Tebuconazol + Triadimenol"},
    # ── OUTROS ──
    {"nome":"Silwet L-77","fab":"Outros","cat":"Adjuvante","ia":"Silicone"},
    # ── BAYER ──
    {"nome":"Sivanto Prime 100 SL","fab":"Bayer","cat":"Inseticida","ia":"Flupyradifurona"},
    {"nome":"Sivanto Prime 200 SL","fab":"Bayer","cat":"Inseticida","ia":"Flupyradifurona"},
    {"nome":"Sonata AS","fab":"Bayer","cat":"Inseticida Biológico","ia":"Bacillus pumilus"},
    # ── UPL ──
    {"nome":"Sperto","fab":"UPL","cat":"Inseticida","ia":"Bifentrina + Imidaclopride"},
    # ── BAYER ──
    {"nome":"Sphere Max","fab":"Bayer","cat":"Fungicida","ia":"Trifloxistrobina + Ciproconazol"},
    # ── UPL ──
    {"nome":"Sphere OF","fab":"UPL","cat":"Fungicida","ia":"Trifloxistrobina + Ciproconazol"},
    # ── CORTEVA ──
    {"nome":"Spinetoram 250 SC","fab":"Corteva","cat":"Inseticida","ia":"Espinetoram"},
    # ── UPL ──
    {"nome":"Spinnaker","fab":"UPL","cat":"Herbicida","ia":"Imazapique"},
    # ── CORTEVA ──
    {"nome":"Spintor 480 SC","fab":"Corteva","cat":"Inseticida","ia":"Espinosade"},
    # ── OUTROS ──
    {"nome":"Spiromax 240 SC","fab":"Outros","cat":"Acaricida","ia":"Espirodiclofeno"},
    # ── SYNGENTA ──
    {"nome":"Sponta Algodão","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole"},
    {"nome":"Sponta Milho","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole"},
    # ── BASF ──
    {"nome":"Spot SC","fab":"BASF","cat":"Fungicida","ia":"Fluazinam"},
    # ── OUTROS ──
    {"nome":"Spread Max","fab":"Outros","cat":"Adjuvante","ia":"Surfactante"},
    # ── BAYER ──
    {"nome":"Standak Top","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Fipronil + Piraclostrobina + Tiofanato"},
    # ── CORTEVA ──
    {"nome":"Starane Quatro","fab":"Corteva","cat":"Herbicida","ia":"Fluroxipir-meptílico"},
    # ── UPL ──
    {"nome":"Start UPL","fab":"UPL","cat":"Inseticida","ia":"Fipronil"},
    # ── TIMAC AGRO ──
    {"nome":"Starter Timac","fab":"Timac Agro","cat":"Fertilizante","ia":"N + P + Zn + aminoácidos"},
    # ── BASF ──
    {"nome":"Status","fab":"BASF","cat":"Fungicida","ia":"Dimoxistrobina + Epoxiconazol"},
    # ── OUTROS ──
    {"nome":"Stimulate Foliar","fab":"Outros","cat":"Regulador de Crescimento","ia":"Citocinina + Auxina + Giberelina"},
    # ── ADAMA ──
    {"nome":"Stomp 400 CS","fab":"ADAMA","cat":"Herbicida","ia":"Pendimetalina"},
    # ── OUTROS ──
    {"nome":"Stopit Ca","fab":"Outros","cat":"Foliar / Nutrição","ia":"Cálcio"},
    # ── BAYER ──
    {"nome":"Stratego 250 EC","fab":"Bayer","cat":"Fungicida","ia":"Trifloxistrobina + Propiconazol"},
    # ── BASF ──
    {"nome":"Stroby SC","fab":"BASF","cat":"Fungicida","ia":"Cresoxim-metílico"},
    # ── TIMAC AGRO ──
    {"nome":"Sulfammo 26N","fab":"Timac Agro","cat":"Fertilizante","ia":"26% N amoniacal + S"},
    {"nome":"Sulfammo MeTA 11","fab":"Timac Agro","cat":"Fertilizante","ia":"11% N + S inibidor MeTA"},
    {"nome":"Sulfammo MeTA 17","fab":"Timac Agro","cat":"Fertilizante","ia":"17% N + S inibidor MeTA"},
    {"nome":"Sulfammo MeTA 21","fab":"Timac Agro","cat":"Fertilizante","ia":"21% N + S inibidor MeTA"},
    {"nome":"Sulfammo MeTA 29","fab":"Timac Agro","cat":"Fertilizante","ia":"29% N + S inibidor MeTA"},
    {"nome":"Sulfammo MeTA 29 Boro","fab":"Timac Agro","cat":"Fertilizante","ia":"29% N + S + B"},
    {"nome":"Sulfammo Ultra","fab":"Timac Agro","cat":"Fertilizante","ia":"N + S alta concentração"},
    # ── OUTROS ──
    {"nome":"Sulfato de Amônio","fab":"Outros","cat":"Fertilizante","ia":"21% N + 24% S"},
    {"nome":"Sulfato de Magnésio","fab":"Outros","cat":"Fertilizante","ia":"Mg 10% + S 13%"},
    {"nome":"Sulfato de Manganês","fab":"Outros","cat":"Fertilizante","ia":"Mn 26% + S"},
    {"nome":"Sulfato de Potássio","fab":"Outros","cat":"Fertilizante","ia":"K2SO4 50% K2O + 18% S"},
    {"nome":"Sulfato de Zinco","fab":"Outros","cat":"Fertilizante","ia":"Zn 21% + S 11%"},
    {"nome":"Sulfentrazona 500 SC","fab":"Outros","cat":"Herbicida","ia":"Sulfentrazona"},
    # ── ADAMA ──
    {"nome":"Sumidan 25 EC","fab":"ADAMA","cat":"Inseticida","ia":"Esfenvalerato"},
    {"nome":"Sumithion 500 EC","fab":"ADAMA","cat":"Inseticida","ia":"Fenitrotiom"},
    # ── OUTROS ──
    {"nome":"Superfosfato Simples","fab":"Outros","cat":"Fertilizante","ia":"SSP 18% P2O5 + 12% S"},
    {"nome":"Superfosfato Triplo","fab":"Outros","cat":"Fertilizante","ia":"STP 46% P2O5"},
    # ── BASF ──
    {"nome":"Surtain","fab":"BASF","cat":"Herbicida","ia":"Saflufenacil + Clomazona"},
    # ── CORTEVA ──
    {"nome":"Switch 625 WG","fab":"Corteva","cat":"Fungicida","ia":"Ciprodinil + Fludioxonil"},
    # ── ADAMA ──
    {"nome":"Systhane 750 WG","fab":"ADAMA","cat":"Fungicida","ia":"Miclobutanil"},
    # ── UPL ──
    {"nome":"Tacklier","fab":"UPL","cat":"Inseticida Biológico","ia":"Bacillus thuringiensis"},
    # ── IHARA ──
    {"nome":"Takumi 20 SC","fab":"Ihara","cat":"Inseticida","ia":"Flubendiamida"},
    # ── FMC ──
    {"nome":"Talstar 100 EC","fab":"FMC","cat":"Inseticida","ia":"Bifentrina"},
    # ── BASF ──
    {"nome":"Targa Max 50 EC","fab":"BASF","cat":"Herbicida","ia":"Quizalofope-P-etílico"},
    # ── ADAMA ──
    {"nome":"Targa Quik","fab":"ADAMA","cat":"Herbicida","ia":"Quizalofope-P-etílico"},
    # ── OURO FINO ──
    {"nome":"Tebuco OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Tebuconazol"},
    # ── BAYER ──
    {"nome":"Tebuconazol 200 EC","fab":"Bayer","cat":"Fungicida","ia":"Tebuconazol"},
    # ── ADAMA ──
    {"nome":"Tebuconazol 750 WG","fab":"ADAMA","cat":"Fungicida","ia":"Tebuconazol"},
    # ── OUTROS ──
    {"nome":"Tepraloxidim 200 EC","fab":"Outros","cat":"Herbicida","ia":"Tepraloxidim"},
    {"nome":"Termofosfato Yoorin","fab":"Outros","cat":"Fertilizante","ia":"P2O5 18% + Ca + Mg + Si"},
    # ── ADAMA ──
    {"nome":"Thiram 480 SC","fab":"ADAMA","cat":"Fungicida","ia":"Thiram"},
    # ── OUTROS ──
    {"nome":"Thiram 750 WS","fab":"Outros","cat":"Fungicida","ia":"Thiram"},
    # ── UPL ──
    {"nome":"Thunder","fab":"UPL","cat":"Herbicida","ia":"Asulam"},
    # ── OUTROS ──
    {"nome":"Tiametoxam 700 WS","fab":"Outros","cat":"Inseticida","ia":"Tiametoxam"},
    # ── FMC ──
    {"nome":"Tiger 100 EC","fab":"FMC","cat":"Inseticida","ia":"Bifentrina"},
    # ── ADAMA ──
    {"nome":"Tilt 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Propiconazol"},
    # ── OUTROS ──
    {"nome":"Tiofanato Metílico 700 WG","fab":"Outros","cat":"Fungicida","ia":"Tiofanato Metílico"},
    # ── BASF ──
    {"nome":"Tirexor","fab":"BASF","cat":"Herbicida","ia":"Trifludimoxazim"},
    # ── TIMAC AGRO ──
    {"nome":"Top-Phos","fab":"Timac Agro","cat":"Fertilizante","ia":"MAP protegido tecnologia CSP"},
    {"nome":"Top-Phos 40","fab":"Timac Agro","cat":"Fertilizante","ia":"Fosfato amoniado protegido 40% P2O5"},
    {"nome":"Top-Phos Arroz","fab":"Timac Agro","cat":"Fertilizante","ia":"Fósforo protegido para arroz"},
    # ── BAYER ──
    {"nome":"Tordon","fab":"Bayer","cat":"Herbicida","ia":"2,4-D + Picloram"},
    # ── CORTEVA ──
    {"nome":"Tornade Duo","fab":"Corteva","cat":"Herbicida","ia":"2,4-D + Picloram"},
    # ── IHARA ──
    {"nome":"Torque 550 SC","fab":"Ihara","cat":"Acaricida","ia":"Fenbutestanho"},
    # ── SYNGENTA ──
    {"nome":"Touchdown IQ","fab":"Syngenta","cat":"Herbicida","ia":"Glifosato"},
    # ── CORTEVA ──
    {"nome":"Tracer 480 SC","fab":"Corteva","cat":"Inseticida","ia":"Espinosade"},
    # ── FMC ──
    {"nome":"Transform 500 WG","fab":"FMC","cat":"Inseticida","ia":"Sulfoxaflor"},
    # ── OUTROS ──
    {"nome":"Trico WP","fab":"Outros","cat":"Fungicida Biológico","ia":"Trichoderma viride"},
    # ── UPL ──
    {"nome":"Tridium","fab":"UPL","cat":"Fungicida","ia":"Trifloxistrobina + Epoxiconazol + Tebuconazol"},
    # ── OUTROS ──
    {"nome":"Trifloxistrobina 250 SC","fab":"Outros","cat":"Fungicida","ia":"Trifloxistrobina"},
    {"nome":"Trifluralin 480 EC","fab":"Outros","cat":"Herbicida","ia":"Trifluralina"},
    # ── BAYER ──
    {"nome":"Trilex Advance","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Trifloxistrobina + Protioconazol + Spirotetramat"},
    # ── SYNGENTA ──
    {"nome":"Trophy 500 EC","fab":"Syngenta","cat":"Herbicida","ia":"Acetocloro"},
    # ── MOSAIC ──
    {"nome":"TSP Mosaic","fab":"Mosaic","cat":"Fertilizante","ia":"Superfosfato triplo 00-46-00"},
    # ── OUTROS ──
    {"nome":"Unika Ca+B","fab":"Outros","cat":"Foliar / Nutrição","ia":"Cálcio + Boro"},
    # ── BAYER ──
    {"nome":"Unison Xpro","fab":"Bayer","cat":"Fungicida","ia":"Bixafem + Propiconazol + Trifloxistrobina"},
    # ── SYNGENTA ──
    {"nome":"Unizeb 750 WG","fab":"Syngenta","cat":"Fungicida","ia":"Mancozebe"},
    # ── UPL ──
    {"nome":"Unizeb Gold","fab":"UPL","cat":"Fungicida","ia":"Mancozebe 750 WG"},
    # ── OUTROS ──
    {"nome":"Ureia 45% N","fab":"Outros","cat":"Fertilizante","ia":"Carbamida 45% N"},
    {"nome":"Ureia NBPT","fab":"Outros","cat":"Fertilizante","ia":"Ureia + inibidor urease NBPT"},
    # ── UPL ──
    {"nome":"Velpar K WG","fab":"UPL","cat":"Herbicida","ia":"Hexazinona + Diurom"},
    # ── OUTROS ──
    {"nome":"Velum Prime","fab":"Outros","cat":"Nematicida","ia":"Fluopyram"},
    # ── OURO FINO ──
    {"nome":"Verdadeiro","fab":"Ouro Fino","cat":"Inseticida","ia":"Tiametoxam"},
    # ── SYNGENTA ──
    {"nome":"Verdadero","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam"},
    {"nome":"Verdavis Milho","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Clorantraniliprole"},
    {"nome":"Verdavis Soja","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Clorantraniliprole"},
    # ── BASF ──
    {"nome":"Verismo","fab":"BASF","cat":"Inseticida","ia":"Metaflumizone"},
    # ── SYNGENTA ──
    {"nome":"Versys","fab":"Syngenta","cat":"Inseticida","ia":"Flupyrimin + Lambda-Cialotrina"},
    # ── ADAMA ──
    {"nome":"Vertimec 18 EC","fab":"ADAMA","cat":"Acaricida","ia":"Abamectina"},
    # ── IHARA ──
    {"nome":"Vertimec Gold","fab":"Ihara","cat":"Acaricida","ia":"Abamectina"},
    # ── SYNGENTA ──
    {"nome":"Vibrance Duo","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Sedaxane + Fludioxonil"},
    {"nome":"Vibrance Integral","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Sedaxane + Fludioxonil + Metalaxil-M"},
    # ── BASF ──
    {"nome":"Vitavax Thiram 200 SC","fab":"BASF","cat":"Tratamento de Sementes","ia":"Carboxim + Thiram"},
    # ── UPL ──
    {"nome":"Vitavax Thiram 200 SC UPL","fab":"UPL","cat":"Fungicida","ia":"Carboxim + Thiram"},
    {"nome":"Vitavax Ultra TS","fab":"UPL","cat":"Tratamento de Sementes","ia":"Carboxim + Tiram + Tiametoxam"},
    # ── SYNGENTA ──
    {"nome":"Voliam Flexi","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Clorantraniliprole"},
    {"nome":"Voliam Targo","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole + Abamectina"},
    # ── BASF ──
    {"nome":"Voraxor","fab":"BASF","cat":"Herbicida","ia":"Trifludimoxazim + Saflufenacil"},
    {"nome":"Vydate 240 SL","fab":"BASF","cat":"Inseticida","ia":"Oxamil"},
    # ── IHARA ──
    {"nome":"Xcyte","fab":"Ihara","cat":"Inseticida","ia":"Ciantraniliprole + Clorfenapir"},
    # ── OUTROS ──
    {"nome":"XenTari WDG","fab":"Outros","cat":"Inseticida Biológico","ia":"Bacillus thuringiensis aizawai"},
    # ── BASF ──
    {"nome":"Zampro","fab":"BASF","cat":"Fungicida","ia":"Ametoctradina + Dimetomorfe"},
    # ── OUTROS ──
    {"nome":"Zeal 72 WP","fab":"Outros","cat":"Acaricida","ia":"Etoxazol"},
    # ── ADAMA ──
    {"nome":"Zeta-Cipermetrina 250 EC","fab":"ADAMA","cat":"Inseticida","ia":"Zeta-Cipermetrina"},
    # ── OURO FINO ──
    {"nome":"Zeus OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Epoxiconazol"},
    # ── OUTROS ──
    {"nome":"Zinco Quelatado 9%","fab":"Outros","cat":"Foliar / Nutrição","ia":"Zinco"},
    # ── FMC ──
    {"nome":"Zoom 750 WG","fab":"FMC","cat":"Inseticida","ia":"Acefato"},
    # ── OUTROS ──
    {"nome":"Ácido Bórico","fab":"Outros","cat":"Fertilizante","ia":"B 17%"},
    # ── OURO FINO ──
    {"nome":"Ênio 200 SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Iprodiona"},
]


# Ordena por nome para o autocomplete
CATALOGO_PRODUTOS.sort(key=lambda x: x["nome"].lower())

def buscar_produtos_catalogo(query):
    """Retorna produtos do catálogo filtrando por nome ou ingrediente ativo."""
    if not query:
        return CATALOGO_PRODUTOS
    q = query.lower()
    # Primeiro os que COMEÇAM com a busca
    starts = [p for p in CATALOGO_PRODUTOS if p["nome"].lower().startswith(q)]
    # Depois os que CONTÊM em qualquer posição (nome ou IA)
    contains = [p for p in CATALOGO_PRODUTOS
                if not p["nome"].lower().startswith(q)
                and (q in p["nome"].lower() or q in p["ia"].lower() or q in p["cat"].lower())]
    return starts + contains


# ─────────────────────────────────────────────
# MENU: ESTOQUE DE INSUMOS
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


def gerar_pdf_programacao_aplicacoes(aplicacoes, fazenda="", talhao="", cultura="", area_ha=0, operador=""):
    """Gera PDF profissional com programação de aplicações por estádio."""
    import io
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm, mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            rightMargin=1.5*cm, leftMargin=1.5*cm,
                            topMargin=1.5*cm, bottomMargin=2*cm)
    story = []

    COR_VERDE  = colors.HexColor("#16a34a")
    COR_VERDE_E= colors.HexColor("#14532d")
    COR_AZUL   = colors.HexColor("#1e3a5f")
    COR_CINZA  = colors.HexColor("#f1f5f9")
    COR_BORDA  = colors.HexColor("#e2e8f0")
    COR_BRANCO = colors.white
    COR_TEXTO  = colors.HexColor("#0f172a")
    COR_SUB    = colors.HexColor("#64748b")
    COR_TIPO   = {
        "Herbicida":colors.HexColor("#fef3c7"),"Fungicida":colors.HexColor("#dbeafe"),
        "Inseticida":colors.HexColor("#fee2e2"),"Adjuvante":colors.HexColor("#d1fae5"),
        "Óleo mineral/vegetal":colors.HexColor("#ede9fe"),"Fertilizante foliar":colors.HexColor("#fce7f3"),
        "Regulador":colors.HexColor("#ffedd5"),"Outro":COR_CINZA,
    }

    def P(txt, size=9, bold=False, color=None, align=TA_LEFT):
        fn = "Helvetica-Bold" if bold else "Helvetica"
        c  = color or COR_TEXTO
        return Paragraph(txt, ParagraphStyle("p", fontName=fn, fontSize=size, textColor=c, alignment=align, leading=size+3))

    # CABEÇALHO
    h = [[P("IAAgro",18,True,COR_VERDE), P("PROGRAMAÇÃO DE APLICACOES",14,True,COR_BRANCO,TA_CENTER),
          P(f"Emitido: {datetime.now().strftime('%d/%m/%Y %H:%M')}",7,False,COR_CINZA,TA_RIGHT)]]
    th = Table(h, colWidths=[4*cm,10*cm,4.5*cm])
    th.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),COR_VERDE_E),
        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    story.append(th); story.append(Spacer(1,3*mm))

    # INFO PROPRIEDADE
    i = [[P(f"<b>Fazenda:</b> {fazenda or '—'}"),P(f"<b>Talhao:</b> {talhao or '—'}"),
          P(f"<b>Cultura:</b> {cultura or '—'}"),P(f"<b>Area:</b> {area_ha} ha"),
          P(f"<b>Responsavel:</b> {operador or '—'}")]]
    ti = Table(i, colWidths=[3.5*cm,3.5*cm,3*cm,2.5*cm,6*cm])
    ti.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),COR_CINZA),("GRID",(0,0),(-1,-1),0.4,COR_BORDA),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),6)]))
    story.append(ti); story.append(Spacer(1,4*mm))

    # LEGENDA
    leg = [("Herbicida","#fef3c7"),("Fungicida","#dbeafe"),("Inseticida","#fee2e2"),
           ("Adjuvante","#d1fae5"),("Oleo","#ede9fe"),("Fert.Foliar","#fce7f3")]
    tl = Table([[P(n,7,True) for n,_ in leg]], colWidths=[3*cm]*6)
    tl.setStyle(TableStyle([*[("BACKGROUND",(i,0),(i,0),colors.HexColor(c)) for i,(n,c) in enumerate(leg)],
        ("GRID",(0,0),(-1,-1),0.3,COR_BORDA),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("ALIGN",(0,0),(-1,-1),"CENTER")]))
    story.append(P("Legenda:",7,False,COR_SUB)); story.append(Spacer(1,1*mm))
    story.append(tl); story.append(Spacer(1,5*mm))

    # BLOCOS POR ESTÁDIO
    for num, aplic in enumerate(aplicacoes, 1):
        est = aplic.get("Estádio") or aplic.get("Aplicação","")
        for e in ["🌱","🌿","🌾","🌸","🫘","📋"]: est = est.replace(e,"").strip()

        cab = [[P(f"{num}. {est}",11,True,COR_BRANCO),
                P(f"Data: {aplic.get('Data','—')} | Area: {aplic.get('Área aplicada ha',0)} ha | "
                  f"Calda: {aplic.get('Volume calda L/ha',0)} L/ha | "
                  f"Tanques: {aplic.get('Número tanques',0):.1f} | "
                  f"Pulverizador: {aplic.get('Pulverizador','—')} | "
                  f"Clima: {aplic.get('Clima aplicação','—')}",8,False,COR_CINZA)]]
        tc = Table(cab, colWidths=[4.5*cm,14*cm])
        tc.setStyle(TableStyle([("BACKGROUND",(0,0),(0,0),COR_VERDE),("BACKGROUND",(1,0),(1,0),COR_AZUL),
            ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
            ("LEFTPADDING",(0,0),(-1,-1),8),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))

        hdr = [P("PRODUTO",8,True,COR_BRANCO,TA_CENTER),P("TIPO",8,True,COR_BRANCO,TA_CENTER),
               P("DOSE/ha",8,True,COR_BRANCO,TA_CENTER),P("UNIDADE",8,True,COR_BRANCO,TA_CENTER),
               P("POR TANQUE",8,True,COR_BRANCO,TA_CENTER),P("TOTAL AREA",8,True,COR_BRANCO,TA_CENTER)]
        rows = [hdr]
        for p in aplic.get("Produtos",[]):
            unid = p.get("Unidade","").replace("/ha","")
            rows.append([
                P(f"<b>{p.get('Produto','')}</b>",8,True),
                P(p.get("Tipo",""),8),
                P(str(p.get("Dose por ha",0)),8,False,None,TA_CENTER),
                P(p.get("Unidade",""),8,False,None,TA_CENTER),
                P(f"<b>{p.get('Produto por tanque',0):.2f}</b> {unid}",8,True,None,TA_CENTER),
                P(f"<b>{p.get('Total usado',0):.2f}</b> {unid}",8,True,COR_VERDE_E,TA_CENTER),
            ])
        tp = Table(rows, colWidths=[4.5*cm,2.5*cm,2*cm,2*cm,3*cm,4.5*cm])
        stp = [("BACKGROUND",(0,0),(-1,0),COR_VERDE_E),("GRID",(0,0),(-1,-1),0.4,COR_BORDA),
               ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
               ("LEFTPADDING",(0,0),(-1,-1),6),("VALIGN",(0,0),(-1,-1),"MIDDLE")]
        for ri, p in enumerate(aplic.get("Produtos",[]),1):
            stp.append(("BACKGROUND",(1,ri),(1,ri),COR_TIPO.get(p.get("Tipo",""),COR_CINZA)))
            stp.append(("BACKGROUND",(0,ri),(0,ri),COR_CINZA if ri%2 else COR_BRANCO))
        tp.setStyle(TableStyle(stp))

        ass = [[P(f"<b>Operador:</b> {aplic.get('Operador','_________________________')}",8),
                P("<b>Inicio:</b> ____/____/______ ___:___ h",8),
                P("<b>Assinatura:</b> _______________________",8)]]
        ta = Table(ass, colWidths=[5.5*cm,5.5*cm,7.5*cm])
        ta.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#f8fafc")),
            ("GRID",(0,0),(-1,-1),0.3,COR_BORDA),("TOPPADDING",(0,0),(-1,-1),5),
            ("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),8)]))

        story.append(KeepTogether([tc,tp,ta,Spacer(1,5*mm)]))

    story.append(HRFlowable(width="100%",thickness=1,color=COR_VERDE))
    story.append(Spacer(1,2*mm))
    story.append(P(f"IAAgro - Inteligencia Agricola de Precisao | {datetime.now().strftime('%d/%m/%Y %H:%M')} | Uso interno",
                   7,False,COR_SUB,TA_CENTER))
    doc.build(story)
    buf.seek(0)
    return buf.read()


def calcular_calcario_por_ph(ph, area):
    """
    Calagem pelo método SMP (CQFS RS/SC 2016) ou pH em água.
    PRNT médio adotado: 75% (calcário comercial típico da região Sul)
    Fórmula: NC (t/ha) = dose_base / (PRNT/100)
    """
    PRNT = 0.75  # PRNT médio 75% — calcário comercial RS/SC/PR

    if   ph < 4.8: dose_base = 4.0
    elif ph < 5.0: dose_base = 3.5
    elif ph < 5.2: dose_base = 3.0
    elif ph < 5.4: dose_base = 2.5
    elif ph < 5.5: dose_base = 2.0
    elif ph < 5.6: dose_base = 1.5
    elif ph < 5.8: dose_base = 1.0
    elif ph < 6.0: dose_base = 0.5
    else:          dose_base = 0.0

    # Corrige pelo PRNT 75%
    dose = round(dose_base / PRNT, 2) if dose_base > 0 else 0.0
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
    # Remove ícone se presente
    cultura = cultura_limpa(cultura) if cultura else "Soja"
    """
    Recomendação NPK baseada em:
    - EMBRAPA Soja — Circular Técnica 98 + Tecnologias de Produção 2022
    - EMBRAPA Milho e Sorgo — Circular Técnica 100/2023
    - CQFS RS/SC 2016 (Manual de Calagem e Adubação)
    - IAC Boletim 100 (2014) — culturas diversas
    - EMBRAPA Trigo — Recomendações Técnicas 2021
    - EMBRAPA Arroz e Feijão
    - MAPA — Boas Práticas Agrícolas
    Unidades: kg/ha de N, P2O5, K2O
    P = Mehlich-1 (mg/dm³) | K = mg/dm³ | MO = g/dm³ ou %
    """
    n = p2o5 = k2o = 0

    if cultura == "Soja":
        # EMBRAPA Soja: N=0 com boa nodulação (BNF supre 200-300 kg N/ha)
        n = 0
        # P2O5 — CQFS RS/SC 2016 Tab. 4.3 — solo argiloso (argila 41-60%)
        # Exportação: ~16 kg P2O5/sc (60 kg) → manutenção + reposição
        if   fosforo < 4:   p2o5 = 140
        elif fosforo < 7:   p2o5 = 110
        elif fosforo < 11:  p2o5 = 90
        elif fosforo < 16:  p2o5 = 70
        elif fosforo < 22:  p2o5 = 55
        elif fosforo < 30:  p2o5 = 40
        else:               p2o5 = 25
        # K2O — CQFS RS/SC 2016 Tab. 4.4 — exportação ~18 kg K2O/sc
        if   potassio < 40:  k2o = 130
        elif potassio < 60:  k2o = 105
        elif potassio < 80:  k2o = 85
        elif potassio < 120: k2o = 70
        elif potassio < 180: k2o = 55
        elif potassio < 240: k2o = 40
        else:                k2o = 25
        # Ajuste produtividade (EMBRAPA — base 50 sc/ha)
        fator_prod = max(1.0, produtividade / 50)
        p2o5 = round(p2o5 * fator_prod, 0)
        k2o  = round(k2o  * fator_prod, 0)

    elif cultura == "Milho":
        # EMBRAPA Milho — base 10 t/ha, N parcelado (plantio + cobertura)
        # N plantio: 20-30 kg/ha | N cobertura: 30-50 kg/ha por 1000 kg grão
        n_plantio = 25
        n_cob     = min(produtividade * 1.5, 140)  # 1,5 kg N / sc 60kg
        n = round(n_plantio + n_cob, 1)
        # P2O5 — CQFS 2016 Tab. 5.3
        if   fosforo < 4:   p2o5 = 130
        elif fosforo < 7:   p2o5 = 105
        elif fosforo < 11:  p2o5 = 85
        elif fosforo < 16:  p2o5 = 65
        elif fosforo < 22:  p2o5 = 50
        elif fosforo < 30:  p2o5 = 35
        else:               p2o5 = 20
        # K2O — CQFS 2016 Tab. 5.4
        if   potassio < 40:  k2o = 120
        elif potassio < 60:  k2o = 95
        elif potassio < 80:  k2o = 75
        elif potassio < 120: k2o = 60
        elif potassio < 180: k2o = 45
        elif potassio < 240: k2o = 30
        else:                k2o = 20
        # Alta produtividade (>150 sc/ha = 9 t/ha)
        if produtividade > 150: p2o5 += 25; k2o += 30; n = min(n + 25, 180)

    elif cultura == "Trigo":
        # EMBRAPA Trigo — Sistema Plantio Direto Sul Brasil 2021
        # N = 30 plantio + cobertura conforme MO e produtividade
        if   materia_organica < 2.5: n = 30 + produtividade * 1.0
        elif materia_organica < 4.0: n = 20 + produtividade * 0.9
        else:                        n = 15 + produtividade * 0.8
        n = min(round(n, 1), 100)
        # P2O5 — CQFS 2016
        if   fosforo < 4:   p2o5 = 110
        elif fosforo < 7:   p2o5 = 90
        elif fosforo < 11:  p2o5 = 70
        elif fosforo < 16:  p2o5 = 55
        elif fosforo < 22:  p2o5 = 40
        else:               p2o5 = 25
        # K2O — CQFS 2016
        if   potassio < 60:  k2o = 90
        elif potassio < 80:  k2o = 70
        elif potassio < 120: k2o = 55
        elif potassio < 180: k2o = 40
        else:                k2o = 25

    elif cultura == "Feijão":
        # EMBRAPA Feijão + CQFS 2016 — fixação parcial de N
        # N starter 20 kg/ha + complemento se não inoculado
        n = 20
        if materia_organica < 2.5: n = 30
        # P2O5
        if   fosforo < 7:   p2o5 = 100
        elif fosforo < 11:  p2o5 = 80
        elif fosforo < 16:  p2o5 = 65
        elif fosforo < 22:  p2o5 = 50
        elif fosforo < 30:  p2o5 = 35
        else:               p2o5 = 20
        # K2O
        if   potassio < 60:  k2o = 80
        elif potassio < 80:  k2o = 65
        elif potassio < 120: k2o = 50
        elif potassio < 180: k2o = 35
        else:                k2o = 20

    elif cultura == "Arroz":
        # EMBRAPA Arroz e Feijão — irrigado e sequeiro
        n = round(20 + produtividade * 2.0, 1)
        n = min(n, 130)
        if   fosforo < 7:   p2o5 = 90
        elif fosforo < 11:  p2o5 = 70
        elif fosforo < 16:  p2o5 = 55
        elif fosforo < 22:  p2o5 = 40
        else:               p2o5 = 25
        if   potassio < 60:  k2o = 90
        elif potassio < 80:  k2o = 70
        elif potassio < 120: k2o = 55
        elif potassio < 180: k2o = 40
        else:                k2o = 25

    elif cultura == "Canola":
        # EMBRAPA Trigo adaptado + pesquisas Paraná/RS
        # Canola extrai muito enxofre — recomenda gesso
        n = round(30 + produtividade * 2.5, 1)
        n = min(n, 120)
        if   fosforo < 7:   p2o5 = 90
        elif fosforo < 11:  p2o5 = 70
        elif fosforo < 16:  p2o5 = 55
        elif fosforo < 22:  p2o5 = 40
        else:               p2o5 = 25
        if   potassio < 60:  k2o = 80
        elif potassio < 80:  k2o = 65
        elif potassio < 120: k2o = 50
        elif potassio < 180: k2o = 35
        else:                k2o = 20

    elif cultura in ["Aveia", "Cevada"]:
        # CQFS RS/SC 2016
        n = round(15 + produtividade * 1.5, 1)
        n = min(n, 90)
        if   fosforo < 7:   p2o5 = 80
        elif fosforo < 11:  p2o5 = 65
        elif fosforo < 16:  p2o5 = 50
        elif fosforo < 22:  p2o5 = 35
        else:               p2o5 = 20
        if   potassio < 60:  k2o = 70
        elif potassio < 80:  k2o = 55
        elif potassio < 120: k2o = 40
        elif potassio < 180: k2o = 30
        else:                k2o = 20

    elif cultura == "Sorgo":
        # EMBRAPA Milho e Sorgo
        n = round(20 + produtividade * 1.5, 1)
        n = min(n, 100)
        if   fosforo < 7:   p2o5 = 75
        elif fosforo < 11:  p2o5 = 60
        elif fosforo < 16:  p2o5 = 45
        else:               p2o5 = 30
        if   potassio < 60:  k2o = 70
        elif potassio < 120: k2o = 50
        else:                k2o = 30

    elif cultura == "Café":
        # EMBRAPA Café — Circular Técnica 132
        # Produtividade em sc/ha beneficiado
        n  = round(80 + produtividade * 1.5, 1)
        n  = min(n, 300)
        if   fosforo < 10:  p2o5 = 100
        elif fosforo < 20:  p2o5 = 70
        elif fosforo < 40:  p2o5 = 50
        else:               p2o5 = 30
        if   potassio < 60:  k2o = 180
        elif potassio < 120: k2o = 140
        elif potassio < 180: k2o = 100
        else:                k2o = 70

    elif cultura in ["Tomate", "Batata"]:
        # IAC Boletim 100 — horticultura
        n  = round(120 + produtividade * 0.8, 1)
        p2o5 = 120 if fosforo < 30 else 80
        k2o  = 200 if potassio < 150 else 150

    elif cultura in ["Eucalipto", "Pinus"]:
        # EMBRAPA Florestas
        n = 30; p2o5 = 100; k2o = 50

    elif cultura == "Pastagem":
        # EMBRAPA Gado de Corte/Leite
        n  = round(40 + produtividade * 0.5, 1)
        n  = min(n, 120)
        p2o5 = 60 if fosforo < 15 else 30
        k2o  = 60 if potassio < 100 else 30

    else:
        # Genérico — conservador
        n = 40; p2o5 = 60; k2o = 60

    # ── Ajustes gerais de solo ──────────────────────────────
    # Textura: solos arenosos (<20% argila) têm menor CTC → mais K
    if argila < 15:     k2o = round(k2o * 1.25, 0)
    elif argila < 25:   k2o = round(k2o * 1.15, 0)
    elif argila > 70:   k2o = round(k2o * 0.90, 0)

    # MO alta reduz necessidade de N (mineralização)
    if materia_organica >= 5.5:   n = round(n * 0.70, 1)
    elif materia_organica >= 4.0: n = round(n * 0.80, 1)
    elif materia_organica >= 3.0: n = round(n * 0.90, 1)

    # pH baixo reduz disponibilidade de P (precipitação com Al e Fe)
    if ph < 5.0:   p2o5 = round(p2o5 * 1.30, 0)
    elif ph < 5.3: p2o5 = round(p2o5 * 1.15, 0)
    elif ph < 5.5: p2o5 = round(p2o5 * 1.08, 0)

    return round(n, 1), round(p2o5, 1), round(k2o, 1)


def score_solo(d, cultura="Soja"):
    """
    Score de qualidade do solo baseado nos parâmetros EMBRAPA/CQFS RS-SC 2016
    Considera limites ideais por cultura
    """
    cultura = cultura_limpa(cultura) if cultura else "Soja"
    score   = 100
    alertas = []
    ph               = d.get("ph", 0)
    fosforo          = d.get("fosforo", 0)
    potassio         = d.get("potassio", 0)
    calcio           = d.get("calcio", 0)
    magnesio         = d.get("magnesio", 0)
    aluminio         = d.get("aluminio", 0)
    materia_organica = d.get("materia_organica", 0)
    enxofre          = d.get("enxofre", 0)
    zinco            = d.get("zinco", 0)
    boro             = d.get("boro", 0)

    # pH ideal por cultura (EMBRAPA/CQFS)
    ph_ideais = {
        "Soja": (5.8, 6.5), "Milho": (5.8, 6.5), "Trigo": (5.8, 6.5),
        "Feijão": (6.0, 6.5), "Arroz": (5.5, 6.0), "Canola": (6.0, 6.5),
        "Café": (5.5, 6.5), "Tomate": (6.0, 6.8), "Batata": (5.5, 6.0),
        "Eucalipto": (5.0, 6.0), "Pinus": (4.5, 5.5),
    }
    ph_min, ph_max = ph_ideais.get(cultura, (5.8, 6.5))

    # pH
    if ph > 0:
        if ph < ph_min - 0.5:
            score -= 20; alertas.append(f"pH muito baixo para {cultura} (ideal {ph_min}-{ph_max})")
        elif ph < ph_min:
            score -= 10; alertas.append(f"pH abaixo do ideal para {cultura}")
        elif ph > ph_max + 0.5:
            score -= 10; alertas.append(f"pH elevado — risco de deficiência de micronutrientes")

    # Fósforo (mg/dm³ — Mehlich-1)
    if fosforo > 0:
        if   fosforo < 6:   score -= 20; alertas.append("Fósforo muito baixo (<6 mg/dm³)")
        elif fosforo < 12:  score -= 12; alertas.append("Fósforo baixo (6-12 mg/dm³)")
        elif fosforo < 18:  score -= 6;  alertas.append("Fósforo médio — atenção")

    # Potássio (mg/dm³)
    if potassio > 0:
        if   potassio < 60:  score -= 20; alertas.append("Potássio muito baixo (<60 mg/dm³)")
        elif potassio < 100: score -= 12; alertas.append("Potássio baixo (60-100 mg/dm³)")
        elif potassio < 150: score -= 5;  alertas.append("Potássio médio — monitorar")

    # Cálcio (cmolc/dm³)
    if calcio > 0:
        if   calcio < 2.0: score -= 20; alertas.append("Cálcio muito baixo (<2 cmolc/dm³)")
        elif calcio < 3.5: score -= 10; alertas.append("Cálcio baixo (2-3,5 cmolc/dm³)")

    # Magnésio (cmolc/dm³)
    if magnesio > 0:
        if   magnesio < 0.5: score -= 15; alertas.append("Magnésio muito baixo (<0,5 cmolc/dm³)")
        elif magnesio < 1.0: score -= 8;  alertas.append("Magnésio baixo (0,5-1,0 cmolc/dm³)")

    # Relação Ca:Mg ideal 3:1 a 5:1
    if calcio > 0 and magnesio > 0:
        rel = calcio / magnesio
        if rel < 2.5: alertas.append(f"Relação Ca:Mg baixa ({rel:.1f}:1) — risco de toxidez Mg")
        elif rel > 8:  alertas.append(f"Relação Ca:Mg alta ({rel:.1f}:1) — deficiência Mg possível")

    # Alumínio (cmolc/dm³) — tóxico acima de 0,3
    if aluminio > 0:
        if aluminio > 1.0: score -= 25; alertas.append(f"Alumínio tóxico ({aluminio} cmolc/dm³) — urgente calcário")
        elif aluminio > 0.5: score -= 15; alertas.append(f"Alumínio elevado ({aluminio} cmolc/dm³)")
        elif aluminio > 0.3: score -= 8;  alertas.append(f"Alumínio detectado ({aluminio} cmolc/dm³)")

    # Matéria orgânica (%)
    if materia_organica > 0:
        if   materia_organica < 1.5: score -= 15; alertas.append("MO muito baixa (<1,5%) — solo degradado")
        elif materia_organica < 2.5: score -= 8;  alertas.append("MO baixa (1,5-2,5%) — adubação verde recomendada")
        elif materia_organica > 6.0: alertas.append("MO alta — reduzir N mineral")

    # Micronutrientes (quando disponíveis)
    if enxofre > 0 and enxofre < 5:
        score -= 8; alertas.append(f"Enxofre baixo (<5 mg/dm³) — usar fertilizante com S")
    if zinco > 0 and zinco < 0.6:
        score -= 5; alertas.append(f"Zinco baixo (<0,6 mg/dm³)")
    if boro > 0 and boro < 0.2:
        score -= 5; alertas.append(f"Boro baixo (<0,2 mg/dm³) — importante para soja/café")

    score = max(0, min(100, score))
    if   score >= 85: classe = "Excelente"
    elif score >= 70: classe = "Boa"
    elif score >= 50: classe = "Média"
    elif score >= 30: classe = "Fraca"
    else:             classe = "Crítica"
    return score, classe, alertas


def baixar_estoque(nome_insumo, quantidade_usada, unidade_usada="L/ha"):
    """
    Dá baixa no estoque convertendo unidades automaticamente.
    Estoque sempre em L ou kg. Aplicação pode ser mL/ha, g/ha, etc.
    """
    def converter_para_base(qtd, unid):
        """Converte para a unidade base: L ou kg."""
        unid = (unid or "").lower().replace(" ", "")
        if "ml" in unid:     return qtd / 1000  # mL → L
        if "g/ha" in unid or unid == "g":   return qtd / 1000  # g → kg
        if "mg" in unid:     return qtd / 1_000_000
        return qtd  # já em L ou kg

    qtd_convertida = converter_para_base(quantidade_usada, unidade_usada)

    for item in st.session_state.estoque:
        if item["Insumo"] == nome_insumo:
            estoque_atual = float(item.get("Quantidade", 0))
            if estoque_atual >= qtd_convertida:
                item["Quantidade"] = round(estoque_atual - qtd_convertida, 4)
                item["Valor Total R$"] = item["Quantidade"] * item.get("Valor Unitário R$", 0)
                return True, f"Baixa de {qtd_convertida:.3f} realizada."
            return False, f"Estoque insuficiente: tem {estoque_atual:.3f}, precisa {qtd_convertida:.3f}"
    return False, "Insumo não encontrado no estoque."


# ─────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────
menu = st.sidebar.radio(
    "📋 Menu",
    [
        "🏠 Início",
        "🌾 Lavoura",
        "🧪 Solo & Adubação",
        "💰 Financeiro",
        "📦 Operacional",
        "🌍 Inteligência",
        "🌱 Safrinha",
        "📄 Relatório Final",
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
# MAPEAMENTO GLOBAL DE CULTURAS POR SEGMENTO
# (definição completa no topo do arquivo — aqui apenas mapas derivados)
# ─────────────────────────────────────────────

# Mapa reverso para extrair nome sem ícone (para lógicas internas)
CULTURA_NOME_LIMPO = {c: c.split(" ",1)[1] if " " in c else c
                      for seg in CULTURAS_POR_SEGMENTO.values() for c in seg}

# Ícone por nome limpo da cultura
CULTURA_ICONE = {c.split(" ",1)[1] if " " in c else c: c.split(" ",1)[0] if " " in c else "🌱"
                 for seg in CULTURAS_POR_SEGMENTO.values() for c in seg}

def get_icone_cultura(cultura):
    """Retorna o ícone da cultura (com ou sem ícone no nome)."""
    if not cultura: return "🌱"
    nome = cultura_limpa(cultura)
    return CULTURA_ICONE.get(nome, "🌱")

# ─────────────────────────────────────────────
# CONTROLE DE PLANOS — Free / Pro / Premium
# ─────────────────────────────────────────────

def verificar_limite(recurso: str) -> tuple:
    """Retorna (pode: bool, usado: int, limite: int)"""
    plano_key = st.session_state.get("sb_plano", "free")
    plano     = PLANOS.get(plano_key, PLANOS["free"])
    limite    = plano.get(recurso, 2)

    if limite == -1:
        return True, 0, -1  # ilimitado

    if recurso == "areas":
        usado = len(st.session_state.get("areas", []))
    elif recurso == "estoque":
        usado = len(st.session_state.get("estoque", []))
    else:
        return True, 0, -1

    return usado < limite, usado, limite

def bloco_upgrade(recurso: str, usado: int, limite: int):
    """Banner de upgrade quando limite é atingido."""
    plano_key = st.session_state.get("sb_plano", "free")
    nomes     = {"areas": "áreas", "estoque": "itens de estoque"}
    nome      = nomes.get(recurso, recurso)

    # Próximo plano sugerido
    if plano_key == "free":
        prox_key   = "pro"
        prox_preco = PLANOS["pro"]["preco"]
        prox_nome  = PLANOS["pro"]["nome"]
    else:
        prox_key   = "premium"
        prox_preco = PLANOS["premium"]["preco"]
        prox_nome  = PLANOS["premium"]["nome"]

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#78350f,#92400e);
    border-radius:12px;padding:18px 20px;border:2px solid #f59e0b;
    margin:10px 0;text-align:center;'>
    <b style='color:#fbbf24;font-size:16px;'>🔒 Limite atingido — {usado}/{limite} {nome}</b><br>
    <span style='color:#fde68a;font-size:13px;'>
    Faça upgrade para continuar usando o IAAGRO sem limites!
    </span><br><br>
    <span style='color:#fff;font-size:18px;font-weight:800;'>
    {prox_nome} — R$ {prox_preco:.2f}/mês
    </span>
    </div>
    """, unsafe_allow_html=True)

    msg = f"Quero+assinar+o+IAAGRO+{prox_nome.replace(' ','+')}+-+R$+{prox_preco:.2f}/mes"
    # Links direto do Mercado Pago — mensal e anual
    if prox_key == "premium":
        link_mes = MP_LINK_PREMIUM_MES
        link_ano = MP_LINK_PREMIUM_ANO
        preco_ano = 149.90 * 12 * 0.85  # 15% desconto anual
    else:
        link_mes = MP_LINK_PRO_MES
        link_ano = MP_LINK_PRO_ANO
        preco_ano = 59.90 * 12 * 0.85

    st.markdown(f"""
    <div style='display:flex;gap:10px;margin-top:8px;'>
    <a href='{link_mes}' target='_blank'
       style='flex:1;display:block;background:#009ee3;color:#fff;text-align:center;
       padding:10px;border-radius:8px;font-weight:700;text-decoration:none;font-size:13px;'>
    💳 Mensal<br>R$ {prox_preco:.2f}/mês
    </a>
    <a href='{link_ano}' target='_blank'
       style='flex:1;display:block;background:#00a650;color:#fff;text-align:center;
       padding:10px;border-radius:8px;font-weight:700;text-decoration:none;font-size:13px;'>
    🏆 Anual<br>R$ {preco_ano:.0f}/ano<br><span style='font-size:10px;'>(-15% desconto)</span>
    </a>
    </div>
    <div style='text-align:center;margin-top:4px;'>
    <span style='color:#94a3b8;font-size:11px;'>PIX • Cartão • Boleto — Mercado Pago</span>
    </div>
    """, unsafe_allow_html=True)

def get_culturas():
    """Retorna lista de culturas (com ícone) filtrada pelo segmento ativo."""
    seg = st.session_state.get("segmento")
    if seg and seg in CULTURAS_POR_SEGMENTO:
        return CULTURAS_POR_SEGMENTO[seg]
    todas = []
    seen = set()
    for culturas in CULTURAS_POR_SEGMENTO.values():
        for c in culturas:
            if c not in seen:
                todas.append(c)
                seen.add(c)
    return todas

def cultura_limpa(c):
    """Remove ícone do nome da cultura para usar nas lógicas internas."""
    if c and " " in c and len(c.split(" ",1)[0]) <= 2:
        return c.split(" ",1)[1]
    return c

# ─────────────────────────────────────────────
# MENU: INÍCIO
# ─────────────────────────────────────────────
if menu == "🏠 Início":

    # ── Segmentos disponíveis ──────────────────────────────────────────
    SEGMENTOS = SEGMENTOS_INFO

    # ── Tela de seleção (só aparece se segmento não foi escolhido ainda) ──
    if not st.session_state.segmento:
        st.markdown("""
        <div style='text-align:center;padding:30px 0 10px 0;'>
        <span style='font-size:48px;'>🌱</span><br>
        <span style='font-size:28px;font-weight:800;color:#22c55e;'>Bem-vindo ao IAAGRO</span><br>
        <span style='font-size:16px;color:#94a3b8;'>Selecione seu segmento para personalizar o sistema</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        for seg, info in SEGMENTOS.items():
            col_btn, col_desc = st.columns([2, 5])
            with col_btn:
                if st.button(seg, key=f"seg_btn_{seg}", use_container_width=True):
                    st.session_state.segmento = seg
                    salvar_dados_iaagro()
                    st.success(f"✅ Segmento **{seg}** selecionado! Bem-vindo.")
                    st.rerun()
            with col_desc:
                st.markdown(
                    f"<div style='padding:10px 0;color:#94a3b8;font-size:14px;'>{info['desc']}</div>",
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("⚙️ Você pode trocar o segmento a qualquer momento em Configurações.")

    else:
        # ── Dashboard principal após segmento selecionado ─────────────
        seg_info = SEGMENTOS.get(st.session_state.segmento, {"cor":"#0f3460","borda":"#22c55e","desc":""})

        col_banner, col_trocar = st.columns([5, 1])
        with col_banner:
            st.markdown(f"""
            <div style='background:{seg_info["cor"]};border-radius:12px;padding:14px 20px;
            border-left:5px solid {seg_info["borda"]};margin-bottom:8px;'>
            <span style='font-size:22px;font-weight:800;color:#f1f5f9;'>🚜 IAAGRO — {st.session_state.segmento}</span><br>
            <span style='font-size:13px;color:#94a3b8;'>{seg_info["desc"]}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_trocar:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("🔄 Trocar\nsegmento", key="btn_trocar_segmento", use_container_width=True):
                st.session_state.segmento = None
                salvar_dados_iaagro()
                st.rerun()

        # Card do plano atual
        _plano_key  = st.session_state.get("sb_plano", "free")
        _plano_info = PLANOS.get(_plano_key, PLANOS["free"])
        _areas_us   = len(st.session_state.get("areas", []))
        _est_us     = len(st.session_state.get("estoque", []))
        _lim_ar     = _plano_info["areas"]
        _lim_est    = _plano_info["estoque"]
        _bar_ar     = f"{_areas_us}/{_lim_ar}" if _lim_ar != -1 else f"{_areas_us}/∞"
        _bar_est    = f"{_est_us}/{_lim_est}"  if _lim_est != -1 else f"{_est_us}/∞"

        st.markdown(f"""
        <div style='background:linear-gradient(135deg,{_plano_info["cor"]},{_plano_info["cor"]}cc);
        border-radius:12px;padding:12px 18px;border:1px solid {_plano_info["borda"]};margin-bottom:12px;'>
        <span style='color:{_plano_info["borda"]};font-weight:800;font-size:15px;'>{_plano_info["nome"]}</span>
        <span style='color:#94a3b8;font-size:12px;float:right;'>
        📍 {_bar_ar} áreas &nbsp;|&nbsp; 📦 {_bar_est} insumos
        </span><br>
        {"<span style='color:#d1fae5;font-size:12px;'>✅ Acesso completo ativo</span>" if _plano_key == "premium" else
         f"<span style='color:#fde68a;font-size:12px;'>Upgrade para mais recursos — <b>R$ {PLANOS['pro' if _plano_key=='free' else 'premium']['preco']:.2f}/mês</b></span>"}
        </div>
        """, unsafe_allow_html=True)

        if _plano_key != "premium":
            _prox      = PLANOS["pro"] if _plano_key == "free" else PLANOS["premium"]
            _lmes = MP_LINK_PRO_MES if _plano_key == "free" else MP_LINK_PREMIUM_MES
            _lano = MP_LINK_PRO_ANO if _plano_key == "free" else MP_LINK_PREMIUM_ANO
            _pano = _prox['preco'] * 12 * 0.85
            st.markdown(f"""
            <div style='display:flex;gap:8px;'>
            <a href='{_lmes}' target='_blank'
            style='flex:1;display:block;background:#009ee3;color:#fff;text-align:center;
            padding:8px;border-radius:8px;font-weight:700;text-decoration:none;font-size:12px;'>
            💳 Mensal R$ {_prox['preco']:.2f}
            </a>
            <a href='{_lano}' target='_blank'
            style='flex:1;display:block;background:#00a650;color:#fff;text-align:center;
            padding:8px;border-radius:8px;font-weight:700;text-decoration:none;font-size:12px;'>
            🏆 Anual R$ {_pano:.0f}
            </a>
            </div>
            """, unsafe_allow_html=True)

        total_areas      = len(st.session_state.areas)
        total_estoque    = len(st.session_state.estoque)
        total_aplicacoes = len(st.session_state.aplicacoes)
        area_total       = sum(a.get("Hectares", 0) for a in st.session_state.areas)
        produtividade_media = (
            sum(a.get("Meta Produtividade", 0) for a in st.session_state.areas) / total_areas
            if total_areas > 0 else 0
        )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🌾 Áreas",      total_areas)
        col2.metric("📦 Estoque",    total_estoque)
        col3.metric("🚜 Aplicações", total_aplicacoes)
        col4.metric("📍 Área Total", f"{area_total:.1f} ha")

        st.divider()

        col5, col6 = st.columns(2)
        with col5:
            st.subheader("📈 Produtividade Média")
            st.metric("Média", f"{produtividade_media:.1f} sc/ha")
        with col6:
            st.subheader("⚠️ Alertas de Estoque")
            estoque_baixo = [i for i in st.session_state.estoque if i.get("Quantidade", 0) < 10]
            if not estoque_baixo:
                st.markdown('<div style="background:#166534;color:#fff;padding:12px 18px;border-radius:10px;font-weight:700;">✅ Nenhum alerta de estoque.</div>', unsafe_allow_html=True)
            else:
                for item in estoque_baixo:
                    nome = item.get("Insumo", item.get("Produto", "Produto"))
                    st.markdown(f'<div style="background:#92400e;color:#fff;padding:10px 16px;border-radius:10px;font-weight:700;margin-bottom:4px;">⚠️ {nome} com estoque baixo.</div>', unsafe_allow_html=True)

        st.divider()
        st.subheader("📋 Resumo das Áreas")
        if total_areas == 0:
            st.markdown('<div style="background:#1e3a5f;color:#fff;padding:14px 18px;border-radius:10px;font-weight:600;">ℹ️ Nenhuma área cadastrada. Vá em <b>Cadastro da Área</b> para começar.</div>', unsafe_allow_html=True)
        else:
            tabela_dashboard = [{
                "Fazenda":    a.get("Fazenda",""),
                "Talhão":     a.get("Talhão",""),
                "Cultura":    a.get("Cultura",""),
                "Área ha":    a.get("Hectares",0),
                "Meta sc/ha": a.get("Meta Produtividade",0),
            } for a in st.session_state.areas]
            df_areas = pd.DataFrame(tabela_dashboard)
            st.dataframe(df_areas, use_container_width=True)
            st.divider()
            st.subheader("📊 Produtividade por Talhão")
            st.bar_chart(df_areas.set_index("Talhão")["Meta sc/ha"])

        if total_estoque > 0:
            df_estoque = pd.DataFrame(st.session_state.estoque)
            if "Insumo" in df_estoque.columns and "Quantidade" in df_estoque.columns:
                st.divider()
                st.subheader("📦 Estoque por Produto")
                st.bar_chart(df_estoque.set_index("Insumo")["Quantidade"])


# ─────────────────────────────────────────────
# MENU: ÁREAS CADASTRADAS
# ─────────────────────────────────────────────
elif menu == "🌾 Lavoura":
    _sub_lav = st.tabs(["➕ Cadastro da Área","📍 Áreas Cadastradas","🗺️ Mapa de Fertilidade","🌧️ Pluviômetro","📈 Histórico de Produtividade"])

if menu == "🌾 Lavoura":
  with _sub_lav[1]:
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
        escolha = st.selectbox("Selecionar área para trabalhar", opcoes, key="sel_selecionar__rea_2910")

        if st.button("Carregar Área Selecionada"):
            indice = opcoes.index(escolha)
            area   = st.session_state.areas[indice]
            st.session_state.id_area          = area["ID"]
            st.session_state.area_selecionada = area["ID"]
            # Carrega dados completos da área (inclui análise de solo)
            _dados_area = area.get("Dados", area.get("dados", {}))
            st.session_state.dados = _dados_area.copy() if _dados_area else {}
            if "id_area" not in st.session_state.dados:
                st.session_state.dados["id_area"] = area["ID"]
            # Garante que campos da área estejam nos dados
            st.session_state.dados.update({
                "cultura":       area.get("Cultura", st.session_state.dados.get("cultura","Soja")),
                "area":          area.get("Hectares", st.session_state.dados.get("area",0)),
                "produtividade": area.get("Produtividade", st.session_state.dados.get("produtividade",50)),
                "fazenda":       area.get("Fazenda", st.session_state.dados.get("fazenda","")),
                "talhao":        area.get("Talhão", st.session_state.dados.get("talhao","")),
            })
            st.session_state.aplicacoes = area.get("Aplicacoes", []).copy()
            st.session_state.estoque    = area.get("Estoque", []).copy()
            salvar_dados_iaagro()
            success_box(f"✅ Área {area['ID']} carregada! {('Análise de solo disponível ✅' if 'ph' in st.session_state.dados else 'Sem análise de solo ainda.')}")
            st.rerun()

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
if menu == "🌾 Lavoura":
  with _sub_lav[0]:
    st.header("Cadastro da Área")

    fazenda   = st.text_input("Nome da fazenda",  st.session_state.dados.get("fazenda", ""), key="txt_nome_da_fazenda_2960")
    talhao    = st.text_input("Nome do talhão",   st.session_state.dados.get("talhao", ""), key="txt_nome_do_talh_o_2961")
    matricula = st.text_input("Matrícula da Área", st.session_state.dados.get("matricula", ""), key="txt_matr_cula_da__r_2962")
    cidade    = st.text_input("Cidade / Estado",   st.session_state.dados.get("cidade", ""), key="txt_cidade___estado_2963")
    area      = st.number_input("Área do talhão em hectares", min_value=0.0,
                                value=float(st.session_state.dados.get("area", 10.0)))

    culturas_disponiveis = get_culturas()
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

    # ── Geolocalização com tratamento robusto ────────────────────────
    # Inicializa com coordenadas salvas ou padrão Brasil-Sul
    latitude  = st.session_state.dados.get("latitude",  -26.88)
    longitude = st.session_state.dados.get("longitude", -52.40)

    col_geo_a, col_geo_b = st.columns([2, 1])
    with col_geo_a:
        latitude  = st.number_input("📍 Latitude",  value=float(latitude),
                                     format="%.6f", key="cad_lat")
        longitude = st.number_input("📍 Longitude", value=float(longitude),
                                     format="%.6f", key="cad_lon")
    with col_geo_b:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📡 Usar GPS do celular", key="btn_gps_cad", use_container_width=True):
            try:
                geo = get_geolocation()
                if geo and geo.get("coords"):
                    st.session_state["_gps_lat"] = geo["coords"]["latitude"]
                    st.session_state["_gps_lon"] = geo["coords"]["longitude"]
                    st.rerun()
            except Exception:
                warning_box("GPS indisponível. Insira as coordenadas manualmente.")
        if st.session_state.get("_gps_lat"):
            latitude  = st.session_state["_gps_lat"]
            longitude = st.session_state["_gps_lon"]
            st.markdown(f'<div style="background:#14532d;color:#fff;padding:6px 10px;'
                        f'border-radius:8px;font-size:11px;font-weight:700;">'
                        f'✅ GPS: {latitude:.5f}, {longitude:.5f}</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="color:#94a3b8;font-size:11px;margin-top:4px;">'
                    'Dica: use Google Maps para obter as coordenadas da área.</div>',
                    unsafe_allow_html=True)

    pode, usado, limite = verificar_limite("areas")
    if not pode:
        bloco_upgrade("areas", usado, limite)
    elif st.button("Salvar Nova Área"):
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
if menu == "🌾 Lavoura":
  with _sub_lav[4]:
    st.header("📈 Histórico de Produtividade")

    if len(st.session_state.areas) == 0:
        warning_box("Cadastre uma área primeiro.")
    else:
        lista_areas        = [f"{a['ID']} - {a['Talhão']}" for a in st.session_state.areas]
        area_escolhida     = st.selectbox("Selecione a Área", lista_areas, key="sel_selecione_a__re_3106")
        safra              = st.text_input("Safra", placeholder="2024/2025", key="txt_safra_3107")

        # Cultura colhida — com ícones
        _culturas_hist = get_culturas()
        # Pega cultura da área selecionada como padrão
        _id_hist = area_escolhida.split(" - ")[0]
        _area_hist_obj = next((a for a in st.session_state.areas if a.get("ID") == _id_hist), None)
        _cult_padrao = _area_hist_obj.get("Cultura", _culturas_hist[0]) if _area_hist_obj else _culturas_hist[0]
        _idx_cult = _culturas_hist.index(_cult_padrao) if _cult_padrao in _culturas_hist else 0
        cultura_colhida = st.selectbox("Cultura colhida", _culturas_hist,
                                        index=_idx_cult, key="sel_cultura_hist")

        produtividade_real = st.number_input("Produtividade Real (sc/ha)", min_value=0.0, value=60.0, key="num_produtividade_r_3108")
        custo_total        = st.number_input("Custo Total por hectare (R$)", min_value=0.0, value=0.0, key="num_custo_total_por_3109")
        observacoes        = st.text_area("Observações da Safra", key="txa_observa__es_da__3110")

        if st.button("💾 Salvar Histórico", key="btn_salvar_hist", use_container_width=True):
            st.session_state.historico_produtividade.append({
                "Área": area_escolhida, "Safra": safra,
                "Cultura": cultura_colhida,
                "Produtividade": produtividade_real,
                "Custo": custo_total, "Observações": observacoes
            })
            salvar_dados_iaagro()
            success_box(f"Histórico salvo! {get_icone_cultura(cultura_colhida)} {cultura_limpa(cultura_colhida)} — {produtividade_real} sc/ha")
            st.rerun()

        if len(st.session_state.historico_produtividade) > 0:
            df_hist = pd.DataFrame(st.session_state.historico_produtividade)
            if "Cultura" not in df_hist.columns:
                df_hist["Cultura"] = "—"

            # ── Botão atualizar registro ──────────────────
            st.divider()
            st.subheader("✏️ Atualizar Registro")
            _opcoes_hist = [
                f"{i+1}. {r.get('Área','')} | {r.get('Safra','')} | {cultura_limpa(r.get('Cultura',''))} | {r.get('Produtividade',0)} sc/ha"
                for i, r in enumerate(st.session_state.historico_produtividade)
            ]
            _sel_hist = st.selectbox("Selecione o registro para editar", _opcoes_hist, key="sel_hist_editar")
            _idx_edit = _opcoes_hist.index(_sel_hist)
            _reg_edit = st.session_state.historico_produtividade[_idx_edit]

            col_e1, col_e2, col_e3 = st.columns(3)
            with col_e1:
                _safra_e  = st.text_input("Safra", value=_reg_edit.get("Safra",""), key="txt_hist_safra_edit")
                _cult_e_list = get_culturas()
                _cult_e_val  = _reg_edit.get("Cultura", _cult_e_list[0])
                _cult_e_idx  = _cult_e_list.index(_cult_e_val) if _cult_e_val in _cult_e_list else 0
                _cult_e   = st.selectbox("Cultura", _cult_e_list, index=_cult_e_idx, key="sel_hist_cult_edit")
            with col_e2:
                _prod_e   = st.number_input("Produtividade (sc/ha)", min_value=0.0,
                                             value=float(_reg_edit.get("Produtividade",0)), key="num_hist_prod_edit")
                _custo_e  = st.number_input("Custo (R$/ha)", min_value=0.0,
                                             value=float(_reg_edit.get("Custo",0)), key="num_hist_custo_edit")
            with col_e3:
                _obs_e    = st.text_area("Observações", value=_reg_edit.get("Observações",""),
                                          key="txt_hist_obs_edit", height=100)

            col_btn1, col_btn2 = st.columns(2)
            if col_btn1.button("💾 Atualizar Registro", key="btn_hist_atualizar", use_container_width=True):
                st.session_state.historico_produtividade[_idx_edit] = {
                    "Área":          _reg_edit.get("Área",""),
                    "Safra":         _safra_e,
                    "Cultura":       _cult_e,
                    "Produtividade": _prod_e,
                    "Custo":         _custo_e,
                    "Observações":   _obs_e,
                }
                salvar_dados_iaagro()
                success_box("✅ Registro atualizado!")
                st.rerun()

            if col_btn2.button("🗑️ Excluir Registro", key="btn_hist_excluir", use_container_width=True):
                st.session_state.historico_produtividade.pop(_idx_edit)
                salvar_dados_iaagro()
                success_box("Registro excluído!")
                st.rerun()

            # ── Tabela e gráfico ──────────────────────────
            st.divider()
            st.subheader("📋 Todos os Registros")
            st.dataframe(df_hist, use_container_width=True)
            st.subheader("📊 Evolução Produtiva")
            area_filtro = st.selectbox("Filtrar gráfico por área", df_hist["Área"].unique(), key="sel_filtrar_gr_fico_3125")
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
if menu == "🌾 Lavoura":
  with _sub_lav[3]:
    st.header("🌧️ Pluviômetro Inteligente")

    if len(st.session_state.areas) == 0:
        warning_box("Cadastre uma área primeiro.")
    else:
        lista_areas   = [f"{a['ID']} - {a['Talhão']}" for a in st.session_state.areas]
        area_chuva    = st.selectbox("Selecione a Área", lista_areas, key="sel_area_chuva_pluvio")
        id_area_chuva = area_chuva.split(" - ")[0]
        area_obj      = next((a for a in st.session_state.areas if a["ID"] == id_area_chuva), {})
        cultura_chuva = area_obj.get("Cultura", "Soja")

        chuva_ideal_padrao = {
            "Soja":120.0,"Milho":140.0,"Trigo":90.0,"Feijão":100.0,"Canola":90.0,
            "Aveia":80.0,"Cana-de-açúcar":180.0,"Arroz":180.0,"Sorgo":90.0,
            "Girassol":90.0,"Cevada":80.0,"Pastagem":120.0,"Algodão":130.0,
            "Café":140.0,"Tabaco":110.0,"Mandioca":100.0,"Batata":100.0,
        }
        chuva_ideal_mes = chuva_ideal_padrao.get(cultura_limpa(cultura_chuva), 120.0)

        st.markdown(f"""
        <div style='background:#0f3460;color:#fff;padding:10px 16px;border-radius:8px;
        border:1px solid #3b82f6;margin-bottom:12px;'>
        🌱 <b>Cultura:</b> {cultura_chuva} &nbsp;|&nbsp;
        🌧️ <b>Chuva ideal/mês:</b> {chuva_ideal_mes} mm
        </div>
        """, unsafe_allow_html=True)

        # ── Registro diário ──────────────────────────────────
        st.subheader("➕ Registrar Chuva Diária")
        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            data_chuva = st.date_input("Data", value=datetime.now().date(), key="date_chuva_diaria")
        with col_d2:
            mm_dia = st.number_input("Precipitação (mm)", min_value=0.0, max_value=500.0,
                                      value=0.0, step=0.1, key="num_mm_dia",
                                      help="Leitura do pluviômetro de campo")
        with col_d3:
            obs_dia = st.text_input("Observação", placeholder="Ex: Chuva forte tarde",
                                     key="txt_obs_chuva")

        if st.button("💾 Registrar", key="btn_reg_chuva", use_container_width=True):
            if mm_dia > 0 or obs_dia:
                _reg = {
                    "area_id":  id_area_chuva,
                    "area":     area_chuva,
                    "data":     str(data_chuva),
                    "ano":      data_chuva.year,
                    "mes":      data_chuva.month,
                    "mes_nome": ["","Janeiro","Fevereiro","Março","Abril","Maio","Junho",
                                 "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"][data_chuva.month],
                    "mm":       round(mm_dia, 1),
                    "obs":      obs_dia,
                }
                st.session_state.pluviometro.append(_reg)
                salvar_dados_iaagro()
                success_box(f"✅ {mm_dia} mm registrado em {data_chuva.strftime('%d/%m/%Y')}")
            else:
                warning_box("Digite a quantidade de chuva.")

        # ── Filtro e acumulado mensal ─────────────────────────
        _regs = [r for r in st.session_state.pluviometro
                 if isinstance(r, dict) and r.get("area_id") == id_area_chuva]

        if _regs:
            import pandas as pd
            df_pluvio = pd.DataFrame(_regs)

            # Garante colunas necessárias
            for col in ["data","ano","mes","mes_nome","mm"]:
                if col not in df_pluvio.columns:
                    df_pluvio[col] = 0 if col in ["ano","mes","mm"] else ""

            df_pluvio["mm"] = pd.to_numeric(df_pluvio["mm"], errors="coerce").fillna(0)
            df_pluvio["data_dt"] = pd.to_datetime(df_pluvio["data"], errors="coerce")
            df_pluvio = df_pluvio.sort_values("data_dt", ascending=False)

            # ── Acumulado mensal automático ──────────────────
            st.subheader("📊 Acumulado Mensal")
            df_mensal = (df_pluvio.groupby(["ano","mes","mes_nome"])["mm"]
                         .sum().reset_index()
                         .sort_values(["ano","mes"]))
            df_mensal["ideal"] = chuva_ideal_mes
            df_mensal["%ideal"] = (df_mensal["mm"] / chuva_ideal_mes * 100).round(1)
            df_mensal["status"] = df_mensal["%ideal"].apply(
                lambda x: "✅ Adequado" if 70<=x<=130
                else ("⚠️ Déficit" if x < 70 else "⚠️ Excesso")
            )
            df_mensal["Período"] = df_mensal["mes_nome"].astype(str) + "/" + df_mensal["ano"].astype(str)

            # Cards dos últimos 3 meses
            _ultimos = df_mensal.tail(3).to_dict("records")
            cols_m = st.columns(len(_ultimos))
            for idx_m, row in enumerate(_ultimos):
                _cor = "#14532d" if "Adequado" in row["status"] else "#78350f"
                cols_m[idx_m].markdown(f"""
                <div style='background:{_cor};border-radius:10px;padding:12px;text-align:center;'>
                <b style='color:#fff;font-size:13px;'>{row['Período']}</b><br>
                <span style='color:#fff;font-size:22px;font-weight:800;'>{row['mm']:.1f} mm</span><br>
                <span style='color:#d1fae5;font-size:11px;'>{row['%ideal']}% do ideal</span><br>
                <span style='color:#fde68a;font-size:11px;'>{row['status']}</span>
                </div>
                """, unsafe_allow_html=True)

            # Gráfico acumulado mensal
            if len(df_mensal) > 0:
                st.markdown("**Chuva acumulada vs ideal por mês:**")
                _chart_data = df_mensal.set_index("Período")[["mm","ideal"]]
                _chart_data.columns = ["Chuva Real (mm)","Ideal (mm)"]
                st.bar_chart(_chart_data)

            # ── Registros diários ────────────────────────────
            st.subheader("📋 Registros Diários")

            # Filtro por mês/ano
            _anos  = sorted(df_pluvio["ano"].dropna().unique().tolist(), reverse=True)
            _meses_nomes = ["Todos","Janeiro","Fevereiro","Março","Abril","Maio","Junho",
                            "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
            col_f1, col_f2 = st.columns(2)
            _ano_sel = col_f1.selectbox("Filtrar ano", ["Todos"] + [str(int(a)) for a in _anos], key="sel_ano_pluvio")
            _mes_sel = col_f2.selectbox("Filtrar mês", _meses_nomes, key="sel_mes_pluvio")

            df_filtrado = df_pluvio.copy()
            if _ano_sel != "Todos":
                df_filtrado = df_filtrado[df_filtrado["ano"] == int(_ano_sel)]
            if _mes_sel != "Todos":
                _mes_num = _meses_nomes.index(_mes_sel)
                df_filtrado = df_filtrado[df_filtrado["mes"] == _mes_num]

            # Resumo do filtro
            _total_filtro = df_filtrado["mm"].sum()
            _dias_chuva   = (df_filtrado["mm"] > 0).sum()
            _media_dia    = df_filtrado[df_filtrado["mm"]>0]["mm"].mean() if _dias_chuva > 0 else 0

            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
            col_r1.metric("🌧️ Total", f"{_total_filtro:.1f} mm")
            col_r2.metric("📅 Dias c/ chuva", f"{_dias_chuva}")
            col_r3.metric("📊 Média/dia", f"{_media_dia:.1f} mm")
            col_r4.metric("🎯 % do ideal", f"{_total_filtro/chuva_ideal_mes*100:.0f}%" if _mes_sel != "Todos" else "-")

            # Tabela diária
            _cols_exib = ["data","mm","obs"] if "obs" in df_filtrado.columns else ["data","mm"]
            _df_show = df_filtrado[_cols_exib].copy()
            _df_show.columns = ["Data","mm","Obs"] if len(_cols_exib) == 3 else ["Data","mm"]
            st.dataframe(_df_show.head(60), use_container_width=True)

            # Excluir registro
            with st.expander("🗑️ Excluir registro"):
                _datas_disp = df_pluvio["data"].tolist()
                if _datas_disp:
                    _data_del = st.selectbox("Selecione a data para excluir",
                                              _datas_disp, key="sel_del_chuva")
                    if st.button("🗑️ Excluir", key="btn_del_chuva"):
                        st.session_state.pluviometro = [
                            r for r in st.session_state.pluviometro
                            if not (isinstance(r, dict) and
                                    r.get("data") == _data_del and
                                    r.get("area_id") == id_area_chuva)
                        ]
                        salvar_dados_iaagro()
                        success_box("Registro excluído!")
                        st.rerun()

            # ── Análise de risco ─────────────────────────────
            st.subheader("🤖 Análise de Risco Hídrico")
            _mensal_recente = df_mensal.tail(3)["mm"].tolist()
            _media_3m = sum(_mensal_recente)/len(_mensal_recente) if _mensal_recente else 0
            _desvio   = abs(_media_3m - chuva_ideal_mes) / chuva_ideal_mes * 100 if chuva_ideal_mes > 0 else 0

            # Estimativa de perda por déficit ou excesso (igual ao modelo anterior)
            if _media_3m < chuva_ideal_mes * 0.7:
                _perda_est = round((_chuva_ideal_mes - _media_3m) * 0.15, 1) if hasattr(locals(), '_chuva_ideal_mes') else round((chuva_ideal_mes - _media_3m) * 0.15, 1)
                _perda_est = round((chuva_ideal_mes - _media_3m) * 0.15, 1)
                _status_h  = "⚠️ Déficit hídrico"
                _risco     = "🔴 Alto risco hídrico — avaliar seguro agrícola"
                _rec       = f"Déficit médio de {chuva_ideal_mes - _media_3m:.0f} mm/mês. Perda estimada: {_perda_est}%. Reavaliar meta produtiva."
            elif _media_3m > chuva_ideal_mes * 1.3:
                _perda_est = round((_media_3m - chuva_ideal_mes) * 0.08, 1)
                _status_h  = "⚠️ Excesso de chuva"
                _risco     = "🟡 Risco por excesso hídrico"
                _rec       = f"Excesso médio de {_media_3m - chuva_ideal_mes:.0f} mm/mês. Perda estimada: {_perda_est}%. Monitorar doenças fúngicas e erosão."
            else:
                _perda_est = 0
                _status_h  = "✅ Chuva adequada"
                _risco     = "🟢 Condição hídrica adequada"
                _rec       = "Precipitação dentro da faixa ideal para a cultura."

            # Métricas de risco
            _col_r1, _col_r2, _col_r3 = st.columns(3)
            _col_r1.metric("🌧️ Média 3 meses", f"{_media_3m:.1f} mm")
            _col_r2.metric("🎯 Ideal/mês", f"{chuva_ideal_mes} mm")
            _col_r3.metric("📉 Perda estimada", f"{_perda_est}%",
                           help="Estimativa de impacto na produtividade por déficit ou excesso hídrico")

            info_box(_risco)
            st.caption(_rec)

            # Progresso do mês atual
            _hoje = datetime.now()
            _regs_mes_atual = [r for r in _regs
                               if isinstance(r, dict)
                               and r.get("mes") == _hoje.month
                               and r.get("ano") == _hoje.year]
            _total_mes_atual = sum(r.get("mm", 0) for r in _regs_mes_atual)
            _pct_mes = min(_total_mes_atual / chuva_ideal_mes, 1.0) if chuva_ideal_mes > 0 else 0

            st.subheader(f"📅 {['','Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'][_hoje.month]}/{_hoje.year} — Progresso")
            st.progress(_pct_mes)
            st.caption(f"{_total_mes_atual:.1f} mm acumulados de {chuva_ideal_mes} mm ideais ({_pct_mes*100:.0f}%)")

        else:
            st.info("📝 Nenhum registro de chuva para esta área ainda. Registre a primeira leitura acima!")




# ─────────────────────────────────────────────
# MENU: MAPA DE FERTILIDADE
# ─────────────────────────────────────────────
if menu == "🌾 Lavoura":
  with _sub_lav[2]:
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

            # ── Dados de calcário e gesso aplicados ──────
            _corr       = st.session_state.get("corretivos_aplicados", [])
            _calc_area  = [c for c in _corr if isinstance(c,dict) and c.get("area_id")==area.get("ID","") and c.get("tipo")=="calcario"]
            _gesso_area = [c for c in _corr if isinstance(c,dict) and c.get("area_id")==area.get("ID","") and c.get("tipo")=="gesso"]
            _calc_total  = round(sum(c.get("toneladas_ha",0) for c in _calc_area), 2)
            _gesso_total = round(sum(c.get("toneladas_ha",0) for c in _gesso_area), 2)

            # Usa pH pós-calagem no score se calcário foi aplicado
            _dados_score = dados_area.copy() if dados_area else {}
            _ph_orig     = _dados_score.get("ph", 0)
            _ph_corrigido = _dados_score.get("ph_pos_calagem", _ph_orig)

            # Se tem calcário mas ph_pos_calagem não foi calculado ainda, calcula agora
            if _calc_total > 0 and _ph_corrigido == _ph_orig and _ph_orig > 0:
                _elevacao_total = round((_calc_total * 0.75) * 0.3, 2)
                _ph_corrigido   = min(round(_ph_orig + _elevacao_total, 1), 7.0)
                _dados_score["ph_pos_calagem"] = _ph_corrigido

            # Usa pH corrigido no score visual
            if _calc_total > 0 and _ph_corrigido > _ph_orig:
                _dados_score["ph"] = _ph_corrigido  # score usa pH pós-calagem

            if _dados_score and "ph" in _dados_score:
                score, classe, alertas = score_solo(_dados_score)
            else:
                score = 0; classe = "Sem análise"; alertas = ["Sem análise de solo"]

            if   score >= 85: cor = "🟢 Verde"
            elif score >= 70: cor = "🟡 Amarelo"
            elif score >= 50: cor = "🟠 Laranja"
            else:             cor = "🔴 Vermelho"

            # Status calagem
            if dados_area and "ph" in dados_area:
                _dose_rec, _ = calcular_calcario_por_ph(dados_area.get("ph",5.5), area.get("Hectares",1))
                if _calc_total == 0:
                    _calc_status = "⚪ Não aplicado"
                elif _calc_total >= _dose_rec:
                    _calc_status = "✅ Meta atingida"
                elif _calc_total >= _dose_rec * 0.5:
                    _calc_status = "🟡 Parcial"
                else:
                    _calc_status = "🔴 Insuficiente"
                _calc_color = {"✅ Meta atingida":"#14532d","🟡 Parcial":"#78350f",
                               "🔴 Insuficiente":"#7f1d1d","⚪ Não aplicado":"#1e293b"}
                _calc_rec_txt = f"{_dose_rec} t/ha"
            else:
                _calc_status = "⚪ Sem análise"
                _calc_color  = {"⚪ Sem análise":"#1e293b"}
                _calc_rec_txt = "-"

            # ── Clima ────────────────────────────────────
            registros_area = [r for r in st.session_state.pluviometro
                              if isinstance(r, dict) and
                              (r.get("area_id") == area.get("ID","") or
                               r.get("Área") == area.get("ID",""))]
            if len(registros_area) > 0:
                if "Perda Estimada" in registros_area[0]:
                    perda_media_clima = sum(r.get("Perda Estimada", 0) for r in registros_area) / len(registros_area)
                else:
                    _ideal = 120.0
                    _meses = {}
                    for r in registros_area:
                        _k = f"{r.get('ano',0)}-{r.get('mes',0)}"
                        _meses[_k] = _meses.get(_k, 0) + r.get("mm", 0)
                    _perdas = []
                    for _mm in _meses.values():
                        if _mm < _ideal * 0.7:   _perdas.append((_ideal - _mm) * 0.15)
                        elif _mm > _ideal * 1.3: _perdas.append((_mm - _ideal) * 0.08)
                        else:                    _perdas.append(0)
                    perda_media_clima = sum(_perdas) / len(_perdas) if _perdas else 0
                if   perda_media_clima <= 5:  clima_cor = "🟢 Ideal"
                elif perda_media_clima <= 12: clima_cor = "🟡 Atenção"
                else:                         clima_cor = "🔴 Crítico"
            else:
                clima_cor = "⚪ Sem dados"

            mapa_dados.append({
                "ID":             area.get("ID",""),
                "Fazenda":        area.get("Fazenda",""),
                "Talhão":         area.get("Talhão",""),
                "Cultura":        area.get("Cultura",""),
                "Área ha":        area.get("Hectares",0),
                "Score":          score,
                "Classe":         classe,
                "Cor":            cor,
                "Clima":          clima_cor,
                "pH atual":       _ph_orig,
                "pH pós-calagem": _ph_corrigido,
                "Calcário t/ha":  _calc_total,
                "Rec. calcário":  _calc_rec_txt,
                "Status calagem": _calc_status,
                "Gesso t/ha":     _gesso_total,
                "Alertas":        ", ".join(alertas),
            })

        df_mapa = pd.DataFrame(mapa_dados)

        # ── Visão geral ──────────────────────────────────
        st.subheader("📍 Visão geral dos talhões")
        st.dataframe(df_mapa, use_container_width=True)

        # ── Cards visuais com calagem ─────────────────────
        st.subheader("🛰️ Mapa Visual dos Talhões")
        st.write("🟢 Verde = solo excelente | 🟡 Amarelo = bom | 🟠 Laranja = médio | 🔴 Vermelho = crítico")
        cols_card = st.columns(3)
        for i, linha in df_mapa.iterrows():
            cor_str = linha["Cor"]
            if "Verde"   in cor_str: fundo = "#16a34a"
            elif "Amarelo" in cor_str: fundo = "#eab308"
            elif "Laranja" in cor_str: fundo = "#f97316"
            else:                      fundo = "#dc2626"
            _cs = linha["Status calagem"]
            _cc_borda = {"✅ Meta atingida":"#22c55e","🟡 Parcial":"#eab308",
                         "🔴 Insuficiente":"#ef4444","⚪ Não aplicado":"#64748b",
                         "⚪ Sem análise":"#64748b"}.get(_cs,"#64748b")
            with cols_card[i % 3]:
                st.markdown(f"""
                <div style="background:{fundo};padding:16px;border-radius:14px;
                margin-bottom:14px;color:white;font-weight:bold;box-shadow:0 4px 12px rgba(0,0,0,0.25);">
                <h3 style="margin:0 0 6px 0;">{linha['Talhão']}</h3>
                <p style="margin:2px 0;">{get_icone_cultura(linha['Cultura'])} {cultura_limpa(linha['Cultura'])} | {linha['Área ha']} ha</p>
                <p style="margin:2px 0;">📊 Score: {linha['Score']} — {linha['Classe']}</p>
                <p style="margin:2px 0;">🌧️ Clima: {linha['Clima']}</p>
                <hr style="border-color:rgba(255,255,255,0.4);margin:8px 0;">
                <p style="margin:2px 0;border-left:3px solid {_cc_borda};padding-left:8px;">
                🪨 Calcário: <b>{linha['Calcário t/ha']} t/ha</b> aplicado (rec: {linha['Rec. calcário']})<br>
                {_cs}<br>
                🧱 Gesso: <b>{linha['Gesso t/ha']} t/ha</b><br>
                🧪 pH: {linha['pH atual']} → <b>{linha['pH pós-calagem']}</b> (pós-calagem)
                </p>
                <p style="margin:6px 0 0 0;font-size:11px;opacity:0.85;">{linha['Alertas']}</p>
                </div>""", unsafe_allow_html=True)

        # ── Heatmap fertilidade ──────────────────────────
        st.subheader("🌡️ Heatmap de Fertilidade")

        def cor_score(val):
            if val >= 70:   return "background-color: #14532d; color: white"
            elif val >= 40: return "background-color: #78350f; color: white"
            else:           return "background-color: #7f1d1d; color: white"

        def cor_calc(val):
            try:
                v = float(val)
                if v == 0:   return "background-color: #1e293b; color: #94a3b8"
                elif v >= 2: return "background-color: #14532d; color: white"
                elif v >= 1: return "background-color: #78350f; color: white"
                else:        return "background-color: #7f1d1d; color: white"
            except: return ""

        def cor_ph(val):
            try:
                v = float(val)
                if v >= 6.0: return "background-color: #14532d; color: white"
                elif v >= 5.5: return "background-color: #78350f; color: white"
                else:          return "background-color: #7f1d1d; color: white"
            except: return ""

        _heat_cols = ["Talhão","Score","pH atual","pH pós-calagem","Calcário t/ha","Gesso t/ha","Status calagem"]
        df_heat = df_mapa[[c for c in _heat_cols if c in df_mapa.columns]].copy()

        try:
            _styled = df_heat.style\
                .applymap(cor_score, subset=["Score"])\
                .applymap(cor_ph, subset=["pH atual","pH pós-calagem"])\
                .applymap(cor_calc, subset=["Calcário t/ha","Gesso t/ha"])
            st.dataframe(_styled, use_container_width=True)
        except Exception:
            st.dataframe(df_heat, use_container_width=True)

        st.caption("🟢 Verde = ótimo | 🟡 Laranja = atenção | 🔴 Vermelho = crítico | ⚫ Cinza = sem dados")

        # ── Ranking ──────────────────────────────────────
        st.subheader("📊 Ranking de Fertilidade")
        st.bar_chart(df_mapa.set_index("Talhão")["Score"])

        st.subheader("🛰️ Mapa GPS dos Talhões")

        # Coordenadas — prioridade: GPS salvo > área cadastrada > padrão
        latitude  = st.session_state.dados.get("latitude",  -26.88)
        longitude = st.session_state.dados.get("longitude", -52.40)

        col_mf1, col_mf2, col_mf3 = st.columns([2, 2, 1])
        with col_mf1:
            latitude  = st.number_input("Latitude",  value=float(latitude),
                                         format="%.6f", key="mapa_fert_lat")
        with col_mf2:
            longitude = st.number_input("Longitude", value=float(longitude),
                                         format="%.6f", key="mapa_fert_lon")
        with col_mf3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📡 GPS", key="btn_gps_mapa_fert", use_container_width=True,
                         help="Clique para usar localização do celular"):
                try:
                    geo = get_geolocation()
                    if geo and geo.get("coords"):
                        st.session_state["_gps_mf_lat"] = geo["coords"]["latitude"]
                        st.session_state["_gps_mf_lon"] = geo["coords"]["longitude"]
                        st.rerun()
                except Exception:
                    pass  # erro silenciado intencionalmente
        if st.session_state.get("_gps_mf_lat"):
            latitude  = st.session_state["_gps_mf_lat"]
            longitude = st.session_state["_gps_mf_lon"]
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
            draw_options={
                "polyline":     False,
                "rectangle":    True,
                "circle":       False,
                "marker":       False,
                "circlemarker": False,
                "polygon": {
                    "allowIntersection": True,
                    "showArea": True,
                    "metric": True,
                }
            },
            edit_options={"edit": True, "remove": True}
        ).add_to(mapa_folium)
        folium.Marker(location=[latitude, longitude], popup="Minha localização",
                      tooltip="Local atual", icon=folium.Icon(color="darkgreen", icon="leaf")
        ).add_to(mapa_folium)
        dados_mapa_folium = st_folium(mapa_folium, width=900, height=500)
        st.subheader("💾 Salvar Desenho do Talhão")

        st.info("💡 **Dica no celular:** Marque os pontos no sentido horário ao redor do talhão, sem cruzar as linhas. Use o botão **Delete last point** para desfazer o último ponto.")

        if dados_mapa_folium and dados_mapa_folium.get("last_active_drawing"):
            desenho = dados_mapa_folium["last_active_drawing"]
            coords  = desenho["geometry"]["coordinates"][0]

            # Corrige automaticamente polígonos com bordas cruzadas usando convex hull
            def convex_hull(points):
                pts = sorted(set(map(tuple, points)))
                if len(pts) <= 1: return pts
                def cross(O, A, B):
                    return (A[0]-O[0])*(B[1]-O[1]) - (A[1]-O[1])*(B[0]-O[0])
                lower = []
                for p in pts:
                    while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                        lower.pop()
                    lower.append(p)
                upper = []
                for p in reversed(pts):
                    while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                        upper.pop()
                    upper.append(p)
                return lower[:-1] + upper[:-1]

            def calcular_area_ha(coords):
                area_val = 0
                for i in range(len(coords) - 1):
                    x1, y1 = coords[i][0], coords[i][1]
                    x2, y2 = coords[i+1][0], coords[i+1][1]
                    area_val += (x1 * y2) - (x2 * y1)
                return abs(area_val) / 2 * 111139 * 111139 / 10000

            area_calculada = calcular_area_ha(coords)
            success_box(f"Área calculada automaticamente: {area_calculada:.2f} ha")

            # Seleção da área para vincular o desenho
            areas_disp = [f"{a.get('Fazenda','')} — {a.get('Talhão','')}" for a in st.session_state.areas]
            area_vincular = st.selectbox("Vincular desenho à área:", ["— Não vincular —"] + areas_disp, key="sel_area_croqui")

            if st.button("Salvar desenho no talhão", key="salvar_desenho_talhao"):
                pts_hull = convex_hull([[c[0], c[1]] for c in coords])
                if len(pts_hull) >= 3:
                    pts_hull.append(pts_hull[0])
                    desenho["geometry"]["coordinates"][0] = [[p[0], p[1]] for p in pts_hull]

                # Salva no session_state global
                st.session_state.dados["desenho_talhao"] = desenho

                # Salva também na área específica se selecionada
                if area_vincular != "— Não vincular —":
                    idx_area = areas_disp.index(area_vincular)
                    st.session_state.areas[idx_area]["desenho"] = desenho
                    st.session_state.areas[idx_area]["area_calculada_ha"] = round(area_calculada, 2)

                salvar_dados_iaagro()
                success_box("✅ Desenho do talhão salvo com sucesso!")


# ─────────────────────────────────────────────
# MENU: ANÁLISE DE SOLO
# ─────────────────────────────────────────────
elif menu == "🧪 Solo & Adubação":
    _sub_solo = st.tabs(["🧪 Análise de Solo","🔬 Diagnóstico Completo","🌱 Adubação","📄 OCR Laudo de Solo","📊 Evolução da Fertilidade"])

if menu == "🧪 Solo & Adubação":
  with _sub_solo[0]:
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
    uploaded_file = st.file_uploader("📄 Upload análise de solo", type=["xlsx","csv"], key="upl___upload_an_lis_3464")
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
            ph       = st.number_input("pH do solo (H₂O 1:1)", min_value=3.5, max_value=8.0, value=float(st.session_state.dados.get("ph", 5.5)), key="num_ph_do_solo_3478")
            fosforo  = st.number_input("Fósforo P (mg/dm³ Mehlich-1)", min_value=0.0, value=float(st.session_state.dados.get("fosforo", 10.0)), key="num_f_sforo_p_3479")
            potassio = st.number_input("Potássio K (mg/dm³ Mehlich-1)", min_value=0.0, value=float(st.session_state.dados.get("potassio", 100.0)), key="num_pot_ssio_k_3480")
        with col2:
            materia_organica = st.number_input("Matéria Orgânica MO (g/dm³)", min_value=0.0, value=float(st.session_state.dados.get("materia_organica", 2.5)), key="num_mat_ria_org_nic_3482", help="1% = 10 g/dm³")
            calcio   = st.number_input("Cálcio Ca²⁺ (cmolc/dm³)", min_value=0.0, value=float(st.session_state.dados.get("calcio", 3.0)), key="num_c_lcio_ca_3483")
            magnesio = st.number_input("Magnésio Mg²⁺ (cmolc/dm³)", min_value=0.0, value=float(st.session_state.dados.get("magnesio", 1.0)), key="num_magn_sio_mg_3484")
        with col3:
            aluminio = st.number_input("Alumínio Al³⁺ (cmolc/dm³)", min_value=0.0, value=float(st.session_state.dados.get("aluminio", 0.2)), key="num_alum_nio_al_3486")
            enxofre  = st.number_input("Enxofre S (mg/dm³)", min_value=0.0, value=float(st.session_state.dados.get("enxofre", 8.0)), key="num_enxofre_s_3487")
            ctc      = st.number_input("CTC pH7 (cmolc/dm³)", min_value=0.0, value=float(st.session_state.dados.get("ctc", 8.0)), key="num_ctc_3488", help="Capacidade de Troca Catiônica")

        # ── Cálculo automático de V% e SB ──────────────────
        sb_calc  = calcio + magnesio + (potassio / 391.0)  # K em cmolc
        ctc_val  = ctc if ctc > 0 else (sb_calc + aluminio + 2.0)
        v_calc   = round((sb_calc / ctc_val) * 100, 1) if ctc_val > 0 else 0.0
        m_calc   = round((aluminio / (sb_calc + aluminio)) * 100, 1) if (sb_calc + aluminio) > 0 else 0.0

        st.markdown(f"""
        <div style='background:#0f3460;border-radius:8px;padding:10px 16px;border:1px solid #3b82f6;margin:8px 0;'>
        <b style='color:#3b82f6;'>📊 Calculado automaticamente (CQFS RS/SC 2016)</b><br>
        <span style='color:#f1f5f9;font-size:13px;'>
        SB = Ca + Mg + K = <b>{sb_calc:.2f} cmolc/dm³</b> &nbsp;|&nbsp;
        <b>V% = {v_calc}%</b> {"🟢 Adequado" if v_calc >= 60 else "🟡 Médio" if v_calc >= 45 else "🔴 Baixo"} &nbsp;|&nbsp;
        <b>m% = {m_calc}%</b> {"🟢 OK" if m_calc < 20 else "🔴 Alto"} &nbsp;|&nbsp;
        Relação Ca/Mg = <b>{round(calcio/magnesio,1) if magnesio > 0 else '-'}</b>
        {"✅" if 2<=round(calcio/magnesio,1)<=5 else "⚠️"  if magnesio > 0 else ""}
        </span>
        </div>
        """, unsafe_allow_html=True)

        # ── V% manual (se vier do laudo) ──
        v_laudo = st.number_input("V% do laudo (deixe 0 para usar o calculado)", min_value=0.0, max_value=100.0,
                                   value=float(st.session_state.dados.get("v_percent", 0.0)), key="num_v_percent",
                                   help="Saturação por bases — use se o laudo já fornecer o valor")
        v_final = v_laudo if v_laudo > 0 else v_calc

        st.subheader("🔬 Micronutrientes (mg/dm³ Mehlich-1)")
        col4, col5, col6 = st.columns(3)
        with col4:
            boro  = st.number_input("Boro B", min_value=0.0, value=float(st.session_state.dados.get("boro", 0.3)), key="num_boro_b_3493")
            zinco = st.number_input("Zinco Zn", min_value=0.0, value=float(st.session_state.dados.get("zinco", 1.0)), key="num_zinco_zn_3494")
        with col5:
            manganes = st.number_input("Manganês Mn", min_value=0.0, value=float(st.session_state.dados.get("manganes", 5.0)), key="num_mangan_s_mn_3496")
            cobre    = st.number_input("Cobre Cu", min_value=0.0, value=float(st.session_state.dados.get("cobre", 0.5)), key="num_cobre_cu_3497")
        with col6:
            ferro    = st.number_input("Ferro Fe", min_value=0.0, value=float(st.session_state.dados.get("ferro", 30.0)), key="num_ferro_fe", help="Referência: >9 mg/dm³")
            molibdenio = st.number_input("Molibdênio Mo", min_value=0.0, value=float(st.session_state.dados.get("molibdenio", 0.1)), key="num_molibdenio", help="Referência: >0.1 mg/dm³")

        st.subheader("🪨 Análise Física do Solo")
        col7, col8, col9 = st.columns(3)
        with col7:
            argila   = st.number_input("Argila (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.dados.get("argila", 35.0)), key="num_argila___3499")
            silte    = st.number_input("Silte (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.dados.get("silte", 25.0)), key="num_silte")
        with col8:
            areia    = st.number_input("Areia total (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.dados.get("areia", 40.0)), key="num_areia")
            dens_solo= st.number_input("Densidade do solo (g/cm³)", min_value=0.5, max_value=2.0, value=float(st.session_state.dados.get("dens_solo", 1.2)), key="num_dens_solo", help="Referência: <1.3 g/cm³ para argilosos")
        with col9:
            dens_part= st.number_input("Densidade de partículas (g/cm³)", min_value=1.0, max_value=3.5, value=float(st.session_state.dados.get("dens_part", 2.65)), key="num_dens_part", help="Padrão: 2.65 g/cm³")
            umidade  = st.number_input("Umidade atual (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.dados.get("umidade", 0.0)), key="num_umidade")

        # Calcula porosidade e textura automaticamente
        _soma_granulo = argila + silte + areia
        _porosidade = round((1 - dens_solo/dens_part)*100, 1) if dens_part > 0 else 0
        if argila >= 60:    _textura = "Muito argiloso"
        elif argila >= 35:  _textura = "Argiloso"
        elif argila >= 25:  _textura = "Média argilosa"
        elif argila >= 15:  _textura = "Franco-argiloso"
        elif silte >= 50:   _textura = "Siltoso"
        elif areia >= 70:   _textura = "Arenoso"
        else:               _textura = "Franco"

        if _soma_granulo > 0:
            st.markdown(f"""
            <div style='background:#0f3460;border-radius:8px;padding:10px 16px;border:1px solid #22c55e;margin:8px 0;'>
            <b style='color:#22c55e;'>🪨 Física do Solo calculada</b><br>
            <span style='color:#f1f5f9;font-size:13px;'>
            Classe textural: <b>{_textura}</b> &nbsp;|&nbsp;
            Porosidade total: <b>{_porosidade}%</b>
            {"🟢 Boa" if _porosidade >= 50 else "🟡 Média" if _porosidade >= 40 else "🔴 Compactado"} &nbsp;|&nbsp;
            Soma granulométrica: <b>{_soma_granulo:.0f}%</b>
            {"✅" if 95<=_soma_granulo<=105 else "⚠️ Verificar soma"}
            </span>
            </div>
            """, unsafe_allow_html=True)

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
                    "boro": boro, "zinco": zinco, "manganes": manganes, "cobre": cobre,
                    "ferro": ferro, "molibdenio": molibdenio,
                    "argila": argila, "silte": silte, "areia": areia,
                    "dens_solo": dens_solo, "dens_part": dens_part, "umidade": umidade,
                    "v_percent": v_final, "saturacao_bases": round(sb_calc, 2),
                    "textura": _textura, "porosidade": _porosidade,
                    "saturacao_al": m_calc,
                })
                # Calcula score/nota/classe e salva nos dados E na área
                nota_s  = calcular_nota(st.session_state.dados)
                score_s, classe_s, _ = score_solo(st.session_state.dados)
                st.session_state.dados["nota_solo"]   = nota_s
                st.session_state.dados["score_solo"]  = score_s
                st.session_state.dados["classe_solo"] = classe_s

                # Salva na área ativa (com chaves padronizadas para Evolução da Fertilidade)
                id_area_atual = st.session_state.dados.get("id_area","")
                for i, _a in enumerate(st.session_state.areas):
                    if _a.get("ID") == id_area_atual:
                        st.session_state.areas[i]["Dados"]       = st.session_state.dados.copy()
                        st.session_state.areas[i]["dados"]       = st.session_state.dados.copy()
                        st.session_state.areas[i]["Nota Solo"]   = nota_s
                        st.session_state.areas[i]["score_solo"]  = score_s
                        st.session_state.areas[i]["classe_solo"] = classe_s
                        # Adiciona ao histórico de análises dentro da área (para Evolução)
                        import datetime as _dt_solo
                        _hist_entry = {
                            "data":             _dt_solo.date.today().isoformat(),
                            "ph":               ph, "fosforo": fosforo, "potassio": potassio,
                            "materia_organica": materia_organica, "calcio": calcio,
                            "magnesio":         magnesio, "aluminio": aluminio,
                            "ctc":              ctc, "nota": nota_s,
                            "score":            score_s, "classe": classe_s,
                        }
                        _hist_atual = st.session_state.areas[i].get("historico_solo", [])
                        _hist_atual.append(_hist_entry)
                        st.session_state.areas[i]["historico_solo"] = _hist_atual
                        break

                salvar_dados_iaagro()
                # Tenta salvar no SQLite local também (funciona localmente)
                if id_area_atual:
                    salvar_analise_solo_db(id_area_atual, st.session_state.dados, nota_s, score_s, classe_s)
                checar_alertas_estoque()
                success_box(f"✅ Análise salva! Score: {score_s}/100 — {classe_s}")

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
if menu == "🧪 Solo & Adubação":
  with _sub_solo[1]:
    st.header("Diagnóstico Completo")
    d = st.session_state.dados
    # Busca dados da área com análise se session_state.dados não tiver pH
    if "ph" not in d and st.session_state.areas:
        _id_s = st.session_state.get("area_selecionada")
        for _a in st.session_state.areas:
            _dad = _a.get("Dados", _a.get("dados", {}))
            if _dad and "ph" in _dad and (_id_s is None or _a.get("ID") == _id_s):
                d = {**_dad, "cultura": _a.get("Cultura","Soja"),
                     "area": _a.get("Hectares",0), "produtividade": _a.get("Produtividade",50)}
                break
        if "ph" not in d:  # pega qualquer área com análise
            for _a in st.session_state.areas:
                _dad = _a.get("Dados", _a.get("dados", {}))
                if _dad and "ph" in _dad:
                    d = {**_dad, "cultura": _a.get("Cultura","Soja"),
                         "area": _a.get("Hectares",0), "produtividade": _a.get("Produtividade",50)}
                    break

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
        _precos_data  = st.session_state.get("precos_data") or {}
        _soja_sc      = _precos_data.get("soja_sc") or {}
        preco_soja    = float(_soja_sc.get("preco", 115.0) or 115.0)
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

        cultura_diag = d.get("cultura", "Soja")
        score, classe_score, alertas_score = score_solo(d, cultura_diag)

        # Tabela completa com micronutrientes
        # Limites EMBRAPA/CQFS RS-SC 2016 por parâmetro
        def _classif_micro(valor, lim_baixo, lim_medio):
            if valor == 0: return "—"
            if   valor < lim_baixo:  return "🔴 Baixo"
            elif valor < lim_medio:  return "🟡 Médio"
            else:                    return "🟢 Adequado"

        tabela = pd.DataFrame({
            "Indicador": [
                "pH","Fósforo (mg/dm³)","Potássio (mg/dm³)",
                "Matéria Orgânica (%)","Cálcio (cmolc/dm³)","Magnésio (cmolc/dm³)",
                "Enxofre (mg/dm³)","Alumínio (cmolc/dm³)","CTC (cmolc/dm³)","Argila (%)",
                "Zinco Zn (mg/dm³)","Boro B (mg/dm³)","Manganês Mn (mg/dm³)","Cobre Cu (mg/dm³)"
            ],
            "Valor": [
                d.get("ph",0), d.get("fosforo",0), d.get("potassio",0),
                d.get("materia_organica",0), d.get("calcio",0), d.get("magnesio",0),
                d.get("enxofre",0), d.get("aluminio",0), d.get("ctc",0), d.get("argila",0),
                d.get("zinco",0), d.get("boro",0), d.get("manganes",0), d.get("cobre",0)
            ],
            "Classificação (EMBRAPA)": [
                "🔴 Baixo" if d.get("ph",0) < 5.5 else ("🟢 Adequado" if d.get("ph",0) <= 6.5 else "🟡 Alto"),
                _classif_micro(d.get("fosforo",0), 6, 18),
                _classif_micro(d.get("potassio",0), 60, 150),
                _classif_micro(d.get("materia_organica",0), 2.5, 4.5),
                _classif_micro(d.get("calcio",0), 2.0, 4.0),
                _classif_micro(d.get("magnesio",0), 0.5, 1.5),
                _classif_micro(d.get("enxofre",0), 5, 10),
                "🟢 OK" if d.get("aluminio",0) <= 0.3 else ("🟡 Atenção" if d.get("aluminio",0) <= 1.0 else "🔴 Tóxico"),
                _classif_micro(d.get("ctc",0), 5, 10),
                _classif_micro(d.get("argila",0), 15, 35),
                _classif_micro(d.get("zinco",0), 0.6, 1.5),
                _classif_micro(d.get("boro",0), 0.2, 0.6),
                _classif_micro(d.get("manganes",0), 1.2, 5.0),
                _classif_micro(d.get("cobre",0), 0.2, 0.8),
            ],
            "Referência EMBRAPA": [
                "5.8–6.5","6–30 (Mehlich-1)","60–200","2.5–4.5%","2–6","0.5–2",
                "5–15","<0.3 ideal","6–15","20–60%",
                "0.6–2.0","0.2–0.6","1.2–5.0","0.2–0.8"
            ]
        })
        st.dataframe(tabela, use_container_width=True)

        # Parecer específico de micronutrientes
        st.subheader("🔬 Parecer de Micronutrientes")
        micro_alertas = []
        zinco_v  = d.get("zinco",0)
        boro_v   = d.get("boro",0)
        mn_v     = d.get("manganes",0)
        cu_v     = d.get("cobre",0)
        enx_v    = d.get("enxofre",0)

        # Zinco — crítico para milho, soja
        if zinco_v > 0:
            if zinco_v < 0.6:
                micro_alertas.append(("🔴", "Zinco", f"{zinco_v} mg/dm³", "Deficiência crítica — aplicar 2-3 kg/ha ZnSO4 ou quelato", "Milho e soja muito sensíveis"))
            elif zinco_v < 1.0:
                micro_alertas.append(("🟡", "Zinco", f"{zinco_v} mg/dm³", "Nível médio — monitorar", "Foliar preventivo em culturas sensíveis"))

        # Boro — crítico para soja, café, algodão
        if boro_v > 0:
            if boro_v < 0.2:
                micro_alertas.append(("🔴", "Boro", f"{boro_v} mg/dm³", "Deficiência — aplicar 1-2 kg/ha B (ácido bórico ou ulexita)", "Soja: afeta enchimento de grãos"))
            elif boro_v < 0.4:
                micro_alertas.append(("🟡", "Boro", f"{boro_v} mg/dm³", "Nível baixo-médio — foliar recomendado no florescimento", "Soja, café e algodão"))

        # Manganês — importante pH>6.5 causa deficiência
        if mn_v > 0:
            if mn_v < 1.2:
                micro_alertas.append(("🔴", "Manganês", f"{mn_v} mg/dm³", "Deficiência — verificar pH (>6.5 indisponibiliza Mn)", "Soja mais sensível"))
            elif mn_v > 20:
                micro_alertas.append(("🟠", "Manganês", f"{mn_v} mg/dm³", "Nível elevado — pH baixo pode causar toxidez", "Elevar pH com calcário"))

        # Cobre
        if cu_v > 0 and cu_v < 0.2:
            micro_alertas.append(("🟡", "Cobre", f"{cu_v} mg/dm³", "Baixo — aplicar CuSO4 0.5-1 kg/ha ou foliar", "Solos orgânicos mais suscetíveis"))

        # Enxofre
        if enx_v > 0 and enx_v < 5:
            micro_alertas.append(("🔴", "Enxofre", f"{enx_v} mg/dm³", "Deficiência — usar gesso agrícola ou fertilizante com S", "Soja: 10-20 kg S/ha; Milho: 10-15 kg S/ha"))

        if micro_alertas:
            for icone, nut, val, rec, obs in micro_alertas:
                st.markdown(f"""
                <div style='background:#1e293b;border-radius:10px;padding:12px 16px;
                margin-bottom:8px;border-left:4px solid {"#ef4444" if icone=="🔴" else "#f59e0b"}'>
                <b style='color:#f1f5f9;'>{icone} {nut}: {val}</b><br>
                <span style='color:#22c55e;font-size:13px;'>💊 Recomendação: {rec}</span><br>
                <span style='color:#94a3b8;font-size:12px;'>📌 {obs}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Micronutrientes dentro dos limites adequados (EMBRAPA/CQFS RS-SC).")


# ─────────────────────────────────────────────
# MENU: ADUBAÇÃO
# ─────────────────────────────────────────────
if menu == "🧪 Solo & Adubação":
  with _sub_solo[2]:
    st.header("🌱 Adubação Inteligente")

    # Busca dados da área selecionada — prioridade: area ativa > primeira área
    d = st.session_state.dados
    _id_sel = st.session_state.get("area_selecionada")

    # Se dados não têm pH mas há áreas cadastradas, pega da área selecionada
    if "ph" not in d and st.session_state.areas:
        for _a in st.session_state.areas:
            if _id_sel and _a.get("ID") == _id_sel:
                _dados_area = _a.get("Dados", _a.get("dados", {}))
                if _dados_area and "ph" in _dados_area:
                    d = {**_dados_area,
                         "cultura": _a.get("Cultura", "Soja"),
                         "area":    _a.get("Hectares", 0),
                         "produtividade": _a.get("Produtividade", 50)}
                    break
        # Se ainda não tem, pega da primeira área com análise
        if "ph" not in d:
            for _a in st.session_state.areas:
                _dados_area = _a.get("Dados", _a.get("dados", {}))
                if _dados_area and "ph" in _dados_area:
                    d = {**_dados_area,
                         "cultura": _a.get("Cultura", "Soja"),
                         "area":    _a.get("Hectares", 0),
                         "produtividade": _a.get("Produtividade", 50)}
                    break

    # Seletor de área quando há múltiplas
    if st.session_state.areas:
        _areas_adub = [f"{a['ID']} — {a.get('Talhão','?')} ({a.get('Cultura','?')})"
                       for a in st.session_state.areas
                       if a.get("Dados") and "ph" in a.get("Dados", {})]
        _areas_sem = [a for a in st.session_state.areas
                      if not a.get("Dados") or "ph" not in a.get("Dados", {})]

        if _areas_sem and not _areas_adub:
            warning_box("Preencha a Análise de Solo para ver as recomendações de adubação.")
        elif _areas_adub:
            if len(_areas_adub) > 1:
                _sel_adub = st.selectbox("📍 Área para adubação", _areas_adub, key="sel_area_adubacao")
            else:
                _sel_adub = _areas_adub[0]
            _id_adub  = _sel_adub.split(" — ")[0]
            _a_obj    = next((a for a in st.session_state.areas if a.get("ID") == _id_adub), None)
            if _a_obj:
                _dad = _a_obj.get("Dados", {})
                if _dad:
                    d = {**_dad,
                         "cultura":       _a_obj.get("Cultura", d.get("cultura","Soja")),
                         "area":          _a_obj.get("Hectares", d.get("area",0)),
                         "produtividade": _a_obj.get("Produtividade", d.get("produtividade",50))}

    st.divider()
    st.subheader("🪨 Controle de Calcário e Gesso Aplicados")

    if not st.session_state.areas:
        warning_box("Cadastre uma área primeiro.")
    else:
        # Seletor explícito de área
        _lista_areas_corr = [f"{a['ID']} — {a.get('Talhão','?')} ({a.get('Fazenda','?')})"
                             for a in st.session_state.areas]
        _sel_area_corr = st.selectbox("📍 Área para corretivos",
                                       _lista_areas_corr, key="sel_area_corretivos")
        _id_area_atual = _sel_area_corr.split(" — ")[0]
        # Inicializa registro de corretivos
        if "corretivos_aplicados" not in st.session_state:
            st.session_state.corretivos_aplicados = []

        _corretivos = [c for c in st.session_state.corretivos_aplicados
                       if isinstance(c, dict) and c.get("area_id") == _id_area_atual]

        # ── Calcário aplicado ────────────────────────────
        st.markdown("#### 🪨 Calcário")
        col_ca1, col_ca2, col_ca3 = st.columns(3)
        with col_ca1:
            _data_calc = st.date_input("Data aplicação", key="date_calcario_aplic",
                                        value=datetime.now().date())
            _toneladas_calc = st.number_input("Quantidade aplicada (t/ha)", min_value=0.0,
                                               step=0.1, key="num_calc_aplic",
                                               help="Toneladas por hectare aplicadas")
        with col_ca2:
            _prnt_aplic = st.number_input("PRNT do produto (%)", min_value=0.0, max_value=100.0,
                                           value=75.0, step=1.0, key="num_prnt_aplic",
                                           help="Verificar na embalagem — padrão 75%")
            _tipo_calc = st.selectbox("Tipo de calcário",
                ["Calcário Dolomítico (Ca+Mg — ideal solos com Mg baixo)",
                 "Calcário Calcítico (só Ca — usar se Mg já adequado)",
                 "Calcário Magnesiano (predomina Mg)",
                 "Cal Virgem (CaO — ação rápida)",
                 "Cal Hidratada (Ca(OH)₂ — ação rápida)",
                 "Outro"], key="sel_tipo_calc",
                help="Dolomítico: >12% MgO | Calcítico: <12% MgO (CQFS RS/SC 2016)")

            # Mostra info sobre o tipo escolhido
            if "Dolomítico" in _tipo_calc:
                st.caption("🟢 **Dolomítico:** fornece Ca e Mg — recomendado quando Ca/Mg < 2:1 ou Mg < 0.5 cmolc/dm³")
            elif "Calcítico" in _tipo_calc:
                st.caption("🔵 **Calcítico:** fornece só Ca — usar quando Mg já está adequado (>1.0 cmolc/dm³)")
            elif "Magnesiano" in _tipo_calc:
                st.caption("🟡 **Magnesiano:** predomina Mg — usar em solos com Mg muito baixo")
        with col_ca3:
            _incorporado = st.checkbox("Incorporado ao solo", value=True, key="chk_incorporado",
                                        help="Incorporado com grade ou arado")
            _obs_calc = st.text_input("Observação", placeholder="Ex: Aplicado antes do plantio",
                                       key="txt_obs_calc")

        if st.button("💾 Registrar Calcário", key="btn_reg_calc", use_container_width=True):
            if _toneladas_calc <= 0:
                st.error(f"❌ Digite a quantidade em t/ha (valor atual: {_toneladas_calc})")
            elif not _id_area_atual:
                st.error("❌ Selecione uma área primeiro")
            else:
                _reg_calc = {
                    "area_id":      _id_area_atual,
                    "tipo":         "calcario",
                    "produto":      _tipo_calc,
                    "data":         str(_data_calc),
                    "toneladas_ha": round(_toneladas_calc, 2),
                    "prnt":         _prnt_aplic,
                    "incorporado":  _incorporado,
                    "obs":          _obs_calc,
                    "corrigido_em": datetime.now().isoformat(),
                }
                st.session_state.corretivos_aplicados.append(_reg_calc)
                # Atualiza dados DENTRO da área correta no array areas
                _ph_atual = 5.5
                for _area_obj in st.session_state.areas:
                    if _area_obj.get("ID") == _id_area_atual:
                        _dados_area = _area_obj.get("Dados", _area_obj.get("dados", {}))
                        _ph_atual   = _dados_area.get("ph", 5.5) if _dados_area else 5.5
                        break
                _elevacao = round((_toneladas_calc * _prnt_aplic / 100) * 0.3, 2)
                _ph_novo  = min(round(_ph_atual + _elevacao, 1), 7.0)
                # Persiste ph_pos_calagem e calcario_aplicado_ha dentro de cada área
                for _area_obj in st.session_state.areas:
                    if _area_obj.get("ID") == _id_area_atual:
                        if "Dados" not in _area_obj:
                            _area_obj["Dados"] = {}
                        _area_obj["Dados"]["ph_pos_calagem"]      = _ph_novo
                        _area_obj["Dados"]["calcario_aplicado_ha"] = round(
                            _area_obj["Dados"].get("calcario_aplicado_ha", 0) + _toneladas_calc, 2)
                        break
                # Atualiza também dados da área ativa se for a mesma
                if st.session_state.get("area_selecionada") == _id_area_atual:
                    st.session_state.dados["ph_pos_calagem"]      = _ph_novo
                    st.session_state.dados["calcario_aplicado_ha"] = round(
                        st.session_state.dados.get("calcario_aplicado_ha", 0) + _toneladas_calc, 2)
                salvar_dados_iaagro()
                success_box(f"✅ {_toneladas_calc} t/ha de {_tipo_calc} registrado! pH estimado pós-calagem: {_ph_novo}")
                st.rerun()
                warning_box("Informe a quantidade aplicada.")

        # ── Gesso aplicado ───────────────────────────────
        st.markdown("#### 🧱 Gesso Agrícola")
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            _data_gesso = st.date_input("Data aplicação", key="date_gesso_aplic",
                                         value=datetime.now().date())
            _ton_gesso  = st.number_input("Quantidade aplicada (t/ha)", min_value=0.0,
                                           step=0.1, key="num_gesso_aplic")
        with col_g2:
            _tipo_gesso = st.selectbox("Tipo de gesso",
                ["Gesso Agrícola","FCA (Fosfogesso)","Outro"], key="sel_tipo_gesso")
            _pureza_gesso = st.number_input("Pureza CaSO₄ (%)", min_value=0.0, max_value=100.0,
                                             value=85.0, step=1.0, key="num_pureza_gesso")
        with col_g3:
            _obs_gesso = st.text_input("Observação", placeholder="Ex: Para subsolagem",
                                        key="txt_obs_gesso")
            _prof_gesso = st.selectbox("Profundidade alvo",
                ["0-20 cm","20-40 cm","40-60 cm","Superficial"], key="sel_prof_gesso")

        if st.button("💾 Registrar Gesso", key="btn_reg_gesso", use_container_width=True):
            if _ton_gesso > 0:
                _reg_gesso = {
                    "area_id":      _id_area_atual,
                    "tipo":         "gesso",
                    "produto":      _tipo_gesso,
                    "data":         str(_data_gesso),
                    "toneladas_ha": round(_ton_gesso, 2),
                    "pureza":       _pureza_gesso,
                    "profundidade": _prof_gesso,
                    "obs":          _obs_gesso,
                    "corrigido_em": datetime.now().isoformat(),
                }
                st.session_state.corretivos_aplicados.append(_reg_gesso)
                # Atualiza gesso dentro da área correta
                for _area_obj in st.session_state.areas:
                    if _area_obj.get("ID") == _id_area_atual:
                        if "Dados" not in _area_obj:
                            _area_obj["Dados"] = {}
                        _area_obj["Dados"]["gesso_aplicado_ha"] = round(
                            _area_obj["Dados"].get("gesso_aplicado_ha", 0) + _ton_gesso, 2)
                        break
                if st.session_state.get("area_selecionada") == _id_area_atual:
                    st.session_state.dados["gesso_aplicado_ha"] = round(
                        st.session_state.dados.get("gesso_aplicado_ha", 0) + _ton_gesso, 2)
                salvar_dados_iaagro()
                success_box(f"✅ {_ton_gesso} t/ha de {_tipo_gesso} registrado!")
                st.rerun()
            else:
                warning_box("Informe a quantidade aplicada.")

        # ── Histórico e status por área ──────────────────
        if _corretivos:
            import pandas as pd
            st.markdown("#### 📋 Histórico de Corretivos")

            df_corr = pd.DataFrame(_corretivos)
            _calc_total = df_corr[df_corr["tipo"]=="calcario"]["toneladas_ha"].sum() if "tipo" in df_corr else 0
            _gesso_total = df_corr[df_corr["tipo"]=="gesso"]["toneladas_ha"].sum() if "tipo" in df_corr else 0

            # Status vs recomendado
            _d_atual = st.session_state.dados
            _ph_atual = _d_atual.get("ph", 5.5)
            _dose_rec, _ = calcular_calcario_por_ph(_ph_atual, _d_atual.get("area", 1))
            _, _dose_gesso_rec, _, _ = calcular_gesso(_d_atual)
            _ph_pos = _d_atual.get("ph_pos_calagem", _ph_atual)

            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            col_s1.metric("🪨 Calcário aplicado", f"{_calc_total:.2f} t/ha",
                          delta=f"Rec: {_dose_rec} t/ha")
            col_s2.metric("🧱 Gesso aplicado", f"{_gesso_total:.2f} t/ha",
                          delta=f"Rec: {_dose_gesso_rec:.1f} t/ha")
            col_s3.metric("pH atual", f"{_ph_atual}")
            col_s4.metric("pH estimado pós-calagem", f"{_ph_pos}",
                          delta=f"+{round(_ph_pos-_ph_atual,1)}" if _ph_pos > _ph_atual else "sem aplicação")

            # Alertas
            if _calc_total < _dose_rec * 0.7:
                st.warning(f"⚠️ Calcário aplicado ({_calc_total:.1f} t/ha) abaixo do recomendado ({_dose_rec} t/ha)")
            elif _calc_total >= _dose_rec:
                st.success(f"✅ Meta de calagem atingida! ({_calc_total:.1f}/{_dose_rec} t/ha)")

            if _gesso_total < _dose_gesso_rec * 0.7 and _dose_gesso_rec > 0:
                st.warning(f"⚠️ Gesso aplicado ({_gesso_total:.1f} t/ha) abaixo do recomendado ({_dose_gesso_rec:.1f} t/ha)")
            elif _gesso_total >= _dose_gesso_rec and _dose_gesso_rec > 0:
                st.success(f"✅ Meta de gessagem atingida! ({_gesso_total:.1f}/{_dose_gesso_rec:.1f} t/ha)")

            # Tabela
            _cols_show = [c for c in ["data","tipo","produto","toneladas_ha","prnt","incorporado","obs"] if c in df_corr.columns]
            st.dataframe(df_corr[_cols_show].rename(columns={
                "data":"Data","tipo":"Tipo","produto":"Produto",
                "toneladas_ha":"t/ha","prnt":"PRNT%","incorporado":"Incorporado","obs":"Obs"
            }), use_container_width=True)

            # Excluir
            with st.expander("🗑️ Excluir registro"):
                _opts = [f"{c.get('data','')} — {c.get('produto','')} — {c.get('toneladas_ha',0)} t/ha"
                         for c in _corretivos]
                _del = st.selectbox("Selecione", _opts, key="sel_del_corretivo")
                if st.button("🗑️ Excluir", key="btn_del_corretivo"):
                    _idx = _opts.index(_del)
                    _all = [i for i,c in enumerate(st.session_state.corretivos_aplicados)
                            if c.get("area_id") == _id_area_atual]
                    st.session_state.corretivos_aplicados.pop(_all[_idx])
                    salvar_dados_iaagro()
                    success_box("Registro excluído!")
                    st.rerun()
        else:
            st.info("📝 Nenhum corretivo registrado para esta área ainda.")
    if "ph" not in d:
        warning_box("Preencha primeiro a Análise de Solo na aba 🧪 Análise de Solo.")
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
        zona = st.selectbox("Zona do talhão", ["Baixa Produtividade","Média Produtividade","Alta Produtividade"], key="sel_zona_do_talh_o_3723")
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
# MENU: OCR LAUDO DE SOLO
# ─────────────────────────────────────────────
if menu == "🧪 Solo & Adubação":
  with _sub_solo[3]:
    st.header("📄 OCR — Leitura Automática de Laudo de Solo")
    st.markdown("""
    <div style='background:#0f3460;border-radius:12px;padding:14px 18px;
    border-left:5px solid #22c55e;margin-bottom:16px;'>
    <b style='color:#22c55e;'>📌 Como funciona</b><br>
    <span style='color:#f1f5f9;font-size:13px;'>
    Faça upload do laudo de solo em PDF ou imagem (JPG/PNG).
    O sistema extrai automaticamente os valores e preenche a Análise de Solo.
    </span>
    </div>
    """, unsafe_allow_html=True)

    col_ocr1, col_ocr2 = st.columns(2)
    with col_ocr1:
        arquivo_ocr = st.file_uploader(
            "📎 Upload do laudo (PDF, JPG, PNG)",
            type=["pdf","jpg","jpeg","png"],
            key="upl_ocr_laudo"
        )
    with col_ocr2:
        _idioma_ocr = st.selectbox("Idioma do laudo", ["por","eng"], key="sel_idioma_ocr",
                                    help="por = Português | eng = Inglês")
        _auto_preencher = st.checkbox("Preencher análise automaticamente", value=True,
                                       key="chk_auto_preencher")

    if arquivo_ocr:
        texto_ocr = ""
        with st.spinner("🔍 Lendo laudo..."):
            try:
                if arquivo_ocr.type == "application/pdf":
                    texto_ocr = extrair_texto_pdf(arquivo_ocr)
                else:
                    from PIL import Image as _PIL
                    _img = _PIL.open(arquivo_ocr)
                    texto_ocr = pytesseract.image_to_string(_img, lang=_idioma_ocr)
            except Exception as _e:
                st.error(f"❌ Erro ao ler arquivo: {_e}")

        if texto_ocr and texto_ocr.strip():
            with st.expander("📋 Texto extraído (bruto)", expanded=False):
                st.text(texto_ocr[:3000])

            # Parseia valores
            _vals = parsear_laudo_ocr(texto_ocr)
            _encontrados = {k: v for k, v in _vals.items() if v is not None}

            if _encontrados:
                st.success(f"✅ {len(_encontrados)} parâmetros encontrados no laudo!")

                # Monta tabela de preview
                _preview_rows = []
                _labels = {
                    "ph": "pH", "fosforo": "Fósforo P (mg/dm³)",
                    "potassio": "Potássio K (mg/dm³)", "calcio": "Cálcio Ca (cmolc/dm³)",
                    "magnesio": "Magnésio Mg (cmolc/dm³)", "aluminio": "Alumínio Al (cmolc/dm³)",
                    "materia_organica": "Matéria Orgânica (%)", "ctc": "CTC (cmolc/dm³)",
                    "enxofre": "Enxofre S (mg/dm³)", "boro": "Boro B",
                    "zinco": "Zinco Zn", "manganes": "Manganês Mn",
                    "cobre": "Cobre Cu",
                }
                for k, v in _encontrados.items():
                    _preview_rows.append({
                        "Parâmetro": _labels.get(k, k),
                        "Valor extraído": v,
                        "Chave": k,
                    })

                import pandas as _pd
                st.dataframe(_pd.DataFrame(_preview_rows)[["Parâmetro","Valor extraído"]],
                             use_container_width=True, hide_index=True)

                if _auto_preencher:
                    if st.button("✅ Aplicar valores na Análise de Solo", key="btn_aplicar_ocr",
                                 use_container_width=True, type="primary"):
                        for k, v in _encontrados.items():
                            try:
                                st.session_state.dados[k] = float(v)
                            except Exception:
                                pass
                        atualizar_area_atual()
                        salvar_dados_iaagro()
                        success_box("✅ Valores aplicados! Vá para a aba 🧪 Análise de Solo para conferir.")
                else:
                    st.info("ℹ️ Marque 'Preencher análise automaticamente' para aplicar os valores.")
            else:
                st.warning("⚠️ Nenhum parâmetro reconhecido automaticamente. Verifique o texto extraído acima e preencha manualmente.")

        elif arquivo_ocr:
            st.error("❌ Não foi possível extrair texto do arquivo. Verifique se o PDF não é escaneado sem OCR ou tente uma imagem JPG/PNG do laudo.")

    # Dicas de uso
    st.divider()
    st.markdown("""
    <div style='background:#0f3460;border-radius:10px;padding:12px 16px;border:1px solid #334155;'>
    <b style='color:#6ee7b7;'>💡 Dicas para melhor resultado</b><br>
    <span style='color:#cbd5e1;font-size:13px;'>
    • <b>PDF digital</b> (gerado por computador) tem melhor precisão que PDF escaneado<br>
    • Para laudos escaneados, tire foto com boa iluminação e envie como JPG<br>
    • Laudos IAC/Embrapa e CQFS RS/SC são reconhecidos automaticamente<br>
    • Após aplicar, confira os valores na aba <b>🧪 Análise de Solo</b>
    </span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MENU: EVOLUÇÃO DA FERTILIDADE DO SOLO
# ─────────────────────────────────────────────
if menu == "🧪 Solo & Adubação":
  with _sub_solo[4]:
    st.header("📊 Evolução da Fertilidade do Solo")

    if not st.session_state.areas:
        st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;">
        ℹ️ Cadastre e analise áreas para ver o histórico.</div>''', unsafe_allow_html=True)
    else:
        opcoes_area_fert = [f"{a['ID']} - {a.get('Talhão','')}" for a in st.session_state.areas]
        area_hist_fert   = st.selectbox("Selecione a área", opcoes_area_fert, key="hist_solo_area_fert")
        id_area_fert     = area_hist_fert.split(" - ")[0]

        # Tenta carregar do SQLite primeiro
        df_hist_fert = carregar_historico_solo_db(id_area_fert)

        # Se SQLite vazio, usa historico_solo da área (salvo no Supabase via areas[])
        if df_hist_fert.empty:
            _area_fert = next((a for a in st.session_state.areas if a.get("ID") == id_area_fert), None)
            if _area_fert:
                _hist_sb = _area_fert.get("historico_solo", [])
                if _hist_sb:
                    import pandas as _pd_fert
                    df_hist_fert = _pd_fert.DataFrame(_hist_sb)
                else:
                    # Busca dados de solo: tenta Dados, dados, ou session_state.dados se for a área ativa
                    _d = (_area_fert.get("Dados") or _area_fert.get("dados") or {})
                    if not _d.get("ph") and st.session_state.dados.get("id_area") == id_area_fert:
                        _d = st.session_state.dados
                    if _d and _d.get("ph"):
                        import pandas as _pd_fert
                        df_hist_fert = _pd_fert.DataFrame([{
                            "data":             "Análise atual",
                            "ph":               float(_d.get("ph", 0)),
                            "fosforo":          float(_d.get("fosforo", 0)),
                            "potassio":         float(_d.get("potassio", 0)),
                            "materia_organica": float(_d.get("materia_organica", 0)),
                            "calcio":           float(_d.get("calcio", 0)),
                            "magnesio":         float(_d.get("magnesio", 0)),
                            "aluminio":         float(_d.get("aluminio", 0)),
                            "nota":             float(_d.get("nota_solo", _area_fert.get("Nota Solo", 0)) or 0),
                            "score":            float(_d.get("score_solo", _area_fert.get("score_solo", 0)) or 0),
                            "classe":           _d.get("classe_solo", _area_fert.get("classe_solo", "—")),
                        }])

        if df_hist_fert.empty:
            st.markdown('''<div style="background:#78350f;color:#fff;padding:13px 18px;
            border-radius:10px;border-left:5px solid #f59e0b;font-weight:600;">
            ⚠️ Nenhuma análise salva para esta área ainda.<br>
            <span style='font-weight:400;font-size:13px;'>
            Preencha e salve a análise na aba <b>🧪 Análise de Solo</b>.
            </span></div>''', unsafe_allow_html=True)
        else:
            # Tabela de histórico
            _cols_disp = [c for c in ["data","ph","fosforo","potassio","materia_organica",
                                       "calcio","magnesio","score","classe"]
                          if c in df_hist_fert.columns]
            st.dataframe(df_hist_fert[_cols_disp], use_container_width=True, hide_index=True)

            # Gráficos de evolução
            st.markdown("#### 📈 Evolução dos Parâmetros")
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.caption("Score de qualidade do solo")
                _cols_score = [c for c in ["score","nota"] if c in df_hist_fert.columns]
                if _cols_score:
                    st.line_chart(df_hist_fert.set_index("data")[_cols_score])
            with col_g2:
                st.caption("pH e macronutrientes")
                _cols_nutr = [c for c in ["ph","fosforo","potassio"] if c in df_hist_fert.columns]
                if _cols_nutr:
                    st.line_chart(df_hist_fert.set_index("data")[_cols_nutr])

            col_g3, col_g4 = st.columns(2)
            with col_g3:
                st.caption("Bases trocáveis")
                _cols_bases = [c for c in ["calcio","magnesio","aluminio"] if c in df_hist_fert.columns]
                if _cols_bases:
                    st.line_chart(df_hist_fert.set_index("data")[_cols_bases])
            with col_g4:
                st.caption("Matéria orgânica")
                if "materia_organica" in df_hist_fert.columns:
                    st.line_chart(df_hist_fert.set_index("data")[["materia_organica"]])

# ─────────────────────────────────────────────
# MENU: CUSTOS
# ─────────────────────────────────────────────
elif menu == "💰 Financeiro":
    _sub_fin = st.tabs([
        "🌾 Custos da Lavoura",
        "🔧 Custos Complementares",
        "🤝 Contratos de Troca",
        "📊 Evolução por Safra",
        "💹 Dashboard",
        "🧾 Imposto de Renda Rural",
    ])

# ── ABA 0: CUSTOS DA LAVOURA ─────────────────────────────────────────────
if menu == "💰 Financeiro":
  with _sub_fin[0]:
    st.header("🌾 Custos da Lavoura")

    # Busca área ativa
    d = st.session_state.dados
    if "ph" not in d and st.session_state.areas:
        for _a in st.session_state.areas:
            _dad = _a.get("Dados", _a.get("dados", {}))
            if _dad and "ph" in _dad:
                d = {**_dad, "cultura": _a.get("Cultura","Soja"),
                     "area": _a.get("Hectares",0), "produtividade": _a.get("Produtividade",50)}
                break

    if not st.session_state.areas:
        warning_box("Cadastre uma área primeiro.")
    else:
        # Só safra — sem seletor de área
        _safra_fin = st.text_input("🌾 Safra", placeholder="2024/2025", key="txt_safra_fin")

        st.divider()
        st.subheader("📦 Insumos do Estoque (automático)")
        st.caption("Gerado a partir das aplicações registradas. Clique em 🗑️ para remover a aplicação.")

        # Calcula custo total de TODAS as aplicações (todas as áreas)
        _custo_insumos = 0.0
        _det_insumos   = []
        for _ap_idx, ap in enumerate(st.session_state.aplicacoes):
            for p in ap.get("Produtos", []):
                _nome_p  = p.get("Produto","")
                _total   = p.get("Total usado", 0)
                _unid    = p.get("Unidade","L/ha")
                _item_e  = next((e for e in st.session_state.estoque if e.get("Insumo") == _nome_p), None)
                _preco_u = _item_e.get("Valor Unitário R$", 0) if _item_e else 0
                def _conv(q, u):
                    u = (u or "").lower()
                    if "ml" in u: return q/1000
                    if "g/" in u or u == "g": return q/1000
                    return q
                _qtd_base     = _conv(_total, _unid)
                _custo_p      = _qtd_base * _preco_u
                _custo_insumos += _custo_p
                _det_insumos.append({
                    "ap_idx":      _ap_idx,
                    "Aplicação":   ap.get("Estádio", ap.get("Aplicação","")),
                    "Produto":     _nome_p,
                    "Tipo":        _item_e.get("Categoria","") if _item_e else p.get("Tipo",""),
                    "Qtd":         f"{_qtd_base:.2f} L/kg",
                    "R$ unit":     f"R$ {_preco_u:.2f}",
                    "Custo R$":    f"R$ {_custo_p:.2f}",
                })

        if _det_insumos:
            # Header
            _hcols = st.columns([2.5, 2, 1.5, 1.5, 1.2, 1.2, 0.7])
            for _h, _lbl in zip(_hcols, ["Aplicação","Produto","Tipo","Qtd","R$/un","Custo",""]): 
                _h.markdown(f"<span style='color:#6ee7b7;font-size:11px;font-weight:800;'>{_lbl}</span>",
                            unsafe_allow_html=True)
            st.markdown("<hr style='margin:4px 0;border-color:#1e4976;'>", unsafe_allow_html=True)

            _ap_indices_deletar = set()
            for _li, _row in enumerate(_det_insumos):
                _rc = st.columns([2.5, 2, 1.5, 1.5, 1.2, 1.2, 0.7])
                _rc[0].markdown(f"<span style='color:#f1f5f9;font-size:12px;'>{_row['Aplicação']}</span>",
                                unsafe_allow_html=True)
                _rc[1].markdown(f"<span style='color:#6ee7b7;font-size:12px;font-weight:600;'>{_row['Produto']}</span>",
                                unsafe_allow_html=True)
                _rc[2].markdown(f"<span style='color:#94a3b8;font-size:11px;'>{_row['Tipo']}</span>",
                                unsafe_allow_html=True)
                _rc[3].markdown(f"<span style='color:#f1f5f9;font-size:12px;'>{_row['Qtd']}</span>",
                                unsafe_allow_html=True)
                _rc[4].markdown(f"<span style='color:#94a3b8;font-size:12px;'>{_row['R$ unit']}</span>",
                                unsafe_allow_html=True)
                _rc[5].markdown(f"<span style='color:#22c55e;font-size:12px;font-weight:700;'>{_row['Custo R$']}</span>",
                                unsafe_allow_html=True)
                if _rc[6].button("🗑️", key=f"del_insumo_{_li}_{_row['ap_idx']}",
                                  help=f"Remover aplicação: {_row['Aplicação']}"):
                    _ap_indices_deletar.add(_row["ap_idx"])

            if _ap_indices_deletar:
                st.session_state.aplicacoes = [
                    a for i, a in enumerate(st.session_state.aplicacoes)
                    if i not in _ap_indices_deletar
                ]
                salvar_dados_iaagro()
                success_box(f"✅ {len(_ap_indices_deletar)} aplicação(ões) removida(s).")
                st.rerun()

            st.markdown(f"""
            <div style='background:#14532d;border-radius:10px;padding:10px 16px;margin-top:8px;'>
            <span style='color:#6ee7b7;font-size:13px;font-weight:700;'>
            💰 Total insumos (todas aplicações): R$ {_custo_insumos:,.2f}
            </span></div>""", unsafe_allow_html=True)
        else:
            st.info("Nenhuma aplicação registrada ainda.")

        st.divider()
        st.subheader("➕ Lançar Custo da Lavoura")

        CAT_LAVOURA = [
            "Semente","Fertilizante (Base)","Fertilizante (Cobertura)","Herbicida",
            "Fungicida","Inseticida","Adjuvante/Óleo","Calcário","Gesso Agrícola",
            "Inoculante","Micronutriente","Seguro Agrícola","Arrendamento","Frete",
            "Armazenagem","Assistência Técnica","Outros"
        ]
        col_l1, col_l2, col_l3 = st.columns(3)
        _cat_l  = col_l1.selectbox("Categoria", CAT_LAVOURA, key="sel_cat_lavoura")
        _desc_l = col_l2.text_input("Descrição", key="txt_desc_lavoura")
        _val_l  = col_l3.number_input("Valor R$", min_value=0.0, key="num_val_lavoura")
        _data_l = st.date_input("Data", key="dat_lavoura")

        if st.button("💾 Lançar Custo", key="btn_lancar_lavoura", use_container_width=True):
            if _val_l > 0:
                if "dre_registros" not in st.session_state:
                    st.session_state.dre_registros = []
                st.session_state.dre_registros.append({
                    "Safra": _safra_fin, "Área ID": "geral", "Tipo": "Custo Variável",
                    "Categoria": _cat_l, "Descrição": _desc_l,
                    "Valor R$": _val_l, "Área ha": 0, "Valor/ha": 0,
                    "Data": str(_data_l), "Origem": "lavoura",
                })
                salvar_dados_iaagro()
                success_box(f"✅ R$ {_val_l:.2f} — {_cat_l}")
            else:
                warning_box("Informe um valor maior que zero.")

        # Resumo por safra
        _regs_l = [r for r in st.session_state.get("dre_registros",[])
                   if r.get("Origem") == "lavoura"
                   and (not _safra_fin or r.get("Safra") == _safra_fin)]
        if _regs_l:
            st.divider()
            st.subheader("📋 Custos lançados")
            import pandas as pd
            df_l = pd.DataFrame(_regs_l)
            _total_l = df_l["Valor R$"].sum()
            col_s1, col_s2 = st.columns(2)
            col_s1.metric("Total custos lançados", f"R$ {_total_l:,.2f}")
            col_s2.metric("Total geral (insumos + custos)", f"R$ {(_total_l + _custo_insumos):,.2f}")
            st.dataframe(df_l[["Data","Safra","Categoria","Descrição","Valor R$"]]
                         .rename(columns={"Valor R$":"R$"}),
                         use_container_width=True, hide_index=True)

            with st.expander("🗑️ Excluir lançamento"):
                _opts_l = [f"{r.get('Data','')} — {r.get('Categoria','')} — R${r.get('Valor R$',0):.2f}"
                           for r in _regs_l]
                _del_l = st.selectbox("Selecione", _opts_l, key="sel_del_lavoura")
                if st.button("🗑️ Excluir", key="btn_del_lavoura"):
                    _idx_l = _opts_l.index(_del_l)
                    _all_l = [i for i,r in enumerate(st.session_state.dre_registros)
                              if r.get("Origem") == "lavoura"]
                    st.session_state.dre_registros.pop(_all_l[_idx_l])
                    salvar_dados_iaagro()
                    st.rerun()

# ── ABA 1: CUSTOS COMPLEMENTARES ─────────────────────────────────────────
if menu == "💰 Financeiro":
  with _sub_fin[1]:
    st.header("🔧 Custos Complementares")
    st.caption("Conserto de máquinas, peças, diesel, revisões e aquisições")

    CAT_COMP = [
        "Diesel e lubrificantes","Conserto de máquinas","Compra de peças",
        "Revisão preventiva","Aquisição de maquinário","Pneus",
        "Mão de obra mecânica","Implementos","Outros"
    ]
    col_c1, col_c2, col_c3 = st.columns(3)
    _cat_c  = col_c1.selectbox("Categoria", CAT_COMP, key="sel_cat_comp")
    _desc_c = col_c2.text_input("Descrição detalhada", key="txt_desc_comp",
                                  placeholder="Ex: Revisão 500h Plantadeira")
    _val_c  = col_c3.number_input("Valor R$", min_value=0.0, key="num_val_comp")
    col_c4, col_c5 = st.columns(2)
    _data_c   = col_c4.date_input("Data", key="dat_comp")
    _maquina  = col_c5.text_input("Máquina/Equipamento", key="txt_maquina_comp",
                                    placeholder="Ex: Trator John Deere 6110J")

    if st.button("💾 Lançar", key="btn_lancar_comp", use_container_width=True):
        if _val_c > 0:
            if "dre_registros" not in st.session_state:
                st.session_state.dre_registros = []
            st.session_state.dre_registros.append({
                "Safra": "", "Área ID": "geral", "Tipo": "Custo Fixo",
                "Categoria": _cat_c, "Descrição": f"{_desc_c} — {_maquina}",
                "Valor R$": _val_c, "Área ha": 0, "Valor/ha": 0,
                "Data": str(_data_c), "Origem": "complementar",
            })
            salvar_dados_iaagro()
            success_box(f"✅ R$ {_val_c:.2f} — {_cat_c}")
        else:
            warning_box("Informe um valor.")

    _regs_c = [r for r in st.session_state.get("dre_registros",[])
               if r.get("Origem") == "complementar"]
    if _regs_c:
        st.divider()
        import pandas as pd
        df_c = pd.DataFrame(_regs_c)
        _total_c = df_c["Valor R$"].sum()
        col_rc1, col_rc2 = st.columns(2)
        col_rc1.metric("Total Complementar", f"R$ {_total_c:,.2f}")
        col_rc2.metric("Maior custo", f"R$ {df_c['Valor R$'].max():,.2f}")
        st.dataframe(df_c[["Data","Categoria","Descrição","Valor R$"]]
                     .rename(columns={"Valor R$":"R$"}),
                     use_container_width=True, hide_index=True)
        # Gráfico por categoria
        _cat_group = df_c.groupby("Categoria")["Valor R$"].sum().sort_values(ascending=False)
        st.bar_chart(_cat_group)

        with st.expander("🗑️ Excluir lançamento"):
            _opts_c = [f"{r.get('Data','')} — {r.get('Categoria','')} — R${r.get('Valor R$',0):.2f}"
                       for r in _regs_c]
            _del_c = st.selectbox("Selecione", _opts_c, key="sel_del_comp")
            if st.button("🗑️ Excluir", key="btn_del_comp"):
                _idx_c = _opts_c.index(_del_c)
                _all_c = [i for i,r in enumerate(st.session_state.dre_registros)
                          if r.get("Origem") == "complementar"]
                st.session_state.dre_registros.pop(_all_c[_idx_c])
                salvar_dados_iaagro()
                st.rerun()

# ── ABA 2: CONTRATOS DE TROCA ─────────────────────────────────────────────
if menu == "💰 Financeiro":
  with _sub_fin[2]:
    st.header("🤝 Contratos de Troca (Barter)")

    # Garante que contratos_troca está inicializado (sem sobrescrever dados carregados)
    if "contratos_troca" not in st.session_state:
        st.session_state.contratos_troca = dados_carregados.get("contratos_troca", [])

    st.subheader("➕ Novo Contrato")
    col_t1, col_t2, col_t3 = st.columns(3)
    _grao_t   = col_t1.selectbox("Grão", ["Milho","Soja","Feijão","Trigo","Sorgo","Outro"], key="sel_grao_troca")
    _qtd_sacs = col_t2.number_input("Sacas (60kg)", min_value=0.0, key="num_qtd_sacs")
    _preco_sc = col_t3.number_input("Valor por saca R$", min_value=0.0, key="num_preco_sc")

    _valor_troca = _qtd_sacs * _preco_sc
    if _valor_troca > 0:
        st.info(f"💰 Valor total: **R$ {_valor_troca:,.2f}**")

    _data_entrega = st.date_input("📅 Data de entrega", key="dat_troca")

    if st.button("💾 Registrar Contrato", key="btn_reg_troca", use_container_width=True):
        if _qtd_sacs > 0 and _preco_sc > 0:
            st.session_state.contratos_troca.append({
                "Grão":           _grao_t,
                "Sacas":          _qtd_sacs,
                "Valor/sc R$":    _preco_sc,
                "Valor total R$": _valor_troca,
                "Data entrega":   str(_data_entrega),
            })
            salvar_dados_iaagro()
            success_box(f"✅ {_qtd_sacs:.0f} sc × R$ {_preco_sc:.2f} = R$ {_valor_troca:,.2f}")
            st.rerun()
        else:
            warning_box("Informe quantidade e valor.")

    if st.session_state.contratos_troca:
        st.divider()
        import pandas as _pd_b
        df_t = _pd_b.DataFrame(st.session_state.contratos_troca)
        _total_t  = df_t["Valor total R$"].sum()
        _total_sc = df_t["Sacas"].sum()

        col_rt1, col_rt2 = st.columns(2)
        col_rt1.metric("💰 Valor total em contratos", f"R$ {_total_t:,.2f}")
        col_rt2.metric("🌾 Total de sacas", f"{_total_sc:,.0f} sc")

        st.markdown("#### 📋 Contratos registrados")
        for _idx_t, _cont in enumerate(st.session_state.contratos_troca):
            _col_c1, _col_c2, _col_c3, _col_c4, _col_c5 = st.columns([2,1.5,1.5,2,0.8])
            _col_c1.markdown(
                f"<div style='background:#0f3460;border-radius:8px;padding:8px 12px;"
                f"border-left:3px solid #22c55e;'>"
                f"<span style='color:#6ee7b7;font-weight:700;font-size:13px;'>🌾 {_cont.get('Grão','')}</span>"
                f"</div>", unsafe_allow_html=True)
            _col_c2.markdown(
                f"<div style='background:#0f3460;border-radius:8px;padding:8px 12px;'>"
                f"<span style='color:#94a3b8;font-size:11px;'>SACAS</span><br>"
                f"<span style='color:#f1f5f9;font-weight:700;'>{_cont.get('Sacas',0):.0f} sc</span>"
                f"</div>", unsafe_allow_html=True)
            _col_c3.markdown(
                f"<div style='background:#0f3460;border-radius:8px;padding:8px 12px;'>"
                f"<span style='color:#94a3b8;font-size:11px;'>R$/SC</span><br>"
                f"<span style='color:#f1f5f9;font-weight:700;'>R$ {_cont.get('Valor/sc R$',0):.2f}</span>"
                f"</div>", unsafe_allow_html=True)
            _col_c4.markdown(
                f"<div style='background:#14532d;border-radius:8px;padding:8px 12px;'>"
                f"<span style='color:#6ee7b7;font-size:11px;'>TOTAL</span><br>"
                f"<span style='color:#22c55e;font-weight:800;'>R$ {_cont.get('Valor total R$',0):,.2f}</span><br>"
                f"<span style='color:#64748b;font-size:10px;'>📅 {_cont.get('Data entrega','')}</span>"
                f"</div>", unsafe_allow_html=True)
            if _col_c5.button("🗑️", key=f"del_barter_{_idx_t}",
                               help=f"Excluir contrato {_cont.get('Grão','')}"):
                st.session_state.contratos_troca.pop(_idx_t)
                salvar_dados_iaagro()
                st.rerun()
            st.markdown("<div style='margin:4px 0;'></div>", unsafe_allow_html=True)

# ── ABA 3: EVOLUÇÃO POR SAFRA ─────────────────────────────────────────────
if menu == "💰 Financeiro":
  with _sub_fin[3]:
    st.header("📊 Evolução por Safra")

    _todos_regs = st.session_state.get("dre_registros", [])
    if not _todos_regs:
        info_box("Nenhum lançamento ainda. Use as abas de custos para registrar.")
    else:
        import pandas as pd
        df_ev = pd.DataFrame(_todos_regs)
        df_ev["Valor R$"] = pd.to_numeric(df_ev["Valor R$"], errors="coerce").fillna(0)

        # Filtros
        col_ev1, col_ev2 = st.columns(2)
        _safras_ev = ["Todas"] + sorted(df_ev["Safra"].dropna().unique().tolist(), reverse=True)
        _safra_ev  = col_ev1.selectbox("Safra", _safras_ev, key="sel_safra_ev")
        _tipo_ev   = col_ev2.selectbox("Tipo", ["Todos","Custo Variável","Custo Fixo","Receita"], key="sel_tipo_ev")

        df_f = df_ev.copy()
        if _safra_ev != "Todas": df_f = df_f[df_f["Safra"] == _safra_ev]
        if _tipo_ev  != "Todos": df_f = df_f[df_f["Tipo"] == _tipo_ev]

        _total_cv = df_f[df_f["Tipo"]=="Custo Variável"]["Valor R$"].sum()
        _total_cf = df_f[df_f["Tipo"]=="Custo Fixo"]["Valor R$"].sum()
        _total_rc = df_f[df_f["Tipo"]=="Receita"]["Valor R$"].sum()
        _result   = _total_rc - _total_cv - _total_cf

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("💚 Receitas",       f"R$ {_total_rc:,.2f}")
        col_m2.metric("🔴 Custo variável", f"R$ {_total_cv:,.2f}")
        col_m3.metric("🟡 Custo fixo",     f"R$ {_total_cf:,.2f}")
        col_m4.metric("💰 Resultado",      f"R$ {_result:,.2f}",
                      delta="lucro" if _result >= 0 else "prejuízo")

        st.divider()
        st.subheader("📈 Evolução por Categoria")
        _cat_sum = df_f.groupby(["Categoria","Tipo"])["Valor R$"].sum().reset_index()
        if not _cat_sum.empty:
            st.bar_chart(_cat_sum.set_index("Categoria")["Valor R$"])

        st.subheader("📋 Todos os Lançamentos")
        _cols_show = [c for c in ["Data","Safra","Categoria","Descrição","Tipo","Valor R$","Origem"] if c in df_f.columns]
        st.dataframe(df_f[_cols_show].sort_values("Data", ascending=False),
                     use_container_width=True, hide_index=True)

        # Receita manual
        st.divider()
        st.subheader("➕ Lançar Receita")
        col_r1, col_r2, col_r3 = st.columns(3)
        _cat_r  = col_r1.selectbox("Categoria receita",
                                    ["Venda de grãos","Venda de soja","Venda de milho",
                                     "Venda de feijão","Prêmios/seguros","Arrendamento recebido","Outros"],
                                    key="sel_cat_rec_ev")
        _val_r  = col_r2.number_input("Valor R$", min_value=0.0, key="num_val_rec_ev")
        _sfr_r  = col_r3.text_input("Safra", key="txt_safra_rec_ev")
        _desc_r = st.text_input("Descrição", key="txt_desc_rec_ev")
        if st.button("💾 Lançar Receita", key="btn_lancar_rec_ev", use_container_width=True):
            if _val_r > 0:
                st.session_state.dre_registros.append({
                    "Safra": _sfr_r, "Área ID": "geral", "Tipo": "Receita",
                    "Categoria": _cat_r, "Descrição": _desc_r,
                    "Valor R$": _val_r, "Área ha": 0, "Valor/ha": 0,
                    "Data": str(datetime.now().date()), "Origem": "receita",
                })
                salvar_dados_iaagro()
                success_box(f"✅ Receita de R$ {_val_r:,.2f} lançada!")
                st.rerun()

# ── ABA 4: DASHBOARD ─────────────────────────────────────────────────────
if menu == "💰 Financeiro":
  with _sub_fin[4]:
    st.header("💹 Dashboard Financeiro")

    _todos = st.session_state.get("dre_registros", [])
    _contr = st.session_state.get("contratos_troca", [])

    if not _todos and not _contr:
        info_box("Nenhum dado financeiro ainda.")
    else:
        import pandas as pd

        df_d = pd.DataFrame(_todos) if _todos else pd.DataFrame()
        if not df_d.empty:
            df_d["Valor R$"] = pd.to_numeric(df_d["Valor R$"], errors="coerce").fillna(0)

        _total_custo = df_d["Valor R$"].sum() if not df_d.empty else 0
        _total_rec   = df_d[df_d["Tipo"]=="Receita"]["Valor R$"].sum() if not df_d.empty else 0
        _total_cv    = df_d[df_d["Tipo"]=="Custo Variável"]["Valor R$"].sum() if not df_d.empty else 0
        _total_cf    = df_d[df_d["Tipo"]=="Custo Fixo"]["Valor R$"].sum() if not df_d.empty else 0
        _total_barter= sum(c.get("Valor total R$",0) for c in _contr)
        _resultado   = _total_rec - _total_cv - _total_cf

        # KPIs principais
        col_k1, col_k2, col_k3 = st.columns(3)
        col_k1.metric("💚 Receita total",    f"R$ {_total_rec:,.2f}")
        col_k2.metric("🔴 Custo total",      f"R$ {(_total_cv+_total_cf):,.2f}")
        col_k3.metric("💰 Resultado",        f"R$ {_resultado:,.2f}",
                      delta=f"{'▲ Lucro' if _resultado>=0 else '▼ Prejuízo'}")

        col_k4, col_k5, col_k6 = st.columns(3)
        col_k4.metric("🤝 Barter registrado", f"R$ {_total_barter:,.2f}")
        _n_aplic = len(st.session_state.aplicacoes)
        col_k5.metric("🚜 Aplicações",        f"{_n_aplic}")
        _n_areas = len(st.session_state.areas)
        col_k6.metric("📍 Áreas",             f"{_n_areas}")

        if not df_d.empty:
            st.divider()
            st.subheader("📊 Custo por Categoria")
            _cat_d = df_d[df_d["Tipo"]!="Receita"].groupby("Categoria")["Valor R$"].sum().sort_values(ascending=False)
            if not _cat_d.empty:
                st.bar_chart(_cat_d)

            st.subheader("📈 Resultado por Safra")
            _sfr_d = df_d.groupby(["Safra","Tipo"])["Valor R$"].sum().unstack(fill_value=0)
            if not _sfr_d.empty:
                st.dataframe(_sfr_d, use_container_width=True)

# ── ABA 5: IR RURAL ──────────────────────────────────────────────────────
if menu == "💰 Financeiro":
  with _sub_fin[5]:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f3460,#1a4a73);border-radius:16px;
    padding:20px 24px;margin-bottom:20px;border:1px solid #22c55e33;'>
    <h2 style='color:#6ee7b7;margin:0 0 4px;font-size:22px;'>🧾 Imposto de Renda Rural</h2>
    <p style='color:#94a3b8;margin:0;font-size:13px;'>
    Apuração simplificada — Lei 8.023/90 | Valores salvos automaticamente
    </p></div>""", unsafe_allow_html=True)

    # ── Init session_state IR ──────────────────────────────────────────────
    for _k, _v in [("ir_ano",2025),("ir_nome",""),("ir_cpf",""),
                    ("ir_cidade",""),("ir_area_total",0.0),
                    ("ir_receitas",{}),("ir_despesas",{})]:
        if _k not in st.session_state:
            st.session_state[_k] = _v

    # ── Dados do produtor ──────────────────────────────────────────────────
    with st.expander("👤 Dados do Produtor", expanded=False):
        _ci1, _ci2, _ci3 = st.columns(3)
        st.session_state.ir_nome       = _ci1.text_input("Nome", value=st.session_state.ir_nome, key="ir_nome_inp")
        st.session_state.ir_cpf        = _ci1.text_input("CPF", value=st.session_state.ir_cpf, key="ir_cpf_inp")
        st.session_state.ir_cidade     = _ci2.text_input("Cidade/UF", value=st.session_state.ir_cidade, key="ir_cid_inp")
        st.session_state.ir_area_total = _ci2.number_input("Área total (ha)", min_value=0.0, value=float(st.session_state.ir_area_total), key="ir_area_inp")
        st.session_state.ir_ano        = _ci3.selectbox("Ano-calendário", [2025,2024,2023,2022], key="ir_ano_sel")

    # ── Auto-importação dos lançamentos do DRE ─────────────────────────────
    _dre_all = st.session_state.get("dre_registros", [])
    _dre_ano = [r for r in _dre_all if str(r.get("Safra","")).startswith(str(st.session_state.ir_ano)[:4])]

    _rec_dre  = sum(r["Valor R$"] for r in _dre_ano if r.get("Tipo") == "Receita")
    _desp_dre = sum(r["Valor R$"] for r in _dre_ano if r.get("Tipo") in ("Custo Variável","Custo Fixo","Custo"))

    # Também soma custos da lavoura
    _custos_lavoura = sum(r["Valor R$"] for r in _dre_all
                          if r.get("Origem") == "lavoura")
    _custos_comp    = sum(r["Valor R$"] for r in _dre_all
                          if r.get("Origem") == "complementar")

    _total_despesas_auto = _desp_dre + _custos_lavoura + _custos_comp

    if _rec_dre > 0 or _total_despesas_auto > 0:
        st.markdown(f"""
        <div style='background:#14532d;border-radius:10px;padding:12px 16px;
        border-left:4px solid #22c55e;margin-bottom:12px;'>
        <b style='color:#6ee7b7;'>✅ Valores importados automaticamente dos seus lançamentos</b><br>
        <span style='color:#f1f5f9;font-size:13px;'>
        💰 Receitas lançadas: <b>R$ {_rec_dre:,.2f}</b> &nbsp;|&nbsp;
        📉 Despesas/custos: <b>R$ {_total_despesas_auto:,.2f}</b>
        </span></div>""", unsafe_allow_html=True)
        if st.button("🔄 Sincronizar com lançamentos do Financeiro", key="btn_sync_ir"):
            # Receitas
            if _rec_dre > 0:
                st.session_state.ir_receitas["venda_graos"] = round(
                    float(st.session_state.ir_receitas.get("venda_graos",0)) + _rec_dre, 2)
            # Despesas por categoria do DRE
            _mapa_cat = {
                "Semente":"sementes","Fertilizante":"fertilizantes",
                "Defensivo":"fertilizantes","Diesel":"combustivel",
                "Combustível":"combustivel","Mão de obra":"mao_de_obra",
                "Maquinário":"manutencao","Frete":"frete","Seguro":"seguro",
                "Arrendamento":"arrendamento_pg",
            }
            for _r in _dre_ano:
                if _r.get("Tipo") in ("Custo Variável","Custo Fixo","Custo"):
                    _chave = _mapa_cat.get(_r.get("Categoria",""), "outras_despesas")
                    st.session_state.ir_despesas[_chave] = round(
                        float(st.session_state.ir_despesas.get(_chave,0)) + _r["Valor R$"], 2)
            # Custos lavoura e complementares → fertilizantes e outros
            if _custos_lavoura > 0:
                st.session_state.ir_despesas["fertilizantes"] = round(
                    float(st.session_state.ir_despesas.get("fertilizantes",0)) + _custos_lavoura, 2)
            if _custos_comp > 0:
                st.session_state.ir_despesas["outras_despesas"] = round(
                    float(st.session_state.ir_despesas.get("outras_despesas",0)) + _custos_comp, 2)
            salvar_dados_iaagro()
            success_box("✅ Valores sincronizados!")
            st.rerun()

    # ── Receitas manuais ────────────────────────────────────────────────────
    st.markdown("#### 💰 Receitas da Atividade Rural")
    _rec_items = [
        ("venda_graos","🌾 Venda de grãos (R$)"),
        ("venda_animais","🐄 Venda de animais (R$)"),
        ("arrendamento","🏡 Arrendamento recebido (R$)"),
        ("subvencoes","💰 Subvenções/PAA (R$)"),
        ("indenizacoes","🛡️ Seguro agrícola (R$)"),
        ("outras_receitas","➕ Outras receitas (R$)"),
    ]
    _rc1, _rc2 = st.columns(2)
    for i, (k, lbl) in enumerate(_rec_items):
        with (_rc1 if i%2==0 else _rc2):
            st.session_state.ir_receitas[k] = st.number_input(
                lbl, min_value=0.0, value=float(st.session_state.ir_receitas.get(k,0)),
                key=f"ir_r_{k}", format="%.2f")

    st.markdown("#### 📉 Despesas Dedutíveis")
    _desp_items = [
        ("sementes","🌱 Sementes e mudas (R$)"),
        ("fertilizantes","🧪 Fertilizantes e defensivos (R$)"),
        ("mao_de_obra","👷 Mão de obra (R$)"),
        ("combustivel","⛽ Combustível (R$)"),
        ("manutencao","🔧 Manutenção de máquinas (R$)"),
        ("arrendamento_pg","🏡 Arrendamento pago (R$)"),
        ("frete","🚛 Fretes (R$)"),
        ("seguro","🛡️ Seguros rurais (R$)"),
        ("assistencia_tec","👨‍🔬 Assistência técnica (R$)"),
        ("juros","💳 Juros de financiamentos (R$)"),
        ("outras_despesas","➕ Outras despesas (R$)"),
    ]
    _dc1, _dc2 = st.columns(2)
    for i, (k, lbl) in enumerate(_desp_items):
        with (_dc1 if i%2==0 else _dc2):
            st.session_state.ir_despesas[k] = st.number_input(
                lbl, min_value=0.0, value=float(st.session_state.ir_despesas.get(k,0)),
                key=f"ir_d_{k}", format="%.2f")

    if st.button("💾 Salvar dados do IR", key="btn_salvar_ir", use_container_width=True):
        salvar_dados_iaagro()
        success_box("✅ Dados do IR salvos!")

    # ── Cálculo ─────────────────────────────────────────────────────────────
    st.divider()
    _rec_total  = sum(st.session_state.ir_receitas.values())
    _desp_total = sum(st.session_state.ir_despesas.values())
    _resultado  = _rec_total - _desp_total
    _ISENCAO    = 142798.50
    _BASE       = max(_resultado, 0.0)

    _tabela_ir = [
        (27110.40, 0.000, 0.00),
        (33919.80, 0.075, 2033.28),
        (45012.60, 0.150, 4576.08),
        (55976.16, 0.225, 7947.24),
        (float("inf"), 0.275, 10752.00),
    ]
    _ir = 0.0; _aliq = 0.0
    if _BASE > _ISENCAO:
        for _lim, _a, _ded in _tabela_ir:
            if _BASE <= _lim:
                _ir = _BASE * _a - _ded
                _aliq = _a; break

    _ir = max(_ir, 0.0)

    # Cards resultado
    _kc = st.columns(4)
    _kc[0].metric("💰 Receita Bruta",    f"R$ {_rec_total:,.2f}")
    _kc[1].metric("📉 Despesas Dedut.", f"R$ {_desp_total:,.2f}")
    _kc[2].metric("📊 Resultado Líquido", f"R$ {_resultado:,.2f}",
                   delta="Lucro" if _resultado >= 0 else "Prejuízo")
    _kc[3].metric("🧾 IR Estimado",       f"R$ {_ir:,.2f}",
                   delta=f"Alíquota {_aliq*100:.1f}%" if _ir > 0 else "Isento")

    # Status fiscal
    if _resultado <= 0:
        st.success("✅ Resultado negativo — não há IR a pagar. O prejuízo pode ser compensado.")
    elif _BASE <= _ISENCAO:
        st.success(f"✅ Resultado abaixo do limite de isenção (R$ {_ISENCAO:,.2f}) — não há IR a pagar.")
    else:
        st.warning(f"⚠️ IR estimado: **R$ {_ir:,.2f}** — consulte seu contador.")

    # Tabela resumo
    with st.expander("📋 Detalhamento completo"):
        import pandas as _pd_ir
        _rows_ir = [
            {"Item":"(+) Receita Bruta",         "Valor R$": _rec_total},
            {"Item":"(-) Despesas Dedutíveis",    "Valor R$":-_desp_total},
            {"Item":"= Resultado Líquido",        "Valor R$": _resultado},
            {"Item":"Limite de Isenção",          "Valor R$": _ISENCAO},
            {"Item":"Base de Cálculo IR",         "Valor R$": _BASE},
            {"Item":f"Alíquota {_aliq*100:.1f}%","Valor R$": _ir},
        ]
        st.dataframe(_pd_ir.DataFrame(_rows_ir), use_container_width=True, hide_index=True)
        st.caption("⚠️ Estimativa para planejamento. Declare com contador habilitado.")

# ─────────────────────────────────────────────
# MENU: OPERACIONAL
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# MENU: OPERACIONAL
# ─────────────────────────────────────────────
elif menu == "📦 Operacional":
    _sub_op = st.tabs(["📦 Estoque de Insumos","🚜 Aplicações","⏱️ Prazo de Carência","📋 Ordem de Serviço","📜 Receituário Agronômico"])

if menu == "📦 Operacional":
  with _sub_op[0]:
    # ── HEADER com KPIs ──────────────────────────────────────────────────────
    import pandas as _pd_est

    _est = st.session_state.estoque
    _df_est = _pd_est.DataFrame(_est) if _est else _pd_est.DataFrame()

    _total_itens   = len(_df_est)
    _valor_total   = float(_df_est["Valor Total R$"].sum()) if not _df_est.empty and "Valor Total R$" in _df_est else 0
    _criticos      = sum(1 for i in _est if float(i.get("Quantidade",0)) <= 0)
    _baixos        = sum(1 for i in _est if 0 < float(i.get("Quantidade",0)) <= 5)

    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f3460,#1a4a73);border-radius:16px;
    padding:20px 24px;margin-bottom:20px;border:1px solid #22c55e33;'>
    <h2 style='color:#6ee7b7;margin:0 0 4px;font-size:22px;'>📦 Estoque de Insumos</h2>
    <p style='color:#94a3b8;margin:0;font-size:13px;'>
    Controle de defensivos, fertilizantes e insumos agrícolas
    </p></div>
    """, unsafe_allow_html=True)

    # KPIs
    _kc1, _kc2, _kc3, _kc4 = st.columns(4)
    _kc1.markdown(f"""<div style='background:#0f3460;border-radius:12px;padding:14px;text-align:center;border:1px solid #1e4976;'>
    <div style='color:#94a3b8;font-size:12px;font-weight:600;'>📦 TOTAL ITENS</div>
    <div style='color:#6ee7b7;font-size:28px;font-weight:800;'>{_total_itens}</div>
    </div>""", unsafe_allow_html=True)
    _kc2.markdown(f"""<div style='background:#0f3460;border-radius:12px;padding:14px;text-align:center;border:1px solid #1e4976;'>
    <div style='color:#94a3b8;font-size:12px;font-weight:600;'>💰 VALOR TOTAL</div>
    <div style='color:#22c55e;font-size:22px;font-weight:800;'>R$ {_valor_total:,.0f}</div>
    </div>""", unsafe_allow_html=True)
    _kc3.markdown(f"""<div style='background:{"#7f1d1d" if _criticos>0 else "#0f3460"};border-radius:12px;padding:14px;text-align:center;border:1px solid {"#ef4444" if _criticos>0 else "#1e4976"};'>
    <div style='color:#94a3b8;font-size:12px;font-weight:600;'>❌ ZERADOS</div>
    <div style='color:#{"ef4444" if _criticos>0 else "6ee7b7"};font-size:28px;font-weight:800;'>{_criticos}</div>
    </div>""", unsafe_allow_html=True)
    _kc4.markdown(f"""<div style='background:{"#78350f" if _baixos>0 else "#0f3460"};border-radius:12px;padding:14px;text-align:center;border:1px solid {"#f59e0b" if _baixos>0 else "#1e4976"};'>
    <div style='color:#94a3b8;font-size:12px;font-weight:600;'>⚠️ ESTOQUE BAIXO</div>
    <div style='color:#{"f59e0b" if _baixos>0 else "6ee7b7"};font-size:28px;font-weight:800;'>{_baixos}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ABAS DE ENTRADA ──────────────────────────────────────────────────────
    _tab_cat, _tab_manual, _tab_nfe = st.tabs([
        "🔍 Buscar Catálogo", "✏️ Cadastro Manual", "📄 Importar NF-e XML"
    ])

    # ── TAB 1: CATÁLOGO ───────────────────────────────────────────────────────
    with _tab_cat:
        st.markdown("#### 🔍 Buscar produto no catálogo")
        _busca_prod = st.text_input("Digite o nome ou ingrediente ativo",
                                     placeholder="Ex: Roundup, glifosato, Fox...",
                                     key="txt_busca_produto_catalogo")
        _resultados = buscar_produtos_catalogo(_busca_prod) if _busca_prod else []

        if _busca_prod and _resultados:
            _opcoes_cat = [f"{p['nome']} ({p['fab']}) — {p['cat']}" for p in _resultados[:20]]
            _sel_cat    = st.selectbox("Selecione o produto", _opcoes_cat, key="sel_prod_catalogo")
            _prod_sel   = _resultados[_opcoes_cat.index(_sel_cat)]
            st.markdown(f"""
            <div style='background:#0f3460;border-radius:10px;padding:10px 14px;
            border-left:4px solid #22c55e;margin:8px 0;'>
            🧪 <b style='color:#6ee7b7;'>IA:</b> {_prod_sel['ia']} &nbsp;|&nbsp;
            <b style='color:#6ee7b7;'>Cat:</b> {_prod_sel['cat']} &nbsp;|&nbsp;
            <b style='color:#6ee7b7;'>Fab:</b> {_prod_sel['fab']}
            </div>""", unsafe_allow_html=True)

            col_cat1, col_cat2, col_cat3 = st.columns(3)
            _qtd_cat   = col_cat1.number_input("Quantidade", min_value=0.0, key="num_qtd_catalogo")
            _unid_cat  = col_cat2.selectbox("Unidade", ["L","kg","mL","g","sc","un"], key="sel_unid_catalogo")
            _emb_cat   = col_cat2.selectbox("Embalagem",
                            ["1 L","5 L","10 L","20 L","50 L","100 L",
                             "1 kg","5 kg","10 kg","20 kg","50 kg",
                             "200 mL","500 mL","1000 mL","100 g","500 g","1000 g","Outro"],
                            key="sel_emb_catalogo")
            _preco_cat = col_cat3.number_input("Preço unitário R$", min_value=0.0, key="num_preco_catalogo")
            _lote_cat  = col_cat3.text_input("Lote/Validade", key="txt_lote_catalogo")
            _estmin_cat = col_cat1.number_input("Estoque mínimo", min_value=0.0, value=5.0, key="num_estmin_cat")

            if st.button("✅ Adicionar ao Estoque", key="btn_add_catalogo",
                         use_container_width=True, type="primary"):
                if _qtd_cat > 0:
                    # Verifica se já existe — soma quantidade
                    _existe = next((i for i in st.session_state.estoque
                                    if i["Insumo"] == _prod_sel["nome"]), None)
                    if _existe:
                        _existe["Quantidade"] = round(float(_existe.get("Quantidade",0)) + _qtd_cat, 4)
                        _existe["Valor Total R$"] = round(_existe["Quantidade"] * _preco_cat, 2)
                        if _preco_cat > 0:
                            _existe["Valor Unitário R$"] = _preco_cat
                        success_box(f"✅ Saldo atualizado: {_prod_sel['nome']} → {_existe['Quantidade']} {_unid_cat}")
                    else:
                        st.session_state.estoque.append({
                            "Insumo": _prod_sel["nome"], "Categoria": _prod_sel["cat"],
                            "Fabricante": _prod_sel["fab"], "Ingrediente Ativo": _prod_sel["ia"],
                            "Quantidade": _qtd_cat, "Unidade": _unid_cat, "Embalagem": _emb_cat,
                            "Valor Unitário R$": _preco_cat,
                            "Valor Total R$": round(_qtd_cat * _preco_cat, 2),
                            "Lote": _lote_cat, "Estoque Mínimo": _estmin_cat,
                        })
                        success_box(f"✅ {_prod_sel['nome']} — {_qtd_cat} {_unid_cat} adicionado!")
                    salvar_dados_iaagro()
                    st.rerun()
                else:
                    warning_box("Informe a quantidade.")
        elif _busca_prod:
            st.info("Produto não encontrado no catálogo. Use a aba **✏️ Cadastro Manual**.")

    # ── TAB 2: MANUAL ────────────────────────────────────────────────────────
    with _tab_manual:
        st.markdown("#### ✏️ Cadastrar produto manualmente")
        col_e1, col_e2, col_e3 = st.columns(3)
        nome_usar   = col_e1.text_input("Nome do insumo *", key="txt_nome_usar")
        categ_usar  = col_e2.selectbox("Categoria", ["Herbicida","Fungicida","Inseticida","Adjuvante",
                                        "Óleo","Fertilizante foliar","Semente","Calcário","Gesso",
                                        "Fertilizante sólido","Micronutriente","Inoculante","Outro"],
                                        key="sel_cat_usar")
        qtd_usar    = col_e3.number_input("Quantidade *", min_value=0.0, key="num_qtd_usar")
        col_e4, col_e5, col_e6 = st.columns(3)
        unid_usar   = col_e4.selectbox("Unidade", ["L","kg","mL","g","sc","un"], key="sel_unid_usar")
        emb_usar    = col_e5.selectbox("Embalagem",
                        ["1 L","5 L","10 L","20 L","50 L","100 L",
                         "1 kg","5 kg","10 kg","20 kg","50 kg",
                         "200 mL","500 mL","1000 mL","Outro"],
                        key="sel_emb_usar")
        preco_usar  = col_e6.number_input("Preço unitário R$", min_value=0.0, key="num_preco_usar")
        col_e7, col_e8, col_e9 = st.columns(3)
        ia_usar     = col_e7.text_input("Ingrediente ativo", key="txt_ia_usar")
        lote_usar   = col_e8.text_input("Lote/Validade", key="txt_lote_usar")
        estmin_usar = col_e9.number_input("Estoque mínimo", min_value=0.0, value=5.0, key="num_estmin_usar")

        if st.button("✅ Adicionar ao Estoque", key="btn_add_estoque",
                     use_container_width=True, type="primary"):
            if nome_usar.strip() and qtd_usar > 0:
                _existe = next((i for i in st.session_state.estoque
                                if i["Insumo"] == nome_usar.strip()), None)
                if _existe:
                    _existe["Quantidade"] = round(float(_existe.get("Quantidade",0)) + qtd_usar, 4)
                    _existe["Valor Total R$"] = round(_existe["Quantidade"] * preco_usar, 2)
                    success_box(f"✅ Saldo atualizado: {nome_usar} → {_existe['Quantidade']} {unid_usar}")
                else:
                    st.session_state.estoque.append({
                        "Insumo": nome_usar.strip(), "Categoria": categ_usar,
                        "Ingrediente Ativo": ia_usar, "Quantidade": qtd_usar,
                        "Unidade": unid_usar, "Embalagem": emb_usar,
                        "Valor Unitário R$": preco_usar,
                        "Valor Total R$": round(qtd_usar * preco_usar, 2),
                        "Lote": lote_usar, "Estoque Mínimo": estmin_usar,
                    })
                    success_box(f"✅ {nome_usar} adicionado ao estoque.")
                salvar_dados_iaagro()
                st.rerun()
            else:
                warning_box("Informe nome e quantidade.")

    # ── TAB 3: NF-e XML ──────────────────────────────────────────────────────
    with _tab_nfe:
        st.markdown("#### 📄 Importar Nota Fiscal Eletrônica (XML)")
        st.markdown("""
        <div style='background:#0f3460;border-radius:10px;padding:12px 16px;
        border-left:4px solid #22c55e;margin-bottom:12px;'>
        <span style='color:#f1f5f9;font-size:13px;'>
        📧 Faça upload do XML da NF-e recebida por e-mail ou do sistema do fornecedor.
        Todos os produtos entram no estoque automaticamente com quantidade e valor.
        </span></div>""", unsafe_allow_html=True)

        _xml_file = st.file_uploader("📎 Upload do XML da NF-e",
                                      type=["xml"], key="upl_nfe_xml")
        if _xml_file:
            try:
                import xml.etree.ElementTree as _ET
                _tree = _ET.parse(_xml_file)
                _root = _tree.getroot()
                _ns   = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

                def _txt(el, tag, ns):
                    _e = el.find(tag, ns)
                    return _e.text.strip() if _e is not None and _e.text else ""

                # Dados da NF
                _inf = _root.find(".//nfe:infNFe", _ns) or _root.find(".//{http://www.portalfiscal.inf.br/nfe}infNFe")
                _emit_nome = ""
                _n_nf = ""
                _dt_emis = ""
                if _inf is not None:
                    _emit_nome = _txt(_inf, "nfe:emit/nfe:xNome", _ns) or _txt(_inf, "{http://www.portalfiscal.inf.br/nfe}emit/{http://www.portalfiscal.inf.br/nfe}xNome", {})
                    _n_nf = _txt(_inf, "nfe:ide/nfe:nNF", _ns)
                    _dt_emis = _txt(_inf, "nfe:ide/nfe:dhEmi", _ns)[:10] if _txt(_inf, "nfe:ide/nfe:dhEmi", _ns) else ""

                # Itens
                _dets = _root.findall(".//nfe:det", _ns)
                if not _dets:
                    _dets = _root.findall(".//{http://www.portalfiscal.inf.br/nfe}det")

                _itens_nfe = []
                for _det in _dets:
                    _prod_el = _det.find("nfe:prod", _ns) or _det.find("{http://www.portalfiscal.inf.br/nfe}prod")
                    if _prod_el is None:
                        continue
                    def _t(tag):
                        _e = _prod_el.find(f"nfe:{tag}", _ns)
                        if _e is None:
                            _e = _prod_el.find(f"{{http://www.portalfiscal.inf.br/nfe}}{tag}")
                        return _e.text.strip() if _e is not None and _e.text else ""

                    _nome_prod = _t("xProd")
                    _qtd_str   = _t("qCom")
                    _unid_str  = _t("uCom")
                    _vul_str   = _t("vUnCom")
                    _vtot_str  = _t("vProd")
                    try: _qtd_f  = float(_qtd_str.replace(",","."))
                    except: _qtd_f = 0.0
                    try: _vul_f  = float(_vul_str.replace(",","."))
                    except: _vul_f = 0.0
                    try: _vtot_f = float(_vtot_str.replace(",","."))
                    except: _vtot_f = round(_qtd_f * _vul_f, 2)

                    # Normaliza unidade
                    _unid_map = {"UN":"un","UNID":"un","L":"L","LT":"L","KG":"kg",
                                 "G":"g","ML":"mL","SC":"sc","SAC":"sc","CX":"un"}
                    _unid_norm = _unid_map.get(_unid_str.upper(), _unid_str.lower() or "un")
                    _itens_nfe.append({
                        "Insumo": _nome_prod, "Quantidade": _qtd_f,
                        "Unidade": _unid_norm, "Valor Unitário R$": _vul_f,
                        "Valor Total R$": _vtot_f,
                    })

                if _itens_nfe:
                    st.success(f"✅ NF-e nº {_n_nf} de **{_emit_nome or 'Fornecedor'}** — {len(_itens_nfe)} produto(s)")
                    if _dt_emis:
                        st.caption(f"📅 Emissão: {_dt_emis}")

                    import pandas as _pd_nfe
                    st.dataframe(_pd_nfe.DataFrame(_itens_nfe)[["Insumo","Quantidade","Unidade","Valor Unitário R$","Valor Total R$"]],
                                 use_container_width=True, hide_index=True)

                    if st.button("✅ Importar todos para o Estoque", key="btn_importar_nfe",
                                 use_container_width=True, type="primary"):
                        _importados = 0
                        for _it in _itens_nfe:
                            if not _it["Insumo"] or _it["Quantidade"] <= 0:
                                continue
                            _existe = next((i for i in st.session_state.estoque
                                           if i["Insumo"] == _it["Insumo"]), None)
                            _obs = f"NF-e nº {_n_nf} — {_emit_nome} — {_dt_emis}"
                            if _existe:
                                _existe["Quantidade"] = round(float(_existe.get("Quantidade",0)) + _it["Quantidade"], 4)
                                _existe["Valor Total R$"] = round(_existe["Quantidade"] * _it["Valor Unitário R$"], 2)
                                if _it["Valor Unitário R$"] > 0:
                                    _existe["Valor Unitário R$"] = _it["Valor Unitário R$"]
                            else:
                                st.session_state.estoque.append({
                                    "Insumo": _it["Insumo"], "Categoria": "Outro",
                                    "Quantidade": _it["Quantidade"], "Unidade": _it["Unidade"],
                                    "Valor Unitário R$": _it["Valor Unitário R$"],
                                    "Valor Total R$": _it["Valor Total R$"],
                                    "Fabricante": _emit_nome, "Lote": _obs,
                                    "Estoque Mínimo": 5.0,
                                })
                            _importados += 1
                        salvar_dados_iaagro()
                        success_box(f"✅ {_importados} produto(s) importado(s) da NF-e para o estoque!")
                        st.rerun()
                else:
                    st.warning("Nenhum produto encontrado no XML. Verifique se é uma NF-e válida.")
            except Exception as _ex:
                st.error(f"❌ Erro ao processar XML: {_ex}")
                st.info("Verifique se o arquivo é um XML de NF-e válido (modelo 55).")

    # ── TABELA DO ESTOQUE ────────────────────────────────────────────────────
    st.markdown("---")
    if st.session_state.estoque:
        _df_show = _pd_est.DataFrame(st.session_state.estoque)
        for _col in ["Embalagem","Ingrediente Ativo","Fabricante","Lote","Estoque Mínimo"]:
            if _col not in _df_show.columns:
                _df_show[_col] = "—" if _col != "Estoque Mínimo" else 5.0

        _df_show["Status"] = _df_show.apply(
            lambda r: "❌ Zerado" if float(r.get("Quantidade",0)) <= 0 else
                      ("⚠️ Baixo" if float(r.get("Quantidade",0)) <= float(r.get("Estoque Mínimo",5)) else "✅ OK"),
            axis=1
        )

        # Filtros
        _col_f1, _col_f2, _col_f3 = st.columns(3)
        _filtro_cat = _col_f1.selectbox("Filtrar por categoria",
                        ["Todas"] + sorted(_df_show["Categoria"].dropna().unique().tolist()),
                        key="filtro_cat_estoque")
        _filtro_status = _col_f2.selectbox("Filtrar por status",
                        ["Todos","✅ OK","⚠️ Baixo","❌ Zerado"], key="filtro_status_estoque")
        _busca_tabela = _col_f3.text_input("🔍 Buscar", placeholder="Nome do produto...",
                                            key="busca_tabela_estoque")

        _df_filtered = _df_show.copy()
        if _filtro_cat != "Todas":
            _df_filtered = _df_filtered[_df_filtered["Categoria"] == _filtro_cat]
        if _filtro_status != "Todos":
            _df_filtered = _df_filtered[_df_filtered["Status"] == _filtro_status]
        if _busca_tabela:
            _df_filtered = _df_filtered[_df_filtered["Insumo"].str.contains(_busca_tabela, case=False, na=False)]

        # Cards de alertas
        _alertas = [i for i in st.session_state.estoque if float(i.get("Quantidade",0)) <= float(i.get("Estoque Mínimo",5))]
        if _alertas:
            with st.expander(f"🔔 {len(_alertas)} alerta(s) de estoque", expanded=True):
                for _al in _alertas:
                    _cor = "#7f1d1d" if float(_al.get("Quantidade",0)) <= 0 else "#78350f"
                    _ico = "❌" if float(_al.get("Quantidade",0)) <= 0 else "⚠️"
                    st.markdown(f"""
                    <div style='background:{_cor};border-radius:8px;padding:8px 14px;
                    margin:3px 0;display:flex;justify-content:space-between;align-items:center;'>
                    <span style='color:#fff;font-weight:600;'>{_ico} {_al.get('Insumo','')}</span>
                    <span style='color:#fca5a5;font-size:13px;'>
                    {_al.get('Quantidade',0):.2f} {_al.get('Unidade','')} restante
                    (mín: {_al.get('Estoque Mínimo',5):.0f})
                    </span>
                    </div>""", unsafe_allow_html=True)

        # Tabela principal
        _cols_exib = [c for c in ["Insumo","Categoria","Quantidade","Unidade",
                                   "Valor Unitário R$","Valor Total R$","Lote","Status"]
                      if c in _df_filtered.columns]
        st.dataframe(_df_filtered[_cols_exib], use_container_width=True, hide_index=True)

        # Editar quantidade manualmente
        with st.expander("✏️ Ajustar quantidade / excluir produto"):
            _nomes_est = [i["Insumo"] for i in st.session_state.estoque]
            _prod_edit = st.selectbox("Produto", _nomes_est, key="sel_prod_edit_est")
            _item_edit = next((i for i in st.session_state.estoque if i["Insumo"] == _prod_edit), None)
            if _item_edit:
                col_ed1, col_ed2 = st.columns(2)
                _nova_qtd = col_ed1.number_input("Nova quantidade",
                                                  min_value=0.0,
                                                  value=float(_item_edit.get("Quantidade",0)),
                                                  key="num_nova_qtd_edit")
                _novo_min = col_ed2.number_input("Novo estoque mínimo",
                                                  min_value=0.0,
                                                  value=float(_item_edit.get("Estoque Mínimo",5)),
                                                  key="num_novo_min_edit")
                col_btn1, col_btn2 = st.columns(2)
                if col_btn1.button("💾 Salvar ajuste", key="btn_salvar_edit_est", use_container_width=True):
                    _item_edit["Quantidade"] = _nova_qtd
                    _item_edit["Estoque Mínimo"] = _novo_min
                    _item_edit["Valor Total R$"] = round(_nova_qtd * float(_item_edit.get("Valor Unitário R$",0)), 2)
                    salvar_dados_iaagro()
                    success_box(f"✅ {_prod_edit} atualizado: {_nova_qtd} {_item_edit.get('Unidade','')}")
                    st.rerun()
                if col_btn2.button("🗑️ Excluir produto", key="btn_excluir_est", use_container_width=True):
                    st.session_state.estoque = [i for i in st.session_state.estoque if i["Insumo"] != _prod_edit]
                    salvar_dados_iaagro()
                    success_box(f"{_prod_edit} removido.")
                    st.rerun()
    else:
        st.markdown("""
        <div style='background:#0f3460;border-radius:12px;padding:30px;text-align:center;
        border:2px dashed #1e4976;margin:20px 0;'>
        <div style='font-size:48px;'>📦</div>
        <div style='color:#94a3b8;font-size:16px;margin-top:8px;'>Estoque vazio</div>
        <div style='color:#64748b;font-size:13px;'>Use as abas acima para adicionar produtos</div>
        </div>""", unsafe_allow_html=True)

  with _sub_op[1]:
    st.header("🚜 Aplicações Agrícolas")

    if "aplicacoes" not in st.session_state:
        st.session_state.aplicacoes = []

    ESTADIOS = [
        "🌱 Pré-plantio","🌿 Pós-plantio / V0","🌾 V1 – V3","🌾 V4 – V6",
        "🌾 V7 – VT","🌸 R1 – R2 (Floração)","🫘 R3 – R4 (Granação)",
        "🫘 R5 – R6","🌾 Pré-colheita","📋 Outro",
    ]
    TIPOS_PRODUTO = ["Herbicida","Fungicida","Inseticida","Adjuvante",
                     "Óleo mineral/vegetal","Fertilizante foliar","Regulador","Outro"]

    if len(st.session_state.estoque) == 0:
        warning_box("Cadastre produtos no estoque antes de registrar aplicações.")
    else:
        st.subheader("➕ Nova Aplicação")
        col_h1, col_h2, col_h3 = st.columns(3)
        with col_h1:
            estadio_sel = st.selectbox("📅 Estádio fenológico", ESTADIOS, key="sel_estadio_aplic")
            if estadio_sel == "📋 Outro":
                nome_aplic = st.text_input("Nome da aplicação", placeholder="Ex: Aplicação especial", key="txt_nome_aplic")
            else:
                nome_aplic = estadio_sel
                st.info(f"📋 Nome: **{nome_aplic}**")
        with col_h2:
            data_aplic = st.date_input("Data", key="dat_data_aplic")
            area_aplic = st.number_input("Área (ha)", min_value=0.0,
                                          value=float(st.session_state.dados.get("area", 0.0)),
                                          key="num_area_aplic")
        with col_h3:
            calda_lha  = st.number_input("Volume calda (L/ha)", min_value=0.0, value=100.0, key="num_calda_lha")
            _cap_salva = st.session_state.dados.get("cap_tanque_salva", 3000.0)
            cap_tanque = st.number_input("Capacidade tanque (L)", min_value=0.0,
                                          value=float(_cap_salva), key="num_cap_tanque",
                                          help="💾 Salvo automaticamente")
            if cap_tanque != _cap_salva and cap_tanque > 0:
                st.session_state.dados["cap_tanque_salva"] = cap_tanque
                salvar_dados_iaagro()
                st.caption(f"✅ Tanque de {cap_tanque:.0f}L salvo!")

        area_por_tanque = round(cap_tanque / calda_lha, 2) if calda_lha > 0 else 0
        n_tanques       = round(area_aplic / area_por_tanque, 2) if area_por_tanque > 0 else 0
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("📐 Área por tanque", f"{area_por_tanque} ha")
        col_m2.metric("🪣 Nº de tanques",   f"{n_tanques}")

        with st.expander("🧑‍🌾 Dados do operador", expanded=False):
            col_o1, col_o2, col_o3 = st.columns(3)
            operador     = col_o1.text_input("Operador", key="txt_operador_aplic")
            pulverizador = col_o2.text_input("Pulverizador/Máquina", key="txt_pulv_aplic")
            velocidade   = col_o1.number_input("Velocidade (km/h)", min_value=0.0, key="num_veloc_aplic")
            pressao      = col_o2.number_input("Pressão (bar)", min_value=0.0, key="num_pressao_aplic")
            clima_aplic  = col_o3.selectbox("Clima", ["Adequado","Vento alto","Muito seco","Chuva próxima","Muito quente"], key="sel_clima_aplic")

        st.subheader("🧪 Produtos da Aplicação")
        _nomes_estoque = [item["Insumo"] for item in st.session_state.estoque]
        n_produtos = int(st.number_input("Quantidade de produtos", min_value=1, max_value=10, value=1, step=1, key="num_qtd_produtos_aplic"))

        produtos_aplic = []
        for i in range(n_produtos):
            st.markdown(f"**Produto {i+1}**")
            col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns([3,2,1,1,2])
            _prod  = col_p1.selectbox("Produto",   _nomes_estoque, key=f"sel_prod_aplic_{i}")
            _tipo_p= col_p2.selectbox("Tipo",       TIPOS_PRODUTO,  key=f"sel_tipo_prod_{i}")
            _dose  = col_p3.number_input("Dose/ha", min_value=0.0,  key=f"num_dose_aplic_{i}")
            _unid  = col_p4.selectbox("Un.", ["L/ha","mL/ha","kg/ha","g/ha"], key=f"sel_unid_aplic_{i}")
            _obs_p = col_p5.text_input("Obs.", key=f"txt_obs_prod_{i}")
            _por_tanque = round(_dose * area_por_tanque, 3)
            _total_prod = round(_dose * area_aplic, 3)
            if _dose > 0:
                st.caption(f"  → {_por_tanque} {_unid.replace('/ha','')} por tanque | Total: {_total_prod} {_unid.replace('/ha','')}")
            produtos_aplic.append({
                "Produto": _prod, "Tipo": _tipo_p, "Dose por ha": _dose, "Unidade": _unid,
                "Produto por tanque": _por_tanque, "Total usado": _total_prod, "Observação": _obs_p
            })

        if st.button("💾 Salvar Aplicação", key="salvar_aplicacao_modelada", use_container_width=True):
            erro = False
            if not nome_aplic.strip(): error_box("Informe o nome da aplicação."); erro = True
            if area_aplic <= 0:        error_box("Informe a área aplicada."); erro = True
            for p in produtos_aplic:
                if p["Dose por ha"] <= 0: error_box(f"Dose zero: {p['Produto']}."); erro = True
            if not erro:
                st.session_state.aplicacoes.append({
                    "ID Área":             st.session_state.dados.get("id_area",""),
                    "Estádio":             estadio_sel,
                    "Aplicação":           nome_aplic,
                    "Data":                str(data_aplic),
                    "Área aplicada ha":    area_aplic,
                    "Volume calda L/ha":   calda_lha,
                    "Capacidade tanque L": cap_tanque,
                    "Área por tanque ha":  area_por_tanque,
                    "Número tanques":      n_tanques,
                    "Operador":            operador,
                    "Pulverizador":        pulverizador,
                    "Velocidade km/h":     velocidade,
                    "Pressão bar":         pressao,
                    "Clima aplicação":     clima_aplic,
                    "Produtos":            produtos_aplic,
                    "Status":              "pendente",
                })
                atualizar_area_atual()
                salvar_dados_iaagro()
                success_box(f"✅ {nome_aplic} salva! {len(produtos_aplic)} produto(s).")
                st.rerun()

        # PDF
        st.divider()
        st.subheader("📋 Histórico de Aplicações")
        if st.session_state.aplicacoes:
            if st.button("📄 Gerar PDF — Programação de Aplicações", key="btn_gerar_pdf_aplic", use_container_width=True):
                try:
                    _d = st.session_state.dados
                    _pdf_bytes = gerar_pdf_programacao_aplicacoes(
                        aplicacoes = st.session_state.aplicacoes,
                        fazenda    = _d.get("fazenda",""),
                        talhao     = _d.get("talhao",""),
                        cultura    = cultura_limpa(_d.get("cultura","")),
                        area_ha    = _d.get("area",0),
                        operador   = _d.get("operador",""),
                    )
                    st.session_state["_pdf_aplic"] = _pdf_bytes
                    st.success("✅ PDF gerado!")
                except Exception as e:
                    st.error(f"Erro ao gerar PDF: {e}")
            if st.session_state.get("_pdf_aplic"):
                st.download_button(
                    label="⬇️ Baixar PDF",
                    data=st.session_state["_pdf_aplic"],
                    file_name=f"programacao_aplicacoes_{datetime.now().strftime('%d%m%Y')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="btn_download_pdf_aplic"
                )

        if len(st.session_state.aplicacoes) == 0:
            info_box("Nenhuma aplicação registrada ainda.")
        else:
            _ordem = {"🌱 Pré-plantio":1,"🌿 Pós-plantio / V0":2,"🌾 V1 – V3":3,
                      "🌾 V4 – V6":4,"🌾 V7 – VT":5,"🌸 R1 – R2 (Floração)":6,
                      "🫘 R3 – R4 (Granação)":7,"🫘 R5 – R6":8,"🌾 Pré-colheita":9}
            aplicacoes_ordenadas = sorted(st.session_state.aplicacoes,
                key=lambda x: _ordem.get(x.get("Estádio", x.get("Aplicação","")), 99))

            for idx_a, aplic in enumerate(aplicacoes_ordenadas):
                _status   = aplic.get("Status", "pendente")
                _badge    = "✅ Aplicado" if _status == "aplicado" else "⏳ Pendente"
                with st.expander(f"{aplic.get('Estádio','') or aplic.get('Aplicação','')} — {aplic.get('Data','')} | {_badge}"):
                    col_i1, col_i2 = st.columns(2)
                    col_i1.markdown(f"**Área:** {aplic.get('Área aplicada ha',0)} ha")
                    col_i1.markdown(f"**Calda:** {aplic.get('Volume calda L/ha',0)} L/ha")
                    col_i1.markdown(f"**Tanques:** {aplic.get('Número tanques',0):.1f}")
                    col_i2.markdown(f"**Operador:** {aplic.get('Operador','—')}")
                    col_i2.markdown(f"**Pulverizador:** {aplic.get('Pulverizador','—')}")
                    col_i2.markdown(f"**Clima:** {aplic.get('Clima aplicação','—')}")
                    st.markdown("**🧪 Produtos:**")
                    for p in aplic.get("Produtos",[]):
                        unid = p.get("Unidade","").replace("/ha","")
                        st.markdown(f"- **{p.get('Produto','')}** ({p.get('Tipo','')}) — "
                                    f"{p.get('Dose por ha',0)} {p.get('Unidade','')} | "
                                    f"Total: {p.get('Total usado',0)} {unid}")
                    col_b1, col_b2, col_b3 = st.columns(3)
                    if _status != "aplicado":
                        if col_b1.button("✅ Marcar como Aplicado", key=f"btn_confirmar_aplic_{idx_a}",
                                         use_container_width=True, type="primary"):
                            _erros_baixa = []
                            for p in aplic.get("Produtos",[]):
                                ok_b, msg_b = baixar_estoque(p["Produto"], p.get("Total usado",0), p.get("Unidade","L/ha"))
                                if not ok_b:
                                    _erros_baixa.append(f"{p.get('Produto','')}: {msg_b}")
                            _idx_orig = next((i for i,a in enumerate(st.session_state.aplicacoes)
                                             if a.get("Data") == aplic.get("Data") and
                                             a.get("Aplicação") == aplic.get("Aplicação")), None)
                            if _idx_orig is not None:
                                st.session_state.aplicacoes[_idx_orig]["Status"] = "aplicado"
                                st.session_state.aplicacoes[_idx_orig]["Data Confirmacao"] = \
                                    datetime.now().strftime("%d/%m/%Y %H:%M")
                            salvar_dados_iaagro()
                            if _erros_baixa:
                                warning_box("Aplicado! Aviso estoque: " + " | ".join(_erros_baixa))
                            else:
                                success_box("✅ Marcado como aplicado! Baixa dada no estoque.")
                            st.rerun()
                    else:
                        col_b1.success(f"✅ Aplicado em {aplic.get('Data Confirmacao', aplic.get('Data',''))}")
                    # Exportar para imprimir
                    _linhas_exp = [
                        f"Aplicação: {aplic.get('Estádio', aplic.get('Aplicação',''))}",
                        f"Data: {aplic.get('Data','')}",
                        f"Área: {aplic.get('Área aplicada ha',0)} ha",
                        f"Calda: {aplic.get('Volume calda L/ha',0)} L/ha",
                        f"Tanques: {aplic.get('Número tanques',0):.1f}",
                        f"Operador: {aplic.get('Operador','—')}",
                        f"Status: {_badge}", "", "PRODUTOS:",
                    ]
                    for _pp in aplic.get("Produtos",[]):
                        _linhas_exp.append(
                            f"  {_pp.get('Produto','')} | {_pp.get('Dose por ha',0)} "
                            f"{_pp.get('Unidade','')} | Total: {_pp.get('Total usado',0)}")
                    _txt_exp = "\n".join(_linhas_exp)
                    col_b2.download_button(
                        "📥 Exportar",
                        data=_txt_exp.encode("utf-8"),
                        file_name=f"aplicacao_{idx_a+1}_{aplic.get('Data','sem_data')}.txt",
                        mime="text/plain",
                        key=f"btn_exp_aplic_{idx_a}",
                        use_container_width=True
                    )
                    if col_b3.button("🗑️ Excluir", key=f"apagar_app_{idx_a}", use_container_width=True):
                        _idx_orig = next((i for i,a in enumerate(st.session_state.aplicacoes)
                                         if a.get("Data") == aplic.get("Data") and
                                         a.get("Aplicação") == aplic.get("Aplicação")), None)
                        if _idx_orig is not None:
                            st.session_state.aplicacoes.pop(_idx_orig)
                        salvar_dados_iaagro()
                        st.rerun()

# ─────────────────────────────────────────────
# MENU: CARÊNCIA
# ─────────────────────────────────────────────
if menu == "📦 Operacional":
  with _sub_op[2]:
    st.header("⏱️ Controle de Prazo de Carência e Reentrada")
    if "carencia_registros" not in st.session_state:
        st.session_state.carencia_registros = []
    st.subheader("➕ Registrar Aplicação com Carência")
    col1, col2, col3 = st.columns(3)
    with col1:
        car_produto    = st.text_input("Nome do produto/defensivo", key="car_produto")
        car_cultura    = st.selectbox("Cultura", get_culturas() + ["Outra"], key="car_cultura")
        car_data_aplic = st.date_input("Data da aplicação", key="car_data")
    with col2:
        car_carencia   = st.number_input("Prazo de carência (dias)", min_value=0, value=14, key="car_carencia")
        car_reentrada  = st.number_input("Prazo de reentrada (horas)", min_value=0, value=48, key="car_reentrada")
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
                "Produto": car_produto, "Cultura": car_cultura, "Talhão": car_talhao,
                "Data Aplicação": str(car_data_aplic), "Carência dias": car_carencia,
                "Data Colheita Segura": str(data_colheita_seg), "Reentrada horas": car_reentrada,
                "Data Reentrada": str(data_reentrada.date()), "Dose": car_dose,
                "EPI": ", ".join(car_epi), "Observações": car_obs,
            })
            salvar_dados_iaagro()
            success_box(f"Registro de {car_produto} salvo! Carência até: {data_colheita_seg}")
    if st.session_state.carencia_registros:
        import pandas as pd
        df_car = pd.DataFrame(st.session_state.carencia_registros)
        st.dataframe(df_car, use_container_width=True)
        with st.expander("🗑️ Excluir"):
            opcoes_del = [f"{r.get('Produto','')} — {r.get('Data Aplicação','')}"
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
if menu == "📦 Operacional":
  with _sub_op[3]:
    st.header("📋 Ordem de Serviço")
    info_box("Gere uma Ordem de Serviço completa para o operador ir ao campo.")
    col1, col2 = st.columns(2)
    with col1:
        os_numero     = st.text_input("Número da OS", value=f"OS-{datetime.now().strftime('%Y%m%d%H%M')}", key="txt_n_mero_da_os_6029")
        os_data       = st.date_input("Data da OS", value=date.today(), key="dat_data_da_os_6030")
        os_fazenda    = st.text_input("Fazenda", value=st.session_state.dados.get("fazenda",""), key="txt_fazenda_6031")
        os_talhao     = st.text_input("Talhão", value=st.session_state.dados.get("talhao",""), key="txt_talh_o_6032")
        os_area       = st.number_input("Área (ha)", value=float(st.session_state.dados.get("area",0)), key="num__rea__ha__6033")
        os_cultura    = st.text_input("Cultura", value=st.session_state.dados.get("cultura",""), key="txt_cultura_6034")
    with col2:
        os_operador   = st.text_input("Operador responsável", key="txt_operador_respon_6036")
        os_maquina    = st.text_input("Máquina / Pulverizador", key="txt_m_quina___pulve_6037")
        os_velocidade = st.number_input("Velocidade (km/h)", value=6.0, key="num_velocidade__km__6038")
        os_pressao    = st.number_input("Pressão de trabalho (bar)", value=2.5, key="num_press_o_de_trab_6039")
        os_volume     = st.number_input("Volume de calda (L/ha)", value=100.0, key="num_volume_de_calda_6040")
        os_inicio     = st.text_input("Horário previsto de início", placeholder="Ex: 06:30", key="txt_hor_rio_previst_6041")
    st.subheader("🧪 Produtos da OS")
    os_qtd_produtos = st.number_input("Quantidade de produtos", min_value=1, max_value=10, value=1, key="os_qtd")
    os_produtos = []
    for i in range(int(os_qtd_produtos)):
        col_p1, col_p2, col_p3 = st.columns(3)
        _p = col_p1.text_input(f"Produto {i+1}", key=f"os_prod_{i}")
        _d = col_p2.number_input(f"Dose/ha {i+1}", min_value=0.0, key=f"os_dose_{i}")
        _u = col_p3.selectbox(f"Un. {i+1}", ["L/ha","mL/ha","kg/ha","g/ha"], key=f"os_unid_{i}")
        os_produtos.append({"Produto":_p,"Dose":_d,"Unidade":_u})
    os_epi = st.multiselect("EPI obrigatório",
                             ["Máscara com filtro","Luvas nitrílicas","Óculos de proteção",
                              "Macacão impermeável","Botas de borracha","Protetor auricular","Avental"],
                             key="os_epi")
    os_obs_geral = st.text_area("Observações gerais", key="os_obs_geral")
    if st.button("📄 Gerar Ordem de Serviço (PDF)", key="btn_gerar_os"):
        from reportlab.lib.units import cm
        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm,
                                topMargin=1.5*cm, bottomMargin=1.5*cm)
        styles = getSampleStyleSheet()
        el = []
        if os.path.exists("IAAgrologo.jpeg"):
            el.append(Image("IAAgrologo.jpeg", width=3*cm, height=1.5*cm))
        el.append(Spacer(1,6))
        el.append(Paragraph(f"ORDEM DE SERVIÇO — {os_numero}", styles["Title"]))
        el.append(Paragraph(f"Data: {os_data} | Fazenda: {os_fazenda} | Talhão: {os_talhao}", styles["Normal"]))
        el.append(Paragraph(f"Operador: {os_operador} | Máquina: {os_maquina}", styles["Normal"]))
        el.append(Paragraph(f"Velocidade: {os_velocidade} km/h | Pressão: {os_pressao} bar | Volume: {os_volume} L/ha", styles["Normal"]))
        el.append(Spacer(1,12))
        el.append(Paragraph("PRODUTOS:", styles["Heading2"]))
        for p in os_produtos:
            el.append(Paragraph(f"• {p['Produto']}: {p['Dose']} {p['Unidade']}", styles["Normal"]))
        el.append(Spacer(1,12))
        el.append(Paragraph(f"EPI obrigatório: {', '.join(os_epi)}", styles["Normal"]))
        el.append(Paragraph(f"Observações: {os_obs_geral}", styles["Normal"]))
        el.append(Spacer(1,24))
        el.append(Paragraph("Assinatura do operador: ___________________________", styles["Normal"]))
        doc.build(el)
        buf.seek(0)
        st.session_state["_os_pdf"] = buf.read()
        st.success("✅ OS gerada!")
    if st.session_state.get("_os_pdf"):
        st.download_button("⬇️ Baixar OS PDF", data=st.session_state["_os_pdf"],
                           file_name=f"OS_{os_numero}.pdf", mime="application/pdf",
                           use_container_width=True, key="btn_dl_os")

# ─────────────────────────────────────────────
# MENU: RECEITUÁRIO
# ─────────────────────────────────────────────
if menu == "📦 Operacional":
  with _sub_op[4]:
    st.header("📜 Receituário Agronômico")
    if "receituarios" not in st.session_state:
        st.session_state.receituarios = []
    col1, col2 = st.columns(2)
    with col1:
        rec_numero    = st.text_input("Número do receituário", key="rec_numero")
        rec_produto   = st.text_input("Produto/defensivo", key="rec_produto")
        rec_cultura   = st.selectbox("Cultura", get_culturas(), key="rec_cultura")
        rec_praga     = st.text_input("Praga/doença/planta daninha", key="rec_praga")
        rec_dose      = st.text_input("Dose recomendada", placeholder="Ex: 0.5 L/ha", key="rec_dose")
        rec_epoca     = st.text_input("Época de aplicação", placeholder="Ex: Estádio R1", key="rec_epoca")
    with col2:
        rec_responsavel = st.text_input("Responsável técnico", key="rec_responsavel")
        rec_crea        = st.text_input("CREA/CRB", key="rec_crea")
        rec_produtor    = st.text_input("Produtor", key="rec_produtor")
        rec_propriedade = st.text_input("Propriedade", key="rec_propriedade")
        rec_area        = st.number_input("Área (ha)", min_value=0.0, key="rec_area")
        rec_data        = st.date_input("Data", key="rec_data")
    rec_obs = st.text_area("Observações técnicas", key="rec_obs")
    if st.button("💾 Salvar Receituário", key="btn_salvar_rec"):
        st.session_state.receituarios.append({
            "Número": rec_numero, "Produto": rec_produto, "Cultura": rec_cultura,
            "Praga/Doença": rec_praga, "Dose": rec_dose, "Época": rec_epoca,
            "Responsável": rec_responsavel, "CREA": rec_crea, "Produtor": rec_produtor,
            "Propriedade": rec_propriedade, "Área ha": rec_area,
            "Data": str(rec_data), "Obs": rec_obs,
        })
        salvar_dados_iaagro()
        success_box("Receituário salvo!")
    if st.session_state.receituarios:
        import pandas as pd
        st.dataframe(pd.DataFrame(st.session_state.receituarios), use_container_width=True)

# ─────────────────────────────────────────────
# MENU: RELATÓRIO FINAL
# ─────────────────────────────────────────────
elif menu == "📄 Relatório Final":
    st.header("📄 Relatório Final da Propriedade")
    if not st.session_state.areas:
        warning_box("Cadastre pelo menos uma área para gerar o relatório.")
    else:
        _areas_rel = [f"{a['ID']} — {a.get('Talhão','?')} ({a.get('Cultura','?')})"
                      for a in st.session_state.areas]
        _sel_rel  = st.selectbox("📍 Área para o relatório", _areas_rel, key="sel_area_relatorio")
        _id_rel   = _sel_rel.split(" — ")[0]
        _area_rel = next((a for a in st.session_state.areas if a.get("ID") == _id_rel), {})
        _dados_rel = _area_rel.get("Dados", _area_rel.get("dados", {})) or {}
        col_r1, col_r2 = st.columns(2)
        nome_produtor = col_r1.text_input("Nome do produtor", value=st.session_state.get("usuario_atual",""), key="rel_produtor")
        municipio     = col_r2.text_input("Município/UF", value=_dados_rel.get("cidade",""), key="rel_municipio")
        if st.button("📄 Gerar Relatório Final (PDF)", key="btn_gerar_relatorio", use_container_width=True):
            try:
                from reportlab.lib.pagesizes import A4 as A4_
                from reportlab.lib import colors as rl_c
                from reportlab.lib.units import cm as cm_
                from reportlab.platypus import SimpleDocTemplate as SDT, Paragraph as Par, Spacer as Sp, Table as Tbl, TableStyle as TS, HRFlowable as HR
                from reportlab.lib.styles import ParagraphStyle as PS
                from reportlab.lib.enums import TA_CENTER as TAC, TA_LEFT as TAL
                buf_r = BytesIO()
                doc_r = SDT(buf_r, pagesize=A4_, rightMargin=2*cm_, leftMargin=2*cm_, topMargin=2*cm_, bottomMargin=2*cm_)
                el_r  = []
                def Pr_(t, sz=9, b=False, c=None, al=TAL):
                    fn = "Helvetica-Bold" if b else "Helvetica"
                    return Par(t, PS("p", fontName=fn, fontSize=sz, textColor=c or rl_c.HexColor("#0f172a"), alignment=al, leading=sz+3))
                COR_V_ = rl_c.HexColor("#16a34a"); COR_E_ = rl_c.HexColor("#14532d")
                COR_C_ = rl_c.HexColor("#f1f5f9"); COR_B_ = rl_c.HexColor("#e2e8f0")
                if os.path.exists("IAAgrologo.jpeg"):
                    el_r.append(Image("IAAgrologo.jpeg", width=3*cm_, height=1.5*cm_))
                el_r.append(Pr_("RELATÓRIO AGRONÔMICO — IAAgro", 15, True, COR_E_, TAC))
                el_r.append(Pr_(f"Emitido: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 8, False, rl_c.HexColor("#64748b"), TAC))
                el_r.append(Sp(1, 0.3*cm_)); el_r.append(HR(width="100%", thickness=2, color=COR_V_)); el_r.append(Sp(1, 0.3*cm_))
                t_inf = Tbl([[Pr_(f"<b>Produtor:</b> {nome_produtor or '—'}"), Pr_(f"<b>Município:</b> {municipio or '—'}"),
                               Pr_(f"<b>Talhão:</b> {_area_rel.get('Talhão','—')}"), Pr_(f"<b>Área:</b> {_area_rel.get('Hectares',0)} ha")]],
                             colWidths=[4*cm_,3.5*cm_,4*cm_,4*cm_])
                t_inf.setStyle(TS([("BACKGROUND",(0,0),(-1,-1),COR_C_),("GRID",(0,0),(-1,-1),0.4,COR_B_),
                    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),6)]))
                el_r.append(t_inf); el_r.append(Sp(1,0.4*cm_))
                if "ph" in _dados_rel:
                    el_r.append(Pr_("ANÁLISE DE SOLO", 11, True, COR_E_))
                    el_r.append(HR(width="100%", thickness=1, color=COR_V_)); el_r.append(Sp(1,0.2*cm_))
                    rows_s = [[Pr_("<b>Parâmetro</b>",9,True,rl_c.white),Pr_("<b>Valor</b>",9,True,rl_c.white),
                               Pr_("<b>Unidade</b>",9,True,rl_c.white),Pr_("<b>Ref.</b>",9,True,rl_c.white)],
                              [Pr_("pH"),Pr_(str(_dados_rel.get("ph","—"))),Pr_("adimensional"),Pr_("5.5–6.5")],
                              [Pr_("Fósforo"),Pr_(str(_dados_rel.get("fosforo","—"))),Pr_("mg/dm3"),Pr_(">12")],
                              [Pr_("Potássio"),Pr_(str(_dados_rel.get("potassio","—"))),Pr_("mg/dm3"),Pr_(">80")],
                              [Pr_("Cálcio"),Pr_(str(_dados_rel.get("calcio","—"))),Pr_("cmolc/dm3"),Pr_(">2.0")],
                              [Pr_("Magnésio"),Pr_(str(_dados_rel.get("magnesio","—"))),Pr_("cmolc/dm3"),Pr_(">0.5")],
                              [Pr_("M.O."),Pr_(str(_dados_rel.get("materia_organica","—"))),Pr_("g/dm3"),Pr_(">25")],
                              [Pr_("V%"),Pr_(str(_dados_rel.get("v_percent","—"))),Pr_("%"),Pr_(">60%")]]
                    ts_ = Tbl(rows_s, colWidths=[4*cm_,3*cm_,3.5*cm_,5*cm_])
                    ts_.setStyle(TS([("BACKGROUND",(0,0),(-1,0),COR_E_),("TEXTCOLOR",(0,0),(-1,0),rl_c.white),
                        ("ROWBACKGROUNDS",(0,1),(-1,-1),[COR_C_,rl_c.white]),("GRID",(0,0),(-1,-1),0.4,COR_B_),
                        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),("LEFTPADDING",(0,0),(-1,-1),6)]))
                    el_r.append(ts_); el_r.append(Sp(1,0.4*cm_))
                _hist = [h for h in st.session_state.historico_produtividade if h.get("Área","").startswith(_id_rel)]
                if _hist:
                    el_r.append(Pr_("HISTÓRICO DE PRODUTIVIDADE", 11, True, COR_E_))
                    el_r.append(HR(width="100%", thickness=1, color=COR_V_)); el_r.append(Sp(1,0.2*cm_))
                    rows_h = [[Pr_("<b>Safra</b>",9,True,rl_c.white),Pr_("<b>Cultura</b>",9,True,rl_c.white),
                               Pr_("<b>Produtividade</b>",9,True,rl_c.white),Pr_("<b>Custo R$/ha</b>",9,True,rl_c.white)]]
                    for h in _hist:
                        rows_h.append([Pr_(h.get("Safra","—"),9),Pr_(cultura_limpa(h.get("Cultura","—")),9),
                                       Pr_(f"{h.get('Produtividade',0):.1f} sc/ha",9),Pr_(f"R$ {h.get('Custo',0):.2f}",9)])
                    th_ = Tbl(rows_h, colWidths=[3*cm_,4*cm_,4*cm_,4.5*cm_])
                    th_.setStyle(TS([("BACKGROUND",(0,0),(-1,0),COR_E_),("TEXTCOLOR",(0,0),(-1,0),rl_c.white),
                        ("ROWBACKGROUNDS",(0,1),(-1,-1),[COR_C_,rl_c.white]),("GRID",(0,0),(-1,-1),0.4,COR_B_),
                        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),("LEFTPADDING",(0,0),(-1,-1),6)]))
                    el_r.append(th_)
                el_r.append(HR(width="100%", thickness=1, color=COR_V_))
                el_r.append(Pr_(f"IAAgro — {datetime.now().strftime('%d/%m/%Y %H:%M')}",7,False,rl_c.HexColor("#64748b"),TAC))
                doc_r.build(el_r)
                buf_r.seek(0)
                st.session_state["_pdf_relatorio"] = buf_r.read()
                st.success("✅ Relatório gerado!")
            except Exception as e:
                st.error(f"Erro: {e}")
        if st.session_state.get("_pdf_relatorio"):
            st.download_button("⬇️ Baixar Relatório PDF", data=st.session_state["_pdf_relatorio"],
                               file_name=f"relatorio_iaagro_{datetime.now().strftime('%d%m%Y')}.pdf",
                               mime="application/pdf", use_container_width=True, key="btn_download_relatorio")

# ─────────────────────────────────────────────
# MENU: INTELIGÊNCIA
# ─────────────────────────────────────────────
elif menu == "🌍 Inteligência":
    _sub_int = st.tabs(["🌤️ Clima & Alertas","💰 Preços de Mercado","🗺️ Mapa de Colheita IA","📅 Calendário Agrícola","🤖 Assistente IA"])

if menu == "🌍 Inteligência":
  with _sub_int[0]:
    # Header profissional
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f3460,#1a4a73);border-radius:16px;
    padding:20px 24px;margin-bottom:20px;border:1px solid #22c55e33;'>
    <h2 style='color:#6ee7b7;margin:0 0 4px;font-size:22px;'>🌤️ Clima & Alertas Agrícolas</h2>
    <p style='color:#94a3b8;margin:0;font-size:13px;'>
    Condições meteorológicas em tempo real e janela de aplicação de defensivos
    </p></div>
    """, unsafe_allow_html=True)

    d = st.session_state.dados
    cidade = d.get("cidade","")
    if not cidade:
        st.markdown("""
        <div style='background:#1e3a5f;border-radius:12px;padding:20px;text-align:center;
        border:2px dashed #3b82f6;'>
        <div style='font-size:40px;'>🏙️</div>
        <div style='color:#94a3b8;margin-top:8px;'>
        Preencha a <b style='color:#6ee7b7;'>cidade</b> no Cadastro da Área para ver o clima em tempo real.
        </div></div>""", unsafe_allow_html=True)
    else:
        try:
            import requests as rq_
            _r = rq_.get(f"https://wttr.in/{cidade}?format=j1", timeout=10)
            if _r.status_code == 200:
                _w   = _r.json()
                _cur = _w["current_condition"][0]
                _temp_c    = int(_cur.get("temp_C", 0))
                _feels     = int(_cur.get("FeelsLikeC", 0))
                _umid      = int(_cur.get("humidity", 0))
                _vento_kmh = int(_cur.get("windspeedKmph", 0))
                _dir_vento = _cur.get("winddir16Point","—")
                _cond_desc = _cur.get("weatherDesc",[{}])[0].get("value","—")
                _chuva_cur = float(_cur.get("precipMM","0") or 0)
                _uv        = int(_cur.get("uvIndex","0") or 0)
                _visib     = _cur.get("visibility","—")

                # Emoji condição
                _cond_lower = _cond_desc.lower()
                if "thunder" in _cond_lower:       _cond_emoji = "⛈️"
                elif "heavy rain" in _cond_lower:  _cond_emoji = "🌧️"
                elif "rain" in _cond_lower or "drizzle" in _cond_lower: _cond_emoji = "🌦️"
                elif "cloud" in _cond_lower or "overcast" in _cond_lower: _cond_emoji = "☁️"
                elif "fog" in _cond_lower or "mist" in _cond_lower: _cond_emoji = "🌫️"
                elif "snow" in _cond_lower:        _cond_emoji = "❄️"
                elif "sunny" in _cond_lower or "clear" in _cond_lower: _cond_emoji = "☀️"
                else:                              _cond_emoji = "🌤️"

                # Traduz condição
                _trad = {
                    "sunny":"Ensolarado","clear":"Céu limpo","partly cloudy":"Parcialmente nublado",
                    "cloudy":"Nublado","overcast":"Encoberto","light rain":"Chuva fraca",
                    "moderate rain":"Chuva moderada","heavy rain":"Chuva forte",
                    "light drizzle":"Garoa","drizzle":"Garoa","light rain shower":"Pancada fraca",
                    "patchy rain possible":"Chuva possível","thundery outbreaks":"Trovoadas",
                    "blizzard":"Nevasca","fog":"Neblina","mist":"Névoa",
                }
                _cond_pt = next((v for k,v in _trad.items() if k in _cond_lower), _cond_desc)

                # ── Cards clima atual ──────────────────────────────────────────
                _cc1, _cc2, _cc3, _cc4, _cc5 = st.columns(5)
                def _clima_card(col, ico, label, valor, sub="", cor="#22c55e"):
                    col.markdown(f"""
                    <div style='background:#0f3460;border-radius:14px;padding:14px 12px;
                    text-align:center;border:1px solid #1e4976;height:110px;'>
                    <div style='color:#94a3b8;font-size:11px;font-weight:700;letter-spacing:1px;'>{ico} {label}</div>
                    <div style='color:{cor};font-size:26px;font-weight:800;margin:4px 0;'>{valor}</div>
                    <div style='color:#64748b;font-size:11px;'>{sub}</div>
                    </div>""", unsafe_allow_html=True)

                _clima_card(_cc1,"🌡️","TEMPERATURA",f"{_temp_c}°C",f"Sens. {_feels}°C","#f59e0b")
                _clima_card(_cc2,"💧","UMIDADE",f"{_umid}%","","#38bdf8")
                _clima_card(_cc3,"💨","VENTO",f"{_vento_kmh}km/h",f"Dir: {_dir_vento}",
                            "#22c55e" if _vento_kmh<=15 else "#ef4444")
                _clima_card(_cc4,"🌧️","CHUVA",f"{_chuva_cur}mm","Agora","#818cf8")
                _clima_card(_cc5,_cond_emoji,"CONDIÇÃO",_cond_pt,"","#6ee7b7")

                st.markdown("<br>", unsafe_allow_html=True)

                # ── Janela de aplicação — card grande ─────────────────────────
                _ok_vento = _vento_kmh <= 15
                _ok_umid  = 40 <= _umid <= 85
                _ok_temp  = _temp_c <= 30
                _ok_chuva = _chuva_cur == 0
                _score    = sum([_ok_vento, _ok_umid, _ok_temp, _ok_chuva])

                if _score == 4:
                    _jan_cor = "#14532d"; _jan_borda = "#22c55e"
                    _jan_ico = "🟢"; _jan_msg = "JANELA ABERTA"
                    _jan_sub = "Condições ideais para aplicação de defensivos agora!"
                elif _score >= 2:
                    _jan_cor = "#78350f"; _jan_borda = "#f59e0b"
                    _jan_ico = "🟡"; _jan_msg = "JANELA PARCIAL"
                    _jan_sub = "Monitore as condições antes de iniciar a aplicação."
                else:
                    _jan_cor = "#7f1d1d"; _jan_borda = "#ef4444"
                    _jan_ico = "🔴"; _jan_msg = "JANELA FECHADA"
                    _jan_sub = "Condições desfavoráveis — evite aplicações agora."

                st.markdown(f"""
                <div style='background:{_jan_cor};border-radius:16px;padding:18px 24px;
                border:2px solid {_jan_borda};margin:8px 0 16px;'>
                <div style='display:flex;align-items:center;gap:12px;'>
                <div style='font-size:36px;'>{_jan_ico}</div>
                <div>
                <div style='color:#fff;font-size:18px;font-weight:800;letter-spacing:1px;'>
                🚜 JANELA DE APLICAÇÃO — {_jan_msg}</div>
                <div style='color:#fde68a;font-size:13px;margin-top:2px;'>{_jan_sub}</div>
                </div></div>
                <div style='display:flex;gap:16px;margin-top:12px;flex-wrap:wrap;'>
                {"".join([
                    f"<span style='background:rgba(0,0,0,0.3);border-radius:8px;padding:4px 12px;"
                    f"color:{'#6ee7b7' if ok else '#fca5a5'};font-size:12px;font-weight:700;'>"
                    f"{'✅' if ok else '❌'} {lbl}</span>"
                    for ok, lbl in [
                        (_ok_vento, f"Vento {_vento_kmh}km/h ≤15"),
                        (_ok_umid,  f"Umidade {_umid}% 40-85%"),
                        (_ok_temp,  f"Temp {_temp_c}°C ≤30°C"),
                        (_ok_chuva, "Sem chuva agora"),
                    ]
                ])}
                </div></div>
                """, unsafe_allow_html=True)

                # ── Previsão 7 dias — cards por dia ───────────────────────────
                st.markdown("### 📅 Previsão dos próximos dias")
                _weather_days = _w.get("weather", [])

                # Dias da semana em PT
                from datetime import datetime as _dt_c, timedelta as _td
                _dias_pt = ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"]

                _cols_prev = st.columns(min(len(_weather_days), 7))
                for _di, day in enumerate(_weather_days):
                    _d_max  = int(day.get("maxtempC",0))
                    _d_min  = int(day.get("mintempC",0))
                    _d_data = day.get("date","")
                    try:
                        _dt_obj  = _dt_c.strptime(_d_data, "%Y-%m-%d")
                        _dia_sem = _dias_pt[_dt_obj.weekday()]
                        _d_fmt   = f"{_dt_obj.day:02d}/{_dt_obj.month:02d}"
                    except Exception:
                        _dia_sem = ""; _d_fmt = _d_data

                    # Chuva acumulada do dia
                    _d_chuva = sum(
                        float(h.get("precipMM","0") or 0)
                        for h in day.get("hourly",[])
                    )
                    _d_umid  = int(day.get("hourly",[{}])[3].get("humidity","0") or 0)
                    _d_cond  = day.get("hourly",[{}])[3].get("weatherDesc",[{}])[0].get("value","—")
                    _d_cond_l = _d_cond.lower()

                    # Define cor do card por chuva
                    if _d_chuva > 15 or "thunder" in _d_cond_l:
                        _d_bg = "#1e1b4b"; _d_borda = "#818cf8"; _d_alerta = "⛈️ Chuva forte"
                        _d_cor_txt = "#a5b4fc"
                    elif _d_chuva > 5 or "heavy rain" in _d_cond_l:
                        _d_bg = "#1e3a5f"; _d_borda = "#3b82f6"; _d_alerta = "🌧️ Chuva"
                        _d_cor_txt = "#93c5fd"
                    elif _d_chuva > 0.5 or "rain" in _d_cond_l or "drizzle" in _d_cond_l:
                        _d_bg = "#0f2d4a"; _d_borda = "#0ea5e9"; _d_alerta = "🌦️ Chuva fraca"
                        _d_cor_txt = "#7dd3fc"
                    elif "cloud" in _d_cond_l or "overcast" in _d_cond_l:
                        _d_bg = "#1e293b"; _d_borda = "#475569"; _d_alerta = "☁️ Nublado"
                        _d_cor_txt = "#94a3b8"
                    else:
                        _d_bg = "#14532d"; _d_borda = "#22c55e"; _d_alerta = "☀️ Bom dia"
                        _d_cor_txt = "#6ee7b7"

                    with _cols_prev[_di]:
                        st.markdown(f"""
                        <div style='background:{_d_bg};border-radius:14px;padding:14px 10px;
                        text-align:center;border:2px solid {_d_borda};margin:2px;'>
                        <div style='color:{_d_cor_txt};font-size:12px;font-weight:800;
                        letter-spacing:1px;'>{_dia_sem}</div>
                        <div style='color:#94a3b8;font-size:11px;'>{_d_fmt}</div>
                        <div style='font-size:22px;margin:6px 0;'>
                        {"⛈️" if "thunder" in _d_cond_l else "🌧️" if _d_chuva>5 else "🌦️" if _d_chuva>0.5 else "☁️" if "cloud" in _d_cond_l else "☀️"}
                        </div>
                        <div style='color:#f1f5f9;font-size:15px;font-weight:800;'>{_d_max}°</div>
                        <div style='color:#64748b;font-size:12px;'>{_d_min}°</div>
                        <div style='color:{_d_cor_txt};font-size:11px;font-weight:700;
                        margin-top:6px;'>{_d_alerta}</div>
                        <div style='color:#94a3b8;font-size:11px;margin-top:2px;'>
                        💧{_d_chuva:.1f}mm</div>
                        </div>""", unsafe_allow_html=True)

                # ── Alertas automáticos para os próximos dias ─────────────────
                st.markdown("<br>", unsafe_allow_html=True)
                _alertas_clima = []
                for _di, day in enumerate(_weather_days):
                    _d_chuva_t = sum(float(h.get("precipMM","0") or 0) for h in day.get("hourly",[]))
                    _d_cond_t  = day.get("hourly",[{}])[3].get("weatherDesc",[{}])[0].get("value","").lower()
                    _d_data_t  = day.get("date","")
                    try:
                        _dt_t = _dt_c.strptime(_d_data_t,"%Y-%m-%d")
                        _d_str = f"{_dt_t.day:02d}/{_dt_t.month:02d}"
                    except: _d_str = _d_data_t
                    if "thunder" in _d_cond_t:
                        _alertas_clima.append(("🔴","#7f1d1d","#ef4444",f"{_d_str} — Risco de trovoadas! Não aplique defensivos."))
                    elif _d_chuva_t > 10:
                        _alertas_clima.append(("🟠","#78350f","#f97316",f"{_d_str} — Chuva prevista {_d_chuva_t:.0f}mm. Aguarde janela seca."))
                    elif _d_chuva_t > 2:
                        _alertas_clima.append(("🟡","#713f12","#fbbf24",f"{_d_str} — Chuva leve {_d_chuva_t:.1f}mm. Monitore antes de aplicar."))

                if _alertas_clima:
                    st.markdown("#### 🔔 Alertas Agrícolas")
                    for _ico_a, _bg_a, _bd_a, _msg_a in _alertas_clima:
                        st.markdown(f"""
                        <div style='background:{_bg_a};border-radius:10px;padding:10px 16px;
                        border-left:4px solid {_bd_a};margin:4px 0;'>
                        <span style='color:#fff;font-weight:600;font-size:13px;'>
                        {_ico_a} {_msg_a}</span></div>""", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background:#14532d;border-radius:10px;padding:10px 16px;
                    border-left:4px solid #22c55e;margin:4px 0;'>
                    <span style='color:#fff;font-weight:600;font-size:13px;'>
                    ✅ Sem alertas para os próximos dias — clima favorável para operações agrícolas!
                    </span></div>""", unsafe_allow_html=True)

            else:
                st.info(f"Clima para '{cidade}' indisponível no momento.")
        except Exception as e:
            st.info(f"Serviço de clima temporariamente indisponível. ({e})")

if menu == "🌍 Inteligência":
  with _sub_int[1]:

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f3460,#1a4a73);border-radius:16px;
    padding:20px 24px;margin-bottom:20px;border:1px solid #22c55e33;'>
    <h2 style='color:#6ee7b7;margin:0 0 4px;font-size:22px;'>💰 Preços de Mercado</h2>
    <p style='color:#94a3b8;margin:0;font-size:13px;'>
    Cotações CEPEA/ESALQ em tempo real — mercado físico brasileiro
    </p></div>
    """, unsafe_allow_html=True)

    # ── Busca dólar (robusto) ─────────────────────────────────────────────────
    _dolar_val  = 0.0
    _dolar_fonte = "—"
    try:
        _d_res = buscar_dolar_awesomeapi()
        if isinstance(_d_res, dict):
            _dolar_val  = float(_d_res.get("preco", 0) or 0)
            _dolar_fonte = _d_res.get("fonte", "—")
        elif isinstance(_d_res, (int, float)):
            _dolar_val = float(_d_res)
    except Exception:
        pass
    if _dolar_val <= 0:
        _dolar_val = 5.80
        _dolar_fonte = "Offline"

    # ── Card do dólar sempre visível ──────────────────────────────────────────
    _dol_c1, _dol_c2, _dol_c3 = st.columns([1.5, 1.5, 3])
    _dol_c1.markdown(f"""
    <div style='background:linear-gradient(135deg,#1e3a5f,#0f2d4a);border-radius:14px;
    padding:16px 18px;border:2px solid #3b82f6;text-align:center;'>
    <div style='color:#93c5fd;font-size:11px;font-weight:800;letter-spacing:2px;'>💵 DÓLAR USD/BRL</div>
    <div style='color:#fff;font-size:28px;font-weight:900;margin:6px 0;'>
    R$ {_dolar_val:.4f}</div>
    <div style='color:#64748b;font-size:10px;'>{_dolar_fonte}</div>
    </div>""", unsafe_allow_html=True)
    _dol_c2.markdown(f"""
    <div style='background:linear-gradient(135deg,#1e1b4b,#0f172a);border-radius:14px;
    padding:16px 18px;border:2px solid #818cf8;text-align:center;'>
    <div style='color:#a5b4fc;font-size:11px;font-weight:800;letter-spacing:2px;'>📅 ATUALIZAÇÃO</div>
    <div style='color:#fff;font-size:16px;font-weight:700;margin:6px 0;'>
    {datetime.now().strftime("%d/%m/%Y")}</div>
    <div style='color:#64748b;font-size:10px;'>{datetime.now().strftime("%H:%M")}</div>
    </div>""", unsafe_allow_html=True)

    # Botão atualizar na terceira coluna
    with _dol_c3:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Atualizar Cotações CEPEA", key="btn_buscar_precos",
                     use_container_width=True, type="primary"):
            # Verifica cache — bloqueia se atualizou há menos de 5 minutos
            _ts_ultimo = st.session_state.get("_precos_ts_unix", 0)
            _seg_desde = datetime.now().timestamp() - _ts_ultimo
            if _ts_ultimo > 0 and _seg_desde < 300:
                _resta = int(300 - _seg_desde)
                st.warning(f"⏳ Aguarde {_resta}s para atualizar novamente (limite de requisições).")
            else:
                with st.spinner("🌐 Buscando cotações CEPEA via IA..."):
                    try:
                        _precos_novos = buscar_precos_cepea_ia()
                        if isinstance(_precos_novos, dict) and _precos_novos:
                            st.session_state["_precos_mercado"]  = _precos_novos
                            st.session_state["_precos_ts"]       = datetime.now().strftime("%H:%M:%S")
                            st.session_state["_precos_ts_unix"]  = datetime.now().timestamp()
                            st.session_state["_cepea_erro"]      = ""
                            st.rerun()
                        else:
                            _err = st.session_state.get("_cepea_erro","Sem resposta")
                            if "429" in str(_err) or "rate_limit" in str(_err).lower():
                                st.error("⏱️ Muitas requisições — aguarde alguns minutos e tente novamente.")
                            elif "API key" in str(_err):
                                st.error("🔑 API Key não configurada. Verifique os Secrets do Streamlit Cloud.")
                            else:
                                st.warning(f"⚠️ Não foi possível buscar preços: {_err}")
                    except Exception as _ex:
                        st.error(f"Erro: {_ex}")
        if st.session_state.get("_precos_ts"):
            st.caption(f"⏱️ Última atualização: {st.session_state['_precos_ts']}")
        _err_show = st.session_state.get("_cepea_erro","")
        if _err_show:
            if "429" in str(_err_show) or "rate_limit" in str(_err_show).lower():
                st.caption("⏱️ Rate limit atingido — aguarde alguns minutos")
            elif "API key" in str(_err_show):
                st.caption("🔑 Verifique a ANTHROPIC_API_KEY nos Secrets")
            elif _err_show:
                st.caption(f"ℹ️ {str(_err_show)[:80]}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Cards das commodities ─────────────────────────────────────────────────
    _precos_cache = st.session_state.get("_precos_mercado") or {}

    COMM_DEF = [
        {"key":"soja",    "nome":"Soja",     "emoji":"🌱", "unid":"R$/sc 60kg", "cor":"#14532d", "borda":"#22c55e"},
        {"key":"milho",   "nome":"Milho",    "emoji":"🌽", "unid":"R$/sc 60kg", "cor":"#713f12", "borda":"#f59e0b"},
        {"key":"trigo",   "nome":"Trigo",    "emoji":"🌾", "unid":"R$/sc 60kg", "cor":"#1e3a5f", "borda":"#38bdf8"},
        {"key":"cafe",    "nome":"Café",     "emoji":"☕", "unid":"R$/sc 60kg", "cor":"#3b1f0a", "borda":"#d97706"},
        {"key":"algodao", "nome":"Algodão",  "emoji":"🏷️", "unid":"R$/@",       "cor":"#1e1b4b", "borda":"#818cf8"},
        {"key":"boi",     "nome":"Boi Gordo","emoji":"🐄", "unid":"R$/@",       "cor":"#3b0f0f", "borda":"#f87171"},
        {"key":"arroz",   "nome":"Arroz",    "emoji":"🍚", "unid":"R$/sc 50kg", "cor":"#0f3460", "borda":"#60a5fa"},
    ]

    if isinstance(_precos_cache, dict) and len(_precos_cache) >= 3:
        _cols_comm = st.columns(4)
        _comm_count = 0
        for comm in COMM_DEF:
            _val_raw = _precos_cache.get(comm["key"])
            if _val_raw is None:
                continue
            try:
                _val_f = float(_val_raw)
                if _val_f <= 0:
                    continue
            except Exception:
                continue

            with _cols_comm[_comm_count % 4]:
                st.markdown(f"""
                <div style='background:linear-gradient(135deg,{comm["cor"]},{comm["cor"]}cc);
                border-radius:14px;padding:16px 14px;border:2px solid {comm["borda"]};
                margin-bottom:10px;text-align:center;'>
                <div style='font-size:24px;margin-bottom:4px;'>{comm["emoji"]}</div>
                <div style='color:#94a3b8;font-size:11px;font-weight:800;letter-spacing:1px;'>
                {comm["nome"].upper()}</div>
                <div style='color:#fff;font-size:22px;font-weight:900;margin:6px 0;'>
                R$ {_val_f:,.2f}</div>
                <div style='background:rgba(0,0,0,0.3);color:{comm["borda"]};font-size:10px;
                font-weight:700;padding:2px 8px;border-radius:20px;display:inline-block;'>
                {comm["unid"]}</div>
                </div>""", unsafe_allow_html=True)
            _comm_count += 1

        _fonte_p = _precos_cache.get("fonte","CEPEA")
        _data_p  = _precos_cache.get("data","")
        _mercado = _precos_cache.get("mercado","")
        _is_fisico = "fisico" in str(_mercado).lower() or "cepea" in str(_fonte_p).lower()

        if _is_fisico:
            st.markdown(f"""
            <div style='background:#14532d;border-radius:8px;padding:8px 14px;
            border-left:4px solid #22c55e;margin:6px 0;'>
            <span style='color:#6ee7b7;font-size:12px;font-weight:700;'>
            ✅ Mercado Físico Brasileiro — {_fonte_p}{f' — {_data_p}' if _data_p else ''}
            </span></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background:#78350f;border-radius:8px;padding:8px 14px;
            border-left:4px solid #f59e0b;margin:6px 0;'>
            <span style='color:#fde68a;font-size:12px;font-weight:700;'>
            ⚠️ Atenção: preços podem ser referência CBOT/Bolsa convertidos para R$ — não representa o mercado físico local.
            Fonte: {_fonte_p}{f' — {_data_p}' if _data_p else ''}
            </span></div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style='background:#0f3460;border-radius:12px;padding:24px;text-align:center;
        border:2px dashed #1e4976;margin:10px 0;'>
        <div style='font-size:40px;'>📊</div>
        <div style='color:#94a3b8;font-size:15px;margin-top:8px;'>
        Clique em <b style='color:#22c55e;'>🔄 Atualizar Cotações CEPEA</b> para carregar os preços.
        </div>
        <div style='color:#64748b;font-size:12px;margin-top:6px;'>
        Dados via IA com web search — CEPEA/ESALQ mercado físico
        </div></div>""", unsafe_allow_html=True)

    # ── Acompanhamento manual ─────────────────────────────────────────────────
    st.divider()
    with st.expander("📈 Registrar cotação manual para histórico"):
        col_gr1, col_gr2, col_gr3 = st.columns(3)
        _p_soja  = col_gr1.number_input("Soja R$/sc",  min_value=0.0, key="num_p_soja_graf")
        _p_milho = col_gr2.number_input("Milho R$/sc", min_value=0.0, key="num_p_milho_graf")
        _p_trigo = col_gr3.number_input("Trigo R$/sc", min_value=0.0, key="num_p_trigo_graf")
        if st.button("📊 Registrar cotação", key="btn_reg_cotacao"):
            if "historico_cotacoes" not in st.session_state:
                st.session_state["historico_cotacoes"] = []
            st.session_state["historico_cotacoes"].append({
                "data":  datetime.now().strftime("%d/%m %H:%M"),
                "Soja":  _p_soja, "Milho": _p_milho, "Trigo": _p_trigo,
            })
            st.rerun()
        if st.session_state.get("historico_cotacoes"):
            import pandas as _pd_cot
            df_cot = _pd_cot.DataFrame(st.session_state["historico_cotacoes"]).set_index("data")
            st.line_chart(df_cot)

    st.markdown("""
    <div style='background:#1e3a5f;border-radius:8px;padding:10px 14px;
    border-left:4px solid #eab308;margin-top:8px;'>
    <b style='color:#eab308;'>⚠️ Aviso</b>
    <span style='color:#f1f5f9;font-size:12px;'>
    Preços CEPEA/ESALQ são referências do mercado físico brasileiro.
    O preço real de venda depende da praça, base e câmbio do dia.
    Consulte seu corretor antes de fechar negócio.
    </span></div>
    """, unsafe_allow_html=True)

if menu == "🌍 Inteligência":
  with _sub_int[2]:
    st.header("🗺️ Mapa de Colheita IA")
    st.markdown("""
    <div style='background:#0f3460;border-radius:10px;padding:12px 16px;
    border-left:5px solid #22c55e;margin-bottom:12px;'>
    <b style='color:#22c55e;'>🛰️ Análise de Mapa de Colheita</b><br>
    <span style='color:#f1f5f9;font-size:13px;'>
    Faça upload do mapa de colheita (imagem ou PDF) e a IA irá identificar
    zonas de produtividade, variabilidade e recomendar manejo por zonas.
    </span></div>
    """, unsafe_allow_html=True)

    _arquivo_mapa = st.file_uploader(
        "📂 Upload do mapa de colheita (JPG, PNG, PDF)",
        type=["jpg","jpeg","png","pdf"],
        key="upload_mapa_colheita"
    )

    if _arquivo_mapa:
        if _arquivo_mapa.type.startswith("image"):
            st.image(_arquivo_mapa, caption="Mapa carregado", use_column_width=True)
        else:
            st.info(f"Arquivo PDF carregado: {_arquivo_mapa.name}")

        col_mc1, col_mc2 = st.columns(2)
        _area_mc    = col_mc1.number_input("Área do mapa (ha)", min_value=0.0,
                                             value=float(st.session_state.dados.get("area",0)),
                                             key="num_area_mapa_colheita")
        _cultura_mc = col_mc2.selectbox("Cultura", get_culturas(), key="sel_cult_mapa_colheita")
        _obs_mc     = st.text_area("Observações sobre o mapa", key="txt_obs_mapa_colheita",
                                    placeholder="Ex: Mapa 2024/25, produtividade média esperada 60 sc/ha")

        if st.button("🤖 Analisar Mapa com IA", key="btn_analisar_mapa", use_container_width=True):
            with st.spinner("Analisando mapa com IA..."):
                try:
                    import requests as _rq_mapa, base64 as _b64_mapa
                    _api_key_mapa = st.secrets.get("ANTHROPIC_API_KEY","")

                    _txt_mapa = (f"Analise este mapa de colheita agrícola. "
                                 f"Cultura: {cultura_limpa(_cultura_mc)}, Área: {_area_mc} ha. "
                                 f"Obs: {_obs_mc}. "
                                 "Identifique: 1) Zonas de alta e baixa produtividade, "
                                 "2) Variabilidade espacial, "
                                 "3) Possíveis causas das variações, "
                                 "4) Recomendações de manejo por zonas. "
                                 "Responda em português, de forma prática para o produtor.")

                    _content_mapa = []
                    # Adiciona imagem se for imagem
                    if _arquivo_mapa.type.startswith("image"):
                        _img_b64 = _b64_mapa.b64encode(_arquivo_mapa.read()).decode()
                        _ext = "jpeg" if "jpg" in _arquivo_mapa.type else "png"
                        _content_mapa.append({
                            "type": "image",
                            "source": {"type": "base64", "media_type": f"image/{_ext}", "data": _img_b64}
                        })
                    _content_mapa.append({"type": "text", "text": _txt_mapa})

                    _resp_mapa = _rq_mapa.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": _api_key_mapa,
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json",
                        },
                        json={
                            "model": "claude-sonnet-4-5",
                            "max_tokens": 1500,
                            "messages": [{"role":"user","content":_content_mapa}],
                        },
                        timeout=60
                    )
                    _analise = _resp_mapa.json().get("content",[{}])[0].get("text","Sem resposta.")
                    st.session_state["_analise_mapa"] = _analise
                except Exception as e:
                    st.error(f"Erro na análise: {e}")

    if st.session_state.get("_analise_mapa"):
        st.divider()
        st.subheader("🤖 Análise da IA")
        st.markdown(st.session_state["_analise_mapa"])
    elif not _arquivo_mapa:
        st.info("Faça o upload do mapa de colheita para análise.")

if menu == "🌍 Inteligência":
  with _sub_int[3]:

    # ── Header ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f3460,#1a4a73);border-radius:16px;
    padding:20px 24px;margin-bottom:20px;border:1px solid #22c55e33;'>
    <h2 style='color:#6ee7b7;margin:0 0 4px;font-size:22px;'>📅 Planejamento & Calendário Agrícola</h2>
    <p style='color:#94a3b8;margin:0;font-size:13px;'>
    Rotação inverno/verão, janelas de plantio e eventos da propriedade
    </p></div>""", unsafe_allow_html=True)

    if "calendario_eventos" not in st.session_state:
        st.session_state.calendario_eventos = []
    if "planejamento_safras" not in st.session_state:
        st.session_state.planejamento_safras = []

    # ── ABAS DO MÓDULO ────────────────────────────────────────────────────────
    _tab_cal, _tab_plan, _tab_rot = st.tabs([
        "📅 Eventos", "🌾 Planejamento de Safras", "🔄 Rotação de Culturas"
    ])

    # ════════════════════════════════════════════════════════════════════════
    # ABA 1 — EVENTOS
    # ════════════════════════════════════════════════════════════════════════
    with _tab_cal:
        st.markdown("#### ➕ Novo Evento Agrícola")

        _tipos_ev = [
            "🌱 Plantio","🚜 Aplicação de defensivo","🪨 Aplicação de calcário/gesso",
            "🌾 Colheita","🧪 Análise de solo","💧 Irrigação","🌧️ Registro de chuva",
            "🔧 Manutenção de máquinas","📋 Vistoria técnica","📦 Recebimento de insumos",
            "💰 Venda de grãos","🤝 Reunião/Visita técnica","⚠️ Evento climático","📝 Outro"
        ]
        _cores_ev = {
            "🌱 Plantio":"#14532d","🚜 Aplicação de defensivo":"#1e3a5f",
            "🪨 Aplicação de calcário/gesso":"#3b1f0a","🌾 Colheita":"#713f12",
            "🧪 Análise de solo":"#1e1b4b","💧 Irrigação":"#0c4a6e",
            "🌧️ Registro de chuva":"#0f172a","🔧 Manutenção de máquinas":"#1c1917",
            "📋 Vistoria técnica":"#14532d","📦 Recebimento de insumos":"#064e3b",
            "💰 Venda de grãos":"#78350f","🤝 Reunião/Visita técnica":"#312e81",
            "⚠️ Evento climático":"#7f1d1d","📝 Outro":"#1e293b"
        }
        _bordas_ev = {
            "🌱 Plantio":"#22c55e","🚜 Aplicação de defensivo":"#3b82f6",
            "🪨 Aplicação de calcário/gesso":"#d97706","🌾 Colheita":"#f59e0b",
            "🧪 Análise de solo":"#818cf8","💧 Irrigação":"#38bdf8",
            "🌧️ Registro de chuva":"#60a5fa","🔧 Manutenção de máquinas":"#78716c",
            "📋 Vistoria técnica":"#4ade80","📦 Recebimento de insumos":"#10b981",
            "💰 Venda de grãos":"#f97316","🤝 Reunião/Visita técnica":"#a78bfa",
            "⚠️ Evento climático":"#ef4444","📝 Outro":"#64748b"
        }

        with st.form("form_evento_cal", clear_on_submit=True):
            col_e1, col_e2 = st.columns(2)
            _ev_titulo = col_e1.text_input("Título do evento *", placeholder="Ex: Plantio soja talhão A")
            _ev_data   = col_e2.date_input("Data *", key="dat_ev_data")
            col_e3, col_e4 = st.columns(2)
            _ev_tipo   = col_e3.selectbox("Tipo de evento", _tipos_ev, key="sel_ev_tipo")
            _ev_area   = col_e4.selectbox("Área/Talhão",
                ["Toda a propriedade"] + [f"{a.get('ID')} - {a.get('Talhão','')}" for a in st.session_state.areas],
                key="sel_ev_area")
            _ev_obs    = st.text_area("Observações", key="txt_ev_obs", height=60)
            _ev_alerta = st.checkbox("🔔 Criar alerta (aparece nos próximos eventos)", value=True, key="chk_ev_alerta")
            _ev_salvar = st.form_submit_button("💾 Salvar Evento", use_container_width=True)

        if _ev_salvar:
            if _ev_titulo.strip():
                st.session_state.calendario_eventos.append({
                    "Título": _ev_titulo.strip(), "Data": str(_ev_data),
                    "Tipo": _ev_tipo, "Área": _ev_area,
                    "Obs": _ev_obs, "Alerta": _ev_alerta,
                    "Concluído": False,
                })
                salvar_dados_iaagro()
                success_box(f"✅ Evento '{_ev_titulo}' salvo!")
                st.rerun()

        # Eventos próximos (7 dias)
        from datetime import date as _date_cal, timedelta as _td_cal
        _hoje_cal = _date_cal.today()
        _proximos = []
        for _ev in st.session_state.calendario_eventos:
            try:
                _d = _date_cal.fromisoformat(_ev.get("Data",""))
                _diff = (_d - _hoje_cal).days
                if 0 <= _diff <= 7 and not _ev.get("Concluído"):
                    _proximos.append((_diff, _ev))
            except Exception:
                pass

        if _proximos:
            st.markdown("#### 🔔 Próximos 7 dias")
            for _diff_d, _ev in sorted(_proximos):
                _cor  = _cores_ev.get(_ev.get("Tipo","📝 Outro"), "#1e293b")
                _bord = _bordas_ev.get(_ev.get("Tipo","📝 Outro"), "#64748b")
                _quando = "Hoje!" if _diff_d == 0 else f"Em {_diff_d} dia{'s' if _diff_d>1 else ''}"
                st.markdown(f"""
                <div style='background:{_cor};border-radius:10px;padding:10px 16px;
                border-left:4px solid {_bord};margin:4px 0;
                display:flex;justify-content:space-between;align-items:center;'>
                <div>
                <span style='color:#fff;font-weight:700;font-size:13px;'>{_ev.get('Tipo','')} {_ev.get('Título','')}</span><br>
                <span style='color:rgba(255,255,255,0.5);font-size:11px;'>{_ev.get('Área','')} &nbsp;·&nbsp; {_ev.get('Obs','')[:40]}</span>
                </div>
                <span style='color:{_bord};font-weight:800;font-size:12px;white-space:nowrap;margin-left:12px;'>{_quando}</span>
                </div>""", unsafe_allow_html=True)

        # Lista completa
        st.markdown("#### 📋 Todos os Eventos")
        if st.session_state.calendario_eventos:
            _fil_tipo = st.selectbox("Filtrar por tipo", ["Todos"] + _tipos_ev, key="fil_tipo_ev")
            _fil_area_ev = st.selectbox("Filtrar por área", ["Todas"] +
                [f"{a.get('ID')} - {a.get('Talhão','')}" for a in st.session_state.areas],
                key="fil_area_ev")

            _evs_sorted = sorted(st.session_state.calendario_eventos,
                                  key=lambda x: x.get("Data",""), reverse=True)
            for _idx_ev, _ev in enumerate(_evs_sorted):
                if _fil_tipo != "Todos" and _ev.get("Tipo") != _fil_tipo:
                    continue
                if _fil_area_ev != "Todas" and _ev.get("Área","") not in ("Toda a propriedade", _fil_area_ev):
                    continue
                _cor  = _cores_ev.get(_ev.get("Tipo","📝 Outro"), "#1e293b")
                _bord = _bordas_ev.get(_ev.get("Tipo","📝 Outro"), "#64748b")
                _concl = _ev.get("Concluído", False)
                _opcity = "0.5" if _concl else "1"
                _c1, _c2, _c3 = st.columns([6, 1, 1])
                _c1.markdown(f"""
                <div style='background:{_cor};border-radius:8px;padding:8px 14px;
                border-left:3px solid {_bord};opacity:{_opcity};'>
                <span style='color:#fff;font-weight:700;font-size:12px;'>
                {"~~" if _concl else ""}{_ev.get("Tipo","")} {_ev.get("Título","")}{"~~" if _concl else ""}
                </span><br>
                <span style='color:rgba(255,255,255,0.5);font-size:11px;'>
                📅 {_ev.get("Data","")} &nbsp;·&nbsp; {_ev.get("Área","")}
                </span></div>""", unsafe_allow_html=True)
                if not _concl:
                    if _c2.button("✅", key=f"concl_ev_{_idx_ev}", help="Marcar como concluído"):
                        _idx_orig = st.session_state.calendario_eventos.index(_ev)
                        st.session_state.calendario_eventos[_idx_orig]["Concluído"] = True
                        salvar_dados_iaagro()
                        st.rerun()
                if _c3.button("🗑️", key=f"del_ev_{_idx_ev}", help="Excluir"):
                    _idx_orig = st.session_state.calendario_eventos.index(_ev)
                    st.session_state.calendario_eventos.pop(_idx_orig)
                    salvar_dados_iaagro()
                    st.rerun()
        else:
            st.info("Nenhum evento cadastrado ainda.")

    # ════════════════════════════════════════════════════════════════════════
    # ABA 2 — PLANEJAMENTO DE SAFRAS
    # ════════════════════════════════════════════════════════════════════════
    with _tab_plan:
        st.markdown("#### 🌾 Planejar Safra por Talhão")

        CULTURAS_INVERNO = [
            "🌾 Trigo","🌿 Aveia Branca","🌿 Aveia Preta","🌾 Cevada","🌻 Canola",
            "🌿 Azevém (pastagem)","🌱 Ervilhaca (cobertura)","🌱 Nabo Forrageiro (cobertura)",
            "🌿 Mix de Cobertura (aveia+nabo+ervilhaca)","🌿 Pousio Planejado",
        ]
        CULTURAS_VERAO = [
            "🌱 Soja","🌽 Milho 1ª safra","🌽 Milho 2ª safra (safrinha)",
            "🌱 Feijão","🌻 Girassol","☕ Café","🍠 Mandioca",
            "🌾 Sorgo","🍚 Arroz","🏷️ Algodão",
        ]

        JANELAS_PLANTIO = {
            "🌾 Trigo":         {"inicio":"Abr","fim":"Jun","colheita":"Set/Out","dias":120},
            "🌿 Aveia Branca":  {"inicio":"Abr","fim":"Jun","colheita":"Set/Out","dias":110},
            "🌿 Aveia Preta":   {"inicio":"Mar","fim":"Jun","colheita":"Jul/Ago","dias":90},
            "🌾 Cevada":        {"inicio":"Mai","fim":"Jun","colheita":"Set/Out","dias":115},
            "🌻 Canola":        {"inicio":"Abr","fim":"Mai","colheita":"Set/Out","dias":130},
            "🌿 Azevém (pastagem)": {"inicio":"Mar","fim":"Mai","colheita":"Pastejo","dias":60},
            "🌿 Mix de Cobertura (aveia+nabo+ervilhaca)": {"inicio":"Mar","fim":"Mai","colheita":"Dessecação","dias":90},
            "🌱 Soja":          {"inicio":"Out","fim":"Nov","colheita":"Fev/Mar","dias":125},
            "🌽 Milho 1ª safra":{"inicio":"Set","fim":"Nov","colheita":"Fev/Mar","dias":130},
            "🌽 Milho 2ª safra (safrinha)": {"inicio":"Jan","fim":"Fev","colheita":"Jun/Jul","dias":120},
            "🌱 Feijão":        {"inicio":"Out","fim":"Nov","colheita":"Jan/Fev","dias":90},
        }

        ROTACOES_RECOMENDADAS = {
            "🌱 Soja":  {"inverno_ideal": ["🌾 Trigo","🌿 Aveia Branca","🌻 Canola"], "motivo": "Trigo/aveia após soja quebra ciclo de doenças"},
            "🌽 Milho 1ª safra": {"inverno_ideal": ["🌿 Aveia Preta","🌿 Mix de Cobertura (aveia+nabo+ervilhaca)","🌿 Azevém (pastagem)"], "motivo": "Coberturas após milho melhoram MO"},
            "🌾 Trigo": {"verao_ideal": ["🌱 Soja","🌽 Milho 1ª safra"], "motivo": "Soja/milho após trigo otimiza NPK"},
            "🌿 Aveia Branca": {"verao_ideal": ["🌱 Soja","🌱 Feijão"], "motivo": "Aveia como antecedente da soja é ideal no PR/SC"},
        }

        if not st.session_state.areas:
            st.info("Cadastre áreas para planejar safras.")
        else:
            _area_plan = st.selectbox("Selecione o talhão",
                [f"{a.get('ID')} - {a.get('Talhão','')} ({a.get('Cultura','?')})"
                 for a in st.session_state.areas], key="sel_area_plan")
            _id_plan = _area_plan.split(" - ")[0]
            _area_obj = next((a for a in st.session_state.areas if a.get("ID") == _id_plan), {})

            col_pl1, col_pl2 = st.columns(2)

            with col_pl1:
                st.markdown("""<div style='background:#1e3a5f;border-radius:10px;padding:10px 14px;
                border-top:3px solid #38bdf8;margin-bottom:8px;'>
                <span style='color:#38bdf8;font-weight:800;font-size:12px;letter-spacing:1px;'>
                ❄️ SAFRA DE INVERNO</span></div>""", unsafe_allow_html=True)
                _cult_inv = st.selectbox("Cultura de inverno", CULTURAS_INVERNO, key="sel_cult_inv")
                _ano_inv  = st.selectbox("Ano", [2025,2026,2027], key="sel_ano_inv")
                _area_inv = st.number_input("Área (ha)", min_value=0.0,
                    value=float(_area_obj.get("Hectares",0)), key="num_area_inv")
                _prod_inv = st.number_input("Meta produtividade (sc/ha)", min_value=0.0, key="num_prod_inv")
                _obs_inv  = st.text_input("Observações", key="txt_obs_inv")

            with col_pl2:
                st.markdown("""<div style='background:#14532d;border-radius:10px;padding:10px 14px;
                border-top:3px solid #22c55e;margin-bottom:8px;'>
                <span style='color:#22c55e;font-weight:800;font-size:12px;letter-spacing:1px;'>
                ☀️ SAFRA DE VERÃO</span></div>""", unsafe_allow_html=True)
                _cult_ver = st.selectbox("Cultura de verão", CULTURAS_VERAO, key="sel_cult_ver")
                _ano_ver  = st.selectbox("Ano", [2025,2026,2027], key="sel_ano_ver",
                    index=[2025,2026,2027].index(min(2027, _ano_inv + (1 if _ano_inv in [2025,2026,2027] else 0))))
                _area_ver = st.number_input("Área (ha)", min_value=0.0,
                    value=float(_area_obj.get("Hectares",0)), key="num_area_ver")
                _prod_ver = st.number_input("Meta produtividade (sc/ha)", min_value=0.0,
                    value=float(_area_obj.get("Meta Produtividade",0)), key="num_prod_ver")
                _obs_ver  = st.text_input("Observações", key="txt_obs_ver")

            # Sugestão de rotação
            _cult_ver_limpa = _cult_ver.split(" ",1)[1] if " " in _cult_ver else _cult_ver
            _rot_rec = ROTACOES_RECOMENDADAS.get(_cult_ver)
            if _rot_rec:
                _inv_ideais = _rot_rec.get("inverno_ideal",[])
                _is_ideal = _cult_inv in _inv_ideais
                _bg_rot = "#14532d" if _is_ideal else "#78350f"
                _brd_rot = "#22c55e" if _is_ideal else "#f59e0b"
                _ico_rot = "✅" if _is_ideal else "⚠️"
                st.markdown(f"""
                <div style='background:{_bg_rot};border-radius:10px;padding:10px 16px;
                border-left:4px solid {_brd_rot};margin:12px 0;'>
                <span style='color:#fff;font-weight:700;font-size:12px;'>
                {_ico_rot} Rotação: {_rot_rec.get('motivo','')}</span><br>
                <span style='color:rgba(255,255,255,0.6);font-size:11px;'>
                Inverno ideal após {_cult_ver}: {", ".join(_inv_ideais[:3])}
                </span></div>""", unsafe_allow_html=True)

            # Janela de plantio
            _jan_inv = JANELAS_PLANTIO.get(_cult_inv)
            _jan_ver = JANELAS_PLANTIO.get(_cult_ver)
            if _jan_inv or _jan_ver:
                st.markdown("**📅 Janelas de Plantio — Sul do Brasil (PR/SC/RS)**")
                _jc1, _jc2 = st.columns(2)
                if _jan_inv:
                    _jc1.markdown(f"""
                    <div style='background:#1e3a5f;border-radius:8px;padding:10px;
                    border-left:3px solid #38bdf8;font-size:12px;'>
                    <b style='color:#38bdf8;'>❄️ {_cult_inv}</b><br>
                    🗓️ Plantio: {_jan_inv['inicio']} a {_jan_inv['fim']}<br>
                    🌾 Colheita: {_jan_inv['colheita']}<br>
                    ⏱️ Ciclo: ~{_jan_inv['dias']} dias
                    </div>""", unsafe_allow_html=True)
                if _jan_ver:
                    _jc2.markdown(f"""
                    <div style='background:#14532d;border-radius:8px;padding:10px;
                    border-left:3px solid #22c55e;font-size:12px;'>
                    <b style='color:#22c55e;'>☀️ {_cult_ver}</b><br>
                    🗓️ Plantio: {_jan_ver['inicio']} a {_jan_ver['fim']}<br>
                    🌾 Colheita: {_jan_ver['colheita']}<br>
                    ⏱️ Ciclo: ~{_jan_ver['dias']} dias
                    </div>""", unsafe_allow_html=True)

            if st.button("💾 Salvar Planejamento", key="btn_salvar_plan",
                         use_container_width=True, type="primary"):
                _plan_entry = {
                    "id_area": _id_plan, "talhao": _area_obj.get("Talhão",""),
                    "inverno": {"cultura": _cult_inv, "ano": _ano_inv, "area": _area_inv,
                                "meta": _prod_inv, "obs": _obs_inv},
                    "verao":   {"cultura": _cult_ver, "ano": _ano_ver, "area": _area_ver,
                                "meta": _prod_ver, "obs": _obs_ver},
                    "data_planejamento": str(_date_cal.today()),
                }
                # Remove planejamento anterior do mesmo talhão+ano e insere novo
                st.session_state.planejamento_safras = [
                    p for p in st.session_state.planejamento_safras
                    if not (p.get("id_area") == _id_plan and
                            p.get("inverno",{}).get("ano") == _ano_inv)
                ]
                st.session_state.planejamento_safras.append(_plan_entry)

                # Gera eventos automáticos no calendário
                if _jan_inv:
                    _mes_inicio = {"Jan":1,"Fev":2,"Mar":3,"Abr":4,"Mai":5,"Jun":6,
                                    "Jul":7,"Ago":8,"Set":9,"Out":10,"Nov":11,"Dez":12}
                    _m_ini = _mes_inicio.get(_jan_inv["inicio"],4)
                    from datetime import date as _d2
                    _data_plant_inv = _d2(_ano_inv, _m_ini, 1)
                    st.session_state.calendario_eventos.append({
                        "Título": f"Plantio {_cult_inv} — {_area_obj.get('Talhão','')}",
                        "Data": str(_data_plant_inv),
                        "Tipo": "🌱 Plantio",
                        "Área": f"{_id_plan} - {_area_obj.get('Talhão','')}",
                        "Obs": f"Meta: {_prod_inv} sc/ha. {_obs_inv}",
                        "Alerta": True, "Concluído": False,
                    })

                salvar_dados_iaagro()
                success_box(f"✅ Planejamento salvo! Evento de plantio criado no calendário.")
                st.rerun()

        # Histórico de planejamentos
        if st.session_state.planejamento_safras:
            st.markdown("---")
            st.markdown("#### 📋 Planejamentos Salvos")
            for _idx_p, _plan in enumerate(st.session_state.planejamento_safras):
                _c1_p, _c2_p = st.columns([5,1])
                with _c1_p:
                    st.markdown(f"""
                    <div style='background:#0f2d4a;border-radius:10px;padding:12px 16px;
                    border-left:3px solid #22c55e;margin:4px 0;'>
                    <span style='color:#6ee7b7;font-weight:700;'>
                    🌾 {_plan.get('talhao','')} — {_plan.get('inverno',{}).get('ano','')}
                    </span><br>
                    <span style='color:#94a3b8;font-size:12px;'>
                    ❄️ {_plan.get('inverno',{}).get('cultura','')} &nbsp;→&nbsp;
                    ☀️ {_plan.get('verao',{}).get('cultura','')}
                    </span>
                    </div>""", unsafe_allow_html=True)
                if _c2_p.button("🗑️", key=f"del_plan_{_idx_p}"):
                    st.session_state.planejamento_safras.pop(_idx_p)
                    salvar_dados_iaagro()
                    st.rerun()

    # ════════════════════════════════════════════════════════════════════════
    # ABA 3 — ROTAÇÃO DE CULTURAS
    # ════════════════════════════════════════════════════════════════════════
    with _tab_rot:
        st.markdown("#### 🔄 Mapa de Rotação por Talhão")

        if not st.session_state.planejamento_safras:
            st.markdown("""
            <div style='background:#0f3460;border-radius:12px;padding:24px;text-align:center;
            border:2px dashed #1e4976;'>
            <div style='font-size:40px;'>🔄</div>
            <div style='color:#94a3b8;margin-top:8px;'>
            Salve planejamentos na aba <b style='color:#6ee7b7;'>🌾 Planejamento de Safras</b>
            para ver o mapa de rotação.
            </div></div>""", unsafe_allow_html=True)
        else:
            # Agrupa por talhão
            _by_talhao = {}
            for _p in st.session_state.planejamento_safras:
                _t = _p.get("talhao","")
                if _t not in _by_talhao:
                    _by_talhao[_t] = []
                _by_talhao[_t].append(_p)

            for _tal, _plans in _by_talhao.items():
                st.markdown(f"**🌾 Talhão: {_tal}**")
                _cols_rot = st.columns(min(len(_plans), 4))
                for _ci, _p in enumerate(_plans):
                    with _cols_rot[_ci % 4]:
                        _inv_c = _p.get("inverno",{}).get("cultura","—")
                        _ver_c = _p.get("verao",{}).get("cultura","—")
                        _ano_c = _p.get("inverno",{}).get("ano","")
                        st.markdown(f"""
                        <div style='background:#0f2d4a;border-radius:12px;padding:14px;
                        text-align:center;border:1px solid #1e4976;margin:2px;'>
                        <div style='color:#94a3b8;font-size:11px;font-weight:700;
                        letter-spacing:1px;margin-bottom:8px;'>SAFRA {_ano_c}</div>
                        <div style='background:#1e3a5f;border-radius:8px;padding:8px;
                        margin-bottom:6px;'>
                        <div style='color:#38bdf8;font-size:10px;font-weight:700;'>❄️ INVERNO</div>
                        <div style='color:#f1f5f9;font-size:12px;font-weight:600;margin-top:2px;'>{_inv_c}</div>
                        </div>
                        <div style='color:#64748b;font-size:18px;'>↓</div>
                        <div style='background:#14532d;border-radius:8px;padding:8px;margin-top:6px;'>
                        <div style='color:#22c55e;font-size:10px;font-weight:700;'>☀️ VERÃO</div>
                        <div style='color:#f1f5f9;font-size:12px;font-weight:600;margin-top:2px;'>{_ver_c}</div>
                        </div></div>""", unsafe_allow_html=True)

            # Regras de rotação (EMBRAPA)
            st.markdown("---")
            st.markdown("#### 📚 Boas Práticas de Rotação — EMBRAPA Sul")
            _regras = [
                ("✅","Soja → Trigo/Aveia → Soja","Rotação clássica do PR/SC/RS. Quebra ciclo de Sclerotinia e ferrugem."),
                ("✅","Milho → Aveia/Mix Cobertura → Soja","Milho melhora estrutura; cobertura repõe MO; soja fixa N."),
                ("✅","Soja → Canola → Soja","Canola quebra ciclo de nematoides e melhora P disponível."),
                ("⚠️","Soja → Soja (monocultura)","Aumenta SCN, ferrugem e podridão radicular. Evitar >2 anos."),
                ("⚠️","Trigo → Trigo","Aumenta brusone e manchas foliares. Máximo 2 anos seguidos."),
                ("❌","Soja → Feijão → Soja","Ambas leguminosas. Amplifica patógenos de solo comuns."),
            ]
            for _ico_r, _rot_r, _desc_r in _regras:
                _bg_r = "#14532d" if _ico_r == "✅" else ("#78350f" if _ico_r == "⚠️" else "#7f1d1d")
                _bd_r = "#22c55e" if _ico_r == "✅" else ("#f59e0b" if _ico_r == "⚠️" else "#ef4444")
                st.markdown(f"""
                <div style='background:{_bg_r};border-radius:8px;padding:8px 14px;
                border-left:3px solid {_bd_r};margin:3px 0;'>
                <span style='color:#fff;font-weight:700;font-size:12px;'>{_ico_r} {_rot_r}</span><br>
                <span style='color:rgba(255,255,255,0.6);font-size:11px;'>{_desc_r}</span>
                </div>""", unsafe_allow_html=True)

if menu == "🌍 Inteligência":
  with _sub_int[4]:
    st.header("🤖 Assistente IA Agrícola")
    if "assistente_hist" not in st.session_state:
        st.session_state.assistente_hist = []
    _d_ia = st.session_state.dados
    _ctx_ia = (f"Cultura: {cultura_limpa(_d_ia.get('cultura','Soja'))}, "
               f"pH: {_d_ia.get('ph',0)}, Área: {_d_ia.get('area',0)} ha")
    for msg in st.session_state.assistente_hist:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    _prompt_ia = st.chat_input("Digite sua pergunta agrícola...")
    if _prompt_ia:
        st.session_state.assistente_hist.append({"role":"user","content":_prompt_ia})
        with st.chat_message("user"):
            st.markdown(_prompt_ia)
        with st.chat_message("assistant"):
            with st.spinner("Consultando..."):
                try:
                    import requests as _rq_ia
                    _api_key_ia = st.secrets.get("ANTHROPIC_API_KEY","")
                    _msgs_ia = [{"role":m["role"],"content":m["content"]}
                                for m in st.session_state.assistente_hist]
                    _resp_ia = _rq_ia.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": _api_key_ia,
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json",
                        },
                        json={
                            "model": "claude-sonnet-4-5",
                            "max_tokens": 800,
                            "system": f"Você é um assistente agrícola especialista brasileiro. Responda sempre em português de forma prática e objetiva para produtores rurais. Baseie-se em EMBRAPA, CQFS RS/SC e boas práticas agrícolas. Contexto da propriedade: {_ctx_ia}",
                            "messages": _msgs_ia,
                        },
                        timeout=30
                    )
                    _data_ia = _resp_ia.json()
                    _ans = _data_ia.get("content",[{}])[0].get("text","Sem resposta.")
                    st.markdown(_ans)
                    st.session_state.assistente_hist.append({"role":"assistant","content":_ans})
                except Exception as e:
                    st.error(f"Erro: {e}")
    if st.session_state.assistente_hist:
        if st.button("🗑️ Limpar conversa", key="btn_limpar_assistente"):
            st.session_state.assistente_hist = []
            st.rerun()

# ─────────────────────────────────────────────
# MENU: SAFRINHA
# ─────────────────────────────────────────────
elif menu == "🌱 Safrinha":
    st.header("🌱 Safrinha")
    if "safrinha_registros" not in st.session_state:
        st.session_state.safrinha_registros = []
    ROTACOES = {
        "Milho → Feijão":  {"1a":"Milho","2a":"Feijão","janela":"Set–Jan / Fev–Mai"},
        "Milho → Soja":    {"1a":"Milho","2a":"Soja",  "janela":"Set–Jan / Out–Mar"},
        "Soja → Feijão":   {"1a":"Soja", "2a":"Feijão","janela":"Out–Jan / Fev–Mai"},
        "Feijão → Soja":   {"1a":"Feijão","2a":"Soja", "janela":"Jan–Abr / Out–Mar"},
        "Feijão → Milho":  {"1a":"Feijão","2a":"Milho","janela":"Jan–Abr / Abr–Ago"},
        "Soja → Milho":    {"1a":"Soja", "2a":"Milho", "janela":"Out–Jan / Fev–Jun"},
    }
    rot_sel = st.selectbox("🔄 Rotação de culturas", list(ROTACOES.keys()), key="safrinha_rotacao_sel")
    rot_info = ROTACOES[rot_sel]
    if rot_info["janela"]:
        st.caption(f"📅 Janela de plantio: {rot_info['janela']}")
    col_sf1, col_sf2 = st.columns(2)
    if st.session_state.areas:
        _lista_sf = [f"{a['ID']} — {a.get('Talhão','?')}" for a in st.session_state.areas]
        area_sf   = col_sf1.selectbox("Área", _lista_sf, key="sf_area")
        _id_sf    = area_sf.split(" — ")[0]
    else:
        st.warning("Cadastre uma área primeiro."); _id_sf = ""
    safra_sf  = col_sf2.text_input("Safra", placeholder="2024/2025", key="sf_safra")
    col_sf3, col_sf4, col_sf5 = st.columns(3)
    data_plantio_sf = col_sf3.date_input("Data de plantio", key="sf_data")
    area_ha_sf      = col_sf4.number_input("Área (ha)", min_value=0.0, key="sf_area_ha")
    prod_esp_sf     = col_sf5.number_input("Produtividade esperada (sc/ha)", min_value=0.0, key="sf_prod")
    obs_sf          = st.text_area("Observações", key="sf_obs", height=80)
    if st.button("💾 Salvar Safrinha", key="btn_salvar_safrinha", use_container_width=True):
        if _id_sf:
            st.session_state.safrinha_registros.append({
                "Rotação": rot_sel, "1ª Cultura": rot_info["1a"], "2ª Cultura": rot_info["2a"],
                "Área ID": _id_sf, "Safra": safra_sf, "Data Plantio": str(data_plantio_sf),
                "Área ha": area_ha_sf, "Produtividade Esperada": prod_esp_sf, "Obs": obs_sf,
            })
            salvar_dados_iaagro()
            success_box(f"✅ Safrinha {rot_sel} registrada!")
        else:
            warning_box("Selecione uma área.")
    if st.session_state.safrinha_registros:
        import pandas as pd
        st.divider()
        st.subheader("📋 Registros de Safrinha")
        st.dataframe(pd.DataFrame(st.session_state.safrinha_registros), use_container_width=True)

# ─────────────────────────────────────────────
elif menu == "⚙️ Configurações":
    st.header("⚙️ Configurações do Sistema")

    tab0, tab_planos, tab1, tab2, tab3, tab4 = st.tabs([
        "🌾 Meu Segmento",
        "💳 Planos & Preços",
        "💾 Backup & Restore",
        "📧 Email & Alertas",
        "📊 Histórico do Solo",
        "📤 Exportar Excel"
    ])

    with tab_planos:
        st.subheader("💳 Planos & Preços")
        _plano_atual = st.session_state.get("sb_plano", "free")

        cols = st.columns(3)
        for idx, (key, plano) in enumerate(PLANOS.items()):
            with cols[idx]:
                is_atual   = key == _plano_atual
                cor        = plano["cor"]
                borda      = plano["borda"]
                nome       = plano["nome"]
                preco      = plano["preco"]
                borda_css  = f"border:3px solid {borda};" if is_atual else f"border:1px solid {borda};"
                atual_txt  = "&nbsp;✅ ATUAL" if is_atual else ""
                preco_txt  = "Grátis" if preco == 0 else f"R$ {preco:.2f}/mês"
                rec_html   = "".join(f"✅ {r}<br>" for r in plano["recursos"])
                bloq_html  = "".join(f"🔒 {r}<br>" for r in plano["bloqueados"])

                card_html = (
                    f"<div style='background:{cor};border-radius:14px;"
                    f"padding:18px 14px;{borda_css}text-align:center;min-height:380px;'>"
                    f"<div style='font-size:22px;font-weight:900;color:{borda};'>{nome}{atual_txt}</div>"
                    f"<div style='font-size:26px;font-weight:800;color:#fff;margin:10px 0;'>{preco_txt}</div>"
                    f"<hr style='border-color:{borda};margin:10px 0;'>"
                    f"<div style='text-align:left;font-size:12px;color:#d1fae5;line-height:1.8;'>"
                    f"{rec_html}{bloq_html}</div></div>"
                )
                st.markdown(card_html, unsafe_allow_html=True)

                if not is_atual and plano["preco"] > 0:
                    # Cada plano tem seu próprio link
                    if key == "pro":
                        btn_lmes = MP_LINK_PRO_MES
                        btn_lano = MP_LINK_PRO_ANO
                        btn_pano = round(49.90 * 12 * 0.85)
                        btn_preco = 49.90
                    else:  # premium
                        btn_lmes = MP_LINK_PREMIUM_MES
                        btn_lano = MP_LINK_PREMIUM_ANO
                        btn_pano = round(119.90 * 12 * 0.85)
                        btn_preco = 119.90
                    st.link_button(
                        f"💳 Mensal — R$ {btn_preco:.2f}/mês",
                        btn_lmes,
                        use_container_width=True
                    )
                    st.link_button(
                        f"🏆 Anual — R$ {btn_pano} (-15%)",
                        btn_lano,
                        use_container_width=True
                    )
                    st.caption("PIX • Cartão • Boleto")
                elif is_atual:
                    st.markdown(f"""
                    <div style='background:{plano["borda"]}33;border-radius:8px;padding:10px;
                    text-align:center;margin-top:8px;color:{plano["borda"]};font-weight:700;'>
                    ✅ Plano Ativo
                    </div>
                    """, unsafe_allow_html=True)

        st.divider()
        st.markdown("""
        <div style='background:#0f3460;border-radius:10px;padding:14px 18px;border:1px solid #3b82f6;'>
        <b style='color:#3b82f6;'>💳 Como ativar o Plano Pro ou Premium?</b><br>
        <span style='color:#f1f5f9;font-size:13px;'>
        1. Clique em <b>Mensal</b> ou <b>Anual</b> no plano desejado<br>
        2. Você será redirecionado para o <b>Mercado Pago</b><br>
        3. Pague via PIX, cartão ou boleto<br>
        4. Seu plano é ativado <b>automaticamente</b> após confirmação<br>
        5. Faça logout e login novamente para ver o novo plano
        </span>
        </div>
        """, unsafe_allow_html=True)

    with tab0:
        st.subheader("🌾 Alterar Segmento de Atuação")
        st.info(f"Segmento atual: **{st.session_state.segmento or 'Não definido'}**")
        SEGMENTOS_CFG = {
            "🌾 Grãos":        "Soja, Milho, Trigo e outros cereais",
            "🌿 Horticultura": "Hortaliças, verduras e legumes",
            "🍎 Fruticultura": "Frutas tropicais, uva, café e outras",
            "🌲 Silvicultura": "Eucalipto, Pinus e reflorestamento",
        }
        st.markdown("#### Selecione o novo segmento:")
        for seg, desc in SEGMENTOS_CFG.items():
            col_s1, col_s2 = st.columns([2, 5])
            with col_s1:
                if st.button(seg, key=f"cfg_seg_{seg}", use_container_width=True):
                    st.session_state.segmento = seg
                    salvar_dados_iaagro()
                    st.success(f"✅ Segmento alterado para **{seg}**!")
                    st.rerun()
            with col_s2:
                st.markdown(f"<div style='padding:10px 0;color:#94a3b8;font-size:13px;'>{desc}</div>", unsafe_allow_html=True)

    # ── TAB 1: BACKUP & RESTORE ──
    with tab1:
        st.subheader("💾 Backup & Restauração de Dados")

        st.markdown('''<div style="background:#7f1d1d;color:#fff;padding:14px 18px;
        border-radius:10px;border-left:5px solid #ef4444;font-weight:700;margin:8px 0 16px 0;font-size:14px;">
        ⚠️ <b>IMPORTANTE — Antes de atualizar o app:</b><br>
        O Streamlit Cloud não persiste arquivos entre deploys. Sempre faça backup
        antes de enviar uma atualização via Git. Após atualizar, restaure o backup para
        recuperar seus dados (usuários, estoque, áreas, histórico).
        </div>''', unsafe_allow_html=True)

        # Auto-backup ao abrir a aba
        st.markdown("#### 📥 Fazer Backup Agora")
        st.markdown('''<div style="background:#0f3460;color:#93c5fd;padding:10px 14px;
        border-radius:8px;font-size:12px;font-weight:600;margin:4px 0 12px 0;">
        💡 Salve este arquivo no seu computador. Ele contém todos os seus dados:
        usuários, estoque, áreas cadastradas, histórico, aplicações e configurações.
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
        st.markdown("#### 📂 Restaurar Backup")
        st.markdown('''<div style="background:#78350f;color:#fff;padding:11px 14px;
        border-radius:8px;border-left:4px solid #f59e0b;font-weight:600;margin:4px 0 12px 0;font-size:13px;">
        ⚠️ A restauração substitui TODOS os dados atuais. Use após atualizar o app.
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
        arquivo_restore = st.file_uploader(
            "Selecione o arquivo de backup (.json)",
            type=["json"],
            key="upl_backup_restore"
        )

        if arquivo_restore is not None:
            # Lê e armazena o conteúdo no session_state imediatamente
            conteudo_backup = arquivo_restore.read()
            st.session_state["_backup_conteudo"] = conteudo_backup
            st.success(f"✅ Arquivo **{arquivo_restore.name}** carregado ({len(conteudo_backup)//1024} KB)")

        if st.session_state.get("_backup_conteudo"):
            if st.button("🔄 Restaurar Backup Agora", key="btn_restore", use_container_width=True, type="primary"):
                import io
                ok, msg = restaurar_backup(io.BytesIO(st.session_state["_backup_conteudo"]))
                if ok:
                    st.session_state["_backup_conteudo"] = None
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

        # Passo a passo
        st.divider()
        st.markdown("#### 📋 Passo a passo para atualizar sem perder dados")
        passos_bk = [
            ("1️⃣", "Acesse ⚙️ Configurações → Backup & Restauração"),
            ("2️⃣", "Clique em **📥 Baixar Backup Completo** e salve no computador"),
            ("3️⃣", "Atualize o app normalmente via Git (git add → commit → push)"),
            ("4️⃣", "Aguarde o Streamlit Cloud reiniciar (1-2 minutos)"),
            ("5️⃣", "Acesse o app → ⚙️ Configurações → Backup & Restauração"),
            ("6️⃣", "Faça upload do arquivo backup e clique em **🔄 Restaurar**"),
            ("7️⃣", "Todos os dados estarão de volta ✅"),
        ]
        for num, desc in passos_bk:
            st.markdown(f'<div style="background:#0f3460;color:#f1f5f9;padding:8px 14px;'
                        f'border-radius:8px;margin:4px 0;font-size:13px;">'
                        f'<b>{num}</b> {desc}</div>', unsafe_allow_html=True)

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
            cfg["remetente"]     = st.text_input("Email remetente (Gmail)", value=cfg.get("remetente",""), key="txt_email_remetente_8822")
            cfg["senha"]         = st.text_input("Senha de app Gmail", type="password", value=cfg.get("senha",""), key="txt_senha_de_app_gm_8823")
        with col2:
            cfg["email_destino"] = st.text_input("Email destino dos alertas", value=cfg.get("email_destino",""), key="txt_email_destino_d_8825")
            cfg["porta"]         = st.number_input("Porta SMTP", value=int(cfg.get("porta",587)), min_value=1, key="num_porta_smtp_8826")

        cfg["smtp"] = st.text_input("Servidor SMTP", value=cfg.get("smtp","smtp.gmail.com"), key="txt_servidor_smtp_8828")
        cfg["ativo"] = st.checkbox("✅ Ativar alertas por email", value=cfg.get("ativo", False), key="chk___ativar_alerta_8829")

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
        st.markdown("""
        <div style='background:#14532d;border-radius:12px;padding:20px 24px;
        border-left:5px solid #22c55e;text-align:center;margin:20px 0;'>
        <div style='font-size:36px;'>📊</div>
        <div style='color:#6ee7b7;font-size:16px;font-weight:800;margin:8px 0;'>
        Evolução da Fertilidade do Solo</div>
        <div style='color:#f1f5f9;font-size:13px;'>
        Esta aba foi movida para o menu principal.<br>
        Acesse em: <b>🧪 Solo & Adubação → 📊 Evolução da Fertilidade</b>
        </div></div>
        """, unsafe_allow_html=True)

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

# ── PWA — Progressive Web App com ícone IAAgro embutido ──
_MANIFEST_B64 = __import__('base64').b64encode('''{
  "name": "IAAgro Pro",
  "short_name": "IAAgro",
  "description": "Inteligência Agrícola de Precisão",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0d2137",
  "theme_color": "#22c55e",
  "icons": [
    {"src": "data:image/jpeg;base64,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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEwAAAAAAAAAAAAAAAAAAAAAAAASgAAAAAAASgTAAAAAAAAAAAAAAAAAJgAAAAAAAAAAAAAAAAAAAEiAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASgAAAAAAAAAJgAAAAAAAAAAJgAAAAAAAAAAAAJgAAAAAAAAAAAAAAAAAAAAAAAAAAATAAAAAJgAAJgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAf//EAAL/2gAMAwEAAgADAAAAIfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPMPPHPPPPPPPPPPPPPPPPPPPPPAPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPONPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPONPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPMfPPPHPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLAvPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPLDOPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPDPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPMPPPPPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPMfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPDPPPPPPPPPPPPPPPPPPPPPLPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPPPPPPNPPPPPPPPPfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPPNPPPPPPOZrjuv/OPPPPPPPKr853+9vPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPHvPPPMPPPPOPPPPOBPPPPD/HPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPPPPPPPPPPPOPPPPNPPH/PPPPL4vPPPPPPPVfPPPPPNfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOdnPPPPPIIvPPPPPLD2tPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPZmLPPPPPLFPPPPPPPN5/PPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOViK/fPPPPAS/DnNCURPx3PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPMPPPPPPPPPPPPPPPPPPPPPOTjOrPPPPPPM2vIYPK6vI9fPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPvLLLPPPPJsmT3vnvP5ITw/wD/AM88888888884880888888888888888888888888888888c888888888+888888stWP4fbPPgQPA268O82888888888888888888888888888s8888888888888888888888888+888888i27c8888888888s4TPx88888888888888888888888888888888888888888888888888888o888888+ac40888888wuMjGcI5w888888888888880888888888888888888888888888888c888887za4PUj4hdc88888v+rxXaG687ZX18wQ888888888888s8888888888888888888888888488888888TD08cmfJfk88888nrBJ2QUfk87B99/eU098888c88888888888888888M8888888888888888888888vqvs88887E8888tvkgGuclk28rc888cs8r0888888888888888888888888888088888888888888888888869xRZ888j8/FwyCBZFwcsi9tI888788888M8888888888s8Mc888888888888888888888888888888hv/AGmPPC2WoBXpZg9cVvOM/NV/PO1+/PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP9/ONj9Al2Wh6p+/fKd3PFPPNTQ9PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP9PPMuNLKvPNTXy6xStRpjdvKv8ArbDzx2JXzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzlwXzwqAAPtzgtOgut7E7vr7zyodd/wD888Pd8888888888888w8884888888888888888888888884882m8888s8rO8s3RGtQBdGPe+88+X88c48888888888888888888888888888888888888s8880888888vyfaK1/8Aog/PJJf9/EV6xjvOPPa0t+RmvPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPLvNcpLkAR8PC+U/0YD4mfPPPPUg7buNvPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP/PPPPPL1XPL6VAr8JNfPPPPKZTPPPPPO/PPLHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP/ADzzzzy5FFC6cByzzzzzzzzSqvzzzzzytTxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzg3l/sPPPfvuH3TyhT7LzzzzBuzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz0+rUwrwHUAWjSs3k/zzzw7dXzzzzzzzzzzzzzzzzzzzzzzzzzzwwzzzzzzzzzzzzzzzzzzzzyzTjzzzzzz41SbRj8QykVTzzzzDjM3zzzzzzzzzzzzzzzzzzzzzzzz3zzzzzzzzzzzzzzzzzzzzzzzzyRdTzzzzzzoPxdXT4HSl7zzzzz++XzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzywLjzzzzyw7T17z17wojzzzyzeXzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxf7vDzhwLzzzzzzisjzzj3d3zzzzzzzzzzzzzzzzzzzzzzzzzzzDzzzzzzzzzzzzzzzzzzzzzzzzzzzzy99/zyx3zzzzzzyz3zzx8/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzyzzzzzzzzzzzzzzjzzzy67rzzzzwMuDzzzzzzzz/ePfzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzykKDzzzzgrY3fzzzzzzz4xdjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzyvB/zzzweVlEHzzzzzz2tfezTzzzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzHzzzzzzzzzzzzzzwuMDzzzybRKKfzzzzzz9zWvibzzzjL76Pb7mv78vpPTb7Kb/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz9Y/zzxgvJ2y8jzzzzhA7ZvMbzzDA8eIfYKcSVWufmn3XklpbzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzysarzzxXAcxSR7zzzz1T7BluJbzjpvP/a+1esssdfPaaraM8tzzzzxzzzzzzzzzzzzTzzzzzzzzzzzzz4nHzyrWDYwl3H7zzx5Vn0TjG9SjH3zzx8r6trbzzooTzzyEVTzzzzzzzzzzzzzwzzzzzzzzzzzzzzzxpLbzwEJPbQowY3zy+LYMKh05p6xBHTzxs36t3fzz70zzzglXTzzzzzzzzzzzzzwzzzzzzzzzzzzzzzyiRnynm2EUCYWQHuxmQXw1Dxf1qT3HzwRZX6ul/wA8tcz88xVp8888888888888888888888888888888o9x0/lM888s8DZ7sdt0c8s84JkNSoAAkAJ23V7888z1JsgRT8888888888888888888888888888888pDm8HPf88888ITrnPq888888euH8mimfm5GeW2888hKOvq3cw84888888888888w88888888884888888sQo0888848kc8c8888888w888haRdbrYRs848888s8888888888888888888gA888888888888888885/9999995BbM888888s888888LZ51VNi0844z7z3LT7208888888888888884w88888888888888885cM88888888M70888888887z8c5X/PP38s88+8888888/Y8888888888888888A8888888888888893U8/z/AP8Azzzzzz3XTzzzzzzsMJfzzzzzzzzyB7zzzzzzBzz/AK88888888888888888888s888888888c888/Loed888888sfPPHPPPeFlcPPPPPPf8A7/8Azzzzgwtdvzyzzzzxzzzzzzzzzzz3zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwxzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzDzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwzzzzzzzzyzzzTzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyzzzzzzxzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzTzTzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyxzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzwzzzzzzzwxzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzDzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwzzzzzzzzzyzzzzzzzzzzyzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzyzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz/8QAAv/aAAwDAQACAAMAAAAQ88888888888888888888888888888888888888888888888848888w88c888888888888888888888A888888888888888888888888880888888888888888888888888888888840888888888888888888888888888888888888888888888888888888888888888888888888840888888888888888888888888888c8888888888888888888888888888888888888888888888888888888888888888888888888888888888888c888888888888888888888888888888888888888888888088888888888888888888x8888c8c88888888888888888888888888888888888888888888888888c88888888888c888888888888888888888888888888c888888s888888888888888888888888888888888888888888888888sC88888888888888888888888888888888888888888888888888888888888884888888888888888sM48888888888888884888888888888888M888888888888888888888488888888888888888s88888888888888888888888888888888888888888888888888888888888884w888888888888888888888w88888888888888888888888888088888888888888888888888888888888888888888c888888888x888888888888888888888888888888888888888888888888888888888888888888888888888888M888888888888888888888s888888s88888888888888888888888c888888888888888808888888898888888888888888888888888888888888888888888888888888888888888888888888888888888888888888488888c808888888888888888888888888888888888888c8888888888888888888888888888888888888s888880808888886ggA03848888888ou+qS29888888888888888888888888888888888888888888888488888888887E488888888488884E8888s8c888888888888888888888888c88888888888888888888848888087H88888+l8888888mp0888881888488888c8888888888888888888888888888888888888888888+cc88888Xqc88888sW208Y88888888888888888888888888888888888s888888888888888888886o4s88888ro888888sim888888808c888808888888888888888888888888888888888888888888/wCcNH/PPPPAvvGdtBphNr2NPPPPPPPPPPPOPPPPPPPPPPPPPPPPPPPPPMPPPPPPPPPPPPPPPPPPPPPO2fOxPPPPPPJRLE/PC9vMgvPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPLPPPPI+DhHKxwnH/Xisu9PPPPPPPPPPOPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPOPPNPPPLFqljT+g4HLI4x5VUpfPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPN3/bHDHLDLDDDLEAI2ofPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPEfPPPPPGWvONPPPPPPMI8N4XPl8PPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPHPPPPPAqgNYlo85cHPPPPPL/2z6gWc/NGRctMKfPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPOFPKeHHJQtVH7fPPPPOZf3sKnE+/Ms+zBQ/FN7HPPHPPPPPPPPPPPPPPPPPDPPNPPPPPPPPPPPPPPPLPPJD1d7PPPPNLVPPPPIUZwHU483fHrPPKHDPPVNPPPPPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPMDz9T/PPON/jp8ld/2R3BMy3DPPPAPPPPPDPPPPPPPPPPLPDDPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPB5/wA1rzxg5q2fs5HaClHyZu7mjzzu4ZzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzTzzzzzyTHzjLgmv1DBsGLaXxetTxDzhRFxzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzh/DzzPPMMXyjLcg5T5aosw9/wAZ5c8z48DH2c8888888888888888888888888888888888888c88888YfnU8glZy0UoUmUp2xl1Ibq881H/vv88sPt8888888888888w888488888888888888488888888488opQU88s8Cc0oluzGLhToPMU88Dl88c480888888888888888888c8888888888888888s8880888888vXuck25+pO8805Nft2YkUO848ELchyD988c8848888888888888888888888888w888888888s888888F8EilYavbw8/KlHn2HKC8888pm2/gvE888888888888888888888888888888808888888888888888A8084887Ec8rAP6aNml88888BXM88888n888sc888888888888888888884888888888808s8888s88e8c8c88q0ZQIDQcs8888888kPc888888BU8c888888888888888888888888888888888888884M888888888c4LbVsMxx4x0qy3zmNzE8884yf28880888888c8888888888888888888888888888888888488c888809pE2nsjFPOgCN28le8888FKc8888888888c8888888888888888MM88888888888888888888t84888888vK0bVIk3MpsU88886sSv88c88888888888888888888898888M8888888888888488s8080Ic8888884W0O70ujw9888888Nel888888888888888888888888888888888s888s88888888888888sZ488888z885O89e8OC0888sr8888888888888888888888888c88888888888888888888888888888sK/27847A08888842lc881yo888888888888888888888888888w8888888888888888c88888888888s+uu888t88888888t888OO88488888888888888888888888888888888808888888888888888088888888848888888888888888888888888888888848488888s8888888888888488885xu08888putw88888886ma/888888888888888888488888888888888888888888888888888c8888qU0c8884AuVe8888888P9u0888888888888888888880888888888888848888888888888888888884ZM0888Rm+wl888c889CdBt888888888888888888888888s888888888888888x888888888888888JnUc884HAZO4888888gvk5Zi8884/04szx9m13gQW839wh2888888888888888888888888888888885NiU88K33BAEo888887vaysM08wnyGj+eDhOInimKuB8F5qQ88888888888888888888888888888887sBU845mtUAmj08883+5w5V9V88iB5fxgTfAVScnGBhZGxZHU8888c88888888888088888888888886mrU8+pIHAhXsU884k4wlEh66UgtJ888NH2ED988/6O88sQg488888888888888M888888888888888OSHU8MkdpHfCYR88jg0tFLkX3+4gW088Fs+TYe88rEn884K7888888888888888M8888888888888888XsU4BQ7jOMs4wbsK1B2LisN2Mwbvw4Mxa+DSe88sZR0w9XnU8888888888888888888888888888889ifwNCX888ssJeRx+T1c8s8c6q0EWDa2jj+b7688sMOXbTG44888888888888888888888888888888s+c06aX88888JO1H/H8c8884PtHw3EwYZDeqp3888hCP7g28w84888888888888w88s888s8884888888sIo0888848sU8c8888s88w8881n5529SIM848888s8888888888c88888888gA8888888888888888827xxx5195JMM888888s888888fT3f7/A08447/AO9y089tPPPPPPPPPPPPPPPOMPPPPPPPPPPPPPPPPIhTPPPPPPPPHC/PPPPPPPOM19HGB/zz93LPJrTPPPPPPPh/PPPPPPPPPPPPPPPAPPPPPPPPPPPPPPPShfP+/wDPzzzzzz2HTzzzzzysjNLzzzzzzzzzL3zzzzzzBzy7Hzzzzzzzzzzzzzzzzzzzyzzzzzzzzzxzzzxwq8T3zzzzzyx/9+d+9/0rhY//APvPfvPfe88884F4UK8888888c8888888888988888888888888888888888c8888888888888srS8888888888c888888888088888888888888888w88888888888888888888888888888888888888888888888888888888c80888888888888888888888888888888888888888888c88888888888888888888s8888888888888880888888888888888888M88888888s880888888c888888888888888848888888888888888888888888888888888888888888888888c88888888888888888888888888888888888888888888888888888888848888888888888888888888888888888888888888888888888888888888888808888888888888888888888888888888888888888888088888888888888888888888888888888888s888888c88888888888888888888s88888888888888888888888c888888888888888888888888888888808884888888888888884888888888888888888888888888888888888888888884888888888888808088888888888888s888888888888888888888888888888s88888888888888888888888888888888848888888888c888888888888888888888888888888c88888888888888888888888sc888888888888888888888888848888888888888888888888888888c8888888888888888848888888888888888888888888888888888888888888888888888888888880888888888888888888888888888888880888888888888888888888888M8888888Mc8888888888888888s8888888888888888888w88888888888888888888888888888888M888888888s8888888888s888888888888s888888888888888888888888888c8888s88s888888888888888Ac8888888888888888888888888888888888888888888888888888g8888888888888c8888//EAEQRAAEDAQQGBggEBAQHAQAAAAEAAgMRBBASMRMgITJRcTBBUFJhoQUUM1NygZHRIiNCspKxweE0QHOgFSRDYGJjgsL/2gAIAQIBAT8A/wBl897WAV6zQLSu9y/y+60rvcv8vutK73L/AC+60rvcv8vumyOJAMTx4mnROcRk0nktI73T/L7rSO90/wAvutI73T/L7rSO90/y+60p90/yTHte0FpqO2XvDBU/IdZKYw1xv3vIDgP8q5jmvxs695vHx59sPeGCp5AcSmMNcb97yGtaJzEGhoq5x2KO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", "sizes": "192x192", "type": "image/jpeg"},
    {"src": "data:image/jpeg;base64,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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEwAAAAAAAAAAAAAAAAAAAAAAAASgAAAAAAASgTAAAAAAAAAAAAAAAAAJgAAAAAAAAAAAAAAAAAAAEiAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASgAAAAAAAAAJgAAAAAAAAAAJgAAAAAAAAAAAAJgAAAAAAAAAAAAAAAAAAAAAAAAAAATAAAAAJgAAJgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAf//EAAL/2gAMAwEAAgADAAAAIfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPMPPHPPPPPPPPPPPPPPPPPPPPPAPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPONPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPONPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPMfPPPHPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLAvPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPLDOPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPDPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPMPPPPPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPMfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPDPPPPPPPPPPPPPPPPPPPPPLPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPPPPPPNPPPPPPPPPfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPPNPPPPPPOZrjuv/OPPPPPPPKr853+9vPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPHvPPPMPPPPOPPPPOBPPPPD/HPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPPPPPPPPPPPOPPPPNPPH/PPPPL4vPPPPPPPVfPPPPPNfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOdnPPPPPIIvPPPPPLD2tPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPZmLPPPPPLFPPPPPPPN5/PPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOViK/fPPPPAS/DnNCURPx3PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPMPPPPPPPPPPPPPPPPPPPPPOTjOrPPPPPPM2vIYPK6vI9fPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPvLLLPPPPJsmT3vnvP5ITw/wD/AM88888888884880888888888888888888888888888888c888888888+888888stWP4fbPPgQPA268O82888888888888888888888888888s8888888888888888888888888+888888i27c8888888888s4TPx88888888888888888888888888888888888888888888888888888o888888+ac40888888wuMjGcI5w888888888888880888888888888888888888888888888c888887za4PUj4hdc88888v+rxXaG687ZX18wQ888888888888s8888888888888888888888888488888888TD08cmfJfk88888nrBJ2QUfk87B99/eU098888c88888888888888888M8888888888888888888888vqvs88887E8888tvkgGuclk28rc888cs8r0888888888888888888888888888088888888888888888888869xRZ888j8/FwyCBZFwcsi9tI888788888M8888888888s8Mc888888888888888888888888888888hv/AGmPPC2WoBXpZg9cVvOM/NV/PO1+/PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP9/ONj9Al2Wh6p+/fKd3PFPPNTQ9PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP9PPMuNLKvPNTXy6xStRpjdvKv8ArbDzx2JXzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzlwXzwqAAPtzgtOgut7E7vr7zyodd/wD888Pd8888888888888w8884888888888888888888888884882m8888s8rO8s3RGtQBdGPe+88+X88c48888888888888888888888888888888888888s8880888888vyfaK1/8Aog/PJJf9/EV6xjvOPPa0t+RmvPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPLvNcpLkAR8PC+U/0YD4mfPPPPUg7buNvPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP/PPPPPL1XPL6VAr8JNfPPPPKZTPPPPPO/PPLHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP/ADzzzzy5FFC6cByzzzzzzzzSqvzzzzzytTxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzg3l/sPPPfvuH3TyhT7LzzzzBuzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz0+rUwrwHUAWjSs3k/zzzw7dXzzzzzzzzzzzzzzzzzzzzzzzzzzwwzzzzzzzzzzzzzzzzzzzzyzTjzzzzzz41SbRj8QykVTzzzzDjM3zzzzzzzzzzzzzzzzzzzzzzzz3zzzzzzzzzzzzzzzzzzzzzzzzyRdTzzzzzzoPxdXT4HSl7zzzzz++XzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzywLjzzzzyw7T17z17wojzzzyzeXzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxf7vDzhwLzzzzzzisjzzj3d3zzzzzzzzzzzzzzzzzzzzzzzzzzzDzzzzzzzzzzzzzzzzzzzzzzzzzzzzy99/zyx3zzzzzzyz3zzx8/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzyzzzzzzzzzzzzzzjzzzy67rzzzzwMuDzzzzzzzz/ePfzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzykKDzzzzgrY3fzzzzzzz4xdjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzyvB/zzzweVlEHzzzzzz2tfezTzzzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzHzzzzzzzzzzzzzzwuMDzzzybRKKfzzzzzz9zWvibzzzjL76Pb7mv78vpPTb7Kb/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz9Y/zzxgvJ2y8jzzzzhA7ZvMbzzDA8eIfYKcSVWufmn3XklpbzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzysarzzxXAcxSR7zzzz1T7BluJbzjpvP/a+1esssdfPaaraM8tzzzzxzzzzzzzzzzzzTzzzzzzzzzzzzz4nHzyrWDYwl3H7zzx5Vn0TjG9SjH3zzx8r6trbzzooTzzyEVTzzzzzzzzzzzzzwzzzzzzzzzzzzzzzxpLbzwEJPbQowY3zy+LYMKh05p6xBHTzxs36t3fzz70zzzglXTzzzzzzzzzzzzzwzzzzzzzzzzzzzzzyiRnynm2EUCYWQHuxmQXw1Dxf1qT3HzwRZX6ul/wA8tcz88xVp8888888888888888888888888888888o9x0/lM888s8DZ7sdt0c8s84JkNSoAAkAJ23V7888z1JsgRT8888888888888888888888888888888pDm8HPf88888ITrnPq888888euH8mimfm5GeW2888hKOvq3cw84888888888888w88888888884888888sQo0888848kc8c8888888w888haRdbrYRs848888s8888888888888888888gA888888888888888885/9999995BbM888888s888888LZ51VNi0844z7z3LT7208888888888888884w88888888888888885cM88888888M70888888887z8c5X/PP38s88+8888888/Y8888888888888888A8888888888888893U8/z/AP8Azzzzzz3XTzzzzzzsMJfzzzzzzzzyB7zzzzzzBzz/AK88888888888888888888s888888888c888/Loed888888sfPPHPPPeFlcPPPPPPf8A7/8Azzzzgwtdvzyzzzzxzzzzzzzzzzz3zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwxzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzDzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwzzzzzzzzyzzzTzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyzzzzzzxzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzTzTzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyxzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzwzzzzzzzwxzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzDzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwzzzzzzzzzyzzzzzzzzzzyzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzyzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz/8QAAv/aAAwDAQACAAMAAAAQ88888888888888888888888888888888888888888888888848888w88c888888888888888888888A888888888888888888888888880888888888888888888888888888888840888888888888888888888888888888888888888888888888888888888888888888888888840888888888888888888888888888c8888888888888888888888888888888888888888888888888888888888888888888888888888888888888c888888888888888888888888888888888888888888888088888888888888888888x8888c8c88888888888888888888888888888888888888888888888888c88888888888c888888888888888888888888888888c888888s888888888888888888888888888888888888888888888888sC88888888888888888888888888888888888888888888888888888888888884888888888888888sM48888888888888884888888888888888M888888888888888888888488888888888888888s88888888888888888888888888888888888888888888888888888888888884w888888888888888888888w88888888888888888888888888088888888888888888888888888888888888888888c888888888x888888888888888888888888888888888888888888888888888888888888888888888888888888M888888888888888888888s888888s88888888888888888888888c888888888888888808888888898888888888888888888888888888888888888888888888888888888888888888888888888888888888888888488888c808888888888888888888888888888888888888c8888888888888888888888888888888888888s888880808888886ggA03848888888ou+qS29888888888888888888888888888888888888888888888488888888887E488888888488884E8888s8c888888888888888888888888c88888888888888888888848888087H88888+l8888888mp0888881888488888c8888888888888888888888888888888888888888888+cc88888Xqc88888sW208Y88888888888888888888888888888888888s888888888888888888886o4s88888ro888888sim888888808c888808888888888888888888888888888888888888888888/wCcNH/PPPPAvvGdtBphNr2NPPPPPPPPPPPOPPPPPPPPPPPPPPPPPPPPPMPPPPPPPPPPPPPPPPPPPPPO2fOxPPPPPPJRLE/PC9vMgvPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPLPPPPI+DhHKxwnH/Xisu9PPPPPPPPPPOPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPOPPNPPPLFqljT+g4HLI4x5VUpfPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPN3/bHDHLDLDDDLEAI2ofPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPEfPPPPPGWvONPPPPPPMI8N4XPl8PPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPHPPPPPAqgNYlo85cHPPPPPL/2z6gWc/NGRctMKfPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPOFPKeHHJQtVH7fPPPPOZf3sKnE+/Ms+zBQ/FN7HPPHPPPPPPPPPPPPPPPPPDPPNPPPPPPPPPPPPPPPLPPJD1d7PPPPNLVPPPPIUZwHU483fHrPPKHDPPVNPPPPPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPMDz9T/PPON/jp8ld/2R3BMy3DPPPAPPPPPDPPPPPPPPPPLPDDPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPB5/wA1rzxg5q2fs5HaClHyZu7mjzzu4ZzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzTzzzzzyTHzjLgmv1DBsGLaXxetTxDzhRFxzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzh/DzzPPMMXyjLcg5T5aosw9/wAZ5c8z48DH2c8888888888888888888888888888888888888c88888YfnU8glZy0UoUmUp2xl1Ibq881H/vv88sPt8888888888888w888488888888888888488888888488opQU88s8Cc0oluzGLhToPMU88Dl88c480888888888888888888c8888888888888888s8880888888vXuck25+pO8805Nft2YkUO848ELchyD988c8848888888888888888888888888w888888888s888888F8EilYavbw8/KlHn2HKC8888pm2/gvE888888888888888888888888888888808888888888888888A8084887Ec8rAP6aNml88888BXM88888n888sc888888888888888888884888888888808s8888s88e8c8c88q0ZQIDQcs8888888kPc888888BU8c888888888888888888888888888888888888884M888888888c4LbVsMxx4x0qy3zmNzE8884yf28880888888c8888888888888888888888888888888888488c888809pE2nsjFPOgCN28le8888FKc8888888888c8888888888888888MM88888888888888888888t84888888vK0bVIk3MpsU88886sSv88c88888888888888888888898888M8888888888888488s8080Ic8888884W0O70ujw9888888Nel888888888888888888888888888888888s888s88888888888888sZ488888z885O89e8OC0888sr8888888888888888888888888c88888888888888888888888888888sK/27847A08888842lc881yo888888888888888888888888888w8888888888888888c88888888888s+uu888t88888888t888OO88488888888888888888888888888888888808888888888888888088888888848888888888888888888888888888888848488888s8888888888888488885xu08888putw88888886ma/888888888888888888488888888888888888888888888888888c8888qU0c8884AuVe8888888P9u0888888888888888888880888888888888848888888888888888888884ZM0888Rm+wl888c889CdBt888888888888888888888888s888888888888888x888888888888888JnUc884HAZO4888888gvk5Zi8884/04szx9m13gQW839wh2888888888888888888888888888888885NiU88K33BAEo888887vaysM08wnyGj+eDhOInimKuB8F5qQ88888888888888888888888888888887sBU845mtUAmj08883+5w5V9V88iB5fxgTfAVScnGBhZGxZHU8888c88888888888088888888888886mrU8+pIHAhXsU884k4wlEh66UgtJ888NH2ED988/6O88sQg488888888888888M888888888888888OSHU8MkdpHfCYR88jg0tFLkX3+4gW088Fs+TYe88rEn884K7888888888888888M8888888888888888XsU4BQ7jOMs4wbsK1B2LisN2Mwbvw4Mxa+DSe88sZR0w9XnU8888888888888888888888888888889ifwNCX888ssJeRx+T1c8s8c6q0EWDa2jj+b7688sMOXbTG44888888888888888888888888888888s+c06aX88888JO1H/H8c8884PtHw3EwYZDeqp3888hCP7g28w84888888888888w88s888s8884888888sIo0888848sU8c8888s88w8881n5529SIM848888s8888888888c88888888gA8888888888888888827xxx5195JMM888888s888888fT3f7/A08447/AO9y089tPPPPPPPPPPPPPPPOMPPPPPPPPPPPPPPPPIhTPPPPPPPPHC/PPPPPPPOM19HGB/zz93LPJrTPPPPPPPh/PPPPPPPPPPPPPPPAPPPPPPPPPPPPPPPShfP+/wDPzzzzzz2HTzzzzzysjNLzzzzzzzzzL3zzzzzzBzy7Hzzzzzzzzzzzzzzzzzzzyzzzzzzzzzxzzzxwq8T3zzzzzyx/9+d+9/0rhY//APvPfvPfe88884F4UK8888888c8888888888988888888888888888888888c8888888888888srS8888888888c888888888088888888888888888w88888888888888888888888888888888888888888888888888888888c80888888888888888888888888888888888888888888c88888888888888888888s8888888888888880888888888888888888M88888888s880888888c888888888888888848888888888888888888888888888888888888888888888888c88888888888888888888888888888888888888888888888888888888848888888888888888888888888888888888888888888888888888888888888808888888888888888888888888888888888888888888088888888888888888888888888888888888s888888c88888888888888888888s88888888888888888888888c888888888888888888888888888888808884888888888888884888888888888888888888888888888888888888888884888888888888808088888888888888s888888888888888888888888888888s88888888888888888888888888888888848888888888c888888888888888888888888888888c88888888888888888888888sc888888888888888888888888848888888888888888888888888888c8888888888888888848888888888888888888888888888888888888888888888888888888888880888888888888888888888888888888880888888888888888888888888M8888888Mc8888888888888888s8888888888888888888w88888888888888888888888888888888M888888888s8888888888s888888888888s888888888888888888888888888c8888s88s888888888888888Ac8888888888888888888888888888888888888888888888888888g8888888888888c8888//EAEQRAAEDAQQGBggEBAQHAQAAAAEAAgMRBBASMRMgITJRcTBBUFJhoQUUM1NygZHRIiNCspKxweE0QHOgFSRDYGJjgsL/2gAIAQIBAT8A/wBl897WAV6zQLSu9y/y+60rvcv8vutK73L/AC+60rvcv8vumyOJAMTx4mnROcRk0nktI73T/L7rSO90/wAvutI73T/L7rSO90/y+60p90/yTHte0FpqO2XvDBU/IdZKYw1xv3vIDgP8q5jmvxs695vHx59sPeGCp5AcSmMNcb97yGtaJzEGhoq5x2KO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", "sizes": "512x512", "type": "image/jpeg"}
  ]
}'''.encode()).decode()

st.markdown(f"""
<link rel="manifest" href="data:application/json;base64,{_MANIFEST_B64}">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="IAAgro Pro">
<meta name="application-name" content="IAAgro Pro">
<meta name="theme-color" content="#22c55e">
<link rel="apple-touch-icon" href="data:image/jpeg;base64,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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEwAAAAAAAAAAAAAAAAAAAAAAAASgAAAAAAASgTAAAAAAAAAAAAAAAAAJgAAAAAAAAAAAAAAAAAAAEiAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASgAAAAAAAAAJgAAAAAAAAAAJgAAAAAAAAAAAAJgAAAAAAAAAAAAAAAAAAAAAAAAAAATAAAAAJgAAJgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAf//EAAL/2gAMAwEAAgADAAAAIfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPMPPHPPPPPPPPPPPPPPPPPPPPPAPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPONPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPONPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPMfPPPHPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLAvPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPLDOPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPDPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPMPPPPPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPMfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPDPPPPPPPPPPPPPPPPPPPPPLPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPPPPPPNPPPPPPPPPfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPPNPPPPPPOZrjuv/OPPPPPPPKr853+9vPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPHvPPPMPPPPOPPPPOBPPPPD/HPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPPPPPPPPPPPOPPPPNPPH/PPPPL4vPPPPPPPVfPPPPPNfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOdnPPPPPIIvPPPPPLD2tPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPZmLPPPPPLFPPPPPPPN5/PPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOViK/fPPPPAS/DnNCURPx3PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPMPPPPPPPPPPPPPPPPPPPPPOTjOrPPPPPPM2vIYPK6vI9fPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPvLLLPPPPJsmT3vnvP5ITw/wD/AM88888888884880888888888888888888888888888888c888888888+888888stWP4fbPPgQPA268O82888888888888888888888888888s8888888888888888888888888+888888i27c8888888888s4TPx88888888888888888888888888888888888888888888888888888o888888+ac40888888wuMjGcI5w888888888888880888888888888888888888888888888c888887za4PUj4hdc88888v+rxXaG687ZX18wQ888888888888s8888888888888888888888888488888888TD08cmfJfk88888nrBJ2QUfk87B99/eU098888c88888888888888888M8888888888888888888888vqvs88887E8888tvkgGuclk28rc888cs8r0888888888888888888888888888088888888888888888888869xRZ888j8/FwyCBZFwcsi9tI888788888M8888888888s8Mc888888888888888888888888888888hv/AGmPPC2WoBXpZg9cVvOM/NV/PO1+/PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP9/ONj9Al2Wh6p+/fKd3PFPPNTQ9PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP9PPMuNLKvPNTXy6xStRpjdvKv8ArbDzx2JXzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzlwXzwqAAPtzgtOgut7E7vr7zyodd/wD888Pd8888888888888w8884888888888888888888888884882m8888s8rO8s3RGtQBdGPe+88+X88c48888888888888888888888888888888888888s8880888888vyfaK1/8Aog/PJJf9/EV6xjvOPPa0t+RmvPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPLvNcpLkAR8PC+U/0YD4mfPPPPUg7buNvPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP/PPPPPL1XPL6VAr8JNfPPPPKZTPPPPPO/PPLHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP/ADzzzzy5FFC6cByzzzzzzzzSqvzzzzzytTxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzg3l/sPPPfvuH3TyhT7LzzzzBuzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz0+rUwrwHUAWjSs3k/zzzw7dXzzzzzzzzzzzzzzzzzzzzzzzzzzwwzzzzzzzzzzzzzzzzzzzzyzTjzzzzzz41SbRj8QykVTzzzzDjM3zzzzzzzzzzzzzzzzzzzzzzzz3zzzzzzzzzzzzzzzzzzzzzzzzyRdTzzzzzzoPxdXT4HSl7zzzzz++XzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzywLjzzzzyw7T17z17wojzzzyzeXzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxf7vDzhwLzzzzzzisjzzj3d3zzzzzzzzzzzzzzzzzzzzzzzzzzzDzzzzzzzzzzzzzzzzzzzzzzzzzzzzy99/zyx3zzzzzzyz3zzx8/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzyzzzzzzzzzzzzzzjzzzy67rzzzzwMuDzzzzzzzz/ePfzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzykKDzzzzgrY3fzzzzzzz4xdjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzyvB/zzzweVlEHzzzzzz2tfezTzzzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzHzzzzzzzzzzzzzzwuMDzzzybRKKfzzzzzz9zWvibzzzjL76Pb7mv78vpPTb7Kb/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz9Y/zzxgvJ2y8jzzzzhA7ZvMbzzDA8eIfYKcSVWufmn3XklpbzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzysarzzxXAcxSR7zzzz1T7BluJbzjpvP/a+1esssdfPaaraM8tzzzzxzzzzzzzzzzzzTzzzzzzzzzzzzz4nHzyrWDYwl3H7zzx5Vn0TjG9SjH3zzx8r6trbzzooTzzyEVTzzzzzzzzzzzzzwzzzzzzzzzzzzzzzxpLbzwEJPbQowY3zy+LYMKh05p6xBHTzxs36t3fzz70zzzglXTzzzzzzzzzzzzzwzzzzzzzzzzzzzzzyiRnynm2EUCYWQHuxmQXw1Dxf1qT3HzwRZX6ul/wA8tcz88xVp8888888888888888888888888888888o9x0/lM888s8DZ7sdt0c8s84JkNSoAAkAJ23V7888z1JsgRT8888888888888888888888888888888pDm8HPf88888ITrnPq888888euH8mimfm5GeW2888hKOvq3cw84888888888888w88888888884888888sQo0888848kc8c8888888w888haRdbrYRs848888s8888888888888888888gA888888888888888885/9999995BbM888888s888888LZ51VNi0844z7z3LT7208888888888888884w88888888888888885cM88888888M70888888887z8c5X/PP38s88+8888888/Y8888888888888888A8888888888888893U8/z/AP8Azzzzzz3XTzzzzzzsMJfzzzzzzzzyB7zzzzzzBzz/AK88888888888888888888s888888888c888/Loed888888sfPPHPPPeFlcPPPPPPf8A7/8Azzzzgwtdvzyzzzzxzzzzzzzzzzz3zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwxzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzDzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwzzzzzzzzyzzzTzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyzzzzzzxzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzTzTzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyxzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzwzzzzzzzwxzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzDzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwzzzzzzzzzyzzzzzzzzzzyzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzyzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz/8QAAv/aAAwDAQACAAMAAAAQ88888888888888888888888888888888888888888888888848888w88c888888888888888888888A888888888888888888888888880888888888888888888888888888888840888888888888888888888888888888888888888888888888888888888888888888888888840888888888888888888888888888c8888888888888888888888888888888888888888888888888888888888888888888888888888888888888c888888888888888888888888888888888888888888888088888888888888888888x8888c8c88888888888888888888888888888888888888888888888888c88888888888c888888888888888888888888888888c888888s888888888888888888888888888888888888888888888888sC88888888888888888888888888888888888888888888888888888888888884888888888888888sM48888888888888884888888888888888M888888888888888888888488888888888888888s88888888888888888888888888888888888888888888888888888888888884w888888888888888888888w88888888888888888888888888088888888888888888888888888888888888888888c888888888x888888888888888888888888888888888888888888888888888888888888888888888888888888M888888888888888888888s888888s88888888888888888888888c888888888888888808888888898888888888888888888888888888888888888888888888888888888888888888888888888888888888888888488888c808888888888888888888888888888888888888c8888888888888888888888888888888888888s888880808888886ggA03848888888ou+qS29888888888888888888888888888888888888888888888488888888887E488888888488884E8888s8c888888888888888888888888c88888888888888888888848888087H88888+l8888888mp0888881888488888c8888888888888888888888888888888888888888888+cc88888Xqc88888sW208Y88888888888888888888888888888888888s888888888888888888886o4s88888ro888888sim888888808c888808888888888888888888888888888888888888888888/wCcNH/PPPPAvvGdtBphNr2NPPPPPPPPPPPOPPPPPPPPPPPPPPPPPPPPPMPPPPPPPPPPPPPPPPPPPPPO2fOxPPPPPPJRLE/PC9vMgvPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPLPPPPI+DhHKxwnH/Xisu9PPPPPPPPPPOPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPOPPNPPPLFqljT+g4HLI4x5VUpfPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPN3/bHDHLDLDDDLEAI2ofPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPEfPPPPPGWvONPPPPPPMI8N4XPl8PPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPHPPPPPAqgNYlo85cHPPPPPL/2z6gWc/NGRctMKfPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPOFPKeHHJQtVH7fPPPPOZf3sKnE+/Ms+zBQ/FN7HPPHPPPPPPPPPPPPPPPPPDPPNPPPPPPPPPPPPPPPLPPJD1d7PPPPNLVPPPPIUZwHU483fHrPPKHDPPVNPPPPPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPMDz9T/PPON/jp8ld/2R3BMy3DPPPAPPPPPDPPPPPPPPPPLPDDPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPB5/wA1rzxg5q2fs5HaClHyZu7mjzzu4ZzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzTzzzzzyTHzjLgmv1DBsGLaXxetTxDzhRFxzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzh/DzzPPMMXyjLcg5T5aosw9/wAZ5c8z48DH2c8888888888888888888888888888888888888c88888YfnU8glZy0UoUmUp2xl1Ibq881H/vv88sPt8888888888888w888488888888888888488888888488opQU88s8Cc0oluzGLhToPMU88Dl88c480888888888888888888c8888888888888888s8880888888vXuck25+pO8805Nft2YkUO848ELchyD988c8848888888888888888888888888w888888888s888888F8EilYavbw8/KlHn2HKC8888pm2/gvE888888888888888888888888888888808888888888888888A8084887Ec8rAP6aNml88888BXM88888n888sc888888888888888888884888888888808s8888s88e8c8c88q0ZQIDQcs8888888kPc888888BU8c888888888888888888888888888888888888884M888888888c4LbVsMxx4x0qy3zmNzE8884yf28880888888c8888888888888888888888888888888888488c888809pE2nsjFPOgCN28le8888FKc8888888888c8888888888888888MM88888888888888888888t84888888vK0bVIk3MpsU88886sSv88c88888888888888888888898888M8888888888888488s8080Ic8888884W0O70ujw9888888Nel888888888888888888888888888888888s888s88888888888888sZ488888z885O89e8OC0888sr8888888888888888888888888c88888888888888888888888888888sK/27847A08888842lc881yo888888888888888888888888888w8888888888888888c88888888888s+uu888t88888888t888OO88488888888888888888888888888888888808888888888888888088888888848888888888888888888888888888888848488888s8888888888888488885xu08888putw88888886ma/888888888888888888488888888888888888888888888888888c8888qU0c8884AuVe8888888P9u0888888888888888888880888888888888848888888888888888888884ZM0888Rm+wl888c889CdBt888888888888888888888888s888888888888888x888888888888888JnUc884HAZO4888888gvk5Zi8884/04szx9m13gQW839wh2888888888888888888888888888888885NiU88K33BAEo888887vaysM08wnyGj+eDhOInimKuB8F5qQ88888888888888888888888888888887sBU845mtUAmj08883+5w5V9V88iB5fxgTfAVScnGBhZGxZHU8888c88888888888088888888888886mrU8+pIHAhXsU884k4wlEh66UgtJ888NH2ED988/6O88sQg488888888888888M888888888888888OSHU8MkdpHfCYR88jg0tFLkX3+4gW088Fs+TYe88rEn884K7888888888888888M8888888888888888XsU4BQ7jOMs4wbsK1B2LisN2Mwbvw4Mxa+DSe88sZR0w9XnU8888888888888888888888888888889ifwNCX888ssJeRx+T1c8s8c6q0EWDa2jj+b7688sMOXbTG44888888888888888888888888888888s+c06aX88888JO1H/H8c8884PtHw3EwYZDeqp3888hCP7g28w84888888888888w88s888s8884888888sIo0888848sU8c8888s88w8881n5529SIM848888s8888888888c88888888gA8888888888888888827xxx5195JMM888888s888888fT3f7/A08447/AO9y089tPPPPPPPPPPPPPPPOMPPPPPPPPPPPPPPPPIhTPPPPPPPPHC/PPPPPPPOM19HGB/zz93LPJrTPPPPPPPh/PPPPPPPPPPPPPPPAPPPPPPPPPPPPPPPShfP+/wDPzzzzzz2HTzzzzzysjNLzzzzzzzzzL3zzzzzzBzy7Hzzzzzzzzzzzzzzzzzzzyzzzzzzzzzxzzzxwq8T3zzzzzyx/9+d+9/0rhY//APvPfvPfe88884F4UK8888888c8888888888988888888888888888888888c8888888888888srS8888888888c888888888088888888888888888w88888888888888888888888888888888888888888888888888888888c80888888888888888888888888888888888888888888c88888888888888888888s8888888888888880888888888888888888M88888888s880888888c888888888888888848888888888888888888888888888888888888888888888888c88888888888888888888888888888888888888888888888888888888848888888888888888888888888888888888888888888888888888888888888808888888888888888888888888888888888888888888088888888888888888888888888888888888s888888c88888888888888888888s88888888888888888888888c888888888888888888888888888888808884888888888888884888888888888888888888888888888888888888888884888888888888808088888888888888s888888888888888888888888888888s88888888888888888888888888888888848888888888c888888888888888888888888888888c88888888888888888888888sc888888888888888888888888848888888888888888888888888888c8888888888888888848888888888888888888888888888888888888888888888888888888888880888888888888888888888888888888880888888888888888888888888M8888888Mc8888888888888888s8888888888888888888w88888888888888888888888888888888M888888888s8888888888s888888888888s888888888888888888888888888c8888s88s888888888888888Ac8888888888888888888888888888888888888888888888888888g8888888888888c8888//EAEQRAAEDAQQGBggEBAQHAQAAAAEAAgMRBBASMRMgITJRcTBBUFJhoQUUM1NygZHRIiNCspKxweE0QHOgFSRDYGJjgsL/2gAIAQIBAT8A/wBl897WAV6zQLSu9y/y+60rvcv8vutK73L/AC+60rvcv8vumyOJAMTx4mnROcRk0nktI73T/L7rSO90/wAvutI73T/L7rSO90/y+60p90/yTHte0FpqO2XvDBU/IdZKYw1xv3vIDgP8q5jmvxs695vHx59sPeGCp5AcSmMNcb97yGtaJzEGhoq5x2KO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">
<link rel="icon" type="image/jpeg" href="data:image/jpeg;base64,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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEwAAAAAAAAAAAAAAAAAAAAAAAASgAAAAAAASgTAAAAAAAAAAAAAAAAAJgAAAAAAAAAAAAAAAAAAAEiAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASgAAAAAAAAAJgAAAAAAAAAAJgAAAAAAAAAAAAJgAAAAAAAAAAAAAAAAAAAAAAAAAAATAAAAAJgAAJgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAf//EAAL/2gAMAwEAAgADAAAAIfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPMPPHPPPPPPPPPPPPPPPPPPPPPAPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPONPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPONPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPMfPPPHPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLAvPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPLDOPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPDPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPMPPPPPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPMfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPDPPPPPPPPPPPPPPPPPPPPPLPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPPPPPPNPPPPPPPPPfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPPNPPPPPPOZrjuv/OPPPPPPPKr853+9vPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPHvPPPMPPPPOPPPPOBPPPPD/HPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPPPPPPPPPPPPPOPPPPNPPH/PPPPL4vPPPPPPPVfPPPPPNfPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOdnPPPPPIIvPPPPPLD2tPHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPZmLPPPPPLFPPPPPPPN5/PPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOViK/fPPPPAS/DnNCURPx3PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPMPPPPPPPPPPPPPPPPPPPPPOTjOrPPPPPPM2vIYPK6vI9fPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPvLLLPPPPJsmT3vnvP5ITw/wD/AM88888888884880888888888888888888888888888888c888888888+888888stWP4fbPPgQPA268O82888888888888888888888888888s8888888888888888888888888+888888i27c8888888888s4TPx88888888888888888888888888888888888888888888888888888o888888+ac40888888wuMjGcI5w888888888888880888888888888888888888888888888c888887za4PUj4hdc88888v+rxXaG687ZX18wQ888888888888s8888888888888888888888888488888888TD08cmfJfk88888nrBJ2QUfk87B99/eU098888c88888888888888888M8888888888888888888888vqvs88887E8888tvkgGuclk28rc888cs8r0888888888888888888888888888088888888888888888888869xRZ888j8/FwyCBZFwcsi9tI888788888M8888888888s8Mc888888888888888888888888888888hv/AGmPPC2WoBXpZg9cVvOM/NV/PO1+/PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP9/ONj9Al2Wh6p+/fKd3PFPPNTQ9PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP9PPMuNLKvPNTXy6xStRpjdvKv8ArbDzx2JXzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzlwXzwqAAPtzgtOgut7E7vr7zyodd/wD888Pd8888888888888w8884888888888888888888888884882m8888s8rO8s3RGtQBdGPe+88+X88c48888888888888888888888888888888888888s8880888888vyfaK1/8Aog/PJJf9/EV6xjvOPPa0t+RmvPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPLvNcpLkAR8PC+U/0YD4mfPPPPUg7buNvPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP/PPPPPL1XPL6VAr8JNfPPPPKZTPPPPPO/PPLHPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP/ADzzzzy5FFC6cByzzzzzzzzSqvzzzzzytTxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzg3l/sPPPfvuH3TyhT7LzzzzBuzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz0+rUwrwHUAWjSs3k/zzzw7dXzzzzzzzzzzzzzzzzzzzzzzzzzzwwzzzzzzzzzzzzzzzzzzzzyzTjzzzzzz41SbRj8QykVTzzzzDjM3zzzzzzzzzzzzzzzzzzzzzzzz3zzzzzzzzzzzzzzzzzzzzzzzzyRdTzzzzzzoPxdXT4HSl7zzzzz++XzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzywLjzzzzyw7T17z17wojzzzyzeXzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxf7vDzhwLzzzzzzisjzzj3d3zzzzzzzzzzzzzzzzzzzzzzzzzzzDzzzzzzzzzzzzzzzzzzzzzzzzzzzzy99/zyx3zzzzzzyz3zzx8/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzyzzzzzzzzzzzzzzjzzzy67rzzzzwMuDzzzzzzzz/ePfzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzykKDzzzzgrY3fzzzzzzz4xdjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzyvB/zzzweVlEHzzzzzz2tfezTzzzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzHzzzzzzzzzzzzzzwuMDzzzybRKKfzzzzzz9zWvibzzzjL76Pb7mv78vpPTb7Kb/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz9Y/zzxgvJ2y8jzzzzhA7ZvMbzzDA8eIfYKcSVWufmn3XklpbzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzysarzzxXAcxSR7zzzz1T7BluJbzjpvP/a+1esssdfPaaraM8tzzzzxzzzzzzzzzzzzTzzzzzzzzzzzzz4nHzyrWDYwl3H7zzx5Vn0TjG9SjH3zzx8r6trbzzooTzzyEVTzzzzzzzzzzzzzwzzzzzzzzzzzzzzzxpLbzwEJPbQowY3zy+LYMKh05p6xBHTzxs36t3fzz70zzzglXTzzzzzzzzzzzzzwzzzzzzzzzzzzzzzyiRnynm2EUCYWQHuxmQXw1Dxf1qT3HzwRZX6ul/wA8tcz88xVp8888888888888888888888888888888o9x0/lM888s8DZ7sdt0c8s84JkNSoAAkAJ23V7888z1JsgRT8888888888888888888888888888888pDm8HPf88888ITrnPq888888euH8mimfm5GeW2888hKOvq3cw84888888888888w88888888884888888sQo0888848kc8c8888888w888haRdbrYRs848888s8888888888888888888gA888888888888888885/9999995BbM888888s888888LZ51VNi0844z7z3LT7208888888888888884w88888888888888885cM88888888M70888888887z8c5X/PP38s88+8888888/Y8888888888888888A8888888888888893U8/z/AP8Azzzzzz3XTzzzzzzsMJfzzzzzzzzyB7zzzzzzBzz/AK88888888888888888888s888888888c888/Loed888888sfPPHPPPeFlcPPPPPPf8A7/8Azzzzgwtdvzyzzzzxzzzzzzzzzzz3zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwxzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzDzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwzzzzzzzzyzzzTzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyzzzzzzxzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzTzTzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzxzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzyxzzzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzTzzzzzzzzzzzzzzzzzzzzzzzwzzzzzzzwxzzzzzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzDzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzwzzzzzzzzzyzzzzzzzzzzyzzzzzzzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzyzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz/8QAAv/aAAwDAQACAAMAAAAQ88888888888888888888888888888888888888888888888848888w88c888888888888888888888A888888888888888888888888880888888888888888888888888888888840888888888888888888888888888888888888888888888888888888888888888888888888840888888888888888888888888888c8888888888888888888888888888888888888888888888888888888888888888888888888888888888888c888888888888888888888888888888888888888888888088888888888888888888x8888c8c88888888888888888888888888888888888888888888888888c88888888888c888888888888888888888888888888c888888s888888888888888888888888888888888888888888888888sC88888888888888888888888888888888888888888888888888888888888884888888888888888sM48888888888888884888888888888888M888888888888888888888488888888888888888s88888888888888888888888888888888888888888888888888888888888884w888888888888888888888w88888888888888888888888888088888888888888888888888888888888888888888c888888888x888888888888888888888888888888888888888888888888888888888888888888888888888888M888888888888888888888s888888s88888888888888888888888c888888888888888808888888898888888888888888888888888888888888888888888888888888888888888888888888888888888888888888488888c808888888888888888888888888888888888888c8888888888888888888888888888888888888s888880808888886ggA03848888888ou+qS29888888888888888888888888888888888888888888888488888888887E488888888488884E8888s8c888888888888888888888888c88888888888888888888848888087H88888+l8888888mp0888881888488888c8888888888888888888888888888888888888888888+cc88888Xqc88888sW208Y88888888888888888888888888888888888s888888888888888888886o4s88888ro888888sim888888808c888808888888888888888888888888888888888888888888/wCcNH/PPPPAvvGdtBphNr2NPPPPPPPPPPPOPPPPPPPPPPPPPPPPPPPPPMPPPPPPPPPPPPPPPPPPPPPO2fOxPPPPPPJRLE/PC9vMgvPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPLPLPPPPI+DhHKxwnH/Xisu9PPPPPPPPPPOPPNPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPHPPPPPPPPPOPPNPPPLFqljT+g4HLI4x5VUpfPPPPPPPPPPPPPPPPPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPN3/bHDHLDLDDDLEAI2ofPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPPPPPPPPEfPPPPPGWvONPPPPPPMI8N4XPl8PPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPHPPPPPAqgNYlo85cHPPPPPL/2z6gWc/NGRctMKfPPPPPPPPPPPLPPPPPPPPPPPPPPPPPPPPPPPPPOPPPPPOFPKeHHJQtVH7fPPPPOZf3sKnE+/Ms+zBQ/FN7HPPHPPPPPPPPPPPPPPPPPDPPNPPPPPPPPPPPPPPPLPPJD1d7PPPPNLVPPPPIUZwHU483fHrPPKHDPPVNPPPPPPPPPPPPPPPPPPPPPPPPPPNPPPPPPPPPPPPPPPPPPPPPMDz9T/PPON/jp8ld/2R3BMy3DPPPAPPPPPDPPPPPPPPPPLPDDPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPB5/wA1rzxg5q2fs5HaClHyZu7mjzzu4ZzzzzzzyzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzxzzzzzzTzzzzzyTHzjLgmv1DBsGLaXxetTxDzhRFxzzzzzzzzzzzzzzzzzzzzzzzzjzzzzzzzzzzzzzzzzzzzh/DzzPPMMXyjLcg5T5aosw9/wAZ5c8z48DH2c8888888888888888888888888888888888888c88888YfnU8glZy0UoUmUp2xl1Ibq881H/vv88sPt8888888888888w888488888888888888488888888488opQU88s8Cc0oluzGLhToPMU88Dl88c480888888888888888888c8888888888888888s8880888888vXuck25+pO8805Nft2YkUO848ELchyD988c8848888888888888888888888888w888888888s888888F8EilYavbw8/KlHn2HKC8888pm2/gvE888888888888888888888888888888808888888888888888A8084887Ec8rAP6aNml88888BXM88888n888sc888888888888888888884888888888808s8888s88e8c8c88q0ZQIDQcs8888888kPc888888BU8c888888888888888888888888888888888888884M888888888c4LbVsMxx4x0qy3zmNzE8884yf28880888888c8888888888888888888888888888888888488c888809pE2nsjFPOgCN28le8888FKc8888888888c8888888888888888MM88888888888888888888t84888888vK0bVIk3MpsU88886sSv88c88888888888888888888898888M8888888888888488s8080Ic8888884W0O70ujw9888888Nel888888888888888888888888888888888s888s88888888888888sZ488888z885O89e8OC0888sr8888888888888888888888888c88888888888888888888888888888sK/27847A08888842lc881yo888888888888888888888888888w8888888888888888c88888888888s+uu888t88888888t888OO88488888888888888888888888888888888808888888888888888088888888848888888888888888888888888888888848488888s8888888888888488885xu08888putw88888886ma/888888888888888888488888888888888888888888888888888c8888qU0c8884AuVe8888888P9u0888888888888888888880888888888888848888888888888888888884ZM0888Rm+wl888c889CdBt888888888888888888888888s888888888888888x888888888888888JnUc884HAZO4888888gvk5Zi8884/04szx9m13gQW839wh2888888888888888888888888888888885NiU88K33BAEo888887vaysM08wnyGj+eDhOInimKuB8F5qQ88888888888888888888888888888887sBU845mtUAmj08883+5w5V9V88iB5fxgTfAVScnGBhZGxZHU8888c88888888888088888888888886mrU8+pIHAhXsU884k4wlEh66UgtJ888NH2ED988/6O88sQg488888888888888M888888888888888OSHU8MkdpHfCYR88jg0tFLkX3+4gW088Fs+TYe88rEn884K7888888888888888M8888888888888888XsU4BQ7jOMs4wbsK1B2LisN2Mwbvw4Mxa+DSe88sZR0w9XnU8888888888888888888888888888889ifwNCX888ssJeRx+T1c8s8c6q0EWDa2jj+b7688sMOXbTG44888888888888888888888888888888s+c06aX88888JO1H/H8c8884PtHw3EwYZDeqp3888hCP7g28w84888888888888w88s888s8884888888sIo0888848sU8c8888s88w8881n5529SIM848888s8888888888c88888888gA8888888888888888827xxx5195JMM888888s888888fT3f7/A08447/AO9y089tPPPPPPPPPPPPPPPOMPPPPPPPPPPPPPPPPIhTPPPPPPPPHC/PPPPPPPOM19HGB/zz93LPJrTPPPPPPPh/PPPPPPPPPPPPPPPAPPPPPPPPPPPPPPPShfP+/wDPzzzzzz2HTzzzzzysjNLzzzzzzzzzL3zzzzzzBzy7Hzzzzzzzzzzzzzzzzzzzyzzzzzzzzzxzzzxwq8T3zzzzzyx/9+d+9/0rhY//APvPfvPfe88884F4UK8888888c8888888888988888888888888888888888c8888888888888srS8888888888c888888888088888888888888888w88888888888888888888888888888888888888888888888888888888c80888888888888888888888888888888888888888888c88888888888888888888s8888888888888880888888888888888888M88888888s880888888c888888888888888848888888888888888888888888888888888888888888888888c88888888888888888888888888888888888888888888888888888888848888888888888888888888888888888888888888888888888888888888888808888888888888888888888888888888888888888888088888888888888888888888888888888888s888888c88888888888888888888s88888888888888888888888c888888888888888888888888888888808884888888888888884888888888888888888888888888888888888888888884888888888888808088888888888888s888888888888888888888888888888s88888888888888888888888888888888848888888888c888888888888888888888888888888c88888888888888888888888sc888888888888888888888888848888888888888888888888888888c8888888888888888848888888888888888888888888888888888888888888888888888888888880888888888888888888888888888888880888888888888888888888888M8888888Mc8888888888888888s8888888888888888888w88888888888888888888888888888888M888888888s8888888888s888888888888s888888888888888888888888888c8888s88s888888888888888Ac8888888888888888888888888888888888888888888888888888g8888888888888c8888//EAEQRAAEDAQQGBggEBAQHAQAAAAEAAgMRBBASMRMgITJRcTBBUFJhoQUUM1NygZHRIiNCspKxweE0QHOgFSRDYGJjgsL/2gAIAQIBAT8A/wBl897WAV6zQLSu9y/y+60rvcv8vutK73L/AC+60rvcv8vumyOJAMTx4mnROcRk0nktI73T/L7rSO90/wAvutI73T/L7rSO90/y+60p90/yTHte0FpqO2XvDBU/IdZKYw1xv3vIDgP8q5jmvxs695vHx59sPeGCp5AcSmMNcb97yGtaJzEGhoq5x2KO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">
""", unsafe_allow_html=True)

# ── Persiste token nos query_params e sessionStorage para sobreviver reload ──
if st.session_state.get("sb_token") and st.session_state.get("sb_user_id"):
    _tk  = st.session_state.sb_token
    _uid = st.session_state.sb_user_id
    _pl  = st.session_state.get("sb_plano","free")
    _nm  = st.session_state.get("usuario_atual","").replace(" ","_")[:20]
    _rf  = st.session_state.get("sb_refresh_token","")
    # Mantém query_params atualizados a cada render
    try:
        st.query_params["_u"]  = _uid
        st.query_params["_p"]  = _pl
        st.query_params["_n"]  = _nm
        st.query_params["_t1"] = _tk[:200]
        st.query_params["_t2"] = _tk[200:400]
        st.query_params["_t3"] = _tk[400:]
        if _rf:
            st.query_params["_rf"] = _rf[:200]
    except Exception:
        pass
    st.markdown(f"""
    <script>
    try {{
        sessionStorage.setItem('iaagro_token',   '{_tk}');
        sessionStorage.setItem('iaagro_uid',     '{_uid}');
        sessionStorage.setItem('iaagro_plano',   '{_pl}');
        sessionStorage.setItem('iaagro_usuario', '{_nm}');
    }} catch(e) {{}}
    </script>
    """, unsafe_allow_html=True)

