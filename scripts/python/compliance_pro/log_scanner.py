"""Log Scanner — detects PII leakage in application log files.

Usage:
    log-scan --target /var/log/myapp --report report.json
    log-scan --target ./logs --fail-on critical
"""
from __future__ import annotations

import gzip
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterator

import click
from rich.console import Console
from rich.table import Table

from .patterns import ALL_PATTERNS, validate_cpf, validate_cnpj, CPF, CNPJ
from .pii_scanner import redact

console = Console()


@dataclass
class LogFinding:
    file: str
    line: int
    pattern: str
    severity: str
    sample_redacted: str
    legal_ref: str

    def to_dict(self) -> dict:
        return asdict(self)


def open_log(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return path.open("r", encoding="utf-8", errors="replace")


def scan_log(path: Path, max_lines: int | None = None) -> Iterator[LogFinding]:
    try:
        f = open_log(path)
    except OSError:
        return
    with f:
        for ln, line in enumerate(f, 1):
            if max_lines and ln > max_lines:
                break
            if len(line) > 8192:
                line = line[:8192]
            for pat in ALL_PATTERNS:
                m = pat.regex.search(line)
                if not m:
                    continue
                if pat is CPF and not validate_cpf(m.group(0)):
                    continue
                if pat is CNPJ and not validate_cnpj(m.group(0)):
                    continue
                yield LogFinding(
                    file=str(path), line=ln, pattern=pat.name,
                    severity=pat.severity.value,
                    sample_redacted=redact(m.group(0)),
                    legal_ref=pat.legal_ref,
                )
                break


@click.command()
@click.option("--target", "-t", required=True, type=click.Path(exists=True))
@click.option("--report", "-r", type=click.Path(), default=None)
@click.option("--max-lines-per-file", type=int, default=None)
@click.option("--fail-on", type=click.Choice(["info","low","medium","high","critical"]), default=None)
def cli(target: str, report: str | None, max_lines_per_file: int | None, fail_on: str | None) -> None:
    """Scan log files for PII leakage (LGPD compliance)."""
    root = Path(target)
    paths: list[Path]
    if root.is_file():
        paths = [root]
    else:
        paths = [p for p in root.rglob("*") if p.is_file() and (p.suffix in {".log", ".txt", ".gz"} or "log" in p.name.lower())]

    findings: list[LogFinding] = []
    for p in paths:
        for f in scan_log(p, max_lines=max_lines_per_file):
            findings.append(f)

    # Aggregate
    by_pattern: Counter[str] = Counter(f.pattern for f in findings)
    by_severity: Counter[str] = Counter(f.severity for f in findings)
    by_file: dict[str, int] = defaultdict(int)
    for f in findings:
        by_file[f.file] += 1

    table = Table(title=f"Log PII scan — {root}", show_lines=False)
    table.add_column("File")
    table.add_column("Findings", justify="right")
    table.add_column("Top patterns")
    for fp, n in sorted(by_file.items(), key=lambda x: -x[1])[:30]:
        top = Counter(f.pattern for f in findings if f.file == fp).most_common(3)
        table.add_row(fp, str(n), ", ".join(f"{k}={v}" for k, v in top))
    console.print(table)
    console.print(f"\n[bold]Files[/]: {len(paths)} | [bold]Findings[/]: {len(findings)} | "
                  + " | ".join(f"{k}={v}" for k, v in by_severity.items()))

    if findings:
        console.print("[yellow]PII em logs viola princípio da segurança (Art. 46) e pode caracterizar incidente.[/]")
        console.print("[yellow]Implementar sanitização SDK e revisar retenção de logs.[/]")

    if report:
        Path(report).write_text(json.dumps({
            "target": str(root),
            "files_scanned": len(paths),
            "findings": [f.to_dict() for f in findings],
            "summary_by_pattern": dict(by_pattern),
            "summary_by_severity": dict(by_severity),
            "summary_by_file": dict(by_file),
        }, indent=2, ensure_ascii=False))
        console.print(f"[green]Report written:[/] {report}")

    if fail_on:
        order = ["info","low","medium","high","critical"]
        threshold = order.index(fail_on)
        if any(order.index(f.severity) >= threshold for f in findings):
            sys.exit(2)


if __name__ == "__main__":
    cli()
