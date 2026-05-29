# Workflow — Decisões Automatizadas (Art. 20 LGPD)

> **Art. 20 LGPD.** Titular tem direito a solicitar **revisão** de decisões tomadas unicamente com base em tratamento automatizado de dados pessoais que afetem seus interesses (definição de perfil, crédito, comportamento, personalidade etc.).
>
> *"Sempre que solicitado, o controlador deverá fornecer informações claras e adequadas a respeito dos critérios e procedimentos utilizados."* (§1º)

---

## Quando Art. 20 incide

Quando há **decisão tomada unicamente por algoritmo** que afeta o titular:

| Caso típico | Aplica Art. 20? |
|---|---|
| Score de crédito que decide aprovação | **Sim** — afeta acesso financeiro |
| Triagem automática de currículo | **Sim** — afeta oportunidade |
| Precificação dinâmica baseada em perfil individual | **Sim** — pode discriminar |
| Antifraude que bloqueia conta | **Sim** — afeta acesso |
| Recommendation engine sem efeito significativo | Não — recomenda mas não decide |
| Cálculo de imposto pela lei | Não — automatização de regra legal pública |
| Score que **apenas sugere** + humano decide | Não — não é "unicamente" automatizada (mas cuidado: humano que só carimba é fictício) |

**Teste**: se o titular fosse impactado negativamente, **ele teria como contestar a decisão de forma efetiva**? Se não, Art. 20.

---

## Obrigações do controlador

### Obrigação 1 — Direito à revisão (caput)
Mecanismo claro para solicitar revisão. Não pode ser apenas a mesma máquina reavaliando — precisa de **revisão humana ou alteração do critério algorítmico**.

> ⚠️ MP 869/2018 tentou trocar "revisão por pessoa natural" por "revisão" simples. O Congresso restaurou o direito implícito a revisão humana via Lei 13.853/2019. Posição da ANPD e jurisprudência: **revisão humana é o padrão**.

### Obrigação 2 — Direito à explicação (§1º)
Fornecer "informações claras e adequadas a respeito dos critérios e procedimentos utilizados".

Não é o **código-fonte**, mas:
- **Lógica geral** do modelo (regras, variáveis usadas)
- **Categorias de dados** consideradas
- **Pesos relativos** (qualitativo, mesmo se modelo é black-box)
- **Resultados típicos** + impacto
- **Como contestar**

### Obrigação 3 — Auditoria por viés (§2º — alteração da Lei 13.853/2019)
Quando há recusa em fornecer informações sob alegação de **segredo comercial/industrial**, a ANPD pode realizar **auditoria** para verificar aspectos discriminatórios.

⇒ Não é desculpa para opacidade. Você deve estar pronto para auditoria.

---

## SLA

| Marco | Prazo |
|---|---|
| Resposta a pedido de revisão | **15 dias** (Art. 19) |
| Resposta a pedido de explicação | **15 dias** |
| Documentação interna do modelo (pronta antes do deploy) | Bloqueador |
| Re-auditoria de viés | Anual + a cada re-treinamento material |

---

## Passo 1 — Inventariar decisões automatizadas

Listar:
- Sistemas que tomam decisões automatizadas
- Para cada um:
  - Finalidade
  - Base legal (geralmente Art. 7 V, IX, ou consentimento)
  - Inputs (dados usados)
  - Output (tipo de decisão)
  - Efeito sobre o titular
  - Existe intervenção humana? Onde? É efetiva?
  - Logs de decisão guardados?

Cada um precisa ter [`DPIA`](dpia-ripd.md) próprio.

---

## Passo 2 — Documentar o modelo (Model Card)

Antes do deploy:

```yaml
modelo: kyc_risk_score_v3.2
finalidade: "Atribuir score de risco para abertura de conta PF"
controlador: "{{Empresa}}"
tipo: "ML (Gradient Boosting) + regras pós-processamento"
treinamento:
  dataset: "Base de KYC histórica + bureaus"
  periodo: "2021-2025"
  volume: "1.2M registros"
  data_subjects: "Brasileiros adultos"
inputs:
  - cpf
  - idade
  - renda_declarada
  - cidade
  - score_bureau_externo
  - tempo_de_relacionamento
  - histórico_inadimplência
inputs_proibidos_explicitamente: # protegidos
  - cor
  - religião
  - opinião_política
  - orientação_sexual
  - cep_isolado # proxy de raça/renda
output: "score 0-100 + decisão {aprova, revisa, recusa}"
threshold_revisao_humana: "score < 40 ou recusa direta"
metricas_fairness:
  - "demographic_parity_difference por sexo: medido trimestralmente"
  - "equal_opportunity_difference por cidade: medido trimestralmente"
  - "calibration: medido mensalmente"
auditoria:
  ultima: 2026-04-15
  proxima: 2026-10-15
  metodo: "Backtesting + audit externa anual"
logs_decisao_retencao: "5 anos"
revisao_humana_processo: "workflows/adm-decisions-art20.md#passo-4"
explicabilidade_canal: "dpo@empresa.com.br + form em /privacidade/decisao-automatizada"
```

---

## Passo 3 — Implementar logging de decisão

Para **cada decisão automatizada**, registrar:

```json
{
  "decision_id": "dec_abc123",
  "titular_id": "u_xyz",
  "model": "kyc_risk_score_v3.2",
  "model_version": "v3.2.1",
  "ts": "2026-05-28T14:30:00Z",
  "inputs_hash": "sha256:...",       // hash dos inputs (não os inputs em claro nos logs)
  "inputs_snapshot_ref": "s3://...", // snapshot armazenado separado (criptografado)
  "output": {"score": 28, "decision": "review"},
  "feature_importance": [             // top features que pesaram
    {"feature": "score_bureau_externo", "weight": 0.42},
    {"feature": "tempo_de_relacionamento", "weight": 0.18}
  ],
  "human_review_required": true,
  "human_reviewer": null,             // preenchido se humano revisa
  "human_decision": null,
  "appeal_status": "none"
}
```

Retenção mínima: **5 anos** (suportar revisão tardia e auditoria ANPD).

---

## Passo 4 — Processo de revisão (quando titular solicita)

### Recebimento
Mesmos canais do DSAR — ver [`workflows/dsar-direitos-titular.md`](dsar-direitos-titular.md).
Pedido normalmente vem como "quero revisar minha recusa" ou "por que fui bloqueado?".

### Passo 4.1 — Identificar a decisão
- Localizar `decision_id` pelo titular + janela temporal
- Recuperar snapshot dos inputs e output

### Passo 4.2 — Revisor humano qualificado
- **Não pode ser o mesmo modelo nem outro modelo automatizado**
- Pessoa treinada na regra de negócio
- Tem acesso ao input completo + contexto adicional do titular
- Tem **poder de overrule** efetivo

### Passo 4.3 — Decisão da revisão
- Manter decisão automatizada → justificar com clareza
- Reverter → executar reversão + comunicar
- Em ambos casos: gerar **documento de revisão** com fundamentos

### Passo 4.4 — Resposta ao titular
Conteúdo:
- Decisão original e fundamento (em linguagem clara)
- Resultado da revisão
- Se mantida: como contestar judicialmente / na ANPD
- Se revertida: confirmação da nova decisão + ação corretiva

Prazo: **15 dias**.

### Passo 4.5 — Evidência
```json
{
  "ts":"<>","event":"art20_review_completed",
  "decision_id":"dec_abc123",
  "outcome":"reversed",
  "reviewer":"<empregado_id>",
  "rationale":"<texto>",
  "hash_prev":"...","hash_self":"..."
}
```

---

## Passo 5 — Resposta a pedido de explicação (§1º)

Quando titular pede "como vocês decidem isso?", responder:

- **Quais dados** sobre você são usados (lista)
- **Para qual finalidade** (decisão de X)
- **Lógica geral** do modelo (sem entrar em IP)
- **Categorias de dados** mais determinantes (sem revelar pesos exatos se segredo industrial)
- **Como o modelo é auditado** (por quem, periodicidade)
- **Como contestar**

Template: [`templates/resposta-explicacao-art20.md`](../templates/resposta-explicacao-art20.md).

**Não** é resposta válida:
- "É confidencial"
- "É um algoritmo proprietário"
- "Decisão automática não pode ser explicada"

---

## Passo 6 — Auditoria contínua por viés

### Métricas a monitorar (escolher conforme caso)
- **Demographic parity**: taxa de aprovação igual entre grupos protegidos (sexo, idade, cidade)
- **Equal opportunity**: taxa de aprovação igual entre grupos **dado o mesmo merecimento**
- **Calibration**: scores significam o mesmo entre grupos
- **Disparate impact ratio** (regra 80%)

### Cadência
- Mensal: drift dos inputs (mudança de distribuição)
- Trimestral: métricas de fairness
- Anual: auditoria completa (externa preferencial)
- Re-treinamento: re-validar todas as métricas antes do deploy

### Se métrica violada
- Pausar uso do modelo
- Investigar causa (dataset enviesado? feature proxy? mudança populacional?)
- Re-treinar ou ajustar
- DPIA atualizado
- Comunicar internamente; se afetou decisões já tomadas → revisão proativa

---

## Casos especiais

### "Não é decisão automatizada, é só sugestão" (mas humano sempre carimba)
Se a taxa de override do humano é < 5%, a sugestão **é** a decisão na prática. Aplicar Art. 20.

### Modelos de terceiros (vendor)
- Você como controlador continua responsável
- DPA deve incluir: cooperação para responder Art. 20 + acesso a explicabilidade
- Se vendor recusa fornecer → trocar vendor

### Modelos de fundação / LLM (IA generativa)
- Se usado para decisão sobre titular → Art. 20 incide
- Explicabilidade é difícil — usar prompt + context window como rastreamento
- Documentar guardrails

### Decisão favorável ao titular
- Aplica-se Art. 20 também (titular pode querer entender por que foi aprovado por nenhum motivo aparente — fraud detection invertido)
- Mas baixo risco de litígio

### Crianças / adolescentes
- Decisões automatizadas sobre menores exigem padrão **mais alto** de cuidado
- Em dúvida — sempre revisão humana

---

## Métricas (KPI)

| Métrica | Meta |
|---|---|
| % de modelos com Model Card publicado | 100% |
| % de modelos com auditoria de fairness ativa | 100% |
| Tempo médio de resposta a pedido Art. 20 | < 10 dias |
| Taxa de overrule em revisão humana | Tracking (se 0%, revisão pode ser fictícia) |
| Drift detection coverage | 100% |
| Modelos com retenção de logs de decisão ≥ 5 anos | 100% |

---

## Referências legais

- **Art. 20** LGPD — direito à revisão
- Lei 13.853/2019 — restaurou §2º (auditoria por viés pela ANPD)
- Art. 5 III — definição de tratamento
- Art. 6 IX — princípio da não discriminação
- Princípio da transparência (Art. 6 VI)
- Princípio da responsabilização (Art. 6 X)

### Soft law e referências internacionais (úteis em fiscalização)
- ANPD — Guia de IA (quando publicado)
- OECD AI Principles
- EU AI Act (alguns casos de uso classificados como alto risco — sistemas de crédito, RH)
- NIST AI Risk Management Framework

---

## Anti-padrões

| ❌ Erro | ✅ Correto |
|---|---|
| Recusa explicação alegando "IP" | LGPD não permite — pode haver auditoria ANPD |
| Revisão pelo mesmo modelo | Revisão por humano qualificado |
| Revisão por humano que apenas confirma 100% | Não é revisão genuína |
| Modelo "caixa preta" sem documentação | Model Card obrigatório |
| Sem logs de decisão | Inviabiliza Art. 20; falha de prestação de contas |
| Métricas de fairness só no deploy, nunca depois | Monitoramento contínuo |
