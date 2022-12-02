import pytest

from src.preprocessing.preprocessor import Preprocessor


@pytest.fixture(scope='session')
def preprocessor():
    """
    | Returns a preprocessor instance.

    :returns: preprocessor
    :rtype: Preprocessor
    """
    preprocessor = Preprocessor()
    return preprocessor
