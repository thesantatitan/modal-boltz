"""CLI interface for Modal Boltz."""

import click
from modal_boltz import __version__


@click.group()
@click.version_option(version=__version__)
@click.pass_context
def main(ctx):
    """Modal Boltz - A Python CLI tool."""
    ctx.ensure_object(dict)


@main.command()
@click.option('--name', default='World', help='Name to greet')
def hello(name):
    """Say hello to someone."""
    click.echo(f"Hello {name} from modal-boltz!")


@main.command()
def info():
    """Show information about modal-boltz."""
    click.echo(f"Modal Boltz v{__version__}")
    click.echo("A Python CLI tool built with Modal and Boltz")


if __name__ == "__main__":
    main()
