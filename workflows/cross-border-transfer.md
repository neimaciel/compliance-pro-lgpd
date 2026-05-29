# Workflow — Transferência Internacional de Dados

> **Capítulo V LGPD (Art. 33-36) + Res. CD/ANPD 19/2024.**
> A regra é: **vedada**, salvo nos casos do Art. 33. TIA (Transfer Impact Assessment) é exigência da Res. 19/2024 para a maioria dos mecanismos.

---

## O que conta como transferência internacional

Qualquer envio, acesso remoto ou armazenamento de dados pessoais em **país diverso do Brasil**.

Casos comuns:
- SaaS hospedado nos EUA (AWS us-east-1, Google Cloud us-central1, Slack)
- Sub-operadores fora do BR (CDN, email, suporte 24/7)
- Funcionário em escritório no exterior acessando sistemas brasileiros
- Disaster recovery em região no exterior
- Análise de dados por matriz/holding no exterior

**Mesmo dado "acessado de fora" sem cópia é transferência** (jurisprudência ANPD em consonância com EDPB).

---

## SLA

| Marco | Prazo |
|---|---|
| TIA antes da transferência iniciar | Bloqueador |
| Revisão de TIA | Anual ou em mudança material |
| Atualização em mudança regulatória do país destino | 30 dias após conhecimento |

---

## Passo 1 — Identificar a transferência

Inventariar (a partir do [`ROPA`](ropa.md)):
- Para onde os dados vão (país, região)
- Que operador / controlador estrangeiro
- Categorias de dados (especial atenção a sensíveis)
- Volume e periodicidade
- Finalidade da transferência

---

## Passo 2 — Verificar nível adequado

A ANPD ainda não publicou (até 2026-05-28) lista oficial de **países com nível adequado** de proteção (Art. 35). Por padrão, **assumir que NÃO há**.

Verificar atualização em: https://www.gov.br/anpd/pt-br/assuntos/cooperacao-internacional

**Se ANPD reconhecer país adequado** → transferência permitida com base no Art. 33, I.

---

## Passo 3 — Escolher mecanismo (se não houver adequação)

Mecanismos autorizados (Art. 33 + Res. 19/2024):

| Mecanismo | Quando usar | Documento exigido |
|---|---|---|
| **Cláusulas-padrão contratuais** (Art. 33, II "a") | Operador-operador, controlador-operador, controlador-controlador | SCC publicado pela ANPD (Res. 19/2024 anexo) ou aprovado caso a caso |
| **Cláusulas contratuais específicas** (Art. 33, II "b") | Quando SCC padrão não se adequa | Submeter à ANPD para aprovação |
| **Normas Corporativas Globais** (BCR — Art. 33, II "c") | Grupos econômicos | Aprovação ANPD |
| **Selos / códigos de conduta** (Art. 33, II "d") | Setores regulamentados | Reconhecimento ANPD |
| **Cooperação jurídica internacional** (Art. 33, III) | Específico (judicial, fiscal) | Tratado/acordo |
| **Proteção da vida** (Art. 33, IV) | Emergência | Não exige documento prévio |
| **Autoridade pública** (Art. 33, V) | Cooperação intergovernamental | Caso a caso |
| **Execução de contrato** (Art. 33, VI) | Quando inerente ao serviço | Documentar |
| **Consentimento específico** (Art. 33, VIII) | Último recurso | Consent destacado, informado, específico, granular |

---

## Passo 4 — TIA (Transfer Impact Assessment)

Use template: [`templates/tia-transfer-impact.md`](../templates/tia-transfer-impact.md).

Estrutura:

### 4.1 Identificação
- Origem (Brasil) → Destino (país)
- Partes envolvidas
- Operador receptor + sub-operadores
- Localização exata dos data centers

### 4.2 Categorização de dados
- Categorias (Art. 5)
- Sensíveis? (Art. 11)
- Menores?
- Volume

### 4.3 Análise do regime jurídico do destino
- Lei de proteção de dados local existe?
- Equivalência com LGPD (princípios, direitos)
- Autoridade independente de fiscalização?
- Direitos dos titulares são exercíveis na prática?
- **Acesso por autoridades públicas estrangeiras** — possibilidade de requisição governamental sem due process equivalente?
  - EUA: FISA 702, CLOUD Act, NSL — risco elevado
  - China: Cybersecurity Law, Data Security Law, PIPL com obrigação de compartilhar com governo
  - Reino Unido: Investigatory Powers Act
- Disponibilidade de recursos judiciais

### 4.4 Risco residual
Mesmo com SCC, há risco se:
- Operador no destino pode ser obrigado a fornecer dados ao governo local sem permitir contestação
- Não há mecanismo para titular brasileiro acessar judiciário local

### 4.5 Medidas suplementares (Schrems II inspired)
- **Criptografia ponta-a-ponta** com chave mantida no Brasil
- **Pseudonimização** antes da transferência
- **Split processing** (parte processa BR, parte exterior, sem dado completo)
- **Cláusulas contratuais reforçadas** (ex: notificar antes de cumprir requisição governamental, contestar judicialmente)

### 4.6 Conclusão
- Transferência **aprovada** com mecanismo X + medidas suplementares Y
- OU **reprovada** → buscar alternativa (data residency no Brasil)
- OU **aprovada com restrições** (apenas dados não-sensíveis, com pseudonimização)

---

## Passo 5 — Implementar mecanismo

### Se SCC (mais comum):
- Anexar SCC ao DPA
- Garantir versão vigente ANPD
- Mapear sub-operadores e fazer SCC em cascata

### Se consentimento (Art. 33 VIII):
- Consent **destacado**, em camada separada
- Específico ao destino + finalidade + operador
- Informar riscos do país destino
- Permitir revogação
- Documentar consent ledger

---

## Passo 6 — Transparência ao titular

Atualizar política de privacidade:
- Quais dados saem do Brasil
- Para onde (país)
- Qual mecanismo (SCC, etc.)
- Quais salvaguardas
- Direitos do titular (ainda válidos)

---

## Passo 7 — Monitoramento

- Re-avaliar TIA **anualmente** ou se houver:
  - Mudança regulatória no destino (nova lei, decisão judicial)
  - Mudança no operador (aquisição, novo sub-operador)
  - Novo precedente da ANPD
  - Incidente envolvendo o operador
- Manter registro versionado

---

## Cenários comuns

### "Uso AWS, Google, Microsoft — o que faço?"

1. Aceitar **DPA + SCC padrão** desses fornecedores
2. Configurar **região brasileira** quando possível (sa-east-1, southamerica-east1, brazilsouth)
3. Para serviços globais (IAM, S3 multi-region) — TIA obrigatório
4. Documentar:
   - Quais buckets/recursos estão no Brasil
   - Quais são globais
   - Quais sub-processadores (AWS lista ~300+, Google ~500+)
   - Critérios para escolher

### "Cliente americano quer acessar relatórios de pacientes/clientes brasileiros"

- Dados sensíveis (saúde) — extrema atenção
- Não basta SCC — exigir medidas suplementares fortes
- Considerar **agregação/anonimização** prévia
- Avaliar se a transferência é mesmo necessária (princípio da minimização)

### "Matriz no exterior auditando filial brasileira"

- Pode-se justificar por execução de contrato/legítimo interesse
- TIA + SCC inter-grupo (BCR é ideal se grupo grande)
- Cuidado com dados de RH (sensíveis, sindicalização)

### "Fornecedor de email transacional (SendGrid, Mailgun) nos EUA"

- DPA + SCC do fornecedor
- Conteúdo do email pode conter dados sensíveis? Reavaliar.
- Considerar fornecedor com região BR

### "Plataforma de IA generativa (OpenAI, Anthropic, etc.)"

- Quando envia prompts contendo PII → transferência
- Verificar: dado é usado para treinamento? (DPA deve **proibir**)
- Verificar retenção (idealmente 0 dias / opt-out de logging)
- Pseudonimizar antes de enviar quando possível
- Considerar deployment local / via Bedrock-BR / Azure-BR / Vertex-BR

---

## Quando recusar a transferência

- Destino sem regime de proteção minimamente equivalente E sem mecanismo viável
- Operador no destino sem garantias suplementares E dado sensível em jogo
- Quando o risco para o titular é desproporcional à finalidade

---

## Métricas

| Métrica | Meta |
|---|---|
| % de transferências internacionais com TIA documentado | 100% |
| % com mecanismo válido (SCC/BCR/consent) | 100% |
| Tempo médio de TIA | < 10 dias |
| % revisões anuais executadas | 100% |
| Sub-operadores fora do BR mapeados | 100% |

---

## Referências legais

- **Art. 33** LGPD — hipóteses autorizadas
- **Art. 34** — definição de nível adequado pela ANPD
- **Art. 35** — atestação de cláusulas-padrão pela ANPD
- **Art. 36** — alterações em garantias requerem nova avaliação
- **Res. CD/ANPD 19/2024** — Regulamento de Transferência Internacional
  - Anexo I — Cláusulas-padrão contratuais
  - Define exigência de TIA
  - Define obrigação de revisão periódica

---

## Anti-padrões

| ❌ Erro | ✅ Correto |
|---|---|
| "EUA tem CCPA, então é ok" | Sem reconhecimento ANPD = sem adequação |
| "Usamos só Cloudflare, não tem problema" | Cloudflare é transferência internacional — TIA + SCC |
| "SCC assinado, problema resolvido" | SCC é necessário mas não suficiente — TIA avalia se é eficaz |
| "Dados criptografados, não conta" | Conta sim — chave fica onde? |
| "Operador é certificado ISO 27001" | Certificação não substitui mecanismo legal |
