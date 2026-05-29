# Template — Notificação à ANPD de Incidente de Segurança

> **Art. 48 LGPD + Res. CD/ANPD 15/2024 (Art. 7).**
> Submeter via formulário oficial: https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca
>
> Este template segue a estrutura mínima exigida. Pode ser usado para preparar a submissão (formulário oficial é online).

---

**À AUTORIDADE NACIONAL DE PROTEÇÃO DE DADOS — ANPD**
**Coordenação-Geral de Fiscalização**

**Assunto:** Comunicado de Incidente de Segurança com Dados Pessoais — {{NOME_INCIDENTE}}
**Tipo de comunicado:** [ ] Preliminar  [ ] Complementar  [ ] Final
**Referência interna:** INC-{{YYYYMMDD-NNNN}}
**Data deste comunicado:** {{DATA_ENVIO}}

---

## 1. Identificação do Controlador

| Campo | Conteúdo |
|---|---|
| Razão social | {{RAZAO_SOCIAL}} |
| Nome fantasia | {{NOME_FANTASIA}} |
| CNPJ | {{CNPJ}} |
| Endereço | {{ENDERECO}} |
| Setor | {{SETOR}} |
| Porte | {{PORTE}} |
| Representante legal | {{NOME}} — {{CPF}} — {{CARGO}} |

### Encarregado (DPO)
| Campo | Conteúdo |
|---|---|
| Nome | {{NOME_DPO}} |
| Email | {{EMAIL_DPO}} |
| Telefone | {{TELEFONE_DPO}} |

### Operador envolvido (se aplicável)
| Campo | Conteúdo |
|---|---|
| Razão social | {{OPERADOR_RAZAO}} |
| CNPJ | {{OPERADOR_CNPJ}} |
| Papel no incidente | {{DESCREVER}} |

---

## 2. Descrição do Incidente

### 2.1 Natureza
Descrever em até 200 palavras:
- O que aconteceu (uma frase clara)
- Vetor identificado ou hipótese mais provável
- Sistemas afetados

> *Exemplo: "Em 2026-05-26, identificamos acesso não autorizado a uma instância do banco de dados de clientes via credencial de colaborador exposta em repositório público. O atacante exfiltrou aproximadamente 12.300 registros contendo nome, email, CPF e telefone, entre 2026-05-25 22:14 UTC e 2026-05-26 03:42 UTC, quando o acesso foi bloqueado."*

{{DESCRICAO_NATUREZA}}

### 2.2 Linha do tempo
| Momento | Evento |
|---|---|
| Data/hora do incidente | {{INICIO_INCIDENTE}} |
| Data/hora do conhecimento | {{DATA_CONHECIMENTO}} |
| Data/hora da contenção | {{DATA_CONTENCAO}} |
| Data/hora desta notificação | {{DATA_NOTIFICACAO}} |
| Tempo até detecção (MTTD) | {{HORAS}} |
| Tempo até contenção (MTTR) | {{HORAS}} |

### 2.3 Justificativa do prazo (se notificação ocorrer > 72h após conhecimento)
{{JUSTIFICATIVA_ATRASO_OU_NA}}

---

## 3. Dados Pessoais Envolvidos

### 3.1 Categorias de dados
- [ ] Cadastrais (nome, contato, documento)
- [ ] Financeiros (cartão, conta, score)
- [ ] Sensíveis (Art. 5, II): {{ESPECIFICAR}}
- [ ] De crianças/adolescentes
- [ ] Autenticação (credenciais, tokens)
- [ ] Localização
- [ ] Comportamentais (navegação, hábitos)
- [ ] Outros: {{ESPECIFICAR}}

### 3.2 Volume
- Número estimado de titulares afetados: {{NUMERO}} (com margem de ±{{MARGEM}}%)
- Número estimado de registros afetados: {{NUMERO}}

### 3.3 Categorias de titulares
{{CLIENTES_ATIVOS / EX_CLIENTES / FUNCIONARIOS / TERCEIROS / etc.}}

### 3.4 Estado dos dados no momento do incidente
- [ ] Em claro
- [ ] Pseudonimizados
- [ ] Criptografados — algoritmo: {{ALGORITMO}}, chave: {{LOCALIZACAO_DA_CHAVE}}, comprometida: {{SIM_NAO}}
- [ ] Tokenizados
- [ ] Anonimizados

---

## 4. Avaliação de Risco

### 4.1 Riscos potenciais ao titular
- [ ] Discriminação
- [ ] Fraude financeira
- [ ] Engenharia social / phishing direcionado
- [ ] Dano moral / constrangimento
- [ ] Dano material direto
- [ ] Roubo de identidade
- [ ] Risco à segurança física
- [ ] Outros: {{DESCREVER}}

### 4.2 Probabilidade de materialização
[ ] Baixa  [ ] Média  [ ] Alta  [ ] Já materializada (citar evidência: {{EVIDENCIA}})

### 4.3 Severidade estimada
[ ] Baixa  [ ] Média  [ ] Alta  [ ] Crítica

### 4.4 Risco global
[ ] Baixo  [ ] Médio  [ ] Alto  [ ] Crítico

---

## 5. Medidas Anteriores ao Incidente

Controles que existiam e razão pela qual não preveniram:

| Controle | Existia? | Por que falhou |
|---|---|---|
| Criptografia at-rest | {{SIM/NAO}} | {{NA_OU_EXPLICACAO}} |
| MFA para acessos administrativos | {{SIM/NAO}} | {{NA_OU_EXPLICACAO}} |
| Logs de auditoria | {{SIM/NAO}} | {{NA_OU_EXPLICACAO}} |
| Detecção de anomalias (SIEM) | {{SIM/NAO}} | {{NA_OU_EXPLICACAO}} |
| Segregação de redes | {{SIM/NAO}} | {{NA_OU_EXPLICACAO}} |
| Treinamento de segurança | {{SIM/NAO}} | {{NA_OU_EXPLICACAO}} |
| Rotina de revisão de acessos | {{SIM/NAO}} | {{NA_OU_EXPLICACAO}} |
| Plano de resposta a incidente | {{SIM/NAO}} | {{NA_OU_EXPLICACAO}} |

---

## 6. Medidas Adotadas

### 6.1 Contenção (imediata)
- [ ] Revogação de credenciais comprometidas
- [ ] Rotação de chaves e segredos
- [ ] Bloqueio de IPs suspeitos
- [ ] Isolamento de sistemas afetados
- [ ] Preservação de evidência forense (snapshots)
- {{OUTRAS}}

### 6.2 Investigação
- [ ] Forense interna (equipe própria)
- [ ] Forense externa contratada: {{EMPRESA}}
- [ ] Análise de logs concluída: {{SIM/NAO}}
- [ ] Vetor confirmado: {{SIM/NAO_HIPOTESE}}

### 6.3 Correção (estrutural)
- {{LISTAR_MUDANCAS_DEFINITIVAS}}

### 6.4 Comunicação aos titulares
- [ ] Em andamento — canal: {{EMAIL / SMS / SITE / IN_APP}}
- [ ] Planejada para: {{DATA}}
- [ ] Concluída em: {{DATA}}
- [ ] Não aplicável — justificativa: {{TEXTO}}

### 6.5 Outras autoridades comunicadas
- [ ] Banco Central
- [ ] ANS
- [ ] CVM
- [ ] Polícia Federal / Polícia Civil
- [ ] Ministério Público
- [ ] Outros: {{ESPECIFICAR}}

---

## 7. Recomendações Fornecidas aos Titulares

Listar as orientações práticas dadas:
- {{TROCAR_SENHA}}
- {{ATIVAR_2FA}}
- {{MONITORAR_CARTAO}}
- {{NAO_CLICAR_EM_LINKS_DESCONHECIDOS}}
- {{ATENDIMENTO_DEDICADO_DISPONIVEL}}

---

## 8. Documentos Anexos

- [ ] Relatório técnico de investigação (parcial ou final)
- [ ] Cópia da comunicação aos titulares
- [ ] Logs relevantes (sanitizados)
- [ ] Política de segurança da informação aplicável
- [ ] RIPD do tratamento afetado, se houver
- [ ] DPA com operador, se incidente em operador

---

## 9. Declaração e Assinatura

Declaramos, sob as penas da lei, que as informações prestadas refletem o conhecimento que temos sobre o incidente nesta data, e nos comprometemos a:

- Atualizar este comunicado com informações complementares em até 20 dias (Res. 15/2024 Art. 8), caso esta seja preliminar
- Cooperar plenamente com eventuais determinações desta Autoridade
- Manter registro do incidente e das medidas adotadas por **mínimo 5 anos**

{{LOCAL}}, {{DATA}}.

___________________________________
**{{NOME_REPRESENTANTE_LEGAL}}**
{{CARGO}}
{{RAZAO_SOCIAL}}
CNPJ {{CNPJ}}

___________________________________
**{{NOME_DPO}}**
Encarregado de Proteção de Dados
{{EMAIL_DPO}} — {{TELEFONE_DPO}}

---

### Anexo I — Histórico de comunicados deste incidente

| Versão | Data | Tipo | Responsável | Hash do documento |
|---|---|---|---|---|
| 1 | {{DATA}} | Preliminar | {{NOME_DPO}} | {{SHA256}} |
| 2 | {{DATA}} | Complementar | {{NOME_DPO}} | {{SHA256}} |
| 3 | {{DATA}} | Final | {{NOME_DPO}} | {{SHA256}} |

---

*Este documento foi gerado a partir do template `compliance-pro-lgpd/templates/notificacao-anpd-incidente.md`.
Fundamento: LGPD Art. 48 + Res. CD/ANPD 15/2024.*
