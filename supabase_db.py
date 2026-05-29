"""
IAAGRO — Módulo de integração com Supabase
Isola dados por user_id, suporta múltiplos usuários simultâneos
"""
import json
import hashlib
import requests
from datetime import datetime


def _headers(api_key: str, token: str = None):
    h = {
        "apikey":       api_key,
        "Content-Type": "application/json",
        "Prefer":       "return=representation",
    }
    if token:
        h["Authorization"] = f"Bearer {token}"
    else:
        h["Authorization"] = f"Bearer {api_key}"
    return h


# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────

def sb_signup(url, api_key, email, senha, nome):
    """Cria usuário no Supabase Auth."""
    r = requests.post(
        f"{url}/auth/v1/signup",
        headers={"apikey": api_key, "Content-Type": "application/json"},
        json={"email": email, "password": senha, "data": {"nome": nome}},
        timeout=10
    )
    return r.json()


def sb_login(url, api_key, email, senha):
    """Autentica usuário e retorna token + user_id."""
    r = requests.post(
        f"{url}/auth/v1/token?grant_type=password",
        headers={"apikey": api_key, "Content-Type": "application/json"},
        json={"email": email, "password": senha},
        timeout=10
    )
    data = r.json()
    if "access_token" in data:
        return {
            "ok":       True,
            "token":    data["access_token"],
            "user_id":  data["user"]["id"],
            "email":    data["user"]["email"],
            "nome":     data["user"].get("user_metadata", {}).get("nome", email),
        }
    return {"ok": False, "erro": data.get("error_description", "Falha no login")}


def sb_logout(url, api_key, token):
    requests.post(
        f"{url}/auth/v1/logout",
        headers=_headers(api_key, token),
        timeout=5
    )


def sb_reset_senha(url, api_key, email):
    APP_URL = "https://iaagro-app-kvrwxtkugla8pqe7dgqeue.streamlit.app"
    r = requests.post(
        f"{url}/auth/v1/recover",
        headers={"apikey": api_key, "Content-Type": "application/json"},
        json={"email": email, "redirect_to": APP_URL},
        timeout=10
    )
    return r.status_code == 200


# ─────────────────────────────────────────────
# DADOS POR USUÁRIO (tabela iaagro_dados)
# ─────────────────────────────────────────────

def sb_carregar(url, api_key, token, user_id):
    """Carrega todos os dados do usuário."""
    r = requests.get(
        f"{url}/rest/v1/iaagro_dados?user_id=eq.{user_id}&select=*",
        headers=_headers(api_key, token),
        timeout=10
    )
    rows = r.json()
    if rows and isinstance(rows, list):
        row = rows[0]
        return {
            "dados":                   json.loads(row.get("dados", "{}")),
            "areas":                   json.loads(row.get("areas", "[]")),
            "estoque":                 json.loads(row.get("estoque", "[]")),
            "aplicacoes":              json.loads(row.get("aplicacoes", "[]")),
            "historico_produtividade": json.loads(row.get("historico_produtividade", "[]")),
            "pluviometro":             json.loads(row.get("pluviometro", "[]")),
            "carencia_registros":      json.loads(row.get("carencia_registros", "[]")),
            "dre_registros":           json.loads(row.get("dre_registros", "[]")),
            "calendario_eventos":      json.loads(row.get("calendario_eventos", "[]")),
            "harvest_historico":       json.loads(row.get("harvest_historico", "[]")),
            "receituarios":            json.loads(row.get("receituarios", "[]")),
            "safrinha_registros":      json.loads(row.get("safrinha_registros", "[]")),
            "segmento":                row.get("segmento", None),
        }
    return None


def sb_salvar(url, api_key, token, user_id, session):
    """Salva/atualiza todos os dados do usuário."""
    payload = {
        "user_id":                 user_id,
        "dados":                   json.dumps(session.get("dados", {}), ensure_ascii=False),
        "areas":                   json.dumps(session.get("areas", []), ensure_ascii=False),
        "estoque":                 json.dumps(session.get("estoque", []), ensure_ascii=False),
        "aplicacoes":              json.dumps(session.get("aplicacoes", []), ensure_ascii=False),
        "historico_produtividade": json.dumps(session.get("historico_produtividade", []), ensure_ascii=False),
        "pluviometro":             json.dumps(session.get("pluviometro", []), ensure_ascii=False),
        "carencia_registros":      json.dumps(session.get("carencia_registros", []), ensure_ascii=False),
        "dre_registros":           json.dumps(session.get("dre_registros", []), ensure_ascii=False),
        "calendario_eventos":      json.dumps(session.get("calendario_eventos", []), ensure_ascii=False),
        "harvest_historico":       json.dumps(session.get("harvest_historico", []), ensure_ascii=False),
        "receituarios":            json.dumps(session.get("receituarios", []), ensure_ascii=False),
        "safrinha_registros":      json.dumps(session.get("safrinha_registros", []), ensure_ascii=False),
        "segmento":                session.get("segmento", None),
        "atualizado_em":           datetime.now().isoformat(),
    }
    headers_base = {
        "apikey":        api_key,
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
    }
    payload_update = {k: v for k, v in payload.items() if k != "user_id"}

    # 1. Tenta PATCH (update)
    r = requests.patch(
        f"{url}/rest/v1/iaagro_dados?user_id=eq.{user_id}",
        headers={**headers_base, "Prefer": "return=representation"},
        json=payload_update,
        timeout=15
    )
    if r.status_code == 200:
        # Verifica se realmente atualizou algo
        try:
            if r.json():  # retornou rows = atualizou
                return True
        except Exception:
            return True

    # 2. Se não atualizou, faz DELETE + INSERT limpo
    requests.delete(
        f"{url}/rest/v1/iaagro_dados?user_id=eq.{user_id}",
        headers=headers_base,
        timeout=10
    )
    r2 = requests.post(
        f"{url}/rest/v1/iaagro_dados",
        headers={**headers_base, "Prefer": "return=minimal"},
        json=payload,
        timeout=15
    )
    return r2.status_code in (200, 201, 204)


def sb_plano(url, api_key, token, user_id):
    """Retorna plano do usuário usando token JWT."""
    # Usa o token do usuário (JWT) para passar pelo RLS
    headers = {
        "apikey":        api_key,
        "Authorization": f"Bearer {token}",  # token JWT do usuário logado
        "Content-Type":  "application/json",
    }
    try:
        r = requests.get(
            f"{url}/rest/v1/iaagro_planos?user_id=eq.{user_id}&select=plano,valido_ate",
            headers=headers,
            timeout=8
        )
        if r.status_code == 200:
            rows = r.json()
            if rows and isinstance(rows, list):
                row = rows[0]
                valido_ate = row.get("valido_ate", "")
                if valido_ate:
                    try:
                        # Remove timezone info para comparar
                        vat = valido_ate.replace("Z","").replace("+00:00","")
                        if datetime.fromisoformat(vat) > datetime.now():
                            return row.get("plano", "free")
                    except Exception:
                        return row.get("plano", "free")
    except Exception:
        pass
    return "free"
