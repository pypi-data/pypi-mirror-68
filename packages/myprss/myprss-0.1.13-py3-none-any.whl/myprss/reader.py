import click
import requests

from myprss import logger
from myprss.config import Config
from myprss.parser import parse_rss_content
from myprss.utils import list_known_feeds, parse_from_date_to_rfc822_with_tz


@click.command(
    "read", help="Read a rss feed", no_args_is_help=True
)
@click.option("-v", "--verbose", default=False, is_flag=True)
@click.argument("name", autocompletion=list_known_feeds)
def read_feed(name, verbose):
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
    logger.info("")

    for item in reversed(content["items"]):
        logger.info(parse_from_date_to_rfc822_with_tz(item["date"]))
        logger.link(item["url"], item["title"])
        if verbose:
            logger.paragraph(item["description"])
        logger.info("")
