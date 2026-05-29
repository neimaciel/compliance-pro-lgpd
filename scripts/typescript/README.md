# compliance-pro-lgpd — TypeScript scripts

Scripts Node/TS para auditoria runtime de compliance LGPD: cookies, TLS e dependências.

## Instalação

```bash
cd scripts/typescript
npm install
npx playwright install chromium    # apenas se for usar cookie-check
npm run build
```

## Comandos

### `cookie-check` — Auditoria de cookies/trackers

```bash
npx tsx src/cookie-checker.ts --url https://meusite.com.br --report cookies.json
npx tsx src/cookie-checker.ts --url https://meusite.com.br --fail-on-violation
```

Carrega o site com Playwright headless e inspeciona:
- Cookies setados **antes de qualquer consent** (deveriam ser apenas essenciais)
- Requisições para domínios de tracking conhecidos (Google Analytics, Meta Pixel, LinkedIn Insight, etc.)
- Flag para CMP que não está bloqueando trackers até opt-in

Base legal: **Art. 7 I + Art. 8 LGPD** — cookies não-essenciais exigem consent prévio.

### `tls-check` — Validação TLS

```bash
npx tsx src/tls-checker.ts --host api.empresa.com.br --report tls.json
npx tsx src/tls-checker.ts --hosts hosts.txt --fail-on-violation
```

Valida:
- Versão TLS (mínimo 1.2)
- Cipher suite (rejeita RC4, DES, NULL; recomenda AEAD: GCM/CHACHA20)
- Validade do certificado (alerta < 30 dias)
- Cadeia de confiança

Base: **LGPD Art. 46** — segurança em trânsito.

### `dep-scan` — Auditoria de dependências npm

```bash
npx tsx src/dependency-scanner.ts --pkg ./package.json --report dep.json
npx tsx src/dependency-scanner.ts --pkg ./package.json --fail-on-finding
```

Flagueia dependências conhecidas que:
- Enviam **telemetria por padrão** (Next.js, Firebase)
- São **trackers/analytics** que exigem consent (GA, Mixpanel, Amplitude, Hotjar, FullStory, LogRocket)
- Fazem **chamadas a terceiros** com PII potencial (Sentry, Datadog RUM, GCP logging)

Para cada uma, retorna nota legal: configurar sanitização, fechar DPA, fazer TIA se transferência internacional.

## Integração CI/CD

```yaml
- name: Dependency scan
  run: npx tsx scripts/typescript/src/dependency-scanner.ts --pkg ./package.json --fail-on-finding

- name: TLS check
  run: npx tsx scripts/typescript/src/tls-checker.ts --hosts hosts.txt --fail-on-violation
```

## Licença

AGPL-3.0
