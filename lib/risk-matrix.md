# Matriz de Risco — Severidade × Probabilidade

> Base para classificação em RIPD/DPIA, decisão de notificação ANPD e priorização de mitigações.

---

## Probabilidade

| Nível | Critério |
|---|---|
| **P1 — Muito baixa** | Requer combinação rara de fatores; nunca observado |
| **P2 — Baixa** | Possível mas improvável dentro de 12 meses |
| **P3 — Média** | Plausível em 12 meses; vetor conhecido |
| **P4 — Alta** | Provável em < 6 meses; já tentado anteriormente |
| **P5 — Muito alta** | Esperado em < 3 meses; recorrente ou em curso |

---

## Severidade (impacto ao titular)

| Nível | Critério |
|---|---|
| **S1 — Insignificante** | Inconveniência mínima, reversível, sem registro |
| **S2 — Baixa** | Dano limitado, recuperável (ex: spam, cadastro indesejado) |
| **S3 — Média** | Dano moral ou material moderado (vazamento de email/telefone, exposição limitada) |
| **S4 — Alta** | Dano significativo (vazamento de dados financeiros, fraude possível, exposição em massa) |
| **S5 — Crítica** | Dano grave e irreversível (sensíveis Art. 11 vazados, vida em risco, discriminação sistêmica, exposição de criança/adolescente) |

---

## Matriz 5×5

|                     | S1 Insignif. | S2 Baixa | S3 Média | S4 Alta | S5 Crítica |
|---------------------|:---:|:---:|:---:|:---:|:---:|
| **P5 Muito alta**   | M | A | A | **C** | **C** |
| **P4 Alta**         | B | M | A | A | **C** |
| **P3 Média**        | B | M | M | A | **C** |
| **P2 Baixa**        | B | B | M | A | A |
| **P1 Muito baixa**  | B | B | B | M | A |

Legenda: **B** = Baixo · **M** = Médio · **A** = Alto · **C** = Crítico

---

## Decisão por nível

| Nível | Ação |
|---|---|
| **Baixo** | Aceitar com monitoramento. Documentar no DPIA. |
| **Médio** | Mitigar com controle padrão. Revisar trimestralmente. |
| **Alto** | Mitigar com controle robusto + plano de ação. Aprovação DPO. |
| **Crítico** | **Não prosseguir** sem mitigação efetiva. Consultar ANPD (Art. 38 parágrafo único) se residual permanece. |

---

## Decisão de notificação ANPD (Art. 48)

| Risco bruto | Risco residual | Notificar ANPD? |
|---|---|---|
| Baixo | Baixo | Não |
| Médio | Baixo (mitigado) | Geralmente não |
| Médio | Médio | Sim (registro interno + avaliar comunicação ao titular) |
| Alto | Médio | Sim |
| Alto | Alto | Sim + comunicar titulares |
| Crítico | Qualquer | Sim + comunicar titulares + considerar comunicado público |

---

## Catálogo de cenários típicos

### Cenário 1 — Email vazado (single titular, base não-sensível)
- Probabilidade base: P3
- Severidade: S2 (S3 se contexto sensível: ex. lista de clientes de clínica)
- Risco bruto: Médio
- Mitigação: comunicar titular, monitorar; geralmente não exige Art. 48

### Cenário 2 — Banco de 100k clientes vazado em claro
- Probabilidade base (atacante competente): P4
- Severidade: S4
- Risco bruto: Alto
- Mitigação obrigatória: notificar ANPD < 72h + comunicar titulares + investigação

### Cenário 3 — Dados sensíveis (saúde, biometria) de 1 titular acessados sem autorização
- Probabilidade base: P3
- Severidade: S5
- Risco bruto: Crítico
- Mitigação: notificar ANPD + comunicar titular + investigar amplitude

### Cenário 4 — Backup criptografado roubado, chave segura
- Probabilidade base de exploração: P1
- Severidade base: S5
- Risco residual (assumindo chave íntegra): Baixo
- Mitigação: registrar internamente; comunicar ANPD apenas se chave também comprometida

### Cenário 5 — Modelo de decisão automatizada com viés racial
- Probabilidade: P3-P4 (se modelo sem fairness testing)
- Severidade: S5 (discriminação sistêmica)
- Risco bruto: Crítico
- Mitigação: auditoria fairness + revisão humana mandatória + correção do modelo + revisão das decisões já tomadas

### Cenário 6 — Cookies de marketing carregando sem consent
- Probabilidade de detecção/reclamação: P5 (já em fiscalização ANPD)
- Severidade ao titular individual: S2
- Risco bruto: Alto (escala compensa baixa severidade individual)
- Mitigação: CMP que bloqueia, ajuste de banner

### Cenário 7 — Operador no exterior sem TIA + sem SCC
- Probabilidade de auditoria: P3
- Severidade: S3 (não-conformidade documentada)
- Risco bruto: Médio
- Mitigação: TIA + adendo contratual + verificar Res. 19/2024

---

## Cálculo automatizado

Função Python sugerida:

```python
def risk_level(prob: int, sev: int) -> str:
    """prob 1-5, sev 1-5 → 'B' | 'M' | 'A' | 'C'"""
    matrix = [
        # S1, S2, S3, S4, S5
        ["B", "B", "B", "M", "A"],  # P1
        ["B", "B", "M", "A", "A"],  # P2
        ["B", "M", "M", "A", "C"],  # P3
        ["B", "M", "A", "A", "C"],  # P4
        ["M", "A", "A", "C", "C"],  # P5
    ]
    return matrix[prob - 1][sev - 1]
```

---

## Fatores que ajustam (modificadores)

Aumentam severidade base:
- Envolve menores (Art. 14) → +1 nível
- Envolve sensíveis (Art. 11) → +1 nível (mín. S4)
- Vazamento já público (não só acessado) → +1 nível
- Identificação sem necessidade de cruzamento → +1 nível
- Possibilita fraude direta (cartão, CPF + dados de contato) → +1 nível

Reduzem severidade base:
- Dados criptografados com chave íntegra → -2 níveis (validar)
- Pseudonimização eficaz + chave segura → -1 nível
- Anonimização (Art. 12) → não é dado pessoal → fora do escopo

---

## Referências

- Res. CD/ANPD 4/2023 — dosimetria de sanção (fatores agravantes/atenuantes)
- Res. CD/ANPD 15/2024 — risco como critério de notificação
- NIST SP 800-30 — Guide for Conducting Risk Assessments
- ENISA Threat Landscape
- ISO/IEC 27005 — Information Security Risk Management
