# Template — TIA (Transfer Impact Assessment)

> **Res. CD/ANPD 19/2024.** Documento obrigatório antes de transferir Dados Pessoais para o exterior, salvo as exceções específicas.
> Inspirado em Schrems II (CJEU C-311/18) — verificar não só o mecanismo legal mas a **eficácia prática** no destino.

---

# AVALIAÇÃO DE IMPACTO DA TRANSFERÊNCIA INTERNACIONAL DE DADOS

| Campo | Conteúdo |
|---|---|
| **Documento** | TIA-{{YYYY}}-{{NNNN}} |
| **Versão** | {{VERSAO}} |
| **Data** | {{DATA}} |
| **Próxima revisão** | {{DATA + 1 ANO}} |
| **Status** | [ ] Draft [ ] Aprovado [ ] Arquivado |

---

## 1. Identificação da Transferência

### 1.1 Partes
| Papel | Entidade | País |
|---|---|---|
| Exportador (Controlador BR) | {{RAZAO_SOCIAL}} | Brasil |
| Importador (Operador / Controlador estrangeiro) | {{NOME}} | {{PAIS}} |
| Sub-operadores | {{LISTAR}} | {{PAISES}} |

### 1.2 Tratamento avaliado
- **Tratamento (ROPA):** {{TRAT-YYYY-NNNN}}
- **Finalidade:** {{TEXTO}}
- **Frequência:** [ ] Pontual [ ] Recorrente [ ] Contínua

### 1.3 Dados envolvidos
| Categoria | Sensível? | Volume | Estado (claro/criptografado) |
|---|---|---|---|
| {{CATEGORIA}} | {{SIM/NAO}} | {{N}} | {{ESTADO}} |

### 1.4 Titulares
| Categoria | Inclui vulneráveis? |
|---|---|
| {{TEXTO}} | {{SIM/NAO}} |

---

## 2. Mecanismo Legal Escolhido (Art. 33 LGPD)

[ ] I — País com nível adequado reconhecido pela ANPD: {{PAIS}}
[ ] II.a — Cláusulas-padrão contratuais (SCC) ANPD — Anexo Res. 19/2024
[ ] II.b — Cláusulas contratuais específicas aprovadas pela ANPD — Protocolo: {{NUMERO}}
[ ] II.c — Normas Corporativas Globais (BCR) — Aprovação ANPD: {{REF}}
[ ] II.d — Selos / códigos de conduta reconhecidos pela ANPD
[ ] III — Cooperação jurídica internacional
[ ] IV — Proteção da vida
[ ] V — Autoridade pública
[ ] VI — Execução de contrato (necessária e diretamente relacionada)
[ ] VII — Cumprimento de obrigação legal
[ ] VIII — Consentimento específico, informado e destacado

**Justificativa da escolha:**
> {{TEXTO}}

---

## 3. Análise do Regime Jurídico do Destino

### 3.1 Lei de proteção de dados local
- País: {{PAIS}}
- Lei aplicável: {{NOME_DA_LEI}}
- Equivalência com LGPD: [ ] Alta [ ] Média [ ] Baixa
- Princípios protegidos: {{COMPARAR_COM_LGPD}}
- Autoridade independente de fiscalização: [ ] Sim [ ] Não
- Direitos efetivos dos titulares (acesso, correção, eliminação): [ ] Sim [ ] Parcialmente [ ] Não
- Mecanismo judicial de tutela: [ ] Sim [ ] Não

### 3.2 Acesso por autoridades públicas estrangeiras (risco "Schrems II")

| Mecanismo do país | Aplicável ao importador? | Garantias para titular estrangeiro |
|---|---|---|
| Requisição massiva / surveillance | {{SIM/NAO/POSSIVEL}} | {{SIM/NAO}} |
| Pedido individualizado com mandado | {{SIM/NAO}} | {{TIPO}} |
| Notificação ao titular após o fato | {{SIM/NAO}} | — |

Exemplos por país (atualizar com pesquisa atual no momento do TIA):
- **EUA:** FISA 702, EO 12333, CLOUD Act, NSL — risco elevado
- **China:** Cybersecurity Law, Data Security Law, PIPL com obrigação de compartilhar
- **Reino Unido:** Investigatory Powers Act 2016
- **Rússia:** Federal Law 374-FZ (Yarovaya)
- **UE:** GDPR + jurisprudência CJEU — risco baixo
- **Argentina/Uruguai:** decisão adequação UE — risco baixo

### 3.3 Histórico do importador
- Número de pedidos governamentais recebidos no último ano: {{N_OU_DESCONHECIDO}}
- Transparency report disponível: {{URL_OU_NAO}}
- Capacidade de contestar judicialmente: {{SIM/NAO/POLITICA}}
- Histórico de incidentes envolvendo o importador: {{LISTAR}}

---

## 4. Avaliação de Risco da Transferência

| Risco | Probabilidade | Severidade | Risco |
|---|---|---|---|
| Acesso governamental sem due process equivalente | {{P}} | Alta | {{R}} |
| Vazamento durante o tratamento no exterior | {{P}} | {{S}} | {{R}} |
| Impossibilidade prática de titular exercer Art. 18 | {{P}} | {{S}} | {{R}} |
| Sub-operadores adicionados sem controle | {{P}} | {{S}} | {{R}} |
| Mudança regulatória no destino enfraquecendo proteção | Baixa | Média | Baixo |
| {{OUTROS}} | | | |

---

## 5. Medidas Suplementares (Schrems II inspired)

Quando o mecanismo legal sozinho não basta, medidas técnicas e organizacionais reforçam:

### 5.1 Técnicas
- [ ] **Criptografia ponta-a-ponta** com chave **mantida exclusivamente no Brasil** (ou em país adequado)
- [ ] **Pseudonimização** antes da transferência — chave de re-identificação fica no Brasil
- [ ] **Split processing** — dados particionados de modo que o importador nunca tem o registro completo
- [ ] **Tokenização** com vault no Brasil
- [ ] **Computação confidencial / TEE** (Intel SGX, AMD SEV, AWS Nitro Enclaves)
- [ ] **Minimização extra** — só envia o mínimo necessário, não a base completa
- [ ] **Logging de acesso** com revisão pelo controlador

### 5.2 Organizacionais
- [ ] Cláusulas contratuais reforçadas:
  - Notificar antes de cumprir requisição governamental (quando legalmente possível)
  - Contestar judicialmente requisição genérica/desproporcional
  - Limitar funcionários do importador com acesso
  - Auditoria anual pelo controlador
- [ ] Política de mínimo privilégio explícita
- [ ] Treinamento de equipe do importador em LGPD
- [ ] Plano de contingência se importador for obrigado a entregar dados — controlador é notificado em janela mínima

### 5.3 Eficácia avaliada
Após medidas:
- O risco de acesso governamental sem due process é **suficientemente reduzido**? {{SIM/PARCIALMENTE/NAO}}
- O titular tem **recurso efetivo**? {{SIM/PARCIALMENTE/NAO}}

---

## 6. Conclusão

[ ] **Aprovada** — mecanismo + medidas suplementares são suficientes
[ ] **Aprovada com restrições**:
   - Apenas dados {{TIPO}} (não sensíveis, por exemplo)
   - Apenas mediante pseudonimização prévia
   - Reavaliação em {{DATA}}
[ ] **Reprovada** — risco residual inaceitável. Alternativas:
   - Mover tratamento para data residency no Brasil
   - Substituir importador por equivalente em país adequado
   - Não realizar a transferência

---

## 7. Transparência ao Titular

Atualizar política de privacidade:
- [ ] Quais dados saem do Brasil
- [ ] Para onde (país + nome do operador)
- [ ] Qual mecanismo legal aplicado
- [ ] Quais salvaguardas suplementares
- [ ] Como exercer direitos (canal LGPD)

---

## 8. Monitoramento Contínuo

| Gatilho de reavaliação | Cadência |
|---|---|
| Mudança regulatória no destino | 30 dias após conhecimento |
| Aquisição/fusão do importador | Imediato |
| Adição de sub-operador | Imediato |
| Incidente envolvendo o importador | Imediato |
| Mudança de precedente ANPD | 30 dias |
| Revisão periódica padrão | Anual |

---

## 9. Aprovação

| Função | Nome | Decisão | Data |
|---|---|---|---|
| DPO | {{NOME}} | [ ] Aprovado | {{DATA}} |
| Jurídico | {{NOME}} | [ ] Sem ressalvas | {{DATA}} |
| Segurança | {{NOME}} | [ ] OK | {{DATA}} |

---

## 10. Anexos

- **A** — Texto integral do mecanismo legal (SCC, BCR, etc.)
- **B** — DPA assinado com o importador
- **C** — Documentação técnica das medidas suplementares
- **D** — Análise jurídica do regime do país destino
- **E** — Histórico do importador (transparency reports, incidentes)

---

**Vinculado ao ROPA:** {{TRAT-YYYY-NNNN}}
**Hash:** {{SHA256}}
**Próxima revisão obrigatória:** {{DATA}}
