# Controle — Privacy Enhancing Technologies (PETs)

> Tecnologias que **reduzem ou eliminam o dado pessoal** mantendo utilidade.
> LGPD Art. 12 — dados anonimizados não são dados pessoais.
> ANPD vem reforçando que pseudonimização **não é** anonimização (Guia de Anonimização ANPD).

---

## Taxonomia

| Técnica | Reversibilidade | LGPD aplicável? |
|---|---|---|
| **Anonimização** real (k-anon ≥ 5, l-diversity, t-closeness) | Irreversível | Não (Art. 12) |
| **Pseudonimização** (hash com salt mantido) | Reversível com chave | Sim (continua PII) |
| **Tokenização** | Reversível com vault | Sim |
| **Mascaramento** (parcial) | Parcialmente reversível | Sim |
| **Diferential Privacy** | Estatisticamente irreversível | Não se aplicada corretamente |
| **Federated Learning** | Dados não saem do dispositivo | Sim (parcial) |
| **Homomorphic Encryption** | Computa sem decifrar | Sim |
| **Multi-Party Computation (MPC)** | Computa sobre dados distribuídos | Sim |
| **Trusted Execution Environments (TEE)** | Computa em enclave | Sim |
| **Synthetic Data** | Dados gerados artificialmente | Não, se gerada corretamente |

---

## Anonimização (Art. 12)

### Definição LGPD (Art. 5, III)
> "utilização de meios técnicos razoáveis e disponíveis no momento do tratamento, por meio dos quais um dado perde a possibilidade de associação, direta ou indireta, a um indivíduo"

### Critérios reconhecidos (Guia ANPD)
- **k-anonimato**: cada combinação de quasi-identificadores aparece para ≥ k indivíduos
- **l-diversity**: dentro de cada grupo k, há ≥ l valores diversos de atributo sensível
- **t-closeness**: distribuição dentro do grupo é próxima da global

### Quando NÃO é anonimização
- Remover apenas nome/CPF mas manter CEP completo + idade + sexo (re-identificação)
- Hash de identificadores sem agregação (continua identificável via re-cálculo)
- Embaralhar IDs (continua mapeável)

### Quando se aplica
- Dados para **BI / dashboards de produto**
- Compartilhamento com **pesquisa acadêmica**
- **Treinamento de ML** quando o objetivo é padrão agregado
- Métricas públicas

### Risco: reidentificação
- Cruzamento com base externa pode reidentificar mesmo k-anonimizado
- Documentar threat model
- Re-avaliar conforme novas bases públicas surgem

---

## Pseudonimização

### Quando usar
- Logs de aplicação que precisam de trace de "qual usuário causou X" sem expor PII
- Datasets de análise interna
- Compartilhamento com operador para finalidade limitada

### Implementação

```python
# HMAC com chave em KMS — determinístico (permite join)
def pseudonymize(cpf: str, kms_key: str) -> str:
    return hmac.new(kms_key, cpf.encode(), hashlib.sha256).hexdigest()
```

Determinístico = permite agrupamento por mesmo titular sem expor CPF.

### Cuidados
- Chave protegida em KMS
- Rotação da chave invalida joins históricos (planejar)
- Não basta para anonimização — quasi-identificadores continuam expondo

---

## Tokenização

### Diferença para pseudonimização
- **Pseudonimização**: derivada matematicamente (hash, encrypt)
- **Tokenização**: aleatória, mapeada em vault separado

```
CPF original         Token armazenado          Vault (separado)
123.456.789-00  →   TK_a8x9b2c4d6e7f0     →   { TK_a8x9b2c4d6e7f0: 123.456.789-00 }
```

### Uso
- Cartão de crédito (PCI-DSS exige)
- Substituir CPF/RG em sistemas analíticos
- Pseudonimização forte com revogação granular

---

## Mascaramento

| Tipo | Exemplo |
|---|---|
| **Estático** (write-time) | `cpf: "***.***.789-00"` armazenado |
| **Dinâmico** (read-time) | Banco guarda `12345678900`, app mostra `***.***.789-00` baseado em papel |
| **Format-preserving** | `cpf: "999.888.777-66"` — mesma estrutura, valor diferente |

### Quando usar
- Atendimento ao cliente vendo dados sensíveis em tela
- Ambientes de não-produção (staging, dev) com cópia de produção mascarada
- Relatórios executivos

### Anti-padrão
- Mascarar só no front-end (rede mostra valor real) → falha
- Mascarar e permitir click-to-reveal sem audit → falha

---

## Differential Privacy

Adiciona **ruído estatístico** controlado de modo que o output não revela presença/ausência de indivíduo específico.

Parâmetro central: **ε (epsilon)** — quanto menor, mais privacidade, menos utilidade.
- ε ≤ 1: forte
- 1 < ε ≤ 10: moderado
- ε > 10: fraco

### Quando usar
- Estatísticas públicas (Census US usa)
- Telemetria de produto (Apple, Google)
- Compartilhamento de tendências sem revelar indivíduos

### Implementações
- OpenDP (Harvard)
- TensorFlow Privacy
- PyDP
- Diffprivlib (IBM)

---

## Federated Learning

Modelo treina **no dispositivo do usuário**; só **gradientes agregados** vão para o servidor.

### Quando usar
- Mobile keyboards (predição de texto)
- Healthcare federado entre hospitais
- Casos onde dado bruto não pode sair

### Cuidados
- Gradientes podem vazar PII (model inversion attacks)
- Combinar com Differential Privacy ou Secure Aggregation
- Frameworks: TensorFlow Federated, PySyft, Flower

---

## Homomorphic Encryption (HE)

Computa sobre dados **cifrados** — nunca decifrados durante o processamento.

### Tipos
- **Partially HE**: 1 operação (ex: soma) — rápido
- **Somewhat HE**: poucas operações
- **Fully HE**: qualquer operação — lento (10⁴-10⁶× mais lento)

### Quando usa hoje
- Computação em nuvem com sensíveis (saúde, financeiro)
- Federated analytics
- Nichos com tolerância a latência

### Bibliotecas
- Microsoft SEAL
- HElib (IBM)
- OpenFHE
- Concrete (Zama)

---

## Multi-Party Computation (MPC)

N partes computam função sobre seus dados sem revelar inputs.

### Caso clássico
"Sou maior que você?" → resposta booleana sem revelar idade exata.

### Aplicações
- Análise de risco compartilhada entre bancos sem revelar carteiras
- Treinamento conjunto de modelo
- Auctioneers

---

## Trusted Execution Environments (TEE)

Hardware com enclave isolado onde dados são decifrados e computados sem expor ao host.

### Tecnologias
- Intel SGX (deprecated em servidores, vivo em desktops)
- AMD SEV-SNP
- AWS Nitro Enclaves
- Azure Confidential Computing
- Google Confidential VMs
- ARM TrustZone

### Trade-offs
- Performance overhead moderado
- Vulnerabilidades side-channel históricas (Foreshadow, Spectre variants)
- Vendor lock-in

---

## Synthetic Data

Geração de dataset **artificial** com propriedades estatísticas similares à base real.

### Quando usar
- Ambientes de não-produção (treinamento de equipe, testes)
- Compartilhamento de dataset para pesquisa
- ML training quando data sharing é proibido

### Riscos
- Modelo generativo pode "memorizar" e regurgitar (membership inference attack)
- Validar não-reidentificação (testes de privacy)

### Ferramentas
- Synthcity
- SDV (Synthetic Data Vault)
- Mostly AI
- Gretel.ai

---

## Como escolher

| Caso de uso | PET recomendada |
|---|---|
| "Quero estatística de uso sem expor titular" | Differential Privacy / k-anon |
| "Preciso unir dados com parceiro sem expor" | MPC / Tokenization com vault compartilhado |
| "Mobile app precisa treinar modelo" | Federated Learning + DP |
| "Compartilhar com pesquisador" | Anonimização (k-anon ≥ 5) ou synthetic |
| "Dev precisa de dados pra testar" | Synthetic ou produção mascarada |
| "Atendimento vê dados sensíveis em tela" | Mascaramento dinâmico + audit |
| "Cartão de crédito" | Tokenização PCI |
| "Vou treinar ML sobre dados sensíveis" | Federated + DP + (opc.) HE |

---

## Anti-padrões

| ❌ Erro | ✅ Correto |
|---|---|
| "Pseudonimizei = anonimizei" | São diferentes; pseudonimizado continua PII |
| Hash de email sem salt como "anonimização" | Reversível por rainbow table |
| Mascarar UI + dado bruto na resposta API | Mascarar no backend |
| DP com ε absurdo (50+) | Calibrar ε com data scientist |
| Synthetic data sem testes de privacy | Validar não-reidentificação |
| Tokenization vault no mesmo banco que dado | Vault separado + IAM diferente |
| Anonimização sem documentar técnica | Documentar Art. 12 — método e parâmetros |

---

## Evidência

```yaml
sistema: "analytics-dashboards"
tecnica_aplicada: "k-anonimato k=5 + remoção de quasi-identificadores"
quasi_identifiers_removed: ["cep_completo", "data_nascimento_dia", "ip"]
k_value: 5
l_diversity: 3
validacao_reidentificacao:
  data: "2026-04-10"
  metodo: "linkage attack contra base pública IBGE"
  resultado: "0 reidentificações sucesso em 10000 tentativas"
classificacao_pos_anonimizacao: "Não-pessoal (Art. 12 LGPD)"
revisao_periodica: "Anual + a cada nova base pública relevante"
```

---

## Referências

- Art. 12 LGPD
- ANPD — Guia Orientativo sobre Anonimização e Pseudonimização
- ENISA — Pseudonymisation Techniques and Best Practices (2019)
- ISO/IEC 20889:2018 — De-identification techniques
- NIST SP 800-188 — De-Identification of Personal Information
- The Algorithmic Foundations of Differential Privacy (Dwork & Roth)
