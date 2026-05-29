# LGPD — Source legal de referência

> **Lei Geral de Proteção de Dados Pessoais** — Lei nº 13.709/2018 + alterações pela Lei nº 13.853/2019 + Lei nº 14.010/2020.
> **Atualizado:** 2026-05-28. Inclui resoluções vigentes ANPD: nº 2/2022, 4/2023, 15/2024, 18/2024, 19/2024.

Este arquivo é a **source-of-truth** legal usada pelos workflows. Não é tutorial — é índice rápido com artigos, definições, prazos e referências cruzadas para os runbooks.

---

## Sumário rápido

| Capítulo | Artigos | Conteúdo |
|---|---|---|
| I — Disposições preliminares | 1-6 | Aplicabilidade, definições, princípios |
| II — Tratamento de dados pessoais | 7-16 | Bases legais (Art. 7 e 11), eliminação (15, 16) |
| III — Direitos do titular | 17-22 | Acesso, retificação, exclusão (Art. 18); decisões automatizadas (Art. 20) |
| IV — Tratamento pelo Poder Público | 23-32 | Específico para administração pública |
| V — Transferência internacional | 33-36 | Países adequados, SCC, garantias (regulamentado pela Res. 19/2024) |
| VI — Agentes de tratamento | 37-45 | Controlador, operador, encarregado (DPO); ROPA (37); DPIA (38); DPA (39) |
| VII — Segurança e boas práticas | 46-54 | Segurança técnica (46); incidentes (48); boas práticas (50) |
| VIII — Fiscalização | 52-54 | Sanções administrativas |
| IX — Autoridade Nacional (ANPD) | 55-A a 59 | Competência da ANPD |
| X — Disposições finais | 60-65 | Vigência |

---

## Princípios (Art. 6) — checklist de aderência

Toda atividade de tratamento deve aderir aos 10 princípios. Em audit, cada um precisa de evidência:

| # | Princípio | Como demonstrar |
|---|---|---|
| I | **Finalidade** | Documentar finalidade explícita por atividade (no ROPA) |
| II | **Adequação** | Mostrar que o dado coletado é apto para a finalidade declarada |
| III | **Necessidade** | Princípio da minimização — só dados necessários |
| IV | **Livre acesso** | Canal funcional para titular consultar (Art. 18 IV) |
| V | **Qualidade dos dados** | Processo de retificação/atualização |
| VI | **Transparência** | Política de privacidade clara + comunicações |
| VII | **Segurança** | Controles técnicos (ver `controls/`) |
| VIII | **Prevenção** | Medidas pre-incidente (DPIA, treinamento) |
| IX | **Não discriminação** | Auditoria de algoritmos (Art. 20) |
| X | **Responsabilização e prestação de contas** | Evidence chain — toda decisão documentada |

---

## Bases legais (Art. 7 e 11) — quando usar cada uma

### Art. 7 — dados pessoais comuns

| Base | Quando usar | Exigências |
|---|---|---|
| **I — Consentimento** | Marketing, cookies não-essenciais, programas de fidelidade | Livre, informado, inequívoco, específico (Art. 8). Revogável (§5). Não cumulável como justificativa adicional |
| **II — Obrigação legal/regulatória** | Retenção de NF, KYC bancário, registro de acesso (Marco Civil Art. 15) | Citar lei/regulação específica |
| **III — Políticas públicas** | Apenas Poder Público | — |
| **IV — Estudos por órgão de pesquisa** | Pesquisa, observados anonimização | Sempre que possível, anonimizar |
| **V — Execução de contrato** | Cadastro de cliente, processamento de pagamento, entrega | Limitado a dados estritamente necessários |
| **VI — Exercício regular de direitos** | Processo judicial, arbitragem | Documentar processo em curso |
| **VII — Proteção da vida** | Emergências médicas | Excepcional |
| **VIII — Tutela da saúde** | Hospital, plano, telemedicina | Por profissional de saúde |
| **IX — Legítimo interesse** | Prevenção fraude, segurança, marketing direto a clientes ativos | **LIA obrigatória** (Legitimate Interest Assessment); titular pode opor-se (Art. 18 §2º) |
| **X — Proteção do crédito** | Bureaus | Limitado ao SCPC/Serasa |

### Art. 11 — dados pessoais sensíveis

Dados sensíveis = origem racial/étnica, convicção religiosa, opinião política, filiação sindical, dados genéticos, biométricos, saúde, vida sexual.

**Bases mais restritas:**
- I — Consentimento **específico e destacado** (não basta consentimento geral)
- II — Sem consentimento somente nas hipóteses específicas listadas (a-g)

### LIA — Legitimate Interest Assessment (obrigatório para base IX)

Documento que demonstra ponderação. Estrutura mínima:

1. **Finalidade do tratamento** (qual interesse legítimo? do controlador, terceiro, titular?)
2. **Necessidade** (não há base menos invasiva disponível?)
3. **Ponderação** (interesses do controlador × direitos do titular)
4. **Salvaguardas** (medidas que reduzem impacto: pseudonymization, opt-out fácil, transparência)
5. **Conclusão** (uso justificável? sob quais condições?)

Quando usar IX → sempre executar workflow `workflows/dpia-ripd.md` com módulo LIA.

---

## Direitos do titular (Art. 18) — prazo 15 dias

Workflow operacional: [`workflows/dsar-direitos-titular.md`](../workflows/dsar-direitos-titular.md)

| Inciso | Direito | Como executar |
|---|---|---|
| I | Confirmação da existência de tratamento | Resposta sim/não com lista de finalidades |
| II | Acesso aos dados | Export completo machine-readable + humano-legível |
| III | Correção de dados incompletos/inexatos | Edição + log da alteração |
| IV | Anonimização/bloqueio/eliminação de dados desnecessários ou excessivos | Verificar base legal, executar deleção segura |
| V | Portabilidade | Format estruturado (JSON, CSV) interoperável |
| VI | Eliminação dos dados tratados com consentimento | Exceto se houver outra base aplicável (ver §3 do Art. 16) |
| VII | Informação sobre uso compartilhado | Lista de operadores/sub-operadores |
| VIII | Informação sobre possibilidade de não fornecer consentimento e consequências | Antes da coleta |
| IX | Revogação do consentimento | Processo facilitado (Art. 8 §5) |

**Prazo:** 15 dias (Art. 19 §1º). Em casos justificados, comunicar prorrogação ao titular.

**Identificação do titular:** exigir comprovação razoável (CPF + documento + selfie em casos sensíveis). Não pode ser onerosa a ponto de inviabilizar exercício do direito (Art. 19 §3º).

---

## Incidentes de segurança (Art. 48) — prazo 72h (recomendado pela Res. 15/2024)

Workflow operacional: [`workflows/breach-72h.md`](../workflows/breach-72h.md)

### Critérios de gravidade (Res. CD/ANPD nº 15/2024, Art. 6)

Notificação obrigatória se o incidente envolver:

- Dados sensíveis (Art. 11)
- Dados de crianças/adolescentes
- Dados em escala (volume significativo)
- Dados que possam causar dano patrimonial ou moral relevante
- Dados financeiros, autenticação, ou que permitam fraude

### Conteúdo da notificação (Res. 15/2024 Art. 7)

A notificação à ANPD deve conter:

1. Descrição da natureza do incidente
2. Tipos e número aproximado de titulares afetados
3. Tipos e categorias dos dados pessoais afetados
4. Medidas técnicas e de segurança usadas para proteção
5. Riscos relacionados ao incidente
6. Razões da demora, se aplicável
7. Medidas adotadas para reverter/mitigar
8. Contato do encarregado/DPO

### Prazo

72 horas — contado a partir do **conhecimento** do incidente (não da ocorrência).

Quando informação não estiver completa em 72h, notificação parcial é aceita com complementação posterior (Res. 15/2024 Art. 8 §2).

### Notificação aos titulares

Sempre que o incidente puder acarretar **risco ou dano relevante**. Comunicação clara e individualizada (não apenas em site).

Template: [`templates/notificacao-anpd-incidente.md`](../templates/notificacao-anpd-incidente.md)

---

## Decisões automatizadas (Art. 20) — explicabilidade

Titular tem direito a:

1. **Solicitar revisão** de decisões tomadas unicamente com base em tratamento automatizado que afete seus interesses (perfilamento, score crédito, decisões de RH).
2. **Informações claras e adequadas** sobre os critérios e procedimentos usados.

ANPD pode realizar **auditoria** dos critérios (Art. 20 §2º).

Workflow: [`workflows/adm-decisions-art20.md`](../workflows/adm-decisions-art20.md)

Aplica-se também sob EU AI Act se houver clientes/usuários europeus.

---

## ROPA — Registro de Operações de Tratamento (Art. 37)

Obrigatório para controlador e operador. Conteúdo mínimo (regulamentado pela Res. CD/ANPD nº 2/2022):

1. Nome, contato, papel (controlador/operador)
2. Finalidades do tratamento
3. Categorias de titulares
4. Categorias de dados (incluindo se há sensíveis)
5. Base legal (Art. 7 ou 11 + inciso)
6. Compartilhamentos (com quem, por quê, base legal do compartilhamento)
7. Transferências internacionais (destino, mecanismo de garantia)
8. Prazos de retenção
9. Medidas de segurança técnicas e administrativas

Template machine-readable: [`templates/ropa-template.yaml`](../templates/ropa-template.yaml)

---

## DPIA / RIPD (Art. 38)

**Relatório de Impacto à Proteção de Dados Pessoais** — obrigatório quando:

- Tratamento baseado em legítimo interesse + dados sensíveis ou de criança/adolescente
- Tratamento sistemático em larga escala
- Decisões automatizadas com efeitos significativos
- Vigilância sistemática
- Tratamento envolvendo novas tecnologias

ANPD pode requisitar o RIPD a qualquer momento.

Workflow + template: [`workflows/dpia-ripd.md`](../workflows/dpia-ripd.md) + [`templates/dpia-template.md`](../templates/dpia-template.md)

---

## Encarregado / DPO (Art. 41)

Obrigatório para controlador (com exceções para agentes de pequeno porte — Res. CD/ANPD 2/2022 Art. 11).

Atribuições mínimas (Art. 41 §2):
- Receber reclamações e comunicações dos titulares
- Receber comunicações da ANPD
- Orientar funcionários e contratados sobre práticas LGPD
- Executar demais atribuições determinadas pelo controlador

**Identidade e canal de contato devem ser divulgados publicamente** (no site/política de privacidade).

---

## Operador e Sub-operadores (Art. 39)

Operador (processor) só pode tratar dados conforme instruções do controlador.

**DPA — Data Processing Agreement** — contrato entre controlador e operador. Template: [`templates/dpa-controller-processor.md`](../templates/dpa-controller-processor.md).

Sub-operadores exigem **autorização prévia** (geralmente cláusula no DPA permitindo lista atualizada).

Workflow: [`workflows/vendor-dpa.md`](../workflows/vendor-dpa.md)

---

## Transferência internacional (Capítulo V + Res. CD/ANPD 19/2024)

A Res. CD/ANPD 19/2024 (publicada 23/08/2024) **regulamentou totalmente** o capítulo V. Quatro mecanismos:

| Mecanismo | Aplicação | Documento |
|---|---|---|
| **Países adequados** | ANPD ainda não publicou lista vigente. Acompanhar | — |
| **Cláusulas Contratuais Padrão (CCPs)** | Modelo aprovado pela ANPD. Devem ser usadas integralmente | Anexo da Res. 19/2024 |
| **Cláusulas Contratuais Específicas** | Outras, mediante validação da ANPD | Pedido formal de aprovação |
| **Normas Corporativas Globais (NCG)** | Multinacionais | Aprovação ANPD |
| **Certificações, selos, códigos de conduta** | Mediante reconhecimento ANPD | — |
| **Consentimento específico** | Excepcional — risco para o titular | Titular deve estar plenamente informado |

**TIA — Transfer Impact Assessment** obrigatório quando o destino não tem nível de proteção adequado:

Workflow: [`workflows/cross-border-transfer.md`](../workflows/cross-border-transfer.md)
Template: [`templates/tia-transfer-impact.md`](../templates/tia-transfer-impact.md)

---

## Eliminação e retenção (Art. 15 e 16)

**Art. 15** — Términus do tratamento:
- I — Verificação de que finalidade foi alcançada / dados deixaram de ser necessários
- II — Fim do período de tratamento
- III — Comunicação do titular (revogação)
- IV — Determinação da ANPD por violação

**Art. 16** — Eliminação ao término, **exceto**:
- I — Cumprimento de obrigação legal/regulatória
- II — Estudo por órgão de pesquisa (com anonimização sempre que possível)
- III — Transferência a terceiro com observância dos requisitos
- IV — Uso exclusivo do controlador, anonimizado, vedado acesso de terceiro

**Retenção:** documentar prazos por categoria de dado. Workflow: [`workflows/retention-disposal.md`](../workflows/retention-disposal.md)

---

## Sanções (Art. 52)

| Sanção | Cabimento |
|---|---|
| Advertência | Primeira infração leve |
| Multa simples | Até 2% do faturamento do grupo no Brasil no último exercício, limitada a R$ 50 milhões por infração |
| Multa diária | Para descumprimento continuado |
| Publicização da infração | Após confirmada |
| Bloqueio dos dados | Até a regularização |
| Eliminação dos dados | — |
| Suspensão parcial do funcionamento do banco de dados | Até 6 meses, prorrogáveis por igual período |
| Suspensão do exercício da atividade de tratamento | Até 6 meses, prorrogáveis |
| Proibição parcial/total do exercício de atividades | Sancão mais grave |

**Dosimetria** regulamentada pela Resolução CD/ANPD nº 4/2023. Critérios incluem: gravidade, intencionalidade, vantagem auferida, cooperação, adoção de boas práticas (programa de governança em privacidade), etc.

Para audit, manter evidência de **adoção de boas práticas** (controles, treinamento, ROPA, DPIA, política) reduz dosimetria.

---

## Resoluções ANPD vigentes (consolidado)

| Resolução | Tema | Status |
|---|---|---|
| Res. CD/ANPD nº 2/2022 | Aplicação a agentes de pequeno porte | Vigente |
| Res. CD/ANPD nº 4/2023 | Dosimetria de sanções | Vigente |
| Res. CD/ANPD nº 15/2024 | Comunicação de incidentes de segurança | Vigente |
| Res. CD/ANPD nº 18/2024 | Encarregado de dados (DPO) | Vigente |
| Res. CD/ANPD nº 19/2024 | Transferência internacional | Vigente |

Outros documentos relevantes:
- **Guias técnicos ANPD**: Segurança (2021), Cookies (2022), Dados de Crianças/Adolescentes (2022)
- **Tomadas de subsídio**: Tratamento de dados pessoais por IA (2023-2024 — ainda sem regulamento)

---

## Como esta source-of-truth é usada

Workflows e templates referenciam este arquivo via **âncoras** (`#bases-legais-art-7-e-11`). Quando você editar o LGPD source, todos os arquivos que apontam para ele se beneficiam.

Mantenedor deve manter alinhamento com:
1. Diário Oficial — resoluções/portarias ANPD
2. Site oficial ANPD: https://www.gov.br/anpd
3. Jurisprudência de processos administrativos sancionatórios
