<div align="center">

# 🛡️ Compliance Pro — LGPD

### Meta-skill open-source de compliance LGPD **audit-grade** para Claude Code

*Workflows com SLA legal · templates jurídicos PT-BR · controles técnicos · scripts executáveis*

[![License](https://img.shields.io/badge/License-AGPL_3.0-2c5282?style=for-the-badge&logo=gnu)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-0e7c66?style=for-the-badge)](CHANGELOG.md)
[![LGPD](https://img.shields.io/badge/LGPD-Art._1--65_+_5_resoluções-1d4ed8?style=for-the-badge)](frameworks/lgpd.md)
[![Status](https://img.shields.io/badge/status-production_ready-22c55e?style=for-the-badge)](#)

[![Made for DPO](https://img.shields.io/badge/-DPO_%2F_Encarregado-374151?style=flat-square)](#para-quem-é)
[![Made for Devs](https://img.shields.io/badge/-Privacy_Engineers-374151?style=flat-square)](#para-quem-é)
[![Made for C-Level](https://img.shields.io/badge/-Board_%2F_C--Level-374151?style=flat-square)](#para-quem-é)
[![ANPD aligned](https://img.shields.io/badge/-ANPD_aligned-374151?style=flat-square)](frameworks/lgpd.md)

[**Início rápido**](#-quick-start) · [**Workflows**](#-workflows) · [**Templates**](#-templates) · [**Scripts**](#-scripts) · [**Maturidade CMMI**](lib/maturity-model.md)

</div>

---

## ✨ Por que usar

Workflows aqui são **runbooks com prazo legal embutido e evidência hash-chained gerada a cada passo**. Cada artefato carrega:

- ⏱️ **Timers reais** — 15 dias para DSAR, 72h para incidente
- 📜 **Citação legal exata** — Art. X + Resolução CD/ANPD aplicável em toda recomendação
- 🔗 **Evidence chain** — log append-only com SHA-256, detecta tampering
- 🤖 **Scripts auditáveis** — Python + TypeScript que rodam no seu código
- 🎯 **Modo adaptativo** — mesma skill atende DPO, Dev e C-level

---

## 👥 Para quem é

<table>
<tr>
<td width="33%" align="center">

### 👔 DPO / Encarregado

Gera **RIPD/DPIA**, responde **DSAR** no prazo, notifica **ANPD em 72h**, mantém **ROPA** atualizado, redige **DPA** com vendors, executa **TIA** internacional.

*Linguagem técnico-jurídica · Cita artigo + resolução · Minutas prontas*

</td>
<td width="33%" align="center">

### 💻 Privacy Engineer

Escaneia código atrás de **PII e secrets**, valida **TLS**, audita **cookies/trackers**, verifica **schema vs ROPA**, integra no **CI/CD**, mantém **evidence chain**.

*Type-safe · Estritamente versionado · Falha o build se necessário*

</td>
<td width="33%" align="center">

### 📊 C-Level / Board

Recebe **CMMI 1-5** de maturidade, **matriz de risco** quantitativa, **ROI** vs exposição a multa ANPD, **benchmarks** setoriais.

*Risco em R$ · KPIs mensuráveis · Linguagem executiva*

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Como skill do Claude Code

```bash
git clone https://github.com/neimaciel/compliance-pro-lgpd ~/.claude/skills/compliance-pro-lgpd
```

No Claude Code:

```
/compliance-pro-lgpd help          # menu interativo
/compliance-pro-lgpd dsar          # responder pedido de titular (15d)
/compliance-pro-lgpd breach        # iniciar resposta a incidente (72h)
/compliance-pro-lgpd dpia <projeto>
/compliance-pro-lgpd ropa
/compliance-pro-lgpd audit         # roda scanners em código local
/compliance-pro-lgpd maturity      # avalia CMMI da org
```

### Scripts standalone (sem Claude)

<table>
<tr>
<td width="50%">

**Python**

```bash
cd scripts/python
pip install -e .

# Detecta PII e secrets em código
pii-scan --target ./meu-projeto --fail-on critical

# Cruza schema SQL com ROPA
retention-scan --schema schema.sql --ropa ropa.yaml

# Verifica integridade do evidence log
audit-integrity verify --file evidence/log.jsonl
```

</td>
<td width="50%">

**TypeScript**

```bash
cd scripts/typescript
npm install

# Audita cookies/trackers da página
npx tsx src/cookie-checker.ts --url https://site.com.br

# Valida TLS
npx tsx src/tls-checker.ts --host api.empresa.com.br

# Flagueia deps com telemetria/tracking
npx tsx src/dependency-scanner.ts --pkg ./package.json
```

</td>
</tr>
</table>

---

## 📋 Workflows

Cada workflow é um **runbook operacional** com SLA real, evidência gerada e citação legal precisa.

| Workflow | Fundamento | SLA |
|---|---|:---:|
| [📨 **DSAR** — Direitos do titular](workflows/dsar-direitos-titular.md) | Art. 18 | **15 dias** |
| [🚨 **Breach 72h** — Incidente de segurança](workflows/breach-72h.md) | Art. 48 + Res. 15/2024 | **72 horas** |
| [📊 **DPIA/RIPD** — Avaliação de impacto](workflows/dpia-ripd.md) | Art. 38 | ~3 semanas |
| [📝 **ROPA** — Registro de operações](workflows/ropa.md) | Art. 37 | Pré-deploy |
| [🤝 **Vendor/DPA** — Operadores](workflows/vendor-dpa.md) | Art. 39, 42 | Pré-contrato |
| [🌐 **Transferência internacional** — TIA](workflows/cross-border-transfer.md) | Cap. V + Res. 19/2024 | Pré-transferência |
| [✅ **Consent ledger** — Gestão de consent](workflows/consent-ledger.md) | Art. 8 | Contínuo |
| [🗑️ **Retenção e descarte**](workflows/retention-disposal.md) | Art. 15-16 | Conforme política |
| [🤖 **Decisões automatizadas** — Art. 20](workflows/adm-decisions-art20.md) | Art. 20 | 15 dias revisão |

---

## 📄 Templates

Artefatos jurídicos PT-BR prontos para preencher placeholders e usar.

| Template | Caso de uso |
|---|---|
| [📜 Política de Privacidade](templates/politica-privacidade.md) | Site, app, B2C/B2B |
| [📊 ROPA — YAML versionável](templates/ropa-template.yaml) | Inventário em Git |
| [⚠️ DPIA/RIPD](templates/dpia-template.md) | Tratamento de alto risco |
| [🤝 DPA — Controlador × Operador](templates/dpa-controller-processor.md) | Vendor agreement |
| [🌐 TIA — Transfer Impact Assessment](templates/tia-transfer-impact.md) | Transferência internacional |
| [🚨 Notificação ANPD — Incidente](templates/notificacao-anpd-incidente.md) | Art. 48 |
| [📬 Resposta DSAR](templates/resposta-dsar.md) | Atender Art. 18 |

---

## 🔧 Scripts

Auditoria automatizada — integráveis em CI/CD.

### 🐍 Python

| Script | Função |
|---|---|
| [`pii-scan`](scripts/python/compliance_pro/pii_scanner.py) | Detecta PII e secrets em código (CPF validado, Art. 11 sensíveis, AWS/GitHub keys, JWT) |
| [`retention-scan`](scripts/python/compliance_pro/retention_scanner.py) | Cruza schema SQL com ROPA YAML para apontar lacunas |
| [`log-scan`](scripts/python/compliance_pro/log_scanner.py) | Detecta PII vazada em logs de aplicação |
| [`audit-integrity`](scripts/python/compliance_pro/audit_log_integrity.py) | Verifica hash chain do evidence log |

### 🟦 TypeScript

| Script | Função |
|---|---|
| [`cookie-check`](scripts/typescript/src/cookie-checker.ts) | Playwright headless valida CMP — trackers carregados sem consent |
| [`tls-check`](scripts/typescript/src/tls-checker.ts) | Valida TLS 1.2+, AEAD, validade de cert |
| [`dep-scan`](scripts/typescript/src/dependency-scanner.ts) | Flagueia npm deps com telemetria/tracking (GA, Sentry, etc.) |

### Integração CI/CD

Workflow GitHub Actions incluso em [`.github/workflows/lgpd-audit.yml`](.github/workflows/lgpd-audit.yml) — auditoria a cada push + agendada semanalmente.

---

## 🛡️ Controles

Documentação técnica + organizacional com citação legal e exemplos de evidência:

- 🔐 [**Criptografia**](controls/encryption.md) — AES-256, gestão de chaves, KMS, PCI
- 🔑 [**RBAC + ABAC**](controls/access-control-rbac.md) — least privilege, JIT, break-glass
- 📋 [**Audit logging**](controls/audit-logging.md) — append-only, hash chain, SIEM
- 🎭 [**PETs**](controls/pets.md) — anonimização, pseudonimização, DP, MPC, TEE
- 🚨 [**Incident response**](controls/incident-response.md) — CSIRT, tabletop, forense

---

## 📚 Base legal coberta

<table>
<tr>
<td>

**Lei 13.709/2018 (LGPD)** — Art. 1 a 65

- Princípios (Art. 6)
- Bases legais (Art. 7, 11)
- Direitos do titular (Art. 18)
- Decisões automatizadas (Art. 20)
- Registro / ROPA (Art. 37)
- DPIA (Art. 38)
- Operadores (Art. 39, 42)
- Encarregado (Art. 41)
- Transferência internacional (Cap. V)
- Segurança e incidentes (Art. 46-48)
- Sanções (Art. 52)

</td>
<td>

**Resoluções CD/ANPD**

- 🟢 Res. 2/2022 — Microempresas e startups
- 🟢 Res. 4/2023 — Dosimetria de sanções
- 🟢 Res. 15/2024 — Comunicação de incidente
- 🟢 Res. 18/2024 — Encarregado (DPO)
- 🟢 Res. 19/2024 — Transferência internacional

**Soft law relevante**
- ANPD — Guia de Anonimização
- NIST Privacy Framework
- ISO/IEC 27701

</td>
</tr>
</table>

---

## 🏗️ Estrutura

```
compliance-pro-lgpd/
│
├── 📘 SKILL.md                       Orquestrador adaptativo (DPO/Dev/Exec)
├── 📕 frameworks/lgpd.md              Source legal completo
│
├── 📋 workflows/                     9 runbooks operacionais com SLA
│   ├── dsar-direitos-titular.md     Art. 18 (15 dias)
│   ├── breach-72h.md                 Art. 48 (72h)
│   ├── dpia-ripd.md                  Art. 38
│   ├── ropa.md                       Art. 37
│   ├── vendor-dpa.md                 Art. 39
│   ├── cross-border-transfer.md      Cap. V + Res. 19/2024
│   ├── consent-ledger.md             Art. 8
│   ├── retention-disposal.md         Art. 15-16
│   └── adm-decisions-art20.md        Art. 20
│
├── 📄 templates/                     7 artefatos PT-BR jurídico
├── 🛡️  controls/                      5 controles técnicos
│
├── 🐍 scripts/python/                pii / retention / log / audit
├── 🟦 scripts/typescript/            cookie / tls / dep
│
├── 📊 lib/                           maturity CMMI, risk matrix, contatos
└── 🔗 evidence/                      hash-chained append-only log
```

---

## 🎯 Diferenciais

<table>
<tr>
<td width="33%">

#### 🧠 Adaptativo

Mesmo arquivo serve DPO (jargão jurídico), Dev (jargão técnico) e C-level (jargão executivo)

</td>
<td width="33%">

#### 🔗 Audit-grade

Toda decisão tem evidência **hash-chained** com timestamp imutável e detecção de tampering

</td>
<td width="33%">

#### 🔄 Cross-framework

Preparado para anexar **GDPR / CCPA / ISO 27701** mantendo single source of truth

</td>
</tr>
<tr>
<td>

#### ⏱️ SLA real

Runbooks com timers (**15 dias**, **72h**), escalation matrix e gatilhos de prorrogação documentados

</td>
<td>

#### 🤖 Executável

Python + TypeScript que escaneiam código real, não só documentos

</td>
<td>

#### 📜 Citação precisa

Cada controle cita **artigo exato + resolução ANPD** aplicável

</td>
</tr>
</table>

---

## 📈 Modelo de maturidade

Avaliação rápida em escala **CMMI 1-5** — ver [`lib/maturity-model.md`](lib/maturity-model.md) para detalhes.

| Nível | Status |
|:---:|---|
| **1** Inicial | Ad hoc · sem política · DPO informal · alto risco |
| **2** Repetível | Política publicada · DPO indicado · ROPA básico |
| **3** Definido | Processos padronizados · DPIA · DPA 100% · consent ledger |
| **4** Gerenciado | KPIs ao board · auditoria interna · privacy by design no SDLC |
| **5** Otimizado | Privacy como vantagem competitiva · PETs · contribuição setorial |

---

## 💡 Filosofia

Toda recomendação cita artigo da LGPD + resolução ANPD aplicável. Toda decisão gera entrada em evidência hash-chained. Templates vêm com placeholders explícitos `{{...}}` no lugar de "preencher conforme o caso". Scripts versionam o que escaneiam e falham o build quando passa do limiar.

Em contrapartida, fora do escopo da skill: litígio ativo, negociações contratuais de alto valor, transferência internacional sem TIA documentado e qualquer recomendação que não venha amarrada a artigo de lei. Para esses casos, ela monta o draft e marca `STATUS: AGUARDANDO REVISÃO JURÍDICA`.

---

## 🤝 Contribuir

Pull Requests bem-vindos. Veja [CONTRIBUTING.md](CONTRIBUTING.md).

Áreas com maior demanda:
- 📐 Refinamento de patterns (reduzir falsos positivos)
- 🏥 Runbooks setoriais (saúde, financeiro, educação, setor público)
- 🌎 Crosswalk para GDPR / UK GDPR
- 🤖 Casos específicos de IA generativa (LGPD + AI Act emergente)

---

## 📊 Roadmap

- **v1.0** — LGPD completo (atual)
- **v1.1** — GDPR + UK GDPR via crosswalk
- **v1.2** — CCPA/CPRA + state laws (CO, VA, CT, UT)
- **v2.0** — ISO 27701 + SOC 2 + EU AI Act

---

## 📄 Licença

**GNU AGPL v3.0** — ver [LICENSE](LICENSE).

✅ Uso comercial permitido
✅ Modificação permitida
✅ Distribuição permitida
⚠️ SaaS exige disponibilizar código modificado (copyleft de rede)

---

<div align="center">

**Atualizado em 2026-05-28**

Conforme **Lei 13.709/2018**, **Res. CD/ANPD 15/2024** (incidentes) e **Res. CD/ANPD 19/2024** (transferência internacional).

Mantenedor: [**@neimaciel**](https://github.com/neimaciel) — `nei@ampler.me`

[Reportar bug](../../issues/new?labels=bug) · [Solicitar feature](../../issues/new?labels=enhancement) · [Discussões](../../discussions)

</div>
