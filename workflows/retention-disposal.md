# Workflow — Retenção e Descarte de Dados

> **Art. 15, 16 LGPD.** Tratamento termina quando finalidade alcançada, dados deixam de ser necessários, fim do período de tratamento, comunicação do titular ou determinação da autoridade.
> Após o término, **eliminação** é a regra, salvo as exceções do Art. 16.

---

## Princípios

| Princípio | Aplicação prática |
|---|---|
| Finalidade (Art. 6 I) | Reter só enquanto a finalidade existir |
| Necessidade (Art. 6 III) | Mínimo necessário |
| Qualidade (Art. 6 V) | Dado desatualizado deve ser corrigido ou eliminado |

---

## Exceções à eliminação (Art. 16)

Dados podem ser mantidos **após** o fim do tratamento original se:

1. **Cumprimento de obrigação legal/regulatória** — citar a lei e o prazo (ex: CVM 7 anos para KYC, NF 5 anos contábil, Marco Civil 6 meses logs de conexão)
2. **Estudo por órgão de pesquisa** com anonimização
3. **Transferência para terceiro** quando cumpridos requisitos LGPD
4. **Uso exclusivo do controlador, vedado acesso a terceiros**, com **anonimização**

Fora dessas — **eliminar**.

---

## Política de retenção

Cada tratamento no ROPA tem **prazo de retenção definido**. Documentar:

```yaml
retencao:
  prazo: "5 anos após encerramento do contrato"
  fundamento: "CVM Inst. 301/1999 Art. 7 — KYC"
  apos_prazo: "Eliminação automatizada"
  excecoes:
    - "Se houver litígio em curso → reter até trânsito em julgado + 2 anos"
```

### Catálogo típico de prazos

| Tipo de dado | Prazo típico | Fundamento |
|---|---|---|
| Cadastrais cliente ativo | Vida do vínculo | Execução de contrato |
| Cadastrais cliente inativo | Vida do contrato + 5 anos | Prescrição civil (CC Art. 206) |
| Dados financeiros / KYC | 5-10 anos | CVM 301, BACEN Res. 4753, Lei 9613/98 |
| Notas fiscais | 5 anos | CTN Art. 174 |
| Folha de pagamento | 5 anos pós desligamento | CLT Art. 11 |
| Currículos não selecionados | 6 meses | Boa prática (TST favorece destruição) |
| Logs de acesso/conexão | 6 meses (Marco Civil) | Lei 12.965/14 Art. 13 |
| Logs de aplicação | 6-12 meses | Boa prática (segurança) |
| Cookies analytics | 13 meses | Boa prática (alinha com GA) |
| Gravações de chamada | 6-12 meses ou conforme regulação setorial | Sec. 1 / Resol BACEN |
| Vídeo de CFTV | 30-90 dias | Boa prática + LGPD |
| Dados de saúde (Resol. CFM) | 20 anos pós atendimento | Resol. CFM 1.821/2007 |
| Dados de menor | Especial cuidado, prazos mais curtos | Princípio do melhor interesse |
| Backups | Idem ao primário + janela de retenção do backup | Documentar |

---

## Métodos de eliminação

### Hard delete (preferencial)
```sql
DELETE FROM users WHERE id = $1;
DELETE FROM users_pii WHERE user_id = $1;
DELETE FROM events WHERE actor_id = $1;
```

- Propagar para **réplicas, search indexes, caches, message queues**
- Garantir que jobs de relatório/BI não recuperem
- Verificar **backups** — se backup ainda contém, deletar quando backup expirar

### Anonimização (alternativa quando há valor analítico)
- Substituir identificadores por hash sem reversibilidade
- Remover quasi-identificadores ou aplicar k-anonimato (k ≥ 5 mínimo)
- Documentar técnica
- **Atenção**: anonimização real é difícil. Pseudonimização não basta como "anonimização" para fins do Art. 12.

### Tokenização
- Substituir dado por token; mapeamento original em vault separado
- Funciona como pseudonimização — não substitui eliminação, mas reduz superfície

### Criptografia + destruição da chave
- Útil para "right to be forgotten" em backups imutáveis
- Documentar como técnica de "eliminação criptográfica"

---

## Workflow operacional

### Passo 1 — Inventário (a partir do ROPA)

Para cada tratamento: prazo de retenção + critério de fim + método de eliminação.

### Passo 2 — Implementar gatilhos

```sql
-- Job mensal
DELETE FROM users
WHERE deleted_at IS NOT NULL
  AND deleted_at < now() - interval '30 days'  -- período de tolerância para reversão
  AND NOT EXISTS (
    SELECT 1 FROM legal_holds WHERE subject_id = users.id
  );
```

Princípio: **soft-delete imediato + hard-delete após tolerância** (configurável, 30 dias típico).

### Passo 3 — Legal hold

Antes de qualquer eliminação automatizada, verificar se há:
- Litígio em curso (cliente vs empresa, empresa vs terceiro envolvendo o dado)
- Investigação interna
- Requisição judicial / da ANPD / de autoridade

Tabela `legal_holds` interrompe eliminação automatizada para `subject_id`.

### Passo 4 — Evidência

Para cada eliminação automatizada:

```json
{
  "ts": "2026-05-28T03:00:00Z",
  "event": "data_purge",
  "scope": "users.deleted > 30d",
  "rows_affected": 142,
  "categories": ["cadastrais", "preferências"],
  "rationale": "retention_policy: ROPA TRAT-2026-0017",
  "performed_by": "job:nightly_purge",
  "hash_prev": "...",
  "hash_self": "..."
}
```

### Passo 5 — Backups

- Backups têm **sua própria política de retenção** (ex: 30 dias rolling)
- Não tente deletar registro dentro de backup — espere o backup expirar
- Documentar: "dado eliminado de prod em D, persiste em backup até D+30"
- Em DSAR de eliminação, comunicar essa janela ao titular

### Passo 6 — Propagação para operadores

Quando você elimina, **operadores também eliminam** (Art. 39 + DPA).
- Endpoint de purge na API do operador (idealmente automatizada)
- Solicitação por canal documentado com SLA
- **Certidão de eliminação** do operador

---

## Casos especiais

### Cliente solicita eliminação mas há obrigação de retenção

Resposta ao titular:
> "Vamos eliminar X, Y, Z. Por força de [LEI/Resolução] precisamos reter [W] até [DATA]. Após esse prazo, será eliminado automaticamente."

### Cliente "morto" / espólio
- Eliminação a pedido do inventariante
- Documentação: termo de inventariante + certidão de óbito

### Sistemas legados sem capacidade de delete (mainframe, planilhas)
- Documentar limitação técnica
- Plano de migração ou wrapper
- Compensação por controles organizacionais (acesso restrito + audit)
- Reconhecer no DPIA

### Backup criptografado em fita imutável
- Eliminação criptográfica via destruição da chave (registrar)
- Ou aguardar expiração do ciclo de retenção da fita

### Dados em sistema de business intelligence / data warehouse
- Frequentemente esquecido — **incluir no inventário**
- Replicar política
- Pipelines de ETL devem respeitar "deleted_at"

---

## Métricas

| Métrica | Meta |
|---|---|
| % de tratamentos com prazo de retenção definido | 100% |
| % de eliminações automatizadas vs manuais | > 90% automatizadas |
| Tempo médio de propagação para operadores | < 7 dias |
| Volume de dados eliminados por mês | Tracking |
| Falhas de eliminação (jobs com erro) | 0 |

---

## Auditoria de retenção

Script: `scripts/python/retention-scanner.py`
- Compara `ROPA` com banco real
- Detecta tabelas com `created_at` muito antigo sem política
- Detecta colunas com PII sem retenção definida
- Detecta logs com PII (que devem ser sanitizados / ter retenção curta)

---

## Referências legais

- Art. 6, III — princípio da necessidade
- Art. 6, V — qualidade dos dados
- Art. 9 — direito à informação sobre tempo de tratamento
- **Art. 15** — término do tratamento
- **Art. 16** — exceções à eliminação
- Lei 12.965/14 (Marco Civil) — guarda de logs
- CC Art. 206 — prescrição
- CLT Art. 11 — prescrição trabalhista
- CTN Art. 174 — prescrição tributária

---

## Anti-padrões

| ❌ Erro | ✅ Correto |
|---|---|
| "Retemos para sempre porque dados são valiosos" | Reter conforme finalidade e obrigação |
| "Vamos anonimizar removendo o nome" | Anonimização exige técnica robusta (k-anon, etc.) |
| "Eliminamos do app, mas backup tem" | Política de backup explícita + comunicar titular |
| Deletar do prod mas BI mantém warehouse | Mapear todos os destinos |
| Cliente pede delete e empresa "esquece" | SLA propagação + monitoramento |
