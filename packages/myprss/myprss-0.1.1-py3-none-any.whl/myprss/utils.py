from myprss.config import Config


def list_known_feeds(ctx):
    config = Config()
    return list(config["registry"].keys())
