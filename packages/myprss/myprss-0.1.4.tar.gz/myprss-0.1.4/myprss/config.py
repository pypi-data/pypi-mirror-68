import os
import sys

import toml

from myprss import logger


CONFIG_DIR_PATH = os.path.expanduser("~/.config/myprss")
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, "config.toml")


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
        print(self.config_file)
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
