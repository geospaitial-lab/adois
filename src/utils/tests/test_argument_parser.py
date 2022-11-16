# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import pytest

from src.utils.argument_parser import get_argument_parser
from src.utils.tests.data import tests_data


@pytest.mark.parametrize('test_input, expected', tests_data.parameters_get_argument_parser)
def test_get_argument_parser(test_input,
                             expected):
    """
    | Tests get_argument_parser() with different arguments.

    :param list[str] test_input: arguments
    :param dict[str, Any] expected: parsed arguments
    :returns: None
    :rtype: None
    """
    argument_parser = get_argument_parser()
    args = argument_parser.parse_args(test_input)

    assert vars(args) == expected
