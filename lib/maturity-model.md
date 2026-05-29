# Modelo de Maturidade — Privacy CMMI (LGPD)

> Adaptado de CMMI (Capability Maturity Model Integration) + frameworks NIST + ISO 27701.
> Permite ao DPO/C-level posicionar a organização em escala 1-5 e definir roadmap.

---

## Níveis

### Nível 1 — Inicial (Ad hoc)
- Sem política formal de privacidade
- DPO informal ou inexistente
- Resposta a incidentes reativa, sem playbook
- ROPA incompleto ou inexistente
- Consent gerenciado caso-a-caso
- Tratamento de DSAR sem SLA, manual
- Sem audit log estruturado
- Score de risco: **Alto a Crítico**

### Nível 2 — Repetível (Documentado)
- Política de privacidade publicada
- DPO formalmente indicado
- Plano de resposta a incidente escrito
- ROPA básico em planilha
- Consent banner instalado (pode ter gaps)
- DSAR atendidos com checklist, mas sem ferramental
- Logs existem mas dispersos
- Score de risco: **Alto**

### Nível 3 — Definido (Padronizado)
- Processos documentados e replicáveis em toda a empresa
- ROPA versionado, vinculado a sistemas
- DPIA/RIPD em tratamentos de alto risco
- Consent ledger auditável + propagação em ≤ 24h
- DSAR com SLA cumprido (15 dias) + ferramental
- Audit log centralizado (SIEM)
- Treinamento LGPD anual obrigatório
- DPA com 100% dos operadores
- Score de risco: **Médio**

### Nível 4 — Gerenciado (Mensurado)
- KPIs de privacidade reportados ao board
- Auditoria interna periódica
- Monitoramento contínuo (drift, fairness, retenção)
- Privacy by design integrado ao SDLC
- Tabletop exercises trimestrais
- Métricas: tempo médio DSAR, taxa de notificação no prazo, gaps fechados
- Audit log hash-chained
- Score de risco: **Baixo a Médio**

### Nível 5 — Otimizado (Melhorado continuamente)
- Privacy é vantagem competitiva
- Investimento contínuo em PETs
- Contribuição para padrões setoriais
- Cooperação ativa com ANPD
- Disclosure transparency proativa
- Privacy engineering como disciplina
- DPI (Data Protection Index) interno acompanhado
- Score de risco: **Baixo**

---

## Dimensões avaliadas

| Dimensão | Nível 1 | Nível 3 | Nível 5 |
|---|---|---|---|
| **Governança** | DPO informal | DPO indicado + comitê | DPO com poder de veto + board |
| **ROPA** | Planilha incompleta | Inventário versionado | ROPA + automação via SDLC |
| **Bases legais** | Ad hoc | Documentadas por atividade | LIA automatizada quando aplicável |
| **DSAR** | Manual, sem SLA | SLA 15d cumprido | DSAR auto-serviço + métricas |
| **Consent** | Banner, sem ledger | Ledger auditável | Granular + revogação propagada |
| **Incidentes** | Reativa | PRI + simulações | Detecção pré-impacto + comunicação proativa |
| **DPIA** | Não realizada | Em alto risco | Em todo lançamento |
| **Vendor mgmt** | Sem DPA | DPA + auditoria anual | Score contínuo + automação |
| **Criptografia** | Default cloud | Application-layer | Camada confidencial (TEE/HE) |
| **Audit logs** | Logs dispersos | SIEM centralizado | Hash-chained + integridade verificada |
| **Treinamento** | Não estruturado | Anual obrigatório | Personalizado por papel + simulado |
| **Métricas** | Inexistentes | Relatório DPO | Board KPIs + benchmarks setor |

---

## Como avaliar

Para cada dimensão, pontuar:
- 1: Inexistente / Ad hoc
- 2: Em construção / parcial
- 3: Implementado e documentado
- 4: Monitorado com métricas
- 5: Otimizado + benchmark

**Score geral** = média ponderada. Ponderação sugerida:
- Governança, ROPA, DSAR, Incidentes: peso 2
- Demais: peso 1

```
score_total = (
    governanca * 2 + ropa * 2 + bases_legais + dsar * 2 +
    consent + incidentes * 2 + dpia + vendor +
    cripto + audit_logs + treinamento + metricas
) / 16
```

---

## Roadmap típico (12-18 meses para sair de N2 → N3)

| Trimestre | Foco |
|---|---|
| Q1 | DPO + política + canal de direitos + ROPA inicial (top 20 atividades) |
| Q2 | DPA com todos os operadores + plano de resposta a incidente + treinamento |
| Q3 | Consent ledger + audit log centralizado + DSAR ferramental |
| Q4 | DPIA nas atividades de alto risco + privacy by design no SDLC + métricas iniciais |
| Q5 | Auditoria interna + simulações + ROPA 100% + ajustes |
| Q6 | Hash-chain de evidência + dashboards C-level + revisão completa |

---

## ROI / Risco

Para apresentação a C-level:

| Investimento típico | Retorno |
|---|---|
| DPO sênior + ferramenta | R$ 300-800k/ano | Evita multa ANPD (até 2% faturamento, máx R$ 50M/infração) |
| Programa de privacy maduro (N3+) | R$ 1-3M/ano em empresa média | Reduz risco de incidente reportável de ~30% para <5% em 24m |
| Privacy engineering integrado | R$ 500k-1.5M/ano | Time-to-market mantido + diferencial competitivo em B2B |

Custo do **não-investimento**:
- Multa máxima ANPD por infração: 2% do faturamento (limite R$ 50M)
- Dano reputacional pós-incidente: 5-15% de churn em B2C
- Litígio individual (CDC + LGPD): R$ 5k-50k por titular afetado
- Bloqueio de transferência internacional → impacto operacional

---

## Benchmarks setor (Brasil 2025-2026)

| Setor | Nível médio atual |
|---|---|
| Financeiro (bancos, fintechs) | 3.5 — pressionados por BACEN |
| Saúde (hospitais, healthtechs) | 2.5 — Resol. CFM ajuda mas não basta |
| Varejo | 2.0 |
| E-commerce | 2.5 |
| Educação (incl. EdTechs) | 2.0 |
| Indústria | 1.5 |
| Setor público | 2.0 — Res. ANPD 1/2023 |
| Big tech BR | 3.0-4.0 |
| Startups early-stage | 1.5 |

Fonte: agregação de pesquisas IAPP, autorregulação setorial, e fiscalizações ANPD públicas.

---

## Self-assessment template

```yaml
organizacao: "{{NOME}}"
data_avaliacao: "2026-05-28"
avaliador: "{{NOME_DPO}}"

dimensoes:
  governanca: 3
  ropa: 3
  bases_legais: 2
  dsar: 3
  consent: 2
  incidentes: 3
  dpia: 2
  vendor: 2
  criptografia: 4
  audit_logs: 3
  treinamento: 3
  metricas: 2

score_geral: 2.75
nivel_inferido: "2.75 — em transição de Nível 2 → Nível 3"

gaps_priorizados:
  - dimensao: "bases_legais"
    acao: "Documentar LIA para tratamentos com base em Art. 7 IX"
    prazo: "Q3 2026"
  - dimensao: "dpia"
    acao: "Implementar trigger automático no SDLC"
    prazo: "Q4 2026"
  - dimensao: "metricas"
    acao: "Dashboard mensal para C-level"
    prazo: "Q3 2026"
```

---

## Referências

- ISO/IEC 27701:2019 — Privacy Information Management Extension
- NIST Privacy Framework
- AICPA Privacy Maturity Model
- Carnegie Mellon CMMI
- ENISA Maturity Model for Public Administrations
