# Workflow — DSAR (Direitos do Titular)

> **Pedido do titular nos termos do Art. 18 LGPD.** Prazo legal: **15 dias** (Art. 19 §1º).
> Este é um runbook, não checklist. Cada passo gera evidência em `evidence/log.jsonl`.

---

## Quando ativar

Sempre que titular (ou representante legal) exercer um dos direitos do Art. 18 LGPD via:

- Email para canal do DPO
- Formulário no site
- Pelo telefone / WhatsApp do atendimento (registrar imediatamente)
- Ofício/notificação extrajudicial
- Resposta a comunicação de incidente

Não importa o canal — todos viram tickets neste workflow.

---

## SLA

| Marco | Prazo a partir do recebimento |
|---|---|
| **Confirmação de recebimento** ao titular | Mesmo dia útil, máx. 48h |
| **Identificação do titular** (verificação) | 3 dias úteis |
| **Análise técnica + base legal** | 7 dias |
| **Resposta final ao titular** | **15 dias corridos** (Art. 19 §1º) |
| Prorrogação (se justificável) | Comunicar ao titular antes de vencer o prazo original |

---

## Passo 0 — Iniciar timer

```
[dsar] Iniciado em: {{ISO 8601 UTC}}
Deadline: {{+15 dias corridos}}
Ticket: DSAR-{{YYYYMMDD-NNNN}}
```

Registrar em `evidence/log.jsonl`:

```json
{"ts":"2026-05-28T14:30:00Z","event":"dsar_received","ticket":"DSAR-20260528-001","channel":"email","claimed_identity":"<email_titular>"}
```

---

## Passo 1 — Classificar o pedido

Identificar qual inciso do Art. 18 está sendo invocado. Pode ser combinado.

| Pedido típico | Inciso | Ação principal |
|---|---|---|
| "Quais dados meus vocês têm?" | II — Acesso | Export completo |
| "Apaguem meus dados" | VI — Eliminação | Verificar base legal + executar |
| "Corrijam minha informação" | III — Correção | Editar + audit log |
| "Quero meus dados em formato que dê pra exportar" | V — Portabilidade | JSON/CSV estruturado |
| "Não quero mais receber email" | IX — Revogação consentimento | Opt-out + propagar |
| "Com quem vocês compartilham?" | VII — Informação sobre uso compartilhado | Lista de operadores |
| "Não fui informado sobre X" | VIII — Informação sobre não-consentimento | Resposta + ajuste de política |
| "Quero revisão de decisão automatizada" | Art. 20 (não Art. 18) | Workflow [`adm-decisions-art20.md`](adm-decisions-art20.md) |

---

## Passo 2 — Verificar identidade do titular (3 dias úteis)

**Princípio**: identificação razoável, não onerosa (Art. 19 §3º).

Matriz de exigências por tipo de dado em jogo:

| Tipo de dado | Verificação mínima |
|---|---|
| Email + telefone (não sensível) | Email com cofre/confirmação |
| Dados financeiros (transações, score) | CPF + email cadastrado + selfie com documento OU vídeo |
| Dados de saúde / sensíveis | CPF + RG + selfie + comprovante de vínculo (cliente atual?) |
| Pedido via representante (advogado, pais) | Procuração + documento do representante + comprovação do vínculo |
| Menor de idade | Documento do menor + documento do responsável + comprovação de vínculo |
| Pessoa falecida (espólio) | Inventariante: termo + certidão de óbito + documento |

**Se a identificação for impossível**: responder informando que **o pedido foi recebido mas não pôde ser processado** sem prova de identidade. Não simplesmente ignorar.

Evidência:
```json
{"ts":"2026-05-29T09:15:00Z","event":"identity_verified","ticket":"DSAR-...","method":"cpf+selfie+vinculo_cliente_ativo"}
```

---

## Passo 3 — Localizar dados (7 dias)

Execute o script `scripts/python/data-discovery.py` apontando para sua infraestrutura (databases, S3, índices). Output: mapa de onde os dados do titular vivem.

```bash
cd scripts/python
python -m compliance_pro.data_discovery --identifier <cpf_ou_email> --target ./infra-config.yaml
```

Para pedidos manuais, consulta cada sistema:

- [ ] Base de produção (DB principal)
- [ ] Réplicas e read replicas
- [ ] Backups (verificar política de retenção)
- [ ] Data warehouse / lago de dados
- [ ] Sistema de email marketing (Mailchimp, Mailerlite, etc.)
- [ ] CRM
- [ ] Logs de aplicação (atenção: PII em logs é violação)
- [ ] Sistema de tickets/suporte
- [ ] Telefônica/WhatsApp (gravações, transcrições)
- [ ] Operadores e sub-operadores (acionar via DPA)

---

## Passo 4 — Análise jurídica de viabilidade

Para cada pedido, validar:

### Pedido de eliminação (VI)
- Há **outra base legal** que justifica manter? (Art. 16)
  - Obrigação legal (NF, KYC, etc.)
  - Estudo por órgão de pesquisa anonimizado
  - Uso exclusivo, anonimizado
- Se sim → eliminação parcial + explicar ao titular quais dados são mantidos e por que

### Pedido de portabilidade (V)
- Dados foram tratados com **consentimento ou execução de contrato**?
- Se sim → exportar em formato interoperável (JSON, CSV, XML)
- Se base legal diferente → portabilidade pode ser limitada/recusada com justificativa

### Pedido de correção (III)
- Validar veracidade da informação alegada antes de alterar

---

## Passo 5 — Executar

### Acesso (II)

Export em **dois formatos**:
1. **Humano-legível** — PDF estruturado com seções: identificação, dados cadastrais, dados transacionais, dados comportamentais, lista de compartilhamentos
2. **Machine-readable** — JSON/CSV para portabilidade

Inclui:
- Lista de finalidades de tratamento
- Lista de operadores que receberam os dados
- Período de retenção previsto

### Eliminação (VI)

```bash
# script propaga para todos os sistemas mapeados
python -m compliance_pro.data_disposal --identifier <id> --ticket DSAR-...
```

O script:
1. Soft-delete no DB principal (com timestamp)
2. Hard-delete após N dias (configurável, default 30) — para permitir reversão se houver erro
3. Propaga para operadores via API/email (DPA exige cooperação)
4. Gera **certidão de eliminação** com hash dos registros eliminados

**Sempre** preservar log de auditoria com hash do que foi eliminado (não o conteúdo). Pra demonstrar à ANPD que ocorreu.

### Correção (III)

Editar + manter histórico (`before`/`after`) em audit log.

### Portabilidade (V)

JSON estruturado em schema documentado (idealmente seguindo Data Transfer Project ou OpenAPI).

### Revogação (IX)

1. Marcar consent no `consent_ledger` como revogado
2. Propagar para todos os sistemas que dependiam daquele consentimento
3. **Cessar** o tratamento daquela finalidade
4. Manter consent histórico (revogação não apaga histórico do consentimento)

---

## Passo 6 — Responder ao titular

Use template: [`templates/resposta-dsar.md`](../templates/resposta-dsar.md).

Resposta deve conter:
- Confirmação do que foi feito
- Se algo foi negado: justificativa **com citação legal** (Art. X, inciso Y)
- Anexo do export (se aplicável)
- Contato para esclarecimentos adicionais
- Direito de reclamar à ANPD (canal: https://www.gov.br/anpd/pt-br/canais_atendimento/cidadao)

Enviar por canal que permita confirmação de entrega (email com leitura confirmada, AR de carta registrada se ofício).

---

## Passo 7 — Encerrar evidência

```json
{"ts":"2026-06-12T16:00:00Z","event":"dsar_closed","ticket":"DSAR-20260528-001","outcome":"fulfilled","action":"data_export+deletion","prev_hash":"<sha256_anterior>","hash":"<sha256_atual>"}
```

Manter ticket arquivado por **5 anos** (recomendação ANPD para histórico de exercício de direitos).

---

## Casos especiais

### Pedido de várias pessoas em uma só comunicação

Tratar como múltiplos tickets. Pode ser fraude (pedido em massa coordenado).

### Pedido manifestamente infundado ou excessivo (repetitivo)

LGPD não tem dispositivo explícito como GDPR Art. 12(5), mas Art. 19 §3º permite exigir comprovação razoável. Para pedidos repetidos sem novo fato:
- Responder informando que pedido idêntico foi atendido em DD/MM/AAAA
- Manter registro

### Conflito entre titulares (dado de A está no contrato de B)

Avaliar caso a caso. Geralmente compartilham titularidade do dado em razão do vínculo contratual. Notificar B antes de alterar.

### Pedido envolve dados de terceiros

(Ex: cliente pede acesso a thread de email, e o thread contém dados de outras pessoas)
- Redigir dados de terceiros antes de entregar
- Documentar a redação

---

## Métricas (KPI do DPO)

| Métrica | Meta |
|---|---|
| Taxa de resposta no prazo | 100% (<15 dias) |
| Tempo médio de resposta | < 7 dias |
| Volume mensal de DSARs | Tracking |
| % de pedidos atendidos integralmente | > 90% |
| % com prorrogação justificada | < 10% |
| Reclamações à ANPD pós-DSAR | 0 |

---

## Referências legais

- Art. 18 LGPD — direitos
- Art. 19 LGPD — prazo (15 dias) + condições de identificação
- Art. 8 §5º — revogação de consentimento
- Art. 16 — exceções à eliminação
- Princípio do livre acesso (Art. 6 IV)
- Princípio da qualidade dos dados (Art. 6 V)

---

## Quando escalar para humano

- Pedidos via ofício judicial → jurídico imediatamente
- Pedidos de figura pública / sensível → DPO + jurídico
- Eliminação de dados em sistema legado sem API → equipe de infra + DPO
- Pedido envolvendo investigação interna em curso → jurídico
