// Supabase Edge Function — webhook do Mercado Pago
// Ativa plano automaticamente quando pagamento é aprovado
// Deploy: supabase functions deploy mercadopago-webhook

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"

const SUPABASE_URL  = Deno.env.get("SUPABASE_URL")!
const SUPABASE_SK   = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
const MP_TOKEN      = Deno.env.get("MP_ACCESS_TOKEN")!

// Mapeia external_reference para plano IAAGRO
const PLANOS_MAP: Record<string, {plano: string, dias: number}> = {
  "iaagro_pro_mensal":     { plano: "pro",     dias: 30  },
  "iaagro_pro_anual":      { plano: "pro",     dias: 365 },
  "iaagro_premium_mensal": { plano: "premium", dias: 30  },
  "iaagro_premium_anual":  { plano: "premium", dias: 365 },
}

serve(async (req) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 })
  }

  try {
    const body = await req.json()
    console.log("Webhook MP recebido:", JSON.stringify(body))

    // Mercado Pago envia: { action: "payment.updated", data: { id: "123" } }
    if (body.action !== "payment.updated" && body.type !== "payment") {
      return new Response(JSON.stringify({ ok: true, msg: "Ignorado" }), { status: 200 })
    }

    const payment_id = body.data?.id
    if (!payment_id) {
      return new Response(JSON.stringify({ ok: false, msg: "Sem payment_id" }), { status: 400 })
    }

    // Busca detalhes do pagamento na API do Mercado Pago
    const mp_resp = await fetch(
      `https://api.mercadopago.com/v1/payments/${payment_id}`,
      { headers: { "Authorization": `Bearer ${MP_TOKEN}` } }
    )
    const payment = await mp_resp.json()
    console.log("Pagamento MP:", payment.status, payment.external_reference)

    // Só processa pagamentos aprovados
    if (payment.status !== "approved") {
      return new Response(JSON.stringify({ ok: true, msg: `Status: ${payment.status}` }), { status: 200 })
    }

    const email     = payment.payer?.email || ""
    const ext_ref   = payment.external_reference || "iaagro_pro_mensal"
    const plano_cfg = PLANOS_MAP[ext_ref] || { plano: "pro", dias: 30 }

    if (!email) {
      return new Response(JSON.stringify({ ok: false, msg: "Email não encontrado" }), { status: 400 })
    }

    console.log(`Ativando plano ${plano_cfg.plano} para ${email}`)

    // Conecta ao Supabase com service role
    const supabase = createClient(SUPABASE_URL, SUPABASE_SK)

    // Busca user_id pelo email
    const { data: users } = await supabase.auth.admin.listUsers()
    const user = users?.users?.find((u: any) => u.email === email)

    const valido_ate = new Date(Date.now() + plano_cfg.dias * 86400000).toISOString()

    if (!user) {
      // Salva como pendente — ativa quando criar conta
      await supabase.from("iaagro_planos_pendentes").insert({
        email, plano: plano_cfg.plano, valido_ate,
        pagamento: JSON.stringify(payment),
      })
      console.log(`Salvo como pendente para ${email}`)
      return new Response(JSON.stringify({ ok: true, msg: "Pendente" }), { status: 200 })
    }

    // Ativa o plano
    const { error } = await supabase.from("iaagro_planos").upsert({
      user_id: user.id, plano: plano_cfg.plano, valido_ate
    }, { onConflict: "user_id" })

    if (error) throw error

    console.log(`✅ Plano ${plano_cfg.plano} ativado para ${email}`)
    return new Response(JSON.stringify({ ok: true, plano: plano_cfg.plano, email }), { status: 200 })

  } catch (err) {
    console.error("Erro:", err)
    return new Response(JSON.stringify({ ok: false, erro: String(err) }), { status: 500 })
  }
})
