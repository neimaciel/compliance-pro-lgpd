# Workflow — DPIA / RIPD (Relatório de Impacto à Proteção de Dados)

> **Art. 38 LGPD.** RIPD = Relatório de Impacto à Proteção de Dados Pessoais.
> Equivalente nacional ao DPIA (GDPR Art. 35).

---

## Quando é obrigatório

Não há lista taxativa na LGPD, mas a ANPD pode requisitar. **Faça preventivamente** quando o tratamento apresenta **alto risco**:

| Gatilho | Por quê |
|---|---|
| Tratamento em larga escala | Volume amplifica dano |
| Dados sensíveis (Art. 5 II) | Risco intrínseco maior |
| Crianças/adolescentes (Art. 14) | Princípio do melhor interesse |
| Monitoramento sistemático de comportamento | Risco de vigilância |
| Decisões automatizadas com efeito jurídico/significativo (Art. 20) | Risco de discriminação algorítmica |
| Cruzamento de bases de dados de origens distintas | Reidentificação |
| Tecnologias emergentes (IA, biometria, IoT) | Riscos não plenamente compreendidos |
| Transferência internacional para país sem nível adequado | Risco de jurisdição |
| Base legal "legítimo interesse" — exige LIA prévia | Demonstrar balanceamento |
| Nova feature/produto que processa PII | Privacy by design |

---

## SLA

| Marco | Prazo |
|---|---|
| Triagem (precisa DPIA?) | 1 dia útil |
| Mapeamento do tratamento | 5 dias |
| Avaliação de riscos | 5 dias |
| Definição de medidas mitigatórias | 5 dias |
| Revisão DPO + Jurídico | 3 dias |
| Aprovação stakeholder + arquivamento | 2 dias |
| **Total** | **~3 semanas** |

DPIA é **vivo** — atualizar quando o tratamento mudar (escopo, finalidade, base legal, tecnologia, operador novo).

---

## Estrutura do RIPD

Use template completo: [`templates/dpia-template.md`](../templates/dpia-template.md).

Aqui está o esqueleto:

### 1. Identificação
- Nome do tratamento / projeto
- Responsável (controlador) + DPO
- Operadores envolvidos
- Versão + data + ciclo de revisão (anual mínimo)

### 2. Descrição do tratamento
- **Finalidade** (específica, explícita, legítima — Art. 6 I)
- **Base legal** (Art. 7 ou Art. 11 se sensível) com justificativa
- **Dados tratados** (categorias) — atenção a sensíveis
- **Titulares** (categorias — clientes, funcionários, menores...)
- **Volume estimado**
- **Operações** (coleta, armazenamento, uso, compartilhamento, eliminação)
- **Tecnologias** envolvidas
- **Fluxo de dados** (diagrama)
- **Retenção** prevista + critério
- **Compartilhamentos** (com quem, por quê, base legal)
- **Transferências internacionais** (se houver)

### 3. Necessidade e proporcionalidade
- Por que esses dados? Por que esse volume?
- Há alternativa menos invasiva?
- Adequação ao princípio da minimização (Art. 6 III)

### 4. Avaliação de riscos

Para cada risco, estimar:
- **Probabilidade**: Baixa / Média / Alta
- **Severidade**: Baixa / Média / Alta / Crítica
- **Risco resultante**: usar matriz em [`lib/risk-matrix.md`](../lib/risk-matrix.md)

Catálogo mínimo de riscos a avaliar:

| Risco | Vetor típico |
|---|---|
| Acesso não autorizado | RBAC ausente, credencial vazada |
| Vazamento / divulgação indevida | Bug, config errada, insider |
| Alteração indevida | Integridade comprometida |
| Perda / destruição | Falha de backup, ransomware |
| Uso fora da finalidade | Function creep |
| Reidentificação de dados anonimizados | Cruzamento, baixa entropia |
| Discriminação | Viés algorítmico (Art. 20) |
| Dano material/moral ao titular | Fraude, constrangimento |
| Não atendimento de direitos (Art. 18) | Dados em silos não mapeados |

### 5. Medidas mitigatórias

Para cada risco, propor controle. Referenciar [`controls/`](../controls/):

| Risco | Mitigação | Controle de referência |
|---|---|---|
| Acesso não autorizado | RBAC + MFA + audit log | [`controls/access-control-rbac.md`](../controls/access-control-rbac.md) |
| Vazamento | Criptografia AES-256 at-rest, TLS 1.2+ em trânsito, redação de PII em logs | [`controls/encryption.md`](../controls/encryption.md) |
| Reidentificação | k-anonimato, pseudonimização | [`controls/pets.md`](../controls/pets.md) |
| Discriminação | Fairness testing, intervenção humana, explicabilidade | [`workflows/adm-decisions-art20.md`](adm-decisions-art20.md) |
| Não atendimento Art. 18 | Mapa de dados + processo DSAR | [`workflows/dsar-direitos-titular.md`](dsar-direitos-titular.md) |

### 6. Risco residual

Após controles, recalcular probabilidade × severidade. **Documentar.**

| Status | Critério | Ação |
|---|---|---|
| Aceitável | Risco baixo | Aprovar tratamento |
| Tolerável | Risco médio com plano de redução | Aprovar com revisão em 6 meses |
| Inaceitável | Risco alto residual | Não prosseguir / consultar ANPD (Art. 38 parágrafo único) |

### 7. Consulta à ANPD (Art. 38 parágrafo único)

Se risco residual for alto e não puder ser mitigado:
- Documentar análise
- Considerar consulta prévia à ANPD
- Não há canal formal padrão, mas pode ser via ofício à Coordenação-Geral de Fiscalização

### 8. Aprovação e arquivamento

- DPO assina (parecer técnico)
- Patrocinador do projeto (negócio) assina (decisão de prosseguir)
- Jurídico revisa (parecer)
- Versão arquivada por **5 anos** + revisões

---

## Passo 0 — Triagem rápida

Antes do DPIA completo, faça **screening de 5 perguntas**:

1. Há dados sensíveis ou de menor? → Sim → **DPIA obrigatório**
2. Há decisão automatizada com efeito significativo? → Sim → **DPIA obrigatório**
3. Há monitoramento sistemático ou cruzamento? → Sim → **DPIA obrigatório**
4. Base legal é "legítimo interesse"? → Sim → **LIA + DPIA**
5. Tratamento envolve nova tecnologia (IA generativa, biometria)? → Sim → **DPIA obrigatório**

Se nenhum → registro simples no ROPA pode ser suficiente, mas documentar a triagem.

---

## Passo 1 — Mapear o tratamento (5 dias)

Workshop com:
- Product Owner (entende finalidade)
- Tech Lead (entende arquitetura)
- DPO (questiona base legal e proporcionalidade)
- Segurança (avalia controles)

Saída: seções 1, 2 e 3 do RIPD preenchidas.

---

## Passo 2 — Avaliar riscos (5 dias)

Usar matriz em [`lib/risk-matrix.md`](../lib/risk-matrix.md).

**Pessimismo controlado** — assuma vetor competente. Não subestime probabilidade só porque "não aconteceu ainda."

---

## Passo 3 — Desenhar mitigações (5 dias)

Princípios:
- Privacy by Design (Art. 46 §2º)
- Privacy by Default
- Minimização (Art. 6 III)
- Defesa em profundidade (não confie em um controle único)

---

## Passo 4 — Recalcular risco residual

Honestidade brutal. Se mitigação é "treinamento anual", isso reduz pouco. Se é "tokenização irreversível", reduz muito.

---

## Passo 5 — Revisão DPO + Jurídico

DPO valida:
- Base legal está correta?
- Finalidade é específica?
- Princípios LGPD respeitados?
- Mitigações são proporcionais?

Jurídico valida:
- Riscos contratuais (DPA com operador)
- Risco de litígio
- Compliance com normativos setoriais (BACEN, ANS, CVM, etc.)

---

## Passo 6 — Aprovação e arquivamento

Se aprovado:
- Vincular RIPD ao [`ROPA`](ropa.md)
- Definir ciclo de revisão (mín. anual ou em mudança material)
- Inserir métricas no monitoramento contínuo

Se reprovado:
- Voltar ao desenho (mudar escopo, base legal, tecnologia)
- OU consultar ANPD
- OU arquivar (não prosseguir)

---

## Casos especiais

### Vendor / SaaS sem controle direto

- Coletar **as informações que o vendor fornece** (TIA / SOC 2 / ISO 27001)
- Refletir limitações no DPIA
- Reforçar contratualmente via DPA

### Sistema legado sem documentação

- Engenharia reversa (logs, código, banco)
- Entrevistas com quem conhece
- Pode resultar em DPIA com "lacunas conhecidas" — explicitar

### Múltiplas finalidades no mesmo tratamento

- Fazer **uma seção por finalidade**
- Cada finalidade pode ter base legal diferente
- Não misturar (ex: marketing + execução de contrato em consent único)

---

## Referências legais

- Art. 5 XVII — definição de RIPD
- Art. 10 §3º — RIPD para legítimo interesse
- Art. 32 — pode ser solicitado pela ANPD
- Art. 38 — autoridade pode determinar
- Art. 50 §2º II d — boas práticas incluem RIPD

---

## Anti-padrões

| ❌ Erro | ✅ Correto |
|---|---|
| RIPD genérico copiado entre projetos | Específico para cada tratamento |
| Probabilidade "média" sempre por default | Justificada com dados/threat model |
| Mitigação = "implementar boas práticas" | Mitigação = controle específico com responsável |
| Aprovação só pelo DPO | DPO + patrocinador + jurídico |
| Arquivado e esquecido | Revisão anual + gatilhos de mudança |
| "Privacy by design" como bullet | Demonstrar nas decisões de arquitetura |
