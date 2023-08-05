from myprss.config import Config


def list_known_feeds(ctx, args, incomplete):
    config = Config()
    return list(config.data["registry"].keys())
