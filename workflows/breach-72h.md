# Workflow — Incidente de Segurança (72h)

> **Art. 48 LGPD + Resolução CD/ANPD 15/2024.**
> SLA: notificação à ANPD em **prazo razoável**, que a ANPD interpreta como **3 dias úteis (72h corridas)** após conhecimento do incidente que possa acarretar risco ou dano relevante aos titulares.

---

## Definição (Res. 15/2024, Art. 2)

**Incidente de segurança com dados pessoais**: evento adverso confirmado, relacionado à violação da segurança de dados pessoais, tais como acesso não autorizado, acidental ou ilícito, que resulte na destruição, perda, alteração, vazamento ou em qualquer forma de tratamento inadequado ou ilícito de dados.

**Não confunda com**: tentativa de intrusão bloqueada, vulnerabilidade não explorada, falha técnica sem comprometimento de dados — essas devem ser registradas internamente mas não disparam notificação.

---

## Critério de notificação obrigatória

Notifica ANPD **se** o incidente puder acarretar **risco ou dano relevante** aos titulares. Sinais:

| Sinal | Eleva probabilidade de "risco relevante" |
|---|---|
| Envolve **dados sensíveis** (Art. 5, II) | ⬆⬆⬆ |
| Envolve **crianças/adolescentes** | ⬆⬆⬆ |
| Volume > 1.000 titulares | ⬆⬆ |
| Dados financeiros (cartão, conta, score) | ⬆⬆ |
| Credenciais de autenticação | ⬆⬆ |
| Possibilita fraude / engenharia social | ⬆⬆ |
| Dado exposto publicamente (não só acessado por interno) | ⬆⬆ |
| Sem criptografia ou tokenização efetiva | ⬆⬆ |
| Possibilidade de discriminação | ⬆ |

Use [`lib/risk-matrix.md`](../lib/risk-matrix.md) para classificar. **Score ≥ Médio → notificar.**

---

## SLA

| Marco | Prazo a partir do **conhecimento** |
|---|---|
| War room ativado + timer iniciado | Imediato |
| Contenção inicial (corte de acesso, rotação de chaves) | < 4h |
| Avaliação preliminar de risco | < 12h |
| Decisão "notifica/não notifica" | < 24h |
| Comunicação ao DPO (se ainda não no loop) | < 4h |
| **Notificação ANPD via formulário** | **< 72h** (Res. 15/2024) |
| Comunicação aos titulares afetados | Tempo razoável após ANPD |
| Relatório de fechamento interno | < 30 dias |

---

## Passo 0 — Disparar war room (Hora 0)

Quando alguém na equipe percebe sinais de incidente:

```
[breach] DETECTADO em: {{ISO 8601 UTC}}
Deadline ANPD: {{+72h}}
Incidente ID: INC-{{YYYYMMDD-NNNN}}
```

Convocar imediatamente:
- DPO (mandatório)
- Sec/InfoSec lead
- Jurídico
- Engenharia (representante)
- Comunicação (preparar mas não acionar sem aprovação do DPO)
- C-level (informar; não bloqueador para iniciar contenção)

Abrir canal dedicado (Slack/Teams) — **não usar email** (rastro lento, vazamento da própria investigação).

Evidência inicial:
```json
{"ts":"2026-05-28T14:30:00Z","event":"breach_detected","incident_id":"INC-20260528-001","reporter":"<quem detectou>","initial_signals":"<o que viu>"}
```

---

## Passo 1 — Contenção (primeiras 4h)

**Antes de investigar a fundo, contenha**. Não preserva forense que vai virar problema maior.

Ações típicas:
- [ ] Cortar acesso comprometido (revogar token, desabilitar conta)
- [ ] Rotacionar chaves/credenciais expostas
- [ ] Tirar serviço afetado do ar (se necessário)
- [ ] Bloquear IPs de origem (se identificáveis)
- [ ] Preservar logs **antes** de qualquer ação que possa sobrescrever
- [ ] Tirar **snapshots forenses** dos sistemas afetados
- [ ] Pausar export/sincronização para sistemas externos

Toda ação de contenção → evidência:
```json
{"ts":"<>","event":"containment_action","incident_id":"INC-...","action":"rotated_aws_keys","by":"<engenheiro>"}
```

---

## Passo 2 — Triagem inicial (12h)

Responder estas perguntas:

1. **O que aconteceu?** (uma frase)
2. **Quando aconteceu?** (data início / data detecção / janela)
3. **Quantos titulares?** (estimativa com margem)
4. **Que dados?** (categorias — cadastrais, financeiros, sensíveis...)
5. **Dado estava criptografado/tokenizado?**
6. **Há evidência de exfiltração?** (logs de download, tráfego anômalo)
7. **Há evidência de exploração maliciosa?** (publicação, venda, uso fraudulento)
8. **Vetor?** (phishing? credencial vazada? bug? insider?)
9. **Quem está envolvido?** (operadores? sub-operadores? só nós?)

Se ainda não dá pra responder com confiança: **comunicar à ANPD assim mesmo** com o que sabe e atualizar conforme avança. Res. 15/2024 prevê **notificação preliminar + complementar**.

---

## Passo 3 — Decisão: notifica ou não? (< 24h)

Use a matriz:

| Cenário | Notifica ANPD? | Notifica titulares? |
|---|---|---|
| Dados criptografados com chave segura, exfil sem chave | Registra interno; pode dispensar | Não, se confirmado risco baixo |
| Dados em claro de 50 titulares, não sensíveis | Sim (volume baixo, mas risco moderado) | Sim |
| Dados sensíveis ainda que de 1 titular | Sim | Sim |
| Credenciais expostas | Sim | Sim + forçar reset |
| Vazamento público (já indexado) | Sim, imediatamente | Sim + comunicado público |
| Dúvida → erre para o lado de notificar | Sim | Caso a caso |

**Decisão registrada com justificativa por escrito.** Vira evidência:

```json
{"ts":"<>","event":"breach_decision","incident_id":"INC-...","decision":"notify","rationale":"<texto>","decided_by":"DPO","approved_by":"jurídico"}
```

---

## Passo 4 — Notificação à ANPD (< 72h)

Canal: **formulário no portal gov.br/anpd** — https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca

Conteúdo obrigatório (Res. 15/2024 Art. 7):

1. **Descrição do incidente** — natureza, circunstâncias, vetor (se conhecido)
2. **Quando ocorreu / quando foi conhecido** (datas)
3. **Categorias de dados afetados** (cadastrais, sensíveis, financeiros...)
4. **Volume de titulares afetados** (com margem de erro se ainda estimativa)
5. **Volume de dados** (registros)
6. **Riscos relacionados** (fraude, discriminação, dano material/moral)
7. **Medidas de segurança que existiam antes** (e por que não preveniram)
8. **Medidas adotadas** (contenção e correção)
9. **Razões para eventual atraso de notificação** (se > 72h)
10. **Se houve / haverá comunicação aos titulares** (e como)
11. **Dados do controlador + DPO** (nome, contato)

Use template: [`templates/notificacao-anpd-incidente.md`](../templates/notificacao-anpd-incidente.md).

**Notificação preliminar é OK.** Não atrasar para "ter tudo." Atualiza depois (Res. 15/2024 Art. 8 — comunicado complementar em até 20 dias).

Evidência:
```json
{"ts":"<>","event":"anpd_notified","incident_id":"INC-...","protocol":"<n.º protocolo ANPD>","type":"preliminary"}
```

---

## Passo 5 — Comunicação aos titulares

Quando? Tempo razoável após conhecimento do risco. Não esperar concluir investigação se há ação que o titular precisa tomar (trocar senha, monitorar cartão).

Conteúdo mínimo (Art. 48 §1º):
- Descrição da natureza dos dados afetados
- Informações sobre os titulares envolvidos
- Indicação das medidas técnicas e de segurança utilizadas
- Riscos relacionados
- Motivos da demora (se houve)
- Medidas adotadas para reverter / mitigar
- Recomendações ao titular (trocar senha, ativar 2FA, monitorar fraude)
- Canal de contato (DPO)

Canal:
- Email direto (preferencial — rastreável)
- Notificação in-app
- SMS (se telefone for o canal principal)
- Comunicado público (se número de afetados não permite individualização ou se já vazou publicamente)

**Não esconda atrás de jargão.** Linguagem clara. Linha 1 deve dizer o que aconteceu.

---

## Passo 6 — Investigação completa e remediação (até 30 dias)

Conduzir post-mortem técnico:
- Root cause
- Timeline detalhada
- O que falhou (controle, processo, pessoa)
- O que vai mudar

Saída: **Relatório de Incidente** arquivado por **5 anos** (referência: padrão de retenção de evidência regulatória).

---

## Passo 7 — Comunicado complementar à ANPD (até 20 dias após preliminar)

Se notificação inicial foi preliminar, **obrigatório** atualizar com informações completas. Evidência:

```json
{"ts":"<>","event":"anpd_notified","incident_id":"INC-...","protocol":"<>","type":"complementary"}
```

---

## Passo 8 — Lessons learned + ajuste de controles

- Atualizar [`controls/incident-response.md`](../controls/incident-response.md) se runbook tem gap
- Atualizar matriz de risco
- Re-rodar DPIA dos sistemas envolvidos
- Treinar equipe se vetor foi humano (phishing, engenharia social)
- Comunicar ao board (relatório executivo curto)

---

## Casos especiais

### Incidente em operador / fornecedor (não em nós)

- Acionar DPA — operador é **obrigado a comunicar imediatamente** (Art. 39)
- Controlador faz a notificação à ANPD (somos quem responde perante o titular)
- Considerar responsabilidade solidária para fins de Art. 42

### Ransomware

- Disponibilidade comprometida mas dados podem **não ter sido exfiltrados** — investigar antes
- Se atacante vaza amostra → tratar como exfiltração confirmada
- Comunicar ANPD mesmo se decidir não pagar (transparência)
- **Nunca** prometer impunidade ao atacante

### Insider malicioso

- Envolver RH + jurídico desde primeiro minuto
- Suspender acesso, preservar evidência forense
- Avaliar comunicação à polícia (crime de invasão / divulgação)
- Considerar Art. 42 (responsabilidade civil) versus o insider

### Dados de menor

- Acionar Conselho Tutelar / Ministério Público se houver dúvida sobre comunicação aos responsáveis
- Tom da comunicação aos titulares precisa ser ainda mais cuidadoso

### "Quase-incidente" (vulnerabilidade descoberta antes de exploração)

- Não exige notificação ANPD
- Exige registro interno + correção
- Disclosure responsável se reportada por externo (programa de bug bounty)

---

## Métricas (KPI)

| Métrica | Meta |
|---|---|
| MTTD (mean time to detect) | < 24h |
| MTTR (mean time to respond — contenção) | < 4h |
| % de notificações ANPD em < 72h | 100% |
| % de comunicação a titulares em < tempo razoável | 100% |
| Recorrência de mesmo vetor | 0 |

---

## Referências legais

- Art. 46 LGPD — segurança
- Art. 48 LGPD — comunicação de incidente
- Art. 50 LGPD — boas práticas e governança
- Res. CD/ANPD 15/2024 — regulamento de comunicação de incidente de segurança
- Res. CD/ANPD 4/2023 — dosimetria de sanção (incidente não comunicado pesa)
- Lei 12.737/2012 (Carolina Dieckmann) — invasão de dispositivo
- Marco Civil da Internet — guarda de logs

---

## Lista de contatos de plantão (preencher localmente)

```
DPO:                {{nome}} — {{telefone}} — {{email}}
Sec/CISO:           {{nome}} — {{telefone}}
Jurídico (sócio):   {{nome}} — {{telefone}}
Comunicação:        {{nome}} — {{telefone}}
Plantão eng:        {{nome}} — {{telefone}}
Forense externa:    {{empresa}} — {{telefone}}
ANPD (referência):  comunicado.incidentes@anpd.gov.br
```
