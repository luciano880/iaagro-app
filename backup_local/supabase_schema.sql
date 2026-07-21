-- ================================================
-- IAAGRO — SQL para criar tabelas no Supabase
-- Execute no Supabase > SQL Editor
-- ================================================

-- 1. Tabela principal de dados por usuário
CREATE TABLE IF NOT EXISTS iaagro_dados (
    id                       BIGSERIAL PRIMARY KEY,
    user_id                  UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
    dados                    TEXT DEFAULT '{}',
    areas                    TEXT DEFAULT '[]',
    estoque                  TEXT DEFAULT '[]',
    aplicacoes               TEXT DEFAULT '[]',
    historico_produtividade  TEXT DEFAULT '[]',
    pluviometro              TEXT DEFAULT '[]',
    carencia_registros       TEXT DEFAULT '[]',
    dre_registros            TEXT DEFAULT '[]',
    calendario_eventos       TEXT DEFAULT '[]',
    harvest_historico        TEXT DEFAULT '[]',
    receituarios             TEXT DEFAULT '[]',
    safrinha_registros       TEXT DEFAULT '[]',
    segmento                 TEXT DEFAULT NULL,
    atualizado_em            TIMESTAMPTZ DEFAULT NOW(),
    criado_em                TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Tabela de planos
CREATE TABLE IF NOT EXISTS iaagro_planos (
    id          BIGSERIAL PRIMARY KEY,
    user_id     UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
    plano       TEXT DEFAULT 'free',   -- free | pro | coop
    valido_ate  TIMESTAMPTZ DEFAULT NULL,
    criado_em   TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Row Level Security — cada usuário só vê seus dados
ALTER TABLE iaagro_dados  ENABLE ROW LEVEL SECURITY;
ALTER TABLE iaagro_planos ENABLE ROW LEVEL SECURITY;

-- Política: usuário só acessa seus próprios dados
CREATE POLICY "Acesso proprio iaagro_dados"  ON iaagro_dados
    USING (auth.uid() = user_id);

CREATE POLICY "Acesso proprio iaagro_planos" ON iaagro_planos
    USING (auth.uid() = user_id);

-- 4. Índices
CREATE INDEX IF NOT EXISTS idx_iaagro_dados_user  ON iaagro_dados(user_id);
CREATE INDEX IF NOT EXISTS idx_iaagro_planos_user ON iaagro_planos(user_id);

-- ================================================
-- LIMITES DO PLANO FREE (via função)
-- ================================================
CREATE OR REPLACE FUNCTION get_limite_plano(p_user_id UUID, p_recurso TEXT)
RETURNS INTEGER AS $$
DECLARE
    v_plano TEXT;
BEGIN
    SELECT plano INTO v_plano FROM iaagro_planos WHERE user_id = p_user_id;
    v_plano := COALESCE(v_plano, 'free');

    IF p_recurso = 'areas' THEN
        RETURN CASE v_plano WHEN 'free' THEN 2 ELSE -1 END;  -- -1 = ilimitado
    ELSIF p_recurso = 'estoque' THEN
        RETURN CASE v_plano WHEN 'free' THEN 20 ELSE -1 END;
    ELSE
        RETURN CASE v_plano WHEN 'free' THEN 0 ELSE 1 END;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
