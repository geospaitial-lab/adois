import pytest

from src.parsing.argument_parser import ArgumentParser


@pytest.fixture(scope='session')
def argument_parser():
    """
    | Returns an argument parser object.

    :returns: argument parser fixture
    :rtype: ArgumentParser
    """
    return ArgumentParser()
