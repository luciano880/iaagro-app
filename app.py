ï»¿import streamlit as st
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

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# TESSERACT Ã¢â¬â caminho para Windows
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
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

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# SUPABASE Ã¢â¬â importa mÃÂ³dulo de integraÃÂ§ÃÂ£o
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
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

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# CORREÃâ¡ÃÆO 1: funÃÂ§ÃÂ£o sem recursÃÂ£o infinita
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
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

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# CSS UNIFICADO (sem conflitos e sem duplicatas)
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
st.markdown("""
<style>
/* Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
   RESET GERAL Ã¢â¬â evita fundo branco do Streamlit
Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="block-container"],
.main, .stApp {
    background-color: #0d2137 !important;
    color: #f1f5f9 !important;
}

/* Ã¢ââ¬Ã¢ââ¬ FUNDO GERAL Ã¢ââ¬Ã¢ââ¬ */
.stApp {
    background: linear-gradient(160deg, #0d2137 0%, #123354 50%, #1a4a73 100%) !important;
}

/* Ã¢ââ¬Ã¢ââ¬ TEXTO GERAL Ã¢ââ¬Ã¢ââ¬ */
p, span, div, li, label,
.stMarkdown p, .stMarkdown li,
[data-testid="stText"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] {
    color: #f1f5f9 !important;
}

/* Ã¢ââ¬Ã¢ââ¬ TÃÂTULOS Ã¢ââ¬Ã¢ââ¬ */
h1, h2, h3, h4, h5, h6 {
    color: #6ee7b7 !important;
    font-weight: 800 !important;
}

/* Ã¢ââ¬Ã¢ââ¬ LABELS DE CAMPOS Ã¢ââ¬Ã¢ââ¬ */
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

/* Ã¢ââ¬Ã¢ââ¬ INPUTS TEXT / NUMBER Ã¢ââ¬Ã¢ââ¬ */
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

/* Ã¢ââ¬Ã¢ââ¬ SELECTBOX Ã¢ââ¬Ã¢ââ¬ */
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

/* Ã¢ââ¬Ã¢ââ¬ DATE INPUT Ã¢ââ¬Ã¢ââ¬ */
.stDateInput input {
    background: #0f3460 !important;
    color: #ffffff !important;
    border: 2px solid #22c55e !important;
    border-radius: 10px !important;
}

/* Ã¢ââ¬Ã¢ââ¬ TEXTAREA Ã¢ââ¬Ã¢ââ¬ */
.stTextArea textarea {
    background: #0f3460 !important;
    color: #ffffff !important;
    border: 2px solid #22c55e !important;
    border-radius: 10px !important;
}

/* Ã¢ââ¬Ã¢ââ¬ NÃÅ¡MERO (botÃÂµes +/-) Ã¢ââ¬Ã¢ââ¬ */
.stNumberInput button {
    background: #1a4a73 !important;
    color: #ffffff !important;
    border: 1px solid #60a5fa !important;
    border-radius: 6px !important;
}

/* Ã¢ââ¬Ã¢ââ¬ BOTÃâ¢ES Ã¢ââ¬Ã¢ââ¬ */
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

/* Ã¢ââ¬Ã¢ââ¬ DOWNLOAD BUTTON Ã¢ââ¬Ã¢ââ¬ */
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

/* Ã¢ââ¬Ã¢ââ¬ MÃâ°TRICAS Ã¢ââ¬Ã¢ââ¬ */
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

/* Ã¢ââ¬Ã¢ââ¬ DATAFRAMES Ã¢ââ¬Ã¢ââ¬ */
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

/* Ã¢ââ¬Ã¢ââ¬ ALERTAS Ã¢ââ¬Ã¢ââ¬ */
.stAlert {
    border-radius: 12px !important;
    font-weight: 600 !important;
}
.stAlert *, .stAlert p, .stAlert div, .stAlert span {
    color: #0f172a !important;
    font-weight: 600 !important;
}

/* Ã¢ââ¬Ã¢ââ¬ TABS Ã¢ââ¬Ã¢ââ¬ */
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

/* Ã¢ââ¬Ã¢ââ¬ EXPANDER Ã¢ââ¬Ã¢ââ¬ */
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

/* Ã¢ââ¬Ã¢ââ¬ SIDEBAR Ã¢ââ¬Ã¢ââ¬ */
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

/* Ã¢ââ¬Ã¢ââ¬ PROGRESS BAR Ã¢ââ¬Ã¢ââ¬ */
.stProgress > div > div {
    background: linear-gradient(90deg, #00c853, #16a34a) !important;
    border-radius: 10px !important;
}
.stProgress > div {
    background: #1a4a73 !important;
    border-radius: 10px !important;
}

/* Ã¢ââ¬Ã¢ââ¬ UPLOAD Ã¢ââ¬Ã¢ââ¬ */
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
/* Texto "Drag and drop" e instruÃÂ§ÃÂµes */
div[data-testid="stFileUploaderDropzone"] span,
div[data-testid="stFileUploaderDropzone"] p,
div[data-testid="stFileUploaderDropzone"] small {
    color: #ffffff !important;
    font-size: 14px !important;
}
/* BotÃÂ£o Browse/Upload */
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
/* ÃÂcone de upload */
div[data-testid="stFileUploaderDropzone"] svg {
    fill: #22c55e !important;
    stroke: #22c55e !important;
}

/* Ã¢ââ¬Ã¢ââ¬ INFO BOX dentro do st.info Ã¢ââ¬Ã¢ââ¬ */
[data-testid="stNotification"] * { color: #0f172a !important; }

/* Ã¢ââ¬Ã¢ââ¬ DIVIDER Ã¢ââ¬Ã¢ââ¬ */
hr { border-color: #1e3a5f !important; }

/* Ã¢ââ¬Ã¢ââ¬ RADIO Ã¢ââ¬Ã¢ââ¬ */
.stRadio > div { background: transparent !important; }
.stRadio [data-testid="stWidgetLabel"] p { color: #6ee7b7 !important; }

/* Ã¢ââ¬Ã¢ââ¬ CHECKBOX Ã¢ââ¬Ã¢ââ¬ */
.stCheckbox label p { color: #f1f5f9 !important; }

/* Ã¢ââ¬Ã¢ââ¬ MULTISELECT Ã¢ââ¬Ã¢ââ¬ */
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
/* Dropdown aberto Ã¢â¬â fundo e texto dos itens */
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
    content: "Ã¢Åâ¦ Todos selecionados" !important;
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

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# HELPERS DE NOTIFICAÃâ¡ÃÆO Ã¢â¬â garantem legibilidade
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
def info_box(msg):
    st.markdown(f'<div style="background:#1e3a5f;color:#ffffff;padding:13px 18px;border-radius:10px;'
                f'border-left:5px solid #3b82f6;font-weight:600;font-size:15px;margin:6px 0;">'
                f'Ã¢âÂ¹Ã¯Â¸Â {msg}</div>', unsafe_allow_html=True)

def success_box(msg):
    st.markdown(f'<div style="background:#14532d;color:#ffffff;padding:13px 18px;border-radius:10px;'
                f'border-left:5px solid #22c55e;font-weight:600;font-size:15px;margin:6px 0;">'
                f'Ã¢Åâ¦ {msg}</div>', unsafe_allow_html=True)

def warning_box(msg):
    st.markdown(f'<div style="background:#78350f;color:#ffffff;padding:13px 18px;border-radius:10px;'
                f'border-left:5px solid #f59e0b;font-weight:600;font-size:15px;margin:6px 0;">'
                f'Ã¢Å¡Â Ã¯Â¸Â {msg}</div>', unsafe_allow_html=True)

def error_box(msg):
    st.markdown(f'<div style="background:#7f1d1d;color:#ffffff;padding:13px 18px;border-radius:10px;'
                f'border-left:5px solid #ef4444;font-weight:600;font-size:15px;margin:6px 0;">'
                f'Ã¢ÂÅ {msg}</div>', unsafe_allow_html=True)


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# ARQUIVOS DE PERSISTÃÅ NCIA
# usuarios.json fica no repositÃÂ³rio (persistente entre deploys)
# dados operacionais ficam em /tmp (sessÃÂ£o)
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
import pathlib

_BASE_DIR = pathlib.Path("/tmp/iaagro_data")
_BASE_DIR.mkdir(parents=True, exist_ok=True)

# UsuÃÂ¡rios: salva no diretÃÂ³rio do app (persistente no Git/repositÃÂ³rio)
_REPO_DIR = pathlib.Path(__file__).parent if "__file__" in dir() else pathlib.Path(".")
ARQUIVO_USUARIOS     = str(_REPO_DIR / "usuarios.json")

# Dados operacionais em /tmp (rÃÂ¡pido, mas reseta no redeploy)
ARQUIVO_ESTOQUE      = str(_BASE_DIR / "estoque.json")
ARQUIVO_AREAS        = str(_BASE_DIR / "areas.json")
ARQUIVO_DADOS_IAAGRO = str(_BASE_DIR / "dados_iaagro.json")
DB_FILE              = str(_BASE_DIR / "iaagro.db")

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# CORREÃâ¡ÃÆO 9: senhas com hash (hashlib)
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    return hash_senha(senha) == hash_armazenado

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# BANCO DE DADOS SQLITE Ã¢â¬â histÃÂ³rico de solo
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
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

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# VALIDAÃâ¡ÃÆO DE CAMPOS
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
def validar_ph(v):
    return 3.5 <= v <= 9.0

def validar_email_fmt(email):
    return bool(re.match(r'^[^@]+@[^@]+\.[^@]+$', email))

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# EXPORTAR XLSX
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
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

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# BACKUP / RESTORE
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
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
            return False, "Arquivo invÃÂ¡lido Ã¢â¬â nÃÂ£o parece ser um backup do IAAgro."
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
        return True, f"Backup de {dados.get('backup_data','?')} restaurado! {n_areas} ÃÂ¡reas, {n_estoque} itens de estoque."
    except json.JSONDecodeError:
        return False, "Arquivo corrompido Ã¢â¬â nÃÂ£o ÃÂ© um JSON vÃÂ¡lido."
    except Exception as e:
        return False, f"Erro ao restaurar: {e}"

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# EMAIL SMTP Ã¢â¬â alertas de estoque
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
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
    """Envia email com token de 6 dÃÂ­gitos para recuperaÃÂ§ÃÂ£o de senha."""
    try:
        cfg = st.session_state.get("email_config", {})
        if not cfg.get("ativo") or not cfg.get("remetente"):
            return False, "Email nÃÂ£o configurado. VÃÂ¡ em Ã¢Å¡â¢Ã¯Â¸Â ConfiguraÃÂ§ÃÂµes Ã¢â â Email SMTP."
        corpo = f"""
        <div style="font-family:Arial,sans-serif;max-width:500px;margin:auto;
        background:#0f2744;color:#fff;border-radius:14px;padding:30px;">
        <h2 style="color:#22c55e;text-align:center;">Ã°Å¸ÅÂ¿ IAAgro Pro</h2>
        <h3 style="text-align:center;color:#fff;">RecuperaÃÂ§ÃÂ£o de Senha</h3>
        <p>OlÃÂ¡, <b>{usuario}</b>!</p>
        <p>Recebemos uma solicitaÃÂ§ÃÂ£o para redefinir sua senha.</p>
        <p>Use o cÃÂ³digo abaixo para criar uma nova senha:</p>
        <div style="background:#1e3a5f;border-radius:10px;padding:20px;text-align:center;
        margin:20px 0;">
          <span style="font-size:36px;font-weight:900;letter-spacing:10px;color:#22c55e;">
          {token}
          </span>
        </div>
        <p style="color:#93c5fd;font-size:13px;">
        Ã¢ÂÂ±Ã¯Â¸Â Este cÃÂ³digo expira em <b>15 minutos</b>.<br>
        Se nÃÂ£o foi vocÃÂª, ignore este email.
        </p>
        <hr style="border-color:#1e3a5f;margin:20px 0;">
        <p style="color:#6b7280;font-size:11px;text-align:center;">
        IAAgro Pro Ã¢â¬â Sistema de GestÃÂ£o AgrÃÂ­cola Inteligente
        </p>
        </div>
        """
        msg = MIMEMultipart()
        msg["From"]    = cfg["remetente"]
        msg["To"]      = email_destino
        msg["Subject"] = "Ã°Å¸ÅÂ¿ IAAgro Pro Ã¢â¬â CÃÂ³digo de recuperaÃÂ§ÃÂ£o de senha"
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
               if 0 < i.get("Quantidade",0) <= i.get("Estoque MÃÂ­nimo",0)]
    if zerados or baixos:
        corpo = "<h2>Ã¢Å¡Â Ã¯Â¸Â IAAgro Pro Ã¢â¬â Alerta de Estoque</h2><ul>"
        for i in zerados:
            corpo += f"<li>Ã¢ÂÅ <b>{i['Insumo']}</b>: estoque ZERADO</li>"
        for i in baixos:
            corpo += f"<li>Ã¢Å¡Â Ã¯Â¸Â <b>{i['Insumo']}</b>: {i['Quantidade']:.1f} (mÃÂ­n: {i['Estoque MÃÂ­nimo']:.1f})</li>"
        corpo += "</ul><p>Acesse o IAAgro Pro para repor o estoque.</p>"
        enviar_email_alerta(cfg["email_destino"], "Ã¢Å¡Â Ã¯Â¸Â IAAgro Ã¢â¬â Alerta de Estoque", corpo)


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# CLIMA EM TEMPO REAL Ã¢â¬â Open-Meteo (gratuito, sem API key)
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
def buscar_clima(lat, lon):
    """Busca clima atual + previsÃÂ£o 7 dias via Open-Meteo (gratuita, sem chave)."""
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
    """Converte weathercode Open-Meteo em emoji + descriÃÂ§ÃÂ£o."""
    mapa = {
        0: ("Ã¢Ëâ¬Ã¯Â¸Â", "CÃÂ©u limpo"), 1: ("Ã°Å¸ÅÂ¤Ã¯Â¸Â", "Principalmente limpo"),
        2: ("Ã¢âºâ¦", "Parcialmente nublado"), 3: ("Ã¢ËÂÃ¯Â¸Â", "Nublado"),
        45: ("Ã°Å¸ÅÂ«Ã¯Â¸Â", "NÃÂ©voa"), 48: ("Ã°Å¸ÅÂ«Ã¯Â¸Â", "NÃÂ©voa com geada"),
        51: ("Ã°Å¸ÅÂ¦Ã¯Â¸Â", "Garoa leve"), 53: ("Ã°Å¸ÅÂ¦Ã¯Â¸Â", "Garoa moderada"),
        55: ("Ã°Å¸ÅÂ§Ã¯Â¸Â", "Garoa intensa"), 61: ("Ã°Å¸ÅÂ§Ã¯Â¸Â", "Chuva leve"),
        63: ("Ã°Å¸ÅÂ§Ã¯Â¸Â", "Chuva moderada"), 65: ("Ã°Å¸ÅÂ§Ã¯Â¸Â", "Chuva intensa"),
        71: ("Ã°Å¸ÅÂ¨Ã¯Â¸Â", "Neve leve"), 73: ("Ã°Å¸ÅÂ¨Ã¯Â¸Â", "Neve moderada"),
        75: ("Ã¢ÂâÃ¯Â¸Â", "Neve intensa"), 80: ("Ã°Å¸ÅÂ¦Ã¯Â¸Â", "Chuva rÃÂ¡pida leve"),
        81: ("Ã°Å¸ÅÂ§Ã¯Â¸Â", "Chuva rÃÂ¡pida moderada"), 82: ("Ã¢âºËÃ¯Â¸Â", "Chuva rÃÂ¡pida intensa"),
        95: ("Ã¢âºËÃ¯Â¸Â", "Trovoada"), 96: ("Ã¢âºËÃ¯Â¸Â", "Trovoada com granizo"),
        99: ("Ã¢âºËÃ¯Â¸Â", "Trovoada intensa"),
    }
    return mapa.get(code, ("Ã°Å¸ÅÂ¡Ã¯Â¸Â", "Desconhecido"))

def alerta_clima_aplicacao(codigo_clima, velocidade_vento, precipitacao):
    """Retorna alerta se o clima nÃÂ£o ÃÂ© ideal para aplicaÃÂ§ÃÂ£o."""
    alertas = []
    if precipitacao > 0:
        alertas.append("Ã°Å¸ÅÂ§Ã¯Â¸Â Chuva detectada Ã¢â¬â evite aplicaÃÂ§ÃÂµes!")
    if velocidade_vento > 15:
        alertas.append(f"Ã°Å¸âÂ¨ Vento alto ({velocidade_vento:.1f} km/h) Ã¢â¬â risco de deriva!")
    if codigo_clima in [95, 96, 99]:
        alertas.append("Ã¢âºËÃ¯Â¸Â Trovoada Ã¢â¬â NÃÆO faÃÂ§a aplicaÃÂ§ÃÂµes!")
    return alertas

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# PREÃâ¡OS DE COMMODITIES Ã¢â¬â CEPEA/ESALQ via scraping
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
def buscar_dolar_awesomeapi():
    """Busca cotaÃÂ§ÃÂ£o real do dÃÂ³lar Ã¢â¬â tenta 4 fontes em sequÃÂªncia."""
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
        pass  # falha silenciada Ã¢â¬â nÃÂ£o crÃÂ­tico
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
        pass  # falha silenciada Ã¢â¬â nÃÂ£o crÃÂ­tico
    # 3. Banco Central do Brasil Ã¢â¬â PTAX
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
        pass  # falha silenciada Ã¢â¬â nÃÂ£o crÃÂ­tico
    return {"preco": 5.80, "fonte": "Offline"}


def buscar_precos_cepea_ia():
    """
    Usa Claude API com web_search para buscar preÃÂ§os CEPEA em tempo real.
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
                pass  # falha silenciada Ã¢â¬â nÃÂ£o crÃÂ­tico
        if not api_key:
            import os
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")

        if not api_key or len(api_key) < 20:
            st.session_state["_cepea_erro"] = "API key nÃÂ£o encontrada ou invÃÂ¡lida"
            return None

        hoje_str = datetime.now().strftime("%d/%m/%Y")
        prompt = (
            f"Data: {hoje_str}. "
            "Pesquise o preÃÂ§o atual de commodities agrÃÂ­colas no Brasil (CEPEA/ESALQ ou mercado fÃÂ­sico). "
            "Responda APENAS com este JSON (sem texto, sem markdown, sem explicaÃÂ§ÃÂ£o):\n"
            '{"soja":118.0,"milho":50.0,"trigo":69.0,"cafe":1850.0,"algodao":122.0,"boi":325.0,"arroz":74.0,"fonte":"CEPEA","data":"'
            + datetime.now().strftime("%d/%m/%Y") + '"}'
        )
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type":      "application/json",
                "x-api-key":         api_key,
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 500,
                "tools":      [{"type": "web_search_20250305", "name": "web_search"}],
                "messages":   [{"role": "user", "content": prompt}]
            },
            timeout=60
        )
        if resp.status_code == 200:
            blocos = resp.json().get("content", [])
            texto  = "".join(b.get("text", "") for b in blocos if b.get("type") == "text")
            texto  = texto.replace("```json", "").replace("```", "").strip()

            # Tenta encontrar JSON em qualquer parte do texto
            dados = None
            # Procura por todos os { } no texto
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
                    pass  # falha silenciada Ã¢â¬â nÃÂ£o crÃÂ­tico
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
                    "cafe":    r"caf[eÃÂ©][^0-9]*(\d+[.,]\d+)",
                    "algodao": r"algod[aÃÂ£]o[^0-9]*(\d+[.,]\d+)",
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
                    valores["data"]  = datetime.now().strftime("%d/%m/%Y")
                    st.session_state["_cepea_erro"] = ""
                    return valores

                st.session_state["_cepea_erro"] = f"JSON nÃÂ£o encontrado: {texto[:60]}"
        else:
            st.session_state["_cepea_erro"] = f"HTTP {resp.status_code}: {resp.text[:60]}"
    except Exception as e:
        st.session_state["_cepea_erro"] = f"ExceÃÂ§ÃÂ£o: {str(e)[:80]}"
    return None


def converter_para_reais(precos_cbot, dolar):
    """Converte cotaÃÂ§ÃÂµes CBOT/ICE para R$."""
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
    Busca preÃÂ§os em tempo real:
    1. DÃÂ³lar via BCB PTAX / AwesomeAPI / ExchangeRate-API
    2. Commodities via IA + web_search CEPEA (principal Ã¢â¬â funciona no Streamlit Cloud)
    3. Fallback: CBOT/ICE via Stooq / Yahoo Finance
    4. Fallback final: referÃÂªncias offline
    """
    resultado = {}
    dolar_data = buscar_dolar_awesomeapi()
    resultado["dolar"] = dolar_data
    dolar_val  = dolar_data.get("preco", 5.80)

    # Verifica cache Ã¢â¬â sÃÂ³ chama IA se passou mais de 30 min
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
        fc = f"{dados_cepea.get('fonte','CEPEA')} Ã¢â¬â {dados_cepea.get('data','')}"
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
        "soja_sc":    {"preco":115.0, "unidade":"R$/sc 60kg","praca":"PR","fonte":f"ReferÃÂªncia {hoje}"},
        "milho_sc":   {"preco": 58.0, "unidade":"R$/sc 60kg","praca":"PR","fonte":f"ReferÃÂªncia {hoje}"},
        "trigo_sc":   {"preco": 69.0, "unidade":"R$/sc 60kg","praca":"PR","fonte":f"ReferÃÂªncia {hoje}"},
        "cafe_sc":    {"preco":2250.0,"unidade":"R$/sc 60kg","praca":"SP","fonte":f"ReferÃÂªncia {hoje}"},
        "algodao_at": {"preco":120.0, "unidade":"R$/@",      "praca":"MT","fonte":f"ReferÃÂªncia {hoje}"},
        "boi_at":     {"preco":320.0, "unidade":"R$/@",      "praca":"SP","fonte":f"ReferÃÂªncia {hoje}"},
        "arroz_sc":   {"preco": 74.0, "unidade":"R$/sc 50kg","praca":"RS","fonte":f"ReferÃÂªncia {hoje}"},
    }.items():
        resultado.setdefault(chave, fb)

    resultado["_atualizado_em"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return resultado

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
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
    """Tenta extrair valores de anÃÂ¡lise de solo do texto OCR."""
    resultado = {}
    padroes = {
        "ph":              r"pH[:\s]+([0-9]+[.,][0-9]+)",
        "fosforo":         r"(?:FÃÂ³sforo|Fosforo|P)[:\s]+([0-9]+[.,][0-9]+)",
        "potassio":        r"(?:PotÃÂ¡ssio|Potassio|K)[:\s]+([0-9]+[.,][0-9]+)",
        "calcio":          r"(?:CÃÂ¡lcio|Calcio|Ca)[:\s]+([0-9]+[.,][0-9]+)",
        "magnesio":        r"(?:MagnÃÂ©sio|Magnesio|Mg)[:\s]+([0-9]+[.,][0-9]+)",
        "aluminio":        r"(?:AlumÃÂ­nio|Aluminio|Al)[:\s]+([0-9]+[.,][0-9]+)",
        "enxofre":         r"(?:Enxofre|S)[:\s]+([0-9]+[.,][0-9]+)",
        "materia_organica":r"(?:MatÃÂ©ria OrgÃÂ¢nica|M\.O\.|MO)[:\s]+([0-9]+[.,][0-9]+)",
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


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# CORREÃâ¡ÃÆO 3: funÃÂ§ÃÂµes sem duplicatas
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
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
        "corretivos_aplicados":    st.session_state.get("corretivos_aplicados", []),
    }
    # LÃÂª variÃÂ¡veis globais dinamicamente (podem nÃÂ£o existir quando funÃÂ§ÃÂ£o ÃÂ© definida)
    _sb_url    = st.secrets.get("SUPABASE_URL", "") if hasattr(st, 'secrets') else ""
    _sb_key    = st.secrets.get("SUPABASE_ANON_KEY", "") if hasattr(st, 'secrets') else ""
    _sb_token  = st.session_state.get("sb_token", "")
    _sb_uid    = st.session_state.get("sb_user_id", "")
    _sb_ok     = bool(_sb_url and _sb_key and _sb_token and _sb_uid and _SB_DISPONIVEL)

    if _sb_ok:
        try:
            ok = sb_salvar(_sb_url, _sb_key, _sb_token, _sb_uid, dados_salvos)
            if ok:
                st.session_state["_ultimo_save"] = f"Ã¢Åâ¦ Supabase {datetime.now().strftime('%H:%M:%S')}"
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
                                st.session_state["_ultimo_save"] = f"Ã¢Åâ¦ Supabase {datetime.now().strftime('%H:%M:%S')} (renovado)"
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
                st.session_state["_ultimo_save"] = f"Ã¢ÂÅ {_r.status_code}: {_r.text[:50]}"
        except Exception as e:
            st.session_state["_ultimo_save"] = f"Ã¢ÂÅ Erro: {str(e)[:40]}"
    else:
        motivo = []
        if not _sb_url: motivo.append("sem URL")
        if not _sb_key: motivo.append("sem KEY")
        if not _sb_token: motivo.append("sem token")
        if not _sb_uid: motivo.append("sem user_id")
        if not _SB_DISPONIVEL: motivo.append("mÃÂ³dulo nÃÂ£o carregou")
        st.session_state["_ultimo_save"] = f"Ã¢Å¡Â Ã¯Â¸Â Local ({', '.join(motivo)})"
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

# CORREÃâ¡ÃÆO 2: carregar_area_por_id movida para escopo global
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
    # Tenta carregar do repositÃÂ³rio primeiro
    for caminho in [ARQUIVO_USUARIOS, str(_BASE_DIR / "usuarios.json")]:
        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding="utf-8") as arquivo:
                    dados = json.load(arquivo)
                    if isinstance(dados, dict) and dados:
                        return dados
            except Exception:
                pass  # falha silenciada Ã¢â¬â nÃÂ£o crÃÂ­tico
    return {}

def salvar_usuarios(usuarios):
    # Salva no repositÃÂ³rio (persistente)
    try:
        with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
    except Exception:
        pass  # falha silenciada Ã¢â¬â nÃÂ£o crÃÂ­tico
    # Backup em /tmp tambÃÂ©m
    try:
        with open(str(_BASE_DIR / "usuarios.json"), "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
    except Exception:
        pass  # falha silenciada Ã¢â¬â nÃÂ£o crÃÂ­tico

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# SUPABASE Ã¢â¬â configuraÃÂ§ÃÂ£o
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
_SB_URL = st.secrets.get("SUPABASE_URL", "")
_SB_KEY = st.secrets.get("SUPABASE_ANON_KEY", "")
_SUPABASE_ATIVO = bool(_SB_URL and _SB_KEY and _SB_DISPONIVEL)

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# AUTO-LOGIN Ã¢â¬â restaura sessÃÂ£o via query_params
# Quando usuÃÂ¡rio recarrega a pÃÂ¡gina, o token
# salvo nos query_params restaura a sessÃÂ£o
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
def _tentar_autologin():
    """Tenta restaurar sessÃÂ£o via query_params apÃÂ³s reload."""
    try:
        params = st.query_params
        _t1  = params.get("_t1", "")
        _t2  = params.get("_t2", "")
        _t3  = params.get("_t3", "")
        _tk  = _t1 + _t2 + _t3
        _uid = params.get("_u", "")
        _pl  = params.get("_p", "free")
        _nm  = params.get("_n", "")
        if _tk and _uid and not st.session_state.get("logado"):
            _dados = sb_carregar(_SB_URL, _SB_KEY, _tk, _uid) if _SUPABASE_ATIVO else None
            if _dados is not None:
                st.session_state.logado        = True
                st.session_state.sb_token      = _tk
                st.session_state.sb_user_id    = _uid
                st.session_state.sb_plano      = _pl
                st.session_state.usuario_atual = (_nm or "UsuÃÂ¡rio").replace("_", " ")
                # Carrega TODOS os campos do Supabase
                _campos = ["dados","areas","estoque","aplicacoes","historico_produtividade",
                           "pluviometro","carencia_registros","dre_registros","calendario_eventos",
                           "harvest_historico","receituarios","safrinha_registros","fluxo_caixa",
                           "corretivos_aplicados","segmento"]
                for k in _campos:
                    if k in _dados and _dados[k] not in (None, [], {}):
                        setattr(st.session_state, k, _dados[k])
                try:
                    st.session_state.sb_plano = sb_plano(_SB_URL, _SB_KEY, _tk, _uid)
                except Exception:
                    pass
                return True
    except Exception:
        pass
    return False

if _SUPABASE_ATIVO and not st.session_state.get("logado"):
    _tentar_autologin()

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# SESSION STATE Ã¢â¬â LOGIN
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if "sb_token"   not in st.session_state: st.session_state.sb_token   = ""
if "sb_user_id" not in st.session_state: st.session_state.sb_user_id = ""
if "sb_plano"   not in st.session_state: st.session_state.sb_plano   = "free"

if "usuarios" not in st.session_state:
    st.session_state.usuarios = carregar_usuarios()

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario_atual" not in st.session_state:
    st.session_state.usuario_atual = ""

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# TELA DE LOGIN
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
def tela_login():
    """Tela de login Ã¢â¬â usa Supabase se disponÃÂ­vel, senÃÂ£o sistema local."""

    # Logo
    if os.path.exists("IAAgrologo.jpeg"):
        import base64 as _b64
        with open("IAAgrologo.jpeg", "rb") as _f:
            _logo_b64 = _b64.b64encode(_f.read()).decode()
        st.markdown(f"""<div style='text-align:center;padding:20px 0 10px;'>
        <img src='data:image/jpeg;base64,{_logo_b64}' style='max-height:120px;border-radius:12px;'/>
        </div>""", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center;color:#22c55e;'>Ã°Å¸ÅÂ¾ IAAGRO</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#94a3b8;'>InteligÃÂªncia AgrÃÂ­cola de PrecisÃÂ£o</p>", unsafe_allow_html=True)

    if _SUPABASE_ATIVO:
        # Ã¢ââ¬Ã¢ââ¬ LOGIN VIA SUPABASE Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        aba_login, aba_cadastro, aba_recuperar = st.tabs(["Ã°Å¸ââ Entrar","Ã¢Å¾â¢ Criar Conta","Ã°Å¸ââ Recuperar Senha"])

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
                        # Carrega dados do usuÃÂ¡rio do Supabase
                        dados_sb = sb_carregar(_SB_URL, _SB_KEY, res["token"], res["user_id"])
                        if dados_sb:
                            for k, v in dados_sb.items():
                                if k not in st.session_state:
                                    setattr(st.session_state, k, v)
                        # Salva refresh info nos query_params para auto-login apÃÂ³s reload
                        try:
                            import hashlib as _hl
                            _nome_url = (res["nome"] or res["email"]).replace(" ", "_")[:20]
                            # Salva token completo Ã¢â¬â query_params suporta strings longas
                            _tk_full = res["token"]
                            st.query_params["_u"] = res["user_id"]
                            st.query_params["_p"] = st.session_state.sb_plano
                            st.query_params["_n"] = _nome_url
                            # Divide token em partes para query_params
                            st.query_params["_t1"] = _tk_full[:200]
                            st.query_params["_t2"] = _tk_full[200:400]
                            st.query_params["_t3"] = _tk_full[400:]
                        except Exception:
                            pass
                        st.success(f"Ã¢Åâ¦ Bem-vindo, {st.session_state.usuario_atual}!")
                        st.rerun()
                    else:
                        st.error(f"Ã¢ÂÅ {res['erro']}")

        with aba_cadastro:
            with st.form("form_cadastro_sb", clear_on_submit=True):
                nome_c  = st.text_input("Nome completo", key="sb_nome_cad")
                email_c = st.text_input("E-mail", key="sb_email_cad")
                senha_c = st.text_input("Senha (mÃÂ­n. 6 caracteres)", type="password", key="sb_senha_cad")
                conf_c  = st.text_input("Confirmar senha", type="password", key="sb_conf_cad")
                btn_c   = st.form_submit_button("Criar Conta", use_container_width=True)
            if btn_c:
                if not nome_c or not email_c or not senha_c:
                    st.error("Preencha todos os campos.")
                elif len(senha_c) < 6:
                    st.error("Senha deve ter pelo menos 6 caracteres.")
                elif senha_c != conf_c:
                    st.error("Senhas nÃÂ£o conferem.")
                else:
                    with st.spinner("Criando conta..."):
                        res = sb_signup(_SB_URL, _SB_KEY, email_c.strip(), senha_c, nome_c.strip())
                    if res.get("id") or res.get("user"):
                        st.success("Ã¢Åâ¦ Conta criada! Verifique seu e-mail e faÃÂ§a login.")
                    else:
                        st.error(f"Ã¢ÂÅ {res.get('msg', res.get('error_description', 'Erro ao criar conta'))}")

        with aba_recuperar:
            st.markdown("#### Ã°Å¸ââ Recuperar Senha")

            if not st.session_state.get("_recup_email"):
                with st.form("form_recup_sb", clear_on_submit=True):
                    email_r = st.text_input("E-mail cadastrado", key="sb_email_recup")
                    btn_r   = st.form_submit_button("Ã°Å¸âÂ¨ Enviar cÃÂ³digo por e-mail", use_container_width=True)
                if btn_r:
                    if not email_r:
                        st.error("Digite seu e-mail.")
                    else:
                        try:
                            import requests as _req
                            # Envia OTP numÃÂ©rico de 6 dÃÂ­gitos
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
                                st.success(f"Ã¢Åâ¦ CÃÂ³digo enviado para **{email_r.strip()}**!")
                                st.info("Ã°Å¸âÂ§ Verifique seu e-mail e copie o cÃÂ³digo de 6 dÃÂ­gitos.")
                                st.rerun()
                            else:
                                st.error("Ã¢ÂÅ E-mail nÃÂ£o encontrado.")
                        except Exception as e:
                            st.error(f"Ã¢ÂÅ Erro: {e}")
            else:
                _email_recup = st.session_state["_recup_email"]
                st.info(f"Ã°Å¸âÂ§ CÃÂ³digo enviado para **{_email_recup}**")
                st.warning("Ã¢Å¡Â Ã¯Â¸Â O e-mail enviado tem um cÃÂ³digo de 6 dÃÂ­gitos. **NÃÂ£o clique no link** Ã¢â¬â copie apenas o cÃÂ³digo numÃÂ©rico.")

                with st.form("form_otp_sb", clear_on_submit=False):
                    otp_code   = st.text_input("CÃÂ³digo de 6 dÃÂ­gitos do e-mail", key="sb_otp_code",
                                               placeholder="123456", max_chars=6)
                    nova_senha = st.text_input("Nova senha (mÃÂ­n. 6 caracteres)", type="password", key="sb_nova_senha")
                    conf_nova  = st.text_input("Confirmar nova senha", type="password", key="sb_conf_nova")
                    btn_otp    = st.form_submit_button("Ã°Å¸âÂ Redefinir Senha", use_container_width=True)

                if btn_otp:
                    if not otp_code or len(otp_code.strip()) < 6:
                        st.error("Digite o cÃÂ³digo de 6 dÃÂ­gitos.")
                    elif len(nova_senha) < 6:
                        st.error("Senha deve ter pelo menos 6 caracteres.")
                    elif nova_senha != conf_nova:
                        st.error("Senhas nÃÂ£o conferem.")
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
                                # Tenta tambÃÂ©m com type "email"
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
                                    st.success("Ã¢Åâ¦ Senha redefinida! FaÃÂ§a login com a nova senha.")
                                    st.balloons()
                                else:
                                    st.error(f"Ã¢ÂÅ Erro ao atualizar senha: {r2.text[:80]}")
                            else:
                                st.error(f"Ã¢ÂÅ CÃÂ³digo invÃÂ¡lido ou expirado. Tente solicitar um novo cÃÂ³digo.")
                        except Exception as e:
                            st.error(f"Ã¢ÂÅ Erro: {e}")

                if st.button("Ã¢â Â©Ã¯Â¸Â Solicitar novo cÃÂ³digo", key="btn_recup_voltar"):
                    st.session_state.pop("_recup_email", None)
                    st.rerun()

        st.markdown("---")
        st.caption("Ã°Å¸ââ Dados protegidos por Supabase | Cada usuÃÂ¡rio tem seus prÃÂ³prios dados")

    else:
        # Ã¢ââ¬Ã¢ââ¬ LOGIN LOCAL (fallback sem Supabase) Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        aba_login, aba_cadastro, aba_recuperar = st.tabs(["Ã°Å¸ââ Entrar","Ã¢Å¾â¢ Criar Conta","Ã°Å¸ââ Recuperar Senha"])

        with aba_login:
            with st.form("form_login", clear_on_submit=False):
                usuario = st.text_input("UsuÃÂ¡rio", key="login_usuario")
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
                    st.error("UsuÃÂ¡rio ou senha incorretos.")

        with aba_cadastro:
            novo_nome       = st.text_input("Nome completo",       key="cad_nome")
            novo_email      = st.text_input("Email de recuperaÃÂ§ÃÂ£o", key="cad_email")
            novo_usuario    = st.text_input("Criar usuÃÂ¡rio",        key="cad_usuario")
            nova_senha      = st.text_input("Criar senha",          type="password", key="cad_senha")
            confirmar_senha = st.text_input("Confirmar senha",      type="password", key="cad_confirmar")
            if st.button("Cadastrar", use_container_width=True, key="btn_cadastrar"):
                if not novo_nome.strip():
                    st.error("Digite seu nome.")
                elif not novo_email.strip() or "@" not in novo_email:
                    st.error("Digite um email vÃÂ¡lido.")
                elif not novo_usuario.strip():
                    st.error("Digite um usuÃÂ¡rio.")
                elif len(nova_senha) < 6:
                    st.error("Senha deve ter pelo menos 6 caracteres.")
                elif nova_senha != confirmar_senha:
                    st.error("As senhas nÃÂ£o conferem.")
                elif novo_usuario in st.session_state.usuarios:
                    st.error("Esse usuÃÂ¡rio jÃÂ¡ existe.")
                else:
                    st.session_state.usuarios[novo_usuario] = {
                        "nome":  novo_nome,
                        "email": novo_email,
                        "senha": hash_senha(nova_senha)
                    }
                    salvar_usuarios(st.session_state.usuarios)
                    st.success("Ã¢Åâ¦ Conta criada! FaÃÂ§a login na aba Entrar.")

        with aba_recuperar:
            st.info("Sistema local Ã¢â¬â recuperaÃÂ§ÃÂ£o de senha nÃÂ£o disponÃÂ­vel sem e-mail configurado.")

        st.caption("Ã¢Å¡Â Ã¯Â¸Â Modo local Ã¢â¬â dados compartilhados. Configure Supabase para multi-usuÃÂ¡rio.")


if not st.session_state.logado:
    # Verifica se havia uma sessÃÂ£o anterior (usuÃÂ¡rio recarregou a pÃÂ¡gina)
    if st.session_state.get("usuario_atual"):
        st.warning("Ã¢ÂÂ³ Sua sessÃÂ£o expirou. FaÃÂ§a login novamente Ã¢â¬â seus dados estÃÂ£o salvos no servidor.")
    tela_login()
    st.stop()

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# SPLASH SCREEN (apenas 1x por sessÃÂ£o)
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
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
            <p style="color:#93c5fd;font-size:1rem;">Sistema de gestÃÂ£o agrÃÂ­cola inteligente</p>
        </div>""", unsafe_allow_html=True)
        _tx.sleep(1.2)
    _ph.empty()
    st.session_state.app_loaded = True

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# BARRA LATERAL
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
st.sidebar.markdown(
    f'<div style="background:#1a4a73;color:#ffffff;padding:10px 14px;border-radius:8px;'
    f'font-weight:700;font-size:14px;margin-bottom:8px;">Ã°Å¸âÂ¤ {st.session_state.usuario_atual}</div>',
    unsafe_allow_html=True
)

# Badge do plano no sidebar
_plano_atual = st.session_state.get("sb_plano", "free")
PLANOS = {
    "free": {
        "nome":    "Ã°Å¸â â Free",
        "preco":   0,
        "areas":   2,
        "estoque": 20,
        "cor":     "#78350f",
        "borda":   "#f59e0b",
        "recursos": [
            "2 ÃÂ¡reas cadastradas",
            "20 itens de estoque",
            "AnÃÂ¡lise de solo bÃÂ¡sica",
            "CalendÃÂ¡rio agrÃÂ­cola",
            "PreÃÂ§os offline",
        ],
        "bloqueados": [
            "RelatÃÂ³rio PDF",
            "ImportaÃÂ§ÃÂ£o NF-e XML",
            "PreÃÂ§os CEPEA tempo real",
            "Mapa de Colheita IA",
            "IR Rural",
            "Safrinha",
        ]
    },
    "pro": {
        "nome":    "Ã°Å¸âÅ½ Pro",
        "preco":   49.90,
        "areas":   10,
        "estoque": 100,
        "cor":     "#1e3a5f",
        "borda":   "#3b82f6",
        "recursos": [
            "10 ÃÂ¡reas cadastradas",
            "100 itens de estoque",
            "DiagnÃÂ³stico completo EMBRAPA",
            "RelatÃÂ³rio PDF premium",
            "ImportaÃÂ§ÃÂ£o NF-e XML",
            "PreÃÂ§os CEPEA tempo real",
            "Safrinha",
            "IR Rural automatizado",
            "ReceituÃÂ¡rio AgronÃÂ´mico",
            "Suporte via WhatsApp",
        ],
        "bloqueados": [
            "ÃÂreas ilimitadas",
            "Estoque ilimitado",
            "Mapa de Colheita IA avanÃÂ§ado",
            "API de integraÃÂ§ÃÂ£o",
            "Multi-usuÃÂ¡rio",
        ]
    },
    "premium": {
        "nome":    "Ã°Å¸Å¡â¬ Premium",
        "preco":   119.90,
        "areas":   -1,   # ilimitado
        "estoque": -1,   # ilimitado
        "cor":     "#14532d",
        "borda":   "#22c55e",
        "recursos": [
            "ÃÂreas ILIMITADAS",
            "Estoque ILIMITADO",
            "Tudo do Plano Pro",
            "Mapa de Colheita IA avanÃÂ§ado",
            "RelatÃÂ³rios agrupados",
            "API de integraÃÂ§ÃÂ£o",
            "Suporte prioritÃÂ¡rio 24h",
            "Treinamento online",
            "White-label disponÃÂ­vel",
        ],
        "bloqueados": []
    },
}

WPP_NUMERO  = "5549998159224"  # Ã¢â Â coloque seu WhatsApp aqui
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

# Status do ÃÂºltimo salvamento (debug)
if st.session_state.get("_ultimo_save"):
    _cor_s = "#14532d" if "Ã¢Åâ¦" in st.session_state["_ultimo_save"] else "#7f1d1d"
    st.sidebar.markdown(
        f"<div style='background:{_cor_s};color:#fff;padding:3px 8px;"
        f"border-radius:4px;font-size:10px;margin-top:2px;'>"
        f"{st.session_state['_ultimo_save']}</div>",
        unsafe_allow_html=True
    )


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# SESSION STATE Ã¢â¬â DADOS
# Carrega do Supabase se tem token, senÃÂ£o arquivo local
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
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
        pass  # falha silenciada Ã¢â¬â usa arquivo local

dados_carregados = {}

# Se autologin funcionou, dados jÃÂ¡ estÃÂ£o no session_state Ã¢â¬â nÃÂ£o sobrescreve
# Se nÃÂ£o, tenta Supabase com token existente, senÃÂ£o arquivo local
if not st.session_state.get("areas"):
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

if "dados" not in st.session_state:
    _d = dados_carregados.get("dados", {})
    st.session_state.dados   = _d if isinstance(_d, dict) else {}
if "areas" not in st.session_state or (not st.session_state.areas and dados_carregados.get("areas")):
    st.session_state.areas   = dados_carregados.get("areas", [])
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

# Ã¢ââ¬Ã¢ââ¬ Mapa de Colheita IA Ã¢â¬â inicializaÃÂ§ÃÂ£o global Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
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
if "fluxo_caixa" not in st.session_state or (not st.session_state.get("fluxo_caixa") and dados_carregados.get("fluxo_caixa")):
    st.session_state.fluxo_caixa = dados_carregados.get("fluxo_caixa", [])
if "corretivos_aplicados" not in st.session_state or (not st.session_state.get("corretivos_aplicados") and dados_carregados.get("corretivos_aplicados")):
    st.session_state.corretivos_aplicados = dados_carregados.get("corretivos_aplicados", [])
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

# Ã¢ââ¬Ã¢ââ¬ GPS session_states Ã¢â¬â inicializaÃÂ§ÃÂ£o segura Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if "_gps_lat"       not in st.session_state: st.session_state._gps_lat       = None
if "_gps_lon"       not in st.session_state: st.session_state._gps_lon       = None
if "_gps_mf_lat"    not in st.session_state: st.session_state._gps_mf_lat    = None
if "_gps_mf_lon"    not in st.session_state: st.session_state._gps_mf_lon    = None
if "_gps_clima_lat" not in st.session_state: st.session_state._gps_clima_lat = None
if "_gps_clima_lon" not in st.session_state: st.session_state._gps_clima_lon = None
if "filtro_out"     not in st.session_state: st.session_state.filtro_out     = []

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬

# BANCO DE PRODUTOS AGRÃÂCOLAS Ã¢â¬â Autocomplete
# Fontes: BASF, Syngenta, Bayer, UPL, MAPA/AGROFIT
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
CATALOGO_PRODUTOS = [
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"2,4-D Amina 806","fab":"Outros","cat":"Herbicida","ia":"2,4-D Amina"},
    {"nome":"2,4-D Ãâ°ster 670","fab":"Outros","cat":"Herbicida","ia":"2,4-D Ãâ°ster"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Abacus HC","fab":"BASF","cat":"Fungicida","ia":"Epoxiconazol + Piraclostrobina"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Abamectina 18 EC","fab":"Outros","cat":"Inseticida","ia":"Abamectina"},
    {"nome":"Abamectina 36 EC","fab":"Outros","cat":"Acaricida","ia":"Abamectina"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Abamex 18 EC","fab":"ADAMA","cat":"Inseticida","ia":"Abamectina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Acabus","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Acaristop 500 SC","fab":"Ouro Fino","cat":"Acaricida","ia":"Clofentezina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Accent 750 WG","fab":"BASF","cat":"Herbicida","ia":"Nicossulfurom"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Accent Gold","fab":"Bayer","cat":"Herbicida","ia":"Nicossulfurom + Rimsulfurom"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Acefato 750 WP","fab":"ADAMA","cat":"Inseticida","ia":"Acefato"},
    {"nome":"Acetamiprido 200 SP","fab":"ADAMA","cat":"Inseticida","ia":"Acetamiprido"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Acimanto SC","fab":"Ihara","cat":"Inseticida","ia":"Acefato"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Acramite 50 WS","fab":"Outros","cat":"Acaricida","ia":"Bifenazate"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Acrobat MZ","fab":"BASF","cat":"Fungicida","ia":"Dimetomorfe + Mancozebe"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Actara 250 WG","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam"},
    {"nome":"Actellic 500 EC","fab":"Syngenta","cat":"Inseticida","ia":"PirimifÃÂ³s-MetÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Actigen","fab":"Ouro Fino","cat":"Fungicida BiolÃÂ³gico","ia":"Bacillus amyloliquefaciens"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Actyon 100 EC","fab":"Ihara","cat":"Inseticida","ia":"Bifentrina"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Adengo","fab":"Bayer","cat":"Herbicida","ia":"Isoxaflutol + Tiencarbazona"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Afalon 450 SC","fab":"ADAMA","cat":"Herbicida","ia":"Linurom"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Agree WP","fab":"Outros","cat":"Inseticida BiolÃÂ³gico","ia":"Bacillus thuringiensis"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Alade","fab":"Syngenta","cat":"Fungicida","ia":"Solatenol + Ciproconazol + Difenoconazol"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ally","fab":"ADAMA","cat":"Herbicida","ia":"Metsulfurom-MetÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Alto 100 SL","fab":"Ihara","cat":"Fungicida","ia":"Ciproconazol"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Amistar 500 WG","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina"},
    {"nome":"Amistar Top","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Difenoconazol"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Amplexus","fab":"BASF","cat":"Herbicida","ia":"Flumioxazina + Lactofen"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ampligo 150 ZC","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole + Lambda-Cialotrina"},
    {"nome":"Ampligo Pro","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole + Clorfenapir"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Amplo","fab":"BASF","cat":"Herbicida","ia":"Imazapique + Imazapir"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Apollo 500 SC","fab":"Outros","cat":"Acaricida","ia":"Clofentezina"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Aproach 500 SC","fab":"Corteva","cat":"Fungicida","ia":"Picoxistrobina"},
    {"nome":"Aproach Prima","fab":"Corteva","cat":"Fungicida","ia":"Picoxistrobina + Ciproconazol"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Artea 330 EC","fab":"Ihara","cat":"Fungicida","ia":"Propiconazol + Ciproconazol"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Arylex Active","fab":"Corteva","cat":"Herbicida","ia":"Halauxifem-metÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ascope","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Asgard BR","fab":"Corteva","cat":"Herbicida","ia":"Sulfentrazona + Clomazona"},
    # Ã¢ââ¬Ã¢ââ¬ MOSAIC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Aspire","fab":"Mosaic","cat":"Fertilizante","ia":"KCl + B granulado"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Assist","fab":"Outros","cat":"Adjuvante","ia":"Ãâleo Mineral"},
    # Ã¢ââ¬Ã¢ââ¬ MOSAIC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Athos","fab":"Mosaic","cat":"Fertilizante","ia":"Sulfato de amÃÂ´nio premium"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ativo TS","fab":"BASF","cat":"Tratamento de Sementes","ia":"Fludioxonil + Metalaxil-M + Tiametoxam"},
    {"nome":"Ativum","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Fluxapiroxade"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Atrazina 500 SC","fab":"Outros","cat":"Herbicida","ia":"Atrazina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Aura 200","fab":"BASF","cat":"Herbicida","ia":"Quizalofope-P-etÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Aureo","fab":"Bayer","cat":"Adjuvante","ia":"Ãâleo de Soja"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Aurora 400 EC","fab":"ADAMA","cat":"Herbicida","ia":"Carfentrazona-etÃÂ­lica"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Authority 700 WDG","fab":"FMC","cat":"Herbicida","ia":"Sulfentrazona"},
    {"nome":"Authority Assist","fab":"FMC","cat":"Herbicida","ia":"Sulfentrazona + Imazaquim"},
    {"nome":"Authority First","fab":"FMC","cat":"Herbicida","ia":"Sulfentrazona + Cloransulam"},
    {"nome":"Authority MTZ","fab":"FMC","cat":"Herbicida","ia":"Sulfentrazona + Metribuzim"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Avaunt 150 SC","fab":"Corteva","cat":"Inseticida","ia":"Indoxacarbe"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Avicta 500 FS","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Abamectina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Axalion","fab":"BASF","cat":"Inseticida","ia":"Afidopiropeno"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Axial","fab":"Syngenta","cat":"Herbicida","ia":"Pinoxaden"},
    {"nome":"Axial One","fab":"Syngenta","cat":"Herbicida","ia":"Pinoxaden + Clodinafope-propargil"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Azimut 250 SC","fab":"ADAMA","cat":"Fungicida","ia":"Azoxistrobina"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Azimut OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Azoxistrobina 250 SC","fab":"Outros","cat":"Fungicida","ia":"Azoxistrobina"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Azoxy OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Propiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Banvel","fab":"Bayer","cat":"Herbicida","ia":"Dicamba"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Basagran 480","fab":"BASF","cat":"Herbicida","ia":"Bentazona"},
    {"nome":"Basagran 600","fab":"BASF","cat":"Herbicida","ia":"Bentazona"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Bayfidan 250 EC","fab":"Bayer","cat":"Fungicida","ia":"Triadimenol"},
    {"nome":"Bayfolan Boro","fab":"Bayer","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"B + aminoÃÂ¡cidos"},
    {"nome":"Bayfolan Cobre","fab":"Bayer","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"Cu + aminoÃÂ¡cidos"},
    {"nome":"Bayfolan Forte","fab":"Bayer","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"NPK + micronutrientes + aminoÃÂ¡cidos"},
    {"nome":"Bayfolan NK","fab":"Bayer","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"N + K + aminoÃÂ¡cidos"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Baytan 150 FS","fab":"BASF","cat":"Tratamento de Sementes","ia":"Triadimenol"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Belt 480 SC","fab":"Bayer","cat":"Inseticida","ia":"Flubendiamida"},
    {"nome":"Belt Expert","fab":"Bayer","cat":"Inseticida","ia":"Flubendiamida + Spirotetramat"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Belyan","fab":"BASF","cat":"Fungicida","ia":"Mefentrifluconazol + Piraclostrobina + Fluxapiroxade"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Bendazol 500 SC","fab":"UPL","cat":"Fungicida","ia":"Carbendazim"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Benevia OD","fab":"Corteva","cat":"Inseticida","ia":"Ciantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Bentazona 600 SL","fab":"Outros","cat":"Herbicida","ia":"Bentazona"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Benza 500 SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Carbendazim"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Bifentrina 100 EC","fab":"Outros","cat":"Inseticida","ia":"Bifentrina"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Biozyme","fab":"UPL","cat":"Bioestimulante","ia":"AminoÃÂ¡cidos + Extrato de algas"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Blavity","fab":"BASF","cat":"Fungicida","ia":"Fluxapiroxade + Protioconazol"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Bold 750 WG","fab":"Bayer","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Boral 500 SC","fab":"Corteva","cat":"Herbicida","ia":"Sulfentrazona"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Boro Max 10%","fab":"Outros","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"Boro"},
    {"nome":"Bovemax SC","fab":"Outros","cat":"Inseticida BiolÃÂ³gico","ia":"Beauveria bassiana"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Boveril WP","fab":"Ihara","cat":"Inseticida BiolÃÂ³gico","ia":"Beauveria bassiana"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Bravonil 500 SC","fab":"Syngenta","cat":"Fungicida","ia":"Clorotalonil"},
    {"nome":"Bravonil Top","fab":"Syngenta","cat":"Fungicida","ia":"Clorotalonil + Ciproconazol"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Bravonil Ultrex","fab":"ADAMA","cat":"Fungicida","ia":"Clorotalonil"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Break Thru S 240","fab":"Outros","cat":"Adjuvante","ia":"Silicone"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Brigade 100 EC","fab":"FMC","cat":"Inseticida","ia":"Bifentrina"},
    {"nome":"Brigade 400 SC","fab":"FMC","cat":"Inseticida","ia":"Bifentrina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Bright","fab":"BASF","cat":"Inseticida","ia":"Ciantraniliprole + Tiametoxam"},
    {"nome":"Brio","fab":"BASF","cat":"Fungicida","ia":"Trifloxistrobina + Propiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Bulldock 125 SC","fab":"Bayer","cat":"Inseticida","ia":"Beta-Ciflutrina"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"BÃÂ³rax","fab":"Outros","cat":"Fertilizante","ia":"B 11%"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cabrio Top","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Metiram"},
    {"nome":"Caipora","fab":"BASF","cat":"Tratamento de Sementes","ia":"Piraclostrobina + Tiofanato + Fipronil"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Calaris Milho","fab":"Syngenta","cat":"Herbicida","ia":"Tembotriona + Atrazina"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"CalcÃÂ¡rio CalcÃÂ­tico","fab":"Outros","cat":"Fertilizante","ia":"CaCO3"},
    {"nome":"CalcÃÂ¡rio DolomÃÂ­tico","fab":"Outros","cat":"Fertilizante","ia":"CaCO3 + MgCO3"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Calipen SC","fab":"Syngenta","cat":"Herbicida","ia":"Cloransulam-metÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Callisto","fab":"Corteva","cat":"Herbicida","ia":"Mesotriona"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cantus","fab":"BASF","cat":"Fungicida","ia":"Boscalida"},
    {"nome":"Caramba 90","fab":"BASF","cat":"Fungicida","ia":"Metconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Carbendazim 500 SC","fab":"Outros","cat":"Fungicida","ia":"Carbendazim"},
    {"nome":"Carbofuran 350 SC","fab":"Outros","cat":"Nematicida","ia":"Carbofurano"},
    {"nome":"Carrier 170 EC","fab":"Outros","cat":"Adjuvante","ia":"Ãâleo Mineral"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Celeiro","fab":"Bayer","cat":"Fungicida","ia":"Tebuconazol + Trifloxistrobina"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cercobin 700 WP","fab":"ADAMA","cat":"Fungicida","ia":"Tiofanato MetÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cerconil WP","fab":"UPL","cat":"Fungicida","ia":"Clorotalonil + Tiofanato"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cereus 72 SC","fab":"Outros","cat":"Regulador de Crescimento","ia":"Trinexapaque-etÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Certano","fab":"Syngenta","cat":"Inseticida BiolÃÂ³gico","ia":"Beauveria bassiana"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Certero 480 SC","fab":"Bayer","cat":"Inseticida","ia":"Triflumurom"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cipermetrina 250 EC","fab":"ADAMA","cat":"Inseticida","ia":"Cipermetrina"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cipro 250 SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Ciproconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Citromax Cal-Boro","fab":"Outros","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"CÃÂ¡lcio + Boro"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Clariva Complete B","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Pasteuria nishizawae + Tiametoxam"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Clethodim 240 EC","fab":"ADAMA","cat":"Herbicida","ia":"Cletodim"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cletodim 240 EC","fab":"Outros","cat":"Herbicida","ia":"Cletodim"},
    {"nome":"Clodinafope 240 EC","fab":"Outros","cat":"Herbicida","ia":"Clodinafope-propargil"},
    {"nome":"Clomazona 500 EC","fab":"Outros","cat":"Herbicida","ia":"Clomazona"},
    {"nome":"Clorantraniliprole 200 SC","fab":"Outros","cat":"Inseticida","ia":"Clorantraniliprole"},
    {"nome":"Cloreto de PotÃÂ¡ssio","fab":"Outros","cat":"Fertilizante","ia":"KCl 00-00-60"},
    # Ã¢ââ¬Ã¢ââ¬ MOSAIC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cloreto de PotÃÂ¡ssio Mosaic","fab":"Mosaic","cat":"Fertilizante","ia":"KCl 00-00-60"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Clorotalonil 720 SC","fab":"Outros","cat":"Fungicida","ia":"Clorotalonil"},
    {"nome":"ClorpirifÃÂ³s 480 EC","fab":"Outros","cat":"Inseticida","ia":"ClorpirifÃÂ³s"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Closer SC","fab":"Corteva","cat":"Inseticida","ia":"Sulfoxaflor"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Clout 100 CS","fab":"Ihara","cat":"Inseticida","ia":"Lambda-Cialotrina"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cobra","fab":"Outros","cat":"Herbicida","ia":"Lactofen"},
    {"nome":"Cobre Foliar 5%","fab":"Outros","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"Cobre"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cobre Sandoz","fab":"BASF","cat":"Fungicida","ia":"Oxicloreto de Cobre"},
    {"nome":"Collis","fab":"BASF","cat":"Fungicida","ia":"Boscalida + Cresoxim-metÃÂ­lico"},
    {"nome":"Comet 200 EC","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Confidor 700 WG","fab":"Bayer","cat":"Inseticida","ia":"Imidaclopride"},
    {"nome":"Confidor Oil","fab":"Bayer","cat":"Inseticida","ia":"Imidaclopride + Ãâleo mineral"},
    {"nome":"Connect","fab":"Bayer","cat":"Inseticida","ia":"Imidaclopride + Beta-Ciflutrina"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Constel","fab":"UPL","cat":"Inseticida","ia":"Clorantraniliprole + Metoxifenozida"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Convintro Duo","fab":"Bayer","cat":"Herbicida","ia":"Halauxifem-metÃÂ­lico + Fluroxipir"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Coragen 200 SC","fab":"Corteva","cat":"Inseticida","ia":"Clorantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Coragen FMC","fab":"FMC","cat":"Inseticida","ia":"Clorantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ TIMAC AGRO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Corona","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"N + B + Mo + aminoÃÂ¡cidos"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cossack OD","fab":"UPL","cat":"Herbicida","ia":"Mesossulfurom + Iodossulfurom"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cripton Xpro","fab":"Bayer","cat":"Fungicida","ia":"Bixafem + Protioconazol + Trifloxistrobina"},
    {"nome":"Cropstar 600 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Imidaclopride + Tiodicarbe"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Crosstin","fab":"UPL","cat":"Herbicida","ia":"Hexazinona + Diurom"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cruiser 350 FS","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Tiametoxam"},
    {"nome":"Cruiser Opti","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Tiametoxam + Fludioxonil + Mefenoxam"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cuprozeb","fab":"ADAMA","cat":"Fungicida","ia":"Cobre + Mancozebe"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Curbix","fab":"Bayer","cat":"Inseticida","ia":"Flupyrimin"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Curyom 550 EC","fab":"Syngenta","cat":"Inseticida","ia":"ProfenofÃÂ³s + Cipermetrina"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cyazypyr 100 OD","fab":"Corteva","cat":"Inseticida","ia":"Ciantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cyazypyr FMC","fab":"FMC","cat":"Inseticida","ia":"Ciantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cypress","fab":"Syngenta","cat":"Fungicida","ia":"Difenoconazol + Propiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Cypress Ihara","fab":"Ihara","cat":"Fungicida","ia":"Difenoconazol + Propiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"CÃÂ¡lcio King 12%","fab":"Outros","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"CÃÂ¡lcio"},
    {"nome":"DAP 18-46-00","fab":"Outros","cat":"Fertilizante","ia":"DiamÃÂ´nio fosfato"},
    # Ã¢ââ¬Ã¢ââ¬ MOSAIC Ã¢ââ¬Ã¢ââ¬
    {"nome":"DAP Mosaic","fab":"Mosaic","cat":"Fertilizante","ia":"DiamÃÂ´nio fosfato 18-46-00"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Dash HC","fab":"Outros","cat":"Adjuvante","ia":"Ãâ°ster MetÃÂ­lico de Ãâleos"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Debussy SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Propiconazol + Difenoconazol"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Decis 25 EC","fab":"Bayer","cat":"Inseticida","ia":"Deltametrina"},
    {"nome":"Decis Protech","fab":"Bayer","cat":"Inseticida","ia":"Deltametrina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Delan","fab":"BASF","cat":"Fungicida","ia":"Ditianonom"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Deltametrina 25 EC","fab":"ADAMA","cat":"Inseticida","ia":"Deltametrina"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Dermacor X-100","fab":"Corteva","cat":"Tratamento de Sementes","ia":"Clorantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Derosal Plus TS","fab":"BASF","cat":"Tratamento de Sementes","ia":"Carbendazim + Tiram"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Diamond 50 EC","fab":"FMC","cat":"Inseticida","ia":"Novalurom"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Diclosulam 840 WG","fab":"ADAMA","cat":"Herbicida","ia":"Diclosulam"},
    {"nome":"Difenoconazol 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Difenoconazol"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Dimilin 250 WP","fab":"Corteva","cat":"Inseticida","ia":"Diflubenzurom"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Dipel WP","fab":"Outros","cat":"Inseticida BiolÃÂ³gico","ia":"Bacillus thuringiensis"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"DMA 806 BR","fab":"Corteva","cat":"Herbicida","ia":"2,4-D Amina"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Domark 100 EC","fab":"UPL","cat":"Fungicida","ia":"Tetraconazol"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Dual Gold 960 EC","fab":"Syngenta","cat":"Herbicida","ia":"S-Metolacloro"},
    {"nome":"Durivo","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Clorantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ecconik","fab":"UPL","cat":"Herbicida","ia":"Isoxaflutol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ecoss WP","fab":"Outros","cat":"Fungicida BiolÃÂ³gico","ia":"Bacillus subtilis"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Eddus","fab":"Syngenta","cat":"Herbicida","ia":"Flumioxazina"},
    {"nome":"Elatus","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Benzovindiflupir"},
    {"nome":"Elatus Ace","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Benzovindiflupir + Propiconazol"},
    {"nome":"Elatus Plus","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Benzovindiflupir + Difenoconazol"},
    {"nome":"Elestal Neo","fab":"Syngenta","cat":"Inseticida","ia":"Sulfoxaflor"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Emamectina 50 WG","fab":"Outros","cat":"Inseticida","ia":"Benzoato de Emamectina"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Eminent 125 EW","fab":"ADAMA","cat":"Fungicida","ia":"Tetraconazol"},
    {"nome":"Eminent Star","fab":"ADAMA","cat":"Fungicida","ia":"Tetraconazol + Fludioxonil"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Engeo Pleno S","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Lambda-Cialotrina"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Enlist Duo","fab":"Corteva","cat":"Herbicida","ia":"2,4-D + Glifosato"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Envidor 240 SC","fab":"Outros","cat":"Acaricida","ia":"Espirodiclofeno"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Epivio Sky","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Fluopyram"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Epoxiconazol 75 SC","fab":"Outros","cat":"Fungicida","ia":"Epoxiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"EsfÃÂ©rica Duo","fab":"ADAMA","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Espinosade 480 SC","fab":"Outros","cat":"Inseticida","ia":"Espinosade"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Estoril OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ethrel 720 SL","fab":"Outros","cat":"Regulador de Crescimento","ia":"Etefom"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Evidence 200 EC","fab":"Bayer","cat":"Fungicida","ia":"Iprodiona"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Evolution","fab":"UPL","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Exalt 600 SC","fab":"FMC","cat":"Inseticida","ia":"Espinetoram"},
    # Ã¢ââ¬Ã¢ââ¬ MOSAIC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Excellen","fab":"Mosaic","cat":"Fertilizante","ia":"N com inibidor de nitrificaÃÂ§ÃÂ£o"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Exirel 100 SE","fab":"Corteva","cat":"Inseticida","ia":"Ciantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Extravon","fab":"Outros","cat":"Adjuvante","ia":"Alquil-polioxietileno"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fastac 100 CE","fab":"BASF","cat":"Inseticida","ia":"Alfa-Cipermetrina"},
    {"nome":"Fastac 50 EC","fab":"BASF","cat":"Inseticida","ia":"Alfa-Cipermetrina"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fastmite","fab":"UPL","cat":"Inseticida","ia":"Abamectina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fegatex","fab":"BASF","cat":"Inseticida","ia":"Acefato"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fernok","fab":"UPL","cat":"Herbicida","ia":"Fenoxaprop + Mefenpir"},
    {"nome":"Feroce","fab":"UPL","cat":"Inseticida","ia":"Lambda-Cialotrina + Tiametoxam"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ferrari","fab":"Ouro Fino","cat":"Fungicida","ia":"Piraclostrobina + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ferro Quelatado 6%","fab":"Outros","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"Ferro EDTA"},
    # Ã¢ââ¬Ã¢ââ¬ TIMAC AGRO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fertiactyl Cana","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"N + K + S"},
    {"nome":"Fertiactyl GramÃÂ­neas","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"N + S + Zn"},
    {"nome":"Fertiactyl GZ","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"N + P + K + aminoÃÂ¡cidos + algas"},
    {"nome":"Fertiactyl Kalibor","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"K + B"},
    {"nome":"Fertiactyl Leguminosas","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"N + P + K + Mo + Co"},
    {"nome":"Fertiactyl Leguminosas NG","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"N + P + K + Mo + Co + aminoÃÂ¡cidos"},
    {"nome":"Fertileader Alpha","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"Seactiv + N + Zn"},
    {"nome":"Fertileader Cana","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"Seactiv + N + K"},
    {"nome":"Fertileader Grena","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"Seactiv + K + Ca + B"},
    {"nome":"Fertileader Maiz","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"Seactiv + N + P + Zn"},
    {"nome":"Fertileader QualitÃÂ©","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"Seactiv + P + K + S"},
    {"nome":"Fertileader Vital","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"Seactiv + NPK"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fetrilon Combi","fab":"Outros","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"Multi-micronutrientes"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Finale","fab":"BASF","cat":"Herbicida","ia":"Glufosinato de AmÃÂ´nio"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fipronil 800 WG","fab":"Outros","cat":"Inseticida","ia":"Fipronil"},
    {"nome":"Floramite 240 SC","fab":"Outros","cat":"Acaricida","ia":"Bifenazate"},
    {"nome":"Fluazifope 250 EC","fab":"Outros","cat":"Herbicida","ia":"Fluazifope-P-butÃÂ­lico"},
    {"nome":"Flumioxazina 500 SC","fab":"Outros","cat":"Herbicida","ia":"Flumioxazina"},
    {"nome":"Fluxapiroxade 500 SC","fab":"Outros","cat":"Fungicida","ia":"Fluxapiroxade"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Folicur 200 EC","fab":"Bayer","cat":"Fungicida","ia":"Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Foltron Plus","fab":"UPL","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"NitrogÃÂªnio + Boro + MolibdÃÂªnio"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fontelis 200 SC","fab":"Corteva","cat":"Fungicida","ia":"Penthiopirad"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fortenza 600 FS","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Afidopiropeno"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fortenza Duo","fab":"BASF","cat":"Tratamento de Sementes","ia":"Afidopiropeno + Sedaxane"},
    {"nome":"Forum","fab":"BASF","cat":"Fungicida","ia":"Dimetomorfe"},
    {"nome":"Forum Plus","fab":"BASF","cat":"Fungicida","ia":"Dimetomorfe + Folpete"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fosfato Reativo","fab":"Outros","cat":"Fertilizante","ia":"Fosfato natural reativo"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fox OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fox Ultra","fab":"Bayer","cat":"Fungicida","ia":"Protioconazol + Impirfluxam + Trifloxistrobina"},
    {"nome":"Fox Xpro","fab":"Bayer","cat":"Fungicida","ia":"Bixafem + Tebuconazol + Trifloxistrobina"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fritas FTE BR-12","fab":"Outros","cat":"Fertilizante","ia":"Multi-micronutrientes fritados"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Frondeo Cana","fab":"Syngenta","cat":"Inseticida","ia":"Plinazolina"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fury 200 EW","fab":"UPL","cat":"Inseticida","ia":"Zeta-Cipermetrina"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Fusilade 250 EW","fab":"ADAMA","cat":"Herbicida","ia":"Fluazifope-P-butÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"FusiÃÂ³n SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Ciproconazol"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Galil SC","fab":"Bayer","cat":"Fungicida","ia":"Iprodiona + Tiofanato MetÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Galvian 500 WG","fab":"UPL","cat":"Inseticida","ia":"Acefato"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Gamit 360 CS","fab":"BASF","cat":"Herbicida","ia":"Clomazona"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Gamit Star","fab":"FMC","cat":"Herbicida","ia":"Clomazona + Pendimetalina"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Gamit UPL","fab":"UPL","cat":"Herbicida","ia":"Clomazona 360 CS"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Gaucho 350 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Imidaclopride"},
    {"nome":"Gaucho 600 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Imidaclopride"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Gesagard 500 SC","fab":"Syngenta","cat":"Herbicida","ia":"Prometrina"},
    {"nome":"Gesaprim 500 SC","fab":"Syngenta","cat":"Herbicida","ia":"Atrazina"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Gesso AgrÃÂ­cola","fab":"Outros","cat":"Fertilizante","ia":"CaSO4"},
    {"nome":"Gibb 10 Plus","fab":"Outros","cat":"Regulador de Crescimento","ia":"ÃÂcido GiberÃÂ©lico"},
    {"nome":"Glifosato CS 480","fab":"Outros","cat":"Herbicida","ia":"Glifosato"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Gramoxone 200","fab":"Syngenta","cat":"Herbicida","ia":"Paraquat"},
    {"nome":"Grower","fab":"Syngenta","cat":"Herbicida","ia":"Nicossulfurom"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Halosulfurom 750 WG","fab":"Outros","cat":"Herbicida","ia":"Halosulfurom-metÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Harness 25 EC","fab":"Syngenta","cat":"Herbicida","ia":"Acetocloro"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Harpoon WP","fab":"Outros","cat":"Fungicida BiolÃÂ³gico","ia":"Trichoderma asperellum"},
    {"nome":"Hasten","fab":"Outros","cat":"Adjuvante","ia":"Ãâleo Vegetal Ãâ°ster"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Headline Amp","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Metconazol"},
    {"nome":"Headline EC","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina"},
    {"nome":"Heat","fab":"BASF","cat":"Herbicida","ia":"Saflufenacil"},
    {"nome":"Herbadox 400 EC","fab":"BASF","cat":"Herbicida","ia":"Pendimetalina"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Herbazida 480","fab":"ADAMA","cat":"Herbicida","ia":"Glifosato"},
    # Ã¢ââ¬Ã¢ââ¬ TIMAC AGRO Ã¢ââ¬Ã¢ââ¬
    {"nome":"HidroFit Arranque","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"P + Zn + aminoÃÂ¡cidos"},
    {"nome":"HidroFit K Plus","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"K + Ca + Mg"},
    {"nome":"HidroFit N-Max","fab":"Timac Agro","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"N + S"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Hokko Cupra 500 PM","fab":"Ihara","cat":"Fungicida","ia":"Oxicloreto de Cobre"},
    # Ã¢ââ¬Ã¢ââ¬ TIMAC AGRO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Humi-K","fab":"Timac Agro","cat":"Fertilizante","ia":"ÃÂcidos hÃÂºmicos + fÃÂºlvicos + K"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Hussar OD","fab":"BASF","cat":"Herbicida","ia":"Iodossulfurom-sÃÂ³dio"},
    {"nome":"Hussar Plus","fab":"BASF","cat":"Herbicida","ia":"Iodossulfurom + Mefenpir"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Iblon","fab":"Bayer","cat":"Fungicida","ia":"Isoflucipram + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Iguape 700 WG","fab":"ADAMA","cat":"Fungicida","ia":"Tiofanato MetÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Iharol EC","fab":"Outros","cat":"Adjuvante","ia":"Ãâleo Mineral"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Imafort","fab":"Ouro Fino","cat":"Fungicida","ia":"Isoflucipramo + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Imazaquim 150 SL","fab":"Outros","cat":"Herbicida","ia":"Imazaquim"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Imazetapir 100 SL","fab":"UPL","cat":"Herbicida","ia":"Imazetapir"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Imidaclopride 700 WS","fab":"ADAMA","cat":"Inseticida","ia":"Imidaclopride"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Imperious","fab":"FMC","cat":"Inseticida","ia":"Clorantraniliprole + Bifentrina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Imunit","fab":"BASF","cat":"Inseticida","ia":"Metaflumizone + Beta-Ciflutrina"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Influx","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Input","fab":"Bayer","cat":"Fungicida","ia":"Protioconazol + Espiropidiona"},
    {"nome":"Inspire","fab":"Bayer","cat":"Herbicida","ia":"Tembotriona"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Inspire Super","fab":"Corteva","cat":"Fungicida","ia":"Difenoconazol + Ciprodinil"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Instivo","fab":"Syngenta","cat":"Inseticida","ia":"Espinetoram"},
    {"nome":"Instivo AlgodÃÂ£o","fab":"Syngenta","cat":"Inseticida","ia":"Espinetoram"},
    {"nome":"Instivo Milho","fab":"Syngenta","cat":"Inseticida","ia":"Espinetoram"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Integral Pro WG","fab":"Outros","cat":"Fungicida BiolÃÂ³gico","ia":"Bacillus subtilis"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Invict","fab":"Syngenta","cat":"Fungicida","ia":"Ciproconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Iprodiona 500 SC","fab":"Outros","cat":"Fungicida","ia":"Iprodiona"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Jacle","fab":"FMC","cat":"Herbicida","ia":"Cloransulam-metÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Joiner CafÃÂ©","fab":"Syngenta","cat":"Inseticida","ia":"Sulfoxaflor + Lambda-Cialotrina"},
    {"nome":"Joiner HF","fab":"Syngenta","cat":"Inseticida","ia":"Sulfoxaflor + Lambda-Cialotrina"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Juno Flex","fab":"Bayer","cat":"Fungicida","ia":"Azoxistrobina + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"K-fol","fab":"UPL","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"PotÃÂ¡ssio"},
    # Ã¢ââ¬Ã¢ââ¬ MOSAIC Ã¢ââ¬Ã¢ââ¬
    {"nome":"K-Mag","fab":"Mosaic","cat":"Fertilizante","ia":"K 21% + Mg 10% + S 21%"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Kaiso Sorby 50 WG","fab":"Syngenta","cat":"Inseticida","ia":"Lambda-Cialotrina"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Kanet OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Mancozebe + Ciproconazol"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Karate Zeon 50 CS","fab":"Syngenta","cat":"Inseticida","ia":"Lambda-Cialotrina"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Kashmir","fab":"UPL","cat":"Herbicida","ia":"Hexazinona + Isoxaflutol + Sulfentrazona"},
    {"nome":"Kasumin 2L","fab":"UPL","cat":"Fungicida","ia":"Kasugamicina"},
    {"nome":"Kennox","fab":"UPL","cat":"Herbicida","ia":"Hexazinona + Diurom"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Keyra","fab":"BASF","cat":"Fungicida","ia":"Mefentrifluconazol + Fenpropimorfe"},
    {"nome":"Kixor BX","fab":"BASF","cat":"Herbicida","ia":"Saflufenacil"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Klorpan 480 EC","fab":"Ihara","cat":"Inseticida","ia":"ClorpirifÃÂ³s"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Kumulus DF","fab":"BASF","cat":"Fungicida","ia":"Enxofre"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Lactofen 240 EC","fab":"Outros","cat":"Herbicida","ia":"Lactofen"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Lambda-Cialotrina 250 CS","fab":"ADAMA","cat":"Inseticida","ia":"Lambda-Cialotrina"},
    {"nome":"Lanata 750 SC","fab":"ADAMA","cat":"Fungicida","ia":"Boscalida + Piraclostrobina"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Lancer Gold","fab":"Ihara","cat":"Inseticida","ia":"Acefato + Imidaclopride"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Lannate BR","fab":"Corteva","cat":"Inseticida","ia":"Metomil"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Larvin 800 WG","fab":"Bayer","cat":"Inseticida","ia":"Tiodicarbe"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Laser 360 CS","fab":"ADAMA","cat":"Herbicida","ia":"Clomazona"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Leverage 360","fab":"FMC","cat":"Inseticida","ia":"Imidaclopride + Beta-Ciflutrina"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Lexar EZ","fab":"Corteva","cat":"Herbicida","ia":"S-Metolacloro + Atrazina + Mesotriona"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Liberty 200 SL","fab":"Bayer","cat":"Herbicida","ia":"Glufosinato de AmÃÂ´nio"},
    {"nome":"Liberty 280 SL","fab":"Bayer","cat":"Herbicida","ia":"Glufosinato de AmÃÂ´nio"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Lintur 700 WG","fab":"ADAMA","cat":"Herbicida","ia":"Dicamba + Triasulfurom"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Locker","fab":"Bayer","cat":"Herbicida","ia":"Fluroxipir-meptÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Lorsban 480 BR","fab":"Corteva","cat":"Inseticida","ia":"ClorpirifÃÂ³s"},
    {"nome":"Lumax EZ","fab":"Corteva","cat":"Herbicida","ia":"S-Metolacloro + Atrazina + Mesotriona"},
    {"nome":"Lumiderm","fab":"Corteva","cat":"Tratamento de Sementes","ia":"Clorantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Luminus","fab":"UPL","cat":"Inseticida BiolÃÂ³gico","ia":"PeptÃÂ­deo Flg22-Bt"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Lumivia","fab":"Corteva","cat":"Tratamento de Sementes","ia":"Clorantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Luna Experience","fab":"Bayer","cat":"Fungicida","ia":"Fluopiram + Tebuconazol"},
    {"nome":"Luna Privilege","fab":"Bayer","cat":"Fungicida","ia":"Fluopiram"},
    {"nome":"Luna Sensation","fab":"Bayer","cat":"Fungicida","ia":"Fluopiram + Trifloxistrobina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Luximo","fab":"BASF","cat":"Herbicida","ia":"Metazacloro"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Malationa 500 CE","fab":"Outros","cat":"Inseticida","ia":"Malationa"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Malatol 500 CE","fab":"ADAMA","cat":"Inseticida","ia":"Malationa"},
    {"nome":"Mancozebe 750 WG","fab":"ADAMA","cat":"Fungicida","ia":"Mancozebe"},
    {"nome":"Mancozebe 800 WP","fab":"ADAMA","cat":"Fungicida","ia":"Mancozebe"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Manfil 750 WG","fab":"Ouro Fino","cat":"Fungicida","ia":"Mancozebe"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"ManganÃÂªs Foliar 15%","fab":"Outros","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"ManganÃÂªs"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Manzate 800 WP","fab":"Ihara","cat":"Fungicida","ia":"Mancozebe"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"MAP 11-52-00","fab":"Outros","cat":"Fertilizante","ia":"Monofosfato de amÃÂ´nio"},
    # Ã¢ââ¬Ã¢ââ¬ MOSAIC Ã¢ââ¬Ã¢ââ¬
    {"nome":"MAP Mosaic","fab":"Mosaic","cat":"Fertilizante","ia":"Monofosfato amÃÂ´nio 11-52-00"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Marshal 200 SC","fab":"ADAMA","cat":"Inseticida","ia":"Carbossulfano"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Match 50 EC","fab":"FMC","cat":"Inseticida","ia":"Lufenurom"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Maxifort","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Fluxapiroxade"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Maxim 025 FS","fab":"Outros","cat":"Tratamento de Sementes","ia":"Fludioxonil"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Maxim Advanced","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Fludioxonil + Metalaxil-M"},
    {"nome":"Maxim XL 035 FS","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Fludioxonil + Metalaxil-M"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Melius","fab":"UPL","cat":"Regulador de Crescimento","ia":"Trinexapaque-etÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Melyra","fab":"BASF","cat":"Fungicida","ia":"Pydiflumetofen + Fludioxonil"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Merlin 750 WG","fab":"Bayer","cat":"Herbicida","ia":"Isoxaflutol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Metalaxil-M 480 EC","fab":"Outros","cat":"Fungicida","ia":"Metalaxil-M"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Metarril SC","fab":"Ihara","cat":"Inseticida BiolÃÂ³gico","ia":"Metarhizium anisopliae"},
    {"nome":"Methomex 215 SL","fab":"Ihara","cat":"Inseticida","ia":"Metomil"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Metribuzim 480 SC","fab":"ADAMA","cat":"Herbicida","ia":"Metribuzim"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Metsulfurom 600 WG","fab":"Outros","cat":"Herbicida","ia":"Metsulfurom-metÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Metsuran 600 WG","fab":"UPL","cat":"Herbicida","ia":"Metsulfurom-MetÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Mibelya","fab":"BASF","cat":"Fungicida","ia":"Pydiflumetofen + Difenoconazol"},
    # Ã¢ââ¬Ã¢ââ¬ MOSAIC Ã¢ââ¬Ã¢ââ¬
    {"nome":"MicroEssentials S15","fab":"Mosaic","cat":"Fertilizante","ia":"MAP + N + P + S 15%"},
    {"nome":"MicroEssentials S9","fab":"Mosaic","cat":"Fertilizante","ia":"MAP + N + P + S 9%"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Minecto Duo","fab":"Syngenta","cat":"Inseticida","ia":"Abamectina + Ciantraniliprole"},
    {"nome":"Minecto Pro","fab":"Syngenta","cat":"Inseticida","ia":"Abamectina + Ciantraniliprole"},
    {"nome":"Miravis","fab":"Syngenta","cat":"Fungicida","ia":"Pydiflumetofen"},
    {"nome":"Miravis Ace","fab":"Syngenta","cat":"Fungicida","ia":"Pydiflumetofen + Azoxistrobina"},
    {"nome":"Miravis Duo","fab":"Syngenta","cat":"Fungicida","ia":"Pydiflumetofen + Difenoconazol"},
    {"nome":"Miravis Pro","fab":"Syngenta","cat":"Fungicida","ia":"Pydiflumetofen + Propiconazol"},
    {"nome":"Mitrion","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Propiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Moddus 250 EC","fab":"Outros","cat":"Regulador de Crescimento","ia":"Trinexapaque-etÃÂ­lico"},
    {"nome":"Molibdato de SÃÂ³dio","fab":"Outros","cat":"Fertilizante","ia":"Mo 39%"},
    {"nome":"MolibdÃÂªnio 10%","fab":"Outros","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"MolibdÃÂªnio"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Monarca 200 OD","fab":"Ihara","cat":"Inseticida","ia":"Metoxifenozida + Espinosade"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Movento 150 OD","fab":"Bayer","cat":"Inseticida","ia":"Spirotetramat"},
    # Ã¢ââ¬Ã¢ââ¬ MOSAIC Ã¢ââ¬Ã¢ââ¬
    {"nome":"MPasto 20-00-20","fab":"Mosaic","cat":"Fertilizante","ia":"NK 20-00-20 + S"},
    {"nome":"MPasto 20-05-20","fab":"Mosaic","cat":"Fertilizante","ia":"NPK 20-05-20 + S + Zn + B"},
    {"nome":"MPasto Plus","fab":"Mosaic","cat":"Fertilizante","ia":"NPK + S + Zn + B"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Murvin 850 PM","fab":"ADAMA","cat":"Inseticida","ia":"Carbaril"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Mustang 350 EW","fab":"Corteva","cat":"Inseticida","ia":"Zeta-Cipermetrina"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Nativo","fab":"Bayer","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Nativo 750 WG","fab":"ADAMA","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Nativo OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Nemathorin 150 EC","fab":"Outros","cat":"Nematicida","ia":"Fostiazate"},
    {"nome":"Nicossulfurom 240 SC","fab":"Outros","cat":"Herbicida","ia":"Nicossulfurom"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Nimaxxa","fab":"UPL","cat":"Nematicida","ia":"Purpureocillium lilacinum"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Nimbus","fab":"Outros","cat":"Adjuvante","ia":"Ãâleo Vegetal"},
    {"nome":"Nimitz Pro","fab":"Outros","cat":"Nematicida","ia":"Fluensulfona"},
    {"nome":"Nitrato de CÃÂ¡lcio","fab":"Outros","cat":"Fertilizante","ia":"15,5% N + 26% CaO"},
    {"nome":"Nitrato de PotÃÂ¡ssio","fab":"Outros","cat":"Fertilizante","ia":"13% N + 46% K2O"},
    {"nome":"Nitrofoska Foliar","fab":"Outros","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"NPK Foliar"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Nomolt 150","fab":"BASF","cat":"Inseticida","ia":"Teflubenzurom"},
    # Ã¢ââ¬Ã¢ââ¬ NORTOX Ã¢ââ¬Ã¢ââ¬
    {"nome":"Nortox 2,4-D","fab":"Nortox","cat":"Herbicida","ia":"2,4-D Amina 806"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Nortox 480 SL","fab":"UPL","cat":"Herbicida","ia":"Glifosato"},
    # Ã¢ââ¬Ã¢ââ¬ NORTOX Ã¢ââ¬Ã¢ââ¬
    {"nome":"Nortox Abamectina","fab":"Nortox","cat":"Inseticida","ia":"Abamectina 18 EC"},
    {"nome":"Nortox Atrazina 500","fab":"Nortox","cat":"Herbicida","ia":"Atrazina"},
    {"nome":"Nortox Cipermetrina","fab":"Nortox","cat":"Inseticida","ia":"Cipermetrina 250 EC"},
    {"nome":"Nortox ClorpirifÃÂ³s","fab":"Nortox","cat":"Inseticida","ia":"ClorpirifÃÂ³s 480 EC"},
    {"nome":"Nortox Deltametrina","fab":"Nortox","cat":"Inseticida","ia":"Deltametrina 25 EC"},
    {"nome":"Nortox Imidaclopride","fab":"Nortox","cat":"Inseticida","ia":"Imidaclopride 480 SC"},
    {"nome":"Nortox Mancozebe","fab":"Nortox","cat":"Fungicida","ia":"Mancozebe 800 WP"},
    {"nome":"Nortox Pendimetalina","fab":"Nortox","cat":"Herbicida","ia":"Pendimetalina 400 EC"},
    {"nome":"Nortox Tebuconazol","fab":"Nortox","cat":"Fungicida","ia":"Tebuconazol 200 EC"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"NPK 04-14-08","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂ§ÃÂ£o NPK 04-14-08"},
    {"nome":"NPK 04-20-20","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂ§ÃÂ£o NPK 04-20-20"},
    {"nome":"NPK 05-25-25","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂ§ÃÂ£o NPK 05-25-25"},
    {"nome":"NPK 08-20-20","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂ§ÃÂ£o NPK 08-20-20"},
    {"nome":"NPK 08-28-16","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂ§ÃÂ£o NPK 08-28-16"},
    {"nome":"NPK 10-10-10","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂ§ÃÂ£o NPK 10-10-10"},
    {"nome":"NPK 10-20-20","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂ§ÃÂ£o NPK 10-20-20"},
    {"nome":"NPK 12-06-12","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂ§ÃÂ£o NPK 12-06-12"},
    {"nome":"NPK 12-12-12","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂ§ÃÂ£o NPK 12-12-12"},
    {"nome":"NPK 15-05-30","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂ§ÃÂ£o NPK 15-05-30"},
    {"nome":"NPK 20-00-20","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂ§ÃÂ£o NPK 20-00-20"},
    {"nome":"NPK 20-05-20","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂ§ÃÂ£o NPK 20-05-20"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Nurelle D 550/50","fab":"Ihara","cat":"Inseticida","ia":"ClorpirifÃÂ³s + Cipermetrina"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Nuvita","fab":"UPL","cat":"Bioestimulante","ia":"Extrato de algas + aminoÃÂ¡cidos"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Oberon 240 SC","fab":"Bayer","cat":"Inseticida","ia":"Espirodiclofeno"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Oberon OF","fab":"Ouro Fino","cat":"Acaricida","ia":"Espirodiclofeno"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Olea","fab":"UPL","cat":"Herbicida","ia":"2,4-D + Metsulfurom + Picloram"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Opera","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Opera OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Opera Ultra","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Orkestra OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Orkestra SC","fab":"BASF","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Orondis Flexi","fab":"Syngenta","cat":"Fungicida","ia":"Oxathiapiprolin + Mandipropamida"},
    {"nome":"Orondis Gold","fab":"Syngenta","cat":"Fungicida","ia":"Oxathiapiprolin + Mefenoxam"},
    {"nome":"Orondis Ultra","fab":"Syngenta","cat":"Fungicida","ia":"Oxathiapiprolin + Clorotalonil"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ortus 50 SC","fab":"Outros","cat":"Acaricida","ia":"Fenpiroximato"},
    {"nome":"Oxifluorfem 240 EC","fab":"Outros","cat":"Herbicida","ia":"Oxifluorfem"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Pagani","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol + Fluxapiroxade"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Palisade EC","fab":"Outros","cat":"Regulador de Crescimento","ia":"Prohexadona de CÃÂ¡lcio"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Pallas 45 OD","fab":"Syngenta","cat":"Herbicida","ia":"Piroxsulam"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Pantera 40 EC","fab":"ADAMA","cat":"Herbicida","ia":"Quizalofope-P-etÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Pavecto","fab":"BASF","cat":"Fungicida","ia":"Mefentrifluconazol + Boscalida"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Pendimetalina 400 EC","fab":"Outros","cat":"Herbicida","ia":"Pendimetalina"},
    # Ã¢ââ¬Ã¢ââ¬ MOSAIC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Performa Bio","fab":"Mosaic","cat":"Fertilizante","ia":"MAP + S + PGPR"},
    {"nome":"Performa Full","fab":"Mosaic","cat":"Fertilizante","ia":"N+P+K+Mg+S+B completo"},
    {"nome":"Performa HF","fab":"Mosaic","cat":"Fertilizante","ia":"MicroEssentials + Aspire + K-Mag"},
    {"nome":"Performa Neo","fab":"Mosaic","cat":"Fertilizante","ia":"MicroEssentials + K-Mag"},
    {"nome":"Performa Plus","fab":"Mosaic","cat":"Fertilizante","ia":"MicroEssentials + Aspire"},
    {"nome":"Performa Ultra","fab":"Mosaic","cat":"Fertilizante","ia":"K + Mg + S + B"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Pergado MZ","fab":"Syngenta","cat":"Fungicida","ia":"Mandipropamida + Mancozebe"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Permetrina 500 EC","fab":"ADAMA","cat":"Inseticida","ia":"Permetrina"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Persist","fab":"FMC","cat":"Herbicida","ia":"Imazaquim"},
    # Ã¢ââ¬Ã¢ââ¬ TIMAC AGRO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Physiostart","fab":"Timac Agro","cat":"Fertilizante","ia":"MAP + Ca + tecnologia Physio"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Picloram 240 SL","fab":"Outros","cat":"Herbicida","ia":"Picloram"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Pidan","fab":"FMC","cat":"Inseticida","ia":"Clorfenapir"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Pidan 360 EC","fab":"Ihara","cat":"Inseticida","ia":"Clorfenapir"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Piraclostrobina 250 EC","fab":"Outros","cat":"Fungicida","ia":"Piraclostrobina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Pirate","fab":"BASF","cat":"Inseticida","ia":"Clorfenapir"},
    {"nome":"Pirimor 500 WG","fab":"BASF","cat":"Inseticida","ia":"Pirimicarbe"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Pirimor 500 WG Adama","fab":"ADAMA","cat":"Inseticida","ia":"Pirimicarbe"},
    {"nome":"Pivot 600 CS","fab":"ADAMA","cat":"Herbicida","ia":"Imazetapir"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Pivotal","fab":"Corteva","cat":"Tratamento de Sementes","ia":"Clorantraniliprole + Tiametoxam"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Plateau 700 WG","fab":"BASF","cat":"Herbicida","ia":"Imazapique"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Plenexos","fab":"Bayer","cat":"Inseticida","ia":"Fluazaindolizina"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Plinazolin","fab":"Syngenta","cat":"Inseticida","ia":"Plinazolina"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Pluto 100 SC","fab":"Outros","cat":"Acaricida","ia":"Etoxazol"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Poast","fab":"ADAMA","cat":"Herbicida","ia":"Setoxidim"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Polo 500 WP","fab":"Syngenta","cat":"Inseticida","ia":"Diafentiurom"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Polyram DF","fab":"BASF","cat":"Fungicida","ia":"Metiram"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Polytrin 400/40 EC","fab":"Ihara","cat":"Inseticida","ia":"ProfenofÃÂ³s + Cipermetrina"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Poncho 600 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Clotianidina"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"PotÃÂ¡ssio Foliar 10%","fab":"Outros","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"PotÃÂ¡ssio"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Predix","fab":"FMC","cat":"Fungicida","ia":"Fluxapiroxade"},
    {"nome":"Premio 200 SC","fab":"FMC","cat":"Inseticida","ia":"Clorantraniliprole"},
    {"nome":"Presence 500","fab":"FMC","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Presence 500 SC","fab":"UPL","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Presence OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Prexio","fab":"BASF","cat":"Inseticida","ia":"Broflanilida"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Primestra Gold","fab":"Bayer","cat":"Herbicida","ia":"S-Metolacloro + Atrazina"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Priori Top","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Difenoconazol"},
    {"nome":"Priori Xtra","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Ciproconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Priori Xtra OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Ciproconazol"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Proclaim 50 WG","fab":"Syngenta","cat":"Inseticida","ia":"Benzoato de Emamectina"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Propiconazol 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Propiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Propose","fab":"UPL","cat":"Inseticida","ia":"Clorantraniliprole + Clorfenapir"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Prosaro 420 SC","fab":"Bayer","cat":"Fungicida","ia":"Protioconazol + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Provar","fab":"Outros","cat":"Acaricida","ia":"Hexitiazox"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Provost 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Propiconazol + Iprodiona"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Provost Opti","fab":"Bayer","cat":"Fungicida","ia":"Iprodiona + Propiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Quadris","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Rabano","fab":"Ouro Fino","cat":"Herbicida","ia":"Fluazifope-P-butÃÂ­lico + Fomesafem"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Rampage 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Ciproconazol"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Raptor","fab":"BASF","cat":"Herbicida","ia":"Imazapique"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ravine 240 EC","fab":"ADAMA","cat":"Fungicida","ia":"Boscalida"},
    {"nome":"Reason 500 SC","fab":"ADAMA","cat":"Fungicida","ia":"Famoxadona + Cimoxanil"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Rebron","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole + Tiametoxam"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Regent 800 WG","fab":"ADAMA","cat":"Inseticida","ia":"Fipronil"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Regent Duo","fab":"BASF","cat":"Inseticida","ia":"Fipronil + Tiametoxam"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Reglone","fab":"Syngenta","cat":"Herbicida","ia":"Diquat"},
    {"nome":"Revus Opti","fab":"Syngenta","cat":"Fungicida","ia":"Mandipropamida + Clorotalonil"},
    {"nome":"Revus Top","fab":"Syngenta","cat":"Fungicida","ia":"Mandipropamida + Difenoconazol"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Revysol","fab":"BASF","cat":"Fungicida","ia":"Mefentrifluconazol"},
    {"nome":"Rhodiauram 700 WS","fab":"BASF","cat":"Tratamento de Sementes","ia":"Thiram"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ridomil Gold MZ","fab":"Syngenta","cat":"Fungicida","ia":"Metalaxil-M + Mancozebe"},
    {"nome":"Ridomil Gold WG","fab":"Syngenta","cat":"Fungicida","ia":"Metalaxil-M + Cobre"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Rinskor Active","fab":"Corteva","cat":"Herbicida","ia":"Florpirauifen-benzil"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ripcord 100 EC","fab":"Syngenta","cat":"Inseticida","ia":"Cipermetrina"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Rizoliq Top","fab":"Outros","cat":"Fungicida BiolÃÂ³gico","ia":"Trichoderma harzianum"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Roundup Original","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},
    {"nome":"Roundup Powermax","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},
    {"nome":"Roundup Ready","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},
    {"nome":"Roundup Transorb HC","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},
    {"nome":"Roundup Ultra Max","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},
    {"nome":"Roundup WG","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Rovral SC","fab":"UPL","cat":"Fungicida","ia":"Iprodiona"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Rynaxypyr 200 SC","fab":"Corteva","cat":"Inseticida","ia":"Clorantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"S-Metolacloro 960 EC","fab":"Outros","cat":"Herbicida","ia":"S-Metolacloro"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Samson Extra 6%","fab":"UPL","cat":"Herbicida","ia":"Nicossulfurom"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Samurai SC","fab":"Ihara","cat":"Inseticida","ia":"Imidaclopride + Lambda-Cialotrina"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Sanmite 150 WP","fab":"ADAMA","cat":"Acaricida","ia":"Piridabem"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Sanson 40 SC","fab":"Syngenta","cat":"Herbicida","ia":"Nicossulfurom"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Savey 50 WP","fab":"Outros","cat":"Acaricida","ia":"Hexitiazox"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Score 250 EC","fab":"Syngenta","cat":"Fungicida","ia":"Difenoconazol"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Score Ihara","fab":"Ihara","cat":"Fungicida","ia":"Difenoconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Score OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Difenoconazol"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Select Max","fab":"Corteva","cat":"Herbicida","ia":"Cletodim"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Seltima","fab":"BASF","cat":"Fungicida","ia":"Isoflucipramo + Propiconazol"},
    {"nome":"Seltima Duo","fab":"BASF","cat":"Fungicida","ia":"Isoflucipramo + Trifloxistrobina"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Semevin 350 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Tiametoxam"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Sencor 480 SC","fab":"ADAMA","cat":"Herbicida","ia":"Metribuzim"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Serenade ASO","fab":"Outros","cat":"Fungicida BiolÃÂ³gico","ia":"Bacillus subtilis"},
    {"nome":"Setoxidim 184 EC","fab":"Outros","cat":"Herbicida","ia":"Setoxidim"},
    # Ã¢ââ¬Ã¢ââ¬ MOSAIC Ã¢ââ¬Ã¢ââ¬
    {"nome":"SFP 10-40-00+S","fab":"Mosaic","cat":"Fertilizante","ia":"N + P + S em grÃÂ¢nulo ÃÂºnico"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Silvacur Combi","fab":"Bayer","cat":"Fungicida","ia":"Tebuconazol + Triadimenol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Silwet L-77","fab":"Outros","cat":"Adjuvante","ia":"Silicone"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Sivanto Prime 100 SL","fab":"Bayer","cat":"Inseticida","ia":"Flupyradifurona"},
    {"nome":"Sivanto Prime 200 SL","fab":"Bayer","cat":"Inseticida","ia":"Flupyradifurona"},
    {"nome":"Sonata AS","fab":"Bayer","cat":"Inseticida BiolÃÂ³gico","ia":"Bacillus pumilus"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Sperto","fab":"UPL","cat":"Inseticida","ia":"Bifentrina + Imidaclopride"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Sphere Max","fab":"Bayer","cat":"Fungicida","ia":"Trifloxistrobina + Ciproconazol"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Sphere OF","fab":"UPL","cat":"Fungicida","ia":"Trifloxistrobina + Ciproconazol"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Spinetoram 250 SC","fab":"Corteva","cat":"Inseticida","ia":"Espinetoram"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Spinnaker","fab":"UPL","cat":"Herbicida","ia":"Imazapique"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Spintor 480 SC","fab":"Corteva","cat":"Inseticida","ia":"Espinosade"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Spiromax 240 SC","fab":"Outros","cat":"Acaricida","ia":"Espirodiclofeno"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Sponta AlgodÃÂ£o","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole"},
    {"nome":"Sponta Milho","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Spot SC","fab":"BASF","cat":"Fungicida","ia":"Fluazinam"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Spread Max","fab":"Outros","cat":"Adjuvante","ia":"Surfactante"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Standak Top","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Fipronil + Piraclostrobina + Tiofanato"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Starane Quatro","fab":"Corteva","cat":"Herbicida","ia":"Fluroxipir-meptÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Start UPL","fab":"UPL","cat":"Inseticida","ia":"Fipronil"},
    # Ã¢ââ¬Ã¢ââ¬ TIMAC AGRO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Starter Timac","fab":"Timac Agro","cat":"Fertilizante","ia":"N + P + Zn + aminoÃÂ¡cidos"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Status","fab":"BASF","cat":"Fungicida","ia":"Dimoxistrobina + Epoxiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Stimulate Foliar","fab":"Outros","cat":"Regulador de Crescimento","ia":"Citocinina + Auxina + Giberelina"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Stomp 400 CS","fab":"ADAMA","cat":"Herbicida","ia":"Pendimetalina"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Stopit Ca","fab":"Outros","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"CÃÂ¡lcio"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Stratego 250 EC","fab":"Bayer","cat":"Fungicida","ia":"Trifloxistrobina + Propiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Stroby SC","fab":"BASF","cat":"Fungicida","ia":"Cresoxim-metÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ TIMAC AGRO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Sulfammo 26N","fab":"Timac Agro","cat":"Fertilizante","ia":"26% N amoniacal + S"},
    {"nome":"Sulfammo MeTA 11","fab":"Timac Agro","cat":"Fertilizante","ia":"11% N + S inibidor MeTA"},
    {"nome":"Sulfammo MeTA 17","fab":"Timac Agro","cat":"Fertilizante","ia":"17% N + S inibidor MeTA"},
    {"nome":"Sulfammo MeTA 21","fab":"Timac Agro","cat":"Fertilizante","ia":"21% N + S inibidor MeTA"},
    {"nome":"Sulfammo MeTA 29","fab":"Timac Agro","cat":"Fertilizante","ia":"29% N + S inibidor MeTA"},
    {"nome":"Sulfammo MeTA 29 Boro","fab":"Timac Agro","cat":"Fertilizante","ia":"29% N + S + B"},
    {"nome":"Sulfammo Ultra","fab":"Timac Agro","cat":"Fertilizante","ia":"N + S alta concentraÃÂ§ÃÂ£o"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Sulfato de AmÃÂ´nio","fab":"Outros","cat":"Fertilizante","ia":"21% N + 24% S"},
    {"nome":"Sulfato de MagnÃÂ©sio","fab":"Outros","cat":"Fertilizante","ia":"Mg 10% + S 13%"},
    {"nome":"Sulfato de ManganÃÂªs","fab":"Outros","cat":"Fertilizante","ia":"Mn 26% + S"},
    {"nome":"Sulfato de PotÃÂ¡ssio","fab":"Outros","cat":"Fertilizante","ia":"K2SO4 50% K2O + 18% S"},
    {"nome":"Sulfato de Zinco","fab":"Outros","cat":"Fertilizante","ia":"Zn 21% + S 11%"},
    {"nome":"Sulfentrazona 500 SC","fab":"Outros","cat":"Herbicida","ia":"Sulfentrazona"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Sumidan 25 EC","fab":"ADAMA","cat":"Inseticida","ia":"Esfenvalerato"},
    {"nome":"Sumithion 500 EC","fab":"ADAMA","cat":"Inseticida","ia":"Fenitrotiom"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Superfosfato Simples","fab":"Outros","cat":"Fertilizante","ia":"SSP 18% P2O5 + 12% S"},
    {"nome":"Superfosfato Triplo","fab":"Outros","cat":"Fertilizante","ia":"STP 46% P2O5"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Surtain","fab":"BASF","cat":"Herbicida","ia":"Saflufenacil + Clomazona"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Switch 625 WG","fab":"Corteva","cat":"Fungicida","ia":"Ciprodinil + Fludioxonil"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Systhane 750 WG","fab":"ADAMA","cat":"Fungicida","ia":"Miclobutanil"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tacklier","fab":"UPL","cat":"Inseticida BiolÃÂ³gico","ia":"Bacillus thuringiensis"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Takumi 20 SC","fab":"Ihara","cat":"Inseticida","ia":"Flubendiamida"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Talstar 100 EC","fab":"FMC","cat":"Inseticida","ia":"Bifentrina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Targa Max 50 EC","fab":"BASF","cat":"Herbicida","ia":"Quizalofope-P-etÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Targa Quik","fab":"ADAMA","cat":"Herbicida","ia":"Quizalofope-P-etÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tebuco OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tebuconazol 200 EC","fab":"Bayer","cat":"Fungicida","ia":"Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tebuconazol 750 WG","fab":"ADAMA","cat":"Fungicida","ia":"Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tepraloxidim 200 EC","fab":"Outros","cat":"Herbicida","ia":"Tepraloxidim"},
    {"nome":"Termofosfato Yoorin","fab":"Outros","cat":"Fertilizante","ia":"P2O5 18% + Ca + Mg + Si"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Thiram 480 SC","fab":"ADAMA","cat":"Fungicida","ia":"Thiram"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Thiram 750 WS","fab":"Outros","cat":"Fungicida","ia":"Thiram"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Thunder","fab":"UPL","cat":"Herbicida","ia":"Asulam"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tiametoxam 700 WS","fab":"Outros","cat":"Inseticida","ia":"Tiametoxam"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tiger 100 EC","fab":"FMC","cat":"Inseticida","ia":"Bifentrina"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tilt 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Propiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tiofanato MetÃÂ­lico 700 WG","fab":"Outros","cat":"Fungicida","ia":"Tiofanato MetÃÂ­lico"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tirexor","fab":"BASF","cat":"Herbicida","ia":"Trifludimoxazim"},
    # Ã¢ââ¬Ã¢ââ¬ TIMAC AGRO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Top-Phos","fab":"Timac Agro","cat":"Fertilizante","ia":"MAP protegido tecnologia CSP"},
    {"nome":"Top-Phos 40","fab":"Timac Agro","cat":"Fertilizante","ia":"Fosfato amoniado protegido 40% P2O5"},
    {"nome":"Top-Phos Arroz","fab":"Timac Agro","cat":"Fertilizante","ia":"FÃÂ³sforo protegido para arroz"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tordon","fab":"Bayer","cat":"Herbicida","ia":"2,4-D + Picloram"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tornade Duo","fab":"Corteva","cat":"Herbicida","ia":"2,4-D + Picloram"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Torque 550 SC","fab":"Ihara","cat":"Acaricida","ia":"Fenbutestanho"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Touchdown IQ","fab":"Syngenta","cat":"Herbicida","ia":"Glifosato"},
    # Ã¢ââ¬Ã¢ââ¬ CORTEVA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tracer 480 SC","fab":"Corteva","cat":"Inseticida","ia":"Espinosade"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Transform 500 WG","fab":"FMC","cat":"Inseticida","ia":"Sulfoxaflor"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Trico WP","fab":"Outros","cat":"Fungicida BiolÃÂ³gico","ia":"Trichoderma viride"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Tridium","fab":"UPL","cat":"Fungicida","ia":"Trifloxistrobina + Epoxiconazol + Tebuconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Trifloxistrobina 250 SC","fab":"Outros","cat":"Fungicida","ia":"Trifloxistrobina"},
    {"nome":"Trifluralin 480 EC","fab":"Outros","cat":"Herbicida","ia":"Trifluralina"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Trilex Advance","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Trifloxistrobina + Protioconazol + Spirotetramat"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Trophy 500 EC","fab":"Syngenta","cat":"Herbicida","ia":"Acetocloro"},
    # Ã¢ââ¬Ã¢ââ¬ MOSAIC Ã¢ââ¬Ã¢ââ¬
    {"nome":"TSP Mosaic","fab":"Mosaic","cat":"Fertilizante","ia":"Superfosfato triplo 00-46-00"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Unika Ca+B","fab":"Outros","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"CÃÂ¡lcio + Boro"},
    # Ã¢ââ¬Ã¢ââ¬ BAYER Ã¢ââ¬Ã¢ââ¬
    {"nome":"Unison Xpro","fab":"Bayer","cat":"Fungicida","ia":"Bixafem + Propiconazol + Trifloxistrobina"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Unizeb 750 WG","fab":"Syngenta","cat":"Fungicida","ia":"Mancozebe"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Unizeb Gold","fab":"UPL","cat":"Fungicida","ia":"Mancozebe 750 WG"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Ureia 45% N","fab":"Outros","cat":"Fertilizante","ia":"Carbamida 45% N"},
    {"nome":"Ureia NBPT","fab":"Outros","cat":"Fertilizante","ia":"Ureia + inibidor urease NBPT"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Velpar K WG","fab":"UPL","cat":"Herbicida","ia":"Hexazinona + Diurom"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Velum Prime","fab":"Outros","cat":"Nematicida","ia":"Fluopyram"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Verdadeiro","fab":"Ouro Fino","cat":"Inseticida","ia":"Tiametoxam"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Verdadero","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam"},
    {"nome":"Verdavis Milho","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Clorantraniliprole"},
    {"nome":"Verdavis Soja","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Clorantraniliprole"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Verismo","fab":"BASF","cat":"Inseticida","ia":"Metaflumizone"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Versys","fab":"Syngenta","cat":"Inseticida","ia":"Flupyrimin + Lambda-Cialotrina"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Vertimec 18 EC","fab":"ADAMA","cat":"Acaricida","ia":"Abamectina"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Vertimec Gold","fab":"Ihara","cat":"Acaricida","ia":"Abamectina"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Vibrance Duo","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Sedaxane + Fludioxonil"},
    {"nome":"Vibrance Integral","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Sedaxane + Fludioxonil + Metalaxil-M"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Vitavax Thiram 200 SC","fab":"BASF","cat":"Tratamento de Sementes","ia":"Carboxim + Thiram"},
    # Ã¢ââ¬Ã¢ââ¬ UPL Ã¢ââ¬Ã¢ââ¬
    {"nome":"Vitavax Thiram 200 SC UPL","fab":"UPL","cat":"Fungicida","ia":"Carboxim + Thiram"},
    {"nome":"Vitavax Ultra TS","fab":"UPL","cat":"Tratamento de Sementes","ia":"Carboxim + Tiram + Tiametoxam"},
    # Ã¢ââ¬Ã¢ââ¬ SYNGENTA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Voliam Flexi","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Clorantraniliprole"},
    {"nome":"Voliam Targo","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole + Abamectina"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Voraxor","fab":"BASF","cat":"Herbicida","ia":"Trifludimoxazim + Saflufenacil"},
    {"nome":"Vydate 240 SL","fab":"BASF","cat":"Inseticida","ia":"Oxamil"},
    # Ã¢ââ¬Ã¢ââ¬ IHARA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Xcyte","fab":"Ihara","cat":"Inseticida","ia":"Ciantraniliprole + Clorfenapir"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"XenTari WDG","fab":"Outros","cat":"Inseticida BiolÃÂ³gico","ia":"Bacillus thuringiensis aizawai"},
    # Ã¢ââ¬Ã¢ââ¬ BASF Ã¢ââ¬Ã¢ââ¬
    {"nome":"Zampro","fab":"BASF","cat":"Fungicida","ia":"Ametoctradina + Dimetomorfe"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Zeal 72 WP","fab":"Outros","cat":"Acaricida","ia":"Etoxazol"},
    # Ã¢ââ¬Ã¢ââ¬ ADAMA Ã¢ââ¬Ã¢ââ¬
    {"nome":"Zeta-Cipermetrina 250 EC","fab":"ADAMA","cat":"Inseticida","ia":"Zeta-Cipermetrina"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"Zeus OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Epoxiconazol"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"Zinco Quelatado 9%","fab":"Outros","cat":"Foliar / NutriÃÂ§ÃÂ£o","ia":"Zinco"},
    # Ã¢ââ¬Ã¢ââ¬ FMC Ã¢ââ¬Ã¢ââ¬
    {"nome":"Zoom 750 WG","fab":"FMC","cat":"Inseticida","ia":"Acefato"},
    # Ã¢ââ¬Ã¢ââ¬ OUTROS Ã¢ââ¬Ã¢ââ¬
    {"nome":"ÃÂcido BÃÂ³rico","fab":"Outros","cat":"Fertilizante","ia":"B 17%"},
    # Ã¢ââ¬Ã¢ââ¬ OURO FINO Ã¢ââ¬Ã¢ââ¬
    {"nome":"ÃÅ nio 200 SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Iprodiona"},
]


# Ordena por nome para o autocomplete
CATALOGO_PRODUTOS.sort(key=lambda x: x["nome"].lower())

def buscar_produtos_catalogo(query):
    """Retorna produtos do catÃÂ¡logo filtrando por nome ou ingrediente ativo."""
    if not query:
        return CATALOGO_PRODUTOS
    q = query.lower()
    # Primeiro os que COMEÃâ¡AM com a busca
    starts = [p for p in CATALOGO_PRODUTOS if p["nome"].lower().startswith(q)]
    # Depois os que CONTÃÅ M em qualquer posiÃÂ§ÃÂ£o (nome ou IA)
    contains = [p for p in CATALOGO_PRODUTOS
                if not p["nome"].lower().startswith(q)
                and (q in p["nome"].lower() or q in p["ia"].lower() or q in p["cat"].lower())]
    return starts + contains


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: ESTOQUE DE INSUMOS
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬

# FUNÃâ¡Ãâ¢ES UTILITÃÂRIAS
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
def classificar(valor, baixo, medio):
    if valor < baixo:   return "Baixo"
    elif valor < medio: return "MÃÂ©dio"
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
                if app.get("ID ÃÂrea", id_area) == id_area
            ]
            st.session_state.areas[i]["Estoque"] = st.session_state.estoque.copy()
            break
    salvar_dados_iaagro()


def gerar_pdf_programacao_aplicacoes(aplicacoes, fazenda="", talhao="", cultura="", area_ha=0, operador=""):
    """Gera PDF profissional com programaÃÂ§ÃÂ£o de aplicaÃÂ§ÃÂµes por estÃÂ¡dio."""
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
        "Ãâleo mineral/vegetal":colors.HexColor("#ede9fe"),"Fertilizante foliar":colors.HexColor("#fce7f3"),
        "Regulador":colors.HexColor("#ffedd5"),"Outro":COR_CINZA,
    }

    def P(txt, size=9, bold=False, color=None, align=TA_LEFT):
        fn = "Helvetica-Bold" if bold else "Helvetica"
        c  = color or COR_TEXTO
        return Paragraph(txt, ParagraphStyle("p", fontName=fn, fontSize=size, textColor=c, alignment=align, leading=size+3))

    # CABEÃâ¡ALHO
    h = [[P("IAAgro",18,True,COR_VERDE), P("PROGRAMAÃâ¡ÃÆO DE APLICACOES",14,True,COR_BRANCO,TA_CENTER),
          P(f"Emitido: {datetime.now().strftime('%d/%m/%Y %H:%M')}",7,False,COR_CINZA,TA_RIGHT)]]
    th = Table(h, colWidths=[4*cm,10*cm,4.5*cm])
    th.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),COR_VERDE_E),
        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    story.append(th); story.append(Spacer(1,3*mm))

    # INFO PROPRIEDADE
    i = [[P(f"<b>Fazenda:</b> {fazenda or 'Ã¢â¬â'}"),P(f"<b>Talhao:</b> {talhao or 'Ã¢â¬â'}"),
          P(f"<b>Cultura:</b> {cultura or 'Ã¢â¬â'}"),P(f"<b>Area:</b> {area_ha} ha"),
          P(f"<b>Responsavel:</b> {operador or 'Ã¢â¬â'}")]]
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

    # BLOCOS POR ESTÃÂDIO
    for num, aplic in enumerate(aplicacoes, 1):
        est = aplic.get("EstÃÂ¡dio") or aplic.get("AplicaÃÂ§ÃÂ£o","")
        for e in ["Ã°Å¸ÅÂ±","Ã°Å¸ÅÂ¿","Ã°Å¸ÅÂ¾","Ã°Å¸ÅÂ¸","Ã°Å¸Â«Ë","Ã°Å¸ââ¹"]: est = est.replace(e,"").strip()

        cab = [[P(f"{num}. {est}",11,True,COR_BRANCO),
                P(f"Data: {aplic.get('Data','Ã¢â¬â')} | Area: {aplic.get('ÃÂrea aplicada ha',0)} ha | "
                  f"Calda: {aplic.get('Volume calda L/ha',0)} L/ha | "
                  f"Tanques: {aplic.get('NÃÂºmero tanques',0):.1f} | "
                  f"Pulverizador: {aplic.get('Pulverizador','Ã¢â¬â')} | "
                  f"Clima: {aplic.get('Clima aplicaÃÂ§ÃÂ£o','Ã¢â¬â')}",8,False,COR_CINZA)]]
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
    Calagem pelo mÃÂ©todo SMP (CQFS RS/SC 2016) ou pH em ÃÂ¡gua.
    PRNT mÃÂ©dio adotado: 75% (calcÃÂ¡rio comercial tÃÂ­pico da regiÃÂ£o Sul)
    FÃÂ³rmula: NC (t/ha) = dose_base / (PRNT/100)
    """
    PRNT = 0.75  # PRNT mÃÂ©dio 75% Ã¢â¬â calcÃÂ¡rio comercial RS/SC/PR

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
        precisa = True; motivos.append("AlumÃÂ­nio elevado")
    if calcio < 3:
        precisa = True; motivos.append("CÃÂ¡lcio baixo")
    if enxofre < 8:
        precisa = True; motivos.append("Enxofre baixo")
    if ctc < 6 and aluminio > 0.2:
        precisa = True; motivos.append("CTC baixa com alumÃÂ­nio presente")
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
    elif nota < 75: return "MÃÂ©dia"
    return "Baixa"


def estimar_producao(meta, nota):
    fator = nota / 100
    if   fator >= 0.85: return meta
    elif fator >= 0.70: return meta * 0.85
    elif fator >= 0.50: return meta * 0.70
    return meta * 0.55


def recomendacao_npk(cultura, produtividade, fosforo, potassio, materia_organica, argila=50, ph=5.5):
    # Remove ÃÂ­cone se presente
    cultura = cultura_limpa(cultura) if cultura else "Soja"
    """
    RecomendaÃÂ§ÃÂ£o NPK baseada em:
    - EMBRAPA Soja Ã¢â¬â Circular TÃÂ©cnica 98 + Tecnologias de ProduÃÂ§ÃÂ£o 2022
    - EMBRAPA Milho e Sorgo Ã¢â¬â Circular TÃÂ©cnica 100/2023
    - CQFS RS/SC 2016 (Manual de Calagem e AdubaÃÂ§ÃÂ£o)
    - IAC Boletim 100 (2014) Ã¢â¬â culturas diversas
    - EMBRAPA Trigo Ã¢â¬â RecomendaÃÂ§ÃÂµes TÃÂ©cnicas 2021
    - EMBRAPA Arroz e FeijÃÂ£o
    - MAPA Ã¢â¬â Boas PrÃÂ¡ticas AgrÃÂ­colas
    Unidades: kg/ha de N, P2O5, K2O
    P = Mehlich-1 (mg/dmÃÂ³) | K = mg/dmÃÂ³ | MO = g/dmÃÂ³ ou %
    """
    n = p2o5 = k2o = 0

    if cultura == "Soja":
        # EMBRAPA Soja: N=0 com boa nodulaÃÂ§ÃÂ£o (BNF supre 200-300 kg N/ha)
        n = 0
        # P2O5 Ã¢â¬â CQFS RS/SC 2016 Tab. 4.3 Ã¢â¬â solo argiloso (argila 41-60%)
        # ExportaÃÂ§ÃÂ£o: ~16 kg P2O5/sc (60 kg) Ã¢â â manutenÃÂ§ÃÂ£o + reposiÃÂ§ÃÂ£o
        if   fosforo < 4:   p2o5 = 140
        elif fosforo < 7:   p2o5 = 110
        elif fosforo < 11:  p2o5 = 90
        elif fosforo < 16:  p2o5 = 70
        elif fosforo < 22:  p2o5 = 55
        elif fosforo < 30:  p2o5 = 40
        else:               p2o5 = 25
        # K2O Ã¢â¬â CQFS RS/SC 2016 Tab. 4.4 Ã¢â¬â exportaÃÂ§ÃÂ£o ~18 kg K2O/sc
        if   potassio < 40:  k2o = 130
        elif potassio < 60:  k2o = 105
        elif potassio < 80:  k2o = 85
        elif potassio < 120: k2o = 70
        elif potassio < 180: k2o = 55
        elif potassio < 240: k2o = 40
        else:                k2o = 25
        # Ajuste produtividade (EMBRAPA Ã¢â¬â base 50 sc/ha)
        fator_prod = max(1.0, produtividade / 50)
        p2o5 = round(p2o5 * fator_prod, 0)
        k2o  = round(k2o  * fator_prod, 0)

    elif cultura == "Milho":
        # EMBRAPA Milho Ã¢â¬â base 10 t/ha, N parcelado (plantio + cobertura)
        # N plantio: 20-30 kg/ha | N cobertura: 30-50 kg/ha por 1000 kg grÃÂ£o
        n_plantio = 25
        n_cob     = min(produtividade * 1.5, 140)  # 1,5 kg N / sc 60kg
        n = round(n_plantio + n_cob, 1)
        # P2O5 Ã¢â¬â CQFS 2016 Tab. 5.3
        if   fosforo < 4:   p2o5 = 130
        elif fosforo < 7:   p2o5 = 105
        elif fosforo < 11:  p2o5 = 85
        elif fosforo < 16:  p2o5 = 65
        elif fosforo < 22:  p2o5 = 50
        elif fosforo < 30:  p2o5 = 35
        else:               p2o5 = 20
        # K2O Ã¢â¬â CQFS 2016 Tab. 5.4
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
        # EMBRAPA Trigo Ã¢â¬â Sistema Plantio Direto Sul Brasil 2021
        # N = 30 plantio + cobertura conforme MO e produtividade
        if   materia_organica < 2.5: n = 30 + produtividade * 1.0
        elif materia_organica < 4.0: n = 20 + produtividade * 0.9
        else:                        n = 15 + produtividade * 0.8
        n = min(round(n, 1), 100)
        # P2O5 Ã¢â¬â CQFS 2016
        if   fosforo < 4:   p2o5 = 110
        elif fosforo < 7:   p2o5 = 90
        elif fosforo < 11:  p2o5 = 70
        elif fosforo < 16:  p2o5 = 55
        elif fosforo < 22:  p2o5 = 40
        else:               p2o5 = 25
        # K2O Ã¢â¬â CQFS 2016
        if   potassio < 60:  k2o = 90
        elif potassio < 80:  k2o = 70
        elif potassio < 120: k2o = 55
        elif potassio < 180: k2o = 40
        else:                k2o = 25

    elif cultura == "FeijÃÂ£o":
        # EMBRAPA FeijÃÂ£o + CQFS 2016 Ã¢â¬â fixaÃÂ§ÃÂ£o parcial de N
        # N starter 20 kg/ha + complemento se nÃÂ£o inoculado
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
        # EMBRAPA Arroz e FeijÃÂ£o Ã¢â¬â irrigado e sequeiro
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
        # EMBRAPA Trigo adaptado + pesquisas ParanÃÂ¡/RS
        # Canola extrai muito enxofre Ã¢â¬â recomenda gesso
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

    elif cultura == "CafÃÂ©":
        # EMBRAPA CafÃÂ© Ã¢â¬â Circular TÃÂ©cnica 132
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
        # IAC Boletim 100 Ã¢â¬â horticultura
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
        # GenÃÂ©rico Ã¢â¬â conservador
        n = 40; p2o5 = 60; k2o = 60

    # Ã¢ââ¬Ã¢ââ¬ Ajustes gerais de solo Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
    # Textura: solos arenosos (<20% argila) tÃÂªm menor CTC Ã¢â â mais K
    if argila < 15:     k2o = round(k2o * 1.25, 0)
    elif argila < 25:   k2o = round(k2o * 1.15, 0)
    elif argila > 70:   k2o = round(k2o * 0.90, 0)

    # MO alta reduz necessidade de N (mineralizaÃÂ§ÃÂ£o)
    if materia_organica >= 5.5:   n = round(n * 0.70, 1)
    elif materia_organica >= 4.0: n = round(n * 0.80, 1)
    elif materia_organica >= 3.0: n = round(n * 0.90, 1)

    # pH baixo reduz disponibilidade de P (precipitaÃÂ§ÃÂ£o com Al e Fe)
    if ph < 5.0:   p2o5 = round(p2o5 * 1.30, 0)
    elif ph < 5.3: p2o5 = round(p2o5 * 1.15, 0)
    elif ph < 5.5: p2o5 = round(p2o5 * 1.08, 0)

    return round(n, 1), round(p2o5, 1), round(k2o, 1)


def score_solo(d, cultura="Soja"):
    """
    Score de qualidade do solo baseado nos parÃÂ¢metros EMBRAPA/CQFS RS-SC 2016
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
        "FeijÃÂ£o": (6.0, 6.5), "Arroz": (5.5, 6.0), "Canola": (6.0, 6.5),
        "CafÃÂ©": (5.5, 6.5), "Tomate": (6.0, 6.8), "Batata": (5.5, 6.0),
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
            score -= 10; alertas.append(f"pH elevado Ã¢â¬â risco de deficiÃÂªncia de micronutrientes")

    # FÃÂ³sforo (mg/dmÃÂ³ Ã¢â¬â Mehlich-1)
    if fosforo > 0:
        if   fosforo < 6:   score -= 20; alertas.append("FÃÂ³sforo muito baixo (<6 mg/dmÃÂ³)")
        elif fosforo < 12:  score -= 12; alertas.append("FÃÂ³sforo baixo (6-12 mg/dmÃÂ³)")
        elif fosforo < 18:  score -= 6;  alertas.append("FÃÂ³sforo mÃÂ©dio Ã¢â¬â atenÃÂ§ÃÂ£o")

    # PotÃÂ¡ssio (mg/dmÃÂ³)
    if potassio > 0:
        if   potassio < 60:  score -= 20; alertas.append("PotÃÂ¡ssio muito baixo (<60 mg/dmÃÂ³)")
        elif potassio < 100: score -= 12; alertas.append("PotÃÂ¡ssio baixo (60-100 mg/dmÃÂ³)")
        elif potassio < 150: score -= 5;  alertas.append("PotÃÂ¡ssio mÃÂ©dio Ã¢â¬â monitorar")

    # CÃÂ¡lcio (cmolc/dmÃÂ³)
    if calcio > 0:
        if   calcio < 2.0: score -= 20; alertas.append("CÃÂ¡lcio muito baixo (<2 cmolc/dmÃÂ³)")
        elif calcio < 3.5: score -= 10; alertas.append("CÃÂ¡lcio baixo (2-3,5 cmolc/dmÃÂ³)")

    # MagnÃÂ©sio (cmolc/dmÃÂ³)
    if magnesio > 0:
        if   magnesio < 0.5: score -= 15; alertas.append("MagnÃÂ©sio muito baixo (<0,5 cmolc/dmÃÂ³)")
        elif magnesio < 1.0: score -= 8;  alertas.append("MagnÃÂ©sio baixo (0,5-1,0 cmolc/dmÃÂ³)")

    # RelaÃÂ§ÃÂ£o Ca:Mg ideal 3:1 a 5:1
    if calcio > 0 and magnesio > 0:
        rel = calcio / magnesio
        if rel < 2.5: alertas.append(f"RelaÃÂ§ÃÂ£o Ca:Mg baixa ({rel:.1f}:1) Ã¢â¬â risco de toxidez Mg")
        elif rel > 8:  alertas.append(f"RelaÃÂ§ÃÂ£o Ca:Mg alta ({rel:.1f}:1) Ã¢â¬â deficiÃÂªncia Mg possÃÂ­vel")

    # AlumÃÂ­nio (cmolc/dmÃÂ³) Ã¢â¬â tÃÂ³xico acima de 0,3
    if aluminio > 0:
        if aluminio > 1.0: score -= 25; alertas.append(f"AlumÃÂ­nio tÃÂ³xico ({aluminio} cmolc/dmÃÂ³) Ã¢â¬â urgente calcÃÂ¡rio")
        elif aluminio > 0.5: score -= 15; alertas.append(f"AlumÃÂ­nio elevado ({aluminio} cmolc/dmÃÂ³)")
        elif aluminio > 0.3: score -= 8;  alertas.append(f"AlumÃÂ­nio detectado ({aluminio} cmolc/dmÃÂ³)")

    # MatÃÂ©ria orgÃÂ¢nica (%)
    if materia_organica > 0:
        if   materia_organica < 1.5: score -= 15; alertas.append("MO muito baixa (<1,5%) Ã¢â¬â solo degradado")
        elif materia_organica < 2.5: score -= 8;  alertas.append("MO baixa (1,5-2,5%) Ã¢â¬â adubaÃÂ§ÃÂ£o verde recomendada")
        elif materia_organica > 6.0: alertas.append("MO alta Ã¢â¬â reduzir N mineral")

    # Micronutrientes (quando disponÃÂ­veis)
    if enxofre > 0 and enxofre < 5:
        score -= 8; alertas.append(f"Enxofre baixo (<5 mg/dmÃÂ³) Ã¢â¬â usar fertilizante com S")
    if zinco > 0 and zinco < 0.6:
        score -= 5; alertas.append(f"Zinco baixo (<0,6 mg/dmÃÂ³)")
    if boro > 0 and boro < 0.2:
        score -= 5; alertas.append(f"Boro baixo (<0,2 mg/dmÃÂ³) Ã¢â¬â importante para soja/cafÃÂ©")

    score = max(0, min(100, score))
    if   score >= 85: classe = "Excelente"
    elif score >= 70: classe = "Boa"
    elif score >= 50: classe = "MÃÂ©dia"
    elif score >= 30: classe = "Fraca"
    else:             classe = "CrÃÂ­tica"
    return score, classe, alertas


def baixar_estoque(nome_insumo, quantidade_usada, unidade_usada="L/ha"):
    """
    DÃÂ¡ baixa no estoque convertendo unidades automaticamente.
    Estoque sempre em L ou kg. AplicaÃÂ§ÃÂ£o pode ser mL/ha, g/ha, etc.
    """
    def converter_para_base(qtd, unid):
        """Converte para a unidade base: L ou kg."""
        unid = (unid or "").lower().replace(" ", "")
        if "ml" in unid:     return qtd / 1000  # mL Ã¢â â L
        if "g/ha" in unid or unid == "g":   return qtd / 1000  # g Ã¢â â kg
        if "mg" in unid:     return qtd / 1_000_000
        return qtd  # jÃÂ¡ em L ou kg

    qtd_convertida = converter_para_base(quantidade_usada, unidade_usada)

    for item in st.session_state.estoque:
        if item["Insumo"] == nome_insumo:
            estoque_atual = float(item.get("Quantidade", 0))
            if estoque_atual >= qtd_convertida:
                item["Quantidade"] = round(estoque_atual - qtd_convertida, 4)
                item["Valor Total R$"] = item["Quantidade"] * item.get("Valor UnitÃÂ¡rio R$", 0)
                return True, f"Baixa de {qtd_convertida:.3f} realizada."
            return False, f"Estoque insuficiente: tem {estoque_atual:.3f}, precisa {qtd_convertida:.3f}"
    return False, "Insumo nÃÂ£o encontrado no estoque."


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
menu = st.sidebar.radio(
    "Ã°Å¸ââ¹ Menu",
    [
        "Ã°Å¸ÂÂ  InÃÂ­cio",
        "Ã°Å¸ÅÂ¾ Lavoura",
        "Ã°Å¸Â§Âª Solo & AdubaÃÂ§ÃÂ£o",
        "Ã°Å¸âÂ° Financeiro",
        "Ã°Å¸âÂ¦ Operacional",
        "Ã°Å¸ÅÂ InteligÃÂªncia",
        "Ã°Å¸ÅÂ± Safrinha",
        "Ã°Å¸ââ RelatÃÂ³rio Final",
        "Ã¢Å¡â¢Ã¯Â¸Â ConfiguraÃÂ§ÃÂµes"
    ]
)

# Ã¢ââ¬Ã¢ââ¬ Backup rÃÂ¡pido na sidebar Ã¢ââ¬Ã¢ââ¬
st.sidebar.divider()
backup_bytes = gerar_backup()
st.sidebar.download_button(
    "Ã°Å¸âÂ¾ Baixar Backup",
    data=backup_bytes,
    file_name=f"iaagro_backup_{date.today()}.json",
    mime="application/json",
    use_container_width=True
)

if st.session_state.area_selecionada:
    st.sidebar.markdown(f'<div style="background:#14532d;color:#fff;padding:8px 12px;border-radius:8px;font-weight:700;font-size:13px;margin-top:6px;">Ã°Å¸ÅÂ¾ ÃÂrea ativa: {st.session_state.area_selecionada}</div>', unsafe_allow_html=True)

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MAPEAMENTO GLOBAL DE CULTURAS POR SEGMENTO
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
SEGMENTOS_INFO = {
    "Ã°Å¸ÅÂ¾ GrÃÂ£os":        {"desc":"Soja, Milho, Trigo e outros cereais",   "cor":"#14532d","borda":"#22c55e"},
    "Ã°Å¸ÅÂ¿ Horticultura": {"desc":"HortaliÃÂ§as, verduras e legumes",         "cor":"#14532d","borda":"#84cc16"},
    "Ã°Å¸ÂÅ½ Fruticultura": {"desc":"Frutas tropicais, uva, cafÃÂ© e outras",  "cor":"#7f1d1d","borda":"#f87171"},
    "Ã°Å¸ÅÂ² Silvicultura": {"desc":"Eucalipto, Pinus e reflorestamento",     "cor":"#1e3a5f","borda":"#38bdf8"},
}

CULTURAS_POR_SEGMENTO = {
    "Ã°Å¸ÅÂ¾ GrÃÂ£os":        ["Ã°Å¸ÅÂ± Soja","Ã°Å¸ÅÂ½ Milho","Ã°Å¸ÅÂ¾ Trigo","Ã°Å¸ÅÂ± FeijÃÂ£o","Ã°Å¸ÅÂ» Canola","Ã°Å¸ÅÂ¿ Aveia","Ã°Å¸ÂÅ¡ Arroz","Ã°Å¸ÅÂ¾ Sorgo","Ã°Å¸ÅÂ¾ Cevada","Ã°Å¸ÅÂ» Girassol"],
    "Ã°Å¸ÅÂ¿ Horticultura": ["Ã°Å¸Ââ¦ Tomate","Ã°Å¸Â¥â Batata","Ã°Å¸Â§â¦ Cebola","Ã°Å¸Â§â Alho","Ã°Å¸ÂÂ  Mandioca"],
    "Ã°Å¸ÂÅ½ Fruticultura": ["Ã°Å¸ÂÅ  Laranja","Ã°Å¸ÂÅ Banana","Ã°Å¸Ââ¡ Uva","Ã°Å¸ÂÅ½ MaÃÂ§ÃÂ£","Ã°Å¸Â¥Â­ Manga","Ã°Å¸Â¥â Abacate","Ã°Å¸Ââ¹ LimÃÂ£o","Ã°Å¸Ââ PÃÂªssego","Ã°Å¸Ââ Caqui","Ã¢Ëâ¢ CafÃÂ©"],
    "Ã°Å¸ÅÂ² Silvicultura": ["Ã°Å¸ÅÂ³ Eucalipto","Ã°Å¸ÅÂ² Pinus","Ã°Å¸ÅÂ´ Teca","Ã°Å¸ÅÂ¿ ParicÃÂ¡","Ã°Å¸ÅÂ² Cedro"],
}

# Mapa reverso para extrair nome sem ÃÂ­cone (para lÃÂ³gicas internas)
CULTURA_NOME_LIMPO = {c: c.split(" ",1)[1] if " " in c else c
                      for seg in CULTURAS_POR_SEGMENTO.values() for c in seg}

# ÃÂcone por nome limpo da cultura
CULTURA_ICONE = {c.split(" ",1)[1] if " " in c else c: c.split(" ",1)[0] if " " in c else "Ã°Å¸ÅÂ±"
                 for seg in CULTURAS_POR_SEGMENTO.values() for c in seg}

def get_icone_cultura(cultura):
    """Retorna o ÃÂ­cone da cultura (com ou sem ÃÂ­cone no nome)."""
    if not cultura: return "Ã°Å¸ÅÂ±"
    nome = cultura_limpa(cultura)
    return CULTURA_ICONE.get(nome, "Ã°Å¸ÅÂ±")

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# CONTROLE DE PLANOS Ã¢â¬â Free / Pro / Premium
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬

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
    """Banner de upgrade quando limite ÃÂ© atingido."""
    plano_key = st.session_state.get("sb_plano", "free")
    nomes     = {"areas": "ÃÂ¡reas", "estoque": "itens de estoque"}
    nome      = nomes.get(recurso, recurso)

    # PrÃÂ³ximo plano sugerido
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
    <b style='color:#fbbf24;font-size:16px;'>Ã°Å¸ââ Limite atingido Ã¢â¬â {usado}/{limite} {nome}</b><br>
    <span style='color:#fde68a;font-size:13px;'>
    FaÃÂ§a upgrade para continuar usando o IAAGRO sem limites!
    </span><br><br>
    <span style='color:#fff;font-size:18px;font-weight:800;'>
    {prox_nome} Ã¢â¬â R$ {prox_preco:.2f}/mÃÂªs
    </span>
    </div>
    """, unsafe_allow_html=True)

    msg = f"Quero+assinar+o+IAAGRO+{prox_nome.replace(' ','+')}+-+R$+{prox_preco:.2f}/mes"
    # Links direto do Mercado Pago Ã¢â¬â mensal e anual
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
    Ã°Å¸âÂ³ Mensal<br>R$ {prox_preco:.2f}/mÃÂªs
    </a>
    <a href='{link_ano}' target='_blank'
       style='flex:1;display:block;background:#00a650;color:#fff;text-align:center;
       padding:10px;border-radius:8px;font-weight:700;text-decoration:none;font-size:13px;'>
    Ã°Å¸Ââ  Anual<br>R$ {preco_ano:.0f}/ano<br><span style='font-size:10px;'>(-15% desconto)</span>
    </a>
    </div>
    <div style='text-align:center;margin-top:4px;'>
    <span style='color:#94a3b8;font-size:11px;'>PIX Ã¢â¬Â¢ CartÃÂ£o Ã¢â¬Â¢ Boleto Ã¢â¬â Mercado Pago</span>
    </div>
    """, unsafe_allow_html=True)

def get_culturas():
    """Retorna lista de culturas (com ÃÂ­cone) filtrada pelo segmento ativo."""
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
    """Remove ÃÂ­cone do nome da cultura para usar nas lÃÂ³gicas internas."""
    if c and " " in c and len(c.split(" ",1)[0]) <= 2:
        return c.split(" ",1)[1]
    return c

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: INÃÂCIO
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸ÂÂ  InÃÂ­cio":

    # Ã¢ââ¬Ã¢ââ¬ Segmentos disponÃÂ­veis Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
    SEGMENTOS = SEGMENTOS_INFO

    # Ã¢ââ¬Ã¢ââ¬ Tela de seleÃÂ§ÃÂ£o (sÃÂ³ aparece se segmento nÃÂ£o foi escolhido ainda) Ã¢ââ¬Ã¢ââ¬
    if not st.session_state.segmento:
        st.markdown("""
        <div style='text-align:center;padding:30px 0 10px 0;'>
        <span style='font-size:48px;'>Ã°Å¸ÅÂ±</span><br>
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
                    st.success(f"Ã¢Åâ¦ Segmento **{seg}** selecionado! Bem-vindo.")
                    st.rerun()
            with col_desc:
                st.markdown(
                    f"<div style='padding:10px 0;color:#94a3b8;font-size:14px;'>{info['desc']}</div>",
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("Ã¢Å¡â¢Ã¯Â¸Â VocÃÂª pode trocar o segmento a qualquer momento em ConfiguraÃÂ§ÃÂµes.")

    else:
        # Ã¢ââ¬Ã¢ââ¬ Dashboard principal apÃÂ³s segmento selecionado Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        seg_info = SEGMENTOS.get(st.session_state.segmento, {"cor":"#0f3460","borda":"#22c55e","desc":""})

        col_banner, col_trocar = st.columns([5, 1])
        with col_banner:
            st.markdown(f"""
            <div style='background:{seg_info["cor"]};border-radius:12px;padding:14px 20px;
            border-left:5px solid {seg_info["borda"]};margin-bottom:8px;'>
            <span style='font-size:22px;font-weight:800;color:#f1f5f9;'>Ã°Å¸Å¡Å IAAGRO Ã¢â¬â {st.session_state.segmento}</span><br>
            <span style='font-size:13px;color:#94a3b8;'>{seg_info["desc"]}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_trocar:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("Ã°Å¸ââ Trocar\nsegmento", key="btn_trocar_segmento", use_container_width=True):
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
        _bar_ar     = f"{_areas_us}/{_lim_ar}" if _lim_ar != -1 else f"{_areas_us}/Ã¢ËÅ¾"
        _bar_est    = f"{_est_us}/{_lim_est}"  if _lim_est != -1 else f"{_est_us}/Ã¢ËÅ¾"

        st.markdown(f"""
        <div style='background:linear-gradient(135deg,{_plano_info["cor"]},{_plano_info["cor"]}cc);
        border-radius:12px;padding:12px 18px;border:1px solid {_plano_info["borda"]};margin-bottom:12px;'>
        <span style='color:{_plano_info["borda"]};font-weight:800;font-size:15px;'>{_plano_info["nome"]}</span>
        <span style='color:#94a3b8;font-size:12px;float:right;'>
        Ã°Å¸âÂ {_bar_ar} ÃÂ¡reas &nbsp;|&nbsp; Ã°Å¸âÂ¦ {_bar_est} insumos
        </span><br>
        {"<span style='color:#d1fae5;font-size:12px;'>Ã¢Åâ¦ Acesso completo ativo</span>" if _plano_key == "premium" else
         f"<span style='color:#fde68a;font-size:12px;'>Upgrade para mais recursos Ã¢â¬â <b>R$ {PLANOS['pro' if _plano_key=='free' else 'premium']['preco']:.2f}/mÃÂªs</b></span>"}
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
            Ã°Å¸âÂ³ Mensal R$ {_prox['preco']:.2f}
            </a>
            <a href='{_lano}' target='_blank'
            style='flex:1;display:block;background:#00a650;color:#fff;text-align:center;
            padding:8px;border-radius:8px;font-weight:700;text-decoration:none;font-size:12px;'>
            Ã°Å¸Ââ  Anual R$ {_pano:.0f}
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
        col1.metric("Ã°Å¸ÅÂ¾ ÃÂreas",      total_areas)
        col2.metric("Ã°Å¸âÂ¦ Estoque",    total_estoque)
        col3.metric("Ã°Å¸Å¡Å AplicaÃÂ§ÃÂµes", total_aplicacoes)
        col4.metric("Ã°Å¸âÂ ÃÂrea Total", f"{area_total:.1f} ha")

        st.divider()

        col5, col6 = st.columns(2)
        with col5:
            st.subheader("Ã°Å¸âË Produtividade MÃÂ©dia")
            st.metric("MÃÂ©dia", f"{produtividade_media:.1f} sc/ha")
        with col6:
            st.subheader("Ã¢Å¡Â Ã¯Â¸Â Alertas de Estoque")
            estoque_baixo = [i for i in st.session_state.estoque if i.get("Quantidade", 0) < 10]
            if not estoque_baixo:
                st.markdown('<div style="background:#166534;color:#fff;padding:12px 18px;border-radius:10px;font-weight:700;">Ã¢Åâ¦ Nenhum alerta de estoque.</div>', unsafe_allow_html=True)
            else:
                for item in estoque_baixo:
                    nome = item.get("Insumo", item.get("Produto", "Produto"))
                    st.markdown(f'<div style="background:#92400e;color:#fff;padding:10px 16px;border-radius:10px;font-weight:700;margin-bottom:4px;">Ã¢Å¡Â Ã¯Â¸Â {nome} com estoque baixo.</div>', unsafe_allow_html=True)

        st.divider()
        st.subheader("Ã°Å¸ââ¹ Resumo das ÃÂreas")
        if total_areas == 0:
            st.markdown('<div style="background:#1e3a5f;color:#fff;padding:14px 18px;border-radius:10px;font-weight:600;">Ã¢âÂ¹Ã¯Â¸Â Nenhuma ÃÂ¡rea cadastrada. VÃÂ¡ em <b>Cadastro da ÃÂrea</b> para comeÃÂ§ar.</div>', unsafe_allow_html=True)
        else:
            tabela_dashboard = [{
                "Fazenda":    a.get("Fazenda",""),
                "TalhÃÂ£o":     a.get("TalhÃÂ£o",""),
                "Cultura":    a.get("Cultura",""),
                "ÃÂrea ha":    a.get("Hectares",0),
                "Meta sc/ha": a.get("Meta Produtividade",0),
            } for a in st.session_state.areas]
            df_areas = pd.DataFrame(tabela_dashboard)
            st.dataframe(df_areas, use_container_width=True)
            st.divider()
            st.subheader("Ã°Å¸âÅ  Produtividade por TalhÃÂ£o")
            st.bar_chart(df_areas.set_index("TalhÃÂ£o")["Meta sc/ha"])

        if total_estoque > 0:
            df_estoque = pd.DataFrame(st.session_state.estoque)
            if "Insumo" in df_estoque.columns and "Quantidade" in df_estoque.columns:
                st.divider()
                st.subheader("Ã°Å¸âÂ¦ Estoque por Produto")
                st.bar_chart(df_estoque.set_index("Insumo")["Quantidade"])


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: ÃÂREAS CADASTRADAS
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
elif menu == "Ã°Å¸ÅÂ¾ Lavoura":
    _sub_lav = st.tabs(["Ã¢Å¾â¢ Cadastro da ÃÂrea","Ã°Å¸âÂ ÃÂreas Cadastradas","Ã°Å¸âÂºÃ¯Â¸Â Mapa de Fertilidade","Ã°Å¸ÅÂ§Ã¯Â¸Â PluviÃÂ´metro","Ã°Å¸âË HistÃÂ³rico de Produtividade"])

if menu == "Ã°Å¸ÅÂ¾ Lavoura":
  with _sub_lav[1]:
    st.header("ÃÂreas Cadastradas")

    if len(st.session_state.areas) == 0:
        st.markdown('<div style="background:#1e3a5f;color:#ffffff;padding:14px 18px;border-radius:10px;font-weight:600;font-size:15px;border:1px solid #3b82f6;">Ã¢âÂ¹Ã¯Â¸Â Nenhuma ÃÂ¡rea cadastrada ainda.</div>', unsafe_allow_html=True)
    else:
        tabela_areas = pd.DataFrame([
            {
                "ID":               a["ID"],
                "Fazenda":          a["Fazenda"],
                "TalhÃÂ£o":          a["TalhÃÂ£o"],
                "Matricula":        a.get("Matricula", ""),
                "Cidade/Estado":    a["Cidade/Estado"],
                "Hectares":         a["Hectares"],
                "Cultura":          a["Cultura"],
                "Meta Produtividade": a["Meta Produtividade"]
            }
            for a in st.session_state.areas
        ])
        st.dataframe(tabela_areas, use_container_width=True)

        opcoes = [f"{area['ID']} - {area['TalhÃÂ£o']} - {area['Cultura']}" for area in st.session_state.areas]
        escolha = st.selectbox("Selecionar ÃÂ¡rea para trabalhar", opcoes, key="sel_selecionar__rea_2910")

        if st.button("Carregar ÃÂrea Selecionada"):
            indice = opcoes.index(escolha)
            area   = st.session_state.areas[indice]
            st.session_state.id_area          = area["ID"]
            st.session_state.area_selecionada = area["ID"]
            # Carrega dados completos da ÃÂ¡rea (inclui anÃÂ¡lise de solo)
            _dados_area = area.get("Dados", area.get("dados", {}))
            st.session_state.dados = _dados_area.copy() if _dados_area else {}
            if "id_area" not in st.session_state.dados:
                st.session_state.dados["id_area"] = area["ID"]
            # Garante que campos da ÃÂ¡rea estejam nos dados
            st.session_state.dados.update({
                "cultura":       area.get("Cultura", st.session_state.dados.get("cultura","Soja")),
                "area":          area.get("Hectares", st.session_state.dados.get("area",0)),
                "produtividade": area.get("Produtividade", st.session_state.dados.get("produtividade",50)),
                "fazenda":       area.get("Fazenda", st.session_state.dados.get("fazenda","")),
                "talhao":        area.get("TalhÃÂ£o", st.session_state.dados.get("talhao","")),
            })
            st.session_state.aplicacoes = area.get("Aplicacoes", []).copy()
            st.session_state.estoque    = area.get("Estoque", []).copy()
            salvar_dados_iaagro()
            success_box(f"Ã¢Åâ¦ ÃÂrea {area['ID']} carregada! {('AnÃÂ¡lise de solo disponÃÂ­vel Ã¢Åâ¦' if 'ph' in st.session_state.dados else 'Sem anÃÂ¡lise de solo ainda.')}")
            st.rerun()

        st.divider()
        st.subheader("Excluir ÃÂrea Individual")
        opcao_excluir = st.selectbox(
            "Escolha a ÃÂ¡rea para excluir",
            [f"{area['ID']} - {area['TalhÃÂ£o']} - {area['Cultura']}" for area in st.session_state.areas],
            key="excluir_area_select"
        )
        if st.button("Excluir ÃÂrea Selecionada", key="excluir_area_btn"):
            indice_excluir = [
                f"{area['ID']} - {area['TalhÃÂ£o']} - {area['Cultura']}"
                for area in st.session_state.areas
            ].index(opcao_excluir)
            area_excluida = st.session_state.areas[indice_excluir]["ID"]
            st.session_state.areas.pop(indice_excluir)
            if st.session_state.area_selecionada == area_excluida:
                st.session_state.area_selecionada = None
                st.session_state.dados = {}
            salvar_dados_iaagro()
            success_box(f"ÃÂrea {area_excluida} excluÃÂ­da com sucesso.")
            st.rerun()

        if st.button("Apagar Todas as ÃÂreas"):
            st.session_state.areas = []
            st.session_state.dados = {}
            st.session_state.area_selecionada = None
            salvar_dados_iaagro()
            warning_box("Todas as ÃÂ¡reas foram apagadas.")

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: CADASTRO DA ÃÂREA
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸ÅÂ¾ Lavoura":
  with _sub_lav[0]:
    st.header("Cadastro da ÃÂrea")

    fazenda   = st.text_input("Nome da fazenda",  st.session_state.dados.get("fazenda", ""), key="txt_nome_da_fazenda_2960")
    talhao    = st.text_input("Nome do talhÃÂ£o",   st.session_state.dados.get("talhao", ""), key="txt_nome_do_talh_o_2961")
    matricula = st.text_input("MatrÃÂ­cula da ÃÂrea", st.session_state.dados.get("matricula", ""), key="txt_matr_cula_da__r_2962")
    cidade    = st.text_input("Cidade / Estado",   st.session_state.dados.get("cidade", ""), key="txt_cidade___estado_2963")
    area      = st.number_input("ÃÂrea do talhÃÂ£o em hectares", min_value=0.0,
                                value=float(st.session_state.dados.get("area", 10.0)))

    culturas_disponiveis = get_culturas()
    config_culturas = {
        "Soja":          {"ph_ideal":"5.8 - 6.5","chuva_ideal":"450 - 800 mm","produtividade_media":65,"nutriente_principal":"PotÃÂ¡ssio"},
        "Milho":         {"ph_ideal":"5.5 - 6.8","chuva_ideal":"500 - 800 mm","produtividade_media":180,"nutriente_principal":"NitrogÃÂªnio"},
        "Trigo":         {"ph_ideal":"5.5 - 6.2","chuva_ideal":"350 - 600 mm","produtividade_media":55,"nutriente_principal":"NitrogÃÂªnio"},
        "FeijÃÂ£o":        {"ph_ideal":"5.8 - 6.5","chuva_ideal":"300 - 500 mm","produtividade_media":45,"nutriente_principal":"FÃÂ³sforo"},
        "Canola":        {"ph_ideal":"5.5 - 6.2","chuva_ideal":"400 - 700 mm","produtividade_media":40,"nutriente_principal":"Enxofre"},
        "Aveia":         {"ph_ideal":"5.2 - 6.0","chuva_ideal":"300 - 550 mm","produtividade_media":70,"nutriente_principal":"NitrogÃÂªnio"},
        "Cana-de-aÃÂ§ÃÂºcar":{"ph_ideal":"5.5 - 6.5","chuva_ideal":"1200 - 1800 mm","produtividade_media":90,"nutriente_principal":"PotÃÂ¡ssio"},
        "Arroz":         {"ph_ideal":"5.0 - 6.0","chuva_ideal":"900 - 1300 mm","produtividade_media":160,"nutriente_principal":"NitrogÃÂªnio"},
        "Sorgo":         {"ph_ideal":"5.5 - 6.5","chuva_ideal":"350 - 650 mm","produtividade_media":120,"nutriente_principal":"NitrogÃÂªnio"},
        "Girassol":      {"ph_ideal":"5.5 - 6.8","chuva_ideal":"400 - 700 mm","produtividade_media":35,"nutriente_principal":"Boro"},
        "Cevada":        {"ph_ideal":"5.5 - 6.5","chuva_ideal":"350 - 600 mm","produtividade_media":60,"nutriente_principal":"NitrogÃÂªnio"},
        "Pastagem":      {"ph_ideal":"5.0 - 6.5","chuva_ideal":"500 - 1200 mm","produtividade_media":0,"nutriente_principal":"NitrogÃÂªnio"},
        "AlgodÃÂ£o":       {"ph_ideal":"5.5 - 6.5","chuva_ideal":"700 - 1300 mm","produtividade_media":300,"nutriente_principal":"PotÃÂ¡ssio"},
        "CafÃÂ©":          {"ph_ideal":"5.5 - 6.5","chuva_ideal":"1200 - 1800 mm","produtividade_media":35,"nutriente_principal":"NitrogÃÂªnio"},
        "Tabaco":        {"ph_ideal":"5.2 - 6.2","chuva_ideal":"600 - 1000 mm","produtividade_media":2500,"nutriente_principal":"PotÃÂ¡ssio"},
        "Mandioca":      {"ph_ideal":"5.0 - 6.5","chuva_ideal":"800 - 1500 mm","produtividade_media":25,"nutriente_principal":"PotÃÂ¡ssio"},
        "Batata":        {"ph_ideal":"5.0 - 6.0","chuva_ideal":"500 - 700 mm","produtividade_media":35,"nutriente_principal":"PotÃÂ¡ssio"},
        "Tomate":        {"ph_ideal":"5.5 - 6.8","chuva_ideal":"400 - 800 mm","produtividade_media":80,"nutriente_principal":"PotÃÂ¡ssio"},
        "Cebola":        {"ph_ideal":"6.0 - 6.8","chuva_ideal":"350 - 650 mm","produtividade_media":40,"nutriente_principal":"PotÃÂ¡ssio"},
        "Alho":          {"ph_ideal":"6.0 - 7.0","chuva_ideal":"300 - 500 mm","produtividade_media":12,"nutriente_principal":"Enxofre"},
        "Uva":           {"ph_ideal":"5.5 - 6.5","chuva_ideal":"500 - 900 mm","produtividade_media":25,"nutriente_principal":"PotÃÂ¡ssio"},
        "MaÃÂ§ÃÂ£":          {"ph_ideal":"5.5 - 6.5","chuva_ideal":"700 - 1200 mm","produtividade_media":45,"nutriente_principal":"CÃÂ¡lcio"},
        "Laranja":       {"ph_ideal":"5.5 - 6.5","chuva_ideal":"1000 - 1500 mm","produtividade_media":35,"nutriente_principal":"PotÃÂ¡ssio"},
        "Banana":        {"ph_ideal":"5.5 - 7.0","chuva_ideal":"1200 - 2000 mm","produtividade_media":45,"nutriente_principal":"PotÃÂ¡ssio"},
        "Eucalipto":     {"ph_ideal":"5.0 - 6.5","chuva_ideal":"800 - 1500 mm","produtividade_media":40,"nutriente_principal":"FÃÂ³sforo"},
        "Pinus":         {"ph_ideal":"4.5 - 6.0","chuva_ideal":"700 - 1400 mm","produtividade_media":35,"nutriente_principal":"FÃÂ³sforo"},
    }

    cultura_atual = st.session_state.dados.get("cultura", "Soja")
    idx_cultura   = culturas_disponiveis.index(cultura_atual) if cultura_atual in culturas_disponiveis else 0
    cultura       = st.selectbox("Cultura", culturas_disponiveis, index=idx_cultura, key="cultura_area")

    info = config_culturas.get(cultura, {"ph_ideal":"NÃÂ£o definido","chuva_ideal":"NÃÂ£o definido","produtividade_media":0,"nutriente_principal":"NÃÂ£o definido"})
    st.markdown(f"""
    <div style="background:#0f3460;color:#ffffff;padding:14px 18px;border-radius:12px;
                border:1px solid #3b82f6;font-size:15px;font-weight:600;line-height:2;">
        Ã°Å¸ÅÂ± <b>Cultura:</b> {cultura} &nbsp;|&nbsp;
        Ã°Å¸Â§Âª <b>pH ideal:</b> {info['ph_ideal']} &nbsp;|&nbsp;
        Ã°Å¸ÅÂ§Ã¯Â¸Â <b>Chuva ideal:</b> {info['chuva_ideal']}<br>
        Ã°Å¸âË <b>Produtividade mÃÂ©dia:</b> {info['produtividade_media']} &nbsp;|&nbsp;
        Ã°Å¸Â§Â¬ <b>Nutriente principal:</b> {info['nutriente_principal']}
    </div>
    """, unsafe_allow_html=True)

    produtividade = st.number_input("Meta de produtividade em sacas/ha", min_value=0.0,
                                    value=float(st.session_state.dados.get("produtividade", 60.0)))

    # Ã¢ââ¬Ã¢ââ¬ GeolocalizaÃÂ§ÃÂ£o com tratamento robusto Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
    # Inicializa com coordenadas salvas ou padrÃÂ£o Brasil-Sul
    latitude  = st.session_state.dados.get("latitude",  -26.88)
    longitude = st.session_state.dados.get("longitude", -52.40)

    col_geo_a, col_geo_b = st.columns([2, 1])
    with col_geo_a:
        latitude  = st.number_input("Ã°Å¸âÂ Latitude",  value=float(latitude),
                                     format="%.6f", key="cad_lat")
        longitude = st.number_input("Ã°Å¸âÂ Longitude", value=float(longitude),
                                     format="%.6f", key="cad_lon")
    with col_geo_b:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Ã°Å¸âÂ¡ Usar GPS do celular", key="btn_gps_cad", use_container_width=True):
            try:
                geo = get_geolocation()
                if geo and geo.get("coords"):
                    st.session_state["_gps_lat"] = geo["coords"]["latitude"]
                    st.session_state["_gps_lon"] = geo["coords"]["longitude"]
                    st.rerun()
            except Exception:
                warning_box("GPS indisponÃÂ­vel. Insira as coordenadas manualmente.")
        if st.session_state.get("_gps_lat"):
            latitude  = st.session_state["_gps_lat"]
            longitude = st.session_state["_gps_lon"]
            st.markdown(f'<div style="background:#14532d;color:#fff;padding:6px 10px;'
                        f'border-radius:8px;font-size:11px;font-weight:700;">'
                        f'Ã¢Åâ¦ GPS: {latitude:.5f}, {longitude:.5f}</div>',
                        unsafe_allow_html=True)
        st.markdown('<div style="color:#94a3b8;font-size:11px;margin-top:4px;">'
                    'Dica: use Google Maps para obter as coordenadas da ÃÂ¡rea.</div>',
                    unsafe_allow_html=True)

    pode, usado, limite = verificar_limite("areas")
    if not pode:
        bloco_upgrade("areas", usado, limite)
    elif st.button("Salvar Nova ÃÂrea"):
        id_area  = f"AREA-{st.session_state.contador_area:03d}"
        nova_area = {
            "ID": id_area,
            "Fazenda": fazenda, "TalhÃÂ£o": talhao, "Matricula": matricula,
            "Cidade/Estado": cidade, "Hectares": area,
            "Latitude": latitude, "Longitude": longitude,
            "Cultura": cultura, "Meta Produtividade": produtividade,
            "pH":              st.session_state.dados.get("ph", 0),
            "FÃÂ³sforo":         st.session_state.dados.get("fosforo", 0),
            "PotÃÂ¡ssio":        st.session_state.dados.get("potassio", 0),
            "MatÃÂ©ria OrgÃÂ¢nica": st.session_state.dados.get("materia_organica", 0),
            "SaturaÃÂ§ÃÂ£o Base":  st.session_state.dados.get("saturacao_bases", 0),
            "CalcÃÂ¡rio t/ha":   st.session_state.dados.get("dose_calcario", 0),
            "Gesso t/ha":      st.session_state.dados.get("dose_gesso", 0),
            "Prioridade":      st.session_state.dados.get("prioridade", "MÃÂ©dia"),
            "Zona":            st.session_state.dados.get("zona_produtividade", "MÃÂ©dia"),
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
        success_box(f"ÃÂrea cadastrada com sucesso. ID gerado: {id_area}")

    if st.session_state.area_selecionada:
        if st.button("Atualizar ÃÂrea Ativa"):
            st.session_state.dados.update({
                "fazenda": fazenda, "talhao": talhao, "cidade": cidade,
                "area": area, "cultura": cultura, "produtividade": produtividade
            })
            for a in st.session_state.areas:
                if a["ID"] == st.session_state.area_selecionada:
                    a["Fazenda"] = fazenda; a["TalhÃÂ£o"] = talhao
                    a["Cidade/Estado"] = cidade; a["Hectares"] = area
                    a["Cultura"] = cultura; a["Meta Produtividade"] = produtividade
                    a["Dados"] = st.session_state.dados.copy()
            salvar_dados_iaagro()
            success_box("ÃÂrea ativa atualizada com sucesso.")

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: HISTÃâRICO DE PRODUTIVIDADE
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸ÅÂ¾ Lavoura":
  with _sub_lav[4]:
    st.header("Ã°Å¸âË HistÃÂ³rico de Produtividade")

    if len(st.session_state.areas) == 0:
        warning_box("Cadastre uma ÃÂ¡rea primeiro.")
    else:
        lista_areas        = [f"{a['ID']} - {a['TalhÃÂ£o']}" for a in st.session_state.areas]
        area_escolhida     = st.selectbox("Selecione a ÃÂrea", lista_areas, key="sel_selecione_a__re_3106")
        safra              = st.text_input("Safra", placeholder="2024/2025", key="txt_safra_3107")

        # Cultura colhida Ã¢â¬â com ÃÂ­cones
        _culturas_hist = get_culturas()
        # Pega cultura da ÃÂ¡rea selecionada como padrÃÂ£o
        _id_hist = area_escolhida.split(" - ")[0]
        _area_hist_obj = next((a for a in st.session_state.areas if a.get("ID") == _id_hist), None)
        _cult_padrao = _area_hist_obj.get("Cultura", _culturas_hist[0]) if _area_hist_obj else _culturas_hist[0]
        _idx_cult = _culturas_hist.index(_cult_padrao) if _cult_padrao in _culturas_hist else 0
        cultura_colhida = st.selectbox("Cultura colhida", _culturas_hist,
                                        index=_idx_cult, key="sel_cultura_hist")

        produtividade_real = st.number_input("Produtividade Real (sc/ha)", min_value=0.0, value=60.0, key="num_produtividade_r_3108")
        custo_total        = st.number_input("Custo Total por hectare (R$)", min_value=0.0, value=0.0, key="num_custo_total_por_3109")
        observacoes        = st.text_area("ObservaÃÂ§ÃÂµes da Safra", key="txa_observa__es_da__3110")

        if st.button("Ã°Å¸âÂ¾ Salvar HistÃÂ³rico", key="btn_salvar_hist", use_container_width=True):
            st.session_state.historico_produtividade.append({
                "ÃÂrea": area_escolhida, "Safra": safra,
                "Cultura": cultura_colhida,
                "Produtividade": produtividade_real,
                "Custo": custo_total, "ObservaÃÂ§ÃÂµes": observacoes
            })
            salvar_dados_iaagro()
            success_box(f"HistÃÂ³rico salvo! {get_icone_cultura(cultura_colhida)} {cultura_limpa(cultura_colhida)} Ã¢â¬â {produtividade_real} sc/ha")
            st.rerun()

        if len(st.session_state.historico_produtividade) > 0:
            df_hist = pd.DataFrame(st.session_state.historico_produtividade)
            if "Cultura" not in df_hist.columns:
                df_hist["Cultura"] = "Ã¢â¬â"

            # Ã¢ââ¬Ã¢ââ¬ BotÃÂ£o atualizar registro Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
            st.divider()
            st.subheader("Ã¢ÅÂÃ¯Â¸Â Atualizar Registro")
            _opcoes_hist = [
                f"{i+1}. {r.get('ÃÂrea','')} | {r.get('Safra','')} | {cultura_limpa(r.get('Cultura',''))} | {r.get('Produtividade',0)} sc/ha"
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
                _obs_e    = st.text_area("ObservaÃÂ§ÃÂµes", value=_reg_edit.get("ObservaÃÂ§ÃÂµes",""),
                                          key="txt_hist_obs_edit", height=100)

            col_btn1, col_btn2 = st.columns(2)
            if col_btn1.button("Ã°Å¸âÂ¾ Atualizar Registro", key="btn_hist_atualizar", use_container_width=True):
                st.session_state.historico_produtividade[_idx_edit] = {
                    "ÃÂrea":          _reg_edit.get("ÃÂrea",""),
                    "Safra":         _safra_e,
                    "Cultura":       _cult_e,
                    "Produtividade": _prod_e,
                    "Custo":         _custo_e,
                    "ObservaÃÂ§ÃÂµes":   _obs_e,
                }
                salvar_dados_iaagro()
                success_box("Ã¢Åâ¦ Registro atualizado!")
                st.rerun()

            if col_btn2.button("Ã°Å¸ââÃ¯Â¸Â Excluir Registro", key="btn_hist_excluir", use_container_width=True):
                st.session_state.historico_produtividade.pop(_idx_edit)
                salvar_dados_iaagro()
                success_box("Registro excluÃÂ­do!")
                st.rerun()

            # Ã¢ââ¬Ã¢ââ¬ Tabela e grÃÂ¡fico Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
            st.divider()
            st.subheader("Ã°Å¸ââ¹ Todos os Registros")
            st.dataframe(df_hist, use_container_width=True)
            st.subheader("Ã°Å¸âÅ  EvoluÃÂ§ÃÂ£o Produtiva")
            area_filtro = st.selectbox("Filtrar grÃÂ¡fico por ÃÂ¡rea", df_hist["ÃÂrea"].unique(), key="sel_filtrar_gr_fico_3125")
            df_area     = df_hist[df_hist["ÃÂrea"] == area_filtro]
            grafico     = df_area.pivot_table(index="Safra", values="Produtividade", aggfunc="mean")
            st.line_chart(grafico)
            media_prod  = df_hist["Produtividade"].mean()
            melhor_prod = df_hist["Produtividade"].max()
            custo_medio = df_hist["Custo"].mean()
            col1, col2, col3 = st.columns(3)
            col1.metric("Ã°Å¸âË MÃÂ©dia Produtiva", f"{media_prod:.1f} sc/ha")
            col2.metric("Ã°Å¸Ââ  Melhor Safra",    f"{melhor_prod:.1f} sc/ha")
            col3.metric("Ã°Å¸âÂ° Custo MÃÂ©dio",      f"R$ {custo_medio:.2f}")


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: PLUVIÃâMETRO
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸ÅÂ¾ Lavoura":
  with _sub_lav[3]:
    st.header("Ã°Å¸ÅÂ§Ã¯Â¸Â PluviÃÂ´metro Inteligente")

    if len(st.session_state.areas) == 0:
        warning_box("Cadastre uma ÃÂ¡rea primeiro.")
    else:
        lista_areas   = [f"{a['ID']} - {a['TalhÃÂ£o']}" for a in st.session_state.areas]
        area_chuva    = st.selectbox("Selecione a ÃÂrea", lista_areas, key="sel_area_chuva_pluvio")
        id_area_chuva = area_chuva.split(" - ")[0]
        area_obj      = next((a for a in st.session_state.areas if a["ID"] == id_area_chuva), {})
        cultura_chuva = area_obj.get("Cultura", "Soja")

        chuva_ideal_padrao = {
            "Soja":120.0,"Milho":140.0,"Trigo":90.0,"FeijÃÂ£o":100.0,"Canola":90.0,
            "Aveia":80.0,"Cana-de-aÃÂ§ÃÂºcar":180.0,"Arroz":180.0,"Sorgo":90.0,
            "Girassol":90.0,"Cevada":80.0,"Pastagem":120.0,"AlgodÃÂ£o":130.0,
            "CafÃÂ©":140.0,"Tabaco":110.0,"Mandioca":100.0,"Batata":100.0,
        }
        chuva_ideal_mes = chuva_ideal_padrao.get(cultura_limpa(cultura_chuva), 120.0)

        st.markdown(f"""
        <div style='background:#0f3460;color:#fff;padding:10px 16px;border-radius:8px;
        border:1px solid #3b82f6;margin-bottom:12px;'>
        Ã°Å¸ÅÂ± <b>Cultura:</b> {cultura_chuva} &nbsp;|&nbsp;
        Ã°Å¸ÅÂ§Ã¯Â¸Â <b>Chuva ideal/mÃÂªs:</b> {chuva_ideal_mes} mm
        </div>
        """, unsafe_allow_html=True)

        # Ã¢ââ¬Ã¢ââ¬ Registro diÃÂ¡rio Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        st.subheader("Ã¢Å¾â¢ Registrar Chuva DiÃÂ¡ria")
        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            data_chuva = st.date_input("Data", value=datetime.now().date(), key="date_chuva_diaria")
        with col_d2:
            mm_dia = st.number_input("PrecipitaÃÂ§ÃÂ£o (mm)", min_value=0.0, max_value=500.0,
                                      value=0.0, step=0.1, key="num_mm_dia",
                                      help="Leitura do pluviÃÂ´metro de campo")
        with col_d3:
            obs_dia = st.text_input("ObservaÃÂ§ÃÂ£o", placeholder="Ex: Chuva forte tarde",
                                     key="txt_obs_chuva")

        if st.button("Ã°Å¸âÂ¾ Registrar", key="btn_reg_chuva", use_container_width=True):
            if mm_dia > 0 or obs_dia:
                _reg = {
                    "area_id":  id_area_chuva,
                    "area":     area_chuva,
                    "data":     str(data_chuva),
                    "ano":      data_chuva.year,
                    "mes":      data_chuva.month,
                    "mes_nome": ["","Janeiro","Fevereiro","MarÃÂ§o","Abril","Maio","Junho",
                                 "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"][data_chuva.month],
                    "mm":       round(mm_dia, 1),
                    "obs":      obs_dia,
                }
                st.session_state.pluviometro.append(_reg)
                salvar_dados_iaagro()
                success_box(f"Ã¢Åâ¦ {mm_dia} mm registrado em {data_chuva.strftime('%d/%m/%Y')}")
            else:
                warning_box("Digite a quantidade de chuva.")

        # Ã¢ââ¬Ã¢ââ¬ Filtro e acumulado mensal Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        _regs = [r for r in st.session_state.pluviometro
                 if isinstance(r, dict) and r.get("area_id") == id_area_chuva]

        if _regs:
            import pandas as pd
            df_pluvio = pd.DataFrame(_regs)

            # Garante colunas necessÃÂ¡rias
            for col in ["data","ano","mes","mes_nome","mm"]:
                if col not in df_pluvio.columns:
                    df_pluvio[col] = 0 if col in ["ano","mes","mm"] else ""

            df_pluvio["mm"] = pd.to_numeric(df_pluvio["mm"], errors="coerce").fillna(0)
            df_pluvio["data_dt"] = pd.to_datetime(df_pluvio["data"], errors="coerce")
            df_pluvio = df_pluvio.sort_values("data_dt", ascending=False)

            # Ã¢ââ¬Ã¢ââ¬ Acumulado mensal automÃÂ¡tico Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
            st.subheader("Ã°Å¸âÅ  Acumulado Mensal")
            df_mensal = (df_pluvio.groupby(["ano","mes","mes_nome"])["mm"]
                         .sum().reset_index()
                         .sort_values(["ano","mes"]))
            df_mensal["ideal"] = chuva_ideal_mes
            df_mensal["%ideal"] = (df_mensal["mm"] / chuva_ideal_mes * 100).round(1)
            df_mensal["status"] = df_mensal["%ideal"].apply(
                lambda x: "Ã¢Åâ¦ Adequado" if 70<=x<=130
                else ("Ã¢Å¡Â Ã¯Â¸Â DÃÂ©ficit" if x < 70 else "Ã¢Å¡Â Ã¯Â¸Â Excesso")
            )
            df_mensal["PerÃÂ­odo"] = df_mensal["mes_nome"].astype(str) + "/" + df_mensal["ano"].astype(str)

            # Cards dos ÃÂºltimos 3 meses
            _ultimos = df_mensal.tail(3).to_dict("records")
            cols_m = st.columns(len(_ultimos))
            for idx_m, row in enumerate(_ultimos):
                _cor = "#14532d" if "Adequado" in row["status"] else "#78350f"
                cols_m[idx_m].markdown(f"""
                <div style='background:{_cor};border-radius:10px;padding:12px;text-align:center;'>
                <b style='color:#fff;font-size:13px;'>{row['PerÃÂ­odo']}</b><br>
                <span style='color:#fff;font-size:22px;font-weight:800;'>{row['mm']:.1f} mm</span><br>
                <span style='color:#d1fae5;font-size:11px;'>{row['%ideal']}% do ideal</span><br>
                <span style='color:#fde68a;font-size:11px;'>{row['status']}</span>
                </div>
                """, unsafe_allow_html=True)

            # GrÃÂ¡fico acumulado mensal
            if len(df_mensal) > 0:
                st.markdown("**Chuva acumulada vs ideal por mÃÂªs:**")
                _chart_data = df_mensal.set_index("PerÃÂ­odo")[["mm","ideal"]]
                _chart_data.columns = ["Chuva Real (mm)","Ideal (mm)"]
                st.bar_chart(_chart_data)

            # Ã¢ââ¬Ã¢ââ¬ Registros diÃÂ¡rios Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
            st.subheader("Ã°Å¸ââ¹ Registros DiÃÂ¡rios")

            # Filtro por mÃÂªs/ano
            _anos  = sorted(df_pluvio["ano"].dropna().unique().tolist(), reverse=True)
            _meses_nomes = ["Todos","Janeiro","Fevereiro","MarÃÂ§o","Abril","Maio","Junho",
                            "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
            col_f1, col_f2 = st.columns(2)
            _ano_sel = col_f1.selectbox("Filtrar ano", ["Todos"] + [str(int(a)) for a in _anos], key="sel_ano_pluvio")
            _mes_sel = col_f2.selectbox("Filtrar mÃÂªs", _meses_nomes, key="sel_mes_pluvio")

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
            col_r1.metric("Ã°Å¸ÅÂ§Ã¯Â¸Â Total", f"{_total_filtro:.1f} mm")
            col_r2.metric("Ã°Å¸ââ¦ Dias c/ chuva", f"{_dias_chuva}")
            col_r3.metric("Ã°Å¸âÅ  MÃÂ©dia/dia", f"{_media_dia:.1f} mm")
            col_r4.metric("Ã°Å¸Å½Â¯ % do ideal", f"{_total_filtro/chuva_ideal_mes*100:.0f}%" if _mes_sel != "Todos" else "-")

            # Tabela diÃÂ¡ria
            _cols_exib = ["data","mm","obs"] if "obs" in df_filtrado.columns else ["data","mm"]
            _df_show = df_filtrado[_cols_exib].copy()
            _df_show.columns = ["Data","mm","Obs"] if len(_cols_exib) == 3 else ["Data","mm"]
            st.dataframe(_df_show.head(60), use_container_width=True)

            # Excluir registro
            with st.expander("Ã°Å¸ââÃ¯Â¸Â Excluir registro"):
                _datas_disp = df_pluvio["data"].tolist()
                if _datas_disp:
                    _data_del = st.selectbox("Selecione a data para excluir",
                                              _datas_disp, key="sel_del_chuva")
                    if st.button("Ã°Å¸ââÃ¯Â¸Â Excluir", key="btn_del_chuva"):
                        st.session_state.pluviometro = [
                            r for r in st.session_state.pluviometro
                            if not (isinstance(r, dict) and
                                    r.get("data") == _data_del and
                                    r.get("area_id") == id_area_chuva)
                        ]
                        salvar_dados_iaagro()
                        success_box("Registro excluÃÂ­do!")
                        st.rerun()

            # Ã¢ââ¬Ã¢ââ¬ AnÃÂ¡lise de risco Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
            st.subheader("Ã°Å¸Â¤â AnÃÂ¡lise de Risco HÃÂ­drico")
            _mensal_recente = df_mensal.tail(3)["mm"].tolist()
            _media_3m = sum(_mensal_recente)/len(_mensal_recente) if _mensal_recente else 0
            _desvio   = abs(_media_3m - chuva_ideal_mes) / chuva_ideal_mes * 100 if chuva_ideal_mes > 0 else 0

            # Estimativa de perda por dÃÂ©ficit ou excesso (igual ao modelo anterior)
            if _media_3m < chuva_ideal_mes * 0.7:
                _perda_est = round((_chuva_ideal_mes - _media_3m) * 0.15, 1) if hasattr(locals(), '_chuva_ideal_mes') else round((chuva_ideal_mes - _media_3m) * 0.15, 1)
                _perda_est = round((chuva_ideal_mes - _media_3m) * 0.15, 1)
                _status_h  = "Ã¢Å¡Â Ã¯Â¸Â DÃÂ©ficit hÃÂ­drico"
                _risco     = "Ã°Å¸âÂ´ Alto risco hÃÂ­drico Ã¢â¬â avaliar seguro agrÃÂ­cola"
                _rec       = f"DÃÂ©ficit mÃÂ©dio de {chuva_ideal_mes - _media_3m:.0f} mm/mÃÂªs. Perda estimada: {_perda_est}%. Reavaliar meta produtiva."
            elif _media_3m > chuva_ideal_mes * 1.3:
                _perda_est = round((_media_3m - chuva_ideal_mes) * 0.08, 1)
                _status_h  = "Ã¢Å¡Â Ã¯Â¸Â Excesso de chuva"
                _risco     = "Ã°Å¸Å¸Â¡ Risco por excesso hÃÂ­drico"
                _rec       = f"Excesso mÃÂ©dio de {_media_3m - chuva_ideal_mes:.0f} mm/mÃÂªs. Perda estimada: {_perda_est}%. Monitorar doenÃÂ§as fÃÂºngicas e erosÃÂ£o."
            else:
                _perda_est = 0
                _status_h  = "Ã¢Åâ¦ Chuva adequada"
                _risco     = "Ã°Å¸Å¸Â¢ CondiÃÂ§ÃÂ£o hÃÂ­drica adequada"
                _rec       = "PrecipitaÃÂ§ÃÂ£o dentro da faixa ideal para a cultura."

            # MÃÂ©tricas de risco
            _col_r1, _col_r2, _col_r3 = st.columns(3)
            _col_r1.metric("Ã°Å¸ÅÂ§Ã¯Â¸Â MÃÂ©dia 3 meses", f"{_media_3m:.1f} mm")
            _col_r2.metric("Ã°Å¸Å½Â¯ Ideal/mÃÂªs", f"{chuva_ideal_mes} mm")
            _col_r3.metric("Ã°Å¸ââ° Perda estimada", f"{_perda_est}%",
                           help="Estimativa de impacto na produtividade por dÃÂ©ficit ou excesso hÃÂ­drico")

            info_box(_risco)
            st.caption(_rec)

            # Progresso do mÃÂªs atual
            _hoje = datetime.now()
            _regs_mes_atual = [r for r in _regs
                               if isinstance(r, dict)
                               and r.get("mes") == _hoje.month
                               and r.get("ano") == _hoje.year]
            _total_mes_atual = sum(r.get("mm", 0) for r in _regs_mes_atual)
            _pct_mes = min(_total_mes_atual / chuva_ideal_mes, 1.0) if chuva_ideal_mes > 0 else 0

            st.subheader(f"Ã°Å¸ââ¦ {['','Janeiro','Fevereiro','MarÃÂ§o','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'][_hoje.month]}/{_hoje.year} Ã¢â¬â Progresso")
            st.progress(_pct_mes)
            st.caption(f"{_total_mes_atual:.1f} mm acumulados de {chuva_ideal_mes} mm ideais ({_pct_mes*100:.0f}%)")

        else:
            st.info("Ã°Å¸âÂ Nenhum registro de chuva para esta ÃÂ¡rea ainda. Registre a primeira leitura acima!")




# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: MAPA DE FERTILIDADE
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸ÅÂ¾ Lavoura":
  with _sub_lav[2]:
    st.header("Ã°Å¸âÂºÃ¯Â¸Â Mapa de Fertilidade por Cores")
    st.subheader("Ã°Å¸ÅÂ¦Ã¯Â¸Â Mapa ClimÃÂ¡tico dos TalhÃÂµes")

    if len(st.session_state.areas) == 0:
        st.markdown('<div style="background:#1e3a5f;color:#ffffff;padding:14px 18px;border-radius:10px;font-weight:600;font-size:15px;border:1px solid #3b82f6;">Ã¢âÂ¹Ã¯Â¸Â Nenhuma ÃÂ¡rea cadastrada.</div>', unsafe_allow_html=True)
    else:
        mapa_dados = []
        for area in st.session_state.areas:
            dados_area = area.get("Dados", area.get("dados", {}))
            media_hist = 0
            historicos_area = [h for h in st.session_state.historico_produtividade if h["ÃÂrea"].startswith(area["ID"])]
            if len(historicos_area) > 0:
                media_hist = sum(h["Produtividade"] for h in historicos_area) / len(historicos_area)

            # Ã¢ââ¬Ã¢ââ¬ Dados de calcÃÂ¡rio e gesso aplicados Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
            _corr       = st.session_state.get("corretivos_aplicados", [])
            _calc_area  = [c for c in _corr if isinstance(c,dict) and c.get("area_id")==area.get("ID","") and c.get("tipo")=="calcario"]
            _gesso_area = [c for c in _corr if isinstance(c,dict) and c.get("area_id")==area.get("ID","") and c.get("tipo")=="gesso"]
            _calc_total  = round(sum(c.get("toneladas_ha",0) for c in _calc_area), 2)
            _gesso_total = round(sum(c.get("toneladas_ha",0) for c in _gesso_area), 2)

            # Usa pH pÃÂ³s-calagem no score se calcÃÂ¡rio foi aplicado
            _dados_score = dados_area.copy() if dados_area else {}
            _ph_orig     = _dados_score.get("ph", 0)
            _ph_corrigido = _dados_score.get("ph_pos_calagem", _ph_orig)

            # Se tem calcÃÂ¡rio mas ph_pos_calagem nÃÂ£o foi calculado ainda, calcula agora
            if _calc_total > 0 and _ph_corrigido == _ph_orig and _ph_orig > 0:
                _elevacao_total = round((_calc_total * 0.75) * 0.3, 2)
                _ph_corrigido   = min(round(_ph_orig + _elevacao_total, 1), 7.0)
                _dados_score["ph_pos_calagem"] = _ph_corrigido

            # Usa pH corrigido no score visual
            if _calc_total > 0 and _ph_corrigido > _ph_orig:
                _dados_score["ph"] = _ph_corrigido  # score usa pH pÃÂ³s-calagem

            if _dados_score and "ph" in _dados_score:
                score, classe, alertas = score_solo(_dados_score)
            else:
                score = 0; classe = "Sem anÃÂ¡lise"; alertas = ["Sem anÃÂ¡lise de solo"]

            if   score >= 85: cor = "Ã°Å¸Å¸Â¢ Verde"
            elif score >= 70: cor = "Ã°Å¸Å¸Â¡ Amarelo"
            elif score >= 50: cor = "Ã°Å¸Å¸Â  Laranja"
            else:             cor = "Ã°Å¸âÂ´ Vermelho"

            # Status calagem
            if dados_area and "ph" in dados_area:
                _dose_rec, _ = calcular_calcario_por_ph(dados_area.get("ph",5.5), area.get("Hectares",1))
                if _calc_total == 0:
                    _calc_status = "Ã¢Å¡Âª NÃÂ£o aplicado"
                elif _calc_total >= _dose_rec:
                    _calc_status = "Ã¢Åâ¦ Meta atingida"
                elif _calc_total >= _dose_rec * 0.5:
                    _calc_status = "Ã°Å¸Å¸Â¡ Parcial"
                else:
                    _calc_status = "Ã°Å¸âÂ´ Insuficiente"
                _calc_color = {"Ã¢Åâ¦ Meta atingida":"#14532d","Ã°Å¸Å¸Â¡ Parcial":"#78350f",
                               "Ã°Å¸âÂ´ Insuficiente":"#7f1d1d","Ã¢Å¡Âª NÃÂ£o aplicado":"#1e293b"}
                _calc_rec_txt = f"{_dose_rec} t/ha"
            else:
                _calc_status = "Ã¢Å¡Âª Sem anÃÂ¡lise"
                _calc_color  = {"Ã¢Å¡Âª Sem anÃÂ¡lise":"#1e293b"}
                _calc_rec_txt = "-"

            # Ã¢ââ¬Ã¢ââ¬ Clima Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
            registros_area = [r for r in st.session_state.pluviometro
                              if isinstance(r, dict) and
                              (r.get("area_id") == area.get("ID","") or
                               r.get("ÃÂrea") == area.get("ID",""))]
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
                if   perda_media_clima <= 5:  clima_cor = "Ã°Å¸Å¸Â¢ Ideal"
                elif perda_media_clima <= 12: clima_cor = "Ã°Å¸Å¸Â¡ AtenÃÂ§ÃÂ£o"
                else:                         clima_cor = "Ã°Å¸âÂ´ CrÃÂ­tico"
            else:
                clima_cor = "Ã¢Å¡Âª Sem dados"

            mapa_dados.append({
                "ID":             area.get("ID",""),
                "Fazenda":        area.get("Fazenda",""),
                "TalhÃÂ£o":         area.get("TalhÃÂ£o",""),
                "Cultura":        area.get("Cultura",""),
                "ÃÂrea ha":        area.get("Hectares",0),
                "Score":          score,
                "Classe":         classe,
                "Cor":            cor,
                "Clima":          clima_cor,
                "pH atual":       _ph_orig,
                "pH pÃÂ³s-calagem": _ph_corrigido,
                "CalcÃÂ¡rio t/ha":  _calc_total,
                "Rec. calcÃÂ¡rio":  _calc_rec_txt,
                "Status calagem": _calc_status,
                "Gesso t/ha":     _gesso_total,
                "Alertas":        ", ".join(alertas),
            })

        df_mapa = pd.DataFrame(mapa_dados)

        # Ã¢ââ¬Ã¢ââ¬ VisÃÂ£o geral Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        st.subheader("Ã°Å¸âÂ VisÃÂ£o geral dos talhÃÂµes")
        st.dataframe(df_mapa, use_container_width=True)

        # Ã¢ââ¬Ã¢ââ¬ Cards visuais com calagem Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        st.subheader("Ã°Å¸âºÂ°Ã¯Â¸Â Mapa Visual dos TalhÃÂµes")
        st.write("Ã°Å¸Å¸Â¢ Verde = solo excelente | Ã°Å¸Å¸Â¡ Amarelo = bom | Ã°Å¸Å¸Â  Laranja = mÃÂ©dio | Ã°Å¸âÂ´ Vermelho = crÃÂ­tico")
        cols_card = st.columns(3)
        for i, linha in df_mapa.iterrows():
            cor_str = linha["Cor"]
            if "Verde"   in cor_str: fundo = "#16a34a"
            elif "Amarelo" in cor_str: fundo = "#eab308"
            elif "Laranja" in cor_str: fundo = "#f97316"
            else:                      fundo = "#dc2626"
            _cs = linha["Status calagem"]
            _cc_borda = {"Ã¢Åâ¦ Meta atingida":"#22c55e","Ã°Å¸Å¸Â¡ Parcial":"#eab308",
                         "Ã°Å¸âÂ´ Insuficiente":"#ef4444","Ã¢Å¡Âª NÃÂ£o aplicado":"#64748b",
                         "Ã¢Å¡Âª Sem anÃÂ¡lise":"#64748b"}.get(_cs,"#64748b")
            with cols_card[i % 3]:
                st.markdown(f"""
                <div style="background:{fundo};padding:16px;border-radius:14px;
                margin-bottom:14px;color:white;font-weight:bold;box-shadow:0 4px 12px rgba(0,0,0,0.25);">
                <h3 style="margin:0 0 6px 0;">{linha['TalhÃÂ£o']}</h3>
                <p style="margin:2px 0;">{get_icone_cultura(linha['Cultura'])} {cultura_limpa(linha['Cultura'])} | {linha['ÃÂrea ha']} ha</p>
                <p style="margin:2px 0;">Ã°Å¸âÅ  Score: {linha['Score']} Ã¢â¬â {linha['Classe']}</p>
                <p style="margin:2px 0;">Ã°Å¸ÅÂ§Ã¯Â¸Â Clima: {linha['Clima']}</p>
                <hr style="border-color:rgba(255,255,255,0.4);margin:8px 0;">
                <p style="margin:2px 0;border-left:3px solid {_cc_borda};padding-left:8px;">
                Ã°Å¸ÂªÂ¨ CalcÃÂ¡rio: <b>{linha['CalcÃÂ¡rio t/ha']} t/ha</b> aplicado (rec: {linha['Rec. calcÃÂ¡rio']})<br>
                {_cs}<br>
                Ã°Å¸Â§Â± Gesso: <b>{linha['Gesso t/ha']} t/ha</b><br>
                Ã°Å¸Â§Âª pH: {linha['pH atual']} Ã¢â â <b>{linha['pH pÃÂ³s-calagem']}</b> (pÃÂ³s-calagem)
                </p>
                <p style="margin:6px 0 0 0;font-size:11px;opacity:0.85;">{linha['Alertas']}</p>
                </div>""", unsafe_allow_html=True)

        # Ã¢ââ¬Ã¢ââ¬ Heatmap fertilidade Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        st.subheader("Ã°Å¸ÅÂ¡Ã¯Â¸Â Heatmap de Fertilidade")

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

        _heat_cols = ["TalhÃÂ£o","Score","pH atual","pH pÃÂ³s-calagem","CalcÃÂ¡rio t/ha","Gesso t/ha","Status calagem"]
        df_heat = df_mapa[[c for c in _heat_cols if c in df_mapa.columns]].copy()

        try:
            _styled = df_heat.style\
                .applymap(cor_score, subset=["Score"])\
                .applymap(cor_ph, subset=["pH atual","pH pÃÂ³s-calagem"])\
                .applymap(cor_calc, subset=["CalcÃÂ¡rio t/ha","Gesso t/ha"])
            st.dataframe(_styled, use_container_width=True)
        except Exception:
            st.dataframe(df_heat, use_container_width=True)

        st.caption("Ã°Å¸Å¸Â¢ Verde = ÃÂ³timo | Ã°Å¸Å¸Â¡ Laranja = atenÃÂ§ÃÂ£o | Ã°Å¸âÂ´ Vermelho = crÃÂ­tico | Ã¢Å¡Â« Cinza = sem dados")

        # Ã¢ââ¬Ã¢ââ¬ Ranking Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        st.subheader("Ã°Å¸âÅ  Ranking de Fertilidade")
        st.bar_chart(df_mapa.set_index("TalhÃÂ£o")["Score"])

        st.subheader("Ã°Å¸âºÂ°Ã¯Â¸Â Mapa GPS dos TalhÃÂµes")

        # Coordenadas Ã¢â¬â prioridade: GPS salvo > ÃÂ¡rea cadastrada > padrÃÂ£o
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
            if st.button("Ã°Å¸âÂ¡ GPS", key="btn_gps_mapa_fert", use_container_width=True,
                         help="Clique para usar localizaÃÂ§ÃÂ£o do celular"):
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
            attr="Esri", name="SatÃÂ©lite", control=True
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
        folium.Marker(location=[latitude, longitude], popup="Minha localizaÃÂ§ÃÂ£o",
                      tooltip="Local atual", icon=folium.Icon(color="darkgreen", icon="leaf")
        ).add_to(mapa_folium)
        dados_mapa_folium = st_folium(mapa_folium, width=900, height=500)
        st.subheader("Ã°Å¸âÂ¾ Salvar Desenho do TalhÃÂ£o")

        st.info("Ã°Å¸âÂ¡ **Dica no celular:** Marque os pontos no sentido horÃÂ¡rio ao redor do talhÃÂ£o, sem cruzar as linhas. Use o botÃÂ£o **Delete last point** para desfazer o ÃÂºltimo ponto.")

        if dados_mapa_folium and dados_mapa_folium.get("last_active_drawing"):
            desenho = dados_mapa_folium["last_active_drawing"]
            coords  = desenho["geometry"]["coordinates"][0]

            # Corrige automaticamente polÃÂ­gonos com bordas cruzadas usando convex hull
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
            success_box(f"ÃÂrea calculada automaticamente: {area_calculada:.2f} ha")

            # SeleÃÂ§ÃÂ£o da ÃÂ¡rea para vincular o desenho
            areas_disp = [f"{a.get('Fazenda','')} Ã¢â¬â {a.get('TalhÃÂ£o','')}" for a in st.session_state.areas]
            area_vincular = st.selectbox("Vincular desenho ÃÂ  ÃÂ¡rea:", ["Ã¢â¬â NÃÂ£o vincular Ã¢â¬â"] + areas_disp, key="sel_area_croqui")

            if st.button("Salvar desenho no talhÃÂ£o", key="salvar_desenho_talhao"):
                pts_hull = convex_hull([[c[0], c[1]] for c in coords])
                if len(pts_hull) >= 3:
                    pts_hull.append(pts_hull[0])
                    desenho["geometry"]["coordinates"][0] = [[p[0], p[1]] for p in pts_hull]

                # Salva no session_state global
                st.session_state.dados["desenho_talhao"] = desenho

                # Salva tambÃÂ©m na ÃÂ¡rea especÃÂ­fica se selecionada
                if area_vincular != "Ã¢â¬â NÃÂ£o vincular Ã¢â¬â":
                    idx_area = areas_disp.index(area_vincular)
                    st.session_state.areas[idx_area]["desenho"] = desenho
                    st.session_state.areas[idx_area]["area_calculada_ha"] = round(area_calculada, 2)

                salvar_dados_iaagro()
                success_box("Ã¢Åâ¦ Desenho do talhÃÂ£o salvo com sucesso!")


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: ANÃÂLISE DE SOLO
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
elif menu == "Ã°Å¸Â§Âª Solo & AdubaÃÂ§ÃÂ£o":
    _sub_solo = st.tabs(["Ã°Å¸Â§Âª AnÃÂ¡lise de Solo","Ã°Å¸âÂ¬ DiagnÃÂ³stico Completo","Ã°Å¸ÅÂ± AdubaÃÂ§ÃÂ£o","Ã°Å¸ââ OCR Laudo de Solo"])

if menu == "Ã°Å¸Â§Âª Solo & AdubaÃÂ§ÃÂ£o":
  with _sub_solo[0]:
    st.header("AnÃÂ¡lise de Solo")

    # Injeta estilo escuro no componente de upload via JS
    st.markdown("""
    <style>
    /* ForÃÂ§a fundo escuro no dropzone do upload */
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploader"] section > div,
    [data-testid="stFileUploaderDropzone"],
    [data-testid="stFileUploaderDropzone"] > div {
        background-color: #0f3460 !important;
        border: 2px solid #22c55e !important;
        border-radius: 12px !important;
    }
    /* BotÃÂ£o Upload */
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
    /* Texto de instruÃÂ§ÃÂ£o */
    [data-testid="stFileUploaderDropzone"] span,
    [data-testid="stFileUploaderDropzone"] p,
    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploaderDropzone"] div {
        color: #ffffff !important;
        opacity: 1 !important;
    }
    /* ÃÂcone */
    [data-testid="stFileUploaderDropzone"] svg path {
        fill: #22c55e !important;
        stroke: #22c55e !important;
    }
    </style>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Ã°Å¸ââ Upload anÃÂ¡lise de solo", type=["xlsx","csv"], key="upl___upload_an_lis_3464")
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df_upload = pd.read_csv(uploaded_file)
        else:
            df_upload = pd.read_excel(uploaded_file)
        success_box("Ã¢Åâ¦ AnÃÂ¡lise carregada com sucesso!")
        st.dataframe(df_upload)

    if not st.session_state.area_selecionada:
        warning_box("Cadastre ou carregue uma ÃÂ¡rea primeiro.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            ph       = st.number_input("pH do solo (HÃ¢ââO 1:1)", min_value=3.5, max_value=8.0, value=float(st.session_state.dados.get("ph", 5.5)), key="num_ph_do_solo_3478")
            fosforo  = st.number_input("FÃÂ³sforo P (mg/dmÃÂ³ Mehlich-1)", min_value=0.0, value=float(st.session_state.dados.get("fosforo", 10.0)), key="num_f_sforo_p_3479")
            potassio = st.number_input("PotÃÂ¡ssio K (mg/dmÃÂ³ Mehlich-1)", min_value=0.0, value=float(st.session_state.dados.get("potassio", 100.0)), key="num_pot_ssio_k_3480")
        with col2:
            materia_organica = st.number_input("MatÃÂ©ria OrgÃÂ¢nica MO (g/dmÃÂ³)", min_value=0.0, value=float(st.session_state.dados.get("materia_organica", 2.5)), key="num_mat_ria_org_nic_3482", help="1% = 10 g/dmÃÂ³")
            calcio   = st.number_input("CÃÂ¡lcio CaÃÂ²Ã¢ÂÂº (cmolc/dmÃÂ³)", min_value=0.0, value=float(st.session_state.dados.get("calcio", 3.0)), key="num_c_lcio_ca_3483")
            magnesio = st.number_input("MagnÃÂ©sio MgÃÂ²Ã¢ÂÂº (cmolc/dmÃÂ³)", min_value=0.0, value=float(st.session_state.dados.get("magnesio", 1.0)), key="num_magn_sio_mg_3484")
        with col3:
            aluminio = st.number_input("AlumÃÂ­nio AlÃÂ³Ã¢ÂÂº (cmolc/dmÃÂ³)", min_value=0.0, value=float(st.session_state.dados.get("aluminio", 0.2)), key="num_alum_nio_al_3486")
            enxofre  = st.number_input("Enxofre S (mg/dmÃÂ³)", min_value=0.0, value=float(st.session_state.dados.get("enxofre", 8.0)), key="num_enxofre_s_3487")
            ctc      = st.number_input("CTC pH7 (cmolc/dmÃÂ³)", min_value=0.0, value=float(st.session_state.dados.get("ctc", 8.0)), key="num_ctc_3488", help="Capacidade de Troca CatiÃÂ´nica")

        # Ã¢ââ¬Ã¢ââ¬ CÃÂ¡lculo automÃÂ¡tico de V% e SB Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        sb_calc  = calcio + magnesio + (potassio / 391.0)  # K em cmolc
        ctc_val  = ctc if ctc > 0 else (sb_calc + aluminio + 2.0)
        v_calc   = round((sb_calc / ctc_val) * 100, 1) if ctc_val > 0 else 0.0
        m_calc   = round((aluminio / (sb_calc + aluminio)) * 100, 1) if (sb_calc + aluminio) > 0 else 0.0

        st.markdown(f"""
        <div style='background:#0f3460;border-radius:8px;padding:10px 16px;border:1px solid #3b82f6;margin:8px 0;'>
        <b style='color:#3b82f6;'>Ã°Å¸âÅ  Calculado automaticamente (CQFS RS/SC 2016)</b><br>
        <span style='color:#f1f5f9;font-size:13px;'>
        SB = Ca + Mg + K = <b>{sb_calc:.2f} cmolc/dmÃÂ³</b> &nbsp;|&nbsp;
        <b>V% = {v_calc}%</b> {"Ã°Å¸Å¸Â¢ Adequado" if v_calc >= 60 else "Ã°Å¸Å¸Â¡ MÃÂ©dio" if v_calc >= 45 else "Ã°Å¸âÂ´ Baixo"} &nbsp;|&nbsp;
        <b>m% = {m_calc}%</b> {"Ã°Å¸Å¸Â¢ OK" if m_calc < 20 else "Ã°Å¸âÂ´ Alto"} &nbsp;|&nbsp;
        RelaÃÂ§ÃÂ£o Ca/Mg = <b>{round(calcio/magnesio,1) if magnesio > 0 else '-'}</b>
        {"Ã¢Åâ¦" if 2<=round(calcio/magnesio,1)<=5 else "Ã¢Å¡Â Ã¯Â¸Â"  if magnesio > 0 else ""}
        </span>
        </div>
        """, unsafe_allow_html=True)

        # Ã¢ââ¬Ã¢ââ¬ V% manual (se vier do laudo) Ã¢ââ¬Ã¢ââ¬
        v_laudo = st.number_input("V% do laudo (deixe 0 para usar o calculado)", min_value=0.0, max_value=100.0,
                                   value=float(st.session_state.dados.get("v_percent", 0.0)), key="num_v_percent",
                                   help="SaturaÃÂ§ÃÂ£o por bases Ã¢â¬â use se o laudo jÃÂ¡ fornecer o valor")
        v_final = v_laudo if v_laudo > 0 else v_calc

        st.subheader("Ã°Å¸âÂ¬ Micronutrientes (mg/dmÃÂ³ Mehlich-1)")
        col4, col5, col6 = st.columns(3)
        with col4:
            boro  = st.number_input("Boro B", min_value=0.0, value=float(st.session_state.dados.get("boro", 0.3)), key="num_boro_b_3493")
            zinco = st.number_input("Zinco Zn", min_value=0.0, value=float(st.session_state.dados.get("zinco", 1.0)), key="num_zinco_zn_3494")
        with col5:
            manganes = st.number_input("ManganÃÂªs Mn", min_value=0.0, value=float(st.session_state.dados.get("manganes", 5.0)), key="num_mangan_s_mn_3496")
            cobre    = st.number_input("Cobre Cu", min_value=0.0, value=float(st.session_state.dados.get("cobre", 0.5)), key="num_cobre_cu_3497")
        with col6:
            ferro    = st.number_input("Ferro Fe", min_value=0.0, value=float(st.session_state.dados.get("ferro", 30.0)), key="num_ferro_fe", help="ReferÃÂªncia: >9 mg/dmÃÂ³")
            molibdenio = st.number_input("MolibdÃÂªnio Mo", min_value=0.0, value=float(st.session_state.dados.get("molibdenio", 0.1)), key="num_molibdenio", help="ReferÃÂªncia: >0.1 mg/dmÃÂ³")

        st.subheader("Ã°Å¸ÂªÂ¨ AnÃÂ¡lise FÃÂ­sica do Solo")
        col7, col8, col9 = st.columns(3)
        with col7:
            argila   = st.number_input("Argila (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.dados.get("argila", 35.0)), key="num_argila___3499")
            silte    = st.number_input("Silte (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.dados.get("silte", 25.0)), key="num_silte")
        with col8:
            areia    = st.number_input("Areia total (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.dados.get("areia", 40.0)), key="num_areia")
            dens_solo= st.number_input("Densidade do solo (g/cmÃÂ³)", min_value=0.5, max_value=2.0, value=float(st.session_state.dados.get("dens_solo", 1.2)), key="num_dens_solo", help="ReferÃÂªncia: <1.3 g/cmÃÂ³ para argilosos")
        with col9:
            dens_part= st.number_input("Densidade de partÃÂ­culas (g/cmÃÂ³)", min_value=1.0, max_value=3.5, value=float(st.session_state.dados.get("dens_part", 2.65)), key="num_dens_part", help="PadrÃÂ£o: 2.65 g/cmÃÂ³")
            umidade  = st.number_input("Umidade atual (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.dados.get("umidade", 0.0)), key="num_umidade")

        # Calcula porosidade e textura automaticamente
        _soma_granulo = argila + silte + areia
        _porosidade = round((1 - dens_solo/dens_part)*100, 1) if dens_part > 0 else 0
        if argila >= 60:    _textura = "Muito argiloso"
        elif argila >= 35:  _textura = "Argiloso"
        elif argila >= 25:  _textura = "MÃÂ©dia argilosa"
        elif argila >= 15:  _textura = "Franco-argiloso"
        elif silte >= 50:   _textura = "Siltoso"
        elif areia >= 70:   _textura = "Arenoso"
        else:               _textura = "Franco"

        if _soma_granulo > 0:
            st.markdown(f"""
            <div style='background:#0f3460;border-radius:8px;padding:10px 16px;border:1px solid #22c55e;margin:8px 0;'>
            <b style='color:#22c55e;'>Ã°Å¸ÂªÂ¨ FÃÂ­sica do Solo calculada</b><br>
            <span style='color:#f1f5f9;font-size:13px;'>
            Classe textural: <b>{_textura}</b> &nbsp;|&nbsp;
            Porosidade total: <b>{_porosidade}%</b>
            {"Ã°Å¸Å¸Â¢ Boa" if _porosidade >= 50 else "Ã°Å¸Å¸Â¡ MÃÂ©dia" if _porosidade >= 40 else "Ã°Å¸âÂ´ Compactado"} &nbsp;|&nbsp;
            Soma granulomÃÂ©trica: <b>{_soma_granulo:.0f}%</b>
            {"Ã¢Åâ¦" if 95<=_soma_granulo<=105 else "Ã¢Å¡Â Ã¯Â¸Â Verificar soma"}
            </span>
            </div>
            """, unsafe_allow_html=True)

        # ValidaÃÂ§ÃÂ£o de campos
        erros_val = []
        if not validar_ph(ph):
            erros_val.append("pH deve estar entre 3.5 e 9.0")
        if ph == 0:
            erros_val.append("pH nÃÂ£o pode ser zero")

        if erros_val:
            for e in erros_val:
                st.markdown(f'''<div style="background:#7f1d1d;color:#fff;padding:10px 16px;
                border-radius:10px;border-left:5px solid #ef4444;font-weight:600;margin:4px 0;">
                Ã¢ÂÅ {e}</div>''', unsafe_allow_html=True)

        if st.button("Salvar AnÃÂ¡lise"):
            if erros_val:
                st.markdown('''<div style="background:#7f1d1d;color:#fff;padding:10px 16px;
                border-radius:10px;border-left:5px solid #ef4444;font-weight:600;">
                Ã¢ÂÅ Corrija os erros antes de salvar.</div>''', unsafe_allow_html=True)
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
                atualizar_area_atual()
                salvar_dados_iaagro()
                # Salvar no banco histÃÂ³rico
                nota_s  = calcular_nota(st.session_state.dados)
                score_s, classe_s, _ = score_solo(st.session_state.dados)
                id_area_atual = st.session_state.dados.get("id_area","")
                if id_area_atual:
                    salvar_analise_solo_db(id_area_atual, st.session_state.dados, nota_s, score_s, classe_s)
                # Checar alertas de estoque por email
                checar_alertas_estoque()
                success_box("AnÃÂ¡lise salva na ÃÂ¡rea ativa e registrada no histÃÂ³rico!")

        # Ã¢ââ¬Ã¢ââ¬ Foto do talhÃÂ£o Ã¢ââ¬Ã¢ââ¬
        st.divider()
        st.subheader("Ã°Å¸âÂ· Foto do TalhÃÂ£o")
        foto = st.file_uploader("Adicionar foto do talhÃÂ£o (JPG, PNG)", type=["jpg","jpeg","png"],
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


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: DIAGNÃâSTICO COMPLETO
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸Â§Âª Solo & AdubaÃÂ§ÃÂ£o":
  with _sub_solo[1]:
    st.header("DiagnÃÂ³stico Completo")
    d = st.session_state.dados
    # Busca dados da ÃÂ¡rea com anÃÂ¡lise se session_state.dados nÃÂ£o tiver pH
    if "ph" not in d and st.session_state.areas:
        _id_s = st.session_state.get("area_selecionada")
        for _a in st.session_state.areas:
            _dad = _a.get("Dados", _a.get("dados", {}))
            if _dad and "ph" in _dad and (_id_s is None or _a.get("ID") == _id_s):
                d = {**_dad, "cultura": _a.get("Cultura","Soja"),
                     "area": _a.get("Hectares",0), "produtividade": _a.get("Produtividade",50)}
                break
        if "ph" not in d:  # pega qualquer ÃÂ¡rea com anÃÂ¡lise
            for _a in st.session_state.areas:
                _dad = _a.get("Dados", _a.get("dados", {}))
                if _dad and "ph" in _dad:
                    d = {**_dad, "cultura": _a.get("Cultura","Soja"),
                         "area": _a.get("Hectares",0), "produtividade": _a.get("Produtividade",50)}
                    break

    if "ph" not in d:
        warning_box("Preencha primeiro a anÃÂ¡lise de solo.")
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
        col3.metric("CalcÃÂ¡rio",          f"{dose_calcario} t/ha")
        col4.metric("Gesso",             f"{dose_gesso} t/ha")
        col5.metric("ProduÃÂ§ÃÂ£o Estimada", f"{producao_estimada:.1f} sc/ha")

        st.subheader("Ã°Å¸Â§Â  Score Inteligente do Solo")
        col1, col2 = st.columns(2)
        col1.metric("Score do Solo",   f"{score}/100")
        col2.metric("ClassificaÃÂ§ÃÂ£o",   classe_score)
        if alertas_score:
            warning_box(" | ".join(alertas_score))
        else:
            success_box("Solo em boas condiÃÂ§ÃÂµes gerais.")

        indice_produtivo  = score * 1.15
        produtividade_ia  = producao_estimada * (indice_produtivo / 100)
        if   indice_produtivo >= 85: status_ia = "ALTO"
        elif indice_produtivo >= 65: status_ia = "MÃâ°DIO"
        else:                        status_ia = "BAIXO"

        st.subheader("Ã°Å¸Â¤â InteligÃÂªncia Artificial Produtiva")
        st.markdown(f'''<div style="background:#1e3a5f;color:#ffffff;padding:15px 18px;border-radius:12px;
        border-left:5px solid #3b82f6;font-size:15px;font-weight:600;line-height:2.0;margin:8px 0;">
        Ã°Å¸Â¤â <b>Potencial estimado:</b> {status_ia}<br>
        Ã°Å¸âË <b>Produtividade prevista pela IA:</b> {produtividade_ia:.1f} sc/ha<br>
        Ã°Å¸âÅ  <b>ÃÂndice produtivo do talhÃÂ£o:</b> {indice_produtivo:.1f}/100
        </div>''', unsafe_allow_html=True)

        st.subheader("Ã°Å¸âÂ° InteligÃÂªncia EconÃÂ´mica")
        area          = float(d["area"])
        _precos_data  = st.session_state.get("precos_data") or {}
        _soja_sc      = _precos_data.get("soja_sc") or {}
        preco_soja    = float(_soja_sc.get("preco", 115.0) or 115.0)
        custo_base    = 3200
        receita_estimada = produtividade_ia * preco_soja * area
        lucro_estimado   = receita_estimada - (custo_base * area)
        if   lucro_estimado > 50000: risco = "BAIXO"
        elif lucro_estimado > 20000: risco = "MÃâ°DIO"
        else:                         risco = "ALTO"
        st.markdown(f'''<div style="background:#14532d;color:#ffffff;padding:15px 18px;border-radius:12px;
        border-left:5px solid #22c55e;font-size:15px;font-weight:600;line-height:2.0;margin:8px 0;">
        Ã°Å¸âÂ° <b>Receita estimada:</b> R$ {receita_estimada:,.2f}<br>
        Ã°Å¸âÂµ <b>Lucro potencial:</b> R$ {lucro_estimado:,.2f}<br>
        Ã°Å¸âÅ  <b>Risco econÃÂ´mico:</b> {risco}
        </div>''', unsafe_allow_html=True)

        st.subheader("CalcÃÂ¡rio")
        st.write(f"Dose estimada: {dose_calcario} t/ha")
        st.write(f"Total estimado: {total_calcario:.1f} toneladas")

        st.subheader("Gesso AgrÃÂ­cola")
        if precisa_gesso:
            warning_box(f"IndicaÃÂ§ÃÂ£o inicial de gesso: {dose_gesso} t/ha")
            st.write(f"Total estimado: {total_gesso:.1f} toneladas")
            for motivo in motivos_gesso:
                st.write(f"- {motivo}")
        else:
            success_box("Sem indicaÃÂ§ÃÂ£o inicial forte para gesso.")

        cultura_diag = d.get("cultura", "Soja")
        score, classe_score, alertas_score = score_solo(d, cultura_diag)

        # Tabela completa com micronutrientes
        # Limites EMBRAPA/CQFS RS-SC 2016 por parÃÂ¢metro
        def _classif_micro(valor, lim_baixo, lim_medio):
            if valor == 0: return "Ã¢â¬â"
            if   valor < lim_baixo:  return "Ã°Å¸âÂ´ Baixo"
            elif valor < lim_medio:  return "Ã°Å¸Å¸Â¡ MÃÂ©dio"
            else:                    return "Ã°Å¸Å¸Â¢ Adequado"

        tabela = pd.DataFrame({
            "Indicador": [
                "pH","FÃÂ³sforo (mg/dmÃÂ³)","PotÃÂ¡ssio (mg/dmÃÂ³)",
                "MatÃÂ©ria OrgÃÂ¢nica (%)","CÃÂ¡lcio (cmolc/dmÃÂ³)","MagnÃÂ©sio (cmolc/dmÃÂ³)",
                "Enxofre (mg/dmÃÂ³)","AlumÃÂ­nio (cmolc/dmÃÂ³)","CTC (cmolc/dmÃÂ³)","Argila (%)",
                "Zinco Zn (mg/dmÃÂ³)","Boro B (mg/dmÃÂ³)","ManganÃÂªs Mn (mg/dmÃÂ³)","Cobre Cu (mg/dmÃÂ³)"
            ],
            "Valor": [
                d.get("ph",0), d.get("fosforo",0), d.get("potassio",0),
                d.get("materia_organica",0), d.get("calcio",0), d.get("magnesio",0),
                d.get("enxofre",0), d.get("aluminio",0), d.get("ctc",0), d.get("argila",0),
                d.get("zinco",0), d.get("boro",0), d.get("manganes",0), d.get("cobre",0)
            ],
            "ClassificaÃÂ§ÃÂ£o (EMBRAPA)": [
                "Ã°Å¸âÂ´ Baixo" if d.get("ph",0) < 5.5 else ("Ã°Å¸Å¸Â¢ Adequado" if d.get("ph",0) <= 6.5 else "Ã°Å¸Å¸Â¡ Alto"),
                _classif_micro(d.get("fosforo",0), 6, 18),
                _classif_micro(d.get("potassio",0), 60, 150),
                _classif_micro(d.get("materia_organica",0), 2.5, 4.5),
                _classif_micro(d.get("calcio",0), 2.0, 4.0),
                _classif_micro(d.get("magnesio",0), 0.5, 1.5),
                _classif_micro(d.get("enxofre",0), 5, 10),
                "Ã°Å¸Å¸Â¢ OK" if d.get("aluminio",0) <= 0.3 else ("Ã°Å¸Å¸Â¡ AtenÃÂ§ÃÂ£o" if d.get("aluminio",0) <= 1.0 else "Ã°Å¸âÂ´ TÃÂ³xico"),
                _classif_micro(d.get("ctc",0), 5, 10),
                _classif_micro(d.get("argila",0), 15, 35),
                _classif_micro(d.get("zinco",0), 0.6, 1.5),
                _classif_micro(d.get("boro",0), 0.2, 0.6),
                _classif_micro(d.get("manganes",0), 1.2, 5.0),
                _classif_micro(d.get("cobre",0), 0.2, 0.8),
            ],
            "ReferÃÂªncia EMBRAPA": [
                "5.8Ã¢â¬â6.5","6Ã¢â¬â30 (Mehlich-1)","60Ã¢â¬â200","2.5Ã¢â¬â4.5%","2Ã¢â¬â6","0.5Ã¢â¬â2",
                "5Ã¢â¬â15","<0.3 ideal","6Ã¢â¬â15","20Ã¢â¬â60%",
                "0.6Ã¢â¬â2.0","0.2Ã¢â¬â0.6","1.2Ã¢â¬â5.0","0.2Ã¢â¬â0.8"
            ]
        })
        st.dataframe(tabela, use_container_width=True)

        # Parecer especÃÂ­fico de micronutrientes
        st.subheader("Ã°Å¸âÂ¬ Parecer de Micronutrientes")
        micro_alertas = []
        zinco_v  = d.get("zinco",0)
        boro_v   = d.get("boro",0)
        mn_v     = d.get("manganes",0)
        cu_v     = d.get("cobre",0)
        enx_v    = d.get("enxofre",0)

        # Zinco Ã¢â¬â crÃÂ­tico para milho, soja
        if zinco_v > 0:
            if zinco_v < 0.6:
                micro_alertas.append(("Ã°Å¸âÂ´", "Zinco", f"{zinco_v} mg/dmÃÂ³", "DeficiÃÂªncia crÃÂ­tica Ã¢â¬â aplicar 2-3 kg/ha ZnSO4 ou quelato", "Milho e soja muito sensÃÂ­veis"))
            elif zinco_v < 1.0:
                micro_alertas.append(("Ã°Å¸Å¸Â¡", "Zinco", f"{zinco_v} mg/dmÃÂ³", "NÃÂ­vel mÃÂ©dio Ã¢â¬â monitorar", "Foliar preventivo em culturas sensÃÂ­veis"))

        # Boro Ã¢â¬â crÃÂ­tico para soja, cafÃÂ©, algodÃÂ£o
        if boro_v > 0:
            if boro_v < 0.2:
                micro_alertas.append(("Ã°Å¸âÂ´", "Boro", f"{boro_v} mg/dmÃÂ³", "DeficiÃÂªncia Ã¢â¬â aplicar 1-2 kg/ha B (ÃÂ¡cido bÃÂ³rico ou ulexita)", "Soja: afeta enchimento de grÃÂ£os"))
            elif boro_v < 0.4:
                micro_alertas.append(("Ã°Å¸Å¸Â¡", "Boro", f"{boro_v} mg/dmÃÂ³", "NÃÂ­vel baixo-mÃÂ©dio Ã¢â¬â foliar recomendado no florescimento", "Soja, cafÃÂ© e algodÃÂ£o"))

        # ManganÃÂªs Ã¢â¬â importante pH>6.5 causa deficiÃÂªncia
        if mn_v > 0:
            if mn_v < 1.2:
                micro_alertas.append(("Ã°Å¸âÂ´", "ManganÃÂªs", f"{mn_v} mg/dmÃÂ³", "DeficiÃÂªncia Ã¢â¬â verificar pH (>6.5 indisponibiliza Mn)", "Soja mais sensÃÂ­vel"))
            elif mn_v > 20:
                micro_alertas.append(("Ã°Å¸Å¸Â ", "ManganÃÂªs", f"{mn_v} mg/dmÃÂ³", "NÃÂ­vel elevado Ã¢â¬â pH baixo pode causar toxidez", "Elevar pH com calcÃÂ¡rio"))

        # Cobre
        if cu_v > 0 and cu_v < 0.2:
            micro_alertas.append(("Ã°Å¸Å¸Â¡", "Cobre", f"{cu_v} mg/dmÃÂ³", "Baixo Ã¢â¬â aplicar CuSO4 0.5-1 kg/ha ou foliar", "Solos orgÃÂ¢nicos mais suscetÃÂ­veis"))

        # Enxofre
        if enx_v > 0 and enx_v < 5:
            micro_alertas.append(("Ã°Å¸âÂ´", "Enxofre", f"{enx_v} mg/dmÃÂ³", "DeficiÃÂªncia Ã¢â¬â usar gesso agrÃÂ­cola ou fertilizante com S", "Soja: 10-20 kg S/ha; Milho: 10-15 kg S/ha"))

        if micro_alertas:
            for icone, nut, val, rec, obs in micro_alertas:
                st.markdown(f"""
                <div style='background:#1e293b;border-radius:10px;padding:12px 16px;
                margin-bottom:8px;border-left:4px solid {"#ef4444" if icone=="Ã°Å¸âÂ´" else "#f59e0b"}'>
                <b style='color:#f1f5f9;'>{icone} {nut}: {val}</b><br>
                <span style='color:#22c55e;font-size:13px;'>Ã°Å¸âÅ  RecomendaÃÂ§ÃÂ£o: {rec}</span><br>
                <span style='color:#94a3b8;font-size:12px;'>Ã°Å¸âÅ {obs}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Ã¢Åâ¦ Micronutrientes dentro dos limites adequados (EMBRAPA/CQFS RS-SC).")


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: ADUBAÃâ¡ÃÆO
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸Â§Âª Solo & AdubaÃÂ§ÃÂ£o":
  with _sub_solo[2]:
    st.header("Ã°Å¸ÅÂ± AdubaÃÂ§ÃÂ£o Inteligente")

    # Busca dados da ÃÂ¡rea selecionada Ã¢â¬â prioridade: area ativa > primeira ÃÂ¡rea
    d = st.session_state.dados
    _id_sel = st.session_state.get("area_selecionada")

    # Se dados nÃÂ£o tÃÂªm pH mas hÃÂ¡ ÃÂ¡reas cadastradas, pega da ÃÂ¡rea selecionada
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
        # Se ainda nÃÂ£o tem, pega da primeira ÃÂ¡rea com anÃÂ¡lise
        if "ph" not in d:
            for _a in st.session_state.areas:
                _dados_area = _a.get("Dados", _a.get("dados", {}))
                if _dados_area and "ph" in _dados_area:
                    d = {**_dados_area,
                         "cultura": _a.get("Cultura", "Soja"),
                         "area":    _a.get("Hectares", 0),
                         "produtividade": _a.get("Produtividade", 50)}
                    break

    # Seletor de ÃÂ¡rea quando hÃÂ¡ mÃÂºltiplas
    if st.session_state.areas:
        _areas_adub = [f"{a['ID']} Ã¢â¬â {a.get('TalhÃÂ£o','?')} ({a.get('Cultura','?')})"
                       for a in st.session_state.areas
                       if a.get("Dados") and "ph" in a.get("Dados", {})]
        _areas_sem = [a for a in st.session_state.areas
                      if not a.get("Dados") or "ph" not in a.get("Dados", {})]

        if _areas_sem and not _areas_adub:
            warning_box("Preencha a AnÃÂ¡lise de Solo para ver as recomendaÃÂ§ÃÂµes de adubaÃÂ§ÃÂ£o.")
        elif _areas_adub:
            if len(_areas_adub) > 1:
                _sel_adub = st.selectbox("Ã°Å¸âÂ ÃÂrea para adubaÃÂ§ÃÂ£o", _areas_adub, key="sel_area_adubacao")
            else:
                _sel_adub = _areas_adub[0]
            _id_adub  = _sel_adub.split(" Ã¢â¬â ")[0]
            _a_obj    = next((a for a in st.session_state.areas if a.get("ID") == _id_adub), None)
            if _a_obj:
                _dad = _a_obj.get("Dados", {})
                if _dad:
                    d = {**_dad,
                         "cultura":       _a_obj.get("Cultura", d.get("cultura","Soja")),
                         "area":          _a_obj.get("Hectares", d.get("area",0)),
                         "produtividade": _a_obj.get("Produtividade", d.get("produtividade",50))}

    st.divider()
    st.subheader("Ã°Å¸ÂªÂ¨ Controle de CalcÃÂ¡rio e Gesso Aplicados")

    if not st.session_state.areas:
        warning_box("Cadastre uma ÃÂ¡rea primeiro.")
    else:
        # Seletor explÃÂ­cito de ÃÂ¡rea
        _lista_areas_corr = [f"{a['ID']} Ã¢â¬â {a.get('TalhÃÂ£o','?')} ({a.get('Fazenda','?')})"
                             for a in st.session_state.areas]
        _sel_area_corr = st.selectbox("Ã°Å¸âÂ ÃÂrea para corretivos",
                                       _lista_areas_corr, key="sel_area_corretivos")
        _id_area_atual = _sel_area_corr.split(" Ã¢â¬â ")[0]
        # Inicializa registro de corretivos
        if "corretivos_aplicados" not in st.session_state:
            st.session_state.corretivos_aplicados = []

        _corretivos = [c for c in st.session_state.corretivos_aplicados
                       if isinstance(c, dict) and c.get("area_id") == _id_area_atual]

        # Ã¢ââ¬Ã¢ââ¬ CalcÃÂ¡rio aplicado Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        st.markdown("#### Ã°Å¸ÂªÂ¨ CalcÃÂ¡rio")
        col_ca1, col_ca2, col_ca3 = st.columns(3)
        with col_ca1:
            _data_calc = st.date_input("Data aplicaÃÂ§ÃÂ£o", key="date_calcario_aplic",
                                        value=datetime.now().date())
            _toneladas_calc = st.number_input("Quantidade aplicada (t/ha)", min_value=0.0,
                                               step=0.1, key="num_calc_aplic",
                                               help="Toneladas por hectare aplicadas")
        with col_ca2:
            _prnt_aplic = st.number_input("PRNT do produto (%)", min_value=0.0, max_value=100.0,
                                           value=75.0, step=1.0, key="num_prnt_aplic",
                                           help="Verificar na embalagem Ã¢â¬â padrÃÂ£o 75%")
            _tipo_calc = st.selectbox("Tipo de calcÃÂ¡rio",
                ["CalcÃÂ¡rio DolomÃÂ­tico (Ca+Mg Ã¢â¬â ideal solos com Mg baixo)",
                 "CalcÃÂ¡rio CalcÃÂ­tico (sÃÂ³ Ca Ã¢â¬â usar se Mg jÃÂ¡ adequado)",
                 "CalcÃÂ¡rio Magnesiano (predomina Mg)",
                 "Cal Virgem (CaO Ã¢â¬â aÃÂ§ÃÂ£o rÃÂ¡pida)",
                 "Cal Hidratada (Ca(OH)Ã¢ââ Ã¢â¬â aÃÂ§ÃÂ£o rÃÂ¡pida)",
                 "Outro"], key="sel_tipo_calc",
                help="DolomÃÂ­tico: >12% MgO | CalcÃÂ­tico: <12% MgO (CQFS RS/SC 2016)")

            # Mostra info sobre o tipo escolhido
            if "DolomÃÂ­tico" in _tipo_calc:
                st.caption("Ã°Å¸Å¸Â¢ **DolomÃÂ­tico:** fornece Ca e Mg Ã¢â¬â recomendado quando Ca/Mg < 2:1 ou Mg < 0.5 cmolc/dmÃÂ³")
            elif "CalcÃÂ­tico" in _tipo_calc:
                st.caption("Ã°Å¸âÂµ **CalcÃÂ­tico:** fornece sÃÂ³ Ca Ã¢â¬â usar quando Mg jÃÂ¡ estÃÂ¡ adequado (>1.0 cmolc/dmÃÂ³)")
            elif "Magnesiano" in _tipo_calc:
                st.caption("Ã°Å¸Å¸Â¡ **Magnesiano:** predomina Mg Ã¢â¬â usar em solos com Mg muito baixo")
        with col_ca3:
            _incorporado = st.checkbox("Incorporado ao solo", value=True, key="chk_incorporado",
                                        help="Incorporado com grade ou arado")
            _obs_calc = st.text_input("ObservaÃÂ§ÃÂ£o", placeholder="Ex: Aplicado antes do plantio",
                                       key="txt_obs_calc")

        if st.button("Ã°Å¸âÂ¾ Registrar CalcÃÂ¡rio", key="btn_reg_calc", use_container_width=True):
            if _toneladas_calc <= 0:
                st.error(f"Ã¢ÂÅ Digite a quantidade em t/ha (valor atual: {_toneladas_calc})")
            elif not _id_area_atual:
                st.error("Ã¢ÂÅ Selecione uma ÃÂ¡rea primeiro")
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
                # Atualiza dados DENTRO da ÃÂ¡rea correta no array areas
                _ph_atual = 5.5
                for _area_obj in st.session_state.areas:
                    if _area_obj.get("ID") == _id_area_atual:
                        _dados_area = _area_obj.get("Dados", _area_obj.get("dados", {}))
                        _ph_atual   = _dados_area.get("ph", 5.5) if _dados_area else 5.5
                        break
                _elevacao = round((_toneladas_calc * _prnt_aplic / 100) * 0.3, 2)
                _ph_novo  = min(round(_ph_atual + _elevacao, 1), 7.0)
                # Persiste ph_pos_calagem e calcario_aplicado_ha dentro de cada ÃÂ¡rea
                for _area_obj in st.session_state.areas:
                    if _area_obj.get("ID") == _id_area_atual:
                        if "Dados" not in _area_obj:
                            _area_obj["Dados"] = {}
                        _area_obj["Dados"]["ph_pos_calagem"]      = _ph_novo
                        _area_obj["Dados"]["calcario_aplicado_ha"] = round(
                            _area_obj["Dados"].get("calcario_aplicado_ha", 0) + _toneladas_calc, 2)
                        break
                # Atualiza tambÃÂ©m dados da ÃÂ¡rea ativa se for a mesma
                if st.session_state.get("area_selecionada") == _id_area_atual:
                    st.session_state.dados["ph_pos_calagem"]      = _ph_novo
                    st.session_state.dados["calcario_aplicado_ha"] = round(
                        st.session_state.dados.get("calcario_aplicado_ha", 0) + _toneladas_calc, 2)
                salvar_dados_iaagro()
                success_box(f"Ã¢Åâ¦ {_toneladas_calc} t/ha de {_tipo_calc} registrado! pH estimado pÃÂ³s-calagem: {_ph_novo}")
                st.rerun()
                warning_box("Informe a quantidade aplicada.")

        # Ã¢ââ¬Ã¢ââ¬ Gesso aplicado Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        st.markdown("#### Ã°Å¸Â§Â± Gesso AgrÃÂ­cola")
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            _data_gesso = st.date_input("Data aplicaÃÂ§ÃÂ£o", key="date_gesso_aplic",
                                         value=datetime.now().date())
            _ton_gesso  = st.number_input("Quantidade aplicada (t/ha)", min_value=0.0,
                                           step=0.1, key="num_gesso_aplic")
        with col_g2:
            _tipo_gesso = st.selectbox("Tipo de gesso",
                ["Gesso AgrÃÂ­cola","FCA (Fosfogesso)","Outro"], key="sel_tipo_gesso")
            _pureza_gesso = st.number_input("Pureza CaSOÃ¢ââ (%)", min_value=0.0, max_value=100.0,
                                             value=85.0, step=1.0, key="num_pureza_gesso")
        with col_g3:
            _obs_gesso = st.text_input("ObservaÃÂ§ÃÂ£o", placeholder="Ex: Para subsolagem",
                                        key="txt_obs_gesso")
            _prof_gesso = st.selectbox("Profundidade alvo",
                ["0-20 cm","20-40 cm","40-60 cm","Superficial"], key="sel_prof_gesso")

        if st.button("Ã°Å¸âÂ¾ Registrar Gesso", key="btn_reg_gesso", use_container_width=True):
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
                # Atualiza gesso dentro da ÃÂ¡rea correta
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
                success_box(f"Ã¢Åâ¦ {_ton_gesso} t/ha de {_tipo_gesso} registrado!")
                st.rerun()
            else:
                warning_box("Informe a quantidade aplicada.")

        # Ã¢ââ¬Ã¢ââ¬ HistÃÂ³rico e status por ÃÂ¡rea Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        if _corretivos:
            import pandas as pd
            st.markdown("#### Ã°Å¸ââ¹ HistÃÂ³rico de Corretivos")

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
            col_s1.metric("Ã°Å¸ÂªÂ¨ CalcÃÂ¡rio aplicado", f"{_calc_total:.2f} t/ha",
                          delta=f"Rec: {_dose_rec} t/ha")
            col_s2.metric("Ã°Å¸Â§Â± Gesso aplicado", f"{_gesso_total:.2f} t/ha",
                          delta=f"Rec: {_dose_gesso_rec:.1f} t/ha")
            col_s3.metric("pH atual", f"{_ph_atual}")
            col_s4.metric("pH estimado pÃÂ³s-calagem", f"{_ph_pos}",
                          delta=f"+{round(_ph_pos-_ph_atual,1)}" if _ph_pos > _ph_atual else "sem aplicaÃÂ§ÃÂ£o")

            # Alertas
            if _calc_total < _dose_rec * 0.7:
                st.warning(f"Ã¢Å¡Â Ã¯Â¸Â CalcÃÂ¡rio aplicado ({_calc_total:.1f} t/ha) abaixo do recomendado ({_dose_rec} t/ha)")
            elif _calc_total >= _dose_rec:
                st.success(f"Ã¢Åâ¦ Meta de calagem atingida! ({_calc_total:.1f}/{_dose_rec} t/ha)")

            if _gesso_total < _dose_gesso_rec * 0.7 and _dose_gesso_rec > 0:
                st.warning(f"Ã¢Å¡Â Ã¯Â¸Â Gesso aplicado ({_gesso_total:.1f} t/ha) abaixo do recomendado ({_dose_gesso_rec:.1f} t/ha)")
            elif _gesso_total >= _dose_gesso_rec and _dose_gesso_rec > 0:
                st.success(f"Ã¢Åâ¦ Meta de gessagem atingida! ({_gesso_total:.1f}/{_dose_gesso_rec:.1f} t/ha)")

            # Tabela
            _cols_show = [c for c in ["data","tipo","produto","toneladas_ha","prnt","incorporado","obs"] if c in df_corr.columns]
            st.dataframe(df_corr[_cols_show].rename(columns={
                "data":"Data","tipo":"Tipo","produto":"Produto",
                "toneladas_ha":"t/ha","prnt":"PRNT%","incorporado":"Incorporado","obs":"Obs"
            }), use_container_width=True)

            # Excluir
            with st.expander("Ã°Å¸ââÃ¯Â¸Â Excluir registro"):
                _opts = [f"{c.get('data','')} Ã¢â¬â {c.get('produto','')} Ã¢â¬â {c.get('toneladas_ha',0)} t/ha"
                         for c in _corretivos]
                _del = st.selectbox("Selecione", _opts, key="sel_del_corretivo")
                if st.button("Ã°Å¸ââÃ¯Â¸Â Excluir", key="btn_del_corretivo"):
                    _idx = _opts.index(_del)
                    _all = [i for i,c in enumerate(st.session_state.corretivos_aplicados)
                            if c.get("area_id") == _id_area_atual]
                    st.session_state.corretivos_aplicados.pop(_all[_idx])
                    salvar_dados_iaagro()
                    success_box("Registro excluÃÂ­do!")
                    st.rerun()
        else:
            st.info("Ã°Å¸âÂ Nenhum corretivo registrado para esta ÃÂ¡rea ainda.")
    if "ph" not in d:
        warning_box("Preencha primeiro a AnÃÂ¡lise de Solo na aba Ã°Å¸Â§Âª AnÃÂ¡lise de Solo.")
    else:
        cultura      = d.get("cultura", "Soja")
        area         = d.get("area", 0)
        produtividade = d.get("produtividade", 0)
        fosforo      = d.get("fosforo", 0)
        potassio     = d.get("potassio", 0)
        ph           = d.get("ph", 0)
        materia_organica = d.get("materia_organica", 0)

        st.subheader("Ã°Å¸Â¤â IA Recomendando AdubaÃÂ§ÃÂ£o")

        # RecomendaÃÂ§ÃÂ£o por cultura
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
        elif cultura == "FeijÃÂ£o":
            p2o5 = 110 if fosforo < 10 else 80
            k2o  = 90  if potassio < 0.30 else 60
            n    = 40
        elif cultura == "Canola":
            p2o5 = 80; k2o = 70; n = 150
        elif cultura == "Aveia":
            p2o5 = 50; k2o = 40; n = 90
        elif cultura == "Cana-de-aÃÂ§ÃÂºcar":
            p2o5 = 100; k2o = 180; n = 140
        else:
            p2o5 = 60; k2o = 60; n = 80

        st.markdown(f'''<div style="background:#14532d;color:#ffffff;padding:15px 18px;border-radius:12px;
        border-left:5px solid #22c55e;font-size:15px;font-weight:600;line-height:2.0;margin:8px 0;">
        Ã°Å¸ÅÂ± <b>RecomendaÃÂ§ÃÂ£o IAAgro</b><br>
        Ã°Å¸Â§Âª NitrogÃÂªnio (N): {n} kg/ha<br>
        Ã°Å¸Â§Âª FÃÂ³sforo (P2O5): {p2o5} kg/ha<br>
        Ã°Å¸Â§Âª PotÃÂ¡ssio (K2O): {k2o} kg/ha
        </div>''', unsafe_allow_html=True)

        st.subheader("Ã°Å¸âÂ Taxa VariÃÂ¡vel Inteligente")
        zona = st.selectbox("Zona do talhÃÂ£o", ["Baixa Produtividade","MÃÂ©dia Produtividade","Alta Produtividade"], key="sel_zona_do_talh_o_3723")
        fator_zona = 0.85 if zona == "Baixa Produtividade" else (1.15 if zona == "Alta Produtividade" else 1.0)
        produtividade_ajustada = produtividade * fator_zona
        n    *= fator_zona
        p2o5 *= fator_zona
        k2o  *= fator_zona

        st.subheader("Dados da ÃÂrea")
        col1, col2, col3 = st.columns(3)
        col1.metric("Cultura", cultura)
        col2.metric("ÃÂrea", f"{area:.2f} ha")
        col3.metric("Meta Produtividade", f"{produtividade_ajustada:.1f} sc/ha")
        st.divider()

        st.subheader("RecomendaÃÂ§ÃÂ£o Base")
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
        col1.metric("NitrogÃÂªnio", f"{n:.1f} kg/ha", delta=f"{((fator_zona-1)*100):+.0f}%")
        col2.metric("PÃ¢ââOÃ¢ââ¦",      f"{p2o5:.1f} kg/ha", delta=f"{((fator_zona-1)*100):+.0f}%")
        col3.metric("KÃ¢ââO",       f"{k2o:.1f} kg/ha", delta=f"{((fator_zona-1)*100):+.0f}%")
        st.divider()

        st.subheader("Produtos Recomendados")
        map_ha_ajustado  = map_ha  * fator_zona
        kcl_ha_ajustado  = kcl_ha  * fator_zona
        ureia_ha_ajustado = ureia_ha * fator_zona
        col1, col2, col3 = st.columns(3)
        col1.metric("MAP 11-52-00", f"{map_ha_ajustado:.1f} kg/ha")
        col2.metric("KCl 00-00-60", f"{kcl_ha_ajustado:.1f} kg/ha")
        col3.metric("Ureia 45% N",  f"{ureia_ha_ajustado:.1f} kg/ha")

        st.subheader("Total para a ÃÂrea")
        total_map  = map_ha_ajustado  * area
        total_kcl  = kcl_ha_ajustado  * area
        total_ureia = ureia_ha_ajustado * area
        col1, col2, col3 = st.columns(3)
        col1.metric("MAP Total",   f"{total_map:.1f} kg")
        col2.metric("KCl Total",   f"{total_kcl:.1f} kg")
        col3.metric("Ureia Total", f"{total_ureia:.1f} kg")

        st.subheader("Ã°Å¸Å¡Å Enviar RecomendaÃÂ§ÃÂ£o para AplicaÃÂ§ÃÂ£o")
        if st.button("Gerar AplicaÃÂ§ÃÂ£o com RecomendaÃÂ§ÃÂ£o IA", key="gerar_aplicacao_ia"):
            nova_aplicacao = {
                "Data": str(date.today()),
                "ID ÃÂrea": st.session_state.dados.get("id_area",""),
                "TalhÃÂ£o": st.session_state.dados.get("talhao",""),
                "Cultura": cultura, "Tipo": "AdubaÃÂ§ÃÂ£o IA", "ÃÂrea ha": area,
                "Produtos": [
                    {"Insumo":"MAP 11-52-00","Dose ha":map_ha_ajustado,"Quantidade usada":total_map,"Unidade":"kg"},
                    {"Insumo":"KCL 00-00-60","Dose ha":kcl_ha_ajustado,"Quantidade usada":total_kcl,"Unidade":"kg"},
                    {"Insumo":"Ureia 45% N", "Dose ha":ureia_ha_ajustado,"Quantidade usada":total_ureia,"Unidade":"kg"},
                ]
            }
            st.session_state.aplicacoes.append(nova_aplicacao)
            salvar_dados_iaagro()
            success_box("AplicaÃÂ§ÃÂ£o de adubaÃÂ§ÃÂ£o IA enviada para o histÃÂ³rico!")
            st.subheader("Ã°Å¸Å¡Â¨ Alerta Inteligente de Estoque")
            for prod in [{"Insumo":"MAP 11-52-00","Necessario":total_map},
                         {"Insumo":"KCL 00-00-60","Necessario":total_kcl},
                         {"Insumo":"Ureia 45% N","Necessario":total_ureia}]:
                nome       = prod["Insumo"]
                necessario = prod["Necessario"]
                estoque_item = next((item for item in st.session_state.estoque if item["Insumo"] == nome), None)
                if estoque_item is None:
                    error_box(f"Ã¢ÂÅ {nome}: nÃÂ£o cadastrado no estoque.")
                elif necessario <= 0:
                    info_box(f"Ã¢âÂ¹Ã¯Â¸Â {nome}: nÃÂ£o necessÃÂ¡rio nesta recomendaÃÂ§ÃÂ£o.")
                elif estoque_item.get("Quantidade",0) >= necessario:
                    sobra = estoque_item["Quantidade"] - necessario
                    success_box(f"Ã¢Åâ¦ {nome}: estoque suficiente. NecessÃÂ¡rio: {necessario:.1f} | Sobra: {sobra:.1f} kg")
                else:
                    falta     = necessario - estoque_item["Quantidade"]
                    cobertura = (estoque_item["Quantidade"] / necessario) * 100
                    warning_box(f"Ã¢Å¡Â Ã¯Â¸Â {nome}: estoque insuficiente. Falta: {falta:.1f} kg | Cobertura: {cobertura:.0f}%")

        st.divider()
        st.subheader("Micronutrientes")
        recomendacoes_micro = []
        if d.get("boro",   0) < 0.3: recomendacoes_micro.append("Boro baixo: considerar aplicaÃÂ§ÃÂ£o de B.")
        if d.get("zinco",  0) < 1.0: recomendacoes_micro.append("Zinco baixo: considerar aplicaÃÂ§ÃÂ£o de Zn.")
        if d.get("manganes",0) < 5:  recomendacoes_micro.append("ManganÃÂªs baixo: monitorar Mn.")
        if d.get("cobre",  0) < 0.5: recomendacoes_micro.append("Cobre baixo: considerar aplicaÃÂ§ÃÂ£o de Cu.")
        if recomendacoes_micro:
            for rec in recomendacoes_micro: warning_box(rec)
        else:
            success_box("Micronutrientes em faixa aceitÃÂ¡vel.")

        st.divider()
        st.subheader("Salvar RecomendaÃÂ§ÃÂ£o")
        recomendacao_adubacao = {
            "Cultura": cultura, "ÃÂrea ha": area, "Produtividade alvo": produtividade,
            "N kg/ha": n_ha, "P2O5 kg/ha": p2o5_ha, "K2O kg/ha": k2o_ha,
            "MAP kg/ha": map_ha, "KCl kg/ha": kcl_ha, "Ureia kg/ha": ureia_ha,
            "MAP total kg": total_map, "KCl total kg": total_kcl, "Ureia total kg": total_ureia,
            "Micronutrientes": recomendacoes_micro
        }
        if st.button("Salvar RecomendaÃÂ§ÃÂ£o de AdubaÃÂ§ÃÂ£o", key="salvar_adubacao_inteligente"):
            st.session_state.dados["adubacao"] = recomendacao_adubacao
            atualizar_area_atual()
            salvar_dados_iaagro()
            success_box("RecomendaÃÂ§ÃÂ£o de adubaÃÂ§ÃÂ£o salva com sucesso.")

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: CUSTOS
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
elif menu == "Ã°Å¸âÂ° Financeiro":
    _sub_fin = st.tabs(["Ã°Å¸âÂ¸ Custos","Ã°Å¸âÂ¹ Dashboard Financeiro","Ã°Å¸âÅ  Comparativo de Safras","Ã°Å¸âÂµ Fluxo de Caixa","Ã°Å¸Â§Â¾ Imposto de Renda Rural"])

if menu == "Ã°Å¸âÂ° Financeiro":
  with _sub_fin[0]:
    st.header("Custos Estimados")
    d = st.session_state.dados

    # Busca dados da ÃÂ¡rea se session_state.dados nÃÂ£o tiver pH
    if "ph" not in d and st.session_state.areas:
        _id_s = st.session_state.get("area_selecionada")
        for _a in st.session_state.areas:
            _dad = _a.get("Dados", _a.get("dados", {}))
            if _dad and "ph" in _dad and (_id_s is None or _a.get("ID") == _id_s):
                d = {**_dad, "cultura": _a.get("Cultura","Soja"),
                     "area": _a.get("Hectares",0),
                     "produtividade": _a.get("Produtividade",50)}
                break
        if "ph" not in d:
            for _a in st.session_state.areas:
                _dad = _a.get("Dados", _a.get("dados", {}))
                if _dad and "ph" in _dad:
                    d = {**_dad, "cultura": _a.get("Cultura","Soja"),
                         "area": _a.get("Hectares",0),
                         "produtividade": _a.get("Produtividade",50)}
                    break

    if "ph" not in d:
        warning_box("Preencha primeiro Cadastro da ÃÂrea e AnÃÂ¡lise de Solo.")
    else:
        dose_calcario, total_calcario = calcular_calcario_por_ph(d["ph"], d["area"])
        precisa_gesso, dose_gesso, total_gesso, _ = calcular_gesso(d)

        preco_calcario    = st.number_input("PreÃÂ§o calcÃÂ¡rio R$/t",     min_value=0.0, value=180.0, key="num_pre_o_calc_rio__3860")
        frete_calcario    = st.number_input("Frete calcÃÂ¡rio R$/t",     min_value=0.0, value=50.0, key="num_frete_calc_rio__3861")
        aplicacao_calcario = st.number_input("AplicaÃÂ§ÃÂ£o calcÃÂ¡rio R$/ha", min_value=0.0, value=80.0, key="num_aplica__o_calc__3862")
        preco_gesso       = st.number_input("PreÃÂ§o gesso R$/t",        min_value=0.0, value=120.0, key="num_pre_o_gesso_r___3863")
        frete_gesso       = st.number_input("Frete gesso R$/t",        min_value=0.0, value=50.0, key="num_frete_gesso_r___3864")
        aplicacao_gesso   = st.number_input("AplicaÃÂ§ÃÂ£o gesso R$/ha",   min_value=0.0, value=70.0, key="num_aplica__o_gesso_3865")

        custo_total_calcario = (total_calcario * preco_calcario
                                + total_calcario * frete_calcario
                                + d["area"] * aplicacao_calcario)
        custo_total_gesso    = (total_gesso * preco_gesso
                                + total_gesso * frete_gesso
                                + d["area"] * aplicacao_gesso)

        st.divider()
        st.subheader("Ã°Å¸âÂ° Custos Complementares")
        custo_semente      = st.number_input("Custo sementes R$/ha",       min_value=0.0, step=1.0, key="num_custo_sementes__3876")
        custo_fertilizante = st.number_input("Custo fertilizantes R$/ha",  min_value=0.0, step=1.0, key="num_custo_fertiliza_3877")
        custo_defensivos   = st.number_input("Custo defensivos R$/ha",     min_value=0.0, step=1.0, key="num_custo_defensivo_3878")
        custo_diesel       = st.number_input("Custo diesel/mÃÂ¡quinas R$/ha", min_value=0.0, step=1.0, key="num_custo_diesel_m__3879")
        outros_custos      = st.number_input("Outros custos R$/ha",        min_value=0.0, step=1.0, key="num_outros_custos_r_3880")

        custo_operacional_total = (custo_semente + custo_fertilizante + custo_defensivos + custo_diesel + outros_custos) * d["area"]
        custo_total_safra       = custo_total_calcario + custo_total_gesso + custo_operacional_total
        custo_por_hectare       = custo_total_safra / d["area"] if d["area"] > 0 else 0

        st.divider()
        st.subheader("Ã°Å¸âÅ  Resumo Financeiro")
        st.metric("Custo Total Safra",    f"R$ {custo_total_safra:,.2f}")
        st.metric("Custo por Hectare",    f"R$ {custo_por_hectare:,.2f}/ha")

        if "produtividade" in d:
            preco_saca   = st.number_input("PreÃÂ§o da saca R$", min_value=0.0, step=1.0, key="num_pre_o_da_saca_r_3892")
            faturamento  = d["produtividade"] * preco_saca * d["area"]
            lucro        = faturamento - custo_total_safra
            margem       = (lucro / faturamento * 100) if faturamento > 0 else 0
            st.metric("Faturamento Estimado", f"R$ {faturamento:,.2f}")
            st.metric("Lucro Estimado",       f"R$ {lucro:,.2f}")
            st.metric("Margem Estimada",      f"{margem:.1f}%")


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
elif menu == "Ã°Å¸âÂ¦ Operacional":
    _sub_op = st.tabs(["Ã°Å¸âÂ¦ Estoque de Insumos","Ã°Å¸Å¡Å AplicaÃÂ§ÃÂµes","Ã¢ÂÂ±Ã¯Â¸Â Prazo de CarÃÂªncia","Ã°Å¸ââ¹ Ordem de ServiÃÂ§o","Ã°Å¸âÅ ReceituÃÂ¡rio AgronÃÂ´mico"])

if menu == "Ã°Å¸âÂ¦ Operacional":
  with _sub_op[0]:
    st.header("Ã°Å¸âÂ¦ Estoque de Insumos")

    # Ã¢ââ¬Ã¢ââ¬ TABS principais Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
    tab_manual, tab_nfe = st.tabs([
        "Ã¢Å¾â¢ Cadastrar Manualmente",
        "Ã°Å¸ââ Importar Nota Fiscal (XML)"
    ])

    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    with tab_nfe:
        st.subheader("Ã°Å¸ââ Importar Nota Fiscal EletrÃÂ´nica (XML)")
        st.info("Ã°Å¸âÅ½ FaÃÂ§a upload do XML da NF-e Ã¢â¬â todos os produtos entram no estoque automaticamente.")

        xml_file = st.file_uploader("Ã°Å¸âÅ½ Upload do XML da NF-e", type=["xml"], key="uploader_nfe")

        if xml_file:
            try:
                conteudo_xml = xml_file.read()
                root = ET.fromstring(conteudo_xml)

                def _strip_ns(tag):
                    return tag.split("}")[-1] if "}" in tag else tag

                def _find_all(node, tag):
                    return [c for c in node.iter() if _strip_ns(c.tag) == tag]

                def _find_text(node, tag, default=""):
                    els = _find_all(node, tag)
                    return els[0].text.strip() if els and els[0].text else default

                n_nf    = _find_text(root, "nNF",   "N/D")
                emit    = _find_text(root, "xNome", "Fornecedor nÃÂ£o identificado")
                dt_emis = _find_text(root, "dhEmi", _find_text(root, "dEmi", ""))
                dt_fmt  = dt_emis[:10] if dt_emis else "N/D"

                st.markdown(f"""
                <div style='background:#0f3460;border-radius:10px;padding:14px 18px;margin-bottom:12px;border:1px solid #22c55e'>
                <b style='color:#22c55e'>Ã°Å¸ââ¹ Nota Fiscal NÃÂº {n_nf}</b><br>
                <span style='color:#f1f5f9'>Emitente: {emit} &nbsp;|&nbsp; Data: {dt_fmt}</span>
                </div>
                """, unsafe_allow_html=True)

                uni_map = {
                    "KG":"kg","KGS":"kg","TON":"ton","T":"ton",
                    "L":"litros","LT":"litros","LTS":"litros",
                    "SC":"sacos","SAC":"sacos","UN":"unidades",
                    "UNI":"unidades","UND":"unidades","GAL":"galÃÂµes",
                }

                itens_nfe = []
                for det in _find_all(root, "det"):
                    prod = None
                    for child in det:
                        if _strip_ns(child.tag) == "prod":
                            prod = child
                            break
                    if prod is None:
                        continue
                    nome_prod = _find_text(prod, "xProd", "Produto sem nome")
                    qtd_prod  = float(_find_text(prod, "qCom",   "0").replace(",",".") or 0)
                    uni_prod  = _find_text(prod, "uCom",  "un")
                    vul_prod  = float(_find_text(prod, "vUnCom", "0").replace(",",".") or 0)
                    itens_nfe.append({
                        "Nome":             nome_prod,
                        "Quantidade":       qtd_prod,
                        "Unidade":          uni_map.get(uni_prod.upper(), "unidades"),
                        "Valor UnitÃÂ¡rio R$":vul_prod,
                        "Valor Total R$":   round(qtd_prod * vul_prod, 2),
                    })

                if not itens_nfe:
                    st.warning("Ã¢Å¡Â Ã¯Â¸Â Nenhum produto encontrado no XML.")
                else:
                    # Importa TODOS os itens automaticamente, sem botÃÂ£o, sem checkbox
                    adicionados = 0
                    for item in itens_nfe:
                        novo = {
                            "Insumo":            item["Nome"],
                            "Categoria":         "Outro",
                            "Quantidade":        item["Quantidade"],
                            "Unidade":           item["Unidade"],
                            "Valor UnitÃÂ¡rio R$": item["Valor UnitÃÂ¡rio R$"],
                            "Valor Total R$":    item["Valor Total R$"],
                            "Estoque MÃÂ­nimo":    0.0,
                            "ObservaÃÂ§ÃÂ£o":        f"NF-e nÃÂº {n_nf} Ã¢â¬â {emit} Ã¢â¬â {dt_fmt}",
                            "Cultura":           "Ambos",
                            "Dose ha":           0.0,
                            "Litros ha":         75.0,
                            "Tanque litros":     2000,
                            "Fabricante":        emit,
                            "Ingrediente Ativo": "",
                        }
                        st.session_state.estoque.append(novo)
                        adicionados += 1

                    salvar_dados_iaagro()

                    st.success(f"Ã¢Åâ¦ {adicionados} produto(s) da NF-e nÃÂº {n_nf} importados para o estoque!")
                    st.markdown("### Ã°Å¸âÂ¦ Produtos importados")
                    st.dataframe(pd.DataFrame(itens_nfe), use_container_width=True)
                    st.balloons()
                    st.rerun()

            except ET.ParseError as e:
                st.error(f"Ã¢ÂÅ Erro ao ler o XML: {e}")
            except Exception as e:
                st.error(f"Ã¢ÂÅ Erro inesperado: {e}")

    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    # TAB 1 Ã¢â¬â CADASTRO MANUAL (conteÃÂºdo original)
    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    with tab_manual:
        st.subheader("Ã¢Å¾â¢ Cadastrar Produto")

        # Ã¢ââ¬Ã¢ââ¬ CSS do autocomplete + tema escuro global Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        st.markdown("""
        <style>
        /* Ã¢ââ¬Ã¢ââ¬ Selectbox Ã¢â¬â fundo escuro igual ao upload Ã¢ââ¬Ã¢ââ¬ */
        div[data-baseweb="select"] > div {
            background-color: #0d1b2a !important;
            border: 2px solid #22c55e !important;
            border-radius: 10px !important;
            color: #f1f5f9 !important;
        }
        div[data-baseweb="select"] > div:focus-within {
            border-color: #4ade80 !important;
            box-shadow: 0 0 0 3px rgba(34,197,94,0.2) !important;
        }
        /* Texto dentro do selectbox */
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div {
            color: #f1f5f9 !important;
            background-color: transparent !important;
        }
        /* Dropdown do selectbox (lista de opÃÂ§ÃÂµes) */
        ul[data-baseweb="menu"],
        div[data-baseweb="popover"] > div,
        div[data-baseweb="menu"] {
            background-color: #0d1b2a !important;
            border: 2px solid #22c55e !important;
            border-radius: 10px !important;
        }
        /* Itens do selectbox */
        li[role="option"] {
            background-color: #0d1b2a !important;
            color: #f1f5f9 !important;
        }
        li[role="option"]:hover,
        li[role="option"][aria-selected="true"] {
            background-color: #0f3460 !important;
            border-left: 3px solid #22c55e !important;
            color: #6ee7b7 !important;
        }
        /* Ã¢ââ¬Ã¢ââ¬ Text input Ã¢â¬â fundo escuro Ã¢ââ¬Ã¢ââ¬ */
        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea {
            background-color: #0d1b2a !important;
            border: 2px solid #22c55e !important;
            border-radius: 10px !important;
            color: #f1f5f9 !important;
            caret-color: #22c55e !important;
        }
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stTextArea"] textarea:focus {
            border-color: #4ade80 !important;
            box-shadow: 0 0 0 3px rgba(34,197,94,0.2) !important;
        }
        div[data-testid="stTextInput"] input::placeholder,
        div[data-testid="stTextArea"] textarea::placeholder {
            color: #4a7b6f !important;
        }
        /* Ã¢ââ¬Ã¢ââ¬ Number input Ã¢ââ¬Ã¢ââ¬ */
        div[data-testid="stNumberInput"] input {
            background-color: #0d1b2a !important;
            border: 2px solid #22c55e !important;
            border-radius: 10px !important;
            color: #f1f5f9 !important;
        }
        div[data-testid="stNumberInput"] button {
            background-color: #0f3460 !important;
            border-color: #22c55e !important;
            color: #22c55e !important;
        }
        /* Ã¢ââ¬Ã¢ââ¬ Labels dos inputs Ã¢ââ¬Ã¢ââ¬ */
        div[data-testid="stTextInput"] label,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stNumberInput"] label,
        div[data-testid="stTextArea"] label {
            color: #22c55e !important;
            font-weight: 700 !important;
            font-size: 13px !important;
        }
        /* Ã¢ââ¬Ã¢ââ¬ BotÃÂµes gerais Ã¢ââ¬Ã¢ââ¬ */
        div[data-testid="stButton"] > button {
            background-color: #0f3460 !important;
            border: 2px solid #22c55e !important;
            border-radius: 10px !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 13px !important;
            transition: all 0.15s !important;
            text-shadow: none !important;
        }
        div[data-testid="stButton"] > button * {
            color: #ffffff !important;
            font-weight: 800 !important;
        }
        div[data-testid="stButton"] > button p {
            color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 13px !important;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #22c55e !important;
            color: #0d1b2a !important;
            border-color: #4ade80 !important;
        }
        div[data-testid="stButton"] > button:hover *,
        div[data-testid="stButton"] > button:hover p {
            color: #0d1b2a !important;
        }
        /* Ã¢ââ¬Ã¢ââ¬ BotÃÂ£o primÃÂ¡rio "Usar este produto" / "Analisar" Ã¢ââ¬Ã¢ââ¬ */
        div[data-testid="stButton"] > button[kind="primary"],
        div[data-testid="stButton"] > button.primary {
            background-color: #16a34a !important;
            border-color: #22c55e !important;
            color: #fff !important;
        }
        /* Ã¢ââ¬Ã¢ââ¬ Upload widget Ã¢ââ¬Ã¢ââ¬ */
        div[data-testid="stFileUploader"] > div {
            background-color: #0d1b2a !important;
            border: 2px dashed #22c55e !important;
            border-radius: 12px !important;
            color: #f1f5f9 !important;
        }
        div[data-testid="stFileUploader"] label {
            color: #22c55e !important;
            font-weight: 700 !important;
        }
        div[data-testid="stFileUploaderDropzone"] {
            background-color: #0d1b2a !important;
        }
        div[data-testid="stFileUploaderDropzone"] span,
        div[data-testid="stFileUploaderDropzone"] p {
            color: #94a3b8 !important;
        }
        /* Ã¢ââ¬Ã¢ââ¬ Checkbox Ã¢ââ¬Ã¢ââ¬ */
        div[data-testid="stCheckbox"] label {
            color: #f1f5f9 !important;
        }
        /* Ã¢ââ¬Ã¢ââ¬ Autocomplete dropdown HTML customizado Ã¢ââ¬Ã¢ââ¬ */
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
            border-left: 3px solid transparent;
            transition: all 0.12s;
            background: #0d1b2a;
        }
        .autocomplete-item:hover {
            background: #0f3460 !important;
            border-left: 3px solid #22c55e !important;
        }
        .autocomplete-item .prod-nome { font-size: 13px; font-weight: 600; color: #f1f5f9; }
        .autocomplete-item .prod-ia   { font-size: 10px; color: #93c5fd; margin-top: 2px; }
        .autocomplete-item .prod-badge {
            font-size: 10px; font-weight: 700; padding: 2px 8px;
            border-radius: 20px; white-space: nowrap; margin-left: 8px;
        }
        .badge-BASF       { background: #1e3a8a; color: #93c5fd; }
        .badge-Syngenta   { background: #14532d; color: #86efac; }
        .badge-Bayer      { background: #7f1d1d; color: #fca5a5; }
        .badge-UPL        { background: #78350f; color: #fcd34d; }
        .badge-Timac-Agro { background: #6b21a8; color: #f0abfc; }
        .badge-Mosaic     { background: #065f46; color: #6ee7b7; }
        .badge-Outros     { background: #1e293b; color: #94a3b8; }
        .autocomplete-header {
            padding: 6px 14px 4px; font-size: 10px; font-weight: 800;
            color: #22c55e; letter-spacing: 1px;
            border-bottom: 1px solid #0f3460;
        }
        /* Ã¢ââ¬Ã¢ââ¬ Scrollbar do dropdown Ã¢ââ¬Ã¢ââ¬ */
        .autocomplete-dropdown::-webkit-scrollbar { width: 5px; }
        .autocomplete-dropdown::-webkit-scrollbar-track { background: #0d1b2a; }
        .autocomplete-dropdown::-webkit-scrollbar-thumb { background: #22c55e; border-radius: 4px; }
        </style>
        """, unsafe_allow_html=True)
    
        # Ã¢ââ¬Ã¢ââ¬ Autocomplete via session_state Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        if "ac_query"       not in st.session_state: st.session_state.ac_query       = ""
        if "ac_selecionado" not in st.session_state: st.session_state.ac_selecionado = None
        if "ac_fab"         not in st.session_state: st.session_state.ac_fab         = "Todos"
    
        # Filtro por fabricante (botÃÂµes em linha)
        fabricantes = ["Todos", "BASF", "Syngenta", "Bayer", "UPL", "Timac Agro", "Mosaic",
                       "Corteva", "FMC", "ADAMA", "Ouro Fino", "Ihara", "Nortox", "Outros"]
        fab_cores = {
            "Todos":      ("#22c55e","#0f3460"),
            "BASF":       ("#93c5fd","#1e3a8a"),
            "Syngenta":   ("#86efac","#14532d"),
            "Bayer":      ("#fca5a5","#7f1d1d"),
            "UPL":        ("#fcd34d","#78350f"),
            "Timac Agro": ("#f0abfc","#6b21a8"),
            "Mosaic":     ("#6ee7b7","#065f46"),
            "Corteva":    ("#67e8f9","#164e63"),
            "FMC":        ("#a5b4fc","#1e1b4b"),
            "ADAMA":      ("#bef264","#365314"),
            "Ouro Fino":  ("#fde68a","#713f12"),
            "Ihara":      ("#f9a8d4","#4a044e"),
            "Nortox":     ("#5eead4","#134e4a"),
            "Outros":     ("#94a3b8","#1e293b"),
        }
    
        FAB_ESTILOS = {
            "Todos":      {"bg":"#166534", "border":"#22c55e", "emoji":"Ã°Å¸âÅ½"},
            "BASF":       {"bg":"#1e3a8a", "border":"#93c5fd", "emoji":"Ã°Å¸âÂµ"},
            "Syngenta":   {"bg":"#14532d", "border":"#86efac", "emoji":"Ã°Å¸Å¸Â¢"},
            "Bayer":      {"bg":"#7f1d1d", "border":"#fca5a5", "emoji":"Ã°Å¸âÂ´"},
            "UPL":        {"bg":"#92400e", "border":"#fcd34d", "emoji":"Ã°Å¸Å¸Â "},
            "Timac Agro": {"bg":"#6b21a8", "border":"#f0abfc", "emoji":"Ã°Å¸Å¸Â£"},
            "Mosaic":     {"bg":"#065f46", "border":"#6ee7b7", "emoji":"Ã°Å¸ÅÅ "},
            "Corteva":    {"bg":"#164e63", "border":"#67e8f9", "emoji":"Ã°Å¸âÂ·"},
            "FMC":        {"bg":"#1e1b4b", "border":"#a5b4fc", "emoji":"Ã°Å¸Å¸Â¦"},
            "ADAMA":      {"bg":"#365314", "border":"#bef264", "emoji":"Ã°Å¸ÅÂ¿"},
            "Ouro Fino":  {"bg":"#713f12", "border":"#fde68a", "emoji":"Ã°Å¸Å¸Â¡"},
            "Ihara":      {"bg":"#4a044e", "border":"#f9a8d4", "emoji":"Ã°Å¸ÅÂ¸"},
            "Nortox":     {"bg":"#134e4a", "border":"#5eead4", "emoji":"Ã°Å¸Åâ¬"},
            "Outros":     {"bg":"#374151", "border":"#9ca3af", "emoji":"Ã¢Å¡Âª"},
        }
    
        st.markdown("**Ã°Å¸ÂÂ­ Filtrar por Fabricante:**")
    
        # Renderiza todos os botÃÂµes como forms HTML Ã¢â¬â fundo e texto totalmente controlados
        cols_fab = st.columns(len(fabricantes)) if fabricantes else st.columns(1)
        for i, fab in enumerate(fabricantes):
            est   = FAB_ESTILOS[fab]
            ativo = st.session_state.ac_fab == fab
            bg    = est["bg"]
            borda = f'4px solid {est["border"]}' if ativo else f'2px solid {est["border"]}55'
            opac  = "1.0" if ativo else "0.65"
            sombra= f'0 0 10px {est["border"]}88' if ativo else "none"
            with cols_fab[i]:
                with st.form(key=f"form_fab_{fab}", border=False):
                    st.markdown(
                        f'<div style="'
                        f'background:{bg};'
                        f'border:{borda};'
                        f'border-radius:10px;'
                        f'padding:8px 4px;'
                        f'text-align:center;'
                        f'font-size:12px;'
                        f'font-weight:900;'
                        f'color:#ffffff;'
                        f'opacity:{opac};'
                        f'box-shadow:{sombra};'
                        f'letter-spacing:0.3px;'
                        f'margin-bottom:2px;'
                        f'">{est["emoji"]} {fab}</div>',
                        unsafe_allow_html=True
                    )
                    if st.form_submit_button("Ã¢Åâ", use_container_width=True):
                        st.session_state.ac_fab = fab
                        st.session_state.ac_query = ""
                        st.session_state.ac_selecionado = None
                        st.rerun()
    
        # Indicador visual do filtro ativo
        fab_ativo = st.session_state.ac_fab
        qtd_fab = len([p for p in CATALOGO_PRODUTOS if fab_ativo == "Todos" or p["fab"] == fab_ativo])
        st.markdown(f"""
        <div style="background:#0f3460;color:#93c5fd;padding:7px 14px;border-radius:8px;
        font-size:12px;font-weight:700;margin:4px 0 10px 0;">
        Ã°Å¸âÅ½ Fabricante ativo: <b>{fab_ativo}</b> Ã¢â¬â {qtd_fab} produtos disponÃÂ­veis
        </div>""", unsafe_allow_html=True)
    
        # Ã¢ââ¬Ã¢ââ¬ Campo de busca Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        query_input = st.text_input(
            "Ã°Å¸âÂ Nome comercial, ingrediente ativo ou categoria",
            value=st.session_state.ac_query,
            placeholder="Ex: Fox Xpro, glifosato, fungicida...",
            key="input_busca_produto"
        )
    
        if query_input != st.session_state.ac_query:
            st.session_state.ac_query = query_input
            if st.session_state.ac_selecionado and query_input != st.session_state.ac_selecionado["nome"]:
                st.session_state.ac_selecionado = None
    
        # Ã¢ââ¬Ã¢ââ¬ Filtra catÃÂ¡logo Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        catalogo_filtrado = CATALOGO_PRODUTOS if fab_ativo == "Todos" else [
            p for p in CATALOGO_PRODUTOS if p["fab"] == fab_ativo
        ]
    
        # Ã¢ââ¬Ã¢ââ¬ Mostra resultados ao digitar Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        if st.session_state.ac_query and not st.session_state.ac_selecionado:
            q = st.session_state.ac_query.lower()
            starts   = [p for p in catalogo_filtrado if p["nome"].lower().startswith(q)]
            contains = [p for p in catalogo_filtrado
                        if not p["nome"].lower().startswith(q)
                        and (q in p["nome"].lower() or q in p["ia"].lower() or q in p["cat"].lower())]
            resultados = (starts + contains)[:20]
    
            if resultados:
                FAB_EM = {"BASF":"Ã°Å¸âÂµ","Syngenta":"Ã°Å¸Å¸Â¢","Bayer":"Ã°Å¸âÂ´","UPL":"Ã°Å¸Å¸Â ",
                          "Timac Agro":"Ã°Å¸Å¸Â£","Mosaic":"Ã°Å¸ÅÅ ","Outros":"Ã¢Å¡Âª"}
                CAT_EM = {"Fungicida":"Ã°Å¸Ââ","Herbicida":"Ã°Å¸ÅÂ¿","Inseticida":"Ã°Å¸Ââº",
                          "Acaricida":"Ã°Å¸â¢Â·Ã¯Â¸Â","Nematicida":"Ã°Å¸ÂªÂ±","Fungicida BiolÃÂ³gico":"Ã°Å¸ÅÂ±",
                          "Inseticida BiolÃÂ³gico":"Ã°Å¸Â¦Â ","Foliar / NutriÃÂ§ÃÂ£o":"Ã°Å¸âÂ§",
                          "Tratamento de Sementes":"Ã°Å¸ÅÂ¾","Regulador de Crescimento":"Ã°Å¸âË",
                          "Adjuvante":"Ã¢Å¡âÃ¯Â¸Â","Fertilizante":"Ã°Å¸Â§Âª","Bioestimulante":"Ã¢ÅÂ¨"}
    
                st.markdown(f'<div style="background:#0f3460;color:#22c55e;padding:6px 14px;'
                            f'border-radius:8px 8px 0 0;font-size:11px;font-weight:800;letter-spacing:1px;">'
                            f'Ã°Å¸ÅÂ¿ {len(resultados)} RESULTADO{"S" if len(resultados)!=1 else ""} Ã¢â¬â clique para selecionar</div>',
                            unsafe_allow_html=True)
    
                # OpÃÂ§ÃÂµes formatadas para o radio
                opcoes_labels = []
                for p in resultados:
                    em_fab = FAB_EM.get(p["fab"], "Ã¢Å¡Âª")
                    em_cat = CAT_EM.get(p["cat"], "Ã°Å¸ÅÂ±")
                    opcoes_labels.append(f"{em_cat} {p['nome']}  |  {em_fab} {p['fab']}  ÃÂ·  {p['cat']}  Ã¢â¬â  {p['ia'][:50]}")
    
                escolha_idx = st.radio(
                    "Resultados:",
                    range(len(opcoes_labels)),
                    format_func=lambda i: opcoes_labels[i],
                    key="radio_produto_catalogo",
                    label_visibility="collapsed"
                )
    
                if st.button("Ã¢Åâ¦ Usar este produto", key="btn_usar_produto", use_container_width=True):
                    prod_sel = resultados[escolha_idx]
                    st.session_state.ac_selecionado = prod_sel
                    st.session_state.ac_query = prod_sel["nome"]
                    # ForÃÂ§a preenchimento dos campos via session_state
                    st.session_state["nome_insumo_final"] = prod_sel["nome"]
                    cat_map_tmp = {
                        "Fungicida":"Fungicida","Herbicida":"Herbicida","Inseticida":"Inseticida",
                        "Acaricida":"Outro","Nematicida":"Outro","Fungicida BiolÃÂ³gico":"BiolÃÂ³gico",
                        "Inseticida BiolÃÂ³gico":"BiolÃÂ³gico","Bioestimulante":"Foliar",
                        "Foliar / NutriÃÂ§ÃÂ£o":"Foliar","Regulador de Crescimento":"Outro",
                        "Adjuvante":"Adjuvante","Tratamento de Sementes":"Outro",
                        "Fertilizante":"Fertilizante",
                    }
                    st.rerun()
    
            else:
                st.markdown(f'<div style="background:#1e293b;color:#f87171;padding:10px 14px;'
                            f'border-radius:8px;font-size:13px;font-weight:600;margin:4px 0;">'
                            f'Ã¢ÂÅ Nenhum produto encontrado para "<b>{st.session_state.ac_query}</b>"</div>',
                            unsafe_allow_html=True)
    
        # Card do produto selecionado
        if st.session_state.ac_selecionado:
            p = st.session_state.ac_selecionado
            fab_bg = {"BASF":"#1e3a8a","Syngenta":"#14532d","Bayer":"#7f1d1d","UPL":"#78350f","Timac Agro":"#6b21a8","Mosaic":"#065f46","Outros":"#1e293b"}.get(p["fab"],"#1e293b")
            fab_tx = {"BASF":"#93c5fd","Syngenta":"#86efac","Bayer":"#fca5a5","UPL":"#fcd34d","Timac Agro":"#f0abfc","Mosaic":"#6ee7b7","Outros":"#94a3b8"}.get(p["fab"],"#94a3b8")
            fab_em = {"BASF":"Ã°Å¸âÂµ","Syngenta":"Ã°Å¸Å¸Â¢","Bayer":"Ã°Å¸âÂ´","UPL":"Ã°Å¸Å¸Â ","Timac Agro":"Ã°Å¸Å¸Â£","Mosaic":"Ã°Å¸ÅÅ ","Outros":"Ã¢Å¡Âª"}.get(p["fab"],"Ã¢Å¡Âª")
            cat_em = {"Fungicida":"Ã°Å¸Ââ","Herbicida":"Ã°Å¸ÅÂ¿","Inseticida":"Ã°Å¸Ââº","Acaricida":"Ã°Å¸â¢Â·Ã¯Â¸Â",
                      "Tratamento de Sementes":"Ã°Å¸ÅÂ¾","Foliar / NutriÃÂ§ÃÂ£o":"Ã°Å¸âÂ§",
                      "Regulador de Crescimento":"Ã°Å¸âË","Adjuvante":"Ã¢Å¡âÃ¯Â¸Â","Nematicida":"Ã°Å¸ÂªÂ±",
                      "Inseticida BiolÃÂ³gico":"Ã°Å¸Â¦Â ","Bioestimulante":"Ã¢ÅÂ¨"}.get(p["cat"],"Ã°Å¸ÅÂ±")
            st.markdown(f"""
            <div style="background:{fab_bg};border:2px solid {fab_tx}33;border-radius:12px;
            padding:12px 16px;margin:6px 0 12px 0;display:flex;align-items:center;gap:12px;">
                <div style="font-size:26px;">{cat_em}</div>
                <div style="flex:1;">
                    <div style="color:#ffffff;font-weight:800;font-size:15px;">{p['nome']}</div>
                    <div style="color:{fab_tx};font-size:12px;margin-top:3px;">{fab_em} {p['fab']} ÃÂ· {p['cat']}</div>
                    <div style="color:#94a3b8;font-size:11px;margin-top:2px;">I.A.: {p['ia']}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    
            if st.button("Ã°Å¸ââ Trocar produto", key="btn_trocar_produto"):
                st.session_state.ac_selecionado = None
                st.session_state.ac_query = ""
                st.rerun()
    
            nome_insumo = p["nome"]
            # Mapeia categoria do catÃÂ¡logo para categoria do estoque
            cat_map = {
                "Fungicida":"Fungicida","Herbicida":"Herbicida","Inseticida":"Inseticida",
                "Acaricida":"Outro","Nematicida":"Outro","Fungicida BiolÃÂ³gico":"BiolÃÂ³gico",
                "Inseticida BiolÃÂ³gico":"BiolÃÂ³gico","Bioestimulante":"Foliar",
                "Foliar / NutriÃÂ§ÃÂ£o":"Foliar","Regulador de Crescimento":"Outro",
                "Adjuvante":"Adjuvante","Tratamento de Sementes":"Outro",
                "Fertilizante":"Fertilizante",
            }
            cat_sugerida = cat_map.get(p["cat"], "Outro")
        else:
            nome_insumo  = st.session_state.ac_query if st.session_state.ac_query else ""
            cat_sugerida = "Fungicida"
    
        # Ã¢ââ¬Ã¢ââ¬ Campos complementares Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            # PrÃÂ©-preenche via session_state quando produto ÃÂ© selecionado do catÃÂ¡logo
            if "nome_insumo_final" not in st.session_state:
                st.session_state["nome_insumo_final"] = nome_insumo
            elif nome_insumo and st.session_state.get("ac_selecionado"):
                st.session_state["nome_insumo_final"] = nome_insumo
            nome_final = st.text_input("Nome do produto / insumo", key="nome_insumo_final")
            _cats = ["Fertilizante","Cloreto de PotÃÂ¡ssio","Ureia","Fungicida","Inseticida",
                     "Herbicida","BiolÃÂ³gico","Foliar","Semente","CalcÃÂ¡rio","Gesso AgrÃÂ­cola","Adjuvante","Outro"]
            _cat_idx = _cats.index(cat_sugerida) if cat_sugerida in _cats else 0
            categoria  = st.selectbox("Categoria", _cats, index=_cat_idx, key="sel_categoria_estoque")
            cultura    = st.selectbox("Cultura", get_culturas() + ["Ambos"], key="cultura_estoque")
            litros_ha  = st.number_input("Litros de calda por hectare", min_value=0.0, value=75.0, key="litros_ha_estoque")
            dose_ha    = st.number_input("Dose por hectare (kg/L)", min_value=0.0, value=0.0, key="dose_ha_estoque")
            capacidade_tanque = st.number_input("Capacidade do tanque (L)", min_value=0,
                                                   value=int(st.session_state.dados.get("cap_tanque_salva", 2000)),
                                                   key="tanque_estoque",
                                                   help="Ã°Å¸âÂ¾ Salvo automaticamente")
            if capacidade_tanque != st.session_state.dados.get("cap_tanque_salva", 2000) and capacidade_tanque > 0:
                st.session_state.dados["cap_tanque_salva"] = capacidade_tanque
                salvar_dados_iaagro()
        with col2:
            quantidade  = st.number_input("Quantidade em estoque", min_value=0.0, value=0.0, key="num_quantidade_em_e_4611")
            unidade     = st.selectbox("Unidade do estoque", ["kg","litros","ton","sacos","galÃÂµes","unidades"], key="sel_unidade_do_esto_4612")

            # Embalagem baseada na unidade
            if unidade == "kg":
                embalagem_opts = ["1 kg","2 kg","5 kg","10 kg","15 kg","20 kg","25 kg","30 kg","50 kg","Granel"]
            elif unidade == "litros":
                embalagem_opts = ["200 ml","500 ml","1 litro","2 litros","5 litros","10 litros","20 litros","200 litros","Granel"]
            elif unidade == "sacos":
                embalagem_opts = ["Saco 20 kg","Saco 25 kg","Saco 40 kg","Saco 50 kg","Saco 60 kg"]
            elif unidade == "ton":
                embalagem_opts = ["Big Bag 500 kg","Big Bag 1000 kg","Granel tonelada"]
            elif unidade == "galÃÂµes":
                embalagem_opts = ["GalÃÂ£o 5L","GalÃÂ£o 10L","GalÃÂ£o 20L","GalÃÂ£o 50L"]
            else:
                embalagem_opts = ["Unidade","Caixa","Fardo","Par"]

            embalagem = st.selectbox("Embalagem / ApresentaÃÂ§ÃÂ£o", embalagem_opts, key="sel_embalagem_estoque")
        with col3:
            valor_unitario = st.number_input("Valor unitÃÂ¡rio R$", min_value=0.0, value=0.0, key="num_valor_unit_rio__4614")
            estoque_minimo = st.number_input("Estoque mÃÂ­nimo", min_value=0.0, value=0.0, key="num_estoque_m_nimo_4615")
    
        observacao = st.text_area("ObservaÃÂ§ÃÂ£o", key="txa_observa__o_4617")
    
        _pode_est, _usado_est, _limite_est = verificar_limite("estoque")
        if not _pode_est:
            bloco_upgrade("estoque", _usado_est, _limite_est)
        elif st.button("Adicionar Produto ao Estoque"):
            nome_usar = nome_final.strip() if nome_final.strip() else nome_insumo.strip()
            if not nome_usar:
                error_box("Digite ou selecione o nome do produto.")
            else:
                # Verifica se produto jÃÂ¡ existe Ã¢â¬â se sim, soma quantidade e valor
                existente = next((i for i in st.session_state.estoque
                                  if i.get("Insumo","").strip().lower() == nome_usar.lower()), None)
                if existente:
                    existente["Quantidade"]      = existente.get("Quantidade", 0) + quantidade
                    existente["Valor Total R$"]  = existente["Quantidade"] * existente.get("Valor UnitÃÂ¡rio R$", valor_unitario)
                    if valor_unitario > 0:
                        existente["Valor UnitÃÂ¡rio R$"] = valor_unitario
                    if estoque_minimo > 0:
                        existente["Estoque MÃÂ­nimo"] = estoque_minimo
                    salvar_dados_iaagro()
                    success_box(f"Ã¢Åâ¦ Estoque de **{nome_usar}** atualizado! Nova quantidade: {existente['Quantidade']:.1f} {existente.get('Unidade','')}")
                else:
                    novo_item = {
                        "Insumo": nome_usar, "Categoria": categoria,
                        "Quantidade": quantidade, "Unidade": unidade,
                        "Embalagem": embalagem,
                        "Valor UnitÃÂ¡rio R$": valor_unitario,
                        "Valor Total R$": quantidade * valor_unitario,
                        "Estoque MÃÂ­nimo": estoque_minimo,
                        "ObservaÃÂ§ÃÂ£o": observacao, "Cultura": cultura,
                        "Dose ha": dose_ha, "Litros ha": litros_ha,
                        "Tanque litros": capacidade_tanque,
                        "Fabricante": st.session_state.ac_selecionado["fab"] if st.session_state.ac_selecionado else "",
                        "Ingrediente Ativo": st.session_state.ac_selecionado["ia"] if st.session_state.ac_selecionado else "",
                    }
                    st.session_state.estoque.append(novo_item)
                    salvar_dados_iaagro()
                    success_box(f"Ã¢Åâ¦ {nome_usar} adicionado ao estoque.")
                # Reseta autocomplete apÃÂ³s adicionar
                st.session_state.ac_selecionado = None
                st.session_state.ac_query = ""
    
        st.subheader("Estoque Atual")
        if len(st.session_state.estoque) == 0:
            info_box("Nenhum produto cadastrado ainda.")
        else:
            tabela_estoque = pd.DataFrame(st.session_state.estoque)
            # Garante coluna Embalagem mesmo em registros antigos
            if "Embalagem" not in tabela_estoque.columns:
                tabela_estoque["Embalagem"] = "Ã¢â¬â"
            else:
                tabela_estoque["Embalagem"] = tabela_estoque["Embalagem"].fillna("Ã¢â¬â")
    
            st.markdown("### Ã°Å¸ââÃ¯Â¸Â Excluir Produto")
            produto_excluir = st.selectbox(
                "Selecione o produto",
                [item["Insumo"] for item in st.session_state.estoque],
                key="produto_excluir_estoque"
            )
            if st.button("Ã¢ÂÅ Excluir Produto", key="btn_excluir_produto"):
                st.session_state.estoque = [i for i in st.session_state.estoque if i["Insumo"] != produto_excluir]
                salvar_dados_iaagro()
                success_box(f"{produto_excluir} removido do estoque.")
                st.rerun()
    
            tabela_estoque["Status"] = tabela_estoque.apply(
                lambda linha: "Estoque baixo" if linha["Quantidade"] <= linha["Estoque MÃÂ­nimo"] else "OK", axis=1
            )
            st.dataframe(tabela_estoque, use_container_width=True)
    
            st.subheader("Ã°Å¸Å¡Â¨ Alertas Inteligentes")
            for item in st.session_state.estoque:
                qtd  = item.get("Quantidade", 0)
                nome = item.get("Insumo", "Produto")
                if   qtd <= 0:   error_box(f"Ã¢ÂÅ {nome}: estoque zerado!")
                elif qtd <= 500: warning_box(f"Ã¢Å¡Â Ã¯Â¸Â {nome}: estoque baixo ({qtd:.1f} kg/L)")
                else:            success_box(f"Ã¢Åâ¦ {nome}: estoque OK ({qtd:.1f} kg/L)")
    
            col4, col5, col6 = st.columns(3)
            col4.metric("Itens cadastrados",      len(tabela_estoque))
            col5.metric("Valor total em estoque", f"R$ {tabela_estoque['Valor Total R$'].sum():,.2f}")
            col6.metric("Itens com estoque baixo", len(tabela_estoque[tabela_estoque["Status"] == "Estoque baixo"]))
    
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: APLICAÃâ¡Ãâ¢ES
# CORREÃâ¡Ãâ¢ES:
#   - operador/pulverizador/velocidade/pressao/clima movidos para fora do loop
#   - loop aninhado duplicado removido
#   - key duplicada no botÃÂ£o corrigida com ÃÂ­ndice ÃÂºnico
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸âÂ¦ Operacional":
  with _sub_op[1]:
    st.header("Ã°Å¸Å¡Å AplicaÃÂ§ÃÂµes AgrÃÂ­colas")

    if "aplicacoes" not in st.session_state:
        st.session_state.aplicacoes = []

    ESTADIOS = [
        "Ã°Å¸ÅÂ± PrÃÂ©-plantio","Ã°Å¸ÅÂ¿ PÃÂ³s-plantio / V0","Ã°Å¸ÅÂ¾ V1 Ã¢â¬â V3","Ã°Å¸ÅÂ¾ V4 Ã¢â¬â V6",
        "Ã°Å¸ÅÂ¾ V7 Ã¢â¬â VT","Ã°Å¸ÅÂ¸ R1 Ã¢â¬â R2 (FloraÃÂ§ÃÂ£o)","Ã°Å¸Â«Ë R3 Ã¢â¬â R4 (GranaÃÂ§ÃÂ£o)",
        "Ã°Å¸Â«Ë R5 Ã¢â¬â R6","Ã°Å¸ÅÂ¾ PrÃÂ©-colheita","Ã°Å¸ââ¹ Outro",
    ]
    TIPOS_PRODUTO = ["Herbicida","Fungicida","Inseticida","Adjuvante",
                     "Ãâleo mineral/vegetal","Fertilizante foliar","Regulador","Outro"]

    if len(st.session_state.estoque) == 0:
        warning_box("Cadastre produtos no estoque antes de registrar aplicaÃÂ§ÃÂµes.")
    else:
        st.subheader("Ã¢Å¾â¢ Nova AplicaÃÂ§ÃÂ£o")
        col_h1, col_h2, col_h3 = st.columns(3)
        with col_h1:
            estadio_sel = st.selectbox("Ã°Å¸ââ¦ EstÃÂ¡dio fenolÃÂ³gico", ESTADIOS, key="sel_estadio_aplic")
            # Nome automÃÂ¡tico conforme estÃÂ¡dio Ã¢â¬â sÃÂ³ pede digitaÃÂ§ÃÂ£o se "Outro"
            if estadio_sel == "Ã°Å¸ââ¹ Outro":
                nome_aplic = st.text_input("Nome da aplicaÃÂ§ÃÂ£o", placeholder="Ex: AplicaÃÂ§ÃÂ£o especial",
                                            key="txt_nome_aplic")
            else:
                nome_aplic = estadio_sel
                st.info(f"Ã°Å¸ââ¹ Nome: **{nome_aplic}**")
        with col_h2:
            data_aplic = st.date_input("Data", key="dat_data_aplic")
            area_aplic = st.number_input("ÃÂrea (ha)", min_value=0.0,
                                          value=float(st.session_state.dados.get("area", 0.0)),
                                          key="num_area_aplic")
        with col_h3:
            calda_lha  = st.number_input("Volume calda (L/ha)", min_value=0.0, value=100.0, key="num_calda_lha")
            # Carrega capacidade salva ou usa padrÃÂ£o 3000L
            _cap_salva = st.session_state.dados.get("cap_tanque_salva", 3000.0)
            cap_tanque = st.number_input("Capacidade tanque (L)", min_value=0.0,
                                          value=float(_cap_salva), key="num_cap_tanque",
                                          help="Ã°Å¸âÂ¾ Salvo automaticamente para prÃÂ³ximas aplicaÃÂ§ÃÂµes")
            # Salva automaticamente quando muda
            if cap_tanque != _cap_salva and cap_tanque > 0:
                st.session_state.dados["cap_tanque_salva"] = cap_tanque
                salvar_dados_iaagro()
                st.caption(f"Ã¢Åâ¦ Tanque de {cap_tanque:.0f}L salvo!")

        area_por_tanque = round(cap_tanque / calda_lha, 2) if calda_lha > 0 else 0
        n_tanques       = round(area_aplic / area_por_tanque, 2) if area_por_tanque > 0 else 0
        col_m1, col_m2  = st.columns(2)
        col_m1.metric("Ã°Å¸âÂ ÃÂrea por tanque", f"{area_por_tanque} ha")
        col_m2.metric("Ã°Å¸ÂªÂ£ NÃÂº de tanques",   f"{n_tanques}")

        with st.expander("Ã°Å¸Â§âÃ¢â¬ÂÃ°Å¸ÅÂ¾ Dados do operador", expanded=False):
            col_o1, col_o2, col_o3 = st.columns(3)
            operador     = col_o1.text_input("Operador", key="txt_operador_aplic")
            pulverizador = col_o2.text_input("Pulverizador/MÃÂ¡quina", key="txt_pulv_aplic")
            velocidade   = col_o1.number_input("Velocidade (km/h)", min_value=0.0, key="num_veloc_aplic")
            pressao      = col_o2.number_input("PressÃÂ£o (bar)", min_value=0.0, key="num_pressao_aplic")
            clima_aplic  = col_o3.selectbox("Clima", ["Adequado","Vento alto","Muito seco","Chuva prÃÂ³xima","Muito quente"], key="sel_clima_aplic")

        st.subheader("Ã°Å¸Â§Âª Produtos da AplicaÃÂ§ÃÂ£o")
        st.caption("Adicione quantos produtos precisar: herbicida, fungicida, adjuvante, ÃÂ³leo, etc.")
        _nomes_estoque = [item["Insumo"] for item in st.session_state.estoque]
        n_produtos = int(st.number_input("Quantidade de produtos", min_value=1, max_value=10, value=1, step=1, key="num_qtd_produtos_aplic"))

        produtos_aplic = []
        for i in range(n_produtos):
            st.markdown(f"**Produto {i+1}**")
            col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns([3,2,1,1,2])
            _prod  = col_p1.selectbox("Produto",   _nomes_estoque,      key=f"sel_prod_aplic_{i}")
            _tipo_p= col_p2.selectbox("Tipo",       TIPOS_PRODUTO,       key=f"sel_tipo_prod_{i}")
            _dose  = col_p3.number_input("Dose/ha", min_value=0.0,       key=f"num_dose_aplic_{i}")
            _unid  = col_p4.selectbox("Un.",        ["L/ha","mL/ha","kg/ha","g/ha"], key=f"sel_unid_aplic_{i}")
            _obs_p = col_p5.text_input("Obs.",      placeholder="adjuvante, sequÃÂªncia...", key=f"txt_obs_prod_{i}")
            _por_tanque = round(_dose * area_por_tanque, 3)
            _total_prod = round(_dose * area_aplic, 3)
            if _dose > 0:
                st.caption(f"  Ã¢â â {_por_tanque} {_unid.replace('/ha','')} por tanque | Total: {_total_prod} {_unid.replace('/ha','')}")
            produtos_aplic.append({
                "Produto": _prod, "Tipo": _tipo_p, "Dose por ha": _dose, "Unidade": _unid,
                "Produto por tanque": _por_tanque, "Total usado": _total_prod, "ObservaÃÂ§ÃÂ£o": _obs_p
            })

        if st.button("Ã°Å¸âÂ¾ Salvar AplicaÃÂ§ÃÂ£o", key="salvar_aplicacao_modelada", use_container_width=True):
            erro = False
            if not nome_aplic.strip(): error_box("Informe o nome da aplicaÃÂ§ÃÂ£o."); erro = True
            if area_aplic <= 0:        error_box("Informe a ÃÂ¡rea aplicada."); erro = True
            for p in produtos_aplic:
                if p["Dose por ha"] <= 0: error_box(f"Dose zero: {p['Produto']}."); erro = True
            if not erro:
                for p in produtos_aplic:
                    s, m = baixar_estoque(p["Produto"], p["Total usado"], p.get("Unidade","L/ha"))
                    if not s: error_box(f"{p['Produto']}: {m}"); erro = True
            if not erro:
                st.session_state.aplicacoes.append({
                    "ID ÃÂrea":             st.session_state.dados.get("id_area",""),
                    "EstÃÂ¡dio":             estadio_sel,
                    "AplicaÃÂ§ÃÂ£o":           nome_aplic,
                    "Data":                str(data_aplic),
                    "ÃÂrea aplicada ha":    area_aplic,
                    "Volume calda L/ha":   calda_lha,
                    "Capacidade tanque L": cap_tanque,
                    "ÃÂrea por tanque ha":  area_por_tanque,
                    "NÃÂºmero tanques":      n_tanques,
                    "Operador":            operador,
                    "Pulverizador":        pulverizador,
                    "Velocidade km/h":     velocidade,
                    "PressÃÂ£o bar":         pressao,
                    "Clima aplicaÃÂ§ÃÂ£o":     clima_aplic,
                    "Produtos":            produtos_aplic
                })
                atualizar_area_atual()
                salvar_dados_iaagro()
                success_box(f"Ã¢Åâ¦ {nome_aplic} salva! {len(produtos_aplic)} produto(s).")
                st.rerun()

        st.divider()
        st.subheader("Ã°Å¸ââ¹ HistÃÂ³rico de AplicaÃÂ§ÃÂµes")

        # BotÃÂ£o PDF de programaÃÂ§ÃÂ£o
        if st.session_state.aplicacoes:
            _d = st.session_state.dados
            if st.button("Ã°Å¸ââ Gerar PDF Ã¢â¬â ProgramaÃÂ§ÃÂ£o de AplicaÃÂ§ÃÂµes",
                         key="btn_gerar_pdf_aplic", use_container_width=True):
                try:
                    _pdf_bytes = gerar_pdf_programacao_aplicacoes(
                        aplicacoes = st.session_state.aplicacoes,
                        fazenda    = _d.get("fazenda",""),
                        talhao     = _d.get("talhao",""),
                        cultura    = cultura_limpa(_d.get("cultura","")),
                        area_ha    = _d.get("area",0),
                        operador   = _d.get("operador",""),
                    )
                    st.session_state["_pdf_aplic"] = _pdf_bytes
                    st.success("Ã¢Åâ¦ PDF gerado! Clique em Baixar abaixo.")
                except Exception as e:
                    st.error(f"Erro ao gerar PDF: {e}")

            if st.session_state.get("_pdf_aplic"):
                st.download_button(
                    label       = "Ã¢Â¬â¡Ã¯Â¸Â Baixar PDF",
                    data        = st.session_state["_pdf_aplic"],
                    file_name   = f"programacao_aplicacoes_{datetime.now().strftime('%d%m%Y')}.pdf",
                    mime        = "application/pdf",
                    use_container_width = True,
                    key         = "btn_download_pdf_aplic"
                )
        if len(st.session_state.aplicacoes) == 0:
            info_box("Nenhuma aplicaÃÂ§ÃÂ£o registrada ainda.")
        else:
            _ordem = {"Ã°Å¸ÅÂ± PrÃÂ©-plantio":1,"Ã°Å¸ÅÂ¿ PÃÂ³s-plantio / V0":2,"Ã°Å¸ÅÂ¾ V1 Ã¢â¬â V3":3,
                      "Ã°Å¸ÅÂ¾ V4 Ã¢â¬â V6":4,"Ã°Å¸ÅÂ¾ V7 Ã¢â¬â VT":5,"Ã°Å¸ÅÂ¸ R1 Ã¢â¬â R2 (FloraÃÂ§ÃÂ£o)":6,
                      "Ã°Å¸Â«Ë R3 Ã¢â¬â R4 (GranaÃÂ§ÃÂ£o)":7,"Ã°Å¸Â«Ë R5 Ã¢â¬â R6":8,"Ã°Å¸ÅÂ¾ PrÃÂ©-colheita":9}
            aplicacoes_ordenadas = sorted(st.session_state.aplicacoes,
                key=lambda x: _ordem.get(x.get("EstÃÂ¡dio", x.get("AplicaÃÂ§ÃÂ£o","")), 99))

            for idx_a, aplic in enumerate(aplicacoes_ordenadas):
                _status = aplic.get("Status", "pendente")
                _cor_card = "#14532d" if _status == "aplicado" else "#1e3a5f"
                _badge    = "Ã¢Åâ¦ Aplicado" if _status == "aplicado" else "Ã¢ÂÂ³ Pendente"

                with st.expander(f"{aplic.get('EstÃÂ¡dio','') or aplic.get('AplicaÃÂ§ÃÂ£o','')} Ã¢â¬â {aplic.get('Data','')} | {_badge}", expanded=False):
                    col_i1, col_i2 = st.columns(2)
                    col_i1.markdown(f"**ÃÂrea:** {aplic.get('ÃÂrea aplicada ha',0)} ha")
                    col_i1.markdown(f"**Calda:** {aplic.get('Volume calda L/ha',0)} L/ha")
                    col_i1.markdown(f"**Tanques:** {aplic.get('NÃÂºmero tanques',0):.1f}")
                    col_i2.markdown(f"**Operador:** {aplic.get('Operador','Ã¢â¬â')}")
                    col_i2.markdown(f"**Pulverizador:** {aplic.get('Pulverizador','Ã¢â¬â')}")
                    col_i2.markdown(f"**Clima:** {aplic.get('Clima aplicaÃÂ§ÃÂ£o','Ã¢â¬â')}")

                    # Produtos
                    st.markdown("**Ã°Å¸Â§Âª Produtos:**")
                    _prods = aplic.get("Produtos", [])
                    for p in _prods:
                        st.markdown(f"- **{p.get('Produto','')}** ({p.get('Tipo','')}) Ã¢â¬â "
                                    f"{p.get('Dose por ha',0)} {p.get('Unidade','')} | "
                                    f"Total: {p.get('Total usado',0)} {p.get('Unidade','').replace('/ha','')}")

                    col_b1, col_b2 = st.columns(2)

                    # BotÃÂ£o confirmar aplicaÃÂ§ÃÂ£o e dar baixa no estoque
                    if _status != "aplicado":
                        if col_b1.button("Ã¢Åâ¦ Confirmar AplicaÃÂ§ÃÂ£o (dÃÂ¡ baixa no estoque)",
                                          key=f"btn_confirmar_aplic_{idx_a}", use_container_width=True):
                            _erro_baixa = False
                            for p in _prods:
                                s, m = baixar_estoque(p["Produto"], p.get("Total usado", 0), p.get("Unidade","L/ha"))
                                if not s:
                                    st.warning(f"Ã¢Å¡Â Ã¯Â¸Â {p['Produto']}: {m}")
                                    _erro_baixa = True
                            # Marca como aplicado
                            _idx_orig = st.session_state.aplicacoes.index(aplic)
                            st.session_state.aplicacoes[_idx_orig]["Status"] = "aplicado"
                            salvar_dados_iaagro()
                            if not _erro_baixa:
                                success_box(f"Ã¢Åâ¦ AplicaÃÂ§ÃÂ£o confirmada! Estoque atualizado.")
                            else:
                                success_box("AplicaÃÂ§ÃÂ£o marcada. Verifique o estoque manualmente.")
                            st.rerun()
                    else:
                        col_b1.success("Ã¢Åâ¦ JÃÂ¡ confirmada e baixa dada no estoque")

                    # BotÃÂ£o excluir
                    if col_b2.button("Ã°Å¸ââÃ¯Â¸Â Excluir", key=f"apagar_app_{idx_a}", use_container_width=True):
                        _idx_orig = st.session_state.aplicacoes.index(aplic)
                        st.session_state.aplicacoes.pop(_idx_orig)
                        salvar_dados_iaagro()
                        st.rerun()

  with _sub_op[2]:
    st.header("Ã¢ÂÂ±Ã¯Â¸Â Controle de Prazo de CarÃÂªncia e Reentrada")
    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
    Ã¢âÂ¹Ã¯Â¸Â Registre os defensivos aplicados e acompanhe automaticamente os prazos de
    carÃÂªncia (colheita) e reentrada (entrada segura na lavoura).
    </div>''', unsafe_allow_html=True)

    # Init storage
    if "carencia_registros" not in st.session_state:
        st.session_state.carencia_registros = []

    # Ã¢ââ¬Ã¢ââ¬ Cadastrar nova aplicaÃÂ§ÃÂ£o com carÃÂªncia Ã¢ââ¬Ã¢ââ¬
    st.subheader("Ã¢Å¾â¢ Registrar AplicaÃÂ§ÃÂ£o com CarÃÂªncia")
    col1, col2, col3 = st.columns(3)
    with col1:
        car_produto    = st.text_input("Nome do produto/defensivo", key="car_produto")
        car_cultura    = st.selectbox("Cultura", get_culturas() + ["Outra"], key="car_cultura")
        car_data_aplic = st.date_input("Data da aplicaÃÂ§ÃÂ£o", key="car_data")
    with col2:
        car_carencia   = st.number_input("Prazo de carÃÂªncia (dias)", min_value=0, value=14, key="car_carencia",
                                          help="Dias apÃÂ³s aplicaÃÂ§ÃÂ£o atÃÂ© a colheita segura")
        car_reentrada  = st.number_input("Prazo de reentrada (horas)", min_value=0, value=48, key="car_reentrada",
                                          help="Horas apÃÂ³s aplicaÃÂ§ÃÂ£o para entrar na lavoura com seguranÃÂ§a")
        car_dose       = st.text_input("Dose aplicada", placeholder="Ex: 0.5 L/ha", key="car_dose")
    with col3:
        car_talhao     = st.text_input("TalhÃÂ£o/ÃÂrea", key="car_talhao")
        car_epi        = st.multiselect("EPI necessÃÂ¡rio",
                                         ["MÃÂ¡scara","Luvas","Ãâculos","MacacÃÂ£o","Botas","Protetor Auricular"],
                                         key="car_epi")
        car_obs        = st.text_area("ObservaÃÂ§ÃÂµes", key="car_obs", height=80)

    if st.button("Ã°Å¸âÂ¾ Salvar Registro de CarÃÂªncia", key="btn_salvar_carencia"):
        if not car_produto.strip():
            error_box("Digite o nome do produto.")
        else:
            from datetime import timedelta
            data_colheita_seg = car_data_aplic + timedelta(days=int(car_carencia))
            data_reentrada    = datetime.combine(car_data_aplic, datetime.min.time()) + timedelta(hours=int(car_reentrada))
            st.session_state.carencia_registros.append({
                "Produto":          car_produto,
                "Cultura":          car_cultura,
                "TalhÃÂ£o":           car_talhao,
                "Data AplicaÃÂ§ÃÂ£o":   str(car_data_aplic),
                "CarÃÂªncia dias":    car_carencia,
                "Data Colheita Segura": str(data_colheita_seg),
                "Reentrada horas":  car_reentrada,
                "Data Reentrada":   str(data_reentrada.date()),
                "Dose":             car_dose,
                "EPI":              ", ".join(car_epi),
                "ObservaÃÂ§ÃÂµes":      car_obs,
            })
            salvar_dados_iaagro()
            success_box(f"Registro de {car_produto} salvo! CarÃÂªncia atÃÂ©: {data_colheita_seg} | Reentrada: {data_reentrada.strftime('%d/%m/%Y %H:%M')}")

    # Ã¢ââ¬Ã¢ââ¬ Painel de situaÃÂ§ÃÂ£o Ã¢ââ¬Ã¢ââ¬
    if st.session_state.carencia_registros:
        st.divider()
        st.subheader("Ã°Å¸âÅ  SituaÃÂ§ÃÂ£o dos Prazos")

        hoje = date.today()
        registros_status = []
        for r in st.session_state.carencia_registros:
            data_colh  = date.fromisoformat(r["Data Colheita Segura"])
            data_reent = date.fromisoformat(r["Data Reentrada"])
            dias_colh  = (data_colh - hoje).days
            dias_reent = (data_reent - hoje).days

            if dias_colh < 0:
                status_colh = "Ã¢Åâ¦ Liberado para colheita"
            elif dias_colh == 0:
                status_colh = "Ã¢Å¡Â Ã¯Â¸Â Liberado hoje"
            else:
                status_colh = f"Ã°Å¸âÂ´ {dias_colh} dias para colheita segura"

            if dias_reent < 0:
                status_reent = "Ã¢Åâ¦ Reentrada liberada"
            elif dias_reent == 0:
                status_reent = "Ã¢Å¡Â Ã¯Â¸Â Reentrada liberada hoje"
            else:
                status_reent = f"Ã°Å¸âÂ´ Aguardar {dias_reent} dia(s) para reentrada"

            registros_status.append({
                "Produto":         r["Produto"],
                "Cultura":         r["Cultura"],
                "TalhÃÂ£o":          r["TalhÃÂ£o"],
                "AplicaÃÂ§ÃÂ£o":       r["Data AplicaÃÂ§ÃÂ£o"],
                "Colheita Segura": r["Data Colheita Segura"],
                "Status Colheita": status_colh,
                "Status Reentrada":status_reent,
                "EPI":             r["EPI"],
            })

        df_car = pd.DataFrame(registros_status)
        st.dataframe(df_car, use_container_width=True)

        # Alertas visuais
        st.divider()
        st.subheader("Ã°Å¸Å¡Â¨ Alertas Ativos")
        alertas_ativos = False
        for r in registros_status:
            if "Ã°Å¸âÂ´" in r["Status Colheita"]:
                st.markdown(f'''<div style="background:#7f1d1d;color:#fff;padding:12px 18px;
                border-radius:10px;border-left:5px solid #ef4444;font-weight:700;margin:4px 0;">
                Ã°Å¸ÅÂ¾ {r["Produto"]} Ã¢â¬â {r["TalhÃÂ£o"]}: {r["Status Colheita"]}</div>''',
                unsafe_allow_html=True)
                alertas_ativos = True
            if "Ã°Å¸âÂ´" in r["Status Reentrada"]:
                st.markdown(f'''<div style="background:#78350f;color:#fff;padding:12px 18px;
                border-radius:10px;border-left:5px solid #f59e0b;font-weight:700;margin:4px 0;">
                Ã¢âºâ {r["Produto"]} Ã¢â¬â {r["TalhÃÂ£o"]}: {r["Status Reentrada"]} | EPI: {r["EPI"]}</div>''',
                unsafe_allow_html=True)
                alertas_ativos = True
        if not alertas_ativos:
            success_box("Nenhum prazo de carÃÂªncia ou reentrada pendente no momento!")

        # Excluir registro
        st.divider()
        opcoes_del = [f"{r['Produto']} Ã¢â¬â {r['TalhÃÂ£o']} ({r['Data AplicaÃÂ§ÃÂ£o']})"
                      for r in st.session_state.carencia_registros]
        del_choice = st.selectbox("Excluir registro", opcoes_del, key="del_carencia")
        if st.button("Ã°Å¸ââÃ¯Â¸Â Excluir", key="btn_del_carencia"):
            idx = opcoes_del.index(del_choice)
            st.session_state.carencia_registros.pop(idx)
            salvar_dados_iaagro()
            success_box("Registro removido.")
            st.rerun()


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: ORDEM DE SERVIÃâ¡O
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸âÂ¦ Operacional":
  with _sub_op[3]:
    st.header("Ã°Å¸ââ¹ Ordem de ServiÃÂ§o")
    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
    Ã¢âÂ¹Ã¯Â¸Â Gere uma Ordem de ServiÃÂ§o completa para o operador ir ao campo. Pode ser impressa ou salva em PDF.
    </div>''', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        os_numero     = st.text_input("NÃÂºmero da OS", value=f"OS-{datetime.now().strftime('%Y%m%d%H%M')}", key="txt_n_mero_da_os_6029")
        os_data       = st.date_input("Data da OS", value=date.today(), key="dat_data_da_os_6030")
        os_fazenda    = st.text_input("Fazenda", value=st.session_state.dados.get("fazenda",""), key="txt_fazenda_6031")
        os_talhao     = st.text_input("TalhÃÂ£o", value=st.session_state.dados.get("talhao",""), key="txt_talh_o_6032")
        os_area       = st.number_input("ÃÂrea (ha)", value=float(st.session_state.dados.get("area",0)), key="num__rea__ha__6033")
        os_cultura    = st.text_input("Cultura", value=st.session_state.dados.get("cultura",""), key="txt_cultura_6034")
    with col2:
        os_operador   = st.text_input("Operador responsÃÂ¡vel", key="txt_operador_respon_6036")
        os_maquina    = st.text_input("MÃÂ¡quina / Pulverizador", key="txt_m_quina___pulve_6037")
        os_velocidade = st.number_input("Velocidade (km/h)", value=6.0, key="num_velocidade__km__6038")
        os_pressao    = st.number_input("PressÃÂ£o de trabalho (bar)", value=2.5, key="num_press_o_de_trab_6039")
        os_volume     = st.number_input("Volume de calda (L/ha)", value=100.0, key="num_volume_de_calda_6040")
        os_inicio     = st.text_input("HorÃÂ¡rio previsto de inÃÂ­cio", placeholder="Ex: 06:30", key="txt_hor_rio_previst_6041")

    st.subheader("Ã°Å¸Â§Âª Produtos da OS")
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

    os_epi     = st.multiselect("EPI obrigatÃÂ³rio",
                                 ["MÃÂ¡scara com filtro","Luvas nitrÃÂ­licas","Ãâculos de proteÃÂ§ÃÂ£o",
                                  "MacacÃÂ£o impermeÃÂ¡vel","Botas de borracha","Protetor auricular","Avental"],
                                 key="os_epi")
    os_obs_geral = st.text_area("ObservaÃÂ§ÃÂµes gerais", key="os_obs_geral")

    if st.button("Ã°Å¸ââ Gerar Ordem de ServiÃÂ§o (PDF)", key="btn_gerar_os"):
        from reportlab.lib.units import cm
        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                rightMargin=1.5*cm, leftMargin=1.5*cm,
                                topMargin=1.5*cm, bottomMargin=1.5*cm)
        styles = getSampleStyleSheet()
        el = []

        # CabeÃÂ§alho
        if os.path.exists("IAAgrologo.jpeg"):
            el.append(Image("IAAgrologo.jpeg", width=3*cm, height=1.5*cm))
        el.append(Spacer(1, 6))

        # TÃÂ­tulo
        titulo_style = styles["Title"]
        el.append(Paragraph(f"<b>ORDEM DE SERVIÃâ¡O Ã¢â¬â {os_numero}</b>", titulo_style))
        el.append(Paragraph(f"Data: {os_data} | Fazenda: {os_fazenda} | TalhÃÂ£o: {os_talhao}", styles["Normal"]))
        el.append(Spacer(1, 12))

        # Dados gerais
        dados_os = [
            ["Campo","InformaÃÂ§ÃÂ£o","Campo","InformaÃÂ§ÃÂ£o"],
            ["Fazenda", os_fazenda, "Operador", os_operador],
            ["TalhÃÂ£o",  os_talhao,  "MÃÂ¡quina",  os_maquina],
            ["ÃÂrea",    f"{os_area} ha", "Cultura", os_cultura],
            ["Volume calda", f"{os_volume} L/ha", "Velocidade", f"{os_velocidade} km/h"],
            ["PressÃÂ£o", f"{os_pressao} bar", "InÃÂ­cio previsto", os_inicio],
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
            prod_data = [["Produto","Dose/ha","Total","ObservaÃÂ§ÃÂ£o"]] +                         [[p["Produto"],p["Dose/ha"],p["Total"],p["Obs"]] for p in os_produtos]
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
            el.append(Paragraph("<b>EPI OBRIGATÃâRIO:</b> " + " | ".join(os_epi), styles["Normal"]))
            el.append(Spacer(1, 8))

        # ObservaÃÂ§ÃÂµes
        if os_obs_geral:
            el.append(Paragraph(f"<b>ObservaÃÂ§ÃÂµes:</b> {os_obs_geral}", styles["Normal"]))
            el.append(Spacer(1, 16))

        # Assinaturas
        assin = Table([
            ["_"*35, " ", "_"*35],
            ["Operador / Data", " ", "ResponsÃÂ¡vel TÃÂ©cnico / Data"],
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
            "Ã°Å¸âÂ¥ Baixar Ordem de ServiÃÂ§o PDF",
            data=pdf_os,
            file_name=f"OS_{os_numero}_{os_data}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        success_box(f"OS {os_numero} gerada com sucesso!")


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: DASHBOARD FINANCEIRO
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸âÂ° Financeiro":
  with _sub_fin[1]:
    st.header("Ã°Å¸âÂ¹ Dashboard Financeiro Ã¢â¬â DRE por Safra")

    if "dre_registros" not in st.session_state:
        st.session_state.dre_registros = []

    tab_dre, tab_novo, tab_grafico = st.tabs([
        "Ã°Å¸âÅ  DRE & Resultados",
        "Ã¢Å¾â¢ LanÃÂ§ar Receita/Custo",
        "Ã°Å¸âË EvoluÃÂ§ÃÂ£o por Safra"
    ])

    with tab_novo:
        st.subheader("Ã¢Å¾â¢ Novo LanÃÂ§amento Financeiro")
        col1, col2, col3 = st.columns(3)
        with col1:
            dre_safra    = st.text_input("Safra", placeholder="2024/2025", key="dre_safra")
            dre_tipo     = st.selectbox("Tipo", ["Receita","Custo VariÃÂ¡vel","Custo Fixo"], key="dre_tipo")
            dre_categ    = st.selectbox("Categoria", [
                "Venda de grÃÂ£os","Venda de outros","Semente","Fertilizante",
                "Defensivo","Diesel e lubrificantes","MÃÂ£o de obra","Aluguel de mÃÂ¡quinas",
                "Arrendamento","Seguro","Transporte","Armazenagem","Outros"
            ], key="dre_categ")
        with col2:
            dre_descricao = st.text_input("DescriÃÂ§ÃÂ£o", key="dre_desc")
            dre_valor     = st.number_input("Valor R$", min_value=0.0, key="dre_valor")
            dre_area_ha   = st.number_input("ÃÂrea referente (ha)", min_value=0.0,
                                             value=float(st.session_state.dados.get("area",0)),
                                             key="dre_area")
        with col3:
            dre_data_lanc = st.date_input("Data", key="dre_data")
            dre_talhao    = st.text_input("TalhÃÂ£o/ÃÂrea", key="dre_talhao")
            dre_cultura   = st.text_input("Cultura", value=st.session_state.dados.get("cultura",""), key="dre_cultura")

        if st.button("Ã°Å¸âÂ¾ Salvar LanÃÂ§amento", key="btn_salvar_dre"):
            if not dre_safra.strip():
                error_box("Informe a safra.")
            elif dre_valor <= 0:
                error_box("Informe um valor maior que zero.")
            else:
                st.session_state.dre_registros.append({
                    "Safra":      dre_safra,
                    "Tipo":       dre_tipo,
                    "Categoria":  dre_categ,
                    "DescriÃÂ§ÃÂ£o":  dre_descricao,
                    "Valor R$":   dre_valor,
                    "ÃÂrea ha":    dre_area_ha,
                    "Valor/ha":   round(dre_valor / dre_area_ha, 2) if dre_area_ha > 0 else 0,
                    "Data":       str(dre_data_lanc),
                    "TalhÃÂ£o":     dre_talhao,
                    "Cultura":    dre_cultura,
                })
                salvar_dados_iaagro()
                success_box(f"LanÃÂ§amento salvo! R$ {dre_valor:,.2f} Ã¢â¬â {dre_categ}")

    with tab_dre:
        if not st.session_state.dre_registros:
            info_box("Nenhum lanÃÂ§amento financeiro ainda. Use a aba 'LanÃÂ§ar Receita/Custo'.")
        else:
            df_dre = pd.DataFrame(st.session_state.dre_registros)
            safras_disp = sorted(df_dre["Safra"].unique().tolist(), reverse=True)
            safra_sel   = st.selectbox("Selecione a safra", safras_disp, key="dre_sel_safra")
            df_safra    = df_dre[df_dre["Safra"] == safra_sel]

            receita      = df_safra[df_safra["Tipo"]=="Receita"]["Valor R$"].sum()
            custo_var    = df_safra[df_safra["Tipo"]=="Custo VariÃÂ¡vel"]["Valor R$"].sum()
            custo_fix    = df_safra[df_safra["Tipo"]=="Custo Fixo"]["Valor R$"].sum()
            custo_total  = custo_var + custo_fix
            lucro_bruto  = receita - custo_var
            lucro_liq    = receita - custo_total
            margem       = (lucro_liq / receita * 100) if receita > 0 else 0
            area_safra   = df_safra["ÃÂrea ha"].max() if not df_safra.empty else 1
            receita_ha   = receita / area_safra if area_safra > 0 else 0
            custo_ha     = custo_total / area_safra if area_safra > 0 else 0
            lucro_ha     = lucro_liq / area_safra if area_safra > 0 else 0
            breakeven    = custo_total / area_safra if area_safra > 0 else 0

            st.subheader(f"Ã°Å¸âÅ  DRE Ã¢â¬â Safra {safra_sel}")
            col1,col2,col3,col4 = st.columns(4)
            col1.metric("Ã°Å¸âÂ° Receita Total",   f"R$ {receita:,.0f}")
            col2.metric("Ã°Å¸âÂ¸ Custo Total",     f"R$ {custo_total:,.0f}")
            col3.metric("Ã°Å¸âÂµ Lucro LÃÂ­quido",   f"R$ {lucro_liq:,.0f}")
            col4.metric("Ã°Å¸âÅ  Margem",          f"{margem:.1f}%")

            col5,col6,col7,col8 = st.columns(4)
            col5.metric("Ã°Å¸âÂ° Receita/ha",  f"R$ {receita_ha:,.0f}")
            col6.metric("Ã°Å¸âÂ¸ Custo/ha",    f"R$ {custo_ha:,.0f}")
            col7.metric("Ã°Å¸âÂµ Lucro/ha",    f"R$ {lucro_ha:,.0f}")
            col8.metric("Ã¢Å¡âÃ¯Â¸Â Break-even",  f"R$ {breakeven:,.0f}/ha")

            # DRE formatado
            st.divider()
            st.subheader("Ã°Å¸ââ¹ Demonstrativo de Resultado (DRE)")
            dre_lines = [
                {"Item": "RECEITA BRUTA",            "Valor R$": receita,      "Tipo": ""},
                {"Item": "(-) Custos VariÃÂ¡veis",     "Valor R$": -custo_var,   "Tipo": ""},
                {"Item": "= LUCRO BRUTO",             "Valor R$": lucro_bruto,  "Tipo": ""},
                {"Item": "(-) Custos Fixos",          "Valor R$": -custo_fix,   "Tipo": ""},
                {"Item": "= LUCRO LÃÂQUIDO",           "Valor R$": lucro_liq,    "Tipo": ""},
                {"Item": f"  Margem LÃÂ­quida",         "Valor R$": margem,       "Tipo": "%"},
            ]
            df_dre_fmt = pd.DataFrame(dre_lines)
            st.dataframe(df_dre_fmt, use_container_width=True, hide_index=True)

            # LanÃÂ§amentos detalhados
            st.divider()
            st.subheader("Ã°Å¸âÂ LanÃÂ§amentos Detalhados")
            st.dataframe(df_safra[["Data","Tipo","Categoria","DescriÃÂ§ÃÂ£o","Valor R$","Valor/ha","TalhÃÂ£o"]],
                         use_container_width=True, hide_index=True)

            # ComposiÃÂ§ÃÂ£o de custos
            st.divider()
            st.subheader("Ã°Å¸Â¥Â§ ComposiÃÂ§ÃÂ£o de Custos")
            df_custos = df_safra[df_safra["Tipo"].isin(["Custo VariÃÂ¡vel","Custo Fixo"])]
            if not df_custos.empty:
                df_comp = df_custos.groupby("Categoria")["Valor R$"].sum().reset_index()
                st.bar_chart(df_comp.set_index("Categoria")["Valor R$"])

            # Exportar DRE
            st.divider()
            xlsx_dre = exportar_excel({
                f"DRE {safra_sel}": dre_lines,
                "LanÃÂ§amentos":      st.session_state.dre_registros
            })
            if xlsx_dre:
                st.download_button(
                    "Ã°Å¸âÂ¥ Exportar DRE Excel",
                    data=xlsx_dre,
                    file_name=f"DRE_{safra_sel.replace('/','_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

    with tab_grafico:
        if len(st.session_state.dre_registros) < 2:
            info_box("LanÃÂ§e dados de pelo menos 2 safras para ver a evoluÃÂ§ÃÂ£o.")
        else:
            df_all  = pd.DataFrame(st.session_state.dre_registros)
            df_evo  = df_all.groupby(["Safra","Tipo"])["Valor R$"].sum().unstack(fill_value=0).reset_index()
            st.subheader("Ã°Å¸âË EvoluÃÂ§ÃÂ£o Financeira por Safra")
            st.dataframe(df_evo, use_container_width=True)
            st.line_chart(df_evo.set_index("Safra"))

            # Lucratividade por safra
            df_lucro = df_all.groupby("Safra").apply(
                lambda x: pd.Series({
                    "Receita":     x[x["Tipo"]=="Receita"]["Valor R$"].sum(),
                    "Custo Total": x[x["Tipo"].isin(["Custo VariÃÂ¡vel","Custo Fixo"])]["Valor R$"].sum(),
                })
            ).reset_index()
            df_lucro["Lucro"] = df_lucro["Receita"] - df_lucro["Custo Total"]
            df_lucro["Margem %"] = (df_lucro["Lucro"] / df_lucro["Receita"] * 100).round(1)
            st.subheader("Ã°Å¸âÂ° Lucratividade por Safra")
            st.dataframe(df_lucro, use_container_width=True)
            st.bar_chart(df_lucro.set_index("Safra")["Lucro"])



# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: RELATÃâRIO FINAL
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
elif menu == "Ã°Å¸ââ RelatÃÂ³rio Final":
    st.header("Ã°Å¸ââ RelatÃÂ³rio Final da Propriedade")

    if not st.session_state.areas:
        warning_box("Cadastre pelo menos uma ÃÂ¡rea para gerar o relatÃÂ³rio.")
    else:
        st.markdown("""
        <div style='background:#0f3460;border-radius:10px;padding:12px 16px;
        border-left:5px solid #22c55e;margin-bottom:12px;'>
        <b style='color:#22c55e;'>Ã°Å¸ââ¹ RelatÃÂ³rio completo da propriedade</b><br>
        <span style='color:#f1f5f9;font-size:13px;'>
        Gera um PDF profissional com anÃÂ¡lise de solo, recomendaÃÂ§ÃÂµes de adubaÃÂ§ÃÂ£o,
        histÃÂ³rico de produtividade e resumo da propriedade.
        </span>
        </div>
        """, unsafe_allow_html=True)

        _areas_rel = [f"{a['ID']} Ã¢â¬â {a.get('TalhÃÂ£o','?')} ({a.get('Cultura','?')})"
                      for a in st.session_state.areas]
        _sel_rel   = st.selectbox("Ã°Å¸âÂ ÃÂrea para o relatÃÂ³rio", _areas_rel, key="sel_area_relatorio")
        _id_rel    = _sel_rel.split(" Ã¢â¬â ")[0]
        _area_rel  = next((a for a in st.session_state.areas if a.get("ID") == _id_rel), {})
        _dados_rel = _area_rel.get("Dados", _area_rel.get("dados", {})) or {}

        col_r1, col_r2 = st.columns(2)
        nome_produtor = col_r1.text_input("Nome do produtor",
                                           value=st.session_state.get("usuario_atual",""),
                                           key="rel_produtor")
        municipio = col_r2.text_input("MunicÃÂ­pio/UF",
                                       value=_dados_rel.get("cidade",""), key="rel_municipio")

        if st.button("Ã°Å¸ââ Gerar RelatÃÂ³rio Final (PDF)", key="btn_gerar_relatorio", use_container_width=True):
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.lib import colors as rl_colors
                from reportlab.lib.units import cm
                from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                                 Table, TableStyle, HRFlowable)
                from reportlab.lib.styles import ParagraphStyle
                from reportlab.lib.enums import TA_CENTER, TA_LEFT
                from io import BytesIO

                buf_r = BytesIO()
                doc_r = SimpleDocTemplate(buf_r, pagesize=A4,
                                          rightMargin=2*cm, leftMargin=2*cm,
                                          topMargin=2*cm, bottomMargin=2*cm)
                el_r = []
                COR_V = rl_colors.HexColor("#16a34a")
                COR_E = rl_colors.HexColor("#14532d")
                COR_A = rl_colors.HexColor("#1e3a5f")
                COR_C = rl_colors.HexColor("#f1f5f9")
                COR_B = rl_colors.HexColor("#e2e8f0")
                COR_W = rl_colors.white

                def Pr(txt, size=9, bold=False, color=None, align=TA_LEFT):
                    fn = "Helvetica-Bold" if bold else "Helvetica"
                    c  = color or rl_colors.HexColor("#0f172a")
                    return Paragraph(txt, ParagraphStyle("p", fontName=fn, fontSize=size,
                                                          textColor=c, alignment=align, leading=size+3))

                # CabeÃÂ§alho
                if os.path.exists("IAAgrologo.jpeg"):
                    from reportlab.platypus import Image as RLImage
                    el_r.append(RLImage("IAAgrologo.jpeg", width=3*cm, height=1.5*cm))
                el_r.append(Pr("RELATÃâRIO AGRONÃâMICO COMPLETO", 16, True, COR_E, TA_CENTER))
                el_r.append(Pr("IAAgro Ã¢â¬â InteligÃÂªncia AgrÃÂ­cola de PrecisÃÂ£o", 9, False, COR_A, TA_CENTER))
                el_r.append(Pr(f"Emitido: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 8, False, rl_colors.HexColor("#64748b"), TA_CENTER))
                el_r.append(Spacer(1, 0.3*cm))
                el_r.append(HRFlowable(width="100%", thickness=2, color=COR_V))
                el_r.append(Spacer(1, 0.3*cm))

                # Info propriedade
                t_inf = Table([[
                    Pr(f"<b>Produtor:</b> {nome_produtor or 'Ã¢â¬â'}"),
                    Pr(f"<b>MunicÃÂ­pio:</b> {municipio or 'Ã¢â¬â'}"),
                    Pr(f"<b>TalhÃÂ£o:</b> {_area_rel.get('TalhÃÂ£o','Ã¢â¬â')}"),
                    Pr(f"<b>ÃÂrea:</b> {_area_rel.get('Hectares',0)} ha"),
                ]], colWidths=[4*cm,3.5*cm,4*cm,4*cm])
                t_inf.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),COR_C),
                    ("GRID",(0,0),(-1,-1),0.4,COR_B),("TOPPADDING",(0,0),(-1,-1),5),
                    ("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),6)]))
                el_r.append(t_inf); el_r.append(Spacer(1,0.4*cm))

                # AnÃÂ¡lise de solo
                if "ph" in _dados_rel:
                    el_r.append(Pr("ANÃÂLISE DE SOLO", 11, True, COR_E))
                    el_r.append(HRFlowable(width="100%", thickness=1, color=COR_V))
                    el_r.append(Spacer(1,0.2*cm))
                    rows_s = [[Pr("<b>ParÃÂ¢metro</b>",9,True,COR_W),Pr("<b>Valor</b>",9,True,COR_W),
                               Pr("<b>Unidade</b>",9,True,COR_W),Pr("<b>ReferÃÂªncia</b>",9,True,COR_W)],
                              [Pr("pH"),Pr(str(_dados_rel.get("ph","Ã¢â¬â"))),Pr("adimensional"),Pr("5.5Ã¢â¬â6.5")],
                              [Pr("FÃÂ³sforo P"),Pr(str(_dados_rel.get("fosforo","Ã¢â¬â"))),Pr("mg/dm3"),Pr(">12")],
                              [Pr("PotÃÂ¡ssio K"),Pr(str(_dados_rel.get("potassio","Ã¢â¬â"))),Pr("mg/dm3"),Pr(">80")],
                              [Pr("CÃÂ¡lcio Ca"),Pr(str(_dados_rel.get("calcio","Ã¢â¬â"))),Pr("cmolc/dm3"),Pr(">2.0")],
                              [Pr("MagnÃÂ©sio Mg"),Pr(str(_dados_rel.get("magnesio","Ã¢â¬â"))),Pr("cmolc/dm3"),Pr(">0.5")],
                              [Pr("Mat. OrgÃÂ¢nica"),Pr(str(_dados_rel.get("materia_organica","Ã¢â¬â"))),Pr("g/dm3"),Pr(">25")],
                              [Pr("CTC"),Pr(str(_dados_rel.get("ctc","Ã¢â¬â"))),Pr("cmolc/dm3"),Pr(">8.0")],
                              [Pr("V%"),Pr(str(_dados_rel.get("v_percent","Ã¢â¬â"))),Pr("%"),Pr(">60%")],
                              [Pr("Argila"),Pr(str(_dados_rel.get("argila","Ã¢â¬â"))),Pr("%"),Pr("Ã¢â¬â")]]
                    ts = Table(rows_s, colWidths=[4*cm,3*cm,3.5*cm,5*cm])
                    ts.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),COR_E),("TEXTCOLOR",(0,0),(-1,0),COR_W),
                        ("ROWBACKGROUNDS",(0,1),(-1,-1),[COR_C,COR_W]),("GRID",(0,0),(-1,-1),0.4,COR_B),
                        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
                        ("LEFTPADDING",(0,0),(-1,-1),6)]))
                    el_r.append(ts); el_r.append(Spacer(1,0.4*cm))

                    # RecomendaÃÂ§ÃÂ£o NPK
                    el_r.append(Pr("RECOMENDAÃâ¡ÃÆO DE ADUBAÃâ¡ÃÆO (EMBRAPA/CQFS 2016)", 11, True, COR_E))
                    el_r.append(HRFlowable(width="100%", thickness=1, color=COR_V))
                    el_r.append(Spacer(1,0.2*cm))
                    try:
                        _cult = cultura_limpa(_area_rel.get("Cultura","Soja"))
                        _prd  = _area_rel.get("Produtividade",50)
                        _aha  = _area_rel.get("Hectares",1)
                        n,p,k = recomendacao_npk(_cult,_prd,
                            _dados_rel.get("fosforo",10),_dados_rel.get("potassio",100),
                            _dados_rel.get("materia_organica",2.5),
                            _dados_rel.get("argila",35),_dados_rel.get("ph",5.5))
                        rows_n = [[Pr("<b>Nutriente</b>",9,True,COR_W),Pr("<b>kg/ha</b>",9,True,COR_W),
                                   Pr("<b>Total ÃÂ¡rea</b>",9,True,COR_W),Pr("<b>Fonte sugerida</b>",9,True,COR_W)],
                                  [Pr("NitrogÃÂªnio (N)"),Pr(f"{n:.0f}"),Pr(f"{n*_aha:.0f} kg"),Pr("Ureia / MAP")],
                                  [Pr("FÃÂ³sforo (P2O5)"),Pr(f"{p:.0f}"),Pr(f"{p*_aha:.0f} kg"),Pr("MAP / TSP")],
                                  [Pr("PotÃÂ¡ssio (K2O)"),Pr(f"{k:.0f}"),Pr(f"{k*_aha:.0f} kg"),Pr("KCl")]]
                        tn = Table(rows_n, colWidths=[4*cm,3*cm,4*cm,4.5*cm])
                        tn.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),COR_E),("TEXTCOLOR",(0,0),(-1,0),COR_W),
                            ("ROWBACKGROUNDS",(0,1),(-1,-1),[COR_C,COR_W]),("GRID",(0,0),(-1,-1),0.4,COR_B),
                            ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
                            ("LEFTPADDING",(0,0),(-1,-1),6)]))
                        el_r.append(tn)
                    except Exception:
                        el_r.append(Pr("Dados insuficientes para recomendaÃÂ§ÃÂ£o.",9))
                    el_r.append(Spacer(1,0.4*cm))

                # HistÃÂ³rico
                _hist = [h for h in st.session_state.historico_produtividade
                         if h.get("ÃÂrea","").startswith(_id_rel)]
                if _hist:
                    el_r.append(Pr("HISTÃâRICO DE PRODUTIVIDADE", 11, True, COR_E))
                    el_r.append(HRFlowable(width="100%", thickness=1, color=COR_V))
                    el_r.append(Spacer(1,0.2*cm))
                    rows_h = [[Pr("<b>Safra</b>",9,True,COR_W),Pr("<b>Cultura</b>",9,True,COR_W),
                               Pr("<b>Produtividade</b>",9,True,COR_W),Pr("<b>Custo R$/ha</b>",9,True,COR_W)]]
                    for h in _hist:
                        rows_h.append([Pr(h.get("Safra","Ã¢â¬â"),9),
                                       Pr(cultura_limpa(h.get("Cultura","Ã¢â¬â")),9),
                                       Pr(f"{h.get('Produtividade',0):.1f} sc/ha",9),
                                       Pr(f"R$ {h.get('Custo',0):.2f}",9)])
                    th_ = Table(rows_h, colWidths=[3*cm,4*cm,4*cm,4.5*cm])
                    th_.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),COR_E),("TEXTCOLOR",(0,0),(-1,0),COR_W),
                        ("ROWBACKGROUNDS",(0,1),(-1,-1),[COR_C,COR_W]),("GRID",(0,0),(-1,-1),0.4,COR_B),
                        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
                        ("LEFTPADDING",(0,0),(-1,-1),6)]))
                    el_r.append(th_); el_r.append(Spacer(1,0.4*cm))

                # RodapÃÂ©
                el_r.append(HRFlowable(width="100%", thickness=1, color=COR_V))
                el_r.append(Pr(f"IAAgro Ã¢â¬â {datetime.now().strftime('%d/%m/%Y %H:%M')} | Uso interno",
                               7, False, rl_colors.HexColor("#64748b"), TA_CENTER))
                doc_r.build(el_r)
                buf_r.seek(0)
                st.session_state["_pdf_relatorio"] = buf_r.read()
                st.success("Ã¢Åâ¦ RelatÃÂ³rio gerado com sucesso!")
            except Exception as e:
                st.error(f"Erro: {e}")

        if st.session_state.get("_pdf_relatorio"):
            st.download_button(
                label     = "Ã¢Â¬â¡Ã¯Â¸Â Baixar RelatÃÂ³rio PDF",
                data      = st.session_state["_pdf_relatorio"],
                file_name = f"relatorio_iaagro_{datetime.now().strftime('%d%m%Y')}.pdf",
                mime      = "application/pdf",
                use_container_width = True,
                key       = "btn_download_relatorio"
            )

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: CALENDÃÂRIO AGRÃÂCOLA
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸ÅÂ InteligÃÂªncia":
  with _sub_int[3]:
    st.header("Ã°Å¸ââ¦ CalendÃÂ¡rio AgrÃÂ­cola")

    if "calendario_eventos" not in st.session_state:
        st.session_state.calendario_eventos = []

    tab_cal, tab_novo_ev, tab_plantio = st.tabs([
        "Ã°Å¸ââ¦ CalendÃÂ¡rio do MÃÂªs",
        "Ã¢Å¾â¢ Novo Evento",
        "Ã°Å¸ÅÂ± Cronograma de Plantio"
    ])

    with tab_novo_ev:
        st.subheader("Ã¢Å¾â¢ Cadastrar Evento AgrÃÂ­cola")
        col1, col2 = st.columns(2)
        with col1:
            ev_tipo   = st.selectbox("Tipo de evento", [
                "Ã°Å¸ÅÂ± Plantio","Ã°Å¸ÅÂ¿ EmergÃÂªncia","Ã°Å¸Å¡Å AplicaÃÂ§ÃÂ£o","Ã¢ÅâÃ¯Â¸Â Poda/Desbaste",
                "Ã°Å¸âÂ§ IrrigaÃÂ§ÃÂ£o","Ã°Å¸ÅÂ¾ Colheita","Ã°Å¸Â§Âª AnÃÂ¡lise de Solo","Ã°Å¸âÂ¦ Recebimento de insumos",
                "Ã°Å¸âÂ§ ManutenÃÂ§ÃÂ£o de equipamentos","Ã°Å¸ââ¹ Vistoria","Ã°Å¸ÅÂ¦Ã¯Â¸Â Evento climÃÂ¡tico","Ã°Å¸âÂ Outro"
            ], key="ev_tipo")
            ev_data   = st.date_input("Data do evento", key="ev_data")
            ev_talhao = st.text_input("TalhÃÂ£o/ÃÂrea", key="ev_talhao")
        with col2:
            ev_cultura = st.text_input("Cultura", value=st.session_state.dados.get("cultura",""), key="ev_cultura")
            ev_resp    = st.text_input("ResponsÃÂ¡vel", key="ev_resp")
            ev_status  = st.selectbox("Status", ["Ã¢ÂÂ³ Planejado","Ã¢Åâ¦ Realizado","Ã¢Å¡Â Ã¯Â¸Â Atrasado","Ã¢ÂÅ Cancelado"], key="ev_status")
        ev_descricao = st.text_area("DescriÃÂ§ÃÂ£o / ObservaÃÂ§ÃÂµes", key="ev_desc")

        if st.button("Ã°Å¸âÂ¾ Salvar Evento", key="btn_salvar_ev"):
            if not ev_tipo:
                error_box("Selecione o tipo de evento.")
            else:
                st.session_state.calendario_eventos.append({
                    "Tipo":        ev_tipo,
                    "Data":        str(ev_data),
                    "TalhÃÂ£o":      ev_talhao,
                    "Cultura":     ev_cultura,
                    "ResponsÃÂ¡vel": ev_resp,
                    "Status":      ev_status,
                    "DescriÃÂ§ÃÂ£o":   ev_descricao,
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
                mes_sel = st.selectbox("MÃÂªs", range(1,13, key="sel_m_s_6377"),
                                        index=date.today().month-1,
                                        format_func=lambda m: ["Jan","Fev","Mar","Abr","Mai","Jun",
                                                                "Jul","Ago","Set","Out","Nov","Dez"][m-1],
                                        key="cal_mes")
            with col_f2:
                ano_sel = st.selectbox("Ano", sorted(df_ev["Data"].dt.year.unique().tolist(), reverse=True, key="sel_ano_6383"),
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
                warning_box("Nenhum evento neste mÃÂªs com os filtros selecionados.")
            else:
                st.subheader(f"Ã°Å¸ââ¦ Eventos Ã¢â¬â {['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'][mes_sel-1]}/{ano_sel}")

                for _, ev in df_mes.iterrows():
                    cor = {"Ã¢Åâ¦ Realizado":"#14532d","Ã¢ÂÂ³ Planejado":"#1e3a5f",
                           "Ã¢Å¡Â Ã¯Â¸Â Atrasado":"#78350f","Ã¢ÂÅ Cancelado":"#7f1d1d"}.get(ev["Status"],"#1e3a5f")
                    borda = {"Ã¢Åâ¦ Realizado":"#22c55e","Ã¢ÂÂ³ Planejado":"#3b82f6",
                             "Ã¢Å¡Â Ã¯Â¸Â Atrasado":"#f59e0b","Ã¢ÂÅ Cancelado":"#ef4444"}.get(ev["Status"],"#3b82f6")
                    st.markdown(f'''<div style="background:{cor};color:#fff;padding:12px 18px;
                    border-radius:10px;border-left:5px solid {borda};
                    font-weight:600;margin:6px 0;font-size:14px;">
                    {ev["Tipo"]} &nbsp;|&nbsp; <b>{ev["Data"].strftime("%d/%m/%Y")}</b>
                    &nbsp;|&nbsp; {ev["TalhÃÂ£o"]} &nbsp;|&nbsp; {ev["Cultura"]}
                    &nbsp;|&nbsp; {ev["Status"]}<br>
                    <span style="font-weight:400;font-size:13px;">{ev["DescriÃÂ§ÃÂ£o"]}</span>
                    </div>''', unsafe_allow_html=True)

            # PrÃÂ³ximos eventos
            st.divider()
            st.subheader("Ã¢ÂÂ° PrÃÂ³ximos Eventos (7 dias)")
            hoje_ts = pd.Timestamp(date.today())
            df_prox = df_ev[
                (df_ev["Data"] >= hoje_ts) &
                (df_ev["Data"] <= hoje_ts + pd.Timedelta(days=7)) &
                (df_ev["Status"] == "Ã¢ÂÂ³ Planejado")
            ].sort_values("Data")
            if df_prox.empty:
                info_box("Nenhum evento planejado nos prÃÂ³ximos 7 dias.")
            else:
                for _, ev in df_prox.iterrows():
                    dias_rest = (ev["Data"].date() - date.today()).days
                    st.markdown(f'''<div style="background:#1e3a5f;color:#fff;padding:10px 16px;
                    border-radius:10px;border-left:5px solid #3b82f6;font-weight:700;margin:4px 0;">
                    {ev["Tipo"]} Ã¢â¬â {ev["TalhÃÂ£o"]} em {ev["Data"].strftime("%d/%m/%Y")}
                    {"(hoje)" if dias_rest==0 else f"(em {dias_rest} dia{'s' if dias_rest>1 else ''})"}
                    </div>''', unsafe_allow_html=True)

            # Excluir evento
            st.divider()
            opcoes_ev = [f"{e['Tipo']} Ã¢â¬â {e['TalhÃÂ£o']} ({e['Data'].strftime('%d/%m/%Y')})"
                          for _, e in df_mes.iterrows()]
            if opcoes_ev:
                del_ev = st.selectbox("Excluir evento", opcoes_ev, key="del_ev_sel")
                if st.button("Ã°Å¸ââÃ¯Â¸Â Excluir Evento", key="btn_del_ev"):
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
        st.subheader("Ã°Å¸ÅÂ± Cronograma de Plantio por Cultura")
        cronograma_completo = {
            "Soja":      {"plantio":["Out","Nov"],"floraÃÂ§ÃÂ£o":["Dez","Jan"],"colheita":["Mar","Abr"],"ciclo":"120-140 dias"},
            "Milho":     {"plantio":["Set","Out","Nov"],"floraÃÂ§ÃÂ£o":["Dez","Jan"],"colheita":["Fev","Mar","Abr"],"ciclo":"120-150 dias"},
            "Trigo":     {"plantio":["Abr","Mai","Jun"],"floraÃÂ§ÃÂ£o":["Jul","Ago"],"colheita":["Set","Out"],"ciclo":"100-130 dias"},
            "FeijÃÂ£o":    {"plantio":["Jan","Jul","Out"],"floraÃÂ§ÃÂ£o":["Fev","Ago","Nov"],"colheita":["Mar","Set","Dez"],"ciclo":"70-90 dias"},
            "Canola":    {"plantio":["Abr","Mai"],"floraÃÂ§ÃÂ£o":["Jun","Jul"],"colheita":["Set","Out"],"ciclo":"120-150 dias"},
            "Aveia":     {"plantio":["Abr","Mai","Jun"],"floraÃÂ§ÃÂ£o":["Jul","Ago"],"colheita":["Set","Out"],"ciclo":"100-120 dias"},
            "CafÃÂ©":      {"plantio":["Out","Nov"],"floraÃÂ§ÃÂ£o":["Jul","Ago"],"colheita":["Mai","Jun","Jul"],"ciclo":"3-4 anos"},
            "Tomate":    {"plantio":["Ago","Set","Jan"],"floraÃÂ§ÃÂ£o":["Out","Fev"],"colheita":["Dez","Abr"],"ciclo":"90-120 dias"},
            "Batata":    {"plantio":["Jul","Ago","Jan"],"floraÃÂ§ÃÂ£o":["Set","Mar"],"colheita":["Nov","Mai"],"ciclo":"90-120 dias"},
            "Eucalipto": {"plantio":["Out","Nov"],"floraÃÂ§ÃÂ£o":["N/A"],"colheita":["6-7 anos"],"ciclo":"6-7 anos"},
            "Pinus":     {"plantio":["Set","Out"],"floraÃÂ§ÃÂ£o":["N/A"],"colheita":["15-20 anos"],"ciclo":"15-20 anos"},
            "Uva":       {"plantio":["Jun","Jul"],"floraÃÂ§ÃÂ£o":["Set","Out"],"colheita":["Jan","Fev"],"ciclo":"2-3 anos"},
            "Laranja":   {"plantio":["Set","Out"],"floraÃÂ§ÃÂ£o":["Ago","Set"],"colheita":["Jun","Jul","Ago"],"ciclo":"3-4 anos"},
            "Banana":    {"plantio":["Set","Out"],"floraÃÂ§ÃÂ£o":["Jan","Fev"],"colheita":["Mar","Abr","Mai"],"ciclo":"12-18 meses"},
        }
        culturas_seg = get_culturas()
        cronograma = {k:v for k,v in cronograma_completo.items() if k in culturas_seg}
        if not cronograma:
            cronograma = cronograma_completo
        cultura_cron = st.selectbox("Selecione a cultura", list(cronograma.keys()), key="cron_cultura")
        cron = cronograma[cultura_cron]
        col1,col2,col3,col4 = st.columns(4)
        col1.metric("Ã°Å¸ÅÂ± Plantio",    ", ".join(cron["plantio"]))
        col2.metric("Ã°Å¸ÅÂ¸ FloraÃÂ§ÃÂ£o",   ", ".join(cron["floraÃÂ§ÃÂ£o"]))
        col3.metric("Ã°Å¸ÅÂ¾ Colheita",   ", ".join(cron["colheita"]))
        col4.metric("Ã¢ÂÂ±Ã¯Â¸Â Ciclo",      cron["ciclo"])

        meses_abrev = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
        fases_linha = []
        for mes in meses_abrev:
            if mes in cron["plantio"]:   fase = "Ã°Å¸ÅÂ± Plantio"
            elif mes in cron["floraÃÂ§ÃÂ£o"]: fase = "Ã°Å¸ÅÂ¸ FloraÃÂ§ÃÂ£o"
            elif mes in cron["colheita"]: fase = "Ã°Å¸ÅÂ¾ Colheita"
            else:                         fase = "Ã¢â¬â"
            fases_linha.append({"MÃÂªs": mes, "Fase": fase})
        df_cron = pd.DataFrame(fases_linha)
        st.dataframe(df_cron.T, use_container_width=True)

        st.markdown('''<div style="background:#14532d;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #22c55e;font-weight:600;margin:10px 0;">
        Ã°Å¸âÂ¡ Use a aba "Novo Evento" para lanÃÂ§ar as datas reais do seu plantio e acompanhar
        o andamento da safra no calendÃÂ¡rio.
        </div>''', unsafe_allow_html=True)


# Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
# MENU: RECEITUÃÂRIO AGRONÃâMICO
# Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
if menu == "Ã°Å¸âÂ¦ Operacional":
  with _sub_op[4]:
    st.header("Ã°Å¸âÅ ReceituÃÂ¡rio AgronÃÂ´mico")
    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
    Ã°Å¸ââ¹ Gere o ReceituÃÂ¡rio AgronÃÂ´mico completo conforme exigido pela Lei 7.802/89 e Decreto 4.074/02.
    ObrigatÃÂ³rio para compra e uso de defensivos agrÃÂ­colas. Gera PDF pronto para assinatura.
    </div>''', unsafe_allow_html=True)

    tab_novo_rec, tab_historico_rec = st.tabs(["Ã¢Å¾â¢ Novo ReceituÃÂ¡rio", "Ã°Å¸âÂ HistÃÂ³rico"])

    # Ã¢ââ¬Ã¢ââ¬ ABA NOVO RECEITUÃÂRIO Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
    with tab_novo_rec:
        st.subheader("Ã°Å¸âÂ Dados do ReceituÃÂ¡rio")

        col_r1, col_r2 = st.columns(2)

        with col_r1:
            st.markdown("**Ã°Å¸âÂ¨Ã¢â¬ÂÃ°Å¸ÅÂ¾ Dados do Produtor**")
            rec_produtor      = st.text_input("Nome do Produtor / RazÃÂ£o Social", key="rec_prod")
            rec_cpf_cnpj      = st.text_input("CPF / CNPJ", placeholder="000.000.000-00", key="rec_cpf")
            rec_propriedade   = st.text_input("Nome da Propriedade", value=st.session_state.dados.get("fazenda",""), key="rec_prop")
            rec_municipio     = st.text_input("MunicÃÂ­pio / UF", key="rec_mun")
            rec_area_ha       = st.number_input("ÃÂrea a tratar (ha)", min_value=0.1,
                                                value=float(st.session_state.dados.get("area", 1.0)), key="rec_area")
            rec_cultura       = st.selectbox("Cultura", get_culturas() + [
                                             "Arroz","Cana-de-AÃÂ§ÃÂºcar","CafÃÂ©","Pastagem","Outro"], key="rec_cult")
            rec_alvo          = st.text_input("Alvo / Problema a combater",
                                              placeholder="Ex: Ferrugem asiÃÂ¡tica, Lagarta-do-cartucho", key="rec_alvo")

        with col_r2:
            st.markdown("**Ã°Å¸Â§âÃ¢â¬ÂÃ°Å¸âÂ¼ Dados do ResponsÃÂ¡vel TÃÂ©cnico**")
            rec_rt_nome       = st.text_input("Nome do Engenheiro AgrÃÂ´nomo / RT", key="rec_rt_nome")
            rec_rt_crea       = st.text_input("CREA / CRBio nÃÂº", placeholder="123456-D/SP", key="rec_rt_crea")
            rec_rt_email      = st.text_input("E-mail do RT", key="rec_rt_email")
            rec_rt_telefone   = st.text_input("Telefone do RT", key="rec_rt_tel")
            rec_data_emissao  = st.date_input("Data de EmissÃÂ£o", value=date.today(), key="rec_data")
            rec_validade_dias = st.number_input("Validade (dias)", min_value=1, max_value=365, value=30, key="rec_val")
            rec_numero        = st.text_input("NÃÂºmero do ReceituÃÂ¡rio", placeholder="001/2026", key="rec_num")

        st.divider()
        st.subheader("Ã°Å¸Â§Âª Produtos Recomendados")

        qtd_prods_rec = st.number_input("Quantidade de produtos", min_value=1, max_value=8, value=1, key="rec_qtd_prods")
        produtos_rec  = []

        for i in range(int(qtd_prods_rec)):
            st.markdown(f"**Produto {i+1}**")
            cr1, cr2, cr3, cr4, cr5 = st.columns([3, 2, 1, 1, 2])
            with cr1:
                # Busca no catÃÂ¡logo ou digitaÃÂ§ÃÂ£o livre
                opcoes_estoque = [p["Insumo"] for p in st.session_state.estoque] if st.session_state.estoque else []
                if opcoes_estoque:
                    nome_prod_rec = st.selectbox(f"Produto {i+1}", opcoes_estoque, key=f"rec_prod_{i}")
                    # Buscar IA do catÃÂ¡logo se disponÃÂ­vel
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
                            f'Ã°Å¸âÂ¦ Total para {rec_area_ha:.1f} ha: <b>{total_produto:.2f} {unid_rec.replace("/ha","").replace("/100L","")}</b>'
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
        st.subheader("Ã¢Å¡â¢Ã¯Â¸Â RecomendaÃÂ§ÃÂµes de AplicaÃÂ§ÃÂ£o")
        col_ap1, col_ap2, col_ap3 = st.columns(3)
        with col_ap1:
            rec_volume_calda  = st.number_input("Volume de calda (L/ha)", min_value=0.0, value=100.0, key="rec_vol")
            rec_equipamento   = st.selectbox("Equipamento", ["Pulverizador tratorizado","Pulverizador costal",
                                             "AviÃÂ£o agrÃÂ­cola","Drone","PivÃÂ´ central","Outro"], key="rec_equip")
        with col_ap2:
            rec_epoca         = st.text_input("Ãâ°poca de aplicaÃÂ§ÃÂ£o", placeholder="Ex: EstÃÂ¡dio R1 da soja", key="rec_epoca")
            rec_intervalo     = st.number_input("Intervalo entre aplicaÃÂ§ÃÂµes (dias)", min_value=0, value=14, key="rec_intv")
        with col_ap3:
            rec_epi           = st.multiselect("EPI obrigatÃÂ³rio", ["MacacÃÂ£o","Luvas nitrÃÂ­licas","Botas de borracha",
                                               "MÃÂ¡scara com filtro","Ãâculos de proteÃÂ§ÃÂ£o","Avental impermeÃÂ¡vel",
                                               "ChapÃÂ©u de abas largas"], key="rec_epi")
            rec_carencia      = st.number_input("Prazo de carÃÂªncia (dias)", min_value=0, value=14, key="rec_car")

        rec_observacoes = st.text_area("ObservaÃÂ§ÃÂµes / RecomendaÃÂ§ÃÂµes adicionais", key="rec_obs",
                                       placeholder="Ex: NÃÂ£o aplicar com ventos acima de 10 km/h...")

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("Ã°Å¸âÂ¾ Salvar ReceituÃÂ¡rio", key="btn_salvar_rec", use_container_width=True):
                if not rec_produtor.strip():
                    error_box("Informe o nome do produtor.")
                elif not rec_rt_nome.strip():
                    error_box("Informe o nome do ResponsÃÂ¡vel TÃÂ©cnico.")
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
                    success_box(f"Ã¢Åâ¦ ReceituÃÂ¡rio {novo_rec['numero']} salvo com sucesso!")

        with col_btn2:
            # Gerar PDF do ÃÂºltimo receituÃÂ¡rio preenchido
            if st.button("Ã°Å¸âÂ¨Ã¯Â¸Â Gerar PDF", key="btn_pdf_rec", use_container_width=True):
                if not rec_produtor.strip() or not rec_rt_nome.strip():
                    error_box("Preencha ao menos produtor e ResponsÃÂ¡vel TÃÂ©cnico antes de gerar o PDF.")
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

                        # Ã¢ââ¬Ã¢ââ¬ CabeÃÂ§alho
                        titulo_sty = ParagraphStyle("titulo", parent=sty_r["Title"],
                                                    fontSize=16, textColor=colors.HexColor("#0f3460"),
                                                    alignment=TA_CENTER)
                        sub_sty    = ParagraphStyle("sub", parent=sty_r["Normal"],
                                                    fontSize=10, textColor=colors.HexColor("#1e3a5f"),
                                                    alignment=TA_CENTER)

                        if os.path.exists("IAAgrologo.jpeg"):
                            el_r.append(Image("IAAgrologo.jpeg", width=2.5*cm, height=1.2*cm))
                        el_r.append(Spacer(1, 6))
                        el_r.append(Paragraph("RECEITUÃÂRIO AGRONÃâMICO", titulo_sty))
                        el_r.append(Paragraph(f"Lei 7.802/89 | Decreto 4.074/02", sub_sty))
                        el_r.append(Paragraph(f"NÃÂº {rec_numero or '---'} | EmissÃÂ£o: {rec_data_emissao.strftime('%d/%m/%Y')} | "
                                              f"Validade: {rec_validade_dias} dias", sub_sty))
                        el_r.append(Spacer(1, 10))

                        # Ã¢ââ¬Ã¢ââ¬ Linha horizontal
                        from reportlab.platypus import HRFlowable
                        el_r.append(HRFlowable(width="100%", thickness=2,
                                               color=colors.HexColor("#0f3460")))
                        el_r.append(Spacer(1, 8))

                        # Ã¢ââ¬Ã¢ââ¬ Dados do Produtor
                        el_r.append(Paragraph("<b>DADOS DO PRODUTOR</b>", sty_r["Heading2"]))
                        dados_prod = [
                            ["Produtor / RazÃÂ£o Social:", rec_produtor,     "CPF / CNPJ:", rec_cpf_cnpj],
                            ["Propriedade:",             rec_propriedade,  "MunicÃÂ­pio/UF:", rec_municipio],
                            ["Cultura:",                 rec_cultura,      "ÃÂrea (ha):",  f"{rec_area_ha:.2f} ha"],
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

                        # Ã¢ââ¬Ã¢ââ¬ Produtos recomendados
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

                        # Ã¢ââ¬Ã¢ââ¬ RecomendaÃÂ§ÃÂµes de aplicaÃÂ§ÃÂ£o
                        el_r.append(Paragraph("<b>RECOMENDAÃâ¡Ãâ¢ES DE APLICAÃâ¡ÃÆO</b>", sty_r["Heading2"]))
                        dados_aplic = [
                            ["Volume de calda:", f"{rec_volume_calda:.0f} L/ha", "Equipamento:", rec_equipamento],
                            ["Ãâ°poca de aplicaÃÂ§ÃÂ£o:", rec_epoca, "Intervalo:", f"{rec_intervalo} dias"],
                            ["Prazo de carÃÂªncia:", f"{rec_carencia} dias", "EPI:", ", ".join(rec_epi) if rec_epi else "Conforme bula"],
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
                            el_r.append(Paragraph("<b>OBSERVAÃâ¡Ãâ¢ES:</b>", sty_r["Heading3"]))
                            el_r.append(Paragraph(rec_observacoes, sty_r["BodyText"]))

                        el_r.append(Spacer(1, 16))
                        el_r.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
                        el_r.append(Spacer(1, 10))

                        # Ã¢ââ¬Ã¢ââ¬ Assinaturas
                        el_r.append(Paragraph("<b>RESPONSÃÂVEL TÃâ°CNICO</b>", sty_r["Heading2"]))
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
                                    [f"Assinatura do RT Ã¢â¬â {rec_rt_crea}", "   ",
                                     f"Assinatura do Produtor Ã¢â¬â {rec_cpf_cnpj}"]]
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
                            f'Este receituÃÂ¡rio ÃÂ© vÃÂ¡lido por {rec_validade_dias} dias a partir da emissÃÂ£o.</font>',
                            sty_r["Normal"]
                        ))

                        doc_r.build(el_r)
                        pdf_rec = buf_r.getvalue()
                        buf_r.close()

                        num_arquivo = (rec_numero or "receituario").replace("/","_").replace(" ","_")
                        st.download_button(
                            "Ã°Å¸âÂ¥ Baixar ReceituÃÂ¡rio PDF",
                            data=pdf_rec,
                            file_name=f"Receituario_{num_arquivo}_{rec_produtor[:15].replace(' ','_')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        error_box(f"Erro ao gerar PDF: {e}")

    # Ã¢ââ¬Ã¢ââ¬ ABA HISTÃâRICO Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
    with tab_historico_rec:
        st.subheader("Ã°Å¸âÂ ReceituÃÂ¡rios Emitidos")
        if not st.session_state.receituarios:
            info_box("Nenhum receituÃÂ¡rio salvo ainda.")
        else:
            # Tabela resumo
            resumo = []
            for r in st.session_state.receituarios:
                resumo.append({
                    "NÃÂº":         r.get("numero",""),
                    "Data":       r.get("data_emissao",""),
                    "Produtor":   r.get("produtor",""),
                    "Cultura":    r.get("cultura",""),
                    "ÃÂrea (ha)":  r.get("area_ha",0),
                    "Alvo":       r.get("alvo",""),
                    "RT":         r.get("rt_nome",""),
                    "Validade":   r.get("validade_ate","")[:10] if r.get("validade_ate") else "",
                })
            df_rec_hist = pd.DataFrame(resumo)
            st.dataframe(df_rec_hist, use_container_width=True, hide_index=True)

            # Ver detalhes / regerar PDF
            st.divider()
            opcoes_rec = [f"{r.get('numero',i)} Ã¢â¬â {r.get('produtor','')} Ã¢â¬â {r.get('data_emissao','')}"
                          for i, r in enumerate(st.session_state.receituarios)]
            sel_rec = st.selectbox("Selecionar receituÃÂ¡rio", opcoes_rec, key="sel_rec_hist")
            idx_sel = opcoes_rec.index(sel_rec)
            rec_sel = st.session_state.receituarios[idx_sel]

            with st.expander("Ã°Å¸âÂÃ¯Â¸Â Ver detalhes completos", expanded=False):
                col_det1, col_det2 = st.columns(2)
                with col_det1:
                    st.markdown(f"**Produtor:** {rec_sel.get('produtor','')}")
                    st.markdown(f"**CPF/CNPJ:** {rec_sel.get('cpf_cnpj','')}")
                    st.markdown(f"**Propriedade:** {rec_sel.get('propriedade','')}")
                    st.markdown(f"**MunicÃÂ­pio:** {rec_sel.get('municipio','')}")
                    st.markdown(f"**Cultura:** {rec_sel.get('cultura','')} Ã¢â¬â {rec_sel.get('area_ha',0)} ha")
                    st.markdown(f"**Alvo:** {rec_sel.get('alvo','')}")
                with col_det2:
                    st.markdown(f"**RT:** {rec_sel.get('rt_nome','')}")
                    st.markdown(f"**CREA:** {rec_sel.get('rt_crea','')}")
                    st.markdown(f"**EmissÃÂ£o:** {rec_sel.get('data_emissao','')}")
                    st.markdown(f"**VÃÂ¡lido atÃÂ©:** {rec_sel.get('validade_ate','')[:10]}")
                    st.markdown(f"**Equipamento:** {rec_sel.get('equipamento','')}")
                    st.markdown(f"**Volume calda:** {rec_sel.get('volume_calda',0)} L/ha")

                if rec_sel.get("produtos"):
                    st.markdown("**Produtos:**")
                    st.dataframe(pd.DataFrame(rec_sel["produtos"]), use_container_width=True, hide_index=True)

            # Excluir
            if st.button("Ã°Å¸ââÃ¯Â¸Â Excluir este receituÃÂ¡rio", key="btn_del_rec"):
                st.session_state.receituarios.pop(idx_sel)
                salvar_dados_iaagro()
                success_box("ReceituÃÂ¡rio excluÃÂ­do.")
                st.rerun()

            # Exportar todos em Excel
            if st.button("Ã°Å¸âÅ  Exportar todos para Excel", key="btn_xlsx_rec", use_container_width=True):
                rows_exp = []
                for r in st.session_state.receituarios:
                    base = {k: v for k, v in r.items() if k != "produtos"}
                    for j, p in enumerate(r.get("produtos", [])):
                        row = base.copy()
                        row.update({f"prod_{j+1}_{k}": v for k, v in p.items()})
                        rows_exp.append(row)
                    if not r.get("produtos"):
                        rows_exp.append(base)
                xlsx_r = exportar_excel({"ReceituÃÂ¡rios": rows_exp})
                if xlsx_r:
                    st.download_button("Ã°Å¸âÂ¥ Baixar Excel", data=xlsx_r,
                        file_name=f"receituarios_{date.today()}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True)


# Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
# MENU: COMPARATIVO DE SAFRAS
# Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
if menu == "Ã°Å¸âÂ° Financeiro":
  with _sub_fin[2]:
    st.header("Ã°Å¸âÅ  Comparativo de Safras")
    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
    Ã°Å¸âË Compare produtividade, custos e lucratividade entre todas as safras cadastradas.
    Identifique tendÃÂªncias e tome decisÃÂµes com base no histÃÂ³rico real da sua propriedade.
    </div>''', unsafe_allow_html=True)

    # Verificar dados disponÃÂ­veis
    tem_hist = len(st.session_state.historico_produtividade) > 0
    tem_dre  = len(st.session_state.get("dre_registros", [])) > 0

    if not tem_hist and not tem_dre:
        warning_box("Cadastre dados em 'HistÃÂ³rico de Produtividade' e/ou 'Dashboard Financeiro' para ver o comparativo.")
    else:
        try:
            import plotly.express as px
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            PLOTLY_OK = True
        except Exception:
            PLOTLY_OK = False

        tab_prod, tab_fin, tab_completo, tab_ia = st.tabs([
            "Ã°Å¸ÅÂ¾ Produtividade",
            "Ã°Å¸âÂ° Financeiro",
            "Ã°Å¸ââ¹ Comparativo Completo",
            "Ã°Å¸Â¤â AnÃÂ¡lise IA"
        ])

        # Ã¢ââ¬Ã¢ââ¬ TAB 1: PRODUTIVIDADE Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        with tab_prod:
            st.subheader("Ã°Å¸ÅÂ¾ EvoluÃÂ§ÃÂ£o da Produtividade por Safra")
            if not tem_hist:
                info_box("Cadastre dados em 'HistÃÂ³rico de Produtividade' para ver esta aba.")
            else:
                df_h = pd.DataFrame(st.session_state.historico_produtividade)

                # Filtros
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    areas_disp = ["Todas"] + sorted(df_h["ÃÂrea"].unique().tolist())
                    area_filtro_comp = st.selectbox("Filtrar por ÃÂ¡rea", areas_disp, key="comp_area_filtro")
                with col_f2:
                    culturas_disp = ["Todas"] + sorted(df_h["ÃÂrea"].unique().tolist())
                    min_safras = st.number_input("MÃÂ­nimo de safras para exibir", min_value=1, value=1, key="comp_min_safras")

                df_hf = df_h if area_filtro_comp == "Todas" else df_h[df_h["ÃÂrea"] == area_filtro_comp]

                if df_hf.empty:
                    info_box("Nenhum dado para o filtro selecionado.")
                else:
                    # MÃÂ©tricas gerais
                    media_geral  = df_hf["Produtividade"].mean()
                    melhor_safra = df_hf.loc[df_hf["Produtividade"].idxmax()]
                    pior_safra   = df_hf.loc[df_hf["Produtividade"].idxmin()]
                    tendencia    = df_hf.groupby("Safra")["Produtividade"].mean()
                    delta_trend  = tendencia.iloc[-1] - tendencia.iloc[0] if len(tendencia) > 1 else 0

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Ã°Å¸âÅ  MÃÂ©dia Geral", f"{media_geral:.1f} sc/ha")
                    c2.metric("Ã°Å¸Ââ  Melhor Safra", f"{melhor_safra['Produtividade']:.1f} sc/ha",
                              f"{melhor_safra['Safra']}")
                    c3.metric("Ã¢Â¬â¡Ã¯Â¸Â Pior Safra", f"{pior_safra['Produtividade']:.1f} sc/ha",
                              f"{pior_safra['Safra']}")
                    c4.metric("Ã°Å¸âË TendÃÂªncia", f"{delta_trend:+.1f} sc/ha",
                              "vs 1ÃÂª safra" if len(tendencia) > 1 else "Ã¢â¬â")

                    if PLOTLY_OK:
                        # GrÃÂ¡fico de barras por safra + linha de mÃÂ©dia
                        df_safra_media = df_hf.groupby("Safra")["Produtividade"].mean().reset_index()
                        df_safra_media.columns = ["Safra","MÃÂ©dia sc/ha"]

                        fig_bar = go.Figure()
                        fig_bar.add_trace(go.Bar(
                            x=df_safra_media["Safra"],
                            y=df_safra_media["MÃÂ©dia sc/ha"],
                            marker_color=[
                                "#22c55e" if v >= media_geral else "#f59e0b"
                                for v in df_safra_media["MÃÂ©dia sc/ha"]
                            ],
                            text=[f"{v:.1f}" for v in df_safra_media["MÃÂ©dia sc/ha"]],
                            textposition="outside",
                            name="Produtividade"
                        ))
                        fig_bar.add_hline(y=media_geral, line_dash="dash",
                                          line_color="#6ee7b7",
                                          annotation_text=f"MÃÂ©dia: {media_geral:.1f}",
                                          annotation_font_color="#6ee7b7")
                        fig_bar.update_layout(
                            title="Produtividade MÃÂ©dia por Safra (sc/ha)",
                            paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",
                            font_color="#f1f5f9", height=380,
                            xaxis_title="Safra", yaxis_title="sc/ha",
                            yaxis=dict(gridcolor="#1e3a5f"),
                            showlegend=False
                        )
                        st.plotly_chart(fig_bar, use_container_width=True)

                        # EvoluÃÂ§ÃÂ£o por ÃÂ¡rea (se mÃÂºltiplas)
                        if df_hf["ÃÂrea"].nunique() > 1:
                            fig_line = px.line(
                                df_hf.groupby(["Safra","ÃÂrea"])["Produtividade"].mean().reset_index(),
                                x="Safra", y="Produtividade", color="ÃÂrea",
                                title="EvoluÃÂ§ÃÂ£o por ÃÂrea/TalhÃÂ£o",
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
                                title="DistribuiÃÂ§ÃÂ£o de Produtividade por Safra",
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
                    st.subheader("Ã°Å¸ââ¹ Dados por Safra")
                    df_tab_comp = df_hf.groupby("Safra").agg(
                        MÃÂ©dia=("Produtividade","mean"),
                        MÃÂ­nimo=("Produtividade","min"),
                        MÃÂ¡ximo=("Produtividade","max"),
                        Registros=("Produtividade","count")
                    ).round(1).reset_index()
                    df_tab_comp["vs MÃÂ©dia"] = (df_tab_comp["MÃÂ©dia"] - media_geral).round(1)
                    st.dataframe(df_tab_comp, use_container_width=True, hide_index=True)

        # Ã¢ââ¬Ã¢ââ¬ TAB 2: FINANCEIRO Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        with tab_fin:
            st.subheader("Ã°Å¸âÂ° Comparativo Financeiro entre Safras")
            if not tem_dre:
                info_box("Cadastre lanÃÂ§amentos em 'Dashboard Financeiro' para ver esta aba.")
            else:
                df_dre_all = pd.DataFrame(st.session_state.dre_registros)

                df_fin_comp = df_dre_all.groupby(["Safra","Tipo"])["Valor R$"].sum().unstack(fill_value=0).reset_index()

                # Garantir colunas mesmo que faltem
                for col in ["Receita","Custo VariÃÂ¡vel","Custo Fixo"]:
                    if col not in df_fin_comp.columns:
                        df_fin_comp[col] = 0

                df_fin_comp["Custo Total"] = df_fin_comp.get("Custo VariÃÂ¡vel",0) + df_fin_comp.get("Custo Fixo",0)
                df_fin_comp["Lucro"]       = df_fin_comp["Receita"] - df_fin_comp["Custo Total"]
                df_fin_comp["Margem %"]    = (df_fin_comp["Lucro"] / df_fin_comp["Receita"] * 100).round(1).where(df_fin_comp["Receita"]>0, 0)

                # ÃÂrea por safra (para mÃÂ©tricas /ha)
                df_area_safra = df_dre_all.groupby("Safra")["ÃÂrea ha"].max().reset_index()
                df_fin_comp   = df_fin_comp.merge(df_area_safra, on="Safra", how="left")
                df_fin_comp["ÃÂrea ha"] = df_fin_comp["ÃÂrea ha"].fillna(1)
                df_fin_comp["Receita/ha"]   = (df_fin_comp["Receita"] / df_fin_comp["ÃÂrea ha"]).round(0)
                df_fin_comp["Custo/ha"]     = (df_fin_comp["Custo Total"] / df_fin_comp["ÃÂrea ha"]).round(0)
                df_fin_comp["Lucro/ha"]     = (df_fin_comp["Lucro"] / df_fin_comp["ÃÂrea ha"]).round(0)

                # MÃÂ©tricas de destaque
                melhor_lucro = df_fin_comp.loc[df_fin_comp["Lucro"].idxmax()] if not df_fin_comp.empty else None
                media_margem = df_fin_comp["Margem %"].mean()

                if melhor_lucro is not None:
                    cm1, cm2, cm3, cm4 = st.columns(4)
                    cm1.metric("Ã°Å¸Ââ  Melhor Lucro", f"R$ {melhor_lucro['Lucro']:,.0f}", melhor_lucro["Safra"])
                    cm2.metric("Ã°Å¸âÅ  Margem MÃÂ©dia", f"{media_margem:.1f}%")
                    cm3.metric("Ã°Å¸âÂ° Maior Receita", f"R$ {df_fin_comp['Receita'].max():,.0f}")
                    cm4.metric("Ã°Å¸âÂ¸ Menor Custo/ha", f"R$ {df_fin_comp['Custo/ha'].min():,.0f}/ha")

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

                    # EvoluÃÂ§ÃÂ£o da margem
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
                            title="EvoluÃÂ§ÃÂ£o da Margem LÃÂ­quida (%)",
                            paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",
                            font_color="#f1f5f9", height=300,
                            yaxis=dict(gridcolor="#1e3a5f"),
                            xaxis_title="Safra", yaxis_title="Margem %"
                        )
                        st.plotly_chart(fig_margem, use_container_width=True)

                # Tabela financeira completa
                st.subheader("Ã°Å¸ââ¹ Resumo Financeiro por Safra")
                cols_exib = ["Safra","Receita","Custo Total","Lucro","Margem %","Receita/ha","Custo/ha","Lucro/ha","ÃÂrea ha"]
                st.dataframe(df_fin_comp[[c for c in cols_exib if c in df_fin_comp.columns]].round(1),
                             use_container_width=True, hide_index=True)

        # Ã¢ââ¬Ã¢ââ¬ TAB 3: COMPARATIVO COMPLETO Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        with tab_completo:
            st.subheader("Ã°Å¸ââ¹ Painel Completo Ã¢â¬â Produtividade + Financeiro")

            if not tem_hist and not tem_dre:
                info_box("Sem dados suficientes.")
            else:
                # Unir produtividade e financeiro por safra
                dados_comp = {}

                if tem_hist:
                    df_hc = pd.DataFrame(st.session_state.historico_produtividade)
                    for safra, grp in df_hc.groupby("Safra"):
                        dados_comp.setdefault(safra, {})["Prod. MÃÂ©dia sc/ha"] = round(grp["Produtividade"].mean(), 1)
                        dados_comp[safra]["Custo HistÃÂ³rico/ha"] = round(grp["Custo"].mean(), 2)

                if tem_dre:
                    df_dc = pd.DataFrame(st.session_state.dre_registros)
                    for safra, grp in df_dc.groupby("Safra"):
                        rec   = grp[grp["Tipo"]=="Receita"]["Valor R$"].sum()
                        custo = grp[grp["Tipo"].isin(["Custo VariÃÂ¡vel","Custo Fixo"])]["Valor R$"].sum()
                        lucro = rec - custo
                        area  = grp["ÃÂrea ha"].max() if not grp.empty else 1
                        dados_comp.setdefault(safra, {})["Receita R$"]  = round(rec, 0)
                        dados_comp[safra]["Custo Total R$"] = round(custo, 0)
                        dados_comp[safra]["Lucro R$"]       = round(lucro, 0)
                        dados_comp[safra]["Margem %"]       = round(lucro/rec*100, 1) if rec > 0 else 0
                        dados_comp[safra]["ÃÂrea ha"]        = area

                df_comp_final = pd.DataFrame(dados_comp).T.reset_index().rename(columns={"index":"Safra"})
                df_comp_final = df_comp_final.sort_values("Safra")

                # Highlight melhor linha
                st.dataframe(df_comp_final, use_container_width=True, hide_index=True)

                if PLOTLY_OK and "Prod. MÃÂ©dia sc/ha" in df_comp_final.columns and "Lucro R$" in df_comp_final.columns:
                    df_plot_dual = df_comp_final.dropna(subset=["Prod. MÃÂ©dia sc/ha","Lucro R$"])
                    if not df_plot_dual.empty:
                        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
                        fig_dual.add_trace(go.Bar(
                            name="Produtividade sc/ha", x=df_plot_dual["Safra"],
                            y=df_plot_dual["Prod. MÃÂ©dia sc/ha"], marker_color="#22c55e",
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
                    st.download_button("Ã°Å¸âÂ¥ Exportar Comparativo Excel", data=xlsx_comp,
                        file_name=f"comparativo_safras_{date.today()}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True)

        # Ã¢ââ¬Ã¢ââ¬ TAB 4: ANÃÂLISE IA Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        with tab_ia:
            st.subheader("Ã°Å¸Â¤â AnÃÂ¡lise Comparativa por InteligÃÂªncia Artificial")

            if st.button("Ã°Å¸Å¡â¬ Gerar AnÃÂ¡lise IA das Safras", key="btn_ia_comp", use_container_width=True):
                with st.spinner("Ã°Å¸Â¤â Analisando histÃÂ³rico de safras..."):
                    # Montar resumo para o prompt
                    resumo_hist = ""
                    if tem_hist:
                        df_hr = pd.DataFrame(st.session_state.historico_produtividade)
                        for safra, grp in df_hr.groupby("Safra"):
                            resumo_hist += (f"Safra {safra}: prod. mÃÂ©dia {grp['Produtividade'].mean():.1f} sc/ha, "
                                           f"custo {grp['Custo'].mean():.2f} R$/ha\n")

                    resumo_fin = ""
                    if tem_dre:
                        df_dr = pd.DataFrame(st.session_state.dre_registros)
                        for safra, grp in df_dr.groupby("Safra"):
                            rec   = grp[grp["Tipo"]=="Receita"]["Valor R$"].sum()
                            custo = grp[grp["Tipo"].isin(["Custo VariÃÂ¡vel","Custo Fixo"])]["Valor R$"].sum()
                            lucro = rec - custo
                            margem = lucro/rec*100 if rec > 0 else 0
                            resumo_fin += (f"Safra {safra}: receita R$ {rec:,.0f}, custo R$ {custo:,.0f}, "
                                          f"lucro R$ {lucro:,.0f}, margem {margem:.1f}%\n")

                    prompt_comp = f"""VocÃÂª ÃÂ© um consultor agrÃÂ­cola analisando o histÃÂ³rico de safras de uma propriedade rural brasileira no sistema IAAgro Pro.

HISTÃâRICO DE PRODUTIVIDADE:
{resumo_hist if resumo_hist else "Sem dados de produtividade."}

HISTÃâRICO FINANCEIRO:
{resumo_fin if resumo_fin else "Sem dados financeiros."}

Gere uma anÃÂ¡lise comparativa profissional com:
1. TENDÃÅ NCIA PRODUTIVA Ã¢â¬â a propriedade estÃÂ¡ evoluindo ou regredindo? Por quÃÂª?
2. EFICIÃÅ NCIA FINANCEIRA Ã¢â¬â qual safra teve melhor relaÃÂ§ÃÂ£o custo-benefÃÂ­cio?
3. PONTOS DE ATENÃâ¡ÃÆO Ã¢â¬â o que chama atenÃÂ§ÃÂ£o negativamente?
4. DESTAQUES POSITIVOS Ã¢â¬â o que estÃÂ¡ indo bem?
5. RECOMENDAÃâ¡Ãâ¢ES ESTRATÃâ°GICAS Ã¢â¬â top 3 aÃÂ§ÃÂµes para melhorar resultados nas prÃÂ³ximas safras
6. PROJEÃâ¡ÃÆO Ã¢â¬â se mantida a tendÃÂªncia, qual a expectativa para a prÃÂ³xima safra?

Seja objetivo, tÃÂ©cnico e prÃÂ¡tico para o produtor rural brasileiro. MÃÂ¡ximo 400 palavras."""

                    try:
                        resp_ia = requests.post(
                            "https://api.anthropic.com/v1/messages",
                            headers={"Content-Type":"application/json"},
                            json={"model": "claude-sonnet-4-20250514","max_tokens":900,
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

                            # PDF da anÃÂ¡lise
                            if st.button("Ã°Å¸âÂ¨Ã¯Â¸Â Gerar PDF da AnÃÂ¡lise", key="btn_pdf_comp"):
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
                                    el_cp.append(Paragraph("<b>ANÃÂLISE COMPARATIVA DE SAFRAS Ã¢â¬â IAAgro IA</b>", sty_cp["Title"]))
                                    el_cp.append(Paragraph(f"Gerado em: {date.today().strftime('%d/%m/%Y')}", sty_cp["Normal"]))
                                    el_cp.append(Spacer(1,12))
                                    el_cp.append(Paragraph("<b>HISTÃâRICO DE PRODUTIVIDADE</b>", sty_cp["Heading2"]))
                                    for linha in resumo_hist.split("\n"):
                                        if linha.strip():
                                            el_cp.append(Paragraph(linha, sty_cp["BodyText"]))
                                    el_cp.append(Spacer(1,8))
                                    el_cp.append(Paragraph("<b>HISTÃâRICO FINANCEIRO</b>", sty_cp["Heading2"]))
                                    for linha in resumo_fin.split("\n"):
                                        if linha.strip():
                                            el_cp.append(Paragraph(linha, sty_cp["BodyText"]))
                                    el_cp.append(Spacer(1,12))
                                    el_cp.append(Paragraph("<b>ANÃÂLISE IA</b>", sty_cp["Heading2"]))
                                    el_cp.append(Spacer(1,6))
                                    for linha in analise_comp.split("\n"):
                                        if linha.strip():
                                            el_cp.append(Paragraph(linha, sty_cp["BodyText"]))
                                            el_cp.append(Spacer(1,3))
                                    doc_cp.build(el_cp)
                                    pdf_cp = buf_cp.getvalue()
                                    buf_cp.close()
                                    st.download_button("Ã°Å¸âÂ¥ Baixar PDF", data=pdf_cp,
                                        file_name=f"analise_safras_{date.today()}.pdf",
                                        mime="application/pdf", use_container_width=True)
                                except Exception as ep:
                                    error_box(f"Erro PDF: {ep}")
                        else:
                            warning_box("IA indisponÃÂ­vel. Verifique a conexÃÂ£o.")
                    except Exception as e:
                        error_box(f"Erro na anÃÂ¡lise IA: {e}")


# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: MAPA DE COLHEITA IA
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸ÅÂ InteligÃÂªncia":
  with _sub_int[2]:
    st.header("Ã°Å¸âÂºÃ¯Â¸Â Mapa de Colheita Ã¢â¬â AnÃÂ¡lise por InteligÃÂªncia Artificial")
    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
    Ã°Å¸âÂ¡ Carregue o mapa de colheita gerado pela colheitadeira (John Deere, Case, New Holland, Claas, etc.)
    nos formatos CSV, Excel, GeoJSON ou Shapefile. A IA analisa produtividade por zona,
    variabilidade espacial, pontos crÃÂ­ticos e gera recomendaÃÂ§ÃÂµes de manejo.
    </div>''', unsafe_allow_html=True)

    # Ã¢ââ¬Ã¢ââ¬ DependÃÂªncias opcionais Ã¢ââ¬Ã¢ââ¬
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
        Ã¢Å¡Â Ã¯Â¸Â Para anÃÂ¡lise completa instale: pip install numpy plotly geopandas</div>''',
        unsafe_allow_html=True)

    # Ã¢â¢ÂÃ¢â¢Â FUNÃâ¡Ãâ¢ES AUXILIARES Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
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
        df["Zona"] = df[col_prod].apply(lambda v: "Ã°Å¸âÂ´ Baixa" if v < p33 else ("Ã°Å¸Å¸Â¡ MÃÂ©dia" if v < p66 else "Ã°Å¸Å¸Â¢ Alta"))
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
            for z in ["Ã°Å¸âÂ´ Baixa","Ã°Å¸Å¸Â¡ MÃÂ©dia","Ã°Å¸Å¸Â¢ Alta"]:
                sub = df[df["Zona"]==z]
                s[f"pct_{z}"] = round(len(sub)/len(df)*100, 1)
                s[f"med_{z}"] = round(sub[col_prod].mean(), 1) if len(sub) > 0 else 0
        return s

    def gerar_recomendacoes(stats, col_prod, cultura, area_ha):
        cv        = stats.get("cv", 0)
        media     = stats.get("media", 0)
        pct_baixa = stats.get("pct_Ã°Å¸âÂ´ Baixa", 0)
        pct_alta  = stats.get("pct_Ã°Å¸Å¸Â¢ Alta",  0)
        med_baixa = stats.get("med_Ã°Å¸âÂ´ Baixa", 0)
        med_alta  = stats.get("med_Ã°Å¸Å¸Â¢ Alta",  0)
        gap       = med_alta - med_baixa
        recs = []

        if cv > 35:
            recs.append({"zona":"Campo todo","tipo":"Ã¢Å¡Â Ã¯Â¸Â ALTA VARIABILIDADE","cor":"#7f1d1d","borda":"#ef4444",
                "texto":f"CV de {cv:.1f}% indica alta heterogeneidade espacial. Implante AplicaÃÂ§ÃÂ£o em Taxa "
                        f"VariÃÂ¡vel (VRA). Realize amostragem por zona de manejo e verifique histÃÂ³rico de compactaÃÂ§ÃÂ£o."})
        elif cv > 20:
            recs.append({"zona":"Campo todo","tipo":"Ã¢âÂ¹Ã¯Â¸Â VARIABILIDADE MODERADA","cor":"#1e3a5f","borda":"#3b82f6",
                "texto":f"CV de {cv:.1f}% ÃÂ© moderado. Avalie mapeamento de solo para identificar causas da variabilidade."})
        else:
            recs.append({"zona":"Campo todo","tipo":"Ã¢Åâ¦ BOA UNIFORMIDADE","cor":"#14532d","borda":"#22c55e",
                "texto":f"CV de {cv:.1f}% indica boa uniformidade. Continue o manejo atual."})

        if pct_baixa > 15:
            recs.append({"zona":"Ã°Å¸âÂ´ Zona Baixa","tipo":"Ã°Å¸âÂ´ INTERVENÃâ¡ÃÆO PRIORITÃÂRIA","cor":"#7f1d1d","borda":"#ef4444",
                "texto":f"{pct_baixa:.0f}% da ÃÂ¡rea com produtividade baixa (mÃÂ©dia {med_baixa:.1f}). AÃÂ§ÃÂµes: "
                        f"(1) Coleta de solo detalhada por zona; "
                        f"(2) Investigar compactaÃÂ§ÃÂ£o com penetrÃÂ´metro; "
                        f"(3) Verificar drenagem e histÃÂ³rico de doenÃÂ§as; "
                        f"(4) Aumentar dose de P e K em Ã¢â°Ë30%; "
                        f"(5) Considerar calagem diferenciada se pH < 5.8."})

        if pct_alta > 20 and med_alta > 0:
            recs.append({"zona":"Ã°Å¸Å¸Â¢ Zona Alta","tipo":"Ã°Å¸Å¸Â¢ POTENCIAL A EXPLORAR","cor":"#14532d","borda":"#22c55e",
                "texto":f"Zona de alta produtividade ({pct_alta:.0f}% da ÃÂ¡rea, mÃÂ©dia {med_alta:.1f}). "
                        f"Mantenha adubaÃÂ§ÃÂ£o de reposiÃÂ§ÃÂ£o precisa. Priorize fungicidas preventivos. "
                        f"Use como referÃÂªncia para seleÃÂ§ÃÂ£o de cultivares de alto potencial."})

        if gap > 10:
            ganho = gap * 0.4 * area_ha
            recs.append({"zona":"Zonas B vs A","tipo":"Ã°Å¸âÅ  GAP PRODUTIVO","cor":"#78350f","borda":"#f59e0b",
                "texto":f"DiferenÃÂ§a de {gap:.1f} sc/ha entre zonas alta e baixa. "
                        f"Potencial de ganho com manejo diferenciado: Ã¢â°Ë{ganho:.0f} sacas adicionais/safra "
                        f"elevando zona baixa em 40%."})

        bench = {"Soja":60,"Milho":180,"Trigo":55,"FeijÃÂ£o":40,"Arroz":160,"AlgodÃÂ£o":280,"CafÃÂ©":35}.get(cultura, 60)
        if media < bench * 0.75:
            recs.append({"zona":"Toda lavoura","tipo":f"Ã°Å¸ââ° ABAIXO DO POTENCIAL ({cultura})","cor":"#4a044e","borda":"#a855f7",
                "texto":f"MÃÂ©dia {media:.1f} estÃÂ¡ {((bench-media)/bench*100):.0f}% abaixo da referÃÂªncia "
                        f"regional ({bench} para {cultura}). Revisar programa completo: solo, semente, nutriÃÂ§ÃÂ£o e fitossanidade."})
        elif media >= bench:
            recs.append({"zona":"Toda lavoura","tipo":f"Ã°Å¸Ââ  ACIMA DA MÃâ°DIA ({cultura})","cor":"#064e3b","borda":"#10b981",
                "texto":f"ParabÃÂ©ns! MÃÂ©dia {media:.1f} supera a referÃÂªncia de {bench} para {cultura}. "
                        f"Documente o manejo desta safra como referÃÂªncia para as prÃÂ³ximas."})
        return recs

    def chamar_ia_colheita(stats, col_prod, cultura, area_ha, nome_arquivo, recs):
        try:
            resumo_rec = "\n".join([f"- {r['tipo']} ({r['zona']}): {r['texto'][:100]}..." for r in recs])
            prompt = f"""VocÃÂª ÃÂ© um agrÃÂ´nomo especialista em agricultura de precisÃÂ£o analisando um mapa de colheita do app IAAgro.

DADOS:
- Arquivo: {nome_arquivo} | Cultura: {cultura} | ÃÂrea: {area_ha} ha | Pontos: {stats['total_pts']}

ESTATÃÂSTICAS:
- MÃÂ©dia: {stats['media']:.1f} sc/ha | Mediana: {stats['mediana']:.1f}
- MÃÂ­nimo: {stats['minimo']:.1f} | MÃÂ¡ximo: {stats['maximo']:.1f}
- Desvio padrÃÂ£o: {stats['desvio']:.1f} | CV: {stats['cv']:.1f}%
- Zona Baixa: {stats.get('pct_Ã°Å¸âÂ´ Baixa',0):.0f}% da ÃÂ¡rea (mÃÂ©dia {stats.get('med_Ã°Å¸âÂ´ Baixa',0):.1f})
- Zona MÃÂ©dia: {stats.get('pct_Ã°Å¸Å¸Â¡ MÃÂ©dia',0):.0f}% da ÃÂ¡rea (mÃÂ©dia {stats.get('med_Ã°Å¸Å¸Â¡ MÃÂ©dia',0):.1f})
- Zona Alta:  {stats.get('pct_Ã°Å¸Å¸Â¢ Alta',0):.0f}% da ÃÂ¡rea (mÃÂ©dia {stats.get('med_Ã°Å¸Å¸Â¢ Alta',0):.1f})

RECOMENDAÃâ¡Ãâ¢ES AUTOMÃÂTICAS:
{resumo_rec}

Gere um laudo agronÃÂ´mico profissional com:
1. DIAGNÃâSTICO GERAL (2-3 frases sobre desempenho da lavoura)
2. ANÃÂLISE DA VARIABILIDADE ESPACIAL (interprete o CV e causas provÃÂ¡veis)
3. PRIORIDADES DE MANEJO (top 3 aÃÂ§ÃÂµes para prÃÂ³xima safra)
4. PROJEÃâ¡ÃÆO DE GANHO (o que ÃÂ© possÃÂ­vel alcanÃÂ§ar com manejo diferenciado)
5. NOTA DO TALHÃÆO (0-100 com justificativa breve)

Seja direto, tÃÂ©cnico e acessÃÂ­vel ao produtor rural brasileiro. MÃÂ¡ximo 350 palavras."""
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={"Content-Type":"application/json"},
                json={"model": "claude-sonnet-4-20250514","max_tokens":900,
                      "messages":[{"role":"user","content":prompt}]},
                timeout=35
            )
            if resp.status_code == 200:
                return resp.json()["content"][0]["text"]
        except Exception:
            pass  # erro silenciado intencionalmente
        return None

    # Ã¢â¢ÂÃ¢â¢Â UPLOAD Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    st.subheader("Ã°Å¸ââ Carregar Mapa de Colheita")
    col_up1, col_up2 = st.columns([2,1])
    with col_up1:
        arquivo = st.file_uploader(
            "Selecione o arquivo",
            type=["csv","xlsx","xls","geojson","json","zip"],
            help="CSV/Excel: John Deere Ops Center, Climate, AFS Connect | GeoJSON/Shapefile ZIP"
        )
    with col_up2:
        cultura_mapa = st.selectbox("Cultura", get_culturas() + ["Outro"], key="cultura_mapa_sel")
        area_mapa    = st.number_input("ÃÂrea (ha)", min_value=0.1, value=float(st.session_state.dados.get("area",50.0)), key="area_mapa_num")

    if arquivo is not None and arquivo.name != st.session_state.harvest_arquivo:
        st.session_state.harvest_arquivo = arquivo.name
        st.session_state.harvest_df      = None
        st.session_state.harvest_analise = None
        with st.spinner(f"Ã¢ÂÂ³ Lendo {arquivo.name}..."):
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
                        except Exception: pass  # erro silenciado Ã¢â¬â nÃÂ£o crÃÂ­tico
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
                                except Exception: pass  # erro silenciado Ã¢â¬â nÃÂ£o crÃÂ­tico
                elif nome.endswith(".zip"):
                    st.markdown('''<div style="background:#78350f;color:#fff;padding:12px 18px;border-radius:10px;border-left:5px solid #f59e0b;font-weight:600;">Ã¢Å¡Â Ã¯Â¸Â Para Shapefile: pip install geopandas</div>''', unsafe_allow_html=True)

                if df_raw is not None and len(df_raw) > 0:
                    st.session_state.harvest_df = df_raw
                    success_box(f"Ã¢Åâ¦ {arquivo.name} Ã¢â¬â {len(df_raw):,} pontos carregados")
                else:
                    error_box("NÃÂ£o foi possÃÂ­vel ler. Verifique o formato.")
            except Exception as e:
                error_box(f"Erro: {e}")

    # Ã¢â¢ÂÃ¢â¢Â CONFIGURAR E ANALISAR Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    if st.session_state.harvest_df is not None:
        df = st.session_state.harvest_df.copy()
        st.divider()
        st.subheader("Ã¢Å¡â¢Ã¯Â¸Â Configurar AnÃÂ¡lise")

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
            st.checkbox("Remover outliers automÃÂ¡tico (ÃÂ±3ÃÆ)", value=True, key="filtro_out")

        df[col_prod] = pd.to_numeric(df[col_prod], errors="coerce")
        df = df.dropna(subset=[col_prod])
        df = df[df[col_prod] > 0]
        if NUMPY_OK and st.session_state.get("filtro_out", True):
            import numpy as np
            mu, sigma = df[col_prod].mean(), df[col_prod].std()
            df = df[abs(df[col_prod] - mu) <= 3 * sigma]

        st.markdown(f'<div style="background:#0f3460;color:#93c5fd;padding:8px 14px;border-radius:8px;font-size:12px;font-weight:700;">'
                    f'Ã°Å¸âÅ  {len(df):,} pontos vÃÂ¡lidos apÃÂ³s filtro | Faixa: {df[col_prod].min():.1f} Ã¢â¬â {df[col_prod].max():.1f} | MÃÂ©dia prÃÂ©via: {df[col_prod].mean():.1f}</div>',
                    unsafe_allow_html=True)

        if st.button("Ã°Å¸Å¡â¬ Analisar Mapa com IA", use_container_width=True, key="btn_analisar"):
            with st.spinner("Ã°Å¸Â¤â Processando... gerando zonas, grÃÂ¡ficos e laudo IA..."):
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
            success_box("Ã¢Åâ¦ AnÃÂ¡lise concluÃÂ­da!")
            st.rerun()

    # Ã¢â¢ÂÃ¢â¢Â RESULTADOS Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    if st.session_state.harvest_analise:
        an       = st.session_state.harvest_analise
        df_z     = an["df"]
        stats    = an["stats"]
        recs     = an["recs"]
        col_prod = an["col_prod"]
        unid     = an["unidade"].split()[0]

        st.divider()
        st.subheader(f"Ã°Å¸âÅ  {an['arquivo']} | {an['cultura']} | {an['area_ha']} ha | {an['data']}")

        # MÃÂ©tricas rÃÂ¡pidas
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        c1.metric("Ã°Å¸ÅÂ¾ MÃÂ©dia",      f"{stats['media']:.1f}",     unid)
        c2.metric("Ã°Å¸âÅ  CV",         f"{stats['cv']:.1f}%",       "variabilidade")
        c3.metric("Ã¢Â¬â¡Ã¯Â¸Â MÃÂ­nimo",    f"{stats['minimo']:.1f}",     unid)
        c4.metric("Ã¢Â¬â Ã¯Â¸Â MÃÂ¡ximo",    f"{stats['maximo']:.1f}",     unid)
        c5.metric("Ã°Å¸âÂ´ Zona Baixa", f"{stats.get('pct_Ã°Å¸âÂ´ Baixa',0):.0f}%", "da ÃÂ¡rea")
        c6.metric("Ã°Å¸Å¸Â¢ Zona Alta",  f"{stats.get('pct_Ã°Å¸Å¸Â¢ Alta',0):.0f}%",  "da ÃÂ¡rea")

        # Ã¢ââ¬Ã¢ââ¬ TABS Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        tab_mapa, tab_graf, tab_tab, tab_ia, tab_rec = st.tabs([
            "Ã°Å¸âÂºÃ¯Â¸Â Mapa Interativo","Ã°Å¸âË GrÃÂ¡ficos","Ã°Å¸ââ¹ Dados","Ã°Å¸Â¤â Laudo IA","Ã°Å¸âÅ RecomendaÃÂ§ÃÂµes"
        ])

        with tab_mapa:
            if an["has_geo"] and PLOTLY_OK:
                import plotly.express as px
                df_plot = df_z.sample(min(5000,len(df_z)), random_state=42) if len(df_z)>5000 else df_z
                fig_map = px.scatter_mapbox(
                    df_plot, lat=an["col_lat"], lon=an["col_lon"], color=col_prod,
                    color_continuous_scale=[[0,"#dc2626"],[0.4,"#f59e0b"],[0.7,"#16a34a"],[1,"#065f46"]],
                    size_max=8, zoom=13, mapbox_style="open-street-map",
                    title=f"Mapa de Produtividade Ã¢â¬â {an['cultura']}",
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
                Ã°Å¸âÂ´ Baixa: &lt; {an["p33"]:.1f} {unid} &nbsp;|&nbsp;
                Ã°Å¸Å¸Â¡ MÃÂ©dia: {an["p33"]:.1f} Ã¢â¬â {an["p66"]:.1f} &nbsp;|&nbsp;
                Ã°Å¸Å¸Â¢ Alta: &gt; {an["p66"]:.1f} {unid}
                </div>''', unsafe_allow_html=True)

            elif an["has_geo"]:
                lat_c = df_z[an["col_lat"]].mean()
                lon_c = df_z[an["col_lon"]].mean()
                mf = folium.Map(location=[lat_c, lon_c], zoom_start=13)
                cores_z = {"Ã°Å¸âÂ´ Baixa":"red","Ã°Å¸Å¸Â¡ MÃÂ©dia":"orange","Ã°Å¸Å¸Â¢ Alta":"green"}
                for _, row in df_z.sample(min(2000,len(df_z)), random_state=42).iterrows():
                    try:
                        folium.CircleMarker([row[an["col_lat"]], row[an["col_lon"]]],
                            radius=4, color=cores_z.get(row.get("Zona",""),"gray"),
                            fill=True, fill_opacity=0.7,
                            popup=f"{col_prod}: {row[col_prod]:.1f}").add_to(mf)
                    except Exception: pass  # erro silenciado Ã¢â¬â nÃÂ£o crÃÂ­tico
                st_folium(mf, width=700, height=500)
            else:
                info_box("Arquivo sem coordenadas geogrÃÂ¡ficas Ã¢â¬â mapa indisponÃÂ­vel. Veja os grÃÂ¡ficos e laudo nas outras abas.")

        with tab_graf:
            if PLOTLY_OK:
                import plotly.express as px
                import plotly.graph_objects as go
                g1, g2 = st.columns(2)
                with g1:
                    fig_h = px.histogram(df_z, x=col_prod, nbins=40, color="Zona",
                        color_discrete_map={"Ã°Å¸âÂ´ Baixa":"#dc2626","Ã°Å¸Å¸Â¡ MÃÂ©dia":"#f59e0b","Ã°Å¸Å¸Â¢ Alta":"#16a34a"},
                        title="DistribuiÃÂ§ÃÂ£o por Zona", labels={col_prod:unid}, height=360)
                    fig_h.update_layout(paper_bgcolor="#0f3460",plot_bgcolor="#0f3460",font_color="#f1f5f9")
                    st.plotly_chart(fig_h, use_container_width=True)
                with g2:
                    zc = df_z["Zona"].value_counts().reset_index()
                    zc.columns = ["Zona","Pontos"]
                    fig_p = px.pie(zc, names="Zona", values="Pontos",
                        color="Zona",
                        color_discrete_map={"Ã°Å¸âÂ´ Baixa":"#dc2626","Ã°Å¸Å¸Â¡ MÃÂ©dia":"#f59e0b","Ã°Å¸Å¸Â¢ Alta":"#16a34a"},
                        title="% da ÃÂrea por Zona", height=360)
                    fig_p.update_layout(paper_bgcolor="#0f3460",font_color="#f1f5f9")
                    st.plotly_chart(fig_p, use_container_width=True)
                fig_b = px.box(df_z, x="Zona", y=col_prod, color="Zona",
                    color_discrete_map={"Ã°Å¸âÂ´ Baixa":"#dc2626","Ã°Å¸Å¸Â¡ MÃÂ©dia":"#f59e0b","Ã°Å¸Å¸Â¢ Alta":"#16a34a"},
                    title="Box Plot por Zona de Manejo", labels={col_prod:unid}, height=380)
                fig_b.update_layout(paper_bgcolor="#0f3460",plot_bgcolor="#0d2137",
                                    font_color="#f1f5f9",showlegend=False,
                                    yaxis=dict(gridcolor="#1e3a5f"))
                st.plotly_chart(fig_b, use_container_width=True)
            else:
                st.bar_chart(df_z[col_prod].value_counts().sort_index())

            # Tabela por zona
            st.subheader("Ã°Å¸âÅ  EstatÃÂ­sticas por Zona")
            zonas_tab = []
            for z in ["Ã°Å¸âÂ´ Baixa","Ã°Å¸Å¸Â¡ MÃÂ©dia","Ã°Å¸Å¸Â¢ Alta"]:
                sub = df_z[df_z["Zona"]==z]
                if len(sub) > 0:
                    zonas_tab.append({"Zona":z,"Pontos":len(sub),
                        "% ÃÂrea":f"{len(sub)/len(df_z)*100:.1f}%",
                        f"MÃÂ©dia {unid}":f"{sub[col_prod].mean():.1f}",
                        "MÃÂ­n":f"{sub[col_prod].min():.1f}","MÃÂ¡x":f"{sub[col_prod].max():.1f}",
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
            st.caption(f"Exibindo atÃÂ© 5.000 de {len(df_z):,} pontos")
            st.download_button("Ã°Å¸âÂ¥ Baixar CSV com zonas",
                data=df_z.to_csv(index=False).encode("utf-8"),
                file_name=f"colheita_zonas_{date.today()}.csv",
                mime="text/csv", use_container_width=True)

        with tab_ia:
            st.subheader("Ã°Å¸Â¤â Laudo AgronÃÂ´mico Ã¢â¬â InteligÃÂªncia Artificial")
            if an.get("laudo_ia"):
                st.markdown(f'''<div style="background:#0f3460;color:#f1f5f9;padding:22px 26px;
                border-radius:14px;border-left:5px solid #6ee7b7;
                font-size:14px;line-height:2;white-space:pre-wrap;font-weight:500;">
{an["laudo_ia"]}
                </div>''', unsafe_allow_html=True)
                st.divider()
                if st.button("Ã°Å¸âÂ¨Ã¯Â¸Â Gerar PDF do Laudo", key="btn_pdf_col", use_container_width=True):
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
                        el.append(Paragraph("<b>LAUDO DE MAPA DE COLHEITA Ã¢â¬â IAAgro IA</b>", sty["Title"]))
                        el.append(Paragraph(f"Arquivo: {an['arquivo']} | Cultura: {an['cultura']} | ÃÂrea: {an['area_ha']} ha | Data: {an['data']}", sty["Normal"]))
                        el.append(Spacer(1,12))
                        tab_data = [["MÃÂ©trica","Valor"],
                            ["MÃÂ©dia", f"{stats['media']:.1f} {unid}"],
                            ["MÃÂ­nimo/MÃÂ¡ximo", f"{stats['minimo']:.1f} / {stats['maximo']:.1f}"],
                            ["Desvio PadrÃÂ£o", f"{stats['desvio']:.1f}"],
                            ["Coef. VariaÃÂ§ÃÂ£o", f"{stats['cv']:.1f}%"],
                            ["Pontos", f"{stats['total_pts']:,}"],
                            ["Zona Baixa", f"{stats.get('pct_Ã°Å¸âÂ´ Baixa',0):.0f}% Ã¢â¬â {stats.get('med_Ã°Å¸âÂ´ Baixa',0):.1f} {unid}"],
                            ["Zona MÃÂ©dia",  f"{stats.get('pct_Ã°Å¸Å¸Â¡ MÃÂ©dia',0):.0f}% Ã¢â¬â {stats.get('med_Ã°Å¸Å¸Â¡ MÃÂ©dia',0):.1f} {unid}"],
                            ["Zona Alta",   f"{stats.get('pct_Ã°Å¸Å¸Â¢ Alta',0):.0f}% Ã¢â¬â {stats.get('med_Ã°Å¸Å¸Â¢ Alta',0):.1f} {unid}"],
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
                        el.append(Paragraph("<b>LAUDO AGRONÃâMICO IA</b>", sty["Heading2"]))
                        el.append(Spacer(1,6))
                        for linha in an["laudo_ia"].split("\n"):
                            if linha.strip():
                                el.append(Paragraph(linha, sty["BodyText"]))
                                el.append(Spacer(1,3))
                        el.append(Spacer(1,12))
                        el.append(Paragraph("<b>RECOMENDAÃâ¡Ãâ¢ES DE MANEJO</b>", sty["Heading2"]))
                        el.append(Spacer(1,6))
                        for r in recs:
                            el.append(Paragraph(f"<b>{r['tipo']} Ã¢â¬â {r['zona']}</b>", sty["Heading3"]))
                            el.append(Paragraph(r["texto"], sty["BodyText"]))
                            el.append(Spacer(1,8))
                        doc_p.build(el)
                        pdf_b = buf_pdf.getvalue()
                        buf_pdf.close()
                        st.download_button("Ã°Å¸âÂ¥ Baixar Laudo PDF", data=pdf_b,
                            file_name=f"laudo_colheita_{date.today()}.pdf",
                            mime="application/pdf", use_container_width=True)
                    except Exception as e:
                        error_box(f"Erro ao gerar PDF: {e}")
            else:
                warning_box("Laudo IA indisponÃÂ­vel. Verifique a conexÃÂ£o com a internet. As recomendaÃÂ§ÃÂµes automÃÂ¡ticas estÃÂ£o na aba RecomendaÃÂ§ÃÂµes.")

        with tab_rec:
            st.subheader("Ã°Å¸âÅ RecomendaÃÂ§ÃÂµes de Manejo por Zona")
            for r in recs:
                st.markdown(f'''<div style="background:{r["cor"]};color:#fff;padding:14px 18px;
                border-radius:12px;border-left:6px solid {r["borda"]};
                font-size:14px;line-height:1.9;margin:8px 0;">
                <b>{r["tipo"]}</b> &nbsp;|&nbsp; Zona: {r["zona"]}<br>{r["texto"]}
                </div>''', unsafe_allow_html=True)

            st.divider()
            st.subheader("Ã°Å¸ââÃ¯Â¸Â Plano de AÃÂ§ÃÂ£o Ã¢â¬â PrÃÂ³xima Safra")
            acoes = [
                ("PrÃÂ©-plantio","Ã°Å¸âÂ¬","Coletar amostras de solo por zona (mÃÂ­n. 1/zona)"),
                ("PrÃÂ©-plantio","Ã°Å¸âÂ","Delimitar zonas de manejo no GPS do trator"),
                ("Plantio","Ã°Å¸ÅÂ±","Aplicar taxa variÃÂ¡vel de P e K por zona"),
                ("V3Ã¢â¬âV4","Ã°Å¸âÅ ","Monitorar desenvolvimento por zona com fotos georeferenciadas"),
                ("FloraÃÂ§ÃÂ£o","Ã°Å¸Å¡Â","NDVI por drone ou satÃÂ©lite para correlacionar com mapa"),
                ("Colheita","Ã°Å¸âÂ¡","Ativar monitor de produtividade para novo mapa"),
                ("PÃÂ³s-colheita","Ã°Å¸âÅ ","Comparar este mapa com o anterior no IAAgro"),
            ]
            st.dataframe(pd.DataFrame(acoes, columns=["Momento","","AÃÂ§ÃÂ£o"]),
                         use_container_width=True, hide_index=True)

    # Ã¢â¢ÂÃ¢â¢Â HISTÃâRICO DE MAPAS Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    if st.session_state.harvest_historico:
        st.divider()
        st.subheader("Ã°Å¸âÂ HistÃÂ³rico de Mapas Analisados")
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
                title="EvoluÃÂ§ÃÂ£o da Produtividade MÃÂ©dia entre Safras",
                paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",
                font_color="#f1f5f9", xaxis_title="Mapa/Safra",
                yaxis_title="MÃÂ©dia sc/ha", height=300
            )
            st.plotly_chart(fig_ev, use_container_width=True)

# Ã¢ââ¬Ã¢ââ¬ Assistente IA (tab 4) Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸ÅÂ InteligÃÂªncia":
  with _sub_int[4]:
    st.header("Ã°Å¸Â¤â Assistente IA AgrÃÂ­cola")
    st.markdown("""
    <div style='background:#0f3460;border-radius:10px;padding:12px 16px;
    border:1px solid #22c55e;margin-bottom:12px;'>
    <b style='color:#22c55e;'>Ã°Å¸ÅÂ¾ Pergunte sobre sua lavoura</b><br>
    <span style='color:#f1f5f9;font-size:13px;'>
    Tire dÃÂºvidas sobre manejo, pragas, doenÃÂ§as, adubaÃÂ§ÃÂ£o, mercado e muito mais.
    </span>
    </div>
    """, unsafe_allow_html=True)

    # Contexto da ÃÂ¡rea ativa
    _ctx_area = ""
    if st.session_state.get("dados"):
        d = st.session_state.dados
        _ctx_area = (
            f"Cultura: {d.get('cultura','Soja')}, "
            f"ÃÂrea: {d.get('area',0)} ha, "
            f"pH: {d.get('ph',0)}, "
            f"RegiÃÂ£o: {d.get('cidade','Sul do Brasil')}, "
            f"Produtividade esperada: {d.get('produtividade',0)} sc/ha"
        )

    # HistÃÂ³rico do chat
    if "assistente_hist" not in st.session_state:
        st.session_state.assistente_hist = []

    # Exibe mensagens anteriores
    for msg in st.session_state.assistente_hist:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    _prompt = st.chat_input("Digite sua pergunta agrÃÂ­cola...")
    if _prompt:
        st.session_state.assistente_hist.append({"role": "user", "content": _prompt})
        with st.chat_message("user"):
            st.markdown(_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consultando..."):
                try:
                    import anthropic as _anth
                    _client = _anth.Anthropic(api_key=st.secrets.get("ANTHROPIC_API_KEY",""))
                    _sys = (
                        "VocÃÂª ÃÂ© um assistente agrÃÂ­cola especialista brasileiro. "
                        "Responda em portuguÃÂªs, de forma prÃÂ¡tica e objetiva para produtores rurais. "
                        "Baseie suas respostas em EMBRAPA, CQFS RS/SC 2016 e boas prÃÂ¡ticas agrÃÂ­colas. "
                        f"Contexto da propriedade: {_ctx_area if _ctx_area else 'nÃÂ£o informado'}."
                    )
                    _msgs = [{"role": m["role"], "content": m["content"]}
                             for m in st.session_state.assistente_hist]
                    _resp = _client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=800,
                        system=_sys,
                        messages=_msgs
                    )
                    _answer = _resp.content[0].text
                    st.markdown(_answer)
                    st.session_state.assistente_hist.append({"role": "assistant", "content": _answer})
                except Exception as e:
                    _answer = f"Erro ao consultar IA: {e}"
                    st.error(_answer)

    # BotÃÂ£o limpar histÃÂ³rico
    if st.session_state.assistente_hist:
        if st.button("Ã°Å¸ââÃ¯Â¸Â Limpar conversa", key="btn_limpar_assistente"):
            st.session_state.assistente_hist = []
            st.rerun()

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
# MENU: SEGUNDA SAFRA / SAFRINHA
# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
elif menu == "Ã°Å¸ÅÂ± Safrinha":
    st.header("Ã°Å¸ÅÂ± Safrinha")

    st.markdown("""
    <div style='background:#0f3460;border-radius:12px;padding:14px 18px;
    border-left:5px solid #22c55e;margin-bottom:16px;'>
    <b style='color:#22c55e;font-size:15px;'>Ã°Å¸ÅÂ± Planejamento de Safrinha</b><br>
    <span style='color:#f1f5f9;font-size:13px;'>
    Planeje a safrinha apÃÂ³s a colheita da safra principal. Escolha a ÃÂ¡rea cadastrada,
    defina a cultura, custos e acompanhe a rentabilidade do ciclo.
    </span>
    </div>
    """, unsafe_allow_html=True)

    # Inicializa session_state
    if "safrinha_registros" not in st.session_state:
        st.session_state.safrinha_registros = []

    tab_s1, tab_s2, tab_s3 = st.tabs([
        "Ã¢Å¾â¢ Planejar Safrinha",
        "Ã°Å¸ââ¹ Registros",
        "Ã°Å¸âÅ  AnÃÂ¡lise de Rentabilidade"
    ])

    # Ã¢ââ¬Ã¢ââ¬ CombinaÃÂ§ÃÂµes tÃÂ­picas da regiÃÂ£o Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
    ROTACOES_TIPICAS = {
        "Milho Ã¢â â FeijÃÂ£o":   {"1a":"Milho", "2a":"FeijÃÂ£o", "janela":"SetÃ¢â¬âJan / FevÃ¢â¬âMai"},
        "Milho Ã¢â â Soja":     {"1a":"Milho", "2a":"Soja",   "janela":"SetÃ¢â¬âJan / OutÃ¢â¬âMar"},
        "Soja Ã¢â â FeijÃÂ£o":    {"1a":"Soja",  "2a":"FeijÃÂ£o", "janela":"OutÃ¢â¬âJan / FevÃ¢â¬âMai"},
        "FeijÃÂ£o Ã¢â â Soja":    {"1a":"FeijÃÂ£o","2a":"Soja",   "janela":"JanÃ¢â¬âAbr / OutÃ¢â¬âMar"},
        "FeijÃÂ£o Ã¢â â Milho":   {"1a":"FeijÃÂ£o","2a":"Milho",  "janela":"JanÃ¢â¬âAbr / AbrÃ¢â¬âAgo"},
        "Soja Ã¢â â Milho":     {"1a":"Soja",  "2a":"Milho",  "janela":"OutÃ¢â¬âJan / FevÃ¢â¬âJun"},
    }

    CULTURAS_SAFRINHA = ["Milho","Soja","FeijÃÂ£o"]

    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    # TAB 1 Ã¢â¬â PLANEJAR ROTAÃâ¡ÃÆO
    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    with tab_s1:
        st.subheader("Ã¢Å¾â¢ Novo Planejamento de Safrinha")

        # Ã¢ââ¬Ã¢ââ¬ SeleÃÂ§ÃÂ£o de ÃÂ¡rea cadastrada Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        areas_cadastradas = st.session_state.get("areas", [])
        area_selecionada_sf = None
        if areas_cadastradas:
            opcoes_areas = ["Ã¢â¬â Selecione uma ÃÂ¡rea cadastrada Ã¢â¬â"] + [
                f"{a.get('Fazenda','?')} Ã¢â¬â {a.get('TalhÃÂ£o','?')} ({a.get('Hectares',0):.1f} ha | {a.get('Cultura','?')})"
                for a in areas_cadastradas
            ]
            area_choice = st.selectbox("Ã°Å¸ÅÂ¾ ÃÂrea cadastrada", opcoes_areas, key="sf_area_choice")
            if area_choice != "Ã¢â¬â Selecione uma ÃÂ¡rea cadastrada Ã¢â¬â":
                idx_area = opcoes_areas.index(area_choice) - 1
                area_selecionada_sf = areas_cadastradas[idx_area]
                st.success(f"Ã¢Åâ¦ ÃÂrea carregada: **{area_selecionada_sf.get('Fazenda','')} Ã¢â¬â {area_selecionada_sf.get('TalhÃÂ£o','')}**")
        else:
            st.info("Nenhuma ÃÂ¡rea cadastrada. VÃÂ¡ em **Cadastro da ÃÂrea** para adicionar.")

        # Preenche defaults da ÃÂ¡rea selecionada
        _area_ha   = float(area_selecionada_sf.get("Hectares", 10.0))    if area_selecionada_sf else 10.0
        _cultura   = area_selecionada_sf.get("Cultura", "Soja")           if area_selecionada_sf else "Soja"
        _prod      = float(area_selecionada_sf.get("Meta Produtividade", 60.0)) if area_selecionada_sf else 60.0
        _talhao    = f"{area_selecionada_sf.get('Fazenda','')} Ã¢â¬â {area_selecionada_sf.get('TalhÃÂ£o','')}" if area_selecionada_sf else ""
        _cidade    = area_selecionada_sf.get("Cidade", "")                if area_selecionada_sf else ""

        st.divider()

        # SeleÃÂ§ÃÂ£o rÃÂ¡pida de rotaÃÂ§ÃÂ£o tÃÂ­pica
        rotacao_sel = st.selectbox(
            "Ã°Å¸ââ RotaÃÂ§ÃÂ£o tÃÂ­pica da regiÃÂ£o",
            list(ROTACOES_TIPICAS.keys()),
            key="safrinha_rotacao_sel"
        )
        rot_info = ROTACOES_TIPICAS[rotacao_sel]
        if rot_info["janela"]:
            st.caption(f"Ã°Å¸ââ¦ Janela de plantio: {rot_info['janela']}")

        # Ã¢ââ¬Ã¢ââ¬ Dados da Safrinha Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        st.markdown("#### Ã°Å¸ÅÂ± Dados da Safrinha")
        culturas_1a = CULTURAS_SAFRINHA
        cultura_1a  = _cultura  # cultura da ÃÂ¡rea selecionada (safra principal)
        area_1a     = _area_ha
        prod_1a     = _prod
        preco_1a    = 115.0
        custo_1a    = 3200.0
        plantio_1a  = ""
        colheita_1a = ""
        luc_1a      = 0.0
        rec_1a      = 0.0

        col_sf1, col_sf2 = st.columns(2)
        with col_sf1:
            idx_2a = culturas_1a.index(rot_info["2a"]) if rot_info["2a"] in culturas_1a else 0
            cultura_2a = st.selectbox("Ã°Å¸ÅÂ± Cultura da safrinha", culturas_1a, index=idx_2a, key="sf_cult2")
            area_2a    = st.number_input("ÃÂrea (ha)", min_value=0.0, value=_area_ha, key="sf_area2")
            prod_2a    = st.number_input("Produtividade esperada (sc/ha)", min_value=0.0, value=45.0, key="sf_prod2")
        with col_sf2:
            preco_2a   = st.number_input("PreÃÂ§o da saca R$", min_value=0.0, value=58.0, key="sf_preco2")
            custo_2a   = st.number_input("Custo total R$/ha", min_value=0.0, value=2200.0, key="sf_custo2")
            plantio_2a = st.text_input("Data de plantio", placeholder="Ex: 25/02/2026", key="sf_plant2")
            colheita_2a = st.text_input("PrevisÃÂ£o de colheita", placeholder="Ex: 30/05/2026", key="sf_colh2")

        st.divider()
        col_obs1, col_obs2 = st.columns(2)
        with col_obs1:
            talhao_sf  = st.text_input("TalhÃÂ£o / ÃÂrea", value=_talhao, placeholder="Ex: TalhÃÂ£o A", key="sf_talhao")
            safra_sf   = st.text_input("Safra", placeholder="Ex: 2025/2026", key="sf_safra")
        with col_obs2:
            obs_sf     = st.text_area("ObservaÃÂ§ÃÂµes", placeholder="Ex: Solo compactado, uso de cobertura...", key="sf_obs", height=80)

        # Preview da rentabilidade antes de salvar
        rec_1a  = prod_1a * preco_1a * area_1a
        cus_1a  = custo_1a * area_1a
        luc_1a  = rec_1a - cus_1a
        rec_2a  = prod_2a * preco_2a * area_2a
        cus_2a  = custo_2a * area_2a
        luc_2a  = rec_2a - cus_2a
        luc_tot = luc_1a + luc_2a

        st.markdown("#### Ã°Å¸âÂ° Preview de Rentabilidade")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(f"Receita {cultura_1a}", f"R$ {rec_1a:,.0f}")
        c2.metric(f"Receita {cultura_2a}", f"R$ {rec_2a:,.0f}")
        c3.metric("Lucro Total", f"R$ {luc_tot:,.0f}",
                  delta="Ã¢Åâ¦ Positivo" if luc_tot > 0 else "Ã¢ÂÅ Negativo")
        c4.metric("Lucro/ha mÃÂ©dio", f"R$ {luc_tot/max(area_1a,1):,.0f}")

        if st.button("Ã°Å¸âÂ¾ Salvar Planejamento", use_container_width=True, key="btn_salvar_safrinha"):
            if not talhao_sf.strip():
                st.error("Informe o talhÃÂ£o.")
            else:
                registro = {
                    "id":          len(st.session_state.safrinha_registros) + 1,
                    "safra":       safra_sf,
                    "talhao":      talhao_sf,
                    "rotacao":     f"{cultura_1a} Ã¢â â {cultura_2a}",
                    "cultura_1a":  cultura_1a,
                    "area_1a":     area_1a,
                    "prod_1a":     prod_1a,
                    "preco_1a":    preco_1a,
                    "custo_1a":    custo_1a,
                    "plantio_1a":  plantio_1a,
                    "colheita_1a": colheita_1a,
                    "receita_1a":  round(rec_1a, 2),
                    "lucro_1a":    round(luc_1a, 2),
                    "cultura_2a":  cultura_2a,
                    "area_2a":     area_2a,
                    "prod_2a":     prod_2a,
                    "preco_2a":    preco_2a,
                    "custo_2a":    custo_2a,
                    "plantio_2a":  plantio_2a,
                    "colheita_2a": colheita_2a,
                    "receita_2a":  round(rec_2a, 2),
                    "lucro_2a":    round(luc_2a, 2),
                    "lucro_total": round(luc_tot, 2),
                    "obs":         obs_sf,
                    "data_registro": datetime.now().strftime("%d/%m/%Y %H:%M"),
                }
                st.session_state.safrinha_registros.append(registro)
                salvar_dados_iaagro()
                st.success(f"Ã¢Åâ¦ RotaÃÂ§ÃÂ£o **{cultura_1a} Ã¢â â {cultura_2a}** salva para o talhÃÂ£o **{talhao_sf}**!")
                st.balloons()
                st.rerun()

    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    # TAB 2 Ã¢â¬â REGISTROS
    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    with tab_s2:
        st.subheader("Ã°Å¸ââ¹ Registros de Safrinha")
        if not st.session_state.safrinha_registros:
            st.info("Nenhum planejamento salvo ainda. Use a aba Ã¢Å¾â¢ Planejar RotaÃÂ§ÃÂ£o.")
        else:
            for i, reg in enumerate(st.session_state.safrinha_registros):
                cor = "#14532d" if reg["lucro_total"] > 0 else "#7f1d1d"
                borda = "#22c55e" if reg["lucro_total"] > 0 else "#ef4444"
                st.markdown(f"""
                <div style='background:{cor};border-radius:12px;padding:14px 18px;
                border-left:5px solid {borda};margin-bottom:10px;'>
                <b style='color:#f1f5f9;font-size:15px;'>Ã°Å¸ââ {reg['rotacao']} Ã¢â¬â {reg['talhao']} ({reg.get('safra','')})</b><br>
                <span style='color:#d1fae5;font-size:13px;'>
                Ã°Å¸ââ¦ {reg['cultura_1a']}: plantio {reg.get('plantio_1a','Ã¢â¬â')} Ã¢â â colheita {reg.get('colheita_1a','Ã¢â¬â')} &nbsp;|&nbsp;
                {reg['cultura_2a']}: plantio {reg.get('plantio_2a','Ã¢â¬â')} Ã¢â â colheita {reg.get('colheita_2a','Ã¢â¬â')}
                </span><br>
                <span style='color:#86efac;font-size:13px;'>
                Ã°Å¸âÂ° Lucro total: <b>R$ {reg['lucro_total']:,.2f}</b> &nbsp;|&nbsp;
                1ÃÂª safra: R$ {reg['lucro_1a']:,.2f} &nbsp;|&nbsp;
                2ÃÂª safra: R$ {reg['lucro_2a']:,.2f}
                </span>
                </div>
                """, unsafe_allow_html=True)

                col_ed, col_del = st.columns([5,1])
                with col_del:
                    if st.button("Ã°Å¸ââÃ¯Â¸Â", key=f"del_safrinha_{i}", help="Excluir registro"):
                        st.session_state.safrinha_registros.pop(i)
                        salvar_dados_iaagro()
                        st.rerun()

            # Tabela resumo
            st.divider()
            st.subheader("Ã°Å¸âÅ  Tabela Resumo")
            df_sf = pd.DataFrame([{
                "TalhÃÂ£o":      r["talhao"],
                "Safra":       r.get("safra",""),
                "RotaÃÂ§ÃÂ£o":     r["rotacao"],
                "ÃÂrea 1ÃÂª ha":  r["area_1a"],
                "Prod 1ÃÂª sc/ha": r["prod_1a"],
                "ÃÂrea 2ÃÂª ha":  r["area_2a"],
                "Prod 2ÃÂª sc/ha": r["prod_2a"],
                "Receita Total R$": r["receita_1a"] + r["receita_2a"],
                "Lucro Total R$":   r["lucro_total"],
            } for r in st.session_state.safrinha_registros])
            st.dataframe(df_sf, use_container_width=True)

    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    # TAB 3 Ã¢â¬â ANÃÂLISE DE RENTABILIDADE
    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    with tab_s3:
        st.subheader("Ã°Å¸âÅ  AnÃÂ¡lise de Rentabilidade por RotaÃÂ§ÃÂ£o")
        if not st.session_state.safrinha_registros:
            st.info("Salve ao menos um planejamento para ver a anÃÂ¡lise.")
        else:
            import plotly.express as px

            df_an = pd.DataFrame([{
                "RotaÃÂ§ÃÂ£o":        r["rotacao"],
                "TalhÃÂ£o":         r["talhao"],
                "Lucro Total R$": r["lucro_total"],
                "Receita 1ÃÂª R$":  r["receita_1a"],
                "Receita 2ÃÂª R$":  r["receita_2a"],
                "Lucro 1ÃÂª R$":    r["lucro_1a"],
                "Lucro 2ÃÂª R$":    r["lucro_2a"],
            } for r in st.session_state.safrinha_registros])

            # GrÃÂ¡fico comparativo
            fig_rot = px.bar(
                df_an, x="TalhÃÂ£o", y=["Lucro 1ÃÂª R$","Lucro 2ÃÂª R$"],
                barmode="group", title="Ã°Å¸âÂ° Lucro por Safra e TalhÃÂ£o",
                color_discrete_sequence=["#22c55e","#3b82f6"],
                template="plotly_dark"
            )
            fig_rot.update_layout(
                paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",
                font_color="#f1f5f9", height=350
            )
            st.plotly_chart(fig_rot, use_container_width=True)

            # Melhor rotaÃÂ§ÃÂ£o
            melhor = df_an.loc[df_an["Lucro Total R$"].idxmax()]
            st.markdown(f"""
            <div style='background:#14532d;border-radius:12px;padding:14px 18px;
            border-left:5px solid #22c55e;margin-top:8px;'>
            <b style='color:#22c55e;'>Ã°Å¸Ââ  RotaÃÂ§ÃÂ£o mais rentÃÂ¡vel:</b>
            <span style='color:#f1f5f9;font-size:14px;'>
            &nbsp;<b>{melhor['RotaÃÂ§ÃÂ£o']}</b> Ã¢â¬â TalhÃÂ£o {melhor['TalhÃÂ£o']} Ã¢â¬â 
            Lucro total: <b>R$ {melhor['Lucro Total R$']:,.2f}</b>
            </span>
            </div>
            """, unsafe_allow_html=True)

            # MÃÂ©tricas gerais
            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("Ã°Å¸âÂ° Lucro total acumulado", f"R$ {df_an['Lucro Total R$'].sum():,.2f}")
            c2.metric("Ã°Å¸âË MÃÂ©dia por rotaÃÂ§ÃÂ£o",     f"R$ {df_an['Lucro Total R$'].mean():,.2f}")
            c3.metric("Ã°Å¸ââ RotaÃÂ§ÃÂµes planejadas",   len(df_an))

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
if menu == "Ã°Å¸âÂ° Financeiro":
  with _sub_fin[3]:
    st.header("Ã°Å¸âÂµ Fluxo de Caixa")
    if not st.session_state.areas:
        st.info("Cadastre uma ÃÂ¡rea para visualizar o fluxo de caixa.")
    else:
        _areas_fc = [f"{a['ID']} - {a['TalhÃÂ£o']}" for a in st.session_state.areas]
        _area_fc  = st.selectbox("ÃÂrea", _areas_fc, key="sel_area_fluxo_caixa")
        _id_fc    = _area_fc.split(" - ")[0]

        st.subheader("Ã¢Å¾â¢ LanÃÂ§amentos")
        col_fc1, col_fc2, col_fc3 = st.columns(3)
        with col_fc1:
            _data_fc   = st.date_input("Data", key="date_fc")
            _tipo_fc   = st.selectbox("Tipo", ["Receita","Despesa"], key="sel_tipo_fc")
        with col_fc2:
            _categ_fc  = st.selectbox("Categoria",
                ["Venda de grÃÂ£os","Venda de subproduto","Insumos","MaquinÃÂ¡rio",
                 "MÃÂ£o de obra","Arrendamento","Frete","Seguro","Outros"], key="sel_categ_fc")
            _valor_fc  = st.number_input("Valor R$", min_value=0.0, key="num_valor_fc")
        with col_fc3:
            _desc_fc   = st.text_input("DescriÃÂ§ÃÂ£o", key="txt_desc_fc")
            _pago_fc   = st.checkbox("Pago/Recebido", value=True, key="chk_pago_fc")

        if st.button("Ã°Å¸âÂ¾ LanÃÂ§ar", key="btn_lancar_fc", use_container_width=True):
            if _valor_fc > 0:
                _lancamento = {
                    "area_id":    _id_fc,
                    "data":       str(_data_fc),
                    "tipo":       _tipo_fc,
                    "categoria":  _categ_fc,
                    "valor":      round(_valor_fc, 2),
                    "descricao":  _desc_fc,
                    "pago":       _pago_fc,
                }
                if "fluxo_caixa" not in st.session_state:
                    st.session_state.fluxo_caixa = []
                st.session_state.fluxo_caixa.append(_lancamento)
                salvar_dados_iaagro()
                st.success(f"Ã¢Åâ¦ {'Receita' if _tipo_fc=='Receita' else 'Despesa'} de R$ {_valor_fc:.2f} lanÃÂ§ada!")
            else:
                st.warning("Digite um valor maior que zero.")

        # Exibe saldo e lanÃÂ§amentos
        _lanc = [l for l in st.session_state.get("fluxo_caixa", []) if l.get("area_id") == _id_fc]
        if _lanc:
            import pandas as pd
            df_fc = pd.DataFrame(_lanc)
            df_fc["valor_signed"] = df_fc.apply(lambda r: r["valor"] if r["tipo"]=="Receita" else -r["valor"], axis=1)
            _total_rec  = df_fc[df_fc["tipo"]=="Receita"]["valor"].sum()
            _total_desp = df_fc[df_fc["tipo"]=="Despesa"]["valor"].sum()
            _saldo      = _total_rec - _total_desp

            col_s1, col_s2, col_s3 = st.columns(3)
            col_s1.metric("Ã°Å¸âÅ¡ Receitas", f"R$ {_total_rec:,.2f}")
            col_s2.metric("Ã°Å¸âÂ´ Despesas", f"R$ {_total_desp:,.2f}")
            col_s3.metric("Ã°Å¸âÂ° Saldo", f"R$ {_saldo:,.2f}",
                         delta=f"{'positivo' if _saldo >= 0 else 'negativo'}")

            # GrÃÂ¡fico evoluÃÂ§ÃÂ£o
            df_fc["data_dt"] = pd.to_datetime(df_fc["data"])
            df_fc = df_fc.sort_values("data_dt")
            df_fc["saldo_acum"] = df_fc["valor_signed"].cumsum()
            st.line_chart(df_fc.set_index("data_dt")["saldo_acum"])

            # Tabela
            st.dataframe(
                df_fc[["data","tipo","categoria","descricao","valor","pago"]]
                .rename(columns={"data":"Data","tipo":"Tipo","categoria":"Categoria",
                                  "descricao":"DescriÃÂ§ÃÂ£o","valor":"R$","pago":"Pago"}),
                use_container_width=True
            )

            # Excluir
            with st.expander("Ã°Å¸ââÃ¯Â¸Â Excluir lanÃÂ§amento"):
                _opcoes = [f"{l['data']} Ã¢â¬â {l['tipo']} Ã¢â¬â R${l['valor']:.2f} Ã¢â¬â {l['descricao']}" for l in _lanc]
                _del_fc = st.selectbox("Selecione", _opcoes, key="sel_del_fc")
                if st.button("Ã°Å¸ââÃ¯Â¸Â Excluir", key="btn_del_fc"):
                    _idx_del = _opcoes.index(_del_fc)
                    _all_ids = [i for i, l in enumerate(st.session_state.fluxo_caixa)
                                if l.get("area_id") == _id_fc]
                    st.session_state.fluxo_caixa.pop(_all_ids[_idx_del])
                    salvar_dados_iaagro()
                    st.success("LanÃÂ§amento excluÃÂ­do!")
                    st.rerun()
        else:
            st.info("Ã°Å¸âÂ Nenhum lanÃÂ§amento para esta ÃÂ¡rea ainda.")

  with _sub_fin[4]:
    import io
    st.header("Ã°Å¸Â§Â¾ Imposto de Renda Ã¢â¬â Produtor Rural")

    st.markdown("""
    <div style='background:#0f3460;border-radius:12px;padding:14px 18px;border-left:5px solid #22c55e;margin-bottom:16px;'>
    <b style='color:#22c55e'>Ã°Å¸âÅ Sobre este mÃÂ³dulo</b><br>
    <span style='color:#f1f5f9;font-size:13px;'>
    Calcula o Imposto de Renda da atividade rural conforme a legislaÃÂ§ÃÂ£o brasileira (Lei 8.023/90 e IN RFB 1.700/17).
    Preencha as receitas e despesas para gerar o relatÃÂ³rio completo em PDF pronto para seu contador.
    </span>
    </div>
    """, unsafe_allow_html=True)

    tab_ir1, tab_ir2, tab_ir3 = st.tabs([
        "Ã°Å¸âÂ¥ Receitas & Despesas",
        "Ã°Å¸âÅ  Resultado & CÃÂ¡lculo",
        "Ã°Å¸ââ Gerar RelatÃÂ³rio PDF"
    ])

    # Ã¢ââ¬Ã¢ââ¬ Inicializa session_state IR Ã¢ââ¬Ã¢ââ¬
    if "ir_ano"        not in st.session_state: st.session_state.ir_ano        = 2025
    if "ir_receitas"   not in st.session_state: st.session_state.ir_receitas   = {}
    if "ir_despesas"   not in st.session_state: st.session_state.ir_despesas   = {}
    if "ir_nome"       not in st.session_state: st.session_state.ir_nome       = ""
    if "ir_cpf"        not in st.session_state: st.session_state.ir_cpf        = ""
    if "ir_cidade"     not in st.session_state: st.session_state.ir_cidade     = ""
    if "ir_area_total" not in st.session_state: st.session_state.ir_area_total = 0.0
    if "ir_producao"   not in st.session_state: st.session_state.ir_producao   = {}

    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    # TAB 1 Ã¢â¬â RECEITAS & DESPESAS
    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    with tab_ir1:
        st.subheader("Ã°Å¸âÂ¤ Dados do Produtor")
        col_id1, col_id2, col_id3 = st.columns(3)
        with col_id1:
            st.session_state.ir_nome  = st.text_input("Nome completo", value=st.session_state.ir_nome, key="ir_nome_input")
            st.session_state.ir_cpf   = st.text_input("CPF", value=st.session_state.ir_cpf, key="ir_cpf_input", placeholder="000.000.000-00")
        with col_id2:
            st.session_state.ir_cidade     = st.text_input("Cidade/UF", value=st.session_state.ir_cidade, key="ir_cidade_input")
            st.session_state.ir_area_total = st.number_input("ÃÂrea total (ha)", min_value=0.0, value=st.session_state.ir_area_total, key="ir_area_input")
        with col_id3:
            st.session_state.ir_ano = st.selectbox("Ano-calendÃÂ¡rio", [2025, 2024, 2023, 2022], key="ir_ano_sel")

        st.divider()
        st.subheader("Ã°Å¸âË Receitas da Atividade Rural")
        st.caption("Informe todas as receitas brutas recebidas no ano")

        # Ã¢ââ¬Ã¢ââ¬ ImportaÃÂ§ÃÂ£o automÃÂ¡tica da Safrinha Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
        safrinha_regs = st.session_state.get("safrinha_registros", [])
        if safrinha_regs:
            receita_safrinha = sum(r.get("receita_1a", 0) + r.get("receita_2a", 0) for r in safrinha_regs)
            custo_safrinha   = sum(
                r.get("custo_1a", 0) * r.get("area_1a", 0) +
                r.get("custo_2a", 0) * r.get("area_2a", 0)
                for r in safrinha_regs
            )
            st.markdown(f"""
            <div style='background:#0f3460;border-radius:10px;padding:12px 16px;
            border:1px solid #22c55e;margin-bottom:12px;'>
            <b style='color:#22c55e;'>Ã°Å¸âÂ¥ Dados da Safrinha disponÃÂ­veis para importar</b><br>
            <span style='color:#f1f5f9;font-size:13px;'>
            {len(safrinha_regs)} rotaÃÂ§ÃÂ£o(ÃÂµes) planejada(s) &nbsp;|&nbsp;
            Receita total: <b>R$ {receita_safrinha:,.2f}</b> &nbsp;|&nbsp;
            Custos: <b>R$ {custo_safrinha:,.2f}</b>
            </span>
            </div>
            """, unsafe_allow_html=True)

            col_imp1, col_imp2 = st.columns(2)
            with col_imp1:
                if st.button("Ã°Å¸âÂ¥ Importar receitas da safrinha", key="btn_imp_rec_safrinha", use_container_width=True):
                    atual = float(st.session_state.ir_receitas.get("venda_graos", 0.0))
                    st.session_state.ir_receitas["venda_graos"] = round(atual + receita_safrinha, 2)
                    st.success(f"Ã¢Åâ¦ R$ {receita_safrinha:,.2f} adicionados ÃÂ s receitas de grÃÂ£os!")
                    st.rerun()
            with col_imp2:
                if st.button("Ã°Å¸âÂ¥ Importar custos da safrinha", key="btn_imp_desp_safrinha", use_container_width=True):
                    # Distribui nos campos de despesa correspondentes
                    atual_sem = float(st.session_state.ir_despesas.get("sementes", 0.0))
                    atual_def = float(st.session_state.ir_despesas.get("fertilizantes", 0.0))
                    # 30% sementes, 70% fertilizantes/defensivos como estimativa
                    st.session_state.ir_despesas["sementes"]      = round(atual_sem + custo_safrinha * 0.30, 2)
                    st.session_state.ir_despesas["fertilizantes"] = round(atual_def + custo_safrinha * 0.70, 2)
                    st.success(f"Ã¢Åâ¦ R$ {custo_safrinha:,.2f} distribuÃÂ­dos nas despesas!")
                    st.rerun()

        rec_items = [
            ("venda_graos",      "Ã°Å¸ÅÂ¾ Venda de grÃÂ£os e cereais (R$)"),
            ("venda_animais",    "Ã°Å¸Ââ Venda de animais e produtos pecuÃÂ¡rios (R$)"),
            ("arrendamento",     "Ã°Å¸ÂÂ¡ Arrendamento recebido (R$)"),
            ("subvencoes",       "Ã°Å¸âÂ° SubvenÃÂ§ÃÂµes e incentivos governamentais (R$)"),
            ("indenizacoes",     "Ã°Å¸âºÂ¡Ã¯Â¸Â IndenizaÃÂ§ÃÂµes de seguro agrÃÂ­cola (R$)"),
            ("outras_receitas",  "Ã¢Å¾â¢ Outras receitas rurais (R$)"),
        ]
        col_r1, col_r2 = st.columns(2)
        for i, (key, label) in enumerate(rec_items):
            with (col_r1 if i % 2 == 0 else col_r2):
                st.session_state.ir_receitas[key] = st.number_input(
                    label, min_value=0.0,
                    value=float(st.session_state.ir_receitas.get(key, 0.0)),
                    key=f"ir_rec_{key}", format="%.2f"
                )

        st.divider()
        st.subheader("Ã°Å¸ââ° Despesas da Atividade Rural")
        st.caption("Despesas dedutÃÂ­veis conforme art. 61 do RIR/2018")

        desp_items = [
            ("sementes",         "Ã°Å¸ÅÂ± Sementes e mudas (R$)"),
            ("fertilizantes",    "Ã°Å¸Â§Âª Fertilizantes e defensivos (R$)"),
            ("mao_de_obra",      "Ã°Å¸âÂ· MÃÂ£o de obra (folha + encargos) (R$)"),
            ("combustivel",      "Ã¢âºÂ½ CombustÃÂ­vel e lubrificantes (R$)"),
            ("energia",          "Ã¢Å¡Â¡ Energia elÃÂ©trica rural (R$)"),
            ("arrendamento_pg",  "Ã°Å¸ÂÂ¡ Arrendamento pago (R$)"),
            ("manutencao",       "Ã°Å¸âÂ§ ManutenÃÂ§ÃÂ£o de mÃÂ¡quinas e benfeitorias (R$)"),
            ("depreciacao",      "Ã°Å¸ââ° DepreciaÃÂ§ÃÂ£o de bens (R$)"),
            ("frete",            "Ã°Å¸Å¡âº Fretes e carretos (R$)"),
            ("seguro",           "Ã°Å¸âºÂ¡Ã¯Â¸Â Seguros rurais (R$)"),
            ("assistencia_tec",  "Ã°Å¸âÂ¨Ã¢â¬ÂÃ°Å¸âÂ¬ AssistÃÂªncia tÃÂ©cnica e agronÃÂ´mica (R$)"),
            ("juros",            "Ã°Å¸âÂ³ Juros de financiamentos rurais (R$)"),
            ("outras_despesas",  "Ã¢Å¾â¢ Outras despesas dedutÃÂ­veis (R$)"),
        ]
        col_d1, col_d2 = st.columns(2)
        for i, (key, label) in enumerate(desp_items):
            with (col_d1 if i % 2 == 0 else col_d2):
                st.session_state.ir_despesas[key] = st.number_input(
                    label, min_value=0.0,
                    value=float(st.session_state.ir_despesas.get(key, 0.0)),
                    key=f"ir_desp_{key}", format="%.2f"
                )

        st.divider()
        st.subheader("Ã°Å¸ÅÂ¾ ProduÃÂ§ÃÂ£o por Cultura (opcional)")
        st.caption("Para o memorial descritivo do relatÃÂ³rio")
        culturas_ir = get_culturas() + (["Outro"] if "Outro" not in get_culturas() else [])
        col_p1, col_p2 = st.columns(2)
        for i, cult in enumerate(culturas_ir):
            with (col_p1 if i % 2 == 0 else col_p2):
                st.session_state.ir_producao[cult] = st.number_input(
                    f"{cult} (sacas/kg produzidas)",
                    min_value=0.0,
                    value=float(st.session_state.ir_producao.get(cult, 0.0)),
                    key=f"ir_prod_{cult}", format="%.1f"
                )

    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    # TAB 2 Ã¢â¬â RESULTADO & CÃÂLCULO
    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    with tab_ir2:
        receita_bruta  = sum(st.session_state.ir_receitas.values())
        despesa_total  = sum(st.session_state.ir_despesas.values())
        resultado_liq  = receita_bruta - despesa_total

        # Resumo da safrinha na base do cÃÂ¡lculo
        safrinha_regs2 = st.session_state.get("safrinha_registros", [])
        if safrinha_regs2:
            rec_sf  = sum(r.get("receita_1a",0)+r.get("receita_2a",0) for r in safrinha_regs2)
            luc_sf  = sum(r.get("lucro_total",0) for r in safrinha_regs2)
            cus_sf  = sum(r.get("custo_1a",0)*r.get("area_1a",0)+r.get("custo_2a",0)*r.get("area_2a",0) for r in safrinha_regs2)
            importado = float(st.session_state.ir_receitas.get("venda_graos",0)) >= rec_sf * 0.9
            st.markdown(f"""
            <div style='background:#1e3a5f;border-radius:10px;padding:12px 16px;
            border:1px solid #3b82f6;margin-bottom:12px;'>
            <b style='color:#3b82f6;'>Ã°Å¸âÅ  Safrinha</b>
            {"&nbsp;<span style='color:#22c55e;font-size:12px;'>Ã¢Åâ¦ Dados importados</span>" if importado else "&nbsp;<span style='color:#f59e0b;font-size:12px;'>Ã¢Å¡Â Ã¯Â¸Â Use o botÃÂ£o Importar na aba anterior</span>"}<br>
            <span style='color:#f1f5f9;font-size:13px;'>
            Receita total safras: <b>R$ {rec_sf:,.2f}</b> &nbsp;|&nbsp;
            Custos: <b>R$ {cus_sf:,.2f}</b> &nbsp;|&nbsp;
            Lucro lÃÂ­quido safras: <b>R$ {luc_sf:,.2f}</b>
            </span>
            </div>
            """, unsafe_allow_html=True)

        # Resultado presumido (20% da receita bruta Ã¢â¬â opcional ao resultado real)
        resultado_pres = receita_bruta * 0.20

        # Limite de isenÃÂ§ÃÂ£o: R$ 142.798,50 (2025) Ã¢â¬â resultado lÃÂ­quido
        LIMITE_ISENCAO = 142798.50
        BASE_CALCULO   = max(resultado_liq, 0.0)

        # Tabela progressiva IRPF 2025 (resultado lÃÂ­quido rural entra na base do IRPF)
        tabela_ir = [
            (2259.20  * 12, 0.000, 0.00),
            (2826.65  * 12, 0.075, 169.44 * 12),
            (3751.05  * 12, 0.150, 381.44 * 12),
            (4664.68  * 12, 0.225, 662.77 * 12),
            (float("inf"),  0.275, 896.00 * 12),
        ]
        ir_devido = 0.0
        aliquota_efetiva = 0.0
        if BASE_CALCULO > LIMITE_ISENCAO:
            base_tributavel = BASE_CALCULO
            for limite, aliq, deducao in tabela_ir:
                if base_tributavel <= limite:
                    ir_devido = base_tributavel * aliq - deducao
                    aliquota_efetiva = aliq
                    break

        ir_devido = max(ir_devido, 0.0)

        # Cards de resultado
        st.markdown("### Ã°Å¸âÅ  Demonstrativo de Resultado")
        c1, c2, c3 = st.columns(3)
        c1.metric("Ã°Å¸âÂ° Receita Bruta", f"R$ {receita_bruta:,.2f}")
        c2.metric("Ã°Å¸ââ° Despesas DedutÃÂ­veis", f"R$ {despesa_total:,.2f}")
        cor_res = "normal" if resultado_liq >= 0 else "inverse"
        c3.metric("Ã°Å¸âÅ  Resultado LÃÂ­quido", f"R$ {resultado_liq:,.2f}", delta=f"{'Lucro' if resultado_liq >= 0 else 'PrejuÃÂ­zo'}")

        st.divider()
        st.markdown("### Ã°Å¸Â§Â® CÃÂ¡lculo do Imposto")

        col_calc1, col_calc2 = st.columns(2)
        with col_calc1:
            st.markdown(f"""
            <div style='background:#0f3460;border-radius:12px;padding:16px 20px;border:1px solid #22c55e;'>
            <b style='color:#22c55e;font-size:15px;'>Ã°Å¸ââ¹ Resultado Real</b><br><br>
            <table style='width:100%;color:#f1f5f9;font-size:13px;'>
            <tr><td>Receita Bruta</td><td align='right'><b>R$ {receita_bruta:,.2f}</b></td></tr>
            <tr><td>(-) Despesas DedutÃÂ­veis</td><td align='right'><b>R$ {despesa_total:,.2f}</b></td></tr>
            <tr style='border-top:1px solid #22c55e;'><td><b>= Resultado LÃÂ­quido</b></td><td align='right'><b>R$ {resultado_liq:,.2f}</b></td></tr>
            <tr><td>Limite de isenÃÂ§ÃÂ£o</td><td align='right'>R$ {LIMITE_ISENCAO:,.2f}</td></tr>
            <tr><td>Base de cÃÂ¡lculo IR</td><td align='right'><b>R$ {BASE_CALCULO:,.2f}</b></td></tr>
            <tr><td>AlÃÂ­quota aplicada</td><td align='right'>{aliquota_efetiva*100:.1f}%</td></tr>
            <tr style='border-top:1px solid #22c55e;'><td><b>IR Devido (estimado)</b></td><td align='right'><b style='color:#f59e0b;'>R$ {ir_devido:,.2f}</b></td></tr>
            </table>
            </div>
            """, unsafe_allow_html=True)

        with col_calc2:
            st.markdown(f"""
            <div style='background:#0f3460;border-radius:12px;padding:16px 20px;border:1px solid #3b82f6;'>
            <b style='color:#3b82f6;font-size:15px;'>Ã°Å¸ââ¹ Resultado Presumido (20%)</b><br><br>
            <table style='width:100%;color:#f1f5f9;font-size:13px;'>
            <tr><td>Receita Bruta</td><td align='right'><b>R$ {receita_bruta:,.2f}</b></td></tr>
            <tr><td>Base presumida (20%)</td><td align='right'><b>R$ {resultado_pres:,.2f}</b></td></tr>
            <tr><td colspan='2' style='color:#94a3b8;font-size:11px;padding-top:6px;'>
            OpÃÂ§ÃÂ£o pelo resultado presumido ÃÂ© vÃÂ¡lida quando a receita bruta anual nÃÂ£o ultrapassar R$ 130.000,00 (art. 4ÃÂº Lei 8.023/90).
            </td></tr>
            </table>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # SituaÃÂ§ÃÂ£o fiscal
        if receita_bruta == 0:
            st.info("Ã¢âÂ¹Ã¯Â¸Â Preencha as receitas na aba anterior para calcular.")
        elif resultado_liq <= 0:
            st.success("Ã¢Åâ¦ Resultado negativo (prejuÃÂ­zo) Ã¢â¬â nÃÂ£o hÃÂ¡ IR a pagar. O prejuÃÂ­zo pode ser compensado nos prÃÂ³ximos anos.")
        elif BASE_CALCULO <= LIMITE_ISENCAO:
            st.success(f"Ã¢Åâ¦ Resultado abaixo do limite de isenÃÂ§ÃÂ£o (R$ {LIMITE_ISENCAO:,.2f}) Ã¢â¬â nÃÂ£o hÃÂ¡ IR a pagar.")
        else:
            st.warning(f"Ã¢Å¡Â Ã¯Â¸Â IR estimado: **R$ {ir_devido:,.2f}** Ã¢â¬â consulte seu contador para a declaraÃÂ§ÃÂ£o oficial.")

        st.markdown("""
        <div style='background:#1e293b;border-radius:8px;padding:10px 14px;margin-top:12px;border-left:3px solid #f59e0b;'>
        <span style='color:#fbbf24;font-size:12px;'>Ã¢Å¡Â Ã¯Â¸Â <b>Aviso legal:</b> Este cÃÂ¡lculo ÃÂ© uma estimativa para fins de planejamento.
        A declaraÃÂ§ÃÂ£o oficial deve ser feita por contador habilitado com base nos documentos fiscais originais.</span>
        </div>
        """, unsafe_allow_html=True)

    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    # TAB 3 Ã¢â¬â GERAR RELATÃâRIO PDF
    # Ã¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢ÂÃ¢â¢Â
    with tab_ir3:
        st.subheader("Ã°Å¸ââ RelatÃÂ³rio para o Contador")
        st.info("Gera um PDF profissional com todos os dados, pronto para entregar ao seu contador.")

        receita_bruta  = sum(st.session_state.ir_receitas.values())
        despesa_total  = sum(st.session_state.ir_despesas.values())
        resultado_liq  = receita_bruta - despesa_total
        LIMITE_ISENCAO = 142798.50
        BASE_CALCULO   = max(resultado_liq, 0.0)
        tabela_ir = [
            (2259.20*12, 0.000, 0.00),
            (2826.65*12, 0.075, 169.44*12),
            (3751.05*12, 0.150, 381.44*12),
            (4664.68*12, 0.225, 662.77*12),
            (float("inf"), 0.275, 896.00*12),
        ]
        ir_devido = 0.0
        aliquota_ef = 0.0
        if BASE_CALCULO > LIMITE_ISENCAO:
            for limite, aliq, ded in tabela_ir:
                if BASE_CALCULO <= limite:
                    ir_devido    = BASE_CALCULO * aliq - ded
                    aliquota_ef  = aliq
                    break
        ir_devido = max(ir_devido, 0.0)

        if st.button("Ã°Å¸ââ Gerar PDF do RelatÃÂ³rio", use_container_width=True, key="btn_gerar_ir_pdf"):
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.lib import colors
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import cm
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
                from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

                buffer = io.BytesIO()
                doc    = SimpleDocTemplate(buffer, pagesize=A4,
                                           leftMargin=2*cm, rightMargin=2*cm,
                                           topMargin=2*cm, bottomMargin=2*cm)

                styles  = getSampleStyleSheet()
                VERDE   = colors.HexColor("#16a34a")
                AZUL_E  = colors.HexColor("#0f3460")
                CINZA   = colors.HexColor("#64748b")
                BRANCO  = colors.white
                AMARELO = colors.HexColor("#f59e0b")

                s_title  = ParagraphStyle("titulo",  parent=styles["Title"],  fontSize=18, textColor=VERDE,   spaceAfter=4,  alignment=TA_CENTER)
                s_sub    = ParagraphStyle("sub",     parent=styles["Normal"], fontSize=11, textColor=AZUL_E,  spaceAfter=2,  alignment=TA_CENTER)
                s_sec    = ParagraphStyle("sec",     parent=styles["Normal"], fontSize=12, textColor=VERDE,   spaceBefore=14, spaceAfter=4, fontName="Helvetica-Bold")
                s_body   = ParagraphStyle("body",    parent=styles["Normal"], fontSize=10, textColor=colors.HexColor("#1e293b"), spaceAfter=3)
                s_aviso  = ParagraphStyle("aviso",   parent=styles["Normal"], fontSize=8,  textColor=CINZA,   spaceAfter=3,  alignment=TA_CENTER)
                s_bold   = ParagraphStyle("bold",    parent=styles["Normal"], fontSize=10, fontName="Helvetica-Bold")

                story = []

                # CabeÃÂ§alho
                story.append(Paragraph("IAAGRO Ã¢â¬â INTELIGÃÅ NCIA AGRÃÂCOLA", s_title))
                story.append(Paragraph("RelatÃÂ³rio de ApuraÃÂ§ÃÂ£o do Imposto de Renda Ã¢â¬â Atividade Rural", s_sub))
                story.append(Paragraph(f"Ano-CalendÃÂ¡rio: {st.session_state.ir_ano} | Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", s_aviso))
                story.append(HRFlowable(width="100%", thickness=2, color=VERDE, spaceAfter=10))

                # Dados do produtor
                story.append(Paragraph("1. IDENTIFICAÃâ¡ÃÆO DO CONTRIBUINTE", s_sec))
                dados_prod = [
                    ["Nome completo:", st.session_state.ir_nome or "Ã¢â¬â"],
                    ["CPF:", st.session_state.ir_cpf or "Ã¢â¬â"],
                    ["Cidade/UF:", st.session_state.ir_cidade or "Ã¢â¬â"],
                    ["ÃÂrea total declarada:", f"{st.session_state.ir_area_total:.2f} ha"],
                    ["Atividade:", "Produtor Rural Ã¢â¬â Pessoa FÃÂ­sica"],
                    ["Base legal:", "Lei 8.023/90 | IN RFB 1.700/17 | RIR/2018"],
                ]
                t_prod = Table(dados_prod, colWidths=[5.5*cm, 11*cm])
                t_prod.setStyle(TableStyle([
                    ("FONTNAME",    (0,0),(-1,-1), "Helvetica"),
                    ("FONTNAME",    (0,0),(0,-1),  "Helvetica-Bold"),
                    ("FONTSIZE",    (0,0),(-1,-1), 10),
                    ("TEXTCOLOR",   (0,0),(0,-1),  AZUL_E),
                    ("ROWBACKGROUNDS", (0,0),(-1,-1), [colors.HexColor("#f8fafc"), BRANCO]),
                    ("GRID",        (0,0),(-1,-1), 0.3, CINZA),
                    ("PADDING",     (0,0),(-1,-1), 5),
                ]))
                story.append(t_prod)
                story.append(Spacer(1, 10))

                # Receitas
                story.append(Paragraph("2. RECEITAS DA ATIVIDADE RURAL", s_sec))
                rec_labels = {
                    "venda_graos":     "Venda de grÃÂ£os e cereais",
                    "venda_animais":   "Venda de animais e produtos pecuÃÂ¡rios",
                    "arrendamento":    "Arrendamento recebido",
                    "subvencoes":      "SubvenÃÂ§ÃÂµes e incentivos governamentais",
                    "indenizacoes":    "IndenizaÃÂ§ÃÂµes de seguro agrÃÂ­cola",
                    "outras_receitas": "Outras receitas rurais",
                }
                rows_rec = [["DescriÃÂ§ÃÂ£o", "Valor (R$)"]]
                for k, label in rec_labels.items():
                    val = st.session_state.ir_receitas.get(k, 0.0)
                    if val > 0:
                        rows_rec.append([label, f"R$ {val:,.2f}"])
                rows_rec.append(["TOTAL RECEITA BRUTA", f"R$ {receita_bruta:,.2f}"])

                t_rec = Table(rows_rec, colWidths=[12*cm, 4.5*cm])
                t_rec.setStyle(TableStyle([
                    ("BACKGROUND",  (0,0),(-1,0),  VERDE),
                    ("TEXTCOLOR",   (0,0),(-1,0),  BRANCO),
                    ("FONTNAME",    (0,0),(-1,0),  "Helvetica-Bold"),
                    ("FONTNAME",    (0,1),(-1,-2), "Helvetica"),
                    ("FONTNAME",    (0,-1),(-1,-1),"Helvetica-Bold"),
                    ("BACKGROUND",  (0,-1),(-1,-1), colors.HexColor("#dcfce7")),
                    ("FONTSIZE",    (0,0),(-1,-1), 10),
                    ("ALIGN",       (1,0),(-1,-1), "RIGHT"),
                    ("ROWBACKGROUNDS", (0,1),(-1,-2), [colors.HexColor("#f8fafc"), BRANCO]),
                    ("GRID",        (0,0),(-1,-1), 0.3, CINZA),
                    ("PADDING",     (0,0),(-1,-1), 6),
                ]))
                story.append(t_rec)
                story.append(Spacer(1, 10))

                # Despesas
                story.append(Paragraph("3. DESPESAS DEDUTÃÂVEIS (art. 61 RIR/2018)", s_sec))
                desp_labels = {
                    "sementes":        "Sementes e mudas",
                    "fertilizantes":   "Fertilizantes e defensivos agrÃÂ­colas",
                    "mao_de_obra":     "MÃÂ£o de obra (salÃÂ¡rios + encargos sociais)",
                    "combustivel":     "CombustÃÂ­vel e lubrificantes",
                    "energia":         "Energia elÃÂ©trica rural",
                    "arrendamento_pg": "Arrendamento pago",
                    "manutencao":      "ManutenÃÂ§ÃÂ£o de mÃÂ¡quinas e benfeitorias",
                    "depreciacao":     "DepreciaÃÂ§ÃÂ£o de bens do ativo imobilizado",
                    "frete":           "Fretes e carretos",
                    "seguro":          "Seguros rurais",
                    "assistencia_tec": "AssistÃÂªncia tÃÂ©cnica e agronÃÂ´mica",
                    "juros":           "Juros de financiamentos rurais",
                    "outras_despesas": "Outras despesas dedutÃÂ­veis",
                }
                rows_desp = [["DescriÃÂ§ÃÂ£o", "Valor (R$)"]]
                for k, label in desp_labels.items():
                    val = st.session_state.ir_despesas.get(k, 0.0)
                    if val > 0:
                        rows_desp.append([label, f"R$ {val:,.2f}"])
                rows_desp.append(["TOTAL DESPESAS DEDUTÃÂVEIS", f"R$ {despesa_total:,.2f}"])

                t_desp = Table(rows_desp, colWidths=[12*cm, 4.5*cm])
                t_desp.setStyle(TableStyle([
                    ("BACKGROUND",  (0,0),(-1,0),  AZUL_E),
                    ("TEXTCOLOR",   (0,0),(-1,0),  BRANCO),
                    ("FONTNAME",    (0,0),(-1,0),  "Helvetica-Bold"),
                    ("FONTNAME",    (0,1),(-1,-2), "Helvetica"),
                    ("FONTNAME",    (0,-1),(-1,-1),"Helvetica-Bold"),
                    ("BACKGROUND",  (0,-1),(-1,-1), colors.HexColor("#dbeafe")),
                    ("FONTSIZE",    (0,0),(-1,-1), 10),
                    ("ALIGN",       (1,0),(-1,-1), "RIGHT"),
                    ("ROWBACKGROUNDS", (0,1),(-1,-2), [colors.HexColor("#f8fafc"), BRANCO]),
                    ("GRID",        (0,0),(-1,-1), 0.3, CINZA),
                    ("PADDING",     (0,0),(-1,-1), 6),
                ]))
                story.append(t_desp)
                story.append(Spacer(1, 10))

                # ApuraÃÂ§ÃÂ£o IR
                story.append(Paragraph("4. APURAÃâ¡ÃÆO DO IMPOSTO DE RENDA", s_sec))
                sit = "NÃÂ£o hÃÂ¡ IR a pagar (resultado negativo ou abaixo do limite de isenÃÂ§ÃÂ£o)" if ir_devido == 0 else f"IR estimado devido: R$ {ir_devido:,.2f}"
                rows_ir = [
                    ["DescriÃÂ§ÃÂ£o", "Valor (R$)"],
                    ["Receita Bruta Total",                  f"R$ {receita_bruta:,.2f}"],
                    ["(-) Despesas DedutÃÂ­veis",               f"R$ {despesa_total:,.2f}"],
                    ["= Resultado LÃÂ­quido da Atividade Rural",f"R$ {resultado_liq:,.2f}"],
                    ["Limite de isenÃÂ§ÃÂ£o (ano-calendÃÂ¡rio)",    f"R$ {LIMITE_ISENCAO:,.2f}"],
                    ["Base de CÃÂ¡lculo do IR",                 f"R$ {BASE_CALCULO:,.2f}"],
                    ["AlÃÂ­quota aplicada (tabela progressiva)",f"{aliquota_ef*100:.1f}%"],
                    ["IR ESTIMADO DEVIDO",                    f"R$ {ir_devido:,.2f}"],
                ]
                t_ir = Table(rows_ir, colWidths=[12*cm, 4.5*cm])
                t_ir.setStyle(TableStyle([
                    ("BACKGROUND",  (0,0),(-1,0),  colors.HexColor("#1e293b")),
                    ("TEXTCOLOR",   (0,0),(-1,0),  BRANCO),
                    ("FONTNAME",    (0,0),(-1,0),  "Helvetica-Bold"),
                    ("FONTNAME",    (0,1),(-1,-2), "Helvetica"),
                    ("FONTNAME",    (0,-1),(-1,-1),"Helvetica-Bold"),
                    ("BACKGROUND",  (0,-1),(-1,-1), colors.HexColor("#fef3c7")),
                    ("TEXTCOLOR",   (0,-1),(-1,-1), colors.HexColor("#92400e")),
                    ("FONTSIZE",    (0,0),(-1,-1), 10),
                    ("ALIGN",       (1,0),(-1,-1), "RIGHT"),
                    ("ROWBACKGROUNDS", (0,1),(-1,-2), [colors.HexColor("#f8fafc"), BRANCO]),
                    ("GRID",        (0,0),(-1,-1), 0.3, CINZA),
                    ("PADDING",     (0,0),(-1,-1), 6),
                ]))
                story.append(t_ir)
                story.append(Spacer(1, 12))

                # ProduÃÂ§ÃÂ£o (se preenchida)
                prod_preench = {k:v for k,v in st.session_state.ir_producao.items() if v > 0}
                if prod_preench:
                    story.append(Paragraph("5. MEMORIAL DESCRITIVO Ã¢â¬â PRODUÃâ¡ÃÆO", s_sec))
                    rows_prod = [["Cultura", "Quantidade produzida"]]
                    for cult, qtd in prod_preench.items():
                        rows_prod.append([cult, f"{qtd:,.1f} sc/kg"])
                    t_prod2 = Table(rows_prod, colWidths=[8*cm, 8.5*cm])
                    t_prod2.setStyle(TableStyle([
                        ("BACKGROUND",  (0,0),(-1,0),  VERDE),
                        ("TEXTCOLOR",   (0,0),(-1,0),  BRANCO),
                        ("FONTNAME",    (0,0),(-1,0),  "Helvetica-Bold"),
                        ("FONTNAME",    (0,1),(-1,-1), "Helvetica"),
                        ("FONTSIZE",    (0,0),(-1,-1), 10),
                        ("ROWBACKGROUNDS", (0,1),(-1,-1), [colors.HexColor("#f8fafc"), BRANCO]),
                        ("GRID",        (0,0),(-1,-1), 0.3, CINZA),
                        ("PADDING",     (0,0),(-1,-1), 6),
                    ]))
                    story.append(t_prod2)
                    story.append(Spacer(1, 10))

                # RodapÃÂ© / aviso legal
                story.append(HRFlowable(width="100%", thickness=1, color=CINZA, spaceAfter=6))
                story.append(Paragraph(
                    "Ã¢Å¡Â Ã¯Â¸Â Este relatÃÂ³rio ÃÂ© um auxÃÂ­lio ao planejamento tributÃÂ¡rio gerado pelo sistema IAAGRO. "
                    "NÃÂ£o substitui a declaraÃÂ§ÃÂ£o oficial do IRPF nem a orientaÃÂ§ÃÂ£o de contador habilitado. "
                    "Base legal: Lei 8.023/1990, IN RFB 1.700/2017, Decreto 9.580/2018 (RIR/2018).",
                    s_aviso
                ))
                story.append(Spacer(1, 4))
                story.append(Paragraph(
                    f"Gerado por IAAGRO Ã¢â¬Â¢ {datetime.now().strftime('%d/%m/%Y ÃÂ s %H:%M')} Ã¢â¬Â¢ www.iaagro.com.br",
                    s_aviso
                ))

                doc.build(story)
                pdf_bytes = buffer.getvalue()

                nome_arq = f"IR_Rural_{st.session_state.ir_nome.replace(' ','_') or 'produtor'}_{st.session_state.ir_ano}.pdf"
                st.success("Ã¢Åâ¦ RelatÃÂ³rio gerado com sucesso!")
                st.download_button(
                    label="Ã°Å¸âÂ¥ Baixar RelatÃÂ³rio PDF",
                    data=pdf_bytes,
                    file_name=nome_arq,
                    mime="application/pdf",
                    use_container_width=True,
                    key="btn_download_ir_pdf"
                )

            except Exception as e:
                st.error(f"Ã¢ÂÅ Erro ao gerar PDF: {e}")

        st.markdown("""
        <div style='background:#0f3460;border-radius:10px;padding:14px 18px;margin-top:16px;border:1px solid #22c55e;'>
        <b style='color:#22c55e;'>Ã°Å¸ââ¹ O relatÃÂ³rio contÃÂ©m:</b>
        <ul style='color:#f1f5f9;font-size:13px;margin-top:8px;'>
        <li>IdentificaÃÂ§ÃÂ£o completa do produtor</li>
        <li>Demonstrativo de receitas por categoria</li>
        <li>Demonstrativo de despesas dedutÃÂ­veis (art. 61 RIR/2018)</li>
        <li>ApuraÃÂ§ÃÂ£o do IR com tabela progressiva 2025</li>
        <li>Memorial descritivo de produÃÂ§ÃÂ£o por cultura</li>
        <li>Base legal completa para o contador</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬Ã¢ââ¬
elif menu == "Ã¢Å¡â¢Ã¯Â¸Â ConfiguraÃÂ§ÃÂµes":
    st.header("Ã¢Å¡â¢Ã¯Â¸Â ConfiguraÃÂ§ÃÂµes do Sistema")

    tab0, tab_planos, tab1, tab2, tab3, tab4 = st.tabs([
        "Ã°Å¸ÅÂ¾ Meu Segmento",
        "Ã°Å¸âÂ³ Planos & PreÃÂ§os",
        "Ã°Å¸âÂ¾ Backup & Restore",
        "Ã°Å¸âÂ§ Email & Alertas",
        "Ã°Å¸âÅ  HistÃÂ³rico do Solo",
        "Ã°Å¸âÂ¤ Exportar Excel"
    ])

    with tab_planos:
        st.subheader("Ã°Å¸âÂ³ Planos & PreÃÂ§os")
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
                atual_txt  = "&nbsp;Ã¢Åâ¦ ATUAL" if is_atual else ""
                preco_txt  = "GrÃÂ¡tis" if preco == 0 else f"R$ {preco:.2f}/mÃÂªs"
                rec_html   = "".join(f"Ã¢Åâ¦ {r}<br>" for r in plano["recursos"])
                bloq_html  = "".join(f"Ã°Å¸ââ {r}<br>" for r in plano["bloqueados"])

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
                    # Cada plano tem seu prÃÂ³prio link
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
                        f"Ã°Å¸âÂ³ Mensal Ã¢â¬â R$ {btn_preco:.2f}/mÃÂªs",
                        btn_lmes,
                        use_container_width=True
                    )
                    st.link_button(
                        f"Ã°Å¸Ââ  Anual Ã¢â¬â R$ {btn_pano} (-15%)",
                        btn_lano,
                        use_container_width=True
                    )
                    st.caption("PIX Ã¢â¬Â¢ CartÃÂ£o Ã¢â¬Â¢ Boleto")
                elif is_atual:
                    st.markdown(f"""
                    <div style='background:{plano["borda"]}33;border-radius:8px;padding:10px;
                    text-align:center;margin-top:8px;color:{plano["borda"]};font-weight:700;'>
                    Ã¢Åâ¦ Plano Ativo
                    </div>
                    """, unsafe_allow_html=True)

        st.divider()
        st.markdown("""
        <div style='background:#0f3460;border-radius:10px;padding:14px 18px;border:1px solid #3b82f6;'>
        <b style='color:#3b82f6;'>Ã°Å¸âÂ³ Como ativar o Plano Pro ou Premium?</b><br>
        <span style='color:#f1f5f9;font-size:13px;'>
        1. Clique em <b>Mensal</b> ou <b>Anual</b> no plano desejado<br>
        2. VocÃÂª serÃÂ¡ redirecionado para o <b>Mercado Pago</b><br>
        3. Pague via PIX, cartÃÂ£o ou boleto<br>
        4. Seu plano ÃÂ© ativado <b>automaticamente</b> apÃÂ³s confirmaÃÂ§ÃÂ£o<br>
        5. FaÃÂ§a logout e login novamente para ver o novo plano
        </span>
        </div>
        """, unsafe_allow_html=True)

    with tab0:
        st.subheader("Ã°Å¸ÅÂ¾ Alterar Segmento de AtuaÃÂ§ÃÂ£o")
        st.info(f"Segmento atual: **{st.session_state.segmento or 'NÃÂ£o definido'}**")
        SEGMENTOS_CFG = {
            "Ã°Å¸ÅÂ¾ GrÃÂ£os":        "Soja, Milho, Trigo e outros cereais",
            "Ã°Å¸ÅÂ¿ Horticultura": "HortaliÃÂ§as, verduras e legumes",
            "Ã°Å¸ÂÅ½ Fruticultura": "Frutas tropicais, uva, cafÃÂ© e outras",
            "Ã°Å¸ÅÂ² Silvicultura": "Eucalipto, Pinus e reflorestamento",
        }
        st.markdown("#### Selecione o novo segmento:")
        for seg, desc in SEGMENTOS_CFG.items():
            col_s1, col_s2 = st.columns([2, 5])
            with col_s1:
                if st.button(seg, key=f"cfg_seg_{seg}", use_container_width=True):
                    st.session_state.segmento = seg
                    salvar_dados_iaagro()
                    st.success(f"Ã¢Åâ¦ Segmento alterado para **{seg}**!")
                    st.rerun()
            with col_s2:
                st.markdown(f"<div style='padding:10px 0;color:#94a3b8;font-size:13px;'>{desc}</div>", unsafe_allow_html=True)

    # Ã¢ââ¬Ã¢ââ¬ TAB 1: BACKUP & RESTORE Ã¢ââ¬Ã¢ââ¬
    with tab1:
        st.subheader("Ã°Å¸âÂ¾ Backup & RestauraÃÂ§ÃÂ£o de Dados")

        st.markdown('''<div style="background:#7f1d1d;color:#fff;padding:14px 18px;
        border-radius:10px;border-left:5px solid #ef4444;font-weight:700;margin:8px 0 16px 0;font-size:14px;">
        Ã¢Å¡Â Ã¯Â¸Â <b>IMPORTANTE Ã¢â¬â Antes de atualizar o app:</b><br>
        O Streamlit Cloud nÃÂ£o persiste arquivos entre deploys. Sempre faÃÂ§a backup
        antes de enviar uma atualizaÃÂ§ÃÂ£o via Git. ApÃÂ³s atualizar, restaure o backup para
        recuperar seus dados (usuÃÂ¡rios, estoque, ÃÂ¡reas, histÃÂ³rico).
        </div>''', unsafe_allow_html=True)

        # Auto-backup ao abrir a aba
        st.markdown("#### Ã°Å¸âÂ¥ Fazer Backup Agora")
        st.markdown('''<div style="background:#0f3460;color:#93c5fd;padding:10px 14px;
        border-radius:8px;font-size:12px;font-weight:600;margin:4px 0 12px 0;">
        Ã°Å¸âÂ¡ Salve este arquivo no seu computador. Ele contÃÂ©m todos os seus dados:
        usuÃÂ¡rios, estoque, ÃÂ¡reas cadastradas, histÃÂ³rico, aplicaÃÂ§ÃÂµes e configuraÃÂ§ÃÂµes.
        </div>''', unsafe_allow_html=True)

        backup_data = gerar_backup()
        st.download_button(
            "Ã°Å¸âÂ¥ Baixar Backup Completo (.json)",
            data=backup_data,
            file_name=f"iaagro_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )

        st.divider()
        st.markdown("#### Ã°Å¸ââ Restaurar Backup")
        st.markdown('''<div style="background:#78350f;color:#fff;padding:11px 14px;
        border-radius:8px;border-left:4px solid #f59e0b;font-weight:600;margin:4px 0 12px 0;font-size:13px;">
        Ã¢Å¡Â Ã¯Â¸Â A restauraÃÂ§ÃÂ£o substitui TODOS os dados atuais. Use apÃÂ³s atualizar o app.
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
            # LÃÂª e armazena o conteÃÂºdo no session_state imediatamente
            conteudo_backup = arquivo_restore.read()
            st.session_state["_backup_conteudo"] = conteudo_backup
            st.success(f"Ã¢Åâ¦ Arquivo **{arquivo_restore.name}** carregado ({len(conteudo_backup)//1024} KB)")

        if st.session_state.get("_backup_conteudo"):
            if st.button("Ã°Å¸ââ Restaurar Backup Agora", key="btn_restore", use_container_width=True, type="primary"):
                import io
                ok, msg = restaurar_backup(io.BytesIO(st.session_state["_backup_conteudo"]))
                if ok:
                    st.session_state["_backup_conteudo"] = None
                    st.success(f"Ã¢Åâ¦ {msg}")
                    st.rerun()
                else:
                    st.error(f"Ã¢ÂÅ {msg}")

        # Passo a passo
        st.divider()
        st.markdown("#### Ã°Å¸ââ¹ Passo a passo para atualizar sem perder dados")
        passos_bk = [
            ("1Ã¯Â¸ÂÃ¢ÆÂ£", "Acesse Ã¢Å¡â¢Ã¯Â¸Â ConfiguraÃÂ§ÃÂµes Ã¢â â Backup & RestauraÃÂ§ÃÂ£o"),
            ("2Ã¯Â¸ÂÃ¢ÆÂ£", "Clique em **Ã°Å¸âÂ¥ Baixar Backup Completo** e salve no computador"),
            ("3Ã¯Â¸ÂÃ¢ÆÂ£", "Atualize o app normalmente via Git (git add Ã¢â â commit Ã¢â â push)"),
            ("4Ã¯Â¸ÂÃ¢ÆÂ£", "Aguarde o Streamlit Cloud reiniciar (1-2 minutos)"),
            ("5Ã¯Â¸ÂÃ¢ÆÂ£", "Acesse o app Ã¢â â Ã¢Å¡â¢Ã¯Â¸Â ConfiguraÃÂ§ÃÂµes Ã¢â â Backup & RestauraÃÂ§ÃÂ£o"),
            ("6Ã¯Â¸ÂÃ¢ÆÂ£", "FaÃÂ§a upload do arquivo backup e clique em **Ã°Å¸ââ Restaurar**"),
            ("7Ã¯Â¸ÂÃ¢ÆÂ£", "Todos os dados estarÃÂ£o de volta Ã¢Åâ¦"),
        ]
        for num, desc in passos_bk:
            st.markdown(f'<div style="background:#0f3460;color:#f1f5f9;padding:8px 14px;'
                        f'border-radius:8px;margin:4px 0;font-size:13px;">'
                        f'<b>{num}</b> {desc}</div>', unsafe_allow_html=True)

    # Ã¢ââ¬Ã¢ââ¬ TAB 2: EMAIL & ALERTAS Ã¢ââ¬Ã¢ââ¬
    with tab2:
        st.subheader("Ã°Å¸âÂ§ ConfiguraÃÂ§ÃÂ£o de Email para Alertas")
        st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
        Ã¢âÂ¹Ã¯Â¸Â Configure um email para receber alertas automÃÂ¡ticos quando o estoque estiver baixo.
        Use Gmail com senha de app (configuraÃÂ§ÃÂµes Ã¢â â seguranÃÂ§a Ã¢â â senhas de app).
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
        cfg["ativo"] = st.checkbox("Ã¢Åâ¦ Ativar alertas por email", value=cfg.get("ativo", False), key="chk___ativar_alerta_8829")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Ã°Å¸âÂ¾ Salvar ConfiguraÃÂ§ÃÂµes de Email"):
                st.session_state.email_config = cfg
                st.markdown('''<div style="background:#14532d;color:#fff;padding:12px 18px;
                border-radius:10px;border-left:5px solid #22c55e;font-weight:600;">
                Ã¢Åâ¦ ConfiguraÃÂ§ÃÂµes salvas!</div>''', unsafe_allow_html=True)
        with col_b:
            if st.button("Ã°Å¸âÂ§ Testar Envio de Email"):
                ok = enviar_email_alerta(
                    cfg.get("email_destino",""),
                    "Ã¢Åâ¦ IAAgro Pro Ã¢â¬â Teste de Email",
                    "<h2>Ã¢Åâ¦ Email configurado com sucesso!</h2><p>VocÃÂª receberÃÂ¡ alertas de estoque aqui.</p>"
                )
                if ok:
                    st.markdown('''<div style="background:#14532d;color:#fff;padding:12px 18px;
                    border-radius:10px;border-left:5px solid #22c55e;font-weight:600;">
                    Ã¢Åâ¦ Email de teste enviado com sucesso!</div>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<div style="background:#7f1d1d;color:#fff;padding:12px 18px;
                    border-radius:10px;border-left:5px solid #ef4444;font-weight:600;">
                    Ã¢ÂÅ Falha ao enviar. Verifique as configuraÃÂ§ÃÂµes.</div>''', unsafe_allow_html=True)

        if cfg.get("ativo"):
            st.divider()
            if st.button("Ã°Å¸ââ Verificar Alertas de Estoque Agora"):
                checar_alertas_estoque()
                st.markdown('''<div style="background:#14532d;color:#fff;padding:12px 18px;
                border-radius:10px;border-left:5px solid #22c55e;font-weight:600;">
                Ã¢Åâ¦ VerificaÃÂ§ÃÂ£o concluÃÂ­da!</div>''', unsafe_allow_html=True)

    # Ã¢ââ¬Ã¢ââ¬ TAB 3: HISTÃâRICO DO SOLO Ã¢ââ¬Ã¢ââ¬
    with tab3:
        st.subheader("Ã°Å¸âÅ  EvoluÃÂ§ÃÂ£o da Fertilidade do Solo")
        if not st.session_state.areas:
            st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
            border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;">
            Ã¢âÂ¹Ã¯Â¸Â Cadastre e analise ÃÂ¡reas para ver o histÃÂ³rico.</div>''', unsafe_allow_html=True)
        else:
            opcoes_area = [f"{a['ID']} - {a['TalhÃÂ£o']}" for a in st.session_state.areas]
            area_hist   = st.selectbox("Selecione a ÃÂ¡rea", opcoes_area, key="hist_solo_area")
            id_area_sel = area_hist.split(" - ")[0]

            df_hist = carregar_historico_solo_db(id_area_sel)
            if df_hist.empty:
                st.markdown('''<div style="background:#78350f;color:#fff;padding:13px 18px;
                border-radius:10px;border-left:5px solid #f59e0b;font-weight:600;">
                Ã¢Å¡Â Ã¯Â¸Â Nenhuma anÃÂ¡lise salva no banco ainda. Salve uma anÃÂ¡lise na aba "AnÃÂ¡lise de Solo".</div>''',
                unsafe_allow_html=True)
            else:
                st.dataframe(df_hist[["data","ph","fosforo","potassio","materia_organica",
                                       "calcio","magnesio","nota","score","classe"]],
                             use_container_width=True)
                st.subheader("Ã°Å¸âË EvoluÃÂ§ÃÂ£o do Score e Nota")
                col1, col2 = st.columns(2)
                with col1:
                    st.line_chart(df_hist.set_index("data")[["score","nota"]])
                with col2:
                    st.line_chart(df_hist.set_index("data")[["ph","fosforo","potassio"]])

    # Ã¢ââ¬Ã¢ââ¬ TAB 4: EXPORTAR EXCEL Ã¢ââ¬Ã¢ââ¬
    with tab4:
        st.subheader("Ã°Å¸âÂ¤ Exportar Dados para Excel")
        st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;
        border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">
        Ã¢âÂ¹Ã¯Â¸Â Gera um arquivo Excel com mÃÂºltiplas abas contendo todos os dados do sistema.
        </div>''', unsafe_allow_html=True)

        if st.button("Ã°Å¸âÅ  Gerar RelatÃÂ³rio Excel Completo"):
            dados_export = {
                "ÃÂreas":     st.session_state.areas,
                "Estoque":   st.session_state.estoque,
                "AplicaÃÂ§ÃÂµes":[
                    {**{k:v for k,v in ap.items() if k != "Produtos"},
                     "Produtos": str(ap.get("Produtos",[]))}
                    for ap in st.session_state.aplicacoes
                ],
                "Hist Produt": st.session_state.historico_produtividade,
                "PluviÃÂ´metro": st.session_state.pluviometro,
                "AnÃÂ¡lise Solo":[st.session_state.dados] if st.session_state.dados else []
            }
            xlsx = exportar_excel(dados_export)
            if xlsx:
                st.download_button(
                    "Ã°Å¸âÂ¥ Baixar Excel Completo",
                    data=xlsx,
                    file_name=f"iaagro_relatorio_{date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

# Ã¢ââ¬Ã¢ââ¬ PWA Ã¢â¬â Progressive Web App (instalÃÂ¡vel no Android/iOS) Ã¢ââ¬Ã¢ââ¬
st.markdown("""
<link rel="manifest" href="https://raw.githubusercontent.com/luciano880/iaagro-app/main/manifest.json">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="IAAGRO">
<meta name="theme-color" content="#22c55e">
<script>
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js').catch(()=>{});
}
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
  deferredPrompt = e;
  const btn = document.getElementById('pwa-install-btn');
  if (btn) btn.style.display = 'block';
});
</script>
""", unsafe_allow_html=True)

# Ã¢ââ¬Ã¢ââ¬ Persiste token no sessionStorage para sobreviver reload Ã¢ââ¬Ã¢ââ¬
if st.session_state.get("sb_token") and st.session_state.get("sb_user_id"):
    _tk  = st.session_state.sb_token
    _uid = st.session_state.sb_user_id
    _pl  = st.session_state.get("sb_plano","free")
    _nm  = st.session_state.get("usuario_atual","")
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

