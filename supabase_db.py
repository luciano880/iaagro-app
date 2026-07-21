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
    """Autentica usuário e retorna token + refresh_token + user_id."""
    r = requests.post(
        f"{url}/auth/v1/token?grant_type=password",
        headers={"apikey": api_key, "Content-Type": "application/json"},
        json={"email": email, "password": senha},
        timeout=10
    )
    data = r.json()
    if "access_token" in data:
        return {
            "ok":            True,
            "token":         data["access_token"],
            "refresh_token": data.get("refresh_token", ""),
            "user_id":       data["user"]["id"],
            "email":         data["user"]["email"],
            "nome":          data["user"].get("user_metadata", {}).get("nome", email),
        }
    return {"ok": False, "erro": data.get("error_description", "Falha no login")}


def sb_refresh(url, api_key, refresh_token):
    """Renova o access_token usando o refresh_token."""
    try:
        r = requests.post(
            f"{url}/auth/v1/token?grant_type=refresh_token",
            headers={"apikey": api_key, "Content-Type": "application/json"},
            json={"refresh_token": refresh_token},
            timeout=10
        )
        data = r.json()
        if "access_token" in data:
            return {
                "ok":            True,
                "token":         data["access_token"],
                "refresh_token": data.get("refresh_token", refresh_token),
            }
    except Exception:
        pass
    return {"ok": False}


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
            "fluxo_caixa":             json.loads(row.get("fluxo_caixa", "[]")),
            "contratos_troca":         json.loads(row.get("contratos_troca", "[]")),
            "corretivos_aplicados":    json.loads(row.get("corretivos_aplicados", "[]")),
            "planejamento_safras":     json.loads(row.get("planejamento_safras", "[]")),
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
        "fluxo_caixa":             json.dumps(session.get("fluxo_caixa", []), ensure_ascii=False),
        "contratos_troca":         json.dumps(session.get("contratos_troca", []), ensure_ascii=False),
        "corretivos_aplicados":    json.dumps(session.get("corretivos_aplicados", []), ensure_ascii=False),
        "planejamento_safras":     json.dumps(session.get("planejamento_safras", []), ensure_ascii=False),
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


def sb_plano(url, api_key, token, user_id, debug=False):
    """
    Retorna o plano do usuário usando token JWT.

    Corrigido: a comparação de data agora normaliza o timezone. O Postgres pode
    devolver a data em vários formatos ("...+00", "...+00:00", "...Z" ou sem
    timezone nenhum), e o código antigo só tratava dois deles — o formato "+00"
    passava batido e quebrava a comparação com TypeError
    ("can't compare offset-naive and offset-aware datetimes").

    Passe debug=True para receber (plano, motivo) e enxergar onde está falhando.
    """
    from datetime import datetime, timezone

    def _resultado(plano, motivo):
        return (plano, motivo) if debug else plano

    headers = {
        "apikey":        api_key,
        "Authorization": f"Bearer {token}",   # token JWT do usuário logado
        "Content-Type":  "application/json",
    }
    try:
        r = requests.get(
            f"{url}/rest/v1/iaagro_planos?user_id=eq.{user_id}&select=plano,valido_ate",
            headers=headers,
            timeout=8
        )
        if r.status_code != 200:
            return _resultado("free", f"HTTP {r.status_code}: {r.text[:200]}")

        rows = r.json()
        if not rows or not isinstance(rows, list):
            # Vazio quase sempre = RLS bloqueando ou user_id sem linha na tabela
            return _resultado("free", "consulta retornou vazio (RLS ou sem registro)")

        row        = rows[0]
        plano      = row.get("plano", "free") or "free"
        valido_ate = row.get("valido_ate", "")

        if not valido_ate:
            # Sem data de validade = plano sem expiração
            return _resultado(plano, "sem valido_ate; plano liberado")

        try:
            txt = str(valido_ate).strip().replace(" ", "T")
            if txt.endswith("Z"):
                txt = txt[:-1] + "+00:00"
            # Normaliza offsets curtos: "+00" -> "+00:00", "-03" -> "-03:00"
            import re as _re
            txt = _re.sub(r"([+-]\d{2})$", r"\1:00", txt)

            venc = datetime.fromisoformat(txt)
            # Compara sempre no mesmo "mundo": aware com aware, naive com naive
            agora = datetime.now(timezone.utc) if venc.tzinfo else datetime.now()

            if venc > agora:
                return _resultado(plano, f"válido até {venc.isoformat()}")
            return _resultado("free", f"plano '{plano}' expirou em {venc.isoformat()}")
        except Exception as e:
            # Data ilegível: não é motivo pra punir o usuário que pagou
            return _resultado(plano, f"valido_ate ilegível ({valido_ate!r}: {e}); plano liberado")

    except Exception as e:
        return _resultado("free", f"erro de conexão: {e}")


