# Workflow — Vendor / Operador / DPA

> **Art. 39 LGPD** — Operador deve realizar tratamento conforme instruções fornecidas pelo controlador.
> **Art. 42** — Responsabilidade solidária quando operador descumprir.

---

## Quando ativar

- Antes de **contratar** novo SaaS/serviço que trate PII em seu nome
- Antes de **enviar dados** para um operador existente (mudança de escopo)
- Quando operador **adicionar sub-operador** (notificar / aprovar)
- Em **revisão anual** de operadores ativos
- Em **off-boarding** (eliminação dos dados ao fim do contrato)

---

## SLA

| Marco | Prazo |
|---|---|
| Due diligence inicial | 5 dias úteis |
| Assinatura de DPA antes de transferir dados | Bloqueador — não envia sem DPA |
| Revisão de operador ativo | Anual |
| Off-boarding pós-contrato | Operador certifica eliminação em 30 dias |

---

## Passo 1 — Due diligence (5 dias)

Checklist para operador candidato:

### Dados básicos
- [ ] Razão social, CNPJ, endereço
- [ ] DPO/Encarregado identificado e contactável
- [ ] Política de privacidade pública (verificar)
- [ ] Subscreve a LGPD (não é só "GDPR")

### Segurança
- [ ] Criptografia at-rest declarada (qual algoritmo?)
- [ ] Criptografia in-transit (TLS mínimo 1.2)
- [ ] MFA disponível para clientes
- [ ] Audit logs disponíveis
- [ ] SOC 2 Type II ou ISO 27001 (preferencial — não substitui DPA)
- [ ] Programa de bug bounty / disclosure responsável
- [ ] Histórico de incidentes públicos (Google pesado)

### Operacional
- [ ] Localização dos data centers (jurisdição)
- [ ] Lista de sub-operadores
- [ ] SLA de uptime
- [ ] SLA de notificação de incidente (deve ser **< 24h** para você cumprir 72h ANPD)
- [ ] Capacidade de atender DSAR via API ou processo claro

### Risco-país (se internacional)
- [ ] País tem nível adequado reconhecido pela ANPD? (ver [`workflows/cross-border-transfer.md`](cross-border-transfer.md))
- [ ] CLOUD Act exposure (EUA)?
- [ ] Histórico de pedidos governamentais ao operador

Score the vendor. Se "vermelho" em segurança → recusar / exigir compensação contratual.

---

## Passo 2 — DPA (Data Protection Addendum)

Template completo: [`templates/dpa-controller-processor.md`](../templates/dpa-controller-processor.md).

Cláusulas **obrigatórias** (Art. 39):

1. **Objeto** — natureza, finalidade, duração do tratamento
2. **Categorias de dados** e de titulares
3. **Instruções documentadas do controlador** — operador NÃO pode tratar fora delas
4. **Confidencialidade** — equipe do operador sob NDA
5. **Segurança técnica e organizacional** — referenciar Anexo Técnico (especificar)
6. **Sub-operadores** — autorização prévia + lista atual + obrigação de notificar mudança
7. **Direitos do titular** — operador deve cooperar (responder a DSAR em prazo que permita 15 dias para controlador)
8. **Incidentes** — notificar controlador em prazo **claramente especificado** (ideal 24h, máximo 48h)
9. **Auditoria** — direito do controlador auditar (ou aceitar relatório SOC 2)
10. **Retorno / eliminação ao fim do contrato** — opção do controlador, com certidão
11. **Transferência internacional** — se houver, mecanismo (SCC, BCR, etc.)
12. **Responsabilidade** — alocação clara; cap de responsabilidade
13. **Lei aplicável e foro** — Brasil para tratamentos LGPD

Cláusulas comumente **mal redigidas** ou **abusivas** (negociar):

| ❌ Abusivo | ✅ Correto |
|---|---|
| "Operador notificará vazamento em prazo razoável" | "Operador notificará em até 24h após conhecimento" |
| "Operador pode contratar sub-operadores a seu critério" | "Operador notifica com 30 dias e controlador pode objetar" |
| "Cap de responsabilidade limitado a 12 meses de mensalidades" | Negociar excluir LGPD/incidente desse cap |
| "Operador retém dados por até 7 anos para fins próprios" | Operador trata apenas conforme instruções do controlador |
| Foro arbitral em país do operador | Foro no Brasil para LGPD |

---

## Passo 3 — Anexo Técnico

DPA deve referenciar **Anexo Técnico** detalhando controles. Use [`controls/`](../controls/) como base:

- Criptografia (algoritmo, gestão de chave)
- Controle de acesso (RBAC, MFA, princípio do mínimo)
- Audit log (o que loga, onde, por quanto tempo)
- Backup e recuperação
- Gestão de vulnerabilidades (patch SLA)
- Resposta a incidente (runbook, contatos)
- Continuidade (RTO, RPO)
- Treinamento de equipe

---

## Passo 4 — Assinatura e arquivamento

- DPA assinado por **representante legal** (não basta o gerente comercial)
- Versão eletrônica com hash + carimbo de tempo (Adobe Sign / ICP-Brasil aceitável)
- Arquivar:
  - Em sistema de gestão de contratos
  - Vincular ao [`ROPA`](ropa.md) — atividades que dependem desse operador
  - Vincular ao [`Inventário de Operadores`](#)

---

## Passo 5 — Onboarding técnico

- Operador recebe credenciais com **mínimo privilégio**
- Chaves de API com escopo limitado
- IP allowlist se aplicável
- Logging do que o operador acessa
- Testar capacidade de atender DSAR ANTES de produção

---

## Passo 6 — Operação contínua

- Monitorar SLAs
- Receber relatórios de segurança (SOC 2 anual, atualização de sub-operadores)
- Avaliar incidentes do operador (qualquer incidente público → re-avaliar)
- Revisar DPA na renovação

---

## Passo 7 — Off-boarding

Quando o contrato termina:

1. **Opção do controlador**: devolução dos dados (formato interoperável) OU eliminação
2. **Prazo**: 30 dias após fim do contrato
3. **Certidão de eliminação**: documento assinado pelo operador comprovando deleção em todos os sistemas (prod, backups, logs)
4. Retorno de credenciais
5. Revogação de acessos
6. Atualizar ROPA — remover operador
7. Comunicar titulares se a mudança implica em mudança de finalidade/operador (Art. 9)

---

## Casos especiais

### Operador descumpre / vaza dados

- Acionar cláusula contratual de penalidade
- Avaliar responsabilidade solidária (Art. 42)
- Reportar ANPD (você é o controlador — sua a obrigação)
- Considerar rescisão imediata
- Comunicar titulares se afetados

### Operador é também controlador para outras finalidades

(ex: provedor de email marketing usa dados agregados para próprio benchmark)
- Inadmissível sem base legal própria + transparência ao titular
- Cláusula no DPA deve **proibir explicitamente** ou exigir documento separado para essa finalidade

### Sub-operador surpresa

(operador adicionou sub-operador sem notificar)
- Violação contratual
- Pode ser violação LGPD se sub-operador tem nível de segurança inferior
- Acionar formalmente; suspender se grave

### Big tech / SaaS de prateleira (Google Workspace, AWS, Slack)

- Aceitar DPA "padrão" deles, mas **ler atentamente**
- Negociar adendo se houver gap crítico
- Documentar como decisão informada de risco

### Operador no exterior

- DPA + workflow [`cross-border-transfer.md`](cross-border-transfer.md)
- SCC (Standard Contractual Clauses) ou outro mecanismo
- TIA (Transfer Impact Assessment) obrigatório (Res. 19/2024)

---

## Métricas

| Métrica | Meta |
|---|---|
| % operadores com DPA assinado | 100% |
| % operadores com SLA de incidente ≤ 24h | 100% (para tratamento crítico) |
| Tempo médio de due diligence | < 5 dias |
| % operadores revisados anualmente | 100% |
| % off-boardings com certidão de eliminação | 100% |

---

## Referências legais

- Art. 5, VII — definição de operador
- Art. 39 — obrigações do operador
- Art. 42 — responsabilidade
- Art. 43 — exceção de responsabilidade
- Princípio da prestação de contas
- Res. CD/ANPD 4/2023 — dosimetria (não diligenciar operador é agravante)

---

## Anti-padrões

| ❌ Erro | ✅ Correto |
|---|---|
| "Esquecemos o DPA, mas o vendor é confiável" | Sem DPA = sem transferência |
| DPA assinado em PDF escaneado sem hash | Adobe Sign / ICP-Brasil |
| Lista de sub-operadores não atualizada há 2 anos | Revisão trimestral mínima |
| Aceitar SLA de notificação "em prazo razoável" | Negociar 24h |
| Off-boarding sem certidão | Não deletar sua cópia até receber certidão |
