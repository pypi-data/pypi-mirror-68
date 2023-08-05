import click

from myprss import logger
from myprss.config import Config
from myprss.utils import list_known_feeds


@click.group("registry", help="Manage your list of rss feeds")
def registry():
    pass


@registry.command(
    "add",
    help="Add a rss feed to the registry",
    no_args_is_help=True,
    options_metavar="",
)
@click.argument("name", required=True)
@click.argument("url", required=True)
def register_new_feed(name, url):
    config = Config()
    config.data["registry"][name] = url
    config.save()
    logger.info(f"{name} has been added to the rss registry")


@registry.command("list", help="List all saved rss feeds")
def list_all_feed():
    config = Config()

    if not config.data["registry"]:
        logger.info("The registry is empty")
        return

    max_name_size = max(len(name) for name in config.data["registry"].keys())

    titles = f"{'NAME':<{max_name_size}}    URL"

    logger.info(titles)
    for name, url in config.data["registry"].items():
        logger.info(f"{name:<{max_name_size}}    {url}")


@registry.command(
    "delete",
    help="Delete a rss feed from the registry",
    no_args_is_help=True,
    options_metavar="",
)
@click.argument("name", required=True, autocompletion=list_known_feeds)
def delete_feed(name):
    config = Config()
    if name not in config.data["registry"]:
        logger.error(f"{name} is unknown")
        return

    del config.data["registry"][name]
    config.save()
    logger.info(f"{name} has been deleted from the rss registry")
