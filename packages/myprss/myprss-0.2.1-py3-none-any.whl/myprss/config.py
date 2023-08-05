import os
import sys

import click
import toml

from myprss import logger


CONFIG_DIR_PATH = os.path.expanduser("~/.config/myprss")
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, "config.toml")

DEFAULT_CONFIG = {"registry": {}, "settings": {"hyperlink": True,}}


class ConfigMeta(type):
    """Metaclass that makes our Config a singleton"""

    _instance = None

    def __call__(cls):
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


class Config(metaclass=ConfigMeta):
    """Class that contains the application settings"""

    def __init__(self, config_file=CONFIG_FILE_PATH):
        if not os.path.exists(CONFIG_DIR_PATH):
            os.makedirs(CONFIG_DIR_PATH, mode=0o774)

        self.config_file = config_file
        self.data = self._load_config()

    def _load_config(self):
        """Load configuration from toml file"""
        if not os.path.exists(self.config_file):
            return {"registry": {}}

        try:
            with open(self.config_file) as f:
                return toml.load(f)

        except toml.TomlDecodeError:
            logger.error(
                f"Configuration file does not respect toml format:"
                f"{self.config_file}"
            )
            sys.exit(1)

    def reset(self):
        """Reset the configuration"""
        self.data = self._load_config()

    def save(self):
        """Save the config"""
        with open(self.config_file, "w") as f:
            toml.dump(self.data, f)

    def update_setting(self, option, new_value):
        """Update a configuration setting"""

        if option not in self.data["settings"]:
            return False, f"Unknown configuration option: {option}"

        self.data["settings"][option] = new_value

        return True, ""


@click.group("settings", help="Manage myprss settings")
def settings():
    pass


@settings.command(
    "update", help="Update a configuration option", no_args_is_help=True
)
@click.option("--hyperlink", default=None, type=bool)
def update_config(**kwargs):
    config = Config()

    for option, new_value in kwargs.items():
        if new_value is None:
            continue

        success, msg = config.update_setting(option, new_value)

        if not success:
            logger.error(msg)

    config.save()

    logger.info("Configuration settings have been succesfully updated")


@settings.command(
    "list",
    help="List all configuration settings and their values",
    options_metavar="",
)
def list_all_settings():
    config = Config()
    max_size_option = len(max(config.data["settings"], key=len))

    logger.info("Current configuration settings\n")
    for option, value in config.data["settings"].items():
        logger.info(f"{option:>{max_size_option}}    {value}")
