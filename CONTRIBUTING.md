# Contribuindo

Obrigado por considerar contribuir com o `compliance-pro-lgpd`.

## Filosofia

Este projeto serve **três públicos** ao mesmo tempo:
- **DPO/Jurídico** — precisa de citação legal precisa e linguagem juridicamente sólida
- **Dev/Privacy Engineer** — precisa de código executável e ferramental integrável
- **C-level/Board** — precisa de visão de risco e métricas

Toda contribuição deve respeitar esses três públicos: escrever para um sem descuidar dos outros.

## Antes de abrir PR

1. **Verifique a base legal**. Se o seu PR muda/adiciona algo de LGPD, cite o artigo + resolução ANPD aplicável.
2. **Não invente**. Se não tem certeza, abra uma issue antes.
3. **Atualize evidências**. Se mudou um workflow, atualize templates e scripts vinculados.
4. **Datas absolutas**. Nunca use "hoje", "esta semana" — sempre ISO 8601 ou prazos em dias.
5. **Rode os testes**:
   - Python: `cd scripts/python && pytest`
   - TS: `cd scripts/typescript && npm test`

## Tipos de contribuição esperados

### Conteúdo legal
- Atualização para novas resoluções ANPD
- Refinamento de citações
- Inclusão de jurisprudência relevante

### Ferramental
- Novos scanners (PostgreSQL extension, cookies em mobile, etc.)
- Integrações CI/CD para mais provedores
- Melhoria de patterns regex (reduzir falsos positivos)

### Workflows
- Cenários comuns ainda não cobertos
- Templates de comunicação para casos especiais
- Runbooks setoriais (saúde, financeiro, educação)

### Localização
- Por enquanto, o projeto é PT-BR. Inglês é roadmap futuro.

## Quando recusamos PR

- Falta citação legal em contribuição jurídica
- Quebra de compatibilidade sem motivação clara
- "Magia" — controle que parece fazer compliance sem rastreabilidade
- Aproximações que sacrificam precisão regulatória por simplicidade
- Adição de telemetria, analytics ou tracking nos scripts (ironia inaceitável)

## Mudanças significativas

Para mudanças que afetam:
- Estrutura de pastas
- Schema de evidence/manifest
- Esquema do ROPA
- Modelo de maturidade

→ Abra uma issue para discussão antes do PR.

## Code style

### Python
- `ruff` + `mypy --strict`
- Type hints obrigatórios
- Docstrings em funções públicas

### TypeScript
- `tsc --strict`
- `noUncheckedIndexedAccess`
- Sem `any` exceto em interop com bibliotecas mal-tipadas

### Markdown
- Linhas até 100 colunas (soft)
- Cabeçalhos em sentence case
- Citações legais em **negrito**: `**Art. 18 LGPD**`

## Licença das contribuições

Ao abrir um PR, você concorda em licenciar sua contribuição sob **AGPL-3.0**.

## Reportar vulnerabilidades

Não abra issue pública. Envie email para `nei@ampler.me` com:
- Descrição
- Reprodução
- Impacto
- Sugestão de fix

Resposta em até 7 dias úteis.

## Mantenedor

[@neimaciel](https://github.com/neimaciel) — `nei@ampler.me`
