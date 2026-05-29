"""Audit Log Integrity — verifies hash-chain integrity in evidence/log.jsonl.

Each line should be a JSON object with:
    { "ts": ..., "event": ..., ..., "hash_prev": "...", "hash_self": "..." }

hash_self = sha256(canonical_json(record_without_hash_self))
hash_prev = hash_self of previous record (or null for first)

Usage:
    audit-integrity verify --file ../../evidence/log.jsonl
    audit-integrity append --file evidence/log.jsonl --event '{"event":"test"}'
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import click
from rich.console import Console

console = Console()


def canonical_json(d: dict) -> str:
    """Canonical JSON for hashing: sorted keys, no whitespace, UTF-8."""
    return json.dumps(d, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def compute_hash(record: dict, prev_hash: str | None) -> str:
    payload = {k: v for k, v in record.items() if k != "hash_self"}
    payload["hash_prev"] = prev_hash
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


@click.group()
def cli() -> None:
    """Audit log hash-chain operations."""


@cli.command()
@click.option("--file", "-f", required=True, type=click.Path(exists=True))
def verify(file: str) -> None:
    """Verify hash chain integrity."""
    prev_hash: str | None = None
    errors = 0
    total = 0
    for line_no, raw in enumerate(Path(file).read_text().splitlines(), 1):
        if not raw.strip():
            continue
        total += 1
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as e:
            console.print(f"[red]Line {line_no}: invalid JSON ({e})[/]")
            errors += 1
            continue
        expected = compute_hash(record, prev_hash)
        actual = record.get("hash_self")
        record_prev = record.get("hash_prev")
        if record_prev != prev_hash:
            console.print(
                f"[red]Line {line_no}: hash_prev mismatch — expected {prev_hash}, got {record_prev}[/]"
            )
            errors += 1
        if actual != expected:
            console.print(
                f"[red]Line {line_no}: hash_self mismatch — expected {expected[:16]}…, got {(actual or '')[:16]}…[/]"
            )
            errors += 1
        prev_hash = actual

    console.print(f"\n[bold]Records[/]: {total} | [bold]Errors[/]: {errors}")
    if errors:
        console.print("[red bold]CHAIN BROKEN — evidence has been tampered or truncated.[/]")
        sys.exit(2)
    else:
        console.print("[green bold]CHAIN INTACT.[/]")


@cli.command()
@click.option("--file", "-f", required=True, type=click.Path())
@click.option("--event", "-e", required=True, help="JSON event payload to append")
def append(file: str, event: str) -> None:
    """Append a new record to the audit log (computes hashes)."""
    payload = json.loads(event)
    path = Path(file)
    prev_hash: str | None = None
    if path.exists():
        for raw in path.read_text().splitlines():
            if raw.strip():
                try:
                    prev_hash = json.loads(raw).get("hash_self")
                except json.JSONDecodeError:
                    pass
    record = {**payload, "hash_prev": prev_hash}
    record["hash_self"] = compute_hash(record, prev_hash)
    with path.open("a", encoding="utf-8") as f:
        f.write(canonical_json(record) + "\n")
    console.print(f"[green]Appended[/] (hash {record['hash_self'][:16]}…)")


if __name__ == "__main__":
    cli()
