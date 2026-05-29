# Template — RIPD / DPIA (Relatório de Impacto à Proteção de Dados)

> Art. 38 LGPD. Documento vivo. Revisão anual + a cada mudança material.
> Use linguagem técnica precisa. Cite artigos. Justifique probabilidade × severidade com dados, não opinião.

---

# RELATÓRIO DE IMPACTO À PROTEÇÃO DE DADOS PESSOAIS (RIPD/DPIA)

| Campo | Conteúdo |
|---|---|
| **Documento** | RIPD-{{YYYY}}-{{NNNN}} |
| **Versão** | {{VERSAO}} |
| **Data desta versão** | {{DATA}} |
| **Próxima revisão** | {{DATA + 1 ANO ou em mudança material}} |
| **Classificação** | Interno / Confidencial |
| **Status** | [ ] Draft  [ ] Em revisão  [ ] Aprovado  [ ] Arquivado |

---

## 1. Identificação

### 1.1 Tratamento avaliado
**Nome:** {{NOME_DO_TRATAMENTO}}
**ID no ROPA:** {{TRAT-YYYY-NNNN}}
**Sistema/Produto:** {{NOME}}
**Equipe responsável:** {{TIME}}
**Patrocinador (negócio):** {{NOME}} — {{CARGO}}

### 1.2 Equipe deste RIPD
- **DPO**: {{NOME_DPO}}
- **Privacy Engineer**: {{NOME}}
- **Tech Lead**: {{NOME}}
- **Jurídico**: {{NOME}}
- **Segurança**: {{NOME}}

### 1.3 Gatilho desta avaliação
[ ] Novo tratamento — pré-deploy
[ ] Revisão anual
[ ] Mudança material em {{O_QUE_MUDOU}}
[ ] Incidente passado relacionado
[ ] Determinação ANPD
[ ] Solicitação do DPO

---

## 2. Descrição do Tratamento

### 2.1 Finalidade
**Específica e explícita** (Art. 6, I LGPD):
> {{TEXTO_FINALIDADE}}

Finalidades secundárias (cada uma com base legal própria):
| Finalidade secundária | Base legal |
|---|---|
| {{TEXTO}} | {{ART_X}} |

### 2.2 Base legal
**Hipótese principal:** Art. {{X}}, inciso {{Y}} LGPD — {{TIPO}}
**Justificativa:**
> {{TEXTO}}

**Se Art. 7, IX (legítimo interesse):** Anexar LIA (Legitimate Interest Assessment) — Anexo C.

### 2.3 Dados tratados
| Categoria | Campos específicos | Sensível? |
|---|---|---|
| Identificação | nome, CPF, RG | Não |
| Contato | email, telefone | Não |
| {{...}} | {{...}} | {{Sim/Não}} |

**Volume estimado:** {{NUMERO}} registros / {{NUMERO}} titulares/mês.
**Origem dos dados:** [ ] Coleta direta  [ ] Terceiros  [ ] Geração automática  [ ] Inferência

### 2.4 Titulares
| Categoria | Vulnerabilidade |
|---|---|
| Clientes PF | — |
| Menores | Sim (Art. 14) |
| Funcionários | Relação assimétrica de poder |

### 2.5 Fluxo de dados
> *Inserir diagrama. Pode ser referência a documento de arquitetura.*

**Etapas principais:**
1. Coleta — {{ONDE_COMO}}
2. Transmissão — {{PROTOCOLO}}
3. Armazenamento — {{SISTEMA, REGIAO}}
4. Processamento — {{O_QUE_FAZ}}
5. Compartilhamento — {{COM_QUEM}}
6. Retenção — {{PRAZO}}
7. Eliminação — {{METODO_E_GATILHO}}

### 2.6 Tecnologias envolvidas
- Banco de dados: {{NOME, VERSAO}}
- Backup: {{TECNOLOGIA}}
- ML / IA: {{MODELO, VERSAO}}
- Criptografia: {{ALGORITMO, GESTAO_DE_CHAVE}}
- {{OUTRAS}}

### 2.7 Operadores e sub-operadores
| Operador | Sub-operadores | DPA | Localização |
|---|---|---|---|
| {{NOME}} | {{LISTAR}} | DPA-XXX | {{PAIS}} |

### 2.8 Transferência internacional
Ocorre? **{{SIM/NAO}}**. Se sim: detalhar em Anexo D + TIA referenciado.

### 2.9 Retenção
| Tipo de dado | Prazo | Fundamento |
|---|---|---|
| {{X}} | {{PRAZO}} | {{FUNDAMENTO_LEGAL_OU_DE_NEGOCIO}} |

---

## 3. Necessidade e Proporcionalidade

### 3.1 Por que esse tratamento é necessário?
> {{TEXTO}}

### 3.2 Alternativas consideradas e descartadas
| Alternativa | Por que descartada |
|---|---|
| Não coletar X | {{RAZAO}} |
| Coletar Y agregado | {{RAZAO}} |
| Anonimização total | {{RAZAO}} |

### 3.3 Aderência à minimização (Art. 6, III)
- Cada dado coletado é estritamente necessário para a finalidade? **{{SIM/NAO}}**
- Há campos coletados "por garantia" ou para "uso futuro"? Listar e justificar ou remover.

### 3.4 Aderência aos demais princípios (Art. 6)
| Princípio | Aderência | Evidência |
|---|---|---|
| Finalidade (I) | OK / Atenção | {{TEXTO}} |
| Adequação (II) | OK | {{TEXTO}} |
| Necessidade (III) | OK | {{TEXTO}} |
| Livre acesso (IV) | OK | {{TEXTO}} |
| Qualidade (V) | OK | {{TEXTO}} |
| Transparência (VI) | OK | {{TEXTO}} |
| Segurança (VII) | OK | {{TEXTO}} |
| Prevenção (VIII) | OK | {{TEXTO}} |
| Não discriminação (IX) | OK | {{TEXTO}} |
| Responsabilização (X) | OK | {{TEXTO}} |

---

## 4. Avaliação de Riscos

### 4.1 Catálogo de riscos identificados

| ID | Risco | Vetor | Probabilidade | Severidade | Risco bruto |
|---|---|---|---|---|---|
| R1 | Acesso não autorizado a dados em produção | Credencial vazada, falta de MFA | Média | Alta | **Alto** |
| R2 | Vazamento de PII em logs | Log mal configurado | Alta | Média | **Alto** |
| R3 | Reidentificação de dados pseudonimizados | Cruzamento com base externa | Baixa | Alta | Médio |
| R4 | Função creep (uso fora da finalidade) | Pressão de outras áreas | Média | Alta | **Alto** |
| R5 | Vazamento por operador | Incidente em vendor | Média | Alta | **Alto** |
| R6 | Discriminação algorítmica | Viés no dataset de treino | Média | Alta | **Alto** |
| R7 | Falha em atender Art. 18 | Dados em silo não mapeado | Média | Média | Médio |
| R8 | Retenção excedendo o necessário | Job de purga quebrado | Alta | Média | **Alto** |
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

Use matriz em [`lib/risk-matrix.md`](../lib/risk-matrix.md).

### 4.2 Riscos detalhados (por risco)

#### R1 — Acesso não autorizado a dados em produção
- **Cenário concreto:** {{TEXTO}}
- **Vetor:** {{DETALHE}}
- **Quem é afetado:** todos os {{N}} titulares
- **Dano potencial:** {{DESCREVER — material, moral, discriminação}}
- **Probabilidade base (sem controle):** Alta
- **Severidade:** Alta (se sensíveis: Crítica)
- **Mitigação primária:** Cláusula 5.1 abaixo

[Repetir para cada risco crítico]

---

## 5. Medidas Mitigatórias

Para cada risco, controle específico. Referenciar [`controls/`](../controls/).

### 5.1 — R1: Acesso não autorizado
| Controle | Tipo | Referência | Responsável | Status |
|---|---|---|---|---|
| MFA obrigatório | Técnico | controls/access-control-rbac.md | Sec | Implementado |
| Audit log com alerta de acesso anômalo | Técnico | controls/audit-logging.md | Sec | Implementado |
| Revisão trimestral de acessos | Org. | controls/access-control-rbac.md | Sec + RH | Em implementação |

**Eficácia esperada:** redução de probabilidade de Alta → Baixa.

### 5.2 — R2: PII em logs
| Controle | Tipo | Status |
|---|---|---|
| Sanitização de logs em SDK comum | Técnico | Implementado |
| CI gate com pii-scanner | Técnico | Implementado |
| Treinamento equipe de eng | Org. | Concluído 2026-04 |

### 5.3 — R3: Reidentificação
| Controle | Tipo | Status |
|---|---|---|
| k-anonimato com k≥5 | Técnico | A implementar |
| Restrição de acesso à camada pseudonimizada | Técnico | Implementado |

[Continuar para cada risco]

---

## 6. Risco Residual

Após aplicar controles:

| ID | Risco | Prob. residual | Sev. residual | Risco residual | Aceitável? |
|---|---|---|---|---|---|
| R1 | Acesso não autorizado | Baixa | Alta | Médio | Sim, monitorado |
| R2 | PII em logs | Muito baixa | Média | Baixo | Sim |
| R3 | Reidentificação | Baixa | Alta | Médio | Sim, monitorado |
| R4 | Função creep | Baixa | Alta | Médio | Sim |
| R5 | Vazamento por operador | Média | Alta | **Alto** | Atenção — plano (Cláusula 7) |
| R6 | Discriminação algorítmica | Baixa | Alta | Médio | Sim, com monitoramento contínuo |
| R7 | Falha Art. 18 | Baixa | Média | Baixo | Sim |
| R8 | Retenção excedida | Baixa | Média | Baixo | Sim |

### 6.1 Classificação geral
[ ] **Aceitável** — todos riscos residuais baixos/médios com plano
[ ] **Tolerável com plano** — alguns médios/altos com mitigação em andamento
[ ] **Inaceitável** — alto residual sem mitigação viável → consultar ANPD ou não prosseguir

---

## 7. Plano de Ação

| Item | Risco endereçado | Prazo | Responsável | Status |
|---|---|---|---|---|
| Implementar k-anonimato pipeline | R3 | 2026-07-15 | Privacy Eng | Em andamento |
| DPA com novo operador (back-to-back SCC) | R5 | 2026-06-30 | Jurídico | Em andamento |
| Auditoria de fairness modelo M | R6 | 2026-09-01 | Data Science + DPO | Planejado |
| {{...}} | | | | |

---

## 8. Consulta à ANPD (Art. 38 parágrafo único)

[ ] Não necessária
[ ] Recomendada — motivo: {{TEXTO}}
[ ] Em curso — referência: {{OFICIO_PROTOCOLO}}

---

## 9. Aprovação

| Função | Nome | Decisão | Data | Assinatura |
|---|---|---|---|---|
| DPO | {{NOME}} | [ ] Aprovado [ ] Aprovado com ressalvas [ ] Reprovado | {{DATA}} | {{SIG}} |
| Patrocinador | {{NOME}} | [ ] Prosseguir [ ] Não prosseguir | {{DATA}} | {{SIG}} |
| Jurídico | {{NOME}} | [ ] Sem ressalvas [ ] Ressalvas (anexo) | {{DATA}} | {{SIG}} |
| Segurança | {{NOME}} | [ ] OK [ ] OK com ressalvas | {{DATA}} | {{SIG}} |

---

## 10. Anexos

- **Anexo A** — Diagrama de fluxo de dados
- **Anexo B** — Inventário de campos detalhado (schema)
- **Anexo C** — LIA (se base legal = legítimo interesse)
- **Anexo D** — TIA (se transferência internacional)
- **Anexo E** — Model Card (se decisão automatizada)
- **Anexo F** — Threat model técnico (STRIDE)
- **Anexo G** — Mapeamento contra requisitos setoriais (BACEN, ANS, etc.)

---

**Hash deste documento (SHA-256):** {{HASH}}
**Vinculado ao ROPA:** {{TRAT-YYYY-NNNN}}
**Vinculado ao plano de ação ID:** {{ID}}
