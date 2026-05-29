# Controle — Controle de Acesso (RBAC + ABAC)

> **Art. 46, 47, 49 LGPD.** Princípio do mínimo privilégio. Acesso a dados pessoais deve ser **necessário, granular, rastreável, revogável**.

---

## Princípios

| Princípio | Aplicação |
|---|---|
| **Least privilege** | Cada identidade tem só o que precisa para a função |
| **Need to know** | Acesso a PII justificado por tarefa específica |
| **Separation of duties** | Quem cria ≠ quem aprova ≠ quem audita |
| **Just-in-time (JIT)** | Permissões privilegiadas por tempo limitado |
| **Default deny** | Negar é o padrão; permitir é exceção justificada |
| **Audit everything** | Toda concessão e cada acesso loggado |

---

## Modelos

### RBAC (Role-Based Access Control)
Permissões agrupadas em **papéis** atribuídos a usuários.

```
Papel: "atendimento_l1"
Permissões:
  - leads.read (apenas do próprio tenant)
  - leads.update.status
  - tickets.read
  - tickets.create
Sem permissão para: dados.financeiros, exportar.massa, eliminar
```

**Pros:** simples, auditável.
**Cons:** explosão de papéis em grandes orgs (papel para cada exceção).

### ABAC (Attribute-Based Access Control)
Permissão computada de atributos (do usuário, recurso, contexto).

```
Permitir LER lead.cpf SE:
  - usuario.departamento = "atendimento" E
  - lead.tenant_id = usuario.tenant_id E
  - dia_da_semana ∈ [Seg..Sex] E
  - horario ∈ [08:00..20:00] BRT E
  - origem.ip ∈ "rede_corporativa"
```

**Pros:** flexível, expressivo.
**Cons:** difícil auditar; políticas viram código.

### Combinação típica
- RBAC como base + ABAC para casos sensíveis (financeiro, RH, sensíveis Art. 11)

---

## Camadas de defesa

### 1. Identidade (quem é)
- **SSO obrigatório** para colaboradores (SAML / OIDC)
- **MFA** obrigatório (TOTP, WebAuthn — não SMS)
- Diretório central (Okta, Azure AD, JumpCloud, Google Workspace)
- Off-boarding automatizado em ≤ 1h da saída

### 2. Autorização (o que pode)
- Política central versionada (OPA, Casbin)
- Avaliada no gateway / serviço, **não no cliente**
- Cache curto (< 5min) para refletir revogação rápida

### 3. Auditoria (o que fez)
- Log de **toda autenticação** (sucesso e falha)
- Log de **toda autorização negada** com motivo
- Log de **todo acesso a PII sensível** (quem, quando, qual registro, qual finalidade declarada)
- Retenção mínima: 12 meses; idealmente 5 anos para PII

### 4. Detecção (algo está errado)
- Alerta para acesso anômalo (volume, horário, geolocalização)
- Alerta para tentativa de privilege escalation
- Alerta para acesso fora de janela típica

---

## Acessos especiais

### Break-glass (emergência)
- Conta separada, sem uso rotineiro
- Requer aprovação dupla (2 humanos)
- Notifica equipe inteira ao ser usada
- Auditoria pós-uso obrigatória em 24h

### Acesso a dados sensíveis (Art. 11)
- Trilha de finalidade declarada (`X precisou ver Y para Z`)
- Aprovação prévia para acesso em massa
- Re-autenticação MFA antes do acesso

### Acesso a dados de menor (Art. 14)
- Restrito a equipe treinada
- Audit log com motivo
- Acesso revogado por padrão se inatividade > 90 dias

### Acesso de fornecedor / consultoria
- Conta nominal (não compartilhada)
- TTL curto (semanas, não meses)
- Restrição por IP / VPN
- DPA antes de qualquer acesso
- Revogação automática ao fim do contrato

### Acesso programático (API keys, service accounts)
- Sem permissão padrão de "admin"
- Escopo restrito (apenas as operações que o serviço executa)
- Rotação automática (≤ 90 dias)
- Vault para guardar (não em código, não em variável de ambiente sem secret manager)
- Audit log de uso

### Acesso a banco em produção (DBA, suporte de engenharia)
- **Bastion + audit obrigatório** — não psql direto via VPN
- JIT: solicitar acesso por janela curta (30min-2h)
- Sessão gravada
- Aprovação por outro engenheiro (4-eyes)

---

## Revisão periódica de acessos

| Frequência | O que revisar |
|---|---|
| Mensal | Acessos privilegiados (admin, root, DBA) |
| Trimestral | Acessos a sistemas com PII |
| Semestral | Todos os acessos / papéis |
| Imediato | Mudança de função (transferência interna) |
| Imediato | Off-boarding |

Processo:
1. Gerar relatório de quem tem acesso a quê
2. Cada gerente confirma necessidade
3. Sem confirmação em N dias → revogar automaticamente
4. Relatório vai para evidence/log

---

## Matriz de papéis típica (LGPD-aware)

| Papel | Acesso a PII | Pode exportar | Pode deletar | Pode ver Art. 11 sensíveis |
|---|---|---|---|---|
| `admin_global` | Total | Sim (com aprovação) | Sim (com aprovação) | Sim (com motivo + audit) |
| `dpo` | Total leitura | Sim (auditado) | Sim (Art. 18 VI) | Sim |
| `engenharia_prod` | Mínimo via bastion | Não em massa | Não | Não (mascarado em queries) |
| `suporte_l1` | Por ticket | Não | Não | Não |
| `suporte_l2` | Por ticket | Limitado | Solicita | Não |
| `analista_dados` | Pseudonimizado | Em formato anonimizado | Não | Não |
| `marketing` | Cadastrais agregados | Em formato consentido | Não | Não |
| `financeiro` | Financeiros + cadastrais | Por tarefa | Não | Não |
| `fornecedor_X` | Mínimo necessário, TTL | Não | Não | Não |

---

## Anti-padrões

| ❌ Erro | ✅ Correto |
|---|---|
| Conta "admin" compartilhada | Conta nominal + audit |
| MFA só "obrigatório" mas usuário pode desabilitar | Política força MFA + revoga sessão sem |
| Papel "superuser" para vários times | Granular por função |
| Permissão eterna ("vai precisar de novo") | TTL + JIT |
| Acesso direto ao banco em prod | Bastion / gateway |
| API key em código no Git | Secret manager + rotação |
| Sem audit log de acesso a PII sensível | Audit por padrão |
| Revisão "anual" só | Trimestral mínimo para PII |
| Off-boarding manual (esquece de revogar) | Automação SSO ⇄ HR system |

---

## Scripts de auditoria

- [`scripts/python/rbac-audit.py`](../scripts/python/rbac-audit.py) — exporta matriz quem-tem-acesso-a-quê
- [`scripts/typescript/iam-drift-check.ts`](../scripts/typescript/iam-drift-check.ts) — detecta drift entre IAM-as-code e estado real

---

## Evidência

```yaml
sistema: "users-db-prod"
modelo: "RBAC + ABAC"
identidade:
  provedor: "Okta"
  mfa: "obrigatório (TOTP + WebAuthn)"
politica:
  ferramenta: "OPA"
  repositorio: "gitlab.example.com/iam/policies"
  versao_atual: "v2.34"
acesso_a_pii_sensivel:
  controle: "ABAC + aprovação prévia + audit"
  ultima_revisao: "2026-04-01"
audit:
  destino: "SIEM (Splunk)"
  retencao: "12 meses (logs) + 5 anos (sensíveis)"
revisoes:
  ultima_global: "2026-03-15"
  ultima_privilegiada: "2026-05-15"
  proxima_global: "2026-09-15"
incidentes_relacionados: []
```

---

## Referências

- Art. 46-49 LGPD
- NIST SP 800-53 (Access Control family)
- NIST SP 800-162 (ABAC)
- ISO/IEC 27002:2022 — Section 5.15 (Access Control)
- CIS Controls v8 — Controls 5, 6, 16
- BCB Res. 4658/2018
