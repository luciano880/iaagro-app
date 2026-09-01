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
from streamlit_js_eval import (get_geolocation, streamlit_js_eval,
                               set_local_storage, get_local_storage, remove_local_storage)
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
    "🌲 Silvicultura": ["🌳 Eucalipto","🌲 Pinus","🌴 Teca","🌿 Paricá","🌲 Cedro","🌳 Mogno Africano"],
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

/* ── Esconde os iframes invisíveis do streamlit_js_eval (localStorage/geolocation) ──
   Eles não têm conteúdo visual mas ocupam espaço e criam uma faixa escura. */
iframe[title="streamlit_js_eval.streamlit_js_eval"],
[data-testid="stIFrame"][title*="streamlit_js_eval"],
.element-container:has(iframe[title*="streamlit_js_eval"]) {
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    display: block !important;
    visibility: hidden !important;
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
/* Mais respiro entre os itens do menu (melhor toque no celular) */
[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label {
    padding: 7px 8px !important;
    margin: 2px 0 !important;
    border-radius: 8px !important;
    transition: background .15s !important;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label:hover {
    background: rgba(34,197,94,0.10) !important;
}
/* Destaque especial para o item Assistente IA (4º item após os 3 primeiros
   grupos) — fundo e borda diferenciados para chamar atenção */
[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label:nth-of-type(9) {
    background: linear-gradient(90deg, rgba(234,179,8,0.15), rgba(34,197,94,0.10)) !important;
    border: 1px solid rgba(234,179,8,0.4) !important;
    box-shadow: 0 0 12px rgba(234,179,8,0.15) !important;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label:nth-of-type(9):hover {
    background: linear-gradient(90deg, rgba(234,179,8,0.25), rgba(34,197,94,0.15)) !important;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] > label:nth-of-type(9) p {
    color: #fde68a !important;
    font-weight: 800 !important;
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
def gerar_pdf_conversa_assistente(historico):
    """
    Gera um PDF profissional da conversa com o Assistente IA: cabeçalho de marca
    IAAgro, cada troca em cartão colorido (pergunta verde à esquerda, resposta
    azul), negrito preservado, e ressalva técnica obrigatória no fim.
    historico = lista de {"role": "user"/"assistant", "content": str}
    """
    import io as _io_c
    import re as _re_c
    from reportlab.lib.units import cm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import HRFlowable, KeepTogether

    _buf = _io_c.BytesIO()
    _doc = SimpleDocTemplate(_buf, pagesize=A4,
                             topMargin=1.2*cm, bottomMargin=1.5*cm,
                             leftMargin=1.6*cm, rightMargin=1.6*cm,
                             title="IAAgro - Conversa com Assistente")
    _el = []

    _verde     = colors.HexColor("#166534")
    _verde_esc = colors.HexColor("#14532d")
    _verde_cl  = colors.HexColor("#dcfce7")
    _verde_brd = colors.HexColor("#22c55e")
    _azul      = colors.HexColor("#0369a1")
    _azul_cl   = colors.HexColor("#eff6ff")
    _azul_brd  = colors.HexColor("#3b82f6")
    _cinza_bd  = colors.HexColor("#cbd5e1")
    _texto     = colors.HexColor("#1e293b")
    _sub       = colors.HexColor("#64748b")

    _st_marca  = ParagraphStyle("m", fontName="Helvetica-Bold", fontSize=22,
                                textColor=_verde, leading=24)
    _st_slogan = ParagraphStyle("s", fontName="Helvetica-Oblique", fontSize=8.5,
                                textColor=_sub, leading=11)
    _st_tit    = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=14,
                                textColor=_verde_esc, leading=17)
    _st_meta   = ParagraphStyle("me", fontName="Helvetica", fontSize=9,
                                textColor=_sub, leading=12)
    _st_rot_u  = ParagraphStyle("ru", fontName="Helvetica-Bold", fontSize=8,
                                textColor=_verde, leading=11, spaceAfter=3)
    _st_rot_b  = ParagraphStyle("rb", fontName="Helvetica-Bold", fontSize=8,
                                textColor=_azul, leading=11, spaceAfter=3)
    _st_user   = ParagraphStyle("u", fontName="Helvetica", fontSize=10,
                                textColor=_texto, leading=14)
    _st_bot    = ParagraphStyle("b", fontName="Helvetica", fontSize=10,
                                textColor=_texto, leading=14)

    def _limpa(txt):
        txt = txt or ""
        # Remove emojis e símbolos que a fonte do PDF não renderiza (viram quadrados)
        txt = _re_c.sub(
            "[" 
            "\U0001F300-\U0001FAFF"  # emojis diversos
            "\U00002600-\U000027BF"  # símbolos, setas decorativas
            "\U0001F000-\U0001F0FF"
            "\U00002190-\U000021FF"  # setas
            "\U00002B00-\U00002BFF"
            "\uFE0F\u200D"           # seletor de emoji e ZWJ
            "]+", "", txt)
        # Remove caracteres de controle invisíveis
        txt = "".join(ch for ch in txt if ch in "\n\t" or ord(ch) >= 32)
        # Tabelas markdown -> texto legível
        _linhas = []
        for _ln in txt.split("\n"):
            _s = _ln.strip()
            if _s.startswith("|") and set(_s.replace("|","").replace(" ","")) <= set("-:"):
                continue
            if _s.startswith("|") and _s.endswith("|"):
                _cels = [c.strip() for c in _s.strip("|").split("|")]
                _linhas.append(" | ".join(c for c in _cels if c))
            else:
                _linhas.append(_ln)
        txt = "\n".join(_linhas)
        # Escapa XML primeiro
        txt = txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # Converte **negrito** em tag do reportlab (depois do escape)
        txt = _re_c.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', txt)
        txt = _re_c.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', txt)
        txt = _re_c.sub(r'`(.+?)`', r'\1', txt)
        txt = _re_c.sub(r'^#{1,6}\s*', '', txt, flags=_re_c.M)
        txt = _re_c.sub(r'\[(.+?)\]\((.+?)\)', r'\1', txt)
        return txt.replace("\n", "<br/>")

    # ── CABEÇALHO ──
    _marca = [Paragraph("IAAgro", _st_marca),
              Paragraph("Assistente Agrícola Inteligente", _st_slogan)]
    _logo_ok = False
    if os.path.exists("IAAgrologo.jpeg"):
        try:
            _cab = Table([[Image("IAAgrologo.jpeg", width=2.4*cm, height=2.4*cm), _marca]],
                         colWidths=[2.8*cm, 13.5*cm])
            _cab.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                                      ("LEFTPADDING",(0,0),(0,0),0),
                                      ("LEFTPADDING",(1,0),(1,0),8)]))
            _el.append(_cab); _logo_ok = True
        except Exception:
            pass
    if not _logo_ok:
        _el.extend(_marca)

    _el.append(Spacer(1, 0.2*cm))
    _el.append(HRFlowable(width="100%", thickness=2.5, color=_verde, spaceAfter=8))
    _el.append(Paragraph("Registro de Conversa - Assistente IA", _st_tit))
    _el.append(Paragraph(f"Gerado em {datetime.now().strftime('%d/%m/%Y as %H:%M')}", _st_meta))
    _el.append(Spacer(1, 0.4*cm))

    # ── CARTÕES DE MENSAGEM ──
    for _m in historico:
        _is_user = _m.get("role") == "user"
        if _is_user:
            _rot, _st_rot, _st_txt = "PERGUNTA DO PRODUTOR", _st_rot_u, _st_user
            _bg, _brd = _verde_cl, _verde_brd
        else:
            _rot, _st_rot, _st_txt = "RESPOSTA DO ASSISTENTE IA", _st_rot_b, _st_bot
            _bg, _brd = _azul_cl, _azul_brd
        _conteudo = [Paragraph(_rot, _st_rot),
                     Paragraph(_limpa(_m.get("content","")), _st_txt)]
        _cel = Table([[_conteudo]], colWidths=[16.3*cm])
        _cel.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1), _bg),
            ("LINEBEFORE",(0,0),(-1,-1), 3, _brd),   # faixa colorida na lateral esquerda
            ("BOX",(0,0),(-1,-1), 0.5, _cinza_bd),
            ("LEFTPADDING",(0,0),(-1,-1), 12),
            ("RIGHTPADDING",(0,0),(-1,-1), 12),
            ("TOPPADDING",(0,0),(-1,-1), 8),
            ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ]))
        _el.append(_cel)
        _el.append(Spacer(1, 0.28*cm))

    # ── RESSALVA TÉCNICA ──
    _el.append(Spacer(1, 0.3*cm))
    _st_av_t = ParagraphStyle("avt", fontName="Helvetica-Bold", fontSize=11,
                              textColor=colors.HexColor("#7f1d1d"), leading=14)
    _st_av   = ParagraphStyle("av", fontName="Helvetica-Bold", fontSize=9.5,
                              textColor=colors.HexColor("#7f1d1d"), leading=14)
    _aviso = [
        Paragraph("⚠️ AVISO IMPORTANTE", _st_av_t),
        Spacer(1, 0.15*cm),
        Paragraph(
            "<b>As informações deste documento foram geradas por inteligência "
            "artificial e têm caráter APENAS ORIENTATIVO. Antes de qualquer "
            "aplicação de defensivos, fertilizantes ou correção de solo, "
            "CONSULTE SEMPRE O ENGENHEIRO AGRÔNOMO OU TÉCNICO RESPONSÁVEL "
            "pela sua propriedade. O receituário agronômico é obrigatório por lei "
            "para a aquisição e aplicação de agrotóxicos. O IAAgro não substitui "
            "a avaliação técnica presencial nem se responsabiliza por decisões "
            "tomadas sem acompanhamento profissional.</b>", _st_av),
    ]
    _cx = Table([[_aviso]], colWidths=[16.3*cm])
    _cx.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), colors.HexColor("#fef2f2")),
        ("BOX",(0,0),(-1,-1), 1.5, colors.HexColor("#ef4444")),
        ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
        ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),
    ]))
    _el.append(KeepTogether(_cx))

    # ── RODAPÉ ──
    _el.append(Spacer(1, 0.5*cm))
    _st_rod = ParagraphStyle("rod", fontName="Helvetica", fontSize=7.5,
                             textColor=_sub, alignment=TA_CENTER, leading=10)
    _el.append(HRFlowable(width="100%", thickness=0.7, color=_cinza_bd, spaceAfter=6))
    _el.append(Paragraph(
        "IAAgro - Inteligência Agrícola de Precisão - iaagropro.streamlit.app", _st_rod))

    try:
        _doc.build(_el)
    except Exception:
        _buf = _io_c.BytesIO()
        _doc2 = SimpleDocTemplate(_buf, pagesize=A4)
        _simp = [Paragraph("IAAgro - Conversa com Assistente", _st_tit), Spacer(1,0.5*cm)]
        for _m in historico:
            _who = "Voce:" if _m.get("role")=="user" else "IAAgro:"
            _safe = _limpa(_m.get("content",""))
            _simp.append(Paragraph(f"<b>{_who}</b> {_safe}", _st_bot))
            _simp.append(Spacer(1,0.3*cm))
        _simp.append(Spacer(1,0.3*cm))
        _st_av_fb = ParagraphStyle("avfb", fontName="Helvetica-Bold", fontSize=10.5,
                                   textColor=colors.HexColor("#7f1d1d"), leading=15)
        _aviso_fb = Paragraph(
            "<b>⚠️ AVISO IMPORTANTE: As informações acima foram geradas por "
            "inteligência artificial e têm caráter APENAS ORIENTATIVO. "
            "CONSULTE SEMPRE O ENGENHEIRO AGRÔNOMO OU TÉCNICO RESPONSÁVEL "
            "antes de qualquer aplicação. O receituário agronômico é "
            "obrigatório por lei.</b>", _st_av_fb)
        _cx_fb = Table([[_aviso_fb]], colWidths=[16.5*cm])
        _cx_fb.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1), colors.HexColor("#fef2f2")),
            ("BOX",(0,0),(-1,-1), 1.5, colors.HexColor("#ef4444")),
            ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
            ("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),12),
        ]))
        _simp.append(_cx_fb)
        _doc2.build(_simp)
    _buf.seek(0)
    return _buf.getvalue()


def gerar_pdf_lista_pecas(itens, titulo="Lista de Compras — Peças de Revisão"):
    """
    Gera um PDF profissional de lista de compras de peças (código + nome + máquina),
    com cabeçalho de marca IAAgro, pronto pra levar/imprimir e comprar na revenda.
    itens = lista de dicts: {"maquina","codigo","nome"}
    """
    import io as _io_pdf
    from reportlab.lib.units import cm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
    from reportlab.platypus import HRFlowable

    _buf = _io_pdf.BytesIO()
    _doc = SimpleDocTemplate(_buf, pagesize=A4,
                             topMargin=1.2*cm, bottomMargin=1.4*cm,
                             leftMargin=1.5*cm, rightMargin=1.5*cm,
                             title="IAAgro - Lista de Peças")
    _el = []

    # Paleta da marca
    _verde     = colors.HexColor("#166534")
    _verde_esc = colors.HexColor("#14532d")
    _verde_cl  = colors.HexColor("#dcfce7")
    _cinza_cl  = colors.HexColor("#f1f5f9")
    _cinza_bd  = colors.HexColor("#cbd5e1")
    _texto     = colors.HexColor("#1e293b")
    _sub       = colors.HexColor("#64748b")

    # ── Estilos ──
    _st_marca = ParagraphStyle("marca", fontName="Helvetica-Bold", fontSize=22,
                               textColor=_verde, leading=24, spaceAfter=0)
    _st_slogan = ParagraphStyle("slogan", fontName="Helvetica-Oblique", fontSize=8.5,
                                textColor=_sub, leading=11)
    _st_titulo = ParagraphStyle("tit", fontName="Helvetica-Bold", fontSize=14,
                                textColor=_verde_esc, leading=17, spaceBefore=2)
    _st_meta   = ParagraphStyle("meta", fontName="Helvetica", fontSize=9,
                                textColor=_sub, leading=12)
    _st_cel    = ParagraphStyle("cel", fontName="Helvetica", fontSize=9.5,
                                textColor=_texto, leading=12)
    _st_cod    = ParagraphStyle("cod", fontName="Courier-Bold", fontSize=9.5,
                                textColor=_verde, leading=12)
    _st_hdr    = ParagraphStyle("hdr", fontName="Helvetica-Bold", fontSize=9.5,
                                textColor=colors.white, leading=12)

    # ── CABEÇALHO: logo + marca ──
    _logo_ok = os.path.exists("IAAgrologo.jpeg")
    _marca_bloco = [
        Paragraph("IAAgro", _st_marca),
        Paragraph("Inteligência Agrícola de Precisão", _st_slogan),
    ]
    if _logo_ok:
        try:
            _logo_img = Image("IAAgrologo.jpeg", width=2.6*cm, height=2.6*cm)
            _cab = Table([[_logo_img, _marca_bloco]], colWidths=[3*cm, 13.5*cm])
            _cab.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, 0), 0),
                ("LEFTPADDING", (1, 0), (1, 0), 8),
            ]))
            _el.append(_cab)
        except Exception:
            _el.extend(_marca_bloco)
    else:
        _el.extend(_marca_bloco)

    # Faixa verde separadora
    _el.append(Spacer(1, 0.25*cm))
    _el.append(HRFlowable(width="100%", thickness=2.5, color=_verde,
                          spaceBefore=0, spaceAfter=8))

    # ── Título do documento + data ──
    _el.append(Paragraph(f"🔧 {titulo}", _st_titulo))
    _el.append(Paragraph(
        f"Lista de compras · Gerada em {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
        _st_meta))
    _el.append(Spacer(1, 0.45*cm))

    if not itens:
        _el.append(Paragraph("Nenhuma peça cadastrada nesta lista.", _st_cel))
    else:
        # Cabeçalho da tabela
        _dados_tab = [[
            Paragraph("#", _st_hdr),
            Paragraph("CÓDIGO", _st_hdr),
            Paragraph("PEÇA", _st_hdr),
            Paragraph("MÁQUINA", _st_hdr),
            Paragraph("✓", _st_hdr),
        ]]
        for _i, _it in enumerate(itens, 1):
            _cod = _it.get("codigo", "") or "—"
            _dados_tab.append([
                Paragraph(str(_i), _st_cel),
                Paragraph(_cod, _st_cod if _cod != "—" else _st_cel),
                Paragraph(_it.get("nome", ""), _st_cel),
                Paragraph(_it.get("maquina", ""), _st_cel),
                "",  # coluna do checkbox (desenhada como quadrado via BOX)
            ])
        _tab = Table(_dados_tab, colWidths=[0.9*cm, 3.3*cm, 6.4*cm, 4.9*cm, 1*cm])
        _estilo = [
            ("BACKGROUND", (0, 0), (-1, 0), _verde),
            ("TOPPADDING", (0, 0), (-1, 0), 7),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
            ("TOPPADDING", (0, 1), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("LINEBELOW", (0, 0), (-1, -1), 0.5, _cinza_bd),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, _cinza_cl]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("ALIGN", (4, 0), (4, -1), "CENTER"),
            ("LINEAFTER", (0, 0), (0, -1), 0.5, _cinza_bd),
            # Desenha o quadrado do checkbox em cada linha de dados
        ]
        for _r in range(1, len(_dados_tab)):
            _estilo.append(("BOX", (4, _r), (4, _r), 0.8, _sub))
            _estilo.append(("TOPPADDING", (4, _r), (4, _r), 2))
            _estilo.append(("BOTTOMPADDING", (4, _r), (4, _r), 2))
        _tab.setStyle(TableStyle(_estilo))
        _el.append(_tab)

        # Total
        _el.append(Spacer(1, 0.35*cm))
        _st_total = ParagraphStyle("tot", fontName="Helvetica-Bold", fontSize=10,
                                   textColor=_verde_esc, alignment=TA_RIGHT)
        _el.append(Paragraph(f"Total de itens: {len(itens)}", _st_total))

    # ── RODAPÉ ──
    _el.append(Spacer(1, 0.8*cm))
    _el.append(HRFlowable(width="100%", thickness=0.7, color=_cinza_bd,
                          spaceBefore=0, spaceAfter=6))
    _st_rodape = ParagraphStyle("rod", fontName="Helvetica", fontSize=7.5,
                                textColor=_sub, alignment=TA_CENTER, leading=10)
    _el.append(Paragraph(
        "Gerado pelo IAAgro · Inteligência Agrícola de Precisão · iaagropro.streamlit.app",
        _st_rodape))

    _doc.build(_el)
    _buf.seek(0)
    return _buf.getvalue()



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
        "harvest_historico":  st.session_state.get("harvest_historico", []),
        "receituarios":       st.session_state.get("receituarios", []),
        "safrinha_registros": st.session_state.get("safrinha_registros", []),
        "fluxo_caixa":        st.session_state.get("fluxo_caixa", []),
        "corretivos_aplicados": st.session_state.get("corretivos_aplicados", []),
        "contratos_troca":    st.session_state.get("contratos_troca", []),
        "planejamento_safras": st.session_state.get("planejamento_safras", []),
        "maquinas":           st.session_state.get("maquinas", []),
        "maquinas_revisoes":  st.session_state.get("maquinas_revisoes", []),
        "segmento":           st.session_state.get("segmento", None),
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
        st.session_state.fluxo_caixa         = dados.get("fluxo_caixa", [])
        st.session_state.corretivos_aplicados = dados.get("corretivos_aplicados", [])
        st.session_state.contratos_troca     = dados.get("contratos_troca", [])
        st.session_state.planejamento_safras = dados.get("planejamento_safras", [])
        st.session_state.maquinas            = dados.get("maquinas", [])
        st.session_state.maquinas_revisoes   = dados.get("maquinas_revisoes", [])
        st.session_state.segmento            = dados.get("segmento", None)
        if dados.get("email_config"):
            st.session_state.email_config = dados["email_config"]
        # Restauração de backup é ação explícita — libera salvar mesmo se vier vazio
        st.session_state["_dados_prontos"] = True
        st.session_state["_permite_salvar_vazio"] = True
        salvar_dados_iaagro()
        st.session_state["_permite_salvar_vazio"] = False
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
                "model":      "claude-sonnet-4-6",
                "max_tokens": 1000,
                "tools":      [{"type": "web_search_20250305", "name": "web_search"}],
                "messages":   [{"role": "user", "content": prompt}]
            },
            timeout=60
        )
        if resp.status_code != 200:
            _err_msg = f"HTTP {resp.status_code}"
            if resp.status_code == 401:
                _err_msg = "Chave API inválida ou expirada"
            elif resp.status_code == 429:
                _err_msg = "Limite de requisições atingido"
            st.session_state["_cepea_erro"] = _err_msg
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
                            "model":    "claude-sonnet-4-6",
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
def _arquivo_dados_do_usuario():
    """
    Caminho do arquivo de fallback local, ISOLADO POR USUÁRIO.

    Motivo: no Streamlit Cloud todos os usuários dividem o mesmo container e o
    mesmo /tmp. Um arquivo de caminho fixo faria o cliente B sobrescrever os
    dados do cliente A — e, se o Supabase falhasse, o B poderia carregar os
    dados do A. Cada usuário passa a ter seu próprio arquivo, identificado por
    um hash do user_id (hash para não expor o UID no nome do arquivo).
    """
    _uid = (st.session_state.get("sb_user_id")
            or st.session_state.get("usuario_atual")
            or "")
    if not _uid:
        # Sem usuário identificado: usa arquivo anônimo isolado da sessão
        _uid = "anonimo_" + str(st.session_state.get("_sessao_id", "local"))
    _tag = hashlib.sha256(str(_uid).encode("utf-8")).hexdigest()[:16]
    return str(_BASE_DIR / f"dados_iaagro_{_tag}.json")


def carregar_dados_iaagro():
    _vazio = {"dados": {}, "areas": [], "estoque": [], "aplicacoes": [],
              "historico_produtividade": [], "pluviometro": [],
              "carencia_registros": [], "dre_registros": [], "calendario_eventos": []}
    _arq = _arquivo_dados_do_usuario()
    if os.path.exists(_arq):
        try:
            with open(_arq, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except Exception:
            return _vazio
    return _vazio

def salvar_dados_iaagro():
    # ── SALVAGUARDA ANTI-PERDA ──
    # Não salvar se o carregamento inicial ainda não confirmou os dados.
    # Isso evita que um estado transitório vazio (durante autologin/reruns
    # do localStorage) sobrescreva no Supabase os dados reais do usuário.
    if not st.session_state.get("_dados_prontos", False):
        st.session_state["_ultimo_save"] = "⏳ Aguardando carregamento — não salvou"
        return

    # Proteção extra: se TUDO está vazio, provavelmente é um reset acidental.
    # Só permite salvar o estado totalmente vazio se o usuário confirmou que
    # realmente zerou (flag _permite_salvar_vazio), evitando apagar o banco.
    _tudo_vazio = (not st.session_state.get("areas") and
                   not st.session_state.get("estoque") and
                   not st.session_state.get("aplicacoes") and
                   not st.session_state.get("dre_registros"))
    if _tudo_vazio and not st.session_state.get("_permite_salvar_vazio", False):
        st.session_state["_ultimo_save"] = "🛡️ Estado vazio — salvamento bloqueado (proteção)"
        return

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
        "maquinas":                st.session_state.get("maquinas", []),
        "maquinas_revisoes":       st.session_state.get("maquinas_revisoes", []),
    }
    # Lê variáveis globais dinamicamente (podem não existir quando função é definida)
    _sb_url    = st.secrets.get("SUPABASE_URL", "") if hasattr(st, 'secrets') else ""
    _sb_key    = st.secrets.get("SUPABASE_ANON_KEY", "") if hasattr(st, 'secrets') else ""
    _sb_token  = st.session_state.get("sb_token", "")
    _sb_uid    = st.session_state.get("sb_user_id", "")
    _sb_ok     = bool(_sb_url and _sb_key and _sb_token and _sb_uid and _SB_DISPONIVEL)

    if _sb_ok:
        try:
            _res = sb_salvar(_sb_url, _sb_key, _sb_token, _sb_uid, dados_salvos, debug=True)
            # Compatível com versão nova (tupla) e antiga (bool)
            if isinstance(_res, tuple):
                ok, _motivo = _res
            else:
                ok, _motivo = _res, "versão antiga (sem debug)"
            st.session_state["_save_motivo"] = _motivo
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
                                _rfn = _novo.get("refresh_token","")
                                if _rfn and st.session_state.get("sb_manter_login", True):
                                    st.query_params["_rf1"] = _rfn[:200]
                                    st.query_params["_rf2"] = _rfn[200:400]
                                    st.query_params["_rf3"] = _rfn[400:]
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
    # Fallback: arquivo local — isolado por usuário (ver _arquivo_dados_do_usuario)
    try:
        with open(_arquivo_dados_do_usuario(), "w", encoding="utf-8") as arquivo:
            json.dump(dados_salvos, arquivo, indent=4, ensure_ascii=False)
    except Exception:
        pass

def carregar_areas():
    # ⚠️ LEGADO — não use. Usa caminho fixo compartilhado entre usuários no
    # Streamlit Cloud (risco de um cliente ler dados de outro). Mantida apenas
    # por compatibilidade; as áreas vêm de salvar/carregar_dados_iaagro().
    if os.path.exists(ARQUIVO_AREAS):
        with open(ARQUIVO_AREAS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return []

def salvar_areas(areas):
    # ⚠️ LEGADO — veja o aviso em carregar_areas().
    with open(ARQUIVO_AREAS, "w", encoding="utf-8") as arquivo:
        json.dump(areas, arquivo, indent=4, ensure_ascii=False)

# CORREÇÃO 2: carregar_area_por_id movida para escopo global
def carregar_area_por_id(id_area):
    for area in st.session_state.areas:
        if area.get("ID") == id_area:
            st.session_state.dados = area.get("Dados", {}).copy()
            st.session_state.aplicacoes = area.get("Aplicacoes", []).copy()
            st.session_state.estoque = area.get("Estoque", []).copy()
            # Recupera o desenho/croqui vinculado à área, se houver
            if area.get("desenho"):
                st.session_state.dados["desenho_talhao"] = area["desenho"]
                if area.get("area_calculada_ha"):
                    st.session_state.dados["area_calculada_ha"] = area["area_calculada_ha"]
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
def _salvar_sessao_local(uid, plano, nome, token, refresh):
    """Salva a sessão no localStorage do navegador (persiste entre aberturas)."""
    try:
        import json as _json_ls
        _payload = _json_ls.dumps({
            "u": uid, "p": plano, "n": nome, "t": token, "rf": refresh
        })
        set_local_storage("iaagro_sessao", _payload, component_key="ls_save_sessao")
    except Exception:
        pass


def _limpar_sessao_local():
    """Remove a sessão do localStorage (usado no logout)."""
    try:
        remove_local_storage("iaagro_sessao", component_key="ls_clear_sessao")
    except Exception:
        pass


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
        # Refresh token completo (3 partes). Compatível com formato antigo (_rf)
        _rf  = (params.get("_rf1", "") + params.get("_rf2", "") + params.get("_rf3", "")) \
               or params.get("_rf", "")

        # Se não achou na URL, tenta o localStorage do navegador (mais persistente)
        if not (_tk and _uid):
            try:
                import json as _json_ls2
                _raw = get_local_storage("iaagro_sessao", component_key="ls_read_sessao")
                # O componente é assíncrono: na 1ª passada retorna None enquanto carrega.
                # Damos até 3 reruns pra ele responder antes de desistir.
                if _raw is None:
                    _tentativas = st.session_state.get("_ls_tentativas", 0)
                    if _tentativas < 3:
                        st.session_state["_ls_tentativas"] = _tentativas + 1
                        import time as _time_ls
                        _time_ls.sleep(0.4)
                        st.rerun()
                if _raw:
                    st.session_state["_ls_tentativas"] = 0
                    # get_local_storage já devolve o valor; pode vir como dict ou string JSON
                    if isinstance(_raw, str):
                        _sess = _json_ls2.loads(_raw)
                    elif isinstance(_raw, dict):
                        _sess = _raw
                    else:
                        _sess = {}
                    _tk  = _sess.get("t", "")
                    _uid = _sess.get("u", "")
                    _pl  = _sess.get("p", "free")
                    _nm  = _sess.get("n", "")
                    _rf  = _sess.get("rf", "")
            except Exception:
                pass
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
                        st.query_params["_rf1"] = _rf[:200]
                        st.query_params["_rf2"] = _rf[200:400]
                        st.query_params["_rf3"] = _rf[400:]
                except Exception:
                    pass
                # Renova também no localStorage (persistência real)
                if st.session_state.get("sb_manter_login", True):
                    _salvar_sessao_local(_uid, st.session_state.sb_plano,
                                         (_nm or "Usuário"), _tk, _rf)
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
                manter_l = st.checkbox("🔒 Manter conectado neste dispositivo", value=True,
                                       key="sb_manter_login",
                                       help="Deixe marcado no seu celular/computador pessoal. "
                                            "Desmarque em dispositivos compartilhados.")
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
                        # Login bem-sucedido: dados vieram do Supabase, libera salvar
                        st.session_state["_dados_prontos"] = True
                        if dados_sb:
                            for k, v in dados_sb.items():
                                if k not in st.session_state:
                                    setattr(st.session_state, k, v)
                            # Aplica segmento do cadastro se for primeiro login
                            if not dados_sb.get("segmento") and st.session_state.get("_seg_novo_usuario"):
                                st.session_state.segmento = st.session_state.pop("_seg_novo_usuario")
                                st.session_state["_permite_salvar_vazio"] = True  # 1º login, conta nova
                                salvar_dados_iaagro()
                                st.session_state["_permite_salvar_vazio"] = False
                        elif st.session_state.get("_seg_novo_usuario"):
                            st.session_state.segmento = st.session_state.pop("_seg_novo_usuario")
                        # Salva refresh info nos query_params para auto-login após reload
                        # SÓ se o usuário marcou "Manter conectado"
                        if st.session_state.get("sb_manter_login", True):
                            try:
                                _nome_url = (res["nome"] or res["email"]).replace(" ", "_")[:20]
                                _tk_full = res["token"]
                                _rf_full = res.get("refresh_token","")
                                st.query_params["_u"] = res["user_id"]
                                st.query_params["_p"] = st.session_state.sb_plano
                                st.query_params["_n"] = _nome_url
                                st.query_params["_t1"] = _tk_full[:200]
                                st.query_params["_t2"] = _tk_full[200:400]
                                st.query_params["_t3"] = _tk_full[400:]
                                # Refresh token completo (pode passar de 200 chars)
                                st.query_params["_rf1"] = _rf_full[:200]
                                st.query_params["_rf2"] = _rf_full[200:400]
                                st.query_params["_rf3"] = _rf_full[400:]
                                # Salva também no localStorage do navegador (persistência real)
                                _salvar_sessao_local(res["user_id"], st.session_state.sb_plano,
                                                     _nome_url, _tk_full, _rf_full)
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
                btn_c = st.form_submit_button("✅ Criar Conta", use_container_width=True)

            # Segmento FORA do form para atualizar culturas em tempo real
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
                    f'<span style="background:#14532d;color:#6ee7b7;padding:2px 8px;border-radius:6px;font-size:12px;font-weight:600;">{c.split(" ",1)[-1] if " " in c else c}</span>'
                    for c in _culturas_seg_c
                )
                st.markdown(f"<div style='margin:6px 0 10px;'>{_nomes_cult}</div>", unsafe_allow_html=True)
            with st.container():
                pass  # placeholder after radio
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
                            # Endpoint /recover é o específico para RESET DE SENHA.
                            # Gera um código do tipo "recovery" enviado por e-mail.
                            r = _req.post(
                                f"{_SB_URL}/auth/v1/recover",
                                headers={"apikey": _SB_KEY, "Content-Type": "application/json"},
                                json={"email": email_r.strip()},
                                timeout=10
                            )
                            if r.status_code in (200, 204):
                                st.session_state["_recup_email"] = email_r.strip()
                                st.success(f"✅ Código enviado para **{email_r.strip()}**!")
                                st.info("📧 Verifique seu e-mail (inclusive spam) e copie o código numérico.")
                                st.rerun()
                            else:
                                st.error("❌ Não foi possível enviar. Verifique se o e-mail está cadastrado.")
                        except Exception as e:
                            st.error(f"❌ Erro: {e}")
            else:
                _email_recup = st.session_state["_recup_email"]
                st.info(f"📧 Código enviado para **{_email_recup}**")
                st.warning("⚠️ O e-mail traz um **código numérico**. **Não clique no link** — "
                           "copie apenas os números do código.")

                with st.form("form_otp_sb", clear_on_submit=False):
                    otp_code   = st.text_input("Código do e-mail (só números)", key="sb_otp_code",
                                               placeholder="123456", max_chars=10)
                    nova_senha = st.text_input("Nova senha (mín. 6 caracteres)", type="password", key="sb_nova_senha")
                    conf_nova  = st.text_input("Confirmar nova senha", type="password", key="sb_conf_nova")
                    btn_otp    = st.form_submit_button("🔐 Redefinir Senha", use_container_width=True)

                if btn_otp:
                    # Aceita qualquer código de 6 a 10 dígitos (Supabase varia entre 6 e 8)
                    _otp_limpo = "".join(c for c in (otp_code or "") if c.isdigit())
                    if len(_otp_limpo) < 6:
                        st.error("Digite o código numérico completo do e-mail (6 a 8 dígitos).")
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
                                json={"type": "recovery", "email": _email_recup, "token": _otp_limpo},
                                timeout=10
                            )
                            if r.status_code != 200:
                                # Tenta com type "magiclink" e depois "email" (compatibilidade)
                                for _tipo in ("magiclink", "email"):
                                    r = _req.post(
                                        f"{_SB_URL}/auth/v1/verify",
                                        headers={"apikey": _SB_KEY, "Content-Type": "application/json"},
                                        json={"type": _tipo, "email": _email_recup, "token": _otp_limpo},
                                        timeout=10
                                    )
                                    if r.status_code == 200:
                                        break
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
        "ia_perguntas_mes": 5,
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
            "Planejamento de Safras",
        ]
    },
    "pro": {
        "nome":    "💎 Pro",
        "preco":   39.90,
        "areas":   10,
        "estoque": 100,
        "ia_perguntas_mes": 150,
        "cor":     "#1e3a5f",
        "borda":   "#3b82f6",
        "recursos": [
            "10 áreas cadastradas",
            "100 itens de estoque",
            "Diagnóstico completo EMBRAPA",
            "Relatório PDF premium",
            "Importação NF-e XML",
            "Preços CEPEA tempo real",
            "Planejamento de Safras",
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
        "preco":   99.90,
        "areas":   -1,   # ilimitado
        "estoque": -1,   # ilimitado
        "ia_perguntas_mes": 500,   # uso justo
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
MP_LINK_PRO_MES     = "https://www.mercadopago.com.br/subscriptions/checkout?preapproval_plan_id=01acc9e1ce454303a618b885331ae9e5"
MP_LINK_PREMIUM_MES = "https://www.mercadopago.com.br/subscriptions/checkout?preapproval_plan_id=416dbeae6a3247318f68384d489db649"
MP_LINK_PRO_ANO     = "https://www.mercadopago.com.br/subscriptions/checkout?preapproval_plan_id=ef9d65771cee403091026fdb75f6de9b"
MP_LINK_PREMIUM_ANO = "https://www.mercadopago.com.br/subscriptions/checkout?preapproval_plan_id=9efddff1bb814a3fa0d1c527104e4ea1"
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
    st.session_state["_ls_persistido"] = False
    try:
        st.query_params.clear()
    except Exception:
        pass
    _limpar_sessao_local()
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
if "maquinas" not in st.session_state or (not st.session_state.get("maquinas") and dados_carregados.get("maquinas")):
    st.session_state.maquinas = dados_carregados.get("maquinas", [])
if "maquinas_revisoes" not in st.session_state or (not st.session_state.get("maquinas_revisoes") and dados_carregados.get("maquinas_revisoes")):
    st.session_state.maquinas_revisoes = dados_carregados.get("maquinas_revisoes", [])

# ── LIBERA O SALVAMENTO (salvaguarda anti-perda) ──
# Só marca "dados prontos" quando o carregamento inicial terminou de fato.
# Enquanto o autologin ainda faz reruns (localStorage assíncrono), sb_token
# pode não estar pronto e dados_carregados vem vazio — nesse caso NÃO liberamos
# o salvamento, pra não gravar um estado vazio por cima dos dados reais.
_carregamento_teve_dados = bool(
    dados_carregados.get("areas") or dados_carregados.get("estoque") or
    dados_carregados.get("aplicacoes") or dados_carregados.get("dre_registros") or
    dados_carregados.get("dados")
)
_sessao_ja_tem_dados = bool(
    st.session_state.get("areas") or st.session_state.get("estoque") or
    st.session_state.get("aplicacoes")
)
# Libera salvar se: (a) o banco trouxe dados, ou (b) a sessão já tem dados de
# uma edição em andamento, ou (c) confirmadamente é usuário novo sem token pendente.
if _carregamento_teve_dados or _sessao_ja_tem_dados:
    st.session_state["_dados_prontos"] = True
elif st.session_state.get("sb_user_id") and not st.session_state.get("_ls_tentativas"):
    # Logado, sem dados em lugar nenhum e sem autologin pendente = usuário novo real
    st.session_state["_dados_prontos"] = True

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

    # ── FMC Fertilizantes ──
    {"nome":"Regent 800 WG","fab":"FMC","cat":"Inseticida","ia":"Fipronil"},
    {"nome":"FMC Nitro Gold","fab":"FMC","cat":"Fertilizante","ia":"Nitrogênio líquido estabilizado"},
    {"nome":"FMC Potássio Líquido","fab":"FMC","cat":"Fertilizante","ia":"K2O 30% líquido"},
    {"nome":"FMC Starter","fab":"FMC","cat":"Fertilizante","ia":"NPK starter líquido para sulco"},
    # ── Corteva Fertilizantes ──
    {"nome":"Encrust","fab":"Corteva","cat":"Tratamento de Sementes","ia":"Polímero + NPK micronutrientes"},
    {"nome":"Corteva N-Enhance","fab":"Corteva","cat":"Fertilizante","ia":"Nitrogênio estabilizado + NBPT"},
    # ── Ihara ──
    {"nome":"Ihara Cobre BR","fab":"Ihara","cat":"Fungicida/Fertilizante","ia":"Oxicloreto de Cobre 84%"},
    {"nome":"Ihara Boro Quelatado","fab":"Ihara","cat":"Fertilizante","ia":"Boro EDTA 10%"},
    {"nome":"Ihara Zinco Quelatado","fab":"Ihara","cat":"Fertilizante","ia":"Zinco EDTA 14%"},
    {"nome":"Ihara Manganês Quelatado","fab":"Ihara","cat":"Fertilizante","ia":"Manganês EDTA 12%"},
    {"nome":"Ihara Mix Micro","fab":"Ihara","cat":"Fertilizante","ia":"B+Cu+Mn+Zn+Mo quelatados"},
    # ── CHDS (Crop Health Direct Solutions) ──
    {"nome":"CHDS Potássio Silicatado","fab":"CHDS","cat":"Fertilizante","ia":"K2SiO3 – Silicato de Potássio"},
    {"nome":"CHDS Silício Foliar","fab":"CHDS","cat":"Fertilizante","ia":"Si foliar estabilizador"},
    {"nome":"CHDS Amino Stress","fab":"CHDS","cat":"Fertilizante","ia":"Aminoácidos + micronutrientes anti-stress"},
    {"nome":"CHDS Enxofre 90 WDG","fab":"CHDS","cat":"Fertilizante","ia":"Enxofre elementar 90%"},
    # ── Timac Agro ──
    {"nome":"Physiostart","fab":"Timac Agro","cat":"Fertilizante","ia":"NPK + Seactiv – arranque radicular"},
    {"nome":"Physiomax","fab":"Timac Agro","cat":"Fertilizante","ia":"Cálcio + Magnésio + Seactiv"},
    {"nome":"Timac MAP Premium","fab":"Timac Agro","cat":"Fertilizante","ia":"MAP 11-52-00 com Seactiv"},
    {"nome":"Timac KCl Premium","fab":"Timac Agro","cat":"Fertilizante","ia":"KCl 00-00-60 granulado premium"},
    {"nome":"Timac Urea+","fab":"Timac Agro","cat":"Fertilizante","ia":"Ureia + NBPT inibidor de urease"},
    {"nome":"Timac Basacote","fab":"Timac Agro","cat":"Fertilizante","ia":"NPK liberação lenta revestido"},
    {"nome":"Fertileader Alpha","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"Seactiv + Aminoácidos + Zn"},
    {"nome":"Fertileader Max","fab":"Timac Agro","cat":"Foliar / Nutrição","ia":"Seactiv + B + Mo + Mn"},
    # ── Mosaic ──
    {"nome":"MicroEssentials SZ","fab":"Mosaic","cat":"Fertilizante","ia":"MAP + S + Zn – 12-40-00+10S+1Zn"},
    {"nome":"Mosaic MAP","fab":"Mosaic","cat":"Fertilizante","ia":"MAP 11-52-00 granulado"},
    {"nome":"Mosaic KCl Standard","fab":"Mosaic","cat":"Fertilizante","ia":"KCl 00-00-60 granulado"},
    {"nome":"Mosaic DAP","fab":"Mosaic","cat":"Fertilizante","ia":"DAP 18-46-00"},
    {"nome":"Mosaic SulPoMag","fab":"Mosaic","cat":"Fertilizante","ia":"K2SO4·MgSO4 – 00-00-22+11Mg+22S"},
    {"nome":"MicroEssentials S15","fab":"Mosaic","cat":"Fertilizante","ia":"10-40-00+15S – MAP+S"},
    {"nome":"Mosaic Granol 25-00-25","fab":"Mosaic","cat":"Fertilizante","ia":"NPK 25-00-25 granulado"},
    {"nome":"Mosaic NPK 08-28-16","fab":"Mosaic","cat":"Fertilizante","ia":"NPK 08-28-16 granulado"},
    {"nome":"Mosaic NPK 04-20-20","fab":"Mosaic","cat":"Fertilizante","ia":"NPK 04-20-20 granulado"},
    {"nome":"Mosaic NPK 05-25-25","fab":"Mosaic","cat":"Fertilizante","ia":"NPK 05-25-25 granulado"},
    # ── Fertipar ──
    {"nome":"Fertipar Sulfato de Amônio","fab":"Fertipar","cat":"Fertilizante","ia":"21% N + 24% S granulado"},
    {"nome":"Fertipar Ureia Perolada","fab":"Fertipar","cat":"Fertilizante","ia":"Ureia 45% N perolada"},
    {"nome":"Fertipar MAP","fab":"Fertipar","cat":"Fertilizante","ia":"MAP 11-52-00"},
    {"nome":"Fertipar KCl","fab":"Fertipar","cat":"Fertilizante","ia":"KCl 00-00-60"},
    {"nome":"Fertipar Superfosfato Simples","fab":"Fertipar","cat":"Fertilizante","ia":"SPS 18% P2O5 + 12% S"},
    {"nome":"Fertipar Superfosfato Triplo","fab":"Fertipar","cat":"Fertilizante","ia":"SFT 41% P2O5"},
    {"nome":"Fertipar Nitrato de Cálcio","fab":"Fertipar","cat":"Fertilizante","ia":"15,5% N + 26% CaO"},
    {"nome":"Fertipar Nitrato de Potássio","fab":"Fertipar","cat":"Fertilizante","ia":"13% N + 46% K2O"},
    {"nome":"Fertipar Sulfato de Potássio","fab":"Fertipar","cat":"Fertilizante","ia":"50% K2O + 17% S"},
    {"nome":"Fertipar NPK 05-20-20","fab":"Fertipar","cat":"Fertilizante","ia":"NPK 05-20-20"},
    {"nome":"Fertipar NPK 08-20-20","fab":"Fertipar","cat":"Fertilizante","ia":"NPK 08-20-20"},
    {"nome":"Fertipar NPK 10-10-10","fab":"Fertipar","cat":"Fertilizante","ia":"NPK 10-10-10"},
    {"nome":"Fertipar NPK 12-06-12","fab":"Fertipar","cat":"Fertilizante","ia":"NPK 12-06-12"},
    # ── Yara ──
    {"nome":"Yarabela Tropicote","fab":"Yara","cat":"Fertilizante","ia":"Nitrato de Amônio 27% N granulado"},
    {"nome":"Yarabela Sulfan","fab":"Yara","cat":"Fertilizante","ia":"Nitrato de Amônio + Sulfato 26% N+14S"},
    {"nome":"YaraMila Complex","fab":"Yara","cat":"Fertilizante","ia":"NPK 12-11-18+S+Mg+micro"},
    {"nome":"YaraMila Actyva S","fab":"Yara","cat":"Fertilizante","ia":"NPK 12-11-18+9S"},
    {"nome":"YaraMila Winner","fab":"Yara","cat":"Fertilizante","ia":"NPK 15-09-20+S"},
    {"nome":"YaraVita Stopit","fab":"Yara","cat":"Foliar / Nutrição","ia":"Cálcio líquido foliar"},
    {"nome":"YaraVita Bortrac","fab":"Yara","cat":"Foliar / Nutrição","ia":"Boro etanolamina 15%"},
    {"nome":"YaraVita Zintrac","fab":"Yara","cat":"Foliar / Nutrição","ia":"Zinco líquido 70 g/L"},
    {"nome":"YaraVita Mantrac","fab":"Yara","cat":"Foliar / Nutrição","ia":"Manganês líquido 500 g/L"},
    {"nome":"YaraVita Cobratec","fab":"Yara","cat":"Foliar / Nutrição","ia":"Cobre líquido 190 g/L"},
    {"nome":"YaraVita Molytrac","fab":"Yara","cat":"Foliar / Nutrição","ia":"Molibdênio líquido"},
    {"nome":"YaraVita Kombiphos","fab":"Yara","cat":"Foliar / Nutrição","ia":"P + K + Mn + Zn foliar"},
    {"nome":"YaraTera Rexolin","fab":"Yara","cat":"Fertilizante","ia":"Micronutrientes quelatados solúveis"},
    {"nome":"Yara Ureia Prill","fab":"Yara","cat":"Fertilizante","ia":"Ureia 45% N prilled"},
    {"nome":"Yara MAP","fab":"Yara","cat":"Fertilizante","ia":"MAP 11-52-00"},
    {"nome":"Yara KCl Granulado","fab":"Yara","cat":"Fertilizante","ia":"KCl 00-00-60"},]


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
            # Sincroniza as aplicações da área SEM descartar nenhuma:
            # adota as órfãs (sem ID) para a área atual e mantém todas as
            # que já estão em memória. Nunca remove aplicações aqui — isso
            # evita perda de dados ao salvar estoque/dados com contexto trocado.
            for _app in st.session_state.aplicacoes:
                if _app.get("ID Área", "") in ("", None):
                    _app["ID Área"] = id_area
            st.session_state.areas[i]["Aplicacoes"] = list(st.session_state.aplicacoes)
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

    def _preco_pdf(nome_insumo):
        """Preço unitário (R$/kg ou R$/L) do estoque, direto — sem conversão por saca."""
        _it = next((e for e in st.session_state.estoque if e.get("Insumo") == nome_insumo), None)
        return preco_por_kg_ou_l(_it)  # (preco, base, aviso)

    def _valor_semente_pdf(nome_variedade):
        """
        Pra SEMENTE, INOCULANTE e MICRO o custo é o VALOR TOTAL do lote no
        estoque (o que foi pago por aquele produto pra área toda), sem
        multiplicar por dose — ex: a BMX 53IX55 pra 32 ha custou R$ 19.942,17.
        Retorna (valor_unitario_cadastrado, valor_total_lote, qtd_lote, unid_lote).
        """
        _it = next((e for e in st.session_state.estoque if e.get("Insumo") == nome_variedade), None)
        if not _it:
            return 0.0, 0.0, 0.0, ""
        _vu = float(_it.get("Valor Unitário R$", 0) or 0)
        _vt = float(_it.get("Valor Total R$", 0) or 0)
        _qt = float(_it.get("Quantidade", 0) or 0)
        _un = _it.get("Unidade","")
        if _vt <= 0:  # fallback: quantidade × unitário
            _vt = round(_qt * _vu, 2)
        return _vu, _vt, _qt, _un

    def _qtd_base_pdf(qtd, unid):
        """Converte mL→L e g→kg pra bater com o preço (que é sempre por kg ou L)."""
        u = (unid or "").lower().replace(" ", "")
        base = u.split("/")[0]
        if base == "ml": return qtd/1000
        if base == "g":  return qtd/1000
        if base == "mg": return qtd/1_000_000
        return qtd

    _custo_total_pdf = 0.0

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
               P("POR TANQUE",8,True,COR_BRANCO,TA_CENTER),P("TOTAL AREA",8,True,COR_BRANCO,TA_CENTER),
               P("VALOR UNIT",8,True,COR_BRANCO,TA_CENTER),P("VALOR TOTAL",8,True,COR_BRANCO,TA_CENTER)]
        rows = [hdr]
        _custo_aplic = 0.0

        # ── Produtos defensivos normais ─────────────────────────────────────
        for p in aplic.get("Produtos",[]):
            unid = p.get("Unidade","").replace("/ha","")
            if p.get("Preço Unitário R$") is not None:
                _pr_u = float(p.get("Preço Unitário R$",0))
            else:
                _pr_u, _base_pr, _ = _preco_pdf(p.get("Produto",""))
            if p.get("Custo Total R$") is not None:
                _pr_t = float(p.get("Custo Total R$",0))
            else:
                _pr_t = round(_qtd_base_pdf(p.get("Total usado",0), p.get("Unidade","")) * _pr_u, 2)
            _custo_aplic += _pr_t
            rows.append([
                P(f"<b>{p.get('Produto','')}</b>",8,True),
                P(p.get("Tipo",""),8),
                P(str(p.get("Dose por ha",0)),8,False,None,TA_CENTER),
                P(p.get("Unidade",""),8,False,None,TA_CENTER),
                P(f"<b>{p.get('Produto por tanque',0):.2f}</b> {unid}",8,True,None,TA_CENTER),
                P(f"<b>{p.get('Total usado',0):.2f}</b> {unid}",8,True,COR_VERDE_E,TA_CENTER),
                P(f"R$ {_pr_u:.2f}",8,False,None,TA_CENTER),
                P(f"<b>R$ {_pr_t:,.2f}</b>",8,True,COR_VERDE_E,TA_CENTER),
            ])

        # ── Dados de Plantio (semente, fertilizantes, inoculantes) ─────────
        _dp = aplic.get("Dados Plantio", {})
        if _dp:
            # Sementes — múltiplas variedades
            _vars_pdf = _dp.get("variedades", [])
            if _vars_pdf:
                _tsi_pdf = f" | TSI: {_dp['tsi']}" if _dp.get("tsi") else ""
                for _vp in _vars_pdf:
                    _pr_u, _pr_t, _, _ = _valor_semente_pdf(_vp.get("nome",""))
                    _custo_aplic += _pr_t
                    rows.append([
                        P(f"<b>🌱 {_vp.get('nome','Semente')}</b> · {_vp.get('pop',0):,} pl/ha · {_vp.get('esp',0)} cm{_tsi_pdf}",8,True,colors.HexColor("#14532d")),
                        P("Semente",8),
                        P(str(_vp.get("dose",0)),8,False,None,TA_CENTER),
                        P("kg/ha",8,False,None,TA_CENTER),
                        P(f"{_vp.get('ha',0)} ha",8,False,None,TA_CENTER),
                        P(f"<b>{_vp.get('total_kg',0):,.0f}</b> kg",8,True,COR_VERDE_E,TA_CENTER),
                        P(f"R$ {_pr_u:.2f}",8,False,None,TA_CENTER),
                        P(f"<b>R$ {_pr_t:,.2f}</b>",8,True,COR_VERDE_E,TA_CENTER),
                    ])
            elif _dp.get("semente") or _dp.get("dose_sem_ha",0) > 0:
                _sem_nome = _dp.get("semente","Semente")
                _tsi = f" | TSI: {_dp['tsi']}" if _dp.get("tsi") else ""
                _pop = f" | Pop: {_dp.get('populacao',0):,} pl/ha" if _dp.get("populacao",0) > 0 else ""
                _pr_u, _pr_t, _, _ = _valor_semente_pdf(_sem_nome)
                _custo_aplic += _pr_t
                rows.append([
                    P(f"<b>🌱 {_sem_nome}</b>{_pop}{_tsi}",8,True,colors.HexColor("#14532d")),
                    P("Semente",8),
                    P(str(_dp.get("dose_sem_ha",0)),8,False,None,TA_CENTER),
                    P("kg/ha",8,False,None,TA_CENTER),
                    P("—",8,False,None,TA_CENTER),
                    P(f"<b>{_dp.get('semente_total_kg',0):,.0f}</b> kg",8,True,COR_VERDE_E,TA_CENTER),
                    P(f"R$ {_pr_u:.2f}",8,False,None,TA_CENTER),
                    P(f"<b>R$ {_pr_t:,.2f}</b>",8,True,COR_VERDE_E,TA_CENTER),
                ])
            # Adubos de base (lista — pode ter 2+ tipos, ex: Inrizza + Top Phos)
            _adubos_pdf = _dp.get("adubos") or (
                [{"nome": _dp["adubo_nome"], "kg_ha": _dp.get("adubo_kg_ha",0),
                  "total_kg": _dp.get("adubo_total_kg",0)}]
                if _dp.get("adubo_nome") and _dp.get("adubo_kg_ha",0) > 0 else []
            )
            for _adb in _adubos_pdf:
                _pr_u, _base_pr, _ = _preco_pdf(_adb.get("nome",""))
                _adb_total = _adb.get("total_kg",0) or round(_adb.get("kg_ha",0) * float(_adb.get("ha",0) or aplic.get("Área aplicada ha",0) or 0), 1)
                _pr_t = round(_adb_total * _pr_u, 2)
                _custo_aplic += _pr_t
                rows.append([
                    P(f"<b>🟡 {_adb.get('nome','')}</b>",8,True),
                    P("Fertilizante",8),
                    P(str(_adb.get("kg_ha",0)),8,False,None,TA_CENTER),
                    P("kg/ha",8,False,None,TA_CENTER),
                    P(f"{_adb.get('ha',0)} ha" if _adb.get("ha",0) else "—",8,False,None,TA_CENTER),
                    P(f"<b>{_adb_total:,.0f}</b> kg",8,True,COR_VERDE_E,TA_CENTER),
                    P(f"R$ {_pr_u:.2f}",8,False,None,TA_CENTER),
                    P(f"<b>R$ {_pr_t:,.2f}</b>",8,True,COR_VERDE_E,TA_CENTER),
                ])
            # KCl
            if _dp.get("kcl_nome") and _dp.get("kcl_kg_ha",0) > 0:
                _pr_u, _base_pr, _ = _preco_pdf(_dp["kcl_nome"])
                _pr_t = round(_dp.get("kcl_total_kg",0) * _pr_u, 2)
                _custo_aplic += _pr_t
                rows.append([
                    P(f"<b>🟣 {_dp['kcl_nome']}</b>",8,True),
                    P("KCl/Potássio",8),
                    P(str(_dp.get("kcl_kg_ha",0)),8,False,None,TA_CENTER),
                    P("kg/ha",8,False,None,TA_CENTER),
                    P("—",8,False,None,TA_CENTER),
                    P(f"<b>{_dp.get('kcl_total_kg',0):,.0f}</b> kg",8,True,COR_VERDE_E,TA_CENTER),
                    P(f"R$ {_pr_u:.2f}",8,False,None,TA_CENTER),
                    P(f"<b>R$ {_pr_t:,.2f}</b>",8,True,COR_VERDE_E,TA_CENTER),
                ])
            # Ureia / N (lista — pode ter 2 ou mais aplicações)
            _ureias_pdf = _dp.get("ureias") or (
                [{"nome": _dp["ureia_nome"], "kg_ha": _dp.get("ureia_kg_ha",0),
                  "total_kg": _dp.get("ureia_total_kg",0)}]
                if _dp.get("ureia_nome") and _dp.get("ureia_kg_ha",0) > 0 else []
            )
            for _urb in _ureias_pdf:
                _pr_u, _base_pr, _ = _preco_pdf(_urb.get("nome",""))
                _urb_total = _urb.get("total_kg",0) or round(_urb.get("kg_ha",0) * float(_urb.get("ha",0) or aplic.get("Área aplicada ha",0) or 0), 1)
                _pr_t = round(_urb_total * _pr_u, 2)
                _custo_aplic += _pr_t
                rows.append([
                    P(f"<b>⬜ {_urb.get('nome','')}</b>",8,True),
                    P("Ureia/N",8),
                    P(str(_urb.get("kg_ha",0)),8,False,None,TA_CENTER),
                    P("kg/ha",8,False,None,TA_CENTER),
                    P(f"{_urb.get('ha',0)} ha" if _urb.get("ha",0) else "—",8,False,None,TA_CENTER),
                    P(f"<b>{_urb_total:,.0f}</b> kg",8,True,COR_VERDE_E,TA_CENTER),
                    P(f"R$ {_pr_u:.2f}",8,False,None,TA_CENTER),
                    P(f"<b>R$ {_pr_t:,.2f}</b>",8,True,COR_VERDE_E,TA_CENTER),
                ])
            # Inoculante 1
            if _dp.get("inoc1_nome") and _dp.get("inoc1_dose",0) > 0:
                _pr_u, _pr_t, _qt_l, _un_l = _valor_semente_pdf(_dp["inoc1_nome"])
                _custo_aplic += _pr_t
                rows.append([
                    P(f"<b>🦠 {_dp['inoc1_nome']}</b>",8,True),
                    P("Inoculante sulco",8),
                    P(str(_dp.get("inoc1_dose",0)),8,False,None,TA_CENTER),
                    P("mL/ha",8,False,None,TA_CENTER),
                    P("—",8,False,None,TA_CENTER),
                    P(f"<b>{_qt_l:,.1f}</b> {_un_l}" if _qt_l > 0 else "—",8,True,COR_VERDE_E,TA_CENTER),
                    P(f"R$ {_pr_u:.2f}" if _pr_u > 0 else "—",8,False,None,TA_CENTER),
                    P(f"<b>R$ {_pr_t:,.2f}</b>" if _pr_t > 0 else "—",8,True,COR_VERDE_E,TA_CENTER),
                ])
            # Co-inoculante
            if _dp.get("inoc2_nome") and _dp.get("inoc2_dose",0) > 0:
                _pr_u, _pr_t, _qt_l, _un_l = _valor_semente_pdf(_dp["inoc2_nome"])
                _custo_aplic += _pr_t
                rows.append([
                    P(f"<b>🦠 {_dp['inoc2_nome']}</b>",8,True),
                    P("Co-inoculante",8),
                    P(str(_dp.get("inoc2_dose",0)),8,False,None,TA_CENTER),
                    P("mL/ha",8,False,None,TA_CENTER),
                    P("—",8,False,None,TA_CENTER),
                    P(f"<b>{_qt_l:,.1f}</b> {_un_l}" if _qt_l > 0 else "—",8,True,COR_VERDE_E,TA_CENTER),
                    P(f"R$ {_pr_u:.2f}" if _pr_u > 0 else "—",8,False,None,TA_CENTER),
                    P(f"<b>R$ {_pr_t:,.2f}</b>" if _pr_t > 0 else "—",8,True,COR_VERDE_E,TA_CENTER),
                ])
            # Inoculante semente
            if _dp.get("inoc3_nome") and _dp.get("inoc3_dose",0) > 0:
                _pr_u, _pr_t, _qt_l, _un_l = _valor_semente_pdf(_dp["inoc3_nome"])
                _custo_aplic += _pr_t
                rows.append([
                    P(f"<b>💉 {_dp['inoc3_nome']}</b>",8,True),
                    P("Inoc. semente",8),
                    P(str(_dp.get("inoc3_dose",0)),8,False,None,TA_CENTER),
                    P("mL/sc",8,False,None,TA_CENTER),
                    P("—",8,False,None,TA_CENTER),
                    P(f"<b>{_qt_l:,.1f}</b> {_un_l}" if _qt_l > 0 else "—",8,True,COR_VERDE_E,TA_CENTER),
                    P(f"R$ {_pr_u:.2f}" if _pr_u > 0 else "—",8,False,None,TA_CENTER),
                    P(f"<b>R$ {_pr_t:,.2f}</b>" if _pr_t > 0 else "—",8,True,COR_VERDE_E,TA_CENTER),
                ])
            # Micro 1
            if _dp.get("micro1_nome") and _dp.get("micro1_dose",0) > 0:
                _pr_u, _pr_t, _qt_l, _un_l = _valor_semente_pdf(_dp["micro1_nome"])
                _custo_aplic += _pr_t
                rows.append([
                    P(f"<b>🌿 {_dp['micro1_nome']}</b>",8,True),
                    P("Micronutriente",8),
                    P(str(_dp.get("micro1_dose",0)),8,False,None,TA_CENTER),
                    P("kg/L ha",8,False,None,TA_CENTER),
                    P("—",8,False,None,TA_CENTER),
                    P(f"<b>{_qt_l:,.1f}</b> {_un_l}" if _qt_l > 0 else "—",8,True,COR_VERDE_E,TA_CENTER),
                    P(f"R$ {_pr_u:.2f}" if _pr_u > 0 else "—",8,False,None,TA_CENTER),
                    P(f"<b>R$ {_pr_t:,.2f}</b>" if _pr_t > 0 else "—",8,True,COR_VERDE_E,TA_CENTER),
                ])
            # Micro 2
            if _dp.get("micro2_nome") and _dp.get("micro2_dose",0) > 0:
                _pr_u, _pr_t, _qt_l, _un_l = _valor_semente_pdf(_dp["micro2_nome"])
                _custo_aplic += _pr_t
                rows.append([
                    P(f"<b>🌿 {_dp['micro2_nome']}</b>",8,True),
                    P("Micronutriente",8),
                    P(str(_dp.get("micro2_dose",0)),8,False,None,TA_CENTER),
                    P("kg/L ha",8,False,None,TA_CENTER),
                    P("—",8,False,None,TA_CENTER),
                    P(f"<b>{_qt_l:,.1f}</b> {_un_l}" if _qt_l > 0 else "—",8,True,COR_VERDE_E,TA_CENTER),
                    P(f"R$ {_pr_u:.2f}" if _pr_u > 0 else "—",8,False,None,TA_CENTER),
                    P(f"<b>R$ {_pr_t:,.2f}</b>" if _pr_t > 0 else "—",8,True,COR_VERDE_E,TA_CENTER),
                ])

        if len(rows) == 1:
            rows.append([P("Nenhum produto registrado",8,False,COR_SUB),"","","","","","",""])

        # Linha de subtotal da aplicação
        rows.append([
            P("<b>TOTAL DESTA APLICAÇÃO</b>",8,True,COR_BRANCO), "", "", "", "", "",
            "", P(f"<b>R$ {_custo_aplic:,.2f}</b>",9,True,COR_BRANCO,TA_CENTER),
        ])
        _custo_total_pdf += _custo_aplic

        tp = Table(rows, colWidths=[3.8*cm,1.7*cm,1.4*cm,1.3*cm,2.0*cm,2.4*cm,1.9*cm,2.2*cm])
        stp = [("BACKGROUND",(0,0),(-1,0),COR_VERDE_E),("GRID",(0,0),(-1,-1),0.4,COR_BORDA),
               ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
               ("LEFTPADDING",(0,0),(-1,-1),6),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
               ("BACKGROUND",(0,-1),(-1,-1),COR_VERDE),("SPAN",(0,-1),(5,-1))]
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

    # ── TOTAL GERAL DO RELATÓRIO (todas as aplicações, área total) ─────────
    story.append(Spacer(1,2*mm))
    tg = [[P(f"💰 CUSTO TOTAL GERAL — {area_ha} ha" + (f" de {cultura}" if cultura else ""),
             11,True,COR_BRANCO),
           P(f"R$ {_custo_total_pdf:,.2f}",13,True,COR_BRANCO,TA_RIGHT)]]
    ttg = Table(tg, colWidths=[13*cm,5.5*cm])
    ttg.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),COR_VERDE_E),
        ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    story.append(ttg)
    story.append(Spacer(1,3*mm))

    story.append(HRFlowable(width="100%",thickness=1,color=COR_VERDE))
    story.append(Spacer(1,2*mm))
    story.append(P(f"IAAgro - Inteligencia Agricola de Precisao | {datetime.now().strftime('%d/%m/%Y %H:%M')} | Uso interno",
                   7,False,COR_SUB,TA_CENTER))
    doc.build(story)
    buf.seek(0)
    return buf.read()


def calcular_calcario_por_v(ctc, v_atual, area, prnt=75, v_desejado=70):
    """
    Calagem pelo método da SATURAÇÃO DE BASES (V%) — CQFS RS/SC 2016.
    É o método mais preciso, usado quando se tem CTC e V% do laudo.
    Fórmula: NC (t/ha) = CTC × (V2 - V1) / (10 × PRNT/100)
      onde V2 = saturação desejada (%), V1 = saturação atual (%)
    v_desejado: 70% é padrão para grãos (soja/milho); 60% para pastagem,
                80% para culturas exigentes.
    Retorna (dose_t_ha, total_t, detalhes).
    """
    if ctc <= 0 or v_atual >= v_desejado:
        return 0.0, 0.0, "V% já adequado ou CTC não informada"
    # NC (t/ha) = CTC × (V2 - V1) / 100 ÷ (PRNT/100)
    nc = (ctc * (v_desejado - v_atual) / 100.0) / (prnt / 100.0)
    dose = round(max(0.0, nc), 2)
    return dose, round(dose * area, 2), f"V {v_atual:.0f}%→{v_desejado}%, CTC {ctc:.1f}, PRNT {prnt}%"


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


# ─────────────────────────────────────────────
# Balanço de nutrientes: absorção total × exportação no grão × resíduo
# Coeficientes em kg de nutriente por TONELADA de grão produzido.
# Fontes: EMBRAPA (Circulares Técnicas Soja/Milho), CQFS RS/SC 2016,
# IAC Boletim 100. "absorve" = extração total pela planta;
# "exporta" = o que sai no grão na colheita; a diferença fica no
# resíduo (palhada) e retorna ao solo na decomposição.
# ─────────────────────────────────────────────
COEF_NUTRIENTES = {
    # cultura: {nutriente: (absorve_kg_por_t, exporta_kg_por_t)}
    "Soja":   {"N": (80, 51), "P2O5": (16, 14), "K2O": (38, 20)},
    "Milho":  {"N": (22, 15), "P2O5": (9,  7),  "K2O": (19, 5)},
    "Trigo":  {"N": (30, 21), "P2O5": (11, 9),  "K2O": (20, 6)},
    "Feijão": {"N": (55, 36), "P2O5": (14, 11), "K2O": (40, 15)},
    "Arroz":  {"N": (22, 12), "P2O5": (9,  6),  "K2O": (26, 4)},
    "Canola": {"N": (48, 32), "P2O5": (18, 14), "K2O": (42, 10)},
    "Aveia":  {"N": (25, 16), "P2O5": (10, 8),  "K2O": (22, 6)},
}

def balanco_nutrientes(cultura, produtividade_sc, peso_saca=60):
    """
    Calcula, para a produtividade esperada, quanto a lavoura:
    - ABSORVE (extração total da planta)
    - EXPORTA (sai no grão na colheita — o que precisa repor)
    - RETORNA ao solo no resíduo/palhada (absorve - exporta)
    Retorna dict por nutriente com as 3 parcelas em kg/ha, ou None.
    """
    cult = cultura_limpa(cultura) if cultura else "Soja"
    coef = COEF_NUTRIENTES.get(cult)
    if not coef:
        return None
    ton_ha = (produtividade_sc * peso_saca) / 1000.0  # t/ha de grão
    res = {}
    for nutri, (absorve_t, exporta_t) in coef.items():
        absorve = round(absorve_t * ton_ha, 1)
        exporta = round(exporta_t * ton_ha, 1)
        res[nutri] = {"absorve": absorve, "exporta": exporta,
                      "residuo": round(absorve - exporta, 1)}
    res["_ton_ha"] = round(ton_ha, 2)
    return res


def estimar_producao(meta, nota):
    fator = nota / 100
    if   fator >= 0.85: return meta
    elif fator >= 0.70: return meta * 0.85
    elif fator >= 0.50: return meta * 0.70
    return meta * 0.55


def opcoes_adubacao(n_ha, p2o5_ha, k2o_ha):
    """
    Gera várias OPÇÕES de fontes de adubo para atingir o mesmo NPK recomendado
    (kg/ha de N, P2O5, K2O). Retorna lista de dicts, cada um uma estratégia:
    econômica (MAP+KCl+Ureia), formulados prontos e linhas tecnológicas
    (Timac, Mosaic, Yara). O produtor escolhe conforme orçamento e objetivo.
    Cada item traz os produtos (nome, teor, kg/ha calculado) e observações.
    """
    ops = []

    def _kg(alvo, teor):
        return round(alvo / (teor/100.0), 1) if alvo > 0 and teor > 0 else 0.0

    # ── 1) ECONÔMICA — fontes simples (padrão do mercado) ──
    itens = []
    if p2o5_ha > 0: itens.append(("MAP 11-52-00", _kg(p2o5_ha, 52), "52% P₂O₅ + 11% N"))
    if k2o_ha  > 0: itens.append(("KCl 00-00-60", _kg(k2o_ha, 60), "60% K₂O"))
    # desconta o N que já veio no MAP (11%)
    n_do_map = round(_kg(p2o5_ha, 52) * 0.11, 1) if p2o5_ha > 0 else 0
    n_falta  = max(0, round(n_ha - n_do_map, 1))
    if n_falta > 0: itens.append(("Ureia 45% N", _kg(n_falta, 45), "45% N"))
    ops.append({
        "nome": "Econômica (fontes simples)",
        "tag": "Menor custo",
        "cor": "#22c55e",
        "itens": itens,
        "obs": "Combinação tradicional e de menor custo por unidade de nutriente. "
               "Exige mistura/aplicação separada e não traz enxofre nem tecnologia de eficiência.",
    })

    # ── 2) FORMULADO NPK PRONTO ──
    # Escolhe um formulado típico conforme a relação P:K
    itens_f = []
    if p2o5_ha > 0 and k2o_ha > 0:
        # base pela maior necessidade entre P e K
        base_kg = round(max(p2o5_ha/0.20, k2o_ha/0.20), 1)  # formulado ~20% P e K
        itens_f.append(("Formulado 02-20-20", base_kg, "2% N · 20% P₂O₅ · 20% K₂O"))
        obs_f = ("Prático: um único produto no plantio com N, P e K juntos. "
                 "Ajuste a dose conforme o formulado disponível na sua revenda "
                 "(ex.: 04-20-20, 08-20-20, 05-25-25).")
    elif p2o5_ha > 0:
        itens_f.append(("Formulado 08-40-00 (tipo MAP+)", _kg(p2o5_ha, 40), "8% N · 40% P₂O₅"))
        obs_f = "Formulado com foco em fósforo de plantio."
    else:
        itens_f.append(("KCl 00-00-60", _kg(k2o_ha, 60), "60% K₂O"))
        obs_f = "Necessidade concentrada em potássio."
    ops.append({
        "nome": "Formulado NPK pronto",
        "tag": "Praticidade",
        "cor": "#3b82f6",
        "itens": itens_f,
        "obs": obs_f,
    })

    # ── 3) LINHA TECNOLÓGICA — fósforo protegido / eficiência ──
    itens_t = []
    if p2o5_ha > 0:
        itens_t.append(("Timac Top-Phos ou Physiostart", _kg(p2o5_ha, 42),
                        "P protegido (tecnologia CSP/Physio) — maior aproveitamento"))
    if k2o_ha > 0:
        itens_t.append(("KCl ou Polysulphato (Yara)", _kg(k2o_ha, 48),
                        "K + enxofre/cálcio/magnésio (Polysulphato)"))
    if n_falta > 0:
        itens_t.append(("Ureia protegida (NBPT)", _kg(n_falta, 45),
                        "menor perda por volatilização"))
    ops.append({
        "nome": "Tecnológica (alta eficiência)",
        "tag": "Máximo aproveitamento",
        "cor": "#eab308",
        "itens": itens_t,
        "obs": "Fontes com tecnologia de proteção/eficiência (Timac, Yara, Mosaic). "
               "Custo por saco maior, mas melhor aproveitamento do nutriente, "
               "menor perda e ganho logístico. Doses são aproximadas — confira o "
               "teor exato do produto na revenda.",
    })

    # ── 4) ENXOFRE + MICROS (linha premium Mosaic) ──
    if p2o5_ha > 0:
        ops.append({
            "nome": "Com enxofre e micros",
            "tag": "P + S + Zn",
            "cor": "#a855f7",
            "itens": [
                ("Mosaic MicroEssentials (MES)", _kg(p2o5_ha, 40),
                 "P + N + enxofre + zinco no mesmo grânulo"),
            ] + ([("KCl 00-00-60", _kg(k2o_ha, 60), "60% K₂O")] if k2o_ha > 0 else []),
            "obs": "Tecnologia que entrega fósforo junto com enxofre e zinco, "
                   "importante em solos deficientes nesses nutrientes. "
                   "Reduz o número de produtos na operação.",
        })

    return ops


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
    manganes         = d.get("manganes", 0)
    cobre            = d.get("cobre", 0)

    # pH ideal por cultura (EMBRAPA/CQFS)
    ph_ideais = {
        "Soja": (5.8, 6.5), "Milho": (5.8, 6.5), "Trigo": (5.8, 6.5),
        "Feijão": (6.0, 6.5), "Arroz": (5.5, 6.0), "Canola": (6.0, 6.5),
        "Café": (5.5, 6.5), "Tomate": (6.0, 6.8), "Batata": (5.5, 6.0),
        "Eucalipto": (5.0, 6.0), "Pinus": (4.5, 5.5), "Mogno Africano": (5.5, 6.5),
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
    if enxofre > 0:
        if   enxofre < 5:  score -= 8; alertas.append("Enxofre baixo (<5 mg/dm³) — usar fertilizante com S")
        elif enxofre < 10: score -= 3; alertas.append("Enxofre médio (5-10 mg/dm³) — atenção em culturas exigentes")
    if zinco > 0 and zinco < 0.6:
        score -= 5; alertas.append(f"Zinco baixo (<0,6 mg/dm³)")
    if boro > 0 and boro < 0.2:
        score -= 5; alertas.append(f"Boro baixo (<0,2 mg/dm³) — importante para soja/café")
    if manganes > 0 and manganes < 1.2:
        score -= 4; alertas.append(f"Manganês baixo (<1,2 mg/dm³)")
    if cobre > 0 and cobre < 0.2:
        score -= 4; alertas.append(f"Cobre baixo (<0,2 mg/dm³)")

    score = max(0, min(100, score))
    if   score >= 85: classe = "Excelente"
    elif score >= 70: classe = "Boa"
    elif score >= 50: classe = "Média"
    elif score >= 30: classe = "Fraca"
    else:             classe = "Crítica"
    return score, classe, alertas


_PKG_RE = re.compile(r"([\d.,]+)\s*(kg|ml|gr|l|g)\b", re.IGNORECASE)

def _parse_pacote(texto):
    """Extrai (número, unidade) de um texto tipo '10 L', '20L', '880GR', '500 mL'."""
    if not texto:
        return None
    m = _PKG_RE.search(texto)
    if not m:
        return None
    try:
        num = float(m.group(1).replace(",", "."))
    except ValueError:
        return None
    un = m.group(2).lower()
    if un == "gr": un = "g"
    if num <= 0:
        return None
    return num, un  # un em {kg, ml, l, g}


def preco_por_kg_ou_l(item):
    """
    Preço por kg ou por L de um item do estoque.
    Na prática o preço quase sempre é cadastrado pelo tamanho da EMBALAGEM
    comprada (ex: R$ 549 pela bombona de 10 L, não R$ 549 por litro) — então
    aqui a gente converte usando o tamanho real da embalagem: primeiro olha o
    campo "Embalagem" do estoque, e se não tiver, olha o próprio nome do
    produto (que no seu catálogo já vem com o tamanho no final, tipo
    "WINFIELD INTERLOCK 10L" ou "HERB. PAXEO 880GR").
    Retorna (preço_por_kg_ou_l, "kg"|"L", aviso).
    """
    if not item:
        return 0.0, "kg", None
    _preco = float(item.get("Valor Unitário R$", 0) or 0)
    if _preco <= 0:
        return 0.0, "kg", None

    _pacote = _parse_pacote(item.get("Embalagem","")) or _parse_pacote(item.get("Insumo",""))
    if _pacote:
        _num, _un = _pacote
        if _un == "l":  return round(_preco/_num, 4), "L", None
        if _un == "kg": return round(_preco/_num, 4), "kg", None
        if _un == "ml": return round(_preco/(_num/1000), 4), "L", None
        if _un == "g":  return round(_preco/(_num/1000), 4), "kg", None

    # Não achou tamanho de embalagem — usa a Unidade cadastrada como último recurso
    _u = (item.get("Unidade","") or "").strip().lower()
    if _u == "kg": return _preco, "kg", None
    if _u == "l":  return _preco, "L", None
    if _u == "g":  return _preco * 1000, "kg", None
    if _u == "ml": return _preco * 1000, "L", None
    _aviso = (f"⚠️ Não consegui identificar o tamanho da embalagem de \"{item.get('Insumo','')}\" "
              f"pra converter o preço pra R$/kg ou R$/L — o custo mostrado pode estar errado. "
              f"Edite o estoque e informe a Embalagem (ex: \"20 L\").")
    return _preco, "kg", _aviso


def baixar_estoque(nome_insumo, quantidade_usada, unidade_usada="L/ha"):
    """
    Dá baixa no estoque convertendo unidades automaticamente.
    Estoque sempre em L ou kg. Aplicação pode ser mL/ha, g/ha, etc.
    """
    def converter_para_base(qtd, unid):
        """Converte para a unidade base: L ou kg."""
        unid = (unid or "").lower().replace(" ", "")
        base = unid.split("/")[0]  # "ml/ha"->"ml"  "kg/ha"->"kg"  "g/ha"->"g"  "mg/ha"->"mg"
        if base == "ml": return qtd / 1000       # mL → L
        if base == "g":  return qtd / 1000       # g → kg (NÃO confundir com "kg")
        if base == "mg": return qtd / 1_000_000
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
        "🌧️ Pluviômetro",
        "🧪 Solo & Adubação",
        "💰 Financeiro",
        "📦 Operacional",
        "🔧 Máquinas",
        "🌍 Inteligência",
        "🧠 Assistente IA",
        "📅 Planejamento de Safras",
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
        preco_ano = 99.90 * 12 * 0.85   # 15% desconto anual
    else:
        link_mes = MP_LINK_PRO_MES
        link_ano = MP_LINK_PRO_ANO
        preco_ano = 39.90 * 12 * 0.85

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

# Necessidade hídrica por CICLO (mm) — faixas técnicas (Embrapa, ESALQ/USP,
# Doorenbos & Kassam 1979). (min, max, fase_critica, sensibilidade).
# sensibilidade: fator 0.6-1.0 de quão sensível a cultura é ao déficit
# (café e milho muito sensíveis na fase crítica; mandioca tolera melhor).
_CHUVA_CICLO_MM = {
    # 🌾 Grãos
    "Soja":     (450, 800,  "Floração e enchimento de grãos (R1-R6)", 1.0),
    "Milho":    (500, 800,  "Pendoamento e enchimento de grãos",       1.0),
    "Trigo":    (350, 600,  "Espigamento e enchimento",                0.9),
    "Feijão":   (300, 500,  "Floração e formação de vagens",           1.0),
    "Canola":   (400, 700,  "Floração e enchimento de síliquas",       0.9),
    "Aveia":    (300, 550,  "Emborrachamento e enchimento",            0.8),
    "Arroz":    (900, 1300, "Perfilhamento e floração",                1.0),
    "Sorgo":    (350, 650,  "Emborrachamento e enchimento",            0.75),
    "Cevada":   (350, 600,  "Espigamento e enchimento",                0.9),
    "Girassol": (400, 700,  "Floração e enchimento de aquênios",       0.9),
    # 🌿 Horticultura
    "Tomate":   (400, 600,  "Floração e frutificação",                 1.0),
    "Batata":   (350, 600,  "Tuberização (formação dos tubérculos)",   1.0),
    "Cebola":   (350, 650,  "Bulbificação",                            0.9),
    "Alho":     (350, 600,  "Bulbificação",                            0.9),
    "Mandioca": (800, 1500, "Formação de raízes (menos sensível)",     0.6),
    "Alface":   (200, 350,  "Formação de cabeça",                      1.0),
    "Cenoura":  (350, 550,  "Engrossamento da raiz",                   0.9),
    "Brócolis": (350, 550,  "Formação da inflorescência",              1.0),
    "Pepino":   (350, 550,  "Floração e frutificação",                 1.0),
    "Pimentão": (600, 900,  "Floração e frutificação",                 1.0),
    # 🎯 Fruticultura (por ciclo/safra anual)
    "Laranja":  (900, 1200, "Florada e crescimento dos frutos",        0.85),
    "Banana":   (1200,1800, "Emissão do cacho e enchimento",           0.9),
    "Uva":      (500, 800,  "Floração e maturação das bagas",          0.85),
    "Maçã":     (800, 1100, "Frutificação e crescimento",              0.85),
    "Manga":    (700, 1200, "Florada e frutificação",                  0.8),
    "Abacate":  (1000,1400, "Frutificação",                            0.85),
    "Limão":    (900, 1200, "Florada e crescimento dos frutos",        0.85),
    "Pêssego":  (700, 1000, "Frutificação e maturação",                0.85),
    "Caqui":    (700, 1100, "Frutificação",                            0.8),
    "Café":     (1200,1800, "Florada, granação e enchimento",          1.0),
    # 🌲 Silvicultura (anual — árvores toleram melhor por raízes profundas)
    "Eucalipto":(1000,1500, "Fase de crescimento inicial (1-2 anos)",  0.6),
    "Pinus":    (1000,1600, "Crescimento inicial",                     0.55),
    "Teca":     (1200,2000, "Estação de crescimento",                  0.6),
    "Paricá":   (1500,2500, "Crescimento",                             0.6),
    "Cedro":    (1200,1800, "Crescimento",                             0.6),
    "Mogno Africano": (1200,1800, "Crescimento",                       0.6),
    # Outras
    "Cana-de-açúcar": (1200,1800, "Perfilhamento e crescimento",       0.85),
    "Algodão":  (700, 1300, "Floração e formação de maçãs",            0.9),
    "Pastagem": (500, 1200, "Rebrota e crescimento vegetativo",        0.7),
}

# Segmento de cada cultura (para a tabela organizada)
_CULTURA_SEGMENTO = {
    "🌾 Grãos": ["Soja","Milho","Trigo","Feijão","Canola","Aveia","Arroz","Sorgo","Cevada","Girassol"],
    "🌿 Horticultura": ["Tomate","Batata","Cebola","Alho","Mandioca","Alface","Cenoura","Brócolis","Pepino","Pimentão"],
    "🎯 Fruticultura": ["Laranja","Banana","Uva","Maçã","Manga","Abacate","Limão","Pêssego","Caqui","Café"],
    "🌲 Silvicultura": ["Eucalipto","Pinus","Teca","Paricá","Cedro","Mogno Africano"],
}

def estimar_perda_hidrica(cultura, chuva_ciclo_mm, chuva_fase_critica=None):
    """
    Estima a perda de produtividade (%) por déficit ou excesso hídrico.

    Base técnica (Embrapa, Doorenbos & Kassam 1979, Bergamaschi et al. 2006):
    - Compara a chuva ACUMULADA do ciclo com a faixa ideal da cultura.
    - Aplica a SENSIBILIDADE da cultura ao déficit (café/milho sofrem mais;
      mandioca/eucalipto toleram melhor por raízes profundas).
    - Se informada a chuva da FASE CRÍTICA (floração/enchimento), ela pesa
      mais no resultado — porque déficit nessa fase causa dano desproporcional
      (um veranico na floração da soja quebra mais que total baixo distribuído).

    Retorna (perda_percentual, situacao_texto).
    """
    _c = cultura_limpa(cultura or "")
    faixa = _CHUVA_CICLO_MM.get(_c)
    if not faixa or chuva_ciclo_mm <= 0:
        return 0.0, "sem parâmetro"
    _min, _max, _fase, _sens = faixa

    # Perda base pelo total do ciclo
    if chuva_ciclo_mm < _min:
        _falta_rel = (_min - chuva_ciclo_mm) / _min
        perda_ciclo = min(_falta_rel * 0.8 * _sens * 100, 60.0)
        situacao = "déficit hídrico (seca)"
    elif chuva_ciclo_mm > _max:
        _sobra_rel = (chuva_ciclo_mm - _max) / _max
        perda_ciclo = min(_sobra_rel * 0.35 * 100, 35.0)
        situacao = "excesso de chuva"
    else:
        perda_ciclo = 0.0
        situacao = "faixa ideal"

    # Refino pela fase crítica: se soubermos a chuva da fase crítica e ela
    # estiver baixa, a perda é maior (peso 60% fase crítica / 40% ciclo geral).
    if chuva_fase_critica is not None and _sens >= 0.7:
        # Necessidade proporcional da fase crítica (~35% da água do ciclo
        # concentrada na fase mais exigente)
        _need_fase = (_min * 0.35)
        if chuva_fase_critica < _need_fase and _need_fase > 0:
            _falta_fase = (_need_fase - chuva_fase_critica) / _need_fase
            perda_fase = min(_falta_fase * 0.9 * _sens * 100, 65.0)
            # Combina: fase crítica pesa mais
            perda_final = perda_ciclo * 0.4 + perda_fase * 0.6
            return round(min(perda_final, 70.0), 1), "déficit na fase crítica"

    return round(perda_ciclo, 1), situacao

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

            # Botão pra quem acabou de pagar ver a liberação sem precisar relogar
            if st.button("🔄 Já paguei — atualizar meu plano", key="btn_revalidar_plano",
                         use_container_width=True):
                if _SUPABASE_ATIVO and st.session_state.get("sb_token"):
                    with st.spinner("Verificando seu pagamento..."):
                        _novo_plano = sb_plano(_SB_URL, _SB_KEY,
                                               st.session_state.sb_token,
                                               st.session_state.sb_user_id)
                    if _novo_plano and _novo_plano != "free":
                        st.session_state.sb_plano = _novo_plano
                        success_box(f"✅ Plano atualizado para {PLANOS.get(_novo_plano,{}).get('nome',_novo_plano)}!")
                        st.rerun()
                    else:
                        st.info("Ainda não identificamos seu pagamento. Após pagar, "
                                "a liberação leva alguns minutos. Se demorar, verifique "
                                "se pagou com o mesmo e-mail do cadastro ou fale com o suporte.")

        # Métricas gerais da propriedade
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
            estoque_baixo = [i for i in st.session_state.estoque if float(i.get("Quantidade",0) or 0) < 10]
            if not estoque_baixo:
                st.markdown("""
                <div style='background:#0f172a;border:1px solid #1e3a2f;border-left:3px solid #22c55e;
                border-radius:8px;padding:7px 12px;margin:2px 0;'>
                <span style='color:#22c55e;font-size:12px;font-weight:700;letter-spacing:.4px;'>✓ ESTOQUE OK</span>
                <span style='color:#94a3b8;font-size:12px;'> — nenhum item abaixo do mínimo</span>
                </div>""", unsafe_allow_html=True)
            else:
                # Ordena: esgotados primeiro, depois por quantidade crescente
                _est_ord = sorted(estoque_baixo, key=lambda i: float(i.get("Quantidade",0) or 0))
                _linhas_tbl = []
                for _n, _it_a in enumerate(_est_ord, 1):
                    _q  = float(_it_a.get("Quantidade",0) or 0)
                    _zr = _q <= 0
                    _cor_s = "#ef4444" if _zr else "#f59e0b"
                    _lbl_s = "ESGOTADO" if _zr else "BAIXO"
                    _linhas_tbl.append(f"""
                    <tr style='border-bottom:1px solid #1e293b;'>
                    <td style='padding:5px 10px;color:#64748b;font-weight:700;text-align:center;width:34px;'>{_n}</td>
                    <td style='padding:5px 10px;color:#e2e8f0;font-weight:600;'>{_it_a.get('Insumo', _it_a.get('Produto','Produto'))}</td>
                    <td style='padding:5px 10px;color:#cbd5e1;text-align:right;white-space:nowrap;'>{_q:.1f} {_it_a.get('Unidade','')}</td>
                    <td style='padding:5px 10px;text-align:center;white-space:nowrap;'>
                    <span style='color:{_cor_s};font-weight:700;font-size:11px;letter-spacing:.3px;'>{_lbl_s}</span></td>
                    </tr>""")
                st.markdown(f"""
                <div style='background:#0f172a;border:1px solid #334155;border-radius:8px;
                max-height:230px;overflow-y:auto;margin:2px 0;'>
                <table style='width:100%;border-collapse:collapse;font-size:12px;'>
                <thead>
                <tr style='position:sticky;top:0;background:#1e293b;z-index:1;'>
                <th style='padding:6px 10px;color:#94a3b8;font-size:11px;text-align:center;width:34px;'>#</th>
                <th style='padding:6px 10px;color:#94a3b8;font-size:11px;text-align:left;'>INSUMO</th>
                <th style='padding:6px 10px;color:#94a3b8;font-size:11px;text-align:right;'>QTD</th>
                <th style='padding:6px 10px;color:#94a3b8;font-size:11px;text-align:center;'>STATUS</th>
                </tr>
                </thead>
                <tbody>{''.join(_linhas_tbl)}</tbody>
                </table>
                </div>""", unsafe_allow_html=True)

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
    _sub_lav = st.tabs(["➕ Cadastro da Área","📍 Áreas Cadastradas","🗺️ Mapa de Fertilidade","📈 Histórico de Produtividade"])

if menu == "🌾 Lavoura":
  with _sub_lav[1]:
    st.header("Áreas Cadastradas")

    if len(st.session_state.areas) == 0:
        st.markdown('<div style="background:#1e3a5f;color:#ffffff;padding:14px 18px;border-radius:10px;font-weight:600;font-size:15px;border:1px solid #3b82f6;">ℹ️ Nenhuma área cadastrada ainda.</div>', unsafe_allow_html=True)
    else:
        tabela_areas = pd.DataFrame([
            {
                "ID":               a.get("ID", "—"),
                "Fazenda":          a.get("Fazenda", ""),
                "Talhão":          a.get("Talhão", ""),
                "Matricula":        a.get("Matricula", ""),
                "Cidade/Estado":    a.get("Cidade/Estado", ""),
                "Hectares":         a.get("Hectares", 0),
                "Cultura":          a.get("Cultura", ""),
                "Meta Produtividade": a.get("Meta Produtividade", 0)
            }
            for a in st.session_state.areas
        ])
        st.dataframe(tabela_areas, use_container_width=True)

        opcoes = [f"{area.get('ID','—')} - {area.get('Talhão','')} - {area.get('Cultura','')}" for area in st.session_state.areas]
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
            # Restaura o croqui/desenho vinculado à área, se houver
            if area.get("desenho"):
                st.session_state.dados["desenho_talhao"] = area["desenho"]
                if area.get("area_calculada_ha"):
                    st.session_state.dados["area_calculada_ha"] = area["area_calculada_ha"]
            salvar_dados_iaagro()
            success_box(f"✅ Área {area['ID']} carregada! {('Análise de solo disponível ✅' if 'ph' in st.session_state.dados else 'Sem análise de solo ainda.')}")
            st.rerun()

        st.divider()
        # ── EDITAR DADOS DE UMA ÁREA CADASTRADA ──
        with st.expander("✏️ Editar dados de uma área cadastrada"):
            st.caption("Corrija fazenda, talhão, matrícula, cidade, hectares, cultura ou meta "
                       "sem precisar excluir e recadastrar. Os dados de solo e aplicações são preservados.")
            _op_edit = [f"{area.get('ID','—')} - {area.get('Talhão','')} - {area.get('Cultura','')}"
                        for area in st.session_state.areas]
            _sel_edit = st.selectbox("Escolha a área para editar", _op_edit, key="sel_editar_area")
            _idx_edit = _op_edit.index(_sel_edit)
            _area_e = st.session_state.areas[_idx_edit]

            with st.form(key="form_editar_area"):
                _ce1, _ce2, _ce3 = st.columns(3)
                _e_fazenda = _ce1.text_input("Fazenda", value=_area_e.get("Fazenda",""), key="edit_area_fazenda")
                _e_talhao  = _ce2.text_input("Talhão", value=_area_e.get("Talhão",""), key="edit_area_talhao")
                _e_matric  = _ce3.text_input("Matrícula", value=_area_e.get("Matricula",""), key="edit_area_matric")

                _ce4, _ce5, _ce6 = st.columns(3)
                _e_cidade  = _ce4.text_input("Cidade/Estado", value=_area_e.get("Cidade/Estado",""), key="edit_area_cidade")
                _e_hectares= _ce5.number_input("Hectares", min_value=0.0,
                    value=float(_area_e.get("Hectares",0) or 0), step=0.1, key="edit_area_hectares")
                _culturas_op = ["Soja","Milho","Trigo","Feijão","Arroz","Algodão","Café","Cana","Pastagem","Outro"]
                _cult_atual = _area_e.get("Cultura","Soja")
                _cult_idx = _culturas_op.index(_cult_atual) if _cult_atual in _culturas_op else 0
                _e_cultura = _ce6.selectbox("Cultura", _culturas_op, index=_cult_idx, key="edit_area_cultura")

                _e_meta = st.number_input("Meta de Produtividade (sc/ha)", min_value=0.0,
                    value=float(_area_e.get("Meta Produtividade",0) or 0), step=1.0, key="edit_area_meta")

                _salvar_area = st.form_submit_button("💾 Salvar alterações da área", type="primary", use_container_width=True)
                if _salvar_area:
                    _area_e["Fazenda"]            = _e_fazenda
                    _area_e["Talhão"]            = _e_talhao
                    _area_e["Matricula"]          = _e_matric
                    _area_e["Cidade/Estado"]      = _e_cidade
                    _area_e["Hectares"]           = _e_hectares
                    _area_e["Cultura"]            = _e_cultura
                    _area_e["Meta Produtividade"] = _e_meta
                    # Se for a área ativa, atualiza também os dados de trabalho
                    if st.session_state.get("area_selecionada") == _area_e.get("ID"):
                        st.session_state.dados.update({
                            "fazenda": _e_fazenda, "talhao": _e_talhao, "cidade": _e_cidade,
                            "area": _e_hectares, "cultura": _e_cultura, "produtividade": _e_meta,
                        })
                        _area_e["Dados"] = st.session_state.dados.copy()
                    salvar_dados_iaagro()
                    success_box(f"✅ Área {_area_e.get('ID','')} atualizada!")
                    st.rerun()

        st.divider()
        st.subheader("Excluir Área Individual")
        opcao_excluir = st.selectbox(
            "Escolha a área para excluir",
            [f"{area.get('ID','—')} - {area.get('Talhão','')} - {area.get('Cultura','')}" for area in st.session_state.areas],
            key="excluir_area_select"
        )
        if st.button("Excluir Área Selecionada", key="excluir_area_btn"):
            indice_excluir = [
                f"{area.get('ID','—')} - {area.get('Talhão','')} - {area.get('Cultura','')}"
                for area in st.session_state.areas
            ].index(opcao_excluir)
            area_excluida = st.session_state.areas[indice_excluir]["ID"]
            st.session_state.areas.pop(indice_excluir)
            if st.session_state.area_selecionada == area_excluida:
                st.session_state.area_selecionada = None
                st.session_state.dados = {}
            st.session_state["_permite_salvar_vazio"] = True  # exclusão legítima
            salvar_dados_iaagro()
            st.session_state["_permite_salvar_vazio"] = False
            success_box(f"Área {area_excluida} excluída com sucesso.")
            st.rerun()

        if st.button("Apagar Todas as Áreas"):
            st.session_state.areas = []
            st.session_state.dados = {}
            st.session_state.area_selecionada = None
            st.session_state["_permite_salvar_vazio"] = True  # ação explícita do usuário
            salvar_dados_iaagro()
            st.session_state["_permite_salvar_vazio"] = False
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
  with _sub_lav[3]:
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
                    # Soma a chuva acumulada por ANO-SAFRA e compara com a faixa
                    # técnica da cultura (perda por déficit ou excesso hídrico).
                    _cultura_area = area.get("Cultura", "")
                    _por_ano = {}
                    for r in registros_area:
                        _ano = r.get("ano", 0)
                        _por_ano[_ano] = _por_ano.get(_ano, 0) + r.get("mm", 0)
                    _perdas = []
                    for _chuva_ano in _por_ano.values():
                        _p, _ = estimar_perda_hidrica(_cultura_area, _chuva_ano)
                        _perdas.append(_p)
                    perda_media_clima = sum(_perdas) / len(_perdas) if _perdas else 0
                # Faixas de status em % de perda de produtividade
                if   perda_media_clima <= 5:  clima_cor = "🟢 Ideal"
                elif perda_media_clima <= 15: clima_cor = "🟡 Atenção"
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
        # Base OpenStreetMap (muito confiável) + satélite Esri como opção.
        # Antes o mapa dependia só da Esri; quando ela não carregava, ficava em branco.
        mapa_folium = folium.Map(location=[latitude, longitude], zoom_start=13,
                                 tiles="OpenStreetMap")
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri", name="🛰️ Satélite", control=True
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

        # Se a área atual já tem um croqui salvo, mostra ele no mapa
        _desenho_salvo = st.session_state.dados.get("desenho_talhao")
        _tem_croqui = False
        if _desenho_salvo and isinstance(_desenho_salvo, dict) and _desenho_salvo.get("geometry"):
            try:
                _geo = _desenho_salvo["geometry"]
                _coords_salvas = _geo.get("coordinates", [[]])[0]
                # Valida que há pelo menos 3 pares de coordenadas numéricas
                if _coords_salvas and len(_coords_salvas) >= 3:
                    _lats = [float(c[1]) for c in _coords_salvas]
                    _lons = [float(c[0]) for c in _coords_salvas]
                    # Só aplica se as coordenadas forem plausíveis (dentro do globo)
                    if (all(-90 <= la <= 90 for la in _lats) and
                        all(-180 <= lo <= 180 for lo in _lons)):
                        # Usa folium.Polygon (recebe [lat,lon] direto) em vez de
                        # GeoJson — o GeoJson quebrava a renderização do mapa quando
                        # havia croqui salvo (confirmado em teste). Polygon é robusto.
                        _pts_poly = [[float(c[1]), float(c[0])] for c in _coords_salvas]
                        folium.Polygon(
                            locations=_pts_poly,
                            color="#15803d", weight=3,
                            fill=True, fill_color="#22c55e", fill_opacity=0.25,
                            tooltip="Talhão salvo",
                        ).add_to(mapa_folium)
                        # Só ajusta o zoom se o polígono tiver tamanho real
                        # (evita fit_bounds degenerado que quebra o mapa)
                        if (max(_lats) - min(_lats) > 1e-6 and
                            max(_lons) - min(_lons) > 1e-6):
                            mapa_folium.fit_bounds(
                                [[min(_lats), min(_lons)], [max(_lats), max(_lons)]]
                            )
                        _tem_croqui = True
            except Exception:
                _tem_croqui = False

        if _tem_croqui:
            st.success("📍 Esta área já tem um croqui salvo (mostrado em verde no mapa). "
                       "Desenhe um novo apenas se quiser substituí-lo.")

        # key única e largura responsiva evitam o mapa sumir após reruns
        _key_mapa = f"mapa_talhao_{st.session_state.dados.get('id_area','x')}"
        dados_mapa_folium = None
        try:
            dados_mapa_folium = st_folium(mapa_folium, width=None, height=500,
                                          key=_key_mapa,
                                          returned_objects=["last_active_drawing","all_drawings"])
        except Exception as _e_mapa:
            st.warning("⚠️ O mapa não pôde ser exibido agora. Isso costuma ser temporário "
                       "(conexão com o servidor de mapas). Recarregue a página. "
                       "Você ainda pode usar Latitude/Longitude e GPS acima normalmente.")
        st.subheader("💾 Salvar Desenho do Talhão")

        st.info("💡 **Dica no celular:** Marque os pontos no sentido horário ao redor do talhão, sem cruzar as linhas. Use o botão **Delete last point** para desfazer o último ponto.")

        # Lê o desenho recém-feito. O Leaflet Draw pode devolver em
        # 'last_active_drawing' OU no fim de 'all_drawings' — aceita os dois,
        # senão, ao redesenhar sobre um croqui existente, o novo não aparecia.
        _novo_desenho = None
        if dados_mapa_folium:
            _novo_desenho = dados_mapa_folium.get("last_active_drawing")
            if not _novo_desenho:
                _todos = dados_mapa_folium.get("all_drawings") or []
                if _todos:
                    _novo_desenho = _todos[-1]  # o último desenhado

        if _novo_desenho and _novo_desenho.get("geometry"):
            desenho = _novo_desenho
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
                # Área geodésica pelo método de Gauss (shoelace), convertendo
                # graus para metros. IMPORTANTE: 1 grau de longitude vale menos
                # metros conforme nos afastamos do equador — por isso a longitude
                # é corrigida pelo cosseno da latitude média. Sem isso, a área
                # fica superestimada (~12% em Santa Catarina).
                import math as _math_area
                if not coords or len(coords) < 3:
                    return 0.0
                # Garante o polígono FECHADO (último ponto = primeiro). Sem isso,
                # o shoelace ignora o último lado e o resultado fica absurdo.
                _pts = list(coords)
                if _pts[0] != _pts[-1]:
                    _pts = _pts + [_pts[0]]
                _lats = [c[1] for c in _pts]
                _lat_media = sum(_lats) / len(_lats)
                _cos_lat = _math_area.cos(_math_area.radians(_lat_media))
                _m_lat = 111132.0                    # metros por grau de latitude
                _m_lon = 111320.0 * _cos_lat         # metros por grau de longitude (corrigido)
                area_val = 0.0
                for i in range(len(_pts) - 1):
                    x1 = _pts[i][0]   * _m_lon
                    y1 = _pts[i][1]   * _m_lat
                    x2 = _pts[i+1][0] * _m_lon
                    y2 = _pts[i+1][1] * _m_lat
                    area_val += (x1 * y2) - (x2 * y1)
                return abs(area_val) / 2 / 10000     # m² → hectares

            area_calculada = calcular_area_ha(coords)
            success_box(f"Área calculada automaticamente: {area_calculada:.2f} ha")

            # Seleção da área para vincular o desenho
            areas_disp = [f"{a.get('Fazenda','')} — {a.get('Talhão','')} [{a.get('ID','')}]"
                          for a in st.session_state.areas]
            area_vincular = st.selectbox("Vincular desenho à área:", ["— Não vincular —"] + areas_disp, key="sel_area_croqui")

            if st.button("Salvar desenho no talhão", key="salvar_desenho_talhao"):
                pts_hull = convex_hull([[c[0], c[1]] for c in coords])
                if len(pts_hull) >= 3:
                    pts_hull.append(pts_hull[0])
                    desenho["geometry"]["coordinates"][0] = [[p[0], p[1]] for p in pts_hull]

                # Salva no session_state global
                st.session_state.dados["desenho_talhao"] = desenho

                # Salva também na área específica se selecionada (o [ID] no rótulo
                # garante que vincula na área certa mesmo com nomes repetidos)
                if area_vincular != "— Não vincular —":
                    idx_area = areas_disp.index(area_vincular)
                    st.session_state.areas[idx_area]["desenho"] = desenho
                    st.session_state.areas[idx_area]["area_calculada_ha"] = round(area_calculada, 2)

                salvar_dados_iaagro()
                success_box("✅ Desenho do talhão salvo/atualizado com sucesso!")
                # Recarrega para o mapa exibir o croqui NOVO (senão fica o antigo)
                st.rerun()


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
    uploaded_file = st.file_uploader("📄 Upload análise de solo (XLSX, CSV ou PDF)", type=["xlsx","csv","pdf"], key="upl___upload_an_lis_3464")
    if uploaded_file is not None:
        if uploaded_file.name.lower().endswith(".pdf"):
            st.info("📑 Laudo em PDF detectado! Para PDFs, use a aba **'📄 OCR Laudo de Solo'** "
                    "(aqui do lado) — ela lê o PDF, extrai os valores e preenche a análise "
                    "automaticamente. O upload de planilha aqui é apenas para arquivos XLSX/CSV.")
        elif uploaded_file.name.lower().endswith(".csv"):
            df_upload = pd.read_csv(uploaded_file)
            success_box("✅ Análise carregada com sucesso!")
            st.dataframe(df_upload)
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
            materia_organica = st.number_input("Matéria Orgânica MO (%)", min_value=0.0, value=float(st.session_state.dados.get("materia_organica", 2.5)), key="num_mat_ria_org_nic_3482", help="Informe em porcentagem (ex.: 2.5 para 2,5%). Se seu laudo estiver em g/dm³, divida por 10.")
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

        # Calagem: método V% (mais preciso) quando há CTC e V%; senão, por pH
        _ctc_d = d.get("ctc", 0)
        _v_d   = d.get("v_percent", 0)
        _metodo_cal = "pH"
        if _ctc_d > 0 and _v_d > 0:
            dose_calcario, total_calcario, _det_cal = calcular_calcario_por_v(
                _ctc_d, _v_d, d["area"], prnt=75, v_desejado=70)
            _metodo_cal = "Saturação de Bases (V%)"
            # Se o V% já está ok mas o pH está muito baixo, checa pelo pH também
            _dose_ph, _tot_ph = calcular_calcario_por_ph(d["ph"], d["area"])
            if dose_calcario == 0 and _dose_ph > 0:
                dose_calcario, total_calcario = _dose_ph, _tot_ph
                _metodo_cal = "pH (V% já adequado)"
        else:
            dose_calcario, total_calcario = calcular_calcario_por_ph(d["ph"], d["area"])
            _det_cal = f"Baseado no pH {d['ph']} (informe CTC e V% para cálculo mais preciso)"

        precisa_gesso, dose_gesso, total_gesso, motivos_gesso = calcular_gesso(d)
        producao_estimada = estimar_producao(d["produtividade"], nota)

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Nota",              f"{nota}/100")
        col2.metric("Prioridade",        prioridade_final)
        col3.metric("Calcário",          f"{dose_calcario} t/ha")
        col4.metric("Gesso",             f"{dose_gesso} t/ha")
        col5.metric("Produção Estimada", f"{producao_estimada:.1f} sc/ha")

        if dose_calcario > 0:
            st.caption(f"🧮 Calagem calculada pelo método **{_metodo_cal}** — {_det_cal}. "
                       f"Meta V% = 70% (padrão grãos). PRNT considerado: 75%.")

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
        argila       = d.get("argila", 35)
        # Guarda de segurança: garante que nunca dê NameError no botão de
        # recomendação, mesmo que algum caminho pule os cálculos abaixo.
        n_ha = p2o5_ha = k2o_ha = 0.0
        map_ha = kcl_ha = ureia_ha = 0.0
        total_map = total_kcl = total_ureia = 0.0

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
        # Recomendação base por cultura (EMBRAPA/IAPAR - Sul do Brasil)
        # N em kg/ha de N puro; P e K em kg/ha de P2O5 e K2O
        # IMPORTANTE: fosforo e potassio vêm em mg/dm³ (Mehlich-1)
        # Faixas de K (mg/dm³, CQFS RS/SC): <40 MtBaixo, 40-60 Baixo,
        #   60-120 Médio, 120-180 Alto, >180 MtAlto
        if cultura == "Soja":
            # Soja fixa N biologicamente - adubação de base é P e K
            n_ha    = 0
            p2o5_ha = 120 if fosforo < 9 else (90 if fosforo < 18 else (60 if fosforo < 30 else 40))
            k2o_ha  = 120 if potassio < 40 else (100 if potassio < 60 else (80 if potassio < 120 else (55 if potassio < 180 else 40)))
            # Ajuste por produtividade meta (sc/ha)
            if produtividade > 70: p2o5_ha += 20; k2o_ha += 20
        elif cultura == "Milho":
            # N parcelado: 1/3 base + 2/3 cobertura; aqui mostra total
            n_ha    = 30 if produtividade <= 80 else (40 if produtividade <= 120 else 50)  # N base
            p2o5_ha = 80 if fosforo < 9 else (60 if fosforo < 18 else (40 if fosforo < 30 else 30))
            k2o_ha  = 100 if potassio < 40 else (80 if potassio < 60 else (60 if potassio < 120 else (45 if potassio < 180 else 30)))
            if produtividade > 100: n_ha += 10; p2o5_ha += 20; k2o_ha += 20
        elif cultura == "Trigo":
            n_ha    = 30  # N base (30-40 kg/ha); cobertura separada
            p2o5_ha = 80 if fosforo < 9 else (60 if fosforo < 18 else (40 if fosforo < 30 else 30))
            k2o_ha  = 80 if potassio < 40 else (60 if potassio < 60 else (45 if potassio < 120 else (30 if potassio < 180 else 20)))
        elif cultura == "Feijão":
            n_ha    = 20  # N base
            p2o5_ha = 100 if fosforo < 9 else (80 if fosforo < 18 else (60 if fosforo < 30 else 40))
            k2o_ha  = 100 if potassio < 40 else (80 if potassio < 60 else (60 if potassio < 120 else (45 if potassio < 180 else 30)))
        elif cultura == "Canola":
            n_ha    = 40
            p2o5_ha = 80 if fosforo < 9 else (60 if fosforo < 18 else 40)
            k2o_ha  = 80 if potassio < 40 else (60 if potassio < 60 else (45 if potassio < 120 else 30))
        elif cultura == "Aveia":
            n_ha    = 20
            p2o5_ha = 60 if fosforo < 9 else (40 if fosforo < 18 else 30)
            k2o_ha  = 60 if potassio < 40 else (45 if potassio < 60 else (30 if potassio < 120 else 20))
        else:
            n_ha    = 30
            p2o5_ha = 60 if fosforo < 9 else (40 if fosforo < 18 else 30)
            k2o_ha  = 60 if potassio < 40 else (45 if potassio < 60 else (30 if potassio < 120 else 25))

        # Redução de N por matéria orgânica alta
        if materia_organica >= 3.5:
            n_ha = max(0, n_ha - 10)
        if materia_organica >= 5.0:
            n_ha = max(0, n_ha - 20)

        # Ajuste do P pela classe de argila (CQFS RS/SC): solos mais argilosos
        # fixam mais fósforo, exigindo dose um pouco maior para o mesmo teor;
        # solos arenosos fixam menos. Ajuste suave de ±15%.
        if p2o5_ha > 0:
            if   argila >= 60: p2o5_ha *= 1.15   # muito argiloso — fixa mais P
            elif argila >= 40: p2o5_ha *= 1.07
            elif argila <  20: p2o5_ha *= 0.88    # arenoso — fixa menos P
            p2o5_ha = round(p2o5_ha, 1)

        # Aplicar fator de zona de produtividade
        n_ha    = round(n_ha    * fator_zona, 1)
        p2o5_ha = round(p2o5_ha * fator_zona, 1)
        k2o_ha  = round(k2o_ha  * fator_zona, 1)

        # Converter para produtos comerciais
        map_ha   = round(p2o5_ha / 0.52, 1)   # MAP 11-52-00: 52% P2O5
        kcl_ha   = round(k2o_ha  / 0.60, 1)   # KCl 00-00-60: 60% K2O
        ureia_ha = round(n_ha    / 0.45, 1) if n_ha > 0 else 0  # Ureia 45% N

        col1, col2, col3 = st.columns(3)
        col1.metric("Nitrogênio", f"{n_ha:.1f} kg/ha", delta=f"{((fator_zona-1)*100):+.0f}%")
        col2.metric("P₂O₅",      f"{p2o5_ha:.1f} kg/ha", delta=f"{((fator_zona-1)*100):+.0f}%")
        col3.metric("K₂O",       f"{k2o_ha:.1f} kg/ha", delta=f"{((fator_zona-1)*100):+.0f}%")
        st.divider()

        st.subheader("🌱 Opções de Adubação — escolha a que melhor se encaixa")
        st.caption(
            "Todas as opções abaixo entregam aproximadamente o mesmo NPK recomendado "
            f"(**N {n_ha:.0f} · P₂O₅ {p2o5_ha:.0f} · K₂O {k2o_ha:.0f}** kg/ha). "
            "A diferença está no custo, na praticidade e na tecnologia. "
            "As doses são calculadas pelo teor de cada fonte — confirme o teor exato "
            "do produto na sua revenda."
        )

        _ops_adubo = opcoes_adubacao(n_ha, p2o5_ha, k2o_ha)
        _cols_op = st.columns(len(_ops_adubo)) if len(_ops_adubo) <= 3 else st.columns(2)
        for _i_op, _op in enumerate(_ops_adubo):
            _col_alvo = _cols_op[_i_op % len(_cols_op)]
            with _col_alvo:
                _linhas_prod = ""
                for _nome_p, _kg_p, _desc_p in _op["itens"]:
                    _total_p = round(_kg_p * area, 0)
                    _linhas_prod += (
                        f"<div style='margin:6px 0;padding:8px;background:rgba(255,255,255,0.03);"
                        f"border-radius:8px;'>"
                        f"<div style='color:#f1f5f9;font-weight:700;font-size:13px;'>{_nome_p}</div>"
                        f"<div style='color:{_op['cor']};font-weight:800;font-size:15px;'>{_kg_p:.0f} kg/ha"
                        f" <span style='color:#94a3b8;font-weight:500;font-size:11px;'>"
                        f"({_total_p:.0f} kg total)</span></div>"
                        f"<div style='color:#64748b;font-size:10px;'>{_desc_p}</div></div>"
                    )
                st.markdown(f"""
                <div style='background:linear-gradient(160deg,#0f2a1a,#0b1f13);
                border:1px solid {_op['cor']}55;border-top:4px solid {_op['cor']};
                border-radius:14px;padding:14px;margin-bottom:12px;min-height:60px;'>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>
                <span style='color:#fff;font-weight:800;font-size:14px;'>{_op['nome']}</span></div>
                <span style='background:{_op['cor']};color:#04140b;font-weight:700;font-size:10px;
                padding:2px 10px;border-radius:100px;text-transform:uppercase;'>{_op['tag']}</span>
                {_linhas_prod}
                <div style='color:#94a3b8;font-size:11px;margin-top:8px;line-height:1.4;'>{_op['obs']}</div>
                </div>""", unsafe_allow_html=True)

        st.info(
            "💡 **Como escolher:** a opção econômica tem o menor custo por quilo de nutriente; "
            "os formulados prontos economizam operação; as linhas tecnológicas (Timac, Mosaic, Yara) "
            "custam mais por saco mas melhoram o aproveitamento e entregam enxofre/micros. "
            "A melhor escolha depende do seu solo, orçamento e logística — confirme com seu agrônomo."
        )

        # Mantém os valores tradicionais para o restante do fluxo (PDF, estoque)
        st.subheader("Total para a Área (base econômica)")
        total_map   = round(map_ha   * area, 1)
        total_kcl   = round(kcl_ha   * area, 1)
        total_ureia = round(ureia_ha  * area, 1)
        col1, col2, col3 = st.columns(3)
        col1.metric("MAP Total",   f"{total_map:.1f} kg")
        col2.metric("KCl Total",   f"{total_kcl:.1f} kg")
        col3.metric("Ureia Total", f"{total_ureia:.1f} kg")

        # ── Balanço de nutrientes: absorção × exportação × resíduo ──
        st.divider()
        st.subheader("🔬 Balanço de Nutrientes da Colheita")
        _bal = balanco_nutrientes(cultura, produtividade_ajustada)
        if _bal:
            st.caption(
                f"Para a meta de {produtividade_ajustada:.0f} sc/ha "
                f"(~{_bal['_ton_ha']} t/ha de grão), veja quanto a lavoura "
                f"absorve, quanto exporta no grão (o que precisa repor) e "
                f"quanto retorna ao solo na palhada:"
            )
            _nomes = {"N": "Nitrogênio (N)", "P2O5": "Fósforo (P₂O₅)", "K2O": "Potássio (K₂O)"}
            for _nut in ["N", "P2O5", "K2O"]:
                _b = _bal[_nut]
                st.markdown(f"""
                <div style='background:#0f172a;border:1px solid #1e3a2f;border-left:4px solid #22c55e;
                border-radius:10px;padding:10px 16px;margin:5px 0;'>
                <div style='color:#6ee7b7;font-weight:800;font-size:14px;margin-bottom:6px;'>{_nomes[_nut]}</div>
                <div style='display:flex;gap:24px;flex-wrap:wrap;'>
                <div><span style='color:#94a3b8;font-size:12px;'>🌱 Absorve (planta toda)</span><br>
                <span style='color:#f1f5f9;font-size:16px;font-weight:700;'>{_b['absorve']:.0f} kg/ha</span></div>
                <div><span style='color:#fbbf24;font-size:12px;'>📤 Exporta (sai no grão)</span><br>
                <span style='color:#fbbf24;font-size:16px;font-weight:700;'>{_b['exporta']:.0f} kg/ha</span></div>
                <div><span style='color:#38bdf8;font-size:12px;'>♻️ Volta ao solo (palhada)</span><br>
                <span style='color:#38bdf8;font-size:16px;font-weight:700;'>{_b['residuo']:.0f} kg/ha</span></div>
                </div></div>""", unsafe_allow_html=True)

            st.info(
                "💡 **Como ler:** a adubação de reposição precisa cobrir o que é "
                "**exportado no grão** (amarelo) — é o que sai da lavoura de vez. "
                "O que volta na palhada (azul) fica no sistema e é reaproveitado "
                "nas próximas safras (importante no plantio direto). A recomendação "
                "acima já considera esse balanço junto com o teor atual do solo."
            )
        else:
            st.caption("Balanço detalhado ainda não disponível para esta cultura.")

        st.divider()
        st.subheader("🚜 Enviar Recomendação para Aplicação")
        if st.button("Gerar Aplicação com Recomendação IA", key="gerar_aplicacao_ia"):
            nova_aplicacao = {
                "Data": str(date.today()),
                "ID Área": st.session_state.dados.get("id_area",""),
                "Talhão": st.session_state.dados.get("talhao",""),
                "Cultura": cultura, "Tipo": "Adubação IA", "Área ha": area,
                "Produtos": [
                    {"Insumo":"MAP 11-52-00","Dose ha":map_ha,"Quantidade usada":total_map,"Unidade":"kg"},
                    {"Insumo":"KCL 00-00-60","Dose ha":kcl_ha,"Quantidade usada":total_kcl,"Unidade":"kg"},
                    {"Insumo":"Ureia 45% N", "Dose ha":ureia_ha,"Quantidade usada":total_ureia,"Unidade":"kg"},
                ]
            }
            st.session_state.aplicacoes.append(nova_aplicacao)
            salvar_dados_iaagro()
            success_box("Aplicação de adubação IA enviada para o histórico!")
            st.markdown("**📦 Verificação de Estoque**")
            for prod in [{"Insumo":"MAP 11-52-00","Necessario":total_map},
                         {"Insumo":"KCL 00-00-60","Necessario":total_kcl},
                         {"Insumo":"Ureia 45% N","Necessario":total_ureia}]:
                nome       = prod["Insumo"]
                necessario = prod["Necessario"]
                estoque_item = next((item for item in st.session_state.estoque if item["Insumo"] == nome), None)
                if necessario <= 0:
                    _cor_e, _lbl_e, _det_e = "#64748b", "N/A", "não necessário nesta recomendação"
                elif estoque_item is None:
                    _cor_e, _lbl_e, _det_e = "#ef4444", "SEM CADASTRO", "não cadastrado no estoque"
                elif estoque_item.get("Quantidade",0) >= necessario:
                    sobra = estoque_item["Quantidade"] - necessario
                    _cor_e, _lbl_e, _det_e = "#22c55e", "OK", f"necessário {necessario:,.0f} kg · sobra {sobra:,.0f} kg"
                else:
                    falta     = necessario - estoque_item["Quantidade"]
                    cobertura = (estoque_item["Quantidade"] / necessario) * 100
                    _cor_e, _lbl_e, _det_e = "#f59e0b", "INSUFICIENTE", f"falta {falta:,.0f} kg · cobertura {cobertura:.0f}%"
                st.markdown(f"""
                <div style='background:#0f172a;border-left:3px solid {_cor_e};
                border-radius:6px;padding:4px 10px;margin:2px 0;
                display:flex;justify-content:space-between;align-items:center;'>
                <span style='color:#e2e8f0;font-size:12px;font-weight:600;'>{nome}</span>
                <span style='font-size:11px;'>
                <span style='color:{_cor_e};font-weight:700;letter-spacing:.3px;'>{_lbl_e}</span>
                <span style='color:#94a3b8;'> · {_det_e}</span>
                </span>
                </div>""", unsafe_allow_html=True)

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
        "🧾 Imposto de Renda Rural",
        "📊 Evolução por Safra",
        "💹 Dashboard",
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
        _avisos_preco  = []
        for _ap_idx, ap in enumerate(st.session_state.aplicacoes):
            for p in ap.get("Produtos", []):
                _nome_p  = p.get("Produto","")
                _total   = p.get("Total usado", 0)
                _unid    = p.get("Unidade","L/ha")
                _item_e  = next((e for e in st.session_state.estoque if e.get("Insumo") == _nome_p), None)
                _preco_u, _base_u, _aviso_u = preco_por_kg_ou_l(_item_e)
                if _aviso_u and _aviso_u not in _avisos_preco:
                    _avisos_preco.append(_aviso_u)
                def _conv(q, u):
                    u = (u or "").lower().replace(" ", "")
                    base = u.split("/")[0]
                    if base == "ml": return q/1000
                    if base == "g":  return q/1000
                    if base == "mg": return q/1_000_000
                    return q
                _qtd_base     = _conv(_total, _unid)
                _custo_p      = _qtd_base * _preco_u
                _custo_insumos += _custo_p
                _det_insumos.append({
                    "ap_idx":      _ap_idx,
                    "Aplicação":   ap.get("Estádio", ap.get("Aplicação","")),
                    "Produto":     _nome_p,
                    "Tipo":        _item_e.get("Categoria","") if _item_e else p.get("Tipo",""),
                    "Qtd":         f"{_qtd_base:.2f} {_base_u}",
                    "R$ unit":     f"R$ {_preco_u:.2f}/{_base_u}",
                    "Custo R$":    f"R$ {_custo_p:.2f}",
                })
        if _avisos_preco:
            for _av in _avisos_preco:
                warning_box(_av)

        if _det_insumos:
            # Tabela compacta rolante (estilo do alerta de estoque)
            _linhas_ins = []
            for _li, _row in enumerate(_det_insumos, 1):
                _cor_tipo = {
                    "Semente":"#a855f7","Fertilizante":"#22c55e","Herbicida":"#f59e0b",
                    "Fungicida":"#ef4444","Inseticida":"#3b82f6","Inoculante":"#14b8a6",
                }.get((_row.get("Tipo","") or "").split()[0] if _row.get("Tipo") else "", "#64748b")
                _linhas_ins.append(f"""
                <tr style='border-bottom:1px solid #1e293b;'>
                <td style='padding:5px 8px;color:#64748b;font-weight:700;text-align:center;width:28px;'>{_li}</td>
                <td style='padding:5px 8px;color:#e2e8f0;font-size:11px;'>{_row['Aplicação']}</td>
                <td style='padding:5px 8px;color:#6ee7b7;font-weight:600;'>{_row['Produto']}</td>
                <td style='padding:5px 8px;text-align:center;'><span style='color:{_cor_tipo};font-size:10px;font-weight:700;'>{_row['Tipo']}</span></td>
                <td style='padding:5px 8px;color:#cbd5e1;text-align:right;white-space:nowrap;'>{_row['Qtd']}</td>
                <td style='padding:5px 8px;color:#94a3b8;text-align:right;white-space:nowrap;font-size:11px;'>{_row['R$ unit']}</td>
                <td style='padding:5px 8px;color:#22c55e;font-weight:700;text-align:right;white-space:nowrap;'>{_row['Custo R$']}</td>
                </tr>""")
            st.markdown(f"""
            <div style='background:#0f172a;border:1px solid #334155;border-radius:8px;
            max-height:320px;overflow-y:auto;margin:2px 0;'>
            <table style='width:100%;border-collapse:collapse;font-size:12px;'>
            <thead>
            <tr style='position:sticky;top:0;background:#1e293b;z-index:1;'>
            <th style='padding:7px 8px;color:#94a3b8;font-size:10px;text-align:center;width:28px;'>#</th>
            <th style='padding:7px 8px;color:#94a3b8;font-size:10px;text-align:left;'>APLICAÇÃO</th>
            <th style='padding:7px 8px;color:#94a3b8;font-size:10px;text-align:left;'>PRODUTO</th>
            <th style='padding:7px 8px;color:#94a3b8;font-size:10px;text-align:center;'>TIPO</th>
            <th style='padding:7px 8px;color:#94a3b8;font-size:10px;text-align:right;'>QTD</th>
            <th style='padding:7px 8px;color:#94a3b8;font-size:10px;text-align:right;'>R$/UN</th>
            <th style='padding:7px 8px;color:#94a3b8;font-size:10px;text-align:right;'>CUSTO</th>
            </tr>
            </thead>
            <tbody>{''.join(_linhas_ins)}</tbody>
            </table>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""
            <div style='background:#14532d;border-radius:10px;padding:10px 16px;margin-top:8px;'>
            <span style='color:#6ee7b7;font-size:13px;font-weight:700;'>
            💰 Total insumos (todas aplicações): R$ {_custo_insumos:,.2f}
            </span></div>""", unsafe_allow_html=True)

            # Remover aplicação — seletor separado (botões não cabem na tabela HTML)
            with st.expander("🗑️ Remover uma aplicação registrada", expanded=False):
                st.caption("Se você registrou uma aplicação duplicada por engano, remova aqui. "
                           "A data e os produtos ajudam a identificar qual remover.")
                _opcoes_del = {}
                for _i, ap in enumerate(st.session_state.aplicacoes):
                    _est = ap.get('Estádio', ap.get('Aplicação', 'Aplicação'))
                    _dt  = ap.get('Data', ap.get('data', ''))
                    _prods = ', '.join(p.get('Produto','') for p in ap.get('Produtos',[])[:3])
                    _reticencias = '...' if len(ap.get('Produtos',[])) > 3 else ''
                    _label = f"[{_i+1}] {_est}"
                    if _dt:
                        _label += f" — {_dt}"
                    if _prods:
                        _label += f" | {_prods}{_reticencias}"
                    _opcoes_del[_label] = _i
                if _opcoes_del:
                    _sel_del = st.selectbox("Escolha a aplicação para remover:",
                                            list(_opcoes_del.keys()), key="sel_del_aplic")
                    if st.button("🗑️ Remover esta aplicação", key="btn_del_aplic_sel"):
                        _idx_del = _opcoes_del[_sel_del]
                        st.session_state.aplicacoes.pop(_idx_del)
                        salvar_dados_iaagro()
                        success_box("✅ Aplicação removida.")
                        st.rerun()
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
  with _sub_fin[4]:
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
  with _sub_fin[5]:
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
  with _sub_fin[3]:
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

    # ── Importação AUTOMÁTICA dos lançamentos (Financeiro + Estoque) ───────
    # Tudo que é lançado nas abas de Finanças (Custos da Lavoura, Custos
    # Complementares, Receitas, Contratos de Troca) e no Estoque entra aqui
    # automaticamente, recalculado a cada acesso (sem duplicar).
    _dre_all = st.session_state.get("dre_registros", [])
    def _pertence_ano_ir(_r):
        # Entra se a Safra OU a Data do lançamento bater com o ano-calendário
        # (custos complementares são gravados com Safra vazia, só com Data)
        _ano_s = str(st.session_state.ir_ano)
        return (str(_r.get("Safra","") or "").startswith(_ano_s[:4])
                or str(_r.get("Data","") or "").startswith(_ano_s))
    _dre_ano = [r for r in _dre_all if _pertence_ano_ir(r)] or _dre_all

    # Receitas automáticas (Financeiro)
    _auto_receitas = {"venda_graos": 0.0, "outras_receitas": 0.0}
    for _r in _dre_ano:
        if _r.get("Tipo") == "Receita":
            _auto_receitas["venda_graos"] += float(_r.get("Valor R$",0) or 0)

    # Receitas automáticas (Contratos de Troca / Barter — entrega de grãos)
    _trocas_all = st.session_state.get("contratos_troca", [])
    _trocas_ano = [c for c in _trocas_all
                   if str(c.get("Data entrega","")).startswith(str(st.session_state.ir_ano))] or _trocas_all
    _auto_rec_trocas = sum(float(c.get("Valor total R$",0) or 0) for c in _trocas_ano)

    # Despesas automáticas (Financeiro — todos os lançamentos de custo,
    # qualquer origem: lavoura, complementar, etc. — categorizados uma única vez)
    _mapa_cat = {
        "Semente":"sementes","Sementes":"sementes",
        "Fertilizante":"fertilizantes","Fertilizantes":"fertilizantes",
        "Defensivo":"fertilizantes","Defensivos":"fertilizantes",
        "Diesel":"combustivel","Diesel e lubrificantes":"combustivel",
        "Combustível":"combustivel",
        "Mão de obra":"mao_de_obra","Mão de obra mecânica":"mao_de_obra",
        "Maquinário":"manutencao","Aquisição de maquinário":"manutencao",
        "Manutenção":"manutencao","Conserto de máquinas":"manutencao",
        "Compra de peças":"manutencao","Revisão preventiva":"manutencao",
        "Pneus":"manutencao","Implementos":"manutencao",
        "Frete":"frete","Seguro":"seguro",
        "Arrendamento":"arrendamento_pg","Assistência técnica":"assistencia_tec",
        "Juros":"juros",
    }
    _auto_despesas = {}
    _lanc_fin_pdf  = []  # lançamentos individuais pro detalhamento do PDF
    for _r in _dre_ano:
        _vr = float(_r.get("Valor R$",0) or 0)
        if _r.get("Tipo") in ("Custo Variável","Custo Fixo","Custo","Despesa"):
            _chave = _mapa_cat.get(_r.get("Categoria",""), "outras_despesas")
            _auto_despesas[_chave] = _auto_despesas.get(_chave,0.0) + _vr
            _lanc_fin_pdf.append(("despesa", _r.get("Data",""), _r.get("Categoria",""),
                                  _r.get("Descrição",""), _vr))
        elif _r.get("Tipo") == "Receita":
            _lanc_fin_pdf.append(("receita", _r.get("Data",""), _r.get("Categoria",""),
                                  _r.get("Descrição",""), _vr))
    for _c in _trocas_ano:
        _lanc_fin_pdf.append(("receita", _c.get("Data entrega",""), "Contrato de troca (barter)",
                              f"{_c.get('Sacas',0):.0f} sc de {_c.get('Grão','')} × R$ {_c.get('Valor/sc R$',0):.2f}",
                              float(_c.get("Valor total R$",0) or 0)))

    # Despesas automáticas (Estoque de Insumos — valor investido em cada item)
    _mapa_cat_estq = {
        "semente":"sementes","fertilizante":"fertilizantes","adubo":"fertilizantes",
        "defensivo":"fertilizantes","herbicida":"fertilizantes","fungicida":"fertilizantes",
        "inseticida":"fertilizantes","inoculante":"fertilizantes","adjuvante":"fertilizantes",
        "óleo":"fertilizantes","oleo":"fertilizantes","micronutriente":"fertilizantes",
        "combustível":"combustivel","combustivel":"combustivel","diesel":"combustivel",
    }
    _estq_por_cat = {}
    for _it in st.session_state.get("estoque", []):
        _vt = float(_it.get("Valor Total R$",0) or 0)
        if _vt <= 0:
            _vt = round(float(_it.get("Quantidade",0) or 0) * float(_it.get("Valor Unitário R$",0) or 0), 2)
        if _vt <= 0:
            continue
        _cat_i  = (_it.get("Categoria","") or "").lower()
        _chave  = next((v for k, v in _mapa_cat_estq.items() if k in _cat_i), "outras_despesas")
        _auto_despesas[_chave] = _auto_despesas.get(_chave,0.0) + _vt
        _estq_por_cat.setdefault(_chave, []).append((_it.get("Insumo",""), _vt))

    _auto_rec_total  = sum(_auto_receitas.values()) + _auto_rec_trocas
    _auto_desp_total = sum(_auto_despesas.values())

    if _auto_rec_total > 0 or _auto_desp_total > 0:
        st.markdown(f"""
        <div style='background:#14532d;border-radius:10px;padding:12px 16px;
        border-left:4px solid #22c55e;margin-bottom:12px;'>
        <b style='color:#6ee7b7;'>✅ Importado automaticamente do Financeiro e do Estoque</b><br>
        <span style='color:#f1f5f9;font-size:13px;'>
        💰 Receitas lançadas: <b>R$ {sum(_auto_receitas.values()):,.2f}</b> &nbsp;|&nbsp;
        🤝 Contratos de troca: <b>R$ {_auto_rec_trocas:,.2f}</b> &nbsp;|&nbsp;
        📉 Despesas/custos (Financeiro + Estoque): <b>R$ {_auto_desp_total:,.2f}</b><br>
        <span style='color:#94a3b8;font-size:11px;'>Esses valores já entram no cálculo abaixo — os campos manuais servem pra complementar o que não foi lançado no app.</span>
        </span></div>""", unsafe_allow_html=True)

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
    _rec_total  = sum(st.session_state.ir_receitas.values()) + _auto_rec_total
    _desp_total = sum(st.session_state.ir_despesas.values()) + _auto_desp_total

    # ── Regime de apuração ──
    # Livro Caixa (real): resultado = receitas - despesas comprovadas
    # Simplificado (presumido): resultado tributável = 20% da receita bruta
    #   (usado por quem não escritura Livro Caixa; a Receita presume 20%)
    st.markdown("#### ⚖️ Regime de Apuração do Resultado")
    _regime = st.radio(
        "Como apurar o resultado tributável?",
        ["📒 Livro Caixa (receitas − despesas reais)",
         "📊 Simplificado (20% da receita bruta)"],
        key="ir_regime", horizontal=False,
        help="Livro Caixa: usa suas despesas reais (melhor quando os custos são altos). "
             "Simplificado: a Receita presume que o lucro é 20% da receita bruta, "
             "ignorando os custos (melhor só quando a margem é muito alta)."
    )

    if _regime.startswith("📊"):
        _resultado = _rec_total * 0.20   # 20% da receita bruta (arbitramento)
        _base_desc = "20% da receita bruta (regime simplificado)"
    else:
        _resultado = _rec_total - _desp_total
        _base_desc = "receitas − despesas (Livro Caixa)"

    _BASE = max(_resultado, 0.0)

    # ── Tabelas progressivas ANUAIS oficiais por ano-calendário (IN RFB 2174) ──
    # Cada faixa: (limite_superior, alíquota, parcela_a_deduzir)
    _tabelas_por_ano = {
        2025: [  # exercício 2026, ano-calendário 2025
            (27110.40, 0.000, 0.00),
            (33919.80, 0.075, 2033.28),
            (45012.60, 0.150, 4577.27),
            (55976.16, 0.225, 7953.21),
            (float("inf"), 0.275, 10752.02),
        ],
        2024: [  # exercício 2025, ano-calendário 2024
            (26963.20, 0.000, 0.00),
            (33919.80, 0.075, 2022.24),
            (45012.60, 0.150, 4566.23),
            (55976.16, 0.225, 7942.17),
            (float("inf"), 0.275, 10740.98),
        ],
    }
    # 2023 e 2022 usam a tabela vigente até então (mesma base de 2024 como aproximação)
    _tabela_ir = _tabelas_por_ano.get(st.session_state.ir_ano, _tabelas_por_ano[2024])

    # IMPORTANTE: o resultado positivo da atividade rural é somado aos demais
    # rendimentos e tributado DIRETO pela tabela progressiva. A "isenção" é
    # apenas a 1ª faixa da tabela (até ~R$ 27 mil) — NÃO existe isenção até
    # R$ 142.798,50 (esse valor é só o limite de OBRIGATORIEDADE de declarar).
    _ir = 0.0; _aliq = 0.0
    for _lim, _a, _ded in _tabela_ir:
        if _BASE <= _lim:
            _ir = max(_BASE * _a - _ded, 0.0)
            _aliq = _a
            break

    _ir = max(_ir, 0.0)
    _LIMITE_DECLARAR = 142798.50  # receita bruta que obriga a declarar

    # Cards resultado
    _kc = st.columns(4)
    _kc[0].metric("💰 Receita Bruta",    f"R$ {_rec_total:,.2f}")
    _kc[1].metric("📉 Despesas Dedut.", f"R$ {_desp_total:,.2f}")
    _kc[2].metric("📊 Resultado Tributável", f"R$ {_resultado:,.2f}",
                   delta="Lucro" if _resultado >= 0 else "Prejuízo")
    _kc[3].metric("🧾 IR Estimado",       f"R$ {_ir:,.2f}",
                   delta=f"Alíquota {_aliq*100:.1f}%" if _ir > 0 else "Isento")

    # Status fiscal
    if _resultado <= 0:
        st.success("✅ Resultado negativo ou zero — não há IR a pagar. "
                   "O prejuízo pode ser compensado em anos seguintes (com Livro Caixa).")
    elif _ir <= 0:
        st.success(f"✅ Resultado dentro da faixa de isenção da tabela progressiva "
                   f"(até R$ {_tabela_ir[0][0]:,.2f}) — não há IR a pagar.")
    else:
        st.warning(f"⚠️ IR estimado: **R$ {_ir:,.2f}** (alíquota {_aliq*100:.1f}%) — "
                   f"apurado por {_base_desc}. Confirme com seu contador.")

    # Aviso de obrigatoriedade de declarar
    if _rec_total > _LIMITE_DECLARAR:
        st.info(f"📋 Sua receita bruta rural (R$ {_rec_total:,.2f}) ultrapassa "
                f"R$ {_LIMITE_DECLARAR:,.2f} — você está **obrigado a declarar** "
                f"a atividade rural no IRPF, mesmo que não haja imposto a pagar.")

    # Tabela resumo
    with st.expander("📋 Detalhamento completo"):
        import pandas as _pd_ir
        _rows_ir = [
            {"Item":"(+) Receitas automáticas (Financeiro)",  "Valor R$": sum(_auto_receitas.values())},
            {"Item":"(+) Contratos de troca (barter)",         "Valor R$": _auto_rec_trocas},
            {"Item":"(+) Receitas manuais",                    "Valor R$": sum(st.session_state.ir_receitas.values())},
            {"Item":"(=) Receita Bruta Total",                 "Valor R$": _rec_total},
            {"Item":"(-) Despesas automáticas (Fin.+Estoque)", "Valor R$":-_auto_desp_total},
            {"Item":"(-) Despesas manuais",                    "Valor R$":-sum(st.session_state.ir_despesas.values())},
            {"Item":f"= Resultado Tributável ({_base_desc})",  "Valor R$": _resultado},
            {"Item":"Base de Cálculo IR",         "Valor R$": _BASE},
            {"Item":f"Alíquota {_aliq*100:.1f}%","Valor R$": _ir},
        ]
        st.dataframe(_pd_ir.DataFrame(_rows_ir), use_container_width=True, hide_index=True)
        st.caption(f"⚠️ Estimativa para planejamento, com a tabela progressiva anual de "
                   f"{st.session_state.ir_ano}. O resultado da atividade rural soma-se aos "
                   f"demais rendimentos da pessoa física. Declare com contador habilitado.")

    # ── EXPORTAÇÃO EM PDF ───────────────────────────────────────────────────
    st.divider()
    st.markdown("#### 📥 Exportar Relatório IR Rural (PDF)")

    def _gerar_pdf_ir_rural():
        from reportlab.lib.pagesizes import A4 as _A4
        from reportlab.lib import colors as _cores
        from reportlab.lib.units import cm as _cm, mm as _mm
        from reportlab.platypus import SimpleDocTemplate as _Doc, Paragraph as _Par, Spacer as _Spc, Table as _Tab, TableStyle as _TSt, HRFlowable as _HR
        from reportlab.lib.styles import ParagraphStyle as _PSt
        from reportlab.lib.enums import TA_LEFT as _TL, TA_CENTER as _TC, TA_RIGHT as _TR
        import io as _io

        _VERDE_E = _cores.HexColor("#14532d"); _VERDE = _cores.HexColor("#22c55e")
        _TXT = _cores.HexColor("#1e293b"); _SUB = _cores.HexColor("#64748b")
        _BRANCO = _cores.white; _CINZA = _cores.HexColor("#f1f5f9"); _BORDA = _cores.HexColor("#cbd5e1")

        def _P(t, s=9, b=False, c=None, a=_TL):
            return _Par(t, _PSt("p", fontName="Helvetica-Bold" if b else "Helvetica",
                        fontSize=s, textColor=c or _TXT, alignment=a, leading=s+3))

        _buf = _io.BytesIO()
        _doc = _Doc(_buf, pagesize=_A4, topMargin=1.2*_cm, bottomMargin=1.2*_cm,
                    leftMargin=1.4*_cm, rightMargin=1.4*_cm)
        _story = []

        # Cabeçalho
        _hdr = _Tab([[_P("IAAgro", 16, True, _VERDE), _P("APURAÇÃO IR RURAL", 14, True, _BRANCO, _TC),
                      _P(f"Ano-calendário: {st.session_state.ir_ano}<br/>Emitido: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 7, False, _BRANCO, _TR)]],
                    colWidths=[4*_cm, 9.5*_cm, 5*_cm])
        _hdr.setStyle(_TSt([("BACKGROUND",(0,0),(-1,-1),_VERDE_E),("TOPPADDING",(0,0),(-1,-1),10),
                            ("BOTTOMPADDING",(0,0),(-1,-1),10),("LEFTPADDING",(0,0),(-1,-1),10),
                            ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        _story.append(_hdr); _story.append(_Spc(1, 3*_mm))

        # Dados do produtor
        _dp_tab = _Tab([[_P(f"<b>Produtor:</b> {st.session_state.ir_nome or '—'}", 9),
                         _P(f"<b>CPF:</b> {st.session_state.ir_cpf or '—'}", 9),
                         _P(f"<b>Cidade/UF:</b> {st.session_state.ir_cidade or '—'}", 9),
                         _P(f"<b>Área total:</b> {st.session_state.ir_area_total} ha", 9)]],
                       colWidths=[6*_cm, 4*_cm, 4.5*_cm, 4*_cm])
        _dp_tab.setStyle(_TSt([("GRID",(0,0),(-1,-1),0.4,_BORDA),("TOPPADDING",(0,0),(-1,-1),6),
                               ("BOTTOMPADDING",(0,0),(-1,-1),6),("LEFTPADDING",(0,0),(-1,-1),8)]))
        _story.append(_dp_tab); _story.append(_Spc(1, 4*_mm))

        _LBL_REC = dict(_rec_items); _LBL_DESP = dict(_desp_items)

        # Receitas
        _story.append(_P("RECEITAS DA ATIVIDADE RURAL", 11, True, _VERDE_E)); _story.append(_Spc(1, 2*_mm))
        _rrows = [[_P("Descrição",8,True,_BRANCO), _P("Origem",8,True,_BRANCO,_TC), _P("Valor",8,True,_BRANCO,_TR)]]
        if _auto_receitas.get("venda_graos",0) > 0:
            _rrows.append([_P("Venda de produção (lançamentos do Financeiro)",8), _P("Automático",8,False,_SUB,_TC),
                           _P(f"R$ {_auto_receitas['venda_graos']:,.2f}",8,True,None,_TR)])
        if _auto_rec_trocas > 0:
            _rrows.append([_P("Contratos de troca / barter (entrega de grãos)",8), _P("Automático",8,False,_SUB,_TC),
                           _P(f"R$ {_auto_rec_trocas:,.2f}",8,True,None,_TR)])
        for _k, _v in st.session_state.ir_receitas.items():
            if float(_v or 0) > 0:
                _rrows.append([_P(_LBL_REC.get(_k,_k).replace(" (R$)",""),8), _P("Manual",8,False,_SUB,_TC),
                               _P(f"R$ {float(_v):,.2f}",8,True,None,_TR)])
        _rrows.append([_P("<b>TOTAL RECEITAS</b>",9,True,_BRANCO), _P("",8),
                       _P(f"<b>R$ {_rec_total:,.2f}</b>",9,True,_BRANCO,_TR)])
        _rt = _Tab(_rrows, colWidths=[11*_cm, 3.5*_cm, 4*_cm])
        _rt.setStyle(_TSt([("BACKGROUND",(0,0),(-1,0),_VERDE_E),("BACKGROUND",(0,-1),(-1,-1),_VERDE),
                           ("GRID",(0,0),(-1,-1),0.4,_BORDA),("TOPPADDING",(0,0),(-1,-1),5),
                           ("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),8)]))
        _story.append(_rt); _story.append(_Spc(1, 4*_mm))

        # Despesas
        _story.append(_P("DESPESAS DEDUTÍVEIS", 11, True, _VERDE_E)); _story.append(_Spc(1, 2*_mm))
        _drows = [[_P("Descrição",8,True,_BRANCO), _P("Origem",8,True,_BRANCO,_TC), _P("Valor",8,True,_BRANCO,_TR)]]
        for _k, _v in sorted(_auto_despesas.items(), key=lambda x: -x[1]):
            if _v > 0:
                _drows.append([_P(_LBL_DESP.get(_k,_k).replace(" (R$)",""),8), _P("Automático (Fin./Estoque)",8,False,_SUB,_TC),
                               _P(f"R$ {_v:,.2f}",8,True,None,_TR)])
        for _k, _v in st.session_state.ir_despesas.items():
            if float(_v or 0) > 0:
                _drows.append([_P(_LBL_DESP.get(_k,_k).replace(" (R$)",""),8), _P("Manual",8,False,_SUB,_TC),
                               _P(f"R$ {float(_v):,.2f}",8,True,None,_TR)])
        _drows.append([_P("<b>TOTAL DESPESAS</b>",9,True,_BRANCO), _P("",8),
                       _P(f"<b>R$ {_desp_total:,.2f}</b>",9,True,_BRANCO,_TR)])
        _dt = _Tab(_drows, colWidths=[11*_cm, 3.5*_cm, 4*_cm])
        _dt.setStyle(_TSt([("BACKGROUND",(0,0),(-1,0),_VERDE_E),("BACKGROUND",(0,-1),(-1,-1),_VERDE),
                           ("GRID",(0,0),(-1,-1),0.4,_BORDA),("TOPPADDING",(0,0),(-1,-1),5),
                           ("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),8)]))
        _story.append(_dt); _story.append(_Spc(1, 4*_mm))

        # Detalhamento do Estoque
        _itens_estq_pdf = [(_nm, _vl) for _lst in _estq_por_cat.values() for _nm, _vl in _lst]
        if _itens_estq_pdf:
            _story.append(_P("DETALHAMENTO — INSUMOS DO ESTOQUE", 11, True, _VERDE_E)); _story.append(_Spc(1, 2*_mm))
            _erows = [[_P("Insumo",8,True,_BRANCO), _P("Valor investido",8,True,_BRANCO,_TR)]]
            for _nm, _vl in sorted(_itens_estq_pdf, key=lambda x: -x[1]):
                _erows.append([_P(_nm,8), _P(f"R$ {_vl:,.2f}",8,False,None,_TR)])
            _et = _Tab(_erows, colWidths=[14.5*_cm, 4*_cm])
            _et.setStyle(_TSt([("BACKGROUND",(0,0),(-1,0),_VERDE_E),("GRID",(0,0),(-1,-1),0.4,_BORDA),
                               ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
                               ("LEFTPADDING",(0,0),(-1,-1),8),
                               *[("BACKGROUND",(0,i),(-1,i),_CINZA) for i in range(2, len(_erows), 2)]]))
            _story.append(_et); _story.append(_Spc(1, 4*_mm))

        # Detalhamento dos lançamentos do Financeiro (cada custo/receita/troca lançado)
        if _lanc_fin_pdf:
            _story.append(_P("DETALHAMENTO — LANÇAMENTOS DO FINANCEIRO", 11, True, _VERDE_E)); _story.append(_Spc(1, 2*_mm))
            _lrows = [[_P("Data",8,True,_BRANCO), _P("Tipo",8,True,_BRANCO,_TC),
                       _P("Categoria",8,True,_BRANCO), _P("Descrição",8,True,_BRANCO),
                       _P("Valor",8,True,_BRANCO,_TR)]]
            for _tp, _dt_l, _cat_l2, _dsc_l, _vl_l in sorted(_lanc_fin_pdf, key=lambda x: str(x[1])):
                _lrows.append([
                    _P(str(_dt_l or "—"),7),
                    _P("Receita" if _tp == "receita" else "Despesa",7,False,
                       _VERDE if _tp == "receita" else _SUB,_TC),
                    _P(str(_cat_l2 or "—"),7),
                    _P(str(_dsc_l or "—"),7),
                    _P(f"R$ {_vl_l:,.2f}",7,True,None,_TR),
                ])
            _lt = _Tab(_lrows, colWidths=[2.2*_cm, 1.8*_cm, 4.2*_cm, 6.8*_cm, 3.5*_cm])
            _lt.setStyle(_TSt([("BACKGROUND",(0,0),(-1,0),_VERDE_E),("GRID",(0,0),(-1,-1),0.4,_BORDA),
                               ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
                               ("LEFTPADDING",(0,0),(-1,-1),6),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                               *[("BACKGROUND",(0,i),(-1,i),_CINZA) for i in range(2, len(_lrows), 2)]]))
            _story.append(_lt); _story.append(_Spc(1, 4*_mm))

        # Apuração final
        _story.append(_P("APURAÇÃO", 11, True, _VERDE_E)); _story.append(_Spc(1, 2*_mm))
        _arows = [
            [_P("(+) Receita Bruta",9), _P(f"R$ {_rec_total:,.2f}",9,True,None,_TR)],
            [_P("(-) Despesas Dedutíveis",9), _P(f"R$ {_desp_total:,.2f}",9,True,None,_TR)],
            [_P("<b>= Resultado Líquido</b>",9,True), _P(f"<b>R$ {_resultado:,.2f}</b>",9,True,None,_TR)],
            [_P("Limite de Isenção",9), _P(f"R$ {_ISENCAO:,.2f}",9,False,None,_TR)],
            [_P(f"<b>IR Estimado (alíquota {_aliq*100:.1f}%)</b>",10,True,_BRANCO),
             _P(f"<b>R$ {_ir:,.2f}</b>",11,True,_BRANCO,_TR)],
        ]
        _at = _Tab(_arows, colWidths=[13*_cm, 5.5*_cm])
        _at.setStyle(_TSt([("GRID",(0,0),(-1,-1),0.4,_BORDA),("TOPPADDING",(0,0),(-1,-1),6),
                           ("BOTTOMPADDING",(0,0),(-1,-1),6),("LEFTPADDING",(0,0),(-1,-1),8),
                           ("BACKGROUND",(0,-1),(-1,-1),_VERDE_E)]))
        _story.append(_at); _story.append(_Spc(1, 3*_mm))
        _story.append(_HR(width="100%", thickness=1, color=_VERDE))
        _story.append(_Spc(1, 2*_mm))
        _story.append(_P("Estimativa para planejamento — Lei 8.023/90. Declare com contador habilitado. | IAAgro", 7, False, _SUB, _TC))
        _doc.build(_story)
        _buf.seek(0)
        return _buf.read()

    try:
        _pdf_ir_bytes = _gerar_pdf_ir_rural()
        st.download_button(
            "📥 Baixar PDF do IR Rural",
            data=_pdf_ir_bytes,
            file_name=f"ir_rural_{st.session_state.ir_ano}.pdf",
            mime="application/pdf",
            key="btn_pdf_ir_rural",
            use_container_width=True, type="primary",
        )
    except Exception as _e_pdf:
        error_box(f"Erro ao gerar PDF do IR: {_e_pdf}")

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
                    atualizar_area_atual()  # sincroniza área (preserva aplicações)
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
                atualizar_area_atual()  # sincroniza área (preserva aplicações)
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

                # Detecta o namespace real do XML automaticamente
                _tag_root = _root.tag
                if _tag_root.startswith("{"):
                    _ns_uri = _tag_root[1:_tag_root.find("}")]
                else:
                    _ns_uri = "http://www.portalfiscal.inf.br/nfe"
                _ns = {"nfe": _ns_uri}

                def _txt(el, tag, ns):
                    _e = el.find(tag, ns)
                    return _e.text.strip() if _e is not None and _e.text else ""

                # Dados da NF
                _inf = _root.find(".//nfe:infNFe", _ns)
                if _inf is None:
                    _inf = _root.find(".//{http://www.portalfiscal.inf.br/nfe}infNFe")
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
                    _prod_el = _det.find("nfe:prod", _ns)
                    if _prod_el is None:
                        _prod_el = _det.find("{http://www.portalfiscal.inf.br/nfe}prod")
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
                        atualizar_area_atual()  # vincula estoque importado à área (preserva aplicações)
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
            with st.expander(f"🔔 {len(_alertas)} alerta(s) de estoque", expanded=False):
                _al_ord = sorted(_alertas, key=lambda i: float(i.get("Quantidade",0) or 0))
                _linhas_al = []
                for _n, _al in enumerate(_al_ord, 1):
                    _q_a = float(_al.get("Quantidade",0) or 0)
                    _zr  = _q_a <= 0
                    _cor_s = "#ef4444" if _zr else "#f59e0b"
                    _lbl_s = "ESGOTADO" if _zr else "BAIXO"
                    _linhas_al.append(f"""
                    <tr style='border-bottom:1px solid #1e293b;'>
                    <td style='padding:5px 10px;color:#64748b;font-weight:700;text-align:center;width:34px;'>{_n}</td>
                    <td style='padding:5px 10px;color:#e2e8f0;font-weight:600;'>{_al.get('Insumo','')}</td>
                    <td style='padding:5px 10px;color:#cbd5e1;text-align:right;white-space:nowrap;'>{_q_a:.1f} {_al.get('Unidade','')}</td>
                    <td style='padding:5px 10px;color:#94a3b8;text-align:right;white-space:nowrap;'>{float(_al.get('Estoque Mínimo',5)):.0f}</td>
                    <td style='padding:5px 10px;text-align:center;white-space:nowrap;'>
                    <span style='color:{_cor_s};font-weight:700;font-size:11px;letter-spacing:.3px;'>{_lbl_s}</span></td>
                    </tr>""")
                st.markdown(f"""
                <div style='background:#0f172a;border:1px solid #334155;border-radius:8px;
                max-height:230px;overflow-y:auto;margin:2px 0;'>
                <table style='width:100%;border-collapse:collapse;font-size:12px;'>
                <thead>
                <tr style='position:sticky;top:0;background:#1e293b;z-index:1;'>
                <th style='padding:6px 10px;color:#94a3b8;font-size:11px;text-align:center;width:34px;'>#</th>
                <th style='padding:6px 10px;color:#94a3b8;font-size:11px;text-align:left;'>INSUMO</th>
                <th style='padding:6px 10px;color:#94a3b8;font-size:11px;text-align:right;'>QTD</th>
                <th style='padding:6px 10px;color:#94a3b8;font-size:11px;text-align:right;'>MÍN</th>
                <th style='padding:6px 10px;color:#94a3b8;font-size:11px;text-align:center;'>STATUS</th>
                </tr>
                </thead>
                <tbody>{''.join(_linhas_al)}</tbody>
                </table>
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
                    atualizar_area_atual()  # vincula à área (preserva aplicações)
                    success_box(f"✅ {_prod_edit} atualizado: {_nova_qtd} {_item_edit.get('Unidade','')}")
                    st.rerun()
                if col_btn2.button("🗑️ Excluir produto", key="btn_excluir_est", use_container_width=True):
                    st.session_state.estoque = [i for i in st.session_state.estoque if i["Insumo"] != _prod_edit]
                    atualizar_area_atual()  # vincula à área (preserva aplicações)
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
        "🚜 Plantio","🌱 Pré-plantio","🌿 Pós-plantio / V0","🌾 V1 – V3","🌾 V4 – V6",
        "🌾 V7 – VT","🌸 R1 – R2 (Floração)","🫘 R3 – R4 (Granação)",
        "🫘 R5 – R6","🌾 Pré-colheita","📋 Outro",
    ]
    TIPOS_PRODUTO = ["Herbicida","Fungicida","Inseticida","Adjuvante",
                     "Óleo mineral/vegetal","Fertilizante foliar","Regulador","Outro"]

    if len(st.session_state.estoque) == 0:
        warning_box("Cadastre produtos no estoque antes de registrar aplicações.")
    else:
        # ── SELEÇÃO DE CULTURA ATIVA ────────────────────────────────────────────
        if "aplic_cultura_ativa" not in st.session_state:
            st.session_state.aplic_cultura_ativa = None
        if "aplic_ha_ativo" not in st.session_state:
            st.session_state.aplic_ha_ativo = 0.0

        _CULTURAS_PLAN = [
            "🌱 Soja","🌽 Milho 1ª Safra","🌽 Milho 2ª Safra (Safrinha)",
            "🌾 Trigo","🌾 Aveia","🌻 Canola","🌱 Feijão","🍚 Arroz","🌾 Sorgo","🌿 Outro"
        ]

        st.markdown("""
        <div style='background:linear-gradient(135deg,#14532d,#0f3d20);border-radius:14px;
        padding:16px 20px;margin-bottom:16px;border:1px solid #22c55e44;'>
        <b style='color:#6ee7b7;font-size:15px;'>🌾 Planejamento de Safra por Cultura</b><br>
        <span style='color:#94a3b8;font-size:12px;'>
        Selecione a cultura e o total de hectares. Monte todas as aplicações e gere o PDF.
        Depois inicie o planejamento da próxima cultura.
        </span></div>""", unsafe_allow_html=True)

        _pc1, _pc2, _pc3 = st.columns([3,2,2])
        _cult_sel = _pc1.selectbox("🌱 Cultura", _CULTURAS_PLAN,
            index=_CULTURAS_PLAN.index(st.session_state.aplic_cultura_ativa)
                  if st.session_state.aplic_cultura_ativa in _CULTURAS_PLAN else 0,
            key="sel_cult_aplic_ativa")
        _ha_sel = _pc2.number_input("Total de hectares", min_value=0.0,
            value=st.session_state.aplic_ha_ativo, step=0.5, key="num_ha_aplic_ativo")

        if _pc3.button("✅ Confirmar Cultura", key="btn_confirmar_cultura_aplic",
                       use_container_width=True, type="primary"):
            st.session_state.aplic_cultura_ativa = _cult_sel
            st.session_state.aplic_ha_ativo      = _ha_sel
            salvar_dados_iaagro()
            st.rerun()

        if st.session_state.aplic_cultura_ativa:
            _cult_ativa = st.session_state.aplic_cultura_ativa
            _ha_ativo   = st.session_state.aplic_ha_ativo
            # Contagem de aplicações desta cultura
            _aplic_cultura = [a for a in st.session_state.aplicacoes
                               if a.get("Cultura") == _cult_ativa]
            _kc1, _kc2, _kc3 = st.columns(3)
            _kc1.metric("🌾 Cultura ativa", _cult_ativa.split(" ",1)[-1] if " " in _cult_ativa else _cult_ativa)
            _kc2.metric("📐 Hectares", f"{_ha_ativo:.1f} ha")
            _kc3.metric("📋 Aplicações", len(_aplic_cultura))

            if _pc3.button("🔄 Nova Cultura", key="btn_nova_cultura_aplic",
                           use_container_width=True):
                st.session_state.aplic_cultura_ativa = None
                st.session_state.aplic_ha_ativo      = 0.0
                st.rerun()

        st.divider()
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
                                          value=float(st.session_state.aplic_ha_ativo) if st.session_state.aplic_ha_ativo > 0 else float(st.session_state.dados.get("area", 0.0)),
                                          key="num_area_aplic")
        with col_h3:
            _calda_opcao = st.selectbox("Volume calda (L/ha)",
                ["— Não se aplica —","50","80","100","120","150","200","Outro"],
                key="sel_calda_opcao")
            if _calda_opcao == "— Não se aplica —":
                calda_lha = 0.0
            elif _calda_opcao == "Outro":
                calda_lha = st.number_input("Volume calda personalizado (L/ha)", min_value=0.0, value=100.0, key="num_calda_custom")
            else:
                calda_lha = float(_calda_opcao)

            _tanque_opcao = st.selectbox("Capacidade tanque (L)",
                ["— Não se aplica —","1000","1500","2000","2500","3000","4000","Outro"],
                key="sel_tanque_opcao",
                help="💾 Selecione o volume do tanque do pulverizador")
            if _tanque_opcao == "— Não se aplica —":
                cap_tanque = 0.0
            elif _tanque_opcao == "Outro":
                _cap_salva = st.session_state.dados.get("cap_tanque_salva", 3000.0)
                cap_tanque = st.number_input("Capacidade personalizada (L)", min_value=0.0,
                                              value=float(_cap_salva), key="num_cap_tanque")
                if cap_tanque != _cap_salva and cap_tanque > 0:
                    st.session_state.dados["cap_tanque_salva"] = cap_tanque
                    salvar_dados_iaagro()
            else:
                cap_tanque = float(_tanque_opcao)

        if calda_lha > 0 and cap_tanque > 0:
            area_por_tanque = round(cap_tanque / calda_lha, 2)
            n_tanques       = round(area_aplic / area_por_tanque, 2) if area_por_tanque > 0 else 0
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("📐 Área por tanque", f"{area_por_tanque} ha")
            col_m2.metric("🪣 Nº de tanques",   f"{n_tanques}")
        else:
            area_por_tanque = 0.0
            n_tanques       = 0.0

        with st.expander("🧑‍🌾 Dados do operador", expanded=False):
            col_o1, col_o2, col_o3 = st.columns(3)
            operador     = col_o1.text_input("Operador", key="txt_operador_aplic")
            pulverizador = col_o2.text_input("Pulverizador/Máquina", key="txt_pulv_aplic")
            velocidade   = col_o1.number_input("Velocidade (km/h)", min_value=0.0, key="num_veloc_aplic")
            pressao      = col_o2.number_input("Pressão (bar)", min_value=0.0, key="num_pressao_aplic")
            clima_aplic  = col_o3.selectbox("Clima", ["Adequado","Vento alto","Muito seco","Chuva próxima","Muito quente"], key="sel_clima_aplic")

        # ── CAMPOS ESPECIAIS PARA PLANTIO ─────────────────────────────────────
        _is_plantio = estadio_sel == "🚜 Plantio"
        if _is_plantio:
            st.markdown("""
            <div style='background:#14532d;border-radius:12px;padding:14px 18px;
            border-left:4px solid #22c55e;margin:8px 0;'>
            <b style='color:#6ee7b7;font-size:14px;'>🚜 Configuração de Plantio</b><br>
            <span style='color:#94a3b8;font-size:12px;'>
            Preencha os fertilizantes de base, KCl, ureia e inoculantes que serão aplicados no sulco.
            </span></div>""", unsafe_allow_html=True)

            st.markdown("#### 🌱 Sementes — Múltiplas Variedades")

            # Init lista de variedades na sessão
            if "pl_variedades" not in st.session_state:
                st.session_state.pl_variedades = []

            # Siglas/abreviações das principais empresas/obtentoras de sementes do
            # mercado brasileiro. Cultivares comerciais quase sempre são nomeados
            # como "SIGLA + código" (ex.: "BMX Desafio RR", "TMG 7062", "DKB 390"),
            # então o nome do insumo no estoque nem sempre contém a palavra
            # "semente/soja/milho" — precisamos reconhecer também a sigla da marca.
            _SIGLAS_SEMENTES = [
                "bmx",       # Brasmax
                "tmg",       # TMG - Tropical Melhoramento e Genética
                "ns",        # Nidera Semillas
                "dm",        # Don Mario / GDM
                "syn",       # Syngenta
                "nk",        # NK - Syngenta (milho)
                "cz",        # Coodetec
                "brs",       # Embrapa
                "fts",       # Fundação MT
                "tec",       # TEC Sementes
                "st",        # Stine
                "dkb",       # Dekalb (milho) - Bayer
                "ag",        # Agroceres (milho)
                "gh",        # Golden Harvest
                "fundacep",  # Fundacep
                "gdm",       # GDM Seeds (Don Mario)
                "aba",       # Aba Agro
                "bs",        # Brasil Seed
                "w",         # W - Sementes
                "cd",        # Coodetec (registros antigos)
                "bono",      # Bono Sementes
                "sps",       # Sementes SPS
            ]
            # regex para achar a sigla como "palavra" (evita falso-positivo tipo
            # "st" dentro de "Ativo"), aceitando também colada a número: "BMX8579"
            _re_siglas = re.compile(
                r"\b(" + "|".join(re.escape(s) for s in _SIGLAS_SEMENTES) + r")\d*\b",
                re.IGNORECASE
            )

            # Catálogo de híbridos de milho das principais empresas — pesquisado na
            # internet — para poder escolher a variedade mesmo que ela ainda não
            # esteja cadastrada no estoque (ex: comprou a semente mas ainda não
            # deu entrada no estoque, ou só quer simular o plantio).
            CATALOGO_SEMENTES_MILHO = [
                {"nome":"AG 1051",        "fab":"Agroceres"},
                {"nome":"AG 7098 PRO2",   "fab":"Agroceres"},
                {"nome":"AG 8065 PRO3",   "fab":"Agroceres"},
                {"nome":"AG 8600 PRO4",   "fab":"Agroceres"},
                {"nome":"AG 8606 VT PRO4","fab":"Agroceres"},
                {"nome":"AG 8701 VT PRO4","fab":"Agroceres"},
                {"nome":"AG 9045 PRO3",   "fab":"Agroceres"},
                {"nome":"AG 9070 PRO4",   "fab":"Agroceres"},
                {"nome":"AS 1633 PRO3",   "fab":"Agroeste"},
                {"nome":"AS 1666 PRO3",   "fab":"Agroeste"},
                {"nome":"AS 1730 PRO3",   "fab":"Agroeste"},
                {"nome":"AS 1735 PRO3",   "fab":"Agroeste"},
                {"nome":"AS 1757 PRO4",   "fab":"Agroeste"},
                {"nome":"AS 1770 PRO3",   "fab":"Agroeste"},
                {"nome":"AS 1780 PRO3",   "fab":"Agroeste"},
                {"nome":"AS 1844 PRO3",   "fab":"Agroeste"},
                {"nome":"AS 1900 PRO4",   "fab":"Agroeste"},
                {"nome":"AS 1955 PRO4",   "fab":"Agroeste"},
                {"nome":"P 3016",         "fab":"Corteva - Pioneer"},
                {"nome":"P 3898",         "fab":"Corteva - Pioneer"},
                {"nome":"30F53",          "fab":"Corteva - Pioneer"},
                {"nome":"B2401 PWU",      "fab":"Corteva - Brevant"},
                {"nome":"B2688 PWU",      "fab":"Corteva - Brevant"},
            ]
            _SEPARADOR_CATALOGO = "── 🌽 Catálogo de milho (não requer estoque) ──"

            # Selectbox com sementes do estoque + manual + catálogo de milho
            _sem_est = ["— digitar manualmente —"] + [
                i["Insumo"] for i in st.session_state.estoque
                if any(p in i.get("Categoria","").lower() or p in i.get("Insumo","").lower()
                       for p in ["semente","seed","milho","soja","trigo","aveia","feijão","canola","sorgo","arroz","híbrido","variedade","cultivar"])
                or _re_siglas.search(i.get("Insumo",""))
            ]
            if len(_sem_est) <= 1:
                _sem_est = ["— digitar manualmente —"] + [i["Insumo"] for i in st.session_state.estoque]
            _sem_est += [_SEPARADOR_CATALOGO] + [
                f"{p['nome']} — {p['fab']}" for p in CATALOGO_SEMENTES_MILHO
            ]

            # Form para adicionar variedade
            with st.form("form_add_variedade", clear_on_submit=True):
                _sv_c1, _sv_c2, _sv_c3 = st.columns(3)
                _sv_sel   = _sv_c1.selectbox("🔍 Variedade/Híbrido", _sem_est, key="sv_sel")
                _sv_man   = _sv_c1.text_input("Ou digite", placeholder="Ex: Brasmax Bônus IPRO", key="sv_man") if _sv_sel == "— digitar manualmente —" else ""
                _sv_invalido = _sv_sel in ("— digitar manualmente —", _SEPARADOR_CATALOGO)
                _sv_nome  = _sv_man if _sv_sel == "— digitar manualmente —" else ("" if _sv_sel == _SEPARADOR_CATALOGO else _sv_sel)
                _sv_ha    = _sv_c2.number_input("Hectares desta variedade", min_value=0.1, value=10.0, step=0.5, key="sv_ha")
                _sv_dose  = _sv_c2.number_input("Dose (kg/ha)", min_value=0.0, value=55.0, step=1.0, key="sv_dose")
                _sv_pop   = _sv_c3.number_input("População (pl/ha)", min_value=0, value=240000, step=5000, key="sv_pop")
                _sv_esp   = _sv_c3.number_input("Espaçamento (cm)", min_value=0.0, value=45.0, key="sv_esp")
                _sv_add   = st.form_submit_button("➕ Adicionar Variedade", use_container_width=True)
                if _sv_sel == _SEPARADOR_CATALOGO:
                    st.caption("⚠️ Isso é só um separador visual — selecione um híbrido da lista acima ou abaixo dele.")

            if _sv_add and _sv_nome and not _sv_invalido:
                st.session_state.pl_variedades.append({
                    "nome": _sv_nome, "ha": _sv_ha,
                    "dose": _sv_dose, "pop": _sv_pop,
                    "esp": _sv_esp,
                    "total_kg": round(_sv_dose * _sv_ha, 1),
                })
                st.rerun()

            # TSI compartilhado para todas as variedades
            _pl_tsi = st.text_area("TSI - Tratamento de sementes (todas as variedades)",
                placeholder="Ex: Maxim Advanced 200mL/sc + Fortenza 200mL/sc + Standak Top 200mL/sc",
                key="pl_txt_tsi", height=68)

            # Mostra variedades adicionadas
            if st.session_state.pl_variedades:
                st.markdown("**📋 Variedades adicionadas:**")
                _tot_ha_sem  = sum(v["ha"] for v in st.session_state.pl_variedades)
                _tot_kg_sem  = sum(v["total_kg"] for v in st.session_state.pl_variedades)
                for _vi, _v in enumerate(st.session_state.pl_variedades):
                    _vc1, _vc2 = st.columns([5,1])
                    _vc1.markdown(f"""
                    <div style='background:#14532d;border-radius:8px;padding:6px 12px;
                    border-left:3px solid #22c55e;margin:2px 0;font-size:12px;'>
                    <b style='color:#6ee7b7;'>{_v['nome']}</b>
                    <span style='color:#f1f5f9;'> · {_v['ha']} ha · {_v['dose']} kg/ha
                    → <b>{_v['total_kg']:,.0f} kg</b>
                    · {_v['pop']:,} pl/ha · {_v['esp']} cm</span>
                    </div>""", unsafe_allow_html=True)
                    if _vc2.button("🗑️", key=f"del_var_{_vi}"):
                        st.session_state.pl_variedades.pop(_vi)
                        st.rerun()

                st.markdown(f"""
                <div style='background:#0f2d4a;border-radius:8px;padding:8px 14px;
                border-left:3px solid #22c55e;margin:4px 0;'>
                <b style='color:#22c55e;'>📊 Total sementes:</b>
                <span style='color:#f1f5f9;'> {_tot_ha_sem:.1f} ha · {_tot_kg_sem:,.0f} kg total</span>
                </div>""", unsafe_allow_html=True)
            else:
                st.info("Adicione ao menos uma variedade acima.")

            # Compat: variáveis usadas abaixo (usa primeira variedade ou vazio)
            _pl_semente  = st.session_state.pl_variedades[0]["nome"] if st.session_state.pl_variedades else ""
            _pl_dose_sem = st.session_state.pl_variedades[0]["dose"] if st.session_state.pl_variedades else 0.0
            _pl_pop      = st.session_state.pl_variedades[0]["pop"]  if st.session_state.pl_variedades else 0
            _pl_espacamento = st.session_state.pl_variedades[0]["esp"] if st.session_state.pl_variedades else 45.0

            st.markdown("#### 🧪 Fertilizantes de Base (sulco e/ou lanço)")

            # Lista do estoque + opção manual
            _est_nomes = ["— digitar manualmente —"] + [i["Insumo"] for i in st.session_state.estoque]

            # ── ADUBOS DE BASE (acumulável — pode adicionar 2 ou mais, ex: Inrizza + Top Phos) ──
            if "pl_adubos" not in st.session_state:
                st.session_state.pl_adubos = []

            with st.form("form_add_adubo", clear_on_submit=True):
                _ad_c1, _ad_c2, _ad_c3, _ad_c4 = st.columns([3,1.5,1.5,1])
                _ad_sel  = _ad_c1.selectbox("🔍 Adubo de base (estoque)", _est_nomes, key="ad_sel")
                _ad_man  = _ad_c1.text_input("Ou digite o nome", placeholder="MAP, Inrizza, Top Phos...", key="ad_man") if _ad_sel == "— digitar manualmente —" else ""
                _ad_nome = _ad_man if _ad_sel == "— digitar manualmente —" else _ad_sel
                _ad_kg   = _ad_c2.number_input("Dose (kg/ha)", min_value=0.0, step=5.0, key="ad_kg")
                _ad_ha   = _ad_c3.number_input("Hectares", min_value=0.0, step=0.5,
                                               value=float(area_aplic or 0), key="ad_ha")
                _ad_add  = _ad_c4.form_submit_button("➕ Adicionar", use_container_width=True)

            if _ad_add and _ad_nome and _ad_nome != "— digitar manualmente —" and _ad_kg > 0 and _ad_ha > 0:
                st.session_state.pl_adubos.append({
                    "nome": _ad_nome, "kg_ha": _ad_kg, "ha": _ad_ha,
                    "total_kg": round(_ad_kg * _ad_ha, 1),
                })
                st.rerun()

            if st.session_state.pl_adubos:
                for _ai, _ad in enumerate(st.session_state.pl_adubos):
                    _adl1, _adl2 = st.columns([5,1])
                    _adl1.markdown(f"🟡 **{_ad['nome']}** — {_ad['kg_ha']} kg/ha × {_ad.get('ha', 0)} ha → Total: {_ad['total_kg']:,.0f} kg")
                    if _adl2.button("🗑️", key=f"del_adubo_{_ai}"):
                        st.session_state.pl_adubos.pop(_ai)
                        st.rerun()

            # Compatibilidade: 1º adubo da lista alimenta os campos legados
            _pl_adubo_nome = st.session_state.pl_adubos[0]["nome"] if st.session_state.pl_adubos else ""
            _pl_adubo_kg   = st.session_state.pl_adubos[0]["kg_ha"] if st.session_state.pl_adubos else 0.0

            # KCl
            _fl_c2, _ = st.columns(2)
            _pl_kcl_sel   = _fl_c2.selectbox("🔍 KCl / Potássio (estoque)", _est_nomes, key="pl_sel_kcl")
            _pl_kcl_man   = _fl_c2.text_input("Ou digite o nome", placeholder="KCl Mosaic, SulPoMag...", key="pl_txt_kcl") if _pl_kcl_sel == "— digitar manualmente —" else ""
            _pl_kcl_nome  = _pl_kcl_man if _pl_kcl_sel == "— digitar manualmente —" else _pl_kcl_sel
            _pl_kcl_kg    = _fl_c2.number_input("Dose KCl (kg/ha)", min_value=0.0, step=5.0, key="pl_num_kcl")

            # ── UREIA / N (acumulável — pode adicionar 2 ou mais aplicações) ──
            st.markdown("##### ⬜ Ureia / Nitrogênio (pode adicionar 2 ou mais aplicações)")
            if "pl_ureias" not in st.session_state:
                st.session_state.pl_ureias = []

            with st.form("form_add_ureia", clear_on_submit=True):
                _ur_c1, _ur_c2, _ur_c3, _ur_c4 = st.columns([3,1.5,1.5,1])
                _ur_sel  = _ur_c1.selectbox("🔍 Ureia / N (estoque)", _est_nomes, key="ur_sel")
                _ur_man  = _ur_c1.text_input("Ou digite o nome", placeholder="Ureia Yara, KAS...", key="ur_man") if _ur_sel == "— digitar manualmente —" else ""
                _ur_nome = _ur_man if _ur_sel == "— digitar manualmente —" else _ur_sel
                _ur_kg   = _ur_c2.number_input("Dose N (kg/ha)", min_value=0.0, step=5.0, key="ur_kg")
                _ur_ha   = _ur_c3.number_input("Hectares", min_value=0.0, step=0.5,
                                               value=float(area_aplic or 0), key="ur_ha")
                _ur_add  = _ur_c4.form_submit_button("➕ Adicionar", use_container_width=True)

            if _ur_add and _ur_nome and _ur_nome != "— digitar manualmente —" and _ur_kg > 0 and _ur_ha > 0:
                st.session_state.pl_ureias.append({
                    "nome": _ur_nome, "kg_ha": _ur_kg, "ha": _ur_ha,
                    "total_kg": round(_ur_kg * _ur_ha, 1),
                })
                st.rerun()

            if st.session_state.pl_ureias:
                for _ui, _ur in enumerate(st.session_state.pl_ureias):
                    _url1, _url2 = st.columns([5,1])
                    _url1.markdown(f"⬜ **{_ur['nome']}** — {_ur['kg_ha']} kg/ha × {_ur.get('ha', 0)} ha → Total: {_ur['total_kg']:,.0f} kg")
                    if _url2.button("🗑️", key=f"del_ureia_{_ui}"):
                        st.session_state.pl_ureias.pop(_ui)
                        st.rerun()

            # Compatibilidade: 1ª ureia da lista alimenta os campos legados
            _pl_ureia_nome = st.session_state.pl_ureias[0]["nome"] if st.session_state.pl_ureias else ""
            _pl_ureia_kg   = st.session_state.pl_ureias[0]["kg_ha"] if st.session_state.pl_ureias else 0.0

            st.markdown("#### 🦠 Inoculantes no Sulco")
            _in_c1, _in_c2, _in_c3 = st.columns(3)

            _pl_inoc1_sel  = _in_c1.selectbox("🔍 Inoculante 1 (estoque)", _est_nomes, key="pl_sel_inoc1")
            _pl_inoc1_man  = _in_c1.text_input("Ou digite", placeholder="Nitragin Gold...", key="pl_txt_inoc1") if _pl_inoc1_sel == "— digitar manualmente —" else ""
            _pl_inoc1_nome = _pl_inoc1_man if _pl_inoc1_sel == "— digitar manualmente —" else _pl_inoc1_sel
            _pl_inoc1_dose = _in_c1.number_input("Dose inoc 1 (mL/ha)", min_value=0.0, key="pl_num_inoc1")

            _pl_inoc2_sel  = _in_c2.selectbox("🔍 Co-inoculante (estoque)", _est_nomes, key="pl_sel_inoc2")
            _pl_inoc2_man  = _in_c2.text_input("Ou digite", placeholder="Azospirillum...", key="pl_txt_inoc2") if _pl_inoc2_sel == "— digitar manualmente —" else ""
            _pl_inoc2_nome = _pl_inoc2_man if _pl_inoc2_sel == "— digitar manualmente —" else _pl_inoc2_sel
            _pl_inoc2_dose = _in_c2.number_input("Dose co-inoc (mL/ha)", min_value=0.0, key="pl_num_inoc2")

            _pl_inoc3_sel  = _in_c3.selectbox("🔍 Inoc. semente (estoque)", _est_nomes, key="pl_sel_inoc3")
            _pl_inoc3_man  = _in_c3.text_input("Ou digite", placeholder="Bradyrhizobium...", key="pl_txt_inoc3") if _pl_inoc3_sel == "— digitar manualmente —" else ""
            _pl_inoc3_nome = _pl_inoc3_man if _pl_inoc3_sel == "— digitar manualmente —" else _pl_inoc3_sel
            _pl_inoc3_dose = _in_c3.number_input("Dose inoc semente (mL/sc)", min_value=0.0, key="pl_num_inoc3")

            st.markdown("#### 🌿 Micronutrientes e Outros no Sulco")
            _mn_c1, _mn_c2 = st.columns(2)

            _pl_micro1_sel  = _mn_c1.selectbox("🔍 Micronutriente 1 (estoque)", _est_nomes, key="pl_sel_micro1")
            _pl_micro1_man  = _mn_c1.text_input("Ou digite", placeholder="Boro Quelatado, Zinco...", key="pl_txt_micro1") if _pl_micro1_sel == "— digitar manualmente —" else ""
            _pl_micro1_nome = _pl_micro1_man if _pl_micro1_sel == "— digitar manualmente —" else _pl_micro1_sel
            _pl_micro1_dose = _mn_c1.number_input("Dose micro 1 (kg/L ha)", min_value=0.0, step=0.1, key="pl_num_micro1")

            _pl_micro2_sel  = _mn_c2.selectbox("🔍 Micronutriente 2 (estoque)", _est_nomes, key="pl_sel_micro2")
            _pl_micro2_man  = _mn_c2.text_input("Ou digite", placeholder="MicroEssentials SZ...", key="pl_txt_micro2") if _pl_micro2_sel == "— digitar manualmente —" else ""
            _pl_micro2_nome = _pl_micro2_man if _pl_micro2_sel == "— digitar manualmente —" else _pl_micro2_sel
            _pl_micro2_dose = _mn_c2.number_input("Dose micro 2 (kg/L ha)", min_value=0.0, step=0.1, key="pl_num_micro2")

            # Mostra totais por ha e área
            _total_adubos_kg = sum(a.get("total_kg",0) for a in st.session_state.get("pl_adubos", []))
            _total_ureias_kg = sum(u.get("total_kg",0) for u in st.session_state.get("pl_ureias", []))
            if area_aplic > 0 and (_total_adubos_kg + _total_ureias_kg + _pl_kcl_kg) > 0:
                st.markdown("---")
                st.markdown("**📊 Totais para a área informada:**")
                _t1, _t2, _t3, _t4 = st.columns(4)
                if _total_adubos_kg > 0:
                    _n_adubos = len(st.session_state.get("pl_adubos", []))
                    _t1.metric(f"🟡 Adubos ({_n_adubos})" if _n_adubos > 1 else f"🟡 {_pl_adubo_nome or 'Adubo'}",
                               f"{_total_adubos_kg:,.0f} kg",
                               f"{_n_adubos} item(ns)")
                if _pl_kcl_kg > 0:
                    _t2.metric(f"🟣 {_pl_kcl_nome or 'KCl'}",
                               f"{_pl_kcl_kg * area_aplic:,.0f} kg",
                               f"{_pl_kcl_kg} kg/ha")
                if _total_ureias_kg > 0:
                    _n_ureias = len(st.session_state.get("pl_ureias", []))
                    _t3.metric(f"⬜ Ureia/N ({_n_ureias})" if _n_ureias > 1 else f"⬜ {_pl_ureia_nome or 'Ureia'}",
                               f"{_total_ureias_kg:,.0f} kg",
                               f"{_n_ureias} aplicação(ões)")
                if _pl_dose_sem > 0:
                    _t4.metric("🌱 Semente",
                               f"{_pl_dose_sem * area_aplic:,.0f} kg",
                               f"{_pl_dose_sem} kg/ha")

            # ── BOTÃO SALVAR PLANTIO DIRETO ──────────────────────────────────
            st.markdown("---")
            if st.button("💾 Salvar Aplicação de Plantio no Cronograma",
                         key="btn_salvar_plantio_direto",
                         use_container_width=True, type="primary"):
                _dp = {
                    "semente": _pl_semente, "dose_sem_ha": _pl_dose_sem,
                    "populacao": _pl_pop, "tsi": _pl_tsi,
                    "espacamento": _pl_espacamento,
                    "variedades": st.session_state.get("pl_variedades", []),
                    "adubo_nome": _pl_adubo_nome, "adubo_kg_ha": _pl_adubo_kg,
                    "adubos": [dict(a) for a in st.session_state.get("pl_adubos", [])],
                    "kcl_nome": _pl_kcl_nome, "kcl_kg_ha": _pl_kcl_kg,
                    "ureia_nome": _pl_ureia_nome, "ureia_kg_ha": _pl_ureia_kg,
                    "ureias": [dict(u) for u in st.session_state.get("pl_ureias", [])],
                    "inoc1_nome": _pl_inoc1_nome, "inoc1_dose": _pl_inoc1_dose,
                    "inoc2_nome": _pl_inoc2_nome, "inoc2_dose": _pl_inoc2_dose,
                    "inoc3_nome": _pl_inoc3_nome, "inoc3_dose": _pl_inoc3_dose,
                    "micro1_nome": _pl_micro1_nome, "micro1_dose": _pl_micro1_dose,
                    "micro2_nome": _pl_micro2_nome, "micro2_dose": _pl_micro2_dose,
                    "adubo_total_kg": round(_pl_adubo_kg * area_aplic, 1),
                    "kcl_total_kg": round(_pl_kcl_kg * area_aplic, 1),
                    "ureia_total_kg": round(_pl_ureia_kg * area_aplic, 1),
                    "semente_total_kg": round(_pl_dose_sem * area_aplic, 1),
                }
                st.session_state.aplicacoes.append({
                    "ID Área":             st.session_state.dados.get("id_area",""),
                    "Cultura":             st.session_state.get("aplic_cultura_ativa",""),
                    "Hectares Cultura":    st.session_state.get("aplic_ha_ativo", area_aplic),
                    "Estádio":             "🚜 Plantio",
                    "Aplicação":           "🚜 Plantio",
                    "Data":                str(data_aplic),
                    "Área aplicada ha":    area_aplic,
                    "Volume calda L/ha":   0,
                    "Capacidade tanque L": 0,
                    "Área por tanque ha":  0,
                    "Número tanques":      0,
                    "Operador":            "",
                    "Pulverizador":        "",
                    "Velocidade km/h":     0,
                    "Pressão bar":         0,
                    "Clima aplicação":     "",
                    "Produtos":            [],
                    "Dados Plantio":       _dp,
                    "Status":              "pendente",
                })
                salvar_dados_iaagro()
                st.session_state.pl_variedades = []
                st.session_state.pl_adubos = []
                st.session_state.pl_ureias = []
                success_box(f"✅ Plantio salvo no cronograma da {st.session_state.get('aplic_cultura_ativa','cultura')}!")
                st.rerun()

        st.subheader("🧪 Produtos da Aplicação" if not _is_plantio else "🧪 Defensivos e Outros Produtos")
        _nomes_estoque = [item["Insumo"] for item in st.session_state.estoque]
        n_produtos = int(st.number_input("Quantidade de produtos", min_value=1, max_value=10, value=1, step=1, key="num_qtd_produtos_aplic"))

        def _conv_unid_base(q, u):
            """Converte mL→L e g→kg pra bater com a unidade do preço no estoque (R$/L ou R$/kg)."""
            u = (u or "").lower().replace(" ", "")
            base = u.split("/")[0]  # "ml/ha"->"ml"  "kg/ha"->"kg"  "g/ha"->"g"
            if base == "ml": return q/1000
            if base == "g":  return q/1000
            if base == "mg": return q/1_000_000
            return q

        produtos_aplic = []
        _custo_total_aplic = 0.0
        # Opção de digitar um produto que não está no estoque
        _opcoes_prod = _nomes_estoque + ["✏️ Outro (digitar manualmente)"]
        for i in range(n_produtos):
            st.markdown(f"**Produto {i+1}**")
            col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns([3,2,1,1,2])
            _prod_sel = col_p1.selectbox("Produto", _opcoes_prod, key=f"sel_prod_aplic_{i}")
            if _prod_sel == "✏️ Outro (digitar manualmente)":
                _prod = col_p1.text_input("Digite o nome do produto", key=f"txt_prod_manual_{i}",
                                          placeholder="Ex: HERB. PAXEO 880GR")
            else:
                _prod = _prod_sel
            _tipo_p= col_p2.selectbox("Tipo",       TIPOS_PRODUTO,  key=f"sel_tipo_prod_{i}")
            _dose  = col_p3.number_input("Dose/ha", min_value=0.0,  key=f"num_dose_aplic_{i}")
            _unid  = col_p4.selectbox("Un.", ["L/ha","mL/ha","kg/ha","g/ha"], key=f"sel_unid_aplic_{i}")
            _obs_p = col_p5.text_input("Obs.", key=f"txt_obs_prod_{i}")
            _por_tanque = round(_dose * area_por_tanque, 3)
            _total_prod = round(_dose * area_aplic, 3)

            # Busca o preço unitário desse produto no estoque, já convertido pra R$/kg ou R$/L
            _item_estq   = next((e for e in st.session_state.estoque if e.get("Insumo") == _prod), None)
            _preco_unit, _base_unit, _aviso_preco = preco_por_kg_ou_l(_item_estq)
            _qtd_base    = _conv_unid_base(_total_prod, _unid)
            _custo_prod  = round(_qtd_base * _preco_unit, 2)
            _custo_total_aplic += _custo_prod

            if _dose > 0:
                st.caption(
                    f"  → {_por_tanque} {_unid.replace('/ha','')} por tanque | "
                    f"Total: {_total_prod} {_unid.replace('/ha','')}  |  "
                    f"💲 R$ {_preco_unit:.2f}/{_base_unit}  →  "
                    f"**Custo: R$ {_custo_prod:,.2f}**"
                )
                if _preco_unit == 0 and not _aviso_preco:
                    st.caption("⚠️ Esse produto não tem preço cadastrado no estoque — custo ficará R$ 0,00. Cadastre o preço no Estoque de Insumos pra aparecer aqui.")
                if _aviso_preco:
                    st.caption(_aviso_preco)

            produtos_aplic.append({
                "Produto": _prod, "Tipo": _tipo_p, "Dose por ha": _dose, "Unidade": _unid,
                "Produto por tanque": _por_tanque, "Total usado": _total_prod, "Observação": _obs_p,
                "Preço Unitário R$": _preco_unit, "Custo Total R$": _custo_prod,
            })

        if n_produtos > 0 and any(p["Dose por ha"] > 0 for p in produtos_aplic):
            st.markdown(f"""
            <div style='background:#14532d;border-radius:8px;padding:8px 14px;margin:6px 0;'>
            <span style='color:#6ee7b7;font-size:13px;font-weight:700;'>
            💰 Custo total desta aplicação: R$ {_custo_total_aplic:,.2f}
            </span></div>""", unsafe_allow_html=True)

        if st.button("💾 Salvar Aplicação", key="salvar_aplicacao_modelada", use_container_width=True):
            erro = False
            if not nome_aplic.strip(): error_box("Informe o nome da aplicação."); erro = True
            if area_aplic <= 0:        error_box("Informe a área aplicada."); erro = True
            for p in produtos_aplic:
                if p["Dose por ha"] <= 0: error_box(f"Dose zero: {p['Produto']}."); erro = True
            if not erro:
                _dados_plantio = {}
                if _is_plantio:
                    _dados_plantio = {
                        "semente":      _pl_semente,    "dose_sem_ha": _pl_dose_sem,
                        "populacao":    _pl_pop,         "tsi":         _pl_tsi,
                        "espacamento":  _pl_espacamento,
                        "variedades":   st.session_state.get("pl_variedades", []),
                        "adubo_nome":   _pl_adubo_nome, "adubo_kg_ha": _pl_adubo_kg,
                        "adubos": [dict(a) for a in st.session_state.get("pl_adubos", [])],
                        "kcl_nome":     _pl_kcl_nome,   "kcl_kg_ha":   _pl_kcl_kg,
                        "ureia_nome":   _pl_ureia_nome, "ureia_kg_ha": _pl_ureia_kg,
                        "ureias": [dict(u) for u in st.session_state.get("pl_ureias", [])],
                        "inoc1_nome":   _pl_inoc1_nome, "inoc1_dose":  _pl_inoc1_dose,
                        "inoc2_nome":   _pl_inoc2_nome, "inoc2_dose":  _pl_inoc2_dose,
                        "inoc3_nome":   _pl_inoc3_nome, "inoc3_dose":  _pl_inoc3_dose,
                        "micro1_nome":  _pl_micro1_nome,"micro1_dose": _pl_micro1_dose,
                        "micro2_nome":  _pl_micro2_nome,"micro2_dose": _pl_micro2_dose,
                        "adubo_total_kg":  round(_pl_adubo_kg * area_aplic, 1),
                        "kcl_total_kg":    round(_pl_kcl_kg * area_aplic, 1),
                        "ureia_total_kg":  round(_pl_ureia_kg * area_aplic, 1),
                        "semente_total_kg":round(_pl_dose_sem * area_aplic, 1),
                    }
                st.session_state.aplicacoes.append({
                    "ID Área":             st.session_state.dados.get("id_area",""),
                    "Cultura":             st.session_state.get("aplic_cultura_ativa",""),
                    "Hectares Cultura":    st.session_state.get("aplic_ha_ativo",0),
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
                    "Dados Plantio":       _dados_plantio,
                    "Status":              "pendente",
                })
                atualizar_area_atual()
                salvar_dados_iaagro()
                if _is_plantio:
                    st.session_state.pl_variedades = []
                    st.session_state.pl_adubos = []
                    st.session_state.pl_ureias = []
                success_box(f"✅ {nome_aplic} salva! {len(produtos_aplic)} produto(s).")
                st.rerun()

        # PDF
        st.divider()
        st.subheader("📋 Histórico de Aplicações")
        if st.session_state.aplicacoes:
            # ── Filtro por cultura para o PDF ──
            # Lista de culturas presentes nas aplicações
            _culturas_disp = list(dict.fromkeys(
                a.get("Cultura","") for a in st.session_state.aplicacoes if a.get("Cultura","")
            ))
            _opcoes_cult_pdf = ["Todas as culturas"] + _culturas_disp

            st.markdown("**Filtrar por cultura para imprimir:**")
            _cult_escolhida = st.selectbox(
                "Cultura",
                _opcoes_cult_pdf,
                key="sel_cult_pdf_aplic",
                label_visibility="collapsed"
            )

            if _cult_escolhida == "Todas as culturas":
                _aplic_pdf = list(st.session_state.aplicacoes)
                _cult_pdf = ""
            else:
                _aplic_pdf = [a for a in st.session_state.aplicacoes
                              if a.get("Cultura","") == _cult_escolhida]
                _cult_pdf = _cult_escolhida
            st.caption(f"✅ {len(_aplic_pdf)} aplicação(ões) nesta seleção.")

            _pc_pdf1, _pc_pdf2 = st.columns(2)
            if _pc_pdf1.button(
                f"📄 Gerar PDF ({len(_aplic_pdf)} aplicação(ões))",
                key="btn_gerar_pdf_aplic", use_container_width=True, type="primary"):
                if not _aplic_pdf:
                    st.warning("⚠️ Não há aplicações para essa cultura.")
                else:
                    try:
                        _d = st.session_state.dados
                        _cult_nome = _cult_pdf.split(" ",1)[-1] if _cult_pdf else cultura_limpa(_d.get("cultura",""))
                        _ha_pdf = st.session_state.get("aplic_ha_ativo", _d.get("area",0))
                        _pdf_bytes = gerar_pdf_programacao_aplicacoes(
                            aplicacoes = _aplic_pdf,
                            fazenda    = _d.get("fazenda",""),
                            talhao     = _d.get("talhao",""),
                            cultura    = _cult_nome,
                            area_ha    = _ha_pdf,
                            operador   = _d.get("operador",""),
                        )
                        st.session_state["_pdf_aplic"] = _pdf_bytes
                        st.success(f"✅ PDF gerado! {len(_aplic_pdf)} aplicação(ões).")
                    except Exception as e:
                        st.error(f"Erro ao gerar PDF: {e}")

            if _pc_pdf2.button("🔄 Nova Cultura / Limpar seleção",
                               key="btn_pdf_nova_cultura", use_container_width=True):
                st.session_state.aplic_cultura_ativa = None
                st.session_state.aplic_ha_ativo      = 0.0
                st.rerun()

            if st.session_state.get("_pdf_aplic"):
                _nome_pdf = (_cult_pdf.split(" ",1)[-1].replace(" ","_") if _cult_pdf else "todas_culturas")
                st.download_button(
                    label="⬇️ Baixar PDF",
                    data=st.session_state["_pdf_aplic"],
                    file_name=f"programacao_{_nome_pdf}_{datetime.now().strftime('%d%m%Y')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="btn_download_pdf_aplic"
                )

        if len(st.session_state.aplicacoes) == 0:
            info_box("Nenhuma aplicação registrada ainda.")
        else:
            _ordem = {"🚜 Plantio":0,"🌱 Pré-plantio":1,"🌿 Pós-plantio / V0":2,"🌾 V1 – V3":3,
                      "🌾 V4 – V6":4,"🌾 V7 – VT":5,"🌸 R1 – R2 (Floração)":6,
                      "🫘 R3 – R4 (Granação)":7,"🫘 R5 – R6":8,"🌾 Pré-colheita":9}

            # Filtro por cultura no histórico
            _culturas_hist = list(dict.fromkeys(
                a.get("Cultura","Sem cultura") for a in st.session_state.aplicacoes))
            _fil_cult_hist = st.selectbox("🔍 Filtrar por cultura",
                ["Todas"] + _culturas_hist, key="sel_fil_cult_hist")

            _aplic_filtradas = st.session_state.aplicacoes if _fil_cult_hist == "Todas" else [
                a for a in st.session_state.aplicacoes
                if a.get("Cultura","Sem cultura") == _fil_cult_hist]

            aplicacoes_ordenadas = sorted(_aplic_filtradas,
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

                    # ── DADOS DE PLANTIO ─────────────────────────────────────
                    _dp_view = aplic.get("Dados Plantio", {})
                    if _dp_view:
                        st.markdown("---")
                        st.markdown("**🚜 Dados de Plantio:**")
                        _dv1, _dv2, _dv3 = st.columns(3)

                        # Semente
                        # Múltiplas variedades
                        _vars_view = _dp_view.get("variedades", [])
                        if _vars_view:
                            _tot_ha_v = sum(v["ha"] for v in _vars_view)
                            _tot_kg_v = sum(v["total_kg"] for v in _vars_view)
                            _linhas_v = "".join([
                                f"<span style='color:#f1f5f9;font-size:11px;'>"
                                f"<b style='color:#6ee7b7;'>{v['nome']}</b> · "
                                f"{v['ha']} ha · {v['dose']} kg/ha → {v['total_kg']:,.0f} kg</span><br>"
                                for v in _vars_view
                            ])
                            _tsi_v = f"<br><span style='color:#fbbf24;font-size:11px;'>TSI: {_dp_view.get('tsi','')}</span>" if _dp_view.get('tsi') else ""
                            _dv1.markdown(f"""
                            <div style='background:#14532d;border-radius:8px;padding:8px 12px;margin:2px 0;'>
                            <b style='color:#6ee7b7;font-size:12px;'>🌱 SEMENTES ({len(_vars_view)} variedades)</b><br>
                            {_linhas_v}
                            <span style='color:#22c55e;font-size:11px;font-weight:700;'>
                            Total: {_tot_ha_v:.1f} ha · {_tot_kg_v:,.0f} kg</span>
                            {_tsi_v}
                            </div>""", unsafe_allow_html=True)
                        elif _dp_view.get("semente") or _dp_view.get("dose_sem_ha",0) > 0:
                            _dv1.markdown(f"""
                            <div style='background:#14532d;border-radius:8px;padding:8px 12px;margin:2px 0;'>
                            <b style='color:#6ee7b7;font-size:12px;'>🌱 SEMENTE</b><br>
                            <span style='color:#f1f5f9;font-size:13px;'>{_dp_view.get('semente','—')}</span><br>
                            <span style='color:#94a3b8;font-size:11px;'>
                            {_dp_view.get('dose_sem_ha',0)} kg/ha · Total: {_dp_view.get('semente_total_kg',0):,.0f} kg<br>
                            Pop: {_dp_view.get('populacao',0):,} pl/ha · Esp: {_dp_view.get('espacamento',0)} cm
                            </span>
                            {f"<br><span style='color:#fbbf24;font-size:11px;'>TSI: {_dp_view.get('tsi','')}</span>" if _dp_view.get('tsi') else ""}
                            </div>""", unsafe_allow_html=True)

                        # Fertilizantes
                        _ferts = []
                        _adubos_view = _dp_view.get("adubos") or (
                            [{"nome": _dp_view["adubo_nome"], "kg_ha": _dp_view.get("adubo_kg_ha",0),
                              "total_kg": _dp_view.get("adubo_total_kg",0)}]
                            if _dp_view.get("adubo_nome") and _dp_view.get("adubo_kg_ha",0) > 0 else []
                        )
                        for _adbv in _adubos_view:
                            _ha_txt = f" × {_adbv.get('ha',0)} ha" if _adbv.get("ha",0) else ""
                            _ferts.append(f"🟡 **{_adbv.get('nome','')}** — {_adbv.get('kg_ha',0)} kg/ha{_ha_txt} (Total: {_adbv.get('total_kg',0):,.0f} kg)")
                        if _dp_view.get("kcl_nome") and _dp_view.get("kcl_kg_ha",0) > 0:
                            _ferts.append(f"🟣 **{_dp_view['kcl_nome']}** — {_dp_view['kcl_kg_ha']} kg/ha (Total: {_dp_view.get('kcl_total_kg',0):,.0f} kg)")
                        _ureias_view = _dp_view.get("ureias") or (
                            [{"nome": _dp_view["ureia_nome"], "kg_ha": _dp_view.get("ureia_kg_ha",0),
                              "total_kg": _dp_view.get("ureia_total_kg",0)}]
                            if _dp_view.get("ureia_nome") and _dp_view.get("ureia_kg_ha",0) > 0 else []
                        )
                        for _urbv in _ureias_view:
                            _ha_txt = f" × {_urbv.get('ha',0)} ha" if _urbv.get("ha",0) else ""
                            _ferts.append(f"⬜ **{_urbv.get('nome','')}** — {_urbv.get('kg_ha',0)} kg/ha{_ha_txt} (Total: {_urbv.get('total_kg',0):,.0f} kg)")
                        if _ferts:
                            _dv2.markdown(f"""
                            <div style='background:#1e3a5f;border-radius:8px;padding:8px 12px;margin:2px 0;'>
                            <b style='color:#38bdf8;font-size:12px;'>🧪 FERTILIZANTES</b><br>
                            {"<br>".join([f"<span style='color:#f1f5f9;font-size:11px;'>{f}</span>" for f in _ferts])}
                            </div>""", unsafe_allow_html=True)

                        # Inoculantes e micros
                        _inocs = []
                        if _dp_view.get("inoc1_nome") and _dp_view.get("inoc1_dose",0) > 0:
                            _inocs.append(f"🦠 {_dp_view['inoc1_nome']} — {_dp_view['inoc1_dose']} mL/ha")
                        if _dp_view.get("inoc2_nome") and _dp_view.get("inoc2_dose",0) > 0:
                            _inocs.append(f"🦠 {_dp_view['inoc2_nome']} — {_dp_view['inoc2_dose']} mL/ha")
                        if _dp_view.get("inoc3_nome") and _dp_view.get("inoc3_dose",0) > 0:
                            _inocs.append(f"💉 {_dp_view['inoc3_nome']} — {_dp_view['inoc3_dose']} mL/sc")
                        if _dp_view.get("micro1_nome") and _dp_view.get("micro1_dose",0) > 0:
                            _inocs.append(f"🌿 {_dp_view['micro1_nome']} — {_dp_view['micro1_dose']} kg/ha")
                        if _dp_view.get("micro2_nome") and _dp_view.get("micro2_dose",0) > 0:
                            _inocs.append(f"🌿 {_dp_view['micro2_nome']} — {_dp_view['micro2_dose']} kg/ha")
                        if _inocs:
                            _dv3.markdown(f"""
                            <div style='background:#064e3b;border-radius:8px;padding:8px 12px;margin:2px 0;'>
                            <b style='color:#34d399;font-size:12px;'>🦠 INOCULANTES / MICROS</b><br>
                            {"<br>".join([f"<span style='color:#f1f5f9;font-size:11px;'>{i}</span>" for i in _inocs])}
                            </div>""", unsafe_allow_html=True)

                    st.markdown("**🧪 Produtos:**")
                    _custo_total_hist = 0.0
                    for p in aplic.get("Produtos",[]):
                        unid = p.get("Unidade","").replace("/ha","")
                        # Sempre recalcula com o preço ATUAL do estoque (não confia em valor
                        # gravado antigo, que pode ter sido salvo com o bug de sc/un).
                        _item_hist = next((e for e in st.session_state.estoque
                                            if e.get("Insumo") == p.get("Produto","")), None)
                        _preco_hist, _base_hist, _aviso_hist = preco_por_kg_ou_l(_item_hist)
                        _u_low = (p.get("Unidade","") or "").lower().replace(" ", "")
                        _base_dose = _u_low.split("/")[0]
                        if _base_dose == "ml":  _qtd_b = p.get("Total usado",0)/1000
                        elif _base_dose == "g": _qtd_b = p.get("Total usado",0)/1000
                        elif _base_dose == "mg":_qtd_b = p.get("Total usado",0)/1_000_000
                        else:                   _qtd_b = p.get("Total usado",0)
                        _custo_hist = round(_qtd_b * _preco_hist, 2)
                        _custo_total_hist += _custo_hist
                        st.markdown(f"- **{p.get('Produto','')}** ({p.get('Tipo','')}) — "
                                    f"{p.get('Dose por ha',0)} {p.get('Unidade','')} | "
                                    f"Total: {p.get('Total usado',0)} {unid} | "
                                    f"💲 R$ {_preco_hist:.2f}/{_base_hist} | "
                                    f"**Custo: R$ {_custo_hist:,.2f}**")
                        if _aviso_hist:
                            st.caption(_aviso_hist)
                    if aplic.get("Produtos"):
                        st.markdown(f"<span style='color:#6ee7b7;font-size:12px;font-weight:700;'>"
                                     f"💰 Custo total dos produtos: R$ {_custo_total_hist:,.2f}</span>",
                                     unsafe_allow_html=True)
                    if not aplic.get("Produtos") and not _dp_view:
                        st.info("Nenhum produto registrado.")
                    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
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
                            f"{_pp.get('Unidade','')} | Total: {_pp.get('Total usado',0)} | "
                            f"R$ unit: {_pp.get('Preço Unitário R$',0):.2f} | "
                            f"Custo: R$ {_pp.get('Custo Total R$',0):,.2f}")
                    if aplic.get("Produtos"):
                        _linhas_exp.append(f"  TOTAL PRODUTOS: R$ {sum(p.get('Custo Total R$',0) for p in aplic.get('Produtos',[])):,.2f}")
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

                    # ── EDITAR APLICAÇÃO ─────────────────────────────────────
                    _edit_key = f"edit_mode_aplic_{idx_a}"
                    if _edit_key not in st.session_state:
                        st.session_state[_edit_key] = False
                    if col_b4.button("✖️ Fechar edição" if st.session_state[_edit_key] else "✏️ Editar",
                                      key=f"btn_toggle_edit_{idx_a}", use_container_width=True):
                        st.session_state[_edit_key] = not st.session_state[_edit_key]
                        st.rerun()

                    if st.session_state[_edit_key]:
                        st.markdown("---")
                        st.markdown("**✏️ Editar Aplicação**")

                        # ── REMOVER PRODUTO INDIVIDUAL (fora do form, botões diretos) ──
                        _prods_atuais = aplic.get("Produtos", [])
                        if _prods_atuais:
                            st.markdown("**🧪 Produtos desta aplicação** — clique em 🗑️ para remover:")
                            for _pi, _p in enumerate(list(_prods_atuais)):
                                _rc1, _rc2 = st.columns([5, 1])
                                _rc1.markdown(
                                    f"<div style='padding:6px 0;color:#cbd5e1;font-size:13px;'>"
                                    f"<b>{_p.get('Produto','—')}</b> — "
                                    f"{_p.get('Dose por ha',0)} {_p.get('Unidade','')}"
                                    f"</div>", unsafe_allow_html=True)
                                if _rc2.button("🗑️", key=f"btn_del_prod_{idx_a}_{_pi}",
                                               help="Remover este produto"):
                                    # Remove pelo objeto real (aplic é o mesmo dict de session_state)
                                    _lista_real = aplic.get("Produtos", [])
                                    if 0 <= _pi < len(_lista_real):
                                        _removido = _lista_real.pop(_pi)  # muta a lista in-place
                                        aplic["Produtos"] = _lista_real
                                        # Reflete na área ativa também (as aplicações vivem lá dentro)
                                        _idw = st.session_state.dados.get("id_area")
                                        if _idw:
                                            for _ar in st.session_state.areas:
                                                if _ar.get("ID") == _idw:
                                                    _ar["Aplicacoes"] = list(st.session_state.aplicacoes)
                                                    break
                                        salvar_dados_iaagro()
                                        success_box(f"✅ Produto removido: {_removido.get('Produto','')}")
                                        st.rerun()
                            st.markdown("---")

                        with st.form(key=f"form_edit_aplic_{idx_a}"):
                            _e1, _e2, _e3 = st.columns(3)
                            _edt_data     = _e1.text_input("Data (dd/mm/aaaa)", value=aplic.get("Data",""), key=f"edt_data_{idx_a}")
                            _edt_estadio  = _e2.text_input("Estádio/Nome da aplicação",
                                value=aplic.get("Estádio", aplic.get("Aplicação","")), key=f"edt_estadio_{idx_a}")
                            _edt_operador = _e3.text_input("Operador", value=aplic.get("Operador",""), key=f"edt_operador_{idx_a}")

                            _e4, _e5, _e6 = st.columns(3)
                            _edt_pulv  = _e4.text_input("Pulverizador", value=aplic.get("Pulverizador",""), key=f"edt_pulv_{idx_a}")
                            _edt_area  = _e5.number_input("Área aplicada (ha)", min_value=0.0,
                                value=float(aplic.get("Área aplicada ha",0) or 0), key=f"edt_area_{idx_a}")
                            _edt_calda = _e6.number_input("Volume calda (L/ha)", min_value=0.0,
                                value=float(aplic.get("Volume calda L/ha",0) or 0), key=f"edt_calda_{idx_a}")

                            _edt_clima = st.text_input("Clima na aplicação", value=aplic.get("Clima aplicação",""), key=f"edt_clima_{idx_a}")

                            # Produtos — edição dos valores (a remoção fica nos botões acima)
                            _produtos_orig = aplic.get("Produtos",[])
                            _edt_produtos = []
                            if _produtos_orig:
                                st.markdown("**🧪 Editar valores dos produtos:**")
                                for _pi, _p in enumerate(_produtos_orig):
                                    _pc1, _pc2, _pc3, _pc4 = st.columns([2,1,1,1])
                                    _p_nome = _pc1.text_input("Produto", value=_p.get("Produto",""),
                                        key=f"edt_prod_nome_{idx_a}_{_pi}")
                                    _p_dose = _pc2.number_input("Dose/ha", min_value=0.0,
                                        value=float(_p.get("Dose por ha",0) or 0), key=f"edt_prod_dose_{idx_a}_{_pi}")
                                    _p_unid = _pc3.text_input("Unidade", value=_p.get("Unidade",""),
                                        key=f"edt_prod_unid_{idx_a}_{_pi}")
                                    _p_preco = _pc4.number_input("R$ unit.", min_value=0.0,
                                        value=float(_p.get("Preço Unitário R$",0) or 0), key=f"edt_prod_preco_{idx_a}_{_pi}")
                                    _p_total_novo = round(_p_dose * _edt_area, 3)
                                    _u_low = (_p_unid or "").lower()
                                    _p_qtd_base = _p_total_novo/1000 if ("ml" in _u_low or _u_low in ("g","g/ha")) else _p_total_novo
                                    _edt_produtos.append({
                                        **_p,
                                        "Produto": _p_nome, "Dose por ha": _p_dose, "Unidade": _p_unid,
                                        "Total usado": _p_total_novo,
                                        "Preço Unitário R$": _p_preco,
                                        "Custo Total R$": round(_p_qtd_base * _p_preco, 2),
                                    })

                            # Variedades de sementes (plantio)
                            _vars_orig = aplic.get("Dados Plantio", {}).get("variedades", [])
                            _edt_variedades = []
                            if _vars_orig:
                                st.markdown("**🌱 Variedades de sementes:**")
                                for _vi, _v in enumerate(_vars_orig):
                                    _vc1, _vc2, _vc3, _vc4 = st.columns([2,1,1,1])
                                    _v_nome = _vc1.text_input("Variedade", value=_v.get("nome",""),
                                        key=f"edt_var_nome_{idx_a}_{_vi}")
                                    _v_ha   = _vc2.number_input("Ha", min_value=0.0,
                                        value=float(_v.get("ha",0) or 0), key=f"edt_var_ha_{idx_a}_{_vi}")
                                    _v_dose = _vc3.number_input("Dose kg/ha", min_value=0.0,
                                        value=float(_v.get("dose",0) or 0), key=f"edt_var_dose_{idx_a}_{_vi}")
                                    _v_pop  = _vc4.number_input("Pop pl/ha", min_value=0,
                                        value=int(_v.get("pop",0) or 0), key=f"edt_var_pop_{idx_a}_{_vi}")
                                    _edt_variedades.append({
                                        **_v,
                                        "nome": _v_nome, "ha": _v_ha, "dose": _v_dose, "pop": _v_pop,
                                        "total_kg": round(_v_dose * _v_ha, 1),
                                    })

                            _salvar_edicao = st.form_submit_button("💾 Salvar edição", type="primary", use_container_width=True)
                            if _salvar_edicao:
                                _idx_orig = next((i for i,a in enumerate(st.session_state.aplicacoes)
                                                 if a.get("Data") == aplic.get("Data") and
                                                 a.get("Aplicação") == aplic.get("Aplicação")), None)
                                if _idx_orig is not None:
                                    _reg = st.session_state.aplicacoes[_idx_orig]
                                    _reg["Data"]              = _edt_data
                                    _reg["Estádio"]           = _edt_estadio
                                    _reg["Aplicação"]         = _edt_estadio
                                    _reg["Operador"]          = _edt_operador
                                    _reg["Pulverizador"]      = _edt_pulv
                                    _reg["Área aplicada ha"]  = _edt_area
                                    _reg["Volume calda L/ha"] = _edt_calda
                                    _reg["Clima aplicação"]   = _edt_clima
                                    # Atualiza a lista de produtos (já sem os que foram marcados para remover)
                                    if _produtos_orig:
                                        _reg["Produtos"] = list(_edt_produtos)
                                    if _vars_orig:
                                        if "Dados Plantio" not in _reg:
                                            _reg["Dados Plantio"] = {}
                                        _reg["Dados Plantio"]["variedades"] = _edt_variedades
                                    salvar_dados_iaagro()
                                    st.session_state[_edit_key] = False
                                    success_box("✅ Aplicação atualizada!")
                                    st.rerun()
                                else:
                                    error_box("Não foi possível localizar a aplicação original para salvar a edição.")

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
    _ROTULOS_INT = ["🌤️ Clima & Alertas","💰 Preços de Mercado","🗺️ Mapa de Colheita IA"]
    _aba_int = st.radio("Seção:", _ROTULOS_INT, key="aba_intel_ativa",
                        horizontal=True)

if menu == "🌍 Inteligência":
  if _aba_int == _ROTULOS_INT[0]:
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

    # ── Seletor de localização (região/estado + cidade) + atualização ──────
    _UFS_BR = {
        "AC":"Acre","AL":"Alagoas","AP":"Amapá","AM":"Amazonas","BA":"Bahia",
        "CE":"Ceará","DF":"Distrito Federal","ES":"Espírito Santo","GO":"Goiás",
        "MA":"Maranhão","MT":"Mato Grosso","MS":"Mato Grosso do Sul","MG":"Minas Gerais",
        "PA":"Pará","PB":"Paraíba","PR":"Paraná","PE":"Pernambuco","PI":"Piauí",
        "RJ":"Rio de Janeiro","RN":"Rio Grande do Norte","RS":"Rio Grande do Sul",
        "RO":"Rondônia","RR":"Roraima","SC":"Santa Catarina","SP":"São Paulo",
        "SE":"Sergipe","TO":"Tocantins",
    }
    _lista_ufs = list(_UFS_BR.keys())
    _sel_c1, _sel_c2, _sel_c3 = st.columns([2.2, 1.8, 1])
    cidade = _sel_c1.text_input("📍 Cidade", value=d.get("cidade","") or "",
                                 placeholder="Ex: Xanxerê", key="clima_cidade_inp").strip()
    _uf_clima = _sel_c2.selectbox("🗺️ Estado / Região", _lista_ufs,
                                   index=_lista_ufs.index("SC"),
                                   format_func=lambda u: f"{u} — {_UFS_BR[u]}",
                                   key="clima_uf_sel")
    with _sel_c3:
        st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Atualizar", key="btn_atualizar_clima", use_container_width=True):
            st.rerun()

    if not cidade:
        st.markdown("""
        <div style='background:#1e3a5f;border-radius:12px;padding:20px;text-align:center;
        border:2px dashed #3b82f6;'>
        <div style='font-size:40px;'>🏙️</div>
        <div style='color:#94a3b8;margin-top:8px;'>
        Digite a <b style='color:#6ee7b7;'>cidade</b> acima (ou preencha no Cadastro da Área) para ver o clima em tempo real.
        </div></div>""", unsafe_allow_html=True)
    else:
        try:
            import requests as rq_
            from urllib.parse import quote as _quote_url

            # Cache de 30 min: evita estourar o limite diário do Open-Meteo
            # (o IP é compartilhado entre todos os usuários do Streamlit)
            @st.cache_data(ttl=1800, show_spinner=False)
            def _buscar_geo(nome):
                try:
                    _u = ("https://geocoding-api.open-meteo.com/v1/search"
                          f"?name={_quote_url(nome.strip())}&count=20&language=pt&format=json")
                    return rq_.get(_u, timeout=10).json()
                except Exception:
                    return {}

            # Fallback: Nominatim (OpenStreetMap) conhece distritos e
            # comunidades rurais que o Open-Meteo não tem. Usado só quando
            # a busca principal falha.
            @st.cache_data(ttl=1800, show_spinner=False)
            def _buscar_geo_osm(nome, uf_nome):
                try:
                    _q = f"{nome.strip()}, {uf_nome}, Brasil"
                    _u = ("https://nominatim.openstreetmap.org/search"
                          f"?q={_quote_url(_q)}&format=json&limit=5&accept-language=pt-BR")
                    _r = rq_.get(_u, timeout=10,
                                 headers={"User-Agent": "IAAgro/1.0 (agro app)"})
                    _dados = _r.json()
                    # Converte formato Nominatim para o formato do Open-Meteo
                    _out = []
                    for _d in _dados:
                        _out.append({
                            "name": (_d.get("display_name","").split(",")[0] or nome),
                            "latitude": float(_d["lat"]),
                            "longitude": float(_d["lon"]),
                            "admin1": uf_nome,
                            "country_code": "BR",
                        })
                    return {"results": _out}
                except Exception:
                    return {}

            @st.cache_data(ttl=1800, show_spinner=False)
            def _buscar_clima(lat, lon):
                try:
                    _u = (
                        "https://api.open-meteo.com/v1/forecast"
                        f"?latitude={lat}&longitude={lon}"
                        "&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
                        "precipitation,weather_code,wind_speed_10m,wind_direction_10m"
                        "&hourly=precipitation,precipitation_probability"
                        "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum"
                        "&timezone=America%2FSao_Paulo&forecast_days=7"
                    )
                    return rq_.get(_u, timeout=12).json()
                except Exception:
                    return {}

            _geo = _buscar_geo(cidade)
            _resultados = _geo.get("results", []) or []
            _br = [r for r in _resultados if r.get("country_code") == "BR"]
            _match = None
            for _res in _br:
                _adm = (_res.get("admin1", "") or "").lower()
                if _uf_clima.lower() in _adm or _UFS_BR[_uf_clima].lower() in _adm:
                    _match = _res; break
            if _match is None and _br:
                _match = _br[0]
            if _match is None and _resultados:
                _match = _resultados[0]

            # Fallback: se não achou, tenta o Nominatim (conhece localidades pequenas)
            if _match is None:
                _geo_osm = _buscar_geo_osm(cidade, _UFS_BR[_uf_clima])
                _res_osm = _geo_osm.get("results", []) or []
                if _res_osm:
                    _match = _res_osm[0]

            if not _match:
                st.warning(f"❌ Não encontrei '{cidade}'. Dicas: verifique o acento "
                           f"(ex: Xanxerê), confira se o estado selecionado está certo, "
                           f"ou use o município maior mais próximo — o clima da região é "
                           f"praticamente o mesmo para fins de aplicação.")
            else:
                _lat = _match["latitude"]; _lon = _match["longitude"]
                _nome_local = _match.get("name", cidade)
                _adm_local  = _match.get("admin1", "")

                _fc = _buscar_clima(_lat, _lon)

                if _fc and _fc.get("error"):
                    _motivo_api = str(_fc.get("reason", "")).lower()
                    if "limit" in _motivo_api:
                        st.warning(
                            "⏳ O serviço de clima atingiu o limite de consultas por hoje. "
                            "A cota é gratuita e compartilhada entre os usuários do app, "
                            "e reseta automaticamente nas próximas horas. "
                            "Evite clicar em Atualizar várias vezes seguidas para não esgotar a cota."
                        )
                    else:
                        st.warning(f"Serviço de clima indisponível no momento. Tente novamente em instantes.")
                elif _fc and "current" in _fc:
                    st.caption(f"📡 Exibindo: **{_nome_local}"
                               f"{(' — ' + _adm_local) if _adm_local else ''}** · "
                               f"Atualizado às {datetime.now().strftime('%H:%M:%S')} · fonte Open-Meteo")

                    # ── Mapeamento código WMO -> descrição PT + emoji ──
                    def _wmo(cod):
                        cod = int(cod or 0)
                        _t = {
                            0:("Céu limpo","☀️"),1:("Poucas nuvens","🌤️"),2:("Parcialmente nublado","⛅"),
                            3:("Nublado","☁️"),45:("Névoa","🌫️"),48:("Névoa gelada","🌫️"),
                            51:("Garoa fraca","🌦️"),53:("Garoa","🌦️"),55:("Garoa forte","🌦️"),
                            61:("Chuva fraca","🌦️"),63:("Chuva moderada","🌧️"),65:("Chuva forte","🌧️"),
                            66:("Chuva congelante","🌧️"),67:("Chuva congelante forte","🌧️"),
                            71:("Neve fraca","❄️"),73:("Neve","❄️"),75:("Neve forte","❄️"),
                            80:("Pancadas fracas","🌦️"),81:("Pancadas","🌧️"),82:("Pancadas fortes","⛈️"),
                            95:("Trovoada","⛈️"),96:("Trovoada c/ granizo","⛈️"),99:("Trovoada forte","⛈️"),
                        }
                        return _t.get(cod, ("—","🌤️"))

                    _cur_o = _fc["current"]
                    _temp_c    = int(round(_cur_o.get("temperature_2m", 0)))
                    _feels     = int(round(_cur_o.get("apparent_temperature", 0)))
                    _umid      = int(round(_cur_o.get("relative_humidity_2m", 0)))
                    _vento_kmh = int(round(_cur_o.get("wind_speed_10m", 0)))
                    _chuva_cur = float(_cur_o.get("precipitation", 0) or 0)
                    _cod_cur   = _cur_o.get("weather_code", 0)
                    _cond_pt, _cond_emoji = _wmo(_cod_cur)
                    _cond_lower = _cond_pt.lower()

                    # Direção do vento (graus -> rosa dos ventos)
                    _deg = _cur_o.get("wind_direction_10m", 0) or 0
                    _pts = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
                    _dir_vento = _pts[int((_deg % 360) / 22.5) % 16]

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

                    # (chuva das próximas horas é calculada abaixo, na janela)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # ── Chuva nas PRÓXIMAS horas (o que importa pra aplicar) ──────
                    # A chuva "agora" pode ser 0 mas com temporal chegando em 1-2h.
                    # Olha as próximas 6 horas: soma prevista + maior probabilidade.
                    _chuva_prox6 = 0.0
                    _prob_prox6  = 0
                    try:
                        _hr = _fc.get("hourly", {})
                        _htimes = _hr.get("time", [])
                        _hprec  = _hr.get("precipitation", [])
                        _hprob  = _hr.get("precipitation_probability", [])
                        # Acha o índice da hora atual
                        _agora_iso = datetime.now().strftime("%Y-%m-%dT%H:00")
                        _idx_now = next((i for i, t in enumerate(_htimes) if t >= _agora_iso), 0)
                        for _j in range(_idx_now, min(_idx_now + 6, len(_hprec))):
                            _chuva_prox6 += float(_hprec[_j] or 0)
                            if _j < len(_hprob):
                                _prob_prox6 = max(_prob_prox6, int(_hprob[_j] or 0))
                    except Exception:
                        pass

                    # ── Janela de aplicação — card grande ─────────────────────────
                    _ok_vento = _vento_kmh <= 15
                    _ok_umid  = 40 <= _umid <= 85
                    _ok_temp  = _temp_c <= 30
                    # Chuva OK só se: não chove agora E pouca chuva prevista E prob. baixa
                    _ok_chuva = (_chuva_cur == 0 and _chuva_prox6 < 1.0 and _prob_prox6 < 60)
                    _score    = sum([_ok_vento, _ok_umid, _ok_temp, _ok_chuva])

                    # Texto do critério de chuva conforme o cenário
                    if _chuva_cur > 0:
                        _lbl_chuva = f"Chovendo agora ({_chuva_cur}mm)"
                    elif _chuva_prox6 >= 1.0:
                        _lbl_chuva = f"Chuva prevista {_chuva_prox6:.1f}mm/6h"
                    elif _prob_prox6 >= 60:
                        _lbl_chuva = f"Risco de chuva {_prob_prox6}% (6h)"
                    else:
                        _lbl_chuva = f"Sem chuva prevista (6h)"

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
                            (_ok_chuva, _lbl_chuva),
                        ]
                    ])}
                    </div></div>
                    """, unsafe_allow_html=True)

                    # ── Previsão 7 dias — a partir do bloco 'daily' do Open-Meteo ──
                    st.markdown("### 📅 Previsão dos próximos dias")
                    from datetime import datetime as _dt_c
                    _dias_pt = ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"]
                    _daily = _fc.get("daily", {})
                    _datas   = _daily.get("time", [])
                    _maxs    = _daily.get("temperature_2m_max", [])
                    _mins    = _daily.get("temperature_2m_min", [])
                    _chuvas  = _daily.get("precipitation_sum", [])
                    _codigos = _daily.get("weather_code", [])

                    _cols_prev = st.columns(min(len(_datas), 7) or 1)
                    for _di in range(min(len(_datas), 7)):
                        _d_max  = int(round(_maxs[_di])) if _di < len(_maxs) else 0
                        _d_min  = int(round(_mins[_di])) if _di < len(_mins) else 0
                        _d_chuva = float(_chuvas[_di] or 0) if _di < len(_chuvas) else 0
                        _d_cod   = _codigos[_di] if _di < len(_codigos) else 0
                        _d_desc, _d_emoji = _wmo(_d_cod)
                        try:
                            _dt_obj  = _dt_c.strptime(_datas[_di], "%Y-%m-%d")
                            _dia_sem = _dias_pt[_dt_obj.weekday()]
                            _d_fmt   = f"{_dt_obj.day:02d}/{_dt_obj.month:02d}"
                        except Exception:
                            _dia_sem = ""; _d_fmt = _datas[_di] if _di < len(_datas) else ""

                        if _d_chuva > 15 or _d_cod in (95,96,99):
                            _d_bg = "#1e1b4b"; _d_borda = "#818cf8"; _d_alerta = "⛈️ Chuva forte"; _d_cor_txt = "#a5b4fc"
                        elif _d_chuva > 5:
                            _d_bg = "#1e3a5f"; _d_borda = "#3b82f6"; _d_alerta = "🌧️ Chuva"; _d_cor_txt = "#93c5fd"
                        elif _d_chuva > 0.5:
                            _d_bg = "#0f2d4a"; _d_borda = "#0ea5e9"; _d_alerta = "🌦️ Chuva fraca"; _d_cor_txt = "#7dd3fc"
                        elif _d_cod == 3:
                            _d_bg = "#1e293b"; _d_borda = "#475569"; _d_alerta = "☁️ Nublado"; _d_cor_txt = "#94a3b8"
                        else:
                            _d_bg = "#14532d"; _d_borda = "#22c55e"; _d_alerta = "☀️ Bom dia"; _d_cor_txt = "#6ee7b7"

                        with _cols_prev[_di]:
                            st.markdown(f"""
                            <div style='background:{_d_bg};border-radius:14px;padding:14px 10px;
                            text-align:center;border:2px solid {_d_borda};margin:2px;'>
                            <div style='color:{_d_cor_txt};font-size:12px;font-weight:800;
                            letter-spacing:1px;'>{_dia_sem}</div>
                            <div style='color:#94a3b8;font-size:11px;'>{_d_fmt}</div>
                            <div style='font-size:22px;margin:6px 0;'>{_d_emoji}</div>
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
                    for _di in range(min(len(_datas), 7)):
                        _d_chuva_t = float(_chuvas[_di] or 0) if _di < len(_chuvas) else 0
                        _d_cod_t   = _codigos[_di] if _di < len(_codigos) else 0
                        try:
                            _dt_t = _dt_c.strptime(_datas[_di],"%Y-%m-%d")
                            _d_str = f"{_dt_t.day:02d}/{_dt_t.month:02d}"
                        except Exception:
                            _d_str = _datas[_di] if _di < len(_datas) else ""
                        if _d_cod_t in (95,96,99):
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

        except Exception as e:
            st.info(f"Serviço de clima temporariamente indisponível. ({e})")

if menu == "🌍 Inteligência":
  if _aba_int == _ROTULOS_INT[1]:

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
  if _aba_int == _ROTULOS_INT[2]:
    st.header("🗺️ Mapa de Colheita IA")
    st.markdown("""
    <div style='background:#0f3460;border-radius:10px;padding:12px 16px;
    border-left:5px solid #22c55e;margin-bottom:12px;'>
    <b style='color:#22c55e;'>🛰️ Análise de Mapas de Precisão</b><br>
    <span style='color:#f1f5f9;font-size:13px;'>
    Faça upload de um mapa (imagem ou PDF) e a IA irá analisá-lo por zonas.
    Funciona com <b>mapas de colheita</b> (produtividade), <b>mapas de aplicação
    a taxa variável</b> (prescrição de adubo/calcário por zona) e mapas de
    fertilidade. A IA identifica zonas, variabilidade e recomenda manejo.
    </span></div>
    """, unsafe_allow_html=True)

    _arquivo_mapa = st.file_uploader(
        "📂 Upload do mapa (JPG, PNG, PDF)",
        type=["jpg","jpeg","png","pdf"],
        key="upload_mapa_colheita"
    )

    if _arquivo_mapa:
        if _arquivo_mapa.type.startswith("image"):
            st.image(_arquivo_mapa, caption="Mapa carregado", use_container_width=True)
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

                    _txt_mapa = (f"Analise este mapa de precisão agrícola (pode ser mapa de "
                                 f"colheita/produtividade OU mapa de aplicação a taxa variável de "
                                 f"insumos). Cultura: {cultura_limpa(_cultura_mc)}, Área: {_area_mc} ha. "
                                 f"Obs: {_obs_mc}. "
                                 "Primeiro identifique que tipo de mapa é. Depois analise: "
                                 "1) Zonas de alta e baixa (produtividade ou dose aplicada), "
                                 "2) Variabilidade espacial dentro do talhão, "
                                 "3) Possíveis causas das variações (fertilidade, textura, relevo, compactação), "
                                 "4) Recomendações práticas de manejo por zonas. "
                                 "Se houver dados numéricos (taxa média, faixas, área por zona), "
                                 "use-os na análise. "
                                 "Responda em português, de forma prática para o produtor.")

                    _content_mapa = []
                    # Adiciona imagem OU PDF conforme o tipo do arquivo
                    _arquivo_mapa.seek(0)
                    if _arquivo_mapa.type.startswith("image"):
                        _img_b64 = _b64_mapa.b64encode(_arquivo_mapa.read()).decode()
                        _ext = "jpeg" if "jpg" in _arquivo_mapa.type else "png"
                        _content_mapa.append({
                            "type": "image",
                            "source": {"type": "base64", "media_type": f"image/{_ext}", "data": _img_b64}
                        })
                    elif _arquivo_mapa.type == "application/pdf":
                        _pdf_b64 = _b64_mapa.b64encode(_arquivo_mapa.read()).decode()
                        _content_mapa.append({
                            "type": "document",
                            "source": {"type": "base64", "media_type": "application/pdf", "data": _pdf_b64}
                        })
                    _content_mapa.append({"type": "text", "text": _txt_mapa})

                    _resp_mapa = _rq_mapa.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": _api_key_mapa,
                            "anthropic-version": "2023-06-01",
                            "anthropic-beta": "pdfs-2024-09-25",
                            "content-type": "application/json",
                        },
                        json={
                            "model": "claude-sonnet-4-6",
                            "max_tokens": 2500,
                            "messages": [{"role":"user","content":_content_mapa}],
                        },
                        timeout=60
                    )
                    _json_mapa = _resp_mapa.json()
                    if "content" in _json_mapa and _json_mapa["content"]:
                        _analise = _json_mapa["content"][0].get("text","Sem resposta.")
                        st.session_state["_analise_mapa"] = _analise
                    else:
                        _erro_api = _json_mapa.get("error",{}).get("message","resposta inesperada da IA")
                        st.error(f"Não foi possível analisar: {_erro_api}")
                except Exception as e:
                    st.error(f"Erro na análise: {e}")

    if st.session_state.get("_analise_mapa"):
        st.divider()
        st.subheader("🤖 Análise da IA")
        st.markdown(st.session_state["_analise_mapa"])
    elif not _arquivo_mapa:
        st.info("Faça o upload do mapa de colheita para análise.")


elif menu == "🧠 Assistente IA":
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f3460,#1a4a73);border-radius:16px;
    padding:20px 24px;margin-bottom:20px;border:1px solid #22c55e33;'>
    <h2 style='color:#6ee7b7;margin:0 0 4px;font-size:22px;'>🤖 Assistente IA Agrícola</h2>
    <p style='color:#94a3b8;margin:0;font-size:13px;'>
    Especialista em agricultura brasileira — EMBRAPA, CQFS RS/SC, manejo integrado
    </p></div>""", unsafe_allow_html=True)

    if "assistente_hist" not in st.session_state:
        st.session_state.assistente_hist = []

    # ── CONTROLE DE USO DO ASSISTENTE (limite por plano) ──
    # Conta perguntas por mês e reseta a cada mês. Persiste em dados (Supabase).
    from datetime import datetime as _dt_ia_lim
    _mes_atual = _dt_ia_lim.now().strftime("%Y-%m")
    _uso_ia = st.session_state.dados.get("ia_uso", {})
    if _uso_ia.get("mes") != _mes_atual:
        # Vira o mês: zera o contador
        _uso_ia = {"mes": _mes_atual, "count": 0}
        st.session_state.dados["ia_uso"] = _uso_ia
    _plano_atual_ia = st.session_state.get("sb_plano", "free")
    _limite_ia = PLANOS.get(_plano_atual_ia, PLANOS["free"]).get("ia_perguntas_mes", 5)
    _usadas_ia = _uso_ia.get("count", 0)
    _restantes_ia = max(_limite_ia - _usadas_ia, 0)

    # Mostra o contador de uso
    _cor_uso = "#22c55e" if _restantes_ia > _limite_ia*0.3 else ("#f59e0b" if _restantes_ia > 0 else "#ef4444")
    st.markdown(f"""
    <div style='background:#0f3460;border-radius:8px;padding:8px 14px;margin-bottom:10px;
    border-left:4px solid {_cor_uso};font-size:12px;color:#cbd5e1;'>
    💬 Perguntas usadas este mês: <b style='color:{_cor_uso};'>{_usadas_ia}/{_limite_ia}</b>
    &nbsp;·&nbsp; Restam <b>{_restantes_ia}</b> no plano {PLANOS.get(_plano_atual_ia,{}).get('nome',_plano_atual_ia)}
    </div>""", unsafe_allow_html=True)

    _limite_atingido = _restantes_ia <= 0

    # Contexto rico da propriedade
    _d_ia  = st.session_state.dados
    _areas_ctx = ""
    if st.session_state.areas:
        _areas_ctx = "; ".join([
            f"{a.get('Talhão','?')} {a.get('Hectares',0)}ha {a.get('Cultura','?')}"
            for a in st.session_state.areas[:3]
        ])
    # Rotação/planejamento de safras — essencial para a IA alertar sobre
    # restrições de plantio (residual de herbicida na próxima cultura).
    _rotacao_ctx = ""
    _plan = st.session_state.get("planejamento_safras", [])
    if _plan:
        _rot = []
        for _p in _plan[:4]:
            _v = _p.get("verao",{}); _i = _p.get("inverno",{})
            _seq = []
            if _i.get("cultura"): _seq.append(f"inverno {_i.get('cultura')}")
            if _v.get("cultura"): _seq.append(f"verão {_v.get('cultura')}")
            if _seq:
                _rot.append(" → ".join(_seq))
        if _rot:
            _rotacao_ctx = f" Rotação planejada: {'; '.join(_rot)}."
    _ctx_ia = (
        f"Segmento: {st.session_state.get('segmento','Grãos')}. "
        f"Propriedade: {_areas_ctx or 'não cadastrada'}.{_rotacao_ctx} "
        f"Região: Sul do Brasil (PR/SC/RS). "
        f"Plano: {st.session_state.get('plano','free')}. "
        f"IMPORTANTE: se for recomendar herbicida, considere a próxima cultura "
        f"da rotação acima para alertar sobre residual/plantback."
    )

    # Busca API key de forma robusta
    import os as _os_ia
    _api_key_ia = ""
    try:
        _api_key_ia = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass
    if not _api_key_ia:
        try:
            _api_key_ia = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            pass
    if not _api_key_ia:
        _api_key_ia = _os_ia.environ.get("ANTHROPIC_API_KEY", "")

    if not _api_key_ia or len(_api_key_ia) < 20:
        st.warning("⚠️ Chave API não configurada. Adicione ANTHROPIC_API_KEY nos secrets do Streamlit.")
    else:
        # Histórico de mensagens
        for msg in st.session_state.assistente_hist:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Upload de documento para análise (PDF, imagem, planilha)
        with st.expander("📎 Anexar documento para análise (PDF, imagem, planilha)"):
            _doc_ia = st.file_uploader(
                "Anexe uma nota fiscal, laudo, planilha de estoque, receituário...",
                type=["pdf","jpg","jpeg","png","xlsx","csv"],
                key="upload_doc_assistente",
                help="O documento será enviado junto com sua próxima pergunta. "
                     "Ex.: anexe uma nota fiscal e pergunte 'quais produtos tem nessa nota?'"
            )
            if _doc_ia:
                st.success(f"✅ {_doc_ia.name} anexado — faça sua pergunta abaixo que eu analiso.")

        if _limite_atingido:
            _prox_plano = "Pro" if _plano_atual_ia == "free" else "Premium"
            st.warning(f"🚫 Você atingiu o limite de **{_limite_ia} perguntas** deste mês "
                       f"no plano {PLANOS.get(_plano_atual_ia,{}).get('nome',_plano_atual_ia)}. "
                       f"O contador zera no início do próximo mês."
                       + (f" Para mais perguntas, faça upgrade para o plano {_prox_plano}."
                          if _plano_atual_ia != "premium" else
                          " Se precisar de mais, fale com o suporte."))
            _prompt_ia = None
        else:
            _prompt_ia = st.chat_input("Pergunte sobre adubação, pragas, clima, preços, manejo... ou anexe um documento acima")

        if _prompt_ia:
            # Incrementa o contador de uso e persiste
            st.session_state.dados["ia_uso"] = {
                "mes": _mes_atual, "count": _usadas_ia + 1
            }
            salvar_dados_iaagro()
            st.session_state.assistente_hist.append({"role":"user","content":_prompt_ia})
            with st.chat_message("user"):
                st.markdown(_prompt_ia)
            with st.chat_message("assistant"):
                with st.spinner("🌾 Analisando... (pode levar 1-2 min se eu precisar consultar bulas e dados na web)"):
                    try:
                        import requests as _rq_ia
                        import base64 as _b64_ia
                        # Monta histórico limitado a 10 mensagens para não exceder tokens
                        _msgs_ia = [
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.assistente_hist[-10:]
                        ]
                        # A API exige que a 1ª mensagem seja do usuário. Se o corte
                        # deixou um 'assistant' no início, remove até achar um 'user'.
                        while _msgs_ia and _msgs_ia[0]["role"] != "user":
                            _msgs_ia.pop(0)
                        if not _msgs_ia:
                            _msgs_ia = [{"role":"user","content":_prompt_ia}]

                        # Se há documento anexado, injeta no ÚLTIMO turno do usuário
                        _doc_anexo = st.session_state.get("upload_doc_assistente")
                        _texto_extra_doc = ""
                        _tem_doc_visual = False
                        if _doc_anexo is not None and _msgs_ia:
                            try:
                                _doc_anexo.seek(0)
                                _tipo_doc = _doc_anexo.type or ""
                                _conteudo_msg = []
                                if _tipo_doc.startswith("image"):
                                    _b64d = _b64_ia.b64encode(_doc_anexo.read()).decode()
                                    _extd = "jpeg" if "jp" in _tipo_doc else "png"
                                    _conteudo_msg.append({"type":"image","source":{
                                        "type":"base64","media_type":f"image/{_extd}","data":_b64d}})
                                    _tem_doc_visual = True
                                elif _tipo_doc == "application/pdf":
                                    _b64d = _b64_ia.b64encode(_doc_anexo.read()).decode()
                                    _conteudo_msg.append({"type":"document","source":{
                                        "type":"base64","media_type":"application/pdf","data":_b64d}})
                                    _tem_doc_visual = True
                                elif _doc_anexo.name.lower().endswith((".xlsx",".csv")):
                                    # Planilha: extrai texto e anexa como contexto
                                    import pandas as _pd_doc
                                    if _doc_anexo.name.lower().endswith(".csv"):
                                        _df_doc = _pd_doc.read_csv(_doc_anexo)
                                    else:
                                        _df_doc = _pd_doc.read_excel(_doc_anexo)
                                    _texto_extra_doc = (f"\n\n[Planilha anexada '{_doc_anexo.name}':\n"
                                                        f"{_df_doc.to_string()[:4000]}]")
                                # Monta o último turno com documento + texto
                                if _conteudo_msg:
                                    _conteudo_msg.append({"type":"text","text":_prompt_ia})
                                    _msgs_ia[-1] = {"role":"user","content":_conteudo_msg}
                                elif _texto_extra_doc:
                                    _msgs_ia[-1] = {"role":"user",
                                                    "content":_prompt_ia + _texto_extra_doc}
                            except Exception as _edoc:
                                st.caption(f"⚠️ Não consegui ler o documento: {_edoc}")

                        _system_ia = (
                            "Você é um agrônomo especialista brasileiro com foco no Sul do Brasil (PR, SC, RS). "
                            "Responda SEMPRE em português, de forma prática e objetiva para produtores rurais. "
                            "Use dados da EMBRAPA, CQFS RS/SC, IAPAR e boas práticas agronômicas. "
                            "Para recomendações de adubação, siga as tabelas CQFS RS/SC 2016. "
                            "Para defensivos, cite apenas produtos registrados no MAPA. "
                            "Seja direto: dê doses, épocas e práticas concretas. "
                            "IMPORTANTE: quando a pergunta envolver informação ATUAL — preços de "
                            "commodities/insumos, cotações, produtos/defensivos e seus princípios "
                            "ativos, lançamentos recentes, registros no MAPA, bulas, notícias de "
                            "safra ou clima — USE a ferramenta de busca na web para trazer dados "
                            "atualizados e completos, e cite a fonte. NUNCA liste defensivos ou "
                            "princípios ativos apenas de memória: o mercado tem hoje uma gama muito "
                            "ampla de ativos e misturas, então busque na web para dar opções atuais "
                            "e abrangentes (vários grupos químicos e marcas), não apenas um exemplo. "
                            "Para conhecimento agronômico consolidado (manejo, doses, épocas), responda "
                            "direto sem precisar buscar. "
                            "MANEJO DE RESISTÊNCIA (fungicidas, inseticidas, herbicidas): este é um tema "
                            "onde você deve ser CUIDADOSO e NÃO DOGMÁTICO. Regras importantes: "
                            "(1) NUNCA crave de memória um limite fixo de aplicações (ex: 'no máximo 2 do "
                            "mesmo grupo') como se valesse para todos os grupos — isso é simplista e "
                            "frequentemente ERRADO. Os limites variam por grupo químico, cultura e são "
                            "definidos pelo FRAC-BR/IRAC/HRAC, EMBRAPA e bulas. Para carboxamidas (SDHI), "
                            "por exemplo, na prática agronômica brasileira ATÉ 3 aplicações por ciclo é "
                            "geralmente aceitável e não caracteriza excesso — o problema seria 4, 5 ou "
                            "mais. Busque a recomendação atual do grupo específico antes de afirmar limites. "
                            "(2) NÃO trate a repetição de um mesmo grupo químico como ERRO automático. Um "
                            "bom programa de aplicação é avaliado no CONJUNTO: qual doença-alvo em cada "
                            "estádio (ex: manchas e fungos de solo no início; ferrugem asiática, que é "
                            "biotrófica, mais para frente), a alternância de triazóis (DMI) ao longo do "
                            "programa, e o uso de multissítios. Repetir um grupo pode ser tecnicamente "
                            "justificado pela pressão de doença. "
                            "(3) IDENTIFIQUE corretamente o grupo/mecanismo de cada princípio ativo (ex: "
                            "fluxapiroxade e piraziflumida são ambos SDHI/carboxamida; mefentrifluconazol, "
                            "difenoconazol, protioconazol e tebuconazol são triazóis/DMI) — se tiver "
                            "dúvida da classificação FRAC de um ativo, BUSQUE, não deduza. "
                            "(4) Ao analisar um programa do produtor, aponte pontos de atenção sem alarmismo "
                            "e SEMPRE reforce que a decisão final é do engenheiro agrônomo responsável, que "
                            "conhece o histórico da área. "
                            "CARÊNCIA E RESTRIÇÕES DE ROTAÇÃO (CRÍTICO — erros aqui causam prejuízo real): "
                            "(A) INTERVALO DE SEGURANÇA (carência pré-colheita): ao recomendar QUALQUER "
                            "defensivo, informe o período de carência (dias entre a última aplicação e a "
                            "colheita) e alerte para respeitá-lo. Esse dado vem da BULA do produto e varia "
                            "por cultura — se não tiver certeza do valor atual, BUSQUE na web/bula (AGROFIT/MAPA) "
                            "antes de afirmar, não invente. "
                            "(B) RESTRIÇÃO DE ROTAÇÃO / CARÊNCIA DE PLANTIO (plantback): este é um ponto que "
                            "você DEVE checar SEMPRE que recomendar herbicidas — especialmente com residual no "
                            "solo (ex: imidazolinonas, sulfonilureias, triazinas como atrazina, clomazona, "
                            "diclosulam, sulfentrazona, picloram). Muitos herbicidas têm efeito residual que "
                            "IMPEDE ou RESTRINGE o plantio de certas culturas na sequência (ex: um herbicida "
                            "usado na soja pode inviabilizar plantar milho, trigo, feijão ou hortaliças em "
                            "pós — o milho é sensível a vários residuais). NUNCA recomende um herbicida sem "
                            "considerar qual será a PRÓXIMA cultura da área (veja o contexto/rotação do "
                            "produtor). Se a recomendação puder afetar a cultura seguinte, ALERTE "
                            "explicitamente e informe o intervalo de plantback da bula. Na dúvida sobre o "
                            "residual ou o intervalo, BUSQUE na bula/AGROFIT — não deduza. "
                            "(C) Ao recomendar produto para uma cultura, confirme que ele é REGISTRADO para "
                            "AQUELA cultura no MAPA/AGROFIT — não recomende uso não registrado (off-label). "
                            "ANÁLISE DE DOCUMENTOS: o produtor pode anexar documentos (notas fiscais, "
                            "laudos, planilhas de estoque, receituários, bulas). Quando houver documento "
                            "anexado, analise-o com atenção: identifique produtos, quantidades, valores, "
                            "princípios ativos, datas E CARÊNCIAS/RESTRIÇÕES DE ROTAÇÃO quando for bula. "
                            "Para notas fiscais e estoque, ajude a organizar, "
                            "conferir e sugerir uso. Para planilhas de estoque, aponte itens em falta, "
                            "vencimentos, ou sugestões de compra conforme o manejo. Seja prático. "
                        )
                        # Monta o payload. Quando há PDF/imagem anexado, NÃO usa
                        # web_search na mesma chamada (a combinação documento + tool
                        # causa HTTP 400). Para análise de documento, a busca não é
                        # necessária — o conteúdo já está no anexo.
                        # PROMPT CACHING: a parte FIXA do system (instruções, ~1500
                        # tokens, igual para todos) é marcada com cache_control — assim
                        # pagamos 90% menos nas repetições. O contexto da propriedade
                        # (que muda por usuário) vai separado, sem cache.
                        _system_blocks = [
                            {"type": "text", "text": _system_ia,
                             "cache_control": {"type": "ephemeral"}},
                            {"type": "text", "text": f"Contexto da propriedade: {_ctx_ia}"},
                        ]
                        _payload_ia = {
                            "model":      "claude-sonnet-4-6",
                            "max_tokens": 4000,
                            "system":     _system_blocks,
                            "messages":   _msgs_ia,
                        }
                        if not _tem_doc_visual:
                            _payload_ia["tools"] = [{
                                "type": "web_search_20250305",
                                "name": "web_search",
                                "max_uses": 4,
                            }]
                        _resp_ia = _rq_ia.post(
                            "https://api.anthropic.com/v1/messages",
                            headers={
                                "x-api-key":         _api_key_ia,
                                "anthropic-version": "2023-06-01",
                                "anthropic-beta":    "pdfs-2024-09-25",
                                "content-type":      "application/json",
                            },
                            json=_payload_ia,
                            timeout=180,  # análises com busca na web podem levar 1-2 min
                        )
                        if _resp_ia.status_code == 200:
                            _data_ia = _resp_ia.json()
                            # Com web search, a resposta vem em vários blocos —
                            # concatena todos os blocos de texto na ordem
                            _blocos = _data_ia.get("content") or []
                            _ans = "".join(
                                b.get("text", "") for b in _blocos
                                if isinstance(b, dict) and b.get("type") == "text"
                            ).strip()
                            if _ans:
                                st.markdown(_ans)
                                st.session_state.assistente_hist.append(
                                    {"role":"assistant","content":_ans})
                            else:
                                st.error("Resposta vazia da API.")
                        elif _resp_ia.status_code == 401:
                            st.error("❌ Chave API inválida ou expirada. Verifique ANTHROPIC_API_KEY.")
                        elif _resp_ia.status_code == 429:
                            st.warning("⏳ Limite de requisições. Aguarde alguns segundos e tente novamente.")
                        else:
                            _det = ""
                            try:
                                _det = _resp_ia.json().get("error",{}).get("message","")[:200]
                            except Exception:
                                pass
                            st.error(f"Erro na API: HTTP {_resp_ia.status_code}"
                                     + (f" — {_det}" if _det else ""))
                    except _rq_ia.exceptions.Timeout:
                        st.warning("⏳ A análise está demorando mais que o normal (muitas buscas na web). "
                                   "Tente de novo, ou faça uma pergunta mais específica — por exemplo, "
                                   "analise um estádio ou produto por vez em vez do programa inteiro.")
                    except Exception as _e_ia:
                        st.error(f"Erro de conexão: {str(_e_ia)[:120]}")

    if st.session_state.assistente_hist:
        st.markdown("---")
        _btn_col1, _btn_col2, _btn_col3 = st.columns(3)

        # Exportar como TXT
        _conv_txt = ""
        for _m in st.session_state.assistente_hist:
            _role = "👨‍🌾 Você" if _m["role"] == "user" else "🤖 IAAgro IA"
            _conv_txt += f"{_role}:\n{_m['content']}\n\n{'─'*50}\n\n"
        _btn_col1.download_button(
            "📥 Exportar TXT", _conv_txt.encode("utf-8"),
            "conversa_iaagro.txt", "text/plain",
            key="btn_exp_conv_txt", use_container_width=True
        )

        # Exportar como PDF profissional
        try:
            _pdf_conv = gerar_pdf_conversa_assistente(st.session_state.assistente_hist)
            _btn_col2.download_button(
                "📄 Exportar PDF", _pdf_conv,
                f"conversa_iaagro_{datetime.now().strftime('%Y%m%d')}.pdf",
                "application/pdf",
                key="btn_exp_conv_pdf", use_container_width=True
            )
        except Exception as _e_pdfc:
            _btn_col2.warning(f"PDF indisponível: {str(_e_pdfc)[:60]}")

        if _btn_col3.button("🗑️ Limpar conversa", key="btn_limpar_assistente",
                            use_container_width=True):
            st.session_state.assistente_hist = []
            st.rerun()

# ─────────────────────────────────────────────
# MENU: PLANEJAMENTO DE SAFRAS
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# MENU: PLUVIÔMETRO
# ─────────────────────────────────────────────
elif menu == "🌧️ Pluviômetro":
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

        # ── Tabela de necessidade hídrica por cultura (por segmento) ──
        with st.expander("💧 Quanto de chuva cada cultura precisa no ciclo (do seu segmento)"):
            st.caption("Faixas técnicas de necessidade hídrica por ciclo (Embrapa, "
                       "ESALQ/USP, Doorenbos & Kassam). A perda é maior quando o "
                       "déficit ocorre na fase crítica de cada cultura.")
            import pandas as _pd_hidrico
            # Descobre o segmento a mostrar: PRIORIZA a cultura da ÁREA selecionada
            # (você está analisando a chuva daquela área específica, então a tabela
            # deve refletir a cultura dela). Usa o segmento do topo só como reserva,
            # quando a cultura da área não estiver identificada.
            _cult_ativa_limpa = cultura_limpa(cultura_chuva)
            _seg_ativo = None
            for _sg, _cults in _CULTURA_SEGMENTO.items():
                if _cult_ativa_limpa in _cults:
                    _seg_ativo = _sg
                    break
            if _seg_ativo is None:
                _seg_usuario = st.session_state.get("segmento")
                if _seg_usuario in _CULTURA_SEGMENTO:
                    _seg_ativo = _seg_usuario

            if _seg_ativo in _CULTURA_SEGMENTO:
                st.caption(f"Mostrando o segmento da cultura desta área "
                           f"(**{_cult_ativa_limpa}**). Para ver outra cultura, "
                           f"selecione uma área dessa cultura acima.")
                st.markdown(f"**{_seg_ativo}**")
                _linhas = []
                for _cult in _CULTURA_SEGMENTO[_seg_ativo]:
                    _info = _CHUVA_CICLO_MM.get(_cult)
                    if _info:
                        _mn, _mx, _fase, _sens = _info
                        _sens_txt = ("🔴 Alta" if _sens >= 0.9 else
                                     "🟡 Média" if _sens >= 0.7 else "🟢 Tolerante")
                        _linhas.append({
                            "Cultura": _cult,
                            "Chuva ideal/ciclo": f"{_mn}–{_mx} mm",
                            "Fase mais crítica": _fase,
                            "Sensib. à seca": _sens_txt,
                        })
                if _linhas:
                    st.dataframe(_pd_hidrico.DataFrame(_linhas),
                                 use_container_width=True, hide_index=True)
            else:
                st.info("Defina o segmento nas configurações (ou selecione uma área "
                        "com cultura cadastrada) para ver a tabela do seu segmento.")
            st.caption("💡 'Sensibilidade à seca' indica o quanto a cultura sofre com "
                       "falta de água na fase crítica: 🔴 Alta (ex: café, milho, soja) · "
                       "🟡 Média · 🟢 Tolerante (ex: mandioca, eucalipto, por raízes profundas).")

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




elif menu == "📅 Planejamento de Safras":
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f3460,#1a4a73);border-radius:16px;
    padding:20px 24px;margin-bottom:16px;border:1px solid #22c55e33;'>
    <h2 style='color:#6ee7b7;margin:0 0 4px;font-size:22px;'>📅 Planejamento de Safras</h2>
    <p style='color:#94a3b8;margin:0;font-size:13px;'>
    Rotação de culturas, safrinha e calendário agrícola num só lugar
    </p></div>""", unsafe_allow_html=True)
    _sub_plan = st.tabs(["🌱 Rotação & Safrinha","📅 Calendário Agrícola"])

if menu == "📅 Planejamento de Safras":
  with _sub_plan[0]:
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

# ── Sub-aba: Calendário Agrícola ──
if menu == "📅 Planejamento de Safras":
  with _sub_plan[1]:

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
        "📅 Eventos", "🌾 Plano por Safra", "🔄 Rotação de Culturas"
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
            Salve planejamentos na aba <b style='color:#6ee7b7;'>🌾 Plano por Safra</b>
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

# ─────────────────────────────────────────────
# MENU: MÁQUINAS (Inventário + Revisões)
# ─────────────────────────────────────────────
elif menu == "🔧 Máquinas":
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f3460,#1a4a73);border-radius:16px;
    padding:20px 24px;margin-bottom:16px;border:1px solid #22c55e33;'>
    <h2 style='color:#6ee7b7;margin:0 0 4px;font-size:22px;'>🔧 Máquinas & Implementos</h2>
    <p style='color:#94a3b8;margin:0;font-size:13px;'>
    Inventário do maquinário e controle de revisões por data e horas de uso
    </p></div>""", unsafe_allow_html=True)
    _sub_maq = st.tabs(["🚜 Inventário", "🔧 Revisões & Alertas"])

if menu == "🔧 Máquinas":
  # ══════════════════════════════════════════════════════════════════════
  # ABA 0 — INVENTÁRIO DE MÁQUINAS
  # ══════════════════════════════════════════════════════════════════════
  with _sub_maq[0]:
    _CATEGORIAS_MAQ = [
        "🚜 Trator", "🌾 Colheitadeira", "🌱 Plantadeira", "💧 Pulverizador",
        "🚛 Caminhão", "🔩 Implemento", "⚙️ Distribuidor", "🔧 Outro",
    ]
    st.markdown("#### ➕ Cadastrar Máquina")
    with st.form("form_maquina", clear_on_submit=True):
        _mc1, _mc2, _mc3 = st.columns(3)
        _m_nome  = _mc1.text_input("Nome / Apelido", placeholder="Ex: Trator John Deere do talhão 3")
        _m_cat   = _mc2.selectbox("Categoria", _CATEGORIAS_MAQ)
        _m_marca = _mc3.text_input("Marca", placeholder="John Deere, Massey, Case...")

        _mc4, _mc5, _mc6 = st.columns(3)
        _m_modelo = _mc4.text_input("Modelo", placeholder="6110J, MF 4707...")
        _m_ano    = _mc5.number_input("Ano", min_value=1950, max_value=2030,
                                      value=2020, step=1)
        _m_horim  = _mc6.number_input("Horímetro atual (h)", min_value=0.0, step=10.0,
                                      help="Horas de uso no horímetro da máquina")

        _mc7, _mc8 = st.columns(2)
        _m_placa  = _mc7.text_input("Placa / Nº série (opcional)", placeholder="ABC-1234 ou nº de série")
        _m_obs    = _mc8.text_input("Observações (opcional)", placeholder="Cor, detalhes, etc.")

        _m_add = st.form_submit_button("➕ Adicionar máquina", use_container_width=True)

    if _m_add:
        if not _m_nome.strip():
            st.error("Dê um nome ou apelido para a máquina.")
        else:
            import uuid as _uuid_m
            st.session_state.maquinas.append({
                "id":        str(_uuid_m.uuid4())[:8],
                "nome":      _m_nome.strip(),
                "categoria": _m_cat,
                "marca":     _m_marca.strip(),
                "modelo":    _m_modelo.strip(),
                "ano":       int(_m_ano),
                "horimetro": float(_m_horim),
                "placa":     _m_placa.strip(),
                "obs":       _m_obs.strip(),
                "cadastro":  datetime.now().strftime("%d/%m/%Y"),
            })
            salvar_dados_iaagro()
            success_box(f"✅ {_m_nome} adicionada ao inventário!")
            st.rerun()

    st.divider()

    # ── Lista do inventário ────────────────────────────────────────────
    _maqs = st.session_state.get("maquinas", [])
    if not _maqs:
        st.info("Nenhuma máquina cadastrada ainda. Use o formulário acima para começar.")
    else:
        st.markdown(f"#### 🚜 Frota cadastrada ({len(_maqs)} máquina(s))")

        # Métricas rápidas
        _mm1, _mm2, _mm3 = st.columns(3)
        _mm1.metric("Total de máquinas", len(_maqs))
        _idade_media = 0
        _anos = [m.get("ano", 0) for m in _maqs if m.get("ano", 0) > 0]
        if _anos:
            _idade_media = datetime.now().year - (sum(_anos) / len(_anos))
        _mm2.metric("Idade média da frota", f"{_idade_media:.0f} anos")
        _horas_tot = sum(m.get("horimetro", 0) for m in _maqs)
        _mm3.metric("Horas totais (frota)", f"{_horas_tot:,.0f} h")

        st.markdown("<br>", unsafe_allow_html=True)

        for _mi, _maq in enumerate(_maqs):
            _idade = datetime.now().year - _maq.get("ano", datetime.now().year)
            with st.container():
                st.markdown(f"""
                <div style='background:#0f172a;border:1px solid #1e3a2f;border-left:4px solid #22c55e;
                border-radius:10px;padding:12px 16px;margin:4px 0;'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                <div>
                <span style='color:#6ee7b7;font-size:16px;font-weight:800;'>{_maq.get('categoria','')} {_maq.get('nome','')}</span><br>
                <span style='color:#cbd5e1;font-size:13px;'>
                {_maq.get('marca','')} {_maq.get('modelo','')} · Ano {_maq.get('ano','—')}
                ({_idade} anos) · {_maq.get('horimetro',0):,.0f} h
                {' · ' + _maq.get('placa','') if _maq.get('placa') else ''}
                </span>
                {'<br><span style="color:#64748b;font-size:12px;">' + _maq.get('obs','') + '</span>' if _maq.get('obs') else ''}
                </div></div></div>""", unsafe_allow_html=True)

                _ce1, _ce2, _ce3, _ce4 = st.columns([1, 1, 1.5, 2.5])
                # Atualizar horímetro
                _novo_h = _ce1.number_input("Atualizar horímetro", min_value=0.0, step=10.0,
                                            value=float(_maq.get("horimetro", 0)),
                                            key=f"uph_{_maq.get('id', _mi)}")
                if _ce2.button("💾 Salvar h", key=f"savh_{_maq.get('id', _mi)}"):
                    st.session_state.maquinas[_mi]["horimetro"] = float(_novo_h)
                    salvar_dados_iaagro()
                    success_box("Horímetro atualizado!")
                    st.rerun()
                _mkey = _maq.get('id', _mi)
                if _ce3.button("✏️ Editar", key=f"editm_{_mkey}"):
                    st.session_state[f"edit_maq_{_mkey}"] = not st.session_state.get(f"edit_maq_{_mkey}", False)
                    st.rerun()
                if _ce4.button("🗑️ Remover máquina", key=f"delm_{_mkey}"):
                    st.session_state.maquinas.pop(_mi)
                    salvar_dados_iaagro()
                    st.rerun()

                # ── Formulário de edição da máquina ──
                if st.session_state.get(f"edit_maq_{_mkey}", False):
                    with st.form(f"form_edit_maq_{_mkey}"):
                        st.markdown("**✏️ Editando máquina**")
                        _ec1, _ec2, _ec3 = st.columns(3)
                        _e_nome  = _ec1.text_input("Nome / Apelido", value=_maq.get("nome",""))
                        _cats_ed = _CATEGORIAS_MAQ
                        _cat_idx = _cats_ed.index(_maq.get("categoria")) if _maq.get("categoria") in _cats_ed else 0
                        _e_cat   = _ec2.selectbox("Categoria", _cats_ed, index=_cat_idx)
                        _e_marca = _ec3.text_input("Marca", value=_maq.get("marca",""))
                        _ec4, _ec5, _ec6 = st.columns(3)
                        _e_modelo = _ec4.text_input("Modelo", value=_maq.get("modelo",""))
                        _e_ano    = _ec5.number_input("Ano", min_value=1950, max_value=2030,
                                                      value=int(_maq.get("ano", 2020)), step=1)
                        _e_horim  = _ec6.number_input("Horímetro (h)", min_value=0.0, step=10.0,
                                                      value=float(_maq.get("horimetro", 0)))
                        _ec7, _ec8 = st.columns(2)
                        _e_placa  = _ec7.text_input("Placa / Nº série", value=_maq.get("placa",""))
                        _e_obs    = _ec8.text_input("Observações", value=_maq.get("obs",""))
                        _eb1, _eb2 = st.columns(2)
                        _e_salvar   = _eb1.form_submit_button("💾 Salvar alterações", use_container_width=True)
                        _e_cancelar = _eb2.form_submit_button("✖️ Cancelar", use_container_width=True)

                    if _e_salvar:
                        if not _e_nome.strip():
                            st.error("O nome não pode ficar vazio.")
                        else:
                            st.session_state.maquinas[_mi].update({
                                "nome": _e_nome.strip(), "categoria": _e_cat,
                                "marca": _e_marca.strip(), "modelo": _e_modelo.strip(),
                                "ano": int(_e_ano), "horimetro": float(_e_horim),
                                "placa": _e_placa.strip(), "obs": _e_obs.strip(),
                            })
                            st.session_state[f"edit_maq_{_mkey}"] = False
                            salvar_dados_iaagro()
                            success_box("✅ Máquina atualizada!")
                            st.rerun()
                    if _e_cancelar:
                        st.session_state[f"edit_maq_{_mkey}"] = False
                        st.rerun()

                # ── Peças fixas da máquina (filtros, óleo — código + nome) ──
                _pcs = _maq.get("pecas", [])
                with st.expander(f"🔩 Peças de revisão desta máquina ({len(_pcs)})"):
                    st.caption("Cadastre aqui os filtros, óleos e peças que esta máquina usa, "
                               "com o código de cada um. Depois é só levar a lista pronta na revenda.")
                    with st.form(f"form_peca_{_maq.get('id', _mi)}", clear_on_submit=True):
                        _pp1, _pp2, _pp3 = st.columns([2, 3, 1])
                        _p_cod  = _pp1.text_input("Código", placeholder="RE504836", key=f"pcod_{_maq.get('id', _mi)}")
                        _p_nome = _pp2.text_input("Nome da peça", placeholder="Filtro de óleo do motor", key=f"pnom_{_maq.get('id', _mi)}")
                        _p_add  = _pp3.form_submit_button("➕", use_container_width=True)
                    if _p_add and _p_nome.strip():
                        st.session_state.maquinas[_mi].setdefault("pecas", []).append({
                            "codigo": _p_cod.strip(), "nome": _p_nome.strip(),
                        })
                        salvar_dados_iaagro()
                        st.rerun()

                    if _pcs:
                        for _pi, _pc in enumerate(_pcs):
                            _pl1, _pl2 = st.columns([6, 1])
                            _cod_txt = f"<code style='background:#1e293b;color:#6ee7b7;padding:1px 6px;border-radius:4px;'>{_pc.get('codigo','—')}</code>" if _pc.get('codigo') else "<span style='color:#64748b;'>sem código</span>"
                            _pl1.markdown(f"{_cod_txt} &nbsp; {_pc.get('nome','')}", unsafe_allow_html=True)
                            if _pl2.button("🗑️", key=f"delpc_{_maq.get('id', _mi)}_{_pi}"):
                                st.session_state.maquinas[_mi]["pecas"].pop(_pi)
                                salvar_dados_iaagro()
                                st.rerun()

                        # ── PDF só desta máquina (pra levar na revenda) ──
                        _nome_maq_pdf = f"{_maq.get('categoria','')} {_maq.get('nome','')}".strip()
                        _itens_maq = [
                            {"maquina": _nome_maq_pdf,
                             "codigo": _p.get("codigo", ""), "nome": _p.get("nome", "")}
                            for _p in _pcs
                        ]
                        try:
                            _pdf_maq = gerar_pdf_lista_pecas(
                                _itens_maq,
                                titulo=f"Peças — {_maq.get('nome','Máquina')}"
                            )
                            _nome_arq = "".join(
                                c if c.isalnum() else "_" for c in _maq.get("nome", "maquina")
                            ).lower()
                            st.download_button(
                                "📥 Baixar/imprimir peças desta máquina (PDF)",
                                data=_pdf_maq,
                                file_name=f"pecas_{_nome_arq}_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                key=f"pdfmaq_{_maq.get('id', _mi)}",
                                use_container_width=True,
                            )
                        except Exception as _e_pm:
                            st.error(f"Erro ao gerar PDF: {_e_pm}")
                    else:
                        st.info("Nenhuma peça cadastrada para esta máquina ainda.")

  # ══════════════════════════════════════════════════════════════════════
  # ABA 1 — REVISÕES & ALERTAS
  # ══════════════════════════════════════════════════════════════════════
  with _sub_maq[1]:
    _maqs_r = st.session_state.get("maquinas", [])
    if not _maqs_r:
        st.info("Cadastre máquinas na aba Inventário antes de programar revisões.")
    else:
        # ── Gerar lista de compras (PDF) das peças ──────────────────────
        with st.expander("🛒 Gerar lista de compras de peças (PDF para a revenda)"):
            _revs_pdf = st.session_state.get("maquinas_revisoes", [])
            _hoje_pdf = datetime.now().date()

            _opcao_lista = st.radio(
                "O que incluir na lista?",
                ["Só revisões vencidas/próximas", "Todas as máquinas (peças cadastradas)"],
                key="opc_lista_pecas", horizontal=True
            )

            _itens_compra = []
            if _opcao_lista == "Todas as máquinas (peças cadastradas)":
                for _m in _maqs_r:
                    for _p in _m.get("pecas", []):
                        _itens_compra.append({
                            "maquina": f"{_m.get('categoria','')} {_m.get('nome','')}".strip(),
                            "codigo": _p.get("codigo", ""), "nome": _p.get("nome", ""),
                        })
            else:
                # Só das revisões vencidas ou próximas (≤15 dias ou ≤30h)
                for _rev in _revs_pdf:
                    _maq_r = next((m for m in _maqs_r if m.get("id") == _rev.get("maq_id")), None)
                    if not _maq_r:
                        continue
                    _venc = False
                    if _rev.get("interv_dias", 0) > 0:
                        try:
                            _dtu = datetime.strptime(_rev["data_ultima"], "%Y-%m-%d").date()
                            if (_dtu + timedelta(days=_rev["interv_dias"]) - _hoje_pdf).days <= 15:
                                _venc = True
                        except Exception:
                            pass
                    if _rev.get("interv_horas", 0) > 0:
                        _hv = _rev.get("horim_ultima", 0) + _rev["interv_horas"]
                        if (_hv - _maq_r.get("horimetro", 0)) <= 30:
                            _venc = True
                    if _venc:
                        for _p in _maq_r.get("pecas", []):
                            _itens_compra.append({
                                "maquina": f"{_maq_r.get('categoria','')} {_maq_r.get('nome','')}".strip(),
                                "codigo": _p.get("codigo", ""), "nome": _p.get("nome", ""),
                            })

            if _itens_compra:
                st.markdown(f"**{len(_itens_compra)} peça(s)** na lista:")
                for _ic in _itens_compra:
                    _c_txt = f"`{_ic['codigo']}`" if _ic.get("codigo") else "*(sem código)*"
                    st.markdown(f"- {_c_txt} {_ic['nome']} — {_ic['maquina']}")
                try:
                    _pdf_bytes = gerar_pdf_lista_pecas(_itens_compra)
                    st.download_button(
                        "📥 Baixar lista de compras (PDF)",
                        data=_pdf_bytes,
                        file_name=f"lista_pecas_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                except Exception as _e_pdf:
                    st.error(f"Erro ao gerar PDF: {_e_pdf}")
            else:
                st.info("Nenhuma peça para listar. Cadastre peças nas máquinas (aba Inventário) "
                        "e, se escolher 'vencidas/próximas', tenha revisões nesse status.")

        st.markdown("#### ➕ Programar Revisão")
        with st.form("form_revisao", clear_on_submit=True):
            _rc1, _rc2 = st.columns(2)
            _r_maq_nome = _rc1.selectbox(
                "Máquina",
                [f"{m.get('categoria','')} {m.get('nome','')}" for m in _maqs_r],
                key="rev_maq_sel"
            )
            _r_tipo = _rc2.text_input("Tipo de revisão", placeholder="Troca de óleo, filtros, revisão geral...")

            _rc3, _rc4, _rc5 = st.columns(3)
            _r_data_ult = _rc3.date_input("Data da última revisão", value=datetime.now())
            _r_interv_dias = _rc4.number_input("Revisar a cada (dias)", min_value=0, step=30,
                                               value=180,
                                               help="0 = não alertar por data")
            _r_interv_horas = _rc5.number_input("Revisar a cada (horas)", min_value=0, step=50,
                                                value=250,
                                                help="0 = não alertar por horas de uso")

            # Horímetro no momento da última revisão
            _idx_maq = [f"{m.get('categoria','')} {m.get('nome','')}" for m in _maqs_r].index(_r_maq_nome)
            _horim_atual = _maqs_r[_idx_maq].get("horimetro", 0)
            _r_horim_ult = st.number_input(
                "Horímetro na última revisão (h)", min_value=0.0, step=10.0,
                value=float(_horim_atual),
                help=f"Horímetro atual da máquina: {_horim_atual:,.0f} h"
            )

            _r_add = st.form_submit_button("➕ Programar revisão", use_container_width=True)

        if _r_add:
            if not _r_tipo.strip():
                st.error("Descreva o tipo de revisão.")
            else:
                import uuid as _uuid_r
                st.session_state.maquinas_revisoes.append({
                    "id":          str(_uuid_r.uuid4())[:8],
                    "maquina":     _r_maq_nome,
                    "maq_id":      _maqs_r[_idx_maq].get("id", ""),
                    "tipo":        _r_tipo.strip(),
                    "data_ultima": _r_data_ult.strftime("%Y-%m-%d"),
                    "interv_dias": int(_r_interv_dias),
                    "interv_horas": int(_r_interv_horas),
                    "horim_ultima": float(_r_horim_ult),
                })
                salvar_dados_iaagro()
                success_box(f"✅ Revisão programada para {_r_maq_nome}!")
                st.rerun()

        st.divider()

        # ── Painel de alertas ──────────────────────────────────────────
        _revs = st.session_state.get("maquinas_revisoes", [])
        if not _revs:
            st.info("Nenhuma revisão programada ainda.")
        else:
            st.markdown("#### 🔔 Status das Revisões")

            # Calcula status de cada revisão (o que vencer primeiro: data OU horas)
            _hoje = datetime.now().date()
            _linhas_rev = []
            for _rev in _revs:
                # Máquina atual (para pegar horímetro atualizado)
                _maq_atual = next((m for m in _maqs_r if m.get("id") == _rev.get("maq_id")), None)
                _horim_now = _maq_atual.get("horimetro", 0) if _maq_atual else 0

                # Vencimento por DATA
                _venc_data = None
                _dias_rest = None
                if _rev.get("interv_dias", 0) > 0:
                    try:
                        _dt_ult = datetime.strptime(_rev["data_ultima"], "%Y-%m-%d").date()
                        _venc_data = _dt_ult + timedelta(days=_rev["interv_dias"])
                        _dias_rest = (_venc_data - _hoje).days
                    except Exception:
                        pass

                # Vencimento por HORAS
                _horas_rest = None
                if _rev.get("interv_horas", 0) > 0:
                    _horim_venc = _rev.get("horim_ultima", 0) + _rev["interv_horas"]
                    _horas_rest = _horim_venc - _horim_now

                # Determina o status pelo que está mais crítico
                _crit = "ok"
                _msgs = []
                if _dias_rest is not None:
                    if _dias_rest < 0:
                        _crit = "vencido"; _msgs.append(f"venceu há {abs(_dias_rest)} dias")
                    elif _dias_rest <= 15:
                        _crit = "proximo" if _crit != "vencido" else _crit
                        _msgs.append(f"vence em {_dias_rest} dias")
                    else:
                        _msgs.append(f"faltam {_dias_rest} dias")
                if _horas_rest is not None:
                    if _horas_rest < 0:
                        _crit = "vencido"; _msgs.append(f"passou {abs(_horas_rest):,.0f}h do limite")
                    elif _horas_rest <= 30:
                        if _crit != "vencido": _crit = "proximo"
                        _msgs.append(f"faltam {_horas_rest:,.0f}h")
                    else:
                        _msgs.append(f"faltam {_horas_rest:,.0f}h")

                _linhas_rev.append((_crit, _rev, _msgs, _horim_now))

            # Ordena: vencidos primeiro, depois próximos, depois ok
            _ordem = {"vencido": 0, "proximo": 1, "ok": 2}
            _linhas_rev.sort(key=lambda x: _ordem.get(x[0], 3))

            # Resumo no topo
            _n_venc = sum(1 for l in _linhas_rev if l[0] == "vencido")
            _n_prox = sum(1 for l in _linhas_rev if l[0] == "proximo")
            _rs1, _rs2, _rs3 = st.columns(3)
            _rs1.metric("🔴 Vencidas", _n_venc)
            _rs2.metric("🟡 Próximas", _n_prox)
            _rs3.metric("🟢 Em dia", len(_linhas_rev) - _n_venc - _n_prox)

            st.markdown("<br>", unsafe_allow_html=True)

            for _crit, _rev, _msgs, _horim_now in _linhas_rev:
                if _crit == "vencido":
                    _bg, _bd, _ico, _lbl = "#7f1d1d", "#ef4444", "🔴", "VENCIDA"
                elif _crit == "proximo":
                    _bg, _bd, _ico, _lbl = "#78350f", "#f59e0b", "🟡", "PRÓXIMA"
                else:
                    _bg, _bd, _ico, _lbl = "#14532d", "#22c55e", "🟢", "EM DIA"

                _det = " · ".join(_msgs)
                st.markdown(f"""
                <div style='background:{_bg};border-radius:10px;padding:10px 16px;
                border-left:4px solid {_bd};margin:4px 0;'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                <div>
                <span style='color:#fff;font-weight:700;font-size:14px;'>{_ico} {_rev.get('maquina','')}</span>
                <span style='color:rgba(255,255,255,0.7);font-size:13px;'> — {_rev.get('tipo','')}</span><br>
                <span style='color:rgba(255,255,255,0.6);font-size:12px;'>
                Última: {_rev.get('data_ultima','')} · a cada {_rev.get('interv_dias',0)} dias / {_rev.get('interv_horas',0)}h · {_det}
                </span>
                </div>
                <span style='color:{_bd};font-weight:800;font-size:12px;letter-spacing:1px;'>{_lbl}</span>
                </div></div>""", unsafe_allow_html=True)

                _re1, _re2, _re3 = st.columns([2, 2, 3])
                if _re1.button("✅ Marcar como revisada hoje", key=f"revok_{_rev.get('id')}"):
                    # Puxa as peças fixas da máquina para registrar no histórico desta revisão
                    _maq_da_rev = next((m for m in _maqs_r if m.get("id") == _rev.get("maq_id")), None)
                    _pecas_usadas = list(_maq_da_rev.get("pecas", [])) if _maq_da_rev else []
                    for _r2 in st.session_state.maquinas_revisoes:
                        if _r2.get("id") == _rev.get("id"):
                            _r2["data_ultima"] = _hoje.strftime("%Y-%m-%d")
                            _r2["horim_ultima"] = float(_horim_now)
                            _r2.setdefault("historico", []).append({
                                "data":  _hoje.strftime("%d/%m/%Y"),
                                "horim": float(_horim_now),
                                "pecas": _pecas_usadas,
                            })
                    salvar_dados_iaagro()
                    success_box("✅ Revisão registrada! Ciclo reiniciado e peças salvas no histórico.")
                    st.rerun()
                if _re3.button("🗑️ Remover programação", key=f"revdel_{_rev.get('id')}"):
                    st.session_state.maquinas_revisoes = [
                        _r2 for _r2 in st.session_state.maquinas_revisoes
                        if _r2.get("id") != _rev.get("id")
                    ]
                    salvar_dados_iaagro()
                    st.rerun()

                # ── Histórico de revisões feitas (com peças de cada uma) ──
                _hist_rev = _rev.get("historico", [])
                if _hist_rev:
                    with st.expander(f"📋 Histórico de revisões feitas ({len(_hist_rev)})"):
                        for _h in reversed(_hist_rev):
                            _pcs_h = _h.get("pecas", [])
                            _pcs_txt = ", ".join(
                                f"{p.get('codigo','')} {p.get('nome','')}".strip() for p in _pcs_h
                            ) if _pcs_h else "sem peças registradas"
                            st.markdown(
                                f"**{_h.get('data','')}** · {_h.get('horim',0):,.0f}h — {_pcs_txt}"
                            )



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
                        btn_pano = round(39.90 * 12 * 0.85)
                        btn_preco = 39.90
                    else:  # premium
                        btn_lmes = MP_LINK_PREMIUM_MES
                        btn_lano = MP_LINK_PREMIUM_ANO
                        btn_pano = round(99.90 * 12 * 0.85)
                        btn_preco = 99.90
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

        # Resumo do que está no backup — confirma que não está vazio antes de baixar
        _n_areas   = len(st.session_state.get("areas", []))
        _n_estoque = len(st.session_state.get("estoque", []))
        _n_aplic   = len(st.session_state.get("aplicacoes", []))
        _n_dre     = len(st.session_state.get("dre_registros", []))
        _n_hist    = len(st.session_state.get("historico_produtividade", []))
        _bk_vazio  = (_n_areas + _n_estoque + _n_aplic + _n_dre) == 0
        if _bk_vazio:
            st.markdown('''<div style="background:#7f1d1d;color:#fff;padding:11px 14px;
            border-radius:8px;font-weight:700;margin:4px 0 12px 0;font-size:13px;">
            🛑 Atenção: seus dados aparecem VAZIOS agora. Se você tem dados cadastrados,
            NÃO baixe este backup (ele salvaria vazio) e NÃO restaure nada — recarregue
            a página primeiro para os dados voltarem.
            </div>''', unsafe_allow_html=True)
        else:
            st.markdown(f'''<div style="background:#14532d;color:#d1fae5;padding:11px 14px;
            border-radius:8px;font-weight:600;margin:4px 0 12px 0;font-size:13px;">
            ✅ Este backup contém: <b>{_n_areas}</b> área(s) · <b>{_n_estoque}</b> item(ns) de estoque ·
            <b>{_n_aplic}</b> aplicação(ões) · <b>{_n_dre}</b> lançamento(s) financeiro(s) ·
            <b>{_n_hist}</b> registro(s) de produtividade.
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

# ── PWA — IAAgro Pro — manifest forçado via JS ────────────────────────────
_IC192 = "data:image/png;base64,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"
_IC512 = "data:image/png;base64,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"
st.markdown(f"""
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="IAAgro Pro">
<meta name="application-name" content="IAAgro Pro">
<meta name="theme-color" content="#22c55e">
<link rel="apple-touch-icon" sizes="192x192" href="{_IC192}">
<link rel="apple-touch-icon" sizes="512x512" href="{_IC512}">
<link rel="icon" type="image/png" sizes="192x192" href="{_IC192}">
<script>
(function forcePWA() {{
  // Remove qualquer manifest existente
  document.querySelectorAll('link[rel="manifest"]').forEach(el => el.remove());
  // Cria novo manifest com ícone embutido
  var manifest = {{
    "name": "IAAgro Pro",
    "short_name": "IAAgro",
    "description": "Gestão agrícola inteligente",
    "start_url": window.location.origin + window.location.pathname,
    "display": "standalone",
    "background_color": "#0d2137",
    "theme_color": "#22c55e",
    "orientation": "portrait-primary",
    "icons": [
      {{"src": "{_IC192}", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"}},
      {{"src": "{_IC512}", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}}
    ]
  }};
  var blob = new Blob([JSON.stringify(manifest)], {{type: "application/manifest+json"}});
  var url  = URL.createObjectURL(blob);
  var link = document.createElement("link");
  link.rel  = "manifest";
  link.href = url;
  document.head.appendChild(link);
  // Service Worker mínimo via blob
  if ('serviceWorker' in navigator) {{
    var swCode = 'self.addEventListener("install",e=>self.skipWaiting());self.addEventListener("activate",e=>self.clients.claim());';
    var swBlob = new Blob([swCode], {{type: "text/javascript"}});
    var swUrl  = URL.createObjectURL(swBlob);
    navigator.serviceWorker.register(swUrl, {{scope: "/"}}).catch(function(){{}});
  }}
}})();
</script>
""", unsafe_allow_html=True)

# ── Persiste token nos query_params e sessionStorage para sobreviver reload ──
if (st.session_state.get("sb_token") and st.session_state.get("sb_user_id")
        and st.session_state.get("sb_manter_login", True)):
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
            st.query_params["_rf1"] = _rf[:200]
            st.query_params["_rf2"] = _rf[200:400]
            st.query_params["_rf3"] = _rf[400:]
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
    # Persiste também no localStorage (sobrevive ao fechamento do navegador),
    # mas só uma vez por sessão pra não recriar o componente a cada render.
    if not st.session_state.get("_ls_persistido"):
        _salvar_sessao_local(_uid, _pl, _nm, _tk, _rf)
        st.session_state["_ls_persistido"] = True

