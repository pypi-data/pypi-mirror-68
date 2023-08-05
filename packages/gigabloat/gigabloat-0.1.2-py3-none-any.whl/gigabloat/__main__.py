import click

from gatherer import commands as gather_commands


@click.group()
def cli():
    pass


cli.add_command(gather_commands.scan)

if __name__ == "__main__":
    cli()
