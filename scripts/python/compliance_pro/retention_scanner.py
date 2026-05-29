"""Retention Scanner — finds tables/columns with PII and no documented retention policy.

Cross-references DB schema vs ROPA YAML.

Usage:
    retention-scan --schema schema.sql --ropa ../../../ropa.yaml --report report.json
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.table import Table

console = Console()


PII_COLUMN_HINTS = re.compile(
    r"\b(?:cpf|cnpj|rg|email|e_mail|telefone|phone|fone|celular|"
    r"nome|name|first_?name|last_?name|sobrenome|"
    r"endereco|endereço|address|street|rua|cep|zip|"
    r"data_?nasc|birth|nascimento|"
    r"cartao|cartão|card|credit|bank|account|conta|agencia|agência|"
    r"senha|password|pin|token|secret|"
    r"diagnostico|diagnóstico|prontuario|prontuário|saude|saúde|cid|"
    r"raca|raça|cor|ethnicity|religion|religiao|religião|"
    r"orientacao|orientação|gender|genero|gênero|biometr|fingerprint|face|"
    r"ip_?addr|user_?agent)\b",
    re.IGNORECASE,
)

# Heuristic for sensitive (Art. 11) keywords
SENSITIVE_HINTS = re.compile(
    r"\b(?:saude|saúde|diagnostico|diagnóstico|prontuario|prontuário|cid|"
    r"raca|raça|ethnicity|religion|religiao|religião|"
    r"orientacao_sexual|orientação_sexual|gender_identity|"
    r"biometr|fingerprint|face_id|iris|retina|"
    r"opinion_political|filiacao_sindical|filiação_sindical)\b",
    re.IGNORECASE,
)


@dataclass
class SchemaColumn:
    table: str
    column: str
    type: str
    nullable: bool

    @property
    def is_pii(self) -> bool:
        return bool(PII_COLUMN_HINTS.search(self.column))

    @property
    def is_sensitive(self) -> bool:
        return bool(SENSITIVE_HINTS.search(self.column))


CREATE_TABLE_RE = re.compile(
    r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[\"`']?(?P<schema>\w+)?[\"`']?\.?[\"`']?(?P<table>\w+)[\"`']?\s*\((?P<body>.+?)\);",
    re.IGNORECASE | re.DOTALL,
)

COLUMN_RE = re.compile(
    r"^\s*[\"`']?(?P<col>\w+)[\"`']?\s+(?P<type>[\w\(\),\s]+?)(?:\s+(?P<extra>.+))?$",
    re.IGNORECASE,
)


def parse_schema_sql(sql: str) -> list[SchemaColumn]:
    cols: list[SchemaColumn] = []
    for m in CREATE_TABLE_RE.finditer(sql):
        table = m.group("table")
        body = m.group("body")
        for raw_line in body.split(","):
            line = raw_line.strip()
            if not line or line.upper().startswith((
                "PRIMARY KEY", "FOREIGN KEY", "UNIQUE", "CONSTRAINT",
                "CHECK", "INDEX", "KEY"
            )):
                continue
            cm = COLUMN_RE.match(line)
            if not cm:
                continue
            col = cm.group("col")
            ctype = (cm.group("type") or "").strip().rstrip(",")
            extra = (cm.group("extra") or "").lower()
            nullable = "not null" not in extra
            cols.append(SchemaColumn(table=table, column=col, type=ctype, nullable=nullable))
    return cols


@dataclass
class Issue:
    table: str
    column: str
    severity: str
    issue: str
    legal_ref: str

    def to_dict(self) -> dict:
        return asdict(self)


def load_ropa(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


def covered_by_ropa(table: str, column: str, ropa: dict) -> bool:
    """Heuristic: ROPA mentions table/column or matching category."""
    text = yaml.dump(ropa).lower()
    return table.lower() in text or column.lower() in text


@click.command()
@click.option("--schema", "-s", required=True, type=click.Path(exists=True))
@click.option("--ropa", "-r", type=click.Path(exists=True), default=None)
@click.option("--report", type=click.Path(), default=None)
@click.option("--fail-on-uncovered/--no-fail", default=False)
def cli(schema: str, ropa: str | None, report: str | None, fail_on_uncovered: bool) -> None:
    """Scan SQL schema vs ROPA for retention compliance."""
    sql = Path(schema).read_text()
    cols = parse_schema_sql(sql)
    ropa_data = load_ropa(Path(ropa)) if ropa else {}

    issues: list[Issue] = []

    pii_cols = [c for c in cols if c.is_pii]
    for c in pii_cols:
        if not ropa_data:
            issues.append(Issue(
                table=c.table, column=c.column,
                severity="medium",
                issue="Coluna com PII identificada; ROPA não fornecido",
                legal_ref="LGPD Art. 37",
            ))
            continue
        if not covered_by_ropa(c.table, c.column, ropa_data):
            sev = "high" if c.is_sensitive else "medium"
            issues.append(Issue(
                table=c.table, column=c.column,
                severity=sev,
                issue="Coluna com PII não consta no ROPA",
                legal_ref="LGPD Art. 37 + Art. 6 V (qualidade) + Art. 15-16 (retenção)",
            ))
        if c.is_sensitive:
            issues.append(Issue(
                table=c.table, column=c.column,
                severity="high",
                issue="Coluna com dado SENSÍVEL (Art. 11) — verificar base legal e controles adicionais",
                legal_ref="LGPD Art. 11 + Art. 5 II",
            ))

    # Render
    table = Table(title=f"Retention scan — schema: {schema}", show_lines=False)
    table.add_column("Severity", style="bold")
    table.add_column("Table.Column")
    table.add_column("Issue")
    table.add_column("Legal ref")

    color = {"high": "red", "medium": "yellow", "low": "cyan"}
    for i in issues[:200]:
        table.add_row(
            f"[{color.get(i.severity,'white')}]{i.severity.upper()}[/]",
            f"{i.table}.{i.column}",
            i.issue,
            i.legal_ref,
        )
    console.print(table)
    console.print(f"\n[bold]Total columns scanned[/]: {len(cols)} | "
                  f"[bold]PII columns[/]: {len(pii_cols)} | "
                  f"[bold]Issues[/]: {len(issues)}")

    if report:
        Path(report).write_text(json.dumps({
            "schema": str(schema),
            "ropa": str(ropa) if ropa else None,
            "total_columns": len(cols),
            "pii_columns": len(pii_cols),
            "issues": [i.to_dict() for i in issues],
        }, indent=2, ensure_ascii=False))
        console.print(f"[green]Report written:[/] {report}")

    if fail_on_uncovered and any(i.severity in ("high", "medium") for i in issues):
        sys.exit(2)


if __name__ == "__main__":
    cli()
