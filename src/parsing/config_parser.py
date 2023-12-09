from pathlib import Path  # noqa: F401 (used for type hinting)

import yaml

from src.parsing.config import Config


class ConfigParser:

    def __init__(self,
                 path):
        """
        | Initializer method

        :param Path path: path to the config
        :returns: None
        :rtype: None
        """
        with open(path) as file:
            self.config = yaml.safe_load(file)

    def parse(self):
        """
        | Returns the parsed config.

        :returns: parsed config
        :rtype: Config
        """
        return Config(**self.config)
