# Controle — Resposta a Incidentes

> **Art. 46, 48 LGPD + Res. CD/ANPD 15/2024.**
> Plano vivo, testado regularmente. Ver workflow operacional em [`workflows/breach-72h.md`](../workflows/breach-72h.md) — este é o controle estrutural.

---

## Plano de Resposta a Incidentes (PRI)

Documento aprovado pela diretoria, revisado anualmente. Conteúdo mínimo:

1. **Definições e escopo** — o que conta como incidente
2. **Estrutura organizacional** — papéis, comando, comitê de crise
3. **Fluxo operacional** — detecção → contenção → erradicação → recuperação → lições
4. **Comunicação** — interna, ANPD, titulares, mídia
5. **Critérios de notificação** — quando notificar ANPD, quando comunicar titulares
6. **Forense e cadeia de custódia** — preservação de evidência
7. **Recuperação e continuidade**
8. **Treinamento e simulações**
9. **Métricas e melhoria contínua**

---

## Estrutura de Incident Response

### Time central (CSIRT)
| Papel | Responsabilidade |
|---|---|
| **Incident Commander (IC)** | Comando único na crise; decide |
| **Sec Lead** | Investigação técnica, contenção |
| **Engenharia Lead** | Execução de containment, rotação |
| **DPO** | LGPD — decisão de notificar, comunicação ANPD/titulares |
| **Jurídico** | Risco legal, contratos, exposição |
| **Comunicação** | Comunicado externo, mídia |
| **Patrocinador C-level** | Aprovações, recursos |
| **Forense** | Coleta de evidência, cadeia de custódia |

Plantão 24x7 documentado. Backup para cada papel.

---

## Classificação de incidentes

| Severidade | Critério | SLA notificação interna |
|---|---|---|
| **SEV-1 (Crítico)** | Vazamento confirmado dados sensíveis OU > 10k titulares OU sistema crítico fora | Imediato (≤ 15 min) |
| **SEV-2 (Alto)** | Vazamento confirmado de qualquer PII OU sistema relevante fora | ≤ 1h |
| **SEV-3 (Médio)** | Tentativa bem-sucedida sem exfiltração confirmada | ≤ 4h |
| **SEV-4 (Baixo)** | Vulnerabilidade descoberta, sem exploração | ≤ 1 dia |

Apenas SEV-1 e SEV-2 (geralmente) disparam Art. 48.

---

## Ciclo de vida do incidente

### Fase 1 — Preparação (contínua, antes do incidente)
- PRI documentado
- Times treinados
- Ferramentas instaladas (SIEM, EDR, forense)
- Contatos atualizados (ANPD, forense externa, jurídico externo)
- Simulações trimestrais
- Backups testados
- Runbooks específicos para cenários comuns

### Fase 2 — Detecção e análise
- Monitoramento (SIEM, EDR, alertas)
- Hotline interna (qualquer colaborador reporta suspeita)
- Bug bounty / disclosure responsável
- Análise inicial: é incidente? Severidade?

### Fase 3 — Contenção
- **Short-term**: parar o sangramento (cortar acesso, isolar máquina)
- **Long-term**: corrigir a vulnerabilidade raiz

### Fase 4 — Erradicação
- Remover artefatos do atacante
- Patch da vulnerabilidade
- Rotação de credenciais comprometidas
- Re-imagem se necessário

### Fase 5 — Recuperação
- Restaurar serviço
- Monitoramento aumentado por janela X
- Confirmar que atacante não tem persistência

### Fase 6 — Pós-incidente
- Post-mortem (blameless)
- Lições aprendidas
- Atualizar runbooks
- Atualizar controles
- Re-treinar equipe se necessário

---

## Comunicação durante o incidente

### Canal único de coordenação
- Slack/Teams dedicado **fora** do sistema afetado
- Não usar email para coordenação ativa (lento, vazamento)
- Documentação em tempo real (timeline)

### Comunicação interna
- Patrocinador C-level: SEV-1 imediato
- Diretoria: SEV-1 em até 1h
- Todo time afetado: conforme necessário
- Comunicado geral à empresa: só após contenção e com mensagem aprovada

### Comunicação externa
**Antes da contenção confirmada**: silêncio.
**Após confirmação**:
- ANPD: workflow [`breach-72h.md`](../workflows/breach-72h.md)
- Titulares: comunicação direta + canal aberto
- Imprensa: só com aprovação Comunicação + Jurídico + C-level
- Reguladores setoriais (BACEN, ANS, etc.): conforme exigências

**Não falar com**:
- Atacante (extorsão, ransomware) — exceto via negociador especializado e com aprovação jurídica
- Pesquisadores que ofereçam "ajuda" não solicitada sem disclosure formal

---

## Cadeia de custódia (forense)

Para preservar valor probatório:

1. **Snapshot imediato** dos sistemas afetados (não mexer no original)
2. **Hash** dos artefatos (SHA-256) — registrado em log imutável
3. **Cadeia documentada** — quem teve acesso, quando, o que fez
4. **Storage isolado** — chave separada
5. **Retenção mínima 5 anos** — pode ser usado em processo

Se houver indício criminal (invasão, extorsão): preservar para Polícia Federal / Delegacia de Crimes Cibernéticos.

---

## Cenários comuns — runbooks

### Credencial vazada (GitHub, leak público)
1. Revogar/rotacionar IMEDIATAMENTE
2. Auditar uso dessa credencial nos últimos 90 dias
3. Verificar se houve exfiltração
4. Se sim → SEV-1 + workflow breach
5. Disclosure responsável ao colaborador (se humano)

### Phishing direcionado bem-sucedido
1. Isolar máquina/conta comprometida
2. Forçar reset de senha + MFA re-enroll
3. Auditar acessos da conta nas últimas 24-72h
4. Revogar todos os tokens/sessões ativos
5. Análise forense da máquina
6. Comunicar internamente com aprendizado

### Ransomware
1. Isolar segmento de rede afetado
2. Não desligar máquinas (preserva RAM forense)
3. Acionar backups offline
4. Forense externa
5. **Não pagar** sem aprovação C-level + jurídico + análise de risco (sanções OFAC, financiamento crime)
6. Notificar ANPD se dados envolvidos (e geralmente estão)
7. Notificar PF se valor relevante

### Insider malicioso
1. RH + Jurídico desde o primeiro minuto
2. Preservar evidência ANTES de confrontar
3. Revogar acessos coordenadamente (não dar pista)
4. Investigar escopo do dano
5. Considerar BO + ação cível
6. Comunicar ANPD se dados envolvidos

### Bug em produção que expôs dados
1. Estimar quantos titulares foram afetados (logs)
2. Corrigir + deploy emergencial
3. Considerar se incidente exige Art. 48 (geralmente sim, mesmo se interno)
4. Comunicar titulares afetados
5. Post-mortem técnico + ajuste de testes

### Operador / vendor vazou
1. Acionar DPA — operador deve notificar
2. Avaliar nosso escopo de exposição
3. Decidir notificação ANPD (nós como controlador)
4. Comunicar titulares
5. Decidir continuar ou trocar operador

---

## Simulações (tabletop exercises)

Cadência mínima:
- **Trimestral**: cenário curto (1h) com time central
- **Semestral**: full exercise (4h) incluindo C-level
- **Anual**: simulação ANPD (notificação fake, prazos reais)

Métricas a observar:
- Tempo até comando ativado
- Tempo até contenção decidida
- Tempo até decisão de notificar
- Qualidade da comunicação
- Lacunas identificadas

---

## Métricas (KPI)

| Métrica | Meta |
|---|---|
| MTTD (mean time to detect) | < 24h |
| MTTR (mean time to respond — contenção) | < 4h |
| MTTC (mean time to contain) | < 12h |
| MTTR (recover) | depende do sistema |
| % incidentes com notificação ANPD < 72h | 100% |
| Recorrência de mesmo vetor | 0 |
| Simulações realizadas no ano | ≥ 4 |
| % do time treinado em PRI no ano | 100% |

---

## Anti-padrões

| ❌ Erro | ✅ Correto |
|---|---|
| Plano genérico copiado de template | Adaptado ao stack/processos reais |
| Sem simulações ("se acontecer, decidimos") | Trimestrais |
| Coordenação por email | Canal dedicado em sistema isolado |
| Desligar máquinas comprometidas (perde RAM forense) | Isolar rede, preservar |
| Negociar com atacante sem orientação | Negociador especializado + jurídico |
| Comunicado público antes de contenção | Esperar — risco de informação parcial gerar pânico |
| "Não é incidente, foi só vulnerabilidade" sem checar exploração | Investigar antes de classificar |
| Não documentar timeline | Documentar em tempo real |

---

## Documentos vinculados

- [`workflows/breach-72h.md`](../workflows/breach-72h.md) — runbook operacional
- [`templates/notificacao-anpd-incidente.md`](../templates/notificacao-anpd-incidente.md) — template ANPD
- [`controls/audit-logging.md`](audit-logging.md) — logs como evidência
- [`controls/encryption.md`](encryption.md) — encryption como mitigação
- [`lib/regulator-contacts.md`](../lib/regulator-contacts.md) — contatos ANPD + reguladores

---

## Referências

- Art. 46, 48 LGPD
- Res. CD/ANPD 15/2024
- NIST SP 800-61 Rev. 2 — Computer Security Incident Handling Guide
- ENISA — Guidelines for SMEs on the security of personal data
- ISO/IEC 27035 — Information security incident management
- BCB Res. 4893/2021
