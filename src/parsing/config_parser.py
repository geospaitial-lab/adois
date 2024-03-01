from pathlib import Path

import yaml

from src.parsing.config import Config


class ConfigParser:

    def __init__(self,
                 path: Path) -> None:
        """
        | Initializer method

        :param path: path to the config
        :returns: None
        """
        with open(path) as file:
            self.config = yaml.safe_load(file)

    def parse(self) -> Config:
        """
        | Returns the parsed config.

        :returns: parsed config
        """
        return Config(**self.config)
