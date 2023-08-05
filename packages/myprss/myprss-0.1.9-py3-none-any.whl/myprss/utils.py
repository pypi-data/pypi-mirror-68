from email.utils import parsedate_to_datetime

from myprss.config import Config


def list_known_feeds(ctx, args, incomplete):
    config = Config()
    return list(config.data["registry"].keys())


def parse_from_rfc822_to_date(date):
    return parsedate_to_datetime(date)

def parse_from_date_to_rfc822_with_tz(date):
    return date.astimezone().strftime("%a, %d %b %Y %H:%M:%S")
