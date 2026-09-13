"""PII Scanner — scans source code / configs / logs for personal data and secrets.

Usage:
    pii-scan --target ./my-project --report report.json
    pii-scan --target . --severity high --fail-on critical
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterator

import click
from rich.console import Console
from rich.table import Table

from .patterns import (
    ALL_PATTERNS, Pattern, Severity,
    CPF, CNPJ, validate_cpf, validate_cnpj,
)

console = Console()


DEFAULT_EXCLUDES = {
    ".git", "node_modules", ".venv", "venv", "__pycache__",
    "dist", "build", ".next", ".nuxt", "target", "vendor",
    ".idea", ".vscode", "coverage", ".pytest_cache", ".mypy_cache",
    ".tox", ".cache", "tmp", "temp", ".terraform",
}

# Files that legitimately contain test fixtures with fake PII.
TEST_FILE_HINTS = re.compile(r"(test|spec|fixture|mock|example|sample|fake)", re.IGNORECASE)

TEXT_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte",
    ".go", ".java", ".kt", ".rs", ".rb", ".php", ".cs", ".cpp", ".c", ".h",
    ".sql", ".prisma", ".graphql",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".env", ".properties",
    ".md", ".rst", ".txt",
    ".html", ".css", ".scss", ".sass",
    ".sh", ".bash", ".zsh", ".fish",
    ".log", ".csv", ".tsv",
}


@dataclass
class Finding:
    file: str
    line: int
    column: int
    pattern: str
    severity: str
    legal_ref: str
    description: str
    match_redacted: str
    validated: bool | None  # None = not validatable

    def to_dict(self) -> dict:
        return asdict(self)


def redact(value: str) -> str:
    """Reduce false-leakage in the report — show only enough to locate."""
    if len(value) <= 6:
        return value[:2] + "*" * max(0, len(value) - 2)
    return value[:3] + "*" * (len(value) - 6) + value[-3:]


def should_skip(path: Path, excludes: set[str], root: Path | None = None) -> bool:
    # Compara só as pastas DENTRO do alvo. Com o caminho absoluto, um projeto que mora
    # em /tmp, build/, vendor/ etc. era pulado inteiro e o scan "passava" com 0 arquivos.
    rel = path.relative_to(root) if root is not None else path
    parts = set(rel.parts)
    if parts & excludes:
        return True
    if path.suffix and path.suffix not in TEXT_EXTENSIONS:
        return True
    return False


def iter_files(root: Path, excludes: set[str]) -> Iterator[Path]:
    for p in root.rglob("*"):
        if p.is_file() and not should_skip(p, excludes, root):
            yield p


def scan_file(path: Path, patterns: list[Pattern], is_test: bool) -> Iterator[Finding]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return
    for line_no, line in enumerate(text.splitlines(), start=1):
        if len(line) > 4096:  # avoid pathological lines
            continue
        for pat in patterns:
            for m in pat.regex.finditer(line):
                # Validate CPF/CNPJ to reduce noise
                validated: bool | None = None
                if pat is CPF:
                    validated = validate_cpf(m.group(0))
                    if not validated and is_test:
                        continue
                elif pat is CNPJ:
                    validated = validate_cnpj(m.group(0))
                    if not validated and is_test:
                        continue
                yield Finding(
                    file=str(path),
                    line=line_no,
                    column=m.start() + 1,
                    pattern=pat.name,
                    severity=pat.severity.value,
                    legal_ref=pat.legal_ref,
                    description=pat.description,
                    match_redacted=redact(m.group(0)),
                    validated=validated,
                )


@click.command()
@click.option("--target", "-t", default=".", type=click.Path(exists=True, file_okay=False))
@click.option("--report", "-r", type=click.Path(), default=None, help="Write JSON report")
@click.option(
    "--severity", "-s",
    type=click.Choice([s.value for s in Severity]),
    default=None, help="Minimum severity to report",
)
@click.option(
    "--fail-on",
    type=click.Choice([s.value for s in Severity]),
    default=None, help="Exit non-zero if any finding ≥ this severity",
)
@click.option("--exclude", multiple=True, help="Additional paths to exclude")
@click.option(
    "--include-tests/--exclude-tests", default=False,
    help="Include test/fixture files (default: validated PII only)",
)
@click.option("--quiet", "-q", is_flag=True, help="Suppress table output")
def cli(
    target: str,
    report: str | None,
    severity: str | None,
    fail_on: str | None,
    exclude: tuple[str, ...],
    include_tests: bool,
    quiet: bool,
) -> None:
    """Scan a directory for LGPD-relevant PII and secrets."""
    root = Path(target).resolve()
    excludes = DEFAULT_EXCLUDES | set(exclude)

    severity_order = [s.value for s in (Severity.INFO, Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL)]
    min_idx = severity_order.index(severity) if severity else 0

    patterns = ALL_PATTERNS
    findings: list[Finding] = []

    files_scanned = 0
    for fp in iter_files(root, excludes):
        files_scanned += 1
        is_test = bool(TEST_FILE_HINTS.search(str(fp.relative_to(root))))  # só o caminho dentro do alvo
        for f in scan_file(fp, patterns, is_test=is_test):
            if severity_order.index(f.severity) < min_idx:
                continue
            findings.append(f)

    summary: dict[str, int] = {s.value: 0 for s in Severity}
    for f in findings:
        summary[f.severity] += 1

    if not quiet:
        table = Table(title=f"PII Scan — {root}", show_lines=False)
        table.add_column("Severity", style="bold")
        table.add_column("Pattern")
        table.add_column("File:Line")
        table.add_column("Match")
        table.add_column("Legal ref")

        sev_color = {
            "critical": "red",
            "high": "magenta",
            "medium": "yellow",
            "low": "cyan",
            "info": "white",
        }
        for f in findings[:200]:  # cap visual output
            table.add_row(
                f"[{sev_color.get(f.severity,'white')}]{f.severity.upper()}[/]",
                f.pattern,
                f"{f.file}:{f.line}",
                f.match_redacted,
                f.legal_ref,
            )
        console.print(table)
        if len(findings) > 200:
            console.print(f"[dim]... +{len(findings)-200} more findings[/]")

        console.print(
            f"\n[bold]Scanned[/]: {files_scanned} files | "
            f"[bold]Findings[/]: {len(findings)} | "
            + " | ".join(f"[{sev_color[k]}]{k}[/]: {v}" for k, v in summary.items() if v)
        )

    if report:
        Path(report).write_text(json.dumps({
            "target": str(root),
            "files_scanned": files_scanned,
            "findings": [f.to_dict() for f in findings],
            "summary": summary,
        }, indent=2, ensure_ascii=False))
        if not quiet:
            console.print(f"[green]Report written:[/] {report}")

    if files_scanned == 0:
        # nada examinado não é aprovação: sem isto, um alvo errado passava no CI em silêncio
        console.print("[yellow bold]AVISO[/]: nenhum arquivo examinado. Confira --target e --exclude.")
        if fail_on:
            sys.exit(3)

    if fail_on:
        fail_idx = severity_order.index(fail_on)
        for f in findings:
            if severity_order.index(f.severity) >= fail_idx:
                console.print(f"[red bold]FAIL[/]: at least one finding ≥ {fail_on}")
                sys.exit(2)


if __name__ == "__main__":
    cli()
