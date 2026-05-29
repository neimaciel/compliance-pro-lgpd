# Controle — Criptografia

> **Art. 46 LGPD.** Medida técnica de segurança proporcional ao risco.
> Criptografia bem implementada **reduz drasticamente** a obrigação de notificação em alguns cenários (Res. 15/2024 considera estado dos dados na avaliação de risco).

---

## Princípios

| Princípio | Aplicação |
|---|---|
| **Defesa em profundidade** | Não confiar em um único algoritmo nem em uma única camada |
| **Gestão de chave é o problema real** | Cifrar é fácil, gerir chave é difícil |
| **Não inventar criptografia** | Usar bibliotecas auditadas (libsodium, AES-GCM via lib do SO) |
| **Auditável** | Capacidade de provar à ANPD que dado X estava cifrado em Y |
| **Rotação periódica** | Chaves têm vida útil; data master rekey anual |

---

## Padrões mínimos

### Em repouso (at-rest)

| Onde | Algoritmo | Modo | Comentário |
|---|---|---|---|
| Banco de dados | AES-256 | GCM ou XTS | Habilitado no nível do storage **e** opcionalmente no nível do app para PII sensível |
| Object storage (S3, GCS) | AES-256 | GCM | Server-side encryption + cliente para sensíveis |
| Backups | AES-256 | GCM | Chave **separada** da chave de produção |
| Filesystem (volumes) | LUKS / FileVault / BitLocker | XTS-AES-256 | Padrão |
| Cache (Redis, Memcached) | TLS in-transit + AES at-rest | — | Não usar para PII sensível sem necessidade |

### Em trânsito (in-transit)

| Onde | Padrão |
|---|---|
| HTTPS público | TLS 1.3 (mínimo 1.2 — TLS 1.0/1.1 proibidos) |
| Cifras | Suites com forward secrecy (ECDHE) |
| HSTS | max-age ≥ 1 ano + includeSubDomains + preload |
| API interna | mTLS preferencial |
| Mensageria (Kafka, RabbitMQ) | TLS + SASL |
| Webhooks de terceiros | TLS + assinatura HMAC |
| Email externo | TLS oportunístico mínimo; MTA-STS recomendado |

### Em uso (in-use) — emergente

- **TEE (Trusted Execution Environment)**: Intel SGX, AMD SEV, AWS Nitro Enclaves
- **Computação confidencial** para análise sobre dados cifrados
- **MPC (Multi-Party Computation)** quando ROI justifica
- **Homomorphic encryption** — ainda lento, mas viável para nichos

---

## Gestão de chaves (KMS)

### Hierarquia recomendada

```
Root Key (HSM / cloud KMS root)
    └── Key Encryption Key (KEK) — rotação anual
        └── Data Encryption Key (DEK) — uma por escopo (cliente, tenant, registro)
            └── Dado cifrado
```

### Princípios

| Princípio | Implementação |
|---|---|
| **Separação de chave e dado** | KMS / HSM separado do banco |
| **Mínimo privilégio** | IAM grant por DEK específica, não master |
| **Rotação** | KEK anual + DEK por evento (off-boarding, suspeita) |
| **Audit log** | Toda operação `Decrypt`/`Encrypt` é loggada com identidade |
| **Backup de chave** | Custódia separada (key escrow); sem chave = sem dado |
| **Destruição criptográfica** | Para "right to be forgotten" em backups imutáveis |

### Opções de KMS

| Solução | Quando usar |
|---|---|
| AWS KMS + CloudHSM | Workloads na AWS |
| Google Cloud KMS | GCP |
| Azure Key Vault | Azure |
| HashiCorp Vault | Multi-cloud / on-prem |
| Equinix SmartKey / Thales | Compliance regulada (BACEN, ANS) — HSM dedicado |

---

## Casos específicos

### PII em campos do banco
- Application-layer encryption para campos como `cpf`, `rg`, `cartao`
- Padrão: `CRYPTO::v1::{kid}::{nonce}::{ciphertext}::{tag}` (versionado para rotação)
- Índices: usar **deterministic encryption** (AES-SIV) para busca exata, ou **searchable encryption** quando viável
- LIKE / range search → não funciona em encrypted column — repensar arquitetura

### Senhas
- **Nunca** "cifrar" — **hash** com Argon2id (preferencial), bcrypt ou scrypt
- Parâmetros mínimos Argon2id: memory=64MB, iterations=3, parallelism=4
- Salt único por senha, gerado por CSPRNG
- Pepper (segredo global) opcional em KMS

### Tokens de API
- Armazenar como **hash** (HMAC-SHA-256 com secret em KMS)
- Token bruto só existe no momento da criação — usuário copia uma vez

### JWT
- Algoritmo: **RS256** ou **EdDSA** (chave assimétrica)
- Não usar HS256 com secret compartilhado entre múltiplos serviços
- Curto TTL (15min) + refresh token rotativo

### Dados sensíveis (Art. 11)
- Encryption-by-default no nível da aplicação
- Acesso à chave granular (não basta acesso ao banco)
- Audit log obrigatório
- Possibilidade de revogar chave por titular (DSAR eliminação por destruição de chave)

### Backups
- Cifrados com chave **diferente** da produção
- Restore testado trimestralmente
- Em caso de eliminação LGPD: documentar janela até backup expirar

### Comunicações com terceiros (SFTP, EDI, etc.)
- SFTP/FTPS apenas — nunca FTP em claro
- Idealmente: arquivo cifrado com PGP além do canal TLS
- Chaves rotacionadas + revogadas no off-boarding

---

## Anti-padrões comuns

| ❌ Erro | ✅ Correto |
|---|---|
| AES-ECB | AES-GCM ou AES-XTS |
| MD5 / SHA-1 para hash sensível | SHA-256 mínimo (SHA-3, BLAKE2 melhor) |
| Senha em MD5/SHA | Argon2id / bcrypt |
| "Encryption" caseira (XOR, ROT, custom) | libsodium, AEAD nativo |
| Chave hardcoded no código | KMS / variável de ambiente em secret manager |
| Chave commitada no Git | git filter-repo + rotacionar imediatamente |
| Mesma chave para todos tenants | DEK por tenant |
| Sem rotação ("se não tá quebrado…") | Rotação anual + por evento |
| Cifrar e jogar fora a chave (sem registrar) | KMS com audit + backup de chave |

---

## Evidência para auditoria

Para cada sistema/tabela com PII:

```yaml
sistema: "users-db"
ambiente: "prod"
classificacao: "PII (cadastrais + financeiros)"
encryption_at_rest:
  storage_layer: "AWS RDS encryption (AES-256, KMS key alias 'rds-prod')"
  application_layer:
    fields: ["cpf", "rg", "cartao_token"]
    algorithm: "AES-256-GCM"
    kek: "arn:aws:kms:sa-east-1:...:key/abc-123"
    rotation_kek: "anual"
encryption_in_transit:
  external: "TLS 1.3 (suite TLS_AES_256_GCM_SHA384), HSTS 1 ano"
  internal: "mTLS via service mesh"
backups:
  encryption: "AES-256, KMS key alias 'backup-prod' (DIFERENTE da prod)"
  key_management: "AWS KMS with separate IAM"
audit_log:
  destination: "CloudTrail + SIEM"
  retention: "12 meses"
last_audit: "2026-04-15"
next_audit: "2026-10-15"
```

---

## Scripts de auditoria

- [`scripts/python/encryption-checker.py`](../scripts/python/encryption-checker.py) — verifica configuração de criptografia em ambiente (S3 buckets, RDS instances, etc.)
- [`scripts/typescript/tls-checker.ts`](../scripts/typescript/tls-checker.ts) — escaneia endpoints e valida TLS version + ciphers

---

## Referências

- Art. 46 LGPD — segurança
- NIST SP 800-57 — Key Management
- NIST SP 800-175B — Cryptographic Standards
- OWASP Cryptographic Storage Cheat Sheet
- BCB Res. 4658/2018 (segurança cibernética bancária)
- BACEN Res. 4893/2021 — proteção de dados em IF
