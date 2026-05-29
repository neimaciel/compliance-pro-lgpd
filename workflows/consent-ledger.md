# Workflow — Consent Ledger (Gestão de Consentimento)

> **Art. 8 LGPD.** Consentimento como base legal exige **manifestação livre, informada, inequívoca e específica** para finalidades determinadas. Quando há mudança, **novo consentimento** (§6).

---

## Quando consentimento é a base legal correta

| Cenário | Use consentimento? |
|---|---|
| Marketing (newsletter, ofertas) | Sim |
| Cookies não essenciais (analytics, ads) | Sim |
| Compartilhamento com parceiros para marketing | Sim |
| Dados sensíveis para fim não obrigatório (Art. 11 I) | Sim (consentimento específico e destacado) |
| Execução de contrato (criar conta, pagar) | Não — use Art. 7, V |
| Cumprimento de obrigação legal (NF, KYC) | Não — use Art. 7, II |
| Proteção da vida | Não — use Art. 7, IV |
| Legítimo interesse para fraude / segurança | Não — use Art. 7, IX com LIA |

**Erro mais comum**: usar consentimento para tudo. Consentimento é **revogável a qualquer momento** (Art. 8 §5º), o que pode quebrar o serviço se foi a base errada.

---

## Requisitos do consentimento válido (Art. 8)

| Requisito | Como implementar |
|---|---|
| **Livre** | Não condicionar serviço a consentimento desnecessário (Art. 9 §1º) |
| **Informado** | Política clara, linguagem acessível, finalidade explícita |
| **Inequívoco** | Ação afirmativa — não pré-marcado, não inferido de inação |
| **Específico** | Por finalidade — granular, não "concordo com tudo" |
| **Destacado** (se cláusula contratual) | Tipograficamente evidente |
| **Comprovável** | Você guarda evidência de quando, como, em quê o titular consentiu |
| **Revogável** | Mecanismo fácil; revogação tão fácil quanto consentir |

Para **dados sensíveis** (Art. 11 I): consentimento **específico e destacado**.
Para **menores** (Art. 14): consentimento de pelo menos um responsável + transparência aos menores.

---

## Schema do consent ledger

Tabela append-only, imutável (cada update é nova linha — você não edita histórico).

```sql
CREATE TABLE consent_ledger (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  titular_id TEXT NOT NULL,              -- ID interno do titular
  titular_identifier TEXT NOT NULL,       -- email/cpf (criptografado se possível)
  finalidade TEXT NOT NULL,               -- chave única ('newsletter', 'cookies_analytics', etc.)
  finalidade_descricao TEXT NOT NULL,     -- texto humano apresentado ao titular
  base_legal TEXT NOT NULL,               -- 'art_8' (consentimento) ou outra
  status TEXT NOT NULL,                   -- 'granted' | 'revoked'
  granted_at TIMESTAMPTZ,
  revoked_at TIMESTAMPTZ,
  collection_method TEXT NOT NULL,        -- 'web_form_v1.2', 'consent_banner_v2', 'api', etc.
  collection_evidence JSONB NOT NULL,     -- { ip, user_agent, ts, form_version, screenshot_hash }
  policy_version TEXT NOT NULL,           -- 'privacy-policy-2026-03-01'
  ttl_review_at TIMESTAMPTZ,              -- quando reavaliar (renovar consent)
  parent_consent_id UUID,                 -- se este é update de outro (revogação de granted, novo após revogado)
  hash_prev TEXT,                         -- hash da linha anterior (chain)
  hash_self TEXT NOT NULL,                -- sha256(jsonb_canonical(esta linha))
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_consent_titular ON consent_ledger(titular_id);
CREATE INDEX idx_consent_finalidade_status ON consent_ledger(finalidade, status);
```

**Imutabilidade**: revogar consentimento = INSERT nova linha com `status='revoked'`, não UPDATE. Histórico preservado.

---

## Coleta de consentimento

### Princípios de UX
- **Não pré-marcar** checkboxes
- **Granular** — separar finalidades (marketing email ≠ marketing SMS ≠ compartilhamento parceiros)
- **Igualar peso visual** entre "Aceitar" e "Recusar"
- **Sem dark pattern** (não esconder "recusar" em link cinza minúsculo)
- **Acessível** — funciona com teclado, leitor de tela
- **Sem condicionamento ilícito** — "para usar o site, aceite todos os cookies" é abuso quando há cookies não-essenciais

### Cookies (Resolução iminente da ANPD + análise atual)

| Categoria | Base legal | Bloqueado até consent? |
|---|---|---|
| **Essenciais** (sessão, autenticação) | Art. 7 V (contrato) | Não — necessários |
| **Funcionais** (preferências) | Art. 7 V ou consent | Idealmente sim |
| **Analytics** (Google Analytics, etc.) | Consent | **Sim** — bloquear até opt-in |
| **Marketing/Ads** (Meta Pixel, etc.) | Consent | **Sim** — bloquear até opt-in |
| **Personalização** | Consent | Sim |

Use Consent Management Platform (CMP) que **bloqueia tags** até consent. Não basta "banner pra inglês ver".

Script de auditoria: `scripts/typescript/cookie-checker.ts`.

---

## Evidência por consentimento

Para cada consent registrado, guardar:

```json
{
  "titular_id": "u_abc123",
  "finalidade": "newsletter",
  "granted_at": "2026-05-28T14:30:00.000Z",
  "evidence": {
    "ip": "200.x.x.x",
    "user_agent": "Mozilla/5.0 ...",
    "form_version": "v2.1",
    "policy_version_shown": "2026-03-01",
    "checkbox_state_pre_submit": false,
    "explicit_action": "checkbox_checked",
    "session_id": "sess_xyz",
    "screenshot_hash": "sha256:..."
  }
}
```

`screenshot_hash` (opcional mas forte) — hash de screenshot do formulário no momento do submit, armazenado em object storage.

---

## Revogação

### Canais que devem oferecer revogação:
- Link "descadastrar" em **todo email** marketing (CAN-SPAM-style)
- Centro de preferências na conta logada
- Resposta a SMS com "PARE" / "SAIR"
- Canal do DPO
- Endpoint público com identificação

### Fluxo técnico:
1. Receber pedido de revogação
2. Validar titular (verificação proporcional ao impacto)
3. INSERT em consent_ledger com `status='revoked'`
4. **Propagar revogação** em até 24h para todos os sistemas afetados:
   - Marketing platform (Mailchimp, etc.)
   - CMP
   - CRM
   - Sistemas internos que usavam aquele consent
5. Confirmar ao titular
6. Auditar: o tratamento parou de fato? (não basta "marcar revogado")

### Quando revogação **não** apaga os dados:
- Se há outra base legal para reter (Art. 16) — explicar ao titular
- Histórico do próprio consent (Art. 16 IV — não usar mais, mas guardar prova)
- Backup com retenção até expirar (documentar)

---

## Renovação de consent (TTL)

Consent **não tem prazo legal de validade explícito**, mas:
- Mudança material em finalidade / operadores → **novo consent** (Art. 8 §6)
- Política de privacidade atualizada materialmente → **re-consent**
- Boas práticas: renovar a cada **24 meses** para tratamentos contínuos (recomendação ANPD em fiscalizações)

Implementação: `ttl_review_at` no schema. Quando expira, próxima interação dispara re-consent.

---

## Casos especiais

### Menor de idade (Art. 14)
- Crianças (até 12 anos): consentimento de **pelo menos um responsável** + sempre que possível, manifestação do menor
- Adolescentes (12-18 anos): podem consentir em situações de seu melhor interesse, mas tratamento depende de responsável em casos sensíveis
- **Verificar idade** antes — não pedir consentimento direto de criança em formulário aberto

### Consent transferido (M&A, sucessão)
- Aquisições mudam controlador → comunicar titulares e oferecer reconfirmação
- Não basta "concordou com a empresa A" → automaticamente válido para B

### Consent em chamada gravada / WhatsApp
- Gravação clara com manifestação afirmativa
- Hash da gravação + timestamp + transcrição arquivada

### Consent em contrato físico (papel)
- Escaneado + OCR + hash
- Cópia original arquivada por 5 anos mínimo

---

## Métricas

| Métrica | Meta |
|---|---|
| % de tratamentos com base "consent" com ledger | 100% |
| Tempo médio entre revogação e propagação | < 24h |
| Taxa de erro na propagação (sistemas órfãos) | 0% |
| % de consentimentos com evidência completa | 100% |
| Idade média do consent (em tratamentos contínuos) | < 24 meses |

---

## Validação contínua

Script: `scripts/typescript/consent-audit.ts`
- Verifica que todo tratamento marcado "consent" no ROPA tem entrada no ledger
- Detecta consents pre-marcados / coletados em condicionamento
- Verifica taxa de revogação por canal (canais com 0 revogações são suspeitos — pode estar quebrado)

---

## Referências legais

- Art. 5 XII — definição de consentimento
- **Art. 8** — consentimento (todos os parágrafos)
- Art. 9 — direito do titular à informação
- Art. 11 I — consentimento para sensíveis
- Art. 14 — menores
- Art. 16 IV — manutenção exclusiva para guarda de consent
- Princípio do consentimento (Art. 6 não cita explicitamente, mas decorre)

---

## Anti-padrões

| ❌ Erro | ✅ Correto |
|---|---|
| Checkbox pré-marcado "concordo" | Estado padrão = não-consentido |
| "Aceitar todos" em verde grande, "Configurar" em cinza pequeno | Igualdade visual |
| Revogação pede ligar em horário comercial / preencher 5 forms | Tão fácil quanto consentir |
| Bundle "marketing + analytics + compartilhamento" em 1 checkbox | Granular |
| Não bloquear tags até consent | CMP com bloqueio prévio |
| Re-pedir consent toda visita após revogação | Respeitar a decisão |
