import click

from myprss.reader import read_feed
from myprss.registry import registry
from myprss.config import settings

# echo -e '\e]8;;http://example.com\aThis is a link\e]8;;\a'


@click.group(options_metavar="")
def cli():
    pass

cli.add_command(registry)
cli.add_command(read_feed)
cli.add_command(settings)


if __name__ == "__main__":
    cli()
