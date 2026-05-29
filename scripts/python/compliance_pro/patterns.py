"""PII regex patterns for Brazilian context (LGPD).

Conservative patterns — false positives preferred over false negatives for compliance scanning.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "critical"  # sensitive (Art. 11) — health, race, sexual orientation, biometric
    HIGH = "high"          # direct identifier — CPF, RG, biometric ID
    MEDIUM = "medium"      # indirect identifier — email, phone, name in context
    LOW = "low"            # quasi-identifier — IP, device ID
    INFO = "info"          # technical, may be relevant in combination


@dataclass(frozen=True)
class Pattern:
    name: str
    regex: re.Pattern[str]
    severity: Severity
    legal_ref: str
    description: str


# CPF: 000.000.000-00 or 00000000000 (11 digits)
CPF = Pattern(
    name="cpf",
    regex=re.compile(
        r"\b(?:\d{3}\.?\d{3}\.?\d{3}-?\d{2})\b"
    ),
    severity=Severity.HIGH,
    legal_ref="LGPD Art. 5, I",
    description="CPF (Cadastro de Pessoa Física)",
)

# CNPJ: 00.000.000/0000-00 (companies, but often linked to PF when MEI/individual)
CNPJ = Pattern(
    name="cnpj",
    regex=re.compile(
        r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b"
    ),
    severity=Severity.LOW,
    legal_ref="LGPD Art. 5, I (quando PF — MEI)",
    description="CNPJ (Cadastro Nacional de Pessoa Jurídica)",
)

# RG: variable format by state — 8-10 digits sometimes with letter
RG = Pattern(
    name="rg",
    regex=re.compile(
        r"\b\d{1,2}\.?\d{3}\.?\d{3}-?[\dXx]\b"
    ),
    severity=Severity.HIGH,
    legal_ref="LGPD Art. 5, I",
    description="RG (Registro Geral)",
)

# CNH: 11 digits
CNH = Pattern(
    name="cnh",
    regex=re.compile(r"\b\d{11}\b"),  # narrow — many false positives
    severity=Severity.MEDIUM,
    legal_ref="LGPD Art. 5, I",
    description="CNH (potencial — 11 dígitos)",
)

# Brazilian phone: +55 (DDD) NNNNN-NNNN or variants
PHONE_BR = Pattern(
    name="phone_br",
    regex=re.compile(
        r"\+?55?\s*\(?\d{2}\)?[\s-]?9?\d{4}[\s-]?\d{4}"
    ),
    severity=Severity.MEDIUM,
    legal_ref="LGPD Art. 5, I",
    description="Telefone brasileiro",
)

# Email
EMAIL = Pattern(
    name="email",
    regex=re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),
    severity=Severity.MEDIUM,
    legal_ref="LGPD Art. 5, I",
    description="Email",
)

# CEP: 00000-000
CEP = Pattern(
    name="cep",
    regex=re.compile(r"\b\d{5}-?\d{3}\b"),
    severity=Severity.LOW,
    legal_ref="LGPD Art. 5, I (quasi-identifier)",
    description="CEP (quase-identificador combinado com outros)",
)

# Credit card (Luhn-like — basic detection, not validation)
CC = Pattern(
    name="credit_card",
    regex=re.compile(
        r"\b(?:\d{4}[\s-]?){3}\d{4}\b"
    ),
    severity=Severity.HIGH,
    legal_ref="LGPD Art. 5, I + PCI-DSS",
    description="Cartão de crédito (potencial — não validado por Luhn)",
)

# IBAN-like Brazilian bank account hints (not exhaustive)
BANK_ACCOUNT = Pattern(
    name="bank_account_hint",
    regex=re.compile(
        r"\b(?:agencia|agência|ag\.?|conta|cc\.?|cp\.?)\s*[:#]?\s*\d{4,}",
        re.IGNORECASE,
    ),
    severity=Severity.HIGH,
    legal_ref="LGPD Art. 5, I",
    description="Dados bancários (heurística)",
)

# PIS/PASEP/NIS — 11 digits with check
PIS = Pattern(
    name="pis_pasep_nis",
    regex=re.compile(r"\b\d{3}\.?\d{5}\.?\d{2}-?\d\b"),
    severity=Severity.HIGH,
    legal_ref="LGPD Art. 5, I",
    description="PIS / PASEP / NIS",
)

# Título de Eleitor: 12 digits
TITULO_ELEITOR = Pattern(
    name="titulo_eleitor",
    regex=re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b"),
    severity=Severity.HIGH,
    legal_ref="LGPD Art. 5, I + Art. 11 (filiação política, se inferida)",
    description="Título de Eleitor",
)

# Passport (BR): 2 letters + 6 digits
PASSPORT_BR = Pattern(
    name="passport_br",
    regex=re.compile(r"\b[A-Z]{2}\d{6}\b"),
    severity=Severity.HIGH,
    legal_ref="LGPD Art. 5, I",
    description="Passaporte brasileiro",
)

# Plate (Mercosul + antigo)
PLATE = Pattern(
    name="vehicle_plate",
    regex=re.compile(r"\b[A-Z]{3}-?\d[A-Z\d]\d{2}\b"),
    severity=Severity.MEDIUM,
    legal_ref="LGPD Art. 5, I",
    description="Placa de veículo (vinculável a titular)",
)

# IP addresses
IPV4 = Pattern(
    name="ipv4",
    regex=re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    severity=Severity.LOW,
    legal_ref="LGPD Art. 5, I (Marco Civil Art. 13)",
    description="Endereço IPv4",
)

# Sensitive context — Art. 11 LGPD keywords (heuristic)
HEALTH = Pattern(
    name="health_keywords",
    regex=re.compile(
        r"\b(?:diagnóstico|prontuário|atestado\s+médico|medicamento|enfermidade|hiv|aids|"
        r"câncer|diabetes|psiquiátric[oa]|saúde\s+mental|exame\s+de\s+sangue|"
        r"laudo\s+médico|cid-?10|prescrição)\b",
        re.IGNORECASE,
    ),
    severity=Severity.CRITICAL,
    legal_ref="LGPD Art. 5, II + Art. 11",
    description="Dado potencial de saúde (Art. 11 — sensível)",
)

BIOMETRIC = Pattern(
    name="biometric_keywords",
    regex=re.compile(
        r"\b(?:digital|impressão\s+digital|biometria|fingerprint|face\s*id|"
        r"reconhecimento\s+facial|íris|retina|template\s+biom[eé]trico)\b",
        re.IGNORECASE,
    ),
    severity=Severity.CRITICAL,
    legal_ref="LGPD Art. 5, II + Art. 11",
    description="Dado biométrico (Art. 11 — sensível)",
)

ETHNICITY = Pattern(
    name="ethnicity_keywords",
    regex=re.compile(
        r"\b(?:raça|cor\s+da\s+pele|etnia|origem\s+étnica|negro|branco|pardo|"
        r"indígena|amarelo|preto|origem\s+racial)\b",
        re.IGNORECASE,
    ),
    severity=Severity.CRITICAL,
    legal_ref="LGPD Art. 5, II + Art. 11",
    description="Origem racial/étnica (Art. 11 — sensível)",
)

RELIGION = Pattern(
    name="religion_keywords",
    regex=re.compile(
        r"\b(?:religião|crença|fé|culto|igreja|denominação\s+religiosa|"
        r"católic[oa]|evangélic[oa]|espírita|umbandista|candomblecista|judeu|"
        r"muçulman[oa]|budista|hinduísta)\b",
        re.IGNORECASE,
    ),
    severity=Severity.CRITICAL,
    legal_ref="LGPD Art. 5, II + Art. 11",
    description="Convicção religiosa (Art. 11 — sensível)",
)

POLITICAL = Pattern(
    name="political_keywords",
    regex=re.compile(
        r"\b(?:partido\s+político|filiação\s+partidária|opinião\s+política|"
        r"ideologia\s+política|conservador|progressista|esquerda|direita)\b",
        re.IGNORECASE,
    ),
    severity=Severity.CRITICAL,
    legal_ref="LGPD Art. 5, II + Art. 11",
    description="Opinião política (Art. 11 — sensível)",
)

SEXUAL = Pattern(
    name="sexual_orientation_keywords",
    regex=re.compile(
        r"\b(?:orientação\s+sexual|homossexual|heterossexual|bissexual|"
        r"lgbt|lgbtq|gay|lésbica|trans|cisgênero|transgênero|"
        r"identidade\s+de\s+gênero)\b",
        re.IGNORECASE,
    ),
    severity=Severity.CRITICAL,
    legal_ref="LGPD Art. 5, II + Art. 11",
    description="Orientação sexual / identidade de gênero (Art. 11 — sensível)",
)

UNION = Pattern(
    name="union_membership",
    regex=re.compile(
        r"\b(?:sindicato|filiação\s+sindical|associação\s+sindical)\b",
        re.IGNORECASE,
    ),
    severity=Severity.CRITICAL,
    legal_ref="LGPD Art. 5, II + Art. 11",
    description="Filiação sindical (Art. 11 — sensível)",
)

# Secrets that should never be in code/logs
AWS_KEY = Pattern(
    name="aws_access_key",
    regex=re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    severity=Severity.CRITICAL,
    legal_ref="LGPD Art. 46 (segurança)",
    description="AWS Access Key — segredo",
)

GITHUB_TOKEN = Pattern(
    name="github_token",
    regex=re.compile(r"\bghp_[A-Za-z0-9]{36}\b"),
    severity=Severity.CRITICAL,
    legal_ref="LGPD Art. 46",
    description="GitHub Personal Access Token",
)

OPENAI_KEY = Pattern(
    name="openai_key",
    regex=re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    severity=Severity.CRITICAL,
    legal_ref="LGPD Art. 46",
    description="OpenAI / Anthropic API key (genérico sk-*)",
)

JWT_TOKEN = Pattern(
    name="jwt_token",
    regex=re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    severity=Severity.HIGH,
    legal_ref="LGPD Art. 46",
    description="JWT — pode conter PII no payload",
)

PRIVATE_KEY = Pattern(
    name="private_key",
    regex=re.compile(
        r"-----BEGIN\s+(?:RSA|DSA|EC|PGP|OPENSSH)\s+PRIVATE\s+KEY-----"
    ),
    severity=Severity.CRITICAL,
    legal_ref="LGPD Art. 46",
    description="Chave privada criptográfica",
)


ALL_PATTERNS: list[Pattern] = [
    CPF, CNPJ, RG, CNH, PHONE_BR, EMAIL, CEP, CC, BANK_ACCOUNT,
    PIS, TITULO_ELEITOR, PASSPORT_BR, PLATE, IPV4,
    HEALTH, BIOMETRIC, ETHNICITY, RELIGION, POLITICAL, SEXUAL, UNION,
    AWS_KEY, GITHUB_TOKEN, OPENAI_KEY, JWT_TOKEN, PRIVATE_KEY,
]


SENSITIVE_PATTERNS: list[Pattern] = [
    p for p in ALL_PATTERNS if p.severity == Severity.CRITICAL
]


def validate_cpf(cpf: str) -> bool:
    """Validate CPF check digits to reduce false positives."""
    digits = [int(d) for d in cpf if d.isdigit()]
    if len(digits) != 11 or len(set(digits)) == 1:
        return False
    for i in (9, 10):
        total = sum(digits[j] * (i + 1 - j) for j in range(i))
        check = (total * 10) % 11 % 10
        if check != digits[i]:
            return False
    return True


def validate_cnpj(cnpj: str) -> bool:
    """Validate CNPJ check digits."""
    digits = [int(d) for d in cnpj if d.isdigit()]
    if len(digits) != 14 or len(set(digits)) == 1:
        return False
    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    weights2 = [6] + weights1
    for weights, idx in ((weights1, 12), (weights2, 13)):
        total = sum(d * w for d, w in zip(digits, weights))
        check = (total % 11)
        check = 0 if check < 2 else 11 - check
        if check != digits[idx]:
            return False
    return True
