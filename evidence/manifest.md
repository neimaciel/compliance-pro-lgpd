# Evidence Manifest — Hash-Chained Append-Only Log

> Schema do log de evidência usado pela meta-skill. Garante **imutabilidade**, **ordenação** e **detecção de tampering**.
> Fundamento: princípio da prestação de contas (Art. 6 X LGPD) + audit-grade para fiscalização ANPD.

---

## Princípios

| Princípio | Implementação |
|---|---|
| **Imutabilidade** | Append-only. Update/delete proibido pelo storage. |
| **Integridade** | Hash SHA-256 de cada registro + cadeia (hash_prev → hash_self). |
| **Ordenação** | hash_prev força ordem. Reordenação quebra a cadeia. |
| **Detecção** | Verificação periódica via `audit-integrity verify` aponta tampering. |
| **Independência** | Storage separado dos sistemas operacionais (S3 com Object Lock, etc.). |
| **Ancoragem externa** | Hash diário ancorado em sistema imutável (S3, blockchain pública opcional). |

---

## Esquema do registro

Cada linha em `log.jsonl` é um registro JSON com:

```json
{
  "ts": "2026-05-28T14:30:00.000Z",
  "event": "dsar_received",
  "ticket": "DSAR-20260528-001",
  "actor": {
    "type": "user|system|dpo",
    "id": "...",
    "name": "..."
  },
  "subject": {
    "titular_id": "u_xyz",
    "type": "lead|customer|employee"
  },
  "details": {
    "...": "..."
  },
  "policy": {
    "ref": "workflows/dsar-direitos-titular.md",
    "version": "v1.0"
  },
  "hash_prev": "sha256_hex_of_previous_record_or_null_if_first",
  "hash_self": "sha256_hex_of_this_record_excluding_hash_self_field"
}
```

### Cálculo de hash

```python
import hashlib, json

def canonical_json(d: dict) -> str:
    return json.dumps(d, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

def compute_hash(record: dict, prev_hash: str | None) -> str:
    payload = {k: v for k, v in record.items() if k != "hash_self"}
    payload["hash_prev"] = prev_hash
    return hashlib.sha256(canonical_json(payload).encode()).hexdigest()
```

A canonicalização ordena chaves para que o hash seja determinístico independente da ordem de escrita.

---

## Tipos de evento padronizados

### Workflow DSAR
- `dsar_received`
- `identity_verified`
- `data_located`
- `dsar_decision`           (allow / partial / deny)
- `data_export_generated`
- `data_disposal_executed`
- `dsar_response_sent`
- `dsar_closed`

### Workflow Incidente
- `breach_detected`
- `containment_action`
- `breach_assessed`
- `breach_decision`         (notify / no_notify)
- `anpd_notified`           (preliminary / complementary / final)
- `titulares_notified`
- `breach_closed`

### Workflow Consent
- `consent_granted`
- `consent_revoked`
- `consent_renewal_due`
- `consent_propagation_completed`

### Workflow ROPA/DPIA
- `ropa_entry_created`
- `ropa_entry_updated`
- `dpia_started`
- `dpia_approved`
- `dpia_review_due`

### Workflow Retenção
- `retention_policy_applied`
- `data_purge_executed`
- `legal_hold_applied`
- `legal_hold_released`

### Decisão automatizada (Art. 20)
- `automated_decision_made`
- `art20_review_requested`
- `art20_review_completed`
- `model_audit_executed`

### Vendor / Operador
- `dpa_signed`
- `dpa_amended`
- `vendor_assessed`
- `sub_processor_added`
- `vendor_offboarded`

### Transferência internacional
- `tia_executed`
- `cross_border_transfer_started`
- `cross_border_transfer_reviewed`

---

## Storage

### Recomendado (produção)

```
evidence/
├── log.jsonl                 # append-only, atual (último ciclo)
├── log.2026-Q1.jsonl.gz      # rotacionado por trimestre
├── log.2026-Q2.jsonl.gz
├── anchors/                  # ancoragens externas
│   └── 2026-05-28.anchor.txt # hash_self do último registro do dia, ancorado em S3 Object Lock
└── manifest.md               # este arquivo
```

Para storage real:

| Camada | Tecnologia |
|---|---|
| Append-only file | local + sync para S3 Object Lock (governance retention) |
| Replicação | região secundária com replication |
| Backup | criptografado com KMS key separada |
| Acesso | restrito a DPO + Sec; meta-audit ativo |
| Retenção | mínimo 5 anos (regulatório) |

### Para testes / desenvolvimento

Local `evidence/log.jsonl` é suficiente. Usar `scripts/python` para verificar integridade.

---

## Operações

### Append

```bash
audit-integrity append \
  --file evidence/log.jsonl \
  --event '{"event":"dsar_received","ticket":"DSAR-20260528-001","actor":{"type":"system"}}'
```

### Verify

```bash
audit-integrity verify --file evidence/log.jsonl
```

Saída:
```
Records: 1342 | Errors: 0
CHAIN INTACT.
```

Se houver tampering:
```
Line 847: hash_self mismatch — expected a4b9…, got f1e2…
CHAIN BROKEN — evidence has been tampered or truncated.
```

### Verify periódico (cron diário)

```yaml
# .github/workflows/evidence-integrity.yml
on:
  schedule:
    - cron: "0 9 * * *"   # 9 AM UTC diariamente
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install compliance-pro-lgpd
      - run: audit-integrity verify --file evidence/log.jsonl
      - if: failure()
        run: |
          # Disparar alerta para DPO + Sec
          curl -X POST $SLACK_WEBHOOK -d '{"text":"Audit log integrity FAILED"}'
```

### Anchoring

Diariamente, hash do último registro é gravado em sistema imutável separado:

```bash
LAST_HASH=$(tail -n 1 evidence/log.jsonl | jq -r '.hash_self')
echo "$(date -u +%FT%TZ) $LAST_HASH" > evidence/anchors/$(date -u +%F).anchor.txt
aws s3 cp evidence/anchors/$(date -u +%F).anchor.txt \
  s3://my-evidence-bucket/anchors/ \
  --object-lock-mode GOVERNANCE \
  --object-lock-retain-until-date $(date -u -d '+5 years' +%FT%TZ)
```

A âncora cria um ponto de verdade externa: mesmo que alguém regrave o `log.jsonl` localmente, a divergência com a âncora prova que houve manipulação.

---

## Exemplo de uso em workflow real

DSAR de eliminação completo gera estes registros:

```jsonl
{"ts":"2026-05-28T14:30:00Z","event":"dsar_received","ticket":"DSAR-20260528-001","actor":{"type":"system","id":"webhook_form"},"subject":{"titular_id":"u_xyz","type":"customer"},"details":{"channel":"web_form","right":"eliminacao"},"policy":{"ref":"workflows/dsar-direitos-titular.md","version":"v1.0"},"hash_prev":"...","hash_self":"sha256_a"}
{"ts":"2026-05-28T16:15:00Z","event":"identity_verified","ticket":"DSAR-20260528-001","actor":{"type":"dpo","id":"dpo@empresa","name":"Nei Maciel"},"details":{"method":"cpf+selfie"},"policy":{"ref":"workflows/dsar-direitos-titular.md","version":"v1.0"},"hash_prev":"sha256_a","hash_self":"sha256_b"}
{"ts":"2026-05-29T10:00:00Z","event":"data_located","ticket":"DSAR-20260528-001","actor":{"type":"system","id":"data_discovery"},"details":{"systems":["users-db","crm","mailerlite"],"records_count":47},"policy":{"ref":"workflows/dsar-direitos-titular.md","version":"v1.0"},"hash_prev":"sha256_b","hash_self":"sha256_c"}
{"ts":"2026-05-30T11:30:00Z","event":"dsar_decision","ticket":"DSAR-20260528-001","actor":{"type":"dpo","id":"dpo@empresa"},"details":{"decision":"partial_grant","retained":["fiscal_2021_2025"],"rationale":"Art. 16, I LGPD c/c CTN Art. 174"},"policy":{"ref":"workflows/dsar-direitos-titular.md","version":"v1.0"},"hash_prev":"sha256_c","hash_self":"sha256_d"}
{"ts":"2026-05-30T14:00:00Z","event":"data_disposal_executed","ticket":"DSAR-20260528-001","actor":{"type":"system","id":"disposal_job"},"details":{"records_deleted":42,"records_retained":5,"systems_propagated":["users-db","crm","mailerlite"]},"policy":{"ref":"workflows/retention-disposal.md","version":"v1.0"},"hash_prev":"sha256_d","hash_self":"sha256_e"}
{"ts":"2026-05-30T15:00:00Z","event":"dsar_response_sent","ticket":"DSAR-20260528-001","actor":{"type":"dpo","id":"dpo@empresa"},"details":{"channel":"email","response_doc_hash":"sha256_..."},"policy":{"ref":"workflows/dsar-direitos-titular.md","version":"v1.0"},"hash_prev":"sha256_e","hash_self":"sha256_f"}
{"ts":"2026-05-30T15:01:00Z","event":"dsar_closed","ticket":"DSAR-20260528-001","actor":{"type":"system","id":"workflow_engine"},"details":{"sla_days":2,"sla_target_days":15,"compliant":true},"policy":{"ref":"workflows/dsar-direitos-titular.md","version":"v1.0"},"hash_prev":"sha256_f","hash_self":"sha256_g"}
```

Em fiscalização ANPD, este trecho prova:
- Quando o pedido chegou
- Quem verificou identidade
- Onde os dados foram localizados
- Decisão e fundamento legal
- Execução
- Resposta ao titular
- Cumprimento do prazo

E o hash chain prova que o log **não foi editado depois**.

---

## Retenção do próprio log

- Mínimo: **5 anos** (Res. CD/ANPD 4/2023 — prazo prescricional sanção)
- Recomendado: 7 anos (alinhamento com obrigações contábeis e fiscais)
- Logs de incidente: 5 anos pós-resolução
- Logs de DSAR: 5 anos pós-encerramento

Após o prazo, **anonimizar** (remover identificadores) mantendo apenas dados agregados para histórico.

---

## Privacidade do próprio log

O log de evidência é, ele mesmo, tratamento de dados pessoais. Aplicar:
- Acesso restrito (DPO + Sec)
- Criptografia at-rest
- Audit do acesso ao log (meta-audit)
- Inclusão no ROPA da organização
- Sujeito a DSAR (eliminação por mascaramento, não exclusão de registro inteiro)

---

## Referências

- Art. 6, X LGPD — princípio da responsabilização e prestação de contas
- Art. 37 — registro de operações
- Art. 50 — boas práticas e governança
- NIST SP 800-92 — Log Management
- ISO/IEC 27037 — Digital evidence
- Bitcoin whitepaper (Nakamoto, 2008) — hash chain proof-of-existence
