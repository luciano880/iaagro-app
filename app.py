import streamlit as st

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



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# TESSERACT ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ caminho para Windows

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# SUPABASE ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ importa mÃÂÃÂ³dulo de integraÃÂÃÂ§ÃÂÃÂ£o

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# CORREÃÂÃ¢ÂÂ¡ÃÂÃÂO 1: funÃÂÃÂ§ÃÂÃÂ£o sem recursÃÂÃÂ£o infinita

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# CSS UNIFICADO (sem conflitos e sem duplicatas)

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

st.markdown("""

<style>

/* ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

   RESET GERAL ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ evita fundo branco do Streamlit

ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ */

html, body, [data-testid="stAppViewContainer"],

[data-testid="stAppViewBlockContainer"],

[data-testid="block-container"],

.main, .stApp {

    background-color: #0d2137 !important;

    color: #f1f5f9 !important;

}



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FUNDO GERAL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

.stApp {

    background: linear-gradient(160deg, #0d2137 0%, #123354 50%, #1a4a73 100%) !important;

}



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TEXTO GERAL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

p, span, div, li, label,

.stMarkdown p, .stMarkdown li,

[data-testid="stText"],

[data-testid="stMarkdownContainer"] p,

[data-testid="stMarkdownContainer"] {

    color: #f1f5f9 !important;

}



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TÃÂÃÂTULOS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

h1, h2, h3, h4, h5, h6 {

    color: #6ee7b7 !important;

    font-weight: 800 !important;

}



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ LABELS DE CAMPOS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ INPUTS TEXT / NUMBER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SELECTBOX ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ DATE INPUT ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

.stDateInput input {

    background: #0f3460 !important;

    color: #ffffff !important;

    border: 2px solid #22c55e !important;

    border-radius: 10px !important;

}



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TEXTAREA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

.stTextArea textarea {

    background: #0f3460 !important;

    color: #ffffff !important;

    border: 2px solid #22c55e !important;

    border-radius: 10px !important;

}



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ NÃÂÃÂ¡MERO (botÃÂÃÂµes +/-) ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

.stNumberInput button {

    background: #1a4a73 !important;

    color: #ffffff !important;

    border: 1px solid #60a5fa !important;

    border-radius: 6px !important;

}



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BOTÃÂÃ¢ÂÂ¢ES ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ DOWNLOAD BUTTON ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MÃÂÃ¢ÂÂ°TRICAS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ DATAFRAMES ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ALERTAS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

.stAlert {

    border-radius: 12px !important;

    font-weight: 600 !important;

}

.stAlert *, .stAlert p, .stAlert div, .stAlert span {

    color: #0f172a !important;

    font-weight: 600 !important;

}



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TABS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ EXPANDER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SIDEBAR ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ PROGRESS BAR ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

.stProgress > div > div {

    background: linear-gradient(90deg, #00c853, #16a34a) !important;

    border-radius: 10px !important;

}

.stProgress > div {

    background: #1a4a73 !important;

    border-radius: 10px !important;

}



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPLOAD ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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

/* Texto "Drag and drop" e instruÃÂÃÂ§ÃÂÃÂµes */

div[data-testid="stFileUploaderDropzone"] span,

div[data-testid="stFileUploaderDropzone"] p,

div[data-testid="stFileUploaderDropzone"] small {

    color: #ffffff !important;

    font-size: 14px !important;

}

/* BotÃÂÃÂ£o Browse/Upload */

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

/* ÃÂÃÂcone de upload */

div[data-testid="stFileUploaderDropzone"] svg {

    fill: #22c55e !important;

    stroke: #22c55e !important;

}



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ INFO BOX dentro do st.info ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

[data-testid="stNotification"] * { color: #0f172a !important; }



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ DIVIDER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

hr { border-color: #1e3a5f !important; }



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ RADIO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

.stRadio > div { background: transparent !important; }

.stRadio [data-testid="stWidgetLabel"] p { color: #6ee7b7 !important; }



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CHECKBOX ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

.stCheckbox label p { color: #f1f5f9 !important; }



/* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MULTISELECT ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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

/* Dropdown aberto ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ fundo e texto dos itens */

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

    content: "ÃÂ¢ÃÂÃ¢ÂÂ¦ Todos selecionados" !important;

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



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# HELPERS DE NOTIFICAÃÂÃ¢ÂÂ¡ÃÂÃÂO ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ garantem legibilidade

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

def info_box(msg):

    st.markdown(f'<div style="background:#1e3a5f;color:#ffffff;padding:13px 18px;border-radius:10px;'

                f'border-left:5px solid #3b82f6;font-weight:600;font-size:15px;margin:6px 0;">'

                f'ÃÂ¢Ã¢ÂÂÃÂ¹ÃÂ¯ÃÂ¸ÃÂ {msg}</div>', unsafe_allow_html=True)



def success_box(msg):

    st.markdown(f'<div style="background:#14532d;color:#ffffff;padding:13px 18px;border-radius:10px;'

                f'border-left:5px solid #22c55e;font-weight:600;font-size:15px;margin:6px 0;">'

                f'ÃÂ¢ÃÂÃ¢ÂÂ¦ {msg}</div>', unsafe_allow_html=True)



def warning_box(msg):

    st.markdown(f'<div style="background:#78350f;color:#ffffff;padding:13px 18px;border-radius:10px;'

                f'border-left:5px solid #f59e0b;font-weight:600;font-size:15px;margin:6px 0;">'

                f'ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ {msg}</div>', unsafe_allow_html=True)



def error_box(msg):

    st.markdown(f'<div style="background:#7f1d1d;color:#ffffff;padding:13px 18px;border-radius:10px;'

                f'border-left:5px solid #ef4444;font-weight:600;font-size:15px;margin:6px 0;">'

                f'ÃÂ¢ÃÂÃÂ {msg}</div>', unsafe_allow_html=True)





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# ARQUIVOS DE PERSISTÃÂÃÂ NCIA

# usuarios.json fica no repositÃÂÃÂ³rio (persistente entre deploys)

# dados operacionais ficam em /tmp (sessÃÂÃÂ£o)

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

import pathlib



_BASE_DIR = pathlib.Path("/tmp/iaagro_data")

_BASE_DIR.mkdir(parents=True, exist_ok=True)



# UsuÃÂÃÂ¡rios: salva no diretÃÂÃÂ³rio do app (persistente no Git/repositÃÂÃÂ³rio)

_REPO_DIR = pathlib.Path(__file__).parent if "__file__" in dir() else pathlib.Path(".")

ARQUIVO_USUARIOS     = str(_REPO_DIR / "usuarios.json")



# Dados operacionais em /tmp (rÃÂÃÂ¡pido, mas reseta no redeploy)

ARQUIVO_ESTOQUE      = str(_BASE_DIR / "estoque.json")

ARQUIVO_AREAS        = str(_BASE_DIR / "areas.json")

ARQUIVO_DADOS_IAAGRO = str(_BASE_DIR / "dados_iaagro.json")

DB_FILE              = str(_BASE_DIR / "iaagro.db")



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# CORREÃÂÃ¢ÂÂ¡ÃÂÃÂO 9: senhas com hash (hashlib)

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

def hash_senha(senha: str) -> str:

    return hashlib.sha256(senha.encode()).hexdigest()



def verificar_senha(senha: str, hash_armazenado: str) -> bool:

    return hash_senha(senha) == hash_armazenado



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# BANCO DE DADOS SQLITE ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ histÃÂÃÂ³rico de solo

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# VALIDAÃÂÃ¢ÂÂ¡ÃÂÃÂO DE CAMPOS

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

def validar_ph(v):

    return 3.5 <= v <= 9.0



def validar_email_fmt(email):

    return bool(re.match(r'^[^@]+@[^@]+\.[^@]+$', email))



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# EXPORTAR XLSX

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# BACKUP / RESTORE

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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

            return False, "Arquivo invÃÂÃÂ¡lido ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o parece ser um backup do IAAgro."

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

        return True, f"Backup de {dados.get('backup_data','?')} restaurado! {n_areas} ÃÂÃÂ¡reas, {n_estoque} itens de estoque."

    except json.JSONDecodeError:

        return False, "Arquivo corrompido ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o ÃÂÃÂ© um JSON vÃÂÃÂ¡lido."

    except Exception as e:

        return False, f"Erro ao restaurar: {e}"



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# EMAIL SMTP ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ alertas de estoque

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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

    """Envia email com token de 6 dÃÂÃÂ­gitos para recuperaÃÂÃÂ§ÃÂÃÂ£o de senha."""

    try:

        cfg = st.session_state.get("email_config", {})

        if not cfg.get("ativo") or not cfg.get("remetente"):

            return False, "Email nÃÂÃÂ£o configurado. VÃÂÃÂ¡ em ÃÂ¢ÃÂ¡Ã¢ÂÂ¢ÃÂ¯ÃÂ¸ÃÂ ConfiguraÃÂÃÂ§ÃÂÃÂµes ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ Email SMTP."

        corpo = f"""

        <div style="font-family:Arial,sans-serif;max-width:500px;margin:auto;

        background:#0f2744;color:#fff;border-radius:14px;padding:30px;">

        <h2 style="color:#22c55e;text-align:center;">ÃÂ°ÃÂ¸ÃÂÃÂ¿ IAAgro Pro</h2>

        <h3 style="text-align:center;color:#fff;">RecuperaÃÂÃÂ§ÃÂÃÂ£o de Senha</h3>

        <p>OlÃÂÃÂ¡, <b>{usuario}</b>!</p>

        <p>Recebemos uma solicitaÃÂÃÂ§ÃÂÃÂ£o para redefinir sua senha.</p>

        <p>Use o cÃÂÃÂ³digo abaixo para criar uma nova senha:</p>

        <div style="background:#1e3a5f;border-radius:10px;padding:20px;text-align:center;

        margin:20px 0;">

          <span style="font-size:36px;font-weight:900;letter-spacing:10px;color:#22c55e;">

          {token}

          </span>

        </div>

        <p style="color:#93c5fd;font-size:13px;">

        ÃÂ¢ÃÂÃÂ±ÃÂ¯ÃÂ¸ÃÂ Este cÃÂÃÂ³digo expira em <b>15 minutos</b>.<br>

        Se nÃÂÃÂ£o foi vocÃÂÃÂª, ignore este email.

        </p>

        <hr style="border-color:#1e3a5f;margin:20px 0;">

        <p style="color:#6b7280;font-size:11px;text-align:center;">

        IAAgro Pro ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Sistema de GestÃÂÃÂ£o AgrÃÂÃÂ­cola Inteligente

        </p>

        </div>

        """

        msg = MIMEMultipart()

        msg["From"]    = cfg["remetente"]

        msg["To"]      = email_destino

        msg["Subject"] = "ÃÂ°ÃÂ¸ÃÂÃÂ¿ IAAgro Pro ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ CÃÂÃÂ³digo de recuperaÃÂÃÂ§ÃÂÃÂ£o de senha"

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

               if 0 < i.get("Quantidade",0) <= i.get("Estoque MÃÂÃÂ­nimo",0)]

    if zerados or baixos:

        corpo = "<h2>ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ IAAgro Pro ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Alerta de Estoque</h2><ul>"

        for i in zerados:

            corpo += f"<li>ÃÂ¢ÃÂÃÂ <b>{i['Insumo']}</b>: estoque ZERADO</li>"

        for i in baixos:

            corpo += f"<li>ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ <b>{i['Insumo']}</b>: {i['Quantidade']:.1f} (mÃÂÃÂ­n: {i['Estoque MÃÂÃÂ­nimo']:.1f})</li>"

        corpo += "</ul><p>Acesse o IAAgro Pro para repor o estoque.</p>"

        enviar_email_alerta(cfg["email_destino"], "ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ IAAgro ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Alerta de Estoque", corpo)





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# CLIMA EM TEMPO REAL ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Open-Meteo (gratuito, sem API key)

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

def buscar_clima(lat, lon):

    """Busca clima atual + previsÃÂÃÂ£o 7 dias via Open-Meteo (gratuita, sem chave)."""

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

    """Converte weathercode Open-Meteo em emoji + descriÃÂÃÂ§ÃÂÃÂ£o."""

    mapa = {

        0: ("ÃÂ¢ÃÂÃ¢ÂÂ¬ÃÂ¯ÃÂ¸ÃÂ", "CÃÂÃÂ©u limpo"), 1: ("ÃÂ°ÃÂ¸ÃÂÃÂ¤ÃÂ¯ÃÂ¸ÃÂ", "Principalmente limpo"),

        2: ("ÃÂ¢Ã¢ÂÂºÃ¢ÂÂ¦", "Parcialmente nublado"), 3: ("ÃÂ¢ÃÂÃÂÃÂ¯ÃÂ¸ÃÂ", "Nublado"),

        45: ("ÃÂ°ÃÂ¸ÃÂÃÂ«ÃÂ¯ÃÂ¸ÃÂ", "NÃÂÃÂ©voa"), 48: ("ÃÂ°ÃÂ¸ÃÂÃÂ«ÃÂ¯ÃÂ¸ÃÂ", "NÃÂÃÂ©voa com geada"),

        51: ("ÃÂ°ÃÂ¸ÃÂÃÂ¦ÃÂ¯ÃÂ¸ÃÂ", "Garoa leve"), 53: ("ÃÂ°ÃÂ¸ÃÂÃÂ¦ÃÂ¯ÃÂ¸ÃÂ", "Garoa moderada"),

        55: ("ÃÂ°ÃÂ¸ÃÂÃÂ§ÃÂ¯ÃÂ¸ÃÂ", "Garoa intensa"), 61: ("ÃÂ°ÃÂ¸ÃÂÃÂ§ÃÂ¯ÃÂ¸ÃÂ", "Chuva leve"),

        63: ("ÃÂ°ÃÂ¸ÃÂÃÂ§ÃÂ¯ÃÂ¸ÃÂ", "Chuva moderada"), 65: ("ÃÂ°ÃÂ¸ÃÂÃÂ§ÃÂ¯ÃÂ¸ÃÂ", "Chuva intensa"),

        71: ("ÃÂ°ÃÂ¸ÃÂÃÂ¨ÃÂ¯ÃÂ¸ÃÂ", "Neve leve"), 73: ("ÃÂ°ÃÂ¸ÃÂÃÂ¨ÃÂ¯ÃÂ¸ÃÂ", "Neve moderada"),

        75: ("ÃÂ¢ÃÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ", "Neve intensa"), 80: ("ÃÂ°ÃÂ¸ÃÂÃÂ¦ÃÂ¯ÃÂ¸ÃÂ", "Chuva rÃÂÃÂ¡pida leve"),

        81: ("ÃÂ°ÃÂ¸ÃÂÃÂ§ÃÂ¯ÃÂ¸ÃÂ", "Chuva rÃÂÃÂ¡pida moderada"), 82: ("ÃÂ¢Ã¢ÂÂºÃÂÃÂ¯ÃÂ¸ÃÂ", "Chuva rÃÂÃÂ¡pida intensa"),

        95: ("ÃÂ¢Ã¢ÂÂºÃÂÃÂ¯ÃÂ¸ÃÂ", "Trovoada"), 96: ("ÃÂ¢Ã¢ÂÂºÃÂÃÂ¯ÃÂ¸ÃÂ", "Trovoada com granizo"),

        99: ("ÃÂ¢Ã¢ÂÂºÃÂÃÂ¯ÃÂ¸ÃÂ", "Trovoada intensa"),

    }

    return mapa.get(code, ("ÃÂ°ÃÂ¸ÃÂÃÂ¡ÃÂ¯ÃÂ¸ÃÂ", "Desconhecido"))



def alerta_clima_aplicacao(codigo_clima, velocidade_vento, precipitacao):

    """Retorna alerta se o clima nÃÂÃÂ£o ÃÂÃÂ© ideal para aplicaÃÂÃÂ§ÃÂÃÂ£o."""

    alertas = []

    if precipitacao > 0:

        alertas.append("ÃÂ°ÃÂ¸ÃÂÃÂ§ÃÂ¯ÃÂ¸ÃÂ Chuva detectada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ evite aplicaÃÂÃÂ§ÃÂÃÂµes!")

    if velocidade_vento > 15:

        alertas.append(f"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¨ Vento alto ({velocidade_vento:.1f} km/h) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ risco de deriva!")

    if codigo_clima in [95, 96, 99]:

        alertas.append("ÃÂ¢Ã¢ÂÂºÃÂÃÂ¯ÃÂ¸ÃÂ Trovoada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ NÃÂÃÂO faÃÂÃÂ§a aplicaÃÂÃÂ§ÃÂÃÂµes!")

    return alertas



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# PREÃÂÃ¢ÂÂ¡OS DE COMMODITIES ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ CEPEA/ESALQ via scraping

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

def buscar_dolar_awesomeapi():

    """Busca cotaÃÂÃÂ§ÃÂÃÂ£o real do dÃÂÃÂ³lar ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ tenta 4 fontes em sequÃÂÃÂªncia."""

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

        pass  # falha silenciada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o crÃÂÃÂ­tico

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

        pass  # falha silenciada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o crÃÂÃÂ­tico

    # 3. Banco Central do Brasil ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ PTAX

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

        pass  # falha silenciada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o crÃÂÃÂ­tico

    return {"preco": 5.80, "fonte": "Offline"}





def buscar_precos_cepea_ia():

    """

    Usa Claude API com web_search para buscar preÃÂÃÂ§os CEPEA em tempo real.

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

                pass  # falha silenciada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o crÃÂÃÂ­tico

        if not api_key:

            import os

            api_key = os.environ.get("ANTHROPIC_API_KEY", "")



        if not api_key or len(api_key) < 20:

            st.session_state["_cepea_erro"] = "API key nÃÂÃÂ£o encontrada ou invÃÂÃÂ¡lida"

            return None



        hoje_str = datetime.now().strftime("%d/%m/%Y")

        prompt = (

            f"Data: {hoje_str}. "

            "Pesquise o preÃÂÃÂ§o atual de commodities agrÃÂÃÂ­colas no Brasil (CEPEA/ESALQ ou mercado fÃÂÃÂ­sico). "

            "Responda APENAS com este JSON (sem texto, sem markdown, sem explicaÃÂÃÂ§ÃÂÃÂ£o):\n"

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

                    pass  # falha silenciada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o crÃÂÃÂ­tico

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

                    "cafe":    r"caf[eÃÂÃÂ©][^0-9]*(\d+[.,]\d+)",

                    "algodao": r"algod[aÃÂÃÂ£]o[^0-9]*(\d+[.,]\d+)",

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



                st.session_state["_cepea_erro"] = f"JSON nÃÂÃÂ£o encontrado: {texto[:60]}"

        else:

            st.session_state["_cepea_erro"] = f"HTTP {resp.status_code}: {resp.text[:60]}"

    except Exception as e:

        st.session_state["_cepea_erro"] = f"ExceÃÂÃÂ§ÃÂÃÂ£o: {str(e)[:80]}"

    return None





def converter_para_reais(precos_cbot, dolar):

    """Converte cotaÃÂÃÂ§ÃÂÃÂµes CBOT/ICE para R$."""

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

    Busca preÃÂÃÂ§os em tempo real:

    1. DÃÂÃÂ³lar via BCB PTAX / AwesomeAPI / ExchangeRate-API

    2. Commodities via IA + web_search CEPEA (principal ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ funciona no Streamlit Cloud)

    3. Fallback: CBOT/ICE via Stooq / Yahoo Finance

    4. Fallback final: referÃÂÃÂªncias offline

    """

    resultado = {}

    dolar_data = buscar_dolar_awesomeapi()

    resultado["dolar"] = dolar_data

    dolar_val  = dolar_data.get("preco", 5.80)



    # Verifica cache ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ sÃÂÃÂ³ chama IA se passou mais de 30 min

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

        fc = f"{dados_cepea.get('fonte','CEPEA')} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {dados_cepea.get('data','')}"

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

        "soja_sc":    {"preco":115.0, "unidade":"R$/sc 60kg","praca":"PR","fonte":f"ReferÃÂÃÂªncia {hoje}"},

        "milho_sc":   {"preco": 58.0, "unidade":"R$/sc 60kg","praca":"PR","fonte":f"ReferÃÂÃÂªncia {hoje}"},

        "trigo_sc":   {"preco": 69.0, "unidade":"R$/sc 60kg","praca":"PR","fonte":f"ReferÃÂÃÂªncia {hoje}"},

        "cafe_sc":    {"preco":2250.0,"unidade":"R$/sc 60kg","praca":"SP","fonte":f"ReferÃÂÃÂªncia {hoje}"},

        "algodao_at": {"preco":120.0, "unidade":"R$/@",      "praca":"MT","fonte":f"ReferÃÂÃÂªncia {hoje}"},

        "boi_at":     {"preco":320.0, "unidade":"R$/@",      "praca":"SP","fonte":f"ReferÃÂÃÂªncia {hoje}"},

        "arroz_sc":   {"preco": 74.0, "unidade":"R$/sc 50kg","praca":"RS","fonte":f"ReferÃÂÃÂªncia {hoje}"},

    }.items():

        resultado.setdefault(chave, fb)



    resultado["_atualizado_em"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    return resultado



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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

    """Tenta extrair valores de anÃÂÃÂ¡lise de solo do texto OCR."""

    resultado = {}

    padroes = {

        "ph":              r"pH[:\s]+([0-9]+[.,][0-9]+)",

        "fosforo":         r"(?:FÃÂÃÂ³sforo|Fosforo|P)[:\s]+([0-9]+[.,][0-9]+)",

        "potassio":        r"(?:PotÃÂÃÂ¡ssio|Potassio|K)[:\s]+([0-9]+[.,][0-9]+)",

        "calcio":          r"(?:CÃÂÃÂ¡lcio|Calcio|Ca)[:\s]+([0-9]+[.,][0-9]+)",

        "magnesio":        r"(?:MagnÃÂÃÂ©sio|Magnesio|Mg)[:\s]+([0-9]+[.,][0-9]+)",

        "aluminio":        r"(?:AlumÃÂÃÂ­nio|Aluminio|Al)[:\s]+([0-9]+[.,][0-9]+)",

        "enxofre":         r"(?:Enxofre|S)[:\s]+([0-9]+[.,][0-9]+)",

        "materia_organica":r"(?:MatÃÂÃÂ©ria OrgÃÂÃÂ¢nica|M\.O\.|MO)[:\s]+([0-9]+[.,][0-9]+)",

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





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# CORREÃÂÃ¢ÂÂ¡ÃÂÃÂO 3: funÃÂÃÂ§ÃÂÃÂµes sem duplicatas

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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

    # LÃÂÃÂª variÃÂÃÂ¡veis globais dinamicamente (podem nÃÂÃÂ£o existir quando funÃÂÃÂ§ÃÂÃÂ£o ÃÂÃÂ© definida)

    _sb_url    = st.secrets.get("SUPABASE_URL", "") if hasattr(st, 'secrets') else ""

    _sb_key    = st.secrets.get("SUPABASE_ANON_KEY", "") if hasattr(st, 'secrets') else ""

    _sb_token  = st.session_state.get("sb_token", "")

    _sb_uid    = st.session_state.get("sb_user_id", "")

    _sb_ok     = bool(_sb_url and _sb_key and _sb_token and _sb_uid and _SB_DISPONIVEL)



    if _sb_ok:

        try:

            ok = sb_salvar(_sb_url, _sb_key, _sb_token, _sb_uid, dados_salvos)

            if ok:

                st.session_state["_ultimo_save"] = f"ÃÂ¢ÃÂÃ¢ÂÂ¦ Supabase {datetime.now().strftime('%H:%M:%S')}"

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

                                st.session_state["_ultimo_save"] = f"ÃÂ¢ÃÂÃ¢ÂÂ¦ Supabase {datetime.now().strftime('%H:%M:%S')} (renovado)"

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

                st.session_state["_ultimo_save"] = f"ÃÂ¢ÃÂÃÂ {_r.status_code}: {_r.text[:50]}"

        except Exception as e:

            st.session_state["_ultimo_save"] = f"ÃÂ¢ÃÂÃÂ Erro: {str(e)[:40]}"

    else:

        motivo = []

        if not _sb_url: motivo.append("sem URL")

        if not _sb_key: motivo.append("sem KEY")

        if not _sb_token: motivo.append("sem token")

        if not _sb_uid: motivo.append("sem user_id")

        if not _SB_DISPONIVEL: motivo.append("mÃÂÃÂ³dulo nÃÂÃÂ£o carregou")

        st.session_state["_ultimo_save"] = f"ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Local ({', '.join(motivo)})"

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



# CORREÃÂÃ¢ÂÂ¡ÃÂÃÂO 2: carregar_area_por_id movida para escopo global

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

    # Tenta carregar do repositÃÂÃÂ³rio primeiro

    for caminho in [ARQUIVO_USUARIOS, str(_BASE_DIR / "usuarios.json")]:

        if os.path.exists(caminho):

            try:

                with open(caminho, "r", encoding="utf-8") as arquivo:

                    dados = json.load(arquivo)

                    if isinstance(dados, dict) and dados:

                        return dados

            except Exception:

                pass  # falha silenciada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o crÃÂÃÂ­tico

    return {}



def salvar_usuarios(usuarios):

    # Salva no repositÃÂÃÂ³rio (persistente)

    try:

        with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:

            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

    except Exception:

        pass  # falha silenciada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o crÃÂÃÂ­tico

    # Backup em /tmp tambÃÂÃÂ©m

    try:

        with open(str(_BASE_DIR / "usuarios.json"), "w", encoding="utf-8") as arquivo:

            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

    except Exception:

        pass  # falha silenciada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o crÃÂÃÂ­tico



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# SUPABASE ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ configuraÃÂÃÂ§ÃÂÃÂ£o

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

_SB_URL = st.secrets.get("SUPABASE_URL", "")

_SB_KEY = st.secrets.get("SUPABASE_ANON_KEY", "")

_SUPABASE_ATIVO = bool(_SB_URL and _SB_KEY and _SB_DISPONIVEL)



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# AUTO-LOGIN ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ restaura sessÃÂÃÂ£o via query_params

# Quando usuÃÂÃÂ¡rio recarrega a pÃÂÃÂ¡gina, o token

# salvo nos query_params restaura a sessÃÂÃÂ£o

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

def _tentar_autologin():

    """Tenta restaurar sessÃÂÃÂ£o via query_params apÃÂÃÂ³s reload."""

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

                st.session_state.usuario_atual = (_nm or "UsuÃÂÃÂ¡rio").replace("_", " ")

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



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# SESSION STATE ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ LOGIN

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if "sb_token"   not in st.session_state: st.session_state.sb_token   = ""

if "sb_user_id" not in st.session_state: st.session_state.sb_user_id = ""

if "sb_plano"   not in st.session_state: st.session_state.sb_plano   = "free"



if "usuarios" not in st.session_state:

    st.session_state.usuarios = carregar_usuarios()



if "logado" not in st.session_state:

    st.session_state.logado = False



if "usuario_atual" not in st.session_state:

    st.session_state.usuario_atual = ""



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# TELA DE LOGIN

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

def tela_login():

    """Tela de login ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ usa Supabase se disponÃÂÃÂ­vel, senÃÂÃÂ£o sistema local."""



    # Logo

    if os.path.exists("IAAgrologo.jpeg"):

        import base64 as _b64

        with open("IAAgrologo.jpeg", "rb") as _f:

            _logo_b64 = _b64.b64encode(_f.read()).decode()

        st.markdown(f"""<div style='text-align:center;padding:20px 0 10px;'>

        <img src='data:image/jpeg;base64,{_logo_b64}' style='max-height:120px;border-radius:12px;'/>

        </div>""", unsafe_allow_html=True)



    st.markdown("<h2 style='text-align:center;color:#22c55e;'>ÃÂ°ÃÂ¸ÃÂÃÂ¾ IAAGRO</h2>", unsafe_allow_html=True)

    st.markdown("<p style='text-align:center;color:#94a3b8;'>InteligÃÂÃÂªncia AgrÃÂÃÂ­cola de PrecisÃÂÃÂ£o</p>", unsafe_allow_html=True)



    if _SUPABASE_ATIVO:

        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ LOGIN VIA SUPABASE ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        aba_login, aba_cadastro, aba_recuperar = st.tabs(["ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Entrar","ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Criar Conta","ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Recuperar Senha"])



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

                        # Carrega dados do usuÃÂÃÂ¡rio do Supabase

                        dados_sb = sb_carregar(_SB_URL, _SB_KEY, res["token"], res["user_id"])

                        if dados_sb:

                            for k, v in dados_sb.items():

                                if k not in st.session_state:

                                    setattr(st.session_state, k, v)

                        # Salva refresh info nos query_params para auto-login apÃÂÃÂ³s reload

                        try:

                            import hashlib as _hl

                            _nome_url = (res["nome"] or res["email"]).replace(" ", "_")[:20]

                            # Salva token completo ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ query_params suporta strings longas

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

                        st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ Bem-vindo, {st.session_state.usuario_atual}!")

                        st.rerun()

                    else:

                        st.error(f"ÃÂ¢ÃÂÃÂ {res['erro']}")



        with aba_cadastro:

            with st.form("form_cadastro_sb", clear_on_submit=True):

                nome_c  = st.text_input("Nome completo", key="sb_nome_cad")

                email_c = st.text_input("E-mail", key="sb_email_cad")

                senha_c = st.text_input("Senha (mÃÂÃÂ­n. 6 caracteres)", type="password", key="sb_senha_cad")

                conf_c  = st.text_input("Confirmar senha", type="password", key="sb_conf_cad")

                btn_c   = st.form_submit_button("Criar Conta", use_container_width=True)

            if btn_c:

                if not nome_c or not email_c or not senha_c:

                    st.error("Preencha todos os campos.")

                elif len(senha_c) < 6:

                    st.error("Senha deve ter pelo menos 6 caracteres.")

                elif senha_c != conf_c:

                    st.error("Senhas nÃÂÃÂ£o conferem.")

                else:

                    with st.spinner("Criando conta..."):

                        res = sb_signup(_SB_URL, _SB_KEY, email_c.strip(), senha_c, nome_c.strip())

                    if res.get("id") or res.get("user"):

                        st.success("ÃÂ¢ÃÂÃ¢ÂÂ¦ Conta criada! Verifique seu e-mail e faÃÂÃÂ§a login.")

                    else:

                        st.error(f"ÃÂ¢ÃÂÃÂ {res.get('msg', res.get('error_description', 'Erro ao criar conta'))}")



        with aba_recuperar:

            st.markdown("#### ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Recuperar Senha")



            if not st.session_state.get("_recup_email"):

                with st.form("form_recup_sb", clear_on_submit=True):

                    email_r = st.text_input("E-mail cadastrado", key="sb_email_recup")

                    btn_r   = st.form_submit_button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¨ Enviar cÃÂÃÂ³digo por e-mail", use_container_width=True)

                if btn_r:

                    if not email_r:

                        st.error("Digite seu e-mail.")

                    else:

                        try:

                            import requests as _req

                            # Envia OTP numÃÂÃÂ©rico de 6 dÃÂÃÂ­gitos

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

                                st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ CÃÂÃÂ³digo enviado para **{email_r.strip()}**!")

                                st.info("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ§ Verifique seu e-mail e copie o cÃÂÃÂ³digo de 6 dÃÂÃÂ­gitos.")

                                st.rerun()

                            else:

                                st.error("ÃÂ¢ÃÂÃÂ E-mail nÃÂÃÂ£o encontrado.")

                        except Exception as e:

                            st.error(f"ÃÂ¢ÃÂÃÂ Erro: {e}")

            else:

                _email_recup = st.session_state["_recup_email"]

                st.info(f"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ§ CÃÂÃÂ³digo enviado para **{_email_recup}**")

                st.warning("ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ O e-mail enviado tem um cÃÂÃÂ³digo de 6 dÃÂÃÂ­gitos. **NÃÂÃÂ£o clique no link** ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ copie apenas o cÃÂÃÂ³digo numÃÂÃÂ©rico.")



                with st.form("form_otp_sb", clear_on_submit=False):

                    otp_code   = st.text_input("CÃÂÃÂ³digo de 6 dÃÂÃÂ­gitos do e-mail", key="sb_otp_code",

                                               placeholder="123456", max_chars=6)

                    nova_senha = st.text_input("Nova senha (mÃÂÃÂ­n. 6 caracteres)", type="password", key="sb_nova_senha")

                    conf_nova  = st.text_input("Confirmar nova senha", type="password", key="sb_conf_nova")

                    btn_otp    = st.form_submit_button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Redefinir Senha", use_container_width=True)



                if btn_otp:

                    if not otp_code or len(otp_code.strip()) < 6:

                        st.error("Digite o cÃÂÃÂ³digo de 6 dÃÂÃÂ­gitos.")

                    elif len(nova_senha) < 6:

                        st.error("Senha deve ter pelo menos 6 caracteres.")

                    elif nova_senha != conf_nova:

                        st.error("Senhas nÃÂÃÂ£o conferem.")

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

                                # Tenta tambÃÂÃÂ©m com type "email"

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

                                    st.success("ÃÂ¢ÃÂÃ¢ÂÂ¦ Senha redefinida! FaÃÂÃÂ§a login com a nova senha.")

                                    st.balloons()

                                else:

                                    st.error(f"ÃÂ¢ÃÂÃÂ Erro ao atualizar senha: {r2.text[:80]}")

                            else:

                                st.error(f"ÃÂ¢ÃÂÃÂ CÃÂÃÂ³digo invÃÂÃÂ¡lido ou expirado. Tente solicitar um novo cÃÂÃÂ³digo.")

                        except Exception as e:

                            st.error(f"ÃÂ¢ÃÂÃÂ Erro: {e}")



                if st.button("ÃÂ¢Ã¢ÂÂ ÃÂ©ÃÂ¯ÃÂ¸ÃÂ Solicitar novo cÃÂÃÂ³digo", key="btn_recup_voltar"):

                    st.session_state.pop("_recup_email", None)

                    st.rerun()



        st.markdown("---")

        st.caption("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Dados protegidos por Supabase | Cada usuÃÂÃÂ¡rio tem seus prÃÂÃÂ³prios dados")



    else:

        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ LOGIN LOCAL (fallback sem Supabase) ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        aba_login, aba_cadastro, aba_recuperar = st.tabs(["ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Entrar","ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Criar Conta","ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Recuperar Senha"])



        with aba_login:

            with st.form("form_login", clear_on_submit=False):

                usuario = st.text_input("UsuÃÂÃÂ¡rio", key="login_usuario")

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

                    st.error("UsuÃÂÃÂ¡rio ou senha incorretos.")



        with aba_cadastro:

            novo_nome       = st.text_input("Nome completo",       key="cad_nome")

            novo_email      = st.text_input("Email de recuperaÃÂÃÂ§ÃÂÃÂ£o", key="cad_email")

            novo_usuario    = st.text_input("Criar usuÃÂÃÂ¡rio",        key="cad_usuario")

            nova_senha      = st.text_input("Criar senha",          type="password", key="cad_senha")

            confirmar_senha = st.text_input("Confirmar senha",      type="password", key="cad_confirmar")

            if st.button("Cadastrar", use_container_width=True, key="btn_cadastrar"):

                if not novo_nome.strip():

                    st.error("Digite seu nome.")

                elif not novo_email.strip() or "@" not in novo_email:

                    st.error("Digite um email vÃÂÃÂ¡lido.")

                elif not novo_usuario.strip():

                    st.error("Digite um usuÃÂÃÂ¡rio.")

                elif len(nova_senha) < 6:

                    st.error("Senha deve ter pelo menos 6 caracteres.")

                elif nova_senha != confirmar_senha:

                    st.error("As senhas nÃÂÃÂ£o conferem.")

                elif novo_usuario in st.session_state.usuarios:

                    st.error("Esse usuÃÂÃÂ¡rio jÃÂÃÂ¡ existe.")

                else:

                    st.session_state.usuarios[novo_usuario] = {

                        "nome":  novo_nome,

                        "email": novo_email,

                        "senha": hash_senha(nova_senha)

                    }

                    salvar_usuarios(st.session_state.usuarios)

                    st.success("ÃÂ¢ÃÂÃ¢ÂÂ¦ Conta criada! FaÃÂÃÂ§a login na aba Entrar.")



        with aba_recuperar:

            st.info("Sistema local ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ recuperaÃÂÃÂ§ÃÂÃÂ£o de senha nÃÂÃÂ£o disponÃÂÃÂ­vel sem e-mail configurado.")



        st.caption("ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Modo local ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ dados compartilhados. Configure Supabase para multi-usuÃÂÃÂ¡rio.")





if not st.session_state.logado:

    # Verifica se havia uma sessÃÂÃÂ£o anterior (usuÃÂÃÂ¡rio recarregou a pÃÂÃÂ¡gina)

    if st.session_state.get("usuario_atual"):

        st.warning("ÃÂ¢ÃÂÃÂ³ Sua sessÃÂÃÂ£o expirou. FaÃÂÃÂ§a login novamente ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ seus dados estÃÂÃÂ£o salvos no servidor.")

    tela_login()

    st.stop()



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# SPLASH SCREEN (apenas 1x por sessÃÂÃÂ£o)

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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

            <p style="color:#93c5fd;font-size:1rem;">Sistema de gestÃÂÃÂ£o agrÃÂÃÂ­cola inteligente</p>

        </div>""", unsafe_allow_html=True)

        _tx.sleep(1.2)

    _ph.empty()

    st.session_state.app_loaded = True



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# BARRA LATERAL

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

st.sidebar.markdown(

    f'<div style="background:#1a4a73;color:#ffffff;padding:10px 14px;border-radius:8px;'

    f'font-weight:700;font-size:14px;margin-bottom:8px;">ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¤ {st.session_state.usuario_atual}</div>',

    unsafe_allow_html=True

)



# Badge do plano no sidebar

_plano_atual = st.session_state.get("sb_plano", "free")

PLANOS = {

    "free": {

        "nome":    "ÃÂ°ÃÂ¸Ã¢ÂÂ Ã¢ÂÂ Free",

        "preco":   0,

        "areas":   2,

        "estoque": 20,

        "cor":     "#78350f",

        "borda":   "#f59e0b",

        "recursos": [

            "2 ÃÂÃÂ¡reas cadastradas",

            "20 itens de estoque",

            "AnÃÂÃÂ¡lise de solo bÃÂÃÂ¡sica",

            "CalendÃÂÃÂ¡rio agrÃÂÃÂ­cola",

            "PreÃÂÃÂ§os offline",

        ],

        "bloqueados": [

            "RelatÃÂÃÂ³rio PDF",

            "ImportaÃÂÃÂ§ÃÂÃÂ£o NF-e XML",

            "PreÃÂÃÂ§os CEPEA tempo real",

            "Mapa de Colheita IA",

            "IR Rural",

            "Safrinha",

        ]

    },

    "pro": {

        "nome":    "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ½ Pro",

        "preco":   49.90,

        "areas":   10,

        "estoque": 100,

        "cor":     "#1e3a5f",

        "borda":   "#3b82f6",

        "recursos": [

            "10 ÃÂÃÂ¡reas cadastradas",

            "100 itens de estoque",

            "DiagnÃÂÃÂ³stico completo EMBRAPA",

            "RelatÃÂÃÂ³rio PDF premium",

            "ImportaÃÂÃÂ§ÃÂÃÂ£o NF-e XML",

            "PreÃÂÃÂ§os CEPEA tempo real",

            "Safrinha",

            "IR Rural automatizado",

            "ReceituÃÂÃÂ¡rio AgronÃÂÃÂ´mico",

            "Suporte via WhatsApp",

        ],

        "bloqueados": [

            "ÃÂÃÂreas ilimitadas",

            "Estoque ilimitado",

            "Mapa de Colheita IA avanÃÂÃÂ§ado",

            "API de integraÃÂÃÂ§ÃÂÃÂ£o",

            "Multi-usuÃÂÃÂ¡rio",

        ]

    },

    "premium": {

        "nome":    "ÃÂ°ÃÂ¸ÃÂ¡Ã¢ÂÂ¬ Premium",

        "preco":   119.90,

        "areas":   -1,   # ilimitado

        "estoque": -1,   # ilimitado

        "cor":     "#14532d",

        "borda":   "#22c55e",

        "recursos": [

            "ÃÂÃÂreas ILIMITADAS",

            "Estoque ILIMITADO",

            "Tudo do Plano Pro",

            "Mapa de Colheita IA avanÃÂÃÂ§ado",

            "RelatÃÂÃÂ³rios agrupados",

            "API de integraÃÂÃÂ§ÃÂÃÂ£o",

            "Suporte prioritÃÂÃÂ¡rio 24h",

            "Treinamento online",

            "White-label disponÃÂÃÂ­vel",

        ],

        "bloqueados": []

    },

}



WPP_NUMERO  = "5549998159224"  # ÃÂ¢Ã¢ÂÂ ÃÂ coloque seu WhatsApp aqui

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



# Status do ÃÂÃÂºltimo salvamento (debug)

if st.session_state.get("_ultimo_save"):

    _cor_s = "#14532d" if "ÃÂ¢ÃÂÃ¢ÂÂ¦" in st.session_state["_ultimo_save"] else "#7f1d1d"

    st.sidebar.markdown(

        f"<div style='background:{_cor_s};color:#fff;padding:3px 8px;"

        f"border-radius:4px;font-size:10px;margin-top:2px;'>"

        f"{st.session_state['_ultimo_save']}</div>",

        unsafe_allow_html=True

    )





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# SESSION STATE ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ DADOS

# Carrega do Supabase se tem token, senÃÂÃÂ£o arquivo local

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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

        pass  # falha silenciada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ usa arquivo local



dados_carregados = {}



# Se autologin funcionou, dados jÃÂÃÂ¡ estÃÂÃÂ£o no session_state ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o sobrescreve

# Se nÃÂÃÂ£o, tenta Supabase com token existente, senÃÂÃÂ£o arquivo local

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



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Mapa de Colheita IA ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ inicializaÃÂÃÂ§ÃÂÃÂ£o global ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ GPS session_states ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ inicializaÃÂÃÂ§ÃÂÃÂ£o segura ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if "_gps_lat"       not in st.session_state: st.session_state._gps_lat       = None

if "_gps_lon"       not in st.session_state: st.session_state._gps_lon       = None

if "_gps_mf_lat"    not in st.session_state: st.session_state._gps_mf_lat    = None

if "_gps_mf_lon"    not in st.session_state: st.session_state._gps_mf_lon    = None

if "_gps_clima_lat" not in st.session_state: st.session_state._gps_clima_lat = None

if "_gps_clima_lon" not in st.session_state: st.session_state._gps_clima_lon = None

if "filtro_out"     not in st.session_state: st.session_state.filtro_out     = []



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬



# BANCO DE PRODUTOS AGRÃÂÃÂCOLAS ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Autocomplete

# Fontes: BASF, Syngenta, Bayer, UPL, MAPA/AGROFIT

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

CATALOGO_PRODUTOS = [

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"2,4-D Amina 806","fab":"Outros","cat":"Herbicida","ia":"2,4-D Amina"},

    {"nome":"2,4-D ÃÂÃ¢ÂÂ°ster 670","fab":"Outros","cat":"Herbicida","ia":"2,4-D ÃÂÃ¢ÂÂ°ster"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Abacus HC","fab":"BASF","cat":"Fungicida","ia":"Epoxiconazol + Piraclostrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Abamectina 18 EC","fab":"Outros","cat":"Inseticida","ia":"Abamectina"},

    {"nome":"Abamectina 36 EC","fab":"Outros","cat":"Acaricida","ia":"Abamectina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Abamex 18 EC","fab":"ADAMA","cat":"Inseticida","ia":"Abamectina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Acabus","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Acaristop 500 SC","fab":"Ouro Fino","cat":"Acaricida","ia":"Clofentezina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Accent 750 WG","fab":"BASF","cat":"Herbicida","ia":"Nicossulfurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Accent Gold","fab":"Bayer","cat":"Herbicida","ia":"Nicossulfurom + Rimsulfurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Acefato 750 WP","fab":"ADAMA","cat":"Inseticida","ia":"Acefato"},

    {"nome":"Acetamiprido 200 SP","fab":"ADAMA","cat":"Inseticida","ia":"Acetamiprido"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Acimanto SC","fab":"Ihara","cat":"Inseticida","ia":"Acefato"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Acramite 50 WS","fab":"Outros","cat":"Acaricida","ia":"Bifenazate"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Acrobat MZ","fab":"BASF","cat":"Fungicida","ia":"Dimetomorfe + Mancozebe"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Actara 250 WG","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam"},

    {"nome":"Actellic 500 EC","fab":"Syngenta","cat":"Inseticida","ia":"PirimifÃÂÃÂ³s-MetÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Actigen","fab":"Ouro Fino","cat":"Fungicida BiolÃÂÃÂ³gico","ia":"Bacillus amyloliquefaciens"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Actyon 100 EC","fab":"Ihara","cat":"Inseticida","ia":"Bifentrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Adengo","fab":"Bayer","cat":"Herbicida","ia":"Isoxaflutol + Tiencarbazona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Afalon 450 SC","fab":"ADAMA","cat":"Herbicida","ia":"Linurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Agree WP","fab":"Outros","cat":"Inseticida BiolÃÂÃÂ³gico","ia":"Bacillus thuringiensis"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Alade","fab":"Syngenta","cat":"Fungicida","ia":"Solatenol + Ciproconazol + Difenoconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ally","fab":"ADAMA","cat":"Herbicida","ia":"Metsulfurom-MetÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Alto 100 SL","fab":"Ihara","cat":"Fungicida","ia":"Ciproconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Amistar 500 WG","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina"},

    {"nome":"Amistar Top","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Difenoconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Amplexus","fab":"BASF","cat":"Herbicida","ia":"Flumioxazina + Lactofen"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ampligo 150 ZC","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole + Lambda-Cialotrina"},

    {"nome":"Ampligo Pro","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole + Clorfenapir"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Amplo","fab":"BASF","cat":"Herbicida","ia":"Imazapique + Imazapir"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Apollo 500 SC","fab":"Outros","cat":"Acaricida","ia":"Clofentezina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Aproach 500 SC","fab":"Corteva","cat":"Fungicida","ia":"Picoxistrobina"},

    {"nome":"Aproach Prima","fab":"Corteva","cat":"Fungicida","ia":"Picoxistrobina + Ciproconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Artea 330 EC","fab":"Ihara","cat":"Fungicida","ia":"Propiconazol + Ciproconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Arylex Active","fab":"Corteva","cat":"Herbicida","ia":"Halauxifem-metÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ascope","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Asgard BR","fab":"Corteva","cat":"Herbicida","ia":"Sulfentrazona + Clomazona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MOSAIC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Aspire","fab":"Mosaic","cat":"Fertilizante","ia":"KCl + B granulado"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Assist","fab":"Outros","cat":"Adjuvante","ia":"ÃÂÃ¢ÂÂleo Mineral"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MOSAIC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Athos","fab":"Mosaic","cat":"Fertilizante","ia":"Sulfato de amÃÂÃÂ´nio premium"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ativo TS","fab":"BASF","cat":"Tratamento de Sementes","ia":"Fludioxonil + Metalaxil-M + Tiametoxam"},

    {"nome":"Ativum","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Fluxapiroxade"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Atrazina 500 SC","fab":"Outros","cat":"Herbicida","ia":"Atrazina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Aura 200","fab":"BASF","cat":"Herbicida","ia":"Quizalofope-P-etÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Aureo","fab":"Bayer","cat":"Adjuvante","ia":"ÃÂÃ¢ÂÂleo de Soja"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Aurora 400 EC","fab":"ADAMA","cat":"Herbicida","ia":"Carfentrazona-etÃÂÃÂ­lica"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Authority 700 WDG","fab":"FMC","cat":"Herbicida","ia":"Sulfentrazona"},

    {"nome":"Authority Assist","fab":"FMC","cat":"Herbicida","ia":"Sulfentrazona + Imazaquim"},

    {"nome":"Authority First","fab":"FMC","cat":"Herbicida","ia":"Sulfentrazona + Cloransulam"},

    {"nome":"Authority MTZ","fab":"FMC","cat":"Herbicida","ia":"Sulfentrazona + Metribuzim"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Avaunt 150 SC","fab":"Corteva","cat":"Inseticida","ia":"Indoxacarbe"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Avicta 500 FS","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Abamectina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Axalion","fab":"BASF","cat":"Inseticida","ia":"Afidopiropeno"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Axial","fab":"Syngenta","cat":"Herbicida","ia":"Pinoxaden"},

    {"nome":"Axial One","fab":"Syngenta","cat":"Herbicida","ia":"Pinoxaden + Clodinafope-propargil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Azimut 250 SC","fab":"ADAMA","cat":"Fungicida","ia":"Azoxistrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Azimut OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Azoxistrobina 250 SC","fab":"Outros","cat":"Fungicida","ia":"Azoxistrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Azoxy OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Propiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Banvel","fab":"Bayer","cat":"Herbicida","ia":"Dicamba"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Basagran 480","fab":"BASF","cat":"Herbicida","ia":"Bentazona"},

    {"nome":"Basagran 600","fab":"BASF","cat":"Herbicida","ia":"Bentazona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Bayfidan 250 EC","fab":"Bayer","cat":"Fungicida","ia":"Triadimenol"},

    {"nome":"Bayfolan Boro","fab":"Bayer","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"B + aminoÃÂÃÂ¡cidos"},

    {"nome":"Bayfolan Cobre","fab":"Bayer","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"Cu + aminoÃÂÃÂ¡cidos"},

    {"nome":"Bayfolan Forte","fab":"Bayer","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"NPK + micronutrientes + aminoÃÂÃÂ¡cidos"},

    {"nome":"Bayfolan NK","fab":"Bayer","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"N + K + aminoÃÂÃÂ¡cidos"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Baytan 150 FS","fab":"BASF","cat":"Tratamento de Sementes","ia":"Triadimenol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Belt 480 SC","fab":"Bayer","cat":"Inseticida","ia":"Flubendiamida"},

    {"nome":"Belt Expert","fab":"Bayer","cat":"Inseticida","ia":"Flubendiamida + Spirotetramat"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Belyan","fab":"BASF","cat":"Fungicida","ia":"Mefentrifluconazol + Piraclostrobina + Fluxapiroxade"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Bendazol 500 SC","fab":"UPL","cat":"Fungicida","ia":"Carbendazim"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Benevia OD","fab":"Corteva","cat":"Inseticida","ia":"Ciantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Bentazona 600 SL","fab":"Outros","cat":"Herbicida","ia":"Bentazona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Benza 500 SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Carbendazim"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Bifentrina 100 EC","fab":"Outros","cat":"Inseticida","ia":"Bifentrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Biozyme","fab":"UPL","cat":"Bioestimulante","ia":"AminoÃÂÃÂ¡cidos + Extrato de algas"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Blavity","fab":"BASF","cat":"Fungicida","ia":"Fluxapiroxade + Protioconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Bold 750 WG","fab":"Bayer","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Boral 500 SC","fab":"Corteva","cat":"Herbicida","ia":"Sulfentrazona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Boro Max 10%","fab":"Outros","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"Boro"},

    {"nome":"Bovemax SC","fab":"Outros","cat":"Inseticida BiolÃÂÃÂ³gico","ia":"Beauveria bassiana"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Boveril WP","fab":"Ihara","cat":"Inseticida BiolÃÂÃÂ³gico","ia":"Beauveria bassiana"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Bravonil 500 SC","fab":"Syngenta","cat":"Fungicida","ia":"Clorotalonil"},

    {"nome":"Bravonil Top","fab":"Syngenta","cat":"Fungicida","ia":"Clorotalonil + Ciproconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Bravonil Ultrex","fab":"ADAMA","cat":"Fungicida","ia":"Clorotalonil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Break Thru S 240","fab":"Outros","cat":"Adjuvante","ia":"Silicone"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Brigade 100 EC","fab":"FMC","cat":"Inseticida","ia":"Bifentrina"},

    {"nome":"Brigade 400 SC","fab":"FMC","cat":"Inseticida","ia":"Bifentrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Bright","fab":"BASF","cat":"Inseticida","ia":"Ciantraniliprole + Tiametoxam"},

    {"nome":"Brio","fab":"BASF","cat":"Fungicida","ia":"Trifloxistrobina + Propiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Bulldock 125 SC","fab":"Bayer","cat":"Inseticida","ia":"Beta-Ciflutrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"BÃÂÃÂ³rax","fab":"Outros","cat":"Fertilizante","ia":"B 11%"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cabrio Top","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Metiram"},

    {"nome":"Caipora","fab":"BASF","cat":"Tratamento de Sementes","ia":"Piraclostrobina + Tiofanato + Fipronil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Calaris Milho","fab":"Syngenta","cat":"Herbicida","ia":"Tembotriona + Atrazina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"CalcÃÂÃÂ¡rio CalcÃÂÃÂ­tico","fab":"Outros","cat":"Fertilizante","ia":"CaCO3"},

    {"nome":"CalcÃÂÃÂ¡rio DolomÃÂÃÂ­tico","fab":"Outros","cat":"Fertilizante","ia":"CaCO3 + MgCO3"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Calipen SC","fab":"Syngenta","cat":"Herbicida","ia":"Cloransulam-metÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Callisto","fab":"Corteva","cat":"Herbicida","ia":"Mesotriona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cantus","fab":"BASF","cat":"Fungicida","ia":"Boscalida"},

    {"nome":"Caramba 90","fab":"BASF","cat":"Fungicida","ia":"Metconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Carbendazim 500 SC","fab":"Outros","cat":"Fungicida","ia":"Carbendazim"},

    {"nome":"Carbofuran 350 SC","fab":"Outros","cat":"Nematicida","ia":"Carbofurano"},

    {"nome":"Carrier 170 EC","fab":"Outros","cat":"Adjuvante","ia":"ÃÂÃ¢ÂÂleo Mineral"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Celeiro","fab":"Bayer","cat":"Fungicida","ia":"Tebuconazol + Trifloxistrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cercobin 700 WP","fab":"ADAMA","cat":"Fungicida","ia":"Tiofanato MetÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cerconil WP","fab":"UPL","cat":"Fungicida","ia":"Clorotalonil + Tiofanato"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cereus 72 SC","fab":"Outros","cat":"Regulador de Crescimento","ia":"Trinexapaque-etÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Certano","fab":"Syngenta","cat":"Inseticida BiolÃÂÃÂ³gico","ia":"Beauveria bassiana"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Certero 480 SC","fab":"Bayer","cat":"Inseticida","ia":"Triflumurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cipermetrina 250 EC","fab":"ADAMA","cat":"Inseticida","ia":"Cipermetrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cipro 250 SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Ciproconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Citromax Cal-Boro","fab":"Outros","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"CÃÂÃÂ¡lcio + Boro"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Clariva Complete B","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Pasteuria nishizawae + Tiametoxam"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Clethodim 240 EC","fab":"ADAMA","cat":"Herbicida","ia":"Cletodim"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cletodim 240 EC","fab":"Outros","cat":"Herbicida","ia":"Cletodim"},

    {"nome":"Clodinafope 240 EC","fab":"Outros","cat":"Herbicida","ia":"Clodinafope-propargil"},

    {"nome":"Clomazona 500 EC","fab":"Outros","cat":"Herbicida","ia":"Clomazona"},

    {"nome":"Clorantraniliprole 200 SC","fab":"Outros","cat":"Inseticida","ia":"Clorantraniliprole"},

    {"nome":"Cloreto de PotÃÂÃÂ¡ssio","fab":"Outros","cat":"Fertilizante","ia":"KCl 00-00-60"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MOSAIC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cloreto de PotÃÂÃÂ¡ssio Mosaic","fab":"Mosaic","cat":"Fertilizante","ia":"KCl 00-00-60"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Clorotalonil 720 SC","fab":"Outros","cat":"Fungicida","ia":"Clorotalonil"},

    {"nome":"ClorpirifÃÂÃÂ³s 480 EC","fab":"Outros","cat":"Inseticida","ia":"ClorpirifÃÂÃÂ³s"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Closer SC","fab":"Corteva","cat":"Inseticida","ia":"Sulfoxaflor"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Clout 100 CS","fab":"Ihara","cat":"Inseticida","ia":"Lambda-Cialotrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cobra","fab":"Outros","cat":"Herbicida","ia":"Lactofen"},

    {"nome":"Cobre Foliar 5%","fab":"Outros","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"Cobre"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cobre Sandoz","fab":"BASF","cat":"Fungicida","ia":"Oxicloreto de Cobre"},

    {"nome":"Collis","fab":"BASF","cat":"Fungicida","ia":"Boscalida + Cresoxim-metÃÂÃÂ­lico"},

    {"nome":"Comet 200 EC","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Confidor 700 WG","fab":"Bayer","cat":"Inseticida","ia":"Imidaclopride"},

    {"nome":"Confidor Oil","fab":"Bayer","cat":"Inseticida","ia":"Imidaclopride + ÃÂÃ¢ÂÂleo mineral"},

    {"nome":"Connect","fab":"Bayer","cat":"Inseticida","ia":"Imidaclopride + Beta-Ciflutrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Constel","fab":"UPL","cat":"Inseticida","ia":"Clorantraniliprole + Metoxifenozida"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Convintro Duo","fab":"Bayer","cat":"Herbicida","ia":"Halauxifem-metÃÂÃÂ­lico + Fluroxipir"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Coragen 200 SC","fab":"Corteva","cat":"Inseticida","ia":"Clorantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Coragen FMC","fab":"FMC","cat":"Inseticida","ia":"Clorantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TIMAC AGRO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Corona","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"N + B + Mo + aminoÃÂÃÂ¡cidos"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cossack OD","fab":"UPL","cat":"Herbicida","ia":"Mesossulfurom + Iodossulfurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cripton Xpro","fab":"Bayer","cat":"Fungicida","ia":"Bixafem + Protioconazol + Trifloxistrobina"},

    {"nome":"Cropstar 600 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Imidaclopride + Tiodicarbe"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Crosstin","fab":"UPL","cat":"Herbicida","ia":"Hexazinona + Diurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cruiser 350 FS","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Tiametoxam"},

    {"nome":"Cruiser Opti","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Tiametoxam + Fludioxonil + Mefenoxam"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cuprozeb","fab":"ADAMA","cat":"Fungicida","ia":"Cobre + Mancozebe"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Curbix","fab":"Bayer","cat":"Inseticida","ia":"Flupyrimin"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Curyom 550 EC","fab":"Syngenta","cat":"Inseticida","ia":"ProfenofÃÂÃÂ³s + Cipermetrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cyazypyr 100 OD","fab":"Corteva","cat":"Inseticida","ia":"Ciantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cyazypyr FMC","fab":"FMC","cat":"Inseticida","ia":"Ciantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cypress","fab":"Syngenta","cat":"Fungicida","ia":"Difenoconazol + Propiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Cypress Ihara","fab":"Ihara","cat":"Fungicida","ia":"Difenoconazol + Propiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"CÃÂÃÂ¡lcio King 12%","fab":"Outros","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"CÃÂÃÂ¡lcio"},

    {"nome":"DAP 18-46-00","fab":"Outros","cat":"Fertilizante","ia":"DiamÃÂÃÂ´nio fosfato"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MOSAIC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"DAP Mosaic","fab":"Mosaic","cat":"Fertilizante","ia":"DiamÃÂÃÂ´nio fosfato 18-46-00"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Dash HC","fab":"Outros","cat":"Adjuvante","ia":"ÃÂÃ¢ÂÂ°ster MetÃÂÃÂ­lico de ÃÂÃ¢ÂÂleos"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Debussy SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Propiconazol + Difenoconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Decis 25 EC","fab":"Bayer","cat":"Inseticida","ia":"Deltametrina"},

    {"nome":"Decis Protech","fab":"Bayer","cat":"Inseticida","ia":"Deltametrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Delan","fab":"BASF","cat":"Fungicida","ia":"Ditianonom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Deltametrina 25 EC","fab":"ADAMA","cat":"Inseticida","ia":"Deltametrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Dermacor X-100","fab":"Corteva","cat":"Tratamento de Sementes","ia":"Clorantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Derosal Plus TS","fab":"BASF","cat":"Tratamento de Sementes","ia":"Carbendazim + Tiram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Diamond 50 EC","fab":"FMC","cat":"Inseticida","ia":"Novalurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Diclosulam 840 WG","fab":"ADAMA","cat":"Herbicida","ia":"Diclosulam"},

    {"nome":"Difenoconazol 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Difenoconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Dimilin 250 WP","fab":"Corteva","cat":"Inseticida","ia":"Diflubenzurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Dipel WP","fab":"Outros","cat":"Inseticida BiolÃÂÃÂ³gico","ia":"Bacillus thuringiensis"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"DMA 806 BR","fab":"Corteva","cat":"Herbicida","ia":"2,4-D Amina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Domark 100 EC","fab":"UPL","cat":"Fungicida","ia":"Tetraconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Dual Gold 960 EC","fab":"Syngenta","cat":"Herbicida","ia":"S-Metolacloro"},

    {"nome":"Durivo","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Clorantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ecconik","fab":"UPL","cat":"Herbicida","ia":"Isoxaflutol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ecoss WP","fab":"Outros","cat":"Fungicida BiolÃÂÃÂ³gico","ia":"Bacillus subtilis"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Eddus","fab":"Syngenta","cat":"Herbicida","ia":"Flumioxazina"},

    {"nome":"Elatus","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Benzovindiflupir"},

    {"nome":"Elatus Ace","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Benzovindiflupir + Propiconazol"},

    {"nome":"Elatus Plus","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Benzovindiflupir + Difenoconazol"},

    {"nome":"Elestal Neo","fab":"Syngenta","cat":"Inseticida","ia":"Sulfoxaflor"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Emamectina 50 WG","fab":"Outros","cat":"Inseticida","ia":"Benzoato de Emamectina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Eminent 125 EW","fab":"ADAMA","cat":"Fungicida","ia":"Tetraconazol"},

    {"nome":"Eminent Star","fab":"ADAMA","cat":"Fungicida","ia":"Tetraconazol + Fludioxonil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Engeo Pleno S","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Lambda-Cialotrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Enlist Duo","fab":"Corteva","cat":"Herbicida","ia":"2,4-D + Glifosato"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Envidor 240 SC","fab":"Outros","cat":"Acaricida","ia":"Espirodiclofeno"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Epivio Sky","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Fluopyram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Epoxiconazol 75 SC","fab":"Outros","cat":"Fungicida","ia":"Epoxiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"EsfÃÂÃÂ©rica Duo","fab":"ADAMA","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Espinosade 480 SC","fab":"Outros","cat":"Inseticida","ia":"Espinosade"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Estoril OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ethrel 720 SL","fab":"Outros","cat":"Regulador de Crescimento","ia":"Etefom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Evidence 200 EC","fab":"Bayer","cat":"Fungicida","ia":"Iprodiona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Evolution","fab":"UPL","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Exalt 600 SC","fab":"FMC","cat":"Inseticida","ia":"Espinetoram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MOSAIC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Excellen","fab":"Mosaic","cat":"Fertilizante","ia":"N com inibidor de nitrificaÃÂÃÂ§ÃÂÃÂ£o"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Exirel 100 SE","fab":"Corteva","cat":"Inseticida","ia":"Ciantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Extravon","fab":"Outros","cat":"Adjuvante","ia":"Alquil-polioxietileno"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fastac 100 CE","fab":"BASF","cat":"Inseticida","ia":"Alfa-Cipermetrina"},

    {"nome":"Fastac 50 EC","fab":"BASF","cat":"Inseticida","ia":"Alfa-Cipermetrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fastmite","fab":"UPL","cat":"Inseticida","ia":"Abamectina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fegatex","fab":"BASF","cat":"Inseticida","ia":"Acefato"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fernok","fab":"UPL","cat":"Herbicida","ia":"Fenoxaprop + Mefenpir"},

    {"nome":"Feroce","fab":"UPL","cat":"Inseticida","ia":"Lambda-Cialotrina + Tiametoxam"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ferrari","fab":"Ouro Fino","cat":"Fungicida","ia":"Piraclostrobina + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ferro Quelatado 6%","fab":"Outros","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"Ferro EDTA"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TIMAC AGRO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fertiactyl Cana","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"N + K + S"},

    {"nome":"Fertiactyl GramÃÂÃÂ­neas","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"N + S + Zn"},

    {"nome":"Fertiactyl GZ","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"N + P + K + aminoÃÂÃÂ¡cidos + algas"},

    {"nome":"Fertiactyl Kalibor","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"K + B"},

    {"nome":"Fertiactyl Leguminosas","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"N + P + K + Mo + Co"},

    {"nome":"Fertiactyl Leguminosas NG","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"N + P + K + Mo + Co + aminoÃÂÃÂ¡cidos"},

    {"nome":"Fertileader Alpha","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"Seactiv + N + Zn"},

    {"nome":"Fertileader Cana","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"Seactiv + N + K"},

    {"nome":"Fertileader Grena","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"Seactiv + K + Ca + B"},

    {"nome":"Fertileader Maiz","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"Seactiv + N + P + Zn"},

    {"nome":"Fertileader QualitÃÂÃÂ©","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"Seactiv + P + K + S"},

    {"nome":"Fertileader Vital","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"Seactiv + NPK"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fetrilon Combi","fab":"Outros","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"Multi-micronutrientes"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Finale","fab":"BASF","cat":"Herbicida","ia":"Glufosinato de AmÃÂÃÂ´nio"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fipronil 800 WG","fab":"Outros","cat":"Inseticida","ia":"Fipronil"},

    {"nome":"Floramite 240 SC","fab":"Outros","cat":"Acaricida","ia":"Bifenazate"},

    {"nome":"Fluazifope 250 EC","fab":"Outros","cat":"Herbicida","ia":"Fluazifope-P-butÃÂÃÂ­lico"},

    {"nome":"Flumioxazina 500 SC","fab":"Outros","cat":"Herbicida","ia":"Flumioxazina"},

    {"nome":"Fluxapiroxade 500 SC","fab":"Outros","cat":"Fungicida","ia":"Fluxapiroxade"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Folicur 200 EC","fab":"Bayer","cat":"Fungicida","ia":"Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Foltron Plus","fab":"UPL","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"NitrogÃÂÃÂªnio + Boro + MolibdÃÂÃÂªnio"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fontelis 200 SC","fab":"Corteva","cat":"Fungicida","ia":"Penthiopirad"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fortenza 600 FS","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Afidopiropeno"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fortenza Duo","fab":"BASF","cat":"Tratamento de Sementes","ia":"Afidopiropeno + Sedaxane"},

    {"nome":"Forum","fab":"BASF","cat":"Fungicida","ia":"Dimetomorfe"},

    {"nome":"Forum Plus","fab":"BASF","cat":"Fungicida","ia":"Dimetomorfe + Folpete"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fosfato Reativo","fab":"Outros","cat":"Fertilizante","ia":"Fosfato natural reativo"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fox OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fox Ultra","fab":"Bayer","cat":"Fungicida","ia":"Protioconazol + Impirfluxam + Trifloxistrobina"},

    {"nome":"Fox Xpro","fab":"Bayer","cat":"Fungicida","ia":"Bixafem + Tebuconazol + Trifloxistrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fritas FTE BR-12","fab":"Outros","cat":"Fertilizante","ia":"Multi-micronutrientes fritados"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Frondeo Cana","fab":"Syngenta","cat":"Inseticida","ia":"Plinazolina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fury 200 EW","fab":"UPL","cat":"Inseticida","ia":"Zeta-Cipermetrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Fusilade 250 EW","fab":"ADAMA","cat":"Herbicida","ia":"Fluazifope-P-butÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"FusiÃÂÃÂ³n SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Ciproconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Galil SC","fab":"Bayer","cat":"Fungicida","ia":"Iprodiona + Tiofanato MetÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Galvian 500 WG","fab":"UPL","cat":"Inseticida","ia":"Acefato"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Gamit 360 CS","fab":"BASF","cat":"Herbicida","ia":"Clomazona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Gamit Star","fab":"FMC","cat":"Herbicida","ia":"Clomazona + Pendimetalina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Gamit UPL","fab":"UPL","cat":"Herbicida","ia":"Clomazona 360 CS"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Gaucho 350 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Imidaclopride"},

    {"nome":"Gaucho 600 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Imidaclopride"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Gesagard 500 SC","fab":"Syngenta","cat":"Herbicida","ia":"Prometrina"},

    {"nome":"Gesaprim 500 SC","fab":"Syngenta","cat":"Herbicida","ia":"Atrazina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Gesso AgrÃÂÃÂ­cola","fab":"Outros","cat":"Fertilizante","ia":"CaSO4"},

    {"nome":"Gibb 10 Plus","fab":"Outros","cat":"Regulador de Crescimento","ia":"ÃÂÃÂcido GiberÃÂÃÂ©lico"},

    {"nome":"Glifosato CS 480","fab":"Outros","cat":"Herbicida","ia":"Glifosato"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Gramoxone 200","fab":"Syngenta","cat":"Herbicida","ia":"Paraquat"},

    {"nome":"Grower","fab":"Syngenta","cat":"Herbicida","ia":"Nicossulfurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Halosulfurom 750 WG","fab":"Outros","cat":"Herbicida","ia":"Halosulfurom-metÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Harness 25 EC","fab":"Syngenta","cat":"Herbicida","ia":"Acetocloro"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Harpoon WP","fab":"Outros","cat":"Fungicida BiolÃÂÃÂ³gico","ia":"Trichoderma asperellum"},

    {"nome":"Hasten","fab":"Outros","cat":"Adjuvante","ia":"ÃÂÃ¢ÂÂleo Vegetal ÃÂÃ¢ÂÂ°ster"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Headline Amp","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Metconazol"},

    {"nome":"Headline EC","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina"},

    {"nome":"Heat","fab":"BASF","cat":"Herbicida","ia":"Saflufenacil"},

    {"nome":"Herbadox 400 EC","fab":"BASF","cat":"Herbicida","ia":"Pendimetalina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Herbazida 480","fab":"ADAMA","cat":"Herbicida","ia":"Glifosato"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TIMAC AGRO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"HidroFit Arranque","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"P + Zn + aminoÃÂÃÂ¡cidos"},

    {"nome":"HidroFit K Plus","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"K + Ca + Mg"},

    {"nome":"HidroFit N-Max","fab":"Timac Agro","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"N + S"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Hokko Cupra 500 PM","fab":"Ihara","cat":"Fungicida","ia":"Oxicloreto de Cobre"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TIMAC AGRO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Humi-K","fab":"Timac Agro","cat":"Fertilizante","ia":"ÃÂÃÂcidos hÃÂÃÂºmicos + fÃÂÃÂºlvicos + K"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Hussar OD","fab":"BASF","cat":"Herbicida","ia":"Iodossulfurom-sÃÂÃÂ³dio"},

    {"nome":"Hussar Plus","fab":"BASF","cat":"Herbicida","ia":"Iodossulfurom + Mefenpir"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Iblon","fab":"Bayer","cat":"Fungicida","ia":"Isoflucipram + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Iguape 700 WG","fab":"ADAMA","cat":"Fungicida","ia":"Tiofanato MetÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Iharol EC","fab":"Outros","cat":"Adjuvante","ia":"ÃÂÃ¢ÂÂleo Mineral"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Imafort","fab":"Ouro Fino","cat":"Fungicida","ia":"Isoflucipramo + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Imazaquim 150 SL","fab":"Outros","cat":"Herbicida","ia":"Imazaquim"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Imazetapir 100 SL","fab":"UPL","cat":"Herbicida","ia":"Imazetapir"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Imidaclopride 700 WS","fab":"ADAMA","cat":"Inseticida","ia":"Imidaclopride"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Imperious","fab":"FMC","cat":"Inseticida","ia":"Clorantraniliprole + Bifentrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Imunit","fab":"BASF","cat":"Inseticida","ia":"Metaflumizone + Beta-Ciflutrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Influx","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Input","fab":"Bayer","cat":"Fungicida","ia":"Protioconazol + Espiropidiona"},

    {"nome":"Inspire","fab":"Bayer","cat":"Herbicida","ia":"Tembotriona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Inspire Super","fab":"Corteva","cat":"Fungicida","ia":"Difenoconazol + Ciprodinil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Instivo","fab":"Syngenta","cat":"Inseticida","ia":"Espinetoram"},

    {"nome":"Instivo AlgodÃÂÃÂ£o","fab":"Syngenta","cat":"Inseticida","ia":"Espinetoram"},

    {"nome":"Instivo Milho","fab":"Syngenta","cat":"Inseticida","ia":"Espinetoram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Integral Pro WG","fab":"Outros","cat":"Fungicida BiolÃÂÃÂ³gico","ia":"Bacillus subtilis"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Invict","fab":"Syngenta","cat":"Fungicida","ia":"Ciproconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Iprodiona 500 SC","fab":"Outros","cat":"Fungicida","ia":"Iprodiona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Jacle","fab":"FMC","cat":"Herbicida","ia":"Cloransulam-metÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Joiner CafÃÂÃÂ©","fab":"Syngenta","cat":"Inseticida","ia":"Sulfoxaflor + Lambda-Cialotrina"},

    {"nome":"Joiner HF","fab":"Syngenta","cat":"Inseticida","ia":"Sulfoxaflor + Lambda-Cialotrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Juno Flex","fab":"Bayer","cat":"Fungicida","ia":"Azoxistrobina + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"K-fol","fab":"UPL","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"PotÃÂÃÂ¡ssio"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MOSAIC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"K-Mag","fab":"Mosaic","cat":"Fertilizante","ia":"K 21% + Mg 10% + S 21%"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Kaiso Sorby 50 WG","fab":"Syngenta","cat":"Inseticida","ia":"Lambda-Cialotrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Kanet OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Mancozebe + Ciproconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Karate Zeon 50 CS","fab":"Syngenta","cat":"Inseticida","ia":"Lambda-Cialotrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Kashmir","fab":"UPL","cat":"Herbicida","ia":"Hexazinona + Isoxaflutol + Sulfentrazona"},

    {"nome":"Kasumin 2L","fab":"UPL","cat":"Fungicida","ia":"Kasugamicina"},

    {"nome":"Kennox","fab":"UPL","cat":"Herbicida","ia":"Hexazinona + Diurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Keyra","fab":"BASF","cat":"Fungicida","ia":"Mefentrifluconazol + Fenpropimorfe"},

    {"nome":"Kixor BX","fab":"BASF","cat":"Herbicida","ia":"Saflufenacil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Klorpan 480 EC","fab":"Ihara","cat":"Inseticida","ia":"ClorpirifÃÂÃÂ³s"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Kumulus DF","fab":"BASF","cat":"Fungicida","ia":"Enxofre"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Lactofen 240 EC","fab":"Outros","cat":"Herbicida","ia":"Lactofen"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Lambda-Cialotrina 250 CS","fab":"ADAMA","cat":"Inseticida","ia":"Lambda-Cialotrina"},

    {"nome":"Lanata 750 SC","fab":"ADAMA","cat":"Fungicida","ia":"Boscalida + Piraclostrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Lancer Gold","fab":"Ihara","cat":"Inseticida","ia":"Acefato + Imidaclopride"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Lannate BR","fab":"Corteva","cat":"Inseticida","ia":"Metomil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Larvin 800 WG","fab":"Bayer","cat":"Inseticida","ia":"Tiodicarbe"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Laser 360 CS","fab":"ADAMA","cat":"Herbicida","ia":"Clomazona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Leverage 360","fab":"FMC","cat":"Inseticida","ia":"Imidaclopride + Beta-Ciflutrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Lexar EZ","fab":"Corteva","cat":"Herbicida","ia":"S-Metolacloro + Atrazina + Mesotriona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Liberty 200 SL","fab":"Bayer","cat":"Herbicida","ia":"Glufosinato de AmÃÂÃÂ´nio"},

    {"nome":"Liberty 280 SL","fab":"Bayer","cat":"Herbicida","ia":"Glufosinato de AmÃÂÃÂ´nio"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Lintur 700 WG","fab":"ADAMA","cat":"Herbicida","ia":"Dicamba + Triasulfurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Locker","fab":"Bayer","cat":"Herbicida","ia":"Fluroxipir-meptÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Lorsban 480 BR","fab":"Corteva","cat":"Inseticida","ia":"ClorpirifÃÂÃÂ³s"},

    {"nome":"Lumax EZ","fab":"Corteva","cat":"Herbicida","ia":"S-Metolacloro + Atrazina + Mesotriona"},

    {"nome":"Lumiderm","fab":"Corteva","cat":"Tratamento de Sementes","ia":"Clorantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Luminus","fab":"UPL","cat":"Inseticida BiolÃÂÃÂ³gico","ia":"PeptÃÂÃÂ­deo Flg22-Bt"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Lumivia","fab":"Corteva","cat":"Tratamento de Sementes","ia":"Clorantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Luna Experience","fab":"Bayer","cat":"Fungicida","ia":"Fluopiram + Tebuconazol"},

    {"nome":"Luna Privilege","fab":"Bayer","cat":"Fungicida","ia":"Fluopiram"},

    {"nome":"Luna Sensation","fab":"Bayer","cat":"Fungicida","ia":"Fluopiram + Trifloxistrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Luximo","fab":"BASF","cat":"Herbicida","ia":"Metazacloro"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Malationa 500 CE","fab":"Outros","cat":"Inseticida","ia":"Malationa"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Malatol 500 CE","fab":"ADAMA","cat":"Inseticida","ia":"Malationa"},

    {"nome":"Mancozebe 750 WG","fab":"ADAMA","cat":"Fungicida","ia":"Mancozebe"},

    {"nome":"Mancozebe 800 WP","fab":"ADAMA","cat":"Fungicida","ia":"Mancozebe"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Manfil 750 WG","fab":"Ouro Fino","cat":"Fungicida","ia":"Mancozebe"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"ManganÃÂÃÂªs Foliar 15%","fab":"Outros","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"ManganÃÂÃÂªs"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Manzate 800 WP","fab":"Ihara","cat":"Fungicida","ia":"Mancozebe"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"MAP 11-52-00","fab":"Outros","cat":"Fertilizante","ia":"Monofosfato de amÃÂÃÂ´nio"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MOSAIC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"MAP Mosaic","fab":"Mosaic","cat":"Fertilizante","ia":"Monofosfato amÃÂÃÂ´nio 11-52-00"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Marshal 200 SC","fab":"ADAMA","cat":"Inseticida","ia":"Carbossulfano"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Match 50 EC","fab":"FMC","cat":"Inseticida","ia":"Lufenurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Maxifort","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Fluxapiroxade"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Maxim 025 FS","fab":"Outros","cat":"Tratamento de Sementes","ia":"Fludioxonil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Maxim Advanced","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Fludioxonil + Metalaxil-M"},

    {"nome":"Maxim XL 035 FS","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Fludioxonil + Metalaxil-M"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Melius","fab":"UPL","cat":"Regulador de Crescimento","ia":"Trinexapaque-etÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Melyra","fab":"BASF","cat":"Fungicida","ia":"Pydiflumetofen + Fludioxonil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Merlin 750 WG","fab":"Bayer","cat":"Herbicida","ia":"Isoxaflutol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Metalaxil-M 480 EC","fab":"Outros","cat":"Fungicida","ia":"Metalaxil-M"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Metarril SC","fab":"Ihara","cat":"Inseticida BiolÃÂÃÂ³gico","ia":"Metarhizium anisopliae"},

    {"nome":"Methomex 215 SL","fab":"Ihara","cat":"Inseticida","ia":"Metomil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Metribuzim 480 SC","fab":"ADAMA","cat":"Herbicida","ia":"Metribuzim"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Metsulfurom 600 WG","fab":"Outros","cat":"Herbicida","ia":"Metsulfurom-metÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Metsuran 600 WG","fab":"UPL","cat":"Herbicida","ia":"Metsulfurom-MetÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Mibelya","fab":"BASF","cat":"Fungicida","ia":"Pydiflumetofen + Difenoconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MOSAIC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"MicroEssentials S15","fab":"Mosaic","cat":"Fertilizante","ia":"MAP + N + P + S 15%"},

    {"nome":"MicroEssentials S9","fab":"Mosaic","cat":"Fertilizante","ia":"MAP + N + P + S 9%"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Minecto Duo","fab":"Syngenta","cat":"Inseticida","ia":"Abamectina + Ciantraniliprole"},

    {"nome":"Minecto Pro","fab":"Syngenta","cat":"Inseticida","ia":"Abamectina + Ciantraniliprole"},

    {"nome":"Miravis","fab":"Syngenta","cat":"Fungicida","ia":"Pydiflumetofen"},

    {"nome":"Miravis Ace","fab":"Syngenta","cat":"Fungicida","ia":"Pydiflumetofen + Azoxistrobina"},

    {"nome":"Miravis Duo","fab":"Syngenta","cat":"Fungicida","ia":"Pydiflumetofen + Difenoconazol"},

    {"nome":"Miravis Pro","fab":"Syngenta","cat":"Fungicida","ia":"Pydiflumetofen + Propiconazol"},

    {"nome":"Mitrion","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Propiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Moddus 250 EC","fab":"Outros","cat":"Regulador de Crescimento","ia":"Trinexapaque-etÃÂÃÂ­lico"},

    {"nome":"Molibdato de SÃÂÃÂ³dio","fab":"Outros","cat":"Fertilizante","ia":"Mo 39%"},

    {"nome":"MolibdÃÂÃÂªnio 10%","fab":"Outros","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"MolibdÃÂÃÂªnio"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Monarca 200 OD","fab":"Ihara","cat":"Inseticida","ia":"Metoxifenozida + Espinosade"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Movento 150 OD","fab":"Bayer","cat":"Inseticida","ia":"Spirotetramat"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MOSAIC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"MPasto 20-00-20","fab":"Mosaic","cat":"Fertilizante","ia":"NK 20-00-20 + S"},

    {"nome":"MPasto 20-05-20","fab":"Mosaic","cat":"Fertilizante","ia":"NPK 20-05-20 + S + Zn + B"},

    {"nome":"MPasto Plus","fab":"Mosaic","cat":"Fertilizante","ia":"NPK + S + Zn + B"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Murvin 850 PM","fab":"ADAMA","cat":"Inseticida","ia":"Carbaril"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Mustang 350 EW","fab":"Corteva","cat":"Inseticida","ia":"Zeta-Cipermetrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Nativo","fab":"Bayer","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Nativo 750 WG","fab":"ADAMA","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Nativo OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Trifloxistrobina + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Nemathorin 150 EC","fab":"Outros","cat":"Nematicida","ia":"Fostiazate"},

    {"nome":"Nicossulfurom 240 SC","fab":"Outros","cat":"Herbicida","ia":"Nicossulfurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Nimaxxa","fab":"UPL","cat":"Nematicida","ia":"Purpureocillium lilacinum"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Nimbus","fab":"Outros","cat":"Adjuvante","ia":"ÃÂÃ¢ÂÂleo Vegetal"},

    {"nome":"Nimitz Pro","fab":"Outros","cat":"Nematicida","ia":"Fluensulfona"},

    {"nome":"Nitrato de CÃÂÃÂ¡lcio","fab":"Outros","cat":"Fertilizante","ia":"15,5% N + 26% CaO"},

    {"nome":"Nitrato de PotÃÂÃÂ¡ssio","fab":"Outros","cat":"Fertilizante","ia":"13% N + 46% K2O"},

    {"nome":"Nitrofoska Foliar","fab":"Outros","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"NPK Foliar"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Nomolt 150","fab":"BASF","cat":"Inseticida","ia":"Teflubenzurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ NORTOX ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Nortox 2,4-D","fab":"Nortox","cat":"Herbicida","ia":"2,4-D Amina 806"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Nortox 480 SL","fab":"UPL","cat":"Herbicida","ia":"Glifosato"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ NORTOX ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Nortox Abamectina","fab":"Nortox","cat":"Inseticida","ia":"Abamectina 18 EC"},

    {"nome":"Nortox Atrazina 500","fab":"Nortox","cat":"Herbicida","ia":"Atrazina"},

    {"nome":"Nortox Cipermetrina","fab":"Nortox","cat":"Inseticida","ia":"Cipermetrina 250 EC"},

    {"nome":"Nortox ClorpirifÃÂÃÂ³s","fab":"Nortox","cat":"Inseticida","ia":"ClorpirifÃÂÃÂ³s 480 EC"},

    {"nome":"Nortox Deltametrina","fab":"Nortox","cat":"Inseticida","ia":"Deltametrina 25 EC"},

    {"nome":"Nortox Imidaclopride","fab":"Nortox","cat":"Inseticida","ia":"Imidaclopride 480 SC"},

    {"nome":"Nortox Mancozebe","fab":"Nortox","cat":"Fungicida","ia":"Mancozebe 800 WP"},

    {"nome":"Nortox Pendimetalina","fab":"Nortox","cat":"Herbicida","ia":"Pendimetalina 400 EC"},

    {"nome":"Nortox Tebuconazol","fab":"Nortox","cat":"Fungicida","ia":"Tebuconazol 200 EC"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"NPK 04-14-08","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂÃÂ§ÃÂÃÂ£o NPK 04-14-08"},

    {"nome":"NPK 04-20-20","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂÃÂ§ÃÂÃÂ£o NPK 04-20-20"},

    {"nome":"NPK 05-25-25","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂÃÂ§ÃÂÃÂ£o NPK 05-25-25"},

    {"nome":"NPK 08-20-20","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂÃÂ§ÃÂÃÂ£o NPK 08-20-20"},

    {"nome":"NPK 08-28-16","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂÃÂ§ÃÂÃÂ£o NPK 08-28-16"},

    {"nome":"NPK 10-10-10","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂÃÂ§ÃÂÃÂ£o NPK 10-10-10"},

    {"nome":"NPK 10-20-20","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂÃÂ§ÃÂÃÂ£o NPK 10-20-20"},

    {"nome":"NPK 12-06-12","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂÃÂ§ÃÂÃÂ£o NPK 12-06-12"},

    {"nome":"NPK 12-12-12","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂÃÂ§ÃÂÃÂ£o NPK 12-12-12"},

    {"nome":"NPK 15-05-30","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂÃÂ§ÃÂÃÂ£o NPK 15-05-30"},

    {"nome":"NPK 20-00-20","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂÃÂ§ÃÂÃÂ£o NPK 20-00-20"},

    {"nome":"NPK 20-05-20","fab":"Outros","cat":"Fertilizante","ia":"FormulaÃÂÃÂ§ÃÂÃÂ£o NPK 20-05-20"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Nurelle D 550/50","fab":"Ihara","cat":"Inseticida","ia":"ClorpirifÃÂÃÂ³s + Cipermetrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Nuvita","fab":"UPL","cat":"Bioestimulante","ia":"Extrato de algas + aminoÃÂÃÂ¡cidos"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Oberon 240 SC","fab":"Bayer","cat":"Inseticida","ia":"Espirodiclofeno"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Oberon OF","fab":"Ouro Fino","cat":"Acaricida","ia":"Espirodiclofeno"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Olea","fab":"UPL","cat":"Herbicida","ia":"2,4-D + Metsulfurom + Picloram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Opera","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Opera OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Opera Ultra","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Orkestra OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Orkestra SC","fab":"BASF","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Orondis Flexi","fab":"Syngenta","cat":"Fungicida","ia":"Oxathiapiprolin + Mandipropamida"},

    {"nome":"Orondis Gold","fab":"Syngenta","cat":"Fungicida","ia":"Oxathiapiprolin + Mefenoxam"},

    {"nome":"Orondis Ultra","fab":"Syngenta","cat":"Fungicida","ia":"Oxathiapiprolin + Clorotalonil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ortus 50 SC","fab":"Outros","cat":"Acaricida","ia":"Fenpiroximato"},

    {"nome":"Oxifluorfem 240 EC","fab":"Outros","cat":"Herbicida","ia":"Oxifluorfem"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Pagani","fab":"BASF","cat":"Fungicida","ia":"Piraclostrobina + Epoxiconazol + Fluxapiroxade"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Palisade EC","fab":"Outros","cat":"Regulador de Crescimento","ia":"Prohexadona de CÃÂÃÂ¡lcio"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Pallas 45 OD","fab":"Syngenta","cat":"Herbicida","ia":"Piroxsulam"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Pantera 40 EC","fab":"ADAMA","cat":"Herbicida","ia":"Quizalofope-P-etÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Pavecto","fab":"BASF","cat":"Fungicida","ia":"Mefentrifluconazol + Boscalida"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Pendimetalina 400 EC","fab":"Outros","cat":"Herbicida","ia":"Pendimetalina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MOSAIC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Performa Bio","fab":"Mosaic","cat":"Fertilizante","ia":"MAP + S + PGPR"},

    {"nome":"Performa Full","fab":"Mosaic","cat":"Fertilizante","ia":"N+P+K+Mg+S+B completo"},

    {"nome":"Performa HF","fab":"Mosaic","cat":"Fertilizante","ia":"MicroEssentials + Aspire + K-Mag"},

    {"nome":"Performa Neo","fab":"Mosaic","cat":"Fertilizante","ia":"MicroEssentials + K-Mag"},

    {"nome":"Performa Plus","fab":"Mosaic","cat":"Fertilizante","ia":"MicroEssentials + Aspire"},

    {"nome":"Performa Ultra","fab":"Mosaic","cat":"Fertilizante","ia":"K + Mg + S + B"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Pergado MZ","fab":"Syngenta","cat":"Fungicida","ia":"Mandipropamida + Mancozebe"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Permetrina 500 EC","fab":"ADAMA","cat":"Inseticida","ia":"Permetrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Persist","fab":"FMC","cat":"Herbicida","ia":"Imazaquim"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TIMAC AGRO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Physiostart","fab":"Timac Agro","cat":"Fertilizante","ia":"MAP + Ca + tecnologia Physio"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Picloram 240 SL","fab":"Outros","cat":"Herbicida","ia":"Picloram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Pidan","fab":"FMC","cat":"Inseticida","ia":"Clorfenapir"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Pidan 360 EC","fab":"Ihara","cat":"Inseticida","ia":"Clorfenapir"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Piraclostrobina 250 EC","fab":"Outros","cat":"Fungicida","ia":"Piraclostrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Pirate","fab":"BASF","cat":"Inseticida","ia":"Clorfenapir"},

    {"nome":"Pirimor 500 WG","fab":"BASF","cat":"Inseticida","ia":"Pirimicarbe"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Pirimor 500 WG Adama","fab":"ADAMA","cat":"Inseticida","ia":"Pirimicarbe"},

    {"nome":"Pivot 600 CS","fab":"ADAMA","cat":"Herbicida","ia":"Imazetapir"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Pivotal","fab":"Corteva","cat":"Tratamento de Sementes","ia":"Clorantraniliprole + Tiametoxam"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Plateau 700 WG","fab":"BASF","cat":"Herbicida","ia":"Imazapique"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Plenexos","fab":"Bayer","cat":"Inseticida","ia":"Fluazaindolizina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Plinazolin","fab":"Syngenta","cat":"Inseticida","ia":"Plinazolina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Pluto 100 SC","fab":"Outros","cat":"Acaricida","ia":"Etoxazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Poast","fab":"ADAMA","cat":"Herbicida","ia":"Setoxidim"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Polo 500 WP","fab":"Syngenta","cat":"Inseticida","ia":"Diafentiurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Polyram DF","fab":"BASF","cat":"Fungicida","ia":"Metiram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Polytrin 400/40 EC","fab":"Ihara","cat":"Inseticida","ia":"ProfenofÃÂÃÂ³s + Cipermetrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Poncho 600 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Clotianidina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"PotÃÂÃÂ¡ssio Foliar 10%","fab":"Outros","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"PotÃÂÃÂ¡ssio"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Predix","fab":"FMC","cat":"Fungicida","ia":"Fluxapiroxade"},

    {"nome":"Premio 200 SC","fab":"FMC","cat":"Inseticida","ia":"Clorantraniliprole"},

    {"nome":"Presence 500","fab":"FMC","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Presence 500 SC","fab":"UPL","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Presence OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Fluxapiroxade + Piraclostrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Prexio","fab":"BASF","cat":"Inseticida","ia":"Broflanilida"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Primestra Gold","fab":"Bayer","cat":"Herbicida","ia":"S-Metolacloro + Atrazina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Priori Top","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Difenoconazol"},

    {"nome":"Priori Xtra","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina + Ciproconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Priori Xtra OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Ciproconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Proclaim 50 WG","fab":"Syngenta","cat":"Inseticida","ia":"Benzoato de Emamectina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Propiconazol 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Propiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Propose","fab":"UPL","cat":"Inseticida","ia":"Clorantraniliprole + Clorfenapir"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Prosaro 420 SC","fab":"Bayer","cat":"Fungicida","ia":"Protioconazol + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Provar","fab":"Outros","cat":"Acaricida","ia":"Hexitiazox"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Provost 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Propiconazol + Iprodiona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Provost Opti","fab":"Bayer","cat":"Fungicida","ia":"Iprodiona + Propiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Quadris","fab":"Syngenta","cat":"Fungicida","ia":"Azoxistrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Rabano","fab":"Ouro Fino","cat":"Herbicida","ia":"Fluazifope-P-butÃÂÃÂ­lico + Fomesafem"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Rampage 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Ciproconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Raptor","fab":"BASF","cat":"Herbicida","ia":"Imazapique"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ravine 240 EC","fab":"ADAMA","cat":"Fungicida","ia":"Boscalida"},

    {"nome":"Reason 500 SC","fab":"ADAMA","cat":"Fungicida","ia":"Famoxadona + Cimoxanil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Rebron","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole + Tiametoxam"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Regent 800 WG","fab":"ADAMA","cat":"Inseticida","ia":"Fipronil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Regent Duo","fab":"BASF","cat":"Inseticida","ia":"Fipronil + Tiametoxam"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Reglone","fab":"Syngenta","cat":"Herbicida","ia":"Diquat"},

    {"nome":"Revus Opti","fab":"Syngenta","cat":"Fungicida","ia":"Mandipropamida + Clorotalonil"},

    {"nome":"Revus Top","fab":"Syngenta","cat":"Fungicida","ia":"Mandipropamida + Difenoconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Revysol","fab":"BASF","cat":"Fungicida","ia":"Mefentrifluconazol"},

    {"nome":"Rhodiauram 700 WS","fab":"BASF","cat":"Tratamento de Sementes","ia":"Thiram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ridomil Gold MZ","fab":"Syngenta","cat":"Fungicida","ia":"Metalaxil-M + Mancozebe"},

    {"nome":"Ridomil Gold WG","fab":"Syngenta","cat":"Fungicida","ia":"Metalaxil-M + Cobre"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Rinskor Active","fab":"Corteva","cat":"Herbicida","ia":"Florpirauifen-benzil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ripcord 100 EC","fab":"Syngenta","cat":"Inseticida","ia":"Cipermetrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Rizoliq Top","fab":"Outros","cat":"Fungicida BiolÃÂÃÂ³gico","ia":"Trichoderma harzianum"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Roundup Original","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},

    {"nome":"Roundup Powermax","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},

    {"nome":"Roundup Ready","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},

    {"nome":"Roundup Transorb HC","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},

    {"nome":"Roundup Ultra Max","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},

    {"nome":"Roundup WG","fab":"Bayer","cat":"Herbicida","ia":"Glifosato"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Rovral SC","fab":"UPL","cat":"Fungicida","ia":"Iprodiona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Rynaxypyr 200 SC","fab":"Corteva","cat":"Inseticida","ia":"Clorantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"S-Metolacloro 960 EC","fab":"Outros","cat":"Herbicida","ia":"S-Metolacloro"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Samson Extra 6%","fab":"UPL","cat":"Herbicida","ia":"Nicossulfurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Samurai SC","fab":"Ihara","cat":"Inseticida","ia":"Imidaclopride + Lambda-Cialotrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Sanmite 150 WP","fab":"ADAMA","cat":"Acaricida","ia":"Piridabem"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Sanson 40 SC","fab":"Syngenta","cat":"Herbicida","ia":"Nicossulfurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Savey 50 WP","fab":"Outros","cat":"Acaricida","ia":"Hexitiazox"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Score 250 EC","fab":"Syngenta","cat":"Fungicida","ia":"Difenoconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Score Ihara","fab":"Ihara","cat":"Fungicida","ia":"Difenoconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Score OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Difenoconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Select Max","fab":"Corteva","cat":"Herbicida","ia":"Cletodim"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Seltima","fab":"BASF","cat":"Fungicida","ia":"Isoflucipramo + Propiconazol"},

    {"nome":"Seltima Duo","fab":"BASF","cat":"Fungicida","ia":"Isoflucipramo + Trifloxistrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Semevin 350 FS","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Tiametoxam"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Sencor 480 SC","fab":"ADAMA","cat":"Herbicida","ia":"Metribuzim"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Serenade ASO","fab":"Outros","cat":"Fungicida BiolÃÂÃÂ³gico","ia":"Bacillus subtilis"},

    {"nome":"Setoxidim 184 EC","fab":"Outros","cat":"Herbicida","ia":"Setoxidim"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MOSAIC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"SFP 10-40-00+S","fab":"Mosaic","cat":"Fertilizante","ia":"N + P + S em grÃÂÃÂ¢nulo ÃÂÃÂºnico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Silvacur Combi","fab":"Bayer","cat":"Fungicida","ia":"Tebuconazol + Triadimenol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Silwet L-77","fab":"Outros","cat":"Adjuvante","ia":"Silicone"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Sivanto Prime 100 SL","fab":"Bayer","cat":"Inseticida","ia":"Flupyradifurona"},

    {"nome":"Sivanto Prime 200 SL","fab":"Bayer","cat":"Inseticida","ia":"Flupyradifurona"},

    {"nome":"Sonata AS","fab":"Bayer","cat":"Inseticida BiolÃÂÃÂ³gico","ia":"Bacillus pumilus"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Sperto","fab":"UPL","cat":"Inseticida","ia":"Bifentrina + Imidaclopride"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Sphere Max","fab":"Bayer","cat":"Fungicida","ia":"Trifloxistrobina + Ciproconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Sphere OF","fab":"UPL","cat":"Fungicida","ia":"Trifloxistrobina + Ciproconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Spinetoram 250 SC","fab":"Corteva","cat":"Inseticida","ia":"Espinetoram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Spinnaker","fab":"UPL","cat":"Herbicida","ia":"Imazapique"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Spintor 480 SC","fab":"Corteva","cat":"Inseticida","ia":"Espinosade"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Spiromax 240 SC","fab":"Outros","cat":"Acaricida","ia":"Espirodiclofeno"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Sponta AlgodÃÂÃÂ£o","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole"},

    {"nome":"Sponta Milho","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Spot SC","fab":"BASF","cat":"Fungicida","ia":"Fluazinam"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Spread Max","fab":"Outros","cat":"Adjuvante","ia":"Surfactante"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Standak Top","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Fipronil + Piraclostrobina + Tiofanato"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Starane Quatro","fab":"Corteva","cat":"Herbicida","ia":"Fluroxipir-meptÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Start UPL","fab":"UPL","cat":"Inseticida","ia":"Fipronil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TIMAC AGRO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Starter Timac","fab":"Timac Agro","cat":"Fertilizante","ia":"N + P + Zn + aminoÃÂÃÂ¡cidos"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Status","fab":"BASF","cat":"Fungicida","ia":"Dimoxistrobina + Epoxiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Stimulate Foliar","fab":"Outros","cat":"Regulador de Crescimento","ia":"Citocinina + Auxina + Giberelina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Stomp 400 CS","fab":"ADAMA","cat":"Herbicida","ia":"Pendimetalina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Stopit Ca","fab":"Outros","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"CÃÂÃÂ¡lcio"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Stratego 250 EC","fab":"Bayer","cat":"Fungicida","ia":"Trifloxistrobina + Propiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Stroby SC","fab":"BASF","cat":"Fungicida","ia":"Cresoxim-metÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TIMAC AGRO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Sulfammo 26N","fab":"Timac Agro","cat":"Fertilizante","ia":"26% N amoniacal + S"},

    {"nome":"Sulfammo MeTA 11","fab":"Timac Agro","cat":"Fertilizante","ia":"11% N + S inibidor MeTA"},

    {"nome":"Sulfammo MeTA 17","fab":"Timac Agro","cat":"Fertilizante","ia":"17% N + S inibidor MeTA"},

    {"nome":"Sulfammo MeTA 21","fab":"Timac Agro","cat":"Fertilizante","ia":"21% N + S inibidor MeTA"},

    {"nome":"Sulfammo MeTA 29","fab":"Timac Agro","cat":"Fertilizante","ia":"29% N + S inibidor MeTA"},

    {"nome":"Sulfammo MeTA 29 Boro","fab":"Timac Agro","cat":"Fertilizante","ia":"29% N + S + B"},

    {"nome":"Sulfammo Ultra","fab":"Timac Agro","cat":"Fertilizante","ia":"N + S alta concentraÃÂÃÂ§ÃÂÃÂ£o"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Sulfato de AmÃÂÃÂ´nio","fab":"Outros","cat":"Fertilizante","ia":"21% N + 24% S"},

    {"nome":"Sulfato de MagnÃÂÃÂ©sio","fab":"Outros","cat":"Fertilizante","ia":"Mg 10% + S 13%"},

    {"nome":"Sulfato de ManganÃÂÃÂªs","fab":"Outros","cat":"Fertilizante","ia":"Mn 26% + S"},

    {"nome":"Sulfato de PotÃÂÃÂ¡ssio","fab":"Outros","cat":"Fertilizante","ia":"K2SO4 50% K2O + 18% S"},

    {"nome":"Sulfato de Zinco","fab":"Outros","cat":"Fertilizante","ia":"Zn 21% + S 11%"},

    {"nome":"Sulfentrazona 500 SC","fab":"Outros","cat":"Herbicida","ia":"Sulfentrazona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Sumidan 25 EC","fab":"ADAMA","cat":"Inseticida","ia":"Esfenvalerato"},

    {"nome":"Sumithion 500 EC","fab":"ADAMA","cat":"Inseticida","ia":"Fenitrotiom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Superfosfato Simples","fab":"Outros","cat":"Fertilizante","ia":"SSP 18% P2O5 + 12% S"},

    {"nome":"Superfosfato Triplo","fab":"Outros","cat":"Fertilizante","ia":"STP 46% P2O5"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Surtain","fab":"BASF","cat":"Herbicida","ia":"Saflufenacil + Clomazona"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Switch 625 WG","fab":"Corteva","cat":"Fungicida","ia":"Ciprodinil + Fludioxonil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Systhane 750 WG","fab":"ADAMA","cat":"Fungicida","ia":"Miclobutanil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tacklier","fab":"UPL","cat":"Inseticida BiolÃÂÃÂ³gico","ia":"Bacillus thuringiensis"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Takumi 20 SC","fab":"Ihara","cat":"Inseticida","ia":"Flubendiamida"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Talstar 100 EC","fab":"FMC","cat":"Inseticida","ia":"Bifentrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Targa Max 50 EC","fab":"BASF","cat":"Herbicida","ia":"Quizalofope-P-etÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Targa Quik","fab":"ADAMA","cat":"Herbicida","ia":"Quizalofope-P-etÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tebuco OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tebuconazol 200 EC","fab":"Bayer","cat":"Fungicida","ia":"Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tebuconazol 750 WG","fab":"ADAMA","cat":"Fungicida","ia":"Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tepraloxidim 200 EC","fab":"Outros","cat":"Herbicida","ia":"Tepraloxidim"},

    {"nome":"Termofosfato Yoorin","fab":"Outros","cat":"Fertilizante","ia":"P2O5 18% + Ca + Mg + Si"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Thiram 480 SC","fab":"ADAMA","cat":"Fungicida","ia":"Thiram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Thiram 750 WS","fab":"Outros","cat":"Fungicida","ia":"Thiram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Thunder","fab":"UPL","cat":"Herbicida","ia":"Asulam"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tiametoxam 700 WS","fab":"Outros","cat":"Inseticida","ia":"Tiametoxam"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tiger 100 EC","fab":"FMC","cat":"Inseticida","ia":"Bifentrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tilt 250 EC","fab":"ADAMA","cat":"Fungicida","ia":"Propiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tiofanato MetÃÂÃÂ­lico 700 WG","fab":"Outros","cat":"Fungicida","ia":"Tiofanato MetÃÂÃÂ­lico"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tirexor","fab":"BASF","cat":"Herbicida","ia":"Trifludimoxazim"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TIMAC AGRO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Top-Phos","fab":"Timac Agro","cat":"Fertilizante","ia":"MAP protegido tecnologia CSP"},

    {"nome":"Top-Phos 40","fab":"Timac Agro","cat":"Fertilizante","ia":"Fosfato amoniado protegido 40% P2O5"},

    {"nome":"Top-Phos Arroz","fab":"Timac Agro","cat":"Fertilizante","ia":"FÃÂÃÂ³sforo protegido para arroz"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tordon","fab":"Bayer","cat":"Herbicida","ia":"2,4-D + Picloram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tornade Duo","fab":"Corteva","cat":"Herbicida","ia":"2,4-D + Picloram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Torque 550 SC","fab":"Ihara","cat":"Acaricida","ia":"Fenbutestanho"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Touchdown IQ","fab":"Syngenta","cat":"Herbicida","ia":"Glifosato"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CORTEVA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tracer 480 SC","fab":"Corteva","cat":"Inseticida","ia":"Espinosade"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Transform 500 WG","fab":"FMC","cat":"Inseticida","ia":"Sulfoxaflor"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Trico WP","fab":"Outros","cat":"Fungicida BiolÃÂÃÂ³gico","ia":"Trichoderma viride"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Tridium","fab":"UPL","cat":"Fungicida","ia":"Trifloxistrobina + Epoxiconazol + Tebuconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Trifloxistrobina 250 SC","fab":"Outros","cat":"Fungicida","ia":"Trifloxistrobina"},

    {"nome":"Trifluralin 480 EC","fab":"Outros","cat":"Herbicida","ia":"Trifluralina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Trilex Advance","fab":"Bayer","cat":"Tratamento de Sementes","ia":"Trifloxistrobina + Protioconazol + Spirotetramat"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Trophy 500 EC","fab":"Syngenta","cat":"Herbicida","ia":"Acetocloro"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ MOSAIC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"TSP Mosaic","fab":"Mosaic","cat":"Fertilizante","ia":"Superfosfato triplo 00-46-00"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Unika Ca+B","fab":"Outros","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"CÃÂÃÂ¡lcio + Boro"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BAYER ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Unison Xpro","fab":"Bayer","cat":"Fungicida","ia":"Bixafem + Propiconazol + Trifloxistrobina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Unizeb 750 WG","fab":"Syngenta","cat":"Fungicida","ia":"Mancozebe"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Unizeb Gold","fab":"UPL","cat":"Fungicida","ia":"Mancozebe 750 WG"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Ureia 45% N","fab":"Outros","cat":"Fertilizante","ia":"Carbamida 45% N"},

    {"nome":"Ureia NBPT","fab":"Outros","cat":"Fertilizante","ia":"Ureia + inibidor urease NBPT"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Velpar K WG","fab":"UPL","cat":"Herbicida","ia":"Hexazinona + Diurom"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Velum Prime","fab":"Outros","cat":"Nematicida","ia":"Fluopyram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Verdadeiro","fab":"Ouro Fino","cat":"Inseticida","ia":"Tiametoxam"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Verdadero","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam"},

    {"nome":"Verdavis Milho","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Clorantraniliprole"},

    {"nome":"Verdavis Soja","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Clorantraniliprole"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Verismo","fab":"BASF","cat":"Inseticida","ia":"Metaflumizone"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Versys","fab":"Syngenta","cat":"Inseticida","ia":"Flupyrimin + Lambda-Cialotrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Vertimec 18 EC","fab":"ADAMA","cat":"Acaricida","ia":"Abamectina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Vertimec Gold","fab":"Ihara","cat":"Acaricida","ia":"Abamectina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Vibrance Duo","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Sedaxane + Fludioxonil"},

    {"nome":"Vibrance Integral","fab":"Syngenta","cat":"Tratamento de Sementes","ia":"Sedaxane + Fludioxonil + Metalaxil-M"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Vitavax Thiram 200 SC","fab":"BASF","cat":"Tratamento de Sementes","ia":"Carboxim + Thiram"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ UPL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Vitavax Thiram 200 SC UPL","fab":"UPL","cat":"Fungicida","ia":"Carboxim + Thiram"},

    {"nome":"Vitavax Ultra TS","fab":"UPL","cat":"Tratamento de Sementes","ia":"Carboxim + Tiram + Tiametoxam"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SYNGENTA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Voliam Flexi","fab":"Syngenta","cat":"Inseticida","ia":"Tiametoxam + Clorantraniliprole"},

    {"nome":"Voliam Targo","fab":"Syngenta","cat":"Inseticida","ia":"Clorantraniliprole + Abamectina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Voraxor","fab":"BASF","cat":"Herbicida","ia":"Trifludimoxazim + Saflufenacil"},

    {"nome":"Vydate 240 SL","fab":"BASF","cat":"Inseticida","ia":"Oxamil"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ IHARA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Xcyte","fab":"Ihara","cat":"Inseticida","ia":"Ciantraniliprole + Clorfenapir"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"XenTari WDG","fab":"Outros","cat":"Inseticida BiolÃÂÃÂ³gico","ia":"Bacillus thuringiensis aizawai"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BASF ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Zampro","fab":"BASF","cat":"Fungicida","ia":"Ametoctradina + Dimetomorfe"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Zeal 72 WP","fab":"Outros","cat":"Acaricida","ia":"Etoxazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ADAMA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Zeta-Cipermetrina 250 EC","fab":"ADAMA","cat":"Inseticida","ia":"Zeta-Cipermetrina"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Zeus OF","fab":"Ouro Fino","cat":"Fungicida","ia":"Azoxistrobina + Epoxiconazol"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Zinco Quelatado 9%","fab":"Outros","cat":"Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o","ia":"Zinco"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ FMC ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"Zoom 750 WG","fab":"FMC","cat":"Inseticida","ia":"Acefato"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OUTROS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"ÃÂÃÂcido BÃÂÃÂ³rico","fab":"Outros","cat":"Fertilizante","ia":"B 17%"},

    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ OURO FINO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    {"nome":"ÃÂÃÂ nio 200 SC","fab":"Ouro Fino","cat":"Fungicida","ia":"Iprodiona"},

]





# Ordena por nome para o autocomplete

CATALOGO_PRODUTOS.sort(key=lambda x: x["nome"].lower())



def buscar_produtos_catalogo(query):

    """Retorna produtos do catÃÂÃÂ¡logo filtrando por nome ou ingrediente ativo."""

    if not query:

        return CATALOGO_PRODUTOS

    q = query.lower()

    # Primeiro os que COMEÃÂÃ¢ÂÂ¡AM com a busca

    starts = [p for p in CATALOGO_PRODUTOS if p["nome"].lower().startswith(q)]

    # Depois os que CONTÃÂÃÂ M em qualquer posiÃÂÃÂ§ÃÂÃÂ£o (nome ou IA)

    contains = [p for p in CATALOGO_PRODUTOS

                if not p["nome"].lower().startswith(q)

                and (q in p["nome"].lower() or q in p["ia"].lower() or q in p["cat"].lower())]

    return starts + contains





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: ESTOQUE DE INSUMOS

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬



# FUNÃÂÃ¢ÂÂ¡ÃÂÃ¢ÂÂ¢ES UTILITÃÂÃÂRIAS

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

def classificar(valor, baixo, medio):

    if valor < baixo:   return "Baixo"

    elif valor < medio: return "MÃÂÃÂ©dio"

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

                if app.get("ID ÃÂÃÂrea", id_area) == id_area

            ]

            st.session_state.areas[i]["Estoque"] = st.session_state.estoque.copy()

            break

    salvar_dados_iaagro()





def gerar_pdf_programacao_aplicacoes(aplicacoes, fazenda="", talhao="", cultura="", area_ha=0, operador=""):

    """Gera PDF profissional com programaÃÂÃÂ§ÃÂÃÂ£o de aplicaÃÂÃÂ§ÃÂÃÂµes por estÃÂÃÂ¡dio."""

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

        "ÃÂÃ¢ÂÂleo mineral/vegetal":colors.HexColor("#ede9fe"),"Fertilizante foliar":colors.HexColor("#fce7f3"),

        "Regulador":colors.HexColor("#ffedd5"),"Outro":COR_CINZA,

    }



    def P(txt, size=9, bold=False, color=None, align=TA_LEFT):

        fn = "Helvetica-Bold" if bold else "Helvetica"

        c  = color or COR_TEXTO

        return Paragraph(txt, ParagraphStyle("p", fontName=fn, fontSize=size, textColor=c, alignment=align, leading=size+3))



    # CABEÃÂÃ¢ÂÂ¡ALHO

    h = [[P("IAAgro",18,True,COR_VERDE), P("PROGRAMAÃÂÃ¢ÂÂ¡ÃÂÃÂO DE APLICACOES",14,True,COR_BRANCO,TA_CENTER),

          P(f"Emitido: {datetime.now().strftime('%d/%m/%Y %H:%M')}",7,False,COR_CINZA,TA_RIGHT)]]

    th = Table(h, colWidths=[4*cm,10*cm,4.5*cm])

    th.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),COR_VERDE_E),

        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),

        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))

    story.append(th); story.append(Spacer(1,3*mm))



    # INFO PROPRIEDADE

    i = [[P(f"<b>Fazenda:</b> {fazenda or 'ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ'}"),P(f"<b>Talhao:</b> {talhao or 'ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ'}"),

          P(f"<b>Cultura:</b> {cultura or 'ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ'}"),P(f"<b>Area:</b> {area_ha} ha"),

          P(f"<b>Responsavel:</b> {operador or 'ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ'}")]]

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



    # BLOCOS POR ESTÃÂÃÂDIO

    for num, aplic in enumerate(aplicacoes, 1):

        est = aplic.get("EstÃÂÃÂ¡dio") or aplic.get("AplicaÃÂÃÂ§ÃÂÃÂ£o","")

        for e in ["ÃÂ°ÃÂ¸ÃÂÃÂ±","ÃÂ°ÃÂ¸ÃÂÃÂ¿","ÃÂ°ÃÂ¸ÃÂÃÂ¾","ÃÂ°ÃÂ¸ÃÂÃÂ¸","ÃÂ°ÃÂ¸ÃÂ«ÃÂ","ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹"]: est = est.replace(e,"").strip()



        cab = [[P(f"{num}. {est}",11,True,COR_BRANCO),

                P(f"Data: {aplic.get('Data','ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ')} | Area: {aplic.get('ÃÂÃÂrea aplicada ha',0)} ha | "

                  f"Calda: {aplic.get('Volume calda L/ha',0)} L/ha | "

                  f"Tanques: {aplic.get('NÃÂÃÂºmero tanques',0):.1f} | "

                  f"Pulverizador: {aplic.get('Pulverizador','ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ')} | "

                  f"Clima: {aplic.get('Clima aplicaÃÂÃÂ§ÃÂÃÂ£o','ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ')}",8,False,COR_CINZA)]]

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

    Calagem pelo mÃÂÃÂ©todo SMP (CQFS RS/SC 2016) ou pH em ÃÂÃÂ¡gua.

    PRNT mÃÂÃÂ©dio adotado: 75% (calcÃÂÃÂ¡rio comercial tÃÂÃÂ­pico da regiÃÂÃÂ£o Sul)

    FÃÂÃÂ³rmula: NC (t/ha) = dose_base / (PRNT/100)

    """

    PRNT = 0.75  # PRNT mÃÂÃÂ©dio 75% ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ calcÃÂÃÂ¡rio comercial RS/SC/PR



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

        precisa = True; motivos.append("AlumÃÂÃÂ­nio elevado")

    if calcio < 3:

        precisa = True; motivos.append("CÃÂÃÂ¡lcio baixo")

    if enxofre < 8:

        precisa = True; motivos.append("Enxofre baixo")

    if ctc < 6 and aluminio > 0.2:

        precisa = True; motivos.append("CTC baixa com alumÃÂÃÂ­nio presente")

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

    elif nota < 75: return "MÃÂÃÂ©dia"

    return "Baixa"





def estimar_producao(meta, nota):

    fator = nota / 100

    if   fator >= 0.85: return meta

    elif fator >= 0.70: return meta * 0.85

    elif fator >= 0.50: return meta * 0.70

    return meta * 0.55





def recomendacao_npk(cultura, produtividade, fosforo, potassio, materia_organica, argila=50, ph=5.5):

    # Remove ÃÂÃÂ­cone se presente

    cultura = cultura_limpa(cultura) if cultura else "Soja"

    """

    RecomendaÃÂÃÂ§ÃÂÃÂ£o NPK baseada em:

    - EMBRAPA Soja ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Circular TÃÂÃÂ©cnica 98 + Tecnologias de ProduÃÂÃÂ§ÃÂÃÂ£o 2022

    - EMBRAPA Milho e Sorgo ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Circular TÃÂÃÂ©cnica 100/2023

    - CQFS RS/SC 2016 (Manual de Calagem e AdubaÃÂÃÂ§ÃÂÃÂ£o)

    - IAC Boletim 100 (2014) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ culturas diversas

    - EMBRAPA Trigo ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ RecomendaÃÂÃÂ§ÃÂÃÂµes TÃÂÃÂ©cnicas 2021

    - EMBRAPA Arroz e FeijÃÂÃÂ£o

    - MAPA ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Boas PrÃÂÃÂ¡ticas AgrÃÂÃÂ­colas

    Unidades: kg/ha de N, P2O5, K2O

    P = Mehlich-1 (mg/dmÃÂÃÂ³) | K = mg/dmÃÂÃÂ³ | MO = g/dmÃÂÃÂ³ ou %

    """

    n = p2o5 = k2o = 0



    if cultura == "Soja":

        # EMBRAPA Soja: N=0 com boa nodulaÃÂÃÂ§ÃÂÃÂ£o (BNF supre 200-300 kg N/ha)

        n = 0

        # P2O5 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ CQFS RS/SC 2016 Tab. 4.3 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ solo argiloso (argila 41-60%)

        # ExportaÃÂÃÂ§ÃÂÃÂ£o: ~16 kg P2O5/sc (60 kg) ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ manutenÃÂÃÂ§ÃÂÃÂ£o + reposiÃÂÃÂ§ÃÂÃÂ£o

        if   fosforo < 4:   p2o5 = 140

        elif fosforo < 7:   p2o5 = 110

        elif fosforo < 11:  p2o5 = 90

        elif fosforo < 16:  p2o5 = 70

        elif fosforo < 22:  p2o5 = 55

        elif fosforo < 30:  p2o5 = 40

        else:               p2o5 = 25

        # K2O ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ CQFS RS/SC 2016 Tab. 4.4 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ exportaÃÂÃÂ§ÃÂÃÂ£o ~18 kg K2O/sc

        if   potassio < 40:  k2o = 130

        elif potassio < 60:  k2o = 105

        elif potassio < 80:  k2o = 85

        elif potassio < 120: k2o = 70

        elif potassio < 180: k2o = 55

        elif potassio < 240: k2o = 40

        else:                k2o = 25

        # Ajuste produtividade (EMBRAPA ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ base 50 sc/ha)

        fator_prod = max(1.0, produtividade / 50)

        p2o5 = round(p2o5 * fator_prod, 0)

        k2o  = round(k2o  * fator_prod, 0)



    elif cultura == "Milho":

        # EMBRAPA Milho ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ base 10 t/ha, N parcelado (plantio + cobertura)

        # N plantio: 20-30 kg/ha | N cobertura: 30-50 kg/ha por 1000 kg grÃÂÃÂ£o

        n_plantio = 25

        n_cob     = min(produtividade * 1.5, 140)  # 1,5 kg N / sc 60kg

        n = round(n_plantio + n_cob, 1)

        # P2O5 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ CQFS 2016 Tab. 5.3

        if   fosforo < 4:   p2o5 = 130

        elif fosforo < 7:   p2o5 = 105

        elif fosforo < 11:  p2o5 = 85

        elif fosforo < 16:  p2o5 = 65

        elif fosforo < 22:  p2o5 = 50

        elif fosforo < 30:  p2o5 = 35

        else:               p2o5 = 20

        # K2O ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ CQFS 2016 Tab. 5.4

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

        # EMBRAPA Trigo ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Sistema Plantio Direto Sul Brasil 2021

        # N = 30 plantio + cobertura conforme MO e produtividade

        if   materia_organica < 2.5: n = 30 + produtividade * 1.0

        elif materia_organica < 4.0: n = 20 + produtividade * 0.9

        else:                        n = 15 + produtividade * 0.8

        n = min(round(n, 1), 100)

        # P2O5 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ CQFS 2016

        if   fosforo < 4:   p2o5 = 110

        elif fosforo < 7:   p2o5 = 90

        elif fosforo < 11:  p2o5 = 70

        elif fosforo < 16:  p2o5 = 55

        elif fosforo < 22:  p2o5 = 40

        else:               p2o5 = 25

        # K2O ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ CQFS 2016

        if   potassio < 60:  k2o = 90

        elif potassio < 80:  k2o = 70

        elif potassio < 120: k2o = 55

        elif potassio < 180: k2o = 40

        else:                k2o = 25



    elif cultura == "FeijÃÂÃÂ£o":

        # EMBRAPA FeijÃÂÃÂ£o + CQFS 2016 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ fixaÃÂÃÂ§ÃÂÃÂ£o parcial de N

        # N starter 20 kg/ha + complemento se nÃÂÃÂ£o inoculado

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

        # EMBRAPA Arroz e FeijÃÂÃÂ£o ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ irrigado e sequeiro

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

        # EMBRAPA Trigo adaptado + pesquisas ParanÃÂÃÂ¡/RS

        # Canola extrai muito enxofre ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ recomenda gesso

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



    elif cultura == "CafÃÂÃÂ©":

        # EMBRAPA CafÃÂÃÂ© ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Circular TÃÂÃÂ©cnica 132

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

        # IAC Boletim 100 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ horticultura

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

        # GenÃÂÃÂ©rico ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ conservador

        n = 40; p2o5 = 60; k2o = 60



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Ajustes gerais de solo ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    # Textura: solos arenosos (<20% argila) tÃÂÃÂªm menor CTC ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ mais K

    if argila < 15:     k2o = round(k2o * 1.25, 0)

    elif argila < 25:   k2o = round(k2o * 1.15, 0)

    elif argila > 70:   k2o = round(k2o * 0.90, 0)



    # MO alta reduz necessidade de N (mineralizaÃÂÃÂ§ÃÂÃÂ£o)

    if materia_organica >= 5.5:   n = round(n * 0.70, 1)

    elif materia_organica >= 4.0: n = round(n * 0.80, 1)

    elif materia_organica >= 3.0: n = round(n * 0.90, 1)



    # pH baixo reduz disponibilidade de P (precipitaÃÂÃÂ§ÃÂÃÂ£o com Al e Fe)

    if ph < 5.0:   p2o5 = round(p2o5 * 1.30, 0)

    elif ph < 5.3: p2o5 = round(p2o5 * 1.15, 0)

    elif ph < 5.5: p2o5 = round(p2o5 * 1.08, 0)



    return round(n, 1), round(p2o5, 1), round(k2o, 1)





def score_solo(d, cultura="Soja"):

    """

    Score de qualidade do solo baseado nos parÃÂÃÂ¢metros EMBRAPA/CQFS RS-SC 2016

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

        "FeijÃÂÃÂ£o": (6.0, 6.5), "Arroz": (5.5, 6.0), "Canola": (6.0, 6.5),

        "CafÃÂÃÂ©": (5.5, 6.5), "Tomate": (6.0, 6.8), "Batata": (5.5, 6.0),

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

            score -= 10; alertas.append(f"pH elevado ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ risco de deficiÃÂÃÂªncia de micronutrientes")



    # FÃÂÃÂ³sforo (mg/dmÃÂÃÂ³ ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Mehlich-1)

    if fosforo > 0:

        if   fosforo < 6:   score -= 20; alertas.append("FÃÂÃÂ³sforo muito baixo (<6 mg/dmÃÂÃÂ³)")

        elif fosforo < 12:  score -= 12; alertas.append("FÃÂÃÂ³sforo baixo (6-12 mg/dmÃÂÃÂ³)")

        elif fosforo < 18:  score -= 6;  alertas.append("FÃÂÃÂ³sforo mÃÂÃÂ©dio ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ atenÃÂÃÂ§ÃÂÃÂ£o")



    # PotÃÂÃÂ¡ssio (mg/dmÃÂÃÂ³)

    if potassio > 0:

        if   potassio < 60:  score -= 20; alertas.append("PotÃÂÃÂ¡ssio muito baixo (<60 mg/dmÃÂÃÂ³)")

        elif potassio < 100: score -= 12; alertas.append("PotÃÂÃÂ¡ssio baixo (60-100 mg/dmÃÂÃÂ³)")

        elif potassio < 150: score -= 5;  alertas.append("PotÃÂÃÂ¡ssio mÃÂÃÂ©dio ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ monitorar")



    # CÃÂÃÂ¡lcio (cmolc/dmÃÂÃÂ³)

    if calcio > 0:

        if   calcio < 2.0: score -= 20; alertas.append("CÃÂÃÂ¡lcio muito baixo (<2 cmolc/dmÃÂÃÂ³)")

        elif calcio < 3.5: score -= 10; alertas.append("CÃÂÃÂ¡lcio baixo (2-3,5 cmolc/dmÃÂÃÂ³)")



    # MagnÃÂÃÂ©sio (cmolc/dmÃÂÃÂ³)

    if magnesio > 0:

        if   magnesio < 0.5: score -= 15; alertas.append("MagnÃÂÃÂ©sio muito baixo (<0,5 cmolc/dmÃÂÃÂ³)")

        elif magnesio < 1.0: score -= 8;  alertas.append("MagnÃÂÃÂ©sio baixo (0,5-1,0 cmolc/dmÃÂÃÂ³)")



    # RelaÃÂÃÂ§ÃÂÃÂ£o Ca:Mg ideal 3:1 a 5:1

    if calcio > 0 and magnesio > 0:

        rel = calcio / magnesio

        if rel < 2.5: alertas.append(f"RelaÃÂÃÂ§ÃÂÃÂ£o Ca:Mg baixa ({rel:.1f}:1) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ risco de toxidez Mg")

        elif rel > 8:  alertas.append(f"RelaÃÂÃÂ§ÃÂÃÂ£o Ca:Mg alta ({rel:.1f}:1) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ deficiÃÂÃÂªncia Mg possÃÂÃÂ­vel")



    # AlumÃÂÃÂ­nio (cmolc/dmÃÂÃÂ³) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ tÃÂÃÂ³xico acima de 0,3

    if aluminio > 0:

        if aluminio > 1.0: score -= 25; alertas.append(f"AlumÃÂÃÂ­nio tÃÂÃÂ³xico ({aluminio} cmolc/dmÃÂÃÂ³) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ urgente calcÃÂÃÂ¡rio")

        elif aluminio > 0.5: score -= 15; alertas.append(f"AlumÃÂÃÂ­nio elevado ({aluminio} cmolc/dmÃÂÃÂ³)")

        elif aluminio > 0.3: score -= 8;  alertas.append(f"AlumÃÂÃÂ­nio detectado ({aluminio} cmolc/dmÃÂÃÂ³)")



    # MatÃÂÃÂ©ria orgÃÂÃÂ¢nica (%)

    if materia_organica > 0:

        if   materia_organica < 1.5: score -= 15; alertas.append("MO muito baixa (<1,5%) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ solo degradado")

        elif materia_organica < 2.5: score -= 8;  alertas.append("MO baixa (1,5-2,5%) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ adubaÃÂÃÂ§ÃÂÃÂ£o verde recomendada")

        elif materia_organica > 6.0: alertas.append("MO alta ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ reduzir N mineral")



    # Micronutrientes (quando disponÃÂÃÂ­veis)

    if enxofre > 0 and enxofre < 5:

        score -= 8; alertas.append(f"Enxofre baixo (<5 mg/dmÃÂÃÂ³) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ usar fertilizante com S")

    if zinco > 0 and zinco < 0.6:

        score -= 5; alertas.append(f"Zinco baixo (<0,6 mg/dmÃÂÃÂ³)")

    if boro > 0 and boro < 0.2:

        score -= 5; alertas.append(f"Boro baixo (<0,2 mg/dmÃÂÃÂ³) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ importante para soja/cafÃÂÃÂ©")



    score = max(0, min(100, score))

    if   score >= 85: classe = "Excelente"

    elif score >= 70: classe = "Boa"

    elif score >= 50: classe = "MÃÂÃÂ©dia"

    elif score >= 30: classe = "Fraca"

    else:             classe = "CrÃÂÃÂ­tica"

    return score, classe, alertas





def baixar_estoque(nome_insumo, quantidade_usada, unidade_usada="L/ha"):

    """

    DÃÂÃÂ¡ baixa no estoque convertendo unidades automaticamente.

    Estoque sempre em L ou kg. AplicaÃÂÃÂ§ÃÂÃÂ£o pode ser mL/ha, g/ha, etc.

    """

    def converter_para_base(qtd, unid):

        """Converte para a unidade base: L ou kg."""

        unid = (unid or "").lower().replace(" ", "")

        if "ml" in unid:     return qtd / 1000  # mL ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ L

        if "g/ha" in unid or unid == "g":   return qtd / 1000  # g ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ kg

        if "mg" in unid:     return qtd / 1_000_000

        return qtd  # jÃÂÃÂ¡ em L ou kg



    qtd_convertida = converter_para_base(quantidade_usada, unidade_usada)



    for item in st.session_state.estoque:

        if item["Insumo"] == nome_insumo:

            estoque_atual = float(item.get("Quantidade", 0))

            if estoque_atual >= qtd_convertida:

                item["Quantidade"] = round(estoque_atual - qtd_convertida, 4)

                item["Valor Total R$"] = item["Quantidade"] * item.get("Valor UnitÃÂÃÂ¡rio R$", 0)

                return True, f"Baixa de {qtd_convertida:.3f} realizada."

            return False, f"Estoque insuficiente: tem {estoque_atual:.3f}, precisa {qtd_convertida:.3f}"

    return False, "Insumo nÃÂÃÂ£o encontrado no estoque."





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

menu = st.sidebar.radio(

    "ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Menu",

    [

        "ÃÂ°ÃÂ¸ÃÂÃÂ  InÃÂÃÂ­cio",

        "ÃÂ°ÃÂ¸ÃÂÃÂ¾ Lavoura",

        "ÃÂ°ÃÂ¸ÃÂ§ÃÂª Solo & AdubaÃÂÃÂ§ÃÂÃÂ£o",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Financeiro",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ Operacional",

        "ÃÂ°ÃÂ¸ÃÂÃÂ InteligÃÂÃÂªncia",

        "ÃÂ°ÃÂ¸ÃÂÃÂ± Safrinha",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ RelatÃÂÃÂ³rio Final",

        "ÃÂ¢ÃÂ¡Ã¢ÂÂ¢ÃÂ¯ÃÂ¸ÃÂ ConfiguraÃÂÃÂ§ÃÂÃÂµes"

    ]

)



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Backup rÃÂÃÂ¡pido na sidebar ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

st.sidebar.divider()

backup_bytes = gerar_backup()

st.sidebar.download_button(

    "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Baixar Backup",

    data=backup_bytes,

    file_name=f"iaagro_backup_{date.today()}.json",

    mime="application/json",

    use_container_width=True

)



if st.session_state.area_selecionada:

    st.sidebar.markdown(f'<div style="background:#14532d;color:#fff;padding:8px 12px;border-radius:8px;font-weight:700;font-size:13px;margin-top:6px;">ÃÂ°ÃÂ¸ÃÂÃÂ¾ ÃÂÃÂrea ativa: {st.session_state.area_selecionada}</div>', unsafe_allow_html=True)



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MAPEAMENTO GLOBAL DE CULTURAS POR SEGMENTO

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

SEGMENTOS_INFO = {

    "ÃÂ°ÃÂ¸ÃÂÃÂ¾ GrÃÂÃÂ£os":        {"desc":"Soja, Milho, Trigo e outros cereais",   "cor":"#14532d","borda":"#22c55e"},

    "ÃÂ°ÃÂ¸ÃÂÃÂ¿ Horticultura": {"desc":"HortaliÃÂÃÂ§as, verduras e legumes",         "cor":"#14532d","borda":"#84cc16"},

    "ÃÂ°ÃÂ¸ÃÂÃÂ½ Fruticultura": {"desc":"Frutas tropicais, uva, cafÃÂÃÂ© e outras",  "cor":"#7f1d1d","borda":"#f87171"},

    "ÃÂ°ÃÂ¸ÃÂÃÂ² Silvicultura": {"desc":"Eucalipto, Pinus e reflorestamento",     "cor":"#1e3a5f","borda":"#38bdf8"},

}



CULTURAS_POR_SEGMENTO = {

    "ÃÂ°ÃÂ¸ÃÂÃÂ¾ GrÃÂÃÂ£os":        ["ÃÂ°ÃÂ¸ÃÂÃÂ± Soja","ÃÂ°ÃÂ¸ÃÂÃÂ½ Milho","ÃÂ°ÃÂ¸ÃÂÃÂ¾ Trigo","ÃÂ°ÃÂ¸ÃÂÃÂ± FeijÃÂÃÂ£o","ÃÂ°ÃÂ¸ÃÂÃÂ» Canola","ÃÂ°ÃÂ¸ÃÂÃÂ¿ Aveia","ÃÂ°ÃÂ¸ÃÂÃÂ¡ Arroz","ÃÂ°ÃÂ¸ÃÂÃÂ¾ Sorgo","ÃÂ°ÃÂ¸ÃÂÃÂ¾ Cevada","ÃÂ°ÃÂ¸ÃÂÃÂ» Girassol"],

    "ÃÂ°ÃÂ¸ÃÂÃÂ¿ Horticultura": ["ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ¦ Tomate","ÃÂ°ÃÂ¸ÃÂ¥Ã¢ÂÂ Batata","ÃÂ°ÃÂ¸ÃÂ§Ã¢ÂÂ¦ Cebola","ÃÂ°ÃÂ¸ÃÂ§Ã¢ÂÂ Alho","ÃÂ°ÃÂ¸ÃÂÃÂ  Mandioca"],

    "ÃÂ°ÃÂ¸ÃÂÃÂ½ Fruticultura": ["ÃÂ°ÃÂ¸ÃÂÃÂ  Laranja","ÃÂ°ÃÂ¸ÃÂÃÂ Banana","ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ¡ Uva","ÃÂ°ÃÂ¸ÃÂÃÂ½ MaÃÂÃÂ§ÃÂÃÂ£","ÃÂ°ÃÂ¸ÃÂ¥ÃÂ­ Manga","ÃÂ°ÃÂ¸ÃÂ¥Ã¢ÂÂ Abacate","ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ¹ LimÃÂÃÂ£o","ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ PÃÂÃÂªssego","ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ Caqui","ÃÂ¢ÃÂÃ¢ÂÂ¢ CafÃÂÃÂ©"],

    "ÃÂ°ÃÂ¸ÃÂÃÂ² Silvicultura": ["ÃÂ°ÃÂ¸ÃÂÃÂ³ Eucalipto","ÃÂ°ÃÂ¸ÃÂÃÂ² Pinus","ÃÂ°ÃÂ¸ÃÂÃÂ´ Teca","ÃÂ°ÃÂ¸ÃÂÃÂ¿ ParicÃÂÃÂ¡","ÃÂ°ÃÂ¸ÃÂÃÂ² Cedro"],

}



# Mapa reverso para extrair nome sem ÃÂÃÂ­cone (para lÃÂÃÂ³gicas internas)

CULTURA_NOME_LIMPO = {c: c.split(" ",1)[1] if " " in c else c

                      for seg in CULTURAS_POR_SEGMENTO.values() for c in seg}



# ÃÂÃÂcone por nome limpo da cultura

CULTURA_ICONE = {c.split(" ",1)[1] if " " in c else c: c.split(" ",1)[0] if " " in c else "ÃÂ°ÃÂ¸ÃÂÃÂ±"

                 for seg in CULTURAS_POR_SEGMENTO.values() for c in seg}



def get_icone_cultura(cultura):

    """Retorna o ÃÂÃÂ­cone da cultura (com ou sem ÃÂÃÂ­cone no nome)."""

    if not cultura: return "ÃÂ°ÃÂ¸ÃÂÃÂ±"

    nome = cultura_limpa(cultura)

    return CULTURA_ICONE.get(nome, "ÃÂ°ÃÂ¸ÃÂÃÂ±")



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# CONTROLE DE PLANOS ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Free / Pro / Premium

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬



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

    """Banner de upgrade quando limite ÃÂÃÂ© atingido."""

    plano_key = st.session_state.get("sb_plano", "free")

    nomes     = {"areas": "ÃÂÃÂ¡reas", "estoque": "itens de estoque"}

    nome      = nomes.get(recurso, recurso)



    # PrÃÂÃÂ³ximo plano sugerido

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

    <b style='color:#fbbf24;font-size:16px;'>ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Limite atingido ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {usado}/{limite} {nome}</b><br>

    <span style='color:#fde68a;font-size:13px;'>

    FaÃÂÃÂ§a upgrade para continuar usando o IAAGRO sem limites!

    </span><br><br>

    <span style='color:#fff;font-size:18px;font-weight:800;'>

    {prox_nome} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ R$ {prox_preco:.2f}/mÃÂÃÂªs

    </span>

    </div>

    """, unsafe_allow_html=True)



    msg = f"Quero+assinar+o+IAAGRO+{prox_nome.replace(' ','+')}+-+R$+{prox_preco:.2f}/mes"

    # Links direto do Mercado Pago ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ mensal e anual

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

    ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ³ Mensal<br>R$ {prox_preco:.2f}/mÃÂÃÂªs

    </a>

    <a href='{link_ano}' target='_blank'

       style='flex:1;display:block;background:#00a650;color:#fff;text-align:center;

       padding:10px;border-radius:8px;font-weight:700;text-decoration:none;font-size:13px;'>

    ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ  Anual<br>R$ {preco_ano:.0f}/ano<br><span style='font-size:10px;'>(-15% desconto)</span>

    </a>

    </div>

    <div style='text-align:center;margin-top:4px;'>

    <span style='color:#94a3b8;font-size:11px;'>PIX ÃÂ¢Ã¢ÂÂ¬ÃÂ¢ CartÃÂÃÂ£o ÃÂ¢Ã¢ÂÂ¬ÃÂ¢ Boleto ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Mercado Pago</span>

    </div>

    """, unsafe_allow_html=True)



def get_culturas():

    """Retorna lista de culturas (com ÃÂÃÂ­cone) filtrada pelo segmento ativo."""

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

    """Remove ÃÂÃÂ­cone do nome da cultura para usar nas lÃÂÃÂ³gicas internas."""

    if c and " " in c and len(c.split(" ",1)[0]) <= 2:

        return c.split(" ",1)[1]

    return c



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: INÃÂÃÂCIO

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸ÃÂÃÂ  InÃÂÃÂ­cio":



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Segmentos disponÃÂÃÂ­veis ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    SEGMENTOS = SEGMENTOS_INFO



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Tela de seleÃÂÃÂ§ÃÂÃÂ£o (sÃÂÃÂ³ aparece se segmento nÃÂÃÂ£o foi escolhido ainda) ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    if not st.session_state.segmento:

        st.markdown("""

        <div style='text-align:center;padding:30px 0 10px 0;'>

        <span style='font-size:48px;'>ÃÂ°ÃÂ¸ÃÂÃÂ±</span><br>

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

                    st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ Segmento **{seg}** selecionado! Bem-vindo.")

                    st.rerun()

            with col_desc:

                st.markdown(

                    f"<div style='padding:10px 0;color:#94a3b8;font-size:14px;'>{info['desc']}</div>",

                    unsafe_allow_html=True

                )



        st.markdown("<br>", unsafe_allow_html=True)

        st.caption("ÃÂ¢ÃÂ¡Ã¢ÂÂ¢ÃÂ¯ÃÂ¸ÃÂ VocÃÂÃÂª pode trocar o segmento a qualquer momento em ConfiguraÃÂÃÂ§ÃÂÃÂµes.")



    else:

        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Dashboard principal apÃÂÃÂ³s segmento selecionado ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        seg_info = SEGMENTOS.get(st.session_state.segmento, {"cor":"#0f3460","borda":"#22c55e","desc":""})



        col_banner, col_trocar = st.columns([5, 1])

        with col_banner:

            st.markdown(f"""

            <div style='background:{seg_info["cor"]};border-radius:12px;padding:14px 20px;

            border-left:5px solid {seg_info["borda"]};margin-bottom:8px;'>

            <span style='font-size:22px;font-weight:800;color:#f1f5f9;'>ÃÂ°ÃÂ¸ÃÂ¡ÃÂ IAAGRO ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {st.session_state.segmento}</span><br>

            <span style='font-size:13px;color:#94a3b8;'>{seg_info["desc"]}</span>

            </div>

            """, unsafe_allow_html=True)

        with col_trocar:

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Trocar\nsegmento", key="btn_trocar_segmento", use_container_width=True):

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

        _bar_ar     = f"{_areas_us}/{_lim_ar}" if _lim_ar != -1 else f"{_areas_us}/ÃÂ¢ÃÂÃÂ¾"

        _bar_est    = f"{_est_us}/{_lim_est}"  if _lim_est != -1 else f"{_est_us}/ÃÂ¢ÃÂÃÂ¾"



        st.markdown(f"""

        <div style='background:linear-gradient(135deg,{_plano_info["cor"]},{_plano_info["cor"]}cc);

        border-radius:12px;padding:12px 18px;border:1px solid {_plano_info["borda"]};margin-bottom:12px;'>

        <span style='color:{_plano_info["borda"]};font-weight:800;font-size:15px;'>{_plano_info["nome"]}</span>

        <span style='color:#94a3b8;font-size:12px;float:right;'>

        ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ {_bar_ar} ÃÂÃÂ¡reas &nbsp;|&nbsp; ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ {_bar_est} insumos

        </span><br>

        {"<span style='color:#d1fae5;font-size:12px;'>ÃÂ¢ÃÂÃ¢ÂÂ¦ Acesso completo ativo</span>" if _plano_key == "premium" else

         f"<span style='color:#fde68a;font-size:12px;'>Upgrade para mais recursos ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ <b>R$ {PLANOS['pro' if _plano_key=='free' else 'premium']['preco']:.2f}/mÃÂÃÂªs</b></span>"}

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

            ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ³ Mensal R$ {_prox['preco']:.2f}

            </a>

            <a href='{_lano}' target='_blank'

            style='flex:1;display:block;background:#00a650;color:#fff;text-align:center;

            padding:8px;border-radius:8px;font-weight:700;text-decoration:none;font-size:12px;'>

            ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ  Anual R$ {_pano:.0f}

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

        col1.metric("ÃÂ°ÃÂ¸ÃÂÃÂ¾ ÃÂÃÂreas",      total_areas)

        col2.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ Estoque",    total_estoque)

        col3.metric("ÃÂ°ÃÂ¸ÃÂ¡ÃÂ AplicaÃÂÃÂ§ÃÂÃÂµes", total_aplicacoes)

        col4.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ ÃÂÃÂrea Total", f"{area_total:.1f} ha")



        st.divider()



        col5, col6 = st.columns(2)

        with col5:

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Produtividade MÃÂÃÂ©dia")

            st.metric("MÃÂÃÂ©dia", f"{produtividade_media:.1f} sc/ha")

        with col6:

            st.subheader("ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Alertas de Estoque")

            estoque_baixo = [i for i in st.session_state.estoque if i.get("Quantidade", 0) < 10]

            if not estoque_baixo:

                st.markdown('<div style="background:#166534;color:#fff;padding:12px 18px;border-radius:10px;font-weight:700;">ÃÂ¢ÃÂÃ¢ÂÂ¦ Nenhum alerta de estoque.</div>', unsafe_allow_html=True)

            else:

                for item in estoque_baixo:

                    nome = item.get("Insumo", item.get("Produto", "Produto"))

                    st.markdown(f'<div style="background:#92400e;color:#fff;padding:10px 16px;border-radius:10px;font-weight:700;margin-bottom:4px;">ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ {nome} com estoque baixo.</div>', unsafe_allow_html=True)



        st.divider()

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Resumo das ÃÂÃÂreas")

        if total_areas == 0:

            st.markdown('<div style="background:#1e3a5f;color:#fff;padding:14px 18px;border-radius:10px;font-weight:600;">ÃÂ¢Ã¢ÂÂÃÂ¹ÃÂ¯ÃÂ¸ÃÂ Nenhuma ÃÂÃÂ¡rea cadastrada. VÃÂÃÂ¡ em <b>Cadastro da ÃÂÃÂrea</b> para comeÃÂÃÂ§ar.</div>', unsafe_allow_html=True)

        else:

            tabela_dashboard = [{

                "Fazenda":    a.get("Fazenda",""),

                "TalhÃÂÃÂ£o":     a.get("TalhÃÂÃÂ£o",""),

                "Cultura":    a.get("Cultura",""),

                "ÃÂÃÂrea ha":    a.get("Hectares",0),

                "Meta sc/ha": a.get("Meta Produtividade",0),

            } for a in st.session_state.areas]

            df_areas = pd.DataFrame(tabela_dashboard)

            st.dataframe(df_areas, use_container_width=True)

            st.divider()

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Produtividade por TalhÃÂÃÂ£o")

            st.bar_chart(df_areas.set_index("TalhÃÂÃÂ£o")["Meta sc/ha"])



        if total_estoque > 0:

            df_estoque = pd.DataFrame(st.session_state.estoque)

            if "Insumo" in df_estoque.columns and "Quantidade" in df_estoque.columns:

                st.divider()

                st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ Estoque por Produto")

                st.bar_chart(df_estoque.set_index("Insumo")["Quantidade"])





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: ÃÂÃÂREAS CADASTRADAS

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

elif menu == "ÃÂ°ÃÂ¸ÃÂÃÂ¾ Lavoura":

    _sub_lav = st.tabs(["ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Cadastro da ÃÂÃÂrea","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ ÃÂÃÂreas Cadastradas","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂºÃÂ¯ÃÂ¸ÃÂ Mapa de Fertilidade","ÃÂ°ÃÂ¸ÃÂÃÂ§ÃÂ¯ÃÂ¸ÃÂ PluviÃÂÃÂ´metro","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ HistÃÂÃÂ³rico de Produtividade"])



if menu == "ÃÂ°ÃÂ¸ÃÂÃÂ¾ Lavoura":

  with _sub_lav[1]:

    st.header("ÃÂÃÂreas Cadastradas")



    if len(st.session_state.areas) == 0:

        st.markdown('<div style="background:#1e3a5f;color:#ffffff;padding:14px 18px;border-radius:10px;font-weight:600;font-size:15px;border:1px solid #3b82f6;">ÃÂ¢Ã¢ÂÂÃÂ¹ÃÂ¯ÃÂ¸ÃÂ Nenhuma ÃÂÃÂ¡rea cadastrada ainda.</div>', unsafe_allow_html=True)

    else:

        tabela_areas = pd.DataFrame([

            {

                "ID":               a["ID"],

                "Fazenda":          a["Fazenda"],

                "TalhÃÂÃÂ£o":          a["TalhÃÂÃÂ£o"],

                "Matricula":        a.get("Matricula", ""),

                "Cidade/Estado":    a["Cidade/Estado"],

                "Hectares":         a["Hectares"],

                "Cultura":          a["Cultura"],

                "Meta Produtividade": a["Meta Produtividade"]

            }

            for a in st.session_state.areas

        ])

        st.dataframe(tabela_areas, use_container_width=True)



        opcoes = [f"{area['ID']} - {area['TalhÃÂÃÂ£o']} - {area['Cultura']}" for area in st.session_state.areas]

        escolha = st.selectbox("Selecionar ÃÂÃÂ¡rea para trabalhar", opcoes, key="sel_selecionar__rea_2910")



        if st.button("Carregar ÃÂÃÂrea Selecionada"):

            indice = opcoes.index(escolha)

            area   = st.session_state.areas[indice]

            st.session_state.id_area          = area["ID"]

            st.session_state.area_selecionada = area["ID"]

            # Carrega dados completos da ÃÂÃÂ¡rea (inclui anÃÂÃÂ¡lise de solo)

            _dados_area = area.get("Dados", area.get("dados", {}))

            st.session_state.dados = _dados_area.copy() if _dados_area else {}

            if "id_area" not in st.session_state.dados:

                st.session_state.dados["id_area"] = area["ID"]

            # Garante que campos da ÃÂÃÂ¡rea estejam nos dados

            st.session_state.dados.update({

                "cultura":       area.get("Cultura", st.session_state.dados.get("cultura","Soja")),

                "area":          area.get("Hectares", st.session_state.dados.get("area",0)),

                "produtividade": area.get("Produtividade", st.session_state.dados.get("produtividade",50)),

                "fazenda":       area.get("Fazenda", st.session_state.dados.get("fazenda","")),

                "talhao":        area.get("TalhÃÂÃÂ£o", st.session_state.dados.get("talhao","")),

            })

            st.session_state.aplicacoes = area.get("Aplicacoes", []).copy()

            st.session_state.estoque    = area.get("Estoque", []).copy()

            salvar_dados_iaagro()

            success_box(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ ÃÂÃÂrea {area['ID']} carregada! {('AnÃÂÃÂ¡lise de solo disponÃÂÃÂ­vel ÃÂ¢ÃÂÃ¢ÂÂ¦' if 'ph' in st.session_state.dados else 'Sem anÃÂÃÂ¡lise de solo ainda.')}")

            st.rerun()



        st.divider()

        st.subheader("Excluir ÃÂÃÂrea Individual")

        opcao_excluir = st.selectbox(

            "Escolha a ÃÂÃÂ¡rea para excluir",

            [f"{area['ID']} - {area['TalhÃÂÃÂ£o']} - {area['Cultura']}" for area in st.session_state.areas],

            key="excluir_area_select"

        )

        if st.button("Excluir ÃÂÃÂrea Selecionada", key="excluir_area_btn"):

            indice_excluir = [

                f"{area['ID']} - {area['TalhÃÂÃÂ£o']} - {area['Cultura']}"

                for area in st.session_state.areas

            ].index(opcao_excluir)

            area_excluida = st.session_state.areas[indice_excluir]["ID"]

            st.session_state.areas.pop(indice_excluir)

            if st.session_state.area_selecionada == area_excluida:

                st.session_state.area_selecionada = None

                st.session_state.dados = {}

            salvar_dados_iaagro()

            success_box(f"ÃÂÃÂrea {area_excluida} excluÃÂÃÂ­da com sucesso.")

            st.rerun()



        if st.button("Apagar Todas as ÃÂÃÂreas"):

            st.session_state.areas = []

            st.session_state.dados = {}

            st.session_state.area_selecionada = None

            salvar_dados_iaagro()

            warning_box("Todas as ÃÂÃÂ¡reas foram apagadas.")



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: CADASTRO DA ÃÂÃÂREA

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸ÃÂÃÂ¾ Lavoura":

  with _sub_lav[0]:

    st.header("Cadastro da ÃÂÃÂrea")



    fazenda   = st.text_input("Nome da fazenda",  st.session_state.dados.get("fazenda", ""), key="txt_nome_da_fazenda_2960")

    talhao    = st.text_input("Nome do talhÃÂÃÂ£o",   st.session_state.dados.get("talhao", ""), key="txt_nome_do_talh_o_2961")

    matricula = st.text_input("MatrÃÂÃÂ­cula da ÃÂÃÂrea", st.session_state.dados.get("matricula", ""), key="txt_matr_cula_da__r_2962")

    cidade    = st.text_input("Cidade / Estado",   st.session_state.dados.get("cidade", ""), key="txt_cidade___estado_2963")

    area      = st.number_input("ÃÂÃÂrea do talhÃÂÃÂ£o em hectares", min_value=0.0,

                                value=float(st.session_state.dados.get("area", 10.0)))



    culturas_disponiveis = get_culturas()

    config_culturas = {

        "Soja":          {"ph_ideal":"5.8 - 6.5","chuva_ideal":"450 - 800 mm","produtividade_media":65,"nutriente_principal":"PotÃÂÃÂ¡ssio"},

        "Milho":         {"ph_ideal":"5.5 - 6.8","chuva_ideal":"500 - 800 mm","produtividade_media":180,"nutriente_principal":"NitrogÃÂÃÂªnio"},

        "Trigo":         {"ph_ideal":"5.5 - 6.2","chuva_ideal":"350 - 600 mm","produtividade_media":55,"nutriente_principal":"NitrogÃÂÃÂªnio"},

        "FeijÃÂÃÂ£o":        {"ph_ideal":"5.8 - 6.5","chuva_ideal":"300 - 500 mm","produtividade_media":45,"nutriente_principal":"FÃÂÃÂ³sforo"},

        "Canola":        {"ph_ideal":"5.5 - 6.2","chuva_ideal":"400 - 700 mm","produtividade_media":40,"nutriente_principal":"Enxofre"},

        "Aveia":         {"ph_ideal":"5.2 - 6.0","chuva_ideal":"300 - 550 mm","produtividade_media":70,"nutriente_principal":"NitrogÃÂÃÂªnio"},

        "Cana-de-aÃÂÃÂ§ÃÂÃÂºcar":{"ph_ideal":"5.5 - 6.5","chuva_ideal":"1200 - 1800 mm","produtividade_media":90,"nutriente_principal":"PotÃÂÃÂ¡ssio"},

        "Arroz":         {"ph_ideal":"5.0 - 6.0","chuva_ideal":"900 - 1300 mm","produtividade_media":160,"nutriente_principal":"NitrogÃÂÃÂªnio"},

        "Sorgo":         {"ph_ideal":"5.5 - 6.5","chuva_ideal":"350 - 650 mm","produtividade_media":120,"nutriente_principal":"NitrogÃÂÃÂªnio"},

        "Girassol":      {"ph_ideal":"5.5 - 6.8","chuva_ideal":"400 - 700 mm","produtividade_media":35,"nutriente_principal":"Boro"},

        "Cevada":        {"ph_ideal":"5.5 - 6.5","chuva_ideal":"350 - 600 mm","produtividade_media":60,"nutriente_principal":"NitrogÃÂÃÂªnio"},

        "Pastagem":      {"ph_ideal":"5.0 - 6.5","chuva_ideal":"500 - 1200 mm","produtividade_media":0,"nutriente_principal":"NitrogÃÂÃÂªnio"},

        "AlgodÃÂÃÂ£o":       {"ph_ideal":"5.5 - 6.5","chuva_ideal":"700 - 1300 mm","produtividade_media":300,"nutriente_principal":"PotÃÂÃÂ¡ssio"},

        "CafÃÂÃÂ©":          {"ph_ideal":"5.5 - 6.5","chuva_ideal":"1200 - 1800 mm","produtividade_media":35,"nutriente_principal":"NitrogÃÂÃÂªnio"},

        "Tabaco":        {"ph_ideal":"5.2 - 6.2","chuva_ideal":"600 - 1000 mm","produtividade_media":2500,"nutriente_principal":"PotÃÂÃÂ¡ssio"},

        "Mandioca":      {"ph_ideal":"5.0 - 6.5","chuva_ideal":"800 - 1500 mm","produtividade_media":25,"nutriente_principal":"PotÃÂÃÂ¡ssio"},

        "Batata":        {"ph_ideal":"5.0 - 6.0","chuva_ideal":"500 - 700 mm","produtividade_media":35,"nutriente_principal":"PotÃÂÃÂ¡ssio"},

        "Tomate":        {"ph_ideal":"5.5 - 6.8","chuva_ideal":"400 - 800 mm","produtividade_media":80,"nutriente_principal":"PotÃÂÃÂ¡ssio"},

        "Cebola":        {"ph_ideal":"6.0 - 6.8","chuva_ideal":"350 - 650 mm","produtividade_media":40,"nutriente_principal":"PotÃÂÃÂ¡ssio"},

        "Alho":          {"ph_ideal":"6.0 - 7.0","chuva_ideal":"300 - 500 mm","produtividade_media":12,"nutriente_principal":"Enxofre"},

        "Uva":           {"ph_ideal":"5.5 - 6.5","chuva_ideal":"500 - 900 mm","produtividade_media":25,"nutriente_principal":"PotÃÂÃÂ¡ssio"},

        "MaÃÂÃÂ§ÃÂÃÂ£":          {"ph_ideal":"5.5 - 6.5","chuva_ideal":"700 - 1200 mm","produtividade_media":45,"nutriente_principal":"CÃÂÃÂ¡lcio"},

        "Laranja":       {"ph_ideal":"5.5 - 6.5","chuva_ideal":"1000 - 1500 mm","produtividade_media":35,"nutriente_principal":"PotÃÂÃÂ¡ssio"},

        "Banana":        {"ph_ideal":"5.5 - 7.0","chuva_ideal":"1200 - 2000 mm","produtividade_media":45,"nutriente_principal":"PotÃÂÃÂ¡ssio"},

        "Eucalipto":     {"ph_ideal":"5.0 - 6.5","chuva_ideal":"800 - 1500 mm","produtividade_media":40,"nutriente_principal":"FÃÂÃÂ³sforo"},

        "Pinus":         {"ph_ideal":"4.5 - 6.0","chuva_ideal":"700 - 1400 mm","produtividade_media":35,"nutriente_principal":"FÃÂÃÂ³sforo"},

    }



    cultura_atual = st.session_state.dados.get("cultura", "Soja")

    idx_cultura   = culturas_disponiveis.index(cultura_atual) if cultura_atual in culturas_disponiveis else 0

    cultura       = st.selectbox("Cultura", culturas_disponiveis, index=idx_cultura, key="cultura_area")



    info = config_culturas.get(cultura, {"ph_ideal":"NÃÂÃÂ£o definido","chuva_ideal":"NÃÂÃÂ£o definido","produtividade_media":0,"nutriente_principal":"NÃÂÃÂ£o definido"})

    st.markdown(f"""

    <div style="background:#0f3460;color:#ffffff;padding:14px 18px;border-radius:12px;

                border:1px solid #3b82f6;font-size:15px;font-weight:600;line-height:2;">

        ÃÂ°ÃÂ¸ÃÂÃÂ± <b>Cultura:</b> {cultura} &nbsp;|&nbsp;

        ÃÂ°ÃÂ¸ÃÂ§ÃÂª <b>pH ideal:</b> {info['ph_ideal']} &nbsp;|&nbsp;

        ÃÂ°ÃÂ¸ÃÂÃÂ§ÃÂ¯ÃÂ¸ÃÂ <b>Chuva ideal:</b> {info['chuva_ideal']}<br>

        ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ <b>Produtividade mÃÂÃÂ©dia:</b> {info['produtividade_media']} &nbsp;|&nbsp;

        ÃÂ°ÃÂ¸ÃÂ§ÃÂ¬ <b>Nutriente principal:</b> {info['nutriente_principal']}

    </div>

    """, unsafe_allow_html=True)



    produtividade = st.number_input("Meta de produtividade em sacas/ha", min_value=0.0,

                                    value=float(st.session_state.dados.get("produtividade", 60.0)))



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ GeolocalizaÃÂÃÂ§ÃÂÃÂ£o com tratamento robusto ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    # Inicializa com coordenadas salvas ou padrÃÂÃÂ£o Brasil-Sul

    latitude  = st.session_state.dados.get("latitude",  -26.88)

    longitude = st.session_state.dados.get("longitude", -52.40)



    col_geo_a, col_geo_b = st.columns([2, 1])

    with col_geo_a:

        latitude  = st.number_input("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Latitude",  value=float(latitude),

                                     format="%.6f", key="cad_lat")

        longitude = st.number_input("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Longitude", value=float(longitude),

                                     format="%.6f", key="cad_lon")

    with col_geo_b:

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¡ Usar GPS do celular", key="btn_gps_cad", use_container_width=True):

            try:

                geo = get_geolocation()

                if geo and geo.get("coords"):

                    st.session_state["_gps_lat"] = geo["coords"]["latitude"]

                    st.session_state["_gps_lon"] = geo["coords"]["longitude"]

                    st.rerun()

            except Exception:

                warning_box("GPS indisponÃÂÃÂ­vel. Insira as coordenadas manualmente.")

        if st.session_state.get("_gps_lat"):

            latitude  = st.session_state["_gps_lat"]

            longitude = st.session_state["_gps_lon"]

            st.markdown(f'<div style="background:#14532d;color:#fff;padding:6px 10px;'

                        f'border-radius:8px;font-size:11px;font-weight:700;">'

                        f'ÃÂ¢ÃÂÃ¢ÂÂ¦ GPS: {latitude:.5f}, {longitude:.5f}</div>',

                        unsafe_allow_html=True)

        st.markdown('<div style="color:#94a3b8;font-size:11px;margin-top:4px;">'

                    'Dica: use Google Maps para obter as coordenadas da ÃÂÃÂ¡rea.</div>',

                    unsafe_allow_html=True)



    pode, usado, limite = verificar_limite("areas")

    if not pode:

        bloco_upgrade("areas", usado, limite)

    elif st.button("Salvar Nova ÃÂÃÂrea"):

        id_area  = f"AREA-{st.session_state.contador_area:03d}"

        nova_area = {

            "ID": id_area,

            "Fazenda": fazenda, "TalhÃÂÃÂ£o": talhao, "Matricula": matricula,

            "Cidade/Estado": cidade, "Hectares": area,

            "Latitude": latitude, "Longitude": longitude,

            "Cultura": cultura, "Meta Produtividade": produtividade,

            "pH":              st.session_state.dados.get("ph", 0),

            "FÃÂÃÂ³sforo":         st.session_state.dados.get("fosforo", 0),

            "PotÃÂÃÂ¡ssio":        st.session_state.dados.get("potassio", 0),

            "MatÃÂÃÂ©ria OrgÃÂÃÂ¢nica": st.session_state.dados.get("materia_organica", 0),

            "SaturaÃÂÃÂ§ÃÂÃÂ£o Base":  st.session_state.dados.get("saturacao_bases", 0),

            "CalcÃÂÃÂ¡rio t/ha":   st.session_state.dados.get("dose_calcario", 0),

            "Gesso t/ha":      st.session_state.dados.get("dose_gesso", 0),

            "Prioridade":      st.session_state.dados.get("prioridade", "MÃÂÃÂ©dia"),

            "Zona":            st.session_state.dados.get("zona_produtividade", "MÃÂÃÂ©dia"),

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

        success_box(f"ÃÂÃÂrea cadastrada com sucesso. ID gerado: {id_area}")



    if st.session_state.area_selecionada:

        if st.button("Atualizar ÃÂÃÂrea Ativa"):

            st.session_state.dados.update({

                "fazenda": fazenda, "talhao": talhao, "cidade": cidade,

                "area": area, "cultura": cultura, "produtividade": produtividade

            })

            for a in st.session_state.areas:

                if a["ID"] == st.session_state.area_selecionada:

                    a["Fazenda"] = fazenda; a["TalhÃÂÃÂ£o"] = talhao

                    a["Cidade/Estado"] = cidade; a["Hectares"] = area

                    a["Cultura"] = cultura; a["Meta Produtividade"] = produtividade

                    a["Dados"] = st.session_state.dados.copy()

            salvar_dados_iaagro()

            success_box("ÃÂÃÂrea ativa atualizada com sucesso.")



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: HISTÃÂÃ¢ÂÂRICO DE PRODUTIVIDADE

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸ÃÂÃÂ¾ Lavoura":

  with _sub_lav[4]:

    st.header("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ HistÃÂÃÂ³rico de Produtividade")



    if len(st.session_state.areas) == 0:

        warning_box("Cadastre uma ÃÂÃÂ¡rea primeiro.")

    else:

        lista_areas        = [f"{a['ID']} - {a['TalhÃÂÃÂ£o']}" for a in st.session_state.areas]

        area_escolhida     = st.selectbox("Selecione a ÃÂÃÂrea", lista_areas, key="sel_selecione_a__re_3106")

        safra              = st.text_input("Safra", placeholder="2024/2025", key="txt_safra_3107")



        # Cultura colhida ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ com ÃÂÃÂ­cones

        _culturas_hist = get_culturas()

        # Pega cultura da ÃÂÃÂ¡rea selecionada como padrÃÂÃÂ£o

        _id_hist = area_escolhida.split(" - ")[0]

        _area_hist_obj = next((a for a in st.session_state.areas if a.get("ID") == _id_hist), None)

        _cult_padrao = _area_hist_obj.get("Cultura", _culturas_hist[0]) if _area_hist_obj else _culturas_hist[0]

        _idx_cult = _culturas_hist.index(_cult_padrao) if _cult_padrao in _culturas_hist else 0

        cultura_colhida = st.selectbox("Cultura colhida", _culturas_hist,

                                        index=_idx_cult, key="sel_cultura_hist")



        produtividade_real = st.number_input("Produtividade Real (sc/ha)", min_value=0.0, value=60.0, key="num_produtividade_r_3108")

        custo_total        = st.number_input("Custo Total por hectare (R$)", min_value=0.0, value=0.0, key="num_custo_total_por_3109")

        observacoes        = st.text_area("ObservaÃÂÃÂ§ÃÂÃÂµes da Safra", key="txa_observa__es_da__3110")



        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Salvar HistÃÂÃÂ³rico", key="btn_salvar_hist", use_container_width=True):

            st.session_state.historico_produtividade.append({

                "ÃÂÃÂrea": area_escolhida, "Safra": safra,

                "Cultura": cultura_colhida,

                "Produtividade": produtividade_real,

                "Custo": custo_total, "ObservaÃÂÃÂ§ÃÂÃÂµes": observacoes

            })

            salvar_dados_iaagro()

            success_box(f"HistÃÂÃÂ³rico salvo! {get_icone_cultura(cultura_colhida)} {cultura_limpa(cultura_colhida)} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {produtividade_real} sc/ha")

            st.rerun()



        if len(st.session_state.historico_produtividade) > 0:

            df_hist = pd.DataFrame(st.session_state.historico_produtividade)

            if "Cultura" not in df_hist.columns:

                df_hist["Cultura"] = "ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"



            # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BotÃÂÃÂ£o atualizar registro ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

            st.divider()

            st.subheader("ÃÂ¢ÃÂÃÂÃÂ¯ÃÂ¸ÃÂ Atualizar Registro")

            _opcoes_hist = [

                f"{i+1}. {r.get('ÃÂÃÂrea','')} | {r.get('Safra','')} | {cultura_limpa(r.get('Cultura',''))} | {r.get('Produtividade',0)} sc/ha"

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

                _obs_e    = st.text_area("ObservaÃÂÃÂ§ÃÂÃÂµes", value=_reg_edit.get("ObservaÃÂÃÂ§ÃÂÃÂµes",""),

                                          key="txt_hist_obs_edit", height=100)



            col_btn1, col_btn2 = st.columns(2)

            if col_btn1.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Atualizar Registro", key="btn_hist_atualizar", use_container_width=True):

                st.session_state.historico_produtividade[_idx_edit] = {

                    "ÃÂÃÂrea":          _reg_edit.get("ÃÂÃÂrea",""),

                    "Safra":         _safra_e,

                    "Cultura":       _cult_e,

                    "Produtividade": _prod_e,

                    "Custo":         _custo_e,

                    "ObservaÃÂÃÂ§ÃÂÃÂµes":   _obs_e,

                }

                salvar_dados_iaagro()

                success_box("ÃÂ¢ÃÂÃ¢ÂÂ¦ Registro atualizado!")

                st.rerun()



            if col_btn2.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Excluir Registro", key="btn_hist_excluir", use_container_width=True):

                st.session_state.historico_produtividade.pop(_idx_edit)

                salvar_dados_iaagro()

                success_box("Registro excluÃÂÃÂ­do!")

                st.rerun()



            # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Tabela e grÃÂÃÂ¡fico ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

            st.divider()

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Todos os Registros")

            st.dataframe(df_hist, use_container_width=True)

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  EvoluÃÂÃÂ§ÃÂÃÂ£o Produtiva")

            area_filtro = st.selectbox("Filtrar grÃÂÃÂ¡fico por ÃÂÃÂ¡rea", df_hist["ÃÂÃÂrea"].unique(), key="sel_filtrar_gr_fico_3125")

            df_area     = df_hist[df_hist["ÃÂÃÂrea"] == area_filtro]

            grafico     = df_area.pivot_table(index="Safra", values="Produtividade", aggfunc="mean")

            st.line_chart(grafico)

            media_prod  = df_hist["Produtividade"].mean()

            melhor_prod = df_hist["Produtividade"].max()

            custo_medio = df_hist["Custo"].mean()

            col1, col2, col3 = st.columns(3)

            col1.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ MÃÂÃÂ©dia Produtiva", f"{media_prod:.1f} sc/ha")

            col2.metric("ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ  Melhor Safra",    f"{melhor_prod:.1f} sc/ha")

            col3.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Custo MÃÂÃÂ©dio",      f"R$ {custo_medio:.2f}")





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: PLUVIÃÂÃ¢ÂÂMETRO

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸ÃÂÃÂ¾ Lavoura":

  with _sub_lav[3]:

    st.header("ÃÂ°ÃÂ¸ÃÂÃÂ§ÃÂ¯ÃÂ¸ÃÂ PluviÃÂÃÂ´metro Inteligente")



    if len(st.session_state.areas) == 0:

        warning_box("Cadastre uma ÃÂÃÂ¡rea primeiro.")

    else:

        lista_areas   = [f"{a['ID']} - {a['TalhÃÂÃÂ£o']}" for a in st.session_state.areas]

        area_chuva    = st.selectbox("Selecione a ÃÂÃÂrea", lista_areas, key="sel_area_chuva_pluvio")

        id_area_chuva = area_chuva.split(" - ")[0]

        area_obj      = next((a for a in st.session_state.areas if a["ID"] == id_area_chuva), {})

        cultura_chuva = area_obj.get("Cultura", "Soja")



        chuva_ideal_padrao = {

            "Soja":120.0,"Milho":140.0,"Trigo":90.0,"FeijÃÂÃÂ£o":100.0,"Canola":90.0,

            "Aveia":80.0,"Cana-de-aÃÂÃÂ§ÃÂÃÂºcar":180.0,"Arroz":180.0,"Sorgo":90.0,

            "Girassol":90.0,"Cevada":80.0,"Pastagem":120.0,"AlgodÃÂÃÂ£o":130.0,

            "CafÃÂÃÂ©":140.0,"Tabaco":110.0,"Mandioca":100.0,"Batata":100.0,

        }

        chuva_ideal_mes = chuva_ideal_padrao.get(cultura_limpa(cultura_chuva), 120.0)



        st.markdown(f"""

        <div style='background:#0f3460;color:#fff;padding:10px 16px;border-radius:8px;

        border:1px solid #3b82f6;margin-bottom:12px;'>

        ÃÂ°ÃÂ¸ÃÂÃÂ± <b>Cultura:</b> {cultura_chuva} &nbsp;|&nbsp;

        ÃÂ°ÃÂ¸ÃÂÃÂ§ÃÂ¯ÃÂ¸ÃÂ <b>Chuva ideal/mÃÂÃÂªs:</b> {chuva_ideal_mes} mm

        </div>

        """, unsafe_allow_html=True)



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Registro diÃÂÃÂ¡rio ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        st.subheader("ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Registrar Chuva DiÃÂÃÂ¡ria")

        col_d1, col_d2, col_d3 = st.columns(3)

        with col_d1:

            data_chuva = st.date_input("Data", value=datetime.now().date(), key="date_chuva_diaria")

        with col_d2:

            mm_dia = st.number_input("PrecipitaÃÂÃÂ§ÃÂÃÂ£o (mm)", min_value=0.0, max_value=500.0,

                                      value=0.0, step=0.1, key="num_mm_dia",

                                      help="Leitura do pluviÃÂÃÂ´metro de campo")

        with col_d3:

            obs_dia = st.text_input("ObservaÃÂÃÂ§ÃÂÃÂ£o", placeholder="Ex: Chuva forte tarde",

                                     key="txt_obs_chuva")



        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Registrar", key="btn_reg_chuva", use_container_width=True):

            if mm_dia > 0 or obs_dia:

                _reg = {

                    "area_id":  id_area_chuva,

                    "area":     area_chuva,

                    "data":     str(data_chuva),

                    "ano":      data_chuva.year,

                    "mes":      data_chuva.month,

                    "mes_nome": ["","Janeiro","Fevereiro","MarÃÂÃÂ§o","Abril","Maio","Junho",

                                 "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"][data_chuva.month],

                    "mm":       round(mm_dia, 1),

                    "obs":      obs_dia,

                }

                st.session_state.pluviometro.append(_reg)

                salvar_dados_iaagro()

                success_box(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ {mm_dia} mm registrado em {data_chuva.strftime('%d/%m/%Y')}")

            else:

                warning_box("Digite a quantidade de chuva.")



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Filtro e acumulado mensal ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        _regs = [r for r in st.session_state.pluviometro

                 if isinstance(r, dict) and r.get("area_id") == id_area_chuva]



        if _regs:

            import pandas as pd

            df_pluvio = pd.DataFrame(_regs)



            # Garante colunas necessÃÂÃÂ¡rias

            for col in ["data","ano","mes","mes_nome","mm"]:

                if col not in df_pluvio.columns:

                    df_pluvio[col] = 0 if col in ["ano","mes","mm"] else ""



            df_pluvio["mm"] = pd.to_numeric(df_pluvio["mm"], errors="coerce").fillna(0)

            df_pluvio["data_dt"] = pd.to_datetime(df_pluvio["data"], errors="coerce")

            df_pluvio = df_pluvio.sort_values("data_dt", ascending=False)



            # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Acumulado mensal automÃÂÃÂ¡tico ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Acumulado Mensal")

            df_mensal = (df_pluvio.groupby(["ano","mes","mes_nome"])["mm"]

                         .sum().reset_index()

                         .sort_values(["ano","mes"]))

            df_mensal["ideal"] = chuva_ideal_mes

            df_mensal["%ideal"] = (df_mensal["mm"] / chuva_ideal_mes * 100).round(1)

            df_mensal["status"] = df_mensal["%ideal"].apply(

                lambda x: "ÃÂ¢ÃÂÃ¢ÂÂ¦ Adequado" if 70<=x<=130

                else ("ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ DÃÂÃÂ©ficit" if x < 70 else "ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Excesso")

            )

            df_mensal["PerÃÂÃÂ­odo"] = df_mensal["mes_nome"].astype(str) + "/" + df_mensal["ano"].astype(str)



            # Cards dos ÃÂÃÂºltimos 3 meses

            _ultimos = df_mensal.tail(3).to_dict("records")

            cols_m = st.columns(len(_ultimos))

            for idx_m, row in enumerate(_ultimos):

                _cor = "#14532d" if "Adequado" in row["status"] else "#78350f"

                cols_m[idx_m].markdown(f"""

                <div style='background:{_cor};border-radius:10px;padding:12px;text-align:center;'>

                <b style='color:#fff;font-size:13px;'>{row['PerÃÂÃÂ­odo']}</b><br>

                <span style='color:#fff;font-size:22px;font-weight:800;'>{row['mm']:.1f} mm</span><br>

                <span style='color:#d1fae5;font-size:11px;'>{row['%ideal']}% do ideal</span><br>

                <span style='color:#fde68a;font-size:11px;'>{row['status']}</span>

                </div>

                """, unsafe_allow_html=True)



            # GrÃÂÃÂ¡fico acumulado mensal

            if len(df_mensal) > 0:

                st.markdown("**Chuva acumulada vs ideal por mÃÂÃÂªs:**")

                _chart_data = df_mensal.set_index("PerÃÂÃÂ­odo")[["mm","ideal"]]

                _chart_data.columns = ["Chuva Real (mm)","Ideal (mm)"]

                st.bar_chart(_chart_data)



            # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Registros diÃÂÃÂ¡rios ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Registros DiÃÂÃÂ¡rios")



            # Filtro por mÃÂÃÂªs/ano

            _anos  = sorted(df_pluvio["ano"].dropna().unique().tolist(), reverse=True)

            _meses_nomes = ["Todos","Janeiro","Fevereiro","MarÃÂÃÂ§o","Abril","Maio","Junho",

                            "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

            col_f1, col_f2 = st.columns(2)

            _ano_sel = col_f1.selectbox("Filtrar ano", ["Todos"] + [str(int(a)) for a in _anos], key="sel_ano_pluvio")

            _mes_sel = col_f2.selectbox("Filtrar mÃÂÃÂªs", _meses_nomes, key="sel_mes_pluvio")



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

            col_r1.metric("ÃÂ°ÃÂ¸ÃÂÃÂ§ÃÂ¯ÃÂ¸ÃÂ Total", f"{_total_filtro:.1f} mm")

            col_r2.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¦ Dias c/ chuva", f"{_dias_chuva}")

            col_r3.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  MÃÂÃÂ©dia/dia", f"{_media_dia:.1f} mm")

            col_r4.metric("ÃÂ°ÃÂ¸ÃÂ½ÃÂ¯ % do ideal", f"{_total_filtro/chuva_ideal_mes*100:.0f}%" if _mes_sel != "Todos" else "-")



            # Tabela diÃÂÃÂ¡ria

            _cols_exib = ["data","mm","obs"] if "obs" in df_filtrado.columns else ["data","mm"]

            _df_show = df_filtrado[_cols_exib].copy()

            _df_show.columns = ["Data","mm","Obs"] if len(_cols_exib) == 3 else ["Data","mm"]

            st.dataframe(_df_show.head(60), use_container_width=True)



            # Excluir registro

            with st.expander("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Excluir registro"):

                _datas_disp = df_pluvio["data"].tolist()

                if _datas_disp:

                    _data_del = st.selectbox("Selecione a data para excluir",

                                              _datas_disp, key="sel_del_chuva")

                    if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Excluir", key="btn_del_chuva"):

                        st.session_state.pluviometro = [

                            r for r in st.session_state.pluviometro

                            if not (isinstance(r, dict) and

                                    r.get("data") == _data_del and

                                    r.get("area_id") == id_area_chuva)

                        ]

                        salvar_dados_iaagro()

                        success_box("Registro excluÃÂÃÂ­do!")

                        st.rerun()



            # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ AnÃÂÃÂ¡lise de risco ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

            st.subheader("ÃÂ°ÃÂ¸ÃÂ¤Ã¢ÂÂ AnÃÂÃÂ¡lise de Risco HÃÂÃÂ­drico")

            _mensal_recente = df_mensal.tail(3)["mm"].tolist()

            _media_3m = sum(_mensal_recente)/len(_mensal_recente) if _mensal_recente else 0

            _desvio   = abs(_media_3m - chuva_ideal_mes) / chuva_ideal_mes * 100 if chuva_ideal_mes > 0 else 0



            # Estimativa de perda por dÃÂÃÂ©ficit ou excesso (igual ao modelo anterior)

            if _media_3m < chuva_ideal_mes * 0.7:

                _perda_est = round((_chuva_ideal_mes - _media_3m) * 0.15, 1) if hasattr(locals(), '_chuva_ideal_mes') else round((chuva_ideal_mes - _media_3m) * 0.15, 1)

                _perda_est = round((chuva_ideal_mes - _media_3m) * 0.15, 1)

                _status_h  = "ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ DÃÂÃÂ©ficit hÃÂÃÂ­drico"

                _risco     = "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Alto risco hÃÂÃÂ­drico ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ avaliar seguro agrÃÂÃÂ­cola"

                _rec       = f"DÃÂÃÂ©ficit mÃÂÃÂ©dio de {chuva_ideal_mes - _media_3m:.0f} mm/mÃÂÃÂªs. Perda estimada: {_perda_est}%. Reavaliar meta produtiva."

            elif _media_3m > chuva_ideal_mes * 1.3:

                _perda_est = round((_media_3m - chuva_ideal_mes) * 0.08, 1)

                _status_h  = "ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Excesso de chuva"

                _risco     = "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ Risco por excesso hÃÂÃÂ­drico"

                _rec       = f"Excesso mÃÂÃÂ©dio de {_media_3m - chuva_ideal_mes:.0f} mm/mÃÂÃÂªs. Perda estimada: {_perda_est}%. Monitorar doenÃÂÃÂ§as fÃÂÃÂºngicas e erosÃÂÃÂ£o."

            else:

                _perda_est = 0

                _status_h  = "ÃÂ¢ÃÂÃ¢ÂÂ¦ Chuva adequada"

                _risco     = "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ CondiÃÂÃÂ§ÃÂÃÂ£o hÃÂÃÂ­drica adequada"

                _rec       = "PrecipitaÃÂÃÂ§ÃÂÃÂ£o dentro da faixa ideal para a cultura."



            # MÃÂÃÂ©tricas de risco

            _col_r1, _col_r2, _col_r3 = st.columns(3)

            _col_r1.metric("ÃÂ°ÃÂ¸ÃÂÃÂ§ÃÂ¯ÃÂ¸ÃÂ MÃÂÃÂ©dia 3 meses", f"{_media_3m:.1f} mm")

            _col_r2.metric("ÃÂ°ÃÂ¸ÃÂ½ÃÂ¯ Ideal/mÃÂÃÂªs", f"{chuva_ideal_mes} mm")

            _col_r3.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ° Perda estimada", f"{_perda_est}%",

                           help="Estimativa de impacto na produtividade por dÃÂÃÂ©ficit ou excesso hÃÂÃÂ­drico")



            info_box(_risco)

            st.caption(_rec)



            # Progresso do mÃÂÃÂªs atual

            _hoje = datetime.now()

            _regs_mes_atual = [r for r in _regs

                               if isinstance(r, dict)

                               and r.get("mes") == _hoje.month

                               and r.get("ano") == _hoje.year]

            _total_mes_atual = sum(r.get("mm", 0) for r in _regs_mes_atual)

            _pct_mes = min(_total_mes_atual / chuva_ideal_mes, 1.0) if chuva_ideal_mes > 0 else 0



            st.subheader(f"ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¦ {['','Janeiro','Fevereiro','MarÃÂÃÂ§o','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'][_hoje.month]}/{_hoje.year} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Progresso")

            st.progress(_pct_mes)

            st.caption(f"{_total_mes_atual:.1f} mm acumulados de {chuva_ideal_mes} mm ideais ({_pct_mes*100:.0f}%)")



        else:

            st.info("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Nenhum registro de chuva para esta ÃÂÃÂ¡rea ainda. Registre a primeira leitura acima!")









# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: MAPA DE FERTILIDADE

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸ÃÂÃÂ¾ Lavoura":

  with _sub_lav[2]:

    st.header("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂºÃÂ¯ÃÂ¸ÃÂ Mapa de Fertilidade por Cores")

    st.subheader("ÃÂ°ÃÂ¸ÃÂÃÂ¦ÃÂ¯ÃÂ¸ÃÂ Mapa ClimÃÂÃÂ¡tico dos TalhÃÂÃÂµes")



    if len(st.session_state.areas) == 0:

        st.markdown('<div style="background:#1e3a5f;color:#ffffff;padding:14px 18px;border-radius:10px;font-weight:600;font-size:15px;border:1px solid #3b82f6;">ÃÂ¢Ã¢ÂÂÃÂ¹ÃÂ¯ÃÂ¸ÃÂ Nenhuma ÃÂÃÂ¡rea cadastrada.</div>', unsafe_allow_html=True)

    else:

        mapa_dados = []

        for area in st.session_state.areas:

            dados_area = area.get("Dados", area.get("dados", {}))

            media_hist = 0

            historicos_area = [h for h in st.session_state.historico_produtividade if h["ÃÂÃÂrea"].startswith(area["ID"])]

            if len(historicos_area) > 0:

                media_hist = sum(h["Produtividade"] for h in historicos_area) / len(historicos_area)



            # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Dados de calcÃÂÃÂ¡rio e gesso aplicados ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

            _corr       = st.session_state.get("corretivos_aplicados", [])

            _calc_area  = [c for c in _corr if isinstance(c,dict) and c.get("area_id")==area.get("ID","") and c.get("tipo")=="calcario"]

            _gesso_area = [c for c in _corr if isinstance(c,dict) and c.get("area_id")==area.get("ID","") and c.get("tipo")=="gesso"]

            _calc_total  = round(sum(c.get("toneladas_ha",0) for c in _calc_area), 2)

            _gesso_total = round(sum(c.get("toneladas_ha",0) for c in _gesso_area), 2)



            # Usa pH pÃÂÃÂ³s-calagem no score se calcÃÂÃÂ¡rio foi aplicado

            _dados_score = dados_area.copy() if dados_area else {}

            _ph_orig     = _dados_score.get("ph", 0)

            _ph_corrigido = _dados_score.get("ph_pos_calagem", _ph_orig)



            # Se tem calcÃÂÃÂ¡rio mas ph_pos_calagem nÃÂÃÂ£o foi calculado ainda, calcula agora

            if _calc_total > 0 and _ph_corrigido == _ph_orig and _ph_orig > 0:

                _elevacao_total = round((_calc_total * 0.75) * 0.3, 2)

                _ph_corrigido   = min(round(_ph_orig + _elevacao_total, 1), 7.0)

                _dados_score["ph_pos_calagem"] = _ph_corrigido



            # Usa pH corrigido no score visual

            if _calc_total > 0 and _ph_corrigido > _ph_orig:

                _dados_score["ph"] = _ph_corrigido  # score usa pH pÃÂÃÂ³s-calagem



            if _dados_score and "ph" in _dados_score:

                score, classe, alertas = score_solo(_dados_score)

            else:

                score = 0; classe = "Sem anÃÂÃÂ¡lise"; alertas = ["Sem anÃÂÃÂ¡lise de solo"]



            if   score >= 85: cor = "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Verde"

            elif score >= 70: cor = "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ Amarelo"

            elif score >= 50: cor = "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ  Laranja"

            else:             cor = "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Vermelho"



            # Status calagem

            if dados_area and "ph" in dados_area:

                _dose_rec, _ = calcular_calcario_por_ph(dados_area.get("ph",5.5), area.get("Hectares",1))

                if _calc_total == 0:

                    _calc_status = "ÃÂ¢ÃÂ¡ÃÂª NÃÂÃÂ£o aplicado"

                elif _calc_total >= _dose_rec:

                    _calc_status = "ÃÂ¢ÃÂÃ¢ÂÂ¦ Meta atingida"

                elif _calc_total >= _dose_rec * 0.5:

                    _calc_status = "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ Parcial"

                else:

                    _calc_status = "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Insuficiente"

                _calc_color = {"ÃÂ¢ÃÂÃ¢ÂÂ¦ Meta atingida":"#14532d","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ Parcial":"#78350f",

                               "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Insuficiente":"#7f1d1d","ÃÂ¢ÃÂ¡ÃÂª NÃÂÃÂ£o aplicado":"#1e293b"}

                _calc_rec_txt = f"{_dose_rec} t/ha"

            else:

                _calc_status = "ÃÂ¢ÃÂ¡ÃÂª Sem anÃÂÃÂ¡lise"

                _calc_color  = {"ÃÂ¢ÃÂ¡ÃÂª Sem anÃÂÃÂ¡lise":"#1e293b"}

                _calc_rec_txt = "-"



            # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Clima ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

            registros_area = [r for r in st.session_state.pluviometro

                              if isinstance(r, dict) and

                              (r.get("area_id") == area.get("ID","") or

                               r.get("ÃÂÃÂrea") == area.get("ID",""))]

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

                if   perda_media_clima <= 5:  clima_cor = "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Ideal"

                elif perda_media_clima <= 12: clima_cor = "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ AtenÃÂÃÂ§ÃÂÃÂ£o"

                else:                         clima_cor = "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ CrÃÂÃÂ­tico"

            else:

                clima_cor = "ÃÂ¢ÃÂ¡ÃÂª Sem dados"



            mapa_dados.append({

                "ID":             area.get("ID",""),

                "Fazenda":        area.get("Fazenda",""),

                "TalhÃÂÃÂ£o":         area.get("TalhÃÂÃÂ£o",""),

                "Cultura":        area.get("Cultura",""),

                "ÃÂÃÂrea ha":        area.get("Hectares",0),

                "Score":          score,

                "Classe":         classe,

                "Cor":            cor,

                "Clima":          clima_cor,

                "pH atual":       _ph_orig,

                "pH pÃÂÃÂ³s-calagem": _ph_corrigido,

                "CalcÃÂÃÂ¡rio t/ha":  _calc_total,

                "Rec. calcÃÂÃÂ¡rio":  _calc_rec_txt,

                "Status calagem": _calc_status,

                "Gesso t/ha":     _gesso_total,

                "Alertas":        ", ".join(alertas),

            })



        df_mapa = pd.DataFrame(mapa_dados)



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ VisÃÂÃÂ£o geral ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ VisÃÂÃÂ£o geral dos talhÃÂÃÂµes")

        st.dataframe(df_mapa, use_container_width=True)



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Cards visuais com calagem ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂºÃÂ°ÃÂ¯ÃÂ¸ÃÂ Mapa Visual dos TalhÃÂÃÂµes")

        st.write("ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Verde = solo excelente | ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ Amarelo = bom | ÃÂ°ÃÂ¸ÃÂ¸ÃÂ  Laranja = mÃÂÃÂ©dio | ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Vermelho = crÃÂÃÂ­tico")

        cols_card = st.columns(3)

        for i, linha in df_mapa.iterrows():

            cor_str = linha["Cor"]

            if "Verde"   in cor_str: fundo = "#16a34a"

            elif "Amarelo" in cor_str: fundo = "#eab308"

            elif "Laranja" in cor_str: fundo = "#f97316"

            else:                      fundo = "#dc2626"

            _cs = linha["Status calagem"]

            _cc_borda = {"ÃÂ¢ÃÂÃ¢ÂÂ¦ Meta atingida":"#22c55e","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ Parcial":"#eab308",

                         "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Insuficiente":"#ef4444","ÃÂ¢ÃÂ¡ÃÂª NÃÂÃÂ£o aplicado":"#64748b",

                         "ÃÂ¢ÃÂ¡ÃÂª Sem anÃÂÃÂ¡lise":"#64748b"}.get(_cs,"#64748b")

            with cols_card[i % 3]:

                st.markdown(f"""

                <div style="background:{fundo};padding:16px;border-radius:14px;

                margin-bottom:14px;color:white;font-weight:bold;box-shadow:0 4px 12px rgba(0,0,0,0.25);">

                <h3 style="margin:0 0 6px 0;">{linha['TalhÃÂÃÂ£o']}</h3>

                <p style="margin:2px 0;">{get_icone_cultura(linha['Cultura'])} {cultura_limpa(linha['Cultura'])} | {linha['ÃÂÃÂrea ha']} ha</p>

                <p style="margin:2px 0;">ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Score: {linha['Score']} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {linha['Classe']}</p>

                <p style="margin:2px 0;">ÃÂ°ÃÂ¸ÃÂÃÂ§ÃÂ¯ÃÂ¸ÃÂ Clima: {linha['Clima']}</p>

                <hr style="border-color:rgba(255,255,255,0.4);margin:8px 0;">

                <p style="margin:2px 0;border-left:3px solid {_cc_borda};padding-left:8px;">

                ÃÂ°ÃÂ¸ÃÂªÃÂ¨ CalcÃÂÃÂ¡rio: <b>{linha['CalcÃÂÃÂ¡rio t/ha']} t/ha</b> aplicado (rec: {linha['Rec. calcÃÂÃÂ¡rio']})<br>

                {_cs}<br>

                ÃÂ°ÃÂ¸ÃÂ§ÃÂ± Gesso: <b>{linha['Gesso t/ha']} t/ha</b><br>

                ÃÂ°ÃÂ¸ÃÂ§ÃÂª pH: {linha['pH atual']} ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ <b>{linha['pH pÃÂÃÂ³s-calagem']}</b> (pÃÂÃÂ³s-calagem)

                </p>

                <p style="margin:6px 0 0 0;font-size:11px;opacity:0.85;">{linha['Alertas']}</p>

                </div>""", unsafe_allow_html=True)



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Heatmap fertilidade ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        st.subheader("ÃÂ°ÃÂ¸ÃÂÃÂ¡ÃÂ¯ÃÂ¸ÃÂ Heatmap de Fertilidade")



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



        _heat_cols = ["TalhÃÂÃÂ£o","Score","pH atual","pH pÃÂÃÂ³s-calagem","CalcÃÂÃÂ¡rio t/ha","Gesso t/ha","Status calagem"]

        df_heat = df_mapa[[c for c in _heat_cols if c in df_mapa.columns]].copy()



        try:

            _styled = df_heat.style\
                .applymap(cor_score, subset=["Score"])\
                .applymap(cor_ph, subset=["pH atual","pH pÃÂÃÂ³s-calagem"])\
                .applymap(cor_calc, subset=["CalcÃÂÃÂ¡rio t/ha","Gesso t/ha"])

            st.dataframe(_styled, use_container_width=True)

        except Exception:

            st.dataframe(df_heat, use_container_width=True)



        st.caption("ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Verde = ÃÂÃÂ³timo | ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ Laranja = atenÃÂÃÂ§ÃÂÃÂ£o | ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Vermelho = crÃÂÃÂ­tico | ÃÂ¢ÃÂ¡ÃÂ« Cinza = sem dados")



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Ranking ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Ranking de Fertilidade")

        st.bar_chart(df_mapa.set_index("TalhÃÂÃÂ£o")["Score"])



        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂºÃÂ°ÃÂ¯ÃÂ¸ÃÂ Mapa GPS dos TalhÃÂÃÂµes")



        # Coordenadas ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ prioridade: GPS salvo > ÃÂÃÂ¡rea cadastrada > padrÃÂÃÂ£o

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

            if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¡ GPS", key="btn_gps_mapa_fert", use_container_width=True,

                         help="Clique para usar localizaÃÂÃÂ§ÃÂÃÂ£o do celular"):

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

            attr="Esri", name="SatÃÂÃÂ©lite", control=True

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

        folium.Marker(location=[latitude, longitude], popup="Minha localizaÃÂÃÂ§ÃÂÃÂ£o",

                      tooltip="Local atual", icon=folium.Icon(color="darkgreen", icon="leaf")

        ).add_to(mapa_folium)

        dados_mapa_folium = st_folium(mapa_folium, width=900, height=500)

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Salvar Desenho do TalhÃÂÃÂ£o")



        st.info("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¡ **Dica no celular:** Marque os pontos no sentido horÃÂÃÂ¡rio ao redor do talhÃÂÃÂ£o, sem cruzar as linhas. Use o botÃÂÃÂ£o **Delete last point** para desfazer o ÃÂÃÂºltimo ponto.")



        if dados_mapa_folium and dados_mapa_folium.get("last_active_drawing"):

            desenho = dados_mapa_folium["last_active_drawing"]

            coords  = desenho["geometry"]["coordinates"][0]



            # Corrige automaticamente polÃÂÃÂ­gonos com bordas cruzadas usando convex hull

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

            success_box(f"ÃÂÃÂrea calculada automaticamente: {area_calculada:.2f} ha")



            # SeleÃÂÃÂ§ÃÂÃÂ£o da ÃÂÃÂ¡rea para vincular o desenho

            areas_disp = [f"{a.get('Fazenda','')} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {a.get('TalhÃÂÃÂ£o','')}" for a in st.session_state.areas]

            area_vincular = st.selectbox("Vincular desenho ÃÂÃÂ  ÃÂÃÂ¡rea:", ["ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ NÃÂÃÂ£o vincular ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"] + areas_disp, key="sel_area_croqui")



            if st.button("Salvar desenho no talhÃÂÃÂ£o", key="salvar_desenho_talhao"):

                pts_hull = convex_hull([[c[0], c[1]] for c in coords])

                if len(pts_hull) >= 3:

                    pts_hull.append(pts_hull[0])

                    desenho["geometry"]["coordinates"][0] = [[p[0], p[1]] for p in pts_hull]



                # Salva no session_state global

                st.session_state.dados["desenho_talhao"] = desenho



                # Salva tambÃÂÃÂ©m na ÃÂÃÂ¡rea especÃÂÃÂ­fica se selecionada

                if area_vincular != "ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ NÃÂÃÂ£o vincular ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ":

                    idx_area = areas_disp.index(area_vincular)

                    st.session_state.areas[idx_area]["desenho"] = desenho

                    st.session_state.areas[idx_area]["area_calculada_ha"] = round(area_calculada, 2)



                salvar_dados_iaagro()

                success_box("ÃÂ¢ÃÂÃ¢ÂÂ¦ Desenho do talhÃÂÃÂ£o salvo com sucesso!")





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: ANÃÂÃÂLISE DE SOLO

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

elif menu == "ÃÂ°ÃÂ¸ÃÂ§ÃÂª Solo & AdubaÃÂÃÂ§ÃÂÃÂ£o":

    _sub_solo = st.tabs(["ÃÂ°ÃÂ¸ÃÂ§ÃÂª AnÃÂÃÂ¡lise de Solo","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¬ DiagnÃÂÃÂ³stico Completo","ÃÂ°ÃÂ¸ÃÂÃÂ± AdubaÃÂÃÂ§ÃÂÃÂ£o","ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ OCR Laudo de Solo"])



if menu == "ÃÂ°ÃÂ¸ÃÂ§ÃÂª Solo & AdubaÃÂÃÂ§ÃÂÃÂ£o":

  with _sub_solo[0]:

    st.header("AnÃÂÃÂ¡lise de Solo")



    # Injeta estilo escuro no componente de upload via JS

    st.markdown("""

    <style>

    /* ForÃÂÃÂ§a fundo escuro no dropzone do upload */

    [data-testid="stFileUploader"] section,

    [data-testid="stFileUploader"] section > div,

    [data-testid="stFileUploaderDropzone"],

    [data-testid="stFileUploaderDropzone"] > div {

        background-color: #0f3460 !important;

        border: 2px solid #22c55e !important;

        border-radius: 12px !important;

    }

    /* BotÃÂÃÂ£o Upload */

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

    /* Texto de instruÃÂÃÂ§ÃÂÃÂ£o */

    [data-testid="stFileUploaderDropzone"] span,

    [data-testid="stFileUploaderDropzone"] p,

    [data-testid="stFileUploaderDropzone"] small,

    [data-testid="stFileUploaderDropzone"] div {

        color: #ffffff !important;

        opacity: 1 !important;

    }

    /* ÃÂÃÂcone */

    [data-testid="stFileUploaderDropzone"] svg path {

        fill: #22c55e !important;

        stroke: #22c55e !important;

    }

    </style>

    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Upload anÃÂÃÂ¡lise de solo", type=["xlsx","csv"], key="upl___upload_an_lis_3464")

    if uploaded_file is not None:

        if uploaded_file.name.endswith(".csv"):

            df_upload = pd.read_csv(uploaded_file)

        else:

            df_upload = pd.read_excel(uploaded_file)

        success_box("ÃÂ¢ÃÂÃ¢ÂÂ¦ AnÃÂÃÂ¡lise carregada com sucesso!")

        st.dataframe(df_upload)



    if not st.session_state.area_selecionada:

        warning_box("Cadastre ou carregue uma ÃÂÃÂ¡rea primeiro.")

    else:

        col1, col2, col3 = st.columns(3)

        with col1:

            ph       = st.number_input("pH do solo (HÃÂ¢Ã¢ÂÂÃ¢ÂÂO 1:1)", min_value=3.5, max_value=8.0, value=float(st.session_state.dados.get("ph", 5.5)), key="num_ph_do_solo_3478")

            fosforo  = st.number_input("FÃÂÃÂ³sforo P (mg/dmÃÂÃÂ³ Mehlich-1)", min_value=0.0, value=float(st.session_state.dados.get("fosforo", 10.0)), key="num_f_sforo_p_3479")

            potassio = st.number_input("PotÃÂÃÂ¡ssio K (mg/dmÃÂÃÂ³ Mehlich-1)", min_value=0.0, value=float(st.session_state.dados.get("potassio", 100.0)), key="num_pot_ssio_k_3480")

        with col2:

            materia_organica = st.number_input("MatÃÂÃÂ©ria OrgÃÂÃÂ¢nica MO (g/dmÃÂÃÂ³)", min_value=0.0, value=float(st.session_state.dados.get("materia_organica", 2.5)), key="num_mat_ria_org_nic_3482", help="1% = 10 g/dmÃÂÃÂ³")

            calcio   = st.number_input("CÃÂÃÂ¡lcio CaÃÂÃÂ²ÃÂ¢ÃÂÃÂº (cmolc/dmÃÂÃÂ³)", min_value=0.0, value=float(st.session_state.dados.get("calcio", 3.0)), key="num_c_lcio_ca_3483")

            magnesio = st.number_input("MagnÃÂÃÂ©sio MgÃÂÃÂ²ÃÂ¢ÃÂÃÂº (cmolc/dmÃÂÃÂ³)", min_value=0.0, value=float(st.session_state.dados.get("magnesio", 1.0)), key="num_magn_sio_mg_3484")

        with col3:

            aluminio = st.number_input("AlumÃÂÃÂ­nio AlÃÂÃÂ³ÃÂ¢ÃÂÃÂº (cmolc/dmÃÂÃÂ³)", min_value=0.0, value=float(st.session_state.dados.get("aluminio", 0.2)), key="num_alum_nio_al_3486")

            enxofre  = st.number_input("Enxofre S (mg/dmÃÂÃÂ³)", min_value=0.0, value=float(st.session_state.dados.get("enxofre", 8.0)), key="num_enxofre_s_3487")

            ctc      = st.number_input("CTC pH7 (cmolc/dmÃÂÃÂ³)", min_value=0.0, value=float(st.session_state.dados.get("ctc", 8.0)), key="num_ctc_3488", help="Capacidade de Troca CatiÃÂÃÂ´nica")



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CÃÂÃÂ¡lculo automÃÂÃÂ¡tico de V% e SB ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        sb_calc  = calcio + magnesio + (potassio / 391.0)  # K em cmolc

        ctc_val  = ctc if ctc > 0 else (sb_calc + aluminio + 2.0)

        v_calc   = round((sb_calc / ctc_val) * 100, 1) if ctc_val > 0 else 0.0

        m_calc   = round((aluminio / (sb_calc + aluminio)) * 100, 1) if (sb_calc + aluminio) > 0 else 0.0



        st.markdown(f"""

        <div style='background:#0f3460;border-radius:8px;padding:10px 16px;border:1px solid #3b82f6;margin:8px 0;'>

        <b style='color:#3b82f6;'>ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Calculado automaticamente (CQFS RS/SC 2016)</b><br>

        <span style='color:#f1f5f9;font-size:13px;'>

        SB = Ca + Mg + K = <b>{sb_calc:.2f} cmolc/dmÃÂÃÂ³</b> &nbsp;|&nbsp;

        <b>V% = {v_calc}%</b> {"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Adequado" if v_calc >= 60 else "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dio" if v_calc >= 45 else "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixo"} &nbsp;|&nbsp;

        <b>m% = {m_calc}%</b> {"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ OK" if m_calc < 20 else "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Alto"} &nbsp;|&nbsp;

        RelaÃÂÃÂ§ÃÂÃÂ£o Ca/Mg = <b>{round(calcio/magnesio,1) if magnesio > 0 else '-'}</b>

        {"ÃÂ¢ÃÂÃ¢ÂÂ¦" if 2<=round(calcio/magnesio,1)<=5 else "ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ"  if magnesio > 0 else ""}

        </span>

        </div>

        """, unsafe_allow_html=True)



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ V% manual (se vier do laudo) ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        v_laudo = st.number_input("V% do laudo (deixe 0 para usar o calculado)", min_value=0.0, max_value=100.0,

                                   value=float(st.session_state.dados.get("v_percent", 0.0)), key="num_v_percent",

                                   help="SaturaÃÂÃÂ§ÃÂÃÂ£o por bases ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ use se o laudo jÃÂÃÂ¡ fornecer o valor")

        v_final = v_laudo if v_laudo > 0 else v_calc



        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¬ Micronutrientes (mg/dmÃÂÃÂ³ Mehlich-1)")

        col4, col5, col6 = st.columns(3)

        with col4:

            boro  = st.number_input("Boro B", min_value=0.0, value=float(st.session_state.dados.get("boro", 0.3)), key="num_boro_b_3493")

            zinco = st.number_input("Zinco Zn", min_value=0.0, value=float(st.session_state.dados.get("zinco", 1.0)), key="num_zinco_zn_3494")

        with col5:

            manganes = st.number_input("ManganÃÂÃÂªs Mn", min_value=0.0, value=float(st.session_state.dados.get("manganes", 5.0)), key="num_mangan_s_mn_3496")

            cobre    = st.number_input("Cobre Cu", min_value=0.0, value=float(st.session_state.dados.get("cobre", 0.5)), key="num_cobre_cu_3497")

        with col6:

            ferro    = st.number_input("Ferro Fe", min_value=0.0, value=float(st.session_state.dados.get("ferro", 30.0)), key="num_ferro_fe", help="ReferÃÂÃÂªncia: >9 mg/dmÃÂÃÂ³")

            molibdenio = st.number_input("MolibdÃÂÃÂªnio Mo", min_value=0.0, value=float(st.session_state.dados.get("molibdenio", 0.1)), key="num_molibdenio", help="ReferÃÂÃÂªncia: >0.1 mg/dmÃÂÃÂ³")



        st.subheader("ÃÂ°ÃÂ¸ÃÂªÃÂ¨ AnÃÂÃÂ¡lise FÃÂÃÂ­sica do Solo")

        col7, col8, col9 = st.columns(3)

        with col7:

            argila   = st.number_input("Argila (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.dados.get("argila", 35.0)), key="num_argila___3499")

            silte    = st.number_input("Silte (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.dados.get("silte", 25.0)), key="num_silte")

        with col8:

            areia    = st.number_input("Areia total (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.dados.get("areia", 40.0)), key="num_areia")

            dens_solo= st.number_input("Densidade do solo (g/cmÃÂÃÂ³)", min_value=0.5, max_value=2.0, value=float(st.session_state.dados.get("dens_solo", 1.2)), key="num_dens_solo", help="ReferÃÂÃÂªncia: <1.3 g/cmÃÂÃÂ³ para argilosos")

        with col9:

            dens_part= st.number_input("Densidade de partÃÂÃÂ­culas (g/cmÃÂÃÂ³)", min_value=1.0, max_value=3.5, value=float(st.session_state.dados.get("dens_part", 2.65)), key="num_dens_part", help="PadrÃÂÃÂ£o: 2.65 g/cmÃÂÃÂ³")

            umidade  = st.number_input("Umidade atual (%)", min_value=0.0, max_value=100.0, value=float(st.session_state.dados.get("umidade", 0.0)), key="num_umidade")



        # Calcula porosidade e textura automaticamente

        _soma_granulo = argila + silte + areia

        _porosidade = round((1 - dens_solo/dens_part)*100, 1) if dens_part > 0 else 0

        if argila >= 60:    _textura = "Muito argiloso"

        elif argila >= 35:  _textura = "Argiloso"

        elif argila >= 25:  _textura = "MÃÂÃÂ©dia argilosa"

        elif argila >= 15:  _textura = "Franco-argiloso"

        elif silte >= 50:   _textura = "Siltoso"

        elif areia >= 70:   _textura = "Arenoso"

        else:               _textura = "Franco"



        if _soma_granulo > 0:

            st.markdown(f"""

            <div style='background:#0f3460;border-radius:8px;padding:10px 16px;border:1px solid #22c55e;margin:8px 0;'>

            <b style='color:#22c55e;'>ÃÂ°ÃÂ¸ÃÂªÃÂ¨ FÃÂÃÂ­sica do Solo calculada</b><br>

            <span style='color:#f1f5f9;font-size:13px;'>

            Classe textural: <b>{_textura}</b> &nbsp;|&nbsp;

            Porosidade total: <b>{_porosidade}%</b>

            {"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Boa" if _porosidade >= 50 else "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dia" if _porosidade >= 40 else "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Compactado"} &nbsp;|&nbsp;

            Soma granulomÃÂÃÂ©trica: <b>{_soma_granulo:.0f}%</b>

            {"ÃÂ¢ÃÂÃ¢ÂÂ¦" if 95<=_soma_granulo<=105 else "ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Verificar soma"}

            </span>

            </div>

            """, unsafe_allow_html=True)



        # ValidaÃÂÃÂ§ÃÂÃÂ£o de campos

        erros_val = []

        if not validar_ph(ph):

            erros_val.append("pH deve estar entre 3.5 e 9.0")

        if ph == 0:

            erros_val.append("pH nÃÂÃÂ£o pode ser zero")



        if erros_val:

            for e in erros_val:

                st.markdown(f'''<div style="background:#7f1d1d;color:#fff;padding:10px 16px;

                border-radius:10px;border-left:5px solid #ef4444;font-weight:600;margin:4px 0;">

                ÃÂ¢ÃÂÃÂ {e}</div>''', unsafe_allow_html=True)



        if st.button("Salvar AnÃÂÃÂ¡lise"):

            if erros_val:

                st.markdown('''<div style="background:#7f1d1d;color:#fff;padding:10px 16px;

                border-radius:10px;border-left:5px solid #ef4444;font-weight:600;">

                ÃÂ¢ÃÂÃÂ Corrija os erros antes de salvar.</div>''', unsafe_allow_html=True)

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

                # Salvar no banco histÃÂÃÂ³rico

                nota_s  = calcular_nota(st.session_state.dados)

                score_s, classe_s, _ = score_solo(st.session_state.dados)

                id_area_atual = st.session_state.dados.get("id_area","")

                if id_area_atual:

                    salvar_analise_solo_db(id_area_atual, st.session_state.dados, nota_s, score_s, classe_s)

                # Checar alertas de estoque por email

                checar_alertas_estoque()

                success_box("AnÃÂÃÂ¡lise salva na ÃÂÃÂ¡rea ativa e registrada no histÃÂÃÂ³rico!")



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Foto do talhÃÂÃÂ£o ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        st.divider()

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ· Foto do TalhÃÂÃÂ£o")

        foto = st.file_uploader("Adicionar foto do talhÃÂÃÂ£o (JPG, PNG)", type=["jpg","jpeg","png"],

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





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: DIAGNÃÂÃ¢ÂÂSTICO COMPLETO

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸ÃÂ§ÃÂª Solo & AdubaÃÂÃÂ§ÃÂÃÂ£o":

  with _sub_solo[1]:

    st.header("DiagnÃÂÃÂ³stico Completo")

    d = st.session_state.dados

    # Busca dados da ÃÂÃÂ¡rea com anÃÂÃÂ¡lise se session_state.dados nÃÂÃÂ£o tiver pH

    if "ph" not in d and st.session_state.areas:

        _id_s = st.session_state.get("area_selecionada")

        for _a in st.session_state.areas:

            _dad = _a.get("Dados", _a.get("dados", {}))

            if _dad and "ph" in _dad and (_id_s is None or _a.get("ID") == _id_s):

                d = {**_dad, "cultura": _a.get("Cultura","Soja"),

                     "area": _a.get("Hectares",0), "produtividade": _a.get("Produtividade",50)}

                break

        if "ph" not in d:  # pega qualquer ÃÂÃÂ¡rea com anÃÂÃÂ¡lise

            for _a in st.session_state.areas:

                _dad = _a.get("Dados", _a.get("dados", {}))

                if _dad and "ph" in _dad:

                    d = {**_dad, "cultura": _a.get("Cultura","Soja"),

                         "area": _a.get("Hectares",0), "produtividade": _a.get("Produtividade",50)}

                    break



    if "ph" not in d:

        warning_box("Preencha primeiro a anÃÂÃÂ¡lise de solo.")

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

        col3.metric("CalcÃÂÃÂ¡rio",          f"{dose_calcario} t/ha")

        col4.metric("Gesso",             f"{dose_gesso} t/ha")

        col5.metric("ProduÃÂÃÂ§ÃÂÃÂ£o Estimada", f"{producao_estimada:.1f} sc/ha")



        st.subheader("ÃÂ°ÃÂ¸ÃÂ§ÃÂ  Score Inteligente do Solo")

        col1, col2 = st.columns(2)

        col1.metric("Score do Solo",   f"{score}/100")

        col2.metric("ClassificaÃÂÃÂ§ÃÂÃÂ£o",   classe_score)

        if alertas_score:

            warning_box(" | ".join(alertas_score))

        else:

            success_box("Solo em boas condiÃÂÃÂ§ÃÂÃÂµes gerais.")



        indice_produtivo  = score * 1.15

        produtividade_ia  = producao_estimada * (indice_produtivo / 100)

        if   indice_produtivo >= 85: status_ia = "ALTO"

        elif indice_produtivo >= 65: status_ia = "MÃÂÃ¢ÂÂ°DIO"

        else:                        status_ia = "BAIXO"



        st.subheader("ÃÂ°ÃÂ¸ÃÂ¤Ã¢ÂÂ InteligÃÂÃÂªncia Artificial Produtiva")

        st.markdown(f'''<div style="background:#1e3a5f;color:#ffffff;padding:15px 18px;border-radius:12px;

        border-left:5px solid #3b82f6;font-size:15px;font-weight:600;line-height:2.0;margin:8px 0;">

        ÃÂ°ÃÂ¸ÃÂ¤Ã¢ÂÂ <b>Potencial estimado:</b> {status_ia}<br>

        ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ <b>Produtividade prevista pela IA:</b> {produtividade_ia:.1f} sc/ha<br>

        ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  <b>ÃÂÃÂndice produtivo do talhÃÂÃÂ£o:</b> {indice_produtivo:.1f}/100

        </div>''', unsafe_allow_html=True)



        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° InteligÃÂÃÂªncia EconÃÂÃÂ´mica")

        area          = float(d["area"])

        _precos_data  = st.session_state.get("precos_data") or {}

        _soja_sc      = _precos_data.get("soja_sc") or {}

        preco_soja    = float(_soja_sc.get("preco", 115.0) or 115.0)

        custo_base    = 3200

        receita_estimada = produtividade_ia * preco_soja * area

        lucro_estimado   = receita_estimada - (custo_base * area)

        if   lucro_estimado > 50000: risco = "BAIXO"

        elif lucro_estimado > 20000: risco = "MÃÂÃ¢ÂÂ°DIO"

        else:                         risco = "ALTO"

        st.markdown(f'''<div style="background:#14532d;color:#ffffff;padding:15px 18px;border-radius:12px;

        border-left:5px solid #22c55e;font-size:15px;font-weight:600;line-height:2.0;margin:8px 0;">

        ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° <b>Receita estimada:</b> R$ {receita_estimada:,.2f}<br>

        ÃÂ°ÃÂ¸Ã¢ÂÂÃÂµ <b>Lucro potencial:</b> R$ {lucro_estimado:,.2f}<br>

        ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  <b>Risco econÃÂÃÂ´mico:</b> {risco}

        </div>''', unsafe_allow_html=True)



        st.subheader("CalcÃÂÃÂ¡rio")

        st.write(f"Dose estimada: {dose_calcario} t/ha")

        st.write(f"Total estimado: {total_calcario:.1f} toneladas")



        st.subheader("Gesso AgrÃÂÃÂ­cola")

        if precisa_gesso:

            warning_box(f"IndicaÃÂÃÂ§ÃÂÃÂ£o inicial de gesso: {dose_gesso} t/ha")

            st.write(f"Total estimado: {total_gesso:.1f} toneladas")

            for motivo in motivos_gesso:

                st.write(f"- {motivo}")

        else:

            success_box("Sem indicaÃÂÃÂ§ÃÂÃÂ£o inicial forte para gesso.")



        cultura_diag = d.get("cultura", "Soja")

        score, classe_score, alertas_score = score_solo(d, cultura_diag)



        # Tabela completa com micronutrientes

        # Limites EMBRAPA/CQFS RS-SC 2016 por parÃÂÃÂ¢metro

        def _classif_micro(valor, lim_baixo, lim_medio):

            if valor == 0: return "ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"

            if   valor < lim_baixo:  return "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixo"

            elif valor < lim_medio:  return "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dio"

            else:                    return "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Adequado"



        tabela = pd.DataFrame({

            "Indicador": [

                "pH","FÃÂÃÂ³sforo (mg/dmÃÂÃÂ³)","PotÃÂÃÂ¡ssio (mg/dmÃÂÃÂ³)",

                "MatÃÂÃÂ©ria OrgÃÂÃÂ¢nica (%)","CÃÂÃÂ¡lcio (cmolc/dmÃÂÃÂ³)","MagnÃÂÃÂ©sio (cmolc/dmÃÂÃÂ³)",

                "Enxofre (mg/dmÃÂÃÂ³)","AlumÃÂÃÂ­nio (cmolc/dmÃÂÃÂ³)","CTC (cmolc/dmÃÂÃÂ³)","Argila (%)",

                "Zinco Zn (mg/dmÃÂÃÂ³)","Boro B (mg/dmÃÂÃÂ³)","ManganÃÂÃÂªs Mn (mg/dmÃÂÃÂ³)","Cobre Cu (mg/dmÃÂÃÂ³)"

            ],

            "Valor": [

                d.get("ph",0), d.get("fosforo",0), d.get("potassio",0),

                d.get("materia_organica",0), d.get("calcio",0), d.get("magnesio",0),

                d.get("enxofre",0), d.get("aluminio",0), d.get("ctc",0), d.get("argila",0),

                d.get("zinco",0), d.get("boro",0), d.get("manganes",0), d.get("cobre",0)

            ],

            "ClassificaÃÂÃÂ§ÃÂÃÂ£o (EMBRAPA)": [

                "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixo" if d.get("ph",0) < 5.5 else ("ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Adequado" if d.get("ph",0) <= 6.5 else "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ Alto"),

                _classif_micro(d.get("fosforo",0), 6, 18),

                _classif_micro(d.get("potassio",0), 60, 150),

                _classif_micro(d.get("materia_organica",0), 2.5, 4.5),

                _classif_micro(d.get("calcio",0), 2.0, 4.0),

                _classif_micro(d.get("magnesio",0), 0.5, 1.5),

                _classif_micro(d.get("enxofre",0), 5, 10),

                "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ OK" if d.get("aluminio",0) <= 0.3 else ("ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ AtenÃÂÃÂ§ÃÂÃÂ£o" if d.get("aluminio",0) <= 1.0 else "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ TÃÂÃÂ³xico"),

                _classif_micro(d.get("ctc",0), 5, 10),

                _classif_micro(d.get("argila",0), 15, 35),

                _classif_micro(d.get("zinco",0), 0.6, 1.5),

                _classif_micro(d.get("boro",0), 0.2, 0.6),

                _classif_micro(d.get("manganes",0), 1.2, 5.0),

                _classif_micro(d.get("cobre",0), 0.2, 0.8),

            ],

            "ReferÃÂÃÂªncia EMBRAPA": [

                "5.8ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ6.5","6ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ30 (Mehlich-1)","60ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ200","2.5ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ4.5%","2ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ6","0.5ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ2",

                "5ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ15","<0.3 ideal","6ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ15","20ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ60%",

                "0.6ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ2.0","0.2ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ0.6","1.2ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ5.0","0.2ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ0.8"

            ]

        })

        st.dataframe(tabela, use_container_width=True)



        # Parecer especÃÂÃÂ­fico de micronutrientes

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¬ Parecer de Micronutrientes")

        micro_alertas = []

        zinco_v  = d.get("zinco",0)

        boro_v   = d.get("boro",0)

        mn_v     = d.get("manganes",0)

        cu_v     = d.get("cobre",0)

        enx_v    = d.get("enxofre",0)



        # Zinco ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ crÃÂÃÂ­tico para milho, soja

        if zinco_v > 0:

            if zinco_v < 0.6:

                micro_alertas.append(("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´", "Zinco", f"{zinco_v} mg/dmÃÂÃÂ³", "DeficiÃÂÃÂªncia crÃÂÃÂ­tica ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ aplicar 2-3 kg/ha ZnSO4 ou quelato", "Milho e soja muito sensÃÂÃÂ­veis"))

            elif zinco_v < 1.0:

                micro_alertas.append(("ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡", "Zinco", f"{zinco_v} mg/dmÃÂÃÂ³", "NÃÂÃÂ­vel mÃÂÃÂ©dio ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ monitorar", "Foliar preventivo em culturas sensÃÂÃÂ­veis"))



        # Boro ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ crÃÂÃÂ­tico para soja, cafÃÂÃÂ©, algodÃÂÃÂ£o

        if boro_v > 0:

            if boro_v < 0.2:

                micro_alertas.append(("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´", "Boro", f"{boro_v} mg/dmÃÂÃÂ³", "DeficiÃÂÃÂªncia ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ aplicar 1-2 kg/ha B (ÃÂÃÂ¡cido bÃÂÃÂ³rico ou ulexita)", "Soja: afeta enchimento de grÃÂÃÂ£os"))

            elif boro_v < 0.4:

                micro_alertas.append(("ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡", "Boro", f"{boro_v} mg/dmÃÂÃÂ³", "NÃÂÃÂ­vel baixo-mÃÂÃÂ©dio ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ foliar recomendado no florescimento", "Soja, cafÃÂÃÂ© e algodÃÂÃÂ£o"))



        # ManganÃÂÃÂªs ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ importante pH>6.5 causa deficiÃÂÃÂªncia

        if mn_v > 0:

            if mn_v < 1.2:

                micro_alertas.append(("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´", "ManganÃÂÃÂªs", f"{mn_v} mg/dmÃÂÃÂ³", "DeficiÃÂÃÂªncia ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ verificar pH (>6.5 indisponibiliza Mn)", "Soja mais sensÃÂÃÂ­vel"))

            elif mn_v > 20:

                micro_alertas.append(("ÃÂ°ÃÂ¸ÃÂ¸ÃÂ ", "ManganÃÂÃÂªs", f"{mn_v} mg/dmÃÂÃÂ³", "NÃÂÃÂ­vel elevado ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ pH baixo pode causar toxidez", "Elevar pH com calcÃÂÃÂ¡rio"))



        # Cobre

        if cu_v > 0 and cu_v < 0.2:

            micro_alertas.append(("ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡", "Cobre", f"{cu_v} mg/dmÃÂÃÂ³", "Baixo ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ aplicar CuSO4 0.5-1 kg/ha ou foliar", "Solos orgÃÂÃÂ¢nicos mais suscetÃÂÃÂ­veis"))



        # Enxofre

        if enx_v > 0 and enx_v < 5:

            micro_alertas.append(("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´", "Enxofre", f"{enx_v} mg/dmÃÂÃÂ³", "DeficiÃÂÃÂªncia ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ usar gesso agrÃÂÃÂ­cola ou fertilizante com S", "Soja: 10-20 kg S/ha; Milho: 10-15 kg S/ha"))



        if micro_alertas:

            for icone, nut, val, rec, obs in micro_alertas:

                st.markdown(f"""

                <div style='background:#1e293b;border-radius:10px;padding:12px 16px;

                margin-bottom:8px;border-left:4px solid {"#ef4444" if icone=="ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´" else "#f59e0b"}'>

                <b style='color:#f1f5f9;'>{icone} {nut}: {val}</b><br>

                <span style='color:#22c55e;font-size:13px;'>ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  RecomendaÃÂÃÂ§ÃÂÃÂ£o: {rec}</span><br>

                <span style='color:#94a3b8;font-size:12px;'>ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ {obs}</span>

                </div>

                """, unsafe_allow_html=True)

        else:

            st.success("ÃÂ¢ÃÂÃ¢ÂÂ¦ Micronutrientes dentro dos limites adequados (EMBRAPA/CQFS RS-SC).")





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: ADUBAÃÂÃ¢ÂÂ¡ÃÂÃÂO

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸ÃÂ§ÃÂª Solo & AdubaÃÂÃÂ§ÃÂÃÂ£o":

  with _sub_solo[2]:

    st.header("ÃÂ°ÃÂ¸ÃÂÃÂ± AdubaÃÂÃÂ§ÃÂÃÂ£o Inteligente")



    # Busca dados da ÃÂÃÂ¡rea selecionada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ prioridade: area ativa > primeira ÃÂÃÂ¡rea

    d = st.session_state.dados

    _id_sel = st.session_state.get("area_selecionada")



    # Se dados nÃÂÃÂ£o tÃÂÃÂªm pH mas hÃÂÃÂ¡ ÃÂÃÂ¡reas cadastradas, pega da ÃÂÃÂ¡rea selecionada

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

        # Se ainda nÃÂÃÂ£o tem, pega da primeira ÃÂÃÂ¡rea com anÃÂÃÂ¡lise

        if "ph" not in d:

            for _a in st.session_state.areas:

                _dados_area = _a.get("Dados", _a.get("dados", {}))

                if _dados_area and "ph" in _dados_area:

                    d = {**_dados_area,

                         "cultura": _a.get("Cultura", "Soja"),

                         "area":    _a.get("Hectares", 0),

                         "produtividade": _a.get("Produtividade", 50)}

                    break



    # Seletor de ÃÂÃÂ¡rea quando hÃÂÃÂ¡ mÃÂÃÂºltiplas

    if st.session_state.areas:

        _areas_adub = [f"{a['ID']} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {a.get('TalhÃÂÃÂ£o','?')} ({a.get('Cultura','?')})"

                       for a in st.session_state.areas

                       if a.get("Dados") and "ph" in a.get("Dados", {})]

        _areas_sem = [a for a in st.session_state.areas

                      if not a.get("Dados") or "ph" not in a.get("Dados", {})]



        if _areas_sem and not _areas_adub:

            warning_box("Preencha a AnÃÂÃÂ¡lise de Solo para ver as recomendaÃÂÃÂ§ÃÂÃÂµes de adubaÃÂÃÂ§ÃÂÃÂ£o.")

        elif _areas_adub:

            if len(_areas_adub) > 1:

                _sel_adub = st.selectbox("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ ÃÂÃÂrea para adubaÃÂÃÂ§ÃÂÃÂ£o", _areas_adub, key="sel_area_adubacao")

            else:

                _sel_adub = _areas_adub[0]

            _id_adub  = _sel_adub.split(" ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ ")[0]

            _a_obj    = next((a for a in st.session_state.areas if a.get("ID") == _id_adub), None)

            if _a_obj:

                _dad = _a_obj.get("Dados", {})

                if _dad:

                    d = {**_dad,

                         "cultura":       _a_obj.get("Cultura", d.get("cultura","Soja")),

                         "area":          _a_obj.get("Hectares", d.get("area",0)),

                         "produtividade": _a_obj.get("Produtividade", d.get("produtividade",50))}



    st.divider()

    st.subheader("ÃÂ°ÃÂ¸ÃÂªÃÂ¨ Controle de CalcÃÂÃÂ¡rio e Gesso Aplicados")



    if not st.session_state.areas:

        warning_box("Cadastre uma ÃÂÃÂ¡rea primeiro.")

    else:

        # Seletor explÃÂÃÂ­cito de ÃÂÃÂ¡rea

        _lista_areas_corr = [f"{a['ID']} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {a.get('TalhÃÂÃÂ£o','?')} ({a.get('Fazenda','?')})"

                             for a in st.session_state.areas]

        _sel_area_corr = st.selectbox("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ ÃÂÃÂrea para corretivos",

                                       _lista_areas_corr, key="sel_area_corretivos")

        _id_area_atual = _sel_area_corr.split(" ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ ")[0]

        # Inicializa registro de corretivos

        if "corretivos_aplicados" not in st.session_state:

            st.session_state.corretivos_aplicados = []



        _corretivos = [c for c in st.session_state.corretivos_aplicados

                       if isinstance(c, dict) and c.get("area_id") == _id_area_atual]



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CalcÃÂÃÂ¡rio aplicado ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        st.markdown("#### ÃÂ°ÃÂ¸ÃÂªÃÂ¨ CalcÃÂÃÂ¡rio")

        col_ca1, col_ca2, col_ca3 = st.columns(3)

        with col_ca1:

            _data_calc = st.date_input("Data aplicaÃÂÃÂ§ÃÂÃÂ£o", key="date_calcario_aplic",

                                        value=datetime.now().date())

            _toneladas_calc = st.number_input("Quantidade aplicada (t/ha)", min_value=0.0,

                                               step=0.1, key="num_calc_aplic",

                                               help="Toneladas por hectare aplicadas")

        with col_ca2:

            _prnt_aplic = st.number_input("PRNT do produto (%)", min_value=0.0, max_value=100.0,

                                           value=75.0, step=1.0, key="num_prnt_aplic",

                                           help="Verificar na embalagem ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ padrÃÂÃÂ£o 75%")

            _tipo_calc = st.selectbox("Tipo de calcÃÂÃÂ¡rio",

                ["CalcÃÂÃÂ¡rio DolomÃÂÃÂ­tico (Ca+Mg ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ ideal solos com Mg baixo)",

                 "CalcÃÂÃÂ¡rio CalcÃÂÃÂ­tico (sÃÂÃÂ³ Ca ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ usar se Mg jÃÂÃÂ¡ adequado)",

                 "CalcÃÂÃÂ¡rio Magnesiano (predomina Mg)",

                 "Cal Virgem (CaO ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ aÃÂÃÂ§ÃÂÃÂ£o rÃÂÃÂ¡pida)",

                 "Cal Hidratada (Ca(OH)ÃÂ¢Ã¢ÂÂÃ¢ÂÂ ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ aÃÂÃÂ§ÃÂÃÂ£o rÃÂÃÂ¡pida)",

                 "Outro"], key="sel_tipo_calc",

                help="DolomÃÂÃÂ­tico: >12% MgO | CalcÃÂÃÂ­tico: <12% MgO (CQFS RS/SC 2016)")



            # Mostra info sobre o tipo escolhido

            if "DolomÃÂÃÂ­tico" in _tipo_calc:

                st.caption("ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ **DolomÃÂÃÂ­tico:** fornece Ca e Mg ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ recomendado quando Ca/Mg < 2:1 ou Mg < 0.5 cmolc/dmÃÂÃÂ³")

            elif "CalcÃÂÃÂ­tico" in _tipo_calc:

                st.caption("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂµ **CalcÃÂÃÂ­tico:** fornece sÃÂÃÂ³ Ca ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ usar quando Mg jÃÂÃÂ¡ estÃÂÃÂ¡ adequado (>1.0 cmolc/dmÃÂÃÂ³)")

            elif "Magnesiano" in _tipo_calc:

                st.caption("ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ **Magnesiano:** predomina Mg ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ usar em solos com Mg muito baixo")

        with col_ca3:

            _incorporado = st.checkbox("Incorporado ao solo", value=True, key="chk_incorporado",

                                        help="Incorporado com grade ou arado")

            _obs_calc = st.text_input("ObservaÃÂÃÂ§ÃÂÃÂ£o", placeholder="Ex: Aplicado antes do plantio",

                                       key="txt_obs_calc")



        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Registrar CalcÃÂÃÂ¡rio", key="btn_reg_calc", use_container_width=True):

            if _toneladas_calc <= 0:

                st.error(f"ÃÂ¢ÃÂÃÂ Digite a quantidade em t/ha (valor atual: {_toneladas_calc})")

            elif not _id_area_atual:

                st.error("ÃÂ¢ÃÂÃÂ Selecione uma ÃÂÃÂ¡rea primeiro")

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

                # Atualiza dados DENTRO da ÃÂÃÂ¡rea correta no array areas

                _ph_atual = 5.5

                for _area_obj in st.session_state.areas:

                    if _area_obj.get("ID") == _id_area_atual:

                        _dados_area = _area_obj.get("Dados", _area_obj.get("dados", {}))

                        _ph_atual   = _dados_area.get("ph", 5.5) if _dados_area else 5.5

                        break

                _elevacao = round((_toneladas_calc * _prnt_aplic / 100) * 0.3, 2)

                _ph_novo  = min(round(_ph_atual + _elevacao, 1), 7.0)

                # Persiste ph_pos_calagem e calcario_aplicado_ha dentro de cada ÃÂÃÂ¡rea

                for _area_obj in st.session_state.areas:

                    if _area_obj.get("ID") == _id_area_atual:

                        if "Dados" not in _area_obj:

                            _area_obj["Dados"] = {}

                        _area_obj["Dados"]["ph_pos_calagem"]      = _ph_novo

                        _area_obj["Dados"]["calcario_aplicado_ha"] = round(

                            _area_obj["Dados"].get("calcario_aplicado_ha", 0) + _toneladas_calc, 2)

                        break

                # Atualiza tambÃÂÃÂ©m dados da ÃÂÃÂ¡rea ativa se for a mesma

                if st.session_state.get("area_selecionada") == _id_area_atual:

                    st.session_state.dados["ph_pos_calagem"]      = _ph_novo

                    st.session_state.dados["calcario_aplicado_ha"] = round(

                        st.session_state.dados.get("calcario_aplicado_ha", 0) + _toneladas_calc, 2)

                salvar_dados_iaagro()

                success_box(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ {_toneladas_calc} t/ha de {_tipo_calc} registrado! pH estimado pÃÂÃÂ³s-calagem: {_ph_novo}")

                st.rerun()

                warning_box("Informe a quantidade aplicada.")



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Gesso aplicado ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        st.markdown("#### ÃÂ°ÃÂ¸ÃÂ§ÃÂ± Gesso AgrÃÂÃÂ­cola")

        col_g1, col_g2, col_g3 = st.columns(3)

        with col_g1:

            _data_gesso = st.date_input("Data aplicaÃÂÃÂ§ÃÂÃÂ£o", key="date_gesso_aplic",

                                         value=datetime.now().date())

            _ton_gesso  = st.number_input("Quantidade aplicada (t/ha)", min_value=0.0,

                                           step=0.1, key="num_gesso_aplic")

        with col_g2:

            _tipo_gesso = st.selectbox("Tipo de gesso",

                ["Gesso AgrÃÂÃÂ­cola","FCA (Fosfogesso)","Outro"], key="sel_tipo_gesso")

            _pureza_gesso = st.number_input("Pureza CaSOÃÂ¢Ã¢ÂÂÃ¢ÂÂ (%)", min_value=0.0, max_value=100.0,

                                             value=85.0, step=1.0, key="num_pureza_gesso")

        with col_g3:

            _obs_gesso = st.text_input("ObservaÃÂÃÂ§ÃÂÃÂ£o", placeholder="Ex: Para subsolagem",

                                        key="txt_obs_gesso")

            _prof_gesso = st.selectbox("Profundidade alvo",

                ["0-20 cm","20-40 cm","40-60 cm","Superficial"], key="sel_prof_gesso")



        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Registrar Gesso", key="btn_reg_gesso", use_container_width=True):

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

                # Atualiza gesso dentro da ÃÂÃÂ¡rea correta

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

                success_box(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ {_ton_gesso} t/ha de {_tipo_gesso} registrado!")

                st.rerun()

            else:

                warning_box("Informe a quantidade aplicada.")



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ HistÃÂÃÂ³rico e status por ÃÂÃÂ¡rea ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        if _corretivos:

            import pandas as pd

            st.markdown("#### ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ HistÃÂÃÂ³rico de Corretivos")



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

            col_s1.metric("ÃÂ°ÃÂ¸ÃÂªÃÂ¨ CalcÃÂÃÂ¡rio aplicado", f"{_calc_total:.2f} t/ha",

                          delta=f"Rec: {_dose_rec} t/ha")

            col_s2.metric("ÃÂ°ÃÂ¸ÃÂ§ÃÂ± Gesso aplicado", f"{_gesso_total:.2f} t/ha",

                          delta=f"Rec: {_dose_gesso_rec:.1f} t/ha")

            col_s3.metric("pH atual", f"{_ph_atual}")

            col_s4.metric("pH estimado pÃÂÃÂ³s-calagem", f"{_ph_pos}",

                          delta=f"+{round(_ph_pos-_ph_atual,1)}" if _ph_pos > _ph_atual else "sem aplicaÃÂÃÂ§ÃÂÃÂ£o")



            # Alertas

            if _calc_total < _dose_rec * 0.7:

                st.warning(f"ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ CalcÃÂÃÂ¡rio aplicado ({_calc_total:.1f} t/ha) abaixo do recomendado ({_dose_rec} t/ha)")

            elif _calc_total >= _dose_rec:

                st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ Meta de calagem atingida! ({_calc_total:.1f}/{_dose_rec} t/ha)")



            if _gesso_total < _dose_gesso_rec * 0.7 and _dose_gesso_rec > 0:

                st.warning(f"ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Gesso aplicado ({_gesso_total:.1f} t/ha) abaixo do recomendado ({_dose_gesso_rec:.1f} t/ha)")

            elif _gesso_total >= _dose_gesso_rec and _dose_gesso_rec > 0:

                st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ Meta de gessagem atingida! ({_gesso_total:.1f}/{_dose_gesso_rec:.1f} t/ha)")



            # Tabela

            _cols_show = [c for c in ["data","tipo","produto","toneladas_ha","prnt","incorporado","obs"] if c in df_corr.columns]

            st.dataframe(df_corr[_cols_show].rename(columns={

                "data":"Data","tipo":"Tipo","produto":"Produto",

                "toneladas_ha":"t/ha","prnt":"PRNT%","incorporado":"Incorporado","obs":"Obs"

            }), use_container_width=True)



            # Excluir

            with st.expander("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Excluir registro"):

                _opts = [f"{c.get('data','')} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {c.get('produto','')} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {c.get('toneladas_ha',0)} t/ha"

                         for c in _corretivos]

                _del = st.selectbox("Selecione", _opts, key="sel_del_corretivo")

                if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Excluir", key="btn_del_corretivo"):

                    _idx = _opts.index(_del)

                    _all = [i for i,c in enumerate(st.session_state.corretivos_aplicados)

                            if c.get("area_id") == _id_area_atual]

                    st.session_state.corretivos_aplicados.pop(_all[_idx])

                    salvar_dados_iaagro()

                    success_box("Registro excluÃÂÃÂ­do!")

                    st.rerun()

        else:

            st.info("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Nenhum corretivo registrado para esta ÃÂÃÂ¡rea ainda.")

    if "ph" not in d:

        warning_box("Preencha primeiro a AnÃÂÃÂ¡lise de Solo na aba ÃÂ°ÃÂ¸ÃÂ§ÃÂª AnÃÂÃÂ¡lise de Solo.")

    else:

        cultura      = d.get("cultura", "Soja")

        area         = d.get("area", 0)

        produtividade = d.get("produtividade", 0)

        fosforo      = d.get("fosforo", 0)

        potassio     = d.get("potassio", 0)

        ph           = d.get("ph", 0)

        materia_organica = d.get("materia_organica", 0)



        st.subheader("ÃÂ°ÃÂ¸ÃÂ¤Ã¢ÂÂ IA Recomendando AdubaÃÂÃÂ§ÃÂÃÂ£o")



        # RecomendaÃÂÃÂ§ÃÂÃÂ£o por cultura

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

        elif cultura == "FeijÃÂÃÂ£o":

            p2o5 = 110 if fosforo < 10 else 80

            k2o  = 90  if potassio < 0.30 else 60

            n    = 40

        elif cultura == "Canola":

            p2o5 = 80; k2o = 70; n = 150

        elif cultura == "Aveia":

            p2o5 = 50; k2o = 40; n = 90

        elif cultura == "Cana-de-aÃÂÃÂ§ÃÂÃÂºcar":

            p2o5 = 100; k2o = 180; n = 140

        else:

            p2o5 = 60; k2o = 60; n = 80



        st.markdown(f'''<div style="background:#14532d;color:#ffffff;padding:15px 18px;border-radius:12px;

        border-left:5px solid #22c55e;font-size:15px;font-weight:600;line-height:2.0;margin:8px 0;">

        ÃÂ°ÃÂ¸ÃÂÃÂ± <b>RecomendaÃÂÃÂ§ÃÂÃÂ£o IAAgro</b><br>

        ÃÂ°ÃÂ¸ÃÂ§ÃÂª NitrogÃÂÃÂªnio (N): {n} kg/ha<br>

        ÃÂ°ÃÂ¸ÃÂ§ÃÂª FÃÂÃÂ³sforo (P2O5): {p2o5} kg/ha<br>

        ÃÂ°ÃÂ¸ÃÂ§ÃÂª PotÃÂÃÂ¡ssio (K2O): {k2o} kg/ha

        </div>''', unsafe_allow_html=True)



        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Taxa VariÃÂÃÂ¡vel Inteligente")

        zona = st.selectbox("Zona do talhÃÂÃÂ£o", ["Baixa Produtividade","MÃÂÃÂ©dia Produtividade","Alta Produtividade"], key="sel_zona_do_talh_o_3723")

        fator_zona = 0.85 if zona == "Baixa Produtividade" else (1.15 if zona == "Alta Produtividade" else 1.0)

        produtividade_ajustada = produtividade * fator_zona

        n    *= fator_zona

        p2o5 *= fator_zona

        k2o  *= fator_zona



        st.subheader("Dados da ÃÂÃÂrea")

        col1, col2, col3 = st.columns(3)

        col1.metric("Cultura", cultura)

        col2.metric("ÃÂÃÂrea", f"{area:.2f} ha")

        col3.metric("Meta Produtividade", f"{produtividade_ajustada:.1f} sc/ha")

        st.divider()



        st.subheader("RecomendaÃÂÃÂ§ÃÂÃÂ£o Base")

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

        col1.metric("NitrogÃÂÃÂªnio", f"{n:.1f} kg/ha", delta=f"{((fator_zona-1)*100):+.0f}%")

        col2.metric("PÃÂ¢Ã¢ÂÂÃ¢ÂÂOÃÂ¢Ã¢ÂÂÃ¢ÂÂ¦",      f"{p2o5:.1f} kg/ha", delta=f"{((fator_zona-1)*100):+.0f}%")

        col3.metric("KÃÂ¢Ã¢ÂÂÃ¢ÂÂO",       f"{k2o:.1f} kg/ha", delta=f"{((fator_zona-1)*100):+.0f}%")

        st.divider()



        st.subheader("Produtos Recomendados")

        map_ha_ajustado  = map_ha  * fator_zona

        kcl_ha_ajustado  = kcl_ha  * fator_zona

        ureia_ha_ajustado = ureia_ha * fator_zona

        col1, col2, col3 = st.columns(3)

        col1.metric("MAP 11-52-00", f"{map_ha_ajustado:.1f} kg/ha")

        col2.metric("KCl 00-00-60", f"{kcl_ha_ajustado:.1f} kg/ha")

        col3.metric("Ureia 45% N",  f"{ureia_ha_ajustado:.1f} kg/ha")



        st.subheader("Total para a ÃÂÃÂrea")

        total_map  = map_ha_ajustado  * area

        total_kcl  = kcl_ha_ajustado  * area

        total_ureia = ureia_ha_ajustado * area

        col1, col2, col3 = st.columns(3)

        col1.metric("MAP Total",   f"{total_map:.1f} kg")

        col2.metric("KCl Total",   f"{total_kcl:.1f} kg")

        col3.metric("Ureia Total", f"{total_ureia:.1f} kg")



        st.subheader("ÃÂ°ÃÂ¸ÃÂ¡ÃÂ Enviar RecomendaÃÂÃÂ§ÃÂÃÂ£o para AplicaÃÂÃÂ§ÃÂÃÂ£o")

        if st.button("Gerar AplicaÃÂÃÂ§ÃÂÃÂ£o com RecomendaÃÂÃÂ§ÃÂÃÂ£o IA", key="gerar_aplicacao_ia"):

            nova_aplicacao = {

                "Data": str(date.today()),

                "ID ÃÂÃÂrea": st.session_state.dados.get("id_area",""),

                "TalhÃÂÃÂ£o": st.session_state.dados.get("talhao",""),

                "Cultura": cultura, "Tipo": "AdubaÃÂÃÂ§ÃÂÃÂ£o IA", "ÃÂÃÂrea ha": area,

                "Produtos": [

                    {"Insumo":"MAP 11-52-00","Dose ha":map_ha_ajustado,"Quantidade usada":total_map,"Unidade":"kg"},

                    {"Insumo":"KCL 00-00-60","Dose ha":kcl_ha_ajustado,"Quantidade usada":total_kcl,"Unidade":"kg"},

                    {"Insumo":"Ureia 45% N", "Dose ha":ureia_ha_ajustado,"Quantidade usada":total_ureia,"Unidade":"kg"},

                ]

            }

            st.session_state.aplicacoes.append(nova_aplicacao)

            salvar_dados_iaagro()

            success_box("AplicaÃÂÃÂ§ÃÂÃÂ£o de adubaÃÂÃÂ§ÃÂÃÂ£o IA enviada para o histÃÂÃÂ³rico!")

            st.subheader("ÃÂ°ÃÂ¸ÃÂ¡ÃÂ¨ Alerta Inteligente de Estoque")

            for prod in [{"Insumo":"MAP 11-52-00","Necessario":total_map},

                         {"Insumo":"KCL 00-00-60","Necessario":total_kcl},

                         {"Insumo":"Ureia 45% N","Necessario":total_ureia}]:

                nome       = prod["Insumo"]

                necessario = prod["Necessario"]

                estoque_item = next((item for item in st.session_state.estoque if item["Insumo"] == nome), None)

                if estoque_item is None:

                    error_box(f"ÃÂ¢ÃÂÃÂ {nome}: nÃÂÃÂ£o cadastrado no estoque.")

                elif necessario <= 0:

                    info_box(f"ÃÂ¢Ã¢ÂÂÃÂ¹ÃÂ¯ÃÂ¸ÃÂ {nome}: nÃÂÃÂ£o necessÃÂÃÂ¡rio nesta recomendaÃÂÃÂ§ÃÂÃÂ£o.")

                elif estoque_item.get("Quantidade",0) >= necessario:

                    sobra = estoque_item["Quantidade"] - necessario

                    success_box(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ {nome}: estoque suficiente. NecessÃÂÃÂ¡rio: {necessario:.1f} | Sobra: {sobra:.1f} kg")

                else:

                    falta     = necessario - estoque_item["Quantidade"]

                    cobertura = (estoque_item["Quantidade"] / necessario) * 100

                    warning_box(f"ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ {nome}: estoque insuficiente. Falta: {falta:.1f} kg | Cobertura: {cobertura:.0f}%")



        st.divider()

        st.subheader("Micronutrientes")

        recomendacoes_micro = []

        if d.get("boro",   0) < 0.3: recomendacoes_micro.append("Boro baixo: considerar aplicaÃÂÃÂ§ÃÂÃÂ£o de B.")

        if d.get("zinco",  0) < 1.0: recomendacoes_micro.append("Zinco baixo: considerar aplicaÃÂÃÂ§ÃÂÃÂ£o de Zn.")

        if d.get("manganes",0) < 5:  recomendacoes_micro.append("ManganÃÂÃÂªs baixo: monitorar Mn.")

        if d.get("cobre",  0) < 0.5: recomendacoes_micro.append("Cobre baixo: considerar aplicaÃÂÃÂ§ÃÂÃÂ£o de Cu.")

        if recomendacoes_micro:

            for rec in recomendacoes_micro: warning_box(rec)

        else:

            success_box("Micronutrientes em faixa aceitÃÂÃÂ¡vel.")



        st.divider()

        st.subheader("Salvar RecomendaÃÂÃÂ§ÃÂÃÂ£o")

        recomendacao_adubacao = {

            "Cultura": cultura, "ÃÂÃÂrea ha": area, "Produtividade alvo": produtividade,

            "N kg/ha": n_ha, "P2O5 kg/ha": p2o5_ha, "K2O kg/ha": k2o_ha,

            "MAP kg/ha": map_ha, "KCl kg/ha": kcl_ha, "Ureia kg/ha": ureia_ha,

            "MAP total kg": total_map, "KCl total kg": total_kcl, "Ureia total kg": total_ureia,

            "Micronutrientes": recomendacoes_micro

        }

        if st.button("Salvar RecomendaÃÂÃÂ§ÃÂÃÂ£o de AdubaÃÂÃÂ§ÃÂÃÂ£o", key="salvar_adubacao_inteligente"):

            st.session_state.dados["adubacao"] = recomendacao_adubacao

            atualizar_area_atual()

            salvar_dados_iaagro()

            success_box("RecomendaÃÂÃÂ§ÃÂÃÂ£o de adubaÃÂÃÂ§ÃÂÃÂ£o salva com sucesso.")



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: CUSTOS

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

elif menu == "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Financeiro":

    _sub_fin = st.tabs(["ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¸ Custos","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¹ Dashboard Financeiro","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Comparativo de Safras","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂµ Fluxo de Caixa","ÃÂ°ÃÂ¸ÃÂ§ÃÂ¾ Imposto de Renda Rural"])



if menu == "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Financeiro":

  with _sub_fin[0]:

    st.header("Custos Estimados")

    d = st.session_state.dados



    # Busca dados da ÃÂÃÂ¡rea se session_state.dados nÃÂÃÂ£o tiver pH

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

        warning_box("Preencha primeiro Cadastro da ÃÂÃÂrea e AnÃÂÃÂ¡lise de Solo.")

    else:

        dose_calcario, total_calcario = calcular_calcario_por_ph(d["ph"], d["area"])

        precisa_gesso, dose_gesso, total_gesso, _ = calcular_gesso(d)



        preco_calcario    = st.number_input("PreÃÂÃÂ§o calcÃÂÃÂ¡rio R$/t",     min_value=0.0, value=180.0, key="num_pre_o_calc_rio__3860")

        frete_calcario    = st.number_input("Frete calcÃÂÃÂ¡rio R$/t",     min_value=0.0, value=50.0, key="num_frete_calc_rio__3861")

        aplicacao_calcario = st.number_input("AplicaÃÂÃÂ§ÃÂÃÂ£o calcÃÂÃÂ¡rio R$/ha", min_value=0.0, value=80.0, key="num_aplica__o_calc__3862")

        preco_gesso       = st.number_input("PreÃÂÃÂ§o gesso R$/t",        min_value=0.0, value=120.0, key="num_pre_o_gesso_r___3863")

        frete_gesso       = st.number_input("Frete gesso R$/t",        min_value=0.0, value=50.0, key="num_frete_gesso_r___3864")

        aplicacao_gesso   = st.number_input("AplicaÃÂÃÂ§ÃÂÃÂ£o gesso R$/ha",   min_value=0.0, value=70.0, key="num_aplica__o_gesso_3865")



        custo_total_calcario = (total_calcario * preco_calcario

                                + total_calcario * frete_calcario

                                + d["area"] * aplicacao_calcario)

        custo_total_gesso    = (total_gesso * preco_gesso

                                + total_gesso * frete_gesso

                                + d["area"] * aplicacao_gesso)



        st.divider()

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Custos Complementares")

        custo_semente      = st.number_input("Custo sementes R$/ha",       min_value=0.0, step=1.0, key="num_custo_sementes__3876")

        custo_fertilizante = st.number_input("Custo fertilizantes R$/ha",  min_value=0.0, step=1.0, key="num_custo_fertiliza_3877")

        custo_defensivos   = st.number_input("Custo defensivos R$/ha",     min_value=0.0, step=1.0, key="num_custo_defensivo_3878")

        custo_diesel       = st.number_input("Custo diesel/mÃÂÃÂ¡quinas R$/ha", min_value=0.0, step=1.0, key="num_custo_diesel_m__3879")

        outros_custos      = st.number_input("Outros custos R$/ha",        min_value=0.0, step=1.0, key="num_outros_custos_r_3880")



        custo_operacional_total = (custo_semente + custo_fertilizante + custo_defensivos + custo_diesel + outros_custos) * d["area"]

        custo_total_safra       = custo_total_calcario + custo_total_gesso + custo_operacional_total

        custo_por_hectare       = custo_total_safra / d["area"] if d["area"] > 0 else 0



        st.divider()

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Resumo Financeiro")

        st.metric("Custo Total Safra",    f"R$ {custo_total_safra:,.2f}")

        st.metric("Custo por Hectare",    f"R$ {custo_por_hectare:,.2f}/ha")



        if "produtividade" in d:

            preco_saca   = st.number_input("PreÃÂÃÂ§o da saca R$", min_value=0.0, step=1.0, key="num_pre_o_da_saca_r_3892")

            faturamento  = d["produtividade"] * preco_saca * d["area"]

            lucro        = faturamento - custo_total_safra

            margem       = (lucro / faturamento * 100) if faturamento > 0 else 0

            st.metric("Faturamento Estimado", f"R$ {faturamento:,.2f}")

            st.metric("Lucro Estimado",       f"R$ {lucro:,.2f}")

            st.metric("Margem Estimada",      f"{margem:.1f}%")





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

elif menu == "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ Operacional":

    _sub_op = st.tabs(["ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ Estoque de Insumos","ÃÂ°ÃÂ¸ÃÂ¡ÃÂ AplicaÃÂÃÂ§ÃÂÃÂµes","ÃÂ¢ÃÂÃÂ±ÃÂ¯ÃÂ¸ÃÂ Prazo de CarÃÂÃÂªncia","ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Ordem de ServiÃÂÃÂ§o","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ ReceituÃÂÃÂ¡rio AgronÃÂÃÂ´mico"])



if menu == "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ Operacional":

  with _sub_op[0]:

    st.header("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ Estoque de Insumos")



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TABS principais ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    tab_manual, tab_nfe = st.tabs([

        "ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Cadastrar Manualmente",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Importar Nota Fiscal (XML)"

    ])



    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    with tab_nfe:

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Importar Nota Fiscal EletrÃÂÃÂ´nica (XML)")

        st.info("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ½ FaÃÂÃÂ§a upload do XML da NF-e ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ todos os produtos entram no estoque automaticamente.")



        xml_file = st.file_uploader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ½ Upload do XML da NF-e", type=["xml"], key="uploader_nfe")



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

                emit    = _find_text(root, "xNome", "Fornecedor nÃÂÃÂ£o identificado")

                dt_emis = _find_text(root, "dhEmi", _find_text(root, "dEmi", ""))

                dt_fmt  = dt_emis[:10] if dt_emis else "N/D"



                st.markdown(f"""

                <div style='background:#0f3460;border-radius:10px;padding:14px 18px;margin-bottom:12px;border:1px solid #22c55e'>

                <b style='color:#22c55e'>ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Nota Fiscal NÃÂÃÂº {n_nf}</b><br>

                <span style='color:#f1f5f9'>Emitente: {emit} &nbsp;|&nbsp; Data: {dt_fmt}</span>

                </div>

                """, unsafe_allow_html=True)



                uni_map = {

                    "KG":"kg","KGS":"kg","TON":"ton","T":"ton",

                    "L":"litros","LT":"litros","LTS":"litros",

                    "SC":"sacos","SAC":"sacos","UN":"unidades",

                    "UNI":"unidades","UND":"unidades","GAL":"galÃÂÃÂµes",

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

                        "Valor UnitÃÂÃÂ¡rio R$":vul_prod,

                        "Valor Total R$":   round(qtd_prod * vul_prod, 2),

                    })



                if not itens_nfe:

                    st.warning("ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Nenhum produto encontrado no XML.")

                else:

                    # Importa TODOS os itens automaticamente, sem botÃÂÃÂ£o, sem checkbox

                    adicionados = 0

                    for item in itens_nfe:

                        novo = {

                            "Insumo":            item["Nome"],

                            "Categoria":         "Outro",

                            "Quantidade":        item["Quantidade"],

                            "Unidade":           item["Unidade"],

                            "Valor UnitÃÂÃÂ¡rio R$": item["Valor UnitÃÂÃÂ¡rio R$"],

                            "Valor Total R$":    item["Valor Total R$"],

                            "Estoque MÃÂÃÂ­nimo":    0.0,

                            "ObservaÃÂÃÂ§ÃÂÃÂ£o":        f"NF-e nÃÂÃÂº {n_nf} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {emit} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {dt_fmt}",

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



                    st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ {adicionados} produto(s) da NF-e nÃÂÃÂº {n_nf} importados para o estoque!")

                    st.markdown("### ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ Produtos importados")

                    st.dataframe(pd.DataFrame(itens_nfe), use_container_width=True)

                    st.balloons()

                    st.rerun()



            except ET.ParseError as e:

                st.error(f"ÃÂ¢ÃÂÃÂ Erro ao ler o XML: {e}")

            except Exception as e:

                st.error(f"ÃÂ¢ÃÂÃÂ Erro inesperado: {e}")



    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    # TAB 1 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ CADASTRO MANUAL (conteÃÂÃÂºdo original)

    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    with tab_manual:

        st.subheader("ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Cadastrar Produto")



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CSS do autocomplete + tema escuro global ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        st.markdown("""

        <style>

        /* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Selectbox ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ fundo escuro igual ao upload ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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

        /* Dropdown do selectbox (lista de opÃÂÃÂ§ÃÂÃÂµes) */

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

        /* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Text input ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ fundo escuro ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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

        /* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Number input ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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

        /* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Labels dos inputs ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

        div[data-testid="stTextInput"] label,

        div[data-testid="stSelectbox"] label,

        div[data-testid="stNumberInput"] label,

        div[data-testid="stTextArea"] label {

            color: #22c55e !important;

            font-weight: 700 !important;

            font-size: 13px !important;

        }

        /* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BotÃÂÃÂµes gerais ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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

        /* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ BotÃÂÃÂ£o primÃÂÃÂ¡rio "Usar este produto" / "Analisar" ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

        div[data-testid="stButton"] > button[kind="primary"],

        div[data-testid="stButton"] > button.primary {

            background-color: #16a34a !important;

            border-color: #22c55e !important;

            color: #fff !important;

        }

        /* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Upload widget ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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

        /* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Checkbox ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

        div[data-testid="stCheckbox"] label {

            color: #f1f5f9 !important;

        }

        /* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Autocomplete dropdown HTML customizado ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

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

        /* ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Scrollbar do dropdown ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ */

        .autocomplete-dropdown::-webkit-scrollbar { width: 5px; }

        .autocomplete-dropdown::-webkit-scrollbar-track { background: #0d1b2a; }

        .autocomplete-dropdown::-webkit-scrollbar-thumb { background: #22c55e; border-radius: 4px; }

        </style>

        """, unsafe_allow_html=True)

    

        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Autocomplete via session_state ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        if "ac_query"       not in st.session_state: st.session_state.ac_query       = ""

        if "ac_selecionado" not in st.session_state: st.session_state.ac_selecionado = None

        if "ac_fab"         not in st.session_state: st.session_state.ac_fab         = "Todos"

    

        # Filtro por fabricante (botÃÂÃÂµes em linha)

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

            "Todos":      {"bg":"#166534", "border":"#22c55e", "emoji":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ½"},

            "BASF":       {"bg":"#1e3a8a", "border":"#93c5fd", "emoji":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂµ"},

            "Syngenta":   {"bg":"#14532d", "border":"#86efac", "emoji":"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢"},

            "Bayer":      {"bg":"#7f1d1d", "border":"#fca5a5", "emoji":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´"},

            "UPL":        {"bg":"#92400e", "border":"#fcd34d", "emoji":"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ "},

            "Timac Agro": {"bg":"#6b21a8", "border":"#f0abfc", "emoji":"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ£"},

            "Mosaic":     {"bg":"#065f46", "border":"#6ee7b7", "emoji":"ÃÂ°ÃÂ¸ÃÂÃÂ "},

            "Corteva":    {"bg":"#164e63", "border":"#67e8f9", "emoji":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ·"},

            "FMC":        {"bg":"#1e1b4b", "border":"#a5b4fc", "emoji":"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¦"},

            "ADAMA":      {"bg":"#365314", "border":"#bef264", "emoji":"ÃÂ°ÃÂ¸ÃÂÃÂ¿"},

            "Ouro Fino":  {"bg":"#713f12", "border":"#fde68a", "emoji":"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡"},

            "Ihara":      {"bg":"#4a044e", "border":"#f9a8d4", "emoji":"ÃÂ°ÃÂ¸ÃÂÃÂ¸"},

            "Nortox":     {"bg":"#134e4a", "border":"#5eead4", "emoji":"ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ¬"},

            "Outros":     {"bg":"#374151", "border":"#9ca3af", "emoji":"ÃÂ¢ÃÂ¡ÃÂª"},

        }

    

        st.markdown("**ÃÂ°ÃÂ¸ÃÂÃÂ­ Filtrar por Fabricante:**")

    

        # Renderiza todos os botÃÂÃÂµes como forms HTML ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ fundo e texto totalmente controlados

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

                    if st.form_submit_button("ÃÂ¢ÃÂÃ¢ÂÂ", use_container_width=True):

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

        ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ½ Fabricante ativo: <b>{fab_ativo}</b> ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {qtd_fab} produtos disponÃÂÃÂ­veis

        </div>""", unsafe_allow_html=True)

    

        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Campo de busca ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        query_input = st.text_input(

            "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Nome comercial, ingrediente ativo ou categoria",

            value=st.session_state.ac_query,

            placeholder="Ex: Fox Xpro, glifosato, fungicida...",

            key="input_busca_produto"

        )

    

        if query_input != st.session_state.ac_query:

            st.session_state.ac_query = query_input

            if st.session_state.ac_selecionado and query_input != st.session_state.ac_selecionado["nome"]:

                st.session_state.ac_selecionado = None

    

        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Filtra catÃÂÃÂ¡logo ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        catalogo_filtrado = CATALOGO_PRODUTOS if fab_ativo == "Todos" else [

            p for p in CATALOGO_PRODUTOS if p["fab"] == fab_ativo

        ]

    

        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Mostra resultados ao digitar ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        if st.session_state.ac_query and not st.session_state.ac_selecionado:

            q = st.session_state.ac_query.lower()

            starts   = [p for p in catalogo_filtrado if p["nome"].lower().startswith(q)]

            contains = [p for p in catalogo_filtrado

                        if not p["nome"].lower().startswith(q)

                        and (q in p["nome"].lower() or q in p["ia"].lower() or q in p["cat"].lower())]

            resultados = (starts + contains)[:20]

    

            if resultados:

                FAB_EM = {"BASF":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂµ","Syngenta":"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢","Bayer":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´","UPL":"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ ",

                          "Timac Agro":"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ£","Mosaic":"ÃÂ°ÃÂ¸ÃÂÃÂ ","Outros":"ÃÂ¢ÃÂ¡ÃÂª"}

                CAT_EM = {"Fungicida":"ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ","Herbicida":"ÃÂ°ÃÂ¸ÃÂÃÂ¿","Inseticida":"ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂº",

                          "Acaricida":"ÃÂ°ÃÂ¸Ã¢ÂÂ¢ÃÂ·ÃÂ¯ÃÂ¸ÃÂ","Nematicida":"ÃÂ°ÃÂ¸ÃÂªÃÂ±","Fungicida BiolÃÂÃÂ³gico":"ÃÂ°ÃÂ¸ÃÂÃÂ±",

                          "Inseticida BiolÃÂÃÂ³gico":"ÃÂ°ÃÂ¸ÃÂ¦ÃÂ ","Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ§",

                          "Tratamento de Sementes":"ÃÂ°ÃÂ¸ÃÂÃÂ¾","Regulador de Crescimento":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ",

                          "Adjuvante":"ÃÂ¢ÃÂ¡Ã¢ÂÂÃÂ¯ÃÂ¸ÃÂ","Fertilizante":"ÃÂ°ÃÂ¸ÃÂ§ÃÂª","Bioestimulante":"ÃÂ¢ÃÂÃÂ¨"}

    

                st.markdown(f'<div style="background:#0f3460;color:#22c55e;padding:6px 14px;'

                            f'border-radius:8px 8px 0 0;font-size:11px;font-weight:800;letter-spacing:1px;">'

                            f'ÃÂ°ÃÂ¸ÃÂÃÂ¿ {len(resultados)} RESULTADO{"S" if len(resultados)!=1 else ""} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ clique para selecionar</div>',

                            unsafe_allow_html=True)

    

                # OpÃÂÃÂ§ÃÂÃÂµes formatadas para o radio

                opcoes_labels = []

                for p in resultados:

                    em_fab = FAB_EM.get(p["fab"], "ÃÂ¢ÃÂ¡ÃÂª")

                    em_cat = CAT_EM.get(p["cat"], "ÃÂ°ÃÂ¸ÃÂÃÂ±")

                    opcoes_labels.append(f"{em_cat} {p['nome']}  |  {em_fab} {p['fab']}  ÃÂÃÂ·  {p['cat']}  ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ  {p['ia'][:50]}")

    

                escolha_idx = st.radio(

                    "Resultados:",

                    range(len(opcoes_labels)),

                    format_func=lambda i: opcoes_labels[i],

                    key="radio_produto_catalogo",

                    label_visibility="collapsed"

                )

    

                if st.button("ÃÂ¢ÃÂÃ¢ÂÂ¦ Usar este produto", key="btn_usar_produto", use_container_width=True):

                    prod_sel = resultados[escolha_idx]

                    st.session_state.ac_selecionado = prod_sel

                    st.session_state.ac_query = prod_sel["nome"]

                    # ForÃÂÃÂ§a preenchimento dos campos via session_state

                    st.session_state["nome_insumo_final"] = prod_sel["nome"]

                    cat_map_tmp = {

                        "Fungicida":"Fungicida","Herbicida":"Herbicida","Inseticida":"Inseticida",

                        "Acaricida":"Outro","Nematicida":"Outro","Fungicida BiolÃÂÃÂ³gico":"BiolÃÂÃÂ³gico",

                        "Inseticida BiolÃÂÃÂ³gico":"BiolÃÂÃÂ³gico","Bioestimulante":"Foliar",

                        "Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o":"Foliar","Regulador de Crescimento":"Outro",

                        "Adjuvante":"Adjuvante","Tratamento de Sementes":"Outro",

                        "Fertilizante":"Fertilizante",

                    }

                    st.rerun()

    

            else:

                st.markdown(f'<div style="background:#1e293b;color:#f87171;padding:10px 14px;'

                            f'border-radius:8px;font-size:13px;font-weight:600;margin:4px 0;">'

                            f'ÃÂ¢ÃÂÃÂ Nenhum produto encontrado para "<b>{st.session_state.ac_query}</b>"</div>',

                            unsafe_allow_html=True)

    

        # Card do produto selecionado

        if st.session_state.ac_selecionado:

            p = st.session_state.ac_selecionado

            fab_bg = {"BASF":"#1e3a8a","Syngenta":"#14532d","Bayer":"#7f1d1d","UPL":"#78350f","Timac Agro":"#6b21a8","Mosaic":"#065f46","Outros":"#1e293b"}.get(p["fab"],"#1e293b")

            fab_tx = {"BASF":"#93c5fd","Syngenta":"#86efac","Bayer":"#fca5a5","UPL":"#fcd34d","Timac Agro":"#f0abfc","Mosaic":"#6ee7b7","Outros":"#94a3b8"}.get(p["fab"],"#94a3b8")

            fab_em = {"BASF":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂµ","Syngenta":"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢","Bayer":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´","UPL":"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ ","Timac Agro":"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ£","Mosaic":"ÃÂ°ÃÂ¸ÃÂÃÂ ","Outros":"ÃÂ¢ÃÂ¡ÃÂª"}.get(p["fab"],"ÃÂ¢ÃÂ¡ÃÂª")

            cat_em = {"Fungicida":"ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ","Herbicida":"ÃÂ°ÃÂ¸ÃÂÃÂ¿","Inseticida":"ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂº","Acaricida":"ÃÂ°ÃÂ¸Ã¢ÂÂ¢ÃÂ·ÃÂ¯ÃÂ¸ÃÂ",

                      "Tratamento de Sementes":"ÃÂ°ÃÂ¸ÃÂÃÂ¾","Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ§",

                      "Regulador de Crescimento":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ","Adjuvante":"ÃÂ¢ÃÂ¡Ã¢ÂÂÃÂ¯ÃÂ¸ÃÂ","Nematicida":"ÃÂ°ÃÂ¸ÃÂªÃÂ±",

                      "Inseticida BiolÃÂÃÂ³gico":"ÃÂ°ÃÂ¸ÃÂ¦ÃÂ ","Bioestimulante":"ÃÂ¢ÃÂÃÂ¨"}.get(p["cat"],"ÃÂ°ÃÂ¸ÃÂÃÂ±")

            st.markdown(f"""

            <div style="background:{fab_bg};border:2px solid {fab_tx}33;border-radius:12px;

            padding:12px 16px;margin:6px 0 12px 0;display:flex;align-items:center;gap:12px;">

                <div style="font-size:26px;">{cat_em}</div>

                <div style="flex:1;">

                    <div style="color:#ffffff;font-weight:800;font-size:15px;">{p['nome']}</div>

                    <div style="color:{fab_tx};font-size:12px;margin-top:3px;">{fab_em} {p['fab']} ÃÂÃÂ· {p['cat']}</div>

                    <div style="color:#94a3b8;font-size:11px;margin-top:2px;">I.A.: {p['ia']}</div>

                </div>

            </div>""", unsafe_allow_html=True)

    

            if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Trocar produto", key="btn_trocar_produto"):

                st.session_state.ac_selecionado = None

                st.session_state.ac_query = ""

                st.rerun()

    

            nome_insumo = p["nome"]

            # Mapeia categoria do catÃÂÃÂ¡logo para categoria do estoque

            cat_map = {

                "Fungicida":"Fungicida","Herbicida":"Herbicida","Inseticida":"Inseticida",

                "Acaricida":"Outro","Nematicida":"Outro","Fungicida BiolÃÂÃÂ³gico":"BiolÃÂÃÂ³gico",

                "Inseticida BiolÃÂÃÂ³gico":"BiolÃÂÃÂ³gico","Bioestimulante":"Foliar",

                "Foliar / NutriÃÂÃÂ§ÃÂÃÂ£o":"Foliar","Regulador de Crescimento":"Outro",

                "Adjuvante":"Adjuvante","Tratamento de Sementes":"Outro",

                "Fertilizante":"Fertilizante",

            }

            cat_sugerida = cat_map.get(p["cat"], "Outro")

        else:

            nome_insumo  = st.session_state.ac_query if st.session_state.ac_query else ""

            cat_sugerida = "Fungicida"

    

        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Campos complementares ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            # PrÃÂÃÂ©-preenche via session_state quando produto ÃÂÃÂ© selecionado do catÃÂÃÂ¡logo

            if "nome_insumo_final" not in st.session_state:

                st.session_state["nome_insumo_final"] = nome_insumo

            elif nome_insumo and st.session_state.get("ac_selecionado"):

                st.session_state["nome_insumo_final"] = nome_insumo

            nome_final = st.text_input("Nome do produto / insumo", key="nome_insumo_final")

            _cats = ["Fertilizante","Cloreto de PotÃÂÃÂ¡ssio","Ureia","Fungicida","Inseticida",

                     "Herbicida","BiolÃÂÃÂ³gico","Foliar","Semente","CalcÃÂÃÂ¡rio","Gesso AgrÃÂÃÂ­cola","Adjuvante","Outro"]

            _cat_idx = _cats.index(cat_sugerida) if cat_sugerida in _cats else 0

            categoria  = st.selectbox("Categoria", _cats, index=_cat_idx, key="sel_categoria_estoque")

            cultura    = st.selectbox("Cultura", get_culturas() + ["Ambos"], key="cultura_estoque")

            litros_ha  = st.number_input("Litros de calda por hectare", min_value=0.0, value=75.0, key="litros_ha_estoque")

            dose_ha    = st.number_input("Dose por hectare (kg/L)", min_value=0.0, value=0.0, key="dose_ha_estoque")

            capacidade_tanque = st.number_input("Capacidade do tanque (L)", min_value=0,

                                                   value=int(st.session_state.dados.get("cap_tanque_salva", 2000)),

                                                   key="tanque_estoque",

                                                   help="ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Salvo automaticamente")

            if capacidade_tanque != st.session_state.dados.get("cap_tanque_salva", 2000) and capacidade_tanque > 0:

                st.session_state.dados["cap_tanque_salva"] = capacidade_tanque

                salvar_dados_iaagro()

        with col2:

            quantidade  = st.number_input("Quantidade em estoque", min_value=0.0, value=0.0, key="num_quantidade_em_e_4611")

            unidade     = st.selectbox("Unidade do estoque", ["kg","litros","ton","sacos","galÃÂÃÂµes","unidades"], key="sel_unidade_do_esto_4612")



            # Embalagem baseada na unidade

            if unidade == "kg":

                embalagem_opts = ["1 kg","2 kg","5 kg","10 kg","15 kg","20 kg","25 kg","30 kg","50 kg","Granel"]

            elif unidade == "litros":

                embalagem_opts = ["200 ml","500 ml","1 litro","2 litros","5 litros","10 litros","20 litros","200 litros","Granel"]

            elif unidade == "sacos":

                embalagem_opts = ["Saco 20 kg","Saco 25 kg","Saco 40 kg","Saco 50 kg","Saco 60 kg"]

            elif unidade == "ton":

                embalagem_opts = ["Big Bag 500 kg","Big Bag 1000 kg","Granel tonelada"]

            elif unidade == "galÃÂÃÂµes":

                embalagem_opts = ["GalÃÂÃÂ£o 5L","GalÃÂÃÂ£o 10L","GalÃÂÃÂ£o 20L","GalÃÂÃÂ£o 50L"]

            else:

                embalagem_opts = ["Unidade","Caixa","Fardo","Par"]



            embalagem = st.selectbox("Embalagem / ApresentaÃÂÃÂ§ÃÂÃÂ£o", embalagem_opts, key="sel_embalagem_estoque")

        with col3:

            valor_unitario = st.number_input("Valor unitÃÂÃÂ¡rio R$", min_value=0.0, value=0.0, key="num_valor_unit_rio__4614")

            estoque_minimo = st.number_input("Estoque mÃÂÃÂ­nimo", min_value=0.0, value=0.0, key="num_estoque_m_nimo_4615")

    

        observacao = st.text_area("ObservaÃÂÃÂ§ÃÂÃÂ£o", key="txa_observa__o_4617")

    

        _pode_est, _usado_est, _limite_est = verificar_limite("estoque")

        if not _pode_est:

            bloco_upgrade("estoque", _usado_est, _limite_est)

        elif st.button("Adicionar Produto ao Estoque"):

            nome_usar = nome_final.strip() if nome_final.strip() else nome_insumo.strip()

            if not nome_usar:

                error_box("Digite ou selecione o nome do produto.")

            else:

                # Verifica se produto jÃÂÃÂ¡ existe ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ se sim, soma quantidade e valor

                existente = next((i for i in st.session_state.estoque

                                  if i.get("Insumo","").strip().lower() == nome_usar.lower()), None)

                if existente:

                    existente["Quantidade"]      = existente.get("Quantidade", 0) + quantidade

                    existente["Valor Total R$"]  = existente["Quantidade"] * existente.get("Valor UnitÃÂÃÂ¡rio R$", valor_unitario)

                    if valor_unitario > 0:

                        existente["Valor UnitÃÂÃÂ¡rio R$"] = valor_unitario

                    if estoque_minimo > 0:

                        existente["Estoque MÃÂÃÂ­nimo"] = estoque_minimo

                    salvar_dados_iaagro()

                    success_box(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ Estoque de **{nome_usar}** atualizado! Nova quantidade: {existente['Quantidade']:.1f} {existente.get('Unidade','')}")

                else:

                    novo_item = {

                        "Insumo": nome_usar, "Categoria": categoria,

                        "Quantidade": quantidade, "Unidade": unidade,

                        "Embalagem": embalagem,

                        "Valor UnitÃÂÃÂ¡rio R$": valor_unitario,

                        "Valor Total R$": quantidade * valor_unitario,

                        "Estoque MÃÂÃÂ­nimo": estoque_minimo,

                        "ObservaÃÂÃÂ§ÃÂÃÂ£o": observacao, "Cultura": cultura,

                        "Dose ha": dose_ha, "Litros ha": litros_ha,

                        "Tanque litros": capacidade_tanque,

                        "Fabricante": st.session_state.ac_selecionado["fab"] if st.session_state.ac_selecionado else "",

                        "Ingrediente Ativo": st.session_state.ac_selecionado["ia"] if st.session_state.ac_selecionado else "",

                    }

                    st.session_state.estoque.append(novo_item)

                    salvar_dados_iaagro()

                    success_box(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ {nome_usar} adicionado ao estoque.")

                # Reseta autocomplete apÃÂÃÂ³s adicionar

                st.session_state.ac_selecionado = None

                st.session_state.ac_query = ""

    

        st.subheader("Estoque Atual")

        if len(st.session_state.estoque) == 0:

            info_box("Nenhum produto cadastrado ainda.")

        else:

            tabela_estoque = pd.DataFrame(st.session_state.estoque)

            # Garante coluna Embalagem mesmo em registros antigos

            if "Embalagem" not in tabela_estoque.columns:

                tabela_estoque["Embalagem"] = "ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"

            else:

                tabela_estoque["Embalagem"] = tabela_estoque["Embalagem"].fillna("ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ")

    

            st.markdown("### ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Excluir Produto")

            produto_excluir = st.selectbox(

                "Selecione o produto",

                [item["Insumo"] for item in st.session_state.estoque],

                key="produto_excluir_estoque"

            )

            if st.button("ÃÂ¢ÃÂÃÂ Excluir Produto", key="btn_excluir_produto"):

                st.session_state.estoque = [i for i in st.session_state.estoque if i["Insumo"] != produto_excluir]

                salvar_dados_iaagro()

                success_box(f"{produto_excluir} removido do estoque.")

                st.rerun()

    

            tabela_estoque["Status"] = tabela_estoque.apply(

                lambda linha: "Estoque baixo" if linha["Quantidade"] <= linha["Estoque MÃÂÃÂ­nimo"] else "OK", axis=1

            )

            st.dataframe(tabela_estoque, use_container_width=True)

    

            st.subheader("ÃÂ°ÃÂ¸ÃÂ¡ÃÂ¨ Alertas Inteligentes")

            for item in st.session_state.estoque:

                qtd  = item.get("Quantidade", 0)

                nome = item.get("Insumo", "Produto")

                if   qtd <= 0:   error_box(f"ÃÂ¢ÃÂÃÂ {nome}: estoque zerado!")

                elif qtd <= 500: warning_box(f"ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ {nome}: estoque baixo ({qtd:.1f} kg/L)")

                else:            success_box(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ {nome}: estoque OK ({qtd:.1f} kg/L)")

    

            col4, col5, col6 = st.columns(3)

            col4.metric("Itens cadastrados",      len(tabela_estoque))

            col5.metric("Valor total em estoque", f"R$ {tabela_estoque['Valor Total R$'].sum():,.2f}")

            col6.metric("Itens com estoque baixo", len(tabela_estoque[tabela_estoque["Status"] == "Estoque baixo"]))

    

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: APLICAÃÂÃ¢ÂÂ¡ÃÂÃ¢ÂÂ¢ES

# CORREÃÂÃ¢ÂÂ¡ÃÂÃ¢ÂÂ¢ES:

#   - operador/pulverizador/velocidade/pressao/clima movidos para fora do loop

#   - loop aninhado duplicado removido

#   - key duplicada no botÃÂÃÂ£o corrigida com ÃÂÃÂ­ndice ÃÂÃÂºnico

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ Operacional":

  with _sub_op[1]:

    st.header("ÃÂ°ÃÂ¸ÃÂ¡ÃÂ AplicaÃÂÃÂ§ÃÂÃÂµes AgrÃÂÃÂ­colas")



    if "aplicacoes" not in st.session_state:

        st.session_state.aplicacoes = []



    ESTADIOS = [

        "ÃÂ°ÃÂ¸ÃÂÃÂ± PrÃÂÃÂ©-plantio","ÃÂ°ÃÂ¸ÃÂÃÂ¿ PÃÂÃÂ³s-plantio / V0","ÃÂ°ÃÂ¸ÃÂÃÂ¾ V1 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ V3","ÃÂ°ÃÂ¸ÃÂÃÂ¾ V4 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ V6",

        "ÃÂ°ÃÂ¸ÃÂÃÂ¾ V7 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ VT","ÃÂ°ÃÂ¸ÃÂÃÂ¸ R1 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ R2 (FloraÃÂÃÂ§ÃÂÃÂ£o)","ÃÂ°ÃÂ¸ÃÂ«ÃÂ R3 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ R4 (GranaÃÂÃÂ§ÃÂÃÂ£o)",

        "ÃÂ°ÃÂ¸ÃÂ«ÃÂ R5 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ R6","ÃÂ°ÃÂ¸ÃÂÃÂ¾ PrÃÂÃÂ©-colheita","ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Outro",

    ]

    TIPOS_PRODUTO = ["Herbicida","Fungicida","Inseticida","Adjuvante",

                     "ÃÂÃ¢ÂÂleo mineral/vegetal","Fertilizante foliar","Regulador","Outro"]



    if len(st.session_state.estoque) == 0:

        warning_box("Cadastre produtos no estoque antes de registrar aplicaÃÂÃÂ§ÃÂÃÂµes.")

    else:

        st.subheader("ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Nova AplicaÃÂÃÂ§ÃÂÃÂ£o")

        col_h1, col_h2, col_h3 = st.columns(3)

        with col_h1:

            estadio_sel = st.selectbox("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¦ EstÃÂÃÂ¡dio fenolÃÂÃÂ³gico", ESTADIOS, key="sel_estadio_aplic")

            # Nome automÃÂÃÂ¡tico conforme estÃÂÃÂ¡dio ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ sÃÂÃÂ³ pede digitaÃÂÃÂ§ÃÂÃÂ£o se "Outro"

            if estadio_sel == "ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Outro":

                nome_aplic = st.text_input("Nome da aplicaÃÂÃÂ§ÃÂÃÂ£o", placeholder="Ex: AplicaÃÂÃÂ§ÃÂÃÂ£o especial",

                                            key="txt_nome_aplic")

            else:

                nome_aplic = estadio_sel

                st.info(f"ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Nome: **{nome_aplic}**")

        with col_h2:

            data_aplic = st.date_input("Data", key="dat_data_aplic")

            area_aplic = st.number_input("ÃÂÃÂrea (ha)", min_value=0.0,

                                          value=float(st.session_state.dados.get("area", 0.0)),

                                          key="num_area_aplic")

        with col_h3:

            calda_lha  = st.number_input("Volume calda (L/ha)", min_value=0.0, value=100.0, key="num_calda_lha")

            # Carrega capacidade salva ou usa padrÃÂÃÂ£o 3000L

            _cap_salva = st.session_state.dados.get("cap_tanque_salva", 3000.0)

            cap_tanque = st.number_input("Capacidade tanque (L)", min_value=0.0,

                                          value=float(_cap_salva), key="num_cap_tanque",

                                          help="ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Salvo automaticamente para prÃÂÃÂ³ximas aplicaÃÂÃÂ§ÃÂÃÂµes")

            # Salva automaticamente quando muda

            if cap_tanque != _cap_salva and cap_tanque > 0:

                st.session_state.dados["cap_tanque_salva"] = cap_tanque

                salvar_dados_iaagro()

                st.caption(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ Tanque de {cap_tanque:.0f}L salvo!")



        area_por_tanque = round(cap_tanque / calda_lha, 2) if calda_lha > 0 else 0

        n_tanques       = round(area_aplic / area_por_tanque, 2) if area_por_tanque > 0 else 0

        col_m1, col_m2  = st.columns(2)

        col_m1.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ ÃÂÃÂrea por tanque", f"{area_por_tanque} ha")

        col_m2.metric("ÃÂ°ÃÂ¸ÃÂªÃÂ£ NÃÂÃÂº de tanques",   f"{n_tanques}")



        with st.expander("ÃÂ°ÃÂ¸ÃÂ§Ã¢ÂÂÃÂ¢Ã¢ÂÂ¬ÃÂÃÂ°ÃÂ¸ÃÂÃÂ¾ Dados do operador", expanded=False):

            col_o1, col_o2, col_o3 = st.columns(3)

            operador     = col_o1.text_input("Operador", key="txt_operador_aplic")

            pulverizador = col_o2.text_input("Pulverizador/MÃÂÃÂ¡quina", key="txt_pulv_aplic")

            velocidade   = col_o1.number_input("Velocidade (km/h)", min_value=0.0, key="num_veloc_aplic")

            pressao      = col_o2.number_input("PressÃÂÃÂ£o (bar)", min_value=0.0, key="num_pressao_aplic")

            clima_aplic  = col_o3.selectbox("Clima", ["Adequado","Vento alto","Muito seco","Chuva prÃÂÃÂ³xima","Muito quente"], key="sel_clima_aplic")



        st.subheader("ÃÂ°ÃÂ¸ÃÂ§ÃÂª Produtos da AplicaÃÂÃÂ§ÃÂÃÂ£o")

        st.caption("Adicione quantos produtos precisar: herbicida, fungicida, adjuvante, ÃÂÃÂ³leo, etc.")

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

            _obs_p = col_p5.text_input("Obs.",      placeholder="adjuvante, sequÃÂÃÂªncia...", key=f"txt_obs_prod_{i}")

            _por_tanque = round(_dose * area_por_tanque, 3)

            _total_prod = round(_dose * area_aplic, 3)

            if _dose > 0:

                st.caption(f"  ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ {_por_tanque} {_unid.replace('/ha','')} por tanque | Total: {_total_prod} {_unid.replace('/ha','')}")

            produtos_aplic.append({

                "Produto": _prod, "Tipo": _tipo_p, "Dose por ha": _dose, "Unidade": _unid,

                "Produto por tanque": _por_tanque, "Total usado": _total_prod, "ObservaÃÂÃÂ§ÃÂÃÂ£o": _obs_p

            })



        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Salvar AplicaÃÂÃÂ§ÃÂÃÂ£o", key="salvar_aplicacao_modelada", use_container_width=True):

            erro = False

            if not nome_aplic.strip(): error_box("Informe o nome da aplicaÃÂÃÂ§ÃÂÃÂ£o."); erro = True

            if area_aplic <= 0:        error_box("Informe a ÃÂÃÂ¡rea aplicada."); erro = True

            for p in produtos_aplic:

                if p["Dose por ha"] <= 0: error_box(f"Dose zero: {p['Produto']}."); erro = True

            if not erro:

                for p in produtos_aplic:

                    s, m = baixar_estoque(p["Produto"], p["Total usado"], p.get("Unidade","L/ha"))

                    if not s: error_box(f"{p['Produto']}: {m}"); erro = True

            if not erro:

                st.session_state.aplicacoes.append({

                    "ID ÃÂÃÂrea":             st.session_state.dados.get("id_area",""),

                    "EstÃÂÃÂ¡dio":             estadio_sel,

                    "AplicaÃÂÃÂ§ÃÂÃÂ£o":           nome_aplic,

                    "Data":                str(data_aplic),

                    "ÃÂÃÂrea aplicada ha":    area_aplic,

                    "Volume calda L/ha":   calda_lha,

                    "Capacidade tanque L": cap_tanque,

                    "ÃÂÃÂrea por tanque ha":  area_por_tanque,

                    "NÃÂÃÂºmero tanques":      n_tanques,

                    "Operador":            operador,

                    "Pulverizador":        pulverizador,

                    "Velocidade km/h":     velocidade,

                    "PressÃÂÃÂ£o bar":         pressao,

                    "Clima aplicaÃÂÃÂ§ÃÂÃÂ£o":     clima_aplic,

                    "Produtos":            produtos_aplic

                })

                atualizar_area_atual()

                salvar_dados_iaagro()

                success_box(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ {nome_aplic} salva! {len(produtos_aplic)} produto(s).")

                st.rerun()



        st.divider()

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ HistÃÂÃÂ³rico de AplicaÃÂÃÂ§ÃÂÃÂµes")



        # BotÃÂÃÂ£o PDF de programaÃÂÃÂ§ÃÂÃÂ£o

        if st.session_state.aplicacoes:

            _d = st.session_state.dados

            if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Gerar PDF ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ ProgramaÃÂÃÂ§ÃÂÃÂ£o de AplicaÃÂÃÂ§ÃÂÃÂµes",

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

                    st.success("ÃÂ¢ÃÂÃ¢ÂÂ¦ PDF gerado! Clique em Baixar abaixo.")

                except Exception as e:

                    st.error(f"Erro ao gerar PDF: {e}")



            if st.session_state.get("_pdf_aplic"):

                st.download_button(

                    label       = "ÃÂ¢ÃÂ¬Ã¢ÂÂ¡ÃÂ¯ÃÂ¸ÃÂ Baixar PDF",

                    data        = st.session_state["_pdf_aplic"],

                    file_name   = f"programacao_aplicacoes_{datetime.now().strftime('%d%m%Y')}.pdf",

                    mime        = "application/pdf",

                    use_container_width = True,

                    key         = "btn_download_pdf_aplic"

                )

        if len(st.session_state.aplicacoes) == 0:

            info_box("Nenhuma aplicaÃÂÃÂ§ÃÂÃÂ£o registrada ainda.")

        else:

            _ordem = {"ÃÂ°ÃÂ¸ÃÂÃÂ± PrÃÂÃÂ©-plantio":1,"ÃÂ°ÃÂ¸ÃÂÃÂ¿ PÃÂÃÂ³s-plantio / V0":2,"ÃÂ°ÃÂ¸ÃÂÃÂ¾ V1 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ V3":3,

                      "ÃÂ°ÃÂ¸ÃÂÃÂ¾ V4 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ V6":4,"ÃÂ°ÃÂ¸ÃÂÃÂ¾ V7 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ VT":5,"ÃÂ°ÃÂ¸ÃÂÃÂ¸ R1 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ R2 (FloraÃÂÃÂ§ÃÂÃÂ£o)":6,

                      "ÃÂ°ÃÂ¸ÃÂ«ÃÂ R3 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ R4 (GranaÃÂÃÂ§ÃÂÃÂ£o)":7,"ÃÂ°ÃÂ¸ÃÂ«ÃÂ R5 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ R6":8,"ÃÂ°ÃÂ¸ÃÂÃÂ¾ PrÃÂÃÂ©-colheita":9}

            aplicacoes_ordenadas = sorted(st.session_state.aplicacoes,

                key=lambda x: _ordem.get(x.get("EstÃÂÃÂ¡dio", x.get("AplicaÃÂÃÂ§ÃÂÃÂ£o","")), 99))



            for idx_a, aplic in enumerate(aplicacoes_ordenadas):

                _status = aplic.get("Status", "pendente")

                _cor_card = "#14532d" if _status == "aplicado" else "#1e3a5f"

                _badge    = "ÃÂ¢ÃÂÃ¢ÂÂ¦ Aplicado" if _status == "aplicado" else "ÃÂ¢ÃÂÃÂ³ Pendente"



                with st.expander(f"{aplic.get('EstÃÂÃÂ¡dio','') or aplic.get('AplicaÃÂÃÂ§ÃÂÃÂ£o','')} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {aplic.get('Data','')} | {_badge}", expanded=False):

                    col_i1, col_i2 = st.columns(2)

                    col_i1.markdown(f"**ÃÂÃÂrea:** {aplic.get('ÃÂÃÂrea aplicada ha',0)} ha")

                    col_i1.markdown(f"**Calda:** {aplic.get('Volume calda L/ha',0)} L/ha")

                    col_i1.markdown(f"**Tanques:** {aplic.get('NÃÂÃÂºmero tanques',0):.1f}")

                    col_i2.markdown(f"**Operador:** {aplic.get('Operador','ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ')}")

                    col_i2.markdown(f"**Pulverizador:** {aplic.get('Pulverizador','ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ')}")

                    col_i2.markdown(f"**Clima:** {aplic.get('Clima aplicaÃÂÃÂ§ÃÂÃÂ£o','ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ')}")



                    # Produtos

                    st.markdown("**ÃÂ°ÃÂ¸ÃÂ§ÃÂª Produtos:**")

                    _prods = aplic.get("Produtos", [])

                    for p in _prods:

                        st.markdown(f"- **{p.get('Produto','')}** ({p.get('Tipo','')}) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ "

                                    f"{p.get('Dose por ha',0)} {p.get('Unidade','')} | "

                                    f"Total: {p.get('Total usado',0)} {p.get('Unidade','').replace('/ha','')}")



                    col_b1, col_b2 = st.columns(2)



                    # BotÃÂÃÂ£o confirmar aplicaÃÂÃÂ§ÃÂÃÂ£o e dar baixa no estoque

                    if _status != "aplicado":

                        if col_b1.button("ÃÂ¢ÃÂÃ¢ÂÂ¦ Confirmar AplicaÃÂÃÂ§ÃÂÃÂ£o (dÃÂÃÂ¡ baixa no estoque)",

                                          key=f"btn_confirmar_aplic_{idx_a}", use_container_width=True):

                            _erro_baixa = False

                            for p in _prods:

                                s, m = baixar_estoque(p["Produto"], p.get("Total usado", 0), p.get("Unidade","L/ha"))

                                if not s:

                                    st.warning(f"ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ {p['Produto']}: {m}")

                                    _erro_baixa = True

                            # Marca como aplicado

                            _idx_orig = st.session_state.aplicacoes.index(aplic)

                            st.session_state.aplicacoes[_idx_orig]["Status"] = "aplicado"

                            salvar_dados_iaagro()

                            if not _erro_baixa:

                                success_box(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ AplicaÃÂÃÂ§ÃÂÃÂ£o confirmada! Estoque atualizado.")

                            else:

                                success_box("AplicaÃÂÃÂ§ÃÂÃÂ£o marcada. Verifique o estoque manualmente.")

                            st.rerun()

                    else:

                        col_b1.success("ÃÂ¢ÃÂÃ¢ÂÂ¦ JÃÂÃÂ¡ confirmada e baixa dada no estoque")



                    # BotÃÂÃÂ£o excluir

                    if col_b2.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Excluir", key=f"apagar_app_{idx_a}", use_container_width=True):

                        _idx_orig = st.session_state.aplicacoes.index(aplic)

                        st.session_state.aplicacoes.pop(_idx_orig)

                        salvar_dados_iaagro()

                        st.rerun()



  with _sub_op[2]:

    st.header("ÃÂ¢ÃÂÃÂ±ÃÂ¯ÃÂ¸ÃÂ Controle de Prazo de CarÃÂÃÂªncia e Reentrada")

    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;

    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">

    ÃÂ¢Ã¢ÂÂÃÂ¹ÃÂ¯ÃÂ¸ÃÂ Registre os defensivos aplicados e acompanhe automaticamente os prazos de

    carÃÂÃÂªncia (colheita) e reentrada (entrada segura na lavoura).

    </div>''', unsafe_allow_html=True)



    # Init storage

    if "carencia_registros" not in st.session_state:

        st.session_state.carencia_registros = []



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Cadastrar nova aplicaÃÂÃÂ§ÃÂÃÂ£o com carÃÂÃÂªncia ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    st.subheader("ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Registrar AplicaÃÂÃÂ§ÃÂÃÂ£o com CarÃÂÃÂªncia")

    col1, col2, col3 = st.columns(3)

    with col1:

        car_produto    = st.text_input("Nome do produto/defensivo", key="car_produto")

        car_cultura    = st.selectbox("Cultura", get_culturas() + ["Outra"], key="car_cultura")

        car_data_aplic = st.date_input("Data da aplicaÃÂÃÂ§ÃÂÃÂ£o", key="car_data")

    with col2:

        car_carencia   = st.number_input("Prazo de carÃÂÃÂªncia (dias)", min_value=0, value=14, key="car_carencia",

                                          help="Dias apÃÂÃÂ³s aplicaÃÂÃÂ§ÃÂÃÂ£o atÃÂÃÂ© a colheita segura")

        car_reentrada  = st.number_input("Prazo de reentrada (horas)", min_value=0, value=48, key="car_reentrada",

                                          help="Horas apÃÂÃÂ³s aplicaÃÂÃÂ§ÃÂÃÂ£o para entrar na lavoura com seguranÃÂÃÂ§a")

        car_dose       = st.text_input("Dose aplicada", placeholder="Ex: 0.5 L/ha", key="car_dose")

    with col3:

        car_talhao     = st.text_input("TalhÃÂÃÂ£o/ÃÂÃÂrea", key="car_talhao")

        car_epi        = st.multiselect("EPI necessÃÂÃÂ¡rio",

                                         ["MÃÂÃÂ¡scara","Luvas","ÃÂÃ¢ÂÂculos","MacacÃÂÃÂ£o","Botas","Protetor Auricular"],

                                         key="car_epi")

        car_obs        = st.text_area("ObservaÃÂÃÂ§ÃÂÃÂµes", key="car_obs", height=80)



    if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Salvar Registro de CarÃÂÃÂªncia", key="btn_salvar_carencia"):

        if not car_produto.strip():

            error_box("Digite o nome do produto.")

        else:

            from datetime import timedelta

            data_colheita_seg = car_data_aplic + timedelta(days=int(car_carencia))

            data_reentrada    = datetime.combine(car_data_aplic, datetime.min.time()) + timedelta(hours=int(car_reentrada))

            st.session_state.carencia_registros.append({

                "Produto":          car_produto,

                "Cultura":          car_cultura,

                "TalhÃÂÃÂ£o":           car_talhao,

                "Data AplicaÃÂÃÂ§ÃÂÃÂ£o":   str(car_data_aplic),

                "CarÃÂÃÂªncia dias":    car_carencia,

                "Data Colheita Segura": str(data_colheita_seg),

                "Reentrada horas":  car_reentrada,

                "Data Reentrada":   str(data_reentrada.date()),

                "Dose":             car_dose,

                "EPI":              ", ".join(car_epi),

                "ObservaÃÂÃÂ§ÃÂÃÂµes":      car_obs,

            })

            salvar_dados_iaagro()

            success_box(f"Registro de {car_produto} salvo! CarÃÂÃÂªncia atÃÂÃÂ©: {data_colheita_seg} | Reentrada: {data_reentrada.strftime('%d/%m/%Y %H:%M')}")



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Painel de situaÃÂÃÂ§ÃÂÃÂ£o ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    if st.session_state.carencia_registros:

        st.divider()

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  SituaÃÂÃÂ§ÃÂÃÂ£o dos Prazos")



        hoje = date.today()

        registros_status = []

        for r in st.session_state.carencia_registros:

            data_colh  = date.fromisoformat(r["Data Colheita Segura"])

            data_reent = date.fromisoformat(r["Data Reentrada"])

            dias_colh  = (data_colh - hoje).days

            dias_reent = (data_reent - hoje).days



            if dias_colh < 0:

                status_colh = "ÃÂ¢ÃÂÃ¢ÂÂ¦ Liberado para colheita"

            elif dias_colh == 0:

                status_colh = "ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Liberado hoje"

            else:

                status_colh = f"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ {dias_colh} dias para colheita segura"



            if dias_reent < 0:

                status_reent = "ÃÂ¢ÃÂÃ¢ÂÂ¦ Reentrada liberada"

            elif dias_reent == 0:

                status_reent = "ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Reentrada liberada hoje"

            else:

                status_reent = f"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Aguardar {dias_reent} dia(s) para reentrada"



            registros_status.append({

                "Produto":         r["Produto"],

                "Cultura":         r["Cultura"],

                "TalhÃÂÃÂ£o":          r["TalhÃÂÃÂ£o"],

                "AplicaÃÂÃÂ§ÃÂÃÂ£o":       r["Data AplicaÃÂÃÂ§ÃÂÃÂ£o"],

                "Colheita Segura": r["Data Colheita Segura"],

                "Status Colheita": status_colh,

                "Status Reentrada":status_reent,

                "EPI":             r["EPI"],

            })



        df_car = pd.DataFrame(registros_status)

        st.dataframe(df_car, use_container_width=True)



        # Alertas visuais

        st.divider()

        st.subheader("ÃÂ°ÃÂ¸ÃÂ¡ÃÂ¨ Alertas Ativos")

        alertas_ativos = False

        for r in registros_status:

            if "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´" in r["Status Colheita"]:

                st.markdown(f'''<div style="background:#7f1d1d;color:#fff;padding:12px 18px;

                border-radius:10px;border-left:5px solid #ef4444;font-weight:700;margin:4px 0;">

                ÃÂ°ÃÂ¸ÃÂÃÂ¾ {r["Produto"]} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {r["TalhÃÂÃÂ£o"]}: {r["Status Colheita"]}</div>''',

                unsafe_allow_html=True)

                alertas_ativos = True

            if "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´" in r["Status Reentrada"]:

                st.markdown(f'''<div style="background:#78350f;color:#fff;padding:12px 18px;

                border-radius:10px;border-left:5px solid #f59e0b;font-weight:700;margin:4px 0;">

                ÃÂ¢Ã¢ÂÂºÃ¢ÂÂ {r["Produto"]} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {r["TalhÃÂÃÂ£o"]}: {r["Status Reentrada"]} | EPI: {r["EPI"]}</div>''',

                unsafe_allow_html=True)

                alertas_ativos = True

        if not alertas_ativos:

            success_box("Nenhum prazo de carÃÂÃÂªncia ou reentrada pendente no momento!")



        # Excluir registro

        st.divider()

        opcoes_del = [f"{r['Produto']} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {r['TalhÃÂÃÂ£o']} ({r['Data AplicaÃÂÃÂ§ÃÂÃÂ£o']})"

                      for r in st.session_state.carencia_registros]

        del_choice = st.selectbox("Excluir registro", opcoes_del, key="del_carencia")

        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Excluir", key="btn_del_carencia"):

            idx = opcoes_del.index(del_choice)

            st.session_state.carencia_registros.pop(idx)

            salvar_dados_iaagro()

            success_box("Registro removido.")

            st.rerun()





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: ORDEM DE SERVIÃÂÃ¢ÂÂ¡O

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ Operacional":

  with _sub_op[3]:

    st.header("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Ordem de ServiÃÂÃÂ§o")

    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;

    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">

    ÃÂ¢Ã¢ÂÂÃÂ¹ÃÂ¯ÃÂ¸ÃÂ Gere uma Ordem de ServiÃÂÃÂ§o completa para o operador ir ao campo. Pode ser impressa ou salva em PDF.

    </div>''', unsafe_allow_html=True)



    col1, col2 = st.columns(2)

    with col1:

        os_numero     = st.text_input("NÃÂÃÂºmero da OS", value=f"OS-{datetime.now().strftime('%Y%m%d%H%M')}", key="txt_n_mero_da_os_6029")

        os_data       = st.date_input("Data da OS", value=date.today(), key="dat_data_da_os_6030")

        os_fazenda    = st.text_input("Fazenda", value=st.session_state.dados.get("fazenda",""), key="txt_fazenda_6031")

        os_talhao     = st.text_input("TalhÃÂÃÂ£o", value=st.session_state.dados.get("talhao",""), key="txt_talh_o_6032")

        os_area       = st.number_input("ÃÂÃÂrea (ha)", value=float(st.session_state.dados.get("area",0)), key="num__rea__ha__6033")

        os_cultura    = st.text_input("Cultura", value=st.session_state.dados.get("cultura",""), key="txt_cultura_6034")

    with col2:

        os_operador   = st.text_input("Operador responsÃÂÃÂ¡vel", key="txt_operador_respon_6036")

        os_maquina    = st.text_input("MÃÂÃÂ¡quina / Pulverizador", key="txt_m_quina___pulve_6037")

        os_velocidade = st.number_input("Velocidade (km/h)", value=6.0, key="num_velocidade__km__6038")

        os_pressao    = st.number_input("PressÃÂÃÂ£o de trabalho (bar)", value=2.5, key="num_press_o_de_trab_6039")

        os_volume     = st.number_input("Volume de calda (L/ha)", value=100.0, key="num_volume_de_calda_6040")

        os_inicio     = st.text_input("HorÃÂÃÂ¡rio previsto de inÃÂÃÂ­cio", placeholder="Ex: 06:30", key="txt_hor_rio_previst_6041")



    st.subheader("ÃÂ°ÃÂ¸ÃÂ§ÃÂª Produtos da OS")

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



    os_epi     = st.multiselect("EPI obrigatÃÂÃÂ³rio",

                                 ["MÃÂÃÂ¡scara com filtro","Luvas nitrÃÂÃÂ­licas","ÃÂÃ¢ÂÂculos de proteÃÂÃÂ§ÃÂÃÂ£o",

                                  "MacacÃÂÃÂ£o impermeÃÂÃÂ¡vel","Botas de borracha","Protetor auricular","Avental"],

                                 key="os_epi")

    os_obs_geral = st.text_area("ObservaÃÂÃÂ§ÃÂÃÂµes gerais", key="os_obs_geral")



    if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Gerar Ordem de ServiÃÂÃÂ§o (PDF)", key="btn_gerar_os"):

        from reportlab.lib.units import cm

        buf = BytesIO()

        doc = SimpleDocTemplate(buf, pagesize=A4,

                                rightMargin=1.5*cm, leftMargin=1.5*cm,

                                topMargin=1.5*cm, bottomMargin=1.5*cm)

        styles = getSampleStyleSheet()

        el = []



        # CabeÃÂÃÂ§alho

        if os.path.exists("IAAgrologo.jpeg"):

            el.append(Image("IAAgrologo.jpeg", width=3*cm, height=1.5*cm))

        el.append(Spacer(1, 6))



        # TÃÂÃÂ­tulo

        titulo_style = styles["Title"]

        el.append(Paragraph(f"<b>ORDEM DE SERVIÃÂÃ¢ÂÂ¡O ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {os_numero}</b>", titulo_style))

        el.append(Paragraph(f"Data: {os_data} | Fazenda: {os_fazenda} | TalhÃÂÃÂ£o: {os_talhao}", styles["Normal"]))

        el.append(Spacer(1, 12))



        # Dados gerais

        dados_os = [

            ["Campo","InformaÃÂÃÂ§ÃÂÃÂ£o","Campo","InformaÃÂÃÂ§ÃÂÃÂ£o"],

            ["Fazenda", os_fazenda, "Operador", os_operador],

            ["TalhÃÂÃÂ£o",  os_talhao,  "MÃÂÃÂ¡quina",  os_maquina],

            ["ÃÂÃÂrea",    f"{os_area} ha", "Cultura", os_cultura],

            ["Volume calda", f"{os_volume} L/ha", "Velocidade", f"{os_velocidade} km/h"],

            ["PressÃÂÃÂ£o", f"{os_pressao} bar", "InÃÂÃÂ­cio previsto", os_inicio],

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

            prod_data = [["Produto","Dose/ha","Total","ObservaÃÂÃÂ§ÃÂÃÂ£o"]] +                         [[p["Produto"],p["Dose/ha"],p["Total"],p["Obs"]] for p in os_produtos]

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

            el.append(Paragraph("<b>EPI OBRIGATÃÂÃ¢ÂÂRIO:</b> " + " | ".join(os_epi), styles["Normal"]))

            el.append(Spacer(1, 8))



        # ObservaÃÂÃÂ§ÃÂÃÂµes

        if os_obs_geral:

            el.append(Paragraph(f"<b>ObservaÃÂÃÂ§ÃÂÃÂµes:</b> {os_obs_geral}", styles["Normal"]))

            el.append(Spacer(1, 16))



        # Assinaturas

        assin = Table([

            ["_"*35, " ", "_"*35],

            ["Operador / Data", " ", "ResponsÃÂÃÂ¡vel TÃÂÃÂ©cnico / Data"],

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

            "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Baixar Ordem de ServiÃÂÃÂ§o PDF",

            data=pdf_os,

            file_name=f"OS_{os_numero}_{os_data}.pdf",

            mime="application/pdf",

            use_container_width=True

        )

        success_box(f"OS {os_numero} gerada com sucesso!")





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: DASHBOARD FINANCEIRO

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Financeiro":

  with _sub_fin[1]:

    st.header("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¹ Dashboard Financeiro ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ DRE por Safra")



    if "dre_registros" not in st.session_state:

        st.session_state.dre_registros = []



    tab_dre, tab_novo, tab_grafico = st.tabs([

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  DRE & Resultados",

        "ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ LanÃÂÃÂ§ar Receita/Custo",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ EvoluÃÂÃÂ§ÃÂÃÂ£o por Safra"

    ])



    with tab_novo:

        st.subheader("ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Novo LanÃÂÃÂ§amento Financeiro")

        col1, col2, col3 = st.columns(3)

        with col1:

            dre_safra    = st.text_input("Safra", placeholder="2024/2025", key="dre_safra")

            dre_tipo     = st.selectbox("Tipo", ["Receita","Custo VariÃÂÃÂ¡vel","Custo Fixo"], key="dre_tipo")

            dre_categ    = st.selectbox("Categoria", [

                "Venda de grÃÂÃÂ£os","Venda de outros","Semente","Fertilizante",

                "Defensivo","Diesel e lubrificantes","MÃÂÃÂ£o de obra","Aluguel de mÃÂÃÂ¡quinas",

                "Arrendamento","Seguro","Transporte","Armazenagem","Outros"

            ], key="dre_categ")

        with col2:

            dre_descricao = st.text_input("DescriÃÂÃÂ§ÃÂÃÂ£o", key="dre_desc")

            dre_valor     = st.number_input("Valor R$", min_value=0.0, key="dre_valor")

            dre_area_ha   = st.number_input("ÃÂÃÂrea referente (ha)", min_value=0.0,

                                             value=float(st.session_state.dados.get("area",0)),

                                             key="dre_area")

        with col3:

            dre_data_lanc = st.date_input("Data", key="dre_data")

            dre_talhao    = st.text_input("TalhÃÂÃÂ£o/ÃÂÃÂrea", key="dre_talhao")

            dre_cultura   = st.text_input("Cultura", value=st.session_state.dados.get("cultura",""), key="dre_cultura")



        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Salvar LanÃÂÃÂ§amento", key="btn_salvar_dre"):

            if not dre_safra.strip():

                error_box("Informe a safra.")

            elif dre_valor <= 0:

                error_box("Informe um valor maior que zero.")

            else:

                st.session_state.dre_registros.append({

                    "Safra":      dre_safra,

                    "Tipo":       dre_tipo,

                    "Categoria":  dre_categ,

                    "DescriÃÂÃÂ§ÃÂÃÂ£o":  dre_descricao,

                    "Valor R$":   dre_valor,

                    "ÃÂÃÂrea ha":    dre_area_ha,

                    "Valor/ha":   round(dre_valor / dre_area_ha, 2) if dre_area_ha > 0 else 0,

                    "Data":       str(dre_data_lanc),

                    "TalhÃÂÃÂ£o":     dre_talhao,

                    "Cultura":    dre_cultura,

                })

                salvar_dados_iaagro()

                success_box(f"LanÃÂÃÂ§amento salvo! R$ {dre_valor:,.2f} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {dre_categ}")



    with tab_dre:

        if not st.session_state.dre_registros:

            info_box("Nenhum lanÃÂÃÂ§amento financeiro ainda. Use a aba 'LanÃÂÃÂ§ar Receita/Custo'.")

        else:

            df_dre = pd.DataFrame(st.session_state.dre_registros)

            safras_disp = sorted(df_dre["Safra"].unique().tolist(), reverse=True)

            safra_sel   = st.selectbox("Selecione a safra", safras_disp, key="dre_sel_safra")

            df_safra    = df_dre[df_dre["Safra"] == safra_sel]



            receita      = df_safra[df_safra["Tipo"]=="Receita"]["Valor R$"].sum()

            custo_var    = df_safra[df_safra["Tipo"]=="Custo VariÃÂÃÂ¡vel"]["Valor R$"].sum()

            custo_fix    = df_safra[df_safra["Tipo"]=="Custo Fixo"]["Valor R$"].sum()

            custo_total  = custo_var + custo_fix

            lucro_bruto  = receita - custo_var

            lucro_liq    = receita - custo_total

            margem       = (lucro_liq / receita * 100) if receita > 0 else 0

            area_safra   = df_safra["ÃÂÃÂrea ha"].max() if not df_safra.empty else 1

            receita_ha   = receita / area_safra if area_safra > 0 else 0

            custo_ha     = custo_total / area_safra if area_safra > 0 else 0

            lucro_ha     = lucro_liq / area_safra if area_safra > 0 else 0

            breakeven    = custo_total / area_safra if area_safra > 0 else 0



            st.subheader(f"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  DRE ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Safra {safra_sel}")

            col1,col2,col3,col4 = st.columns(4)

            col1.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Receita Total",   f"R$ {receita:,.0f}")

            col2.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¸ Custo Total",     f"R$ {custo_total:,.0f}")

            col3.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂµ Lucro LÃÂÃÂ­quido",   f"R$ {lucro_liq:,.0f}")

            col4.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Margem",          f"{margem:.1f}%")



            col5,col6,col7,col8 = st.columns(4)

            col5.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Receita/ha",  f"R$ {receita_ha:,.0f}")

            col6.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¸ Custo/ha",    f"R$ {custo_ha:,.0f}")

            col7.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂµ Lucro/ha",    f"R$ {lucro_ha:,.0f}")

            col8.metric("ÃÂ¢ÃÂ¡Ã¢ÂÂÃÂ¯ÃÂ¸ÃÂ Break-even",  f"R$ {breakeven:,.0f}/ha")



            # DRE formatado

            st.divider()

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Demonstrativo de Resultado (DRE)")

            dre_lines = [

                {"Item": "RECEITA BRUTA",            "Valor R$": receita,      "Tipo": ""},

                {"Item": "(-) Custos VariÃÂÃÂ¡veis",     "Valor R$": -custo_var,   "Tipo": ""},

                {"Item": "= LUCRO BRUTO",             "Valor R$": lucro_bruto,  "Tipo": ""},

                {"Item": "(-) Custos Fixos",          "Valor R$": -custo_fix,   "Tipo": ""},

                {"Item": "= LUCRO LÃÂÃÂQUIDO",           "Valor R$": lucro_liq,    "Tipo": ""},

                {"Item": f"  Margem LÃÂÃÂ­quida",         "Valor R$": margem,       "Tipo": "%"},

            ]

            df_dre_fmt = pd.DataFrame(dre_lines)

            st.dataframe(df_dre_fmt, use_container_width=True, hide_index=True)



            # LanÃÂÃÂ§amentos detalhados

            st.divider()

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ LanÃÂÃÂ§amentos Detalhados")

            st.dataframe(df_safra[["Data","Tipo","Categoria","DescriÃÂÃÂ§ÃÂÃÂ£o","Valor R$","Valor/ha","TalhÃÂÃÂ£o"]],

                         use_container_width=True, hide_index=True)



            # ComposiÃÂÃÂ§ÃÂÃÂ£o de custos

            st.divider()

            st.subheader("ÃÂ°ÃÂ¸ÃÂ¥ÃÂ§ ComposiÃÂÃÂ§ÃÂÃÂ£o de Custos")

            df_custos = df_safra[df_safra["Tipo"].isin(["Custo VariÃÂÃÂ¡vel","Custo Fixo"])]

            if not df_custos.empty:

                df_comp = df_custos.groupby("Categoria")["Valor R$"].sum().reset_index()

                st.bar_chart(df_comp.set_index("Categoria")["Valor R$"])



            # Exportar DRE

            st.divider()

            xlsx_dre = exportar_excel({

                f"DRE {safra_sel}": dre_lines,

                "LanÃÂÃÂ§amentos":      st.session_state.dre_registros

            })

            if xlsx_dre:

                st.download_button(

                    "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Exportar DRE Excel",

                    data=xlsx_dre,

                    file_name=f"DRE_{safra_sel.replace('/','_')}.xlsx",

                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                    use_container_width=True

                )



    with tab_grafico:

        if len(st.session_state.dre_registros) < 2:

            info_box("LanÃÂÃÂ§e dados de pelo menos 2 safras para ver a evoluÃÂÃÂ§ÃÂÃÂ£o.")

        else:

            df_all  = pd.DataFrame(st.session_state.dre_registros)

            df_evo  = df_all.groupby(["Safra","Tipo"])["Valor R$"].sum().unstack(fill_value=0).reset_index()

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ EvoluÃÂÃÂ§ÃÂÃÂ£o Financeira por Safra")

            st.dataframe(df_evo, use_container_width=True)

            st.line_chart(df_evo.set_index("Safra"))



            # Lucratividade por safra

            df_lucro = df_all.groupby("Safra").apply(

                lambda x: pd.Series({

                    "Receita":     x[x["Tipo"]=="Receita"]["Valor R$"].sum(),

                    "Custo Total": x[x["Tipo"].isin(["Custo VariÃÂÃÂ¡vel","Custo Fixo"])]["Valor R$"].sum(),

                })

            ).reset_index()

            df_lucro["Lucro"] = df_lucro["Receita"] - df_lucro["Custo Total"]

            df_lucro["Margem %"] = (df_lucro["Lucro"] / df_lucro["Receita"] * 100).round(1)

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Lucratividade por Safra")

            st.dataframe(df_lucro, use_container_width=True)

            st.bar_chart(df_lucro.set_index("Safra")["Lucro"])







# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: RELATÃÂÃ¢ÂÂRIO FINAL

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

elif menu == "ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ RelatÃÂÃÂ³rio Final":

    st.header("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ RelatÃÂÃÂ³rio Final da Propriedade")



    if not st.session_state.areas:

        warning_box("Cadastre pelo menos uma ÃÂÃÂ¡rea para gerar o relatÃÂÃÂ³rio.")

    else:

        st.markdown("""

        <div style='background:#0f3460;border-radius:10px;padding:12px 16px;

        border-left:5px solid #22c55e;margin-bottom:12px;'>

        <b style='color:#22c55e;'>ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ RelatÃÂÃÂ³rio completo da propriedade</b><br>

        <span style='color:#f1f5f9;font-size:13px;'>

        Gera um PDF profissional com anÃÂÃÂ¡lise de solo, recomendaÃÂÃÂ§ÃÂÃÂµes de adubaÃÂÃÂ§ÃÂÃÂ£o,

        histÃÂÃÂ³rico de produtividade e resumo da propriedade.

        </span>

        </div>

        """, unsafe_allow_html=True)



        _areas_rel = [f"{a['ID']} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {a.get('TalhÃÂÃÂ£o','?')} ({a.get('Cultura','?')})"

                      for a in st.session_state.areas]

        _sel_rel   = st.selectbox("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ ÃÂÃÂrea para o relatÃÂÃÂ³rio", _areas_rel, key="sel_area_relatorio")

        _id_rel    = _sel_rel.split(" ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ ")[0]

        _area_rel  = next((a for a in st.session_state.areas if a.get("ID") == _id_rel), {})

        _dados_rel = _area_rel.get("Dados", _area_rel.get("dados", {})) or {}



        col_r1, col_r2 = st.columns(2)

        nome_produtor = col_r1.text_input("Nome do produtor",

                                           value=st.session_state.get("usuario_atual",""),

                                           key="rel_produtor")

        municipio = col_r2.text_input("MunicÃÂÃÂ­pio/UF",

                                       value=_dados_rel.get("cidade",""), key="rel_municipio")



        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Gerar RelatÃÂÃÂ³rio Final (PDF)", key="btn_gerar_relatorio", use_container_width=True):

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



                # CabeÃÂÃÂ§alho

                if os.path.exists("IAAgrologo.jpeg"):

                    from reportlab.platypus import Image as RLImage

                    el_r.append(RLImage("IAAgrologo.jpeg", width=3*cm, height=1.5*cm))

                el_r.append(Pr("RELATÃÂÃ¢ÂÂRIO AGRONÃÂÃ¢ÂÂMICO COMPLETO", 16, True, COR_E, TA_CENTER))

                el_r.append(Pr("IAAgro ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ InteligÃÂÃÂªncia AgrÃÂÃÂ­cola de PrecisÃÂÃÂ£o", 9, False, COR_A, TA_CENTER))

                el_r.append(Pr(f"Emitido: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 8, False, rl_colors.HexColor("#64748b"), TA_CENTER))

                el_r.append(Spacer(1, 0.3*cm))

                el_r.append(HRFlowable(width="100%", thickness=2, color=COR_V))

                el_r.append(Spacer(1, 0.3*cm))



                # Info propriedade

                t_inf = Table([[

                    Pr(f"<b>Produtor:</b> {nome_produtor or 'ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ'}"),

                    Pr(f"<b>MunicÃÂÃÂ­pio:</b> {municipio or 'ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ'}"),

                    Pr(f"<b>TalhÃÂÃÂ£o:</b> {_area_rel.get('TalhÃÂÃÂ£o','ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ')}"),

                    Pr(f"<b>ÃÂÃÂrea:</b> {_area_rel.get('Hectares',0)} ha"),

                ]], colWidths=[4*cm,3.5*cm,4*cm,4*cm])

                t_inf.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),COR_C),

                    ("GRID",(0,0),(-1,-1),0.4,COR_B),("TOPPADDING",(0,0),(-1,-1),5),

                    ("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),6)]))

                el_r.append(t_inf); el_r.append(Spacer(1,0.4*cm))



                # AnÃÂÃÂ¡lise de solo

                if "ph" in _dados_rel:

                    el_r.append(Pr("ANÃÂÃÂLISE DE SOLO", 11, True, COR_E))

                    el_r.append(HRFlowable(width="100%", thickness=1, color=COR_V))

                    el_r.append(Spacer(1,0.2*cm))

                    rows_s = [[Pr("<b>ParÃÂÃÂ¢metro</b>",9,True,COR_W),Pr("<b>Valor</b>",9,True,COR_W),

                               Pr("<b>Unidade</b>",9,True,COR_W),Pr("<b>ReferÃÂÃÂªncia</b>",9,True,COR_W)],

                              [Pr("pH"),Pr(str(_dados_rel.get("ph","ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"))),Pr("adimensional"),Pr("5.5ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ6.5")],

                              [Pr("FÃÂÃÂ³sforo P"),Pr(str(_dados_rel.get("fosforo","ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"))),Pr("mg/dm3"),Pr(">12")],

                              [Pr("PotÃÂÃÂ¡ssio K"),Pr(str(_dados_rel.get("potassio","ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"))),Pr("mg/dm3"),Pr(">80")],

                              [Pr("CÃÂÃÂ¡lcio Ca"),Pr(str(_dados_rel.get("calcio","ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"))),Pr("cmolc/dm3"),Pr(">2.0")],

                              [Pr("MagnÃÂÃÂ©sio Mg"),Pr(str(_dados_rel.get("magnesio","ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"))),Pr("cmolc/dm3"),Pr(">0.5")],

                              [Pr("Mat. OrgÃÂÃÂ¢nica"),Pr(str(_dados_rel.get("materia_organica","ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"))),Pr("g/dm3"),Pr(">25")],

                              [Pr("CTC"),Pr(str(_dados_rel.get("ctc","ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"))),Pr("cmolc/dm3"),Pr(">8.0")],

                              [Pr("V%"),Pr(str(_dados_rel.get("v_percent","ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"))),Pr("%"),Pr(">60%")],

                              [Pr("Argila"),Pr(str(_dados_rel.get("argila","ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"))),Pr("%"),Pr("ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ")]]

                    ts = Table(rows_s, colWidths=[4*cm,3*cm,3.5*cm,5*cm])

                    ts.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),COR_E),("TEXTCOLOR",(0,0),(-1,0),COR_W),

                        ("ROWBACKGROUNDS",(0,1),(-1,-1),[COR_C,COR_W]),("GRID",(0,0),(-1,-1),0.4,COR_B),

                        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),

                        ("LEFTPADDING",(0,0),(-1,-1),6)]))

                    el_r.append(ts); el_r.append(Spacer(1,0.4*cm))



                    # RecomendaÃÂÃÂ§ÃÂÃÂ£o NPK

                    el_r.append(Pr("RECOMENDAÃÂÃ¢ÂÂ¡ÃÂÃÂO DE ADUBAÃÂÃ¢ÂÂ¡ÃÂÃÂO (EMBRAPA/CQFS 2016)", 11, True, COR_E))

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

                                   Pr("<b>Total ÃÂÃÂ¡rea</b>",9,True,COR_W),Pr("<b>Fonte sugerida</b>",9,True,COR_W)],

                                  [Pr("NitrogÃÂÃÂªnio (N)"),Pr(f"{n:.0f}"),Pr(f"{n*_aha:.0f} kg"),Pr("Ureia / MAP")],

                                  [Pr("FÃÂÃÂ³sforo (P2O5)"),Pr(f"{p:.0f}"),Pr(f"{p*_aha:.0f} kg"),Pr("MAP / TSP")],

                                  [Pr("PotÃÂÃÂ¡ssio (K2O)"),Pr(f"{k:.0f}"),Pr(f"{k*_aha:.0f} kg"),Pr("KCl")]]

                        tn = Table(rows_n, colWidths=[4*cm,3*cm,4*cm,4.5*cm])

                        tn.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),COR_E),("TEXTCOLOR",(0,0),(-1,0),COR_W),

                            ("ROWBACKGROUNDS",(0,1),(-1,-1),[COR_C,COR_W]),("GRID",(0,0),(-1,-1),0.4,COR_B),

                            ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),

                            ("LEFTPADDING",(0,0),(-1,-1),6)]))

                        el_r.append(tn)

                    except Exception:

                        el_r.append(Pr("Dados insuficientes para recomendaÃÂÃÂ§ÃÂÃÂ£o.",9))

                    el_r.append(Spacer(1,0.4*cm))



                # HistÃÂÃÂ³rico

                _hist = [h for h in st.session_state.historico_produtividade

                         if h.get("ÃÂÃÂrea","").startswith(_id_rel)]

                if _hist:

                    el_r.append(Pr("HISTÃÂÃ¢ÂÂRICO DE PRODUTIVIDADE", 11, True, COR_E))

                    el_r.append(HRFlowable(width="100%", thickness=1, color=COR_V))

                    el_r.append(Spacer(1,0.2*cm))

                    rows_h = [[Pr("<b>Safra</b>",9,True,COR_W),Pr("<b>Cultura</b>",9,True,COR_W),

                               Pr("<b>Produtividade</b>",9,True,COR_W),Pr("<b>Custo R$/ha</b>",9,True,COR_W)]]

                    for h in _hist:

                        rows_h.append([Pr(h.get("Safra","ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"),9),

                                       Pr(cultura_limpa(h.get("Cultura","ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ")),9),

                                       Pr(f"{h.get('Produtividade',0):.1f} sc/ha",9),

                                       Pr(f"R$ {h.get('Custo',0):.2f}",9)])

                    th_ = Table(rows_h, colWidths=[3*cm,4*cm,4*cm,4.5*cm])

                    th_.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),COR_E),("TEXTCOLOR",(0,0),(-1,0),COR_W),

                        ("ROWBACKGROUNDS",(0,1),(-1,-1),[COR_C,COR_W]),("GRID",(0,0),(-1,-1),0.4,COR_B),

                        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),

                        ("LEFTPADDING",(0,0),(-1,-1),6)]))

                    el_r.append(th_); el_r.append(Spacer(1,0.4*cm))



                # RodapÃÂÃÂ©

                el_r.append(HRFlowable(width="100%", thickness=1, color=COR_V))

                el_r.append(Pr(f"IAAgro ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {datetime.now().strftime('%d/%m/%Y %H:%M')} | Uso interno",

                               7, False, rl_colors.HexColor("#64748b"), TA_CENTER))

                doc_r.build(el_r)

                buf_r.seek(0)

                st.session_state["_pdf_relatorio"] = buf_r.read()

                st.success("ÃÂ¢ÃÂÃ¢ÂÂ¦ RelatÃÂÃÂ³rio gerado com sucesso!")

            except Exception as e:

                st.error(f"Erro: {e}")



        if st.session_state.get("_pdf_relatorio"):

            st.download_button(

                label     = "ÃÂ¢ÃÂ¬Ã¢ÂÂ¡ÃÂ¯ÃÂ¸ÃÂ Baixar RelatÃÂÃÂ³rio PDF",

                data      = st.session_state["_pdf_relatorio"],

                file_name = f"relatorio_iaagro_{datetime.now().strftime('%d%m%Y')}.pdf",

                mime      = "application/pdf",

                use_container_width = True,

                key       = "btn_download_relatorio"

            )



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: CALENDÃÂÃÂRIO AGRÃÂÃÂCOLA

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸ÃÂÃÂ InteligÃÂÃÂªncia":

  with _sub_int[3]:

    st.header("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¦ CalendÃÂÃÂ¡rio AgrÃÂÃÂ­cola")



    if "calendario_eventos" not in st.session_state:

        st.session_state.calendario_eventos = []



    tab_cal, tab_novo_ev, tab_plantio = st.tabs([

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¦ CalendÃÂÃÂ¡rio do MÃÂÃÂªs",

        "ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Novo Evento",

        "ÃÂ°ÃÂ¸ÃÂÃÂ± Cronograma de Plantio"

    ])



    with tab_novo_ev:

        st.subheader("ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Cadastrar Evento AgrÃÂÃÂ­cola")

        col1, col2 = st.columns(2)

        with col1:

            ev_tipo   = st.selectbox("Tipo de evento", [

                "ÃÂ°ÃÂ¸ÃÂÃÂ± Plantio","ÃÂ°ÃÂ¸ÃÂÃÂ¿ EmergÃÂÃÂªncia","ÃÂ°ÃÂ¸ÃÂ¡ÃÂ AplicaÃÂÃÂ§ÃÂÃÂ£o","ÃÂ¢ÃÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Poda/Desbaste",

                "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ§ IrrigaÃÂÃÂ§ÃÂÃÂ£o","ÃÂ°ÃÂ¸ÃÂÃÂ¾ Colheita","ÃÂ°ÃÂ¸ÃÂ§ÃÂª AnÃÂÃÂ¡lise de Solo","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ Recebimento de insumos",

                "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ§ ManutenÃÂÃÂ§ÃÂÃÂ£o de equipamentos","ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Vistoria","ÃÂ°ÃÂ¸ÃÂÃÂ¦ÃÂ¯ÃÂ¸ÃÂ Evento climÃÂÃÂ¡tico","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Outro"

            ], key="ev_tipo")

            ev_data   = st.date_input("Data do evento", key="ev_data")

            ev_talhao = st.text_input("TalhÃÂÃÂ£o/ÃÂÃÂrea", key="ev_talhao")

        with col2:

            ev_cultura = st.text_input("Cultura", value=st.session_state.dados.get("cultura",""), key="ev_cultura")

            ev_resp    = st.text_input("ResponsÃÂÃÂ¡vel", key="ev_resp")

            ev_status  = st.selectbox("Status", ["ÃÂ¢ÃÂÃÂ³ Planejado","ÃÂ¢ÃÂÃ¢ÂÂ¦ Realizado","ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Atrasado","ÃÂ¢ÃÂÃÂ Cancelado"], key="ev_status")

        ev_descricao = st.text_area("DescriÃÂÃÂ§ÃÂÃÂ£o / ObservaÃÂÃÂ§ÃÂÃÂµes", key="ev_desc")



        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Salvar Evento", key="btn_salvar_ev"):

            if not ev_tipo:

                error_box("Selecione o tipo de evento.")

            else:

                st.session_state.calendario_eventos.append({

                    "Tipo":        ev_tipo,

                    "Data":        str(ev_data),

                    "TalhÃÂÃÂ£o":      ev_talhao,

                    "Cultura":     ev_cultura,

                    "ResponsÃÂÃÂ¡vel": ev_resp,

                    "Status":      ev_status,

                    "DescriÃÂÃÂ§ÃÂÃÂ£o":   ev_descricao,

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

                mes_sel = st.selectbox("MÃÂÃÂªs", range(1,13, key="sel_m_s_6377"),

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

                warning_box("Nenhum evento neste mÃÂÃÂªs com os filtros selecionados.")

            else:

                st.subheader(f"ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¦ Eventos ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'][mes_sel-1]}/{ano_sel}")



                for _, ev in df_mes.iterrows():

                    cor = {"ÃÂ¢ÃÂÃ¢ÂÂ¦ Realizado":"#14532d","ÃÂ¢ÃÂÃÂ³ Planejado":"#1e3a5f",

                           "ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Atrasado":"#78350f","ÃÂ¢ÃÂÃÂ Cancelado":"#7f1d1d"}.get(ev["Status"],"#1e3a5f")

                    borda = {"ÃÂ¢ÃÂÃ¢ÂÂ¦ Realizado":"#22c55e","ÃÂ¢ÃÂÃÂ³ Planejado":"#3b82f6",

                             "ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Atrasado":"#f59e0b","ÃÂ¢ÃÂÃÂ Cancelado":"#ef4444"}.get(ev["Status"],"#3b82f6")

                    st.markdown(f'''<div style="background:{cor};color:#fff;padding:12px 18px;

                    border-radius:10px;border-left:5px solid {borda};

                    font-weight:600;margin:6px 0;font-size:14px;">

                    {ev["Tipo"]} &nbsp;|&nbsp; <b>{ev["Data"].strftime("%d/%m/%Y")}</b>

                    &nbsp;|&nbsp; {ev["TalhÃÂÃÂ£o"]} &nbsp;|&nbsp; {ev["Cultura"]}

                    &nbsp;|&nbsp; {ev["Status"]}<br>

                    <span style="font-weight:400;font-size:13px;">{ev["DescriÃÂÃÂ§ÃÂÃÂ£o"]}</span>

                    </div>''', unsafe_allow_html=True)



            # PrÃÂÃÂ³ximos eventos

            st.divider()

            st.subheader("ÃÂ¢ÃÂÃÂ° PrÃÂÃÂ³ximos Eventos (7 dias)")

            hoje_ts = pd.Timestamp(date.today())

            df_prox = df_ev[

                (df_ev["Data"] >= hoje_ts) &

                (df_ev["Data"] <= hoje_ts + pd.Timedelta(days=7)) &

                (df_ev["Status"] == "ÃÂ¢ÃÂÃÂ³ Planejado")

            ].sort_values("Data")

            if df_prox.empty:

                info_box("Nenhum evento planejado nos prÃÂÃÂ³ximos 7 dias.")

            else:

                for _, ev in df_prox.iterrows():

                    dias_rest = (ev["Data"].date() - date.today()).days

                    st.markdown(f'''<div style="background:#1e3a5f;color:#fff;padding:10px 16px;

                    border-radius:10px;border-left:5px solid #3b82f6;font-weight:700;margin:4px 0;">

                    {ev["Tipo"]} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {ev["TalhÃÂÃÂ£o"]} em {ev["Data"].strftime("%d/%m/%Y")}

                    {"(hoje)" if dias_rest==0 else f"(em {dias_rest} dia{'s' if dias_rest>1 else ''})"}

                    </div>''', unsafe_allow_html=True)



            # Excluir evento

            st.divider()

            opcoes_ev = [f"{e['Tipo']} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {e['TalhÃÂÃÂ£o']} ({e['Data'].strftime('%d/%m/%Y')})"

                          for _, e in df_mes.iterrows()]

            if opcoes_ev:

                del_ev = st.selectbox("Excluir evento", opcoes_ev, key="del_ev_sel")

                if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Excluir Evento", key="btn_del_ev"):

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

        st.subheader("ÃÂ°ÃÂ¸ÃÂÃÂ± Cronograma de Plantio por Cultura")

        cronograma_completo = {

            "Soja":      {"plantio":["Out","Nov"],"floraÃÂÃÂ§ÃÂÃÂ£o":["Dez","Jan"],"colheita":["Mar","Abr"],"ciclo":"120-140 dias"},

            "Milho":     {"plantio":["Set","Out","Nov"],"floraÃÂÃÂ§ÃÂÃÂ£o":["Dez","Jan"],"colheita":["Fev","Mar","Abr"],"ciclo":"120-150 dias"},

            "Trigo":     {"plantio":["Abr","Mai","Jun"],"floraÃÂÃÂ§ÃÂÃÂ£o":["Jul","Ago"],"colheita":["Set","Out"],"ciclo":"100-130 dias"},

            "FeijÃÂÃÂ£o":    {"plantio":["Jan","Jul","Out"],"floraÃÂÃÂ§ÃÂÃÂ£o":["Fev","Ago","Nov"],"colheita":["Mar","Set","Dez"],"ciclo":"70-90 dias"},

            "Canola":    {"plantio":["Abr","Mai"],"floraÃÂÃÂ§ÃÂÃÂ£o":["Jun","Jul"],"colheita":["Set","Out"],"ciclo":"120-150 dias"},

            "Aveia":     {"plantio":["Abr","Mai","Jun"],"floraÃÂÃÂ§ÃÂÃÂ£o":["Jul","Ago"],"colheita":["Set","Out"],"ciclo":"100-120 dias"},

            "CafÃÂÃÂ©":      {"plantio":["Out","Nov"],"floraÃÂÃÂ§ÃÂÃÂ£o":["Jul","Ago"],"colheita":["Mai","Jun","Jul"],"ciclo":"3-4 anos"},

            "Tomate":    {"plantio":["Ago","Set","Jan"],"floraÃÂÃÂ§ÃÂÃÂ£o":["Out","Fev"],"colheita":["Dez","Abr"],"ciclo":"90-120 dias"},

            "Batata":    {"plantio":["Jul","Ago","Jan"],"floraÃÂÃÂ§ÃÂÃÂ£o":["Set","Mar"],"colheita":["Nov","Mai"],"ciclo":"90-120 dias"},

            "Eucalipto": {"plantio":["Out","Nov"],"floraÃÂÃÂ§ÃÂÃÂ£o":["N/A"],"colheita":["6-7 anos"],"ciclo":"6-7 anos"},

            "Pinus":     {"plantio":["Set","Out"],"floraÃÂÃÂ§ÃÂÃÂ£o":["N/A"],"colheita":["15-20 anos"],"ciclo":"15-20 anos"},

            "Uva":       {"plantio":["Jun","Jul"],"floraÃÂÃÂ§ÃÂÃÂ£o":["Set","Out"],"colheita":["Jan","Fev"],"ciclo":"2-3 anos"},

            "Laranja":   {"plantio":["Set","Out"],"floraÃÂÃÂ§ÃÂÃÂ£o":["Ago","Set"],"colheita":["Jun","Jul","Ago"],"ciclo":"3-4 anos"},

            "Banana":    {"plantio":["Set","Out"],"floraÃÂÃÂ§ÃÂÃÂ£o":["Jan","Fev"],"colheita":["Mar","Abr","Mai"],"ciclo":"12-18 meses"},

        }

        culturas_seg = get_culturas()

        cronograma = {k:v for k,v in cronograma_completo.items() if k in culturas_seg}

        if not cronograma:

            cronograma = cronograma_completo

        cultura_cron = st.selectbox("Selecione a cultura", list(cronograma.keys()), key="cron_cultura")

        cron = cronograma[cultura_cron]

        col1,col2,col3,col4 = st.columns(4)

        col1.metric("ÃÂ°ÃÂ¸ÃÂÃÂ± Plantio",    ", ".join(cron["plantio"]))

        col2.metric("ÃÂ°ÃÂ¸ÃÂÃÂ¸ FloraÃÂÃÂ§ÃÂÃÂ£o",   ", ".join(cron["floraÃÂÃÂ§ÃÂÃÂ£o"]))

        col3.metric("ÃÂ°ÃÂ¸ÃÂÃÂ¾ Colheita",   ", ".join(cron["colheita"]))

        col4.metric("ÃÂ¢ÃÂÃÂ±ÃÂ¯ÃÂ¸ÃÂ Ciclo",      cron["ciclo"])



        meses_abrev = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

        fases_linha = []

        for mes in meses_abrev:

            if mes in cron["plantio"]:   fase = "ÃÂ°ÃÂ¸ÃÂÃÂ± Plantio"

            elif mes in cron["floraÃÂÃÂ§ÃÂÃÂ£o"]: fase = "ÃÂ°ÃÂ¸ÃÂÃÂ¸ FloraÃÂÃÂ§ÃÂÃÂ£o"

            elif mes in cron["colheita"]: fase = "ÃÂ°ÃÂ¸ÃÂÃÂ¾ Colheita"

            else:                         fase = "ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"

            fases_linha.append({"MÃÂÃÂªs": mes, "Fase": fase})

        df_cron = pd.DataFrame(fases_linha)

        st.dataframe(df_cron.T, use_container_width=True)



        st.markdown('''<div style="background:#14532d;color:#fff;padding:13px 18px;

        border-radius:10px;border-left:5px solid #22c55e;font-weight:600;margin:10px 0;">

        ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¡ Use a aba "Novo Evento" para lanÃÂÃÂ§ar as datas reais do seu plantio e acompanhar

        o andamento da safra no calendÃÂÃÂ¡rio.

        </div>''', unsafe_allow_html=True)





# ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

# MENU: RECEITUÃÂÃÂRIO AGRONÃÂÃ¢ÂÂMICO

# ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

if menu == "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ Operacional":

  with _sub_op[4]:

    st.header("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ ReceituÃÂÃÂ¡rio AgronÃÂÃÂ´mico")

    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;

    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">

    ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Gere o ReceituÃÂÃÂ¡rio AgronÃÂÃÂ´mico completo conforme exigido pela Lei 7.802/89 e Decreto 4.074/02.

    ObrigatÃÂÃÂ³rio para compra e uso de defensivos agrÃÂÃÂ­colas. Gera PDF pronto para assinatura.

    </div>''', unsafe_allow_html=True)



    tab_novo_rec, tab_historico_rec = st.tabs(["ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Novo ReceituÃÂÃÂ¡rio", "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ HistÃÂÃÂ³rico"])



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ABA NOVO RECEITUÃÂÃÂRIO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    with tab_novo_rec:

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Dados do ReceituÃÂÃÂ¡rio")



        col_r1, col_r2 = st.columns(2)



        with col_r1:

            st.markdown("**ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¨ÃÂ¢Ã¢ÂÂ¬ÃÂÃÂ°ÃÂ¸ÃÂÃÂ¾ Dados do Produtor**")

            rec_produtor      = st.text_input("Nome do Produtor / RazÃÂÃÂ£o Social", key="rec_prod")

            rec_cpf_cnpj      = st.text_input("CPF / CNPJ", placeholder="000.000.000-00", key="rec_cpf")

            rec_propriedade   = st.text_input("Nome da Propriedade", value=st.session_state.dados.get("fazenda",""), key="rec_prop")

            rec_municipio     = st.text_input("MunicÃÂÃÂ­pio / UF", key="rec_mun")

            rec_area_ha       = st.number_input("ÃÂÃÂrea a tratar (ha)", min_value=0.1,

                                                value=float(st.session_state.dados.get("area", 1.0)), key="rec_area")

            rec_cultura       = st.selectbox("Cultura", get_culturas() + [

                                             "Arroz","Cana-de-AÃÂÃÂ§ÃÂÃÂºcar","CafÃÂÃÂ©","Pastagem","Outro"], key="rec_cult")

            rec_alvo          = st.text_input("Alvo / Problema a combater",

                                              placeholder="Ex: Ferrugem asiÃÂÃÂ¡tica, Lagarta-do-cartucho", key="rec_alvo")



        with col_r2:

            st.markdown("**ÃÂ°ÃÂ¸ÃÂ§Ã¢ÂÂÃÂ¢Ã¢ÂÂ¬ÃÂÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¼ Dados do ResponsÃÂÃÂ¡vel TÃÂÃÂ©cnico**")

            rec_rt_nome       = st.text_input("Nome do Engenheiro AgrÃÂÃÂ´nomo / RT", key="rec_rt_nome")

            rec_rt_crea       = st.text_input("CREA / CRBio nÃÂÃÂº", placeholder="123456-D/SP", key="rec_rt_crea")

            rec_rt_email      = st.text_input("E-mail do RT", key="rec_rt_email")

            rec_rt_telefone   = st.text_input("Telefone do RT", key="rec_rt_tel")

            rec_data_emissao  = st.date_input("Data de EmissÃÂÃÂ£o", value=date.today(), key="rec_data")

            rec_validade_dias = st.number_input("Validade (dias)", min_value=1, max_value=365, value=30, key="rec_val")

            rec_numero        = st.text_input("NÃÂÃÂºmero do ReceituÃÂÃÂ¡rio", placeholder="001/2026", key="rec_num")



        st.divider()

        st.subheader("ÃÂ°ÃÂ¸ÃÂ§ÃÂª Produtos Recomendados")



        qtd_prods_rec = st.number_input("Quantidade de produtos", min_value=1, max_value=8, value=1, key="rec_qtd_prods")

        produtos_rec  = []



        for i in range(int(qtd_prods_rec)):

            st.markdown(f"**Produto {i+1}**")

            cr1, cr2, cr3, cr4, cr5 = st.columns([3, 2, 1, 1, 2])

            with cr1:

                # Busca no catÃÂÃÂ¡logo ou digitaÃÂÃÂ§ÃÂÃÂ£o livre

                opcoes_estoque = [p["Insumo"] for p in st.session_state.estoque] if st.session_state.estoque else []

                if opcoes_estoque:

                    nome_prod_rec = st.selectbox(f"Produto {i+1}", opcoes_estoque, key=f"rec_prod_{i}")

                    # Buscar IA do catÃÂÃÂ¡logo se disponÃÂÃÂ­vel

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

                            f'ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¦ Total para {rec_area_ha:.1f} ha: <b>{total_produto:.2f} {unid_rec.replace("/ha","").replace("/100L","")}</b>'

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

        st.subheader("ÃÂ¢ÃÂ¡Ã¢ÂÂ¢ÃÂ¯ÃÂ¸ÃÂ RecomendaÃÂÃÂ§ÃÂÃÂµes de AplicaÃÂÃÂ§ÃÂÃÂ£o")

        col_ap1, col_ap2, col_ap3 = st.columns(3)

        with col_ap1:

            rec_volume_calda  = st.number_input("Volume de calda (L/ha)", min_value=0.0, value=100.0, key="rec_vol")

            rec_equipamento   = st.selectbox("Equipamento", ["Pulverizador tratorizado","Pulverizador costal",

                                             "AviÃÂÃÂ£o agrÃÂÃÂ­cola","Drone","PivÃÂÃÂ´ central","Outro"], key="rec_equip")

        with col_ap2:

            rec_epoca         = st.text_input("ÃÂÃ¢ÂÂ°poca de aplicaÃÂÃÂ§ÃÂÃÂ£o", placeholder="Ex: EstÃÂÃÂ¡dio R1 da soja", key="rec_epoca")

            rec_intervalo     = st.number_input("Intervalo entre aplicaÃÂÃÂ§ÃÂÃÂµes (dias)", min_value=0, value=14, key="rec_intv")

        with col_ap3:

            rec_epi           = st.multiselect("EPI obrigatÃÂÃÂ³rio", ["MacacÃÂÃÂ£o","Luvas nitrÃÂÃÂ­licas","Botas de borracha",

                                               "MÃÂÃÂ¡scara com filtro","ÃÂÃ¢ÂÂculos de proteÃÂÃÂ§ÃÂÃÂ£o","Avental impermeÃÂÃÂ¡vel",

                                               "ChapÃÂÃÂ©u de abas largas"], key="rec_epi")

            rec_carencia      = st.number_input("Prazo de carÃÂÃÂªncia (dias)", min_value=0, value=14, key="rec_car")



        rec_observacoes = st.text_area("ObservaÃÂÃÂ§ÃÂÃÂµes / RecomendaÃÂÃÂ§ÃÂÃÂµes adicionais", key="rec_obs",

                                       placeholder="Ex: NÃÂÃÂ£o aplicar com ventos acima de 10 km/h...")



        col_btn1, col_btn2 = st.columns(2)



        with col_btn1:

            if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Salvar ReceituÃÂÃÂ¡rio", key="btn_salvar_rec", use_container_width=True):

                if not rec_produtor.strip():

                    error_box("Informe o nome do produtor.")

                elif not rec_rt_nome.strip():

                    error_box("Informe o nome do ResponsÃÂÃÂ¡vel TÃÂÃÂ©cnico.")

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

                    success_box(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ ReceituÃÂÃÂ¡rio {novo_rec['numero']} salvo com sucesso!")



        with col_btn2:

            # Gerar PDF do ÃÂÃÂºltimo receituÃÂÃÂ¡rio preenchido

            if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¨ÃÂ¯ÃÂ¸ÃÂ Gerar PDF", key="btn_pdf_rec", use_container_width=True):

                if not rec_produtor.strip() or not rec_rt_nome.strip():

                    error_box("Preencha ao menos produtor e ResponsÃÂÃÂ¡vel TÃÂÃÂ©cnico antes de gerar o PDF.")

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



                        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CabeÃÂÃÂ§alho

                        titulo_sty = ParagraphStyle("titulo", parent=sty_r["Title"],

                                                    fontSize=16, textColor=colors.HexColor("#0f3460"),

                                                    alignment=TA_CENTER)

                        sub_sty    = ParagraphStyle("sub", parent=sty_r["Normal"],

                                                    fontSize=10, textColor=colors.HexColor("#1e3a5f"),

                                                    alignment=TA_CENTER)



                        if os.path.exists("IAAgrologo.jpeg"):

                            el_r.append(Image("IAAgrologo.jpeg", width=2.5*cm, height=1.2*cm))

                        el_r.append(Spacer(1, 6))

                        el_r.append(Paragraph("RECEITUÃÂÃÂRIO AGRONÃÂÃ¢ÂÂMICO", titulo_sty))

                        el_r.append(Paragraph(f"Lei 7.802/89 | Decreto 4.074/02", sub_sty))

                        el_r.append(Paragraph(f"NÃÂÃÂº {rec_numero or '---'} | EmissÃÂÃÂ£o: {rec_data_emissao.strftime('%d/%m/%Y')} | "

                                              f"Validade: {rec_validade_dias} dias", sub_sty))

                        el_r.append(Spacer(1, 10))



                        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Linha horizontal

                        from reportlab.platypus import HRFlowable

                        el_r.append(HRFlowable(width="100%", thickness=2,

                                               color=colors.HexColor("#0f3460")))

                        el_r.append(Spacer(1, 8))



                        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Dados do Produtor

                        el_r.append(Paragraph("<b>DADOS DO PRODUTOR</b>", sty_r["Heading2"]))

                        dados_prod = [

                            ["Produtor / RazÃÂÃÂ£o Social:", rec_produtor,     "CPF / CNPJ:", rec_cpf_cnpj],

                            ["Propriedade:",             rec_propriedade,  "MunicÃÂÃÂ­pio/UF:", rec_municipio],

                            ["Cultura:",                 rec_cultura,      "ÃÂÃÂrea (ha):",  f"{rec_area_ha:.2f} ha"],

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



                        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Produtos recomendados

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



                        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ RecomendaÃÂÃÂ§ÃÂÃÂµes de aplicaÃÂÃÂ§ÃÂÃÂ£o

                        el_r.append(Paragraph("<b>RECOMENDAÃÂÃ¢ÂÂ¡ÃÂÃ¢ÂÂ¢ES DE APLICAÃÂÃ¢ÂÂ¡ÃÂÃÂO</b>", sty_r["Heading2"]))

                        dados_aplic = [

                            ["Volume de calda:", f"{rec_volume_calda:.0f} L/ha", "Equipamento:", rec_equipamento],

                            ["ÃÂÃ¢ÂÂ°poca de aplicaÃÂÃÂ§ÃÂÃÂ£o:", rec_epoca, "Intervalo:", f"{rec_intervalo} dias"],

                            ["Prazo de carÃÂÃÂªncia:", f"{rec_carencia} dias", "EPI:", ", ".join(rec_epi) if rec_epi else "Conforme bula"],

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

                            el_r.append(Paragraph("<b>OBSERVAÃÂÃ¢ÂÂ¡ÃÂÃ¢ÂÂ¢ES:</b>", sty_r["Heading3"]))

                            el_r.append(Paragraph(rec_observacoes, sty_r["BodyText"]))



                        el_r.append(Spacer(1, 16))

                        el_r.append(HRFlowable(width="100%", thickness=1, color=colors.grey))

                        el_r.append(Spacer(1, 10))



                        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Assinaturas

                        el_r.append(Paragraph("<b>RESPONSÃÂÃÂVEL TÃÂÃ¢ÂÂ°CNICO</b>", sty_r["Heading2"]))

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

                                    [f"Assinatura do RT ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {rec_rt_crea}", "   ",

                                     f"Assinatura do Produtor ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {rec_cpf_cnpj}"]]

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

                            f'Este receituÃÂÃÂ¡rio ÃÂÃÂ© vÃÂÃÂ¡lido por {rec_validade_dias} dias a partir da emissÃÂÃÂ£o.</font>',

                            sty_r["Normal"]

                        ))



                        doc_r.build(el_r)

                        pdf_rec = buf_r.getvalue()

                        buf_r.close()



                        num_arquivo = (rec_numero or "receituario").replace("/","_").replace(" ","_")

                        st.download_button(

                            "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Baixar ReceituÃÂÃÂ¡rio PDF",

                            data=pdf_rec,

                            file_name=f"Receituario_{num_arquivo}_{rec_produtor[:15].replace(' ','_')}.pdf",

                            mime="application/pdf",

                            use_container_width=True

                        )

                    except Exception as e:

                        error_box(f"Erro ao gerar PDF: {e}")



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ABA HISTÃÂÃ¢ÂÂRICO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    with tab_historico_rec:

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ ReceituÃÂÃÂ¡rios Emitidos")

        if not st.session_state.receituarios:

            info_box("Nenhum receituÃÂÃÂ¡rio salvo ainda.")

        else:

            # Tabela resumo

            resumo = []

            for r in st.session_state.receituarios:

                resumo.append({

                    "NÃÂÃÂº":         r.get("numero",""),

                    "Data":       r.get("data_emissao",""),

                    "Produtor":   r.get("produtor",""),

                    "Cultura":    r.get("cultura",""),

                    "ÃÂÃÂrea (ha)":  r.get("area_ha",0),

                    "Alvo":       r.get("alvo",""),

                    "RT":         r.get("rt_nome",""),

                    "Validade":   r.get("validade_ate","")[:10] if r.get("validade_ate") else "",

                })

            df_rec_hist = pd.DataFrame(resumo)

            st.dataframe(df_rec_hist, use_container_width=True, hide_index=True)



            # Ver detalhes / regerar PDF

            st.divider()

            opcoes_rec = [f"{r.get('numero',i)} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {r.get('produtor','')} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {r.get('data_emissao','')}"

                          for i, r in enumerate(st.session_state.receituarios)]

            sel_rec = st.selectbox("Selecionar receituÃÂÃÂ¡rio", opcoes_rec, key="sel_rec_hist")

            idx_sel = opcoes_rec.index(sel_rec)

            rec_sel = st.session_state.receituarios[idx_sel]



            with st.expander("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂÃÂ¯ÃÂ¸ÃÂ Ver detalhes completos", expanded=False):

                col_det1, col_det2 = st.columns(2)

                with col_det1:

                    st.markdown(f"**Produtor:** {rec_sel.get('produtor','')}")

                    st.markdown(f"**CPF/CNPJ:** {rec_sel.get('cpf_cnpj','')}")

                    st.markdown(f"**Propriedade:** {rec_sel.get('propriedade','')}")

                    st.markdown(f"**MunicÃÂÃÂ­pio:** {rec_sel.get('municipio','')}")

                    st.markdown(f"**Cultura:** {rec_sel.get('cultura','')} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {rec_sel.get('area_ha',0)} ha")

                    st.markdown(f"**Alvo:** {rec_sel.get('alvo','')}")

                with col_det2:

                    st.markdown(f"**RT:** {rec_sel.get('rt_nome','')}")

                    st.markdown(f"**CREA:** {rec_sel.get('rt_crea','')}")

                    st.markdown(f"**EmissÃÂÃÂ£o:** {rec_sel.get('data_emissao','')}")

                    st.markdown(f"**VÃÂÃÂ¡lido atÃÂÃÂ©:** {rec_sel.get('validade_ate','')[:10]}")

                    st.markdown(f"**Equipamento:** {rec_sel.get('equipamento','')}")

                    st.markdown(f"**Volume calda:** {rec_sel.get('volume_calda',0)} L/ha")



                if rec_sel.get("produtos"):

                    st.markdown("**Produtos:**")

                    st.dataframe(pd.DataFrame(rec_sel["produtos"]), use_container_width=True, hide_index=True)



            # Excluir

            if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Excluir este receituÃÂÃÂ¡rio", key="btn_del_rec"):

                st.session_state.receituarios.pop(idx_sel)

                salvar_dados_iaagro()

                success_box("ReceituÃÂÃÂ¡rio excluÃÂÃÂ­do.")

                st.rerun()



            # Exportar todos em Excel

            if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Exportar todos para Excel", key="btn_xlsx_rec", use_container_width=True):

                rows_exp = []

                for r in st.session_state.receituarios:

                    base = {k: v for k, v in r.items() if k != "produtos"}

                    for j, p in enumerate(r.get("produtos", [])):

                        row = base.copy()

                        row.update({f"prod_{j+1}_{k}": v for k, v in p.items()})

                        rows_exp.append(row)

                    if not r.get("produtos"):

                        rows_exp.append(base)

                xlsx_r = exportar_excel({"ReceituÃÂÃÂ¡rios": rows_exp})

                if xlsx_r:

                    st.download_button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Baixar Excel", data=xlsx_r,

                        file_name=f"receituarios_{date.today()}.xlsx",

                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                        use_container_width=True)





# ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

# MENU: COMPARATIVO DE SAFRAS

# ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

if menu == "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Financeiro":

  with _sub_fin[2]:

    st.header("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Comparativo de Safras")

    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;

    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">

    ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Compare produtividade, custos e lucratividade entre todas as safras cadastradas.

    Identifique tendÃÂÃÂªncias e tome decisÃÂÃÂµes com base no histÃÂÃÂ³rico real da sua propriedade.

    </div>''', unsafe_allow_html=True)



    # Verificar dados disponÃÂÃÂ­veis

    tem_hist = len(st.session_state.historico_produtividade) > 0

    tem_dre  = len(st.session_state.get("dre_registros", [])) > 0



    if not tem_hist and not tem_dre:

        warning_box("Cadastre dados em 'HistÃÂÃÂ³rico de Produtividade' e/ou 'Dashboard Financeiro' para ver o comparativo.")

    else:

        try:

            import plotly.express as px

            import plotly.graph_objects as go

            from plotly.subplots import make_subplots

            PLOTLY_OK = True

        except Exception:

            PLOTLY_OK = False



        tab_prod, tab_fin, tab_completo, tab_ia = st.tabs([

            "ÃÂ°ÃÂ¸ÃÂÃÂ¾ Produtividade",

            "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Financeiro",

            "ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Comparativo Completo",

            "ÃÂ°ÃÂ¸ÃÂ¤Ã¢ÂÂ AnÃÂÃÂ¡lise IA"

        ])



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TAB 1: PRODUTIVIDADE ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        with tab_prod:

            st.subheader("ÃÂ°ÃÂ¸ÃÂÃÂ¾ EvoluÃÂÃÂ§ÃÂÃÂ£o da Produtividade por Safra")

            if not tem_hist:

                info_box("Cadastre dados em 'HistÃÂÃÂ³rico de Produtividade' para ver esta aba.")

            else:

                df_h = pd.DataFrame(st.session_state.historico_produtividade)



                # Filtros

                col_f1, col_f2 = st.columns(2)

                with col_f1:

                    areas_disp = ["Todas"] + sorted(df_h["ÃÂÃÂrea"].unique().tolist())

                    area_filtro_comp = st.selectbox("Filtrar por ÃÂÃÂ¡rea", areas_disp, key="comp_area_filtro")

                with col_f2:

                    culturas_disp = ["Todas"] + sorted(df_h["ÃÂÃÂrea"].unique().tolist())

                    min_safras = st.number_input("MÃÂÃÂ­nimo de safras para exibir", min_value=1, value=1, key="comp_min_safras")



                df_hf = df_h if area_filtro_comp == "Todas" else df_h[df_h["ÃÂÃÂrea"] == area_filtro_comp]



                if df_hf.empty:

                    info_box("Nenhum dado para o filtro selecionado.")

                else:

                    # MÃÂÃÂ©tricas gerais

                    media_geral  = df_hf["Produtividade"].mean()

                    melhor_safra = df_hf.loc[df_hf["Produtividade"].idxmax()]

                    pior_safra   = df_hf.loc[df_hf["Produtividade"].idxmin()]

                    tendencia    = df_hf.groupby("Safra")["Produtividade"].mean()

                    delta_trend  = tendencia.iloc[-1] - tendencia.iloc[0] if len(tendencia) > 1 else 0



                    c1, c2, c3, c4 = st.columns(4)

                    c1.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  MÃÂÃÂ©dia Geral", f"{media_geral:.1f} sc/ha")

                    c2.metric("ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ  Melhor Safra", f"{melhor_safra['Produtividade']:.1f} sc/ha",

                              f"{melhor_safra['Safra']}")

                    c3.metric("ÃÂ¢ÃÂ¬Ã¢ÂÂ¡ÃÂ¯ÃÂ¸ÃÂ Pior Safra", f"{pior_safra['Produtividade']:.1f} sc/ha",

                              f"{pior_safra['Safra']}")

                    c4.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ TendÃÂÃÂªncia", f"{delta_trend:+.1f} sc/ha",

                              "vs 1ÃÂÃÂª safra" if len(tendencia) > 1 else "ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ")



                    if PLOTLY_OK:

                        # GrÃÂÃÂ¡fico de barras por safra + linha de mÃÂÃÂ©dia

                        df_safra_media = df_hf.groupby("Safra")["Produtividade"].mean().reset_index()

                        df_safra_media.columns = ["Safra","MÃÂÃÂ©dia sc/ha"]



                        fig_bar = go.Figure()

                        fig_bar.add_trace(go.Bar(

                            x=df_safra_media["Safra"],

                            y=df_safra_media["MÃÂÃÂ©dia sc/ha"],

                            marker_color=[

                                "#22c55e" if v >= media_geral else "#f59e0b"

                                for v in df_safra_media["MÃÂÃÂ©dia sc/ha"]

                            ],

                            text=[f"{v:.1f}" for v in df_safra_media["MÃÂÃÂ©dia sc/ha"]],

                            textposition="outside",

                            name="Produtividade"

                        ))

                        fig_bar.add_hline(y=media_geral, line_dash="dash",

                                          line_color="#6ee7b7",

                                          annotation_text=f"MÃÂÃÂ©dia: {media_geral:.1f}",

                                          annotation_font_color="#6ee7b7")

                        fig_bar.update_layout(

                            title="Produtividade MÃÂÃÂ©dia por Safra (sc/ha)",

                            paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",

                            font_color="#f1f5f9", height=380,

                            xaxis_title="Safra", yaxis_title="sc/ha",

                            yaxis=dict(gridcolor="#1e3a5f"),

                            showlegend=False

                        )

                        st.plotly_chart(fig_bar, use_container_width=True)



                        # EvoluÃÂÃÂ§ÃÂÃÂ£o por ÃÂÃÂ¡rea (se mÃÂÃÂºltiplas)

                        if df_hf["ÃÂÃÂrea"].nunique() > 1:

                            fig_line = px.line(

                                df_hf.groupby(["Safra","ÃÂÃÂrea"])["Produtividade"].mean().reset_index(),

                                x="Safra", y="Produtividade", color="ÃÂÃÂrea",

                                title="EvoluÃÂÃÂ§ÃÂÃÂ£o por ÃÂÃÂrea/TalhÃÂÃÂ£o",

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

                                title="DistribuiÃÂÃÂ§ÃÂÃÂ£o de Produtividade por Safra",

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

                    st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Dados por Safra")

                    df_tab_comp = df_hf.groupby("Safra").agg(

                        MÃÂÃÂ©dia=("Produtividade","mean"),

                        MÃÂÃÂ­nimo=("Produtividade","min"),

                        MÃÂÃÂ¡ximo=("Produtividade","max"),

                        Registros=("Produtividade","count")

                    ).round(1).reset_index()

                    df_tab_comp["vs MÃÂÃÂ©dia"] = (df_tab_comp["MÃÂÃÂ©dia"] - media_geral).round(1)

                    st.dataframe(df_tab_comp, use_container_width=True, hide_index=True)



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TAB 2: FINANCEIRO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        with tab_fin:

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Comparativo Financeiro entre Safras")

            if not tem_dre:

                info_box("Cadastre lanÃÂÃÂ§amentos em 'Dashboard Financeiro' para ver esta aba.")

            else:

                df_dre_all = pd.DataFrame(st.session_state.dre_registros)



                df_fin_comp = df_dre_all.groupby(["Safra","Tipo"])["Valor R$"].sum().unstack(fill_value=0).reset_index()



                # Garantir colunas mesmo que faltem

                for col in ["Receita","Custo VariÃÂÃÂ¡vel","Custo Fixo"]:

                    if col not in df_fin_comp.columns:

                        df_fin_comp[col] = 0



                df_fin_comp["Custo Total"] = df_fin_comp.get("Custo VariÃÂÃÂ¡vel",0) + df_fin_comp.get("Custo Fixo",0)

                df_fin_comp["Lucro"]       = df_fin_comp["Receita"] - df_fin_comp["Custo Total"]

                df_fin_comp["Margem %"]    = (df_fin_comp["Lucro"] / df_fin_comp["Receita"] * 100).round(1).where(df_fin_comp["Receita"]>0, 0)



                # ÃÂÃÂrea por safra (para mÃÂÃÂ©tricas /ha)

                df_area_safra = df_dre_all.groupby("Safra")["ÃÂÃÂrea ha"].max().reset_index()

                df_fin_comp   = df_fin_comp.merge(df_area_safra, on="Safra", how="left")

                df_fin_comp["ÃÂÃÂrea ha"] = df_fin_comp["ÃÂÃÂrea ha"].fillna(1)

                df_fin_comp["Receita/ha"]   = (df_fin_comp["Receita"] / df_fin_comp["ÃÂÃÂrea ha"]).round(0)

                df_fin_comp["Custo/ha"]     = (df_fin_comp["Custo Total"] / df_fin_comp["ÃÂÃÂrea ha"]).round(0)

                df_fin_comp["Lucro/ha"]     = (df_fin_comp["Lucro"] / df_fin_comp["ÃÂÃÂrea ha"]).round(0)



                # MÃÂÃÂ©tricas de destaque

                melhor_lucro = df_fin_comp.loc[df_fin_comp["Lucro"].idxmax()] if not df_fin_comp.empty else None

                media_margem = df_fin_comp["Margem %"].mean()



                if melhor_lucro is not None:

                    cm1, cm2, cm3, cm4 = st.columns(4)

                    cm1.metric("ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ  Melhor Lucro", f"R$ {melhor_lucro['Lucro']:,.0f}", melhor_lucro["Safra"])

                    cm2.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Margem MÃÂÃÂ©dia", f"{media_margem:.1f}%")

                    cm3.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Maior Receita", f"R$ {df_fin_comp['Receita'].max():,.0f}")

                    cm4.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¸ Menor Custo/ha", f"R$ {df_fin_comp['Custo/ha'].min():,.0f}/ha")



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



                    # EvoluÃÂÃÂ§ÃÂÃÂ£o da margem

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

                            title="EvoluÃÂÃÂ§ÃÂÃÂ£o da Margem LÃÂÃÂ­quida (%)",

                            paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",

                            font_color="#f1f5f9", height=300,

                            yaxis=dict(gridcolor="#1e3a5f"),

                            xaxis_title="Safra", yaxis_title="Margem %"

                        )

                        st.plotly_chart(fig_margem, use_container_width=True)



                # Tabela financeira completa

                st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Resumo Financeiro por Safra")

                cols_exib = ["Safra","Receita","Custo Total","Lucro","Margem %","Receita/ha","Custo/ha","Lucro/ha","ÃÂÃÂrea ha"]

                st.dataframe(df_fin_comp[[c for c in cols_exib if c in df_fin_comp.columns]].round(1),

                             use_container_width=True, hide_index=True)



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TAB 3: COMPARATIVO COMPLETO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        with tab_completo:

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Painel Completo ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Produtividade + Financeiro")



            if not tem_hist and not tem_dre:

                info_box("Sem dados suficientes.")

            else:

                # Unir produtividade e financeiro por safra

                dados_comp = {}



                if tem_hist:

                    df_hc = pd.DataFrame(st.session_state.historico_produtividade)

                    for safra, grp in df_hc.groupby("Safra"):

                        dados_comp.setdefault(safra, {})["Prod. MÃÂÃÂ©dia sc/ha"] = round(grp["Produtividade"].mean(), 1)

                        dados_comp[safra]["Custo HistÃÂÃÂ³rico/ha"] = round(grp["Custo"].mean(), 2)



                if tem_dre:

                    df_dc = pd.DataFrame(st.session_state.dre_registros)

                    for safra, grp in df_dc.groupby("Safra"):

                        rec   = grp[grp["Tipo"]=="Receita"]["Valor R$"].sum()

                        custo = grp[grp["Tipo"].isin(["Custo VariÃÂÃÂ¡vel","Custo Fixo"])]["Valor R$"].sum()

                        lucro = rec - custo

                        area  = grp["ÃÂÃÂrea ha"].max() if not grp.empty else 1

                        dados_comp.setdefault(safra, {})["Receita R$"]  = round(rec, 0)

                        dados_comp[safra]["Custo Total R$"] = round(custo, 0)

                        dados_comp[safra]["Lucro R$"]       = round(lucro, 0)

                        dados_comp[safra]["Margem %"]       = round(lucro/rec*100, 1) if rec > 0 else 0

                        dados_comp[safra]["ÃÂÃÂrea ha"]        = area



                df_comp_final = pd.DataFrame(dados_comp).T.reset_index().rename(columns={"index":"Safra"})

                df_comp_final = df_comp_final.sort_values("Safra")



                # Highlight melhor linha

                st.dataframe(df_comp_final, use_container_width=True, hide_index=True)



                if PLOTLY_OK and "Prod. MÃÂÃÂ©dia sc/ha" in df_comp_final.columns and "Lucro R$" in df_comp_final.columns:

                    df_plot_dual = df_comp_final.dropna(subset=["Prod. MÃÂÃÂ©dia sc/ha","Lucro R$"])

                    if not df_plot_dual.empty:

                        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

                        fig_dual.add_trace(go.Bar(

                            name="Produtividade sc/ha", x=df_plot_dual["Safra"],

                            y=df_plot_dual["Prod. MÃÂÃÂ©dia sc/ha"], marker_color="#22c55e",

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

                    st.download_button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Exportar Comparativo Excel", data=xlsx_comp,

                        file_name=f"comparativo_safras_{date.today()}.xlsx",

                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                        use_container_width=True)



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TAB 4: ANÃÂÃÂLISE IA ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        with tab_ia:

            st.subheader("ÃÂ°ÃÂ¸ÃÂ¤Ã¢ÂÂ AnÃÂÃÂ¡lise Comparativa por InteligÃÂÃÂªncia Artificial")



            if st.button("ÃÂ°ÃÂ¸ÃÂ¡Ã¢ÂÂ¬ Gerar AnÃÂÃÂ¡lise IA das Safras", key="btn_ia_comp", use_container_width=True):

                with st.spinner("ÃÂ°ÃÂ¸ÃÂ¤Ã¢ÂÂ Analisando histÃÂÃÂ³rico de safras..."):

                    # Montar resumo para o prompt

                    resumo_hist = ""

                    if tem_hist:

                        df_hr = pd.DataFrame(st.session_state.historico_produtividade)

                        for safra, grp in df_hr.groupby("Safra"):

                            resumo_hist += (f"Safra {safra}: prod. mÃÂÃÂ©dia {grp['Produtividade'].mean():.1f} sc/ha, "

                                           f"custo {grp['Custo'].mean():.2f} R$/ha\n")



                    resumo_fin = ""

                    if tem_dre:

                        df_dr = pd.DataFrame(st.session_state.dre_registros)

                        for safra, grp in df_dr.groupby("Safra"):

                            rec   = grp[grp["Tipo"]=="Receita"]["Valor R$"].sum()

                            custo = grp[grp["Tipo"].isin(["Custo VariÃÂÃÂ¡vel","Custo Fixo"])]["Valor R$"].sum()

                            lucro = rec - custo

                            margem = lucro/rec*100 if rec > 0 else 0

                            resumo_fin += (f"Safra {safra}: receita R$ {rec:,.0f}, custo R$ {custo:,.0f}, "

                                          f"lucro R$ {lucro:,.0f}, margem {margem:.1f}%\n")



                    prompt_comp = f"""VocÃÂÃÂª ÃÂÃÂ© um consultor agrÃÂÃÂ­cola analisando o histÃÂÃÂ³rico de safras de uma propriedade rural brasileira no sistema IAAgro Pro.



HISTÃÂÃ¢ÂÂRICO DE PRODUTIVIDADE:

{resumo_hist if resumo_hist else "Sem dados de produtividade."}



HISTÃÂÃ¢ÂÂRICO FINANCEIRO:

{resumo_fin if resumo_fin else "Sem dados financeiros."}



Gere uma anÃÂÃÂ¡lise comparativa profissional com:

1. TENDÃÂÃÂ NCIA PRODUTIVA ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ a propriedade estÃÂÃÂ¡ evoluindo ou regredindo? Por quÃÂÃÂª?

2. EFICIÃÂÃÂ NCIA FINANCEIRA ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ qual safra teve melhor relaÃÂÃÂ§ÃÂÃÂ£o custo-benefÃÂÃÂ­cio?

3. PONTOS DE ATENÃÂÃ¢ÂÂ¡ÃÂÃÂO ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ o que chama atenÃÂÃÂ§ÃÂÃÂ£o negativamente?

4. DESTAQUES POSITIVOS ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ o que estÃÂÃÂ¡ indo bem?

5. RECOMENDAÃÂÃ¢ÂÂ¡ÃÂÃ¢ÂÂ¢ES ESTRATÃÂÃ¢ÂÂ°GICAS ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ top 3 aÃÂÃÂ§ÃÂÃÂµes para melhorar resultados nas prÃÂÃÂ³ximas safras

6. PROJEÃÂÃ¢ÂÂ¡ÃÂÃÂO ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ se mantida a tendÃÂÃÂªncia, qual a expectativa para a prÃÂÃÂ³xima safra?



Seja objetivo, tÃÂÃÂ©cnico e prÃÂÃÂ¡tico para o produtor rural brasileiro. MÃÂÃÂ¡ximo 400 palavras."""



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



                            # PDF da anÃÂÃÂ¡lise

                            if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¨ÃÂ¯ÃÂ¸ÃÂ Gerar PDF da AnÃÂÃÂ¡lise", key="btn_pdf_comp"):

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

                                    el_cp.append(Paragraph("<b>ANÃÂÃÂLISE COMPARATIVA DE SAFRAS ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ IAAgro IA</b>", sty_cp["Title"]))

                                    el_cp.append(Paragraph(f"Gerado em: {date.today().strftime('%d/%m/%Y')}", sty_cp["Normal"]))

                                    el_cp.append(Spacer(1,12))

                                    el_cp.append(Paragraph("<b>HISTÃÂÃ¢ÂÂRICO DE PRODUTIVIDADE</b>", sty_cp["Heading2"]))

                                    for linha in resumo_hist.split("\n"):

                                        if linha.strip():

                                            el_cp.append(Paragraph(linha, sty_cp["BodyText"]))

                                    el_cp.append(Spacer(1,8))

                                    el_cp.append(Paragraph("<b>HISTÃÂÃ¢ÂÂRICO FINANCEIRO</b>", sty_cp["Heading2"]))

                                    for linha in resumo_fin.split("\n"):

                                        if linha.strip():

                                            el_cp.append(Paragraph(linha, sty_cp["BodyText"]))

                                    el_cp.append(Spacer(1,12))

                                    el_cp.append(Paragraph("<b>ANÃÂÃÂLISE IA</b>", sty_cp["Heading2"]))

                                    el_cp.append(Spacer(1,6))

                                    for linha in analise_comp.split("\n"):

                                        if linha.strip():

                                            el_cp.append(Paragraph(linha, sty_cp["BodyText"]))

                                            el_cp.append(Spacer(1,3))

                                    doc_cp.build(el_cp)

                                    pdf_cp = buf_cp.getvalue()

                                    buf_cp.close()

                                    st.download_button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Baixar PDF", data=pdf_cp,

                                        file_name=f"analise_safras_{date.today()}.pdf",

                                        mime="application/pdf", use_container_width=True)

                                except Exception as ep:

                                    error_box(f"Erro PDF: {ep}")

                        else:

                            warning_box("IA indisponÃÂÃÂ­vel. Verifique a conexÃÂÃÂ£o.")

                    except Exception as e:

                        error_box(f"Erro na anÃÂÃÂ¡lise IA: {e}")





# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: MAPA DE COLHEITA IA

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸ÃÂÃÂ InteligÃÂÃÂªncia":

  with _sub_int[2]:

    st.header("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂºÃÂ¯ÃÂ¸ÃÂ Mapa de Colheita ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ AnÃÂÃÂ¡lise por InteligÃÂÃÂªncia Artificial")

    st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;

    border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">

    ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¡ Carregue o mapa de colheita gerado pela colheitadeira (John Deere, Case, New Holland, Claas, etc.)

    nos formatos CSV, Excel, GeoJSON ou Shapefile. A IA analisa produtividade por zona,

    variabilidade espacial, pontos crÃÂÃÂ­ticos e gera recomendaÃÂÃÂ§ÃÂÃÂµes de manejo.

    </div>''', unsafe_allow_html=True)



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ DependÃÂÃÂªncias opcionais ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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

        ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Para anÃÂÃÂ¡lise completa instale: pip install numpy plotly geopandas</div>''',

        unsafe_allow_html=True)



    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ FUNÃÂÃ¢ÂÂ¡ÃÂÃ¢ÂÂ¢ES AUXILIARES ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

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

        df["Zona"] = df[col_prod].apply(lambda v: "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa" if v < p33 else ("ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dia" if v < p66 else "ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta"))

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

            for z in ["ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dia","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta"]:

                sub = df[df["Zona"]==z]

                s[f"pct_{z}"] = round(len(sub)/len(df)*100, 1)

                s[f"med_{z}"] = round(sub[col_prod].mean(), 1) if len(sub) > 0 else 0

        return s



    def gerar_recomendacoes(stats, col_prod, cultura, area_ha):

        cv        = stats.get("cv", 0)

        media     = stats.get("media", 0)

        pct_baixa = stats.get("pct_ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa", 0)

        pct_alta  = stats.get("pct_ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta",  0)

        med_baixa = stats.get("med_ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa", 0)

        med_alta  = stats.get("med_ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta",  0)

        gap       = med_alta - med_baixa

        recs = []



        if cv > 35:

            recs.append({"zona":"Campo todo","tipo":"ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ ALTA VARIABILIDADE","cor":"#7f1d1d","borda":"#ef4444",

                "texto":f"CV de {cv:.1f}% indica alta heterogeneidade espacial. Implante AplicaÃÂÃÂ§ÃÂÃÂ£o em Taxa "

                        f"VariÃÂÃÂ¡vel (VRA). Realize amostragem por zona de manejo e verifique histÃÂÃÂ³rico de compactaÃÂÃÂ§ÃÂÃÂ£o."})

        elif cv > 20:

            recs.append({"zona":"Campo todo","tipo":"ÃÂ¢Ã¢ÂÂÃÂ¹ÃÂ¯ÃÂ¸ÃÂ VARIABILIDADE MODERADA","cor":"#1e3a5f","borda":"#3b82f6",

                "texto":f"CV de {cv:.1f}% ÃÂÃÂ© moderado. Avalie mapeamento de solo para identificar causas da variabilidade."})

        else:

            recs.append({"zona":"Campo todo","tipo":"ÃÂ¢ÃÂÃ¢ÂÂ¦ BOA UNIFORMIDADE","cor":"#14532d","borda":"#22c55e",

                "texto":f"CV de {cv:.1f}% indica boa uniformidade. Continue o manejo atual."})



        if pct_baixa > 15:

            recs.append({"zona":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Zona Baixa","tipo":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ INTERVENÃÂÃ¢ÂÂ¡ÃÂÃÂO PRIORITÃÂÃÂRIA","cor":"#7f1d1d","borda":"#ef4444",

                "texto":f"{pct_baixa:.0f}% da ÃÂÃÂ¡rea com produtividade baixa (mÃÂÃÂ©dia {med_baixa:.1f}). AÃÂÃÂ§ÃÂÃÂµes: "

                        f"(1) Coleta de solo detalhada por zona; "

                        f"(2) Investigar compactaÃÂÃÂ§ÃÂÃÂ£o com penetrÃÂÃÂ´metro; "

                        f"(3) Verificar drenagem e histÃÂÃÂ³rico de doenÃÂÃÂ§as; "

                        f"(4) Aumentar dose de P e K em ÃÂ¢Ã¢ÂÂ°ÃÂ30%; "

                        f"(5) Considerar calagem diferenciada se pH < 5.8."})



        if pct_alta > 20 and med_alta > 0:

            recs.append({"zona":"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Zona Alta","tipo":"ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ POTENCIAL A EXPLORAR","cor":"#14532d","borda":"#22c55e",

                "texto":f"Zona de alta produtividade ({pct_alta:.0f}% da ÃÂÃÂ¡rea, mÃÂÃÂ©dia {med_alta:.1f}). "

                        f"Mantenha adubaÃÂÃÂ§ÃÂÃÂ£o de reposiÃÂÃÂ§ÃÂÃÂ£o precisa. Priorize fungicidas preventivos. "

                        f"Use como referÃÂÃÂªncia para seleÃÂÃÂ§ÃÂÃÂ£o de cultivares de alto potencial."})



        if gap > 10:

            ganho = gap * 0.4 * area_ha

            recs.append({"zona":"Zonas B vs A","tipo":"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  GAP PRODUTIVO","cor":"#78350f","borda":"#f59e0b",

                "texto":f"DiferenÃÂÃÂ§a de {gap:.1f} sc/ha entre zonas alta e baixa. "

                        f"Potencial de ganho com manejo diferenciado: ÃÂ¢Ã¢ÂÂ°ÃÂ{ganho:.0f} sacas adicionais/safra "

                        f"elevando zona baixa em 40%."})



        bench = {"Soja":60,"Milho":180,"Trigo":55,"FeijÃÂÃÂ£o":40,"Arroz":160,"AlgodÃÂÃÂ£o":280,"CafÃÂÃÂ©":35}.get(cultura, 60)

        if media < bench * 0.75:

            recs.append({"zona":"Toda lavoura","tipo":f"ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ° ABAIXO DO POTENCIAL ({cultura})","cor":"#4a044e","borda":"#a855f7",

                "texto":f"MÃÂÃÂ©dia {media:.1f} estÃÂÃÂ¡ {((bench-media)/bench*100):.0f}% abaixo da referÃÂÃÂªncia "

                        f"regional ({bench} para {cultura}). Revisar programa completo: solo, semente, nutriÃÂÃÂ§ÃÂÃÂ£o e fitossanidade."})

        elif media >= bench:

            recs.append({"zona":"Toda lavoura","tipo":f"ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ  ACIMA DA MÃÂÃ¢ÂÂ°DIA ({cultura})","cor":"#064e3b","borda":"#10b981",

                "texto":f"ParabÃÂÃÂ©ns! MÃÂÃÂ©dia {media:.1f} supera a referÃÂÃÂªncia de {bench} para {cultura}. "

                        f"Documente o manejo desta safra como referÃÂÃÂªncia para as prÃÂÃÂ³ximas."})

        return recs



    def chamar_ia_colheita(stats, col_prod, cultura, area_ha, nome_arquivo, recs):

        try:

            resumo_rec = "\n".join([f"- {r['tipo']} ({r['zona']}): {r['texto'][:100]}..." for r in recs])

            prompt = f"""VocÃÂÃÂª ÃÂÃÂ© um agrÃÂÃÂ´nomo especialista em agricultura de precisÃÂÃÂ£o analisando um mapa de colheita do app IAAgro.



DADOS:

- Arquivo: {nome_arquivo} | Cultura: {cultura} | ÃÂÃÂrea: {area_ha} ha | Pontos: {stats['total_pts']}



ESTATÃÂÃÂSTICAS:

- MÃÂÃÂ©dia: {stats['media']:.1f} sc/ha | Mediana: {stats['mediana']:.1f}

- MÃÂÃÂ­nimo: {stats['minimo']:.1f} | MÃÂÃÂ¡ximo: {stats['maximo']:.1f}

- Desvio padrÃÂÃÂ£o: {stats['desvio']:.1f} | CV: {stats['cv']:.1f}%

- Zona Baixa: {stats.get('pct_ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa',0):.0f}% da ÃÂÃÂ¡rea (mÃÂÃÂ©dia {stats.get('med_ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa',0):.1f})

- Zona MÃÂÃÂ©dia: {stats.get('pct_ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dia',0):.0f}% da ÃÂÃÂ¡rea (mÃÂÃÂ©dia {stats.get('med_ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dia',0):.1f})

- Zona Alta:  {stats.get('pct_ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta',0):.0f}% da ÃÂÃÂ¡rea (mÃÂÃÂ©dia {stats.get('med_ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta',0):.1f})



RECOMENDAÃÂÃ¢ÂÂ¡ÃÂÃ¢ÂÂ¢ES AUTOMÃÂÃÂTICAS:

{resumo_rec}



Gere um laudo agronÃÂÃÂ´mico profissional com:

1. DIAGNÃÂÃ¢ÂÂSTICO GERAL (2-3 frases sobre desempenho da lavoura)

2. ANÃÂÃÂLISE DA VARIABILIDADE ESPACIAL (interprete o CV e causas provÃÂÃÂ¡veis)

3. PRIORIDADES DE MANEJO (top 3 aÃÂÃÂ§ÃÂÃÂµes para prÃÂÃÂ³xima safra)

4. PROJEÃÂÃ¢ÂÂ¡ÃÂÃÂO DE GANHO (o que ÃÂÃÂ© possÃÂÃÂ­vel alcanÃÂÃÂ§ar com manejo diferenciado)

5. NOTA DO TALHÃÂÃÂO (0-100 com justificativa breve)



Seja direto, tÃÂÃÂ©cnico e acessÃÂÃÂ­vel ao produtor rural brasileiro. MÃÂÃÂ¡ximo 350 palavras."""

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



    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ UPLOAD ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Carregar Mapa de Colheita")

    col_up1, col_up2 = st.columns([2,1])

    with col_up1:

        arquivo = st.file_uploader(

            "Selecione o arquivo",

            type=["csv","xlsx","xls","geojson","json","zip"],

            help="CSV/Excel: John Deere Ops Center, Climate, AFS Connect | GeoJSON/Shapefile ZIP"

        )

    with col_up2:

        cultura_mapa = st.selectbox("Cultura", get_culturas() + ["Outro"], key="cultura_mapa_sel")

        area_mapa    = st.number_input("ÃÂÃÂrea (ha)", min_value=0.1, value=float(st.session_state.dados.get("area",50.0)), key="area_mapa_num")



    if arquivo is not None and arquivo.name != st.session_state.harvest_arquivo:

        st.session_state.harvest_arquivo = arquivo.name

        st.session_state.harvest_df      = None

        st.session_state.harvest_analise = None

        with st.spinner(f"ÃÂ¢ÃÂÃÂ³ Lendo {arquivo.name}..."):

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

                        except Exception: pass  # erro silenciado ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o crÃÂÃÂ­tico

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

                                except Exception: pass  # erro silenciado ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o crÃÂÃÂ­tico

                elif nome.endswith(".zip"):

                    st.markdown('''<div style="background:#78350f;color:#fff;padding:12px 18px;border-radius:10px;border-left:5px solid #f59e0b;font-weight:600;">ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Para Shapefile: pip install geopandas</div>''', unsafe_allow_html=True)



                if df_raw is not None and len(df_raw) > 0:

                    st.session_state.harvest_df = df_raw

                    success_box(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ {arquivo.name} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {len(df_raw):,} pontos carregados")

                else:

                    error_box("NÃÂÃÂ£o foi possÃÂÃÂ­vel ler. Verifique o formato.")

            except Exception as e:

                error_box(f"Erro: {e}")



    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ CONFIGURAR E ANALISAR ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    if st.session_state.harvest_df is not None:

        df = st.session_state.harvest_df.copy()

        st.divider()

        st.subheader("ÃÂ¢ÃÂ¡Ã¢ÂÂ¢ÃÂ¯ÃÂ¸ÃÂ Configurar AnÃÂÃÂ¡lise")



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

            st.checkbox("Remover outliers automÃÂÃÂ¡tico (ÃÂÃÂ±3ÃÂÃÂ)", value=True, key="filtro_out")



        df[col_prod] = pd.to_numeric(df[col_prod], errors="coerce")

        df = df.dropna(subset=[col_prod])

        df = df[df[col_prod] > 0]

        if NUMPY_OK and st.session_state.get("filtro_out", True):

            import numpy as np

            mu, sigma = df[col_prod].mean(), df[col_prod].std()

            df = df[abs(df[col_prod] - mu) <= 3 * sigma]



        st.markdown(f'<div style="background:#0f3460;color:#93c5fd;padding:8px 14px;border-radius:8px;font-size:12px;font-weight:700;">'

                    f'ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  {len(df):,} pontos vÃÂÃÂ¡lidos apÃÂÃÂ³s filtro | Faixa: {df[col_prod].min():.1f} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {df[col_prod].max():.1f} | MÃÂÃÂ©dia prÃÂÃÂ©via: {df[col_prod].mean():.1f}</div>',

                    unsafe_allow_html=True)



        if st.button("ÃÂ°ÃÂ¸ÃÂ¡Ã¢ÂÂ¬ Analisar Mapa com IA", use_container_width=True, key="btn_analisar"):

            with st.spinner("ÃÂ°ÃÂ¸ÃÂ¤Ã¢ÂÂ Processando... gerando zonas, grÃÂÃÂ¡ficos e laudo IA..."):

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

            success_box("ÃÂ¢ÃÂÃ¢ÂÂ¦ AnÃÂÃÂ¡lise concluÃÂÃÂ­da!")

            st.rerun()



    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ RESULTADOS ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    if st.session_state.harvest_analise:

        an       = st.session_state.harvest_analise

        df_z     = an["df"]

        stats    = an["stats"]

        recs     = an["recs"]

        col_prod = an["col_prod"]

        unid     = an["unidade"].split()[0]



        st.divider()

        st.subheader(f"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  {an['arquivo']} | {an['cultura']} | {an['area_ha']} ha | {an['data']}")



        # MÃÂÃÂ©tricas rÃÂÃÂ¡pidas

        c1,c2,c3,c4,c5,c6 = st.columns(6)

        c1.metric("ÃÂ°ÃÂ¸ÃÂÃÂ¾ MÃÂÃÂ©dia",      f"{stats['media']:.1f}",     unid)

        c2.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  CV",         f"{stats['cv']:.1f}%",       "variabilidade")

        c3.metric("ÃÂ¢ÃÂ¬Ã¢ÂÂ¡ÃÂ¯ÃÂ¸ÃÂ MÃÂÃÂ­nimo",    f"{stats['minimo']:.1f}",     unid)

        c4.metric("ÃÂ¢ÃÂ¬Ã¢ÂÂ ÃÂ¯ÃÂ¸ÃÂ MÃÂÃÂ¡ximo",    f"{stats['maximo']:.1f}",     unid)

        c5.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Zona Baixa", f"{stats.get('pct_ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa',0):.0f}%", "da ÃÂÃÂ¡rea")

        c6.metric("ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Zona Alta",  f"{stats.get('pct_ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta',0):.0f}%",  "da ÃÂÃÂ¡rea")



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TABS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        tab_mapa, tab_graf, tab_tab, tab_ia, tab_rec = st.tabs([

            "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂºÃÂ¯ÃÂ¸ÃÂ Mapa Interativo","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ GrÃÂÃÂ¡ficos","ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Dados","ÃÂ°ÃÂ¸ÃÂ¤Ã¢ÂÂ Laudo IA","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ RecomendaÃÂÃÂ§ÃÂÃÂµes"

        ])



        with tab_mapa:

            if an["has_geo"] and PLOTLY_OK:

                import plotly.express as px

                df_plot = df_z.sample(min(5000,len(df_z)), random_state=42) if len(df_z)>5000 else df_z

                fig_map = px.scatter_mapbox(

                    df_plot, lat=an["col_lat"], lon=an["col_lon"], color=col_prod,

                    color_continuous_scale=[[0,"#dc2626"],[0.4,"#f59e0b"],[0.7,"#16a34a"],[1,"#065f46"]],

                    size_max=8, zoom=13, mapbox_style="open-street-map",

                    title=f"Mapa de Produtividade ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {an['cultura']}",

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

                ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa: &lt; {an["p33"]:.1f} {unid} &nbsp;|&nbsp;

                ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dia: {an["p33"]:.1f} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {an["p66"]:.1f} &nbsp;|&nbsp;

                ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta: &gt; {an["p66"]:.1f} {unid}

                </div>''', unsafe_allow_html=True)



            elif an["has_geo"]:

                lat_c = df_z[an["col_lat"]].mean()

                lon_c = df_z[an["col_lon"]].mean()

                mf = folium.Map(location=[lat_c, lon_c], zoom_start=13)

                cores_z = {"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa":"red","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dia":"orange","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta":"green"}

                for _, row in df_z.sample(min(2000,len(df_z)), random_state=42).iterrows():

                    try:

                        folium.CircleMarker([row[an["col_lat"]], row[an["col_lon"]]],

                            radius=4, color=cores_z.get(row.get("Zona",""),"gray"),

                            fill=True, fill_opacity=0.7,

                            popup=f"{col_prod}: {row[col_prod]:.1f}").add_to(mf)

                    except Exception: pass  # erro silenciado ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o crÃÂÃÂ­tico

                st_folium(mf, width=700, height=500)

            else:

                info_box("Arquivo sem coordenadas geogrÃÂÃÂ¡ficas ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ mapa indisponÃÂÃÂ­vel. Veja os grÃÂÃÂ¡ficos e laudo nas outras abas.")



        with tab_graf:

            if PLOTLY_OK:

                import plotly.express as px

                import plotly.graph_objects as go

                g1, g2 = st.columns(2)

                with g1:

                    fig_h = px.histogram(df_z, x=col_prod, nbins=40, color="Zona",

                        color_discrete_map={"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa":"#dc2626","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dia":"#f59e0b","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta":"#16a34a"},

                        title="DistribuiÃÂÃÂ§ÃÂÃÂ£o por Zona", labels={col_prod:unid}, height=360)

                    fig_h.update_layout(paper_bgcolor="#0f3460",plot_bgcolor="#0f3460",font_color="#f1f5f9")

                    st.plotly_chart(fig_h, use_container_width=True)

                with g2:

                    zc = df_z["Zona"].value_counts().reset_index()

                    zc.columns = ["Zona","Pontos"]

                    fig_p = px.pie(zc, names="Zona", values="Pontos",

                        color="Zona",

                        color_discrete_map={"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa":"#dc2626","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dia":"#f59e0b","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta":"#16a34a"},

                        title="% da ÃÂÃÂrea por Zona", height=360)

                    fig_p.update_layout(paper_bgcolor="#0f3460",font_color="#f1f5f9")

                    st.plotly_chart(fig_p, use_container_width=True)

                fig_b = px.box(df_z, x="Zona", y=col_prod, color="Zona",

                    color_discrete_map={"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa":"#dc2626","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dia":"#f59e0b","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta":"#16a34a"},

                    title="Box Plot por Zona de Manejo", labels={col_prod:unid}, height=380)

                fig_b.update_layout(paper_bgcolor="#0f3460",plot_bgcolor="#0d2137",

                                    font_color="#f1f5f9",showlegend=False,

                                    yaxis=dict(gridcolor="#1e3a5f"))

                st.plotly_chart(fig_b, use_container_width=True)

            else:

                st.bar_chart(df_z[col_prod].value_counts().sort_index())



            # Tabela por zona

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  EstatÃÂÃÂ­sticas por Zona")

            zonas_tab = []

            for z in ["ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dia","ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta"]:

                sub = df_z[df_z["Zona"]==z]

                if len(sub) > 0:

                    zonas_tab.append({"Zona":z,"Pontos":len(sub),

                        "% ÃÂÃÂrea":f"{len(sub)/len(df_z)*100:.1f}%",

                        f"MÃÂÃÂ©dia {unid}":f"{sub[col_prod].mean():.1f}",

                        "MÃÂÃÂ­n":f"{sub[col_prod].min():.1f}","MÃÂÃÂ¡x":f"{sub[col_prod].max():.1f}",

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

            st.caption(f"Exibindo atÃÂÃÂ© 5.000 de {len(df_z):,} pontos")

            st.download_button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Baixar CSV com zonas",

                data=df_z.to_csv(index=False).encode("utf-8"),

                file_name=f"colheita_zonas_{date.today()}.csv",

                mime="text/csv", use_container_width=True)



        with tab_ia:

            st.subheader("ÃÂ°ÃÂ¸ÃÂ¤Ã¢ÂÂ Laudo AgronÃÂÃÂ´mico ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ InteligÃÂÃÂªncia Artificial")

            if an.get("laudo_ia"):

                st.markdown(f'''<div style="background:#0f3460;color:#f1f5f9;padding:22px 26px;

                border-radius:14px;border-left:5px solid #6ee7b7;

                font-size:14px;line-height:2;white-space:pre-wrap;font-weight:500;">

{an["laudo_ia"]}

                </div>''', unsafe_allow_html=True)

                st.divider()

                if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¨ÃÂ¯ÃÂ¸ÃÂ Gerar PDF do Laudo", key="btn_pdf_col", use_container_width=True):

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

                        el.append(Paragraph("<b>LAUDO DE MAPA DE COLHEITA ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ IAAgro IA</b>", sty["Title"]))

                        el.append(Paragraph(f"Arquivo: {an['arquivo']} | Cultura: {an['cultura']} | ÃÂÃÂrea: {an['area_ha']} ha | Data: {an['data']}", sty["Normal"]))

                        el.append(Spacer(1,12))

                        tab_data = [["MÃÂÃÂ©trica","Valor"],

                            ["MÃÂÃÂ©dia", f"{stats['media']:.1f} {unid}"],

                            ["MÃÂÃÂ­nimo/MÃÂÃÂ¡ximo", f"{stats['minimo']:.1f} / {stats['maximo']:.1f}"],

                            ["Desvio PadrÃÂÃÂ£o", f"{stats['desvio']:.1f}"],

                            ["Coef. VariaÃÂÃÂ§ÃÂÃÂ£o", f"{stats['cv']:.1f}%"],

                            ["Pontos", f"{stats['total_pts']:,}"],

                            ["Zona Baixa", f"{stats.get('pct_ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa',0):.0f}% ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {stats.get('med_ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Baixa',0):.1f} {unid}"],

                            ["Zona MÃÂÃÂ©dia",  f"{stats.get('pct_ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dia',0):.0f}% ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {stats.get('med_ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¡ MÃÂÃÂ©dia',0):.1f} {unid}"],

                            ["Zona Alta",   f"{stats.get('pct_ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta',0):.0f}% ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {stats.get('med_ÃÂ°ÃÂ¸ÃÂ¸ÃÂ¢ Alta',0):.1f} {unid}"],

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

                        el.append(Paragraph("<b>LAUDO AGRONÃÂÃ¢ÂÂMICO IA</b>", sty["Heading2"]))

                        el.append(Spacer(1,6))

                        for linha in an["laudo_ia"].split("\n"):

                            if linha.strip():

                                el.append(Paragraph(linha, sty["BodyText"]))

                                el.append(Spacer(1,3))

                        el.append(Spacer(1,12))

                        el.append(Paragraph("<b>RECOMENDAÃÂÃ¢ÂÂ¡ÃÂÃ¢ÂÂ¢ES DE MANEJO</b>", sty["Heading2"]))

                        el.append(Spacer(1,6))

                        for r in recs:

                            el.append(Paragraph(f"<b>{r['tipo']} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {r['zona']}</b>", sty["Heading3"]))

                            el.append(Paragraph(r["texto"], sty["BodyText"]))

                            el.append(Spacer(1,8))

                        doc_p.build(el)

                        pdf_b = buf_pdf.getvalue()

                        buf_pdf.close()

                        st.download_button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Baixar Laudo PDF", data=pdf_b,

                            file_name=f"laudo_colheita_{date.today()}.pdf",

                            mime="application/pdf", use_container_width=True)

                    except Exception as e:

                        error_box(f"Erro ao gerar PDF: {e}")

            else:

                warning_box("Laudo IA indisponÃÂÃÂ­vel. Verifique a conexÃÂÃÂ£o com a internet. As recomendaÃÂÃÂ§ÃÂÃÂµes automÃÂÃÂ¡ticas estÃÂÃÂ£o na aba RecomendaÃÂÃÂ§ÃÂÃÂµes.")



        with tab_rec:

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ RecomendaÃÂÃÂ§ÃÂÃÂµes de Manejo por Zona")

            for r in recs:

                st.markdown(f'''<div style="background:{r["cor"]};color:#fff;padding:14px 18px;

                border-radius:12px;border-left:6px solid {r["borda"]};

                font-size:14px;line-height:1.9;margin:8px 0;">

                <b>{r["tipo"]}</b> &nbsp;|&nbsp; Zona: {r["zona"]}<br>{r["texto"]}

                </div>''', unsafe_allow_html=True)



            st.divider()

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Plano de AÃÂÃÂ§ÃÂÃÂ£o ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ PrÃÂÃÂ³xima Safra")

            acoes = [

                ("PrÃÂÃÂ©-plantio","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¬","Coletar amostras de solo por zona (mÃÂÃÂ­n. 1/zona)"),

                ("PrÃÂÃÂ©-plantio","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ","Delimitar zonas de manejo no GPS do trator"),

                ("Plantio","ÃÂ°ÃÂ¸ÃÂÃÂ±","Aplicar taxa variÃÂÃÂ¡vel de P e K por zona"),

                ("V3ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂV4","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ ","Monitorar desenvolvimento por zona com fotos georeferenciadas"),

                ("FloraÃÂÃÂ§ÃÂÃÂ£o","ÃÂ°ÃÂ¸ÃÂ¡ÃÂ","NDVI por drone ou satÃÂÃÂ©lite para correlacionar com mapa"),

                ("Colheita","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¡","Ativar monitor de produtividade para novo mapa"),

                ("PÃÂÃÂ³s-colheita","ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ ","Comparar este mapa com o anterior no IAAgro"),

            ]

            st.dataframe(pd.DataFrame(acoes, columns=["Momento","","AÃÂÃÂ§ÃÂÃÂ£o"]),

                         use_container_width=True, hide_index=True)



    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ HISTÃÂÃ¢ÂÂRICO DE MAPAS ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    if st.session_state.harvest_historico:

        st.divider()

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ HistÃÂÃÂ³rico de Mapas Analisados")

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

                title="EvoluÃÂÃÂ§ÃÂÃÂ£o da Produtividade MÃÂÃÂ©dia entre Safras",

                paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",

                font_color="#f1f5f9", xaxis_title="Mapa/Safra",

                yaxis_title="MÃÂÃÂ©dia sc/ha", height=300

            )

            st.plotly_chart(fig_ev, use_container_width=True)



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Assistente IA (tab 4) ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸ÃÂÃÂ InteligÃÂÃÂªncia":

  with _sub_int[4]:

    st.header("ÃÂ°ÃÂ¸ÃÂ¤Ã¢ÂÂ Assistente IA AgrÃÂÃÂ­cola")

    st.markdown("""

    <div style='background:#0f3460;border-radius:10px;padding:12px 16px;

    border:1px solid #22c55e;margin-bottom:12px;'>

    <b style='color:#22c55e;'>ÃÂ°ÃÂ¸ÃÂÃÂ¾ Pergunte sobre sua lavoura</b><br>

    <span style='color:#f1f5f9;font-size:13px;'>

    Tire dÃÂÃÂºvidas sobre manejo, pragas, doenÃÂÃÂ§as, adubaÃÂÃÂ§ÃÂÃÂ£o, mercado e muito mais.

    </span>

    </div>

    """, unsafe_allow_html=True)



    # Contexto da ÃÂÃÂ¡rea ativa

    _ctx_area = ""

    if st.session_state.get("dados"):

        d = st.session_state.dados

        _ctx_area = (

            f"Cultura: {d.get('cultura','Soja')}, "

            f"ÃÂÃÂrea: {d.get('area',0)} ha, "

            f"pH: {d.get('ph',0)}, "

            f"RegiÃÂÃÂ£o: {d.get('cidade','Sul do Brasil')}, "

            f"Produtividade esperada: {d.get('produtividade',0)} sc/ha"

        )



    # HistÃÂÃÂ³rico do chat

    if "assistente_hist" not in st.session_state:

        st.session_state.assistente_hist = []



    # Exibe mensagens anteriores

    for msg in st.session_state.assistente_hist:

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])



    # Input

    _prompt = st.chat_input("Digite sua pergunta agrÃÂÃÂ­cola...")

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

                        "VocÃÂÃÂª ÃÂÃÂ© um assistente agrÃÂÃÂ­cola especialista brasileiro. "

                        "Responda em portuguÃÂÃÂªs, de forma prÃÂÃÂ¡tica e objetiva para produtores rurais. "

                        "Baseie suas respostas em EMBRAPA, CQFS RS/SC 2016 e boas prÃÂÃÂ¡ticas agrÃÂÃÂ­colas. "

                        f"Contexto da propriedade: {_ctx_area if _ctx_area else 'nÃÂÃÂ£o informado'}."

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



    # BotÃÂÃÂ£o limpar histÃÂÃÂ³rico

    if st.session_state.assistente_hist:

        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Limpar conversa", key="btn_limpar_assistente"):

            st.session_state.assistente_hist = []

            st.rerun()



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

# MENU: SEGUNDA SAFRA / SAFRINHA

# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

elif menu == "ÃÂ°ÃÂ¸ÃÂÃÂ± Safrinha":

    st.header("ÃÂ°ÃÂ¸ÃÂÃÂ± Safrinha")



    st.markdown("""

    <div style='background:#0f3460;border-radius:12px;padding:14px 18px;

    border-left:5px solid #22c55e;margin-bottom:16px;'>

    <b style='color:#22c55e;font-size:15px;'>ÃÂ°ÃÂ¸ÃÂÃÂ± Planejamento de Safrinha</b><br>

    <span style='color:#f1f5f9;font-size:13px;'>

    Planeje a safrinha apÃÂÃÂ³s a colheita da safra principal. Escolha a ÃÂÃÂ¡rea cadastrada,

    defina a cultura, custos e acompanhe a rentabilidade do ciclo.

    </span>

    </div>

    """, unsafe_allow_html=True)



    # Inicializa session_state

    if "safrinha_registros" not in st.session_state:

        st.session_state.safrinha_registros = []



    tab_s1, tab_s2, tab_s3 = st.tabs([

        "ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Planejar Safrinha",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Registros",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  AnÃÂÃÂ¡lise de Rentabilidade"

    ])



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ CombinaÃÂÃÂ§ÃÂÃÂµes tÃÂÃÂ­picas da regiÃÂÃÂ£o ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    ROTACOES_TIPICAS = {

        "Milho ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ FeijÃÂÃÂ£o":   {"1a":"Milho", "2a":"FeijÃÂÃÂ£o", "janela":"SetÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂJan / FevÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂMai"},

        "Milho ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ Soja":     {"1a":"Milho", "2a":"Soja",   "janela":"SetÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂJan / OutÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂMar"},

        "Soja ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ FeijÃÂÃÂ£o":    {"1a":"Soja",  "2a":"FeijÃÂÃÂ£o", "janela":"OutÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂJan / FevÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂMai"},

        "FeijÃÂÃÂ£o ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ Soja":    {"1a":"FeijÃÂÃÂ£o","2a":"Soja",   "janela":"JanÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂAbr / OutÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂMar"},

        "FeijÃÂÃÂ£o ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ Milho":   {"1a":"FeijÃÂÃÂ£o","2a":"Milho",  "janela":"JanÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂAbr / AbrÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂAgo"},

        "Soja ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ Milho":     {"1a":"Soja",  "2a":"Milho",  "janela":"OutÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂJan / FevÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂJun"},

    }



    CULTURAS_SAFRINHA = ["Milho","Soja","FeijÃÂÃÂ£o"]



    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    # TAB 1 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ PLANEJAR ROTAÃÂÃ¢ÂÂ¡ÃÂÃÂO

    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    with tab_s1:

        st.subheader("ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Novo Planejamento de Safrinha")



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ SeleÃÂÃÂ§ÃÂÃÂ£o de ÃÂÃÂ¡rea cadastrada ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        areas_cadastradas = st.session_state.get("areas", [])

        area_selecionada_sf = None

        if areas_cadastradas:

            opcoes_areas = ["ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Selecione uma ÃÂÃÂ¡rea cadastrada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"] + [

                f"{a.get('Fazenda','?')} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {a.get('TalhÃÂÃÂ£o','?')} ({a.get('Hectares',0):.1f} ha | {a.get('Cultura','?')})"

                for a in areas_cadastradas

            ]

            area_choice = st.selectbox("ÃÂ°ÃÂ¸ÃÂÃÂ¾ ÃÂÃÂrea cadastrada", opcoes_areas, key="sf_area_choice")

            if area_choice != "ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Selecione uma ÃÂÃÂ¡rea cadastrada ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ":

                idx_area = opcoes_areas.index(area_choice) - 1

                area_selecionada_sf = areas_cadastradas[idx_area]

                st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ ÃÂÃÂrea carregada: **{area_selecionada_sf.get('Fazenda','')} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {area_selecionada_sf.get('TalhÃÂÃÂ£o','')}**")

        else:

            st.info("Nenhuma ÃÂÃÂ¡rea cadastrada. VÃÂÃÂ¡ em **Cadastro da ÃÂÃÂrea** para adicionar.")



        # Preenche defaults da ÃÂÃÂ¡rea selecionada

        _area_ha   = float(area_selecionada_sf.get("Hectares", 10.0))    if area_selecionada_sf else 10.0

        _cultura   = area_selecionada_sf.get("Cultura", "Soja")           if area_selecionada_sf else "Soja"

        _prod      = float(area_selecionada_sf.get("Meta Produtividade", 60.0)) if area_selecionada_sf else 60.0

        _talhao    = f"{area_selecionada_sf.get('Fazenda','')} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {area_selecionada_sf.get('TalhÃÂÃÂ£o','')}" if area_selecionada_sf else ""

        _cidade    = area_selecionada_sf.get("Cidade", "")                if area_selecionada_sf else ""



        st.divider()



        # SeleÃÂÃÂ§ÃÂÃÂ£o rÃÂÃÂ¡pida de rotaÃÂÃÂ§ÃÂÃÂ£o tÃÂÃÂ­pica

        rotacao_sel = st.selectbox(

            "ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ RotaÃÂÃÂ§ÃÂÃÂ£o tÃÂÃÂ­pica da regiÃÂÃÂ£o",

            list(ROTACOES_TIPICAS.keys()),

            key="safrinha_rotacao_sel"

        )

        rot_info = ROTACOES_TIPICAS[rotacao_sel]

        if rot_info["janela"]:

            st.caption(f"ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¦ Janela de plantio: {rot_info['janela']}")



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Dados da Safrinha ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

        st.markdown("#### ÃÂ°ÃÂ¸ÃÂÃÂ± Dados da Safrinha")

        culturas_1a = CULTURAS_SAFRINHA

        cultura_1a  = _cultura  # cultura da ÃÂÃÂ¡rea selecionada (safra principal)

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

            cultura_2a = st.selectbox("ÃÂ°ÃÂ¸ÃÂÃÂ± Cultura da safrinha", culturas_1a, index=idx_2a, key="sf_cult2")

            area_2a    = st.number_input("ÃÂÃÂrea (ha)", min_value=0.0, value=_area_ha, key="sf_area2")

            prod_2a    = st.number_input("Produtividade esperada (sc/ha)", min_value=0.0, value=45.0, key="sf_prod2")

        with col_sf2:

            preco_2a   = st.number_input("PreÃÂÃÂ§o da saca R$", min_value=0.0, value=58.0, key="sf_preco2")

            custo_2a   = st.number_input("Custo total R$/ha", min_value=0.0, value=2200.0, key="sf_custo2")

            plantio_2a = st.text_input("Data de plantio", placeholder="Ex: 25/02/2026", key="sf_plant2")

            colheita_2a = st.text_input("PrevisÃÂÃÂ£o de colheita", placeholder="Ex: 30/05/2026", key="sf_colh2")



        st.divider()

        col_obs1, col_obs2 = st.columns(2)

        with col_obs1:

            talhao_sf  = st.text_input("TalhÃÂÃÂ£o / ÃÂÃÂrea", value=_talhao, placeholder="Ex: TalhÃÂÃÂ£o A", key="sf_talhao")

            safra_sf   = st.text_input("Safra", placeholder="Ex: 2025/2026", key="sf_safra")

        with col_obs2:

            obs_sf     = st.text_area("ObservaÃÂÃÂ§ÃÂÃÂµes", placeholder="Ex: Solo compactado, uso de cobertura...", key="sf_obs", height=80)



        # Preview da rentabilidade antes de salvar

        rec_1a  = prod_1a * preco_1a * area_1a

        cus_1a  = custo_1a * area_1a

        luc_1a  = rec_1a - cus_1a

        rec_2a  = prod_2a * preco_2a * area_2a

        cus_2a  = custo_2a * area_2a

        luc_2a  = rec_2a - cus_2a

        luc_tot = luc_1a + luc_2a



        st.markdown("#### ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Preview de Rentabilidade")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(f"Receita {cultura_1a}", f"R$ {rec_1a:,.0f}")

        c2.metric(f"Receita {cultura_2a}", f"R$ {rec_2a:,.0f}")

        c3.metric("Lucro Total", f"R$ {luc_tot:,.0f}",

                  delta="ÃÂ¢ÃÂÃ¢ÂÂ¦ Positivo" if luc_tot > 0 else "ÃÂ¢ÃÂÃÂ Negativo")

        c4.metric("Lucro/ha mÃÂÃÂ©dio", f"R$ {luc_tot/max(area_1a,1):,.0f}")



        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Salvar Planejamento", use_container_width=True, key="btn_salvar_safrinha"):

            if not talhao_sf.strip():

                st.error("Informe o talhÃÂÃÂ£o.")

            else:

                registro = {

                    "id":          len(st.session_state.safrinha_registros) + 1,

                    "safra":       safra_sf,

                    "talhao":      talhao_sf,

                    "rotacao":     f"{cultura_1a} ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ {cultura_2a}",

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

                st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ RotaÃÂÃÂ§ÃÂÃÂ£o **{cultura_1a} ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ {cultura_2a}** salva para o talhÃÂÃÂ£o **{talhao_sf}**!")

                st.balloons()

                st.rerun()



    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    # TAB 2 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ REGISTROS

    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    with tab_s2:

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Registros de Safrinha")

        if not st.session_state.safrinha_registros:

            st.info("Nenhum planejamento salvo ainda. Use a aba ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Planejar RotaÃÂÃÂ§ÃÂÃÂ£o.")

        else:

            for i, reg in enumerate(st.session_state.safrinha_registros):

                cor = "#14532d" if reg["lucro_total"] > 0 else "#7f1d1d"

                borda = "#22c55e" if reg["lucro_total"] > 0 else "#ef4444"

                st.markdown(f"""

                <div style='background:{cor};border-radius:12px;padding:14px 18px;

                border-left:5px solid {borda};margin-bottom:10px;'>

                <b style='color:#f1f5f9;font-size:15px;'>ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ {reg['rotacao']} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {reg['talhao']} ({reg.get('safra','')})</b><br>

                <span style='color:#d1fae5;font-size:13px;'>

                ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¦ {reg['cultura_1a']}: plantio {reg.get('plantio_1a','ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ')} ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ colheita {reg.get('colheita_1a','ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ')} &nbsp;|&nbsp;

                {reg['cultura_2a']}: plantio {reg.get('plantio_2a','ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ')} ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ colheita {reg.get('colheita_2a','ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ')}

                </span><br>

                <span style='color:#86efac;font-size:13px;'>

                ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Lucro total: <b>R$ {reg['lucro_total']:,.2f}</b> &nbsp;|&nbsp;

                1ÃÂÃÂª safra: R$ {reg['lucro_1a']:,.2f} &nbsp;|&nbsp;

                2ÃÂÃÂª safra: R$ {reg['lucro_2a']:,.2f}

                </span>

                </div>

                """, unsafe_allow_html=True)



                col_ed, col_del = st.columns([5,1])

                with col_del:

                    if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ", key=f"del_safrinha_{i}", help="Excluir registro"):

                        st.session_state.safrinha_registros.pop(i)

                        salvar_dados_iaagro()

                        st.rerun()



            # Tabela resumo

            st.divider()

            st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Tabela Resumo")

            df_sf = pd.DataFrame([{

                "TalhÃÂÃÂ£o":      r["talhao"],

                "Safra":       r.get("safra",""),

                "RotaÃÂÃÂ§ÃÂÃÂ£o":     r["rotacao"],

                "ÃÂÃÂrea 1ÃÂÃÂª ha":  r["area_1a"],

                "Prod 1ÃÂÃÂª sc/ha": r["prod_1a"],

                "ÃÂÃÂrea 2ÃÂÃÂª ha":  r["area_2a"],

                "Prod 2ÃÂÃÂª sc/ha": r["prod_2a"],

                "Receita Total R$": r["receita_1a"] + r["receita_2a"],

                "Lucro Total R$":   r["lucro_total"],

            } for r in st.session_state.safrinha_registros])

            st.dataframe(df_sf, use_container_width=True)



    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    # TAB 3 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ ANÃÂÃÂLISE DE RENTABILIDADE

    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    with tab_s3:

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  AnÃÂÃÂ¡lise de Rentabilidade por RotaÃÂÃÂ§ÃÂÃÂ£o")

        if not st.session_state.safrinha_registros:

            st.info("Salve ao menos um planejamento para ver a anÃÂÃÂ¡lise.")

        else:

            import plotly.express as px



            df_an = pd.DataFrame([{

                "RotaÃÂÃÂ§ÃÂÃÂ£o":        r["rotacao"],

                "TalhÃÂÃÂ£o":         r["talhao"],

                "Lucro Total R$": r["lucro_total"],

                "Receita 1ÃÂÃÂª R$":  r["receita_1a"],

                "Receita 2ÃÂÃÂª R$":  r["receita_2a"],

                "Lucro 1ÃÂÃÂª R$":    r["lucro_1a"],

                "Lucro 2ÃÂÃÂª R$":    r["lucro_2a"],

            } for r in st.session_state.safrinha_registros])



            # GrÃÂÃÂ¡fico comparativo

            fig_rot = px.bar(

                df_an, x="TalhÃÂÃÂ£o", y=["Lucro 1ÃÂÃÂª R$","Lucro 2ÃÂÃÂª R$"],

                barmode="group", title="ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Lucro por Safra e TalhÃÂÃÂ£o",

                color_discrete_sequence=["#22c55e","#3b82f6"],

                template="plotly_dark"

            )

            fig_rot.update_layout(

                paper_bgcolor="#0f3460", plot_bgcolor="#0d2137",

                font_color="#f1f5f9", height=350

            )

            st.plotly_chart(fig_rot, use_container_width=True)



            # Melhor rotaÃÂÃÂ§ÃÂÃÂ£o

            melhor = df_an.loc[df_an["Lucro Total R$"].idxmax()]

            st.markdown(f"""

            <div style='background:#14532d;border-radius:12px;padding:14px 18px;

            border-left:5px solid #22c55e;margin-top:8px;'>

            <b style='color:#22c55e;'>ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ  RotaÃÂÃÂ§ÃÂÃÂ£o mais rentÃÂÃÂ¡vel:</b>

            <span style='color:#f1f5f9;font-size:14px;'>

            &nbsp;<b>{melhor['RotaÃÂÃÂ§ÃÂÃÂ£o']}</b> ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ TalhÃÂÃÂ£o {melhor['TalhÃÂÃÂ£o']} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ 

            Lucro total: <b>R$ {melhor['Lucro Total R$']:,.2f}</b>

            </span>

            </div>

            """, unsafe_allow_html=True)



            # MÃÂÃÂ©tricas gerais

            st.divider()

            c1, c2, c3 = st.columns(3)

            c1.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Lucro total acumulado", f"R$ {df_an['Lucro Total R$'].sum():,.2f}")

            c2.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ MÃÂÃÂ©dia por rotaÃÂÃÂ§ÃÂÃÂ£o",     f"R$ {df_an['Lucro Total R$'].mean():,.2f}")

            c3.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ RotaÃÂÃÂ§ÃÂÃÂµes planejadas",   len(df_an))



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

if menu == "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Financeiro":

  with _sub_fin[3]:

    st.header("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂµ Fluxo de Caixa")

    if not st.session_state.areas:

        st.info("Cadastre uma ÃÂÃÂ¡rea para visualizar o fluxo de caixa.")

    else:

        _areas_fc = [f"{a['ID']} - {a['TalhÃÂÃÂ£o']}" for a in st.session_state.areas]

        _area_fc  = st.selectbox("ÃÂÃÂrea", _areas_fc, key="sel_area_fluxo_caixa")

        _id_fc    = _area_fc.split(" - ")[0]



        st.subheader("ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ LanÃÂÃÂ§amentos")

        col_fc1, col_fc2, col_fc3 = st.columns(3)

        with col_fc1:

            _data_fc   = st.date_input("Data", key="date_fc")

            _tipo_fc   = st.selectbox("Tipo", ["Receita","Despesa"], key="sel_tipo_fc")

        with col_fc2:

            _categ_fc  = st.selectbox("Categoria",

                ["Venda de grÃÂÃÂ£os","Venda de subproduto","Insumos","MaquinÃÂÃÂ¡rio",

                 "MÃÂÃÂ£o de obra","Arrendamento","Frete","Seguro","Outros"], key="sel_categ_fc")

            _valor_fc  = st.number_input("Valor R$", min_value=0.0, key="num_valor_fc")

        with col_fc3:

            _desc_fc   = st.text_input("DescriÃÂÃÂ§ÃÂÃÂ£o", key="txt_desc_fc")

            _pago_fc   = st.checkbox("Pago/Recebido", value=True, key="chk_pago_fc")



        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ LanÃÂÃÂ§ar", key="btn_lancar_fc", use_container_width=True):

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

                st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ {'Receita' if _tipo_fc=='Receita' else 'Despesa'} de R$ {_valor_fc:.2f} lanÃÂÃÂ§ada!")

            else:

                st.warning("Digite um valor maior que zero.")



        # Exibe saldo e lanÃÂÃÂ§amentos

        _lanc = [l for l in st.session_state.get("fluxo_caixa", []) if l.get("area_id") == _id_fc]

        if _lanc:

            import pandas as pd

            df_fc = pd.DataFrame(_lanc)

            df_fc["valor_signed"] = df_fc.apply(lambda r: r["valor"] if r["tipo"]=="Receita" else -r["valor"], axis=1)

            _total_rec  = df_fc[df_fc["tipo"]=="Receita"]["valor"].sum()

            _total_desp = df_fc[df_fc["tipo"]=="Despesa"]["valor"].sum()

            _saldo      = _total_rec - _total_desp



            col_s1, col_s2, col_s3 = st.columns(3)

            col_s1.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¡ Receitas", f"R$ {_total_rec:,.2f}")

            col_s2.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ´ Despesas", f"R$ {_total_desp:,.2f}")

            col_s3.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Saldo", f"R$ {_saldo:,.2f}",

                         delta=f"{'positivo' if _saldo >= 0 else 'negativo'}")



            # GrÃÂÃÂ¡fico evoluÃÂÃÂ§ÃÂÃÂ£o

            df_fc["data_dt"] = pd.to_datetime(df_fc["data"])

            df_fc = df_fc.sort_values("data_dt")

            df_fc["saldo_acum"] = df_fc["valor_signed"].cumsum()

            st.line_chart(df_fc.set_index("data_dt")["saldo_acum"])



            # Tabela

            st.dataframe(

                df_fc[["data","tipo","categoria","descricao","valor","pago"]]

                .rename(columns={"data":"Data","tipo":"Tipo","categoria":"Categoria",

                                  "descricao":"DescriÃÂÃÂ§ÃÂÃÂ£o","valor":"R$","pago":"Pago"}),

                use_container_width=True

            )



            # Excluir

            with st.expander("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Excluir lanÃÂÃÂ§amento"):

                _opcoes = [f"{l['data']} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {l['tipo']} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ R${l['valor']:.2f} ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ {l['descricao']}" for l in _lanc]

                _del_fc = st.selectbox("Selecione", _opcoes, key="sel_del_fc")

                if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂÃÂ¯ÃÂ¸ÃÂ Excluir", key="btn_del_fc"):

                    _idx_del = _opcoes.index(_del_fc)

                    _all_ids = [i for i, l in enumerate(st.session_state.fluxo_caixa)

                                if l.get("area_id") == _id_fc]

                    st.session_state.fluxo_caixa.pop(_all_ids[_idx_del])

                    salvar_dados_iaagro()

                    st.success("LanÃÂÃÂ§amento excluÃÂÃÂ­do!")

                    st.rerun()

        else:

            st.info("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Nenhum lanÃÂÃÂ§amento para esta ÃÂÃÂ¡rea ainda.")



  with _sub_fin[4]:

    import io

    st.header("ÃÂ°ÃÂ¸ÃÂ§ÃÂ¾ Imposto de Renda ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Produtor Rural")



    st.markdown("""

    <div style='background:#0f3460;border-radius:12px;padding:14px 18px;border-left:5px solid #22c55e;margin-bottom:16px;'>

    <b style='color:#22c55e'>ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Sobre este mÃÂÃÂ³dulo</b><br>

    <span style='color:#f1f5f9;font-size:13px;'>

    Calcula o Imposto de Renda da atividade rural conforme a legislaÃÂÃÂ§ÃÂÃÂ£o brasileira (Lei 8.023/90 e IN RFB 1.700/17).

    Preencha as receitas e despesas para gerar o relatÃÂÃÂ³rio completo em PDF pronto para seu contador.

    </span>

    </div>

    """, unsafe_allow_html=True)



    tab_ir1, tab_ir2, tab_ir3 = st.tabs([

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Receitas & Despesas",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Resultado & CÃÂÃÂ¡lculo",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Gerar RelatÃÂÃÂ³rio PDF"

    ])



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Inicializa session_state IR ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    if "ir_ano"        not in st.session_state: st.session_state.ir_ano        = 2025

    if "ir_receitas"   not in st.session_state: st.session_state.ir_receitas   = {}

    if "ir_despesas"   not in st.session_state: st.session_state.ir_despesas   = {}

    if "ir_nome"       not in st.session_state: st.session_state.ir_nome       = ""

    if "ir_cpf"        not in st.session_state: st.session_state.ir_cpf        = ""

    if "ir_cidade"     not in st.session_state: st.session_state.ir_cidade     = ""

    if "ir_area_total" not in st.session_state: st.session_state.ir_area_total = 0.0

    if "ir_producao"   not in st.session_state: st.session_state.ir_producao   = {}



    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    # TAB 1 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ RECEITAS & DESPESAS

    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    with tab_ir1:

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¤ Dados do Produtor")

        col_id1, col_id2, col_id3 = st.columns(3)

        with col_id1:

            st.session_state.ir_nome  = st.text_input("Nome completo", value=st.session_state.ir_nome, key="ir_nome_input")

            st.session_state.ir_cpf   = st.text_input("CPF", value=st.session_state.ir_cpf, key="ir_cpf_input", placeholder="000.000.000-00")

        with col_id2:

            st.session_state.ir_cidade     = st.text_input("Cidade/UF", value=st.session_state.ir_cidade, key="ir_cidade_input")

            st.session_state.ir_area_total = st.number_input("ÃÂÃÂrea total (ha)", min_value=0.0, value=st.session_state.ir_area_total, key="ir_area_input")

        with col_id3:

            st.session_state.ir_ano = st.selectbox("Ano-calendÃÂÃÂ¡rio", [2025, 2024, 2023, 2022], key="ir_ano_sel")



        st.divider()

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ Receitas da Atividade Rural")

        st.caption("Informe todas as receitas brutas recebidas no ano")



        # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ ImportaÃÂÃÂ§ÃÂÃÂ£o automÃÂÃÂ¡tica da Safrinha ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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

            <b style='color:#22c55e;'>ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Dados da Safrinha disponÃÂÃÂ­veis para importar</b><br>

            <span style='color:#f1f5f9;font-size:13px;'>

            {len(safrinha_regs)} rotaÃÂÃÂ§ÃÂÃÂ£o(ÃÂÃÂµes) planejada(s) &nbsp;|&nbsp;

            Receita total: <b>R$ {receita_safrinha:,.2f}</b> &nbsp;|&nbsp;

            Custos: <b>R$ {custo_safrinha:,.2f}</b>

            </span>

            </div>

            """, unsafe_allow_html=True)



            col_imp1, col_imp2 = st.columns(2)

            with col_imp1:

                if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Importar receitas da safrinha", key="btn_imp_rec_safrinha", use_container_width=True):

                    atual = float(st.session_state.ir_receitas.get("venda_graos", 0.0))

                    st.session_state.ir_receitas["venda_graos"] = round(atual + receita_safrinha, 2)

                    st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ R$ {receita_safrinha:,.2f} adicionados ÃÂÃÂ s receitas de grÃÂÃÂ£os!")

                    st.rerun()

            with col_imp2:

                if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Importar custos da safrinha", key="btn_imp_desp_safrinha", use_container_width=True):

                    # Distribui nos campos de despesa correspondentes

                    atual_sem = float(st.session_state.ir_despesas.get("sementes", 0.0))

                    atual_def = float(st.session_state.ir_despesas.get("fertilizantes", 0.0))

                    # 30% sementes, 70% fertilizantes/defensivos como estimativa

                    st.session_state.ir_despesas["sementes"]      = round(atual_sem + custo_safrinha * 0.30, 2)

                    st.session_state.ir_despesas["fertilizantes"] = round(atual_def + custo_safrinha * 0.70, 2)

                    st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ R$ {custo_safrinha:,.2f} distribuÃÂÃÂ­dos nas despesas!")

                    st.rerun()



        rec_items = [

            ("venda_graos",      "ÃÂ°ÃÂ¸ÃÂÃÂ¾ Venda de grÃÂÃÂ£os e cereais (R$)"),

            ("venda_animais",    "ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ Venda de animais e produtos pecuÃÂÃÂ¡rios (R$)"),

            ("arrendamento",     "ÃÂ°ÃÂ¸ÃÂÃÂ¡ Arrendamento recebido (R$)"),

            ("subvencoes",       "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° SubvenÃÂÃÂ§ÃÂÃÂµes e incentivos governamentais (R$)"),

            ("indenizacoes",     "ÃÂ°ÃÂ¸Ã¢ÂÂºÃÂ¡ÃÂ¯ÃÂ¸ÃÂ IndenizaÃÂÃÂ§ÃÂÃÂµes de seguro agrÃÂÃÂ­cola (R$)"),

            ("outras_receitas",  "ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Outras receitas rurais (R$)"),

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

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ° Despesas da Atividade Rural")

        st.caption("Despesas dedutÃÂÃÂ­veis conforme art. 61 do RIR/2018")



        desp_items = [

            ("sementes",         "ÃÂ°ÃÂ¸ÃÂÃÂ± Sementes e mudas (R$)"),

            ("fertilizantes",    "ÃÂ°ÃÂ¸ÃÂ§ÃÂª Fertilizantes e defensivos (R$)"),

            ("mao_de_obra",      "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ· MÃÂÃÂ£o de obra (folha + encargos) (R$)"),

            ("combustivel",      "ÃÂ¢Ã¢ÂÂºÃÂ½ CombustÃÂÃÂ­vel e lubrificantes (R$)"),

            ("energia",          "ÃÂ¢ÃÂ¡ÃÂ¡ Energia elÃÂÃÂ©trica rural (R$)"),

            ("arrendamento_pg",  "ÃÂ°ÃÂ¸ÃÂÃÂ¡ Arrendamento pago (R$)"),

            ("manutencao",       "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ§ ManutenÃÂÃÂ§ÃÂÃÂ£o de mÃÂÃÂ¡quinas e benfeitorias (R$)"),

            ("depreciacao",      "ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ° DepreciaÃÂÃÂ§ÃÂÃÂ£o de bens (R$)"),

            ("frete",            "ÃÂ°ÃÂ¸ÃÂ¡Ã¢ÂÂº Fretes e carretos (R$)"),

            ("seguro",           "ÃÂ°ÃÂ¸Ã¢ÂÂºÃÂ¡ÃÂ¯ÃÂ¸ÃÂ Seguros rurais (R$)"),

            ("assistencia_tec",  "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¨ÃÂ¢Ã¢ÂÂ¬ÃÂÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¬ AssistÃÂÃÂªncia tÃÂÃÂ©cnica e agronÃÂÃÂ´mica (R$)"),

            ("juros",            "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ³ Juros de financiamentos rurais (R$)"),

            ("outras_despesas",  "ÃÂ¢ÃÂ¾Ã¢ÂÂ¢ Outras despesas dedutÃÂÃÂ­veis (R$)"),

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

        st.subheader("ÃÂ°ÃÂ¸ÃÂÃÂ¾ ProduÃÂÃÂ§ÃÂÃÂ£o por Cultura (opcional)")

        st.caption("Para o memorial descritivo do relatÃÂÃÂ³rio")

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



    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    # TAB 2 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ RESULTADO & CÃÂÃÂLCULO

    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    with tab_ir2:

        receita_bruta  = sum(st.session_state.ir_receitas.values())

        despesa_total  = sum(st.session_state.ir_despesas.values())

        resultado_liq  = receita_bruta - despesa_total



        # Resumo da safrinha na base do cÃÂÃÂ¡lculo

        safrinha_regs2 = st.session_state.get("safrinha_registros", [])

        if safrinha_regs2:

            rec_sf  = sum(r.get("receita_1a",0)+r.get("receita_2a",0) for r in safrinha_regs2)

            luc_sf  = sum(r.get("lucro_total",0) for r in safrinha_regs2)

            cus_sf  = sum(r.get("custo_1a",0)*r.get("area_1a",0)+r.get("custo_2a",0)*r.get("area_2a",0) for r in safrinha_regs2)

            importado = float(st.session_state.ir_receitas.get("venda_graos",0)) >= rec_sf * 0.9

            st.markdown(f"""

            <div style='background:#1e3a5f;border-radius:10px;padding:12px 16px;

            border:1px solid #3b82f6;margin-bottom:12px;'>

            <b style='color:#3b82f6;'>ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Safrinha</b>

            {"&nbsp;<span style='color:#22c55e;font-size:12px;'>ÃÂ¢ÃÂÃ¢ÂÂ¦ Dados importados</span>" if importado else "&nbsp;<span style='color:#f59e0b;font-size:12px;'>ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Use o botÃÂÃÂ£o Importar na aba anterior</span>"}<br>

            <span style='color:#f1f5f9;font-size:13px;'>

            Receita total safras: <b>R$ {rec_sf:,.2f}</b> &nbsp;|&nbsp;

            Custos: <b>R$ {cus_sf:,.2f}</b> &nbsp;|&nbsp;

            Lucro lÃÂÃÂ­quido safras: <b>R$ {luc_sf:,.2f}</b>

            </span>

            </div>

            """, unsafe_allow_html=True)



        # Resultado presumido (20% da receita bruta ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ opcional ao resultado real)

        resultado_pres = receita_bruta * 0.20



        # Limite de isenÃÂÃÂ§ÃÂÃÂ£o: R$ 142.798,50 (2025) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ resultado lÃÂÃÂ­quido

        LIMITE_ISENCAO = 142798.50

        BASE_CALCULO   = max(resultado_liq, 0.0)



        # Tabela progressiva IRPF 2025 (resultado lÃÂÃÂ­quido rural entra na base do IRPF)

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

        st.markdown("### ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Demonstrativo de Resultado")

        c1, c2, c3 = st.columns(3)

        c1.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ° Receita Bruta", f"R$ {receita_bruta:,.2f}")

        c2.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ° Despesas DedutÃÂÃÂ­veis", f"R$ {despesa_total:,.2f}")

        cor_res = "normal" if resultado_liq >= 0 else "inverse"

        c3.metric("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Resultado LÃÂÃÂ­quido", f"R$ {resultado_liq:,.2f}", delta=f"{'Lucro' if resultado_liq >= 0 else 'PrejuÃÂÃÂ­zo'}")



        st.divider()

        st.markdown("### ÃÂ°ÃÂ¸ÃÂ§ÃÂ® CÃÂÃÂ¡lculo do Imposto")



        col_calc1, col_calc2 = st.columns(2)

        with col_calc1:

            st.markdown(f"""

            <div style='background:#0f3460;border-radius:12px;padding:16px 20px;border:1px solid #22c55e;'>

            <b style='color:#22c55e;font-size:15px;'>ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Resultado Real</b><br><br>

            <table style='width:100%;color:#f1f5f9;font-size:13px;'>

            <tr><td>Receita Bruta</td><td align='right'><b>R$ {receita_bruta:,.2f}</b></td></tr>

            <tr><td>(-) Despesas DedutÃÂÃÂ­veis</td><td align='right'><b>R$ {despesa_total:,.2f}</b></td></tr>

            <tr style='border-top:1px solid #22c55e;'><td><b>= Resultado LÃÂÃÂ­quido</b></td><td align='right'><b>R$ {resultado_liq:,.2f}</b></td></tr>

            <tr><td>Limite de isenÃÂÃÂ§ÃÂÃÂ£o</td><td align='right'>R$ {LIMITE_ISENCAO:,.2f}</td></tr>

            <tr><td>Base de cÃÂÃÂ¡lculo IR</td><td align='right'><b>R$ {BASE_CALCULO:,.2f}</b></td></tr>

            <tr><td>AlÃÂÃÂ­quota aplicada</td><td align='right'>{aliquota_efetiva*100:.1f}%</td></tr>

            <tr style='border-top:1px solid #22c55e;'><td><b>IR Devido (estimado)</b></td><td align='right'><b style='color:#f59e0b;'>R$ {ir_devido:,.2f}</b></td></tr>

            </table>

            </div>

            """, unsafe_allow_html=True)



        with col_calc2:

            st.markdown(f"""

            <div style='background:#0f3460;border-radius:12px;padding:16px 20px;border:1px solid #3b82f6;'>

            <b style='color:#3b82f6;font-size:15px;'>ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Resultado Presumido (20%)</b><br><br>

            <table style='width:100%;color:#f1f5f9;font-size:13px;'>

            <tr><td>Receita Bruta</td><td align='right'><b>R$ {receita_bruta:,.2f}</b></td></tr>

            <tr><td>Base presumida (20%)</td><td align='right'><b>R$ {resultado_pres:,.2f}</b></td></tr>

            <tr><td colspan='2' style='color:#94a3b8;font-size:11px;padding-top:6px;'>

            OpÃÂÃÂ§ÃÂÃÂ£o pelo resultado presumido ÃÂÃÂ© vÃÂÃÂ¡lida quando a receita bruta anual nÃÂÃÂ£o ultrapassar R$ 130.000,00 (art. 4ÃÂÃÂº Lei 8.023/90).

            </td></tr>

            </table>

            </div>

            """, unsafe_allow_html=True)



        st.divider()



        # SituaÃÂÃÂ§ÃÂÃÂ£o fiscal

        if receita_bruta == 0:

            st.info("ÃÂ¢Ã¢ÂÂÃÂ¹ÃÂ¯ÃÂ¸ÃÂ Preencha as receitas na aba anterior para calcular.")

        elif resultado_liq <= 0:

            st.success("ÃÂ¢ÃÂÃ¢ÂÂ¦ Resultado negativo (prejuÃÂÃÂ­zo) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o hÃÂÃÂ¡ IR a pagar. O prejuÃÂÃÂ­zo pode ser compensado nos prÃÂÃÂ³ximos anos.")

        elif BASE_CALCULO <= LIMITE_ISENCAO:

            st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ Resultado abaixo do limite de isenÃÂÃÂ§ÃÂÃÂ£o (R$ {LIMITE_ISENCAO:,.2f}) ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ nÃÂÃÂ£o hÃÂÃÂ¡ IR a pagar.")

        else:

            st.warning(f"ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ IR estimado: **R$ {ir_devido:,.2f}** ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ consulte seu contador para a declaraÃÂÃÂ§ÃÂÃÂ£o oficial.")



        st.markdown("""

        <div style='background:#1e293b;border-radius:8px;padding:10px 14px;margin-top:12px;border-left:3px solid #f59e0b;'>

        <span style='color:#fbbf24;font-size:12px;'>ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ <b>Aviso legal:</b> Este cÃÂÃÂ¡lculo ÃÂÃÂ© uma estimativa para fins de planejamento.

        A declaraÃÂÃÂ§ÃÂÃÂ£o oficial deve ser feita por contador habilitado com base nos documentos fiscais originais.</span>

        </div>

        """, unsafe_allow_html=True)



    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    # TAB 3 ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ GERAR RELATÃÂÃ¢ÂÂRIO PDF

    # ÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂÃÂ¢Ã¢ÂÂ¢ÃÂ

    with tab_ir3:

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ RelatÃÂÃÂ³rio para o Contador")

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



        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Gerar PDF do RelatÃÂÃÂ³rio", use_container_width=True, key="btn_gerar_ir_pdf"):

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



                # CabeÃÂÃÂ§alho

                story.append(Paragraph("IAAGRO ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ INTELIGÃÂÃÂ NCIA AGRÃÂÃÂCOLA", s_title))

                story.append(Paragraph("RelatÃÂÃÂ³rio de ApuraÃÂÃÂ§ÃÂÃÂ£o do Imposto de Renda ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Atividade Rural", s_sub))

                story.append(Paragraph(f"Ano-CalendÃÂÃÂ¡rio: {st.session_state.ir_ano} | Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", s_aviso))

                story.append(HRFlowable(width="100%", thickness=2, color=VERDE, spaceAfter=10))



                # Dados do produtor

                story.append(Paragraph("1. IDENTIFICAÃÂÃ¢ÂÂ¡ÃÂÃÂO DO CONTRIBUINTE", s_sec))

                dados_prod = [

                    ["Nome completo:", st.session_state.ir_nome or "ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"],

                    ["CPF:", st.session_state.ir_cpf or "ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"],

                    ["Cidade/UF:", st.session_state.ir_cidade or "ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ"],

                    ["ÃÂÃÂrea total declarada:", f"{st.session_state.ir_area_total:.2f} ha"],

                    ["Atividade:", "Produtor Rural ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Pessoa FÃÂÃÂ­sica"],

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

                    "venda_graos":     "Venda de grÃÂÃÂ£os e cereais",

                    "venda_animais":   "Venda de animais e produtos pecuÃÂÃÂ¡rios",

                    "arrendamento":    "Arrendamento recebido",

                    "subvencoes":      "SubvenÃÂÃÂ§ÃÂÃÂµes e incentivos governamentais",

                    "indenizacoes":    "IndenizaÃÂÃÂ§ÃÂÃÂµes de seguro agrÃÂÃÂ­cola",

                    "outras_receitas": "Outras receitas rurais",

                }

                rows_rec = [["DescriÃÂÃÂ§ÃÂÃÂ£o", "Valor (R$)"]]

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

                story.append(Paragraph("3. DESPESAS DEDUTÃÂÃÂVEIS (art. 61 RIR/2018)", s_sec))

                desp_labels = {

                    "sementes":        "Sementes e mudas",

                    "fertilizantes":   "Fertilizantes e defensivos agrÃÂÃÂ­colas",

                    "mao_de_obra":     "MÃÂÃÂ£o de obra (salÃÂÃÂ¡rios + encargos sociais)",

                    "combustivel":     "CombustÃÂÃÂ­vel e lubrificantes",

                    "energia":         "Energia elÃÂÃÂ©trica rural",

                    "arrendamento_pg": "Arrendamento pago",

                    "manutencao":      "ManutenÃÂÃÂ§ÃÂÃÂ£o de mÃÂÃÂ¡quinas e benfeitorias",

                    "depreciacao":     "DepreciaÃÂÃÂ§ÃÂÃÂ£o de bens do ativo imobilizado",

                    "frete":           "Fretes e carretos",

                    "seguro":          "Seguros rurais",

                    "assistencia_tec": "AssistÃÂÃÂªncia tÃÂÃÂ©cnica e agronÃÂÃÂ´mica",

                    "juros":           "Juros de financiamentos rurais",

                    "outras_despesas": "Outras despesas dedutÃÂÃÂ­veis",

                }

                rows_desp = [["DescriÃÂÃÂ§ÃÂÃÂ£o", "Valor (R$)"]]

                for k, label in desp_labels.items():

                    val = st.session_state.ir_despesas.get(k, 0.0)

                    if val > 0:

                        rows_desp.append([label, f"R$ {val:,.2f}"])

                rows_desp.append(["TOTAL DESPESAS DEDUTÃÂÃÂVEIS", f"R$ {despesa_total:,.2f}"])



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



                # ApuraÃÂÃÂ§ÃÂÃÂ£o IR

                story.append(Paragraph("4. APURAÃÂÃ¢ÂÂ¡ÃÂÃÂO DO IMPOSTO DE RENDA", s_sec))

                sit = "NÃÂÃÂ£o hÃÂÃÂ¡ IR a pagar (resultado negativo ou abaixo do limite de isenÃÂÃÂ§ÃÂÃÂ£o)" if ir_devido == 0 else f"IR estimado devido: R$ {ir_devido:,.2f}"

                rows_ir = [

                    ["DescriÃÂÃÂ§ÃÂÃÂ£o", "Valor (R$)"],

                    ["Receita Bruta Total",                  f"R$ {receita_bruta:,.2f}"],

                    ["(-) Despesas DedutÃÂÃÂ­veis",               f"R$ {despesa_total:,.2f}"],

                    ["= Resultado LÃÂÃÂ­quido da Atividade Rural",f"R$ {resultado_liq:,.2f}"],

                    ["Limite de isenÃÂÃÂ§ÃÂÃÂ£o (ano-calendÃÂÃÂ¡rio)",    f"R$ {LIMITE_ISENCAO:,.2f}"],

                    ["Base de CÃÂÃÂ¡lculo do IR",                 f"R$ {BASE_CALCULO:,.2f}"],

                    ["AlÃÂÃÂ­quota aplicada (tabela progressiva)",f"{aliquota_ef*100:.1f}%"],

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



                # ProduÃÂÃÂ§ÃÂÃÂ£o (se preenchida)

                prod_preench = {k:v for k,v in st.session_state.ir_producao.items() if v > 0}

                if prod_preench:

                    story.append(Paragraph("5. MEMORIAL DESCRITIVO ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ PRODUÃÂÃ¢ÂÂ¡ÃÂÃÂO", s_sec))

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



                # RodapÃÂÃÂ© / aviso legal

                story.append(HRFlowable(width="100%", thickness=1, color=CINZA, spaceAfter=6))

                story.append(Paragraph(

                    "ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Este relatÃÂÃÂ³rio ÃÂÃÂ© um auxÃÂÃÂ­lio ao planejamento tributÃÂÃÂ¡rio gerado pelo sistema IAAGRO. "

                    "NÃÂÃÂ£o substitui a declaraÃÂÃÂ§ÃÂÃÂ£o oficial do IRPF nem a orientaÃÂÃÂ§ÃÂÃÂ£o de contador habilitado. "

                    "Base legal: Lei 8.023/1990, IN RFB 1.700/2017, Decreto 9.580/2018 (RIR/2018).",

                    s_aviso

                ))

                story.append(Spacer(1, 4))

                story.append(Paragraph(

                    f"Gerado por IAAGRO ÃÂ¢Ã¢ÂÂ¬ÃÂ¢ {datetime.now().strftime('%d/%m/%Y ÃÂÃÂ s %H:%M')} ÃÂ¢Ã¢ÂÂ¬ÃÂ¢ www.iaagro.com.br",

                    s_aviso

                ))



                doc.build(story)

                pdf_bytes = buffer.getvalue()



                nome_arq = f"IR_Rural_{st.session_state.ir_nome.replace(' ','_') or 'produtor'}_{st.session_state.ir_ano}.pdf"

                st.success("ÃÂ¢ÃÂÃ¢ÂÂ¦ RelatÃÂÃÂ³rio gerado com sucesso!")

                st.download_button(

                    label="ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Baixar RelatÃÂÃÂ³rio PDF",

                    data=pdf_bytes,

                    file_name=nome_arq,

                    mime="application/pdf",

                    use_container_width=True,

                    key="btn_download_ir_pdf"

                )



            except Exception as e:

                st.error(f"ÃÂ¢ÃÂÃÂ Erro ao gerar PDF: {e}")



        st.markdown("""

        <div style='background:#0f3460;border-radius:10px;padding:14px 18px;margin-top:16px;border:1px solid #22c55e;'>

        <b style='color:#22c55e;'>ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ O relatÃÂÃÂ³rio contÃÂÃÂ©m:</b>

        <ul style='color:#f1f5f9;font-size:13px;margin-top:8px;'>

        <li>IdentificaÃÂÃÂ§ÃÂÃÂ£o completa do produtor</li>

        <li>Demonstrativo de receitas por categoria</li>

        <li>Demonstrativo de despesas dedutÃÂÃÂ­veis (art. 61 RIR/2018)</li>

        <li>ApuraÃÂÃÂ§ÃÂÃÂ£o do IR com tabela progressiva 2025</li>

        <li>Memorial descritivo de produÃÂÃÂ§ÃÂÃÂ£o por cultura</li>

        <li>Base legal completa para o contador</li>

        </ul>

        </div>

        """, unsafe_allow_html=True)



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

elif menu == "ÃÂ¢ÃÂ¡Ã¢ÂÂ¢ÃÂ¯ÃÂ¸ÃÂ ConfiguraÃÂÃÂ§ÃÂÃÂµes":

    st.header("ÃÂ¢ÃÂ¡Ã¢ÂÂ¢ÃÂ¯ÃÂ¸ÃÂ ConfiguraÃÂÃÂ§ÃÂÃÂµes do Sistema")



    tab0, tab_planos, tab1, tab2, tab3, tab4 = st.tabs([

        "ÃÂ°ÃÂ¸ÃÂÃÂ¾ Meu Segmento",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ³ Planos & PreÃÂÃÂ§os",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Backup & Restore",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ§ Email & Alertas",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  HistÃÂÃÂ³rico do Solo",

        "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¤ Exportar Excel"

    ])



    with tab_planos:

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ³ Planos & PreÃÂÃÂ§os")

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

                atual_txt  = "&nbsp;ÃÂ¢ÃÂÃ¢ÂÂ¦ ATUAL" if is_atual else ""

                preco_txt  = "GrÃÂÃÂ¡tis" if preco == 0 else f"R$ {preco:.2f}/mÃÂÃÂªs"

                rec_html   = "".join(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ {r}<br>" for r in plano["recursos"])

                bloq_html  = "".join(f"ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ {r}<br>" for r in plano["bloqueados"])



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

                    # Cada plano tem seu prÃÂÃÂ³prio link

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

                        f"ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ³ Mensal ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ R$ {btn_preco:.2f}/mÃÂÃÂªs",

                        btn_lmes,

                        use_container_width=True

                    )

                    st.link_button(

                        f"ÃÂ°ÃÂ¸ÃÂÃ¢ÂÂ  Anual ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ R$ {btn_pano} (-15%)",

                        btn_lano,

                        use_container_width=True

                    )

                    st.caption("PIX ÃÂ¢Ã¢ÂÂ¬ÃÂ¢ CartÃÂÃÂ£o ÃÂ¢Ã¢ÂÂ¬ÃÂ¢ Boleto")

                elif is_atual:

                    st.markdown(f"""

                    <div style='background:{plano["borda"]}33;border-radius:8px;padding:10px;

                    text-align:center;margin-top:8px;color:{plano["borda"]};font-weight:700;'>

                    ÃÂ¢ÃÂÃ¢ÂÂ¦ Plano Ativo

                    </div>

                    """, unsafe_allow_html=True)



        st.divider()

        st.markdown("""

        <div style='background:#0f3460;border-radius:10px;padding:14px 18px;border:1px solid #3b82f6;'>

        <b style='color:#3b82f6;'>ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ³ Como ativar o Plano Pro ou Premium?</b><br>

        <span style='color:#f1f5f9;font-size:13px;'>

        1. Clique em <b>Mensal</b> ou <b>Anual</b> no plano desejado<br>

        2. VocÃÂÃÂª serÃÂÃÂ¡ redirecionado para o <b>Mercado Pago</b><br>

        3. Pague via PIX, cartÃÂÃÂ£o ou boleto<br>

        4. Seu plano ÃÂÃÂ© ativado <b>automaticamente</b> apÃÂÃÂ³s confirmaÃÂÃÂ§ÃÂÃÂ£o<br>

        5. FaÃÂÃÂ§a logout e login novamente para ver o novo plano

        </span>

        </div>

        """, unsafe_allow_html=True)



    with tab0:

        st.subheader("ÃÂ°ÃÂ¸ÃÂÃÂ¾ Alterar Segmento de AtuaÃÂÃÂ§ÃÂÃÂ£o")

        st.info(f"Segmento atual: **{st.session_state.segmento or 'NÃÂÃÂ£o definido'}**")

        SEGMENTOS_CFG = {

            "ÃÂ°ÃÂ¸ÃÂÃÂ¾ GrÃÂÃÂ£os":        "Soja, Milho, Trigo e outros cereais",

            "ÃÂ°ÃÂ¸ÃÂÃÂ¿ Horticultura": "HortaliÃÂÃÂ§as, verduras e legumes",

            "ÃÂ°ÃÂ¸ÃÂÃÂ½ Fruticultura": "Frutas tropicais, uva, cafÃÂÃÂ© e outras",

            "ÃÂ°ÃÂ¸ÃÂÃÂ² Silvicultura": "Eucalipto, Pinus e reflorestamento",

        }

        st.markdown("#### Selecione o novo segmento:")

        for seg, desc in SEGMENTOS_CFG.items():

            col_s1, col_s2 = st.columns([2, 5])

            with col_s1:

                if st.button(seg, key=f"cfg_seg_{seg}", use_container_width=True):

                    st.session_state.segmento = seg

                    salvar_dados_iaagro()

                    st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ Segmento alterado para **{seg}**!")

                    st.rerun()

            with col_s2:

                st.markdown(f"<div style='padding:10px 0;color:#94a3b8;font-size:13px;'>{desc}</div>", unsafe_allow_html=True)



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TAB 1: BACKUP & RESTORE ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    with tab1:

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Backup & RestauraÃÂÃÂ§ÃÂÃÂ£o de Dados")



        st.markdown('''<div style="background:#7f1d1d;color:#fff;padding:14px 18px;

        border-radius:10px;border-left:5px solid #ef4444;font-weight:700;margin:8px 0 16px 0;font-size:14px;">

        ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ <b>IMPORTANTE ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Antes de atualizar o app:</b><br>

        O Streamlit Cloud nÃÂÃÂ£o persiste arquivos entre deploys. Sempre faÃÂÃÂ§a backup

        antes de enviar uma atualizaÃÂÃÂ§ÃÂÃÂ£o via Git. ApÃÂÃÂ³s atualizar, restaure o backup para

        recuperar seus dados (usuÃÂÃÂ¡rios, estoque, ÃÂÃÂ¡reas, histÃÂÃÂ³rico).

        </div>''', unsafe_allow_html=True)



        # Auto-backup ao abrir a aba

        st.markdown("#### ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Fazer Backup Agora")

        st.markdown('''<div style="background:#0f3460;color:#93c5fd;padding:10px 14px;

        border-radius:8px;font-size:12px;font-weight:600;margin:4px 0 12px 0;">

        ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¡ Salve este arquivo no seu computador. Ele contÃÂÃÂ©m todos os seus dados:

        usuÃÂÃÂ¡rios, estoque, ÃÂÃÂ¡reas cadastradas, histÃÂÃÂ³rico, aplicaÃÂÃÂ§ÃÂÃÂµes e configuraÃÂÃÂ§ÃÂÃÂµes.

        </div>''', unsafe_allow_html=True)



        backup_data = gerar_backup()

        st.download_button(

            "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Baixar Backup Completo (.json)",

            data=backup_data,

            file_name=f"iaagro_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json",

            mime="application/json",

            use_container_width=True

        )



        st.divider()

        st.markdown("#### ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Restaurar Backup")

        st.markdown('''<div style="background:#78350f;color:#fff;padding:11px 14px;

        border-radius:8px;border-left:4px solid #f59e0b;font-weight:600;margin:4px 0 12px 0;font-size:13px;">

        ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ A restauraÃÂÃÂ§ÃÂÃÂ£o substitui TODOS os dados atuais. Use apÃÂÃÂ³s atualizar o app.

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

            # LÃÂÃÂª e armazena o conteÃÂÃÂºdo no session_state imediatamente

            conteudo_backup = arquivo_restore.read()

            st.session_state["_backup_conteudo"] = conteudo_backup

            st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ Arquivo **{arquivo_restore.name}** carregado ({len(conteudo_backup)//1024} KB)")



        if st.session_state.get("_backup_conteudo"):

            if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Restaurar Backup Agora", key="btn_restore", use_container_width=True, type="primary"):

                import io

                ok, msg = restaurar_backup(io.BytesIO(st.session_state["_backup_conteudo"]))

                if ok:

                    st.session_state["_backup_conteudo"] = None

                    st.success(f"ÃÂ¢ÃÂÃ¢ÂÂ¦ {msg}")

                    st.rerun()

                else:

                    st.error(f"ÃÂ¢ÃÂÃÂ {msg}")



        # Passo a passo

        st.divider()

        st.markdown("#### ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ¹ Passo a passo para atualizar sem perder dados")

        passos_bk = [

            ("1ÃÂ¯ÃÂ¸ÃÂÃÂ¢ÃÂÃÂ£", "Acesse ÃÂ¢ÃÂ¡Ã¢ÂÂ¢ÃÂ¯ÃÂ¸ÃÂ ConfiguraÃÂÃÂ§ÃÂÃÂµes ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ Backup & RestauraÃÂÃÂ§ÃÂÃÂ£o"),

            ("2ÃÂ¯ÃÂ¸ÃÂÃÂ¢ÃÂÃÂ£", "Clique em **ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Baixar Backup Completo** e salve no computador"),

            ("3ÃÂ¯ÃÂ¸ÃÂÃÂ¢ÃÂÃÂ£", "Atualize o app normalmente via Git (git add ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ commit ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ push)"),

            ("4ÃÂ¯ÃÂ¸ÃÂÃÂ¢ÃÂÃÂ£", "Aguarde o Streamlit Cloud reiniciar (1-2 minutos)"),

            ("5ÃÂ¯ÃÂ¸ÃÂÃÂ¢ÃÂÃÂ£", "Acesse o app ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ ÃÂ¢ÃÂ¡Ã¢ÂÂ¢ÃÂ¯ÃÂ¸ÃÂ ConfiguraÃÂÃÂ§ÃÂÃÂµes ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ Backup & RestauraÃÂÃÂ§ÃÂÃÂ£o"),

            ("6ÃÂ¯ÃÂ¸ÃÂÃÂ¢ÃÂÃÂ£", "FaÃÂÃÂ§a upload do arquivo backup e clique em **ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Restaurar**"),

            ("7ÃÂ¯ÃÂ¸ÃÂÃÂ¢ÃÂÃÂ£", "Todos os dados estarÃÂÃÂ£o de volta ÃÂ¢ÃÂÃ¢ÂÂ¦"),

        ]

        for num, desc in passos_bk:

            st.markdown(f'<div style="background:#0f3460;color:#f1f5f9;padding:8px 14px;'

                        f'border-radius:8px;margin:4px 0;font-size:13px;">'

                        f'<b>{num}</b> {desc}</div>', unsafe_allow_html=True)



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TAB 2: EMAIL & ALERTAS ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    with tab2:

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ§ ConfiguraÃÂÃÂ§ÃÂÃÂ£o de Email para Alertas")

        st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;

        border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">

        ÃÂ¢Ã¢ÂÂÃÂ¹ÃÂ¯ÃÂ¸ÃÂ Configure um email para receber alertas automÃÂÃÂ¡ticos quando o estoque estiver baixo.

        Use Gmail com senha de app (configuraÃÂÃÂ§ÃÂÃÂµes ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ seguranÃÂÃÂ§a ÃÂ¢Ã¢ÂÂ Ã¢ÂÂ senhas de app).

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

        cfg["ativo"] = st.checkbox("ÃÂ¢ÃÂÃ¢ÂÂ¦ Ativar alertas por email", value=cfg.get("ativo", False), key="chk___ativar_alerta_8829")



        col_a, col_b = st.columns(2)

        with col_a:

            if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¾ Salvar ConfiguraÃÂÃÂ§ÃÂÃÂµes de Email"):

                st.session_state.email_config = cfg

                st.markdown('''<div style="background:#14532d;color:#fff;padding:12px 18px;

                border-radius:10px;border-left:5px solid #22c55e;font-weight:600;">

                ÃÂ¢ÃÂÃ¢ÂÂ¦ ConfiguraÃÂÃÂ§ÃÂÃÂµes salvas!</div>''', unsafe_allow_html=True)

        with col_b:

            if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ§ Testar Envio de Email"):

                ok = enviar_email_alerta(

                    cfg.get("email_destino",""),

                    "ÃÂ¢ÃÂÃ¢ÂÂ¦ IAAgro Pro ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Teste de Email",

                    "<h2>ÃÂ¢ÃÂÃ¢ÂÂ¦ Email configurado com sucesso!</h2><p>VocÃÂÃÂª receberÃÂÃÂ¡ alertas de estoque aqui.</p>"

                )

                if ok:

                    st.markdown('''<div style="background:#14532d;color:#fff;padding:12px 18px;

                    border-radius:10px;border-left:5px solid #22c55e;font-weight:600;">

                    ÃÂ¢ÃÂÃ¢ÂÂ¦ Email de teste enviado com sucesso!</div>''', unsafe_allow_html=True)

                else:

                    st.markdown('''<div style="background:#7f1d1d;color:#fff;padding:12px 18px;

                    border-radius:10px;border-left:5px solid #ef4444;font-weight:600;">

                    ÃÂ¢ÃÂÃÂ Falha ao enviar. Verifique as configuraÃÂÃÂ§ÃÂÃÂµes.</div>''', unsafe_allow_html=True)



        if cfg.get("ativo"):

            st.divider()

            if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃ¢ÂÂ Verificar Alertas de Estoque Agora"):

                checar_alertas_estoque()

                st.markdown('''<div style="background:#14532d;color:#fff;padding:12px 18px;

                border-radius:10px;border-left:5px solid #22c55e;font-weight:600;">

                ÃÂ¢ÃÂÃ¢ÂÂ¦ VerificaÃÂÃÂ§ÃÂÃÂ£o concluÃÂÃÂ­da!</div>''', unsafe_allow_html=True)



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TAB 3: HISTÃÂÃ¢ÂÂRICO DO SOLO ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    with tab3:

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  EvoluÃÂÃÂ§ÃÂÃÂ£o da Fertilidade do Solo")

        if not st.session_state.areas:

            st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;

            border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;">

            ÃÂ¢Ã¢ÂÂÃÂ¹ÃÂ¯ÃÂ¸ÃÂ Cadastre e analise ÃÂÃÂ¡reas para ver o histÃÂÃÂ³rico.</div>''', unsafe_allow_html=True)

        else:

            opcoes_area = [f"{a['ID']} - {a['TalhÃÂÃÂ£o']}" for a in st.session_state.areas]

            area_hist   = st.selectbox("Selecione a ÃÂÃÂ¡rea", opcoes_area, key="hist_solo_area")

            id_area_sel = area_hist.split(" - ")[0]



            df_hist = carregar_historico_solo_db(id_area_sel)

            if df_hist.empty:

                st.markdown('''<div style="background:#78350f;color:#fff;padding:13px 18px;

                border-radius:10px;border-left:5px solid #f59e0b;font-weight:600;">

                ÃÂ¢ÃÂ¡ÃÂ ÃÂ¯ÃÂ¸ÃÂ Nenhuma anÃÂÃÂ¡lise salva no banco ainda. Salve uma anÃÂÃÂ¡lise na aba "AnÃÂÃÂ¡lise de Solo".</div>''',

                unsafe_allow_html=True)

            else:

                st.dataframe(df_hist[["data","ph","fosforo","potassio","materia_organica",

                                       "calcio","magnesio","nota","score","classe"]],

                             use_container_width=True)

                st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ EvoluÃÂÃÂ§ÃÂÃÂ£o do Score e Nota")

                col1, col2 = st.columns(2)

                with col1:

                    st.line_chart(df_hist.set_index("data")[["score","nota"]])

                with col2:

                    st.line_chart(df_hist.set_index("data")[["ph","fosforo","potassio"]])



    # ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ TAB 4: EXPORTAR EXCEL ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

    with tab4:

        st.subheader("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¤ Exportar Dados para Excel")

        st.markdown('''<div style="background:#1e3a5f;color:#fff;padding:13px 18px;

        border-radius:10px;border-left:5px solid #3b82f6;font-weight:600;margin:8px 0;">

        ÃÂ¢Ã¢ÂÂÃÂ¹ÃÂ¯ÃÂ¸ÃÂ Gera um arquivo Excel com mÃÂÃÂºltiplas abas contendo todos os dados do sistema.

        </div>''', unsafe_allow_html=True)



        if st.button("ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ  Gerar RelatÃÂÃÂ³rio Excel Completo"):

            dados_export = {

                "ÃÂÃÂreas":     st.session_state.areas,

                "Estoque":   st.session_state.estoque,

                "AplicaÃÂÃÂ§ÃÂÃÂµes":[

                    {**{k:v for k,v in ap.items() if k != "Produtos"},

                     "Produtos": str(ap.get("Produtos",[]))}

                    for ap in st.session_state.aplicacoes

                ],

                "Hist Produt": st.session_state.historico_produtividade,

                "PluviÃÂÃÂ´metro": st.session_state.pluviometro,

                "AnÃÂÃÂ¡lise Solo":[st.session_state.dados] if st.session_state.dados else []

            }

            xlsx = exportar_excel(dados_export)

            if xlsx:

                st.download_button(

                    "ÃÂ°ÃÂ¸Ã¢ÂÂÃÂ¥ Baixar Excel Completo",

                    data=xlsx,

                    file_name=f"iaagro_relatorio_{date.today()}.xlsx",

                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                    use_container_width=True

                )



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ PWA ÃÂ¢Ã¢ÂÂ¬Ã¢ÂÂ Progressive Web App (instalÃÂÃÂ¡vel no Android/iOS) ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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



# ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ Persiste token no sessionStorage para sobreviver reload ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬ÃÂ¢Ã¢ÂÂÃ¢ÂÂ¬

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



