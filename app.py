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

# ─────────────────────────────────────────────
# API KEY ANTHROPIC — lê do Streamlit Secrets
# ou variável de ambiente (para uso local)
# ─────────────────────────────────────────────
def get_anthropic_headers():
    """Retorna headers completos para a API Anthropic, incluindo a chave."""
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    return {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }

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
# PWA — manifest + ícone + meta tags mobile
# ─────────────────────────────────────────────
st.markdown("""
<link rel="manifest" href="/app/static/manifest.json">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="IAAgro Pro">
<meta name="theme-color" content="#22c55e">
<link rel="apple-touch-icon" href="/app/static/IAAgrologo.jpeg">
""", unsafe_allow_html=True)

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
        "notas_fiscal":       st.session_state.get("notas_fiscal", []),
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
        st.session_state.notas_fiscal        = dados.get("notas_fiscal", [])
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
    """Busca cotação real do dólar via AwesomeAPI (gratuita, sem chave)."""
    try:
        r = requests.get(
            "https://economia.awesomeapi.com.br/json/last/USD-BRL",
            timeout=6, headers={"User-Agent": "iaagro/1.0"}
        )
        if r.status_code == 200:
            d = r.json()
            bid = float(d["USDBRL"]["bid"])
            return {"preco": round(bid, 4), "fonte": "AwesomeAPI (tempo real)", "horario": d["USDBRL"].get("create_date","")}
    except Exception:
        pass
    return {"preco": 5.80, "fonte": "Fallback offline"}

def buscar_precos_ia_cepea():
    """Usa Claude para buscar cotações CEPEA/ESALQ via web search em tempo real."""
    try:
        prompt = """Pesquise os preços atuais das seguintes commodities agrícolas no mercado brasileiro (CEPEA/ESALQ ou B3, data de hoje):
- Soja (saca 60kg, Paraná ou Mato Grosso)
- Milho (saca 60kg, Paraná ou Mato Grosso)
- Trigo (saca 60kg, Paraná)
- Café arábica (saca 60kg, CEPEA)
- Algodão (@/lb ou R$/arroba, CEPEA)
- Boi gordo (arroba, CEPEA, São Paulo)
- Arroz em casca (saca 50kg, Rio Grande do Sul)

Retorne APENAS um JSON válido, sem explicações, sem markdown, sem backticks, exatamente neste formato:
{
  "soja_sc":    {"preco": 0.0, "unidade": "R$/sc 60kg", "praça": "PR"},
  "milho_sc":   {"preco": 0.0, "unidade": "R$/sc 60kg", "praça": "PR"},
  "trigo_sc":   {"preco": 0.0, "unidade": "R$/sc 60kg", "praça": "PR"},
  "cafe_sc":    {"preco": 0.0, "unidade": "R$/sc 60kg", "praça": "SP"},
  "algodao_at": {"preco": 0.0, "unidade": "R$/@",       "praça": "MT"},
  "boi_at":     {"preco": 0.0, "unidade": "R$/@",       "praça": "SP"},
  "arroz_sc":   {"preco": 0.0, "unidade": "R$/sc 50kg", "praça": "RS"},
  "fonte": "CEPEA/ESALQ",
  "data": "DD/MM/AAAA"
}"""

        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=get_anthropic_headers(),
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 600,
                "tools": [{"type": "web_search_20250305", "name": "web_search"}],
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=40
        )
        if resp.status_code == 200:
            texto = ""
            for bloco in resp.json().get("content", []):
                if bloco.get("type") == "text":
                    texto += bloco.get("text", "")
            # Limpar e parsear JSON
            texto = texto.strip()
            # Remover possíveis backticks ou prefixo "json"
            if "```" in texto:
                texto = texto.split("```")[1]
                if texto.startswith("json"):
                    texto = texto[4:]
            # Extrair só o JSON (entre { })
            inicio = texto.find("{")
            fim    = texto.rfind("}") + 1
            if inicio >= 0 and fim > inicio:
                dados = json.loads(texto[inicio:fim])
                dados["_fonte_ia"] = True
                return dados
    except Exception:
        pass
    return None

def buscar_precos_commodities():
    """Busca preços reais: dólar via AwesomeAPI + grãos via IA/CEPEA."""
    resultado = {}

    # 1. Dólar em tempo real (AwesomeAPI — gratuita)
    resultado["dolar"] = buscar_dolar_awesomeapi()

    # 2. Grãos via IA + web search (CEPEA/ESALQ)
    dados_ia = buscar_precos_ia_cepea()
    if dados_ia:
        fonte_ia = dados_ia.get("fonte", "CEPEA via IA")
        data_ia  = dados_ia.get("data", "")
        label    = f"{fonte_ia} — {data_ia}" if data_ia else fonte_ia

        for chave in ["soja_sc","milho_sc","trigo_sc","cafe_sc","algodao_at","boi_at","arroz_sc"]:
            if chave in dados_ia and isinstance(dados_ia[chave], dict):
                resultado[chave] = {
                    "preco":  float(dados_ia[chave].get("preco", 0)),
                    "unidade":dados_ia[chave].get("unidade",""),
                    "praca":  dados_ia[chave].get("praça",""),
                    "fonte":  label,
                }
    else:
        # Fallback offline com valores de referência recentes (Mai/2026)
        resultado.setdefault("soja_sc",    {"preco": 138.0, "unidade": "R$/sc 60kg", "praca": "PR",  "fonte": "Referência offline"})
        resultado.setdefault("milho_sc",   {"preco":  72.0, "unidade": "R$/sc 60kg", "praca": "PR",  "fonte": "Referência offline"})
        resultado.setdefault("trigo_sc",   {"preco":  98.0, "unidade": "R$/sc 60kg", "praca": "PR",  "fonte": "Referência offline"})
        resultado.setdefault("cafe_sc",    {"preco": 2100.0,"unidade": "R$/sc 60kg", "praca": "SP",  "fonte": "Referência offline"})
        resultado.setdefault("algodao_at", {"preco":  118.0,"unidade": "R$/@",       "praca": "MT",  "fonte": "Referência offline"})
        resultado.setdefault("boi_at",     {"preco":  310.0,"unidade": "R$/@",       "praca": "SP",  "fonte": "Referência offline"})
        resultado.setdefault("arroz_sc",   {"preco":   72.0,"unidade": "R$/sc 50kg", "praca": "RS",  "fonte": "Referência offline"})

    return resultado

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
        "harvest_historico":   st.session_state.get("harvest_historico", []),
        "receituarios":        st.session_state.get("receituarios", []),
        "notas_fiscal":        st.session_state.get("notas_fiscal", []),
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
if "notas_fiscal" not in st.session_state:
    st.session_state.notas_fiscal = dados_carregados.get("notas_fiscal", [])

# ── Mapa de Colheita IA — inicialização global ──────────────────
if "harvest_df"        not in st.session_state: st.session_state.harvest_df        = None
if "harvest_analise"   not in st.session_state: st.session_state.harvest_analise   = None
if "harvest_arquivo"   not in st.session_state: st.session_state.harvest_arquivo   = ""
if "harvest_historico" not in st.session_state: st.session_state.harvest_historico = dados_carregados.get("harvest_historico", [])
if "clima_data"        not in st.session_state: st.session_state.clima_data        = None
if "precos_data"       not in st.session_state: st.session_state.precos_data       = None
if "receituarios"      not in st.session_state: st.session_state.receituarios      = dados_carregados.get("receituarios", [])

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
        "⏱️ Prazo de Carência",
        "📋 Ordem de Serviço",
        "💹 Dashboard Financeiro",
        "📅 Calendário Agrícola",
        "🗺️ Mapa de Colheita IA",
        "📜 Receituário Agronômico",
        "📊 Comparativo de Safras",
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
    st.header("🧪 Análise de Solo")

    # ── CSS upload ──────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploader"] section > div,
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
        font-size: 14px !important;
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
        stroke: #22c55e !important;
    }
    </style>
    """, unsafe_allow_html=True)

    tab_manual, tab_ocr, tab_foto = st.tabs([
        "📋 Inserir / Editar Dados",
        "📄 OCR — Ler Laudo Automaticamente",
        "📷 Foto do Talhão",
    ])

    # ════════════════════════════════════════════════════════════════
    # TAB 1 — INSERÇÃO MANUAL (conteúdo original de Análise de Solo)
    # ════════════════════════════════════════════════════════════════
    with tab_manual:
        uploaded_file = st.file_uploader("📄 Upload planilha de análise (xlsx/csv)", type=["xlsx","csv"], key="solo_upload_planilha")
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".csv"):
                df_upload = pd.read_csv(uploaded_file)
            else:
                df_upload = pd.read_excel(uploaded_file)
            success_box("✅ Planilha carregada com sucesso!")
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

            if st.button("Salvar Análise", key="btn_salvar_analise_manual"):
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
                    nota_s  = calcular_nota(st.session_state.dados)
                    score_s, classe_s, _ = score_solo(st.session_state.dados)
                    id_area_atual = st.session_state.dados.get("id_area","")
                    if id_area_atual:
                        salvar_analise_solo_db(id_area_atual, st.session_state.dados, nota_s, score_s, classe_s)
                    checar_alertas_estoque()
                    success_box("Análise salva na área ativa e registrada no histórico!")

    # ════════════════════════════════════════════════════════════════
    # TAB 2 — OCR: leitura automática do laudo
    # ════════════════════════════════════════════════════════════════
    with tab_ocr:
        st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
        ℹ️ Faça upload do seu laudo de solo (PDF ou imagem JPG/PNG) e o sistema tentará
        extrair os valores automaticamente usando OCR e preenchê-los na análise de solo.
        </div>''', unsafe_allow_html=True)

        tipo_arquivo = st.radio("Tipo de arquivo", ["📄 PDF", "🖼️ Imagem (JPG/PNG)"],
                                horizontal=True, key="ocr_tipo")

        texto_ocr  = ""
        campos_ocr = {}

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
                        error_box('Carregue uma área primeiro em "Áreas Cadastradas".')
                    else:
                        st.session_state.dados.update(campos_editados)
                        atualizar_area_atual()
                        salvar_dados_iaagro()
                        success_box(f"{len(campos_editados)} campos importados! Confira na aba 'Inserir / Editar Dados'.")
            else:
                warning_box("Não foi possível detectar valores automaticamente. Verifique se o laudo está legível.")
                with st.expander("💡 Dicas para melhor resultado"):
                    st.markdown("""
                    - Use laudos com texto digital (não escaneados em baixa resolução)
                    - Laudos da EMBRAPA, IAC e laboratórios com formato padrão funcionam melhor
                    - Para imagens, tire a foto com boa iluminação e sem sombras
                    - O OCR reconhece: pH, Fósforo, Potássio, Cálcio, Magnésio, Alumínio, Argila, CTC, MO
                    """)

    # ════════════════════════════════════════════════════════════════
    # TAB 3 — FOTO DO TALHÃO
    # ════════════════════════════════════════════════════════════════
    with tab_foto:
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
        else:
            info_box("Nenhuma foto adicionada ainda para a área ativa.")


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
elif menu == "Estoque de Insumos":
    st.header("📦 Estoque de Insumos")

    if "bc_codigo"     not in st.session_state: st.session_state.bc_codigo     = ""
    if "bc_produto"    not in st.session_state: st.session_state.bc_produto    = None
    if "notas_fiscal"  not in st.session_state: st.session_state.notas_fiscal  = []
    if "nf_itens_temp" not in st.session_state: st.session_state.nf_itens_temp = []

    tab_cadastro, tab_leitor, tab_notas, tab_ir = st.tabs([
        "➕ Cadastrar / Visualizar",
        "📷 Leitor de Código de Barras",
        "🧾 Notas Fiscais",
        "📊 Relatório IR Rural",
    ])

    # ════════════════════════════════════════════════════════════════
    # TAB 1 — CADASTRAR / VISUALIZAR (conteúdo original do Estoque)
    # ════════════════════════════════════════════════════════════════
    with tab_cadastro:
        st.subheader("➕ Cadastrar Produto")

        st.markdown("""
        <style>
        div[data-baseweb="select"] > div {
            background-color: #0d1b2a !important;
            border: 2px solid #22c55e !important;
            border-radius: 10px !important;
            color: #f1f5f9 !important;
        }
        div[data-baseweb="select"] > div:focus-within {
            border-color: #4ade80 !important;
            box-shadow: 0 0 0 3px rgba(34,197,94,0.18) !important;
        }
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div,
        div[data-baseweb="select"] input {
            color: #f1f5f9 !important;
            background-color: transparent !important;
        }
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input {
            background-color: #0d1b2a !important;
            color: #f1f5f9 !important;
            border: 2px solid #22c55e !important;
            border-radius: 10px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
        }
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stNumberInput"] input:focus {
            border-color: #4ade80 !important;
            box-shadow: 0 0 0 3px rgba(34,197,94,0.18) !important;
        }
        div[data-testid="stNumberInput"] button {
            background-color: #0f3460 !important;
            border-color: #22c55e !important;
            color: #22c55e !important;
        }
        div[data-testid="stTextInput"] label,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stNumberInput"] label,
        div[data-testid="stTextArea"] label {
            color: #22c55e !important;
            font-weight: 700 !important;
            font-size: 13px !important;
        }
        div[data-testid="stButton"] > button {
            background-color: #0f3460 !important;
            border: 2px solid #22c55e !important;
            border-radius: 10px !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 13px !important;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #22c55e !important;
            color: #0d1b2a !important;
        }
        div[data-testid="stFileUploader"] > div {
            background-color: #0d1b2a !important;
            border: 2px dashed #22c55e !important;
            border-radius: 12px !important;
        }
        .autocomplete-container { position: relative; margin-bottom: 6px; }
        .autocomplete-dropdown {
            position: absolute; top: 100%; left: 0; right: 0;
            background: #0d1b2a; border: 2px solid #22c55e;
            border-radius: 10px; max-height: 260px; overflow-y: auto;
            z-index: 9999; box-shadow: 0 8px 32px rgba(0,0,0,0.6);
        }
        .autocomplete-item {
            display: flex; align-items: center; justify-content: space-between;
            padding: 9px 14px; cursor: pointer;
            border-left: 3px solid transparent; transition: all 0.12s;
            background: #0d1b2a;
        }
        .autocomplete-item:hover { background: #0f3460 !important; border-left: 3px solid #22c55e !important; }
        .autocomplete-item .prod-nome { font-size: 13px; font-weight: 600; color: #f1f5f9; }
        .autocomplete-item .prod-ia   { font-size: 10px; color: #93c5fd; margin-top: 2px; }
        .autocomplete-item .prod-badge {
            font-size: 10px; font-weight: 700; padding: 2px 8px;
            border-radius: 20px; white-space: nowrap; margin-left: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

        if "ac_query"       not in st.session_state: st.session_state.ac_query       = ""
        if "ac_selecionado" not in st.session_state: st.session_state.ac_selecionado = None
        if "ac_fab"         not in st.session_state: st.session_state.ac_fab         = "Todos"

        fabricantes = ["Todos", "BASF", "Syngenta", "Bayer", "UPL", "Timac Agro", "Mosaic",
                       "Corteva", "FMC", "ADAMA", "Ouro Fino", "Ihara", "Nortox", "Outros"]
        FAB_ESTILOS = {
            "Todos":      {"bg":"#166534", "border":"#22c55e", "emoji":"🔎"},
            "BASF":       {"bg":"#1e3a8a", "border":"#93c5fd", "emoji":"🔵"},
            "Syngenta":   {"bg":"#14532d", "border":"#86efac", "emoji":"🟢"},
            "Bayer":      {"bg":"#7f1d1d", "border":"#fca5a5", "emoji":"🔴"},
            "UPL":        {"bg":"#92400e", "border":"#fcd34d", "emoji":"🟠"},
            "Timac Agro": {"bg":"#6b21a8", "border":"#f0abfc", "emoji":"🟣"},
            "Mosaic":     {"bg":"#065f46", "border":"#6ee7b7", "emoji":"🌊"},
            "Corteva":    {"bg":"#164e63", "border":"#67e8f9", "emoji":"🔷"},
            "FMC":        {"bg":"#1e1b4b", "border":"#a5b4fc", "emoji":"🟦"},
            "ADAMA":      {"bg":"#365314", "border":"#bef264", "emoji":"🌿"},
            "Ouro Fino":  {"bg":"#713f12", "border":"#fde68a", "emoji":"🟡"},
            "Ihara":      {"bg":"#4a044e", "border":"#f9a8d4", "emoji":"🌸"},
            "Nortox":     {"bg":"#134e4a", "border":"#5eead4", "emoji":"🌀"},
            "Outros":     {"bg":"#374151", "border":"#9ca3af", "emoji":"⚪"},
        }

        st.markdown("**🏭 Filtrar por Fabricante:**")
        cols_fab = st.columns(len(fabricantes))
        for i, fab in enumerate(fabricantes):
            est   = FAB_ESTILOS[fab]
            ativo = st.session_state.ac_fab == fab
            borda = f'4px solid {est["border"]}' if ativo else f'2px solid {est["border"]}55'
            opac  = "1.0" if ativo else "0.65"
            sombra= f'0 0 10px {est["border"]}88' if ativo else "none"
            with cols_fab[i]:
                with st.form(key=f"form_fab_{fab}", border=False):
                    st.markdown(
                        f'<div style="background:{est["bg"]};border:{borda};border-radius:10px;'
                        f'padding:8px 4px;text-align:center;font-size:12px;font-weight:900;'
                        f'color:#ffffff;opacity:{opac};box-shadow:{sombra};letter-spacing:0.3px;'
                        f'margin-bottom:2px;">{est["emoji"]} {fab}</div>',
                        unsafe_allow_html=True
                    )
                    if st.form_submit_button("✔", use_container_width=True):
                        st.session_state.ac_fab = fab
                        st.session_state.ac_query = ""
                        st.session_state.ac_selecionado = None
                        st.rerun()

        fab_ativo = st.session_state.ac_fab
        qtd_fab = len([p for p in CATALOGO_PRODUTOS if fab_ativo == "Todos" or p["fab"] == fab_ativo])
        st.markdown(f'<div style="background:#0f3460;color:#93c5fd;padding:7px 14px;border-radius:8px;'
                    f'font-size:12px;font-weight:700;margin:4px 0 10px 0;">'
                    f'🔎 Fabricante ativo: <b>{fab_ativo}</b> — {qtd_fab} produtos disponíveis</div>',
                    unsafe_allow_html=True)

        query_input = st.text_input(
            "🔍 Nome comercial, ingrediente ativo ou categoria",
            value=st.session_state.ac_query,
            placeholder="Ex: Fox Xpro, glifosato, fungicida...",
            key="input_busca_produto"
        )
        if query_input != st.session_state.ac_query:
            st.session_state.ac_query = query_input
            if st.session_state.ac_selecionado and query_input != st.session_state.ac_selecionado["nome"]:
                st.session_state.ac_selecionado = None

        catalogo_filtrado = CATALOGO_PRODUTOS if fab_ativo == "Todos" else [
            p for p in CATALOGO_PRODUTOS if p["fab"] == fab_ativo
        ]

        if st.session_state.ac_query and not st.session_state.ac_selecionado:
            q = st.session_state.ac_query.lower()
            starts   = [p for p in catalogo_filtrado if p["nome"].lower().startswith(q)]
            contains = [p for p in catalogo_filtrado
                        if not p["nome"].lower().startswith(q)
                        and (q in p["nome"].lower() or q in p["ia"].lower() or q in p["cat"].lower())]
            resultados = (starts + contains)[:20]
            if resultados:
                FAB_EM = {"BASF":"🔵","Syngenta":"🟢","Bayer":"🔴","UPL":"🟠",
                          "Timac Agro":"🟣","Mosaic":"🌊","Outros":"⚪"}
                CAT_EM = {"Fungicida":"🍄","Herbicida":"🌿","Inseticida":"🐛",
                          "Acaricida":"🕷️","Nematicida":"🪱","Fungicida Biológico":"🌱",
                          "Inseticida Biológico":"🦠","Foliar / Nutrição":"💧",
                          "Tratamento de Sementes":"🌾","Regulador de Crescimento":"📈",
                          "Adjuvante":"⚗️","Fertilizante":"🧪","Bioestimulante":"✨"}
                st.markdown(f'<div style="background:#0f3460;color:#22c55e;padding:6px 14px;'
                            f'border-radius:8px 8px 0 0;font-size:11px;font-weight:800;letter-spacing:1px;">'
                            f'🌿 {len(resultados)} RESULTADO(S) — clique para selecionar</div>',
                            unsafe_allow_html=True)
                opcoes_labels = []
                for p in resultados:
                    em_fab = FAB_EM.get(p["fab"], "⚪")
                    em_cat = CAT_EM.get(p["cat"], "🌱")
                    opcoes_labels.append(f"{em_cat} {p['nome']}  |  {em_fab} {p['fab']}  ·  {p['cat']}  —  {p['ia'][:50]}")
                escolha_idx = st.radio(
                    "Resultados:", range(len(opcoes_labels)),
                    format_func=lambda i: opcoes_labels[i],
                    key="radio_produto_catalogo", label_visibility="collapsed"
                )
                if st.button("✅ Usar este produto", key="btn_usar_produto", use_container_width=True):
                    prod_sel = resultados[escolha_idx]
                    st.session_state.ac_selecionado = prod_sel
                    st.session_state.ac_query = prod_sel["nome"]
                    st.rerun()
            else:
                st.markdown(f'<div style="background:#1e293b;color:#f87171;padding:10px 14px;'
                            f'border-radius:8px;font-size:13px;font-weight:600;margin:4px 0;">'
                            f'❌ Nenhum produto encontrado para "<b>{st.session_state.ac_query}</b>"</div>',
                            unsafe_allow_html=True)

        if st.session_state.ac_selecionado:
            p = st.session_state.ac_selecionado
            fab_bg = {"BASF":"#1e3a8a","Syngenta":"#14532d","Bayer":"#7f1d1d","UPL":"#78350f","Timac Agro":"#6b21a8","Mosaic":"#065f46","Outros":"#1e293b"}.get(p["fab"],"#1e293b")
            fab_tx = {"BASF":"#93c5fd","Syngenta":"#86efac","Bayer":"#fca5a5","UPL":"#fcd34d","Timac Agro":"#f0abfc","Mosaic":"#6ee7b7","Outros":"#94a3b8"}.get(p["fab"],"#94a3b8")
            fab_em = {"BASF":"🔵","Syngenta":"🟢","Bayer":"🔴","UPL":"🟠","Timac Agro":"🟣","Mosaic":"🌊","Outros":"⚪"}.get(p["fab"],"⚪")
            cat_em = {"Fungicida":"🍄","Herbicida":"🌿","Inseticida":"🐛","Acaricida":"🕷️",
                      "Tratamento de Sementes":"🌾","Foliar / Nutrição":"💧",
                      "Regulador de Crescimento":"📈","Adjuvante":"⚗️","Nematicida":"🪱",
                      "Inseticida Biológico":"🦠","Bioestimulante":"✨"}.get(p["cat"],"🌱")
            st.markdown(f"""
            <div style="background:{fab_bg};border:2px solid {fab_tx}33;border-radius:12px;
            padding:12px 16px;margin:6px 0 12px 0;display:flex;align-items:center;gap:12px;">
                <div style="font-size:26px;">{cat_em}</div>
                <div style="flex:1;">
                    <div style="color:#ffffff;font-weight:800;font-size:15px;">{p['nome']}</div>
                    <div style="color:{fab_tx};font-size:12px;margin-top:3px;">{fab_em} {p['fab']} · {p['cat']}</div>
                    <div style="color:#94a3b8;font-size:11px;margin-top:2px;">I.A.: {p['ia']}</div>
                </div>
            </div>""", unsafe_allow_html=True)
            if st.button("🔄 Trocar produto", key="btn_trocar_produto"):
                st.session_state.ac_selecionado = None
                st.session_state.ac_query = ""
                st.rerun()
            nome_insumo = p["nome"]
            cat_map = {
                "Fungicida":"Fungicida","Herbicida":"Herbicida","Inseticida":"Inseticida",
                "Acaricida":"Outro","Nematicida":"Outro","Fungicida Biológico":"Biológico",
                "Inseticida Biológico":"Biológico","Bioestimulante":"Foliar",
                "Foliar / Nutrição":"Foliar","Regulador de Crescimento":"Outro",
                "Adjuvante":"Adjuvante","Tratamento de Sementes":"Outro",
                "Fertilizante":"Fertilizante",
            }
            cat_sugerida = cat_map.get(p["cat"], "Outro")
        else:
            nome_insumo  = st.session_state.ac_query if st.session_state.ac_query else ""
            cat_sugerida = "Fungicida"

        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            nome_final = st.text_input("Nome do produto / insumo", value=nome_insumo, key="nome_insumo_final")
            categoria  = st.selectbox("Categoria", [
                "Fertilizante","Cloreto de Potássio","Ureia","Fungicida","Inseticida",
                "Herbicida","Biológico","Foliar","Semente","Calcário","Gesso Agrícola","Adjuvante","Outro"
            ], index=["Fertilizante","Cloreto de Potássio","Ureia","Fungicida","Inseticida",
                      "Herbicida","Biológico","Foliar","Semente","Calcário","Gesso Agrícola","Adjuvante","Outro"
                     ].index(cat_sugerida) if cat_sugerida in [
                      "Fertilizante","Cloreto de Potássio","Ureia","Fungicida","Inseticida",
                      "Herbicida","Biológico","Foliar","Semente","Calcário","Gesso Agrícola","Adjuvante","Outro"
                     ] else 0)
            cultura    = st.selectbox("Cultura", ["Soja","Milho","Ambos"], key="cultura_estoque")
            litros_ha  = st.number_input("Litros de calda por hectare", min_value=0.0, value=75.0, key="litros_ha_estoque")
            capacidade_tanque = st.number_input("Capacidade do tanque (L)", min_value=0, value=2000, key="tanque_estoque")
        with col2:
            quantidade  = st.number_input("Quantidade em estoque", min_value=0.0, value=0.0)
            unidade     = st.selectbox("Unidade do estoque", ["kg","ton","litros","sacos","galões","unidades"])
        with col3:
            valor_unitario = st.number_input("Valor unitário R$", min_value=0.0, value=0.0)
            estoque_minimo = st.number_input("Estoque mínimo", min_value=0.0, value=0.0)

        # Campo código de barras no cadastro manual
        cod_barras_manual = st.text_input("Código de Barras (opcional)", placeholder="Deixe em branco ou escaneie", key="cod_barras_manual")
        observacao = st.text_area("Observação")

        if st.button("Adicionar Produto ao Estoque"):
            nome_usar = nome_final.strip() if nome_final.strip() else nome_insumo.strip()
            if not nome_usar:
                error_box("Digite ou selecione o nome do produto.")
            else:
                novo_item = {
                    "Insumo": nome_usar, "Categoria": categoria,
                    "Quantidade": quantidade, "Unidade": unidade,
                    "Valor Unitário R$": valor_unitario,
                    "Valor Total R$": quantidade * valor_unitario,
                    "Estoque Mínimo": estoque_minimo,
                    "Observação": observacao, "Cultura": cultura,
                    "Dose ha": dose_ha, "Litros ha": litros_ha,
                    "Tanque litros": capacidade_tanque,
                    "Fabricante": st.session_state.ac_selecionado["fab"] if st.session_state.ac_selecionado else "",
                    "Ingrediente Ativo": st.session_state.ac_selecionado["ia"] if st.session_state.ac_selecionado else "",
                    "Codigo_Barras": cod_barras_manual.strip(),
                }
                st.session_state.estoque.append(novo_item)
                st.session_state.ac_selecionado = None
                st.session_state.ac_query = ""
                salvar_dados_iaagro()
                success_box(f"✅ {nome_usar} adicionado ao estoque.")

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
            col4.metric("Itens cadastrados",       len(tabela_estoque))
            col5.metric("Valor total em estoque",  f"R$ {tabela_estoque['Valor Total R$'].sum():,.2f}")
            col6.metric("Itens com estoque baixo", len(tabela_estoque[tabela_estoque["Status"] == "Estoque baixo"]))

    # ════════════════════════════════════════════════════════════════
    # TAB 2 — LEITOR DE CÓDIGO DE BARRAS
    # ════════════════════════════════════════════════════════════════
    with tab_leitor:
        st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
        ℹ️ Use a câmera do celular para escanear o código de barras, ou conecte um leitor USB.
        </div>''', unsafe_allow_html=True)

        col_modo1, col_modo2 = st.columns(2)
        with col_modo1:
            bc_modo = st.selectbox("Modo de operação", ["Entrada de estoque", "Consultar produto"], key="bc_modo_sel")
        with col_modo2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('''<div style="background:#0f3460;color:#93c5fd;padding:9px 14px;
            border-radius:8px;font-size:12px;font-weight:700;">
            📱 Câmera ou 💻 Leitor USB — ambos funcionam!
            </div>''', unsafe_allow_html=True)

        st.divider()

        # ── Câmera do celular ─────────────────────────────────────────
        st.subheader("📷 Escanear pela Câmera")
        try:
            from streamlit_barcode_reader import st_barcode_reader
            codigo_camera = st_barcode_reader()
            if codigo_camera and codigo_camera.strip():
                st.session_state.bc_codigo = codigo_camera.strip()
                produto_encontrado = None
                for item in st.session_state.estoque:
                    if item.get("Codigo_Barras", "") == codigo_camera.strip():
                        produto_encontrado = item
                        break
                st.session_state.bc_produto = produto_encontrado
                success_box(f"✅ Código lido pela câmera: {codigo_camera}")
        except Exception:
            st.markdown('''<div style="background:#78350f;color:#fff;padding:10px 16px;
            border-radius:8px;border-left:4px solid #f59e0b;font-size:13px;font-weight:600;">
            ⚠️ Scanner de câmera não disponível neste dispositivo. Use o campo abaixo.
            </div>''', unsafe_allow_html=True)

        # ── Leitor USB ou digitação manual ────────────────────────────
        st.subheader("⌨️ Leitor USB ou Digitação Manual")
        codigo_barras = st.text_input(
            "🔍 Aponte o leitor ou digite o código aqui:",
            placeholder="Aguardando leitura...",
            key="bc_input_codigo"
        )
        col_bc1, col_bc2 = st.columns([1, 3])
        with col_bc1:
            buscar_codigo = st.button("🔎 Buscar Produto", key="btn_bc_buscar", use_container_width=True)

        if buscar_codigo and codigo_barras.strip():
            produto_encontrado = None
            for item in st.session_state.estoque:
                if item.get("Codigo_Barras", "") == codigo_barras.strip():
                    produto_encontrado = item
                    break
            st.session_state.bc_codigo  = codigo_barras.strip()
            st.session_state.bc_produto = produto_encontrado

        if st.session_state.bc_codigo:
            st.divider()
            if st.session_state.bc_produto:
                p = st.session_state.bc_produto
                st.markdown(f'''<div style="background:#14532d;color:#fff;padding:15px 18px;
                border-radius:10px;border-left:5px solid #22c55e;font-weight:600;margin:8px 0;">
                ✅ Produto encontrado: <b>{p.get("Insumo","")}</b> |
                Estoque atual: <b>{p.get("Quantidade",0):.1f} {p.get("Unidade","")}</b> |
                Cat: {p.get("Categoria","")} | Fab: {p.get("Fabricante","—")}
                </div>''', unsafe_allow_html=True)

                if bc_modo == "Entrada de estoque":
                    st.subheader("➕ Registrar Entrada")
                    col_e1, col_e2, col_e3 = st.columns(3)
                    with col_e1:
                        qtd_entrada = st.number_input("Quantidade recebida", min_value=0.0, value=0.0, key="bc_qtd_entrada")
                    with col_e2:
                        vl_entrada  = st.number_input("Valor unitário R$", min_value=0.0, value=float(p.get("Valor Unitário R$", 0)), key="bc_vl_entrada")
                    with col_e3:
                        fornec_entr = st.text_input("Fornecedor", key="bc_forn_entrada")
                    nota_ref = st.text_input("Nº Nota Fiscal / Referência", key="bc_nota_ref")

                    if st.button("✅ Confirmar Entrada no Estoque", key="btn_bc_confirmar", use_container_width=True):
                        if qtd_entrada <= 0:
                            error_box("Informe a quantidade recebida.")
                        else:
                            for item in st.session_state.estoque:
                                if item.get("Codigo_Barras","") == st.session_state.bc_codigo:
                                    item["Quantidade"]        += qtd_entrada
                                    item["Valor Unitário R$"]  = vl_entrada
                                    item["Valor Total R$"]     = item["Quantidade"] * vl_entrada
                                    break
                            st.session_state.notas_fiscal.append({
                                "Tipo": "Entrada", "Insumo": p.get("Insumo",""),
                                "Codigo_Barras": st.session_state.bc_codigo,
                                "Quantidade": qtd_entrada, "Unidade": p.get("Unidade",""),
                                "Valor Unitário": vl_entrada,
                                "Valor Total": round(qtd_entrada * vl_entrada, 2),
                                "Fornecedor": fornec_entr, "Numero_NF": nota_ref,
                                "Data": str(date.today()), "Categoria": p.get("Categoria",""),
                                "Categoria_IR": "Custeio — Insumos", "Safra": "",
                            })
                            salvar_dados_iaagro()
                            success_box(f"✅ +{qtd_entrada:.1f} {p.get('Unidade','')} de {p.get('Insumo','')} registrado!")
                            st.session_state.bc_codigo  = ""
                            st.session_state.bc_produto = None
                            st.rerun()
            else:
                st.markdown(f'''<div style="background:#78350f;color:#fff;padding:13px 18px;
                border-radius:10px;border-left:5px solid #f59e0b;font-weight:600;margin:8px 0;">
                ⚠️ Código <b>{st.session_state.bc_codigo}</b> não encontrado. Preencha os dados abaixo para cadastrar.
                </div>''', unsafe_allow_html=True)

                col_n1, col_n2, col_n3 = st.columns(3)
                with col_n1:
                    bc_nome    = st.text_input("Nome do produto*", key="bc_nome_novo")
                    bc_cat     = st.selectbox("Categoria", [
                        "Fertilizante","Cloreto de Potássio","Ureia","Fungicida","Inseticida",
                        "Herbicida","Biológico","Foliar","Semente","Calcário","Gesso Agrícola","Adjuvante","Outro"
                    ], key="bc_cat_novo")
                    bc_cultura = st.selectbox("Cultura", ["Soja","Milho","Ambos"], key="bc_cult_novo")
                with col_n2:
                    bc_qtd     = st.number_input("Quantidade inicial", min_value=0.0, value=0.0, key="bc_qtd_novo")
                    bc_unidade = st.selectbox("Unidade", ["kg","ton","litros","sacos","galões","unidades"], key="bc_uni_novo")
                    bc_minimo  = st.number_input("Estoque mínimo", min_value=0.0, value=0.0, key="bc_min_novo")
                with col_n3:
                    bc_vl  = st.number_input("Valor unitário R$", min_value=0.0, value=0.0, key="bc_vl_novo")
                    bc_fab = st.text_input("Fabricante", key="bc_fab_novo")
                    bc_forn= st.text_input("Fornecedor", key="bc_forn_novo")
                bc_nota_novo = st.text_input("Nº Nota Fiscal", key="bc_nota_novo_nf")

                if st.button("💾 Cadastrar e Registrar Entrada", key="btn_bc_cadastrar", use_container_width=True):
                    if not bc_nome.strip():
                        error_box("Informe o nome do produto.")
                    else:
                        st.session_state.estoque.append({
                            "Insumo": bc_nome.strip(), "Categoria": bc_cat,
                            "Quantidade": bc_qtd, "Unidade": bc_unidade,
                            "Valor Unitário R$": bc_vl, "Valor Total R$": round(bc_qtd * bc_vl, 2),
                            "Estoque Mínimo": bc_minimo, "Observação": "",
                            "Cultura": bc_cultura, "Fabricante": bc_fab,
                            "Ingrediente Ativo": "", "Dose ha": 0.0,
                            "Litros ha": 75.0, "Tanque litros": 2000,
                            "Codigo_Barras": st.session_state.bc_codigo,
                        })
                        st.session_state.notas_fiscal.append({
                            "Tipo": "Entrada", "Insumo": bc_nome.strip(),
                            "Codigo_Barras": st.session_state.bc_codigo,
                            "Quantidade": bc_qtd, "Unidade": bc_unidade,
                            "Valor Unitário": bc_vl, "Valor Total": round(bc_qtd * bc_vl, 2),
                            "Fornecedor": bc_forn, "Numero_NF": bc_nota_novo,
                            "Data": str(date.today()), "Categoria": bc_cat,
                            "Categoria_IR": "Custeio — Insumos", "Safra": "",
                        })
                        salvar_dados_iaagro()
                        success_box(f"✅ {bc_nome} cadastrado com código {st.session_state.bc_codigo}!")
                        st.session_state.bc_codigo  = ""
                        st.session_state.bc_produto = None
                        st.rerun()

        # Histórico de entradas por scanner
        st.divider()
        st.subheader("📋 Histórico de Entradas por Leitor")
        entradas_bc = [n for n in st.session_state.notas_fiscal if n.get("Codigo_Barras")]
        if not entradas_bc:
            info_box("Nenhuma entrada registrada por leitor ainda.")
        else:
            df_bc = pd.DataFrame(entradas_bc)
            st.dataframe(df_bc, use_container_width=True)
            total_bc = df_bc["Valor Total"].sum() if "Valor Total" in df_bc.columns else 0
            st.metric("Valor total de entradas", f"R$ {total_bc:,.2f}")

    # ════════════════════════════════════════════════════════════════
    # TAB 3 — NOTAS FISCAIS
    # ════════════════════════════════════════════════════════════════
    with tab_notas:
        st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
        ℹ️ Registre compras e vendas de insumos. Os lançamentos gerados pelo leitor de código
        de barras aparecem aqui automaticamente.
        </div>''', unsafe_allow_html=True)

        sub_nova, sub_lista = st.tabs(["➕ Nova Nota", "📂 Notas Salvas"])

        with sub_nova:
            st.subheader("➕ Registrar Nova Nota Fiscal / Lançamento")
            col1, col2, col3 = st.columns(3)
            with col1:
                nf_tipo   = st.selectbox("Tipo de Operação", [
                    "Compra de Insumo", "Venda de Produção", "Prestação de Serviço",
                    "Arrendamento Pago", "Arrendamento Recebido", "Devolução", "Outros"
                ], key="nf_tipo")
                nf_fornec = st.text_input("Fornecedor / Destinatário", key="nf_fornec")
                nf_cnpj   = st.text_input("CNPJ / CPF (opcional)", key="nf_cnpj")
            with col2:
                nf_numero = st.text_input("Nº da Nota Fiscal", key="nf_numero")
                nf_data   = st.date_input("Data", key="nf_data")
                nf_safra  = st.text_input("Safra de referência", placeholder="2024/2025", key="nf_safra")
            with col3:
                nf_valor  = st.number_input("Valor Total R$", min_value=0.0, key="nf_valor")
                nf_categ  = st.selectbox("Categoria IR Rural", [
                    "Custeio — Insumos", "Custeio — Defensivos", "Custeio — Sementes",
                    "Custeio — Combustível", "Custeio — Mão de obra",
                    "Investimento — Máquinas", "Investimento — Benfeitorias",
                    "Receita — Venda de produção", "Receita — Arrendamento",
                    "Despesa — Arrendamento", "Outros"
                ], key="nf_categ")
                nf_area_ha = st.number_input("Área referente (ha)", min_value=0.0, key="nf_area_ha")

            nf_obs = st.text_area("Observações / Descrição", key="nf_obs",
                                  placeholder="Ex: Compra de 500kg de ureia para safra de soja 2025...")

            st.markdown("**Itens da nota (opcional):**")
            col_i1, col_i2, col_i3, col_i4 = st.columns([3,1,1,1])
            with col_i1: nf_item_desc = st.text_input("Produto/Serviço", key="nf_item_desc")
            with col_i2: nf_item_qtd  = st.number_input("Qtd", min_value=0.0, value=1.0, key="nf_item_qtd")
            with col_i3: nf_item_uni  = st.selectbox("Un", ["kg","L","sc","un","t","h"], key="nf_item_uni")
            with col_i4: nf_item_vl   = st.number_input("Vl Unit R$", min_value=0.0, key="nf_item_vl")

            col_ia, col_ib = st.columns(2)
            with col_ia:
                if st.button("➕ Adicionar Item", key="btn_nf_add_item"):
                    if nf_item_desc.strip():
                        st.session_state.nf_itens_temp.append({
                            "Produto": nf_item_desc.strip(), "Qtd": nf_item_qtd,
                            "Unidade": nf_item_uni, "Vl Unit R$": nf_item_vl,
                            "Total R$": round(nf_item_qtd * nf_item_vl, 2),
                        })
                        success_box(f"Item '{nf_item_desc}' adicionado.")
            with col_ib:
                if st.button("🗑️ Limpar Itens", key="btn_nf_clear_items"):
                    st.session_state.nf_itens_temp = []

            if st.session_state.nf_itens_temp:
                df_itens_temp = pd.DataFrame(st.session_state.nf_itens_temp)
                st.dataframe(df_itens_temp, use_container_width=True, hide_index=True)
                st.metric("Total dos itens", f"R$ {df_itens_temp['Total R$'].sum():,.2f}")

            st.divider()
            if st.button("💾 Salvar Nota Fiscal", key="btn_salvar_nf", use_container_width=True):
                if not nf_fornec.strip():
                    error_box("Informe o fornecedor / destinatário.")
                elif nf_valor <= 0 and not st.session_state.nf_itens_temp:
                    error_box("Informe o valor total ou adicione itens à nota.")
                else:
                    valor_final = nf_valor if nf_valor > 0 else sum(
                        i["Total R$"] for i in st.session_state.nf_itens_temp
                    )
                    st.session_state.notas_fiscal.append({
                        "Tipo": nf_tipo, "Fornecedor": nf_fornec, "CNPJ_CPF": nf_cnpj,
                        "Numero_NF": nf_numero, "Data": str(nf_data), "Safra": nf_safra,
                        "Valor Total": round(valor_final, 2), "Categoria_IR": nf_categ,
                        "Area_ha": nf_area_ha, "Observacao": nf_obs,
                        "Itens": st.session_state.nf_itens_temp.copy(),
                        "Codigo_Barras": "", "Insumo": "",
                    })
                    st.session_state.nf_itens_temp = []
                    salvar_dados_iaagro()
                    success_box(f"✅ Nota {nf_numero or '(sem número)'} salva! R$ {valor_final:,.2f} — {nf_tipo}")

        with sub_lista:
            st.subheader("📂 Notas Fiscais Salvas")
            if not st.session_state.notas_fiscal:
                info_box("Nenhuma nota registrada ainda.")
            else:
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    tipos_disp   = ["Todos"] + list({n["Tipo"] for n in st.session_state.notas_fiscal})
                    filtro_tipo  = st.selectbox("Filtrar por tipo",  tipos_disp, key="nf_filtro_tipo")
                with col_f2:
                    safras_disp  = ["Todas"] + sorted(
                        list({n.get("Safra","") for n in st.session_state.notas_fiscal if n.get("Safra")}),
                        reverse=True
                    )
                    filtro_safra = st.selectbox("Filtrar por safra", safras_disp, key="nf_filtro_safra")

                notas_filtradas = [
                    n for n in st.session_state.notas_fiscal
                    if (filtro_tipo  == "Todos" or n["Tipo"] == filtro_tipo)
                    and (filtro_safra == "Todas" or n.get("Safra","") == filtro_safra)
                ]
                if not notas_filtradas:
                    warning_box("Nenhuma nota encontrada com os filtros selecionados.")
                else:
                    total_filtro = sum(n.get("Valor Total", 0) for n in notas_filtradas)
                    col_m1, col_m2 = st.columns(2)
                    col_m1.metric("Notas encontradas", len(notas_filtradas))
                    col_m2.metric("Valor total filtrado", f"R$ {total_filtro:,.2f}")

                    for nota in notas_filtradas:
                        with st.expander(f"📄 {nota.get('Tipo','')} | {nota.get('Fornecedor','')} | {nota.get('Data','')} | R$ {nota.get('Valor Total',0):,.2f}"):
                            c1, c2, c3 = st.columns(3)
                            c1.write(f"**Nº NF:** {nota.get('Numero_NF','—')}")
                            c1.write(f"**CNPJ/CPF:** {nota.get('CNPJ_CPF','—')}")
                            c2.write(f"**Safra:** {nota.get('Safra','—')}")
                            c2.write(f"**Categoria IR:** {nota.get('Categoria_IR','—')}")
                            c3.write(f"**Área ref:** {nota.get('Area_ha',0):.1f} ha")
                            c3.write(f"**Cód. Barras:** {nota.get('Codigo_Barras','—')}")
                            if nota.get("Observacao"):
                                st.write(f"**Obs:** {nota.get('Observacao','')}")
                            if nota.get("Itens"):
                                st.dataframe(pd.DataFrame(nota["Itens"]), use_container_width=True, hide_index=True)

                    st.divider()
                    notas_export = [{k: v for k, v in n.items() if k != "Itens"} for n in notas_filtradas]
                    xlsx_nf = exportar_excel({"Notas Fiscais": notas_export})
                    if xlsx_nf:
                        st.download_button(
                            "📥 Exportar Notas para Excel",
                            data=xlsx_nf,
                            file_name=f"notas_fiscais_{date.today()}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )

    # ════════════════════════════════════════════════════════════════
    # TAB 4 — RELATÓRIO IR RURAL
    # ════════════════════════════════════════════════════════════════
    with tab_ir:
        st.subheader("📊 Relatório para Imposto de Renda Rural")
        st.markdown('''<div style="background:#14532d;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #22c55e;font-weight:600;margin:8px 0;">
        ✅ Consolida todas as despesas e receitas por categoria — pronto para o Livro-Caixa
        do IR Rural e compatível com importação no IAAGro.
        </div>''', unsafe_allow_html=True)

        if not st.session_state.notas_fiscal:
            info_box("Nenhum lançamento ainda. Registre notas ou use o leitor de código de barras.")
        else:
            from collections import defaultdict as _dd
            grupos_ir = _dd(list)
            for n in st.session_state.notas_fiscal:
                cat = n.get("Categoria_IR") or n.get("Categoria") or "Outros"
                grupos_ir[cat].append(n)

            resumo_ir = []
            for cat, notas_cat in grupos_ir.items():
                resumo_ir.append({
                    "Categoria":      cat,
                    "Qtd Notas":      len(notas_cat),
                    "Valor Total R$": round(sum(n.get("Valor Total", 0) for n in notas_cat), 2),
                })

            df_resumo_ir = pd.DataFrame(resumo_ir).sort_values("Valor Total R$", ascending=False)
            st.subheader("📋 Resumo por Categoria")
            st.dataframe(df_resumo_ir, use_container_width=True, hide_index=True)

            total_desp = sum(r["Valor Total R$"] for r in resumo_ir
                             if any(x in r["Categoria"] for x in ["Custeio","Investimento","Despesa"]))
            total_rec  = sum(r["Valor Total R$"] for r in resumo_ir if "Receita" in r["Categoria"])
            resultado  = total_rec - total_desp
            c1, c2, c3 = st.columns(3)
            c1.metric("💸 Total Despesas / Custos", f"R$ {total_desp:,.2f}")
            c2.metric("💰 Total Receitas",           f"R$ {total_rec:,.2f}")
            c3.metric("📊 Resultado Apurado",        f"R$ {resultado:,.2f}",
                      "✅ Lucro" if resultado >= 0 else "⚠️ Prejuízo")

            if not df_resumo_ir.empty:
                st.divider()
                st.subheader("📈 Distribuição por Categoria")
                st.bar_chart(df_resumo_ir.set_index("Categoria")["Valor Total R$"])

            st.divider()
            st.subheader("📤 Exportar para IAAGro / IR Rural")
            todas_notas_exp = [{
                "Tipo":           n.get("Tipo",""),
                "Categoria_IR":   n.get("Categoria_IR") or n.get("Categoria",""),
                "Fornecedor":     n.get("Fornecedor",""),
                "CNPJ_CPF":       n.get("CNPJ_CPF",""),
                "Numero_NF":      n.get("Numero_NF",""),
                "Data":           n.get("Data",""),
                "Safra":          n.get("Safra",""),
                "Valor_Total_R$": n.get("Valor Total", 0),
                "Area_ha":        n.get("Area_ha", 0),
                "Observacao":     n.get("Observacao",""),
                "Codigo_Barras":  n.get("Codigo_Barras",""),
                "Insumo":         n.get("Insumo",""),
            } for n in st.session_state.notas_fiscal]

            xlsx_ir = exportar_excel({
                "Notas Fiscais":  todas_notas_exp,
                "Resumo IR Rural": resumo_ir,
            })
            if xlsx_ir:
                st.download_button(
                    "📥 Baixar Relatório IR Rural (.xlsx) — IAAGro",
                    data=xlsx_ir,
                    file_name=f"iaagro_IR_rural_{date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            import io as _io, csv as _csv
            csv_buf = _io.StringIO()
            if todas_notas_exp:
                writer = _csv.DictWriter(csv_buf, fieldnames=todas_notas_exp[0].keys(), delimiter=";")
                writer.writeheader()
                writer.writerows(todas_notas_exp)
            csv_bytes = ("\ufeff" + csv_buf.getvalue()).encode("utf-8")
            st.download_button(
                "📥 Baixar CSV para Importação (IR / IAAGro)",
                data=csv_bytes,
                file_name=f"iaagro_IR_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )

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
    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:11px 16px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:6px 0 12px 0;font-size:13px;">
    📡 Dados via <b>Open-Meteo API</b> (gratuita, sem chave) · Atualização automática ao abrir · Clique em
    Atualizar para forçar nova busca
    </div>''', unsafe_allow_html=True)

    # ── Geolocalização ──────────────────────────────────────────────────
    geo = get_geolocation()
    if geo:
        lat = geo["coords"]["latitude"]
        lon = geo["coords"]["longitude"]
        fonte_loc = "📍 GPS do navegador"
    else:
        lat = st.session_state.dados.get("latitude", -26.88)
        lon = st.session_state.dados.get("longitude", -52.40)
        fonte_loc = "📌 Coordenadas da área cadastrada"

    # Permitir ajuste manual
    with st.expander("📍 Ajustar localização manualmente", expanded=False):
        col_geo1, col_geo2 = st.columns(2)
        with col_geo1:
            lat = st.number_input("Latitude", value=float(lat), format="%.4f", key="lat_clima")
        with col_geo2:
            lon = st.number_input("Longitude", value=float(lon), format="%.4f", key="lon_clima")

    # ── Botão atualizar + info ──────────────────────────────────────────
    col_cb1, col_cb2 = st.columns([1, 3])
    with col_cb1:
        if st.button("🔄 Atualizar Clima", key="btn_clima", use_container_width=True):
            with st.spinner("🌐 Buscando dados climáticos..."):
                st.session_state.clima_data = buscar_clima(lat, lon)
            if st.session_state.clima_data:
                success_box("✅ Clima atualizado!")
            else:
                error_box("Não foi possível buscar dados. Verifique a conexão.")
    with col_cb2:
        ult_at = st.session_state.get("clima_data", {})
        if ult_at and isinstance(ult_at, dict):
            horario = ult_at.get("_atualizado_em", "")
            st.markdown(
                f'<div style="background:#0f3460;color:#6ee7b7;padding:8px 14px;border-radius:8px;'
                f'font-size:12px;font-weight:700;margin-top:4px;">'
                f'🕐 Última atualização: {horario or "agora"} &nbsp;|&nbsp; {fonte_loc} &nbsp;|&nbsp; '
                f'{lat:.4f}, {lon:.4f}</div>',
                unsafe_allow_html=True
            )

    # Buscar dados se não tiver ou se mudou localização
    if not st.session_state.get("clima_data"):
        with st.spinner("🌐 Carregando dados climáticos..."):
            st.session_state.clima_data = buscar_clima(lat, lon)

    dados_clima = st.session_state.get("clima_data")

    if dados_clima and "current" in dados_clima:
        current = dados_clima.get("current", {})
        daily   = dados_clima.get("daily", {})
        hourly  = dados_clima.get("hourly", {})

        # Extrair dados atuais
        temp        = current.get("temperature_2m", 0)
        temp_sens   = current.get("apparent_temperature", 0)
        umidade     = current.get("relative_humidity_2m", 0)
        chuva       = current.get("precipitation", 0)
        vento       = current.get("windspeed_10m", 0)
        vento_dir   = current.get("winddirection_10m", 0)
        pressao     = current.get("surface_pressure", 0)
        visib       = current.get("visibility", 0)
        uv          = current.get("uv_index", 0)
        wcode       = current.get("weathercode", 0)
        emoji_c, desc_c = codigo_clima_emoji(wcode)

        # Direção do vento
        dirs = ["N","NE","L","SE","S","SO","O","NO"]
        dir_vento = dirs[int((vento_dir + 22.5) / 45) % 8]

        # ── PAINEL PRINCIPAL ─────────────────────────────────────────────
        st.markdown(f'''
        <div style="background:linear-gradient(135deg,#0f2744,#1a3a5c);border-radius:16px;
        padding:20px 24px;margin:10px 0;border:1px solid #22c55e33;">
          <div style="font-size:48px;text-align:center;">{emoji_c}</div>
          <div style="text-align:center;color:#6ee7b7;font-size:22px;font-weight:900;
          margin:4px 0;">{temp:.1f}°C</div>
          <div style="text-align:center;color:#93c5fd;font-size:14px;font-weight:600;">
          {desc_c} &nbsp;·&nbsp; Sensação {temp_sens:.1f}°C</div>
        </div>''', unsafe_allow_html=True)

        # Cards detalhados
        cc1, cc2, cc3, cc4, cc5, cc6 = st.columns(6)
        cc1.metric("💧 Umidade",    f"{umidade:.0f}%")
        cc2.metric("🌧️ Precipit.", f"{chuva:.1f} mm")
        cc3.metric("💨 Vento",      f"{vento:.1f} km/h", dir_vento)
        cc4.metric("🔵 Pressão",   f"{pressao:.0f} hPa")
        cc5.metric("👁️ Visib.",    f"{visib/1000:.1f} km" if visib > 0 else "—")
        cc6.metric("☀️ UV",        f"{uv:.1f}", "🟢 Baixo" if uv < 3 else ("🟡 Mod" if uv < 6 else "🔴 Alto"))

        # ── ALERTA DE APLICAÇÃO ──────────────────────────────────────────
        st.divider()
        st.subheader("🚜 Janela de Aplicação de Defensivos — Agora")

        alertas_ap = alerta_clima_aplicacao(wcode, vento, chuva)

        # Verificações detalhadas
        ok_temp   = 10 <= temp <= 30
        ok_vento  = vento <= 10
        ok_chuva  = chuva == 0
        ok_umid   = 40 <= umidade <= 90
        ok_uv     = uv < 10
        n_ok = sum([ok_temp, ok_vento, ok_chuva, ok_umid, ok_uv])
        score_aplic = int(n_ok / 5 * 100)

        # Barra de score
        cor_score = "#22c55e" if score_aplic >= 80 else ("#f59e0b" if score_aplic >= 50 else "#ef4444")
        label_score = "✅ IDEAL PARA APLICAÇÃO" if score_aplic >= 80 else ("⚠️ ATENÇÃO — Verifique condições" if score_aplic >= 50 else "❌ NÃO RECOMENDADO AGORA")
        st.markdown(f'''
        <div style="background:#0f2744;border-radius:12px;padding:16px 20px;margin:8px 0;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <span style="color:#fff;font-weight:800;font-size:15px;">{label_score}</span>
            <span style="color:{cor_score};font-weight:900;font-size:20px;">{score_aplic}%</span>
          </div>
          <div style="background:#1e3a5f;border-radius:8px;height:12px;overflow:hidden;">
            <div style="background:{cor_score};width:{score_aplic}%;height:12px;border-radius:8px;
            transition:width 0.3s;"></div>
          </div>
        </div>''', unsafe_allow_html=True)

        # Detalhes por parâmetro
        params = [
            ("🌡️ Temperatura", f"{temp:.1f}°C", ok_temp, "Ideal: 10–30°C"),
            ("💨 Vento",        f"{vento:.1f} km/h ({dir_vento})", ok_vento, "Ideal: ≤ 10 km/h"),
            ("🌧️ Chuva",       f"{chuva:.1f} mm", ok_chuva, "Ideal: 0 mm"),
            ("💧 Umidade",      f"{umidade:.0f}%", ok_umid, "Ideal: 40–90%"),
            ("☀️ Índice UV",    f"{uv:.1f}", ok_uv, "Ideal: < 10"),
        ]
        p_cols = st.columns(5)
        for idx, (label, valor, ok, ideal) in enumerate(params):
            bg  = "#14532d" if ok else "#7f1d1d"
            ico = "✅" if ok else "❌"
            p_cols[idx].markdown(
                f'<div style="background:{bg};border-radius:10px;padding:10px 8px;'
                f'text-align:center;color:#fff;font-size:12px;">'
                f'<div style="font-size:16px;">{label}</div>'
                f'<div style="font-size:18px;font-weight:900;margin:4px 0;">{valor}</div>'
                f'<div style="font-size:10px;opacity:0.8;">{ideal}</div>'
                f'<div style="font-size:14px;margin-top:4px;">{ico}</div>'
                f'</div>', unsafe_allow_html=True
            )

        if alertas_ap:
            st.markdown("<br>", unsafe_allow_html=True)
            for a in alertas_ap:
                st.markdown(f'''<div style="background:#7f1d1d;color:#fff;padding:11px 16px;
                border-radius:10px;border-left:5px solid #ef4444;font-weight:700;margin:4px 0;">
                {a}</div>''', unsafe_allow_html=True)

        # ── ETo EVAPOTRANSPIRAÇÃO ────────────────────────────────────────
        st.divider()
        st.subheader("🌱 Evapotranspiração & Balanço Hídrico")
        eto_hoje = daily.get("et0_fao_evapotranspiration", [0])[0] if daily.get("et0_fao_evapotranspiration") else 0
        chuva_hoje = daily.get("precipitation_sum", [0])[0] if daily.get("precipitation_sum") else 0
        balanco = chuva_hoje - eto_hoje

        be1, be2, be3 = st.columns(3)
        be1.metric("💧 ETo hoje (FAO-56)", f"{eto_hoje:.1f} mm/dia",
                   help="Evapotranspiração de referência — quanto a cultura consome de água")
        be2.metric("🌧️ Chuva hoje",       f"{chuva_hoje:.1f} mm")
        be3.metric("⚖️ Balanço Hídrico",  f"{balanco:+.1f} mm",
                   "✅ Superávit" if balanco >= 0 else "⚠️ Déficit hídrico")

        if balanco < -3:
            warning_box(f"⚠️ Déficit hídrico de {abs(balanco):.1f} mm — considere irrigação suplementar.")
        elif balanco > 5:
            info_box(f"💧 Superávit de {balanco:.1f} mm — solo úmido, aguarde antes de aplicar.")

        # ── PREVISÃO 7 DIAS ──────────────────────────────────────────────
        st.divider()
        st.subheader("📅 Previsão para os Próximos 7 Dias")

        if daily and "temperature_2m_max" in daily:
            datas       = daily.get("time", [])
            temp_max    = daily.get("temperature_2m_max", [])
            temp_min    = daily.get("temperature_2m_min", [])
            chuva_d     = daily.get("precipitation_sum", [])
            prob_chuva  = daily.get("precipitation_probability_max", [])
            vento_d     = daily.get("windspeed_10m_max", [])
            wcode_d     = daily.get("weathercode", [])
            uv_d        = daily.get("uv_index_max", [])
            eto_d       = daily.get("et0_fao_evapotranspiration", [])
            sunrise_d   = daily.get("sunrise", [])
            sunset_d    = daily.get("sunset", [])

            # Cards diários
            n_dias = min(7, len(datas))
            cols_dias = st.columns(n_dias)
            for i in range(n_dias):
                try:
                    from datetime import date as _date
                    dt = _date.fromisoformat(datas[i])
                    dia_semana = ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"][dt.weekday()]
                    dia_label  = f"{dia_semana} {dt.day:02d}/{dt.month:02d}"
                except Exception:
                    dia_label = datas[i]

                em, _ = codigo_clima_emoji(wcode_d[i] if i < len(wcode_d) else 0)
                tmax  = temp_max[i] if i < len(temp_max) else 0
                tmin  = temp_min[i] if i < len(temp_min) else 0
                ch    = chuva_d[i] if i < len(chuva_d) else 0
                prob  = prob_chuva[i] if i < len(prob_chuva) else 0
                vd    = vento_d[i] if i < len(vento_d) else 0
                et    = eto_d[i] if i < len(eto_d) else 0
                ok_dia = (ch == 0 and vd <= 10)
                bg_dia = "#14532d" if ok_dia else ("#78350f" if ch > 0 else "#1e3a5f")
                borda  = "#22c55e" if ok_dia else ("#f59e0b" if ch > 0 else "#3b82f6")

                with cols_dias[i]:
                    st.markdown(
                        f'<div style="background:{bg_dia};border:2px solid {borda};border-radius:12px;'
                        f'padding:10px 6px;text-align:center;color:#fff;font-size:11px;">'
                        f'<div style="font-weight:800;font-size:12px;margin-bottom:4px;">{dia_label}</div>'
                        f'<div style="font-size:26px;">{em}</div>'
                        f'<div style="font-weight:700;margin:4px 0;">{tmax:.0f}° / {tmin:.0f}°</div>'
                        f'<div style="color:#93c5fd;">🌧️ {ch:.1f}mm</div>'
                        f'<div style="color:#67e8f9;">☔ {prob:.0f}%</div>'
                        f'<div style="color:#fcd34d;">💨 {vd:.0f}km/h</div>'
                        f'<div style="color:#86efac;font-size:10px;">ETo {et:.1f}mm</div>'
                        f'<div style="margin-top:6px;font-size:13px;">{"✅" if ok_dia else "❌"}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            # Tabela detalhada
            st.markdown("<br>", unsafe_allow_html=True)
            df_prev = pd.DataFrame({
                "Data":          datas[:n_dias],
                "Cond.":         [codigo_clima_emoji(wcode_d[i] if i < len(wcode_d) else 0)[0] for i in range(n_dias)],
                "Máx °C":        [round(temp_max[i], 1) if i < len(temp_max) else 0 for i in range(n_dias)],
                "Mín °C":        [round(temp_min[i], 1) if i < len(temp_min) else 0 for i in range(n_dias)],
                "Chuva mm":      [round(chuva_d[i], 1) if i < len(chuva_d) else 0 for i in range(n_dias)],
                "Prob. Chuva %": [round(prob_chuva[i]) if i < len(prob_chuva) else 0 for i in range(n_dias)],
                "Vento km/h":    [round(vento_d[i], 1) if i < len(vento_d) else 0 for i in range(n_dias)],
                "UV máx":        [round(uv_d[i], 1) if i < len(uv_d) else 0 for i in range(n_dias)],
                "ETo mm":        [round(eto_d[i], 1) if i < len(eto_d) else 0 for i in range(n_dias)],
                "Aplicar?":      ["✅ Sim" if (
                                    (chuva_d[i] if i < len(chuva_d) else 1) == 0 and
                                    (vento_d[i] if i < len(vento_d) else 99) <= 10
                                  ) else "❌ Não" for i in range(n_dias)],
            })
            st.dataframe(df_prev, use_container_width=True, hide_index=True)

            # Gráfico temperatura + chuva
            st.subheader("🌡️ Temperatura (°C)")
            st.line_chart(df_prev.set_index("Data")[["Máx °C","Mín °C"]])
            st.subheader("🌧️ Chuva (mm) e Probabilidade (%)")
            st.bar_chart(df_prev.set_index("Data")[["Chuva mm","Prob. Chuva %"]])

            # Melhores dias para aplicação
            dias_bons = [datas[i] for i in range(n_dias)
                         if (chuva_d[i] if i < len(chuva_d) else 1) == 0
                         and (vento_d[i] if i < len(vento_d) else 99) <= 10]
            if dias_bons:
                st.markdown(f'''<div style="background:#14532d;color:#fff;padding:13px 18px;
                border-radius:10px;border-left:5px solid #22c55e;font-weight:700;margin:8px 0;">
                ✅ Melhores dias para aplicação: {" &nbsp;·&nbsp; ".join(dias_bons)}
                </div>''', unsafe_allow_html=True)
            else:
                warning_box("⚠️ Nenhum dia ideal para aplicação nos próximos 7 dias. Monitore a previsão.")

            # Nascer/pôr do sol
            if sunrise_d and sunset_d:
                st.divider()
                st.subheader("🌅 Nascer e Pôr do Sol")
                sol_cols = st.columns(min(7, len(sunrise_d)))
                for i, col in enumerate(sol_cols):
                    if i < len(sunrise_d):
                        sr = sunrise_d[i][-5:] if len(sunrise_d[i]) >= 5 else sunrise_d[i]
                        ss = sunset_d[i][-5:]  if len(sunset_d[i]) >= 5  else sunset_d[i]
                        col.markdown(
                            f'<div style="background:#1e3a5f;border-radius:10px;padding:8px 6px;'
                            f'text-align:center;color:#fff;font-size:11px;">'
                            f'<div style="color:#fde68a;font-weight:700;">{datas[i][5:]}</div>'
                            f'<div>🌅 {sr}</div><div>🌇 {ss}</div>'
                            f'</div>', unsafe_allow_html=True
                        )

    else:
        st.markdown('''<div style="background:#78350f;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #f59e0b;font-weight:600;">
        ⚠️ Não foi possível buscar dados climáticos. Verifique sua conexão com a internet.
        </div>''', unsafe_allow_html=True)

        # Modo offline — entrada manual
        st.subheader("✍️ Inserir Condições Manualmente")
        col1, col2, col3 = st.columns(3)
        with col1: temp_m   = st.number_input("Temperatura °C",   0.0, 50.0, 25.0, key="temp_m_cli")
        with col2: vento_m  = st.number_input("Vento km/h",       0.0, 100.0, 8.0, key="vento_m_cli")
        with col3: chuva_m  = st.number_input("Precipitação mm",  0.0, 200.0, 0.0, key="chuva_m_cli")
        col4, col5 = st.columns(2)
        with col4: umid_m   = st.number_input("Umidade %",        0.0, 100.0, 65.0, key="umid_m_cli")
        with col5: uv_m     = st.number_input("Índice UV",        0.0, 15.0, 4.0,  key="uv_m_cli")

        alertas_m = alerta_clima_aplicacao(0, vento_m, chuva_m)
        ok_m = (10 <= temp_m <= 30 and vento_m <= 10 and chuva_m == 0
                and 40 <= umid_m <= 90 and uv_m < 10)
        if alertas_m:
            for a in alertas_m:
                st.markdown(f'''<div style="background:#7f1d1d;color:#fff;padding:12px 18px;
                border-radius:10px;border-left:5px solid #ef4444;font-weight:700;">{a}</div>''',
                unsafe_allow_html=True)
        elif ok_m:
            st.markdown('''<div style="background:#14532d;color:#fff;padding:12px 18px;
            border-radius:10px;border-left:5px solid #22c55e;font-weight:700;">
            ✅ Condições adequadas para aplicação!</div>''', unsafe_allow_html=True)
        else:
            warning_box("⚠️ Verifique as condições antes de aplicar.")


# ─────────────────────────────────────────────
# MENU: PREÇOS DE MERCADO
# ─────────────────────────────────────────────
elif menu == "💰 Preços de Mercado":
    st.header("💰 Preços de Commodities em Tempo Real")
    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:11px 16px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:6px 0 12px 0;font-size:13px;">
    💡 Dólar via <b>AwesomeAPI</b> (tempo real) · Grãos via <b>IA + CEPEA/ESALQ</b> (busca na web agora)
    </div>''', unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        atualizar = st.button("🔄 Atualizar Preços", key="btn_precos", use_container_width=True)
    with col_btn2:
        if st.session_state.get("precos_data"):
            fonte_exib = st.session_state.precos_data.get("soja_sc", {}).get("fonte", "")
            horario_dolar = st.session_state.precos_data.get("dolar", {}).get("horario", "")
            st.markdown(f'<div style="background:#0f3460;color:#6ee7b7;padding:8px 14px;border-radius:8px;'
                        f'font-size:12px;font-weight:700;">✅ Última atualização: {fonte_exib}'
                        f'{" | Dólar: " + horario_dolar if horario_dolar else ""}</div>',
                        unsafe_allow_html=True)

    if atualizar:
        with st.spinner("🌐 Buscando cotações em tempo real (CEPEA + AwesomeAPI)..."):
            st.session_state.precos_data = buscar_precos_commodities()
        success_box("✅ Preços atualizados!")

    precos = st.session_state.get("precos_data") or buscar_precos_commodities()
    if not st.session_state.get("precos_data"):
        st.session_state.precos_data = precos

    # ── Extrai todos os valores ──────────────────────────────────────
    pm = st.session_state.get("precos_manuais", {})
    soja_p     = pm.get("soja",    precos.get("soja_sc",    {}).get("preco", 138.0))
    milho_p    = pm.get("milho",   precos.get("milho_sc",   {}).get("preco",  72.0))
    trigo_p    = pm.get("trigo",   precos.get("trigo_sc",   {}).get("preco",  98.0))
    cafe_p     = pm.get("cafe",    precos.get("cafe_sc",    {}).get("preco", 2100.0))
    algodao_p  = pm.get("algodao", precos.get("algodao_at", {}).get("preco", 118.0))
    boi_p      = pm.get("boi",     precos.get("boi_at",     {}).get("preco", 310.0))
    arroz_p    = pm.get("arroz",   precos.get("arroz_sc",   {}).get("preco",  72.0))
    dolar_p    = pm.get("dolar",   precos.get("dolar",      {}).get("preco",   5.80))
    fonte_dolar= precos.get("dolar",      {}).get("fonte", "")
    fonte_graos= precos.get("soja_sc",    {}).get("fonte", "")
    _tem_manual = bool(pm)

    # ── Painel de cotações ───────────────────────────────────────────
    st.subheader("📊 Cotações Atuais")

    # Linha 1 — Grãos
    st.markdown("**🌾 Grãos (R$/saca 60kg)**")
    cg1, cg2, cg3, cg4 = st.columns(4)
    cg1.metric("🌱 Soja",   f"R$ {soja_p:.2f}",
               precos.get("soja_sc",{}).get("praca","PR"))
    cg2.metric("🌽 Milho",  f"R$ {milho_p:.2f}",
               precos.get("milho_sc",{}).get("praca","PR"))
    cg3.metric("🌾 Trigo",  f"R$ {trigo_p:.2f}",
               precos.get("trigo_sc",{}).get("praca","PR"))
    cg4.metric("🍚 Arroz",  f"R$ {arroz_p:.2f}",
               precos.get("arroz_sc",{}).get("praca","RS") + " sc 50kg")

    st.markdown("**🐄 Pecuária & Fibra**")
    cp1, cp2, cp3, cp4 = st.columns(4)
    cp1.metric("☕ Café",      f"R$ {cafe_p:.2f}",
               precos.get("cafe_sc",{}).get("praca","SP") + " sc 60kg")
    cp2.metric("🏭 Algodão",  f"R$ {algodao_p:.2f}",
               precos.get("algodao_at",{}).get("praca","MT") + " @")
    cp3.metric("🐂 Boi Gordo",f"R$ {boi_p:.2f}",
               precos.get("boi_at",{}).get("praca","SP") + " @")
    fonte_dolar_label = "Tempo real" if "AwesomeAPI" in fonte_dolar else "Offline"
    cp4.metric("💵 Dólar",    f"R$ {dolar_p:.4f}", fonte_dolar_label)

    # Indicadores de fonte
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        if _tem_manual:
            st.markdown('<div style="background:#78350f;color:#fff;padding:7px 13px;border-radius:8px;'
                        'font-size:12px;font-weight:700;">✏️ Grãos: Inseridos manualmente</div>',
                        unsafe_allow_html=True)
        else:
            cor_f  = "#14532d" if ("IA" in fonte_graos or "CEPEA" in fonte_graos) and "offline" not in fonte_graos.lower() else "#78350f"
            icone_f = "🟢" if cor_f == "#14532d" else "🟡"
            st.markdown(f'<div style="background:{cor_f};color:#fff;padding:7px 13px;border-radius:8px;'
                        f'font-size:12px;font-weight:700;">{icone_f} Grãos: {fonte_graos or "Aguardando atualização"}</div>',
                        unsafe_allow_html=True)
    with col_f2:
        if _tem_manual and pm.get("dolar"):
            st.markdown('<div style="background:#78350f;color:#fff;padding:7px 13px;border-radius:8px;'
                        'font-size:12px;font-weight:700;">✏️ Dólar: Inserido manualmente</div>',
                        unsafe_allow_html=True)
        else:
            cor_d  = "#14532d" if "AwesomeAPI" in fonte_dolar else "#78350f"
            icone_d = "🟢" if cor_d == "#14532d" else "🟡"
            st.markdown(f'<div style="background:{cor_d};color:#fff;padding:7px 13px;border-radius:8px;'
                        f'font-size:12px;font-weight:700;">{icone_d} Dólar: {fonte_dolar or "Aguardando"}</div>',
                        unsafe_allow_html=True)

    st.divider()

    # ── Atualização Manual de Preços ─────────────────────────────────
    with st.expander("✏️ Atualizar Preços Manualmente", expanded=False):
        st.markdown('''<div style="background:#78350f;color:#fff;padding:10px 16px;
        border-radius:8px;border-left:4px solid #f59e0b;font-size:13px;font-weight:600;margin-bottom:12px;">
        ⚠️ Use quando os preços automáticos estiverem offline ou desatualizados.
        Os valores inseridos aqui substituem os da API e ficam salvos na sessão.
        </div>''', unsafe_allow_html=True)

        if "precos_manuais" not in st.session_state:
            st.session_state.precos_manuais = {}

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown("**🌾 Grãos**")
            pm_soja   = st.number_input("Soja R$/sc 60kg",    min_value=0.0, value=float(st.session_state.precos_manuais.get("soja",   soja_p)),   step=0.50, key="pm_soja")
            pm_milho  = st.number_input("Milho R$/sc 60kg",   min_value=0.0, value=float(st.session_state.precos_manuais.get("milho",  milho_p)),  step=0.50, key="pm_milho")
        with col_m2:
            st.markdown("**🌾 Grãos**")
            pm_trigo  = st.number_input("Trigo R$/sc 60kg",   min_value=0.0, value=float(st.session_state.precos_manuais.get("trigo",  trigo_p)),  step=0.50, key="pm_trigo")
            pm_arroz  = st.number_input("Arroz R$/sc 50kg",   min_value=0.0, value=float(st.session_state.precos_manuais.get("arroz",  arroz_p)),  step=0.50, key="pm_arroz")
        with col_m3:
            st.markdown("**🐄 Pecuária & Outros**")
            pm_cafe   = st.number_input("Café R$/sc 60kg",    min_value=0.0, value=float(st.session_state.precos_manuais.get("cafe",   cafe_p)),   step=10.0, key="pm_cafe")
            pm_algodao= st.number_input("Algodão R$/@",       min_value=0.0, value=float(st.session_state.precos_manuais.get("algodao",algodao_p)),step=1.0,  key="pm_algodao")
        with col_m4:
            st.markdown("**🐄 Pecuária & Outros**")
            pm_boi    = st.number_input("Boi Gordo R$/@",     min_value=0.0, value=float(st.session_state.precos_manuais.get("boi",    boi_p)),    step=1.0,  key="pm_boi")
            pm_dolar  = st.number_input("Dólar R$",           min_value=0.0, value=float(st.session_state.precos_manuais.get("dolar",  dolar_p)),  step=0.01, key="pm_dolar")

        col_btn_m1, col_btn_m2 = st.columns(2)
        with col_btn_m1:
            if st.button("💾 Aplicar Preços Manuais", key="btn_aplicar_manuais", use_container_width=True):
                st.session_state.precos_manuais = {
                    "soja": pm_soja, "milho": pm_milho, "trigo": pm_trigo,
                    "arroz": pm_arroz, "cafe": pm_cafe, "algodao": pm_algodao,
                    "boi": pm_boi, "dolar": pm_dolar,
                }
                # Sobrescreve precos_data com valores manuais
                if not st.session_state.get("precos_data"):
                    st.session_state.precos_data = {}
                for chave, val, praca in [
                    ("soja_sc",    pm_soja,    "PR"),
                    ("milho_sc",   pm_milho,   "PR"),
                    ("trigo_sc",   pm_trigo,   "PR"),
                    ("arroz_sc",   pm_arroz,   "RS"),
                    ("cafe_sc",    pm_cafe,    "SP"),
                    ("algodao_at", pm_algodao, "MT"),
                    ("boi_at",     pm_boi,     "SP"),
                ]:
                    st.session_state.precos_data[chave] = {
                        "preco": val, "fonte": "Manual", "praca": praca
                    }
                st.session_state.precos_data["dolar"] = {
                    "preco": pm_dolar, "fonte": "Manual", "horario": str(datetime.now().strftime("%d/%m/%Y %H:%M"))
                }
                success_box("✅ Preços manuais aplicados! Recarregue a página para ver as cotações atualizadas.")
        with col_btn_m2:
            if st.button("🗑️ Limpar Preços Manuais", key="btn_limpar_manuais", use_container_width=True):
                st.session_state.precos_manuais = {}
                st.session_state.precos_data    = None
                success_box("Preços manuais removidos. Clique em 'Atualizar Preços' para buscar automaticamente.")

    st.divider()

    # ── Simulador de rentabilidade ───────────────────────────────────
    st.subheader("🧮 Simulador de Rentabilidade por Talhão")
    d = st.session_state.dados

    if not d.get("area"):
        info_box("Cadastre uma área primeiro para usar o simulador.")
    else:
        cultura_sim = d.get("cultura", "Soja")
        area_sim    = float(d.get("area", 10))
        produt_sim  = float(d.get("produtividade", 60))

        preco_map = {
            "Soja": soja_p, "Milho": milho_p, "Trigo": trigo_p,
            "Arroz": arroz_p, "Café": cafe_p
        }
        preco_sim = preco_map.get(cultura_sim, soja_p)

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            cult_sim_sel  = st.selectbox("Cultura", list(preco_map.keys()),
                                          index=list(preco_map.keys()).index(cultura_sim)
                                          if cultura_sim in preco_map else 0,
                                          key="sim_cult")
            produt_real   = st.number_input("Produtividade esperada (sc/ha)", 0.0, 500.0, produt_sim, key="sim_prod")
            preco_custom  = st.number_input("Preço da saca (R$)", 0.0, 10000.0,
                                             preco_map.get(cult_sim_sel, soja_p), key="sim_preco")
        with col_s2:
            custo_ha   = st.number_input("Custo total por hectare (R$)", 0.0, 50000.0, 3200.0, key="sim_custo")
            area_calc  = st.number_input("Área (ha)", 0.1, 100000.0, area_sim, key="sim_area")

        receita     = produt_real * preco_custom * area_calc
        custo_total = custo_ha * area_calc
        lucro       = receita - custo_total
        margem      = (lucro / receita * 100) if receita > 0 else 0
        breakeven   = custo_ha / preco_custom if preco_custom > 0 else 0
        preco_min   = custo_ha / produt_real  if produt_real  > 0 else 0

        st.divider()
        col_r1, col_r2, col_r3 = st.columns(3)
        col_r1.metric("💰 Receita Total", f"R$ {receita:,.0f}")
        col_r2.metric("💸 Custo Total",   f"R$ {custo_total:,.0f}")
        col_r3.metric("💵 Lucro Líquido", f"R$ {lucro:,.0f}")

        col_r4, col_r5, col_r6 = st.columns(3)
        col_r4.metric("📊 Margem",           f"{margem:.1f}%")
        col_r5.metric("⚖️ Break-even sc/ha", f"{breakeven:.1f} sc")
        col_r6.metric("💲 Preço mín R$/sc",  f"R$ {preco_min:.2f}")

        if lucro > 0:
            st.markdown(f'''<div style="background:#14532d;color:#fff;padding:13px 18px;
            border-radius:10px;border-left:5px solid #22c55e;font-weight:700;font-size:15px;margin:10px 0;">
            ✅ Operação LUCRATIVA — Lucro de R$ {lucro:,.2f} com margem de {margem:.1f}%
            </div>''', unsafe_allow_html=True)
        else:
            st.markdown(f'''<div style="background:#7f1d1d;color:#fff;padding:13px 18px;
            border-radius:10px;border-left:5px solid #ef4444;font-weight:700;font-size:15px;margin:10px 0;">
            ❌ Operação no PREJUÍZO — Revise custos ou produtividade esperada.
            </div>''', unsafe_allow_html=True)

        # ── Análise de sensibilidade ─────────────────────────────────
        st.divider()
        st.subheader("📈 Análise de Sensibilidade — Variação de Preço")
        precos_range = [preco_custom * f for f in [0.70, 0.80, 0.90, 1.00, 1.10, 1.20, 1.30]]
        lucros_range = [(p * produt_real * area_calc - custo_total) for p in precos_range]
        df_sens = pd.DataFrame({
            "Cenário":     [f"-30%","-20%","-10%","Atual","+10%","+20%","+30%"],
            "Preço R$/sc": [f"R$ {p:.2f}" for p in precos_range],
            "Lucro R$":    [f"R$ {l:,.0f}" for l in lucros_range],
            "Status":      ["✅" if l > 0 else "❌" for l in lucros_range],
        })
        st.dataframe(df_sens, use_container_width=True, hide_index=True)

        # ── Comparativo entre todas as commodities ───────────────────
        st.divider()
        st.subheader("🔄 Comparativo Entre Culturas com Preços Atuais")
        benchmarks = {
            "Soja":    (65,  soja_p,    "sc 60kg"),
            "Milho":   (180, milho_p,   "sc 60kg"),
            "Trigo":   (55,  trigo_p,   "sc 60kg"),
            "Arroz":   (160, arroz_p,   "sc 50kg"),
            "Café":    (30,  cafe_p,    "sc 60kg"),
        }
        comp_data = []
        for cult, (prod_ref, preco_c, unid_c) in benchmarks.items():
            rec_c  = prod_ref * preco_c * area_calc
            luc_c  = rec_c - custo_total
            marg_c = (luc_c / rec_c * 100) if rec_c > 0 else 0
            comp_data.append({
                "Cultura":           cult,
                "Prod. ref (sc/ha)": prod_ref,
                f"Preço ({unid_c})":  f"R$ {preco_c:.2f}",
                "Receita R$":        f"R$ {rec_c:,.0f}",
                "Lucro R$":          f"R$ {luc_c:,.0f}",
                "Margem %":          f"{marg_c:.1f}%",
                "Status":            "✅" if luc_c > 0 else "❌",
            })
        st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# MENU: OCR LAUDO DE SOLO
# ─────────────────────────────────────────────
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
                    if idx_del < len(df_mes):
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


# ═══════════════════════════════════════════════════════════════════
# MENU: RECEITUÁRIO AGRONÔMICO
# ═══════════════════════════════════════════════════════════════════
elif menu == "📜 Receituário Agronômico":
    st.header("📜 Receituário Agronômico")
    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
    📋 Gere o Receituário Agronômico completo conforme exigido pela Lei 7.802/89 e Decreto 4.074/02.
    Obrigatório para compra e uso de defensivos agrícolas. Gera PDF pronto para assinatura.
    </div>''', unsafe_allow_html=True)

    tab_novo_rec, tab_historico_rec = st.tabs(["➕ Novo Receituário", "📁 Histórico"])

    # ── ABA NOVO RECEITUÁRIO ────────────────────────────────────────
    with tab_novo_rec:
        st.subheader("📝 Dados do Receituário")

        col_r1, col_r2 = st.columns(2)

        with col_r1:
            st.markdown("**👨‍🌾 Dados do Produtor**")
            rec_produtor      = st.text_input("Nome do Produtor / Razão Social", key="rec_prod")
            rec_cpf_cnpj      = st.text_input("CPF / CNPJ", placeholder="000.000.000-00", key="rec_cpf")
            rec_propriedade   = st.text_input("Nome da Propriedade", value=st.session_state.dados.get("fazenda",""), key="rec_prop")
            rec_municipio     = st.text_input("Município / UF", key="rec_mun")
            rec_area_ha       = st.number_input("Área a tratar (ha)", min_value=0.1,
                                                value=float(st.session_state.dados.get("area", 1.0)), key="rec_area")
            rec_cultura       = st.selectbox("Cultura", ["Soja","Milho","Trigo","Feijão","Algodão",
                                             "Arroz","Cana-de-Açúcar","Café","Pastagem","Outro"], key="rec_cult")
            rec_alvo          = st.text_input("Alvo / Problema a combater",
                                              placeholder="Ex: Ferrugem asiática, Lagarta-do-cartucho", key="rec_alvo")

        with col_r2:
            st.markdown("**🧑‍💼 Dados do Responsável Técnico**")
            rec_rt_nome       = st.text_input("Nome do Engenheiro Agrônomo / RT", key="rec_rt_nome")
            rec_rt_crea       = st.text_input("CREA / CRBio nº", placeholder="123456-D/SP", key="rec_rt_crea")
            rec_rt_email      = st.text_input("E-mail do RT", key="rec_rt_email")
            rec_rt_telefone   = st.text_input("Telefone do RT", key="rec_rt_tel")
            rec_data_emissao  = st.date_input("Data de Emissão", value=date.today(), key="rec_data")
            rec_validade_dias = st.number_input("Validade (dias)", min_value=1, max_value=365, value=30, key="rec_val")
            rec_numero        = st.text_input("Número do Receituário", placeholder="001/2026", key="rec_num")

        st.divider()
        st.subheader("🧪 Produtos Recomendados")

        qtd_prods_rec = st.number_input("Quantidade de produtos", min_value=1, max_value=8, value=1, key="rec_qtd_prods")
        produtos_rec  = []

        for i in range(int(qtd_prods_rec)):
            st.markdown(f"**Produto {i+1}**")
            cr1, cr2, cr3, cr4, cr5 = st.columns([3, 2, 1, 1, 2])
            with cr1:
                # Busca no catálogo ou digitação livre
                opcoes_estoque = [p["Insumo"] for p in st.session_state.estoque] if st.session_state.estoque else []
                if opcoes_estoque:
                    nome_prod_rec = st.selectbox(f"Produto {i+1}", opcoes_estoque, key=f"rec_prod_{i}")
                    # Buscar IA do catálogo se disponível
                    ia_auto = next((p.get("Ingrediente Ativo","") for p in st.session_state.estoque if p["Insumo"] == nome_prod_rec), "")
                else:
                    nome_prod_rec = st.text_input(f"Nome comercial {i+1}", key=f"rec_prod_{i}")
                    ia_auto = ""
            with cr2:
                ia_prod_rec   = st.text_input(f"Ingrediente Ativo {i+1}", value=ia_auto, key=f"rec_ia_{i}")
            with cr3:
                dose_rec      = st.number_input(f"Dose {i+1}", min_value=0.0, value=0.0, key=f"rec_dose_{i}")
            with cr4:
                unid_rec      = st.selectbox(f"Unid {i+1}", ["L/ha","mL/ha","kg/ha","g/ha","kg/100L"], key=f"rec_unid_{i}")
            with cr5:
                classe_rec    = st.selectbox(f"Classe {i+1}", ["Fungicida","Herbicida","Inseticida",
                                             "Acaricida","Nematicida","Adjuvante","Fertilizante","Outro"], key=f"rec_classe_{i}")

            # Calcular totais
            total_produto = dose_rec * rec_area_ha
            if dose_rec > 0:
                st.markdown(f'<div style="background:#0f3460;color:#6ee7b7;padding:5px 12px;border-radius:6px;'
                            f'font-size:12px;font-weight:700;margin:2px 0 8px 0;">'
                            f'📦 Total para {rec_area_ha:.1f} ha: <b>{total_produto:.2f} {unid_rec.replace("/ha","").replace("/100L","")}</b>'
                            f'</div>', unsafe_allow_html=True)

            produtos_rec.append({
                "Produto":           nome_prod_rec,
                "Ingrediente Ativo": ia_prod_rec,
                "Dose":              dose_rec,
                "Unidade":           unid_rec,
                "Classe":            classe_rec,
                "Total":             round(total_produto, 2),
            })

        st.divider()
        st.subheader("⚙️ Recomendações de Aplicação")
        col_ap1, col_ap2, col_ap3 = st.columns(3)
        with col_ap1:
            rec_volume_calda  = st.number_input("Volume de calda (L/ha)", min_value=0.0, value=100.0, key="rec_vol")
            rec_equipamento   = st.selectbox("Equipamento", ["Pulverizador tratorizado","Pulverizador costal",
                                             "Avião agrícola","Drone","Pivô central","Outro"], key="rec_equip")
        with col_ap2:
            rec_epoca         = st.text_input("Época de aplicação", placeholder="Ex: Estádio R1 da soja", key="rec_epoca")
            rec_intervalo     = st.number_input("Intervalo entre aplicações (dias)", min_value=0, value=14, key="rec_intv")
        with col_ap3:
            rec_epi           = st.multiselect("EPI obrigatório", ["Macacão","Luvas nitrílicas","Botas de borracha",
                                               "Máscara com filtro","Óculos de proteção","Avental impermeável",
                                               "Chapéu de abas largas"], key="rec_epi")
            rec_carencia      = st.number_input("Prazo de carência (dias)", min_value=0, value=14, key="rec_car")

        rec_observacoes = st.text_area("Observações / Recomendações adicionais", key="rec_obs",
                                       placeholder="Ex: Não aplicar com ventos acima de 10 km/h...")

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("💾 Salvar Receituário", key="btn_salvar_rec", use_container_width=True):
                if not rec_produtor.strip():
                    error_box("Informe o nome do produtor.")
                elif not rec_rt_nome.strip():
                    error_box("Informe o nome do Responsável Técnico.")
                elif not rec_rt_crea.strip():
                    error_box("Informe o CREA/CRBio do RT.")
                else:
                    novo_rec = {
                        "numero":         rec_numero or f"{len(st.session_state.receituarios)+1:03d}/{date.today().year}",
                        "data_emissao":   str(rec_data_emissao),
                        "validade_dias":  rec_validade_dias,
                        "validade_ate":   str(pd.Timestamp(rec_data_emissao) + pd.Timedelta(days=rec_validade_dias)),
                        "produtor":       rec_produtor,
                        "cpf_cnpj":       rec_cpf_cnpj,
                        "propriedade":    rec_propriedade,
                        "municipio":      rec_municipio,
                        "area_ha":        rec_area_ha,
                        "cultura":        rec_cultura,
                        "alvo":           rec_alvo,
                        "rt_nome":        rec_rt_nome,
                        "rt_crea":        rec_rt_crea,
                        "rt_email":       rec_rt_email,
                        "rt_telefone":    rec_rt_telefone,
                        "volume_calda":   rec_volume_calda,
                        "equipamento":    rec_equipamento,
                        "epoca":          rec_epoca,
                        "intervalo_dias": rec_intervalo,
                        "epi":            rec_epi,
                        "carencia_dias":  rec_carencia,
                        "observacoes":    rec_observacoes,
                        "produtos":       produtos_rec,
                    }
                    st.session_state.receituarios.append(novo_rec)
                    salvar_dados_iaagro()
                    success_box(f"✅ Receituário {novo_rec['numero']} salvo com sucesso!")

        with col_btn2:
            # Gerar PDF do último receituário preenchido
            if st.button("🖨️ Gerar PDF", key="btn_pdf_rec", use_container_width=True):
                if not rec_produtor.strip() or not rec_rt_nome.strip():
                    error_box("Preencha ao menos produtor e Responsável Técnico antes de gerar o PDF.")
                else:
                    try:
                        from reportlab.lib.units import cm
                        from reportlab.lib.enums import TA_CENTER, TA_LEFT
                        from reportlab.lib.styles import ParagraphStyle

                        buf_r = BytesIO()
                        doc_r = SimpleDocTemplate(buf_r, pagesize=A4,
                                                  rightMargin=2*cm, leftMargin=2*cm,
                                                  topMargin=2*cm, bottomMargin=2*cm)
                        sty_r = getSampleStyleSheet()
                        el_r  = []

                        # ── Cabeçalho
                        titulo_sty = ParagraphStyle("titulo", parent=sty_r["Title"],
                                                    fontSize=16, textColor=colors.HexColor("#0f3460"),
                                                    alignment=TA_CENTER)
                        sub_sty    = ParagraphStyle("sub", parent=sty_r["Normal"],
                                                    fontSize=10, textColor=colors.HexColor("#1e3a5f"),
                                                    alignment=TA_CENTER)

                        if os.path.exists("IAAgrologo.jpeg"):
                            el_r.append(Image("IAAgrologo.jpeg", width=2.5*cm, height=1.2*cm))
                        el_r.append(Spacer(1, 6))
                        el_r.append(Paragraph("RECEITUÁRIO AGRONÔMICO", titulo_sty))
                        el_r.append(Paragraph(f"Lei 7.802/89 | Decreto 4.074/02", sub_sty))
                        el_r.append(Paragraph(f"Nº {rec_numero or '---'} | Emissão: {rec_data_emissao.strftime('%d/%m/%Y')} | "
                                              f"Validade: {rec_validade_dias} dias", sub_sty))
                        el_r.append(Spacer(1, 10))

                        # ── Linha horizontal
                        from reportlab.platypus import HRFlowable
                        el_r.append(HRFlowable(width="100%", thickness=2,
                                               color=colors.HexColor("#0f3460")))
                        el_r.append(Spacer(1, 8))

                        # ── Dados do Produtor
                        el_r.append(Paragraph("<b>DADOS DO PRODUTOR</b>", sty_r["Heading2"]))
                        dados_prod = [
                            ["Produtor / Razão Social:", rec_produtor,     "CPF / CNPJ:", rec_cpf_cnpj],
                            ["Propriedade:",             rec_propriedade,  "Município/UF:", rec_municipio],
                            ["Cultura:",                 rec_cultura,      "Área (ha):",  f"{rec_area_ha:.2f} ha"],
                            ["Alvo / Problema:",         rec_alvo,         "",            ""],
                        ]
                        t_prod = Table(dados_prod, colWidths=[4*cm, 7*cm, 3.5*cm, 3*cm])
                        t_prod.setStyle(TableStyle([
                            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
                            ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
                            ("FONTNAME",(2,0),(2,-1),"Helvetica-Bold"),
                            ("FONTSIZE",(0,0),(-1,-1),9),
                            ("GRID",(0,0),(-1,-1),0.3,colors.grey),
                            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#eef4ff")),
                            ("BACKGROUND",(2,0),(2,-1),colors.HexColor("#eef4ff")),
                            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                            ("PADDING",(0,0),(-1,-1),4),
                        ]))
                        el_r.append(t_prod)
                        el_r.append(Spacer(1, 10))

                        # ── Produtos recomendados
                        el_r.append(Paragraph("<b>PRODUTOS RECOMENDADOS</b>", sty_r["Heading2"]))
                        header_prod = ["Produto Comercial","Ingrediente Ativo","Dose","Unidade","Classe","Total"]
                        rows_prod   = [header_prod]
                        for p in produtos_rec:
                            rows_prod.append([
                                p["Produto"], p["Ingrediente Ativo"],
                                str(p["Dose"]), p["Unidade"], p["Classe"], str(p["Total"])
                            ])
                        t_prods = Table(rows_prod, colWidths=[4*cm, 4.5*cm, 1.5*cm, 1.8*cm, 2.2*cm, 2*cm])
                        t_prods.setStyle(TableStyle([
                            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0f3460")),
                            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
                            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
                            ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
                            ("FONTSIZE",(0,0),(-1,-1),8.5),
                            ("GRID",(0,0),(-1,-1),0.3,colors.grey),
                            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f0f6ff")]),
                            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                            ("PADDING",(0,0),(-1,-1),4),
                        ]))
                        el_r.append(t_prods)
                        el_r.append(Spacer(1, 10))

                        # ── Recomendações de aplicação
                        el_r.append(Paragraph("<b>RECOMENDAÇÕES DE APLICAÇÃO</b>", sty_r["Heading2"]))
                        dados_aplic = [
                            ["Volume de calda:", f"{rec_volume_calda:.0f} L/ha", "Equipamento:", rec_equipamento],
                            ["Época de aplicação:", rec_epoca, "Intervalo:", f"{rec_intervalo} dias"],
                            ["Prazo de carência:", f"{rec_carencia} dias", "EPI:", ", ".join(rec_epi) if rec_epi else "Conforme bula"],
                        ]
                        t_aplic = Table(dados_aplic, colWidths=[4*cm, 5.5*cm, 3.5*cm, 4.5*cm])
                        t_aplic.setStyle(TableStyle([
                            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
                            ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
                            ("FONTNAME",(2,0),(2,-1),"Helvetica-Bold"),
                            ("FONTSIZE",(0,0),(-1,-1),9),
                            ("GRID",(0,0),(-1,-1),0.3,colors.grey),
                            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#eef4ff")),
                            ("BACKGROUND",(2,0),(2,-1),colors.HexColor("#eef4ff")),
                            ("PADDING",(0,0),(-1,-1),4),
                        ]))
                        el_r.append(t_aplic)

                        if rec_observacoes.strip():
                            el_r.append(Spacer(1, 8))
                            el_r.append(Paragraph("<b>OBSERVAÇÕES:</b>", sty_r["Heading3"]))
                            el_r.append(Paragraph(rec_observacoes, sty_r["BodyText"]))

                        el_r.append(Spacer(1, 16))
                        el_r.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
                        el_r.append(Spacer(1, 10))

                        # ── Assinaturas
                        el_r.append(Paragraph("<b>RESPONSÁVEL TÉCNICO</b>", sty_r["Heading2"]))
                        dados_rt = [
                            ["Nome:", rec_rt_nome, "CREA/CRBio:", rec_rt_crea],
                            ["E-mail:", rec_rt_email, "Telefone:", rec_rt_telefone],
                        ]
                        t_rt = Table(dados_rt, colWidths=[2.5*cm, 7*cm, 3*cm, 5*cm])
                        t_rt.setStyle(TableStyle([
                            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
                            ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
                            ("FONTNAME",(2,0),(2,-1),"Helvetica-Bold"),
                            ("FONTSIZE",(0,0),(-1,-1),9),
                            ("GRID",(0,0),(-1,-1),0.3,colors.grey),
                            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#eef4ff")),
                            ("BACKGROUND",(2,0),(2,-1),colors.HexColor("#eef4ff")),
                            ("PADDING",(0,0),(-1,-1),4),
                        ]))
                        el_r.append(t_rt)
                        el_r.append(Spacer(1, 30))

                        # Linha de assinatura
                        ass_data = [["_"*40, "   ", "_"*40],
                                    [f"Assinatura do RT — {rec_rt_crea}", "   ",
                                     f"Assinatura do Produtor — {rec_cpf_cnpj}"]]
                        t_ass = Table(ass_data, colWidths=[7.5*cm, 1.5*cm, 8.5*cm])
                        t_ass.setStyle(TableStyle([
                            ("FONTSIZE",(0,0),(-1,-1),9),
                            ("ALIGN",(0,0),(-1,-1),"CENTER"),
                            ("FONTNAME",(0,1),(-1,1),"Helvetica"),
                            ("TEXTCOLOR",(0,1),(-1,1),colors.HexColor("#555")),
                        ]))
                        el_r.append(t_ass)

                        el_r.append(Spacer(1, 14))
                        el_r.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
                        el_r.append(Paragraph(
                            f'<font size="7" color="grey">Documento gerado pelo IAAgro Pro em {date.today().strftime("%d/%m/%Y")} | '
                            f'Este receituário é válido por {rec_validade_dias} dias a partir da emissão.</font>',
                            sty_r["Normal"]
                        ))

                        doc_r.build(el_r)
                        pdf_rec = buf_r.getvalue()
                        buf_r.close()

                        num_arquivo = (rec_numero or "receituario").replace("/","_").replace(" ","_")
                        st.download_button(
                            "📥 Baixar Receituário PDF",
                            data=pdf_rec,
                            file_name=f"Receituario_{num_arquivo}_{rec_produtor[:15].replace(' ','_')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        error_box(f"Erro ao gerar PDF: {e}")

    # ── ABA HISTÓRICO ───────────────────────────────────────────────
    with tab_historico_rec:
        st.subheader("📁 Receituários Emitidos")
        if not st.session_state.receituarios:
            info_box("Nenhum receituário salvo ainda.")
        else:
            # Tabela resumo
            resumo = []
            for r in st.session_state.receituarios:
                resumo.append({
                    "Nº":         r.get("numero",""),
                    "Data":       r.get("data_emissao",""),
                    "Produtor":   r.get("produtor",""),
                    "Cultura":    r.get("cultura",""),
                    "Área (ha)":  r.get("area_ha",0),
                    "Alvo":       r.get("alvo",""),
                    "RT":         r.get("rt_nome",""),
                    "Validade":   r.get("validade_ate","")[:10] if r.get("validade_ate") else "",
                })
            df_rec_hist = pd.DataFrame(resumo)
            st.dataframe(df_rec_hist, use_container_width=True, hide_index=True)

            # Ver detalhes / regerar PDF
            st.divider()
            opcoes_rec = [f"{r.get('numero',i)} — {r.get('produtor','')} — {r.get('data_emissao','')}"
                          for i, r in enumerate(st.session_state.receituarios)]
            sel_rec = st.selectbox("Selecionar receituário", opcoes_rec, key="sel_rec_hist")
            idx_sel = opcoes_rec.index(sel_rec)
            rec_sel = st.session_state.receituarios[idx_sel]

            with st.expander("👁️ Ver detalhes completos", expanded=False):
                col_det1, col_det2 = st.columns(2)
                with col_det1:
                    st.markdown(f"**Produtor:** {rec_sel.get('produtor','')}")
                    st.markdown(f"**CPF/CNPJ:** {rec_sel.get('cpf_cnpj','')}")
                    st.markdown(f"**Propriedade:** {rec_sel.get('propriedade','')}")
                    st.markdown(f"**Município:** {rec_sel.get('municipio','')}")
                    st.markdown(f"**Cultura:** {rec_sel.get('cultura','')} — {rec_sel.get('area_ha',0)} ha")
                    st.markdown(f"**Alvo:** {rec_sel.get('alvo','')}")
                with col_det2:
                    st.markdown(f"**RT:** {rec_sel.get('rt_nome','')}")
                    st.markdown(f"**CREA:** {rec_sel.get('rt_crea','')}")
                    st.markdown(f"**Emissão:** {rec_sel.get('data_emissao','')}")
                    st.markdown(f"**Válido até:** {rec_sel.get('validade_ate','')[:10]}")
                    st.markdown(f"**Equipamento:** {rec_sel.get('equipamento','')}")
                    st.markdown(f"**Volume calda:** {rec_sel.get('volume_calda',0)} L/ha")

                if rec_sel.get("produtos"):
                    st.markdown("**Produtos:**")
                    st.dataframe(pd.DataFrame(rec_sel["produtos"]), use_container_width=True, hide_index=True)

            # Excluir
            if st.button("🗑️ Excluir este receituário", key="btn_del_rec"):
                st.session_state.receituarios.pop(idx_sel)
                salvar_dados_iaagro()
                success_box("Receituário excluído.")
                st.rerun()

            # Exportar todos em Excel
            if st.button("📊 Exportar todos para Excel", key="btn_xlsx_rec", use_container_width=True):
                rows_exp = []
                for r in st.session_state.receituarios:
                    base = {k: v for k, v in r.items() if k != "produtos"}
                    for j, p in enumerate(r.get("produtos", [])):
                        row = base.copy()
                        row.update({f"prod_{j+1}_{k}": v for k, v in p.items()})
                        rows_exp.append(row)
                    if not r.get("produtos"):
                        rows_exp.append(base)
                xlsx_r = exportar_excel({"Receituários": rows_exp})
                if xlsx_r:
                    st.download_button("📥 Baixar Excel", data=xlsx_r,
                        file_name=f"receituarios_{date.today()}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True)


# ═══════════════════════════════════════════════════════════════════
# MENU: COMPARATIVO DE SAFRAS
# ═══════════════════════════════════════════════════════════════════
elif menu == "📊 Comparativo de Safras":
    st.header("📊 Comparativo de Safras")
    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
    📈 Compare produtividade, custos e lucratividade entre todas as safras cadastradas.
    Identifique tendências e tome decisões com base no histórico real da sua propriedade.
    </div>''', unsafe_allow_html=True)

    # Verificar dados disponíveis
    tem_hist = len(st.session_state.historico_produtividade) > 0
    tem_dre  = len(st.session_state.get("dre_registros", [])) > 0

    if not tem_hist and not tem_dre:
        warning_box("Cadastre dados em 'Histórico de Produtividade' e/ou 'Dashboard Financeiro' para ver o comparativo.")
    else:
        try:
            import plotly.express as px
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            PLOTLY_OK = True
        except ImportError:
            PLOTLY_OK = False

        tab_prod, tab_fin, tab_completo, tab_ia = st.tabs([
            "🌾 Produtividade",
            "💰 Financeiro",
            "📋 Comparativo Completo",
            "🤖 Análise IA"
        ])

        # ── TAB 1: PRODUTIVIDADE ────────────────────────────────────
        with tab_prod:
            st.subheader("🌾 Evolução da Produtividade por Safra")
            if not tem_hist:
                info_box("Cadastre dados em 'Histórico de Produtividade' para ver esta aba.")
            else:
                df_h = pd.DataFrame(st.session_state.historico_produtividade)

                # Filtros
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    areas_disp = ["Todas"] + sorted(df_h["Área"].unique().tolist())
                    area_filtro_comp = st.selectbox("Filtrar por área", areas_disp, key="comp_area_filtro")
                with col_f2:
                    culturas_disp = ["Todas"] + sorted(df_h["Área"].unique().tolist())
                    min_safras = st.number_input("Mínimo de safras para exibir", min_value=1, value=1, key="comp_min_safras")

                df_hf = df_h if area_filtro_comp == "Todas" else df_h[df_h["Área"] == area_filtro_comp]

                if df_hf.empty:
                    info_box("Nenhum dado para o filtro selecionado.")
                else:
                    # Métricas gerais
                    media_geral  = df_hf["Produtividade"].mean()
                    melhor_safra = df_hf.loc[df_hf["Produtividade"].idxmax()]
                    pior_safra   = df_hf.loc[df_hf["Produtividade"].idxmin()]
                    tendencia    = df_hf.groupby("Safra")["Produtividade"].mean()
                    delta_trend  = tendencia.iloc[-1] - tendencia.iloc[0] if len(tendencia) > 1 else 0

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("📊 Média Geral", f"{media_geral:.1f} sc/ha")
                    c2.metric("🏆 Melhor Safra", f"{melhor_safra['Produtividade']:.1f} sc/ha",
                              f"{melhor_safra['Safra']}")
                    c3.metric("⬇️ Pior Safra", f"{pior_safra['Produtividade']:.1f} sc/ha",
                              f"{pior_safra['Safra']}")
                    c4.metric("📈 Tendência", f"{delta_trend:+.1f} sc/ha",
                              "vs 1ª safra" if len(tendencia) > 1 else "—")

                    if PLOTLY_OK:
                        # Gráfico de barras por safra + linha de média
                        df_safra_media = df_hf.groupby("Safra")["Produtividade"].mean().reset_index()
                        df_safra_media.columns = ["Safra","Média sc/ha"]

                        fig_bar = go.Figure()
                        fig_bar.add_trace(go.Bar(
                            x=df_safra_media["Safra"],
                            y=df_safra_media["Média sc/ha"],
                            marker_color=[
                                "#22c55e" if v >= media_geral else "#f59e0b"
                                for v in df_safra_media["Média sc/ha"]
                            ],
                            text=[f"{v:.1f}" for v in df_safra_media["Média sc/ha"]],
                            textposition="outside",
                            name="Produtividade"
                        ))
                        fig_bar.add_hline(y=media_geral, line_dash="dash",
                                          line_color="#6ee7b7",
                                          annotation_text=f"Média: {media_geral:.1f}",
                                          annotation_font_color="#6ee7b7")
                        fig_bar.update_layout(
                            title="Produtividade Média por Safra (sc/ha)",
                            paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",
                            font_color="#f1f5f9", height=380,
                            xaxis_title="Safra", yaxis_title="sc/ha",
                            yaxis=dict(gridcolor="#1e3a5f"),
                            showlegend=False
                        )
                        st.plotly_chart(fig_bar, use_container_width=True)

                        # Evolução por área (se múltiplas)
                        if df_hf["Área"].nunique() > 1:
                            fig_line = px.line(
                                df_hf.groupby(["Safra","Área"])["Produtividade"].mean().reset_index(),
                                x="Safra", y="Produtividade", color="Área",
                                title="Evolução por Área/Talhão",
                                markers=True, height=340,
                                labels={"Produtividade":"sc/ha"}
                            )
                            fig_line.update_layout(
                                paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",
                                font_color="#f1f5f9",
                                yaxis=dict(gridcolor="#1e3a5f")
                            )
                            st.plotly_chart(fig_line, use_container_width=True)

                        # Box plot das safras
                        if df_hf["Safra"].nunique() > 1:
                            fig_box2 = px.box(
                                df_hf, x="Safra", y="Produtividade",
                                color="Safra",
                                title="Distribuição de Produtividade por Safra",
                                height=320, labels={"Produtividade":"sc/ha"}
                            )
                            fig_box2.update_layout(
                                paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",
                                font_color="#f1f5f9", showlegend=False,
                                yaxis=dict(gridcolor="#1e3a5f")
                            )
                            st.plotly_chart(fig_box2, use_container_width=True)
                    else:
                        st.line_chart(df_hf.groupby("Safra")["Produtividade"].mean())

                    # Tabela completa
                    st.subheader("📋 Dados por Safra")
                    df_tab_comp = df_hf.groupby("Safra").agg(
                        Média=("Produtividade","mean"),
                        Mínimo=("Produtividade","min"),
                        Máximo=("Produtividade","max"),
                        Registros=("Produtividade","count")
                    ).round(1).reset_index()
                    df_tab_comp["vs Média"] = (df_tab_comp["Média"] - media_geral).round(1)
                    st.dataframe(df_tab_comp, use_container_width=True, hide_index=True)

        # ── TAB 2: FINANCEIRO ───────────────────────────────────────
        with tab_fin:
            st.subheader("💰 Comparativo Financeiro entre Safras")
            if not tem_dre:
                info_box("Cadastre lançamentos em 'Dashboard Financeiro' para ver esta aba.")
            else:
                df_dre_all = pd.DataFrame(st.session_state.dre_registros)

                df_fin_comp = df_dre_all.groupby(["Safra","Tipo"])["Valor R$"].sum().unstack(fill_value=0).reset_index()

                # Garantir colunas mesmo que faltem
                for col in ["Receita","Custo Variável","Custo Fixo"]:
                    if col not in df_fin_comp.columns:
                        df_fin_comp[col] = 0

                df_fin_comp["Custo Total"] = df_fin_comp.get("Custo Variável",0) + df_fin_comp.get("Custo Fixo",0)
                df_fin_comp["Lucro"]       = df_fin_comp["Receita"] - df_fin_comp["Custo Total"]
                df_fin_comp["Margem %"]    = (df_fin_comp["Lucro"] / df_fin_comp["Receita"] * 100).round(1).where(df_fin_comp["Receita"]>0, 0)

                # Área por safra (para métricas /ha)
                df_area_safra = df_dre_all.groupby("Safra")["Área ha"].max().reset_index()
                df_fin_comp   = df_fin_comp.merge(df_area_safra, on="Safra", how="left")
                df_fin_comp["Área ha"] = df_fin_comp["Área ha"].fillna(1)
                df_fin_comp["Receita/ha"]   = (df_fin_comp["Receita"] / df_fin_comp["Área ha"]).round(0)
                df_fin_comp["Custo/ha"]     = (df_fin_comp["Custo Total"] / df_fin_comp["Área ha"]).round(0)
                df_fin_comp["Lucro/ha"]     = (df_fin_comp["Lucro"] / df_fin_comp["Área ha"]).round(0)

                # Métricas de destaque
                melhor_lucro = df_fin_comp.loc[df_fin_comp["Lucro"].idxmax()] if not df_fin_comp.empty else None
                media_margem = df_fin_comp["Margem %"].mean()

                if melhor_lucro is not None:
                    cm1, cm2, cm3, cm4 = st.columns(4)
                    cm1.metric("🏆 Melhor Lucro", f"R$ {melhor_lucro['Lucro']:,.0f}", melhor_lucro["Safra"])
                    cm2.metric("📊 Margem Média", f"{media_margem:.1f}%")
                    cm3.metric("💰 Maior Receita", f"R$ {df_fin_comp['Receita'].max():,.0f}")
                    cm4.metric("💸 Menor Custo/ha", f"R$ {df_fin_comp['Custo/ha'].min():,.0f}/ha")

                if PLOTLY_OK:
                    # Barras agrupadas Receita x Custo x Lucro
                    fig_fin = go.Figure()
                    fig_fin.add_trace(go.Bar(name="Receita", x=df_fin_comp["Safra"],
                                             y=df_fin_comp["Receita"], marker_color="#22c55e",
                                             text=df_fin_comp["Receita"].apply(lambda v: f"R$ {v:,.0f}"),
                                             textposition="outside"))
                    fig_fin.add_trace(go.Bar(name="Custo Total", x=df_fin_comp["Safra"],
                                             y=df_fin_comp["Custo Total"], marker_color="#ef4444",
                                             text=df_fin_comp["Custo Total"].apply(lambda v: f"R$ {v:,.0f}"),
                                             textposition="outside"))
                    fig_fin.add_trace(go.Bar(name="Lucro", x=df_fin_comp["Safra"],
                                             y=df_fin_comp["Lucro"],
                                             marker_color=["#6ee7b7" if v >= 0 else "#f87171"
                                                           for v in df_fin_comp["Lucro"]],
                                             text=df_fin_comp["Lucro"].apply(lambda v: f"R$ {v:,.0f}"),
                                             textposition="outside"))
                    fig_fin.update_layout(
                        barmode="group",
                        title="Receita x Custo x Lucro por Safra",
                        paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",
                        font_color="#f1f5f9", height=400,
                        xaxis_title="Safra", yaxis_title="R$",
                        yaxis=dict(gridcolor="#1e3a5f"),
                        legend=dict(bgcolor="#0f3460", bordercolor="#22c55e", borderwidth=1)
                    )
                    st.plotly_chart(fig_fin, use_container_width=True)

                    # Evolução da margem
                    if len(df_fin_comp) > 1:
                        fig_margem = go.Figure()
                        fig_margem.add_trace(go.Scatter(
                            x=df_fin_comp["Safra"], y=df_fin_comp["Margem %"],
                            mode="lines+markers+text",
                            text=[f"{v:.1f}%" for v in df_fin_comp["Margem %"]],
                            textposition="top center",
                            line=dict(color="#f59e0b", width=3),
                            marker=dict(size=10),
                            name="Margem %"
                        ))
                        fig_margem.add_hline(y=0, line_dash="dash", line_color="#ef4444",
                                             annotation_text="Break-even", annotation_font_color="#ef4444")
                        fig_margem.update_layout(
                            title="Evolução da Margem Líquida (%)",
                            paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",
                            font_color="#f1f5f9", height=300,
                            yaxis=dict(gridcolor="#1e3a5f"),
                            xaxis_title="Safra", yaxis_title="Margem %"
                        )
                        st.plotly_chart(fig_margem, use_container_width=True)

                # Tabela financeira completa
                st.subheader("📋 Resumo Financeiro por Safra")
                cols_exib = ["Safra","Receita","Custo Total","Lucro","Margem %","Receita/ha","Custo/ha","Lucro/ha","Área ha"]
                st.dataframe(df_fin_comp[[c for c in cols_exib if c in df_fin_comp.columns]].round(1),
                             use_container_width=True, hide_index=True)

        # ── TAB 3: COMPARATIVO COMPLETO ─────────────────────────────
        with tab_completo:
            st.subheader("📋 Painel Completo — Produtividade + Financeiro")

            if not tem_hist and not tem_dre:
                info_box("Sem dados suficientes.")
            else:
                # Unir produtividade e financeiro por safra
                dados_comp = {}

                if tem_hist:
                    df_hc = pd.DataFrame(st.session_state.historico_produtividade)
                    for safra, grp in df_hc.groupby("Safra"):
                        dados_comp.setdefault(safra, {})["Prod. Média sc/ha"] = round(grp["Produtividade"].mean(), 1)
                        dados_comp[safra]["Custo Histórico/ha"] = round(grp["Custo"].mean(), 2)

                if tem_dre:
                    df_dc = pd.DataFrame(st.session_state.dre_registros)
                    for safra, grp in df_dc.groupby("Safra"):
                        rec   = grp[grp["Tipo"]=="Receita"]["Valor R$"].sum()
                        custo = grp[grp["Tipo"].isin(["Custo Variável","Custo Fixo"])]["Valor R$"].sum()
                        lucro = rec - custo
                        area  = grp["Área ha"].max() if not grp.empty else 1
                        dados_comp.setdefault(safra, {})["Receita R$"]  = round(rec, 0)
                        dados_comp[safra]["Custo Total R$"] = round(custo, 0)
                        dados_comp[safra]["Lucro R$"]       = round(lucro, 0)
                        dados_comp[safra]["Margem %"]       = round(lucro/rec*100, 1) if rec > 0 else 0
                        dados_comp[safra]["Área ha"]        = area

                df_comp_final = pd.DataFrame(dados_comp).T.reset_index().rename(columns={"index":"Safra"})
                df_comp_final = df_comp_final.sort_values("Safra")

                # Highlight melhor linha
                st.dataframe(df_comp_final, use_container_width=True, hide_index=True)

                if PLOTLY_OK and "Prod. Média sc/ha" in df_comp_final.columns and "Lucro R$" in df_comp_final.columns:
                    df_plot_dual = df_comp_final.dropna(subset=["Prod. Média sc/ha","Lucro R$"])
                    if not df_plot_dual.empty:
                        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
                        fig_dual.add_trace(go.Bar(
                            name="Produtividade sc/ha", x=df_plot_dual["Safra"],
                            y=df_plot_dual["Prod. Média sc/ha"], marker_color="#22c55e",
                            opacity=0.85
                        ), secondary_y=False)
                        fig_dual.add_trace(go.Scatter(
                            name="Lucro R$", x=df_plot_dual["Safra"],
                            y=df_plot_dual["Lucro R$"],
                            mode="lines+markers", line=dict(color="#f59e0b", width=3),
                            marker=dict(size=9)
                        ), secondary_y=True)
                        fig_dual.update_layout(
                            title="Produtividade (sc/ha) vs Lucro (R$) por Safra",
                            paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",
                            font_color="#f1f5f9", height=400,
                            legend=dict(bgcolor="#0f3460", bordercolor="#22c55e", borderwidth=1)
                        )
                        fig_dual.update_yaxes(title_text="sc/ha", secondary_y=False,
                                              gridcolor="#1e3a5f")
                        fig_dual.update_yaxes(title_text="Lucro R$", secondary_y=True)
                        st.plotly_chart(fig_dual, use_container_width=True)

                # Download
                xlsx_comp = exportar_excel({"Comparativo Safras": df_comp_final.to_dict("records")})
                if xlsx_comp:
                    st.download_button("📥 Exportar Comparativo Excel", data=xlsx_comp,
                        file_name=f"comparativo_safras_{date.today()}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True)

        # ── TAB 4: ANÁLISE IA ───────────────────────────────────────
        with tab_ia:
            st.subheader("🤖 Análise Comparativa por Inteligência Artificial")

            if st.button("🚀 Gerar Análise IA das Safras", key="btn_ia_comp", use_container_width=True):
                with st.spinner("🤖 Analisando histórico de safras..."):
                    # Montar resumo para o prompt
                    resumo_hist = ""
                    if tem_hist:
                        df_hr = pd.DataFrame(st.session_state.historico_produtividade)
                        for safra, grp in df_hr.groupby("Safra"):
                            resumo_hist += (f"Safra {safra}: prod. média {grp['Produtividade'].mean():.1f} sc/ha, "
                                           f"custo {grp['Custo'].mean():.2f} R$/ha\n")

                    resumo_fin = ""
                    if tem_dre:
                        df_dr = pd.DataFrame(st.session_state.dre_registros)
                        for safra, grp in df_dr.groupby("Safra"):
                            rec   = grp[grp["Tipo"]=="Receita"]["Valor R$"].sum()
                            custo = grp[grp["Tipo"].isin(["Custo Variável","Custo Fixo"])]["Valor R$"].sum()
                            lucro = rec - custo
                            margem = lucro/rec*100 if rec > 0 else 0
                            resumo_fin += (f"Safra {safra}: receita R$ {rec:,.0f}, custo R$ {custo:,.0f}, "
                                          f"lucro R$ {lucro:,.0f}, margem {margem:.1f}%\n")

                    prompt_comp = f"""Você é um consultor agrícola analisando o histórico de safras de uma propriedade rural brasileira no sistema IAAgro Pro.

HISTÓRICO DE PRODUTIVIDADE:
{resumo_hist if resumo_hist else "Sem dados de produtividade."}

HISTÓRICO FINANCEIRO:
{resumo_fin if resumo_fin else "Sem dados financeiros."}

Gere uma análise comparativa profissional com:
1. TENDÊNCIA PRODUTIVA — a propriedade está evoluindo ou regredindo? Por quê?
2. EFICIÊNCIA FINANCEIRA — qual safra teve melhor relação custo-benefício?
3. PONTOS DE ATENÇÃO — o que chama atenção negativamente?
4. DESTAQUES POSITIVOS — o que está indo bem?
5. RECOMENDAÇÕES ESTRATÉGICAS — top 3 ações para melhorar resultados nas próximas safras
6. PROJEÇÃO — se mantida a tendência, qual a expectativa para a próxima safra?

Seja objetivo, técnico e prático para o produtor rural brasileiro. Máximo 400 palavras."""

                    try:
                        resp_ia = requests.post(
                            "https://api.anthropic.com/v1/messages",
                            headers=get_anthropic_headers(),
                            json={"model":"claude-sonnet-4-20250514","max_tokens":900,
                                  "messages":[{"role":"user","content":prompt_comp}]},
                            timeout=35
                        )
                        if resp_ia.status_code == 200:
                            analise_comp = resp_ia.json()["content"][0]["text"]
                            st.markdown(f'''<div style="background:#0f3460;color:#f1f5f9;padding:22px 26px;
                            border-radius:14px;border-left:5px solid #6ee7b7;
                            font-size:14px;line-height:2;white-space:pre-wrap;font-weight:500;">
{analise_comp}
                            </div>''', unsafe_allow_html=True)

                            # PDF da análise
                            if st.button("🖨️ Gerar PDF da Análise", key="btn_pdf_comp"):
                                try:
                                    from reportlab.lib.units import cm
                                    buf_cp = BytesIO()
                                    doc_cp = SimpleDocTemplate(buf_cp, pagesize=A4,
                                                               rightMargin=2*cm, leftMargin=2*cm,
                                                               topMargin=2*cm, bottomMargin=2*cm)
                                    sty_cp = getSampleStyleSheet()
                                    el_cp  = []
                                    if os.path.exists("IAAgrologo.jpeg"):
                                        el_cp.append(Image("IAAgrologo.jpeg", width=3*cm, height=1.5*cm))
                                    el_cp.append(Spacer(1,8))
                                    el_cp.append(Paragraph("<b>ANÁLISE COMPARATIVA DE SAFRAS — IAAgro IA</b>", sty_cp["Title"]))
                                    el_cp.append(Paragraph(f"Gerado em: {date.today().strftime('%d/%m/%Y')}", sty_cp["Normal"]))
                                    el_cp.append(Spacer(1,12))
                                    el_cp.append(Paragraph("<b>HISTÓRICO DE PRODUTIVIDADE</b>", sty_cp["Heading2"]))
                                    for linha in resumo_hist.split("\n"):
                                        if linha.strip():
                                            el_cp.append(Paragraph(linha, sty_cp["BodyText"]))
                                    el_cp.append(Spacer(1,8))
                                    el_cp.append(Paragraph("<b>HISTÓRICO FINANCEIRO</b>", sty_cp["Heading2"]))
                                    for linha in resumo_fin.split("\n"):
                                        if linha.strip():
                                            el_cp.append(Paragraph(linha, sty_cp["BodyText"]))
                                    el_cp.append(Spacer(1,12))
                                    el_cp.append(Paragraph("<b>ANÁLISE IA</b>", sty_cp["Heading2"]))
                                    el_cp.append(Spacer(1,6))
                                    for linha in analise_comp.split("\n"):
                                        if linha.strip():
                                            el_cp.append(Paragraph(linha, sty_cp["BodyText"]))
                                            el_cp.append(Spacer(1,3))
                                    doc_cp.build(el_cp)
                                    pdf_cp = buf_cp.getvalue()
                                    buf_cp.close()
                                    st.download_button("📥 Baixar PDF", data=pdf_cp,
                                        file_name=f"analise_safras_{date.today()}.pdf",
                                        mime="application/pdf", use_container_width=True)
                                except Exception as ep:
                                    error_box(f"Erro PDF: {ep}")
                        else:
                            warning_box("IA indisponível. Verifique a conexão.")
                    except Exception as e:
                        error_box(f"Erro na análise IA: {e}")


# ─────────────────────────────────────────────
# MENU: MAPA DE COLHEITA IA
# ─────────────────────────────────────────────
elif menu == "🗺️ Mapa de Colheita IA":
    st.header("🗺️ Mapa de Colheita — Análise por Inteligência Artificial")
    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
    📡 Carregue o mapa de colheita gerado pela colheitadeira (John Deere, Case, New Holland, Claas, etc.)
    nos formatos CSV, Excel, GeoJSON ou Shapefile. A IA analisa produtividade por zona,
    variabilidade espacial, pontos críticos e gera recomendações de manejo.
    </div>''', unsafe_allow_html=True)

    # ── Dependências opcionais ──
    try:
        import numpy as np
        NUMPY_OK = True
    except ImportError:
        NUMPY_OK = False
    try:
        import geopandas as gpd
        GEO_OK = True
    except ImportError:
        GEO_OK = False
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        PLOTLY_OK = True
    except ImportError:
        PLOTLY_OK = False

    if not NUMPY_OK:
        st.markdown('''<div style="background:#78350f;color:#fff;padding:12px 18px;
        border-radius:10px;border-left:5px solid #f59e0b;font-weight:600;">
        ⚠️ Para análise completa instale: pip install numpy plotly geopandas</div>''',
        unsafe_allow_html=True)

    # ══ FUNÇÕES AUXILIARES ══════════════════════════════════════════════
    def detectar_coluna_produtividade(colunas):
        candidatos = ["produtividade","yield","Yield","YIELD","Prod","prod","PROD",
                      "HarvestMass","harvest_mass","Massa","massa","sc_ha","sc/ha",
                      "sacas","Sacas","bu_ac","bu/ac","t_ha","t/ha","ton_ha",
                      "Rendimento","rendimento","productivity","Productivity"]
        for c in candidatos:
            if c in colunas: return c
        for col in colunas:
            for chave in ["prod","yield","mass","sacas","rendim","sc","bu"]:
                if chave.lower() in col.lower(): return col
        return None

    def detectar_colunas_geo(colunas):
        lat_c = next((c for c in ["lat","Lat","LAT","latitude","Latitude","LATITUDE","y","Y"] if c in colunas), None)
        lon_c = next((c for c in ["lon","Lon","LON","lng","Lng","LNG","longitude","Longitude","LONGITUDE","x","X"] if c in colunas), None)
        if not lat_c: lat_c = next((c for c in colunas if "lat" in c.lower()), None)
        if not lon_c: lon_c = next((c for c in colunas if any(x in c.lower() for x in ["lon","lng"])), None)
        return lat_c, lon_c

    def zonear_produtividade(df, col_prod):
        import numpy as np
        p33 = np.percentile(df[col_prod].dropna(), 33)
        p66 = np.percentile(df[col_prod].dropna(), 66)
        df = df.copy()
        df["Zona"] = df[col_prod].apply(lambda v: "🔴 Baixa" if v < p33 else ("🟡 Média" if v < p66 else "🟢 Alta"))
        return df, p33, p66

    def calcular_estatisticas(df, col_prod):
        s = {}
        s["media"]     = float(df[col_prod].mean())
        s["mediana"]   = float(df[col_prod].median())
        s["desvio"]    = float(df[col_prod].std())
        s["minimo"]    = float(df[col_prod].min())
        s["maximo"]    = float(df[col_prod].max())
        s["cv"]        = float(df[col_prod].std()/df[col_prod].mean()*100) if s["media"] > 0 else 0
        s["total_pts"] = len(df)
        if "Zona" in df.columns:
            for z in ["🔴 Baixa","🟡 Média","🟢 Alta"]:
                sub = df[df["Zona"]==z]
                s[f"pct_{z}"] = round(len(sub)/len(df)*100, 1)
                s[f"med_{z}"] = round(sub[col_prod].mean(), 1) if len(sub) > 0 else 0
        return s

    def gerar_recomendacoes(stats, col_prod, cultura, area_ha):
        cv        = stats.get("cv", 0)
        media     = stats.get("media", 0)
        pct_baixa = stats.get("pct_🔴 Baixa", 0)
        pct_alta  = stats.get("pct_🟢 Alta",  0)
        med_baixa = stats.get("med_🔴 Baixa", 0)
        med_alta  = stats.get("med_🟢 Alta",  0)
        gap       = med_alta - med_baixa
        recs = []

        if cv > 35:
            recs.append({"zona":"Campo todo","tipo":"⚠️ ALTA VARIABILIDADE","cor":"#7f1d1d","borda":"#ef4444",
                "texto":f"CV de {cv:.1f}% indica alta heterogeneidade espacial. Implante Aplicação em Taxa "
                        f"Variável (VRA). Realize amostragem por zona de manejo e verifique histórico de compactação."})
        elif cv > 20:
            recs.append({"zona":"Campo todo","tipo":"ℹ️ VARIABILIDADE MODERADA","cor":"#1e3a5f","borda":"#3b82f6",
                "texto":f"CV de {cv:.1f}% é moderado. Avalie mapeamento de solo para identificar causas da variabilidade."})
        else:
            recs.append({"zona":"Campo todo","tipo":"✅ BOA UNIFORMIDADE","cor":"#14532d","borda":"#22c55e",
                "texto":f"CV de {cv:.1f}% indica boa uniformidade. Continue o manejo atual."})

        if pct_baixa > 15:
            recs.append({"zona":"🔴 Zona Baixa","tipo":"🔴 INTERVENÇÃO PRIORITÁRIA","cor":"#7f1d1d","borda":"#ef4444",
                "texto":f"{pct_baixa:.0f}% da área com produtividade baixa (média {med_baixa:.1f}). Ações: "
                        f"(1) Coleta de solo detalhada por zona; "
                        f"(2) Investigar compactação com penetrômetro; "
                        f"(3) Verificar drenagem e histórico de doenças; "
                        f"(4) Aumentar dose de P e K em ≈30%; "
                        f"(5) Considerar calagem diferenciada se pH < 5.8."})

        if pct_alta > 20 and med_alta > 0:
            recs.append({"zona":"🟢 Zona Alta","tipo":"🟢 POTENCIAL A EXPLORAR","cor":"#14532d","borda":"#22c55e",
                "texto":f"Zona de alta produtividade ({pct_alta:.0f}% da área, média {med_alta:.1f}). "
                        f"Mantenha adubação de reposição precisa. Priorize fungicidas preventivos. "
                        f"Use como referência para seleção de cultivares de alto potencial."})

        if gap > 10:
            ganho = gap * 0.4 * area_ha
            recs.append({"zona":"Zonas B vs A","tipo":"📊 GAP PRODUTIVO","cor":"#78350f","borda":"#f59e0b",
                "texto":f"Diferença de {gap:.1f} sc/ha entre zonas alta e baixa. "
                        f"Potencial de ganho com manejo diferenciado: ≈{ganho:.0f} sacas adicionais/safra "
                        f"elevando zona baixa em 40%."})

        bench = {"Soja":60,"Milho":180,"Trigo":55,"Feijão":40,"Arroz":160,"Algodão":280,"Café":35}.get(cultura, 60)
        if media < bench * 0.75:
            recs.append({"zona":"Toda lavoura","tipo":f"📉 ABAIXO DO POTENCIAL ({cultura})","cor":"#4a044e","borda":"#a855f7",
                "texto":f"Média {media:.1f} está {((bench-media)/bench*100):.0f}% abaixo da referência "
                        f"regional ({bench} para {cultura}). Revisar programa completo: solo, semente, nutrição e fitossanidade."})
        elif media >= bench:
            recs.append({"zona":"Toda lavoura","tipo":f"🏆 ACIMA DA MÉDIA ({cultura})","cor":"#064e3b","borda":"#10b981",
                "texto":f"Parabéns! Média {media:.1f} supera a referência de {bench} para {cultura}. "
                        f"Documente o manejo desta safra como referência para as próximas."})
        return recs

    def chamar_ia_colheita(stats, col_prod, cultura, area_ha, nome_arquivo, recs):
        try:
            resumo_rec = "\n".join([f"- {r['tipo']} ({r['zona']}): {r['texto'][:100]}..." for r in recs])
            prompt = f"""Você é um agrônomo especialista em agricultura de precisão analisando um mapa de colheita do app IAAgro.

DADOS:
- Arquivo: {nome_arquivo} | Cultura: {cultura} | Área: {area_ha} ha | Pontos: {stats['total_pts']}

ESTATÍSTICAS:
- Média: {stats['media']:.1f} sc/ha | Mediana: {stats['mediana']:.1f}
- Mínimo: {stats['minimo']:.1f} | Máximo: {stats['maximo']:.1f}
- Desvio padrão: {stats['desvio']:.1f} | CV: {stats['cv']:.1f}%
- Zona Baixa: {stats.get('pct_🔴 Baixa',0):.0f}% da área (média {stats.get('med_🔴 Baixa',0):.1f})
- Zona Média: {stats.get('pct_🟡 Média',0):.0f}% da área (média {stats.get('med_🟡 Média',0):.1f})
- Zona Alta:  {stats.get('pct_🟢 Alta',0):.0f}% da área (média {stats.get('med_🟢 Alta',0):.1f})

RECOMENDAÇÕES AUTOMÁTICAS:
{resumo_rec}

Gere um laudo agronômico profissional com:
1. DIAGNÓSTICO GERAL (2-3 frases sobre desempenho da lavoura)
2. ANÁLISE DA VARIABILIDADE ESPACIAL (interprete o CV e causas prováveis)
3. PRIORIDADES DE MANEJO (top 3 ações para próxima safra)
4. PROJEÇÃO DE GANHO (o que é possível alcançar com manejo diferenciado)
5. NOTA DO TALHÃO (0-100 com justificativa breve)

Seja direto, técnico e acessível ao produtor rural brasileiro. Máximo 350 palavras."""
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=get_anthropic_headers(),
                json={"model":"claude-sonnet-4-20250514","max_tokens":900,
                      "messages":[{"role":"user","content":prompt}]},
                timeout=35
            )
            if resp.status_code == 200:
                return resp.json()["content"][0]["text"]
        except Exception:
            pass
        return None

    # ══ UPLOAD ═══════════════════════════════════════════════════════════
    st.subheader("📂 Carregar Mapa de Colheita")
    col_up1, col_up2 = st.columns([2,1])
    with col_up1:
        arquivo = st.file_uploader(
            "Selecione o arquivo",
            type=["csv","xlsx","xls","geojson","json","zip"],
            help="CSV/Excel: John Deere Ops Center, Climate, AFS Connect | GeoJSON/Shapefile ZIP"
        )
    with col_up2:
        cultura_mapa = st.selectbox("Cultura", ["Soja","Milho","Trigo","Feijão","Algodão","Arroz","Canola","Café","Outro"], key="cultura_mapa_sel")
        area_mapa    = st.number_input("Área (ha)", min_value=0.1, value=float(st.session_state.dados.get("area",50.0)), key="area_mapa_num")

    if arquivo is not None and arquivo.name != st.session_state.harvest_arquivo:
        st.session_state.harvest_arquivo = arquivo.name
        st.session_state.harvest_df      = None
        st.session_state.harvest_analise = None
        with st.spinner(f"⏳ Lendo {arquivo.name}..."):
            try:
                nome  = arquivo.name.lower()
                df_raw = None
                if nome.endswith(".csv"):
                    conteudo = arquivo.read().decode("utf-8", errors="replace")
                    arquivo.seek(0)
                    sep = ";" if conteudo.count(";") > conteudo.count(",") else ","
                    df_raw = pd.read_csv(arquivo, sep=sep, encoding="utf-8", on_bad_lines="skip")
                elif nome.endswith((".xlsx",".xls")):
                    df_raw = pd.read_excel(arquivo)
                elif nome.endswith((".geojson",".json")):
                    if GEO_OK:
                        import geopandas as gpd
                        gdf    = gpd.read_file(arquivo)
                        df_raw = pd.DataFrame(gdf.drop(columns="geometry", errors="ignore"))
                        try:
                            df_raw["latitude"]  = gdf.geometry.centroid.y
                            df_raw["longitude"] = gdf.geometry.centroid.x
                        except Exception: pass
                    else:
                        dados_geo = json.load(arquivo)
                        rows = []
                        for feat in dados_geo.get("features",[]):
                            row = feat.get("properties",{}).copy()
                            geom = feat.get("geometry",{})
                            if geom.get("type") == "Point":
                                row["longitude"] = geom["coordinates"][0]
                                row["latitude"]  = geom["coordinates"][1]
                            rows.append(row)
                        df_raw = pd.DataFrame(rows)
                elif nome.endswith(".zip") and GEO_OK:
                    import geopandas as gpd, zipfile, tempfile
                    with zipfile.ZipFile(arquivo) as zf:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            zf.extractall(tmpdir)
                            shps = [f for f in os.listdir(tmpdir) if f.endswith(".shp")]
                            if shps:
                                gdf    = gpd.read_file(os.path.join(tmpdir, shps[0]))
                                df_raw = pd.DataFrame(gdf.drop(columns="geometry", errors="ignore"))
                                try:
                                    df_raw["latitude"]  = gdf.geometry.centroid.y
                                    df_raw["longitude"] = gdf.geometry.centroid.x
                                except Exception: pass
                elif nome.endswith(".zip"):
                    st.markdown('''<div style="background:#78350f;color:#fff;padding:12px 18px;border-radius:10px;border-left:5px solid #f59e0b;font-weight:600;">⚠️ Para Shapefile: pip install geopandas</div>''', unsafe_allow_html=True)

                if df_raw is not None and len(df_raw) > 0:
                    st.session_state.harvest_df = df_raw
                    success_box(f"✅ {arquivo.name} — {len(df_raw):,} pontos carregados")
                else:
                    error_box("Não foi possível ler. Verifique o formato.")
            except Exception as e:
                error_box(f"Erro: {e}")

    # ══ CONFIGURAR E ANALISAR ════════════════════════════════════════════
    if st.session_state.harvest_df is not None:
        df = st.session_state.harvest_df.copy()
        st.divider()
        st.subheader("⚙️ Configurar Análise")

        col_prod_auto = detectar_coluna_produtividade(df.columns.tolist())
        lat_auto, lon_auto = detectar_colunas_geo(df.columns.tolist())

        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            col_prod = st.selectbox("Coluna de Produtividade", df.columns.tolist(),
                index=df.columns.tolist().index(col_prod_auto) if col_prod_auto in df.columns else 0, key="col_prod_sel")
        with cc2:
            col_lat = st.selectbox("Coluna de Latitude", ["(nenhuma)"]+df.columns.tolist(),
                index=(["(nenhuma)"]+df.columns.tolist()).index(lat_auto) if lat_auto in df.columns else 0, key="col_lat_sel")
        with cc3:
            col_lon = st.selectbox("Coluna de Longitude", ["(nenhuma)"]+df.columns.tolist(),
                index=(["(nenhuma)"]+df.columns.tolist()).index(lon_auto) if lon_auto in df.columns else 0, key="col_lon_sel")

        cc4, cc5 = st.columns(2)
        with cc4:
            unidade = st.selectbox("Unidade", ["sc/ha (sacas)","t/ha (toneladas)","kg/ha","bu/ac"], key="unid_sel")
        with cc5:
            st.checkbox("Remover outliers automático (±3σ)", value=True, key="filtro_out")

        df[col_prod] = pd.to_numeric(df[col_prod], errors="coerce")
        df = df.dropna(subset=[col_prod])
        df = df[df[col_prod] > 0]
        if NUMPY_OK and st.session_state.get("filtro_out", True):
            import numpy as np
            mu, sigma = df[col_prod].mean(), df[col_prod].std()
            df = df[abs(df[col_prod] - mu) <= 3 * sigma]

        st.markdown(f'<div style="background:#0f3460;color:#93c5fd;padding:8px 14px;border-radius:8px;font-size:12px;font-weight:700;">'
                    f'📊 {len(df):,} pontos válidos após filtro | Faixa: {df[col_prod].min():.1f} – {df[col_prod].max():.1f} | Média prévia: {df[col_prod].mean():.1f}</div>',
                    unsafe_allow_html=True)

        if st.button("🚀 Analisar Mapa com IA", use_container_width=True, key="btn_analisar"):
            with st.spinner("🤖 Processando... gerando zonas, gráficos e laudo IA..."):
                df_z, p33, p66 = zonear_produtividade(df, col_prod)
                stats           = calcular_estatisticas(df_z, col_prod)
                recs            = gerar_recomendacoes(stats, col_prod, cultura_mapa, area_mapa)
                laudo_ia        = chamar_ia_colheita(stats, col_prod, cultura_mapa, area_mapa,
                                                     st.session_state.harvest_arquivo, recs)

                has_geo = (col_lat != "(nenhuma)" and col_lon != "(nenhuma)"
                           and col_lat in df_z.columns and col_lon in df_z.columns)
                if has_geo:
                    df_z[col_lat] = pd.to_numeric(df_z[col_lat], errors="coerce")
                    df_z[col_lon] = pd.to_numeric(df_z[col_lon], errors="coerce")
                    df_z = df_z.dropna(subset=[col_lat, col_lon])

                st.session_state.harvest_analise = {
                    "df":df_z,"stats":stats,"recs":recs,"laudo_ia":laudo_ia,
                    "col_prod":col_prod,"col_lat":col_lat if has_geo else None,
                    "col_lon":col_lon if has_geo else None,"has_geo":has_geo,
                    "p33":p33,"p66":p66,"unidade":unidade,"cultura":cultura_mapa,
                    "area_ha":area_mapa,"arquivo":st.session_state.harvest_arquivo,"data":str(date.today()),
                }
                st.session_state.harvest_historico.append({
                    "arquivo":st.session_state.harvest_arquivo,"data":str(date.today()),
                    "cultura":cultura_mapa,"area_ha":area_mapa,
                    "media":round(stats["media"],1),"cv":round(stats["cv"],1),"pontos":stats["total_pts"],
                })
                salvar_dados_iaagro()
            success_box("✅ Análise concluída!")
            st.rerun()

    # ══ RESULTADOS ═══════════════════════════════════════════════════════
    if st.session_state.harvest_analise:
        an       = st.session_state.harvest_analise
        df_z     = an["df"]
        stats    = an["stats"]
        recs     = an["recs"]
        col_prod = an["col_prod"]
        unid     = an["unidade"].split()[0]

        st.divider()
        st.subheader(f"📊 {an['arquivo']} | {an['cultura']} | {an['area_ha']} ha | {an['data']}")

        # Métricas rápidas
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        c1.metric("🌾 Média",      f"{stats['media']:.1f}",     unid)
        c2.metric("📊 CV",         f"{stats['cv']:.1f}%",       "variabilidade")
        c3.metric("⬇️ Mínimo",    f"{stats['minimo']:.1f}",     unid)
        c4.metric("⬆️ Máximo",    f"{stats['maximo']:.1f}",     unid)
        c5.metric("🔴 Zona Baixa", f"{stats.get('pct_🔴 Baixa',0):.0f}%", "da área")
        c6.metric("🟢 Zona Alta",  f"{stats.get('pct_🟢 Alta',0):.0f}%",  "da área")

        # ── TABS ────────────────────────────────────────────────────────
        tab_mapa, tab_graf, tab_tab, tab_ia, tab_rec = st.tabs([
            "🗺️ Mapa Interativo","📈 Gráficos","📋 Dados","🤖 Laudo IA","📌 Recomendações"
        ])

        with tab_mapa:
            if an["has_geo"] and PLOTLY_OK:
                import plotly.express as px
                df_plot = df_z.sample(min(5000,len(df_z)), random_state=42) if len(df_z)>5000 else df_z
                fig_map = px.scatter_mapbox(
                    df_plot, lat=an["col_lat"], lon=an["col_lon"], color=col_prod,
                    color_continuous_scale=[[0,"#dc2626"],[0.4,"#f59e0b"],[0.7,"#16a34a"],[1,"#065f46"]],
                    size_max=8, zoom=13, mapbox_style="open-street-map",
                    title=f"Mapa de Produtividade — {an['cultura']}",
                    labels={col_prod: unid},
                    hover_data={col_prod:":.1f", an["col_lat"]:False, an["col_lon"]:False},
                    height=560
                )
                fig_map.update_layout(
                    paper_bgcolor="#0d2137", plot_bgcolor="#0d2137", font_color="#f1f5f9",
                    coloraxis_colorbar=dict(title=unid, tickfont=dict(color="#f1f5f9"),
                                           titlefont=dict(color="#6ee7b7")),
                    margin=dict(l=0,r=0,t=40,b=0)
                )
                st.plotly_chart(fig_map, use_container_width=True)
                st.markdown(f'''<div style="background:#0f3460;color:#fff;padding:9px 16px;
                border-radius:10px;font-size:12px;font-weight:700;text-align:center;">
                🔴 Baixa: &lt; {an["p33"]:.1f} {unid} &nbsp;|&nbsp;
                🟡 Média: {an["p33"]:.1f} – {an["p66"]:.1f} &nbsp;|&nbsp;
                🟢 Alta: &gt; {an["p66"]:.1f} {unid}
                </div>''', unsafe_allow_html=True)

            elif an["has_geo"]:
                lat_c = df_z[an["col_lat"]].mean()
                lon_c = df_z[an["col_lon"]].mean()
                mf = folium.Map(location=[lat_c, lon_c], zoom_start=13)
                cores_z = {"🔴 Baixa":"red","🟡 Média":"orange","🟢 Alta":"green"}
                for _, row in df_z.sample(min(2000,len(df_z)), random_state=42).iterrows():
                    try:
                        folium.CircleMarker([row[an["col_lat"]], row[an["col_lon"]]],
                            radius=4, color=cores_z.get(row.get("Zona",""),"gray"),
                            fill=True, fill_opacity=0.7,
                            popup=f"{col_prod}: {row[col_prod]:.1f}").add_to(mf)
                    except Exception: pass
                st_folium(mf, width=700, height=500)
            else:
                info_box("Arquivo sem coordenadas geográficas — mapa indisponível. Veja os gráficos e laudo nas outras abas.")

        with tab_graf:
            if PLOTLY_OK:
                import plotly.express as px
                import plotly.graph_objects as go
                g1, g2 = st.columns(2)
                with g1:
                    fig_h = px.histogram(df_z, x=col_prod, nbins=40, color="Zona",
                        color_discrete_map={"🔴 Baixa":"#dc2626","🟡 Média":"#f59e0b","🟢 Alta":"#16a34a"},
                        title="Distribuição por Zona", labels={col_prod:unid}, height=360)
                    fig_h.update_layout(paper_bgcolor="#0f3460",plot_bgcolor="#0f3460",font_color="#f1f5f9")
                    st.plotly_chart(fig_h, use_container_width=True)
                with g2:
                    zc = df_z["Zona"].value_counts().reset_index()
                    zc.columns = ["Zona","Pontos"]
                    fig_p = px.pie(zc, names="Zona", values="Pontos",
                        color="Zona",
                        color_discrete_map={"🔴 Baixa":"#dc2626","🟡 Média":"#f59e0b","🟢 Alta":"#16a34a"},
                        title="% da Área por Zona", height=360)
                    fig_p.update_layout(paper_bgcolor="#0f3460",font_color="#f1f5f9")
                    st.plotly_chart(fig_p, use_container_width=True)
                fig_b = px.box(df_z, x="Zona", y=col_prod, color="Zona",
                    color_discrete_map={"🔴 Baixa":"#dc2626","🟡 Média":"#f59e0b","🟢 Alta":"#16a34a"},
                    title="Box Plot por Zona de Manejo", labels={col_prod:unid}, height=380)
                fig_b.update_layout(paper_bgcolor="#0f3460",plot_bgcolor="#0d2137",
                                    font_color="#f1f5f9",showlegend=False,
                                    yaxis=dict(gridcolor="#1e3a5f"))
                st.plotly_chart(fig_b, use_container_width=True)
            else:
                st.bar_chart(df_z[col_prod].value_counts().sort_index())

            # Tabela por zona
            st.subheader("📊 Estatísticas por Zona")
            zonas_tab = []
            for z in ["🔴 Baixa","🟡 Média","🟢 Alta"]:
                sub = df_z[df_z["Zona"]==z]
                if len(sub) > 0:
                    zonas_tab.append({"Zona":z,"Pontos":len(sub),
                        "% Área":f"{len(sub)/len(df_z)*100:.1f}%",
                        f"Média {unid}":f"{sub[col_prod].mean():.1f}",
                        "Mín":f"{sub[col_prod].min():.1f}","Máx":f"{sub[col_prod].max():.1f}",
                        "Desvio":f"{sub[col_prod].std():.1f}"})
            if zonas_tab:
                st.dataframe(pd.DataFrame(zonas_tab), use_container_width=True, hide_index=True)

        with tab_tab:
            exibir = [col_prod,"Zona"]
            if an["col_lat"]: exibir.append(an["col_lat"])
            if an["col_lon"]: exibir.append(an["col_lon"])
            exibir += [c for c in df_z.columns if c not in exibir and c not in ["p33","p66"]]
            st.dataframe(df_z[[c for c in exibir if c in df_z.columns]].head(5000),
                         use_container_width=True)
            st.caption(f"Exibindo até 5.000 de {len(df_z):,} pontos")
            st.download_button("📥 Baixar CSV com zonas",
                data=df_z.to_csv(index=False).encode("utf-8"),
                file_name=f"colheita_zonas_{date.today()}.csv",
                mime="text/csv", use_container_width=True)

        with tab_ia:
            st.subheader("🤖 Laudo Agronômico — Inteligência Artificial")
            if an.get("laudo_ia"):
                st.markdown(f'''<div style="background:#0f3460;color:#f1f5f9;padding:22px 26px;
                border-radius:14px;border-left:5px solid #6ee7b7;
                font-size:14px;line-height:2;white-space:pre-wrap;font-weight:500;">
{an["laudo_ia"]}
                </div>''', unsafe_allow_html=True)
                st.divider()
                if st.button("🖨️ Gerar PDF do Laudo", key="btn_pdf_col", use_container_width=True):
                    try:
                        from reportlab.lib.units import cm
                        buf_pdf = BytesIO()
                        doc_p   = SimpleDocTemplate(buf_pdf, pagesize=A4,
                                                    rightMargin=2*cm,leftMargin=2*cm,
                                                    topMargin=2*cm,bottomMargin=2*cm)
                        sty = getSampleStyleSheet()
                        el  = []
                        if os.path.exists("IAAgrologo.jpeg"):
                            el.append(Image("IAAgrologo.jpeg", width=3*cm, height=1.5*cm))
                        el.append(Spacer(1,8))
                        el.append(Paragraph("<b>LAUDO DE MAPA DE COLHEITA — IAAgro IA</b>", sty["Title"]))
                        el.append(Paragraph(f"Arquivo: {an['arquivo']} | Cultura: {an['cultura']} | Área: {an['area_ha']} ha | Data: {an['data']}", sty["Normal"]))
                        el.append(Spacer(1,12))
                        tab_data = [["Métrica","Valor"],
                            ["Média", f"{stats['media']:.1f} {unid}"],
                            ["Mínimo/Máximo", f"{stats['minimo']:.1f} / {stats['maximo']:.1f}"],
                            ["Desvio Padrão", f"{stats['desvio']:.1f}"],
                            ["Coef. Variação", f"{stats['cv']:.1f}%"],
                            ["Pontos", f"{stats['total_pts']:,}"],
                            ["Zona Baixa", f"{stats.get('pct_🔴 Baixa',0):.0f}% — {stats.get('med_🔴 Baixa',0):.1f} {unid}"],
                            ["Zona Média",  f"{stats.get('pct_🟡 Média',0):.0f}% — {stats.get('med_🟡 Média',0):.1f} {unid}"],
                            ["Zona Alta",   f"{stats.get('pct_🟢 Alta',0):.0f}% — {stats.get('med_🟢 Alta',0):.1f} {unid}"],
                        ]
                        t_e = Table(tab_data, colWidths=[7*cm,9*cm])
                        t_e.setStyle(TableStyle([
                            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0f3460")),
                            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
                            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
                            ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
                            ("FONTSIZE",(0,0),(-1,-1),10),
                            ("GRID",(0,0),(-1,-1),0.5,colors.grey),
                            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f0f9ff")]),
                        ]))
                        el.append(t_e)
                        el.append(Spacer(1,14))
                        el.append(Paragraph("<b>LAUDO AGRONÔMICO IA</b>", sty["Heading2"]))
                        el.append(Spacer(1,6))
                        for linha in an["laudo_ia"].split("\n"):
                            if linha.strip():
                                el.append(Paragraph(linha, sty["BodyText"]))
                                el.append(Spacer(1,3))
                        el.append(Spacer(1,12))
                        el.append(Paragraph("<b>RECOMENDAÇÕES DE MANEJO</b>", sty["Heading2"]))
                        el.append(Spacer(1,6))
                        for r in recs:
                            el.append(Paragraph(f"<b>{r['tipo']} — {r['zona']}</b>", sty["Heading3"]))
                            el.append(Paragraph(r["texto"], sty["BodyText"]))
                            el.append(Spacer(1,8))
                        doc_p.build(el)
                        pdf_b = buf_pdf.getvalue()
                        buf_pdf.close()
                        st.download_button("📥 Baixar Laudo PDF", data=pdf_b,
                            file_name=f"laudo_colheita_{date.today()}.pdf",
                            mime="application/pdf", use_container_width=True)
                    except Exception as e:
                        error_box(f"Erro ao gerar PDF: {e}")
            else:
                warning_box("Laudo IA indisponível. Verifique a conexão com a internet. As recomendações automáticas estão na aba Recomendações.")

        with tab_rec:
            st.subheader("📌 Recomendações de Manejo por Zona")
            for r in recs:
                st.markdown(f'''<div style="background:{r["cor"]};color:#fff;padding:14px 18px;
                border-radius:12px;border-left:6px solid {r["borda"]};
                font-size:14px;line-height:1.9;margin:8px 0;">
                <b>{r["tipo"]}</b> &nbsp;|&nbsp; Zona: {r["zona"]}<br>{r["texto"]}
                </div>''', unsafe_allow_html=True)

            st.divider()
            st.subheader("🗓️ Plano de Ação — Próxima Safra")
            acoes = [
                ("Pré-plantio","🔬","Coletar amostras de solo por zona (mín. 1/zona)"),
                ("Pré-plantio","📐","Delimitar zonas de manejo no GPS do trator"),
                ("Plantio","🌱","Aplicar taxa variável de P e K por zona"),
                ("V3–V4","💊","Monitorar desenvolvimento por zona com fotos georeferenciadas"),
                ("Floração","🚁","NDVI por drone ou satélite para correlacionar com mapa"),
                ("Colheita","📡","Ativar monitor de produtividade para novo mapa"),
                ("Pós-colheita","📊","Comparar este mapa com o anterior no IAAgro"),
            ]
            st.dataframe(pd.DataFrame(acoes, columns=["Momento","","Ação"]),
                         use_container_width=True, hide_index=True)

    # ══ HISTÓRICO DE MAPAS ════════════════════════════════════════════════
    if st.session_state.harvest_historico:
        st.divider()
        st.subheader("📁 Histórico de Mapas Analisados")
        df_hist_m = pd.DataFrame(st.session_state.harvest_historico)
        st.dataframe(df_hist_m, use_container_width=True, hide_index=True)
        if len(st.session_state.harvest_historico) >= 2 and PLOTLY_OK:
            import plotly.graph_objects as go
            fig_ev = go.Figure()
            fig_ev.add_trace(go.Scatter(
                x=[h["arquivo"] for h in st.session_state.harvest_historico],
                y=[h["media"]   for h in st.session_state.harvest_historico],
                mode="lines+markers+text",
                text=[f"{h['media']:.1f}" for h in st.session_state.harvest_historico],
                textposition="top center",
                line=dict(color="#22c55e", width=3),
                marker=dict(size=10, color="#6ee7b7"),
            ))
            fig_ev.update_layout(
                title="Evolução da Produtividade Média entre Safras",
                paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",
                font_color="#f1f5f9", xaxis_title="Mapa/Safra",
                yaxis_title="Média sc/ha", height=300
            )
            st.plotly_chart(fig_ev, use_container_width=True)


# ─────────────────────────────────────────────
# MENU: LEITOR DE CODIGO DE BARRAS
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
