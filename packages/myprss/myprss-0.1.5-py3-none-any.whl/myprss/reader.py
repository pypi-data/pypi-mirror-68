import click
import requests

from myprss import logger
from myprss.config import Config
from myprss.parser import parse_rss_content
from myprss.utils import list_known_feeds


@click.command(
    "read", help="Read a rss feed", no_args_is_help=True, options_metavar=""
)
@click.argument("name", autocompletion=list_known_feeds)
def read_feed(name):
    config = Config()

    if name not in config.data["registry"]:
        logger.error(f"Unknown rss feed: {name}")
        return

    url = config.data["registry"][name]
    response = requests.get(url)

    if response.status_code != 200:
        logger.error(f"{response.reason} -> {url}")
        return

    content = parse_rss_content(response.content)

    logger.info(content["site"])

    for item in reversed(content["items"]):
        logger.info(item["date"])
        logger.link(item["url"], item["title"])
        logger.paragraph(item["description"])
        logger.info("")
