# Controle — Logging e Auditoria

> **Art. 37 (registro), Art. 46 (segurança), Art. 48 (incidente).**
> Sem audit log, não há prestação de contas (Art. 6 X) nem evidência para DSAR/breach/ANPD.

---

## O que precisa ser loggado

### Categoria A — Sempre (LGPD-critical)
- Acesso a PII (qualquer leitura — quem, quando, qual registro, finalidade declarada se sensível)
- Modificação de PII (campo, valor antes/depois)
- Eliminação de PII (com hash do conteúdo eliminado, não o conteúdo)
- Exercício de direito (Art. 18 — recebimento + cada ação)
- Decisões automatizadas (input_hash, output, modelo, versão)
- Concessão / revogação de acesso (RBAC mudanças)
- Eventos de consentimento (granted, revoked, ledger entry)
- Eventos de incidente (detecção, contenção, notificação)

### Categoria B — Segurança
- Autenticação (sucesso, falha, anomalia)
- Privilege escalation (sudo, role assumed, break-glass)
- Falhas de autorização (acesso negado)
- Mudanças em configuração crítica (firewall, IAM, KMS)
- Eventos de criptografia (chave criada/rotacionada/destruída)
- Job de eliminação automatizada (executado, escopo, volume)

### Categoria C — Operacional
- Deploys, mudanças de schema
- Acessos administrativos (sessões em bastion)
- Mudanças em DPA / contratos com operadores

### Não loggar (proibido)
- Senhas em claro (nem cifradas no log)
- Tokens / API keys completos (truncar / fingerprint)
- PII em logs de aplicação **a menos que seja log de auditoria explícito com retenção controlada**
- Dados sensíveis exceto via canal específico de audit

---

## Estrutura mínima de um log de auditoria

```json
{
  "ts": "2026-05-28T14:30:00.123Z",
  "event_id": "evt_abc123",
  "event_type": "pii.read",
  "actor": {
    "type": "user",
    "id": "u_xyz",
    "session_id": "sess_456",
    "ip": "200.x.x.x",
    "user_agent": "..."
  },
  "resource": {
    "type": "lead",
    "id": "lead_789",
    "tenant_id": "tenant_abc",
    "pii_fields_accessed": ["cpf", "telefone"]
  },
  "context": {
    "purpose_declared": "atendimento_ticket_TKT-123",
    "policy_evaluated": "OPA::pii.read::v2.34",
    "decision": "allow"
  },
  "hash_prev": "sha256:...",
  "hash_self": "sha256:..."
}
```

### Hash chain (append-only com integridade)

Cada log calcula `hash_self = sha256(canonical_json(this_record))` e referencia `hash_prev = hash_self` do anterior. Comprova:
- Imutabilidade — não dá pra apagar/alterar registro intermediário sem quebrar a chain
- Ordenação — não dá pra reordenar
- Detecção — alteração detectada na verificação

Cadência: âncora externa do hash atual em sistema imutável (write-once storage, blockchain pública opcional) — diariamente.

---

## Onde armazenar

### Princípios
- **Write-only** para a aplicação que gera (nunca update/delete em log)
- **Append-only** no storage (S3 object lock, banco com gatilho que rejeita update/delete)
- **Replicado** em região diferente
- **Criptografado at-rest** com chave separada da operação normal

### Opções
| Solução | Quando usar |
|---|---|
| AWS CloudTrail + S3 object lock | Eventos AWS |
| Loki / Elasticsearch + immutable index | Logs de aplicação |
| Postgres com gatilho `ON DELETE/UPDATE → RAISE` | DB-resident audit |
| Vault audit log | Eventos de KMS / secret access |
| SIEM (Splunk, Sentinel) | Correlação + alerting |

### Retenção
| Tipo | Mínimo | Recomendado |
|---|---|---|
| Logs de acesso (autenticação) | 6 meses (Marco Civil) | 12 meses |
| Logs de acesso a PII | 12 meses | 5 anos |
| Logs de acesso a PII sensível | 12 meses | 5 anos |
| Logs de DSAR (ticket completo) | 5 anos | 5 anos |
| Logs de incidente | 5 anos | 5 anos |
| Logs de decisão automatizada | 5 anos | 5 anos |
| Logs operacionais (debug) | 30-90 dias | 6 meses |

---

## Cuidados específicos LGPD

### PII em logs operacionais
**Sanitizar** antes de logar:
- Email → hash ou primeira letra + asterisco (`a***@dominio.com`)
- CPF → hash determinístico (HMAC-SHA-256 com chave em KMS)
- Telefone → últimos 4 dígitos
- IP → opcional truncar último octeto (debate de privacy vs forensics)

Padrão: SDK comum com sanitização **default**, exigindo opt-in explícito para logar valor.

### Logs como dado pessoal
Logs com PII são tratamento de dados pessoais → ROPA + retenção + DSAR.
Em pedido de eliminação (Art. 18 VI), considerar redação de logs (não eliminar o log, mas mascarar campos identificadores).

### Acesso aos logs também é tratamento
- Quem pode ler audit log? Times limitados (DPO, Sec)
- Logging do acesso ao log (meta-audit)
- Off-boarding revoga acesso ao SIEM

---

## Alerting

Não basta logar — **agir**. Eventos que devem disparar alertas:

| Evento | Quem alerta | Janela |
|---|---|---|
| Falhas de autenticação > N em janela curta | Sec | 5 min |
| Acesso a PII fora de janela típica (horário, IP, volume) | Sec + DPO | 15 min |
| Break-glass utilizado | Equipe inteira | Imediato |
| Permissão privilegiada concedida | Sec | 30 min |
| Job de eliminação falhou | DPO + Eng | 1h |
| Volume de DSAR anormalmente alto | DPO | 1h (pode ser ataque coordenado) |
| Acesso a logs de auditoria | Sec | 30 min |
| Decisão automatizada com fairness fora do threshold | DPO + Data | 1 dia |

---

## Evidência para ANPD

Em fiscalização ou pós-incidente, ANPD pode pedir:
- Log de quem acessou dados do titular X em janela Y
- Log de exercício de direitos
- Log de eliminação
- Log do que operador Y fez

Você deve conseguir gerar relatório em < 5 dias.

### Relatório padrão pós-DSAR
```yaml
ticket: DSAR-20260528-001
titular: u_xyz
escopo: "todos os acessos aos dados do titular nos últimos 12 meses"
total_acessos: 23
acessos_por_papel:
  - atendimento_l1: 18
  - dpo: 3
  - sistema_marketing: 2
detalhes: [array de eventos individuais]
hash_chain_verified: true
gerado_em: "2026-05-28T16:00:00Z"
```

---

## Anti-padrões

| ❌ Erro | ✅ Correto |
|---|---|
| Logs em arquivo local da máquina | Centralizado + replicado |
| Log de "DEBUG" com PII em produção | Sanitização SDK + nível controlado |
| Senha em log "para debugar problema" | Nunca; reproduzir local com dados fake |
| Log pode ser editado por admin do app | Write-only + hash chain |
| Sem retenção definida ("ficam pra sempre") | Política explícita por categoria |
| Sem alerting (só armazena) | Alertas em eventos críticos |
| Mesmo storage de logs e dados | Storage e KMS separados |
| Audit log dentro do banco da aplicação | Sistema dedicado (SIEM) |

---

## Scripts

- [`scripts/python/log-scanner.py`](../scripts/python/log-scanner.py) — detecta PII em logs operacionais
- [`scripts/python/audit-log-integrity.py`](../scripts/python/audit-log-integrity.py) — verifica hash chain

---

## Evidência

```yaml
sistema_audit:
  destino: "Splunk + AWS S3 com Object Lock"
  ingestion: "Fluentd → Kafka → Splunk + S3"
  formato: "OpenTelemetry + custom schema lgpd-v1"
  hash_chain: "habilitada (SHA-256, ancorada em S3 Object Lock diariamente)"
  encryption_at_rest: "AES-256 KMS key 'audit-prod' (separada da prod)"
retencao:
  acesso_autenticacao: "12 meses"
  acesso_pii: "5 anos"
  acesso_pii_sensivel: "5 anos"
  decisoes_automatizadas: "5 anos"
  dsar_tickets: "5 anos"
acesso_aos_logs:
  papeis_autorizados: ["dpo", "sec-lead", "compliance-officer"]
  meta_audit: "habilitada"
alerting:
  ferramenta: "Splunk ITSI"
  rules_count: 47
  ultima_revisao: "2026-04-15"
```

---

## Referências

- Art. 37, 46, 48 LGPD
- Princípio da prestação de contas (Art. 6 X)
- Marco Civil da Internet (Lei 12.965/14) — guarda de logs de conexão (6 meses) e aplicação (6 meses)
- NIST SP 800-92 (Computer Security Log Management)
- OWASP Logging Cheat Sheet
- ISO/IEC 27002:2022 — Section 8.15 (Logging)
