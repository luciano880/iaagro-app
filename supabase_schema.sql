CREATE TABLE IF NOT EXISTS iaagro_dados (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
    dados TEXT DEFAULT '{}',
    areas TEXT DEFAULT '[]',
    estoque TEXT DEFAULT '[]',
    aplicacoes TEXT DEFAULT '[]',
    historico_produtividade TEXT DEFAULT '[]',
    pluviometro TEXT DEFAULT '[]',
    carencia_registros TEXT DEFAULT '[]',
    dre_registros TEXT DEFAULT '[]',
    calendario_eventos TEXT DEFAULT '[]',
    harvest_historico TEXT DEFAULT '[]',
    receituarios TEXT DEFAULT '[]',
    safrinha_registros TEXT DEFAULT '[]',
    segmento TEXT DEFAULT NULL,
    atualizado_em TIMESTAMPTZ DEFAULT NOW(),
    criado_em TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS iaagro_planos (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
    plano TEXT DEFAULT 'free',
    valido_ate TIMESTAMPTZ DEFAULT NULL,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE iaagro_dados ENABLE ROW LEVEL SECURITY;
ALTER TABLE iaagro_planos ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Acesso proprio iaagro_dados" ON iaagro_dados USING (auth.uid() = user_id);
CREATE POLICY "Acesso proprio iaagro_planos" ON iaagro_planos USING (auth.uid() = user_id);
