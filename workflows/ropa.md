# Workflow — ROPA (Registro de Operações de Tratamento)

> **Art. 37 LGPD** — *"O controlador e o operador devem manter registro das operações de tratamento de dados pessoais que realizarem..."*
>
> Documento vivo. Base de tudo: sem ROPA, não há DPIA, não há resposta a DSAR confiável, não há defesa perante ANPD.

---

## SLA

Não há prazo legal explícito para "criar pela primeira vez", mas a ANPD pode requisitar **a qualquer momento** (Art. 37 + Art. 32). Resposta esperada: **fornecer em até 5 dias úteis** após requisição.

| Marco | Cadência |
|---|---|
| Criação inicial | Antes de qualquer tratamento ir para produção |
| Atualização incremental | A cada novo tratamento (CI/CD com gate) |
| Revisão completa | Mínimo anual |
| Disponibilidade para ANPD | Em até 5 dias úteis após requisição |

---

## Estrutura de uma entrada de ROPA

Use template em [`templates/ropa-template.yaml`](../templates/ropa-template.yaml).

Cada **atividade de tratamento** = uma entrada. Campos mínimos:

```yaml
id: TRAT-2026-0042
nome: "Onboarding de cliente PJ — KYC"
versao: 1.3
ultima_revisao: 2026-05-28
proxima_revisao: 2027-05-28

controlador:
  razao_social: "{{Empresa}}"
  cnpj: "{{CNPJ}}"
  contato_dpo: "dpo@empresa.com.br"

operador_envolvido: # se aplicável
  - razao_social: "Acme KYC Ltda"
    cnpj: "{{CNPJ}}"
    dpa_assinado: true
    data_dpa: 2025-11-15

finalidade:
  primaria: "Verificação de identidade e antecedentes para abertura de conta"
  secundarias: [] # listar se houver — cada uma com base legal própria

base_legal:
  artigo: "Art. 7, V" # execução de contrato
  justificativa: "Necessário para celebração e execução do contrato de prestação de serviços"
  lia_aplicavel: false # se Art. 7, IX (legítimo interesse) → true + documento LIA

dados:
  categorias:
    - cadastrais: ["nome", "CPF", "RG", "endereço", "telefone", "email"]
    - dados_de_negocio: ["razão social CNPJ", "atividade", "faturamento"]
    - sensiveis: [] # se houver, justificar Art. 11
  volume_estimado: "~2.000 novos/mês"
  origem: "Coleta direta do titular via formulário"

titulares:
  categorias: ["pessoas físicas representantes legais de PJ"]
  inclui_vulneraveis: false # menores, idosos, doentes

operacoes:
  - coleta: "Form web"
  - transmissao: "TLS 1.3, JWT scoped"
  - armazenamento: "PostgreSQL on AWS (sa-east-1), AES-256 at-rest"
  - uso: "Validação KYC + score de risco"
  - compartilhamento: "Operador Acme + Receita Federal (consulta CPF)"
  - eliminacao: "Após 5 anos do encerramento contratual (obrig. legal CVM Inst. 301)"

retencao:
  prazo: "Vida do contrato + 5 anos"
  fundamento: "CVM Inst. 301, Art. 7 — guarda de documentos KYC"
  apos_prazo: "Eliminação automatizada via job mensal"

compartilhamento_terceiros:
  - parte: "Acme KYC Ltda"
    finalidade: "Verificação de antecedentes"
    base_legal: "Art. 7, V"
    contrato: "DPA-2025-0017"
  - parte: "Receita Federal do Brasil"
    finalidade: "Validação de CPF/CNPJ"
    base_legal: "Art. 7, II (obrigação legal — KYC)"

transferencia_internacional:
  ocorre: false
  # se true:
  # destino_pais: ""
  # nivel_adequado_anpd: false
  # mecanismo: "" # SCC, BCR, consentimento, etc.
  # documento_tia: ""

medidas_seguranca:
  controles_tecnicos:
    - "Criptografia AES-256 at-rest"
    - "TLS 1.3 in transit"
    - "RBAC com least privilege"
    - "MFA obrigatório para colaboradores"
    - "Logs imutáveis (write-only) com retenção 1 ano"
    - "Backup criptografado, restore testado trimestralmente"
  controles_organizacionais:
    - "Treinamento LGPD anual obrigatório"
    - "NDA + cláusula de privacidade nos contratos de trabalho"
    - "Política de mesa limpa"

decisao_automatizada:
  ocorre: true
  descricao: "Score de risco KYC com regras + ML"
  efeito_significativo_titular: true # afeta abertura de conta
  intervencao_humana: "Score abaixo de threshold → revisão manual obrigatória"
  explicabilidade: "Titular pode solicitar revisão (Art. 20) — workflow definido"
  workflow_ref: "workflows/adm-decisions-art20.md"

direitos_titular:
  canal: "dpo@empresa.com.br + form em /privacidade"
  workflow_ref: "workflows/dsar-direitos-titular.md"
  prazo_resposta: "15 dias (Art. 19)"

ripd_realizado:
  necessario: true
  ref: "RIPD-2026-0007"
  ultima_versao: 2026-04-12

incidentes_historicos: []

observacoes: |
  Sistema integra com Acme KYC via webhook. Falha de webhook gera retry com backoff;
  payload é criptografado em trânsito e logs sanitizam PII com hash SHA-256 dos identificadores.
```

---

## Passo a passo da construção

### Passo 1 — Inventariar atividades (discovery)

Não tente listar "todos os dados". Liste **finalidades de negócio** e a cada uma associe os dados que ela consome.

Métodos:
- Workshop com cada área (Marketing, Vendas, Produto, RH, Financeiro, Suporte, Eng, Jurídico)
- Análise de schema de DB (script `data-discovery.py`)
- Análise de integrações (lista de operadores, contratos)
- Análise de logs / pixels do site
- Análise de cookies (script `cookie-checker.ts`)

Saída: lista de 20–80 atividades típicas para empresa média.

### Passo 2 — Para cada atividade, preencher base legal

**Esta é a parte mais crítica e mais errada.** Para cada atividade, escolher **uma** base legal do Art. 7 (ou Art. 11 se sensível). Múltiplas finalidades = múltiplas bases.

Erros comuns:
- "Tudo é consentimento" — não. Consentimento é específico, revogável, e exige granularidade. Para execução de contrato → use Art. 7 V, não consentimento.
- "Legítimo interesse" sem LIA — exige documento de balanceamento (Art. 10 §3º)
- "Cumprimento de obrigação legal" sem citar a lei → cite a lei

### Passo 3 — Mapear operadores

Para cada operador (vendor que trata dados em seu nome):
- DPA assinado?
- Onde armazena? (jurisdição)
- Sub-operadores? (cadeia)
- Certificações de segurança? (SOC 2, ISO 27001)

Operador sem DPA = **violação contratual e LGPD**. Workflow [`vendor-dpa.md`](vendor-dpa.md).

### Passo 4 — Identificar transferências internacionais

Se algum operador / serviço armazena dados fora do Brasil → workflow [`cross-border-transfer.md`](cross-border-transfer.md).

### Passo 5 — Validar princípios

Para cada atividade, checar Art. 6 LGPD:
- Finalidade — específica?
- Adequação — coerente com finalidade?
- Necessidade — mínimo necessário?
- Livre acesso — titular consegue exercer direitos?
- Qualidade — dados exatos e atualizados?
- Transparência — explícito ao titular?
- Segurança — medidas implementadas?
- Prevenção — riscos avaliados?
- Não discriminação — não usado para fins ilícitos/abusivos?
- Responsabilização — evidências de compliance?

### Passo 6 — Gerar versão final + governança

- Aprovação DPO
- Ciclo de revisão (anual + gatilhos)
- Gate no CI/CD: novo tratamento exige entrada no ROPA antes do merge
- Armazenamento versionado (Git é ideal)

---

## Quem mantém

| Função | Responsabilidade |
|---|---|
| Donos de produto/área | Reportam novas atividades |
| DPO | Valida base legal + princípios |
| Engenharia | Implementa controles, atualiza fluxo de dados |
| Segurança | Atesta controles técnicos |
| Jurídico | Valida bases legais e contratos com operadores |

---

## Operador também mantém ROPA

Art. 37 — **operador também é obrigado**. Se você é operador para clientes, mantenha ROPA das atividades que executa em nome deles, mesmo que cada cliente tenha seu próprio ROPA do tratamento global.

---

## Como apresentar à ANPD

A ANPD pode requisitar via ofício. Resposta:
1. Cópia do ROPA (em formato legível — PDF + YAML/JSON anexo)
2. Política de governança em dados (Art. 50)
3. Evidência de revisão (logs de versionamento)
4. Indicação do DPO + contato

Não enviar dados pessoais reais — só **categorias**.

---

## Métricas (KPI)

| Métrica | Meta |
|---|---|
| % de atividades com ROPA | 100% (gate CI/CD) |
| % de operadores com DPA assinado | 100% |
| % de atividades com base legal documentada | 100% |
| Tempo médio entre nova atividade e entrada no ROPA | < 5 dias |
| % de atividades revisadas no ciclo anual | 100% |

---

## Anti-padrões

| ❌ Erro | ✅ Correto |
|---|---|
| Planilha Excel solta sem versionamento | YAML/JSON em repositório Git |
| ROPA com 5 entradas em empresa de 200 funcionários | Provavelmente incompleto — re-fazer discovery |
| Base legal "interesse legítimo" para tudo | Justificar; consentimento, contrato, obrigação legal cobrem ~70% dos casos |
| "Dados anonimizados" sem método documentado | Anonimização é técnica (k-anonimato, etc.) — comprovar |
| Operadores sem CNPJ ou contato no DPA | Inadmissível — re-fazer DPA |

---

## Referências legais

- Art. 37 — obrigação de manter registro
- Art. 32 — ANPD pode determinar publicação
- Art. 38 — pode determinar RIPD a partir do ROPA
- Art. 41 — encarregado dispõe do ROPA
- Art. 50 §2º II a — ROPA é boa prática
