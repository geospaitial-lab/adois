import argparse
import unittest.mock as mock

import pytest

from src.parsing.argument_parser import ArgumentParser

from .data.data_test_argument_parser import (
    data_test_parse_integration,
    data_test_parse_SystemExit_integration)


@mock.patch('src.parsing.argument_parser.argparse.ArgumentParser')
def test_init(mocked_argument_parser):
    """
    | Tests __init__().

    :param mock.MagicMock mocked_argument_parser: mocked argument parser
    :returns: None
    :rtype: None
    """
    argument_parser = ArgumentParser()

    assert isinstance(argument_parser, ArgumentParser)
    attributes = ['argument_parser']
    assert list(vars(argument_parser).keys()) == attributes

    mocked_argument_parser.assert_called_once_with(description='adois - automatic detection of impervious surfaces')
    assert len(mocked_argument_parser.return_value.add_argument.mock_calls) == 2

    mock_call_1 = mock.call('path_config',
                            type=str,
                            help='path to the config')

    mock_call_2 = mock.call('-d',
                            '--debug',
                            action='store_true',
                            help='debug mode')

    mocked_argument_parser.return_value.add_argument.assert_has_calls([mock_call_1, mock_call_2])


@mock.patch('src.parsing.argument_parser.ArgumentParser.parse')
def test_parse(mocked_parse,
               argument_parser):
    """
    | Tests parse().

    :param mock.MagicMock mocked_parse: mocked parse method
    :param ArgumentParser argument_parser: argument parser fixture
    :returns: None
    :rtype: None
    """
    args = ['path/to/config.yaml', '-d']

    expected = argparse.Namespace(path_config='path/to/config.yaml', debug=True)

    mocked_parse.return_value = expected

    args_parsed = argument_parser.parse(args=args)

    mocked_parse.assert_called_once_with(args=args)

    assert isinstance(args_parsed, argparse.Namespace)
    assert args_parsed.path_config == expected.path_config
    assert args_parsed.debug is expected.debug


@pytest.mark.integration
@pytest.mark.parametrize('test_input, expected', data_test_parse_integration)
def test_parse_integration(test_input,
                           expected,
                           argument_parser):
    """
    | Tests parse().
    | Integration test.

    :param list[str] test_input: args
    :param argparse.Namespace expected: parsed arguments
    :param ArgumentParser argument_parser: argument parser fixture
    :returns: None
    :rtype: None
    """
    args_parsed = argument_parser.parse(args=test_input)

    assert isinstance(args_parsed, argparse.Namespace)
    assert args_parsed.path_config == expected.path_config
    assert args_parsed.debug is expected.debug


@pytest.mark.integration
@pytest.mark.parametrize('test_input, expected', data_test_parse_SystemExit_integration)
def test_parse_SystemExit_integration(test_input,
                                      expected,
                                      argument_parser,
                                      capsys):
    """
    | Tests parse().
    | Integration test.

    :param list[str] test_input: args
    :param str expected: message
    :param ArgumentParser argument_parser: argument parser fixture
    :param capsys: pytest capsys
    :returns: None
    :rtype: None
    """
    with pytest.raises(SystemExit):
        argument_parser.parse(args=test_input)

    assert expected in capsys.readouterr().err
