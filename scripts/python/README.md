# compliance-pro-lgpd — Python scripts

Scripts executáveis para auditoria de compliance LGPD em código, schemas e logs.

## Instalação

```bash
cd scripts/python
pip install -e .
```

## Comandos

### `pii-scan` — Detecta PII e segredos em código

```bash
pii-scan --target /path/to/project --report report.json
pii-scan --target . --fail-on critical    # exit 2 se houver findings críticos
pii-scan --target . --severity high       # apenas high+
```

Detecta padrões brasileiros: CPF (com validação check digit), CNPJ, RG, CNH, telefone, email, CEP, dados bancários, cartão de crédito, PIS, título de eleitor, passaporte, placa de veículo.

Detecta dados sensíveis (Art. 11): saúde, biometria, raça/etnia, religião, opinião política, orientação sexual, filiação sindical (via heurística de palavras-chave).

Detecta secrets: AWS keys, GitHub tokens, OpenAI/Anthropic keys, JWT, chaves privadas.

### `retention-scan` — Audita schema vs ROPA

```bash
retention-scan --schema schema.sql --ropa ../../ropa-prod.yaml --report report.json
```

Cruza colunas com PII no schema SQL contra atividades documentadas no ROPA YAML. Aponta:
- Colunas com PII não mapeadas no ROPA
- Colunas com dados sensíveis (Art. 11) sem controles documentados

### `log-scan` — Detecta PII em logs de aplicação

```bash
log-scan --target /var/log/myapp --report report.json
log-scan --target ./logs --fail-on high
```

Escaneia logs (incluindo `.gz`) procurando PII vazada. PII em logs operacionais é violação do princípio da segurança (Art. 46) e pode caracterizar incidente (Art. 48).

### `audit-integrity` — Verifica hash-chain de evidence log

```bash
audit-integrity verify --file evidence/log.jsonl
audit-integrity append --file evidence/log.jsonl --event '{"event":"dsar_received","ticket":"DSAR-001"}'
```

Implementa o esquema hash-chained descrito em [`evidence/manifest.md`](../../evidence/manifest.md):
- `hash_self = sha256(canonical_json(record sem hash_self))`
- `hash_prev` aponta para o `hash_self` do registro anterior
- Verificação detecta tampering ou truncamento

## Integração CI/CD

```yaml
# .github/workflows/lgpd-audit.yml
name: LGPD Audit
on: [push, pull_request]
jobs:
  pii-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install compliance-pro-lgpd
      - run: pii-scan --target . --fail-on critical
```

## Limitações

- Regex-based: pode ter falsos positivos. Use `--include-tests=false` (padrão) para reduzir ruído de fixtures.
- Não substitui análise jurídica — é triagem técnica.
- Para sensitivity scanning real (Art. 11), considere combinar com NLP/LLM em pipeline separado.

## Licença

AGPL-3.0 — ver [LICENSE](../../LICENSE).
