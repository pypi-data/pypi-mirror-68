from email.utils import parsedate_to_datetime

from myprss.config import Config


def list_known_feeds(ctx, args, incomplete):
    config = Config()
    return list(config.data["registry"].keys())


def parse_rfc822_date(date):
    return parsedate_to_datetime(date).astimezone().strftime("%a, %d %b %Y %H:%M:%S")
