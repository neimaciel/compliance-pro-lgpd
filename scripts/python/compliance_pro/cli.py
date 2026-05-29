"""Compliance Pro — unified CLI orchestrator."""
from __future__ import annotations

import click

from . import __version__
from .pii_scanner import cli as pii_cli
from .retention_scanner import cli as retention_cli
from .log_scanner import cli as log_cli
from .audit_log_integrity import cli as audit_cli


@click.group(invoke_without_command=True)
@click.version_option(__version__)
@click.pass_context
def main(ctx: click.Context) -> None:
    """Compliance Pro — LGPD audit toolkit."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


main.add_command(pii_cli, name="pii")
main.add_command(retention_cli, name="retention")
main.add_command(log_cli, name="log")
main.add_command(audit_cli, name="audit")


if __name__ == "__main__":
    main()
