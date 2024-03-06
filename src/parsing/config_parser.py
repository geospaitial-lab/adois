from pathlib import Path

import yaml

from src.parsing.config import Config


class ConfigParser:

    def __init__(self,
                 path: Path) -> None:
        """
        :param path: path to the config
        """
        with open(path) as file:
            self.config = yaml.safe_load(file)

    def parse(self) -> Config:
        """
        | Returns the parsed config.

        :returns: parsed config
        """
        return Config(**self.config)
