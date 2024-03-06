import argparse


class ArgumentParser:

    def __init__(self) -> None:
        description = 'adois - automatic detection of impervious surfaces'
        self.argument_parser = argparse.ArgumentParser(description=description)

        self.argument_parser.add_argument('path_config',
                                          type=str,
                                          help='path to the config')

        self.argument_parser.add_argument('-d',
                                          '--debug',
                                          action='store_true',
                                          help='debug mode')

    def parse(self,
              args: list | tuple | None = None) -> argparse.Namespace:
        """
        | Returns the parsed arguments.

        :param args: arguments
        :returns: parsed arguments
        """
        return self.argument_parser.parse_args(args)
