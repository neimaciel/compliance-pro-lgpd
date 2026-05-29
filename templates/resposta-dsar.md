# Template — Resposta a Pedido de Titular (DSAR)

> Use o bloco apropriado conforme o direito exercido. Linguagem clara. Sempre citar o artigo da LGPD.
> Fundamento: Art. 19 §1º (15 dias) + Art. 18.

---

## Cabeçalho padrão

**De:** {{NOME_DPO}} — Encarregado de Proteção de Dados
**Para:** {{NOME_TITULAR}} — {{EMAIL_TITULAR}}
**Assunto:** Resposta ao seu pedido de [{{TIPO}}] — Ref. {{TICKET_DSAR}}
**Data:** {{DATA_RESPOSTA}}

Prezado(a) {{PRIMEIRO_NOME}},

Recebemos seu pedido em {{DATA_RECEBIMENTO}}, referente a [{{TIPO_DIREITO}}] previsto no Art. 18 da Lei Geral de Proteção de Dados (Lei nº 13.709/2018 — LGPD).

Após verificação de sua identidade e análise técnica, informamos:

---

## Bloco A — Acesso e confirmação (Art. 18, I e II)

Confirmamos que tratamos dados pessoais seus para as seguintes finalidades:

| Finalidade | Base legal | Operadores envolvidos |
|---|---|---|
| {{FINALIDADE_1}} | {{ART_X}} | {{OPERADORES}} |
| {{FINALIDADE_2}} | {{ART_X}} | {{OPERADORES}} |

**Categorias de dados que tratamos sobre você:**
- Cadastrais: {{LISTAR}}
- Transacionais: {{LISTAR}}
- Comportamentais: {{LISTAR}}
- {{OUTRAS}}

**Em anexo:** export completo de seus dados em formato:
- [ ] PDF (humano-legível) — `dsar-{{TICKET}}.pdf`
- [ ] JSON / CSV (machine-readable, para portabilidade) — `dsar-{{TICKET}}.json`

**Tempo de retenção previsto:** {{PRAZO}} — fundamento: {{LEI_OU_FUNDAMENTO}}.

---

## Bloco B — Correção (Art. 18, III)

Após validação, atualizamos os seguintes dados conforme solicitado:

| Campo | Antes | Depois | Data da alteração |
|---|---|---|---|
| {{CAMPO}} | {{VALOR_ANTERIOR}} | {{VALOR_NOVO}} | {{TIMESTAMP}} |

Essa alteração foi propagada para nossos sistemas internos e operadores em até 24 horas.

---

## Bloco C — Eliminação (Art. 18, VI)

### C.1 — Eliminação concluída
Eliminamos os seguintes dados em {{DATA_ELIMINACAO}}:
- {{LISTAR_CATEGORIAS_ELIMINADAS}}

**Sistemas afetados:** {{LISTAR}}
**Operadores notificados para eliminação correspondente:** {{LISTAR}}
**Backups:** dados permanecem em backups até expirarem em {{DATA_EXPIRACAO_BACKUP}} (não são acessados durante esse período).

Anexo: certidão de eliminação `cert-elim-{{TICKET}}.pdf`.

### C.2 — Eliminação parcial
Eliminamos {{CATEGORIAS_ELIMINADAS}}.

Não pudemos eliminar {{CATEGORIAS_MANTIDAS}} por força de:
> {{FUNDAMENTO_LEGAL — Ex: Art. 16, I LGPD c/c Art. 7º da Instrução CVM 301/1999 — guarda obrigatória de documentos KYC pelo prazo de 5 anos após o encerramento do relacionamento.}}

Esses dados serão eliminados automaticamente em {{DATA_FUTURA}}.

### C.3 — Eliminação negada
Não pudemos atender ao pedido de eliminação porque os dados continuam necessários para:

> {{FUNDAMENTO — citar Art. 16 LGPD + lei específica}}

Você pode discordar dessa análise contestando perante a ANPD: https://www.gov.br/anpd/pt-br/canais_atendimento/cidadao

---

## Bloco D — Portabilidade (Art. 18, V)

Em anexo, enviamos seus dados em formato interoperável (`dsar-port-{{TICKET}}.json`), estruturado conforme:
- Esquema: {{NOME_ESQUEMA — Ex: Data Transfer Project / OpenAPI custom}}
- Codificação: UTF-8
- Hash de integridade (SHA-256): {{HASH}}

A portabilidade abrange dados que tratamos com base em **{{BASE_LEGAL}}** ({{CONSENTIMENTO_OU_CONTRATO}}). Dados tratados com outras bases legais não são objeto de portabilidade, conforme Art. 18 V.

---

## Bloco E — Revogação de consentimento (Art. 8 §5º + Art. 18, IX)

Sua revogação foi registrada em {{TIMESTAMP}} e propagada para todos os sistemas que dependiam daquele consentimento, dentro de 24 horas:

| Sistema/Operador | Status |
|---|---|
| {{NOME}} | Revogação confirmada em {{DATA}} |

Continuamos tratando dados seus apenas com base nas hipóteses do Art. 7 LGPD diversas do consentimento, conforme detalhamos em nossa Política de Privacidade ({{URL}}).

---

## Bloco F — Compartilhamento (Art. 18, VII)

Seus dados foram compartilhados com:

| Parte | Finalidade | Base legal | Categorias compartilhadas |
|---|---|---|---|
| {{NOME}} | {{FINALIDADE}} | {{ART_X}} | {{CATEGORIAS}} |

Todos os compartilhamentos estão amparados em contratos (DPA) com obrigações de confidencialidade e segurança.

---

## Bloco G — Revisão de decisão automatizada (Art. 20)

Sobre a decisão automatizada de {{DATA}} relativa a {{DESCREVER}}:

**Lógica utilizada (em linguagem clara):**
{{EXPLICACAO_DO_MODELO_E_CRITERIOS}}

**Categorias de dados consideradas:**
{{LISTAR}}

**Pesos relativos (mais determinantes):**
1. {{FATOR_1}}
2. {{FATOR_2}}
3. {{FATOR_3}}

**Resultado da revisão humana realizada em {{DATA_REVISAO}}:**
- [ ] Decisão **mantida** — fundamento: {{TEXTO}}
- [ ] Decisão **revertida** — novo resultado: {{DESCREVER}}

Você pode, ainda, contestar judicialmente ou junto à ANPD.

---

## Bloco H — Quando o pedido foi negado

Não pudemos atender ao seu pedido pelas seguintes razões fundamentadas:

> {{FUNDAMENTO — citar artigo LGPD + circunstância}}

Você tem direito de:
1. Reapresentar o pedido com elementos adicionais
2. Reclamar à ANPD (link acima)
3. Buscar tutela jurisdicional

---

## Bloco I — Quando precisamos prorrogar (excepcional)

Por razões {{TÉCNICAS / COMPLEXIDADE / VOLUME}}, prorrogamos a análise por {{DIAS}} dias. Prazo final de resposta: {{NOVA_DATA}}.

Comunicamos esta prorrogação dentro do prazo original (15 dias) conforme Art. 19 §1º.

---

## Encerramento padrão

Caso haja qualquer dúvida sobre esta resposta ou queira solicitar esclarecimentos adicionais, basta responder a este email ou entrar em contato pelo canal {{EMAIL_DPO}}.

Você também pode, a qualquer tempo, apresentar reclamação à **Autoridade Nacional de Proteção de Dados (ANPD)**:
https://www.gov.br/anpd/pt-br/canais_atendimento/cidadao

Atenciosamente,

**{{NOME_DPO}}**
Encarregado de Proteção de Dados (DPO)
{{RAZAO_SOCIAL}}
{{EMAIL_DPO}} — {{TELEFONE_DPO}}

---

**Referência interna:** {{TICKET_DSAR}}
**Hash desta resposta (SHA-256):** {{HASH}}
**Prazo legal cumprido:** {{DIAS_ATE_RESPOSTA}} dias (Art. 19 §1º LGPD)
