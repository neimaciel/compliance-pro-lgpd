# Changelog

Todas as mudanças notáveis neste projeto serão documentadas aqui.

Segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e [SemVer](https://semver.org/lang/pt-BR/).

## [1.0.0] — 2026-05-28

### Adicionado
- **SKILL.md** — orquestrador adaptativo (DPO/Dev/Exec)
- **frameworks/lgpd.md** — Lei 13.709/2018 + Res. CD/ANPD 2/2022, 4/2023, 15/2024, 18/2024, 19/2024
- **9 workflows operacionais** com SLA real:
  - `dsar-direitos-titular.md` (Art. 18, 15 dias)
  - `breach-72h.md` (Art. 48, 72h)
  - `dpia-ripd.md` (Art. 38)
  - `ropa.md` (Art. 37)
  - `vendor-dpa.md` (Art. 39)
  - `cross-border-transfer.md` (Cap. V + Res. 19/2024)
  - `consent-ledger.md` (Art. 8)
  - `retention-disposal.md` (Art. 15-16)
  - `adm-decisions-art20.md` (Art. 20)
- **6 templates jurídicos PT-BR**:
  - `politica-privacidade.md`
  - `ropa-template.yaml`
  - `dpia-template.md`
  - `dpa-controller-processor.md`
  - `notificacao-anpd-incidente.md`
  - `resposta-dsar.md`
  - `tia-transfer-impact.md`
- **5 controles técnicos** com evidência:
  - `encryption.md`
  - `access-control-rbac.md`
  - `audit-logging.md`
  - `pets.md` (Privacy Enhancing Technologies)
  - `incident-response.md`
- **Scripts Python** (pii-scanner, retention-scanner, log-scanner, audit-log-integrity)
- **Scripts TypeScript** (cookie-checker, tls-checker, dependency-scanner)
- **lib/** — maturity model CMMI 1-5, matriz de risco, contatos ANPD
- **evidence/** — schema hash-chained append-only

### Notas
- Cobertura legal: LGPD Art. 1-65 + 5 resoluções ANPD vigentes
- Licença: AGPL-3.0

## [Unreleased]

### Roadmap v1.1
- GDPR + UK GDPR via crosswalk (reuso ~70% dos controles)
- Workflow específico para AI Act (em consulta no Brasil)

### Roadmap v1.2
- CCPA/CPRA + state laws (CO, VA, CT, UT)

### Roadmap v2.0
- ISO 27701 + SOC 2 mapping
- EU AI Act integration
