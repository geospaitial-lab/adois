# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import pytest

from src.utils.config_parser import Postprocessing
from src.utils.config_parser_exceptions import *

from src.utils.tests.data import tests_data


@pytest.mark.parametrize('test_input, expected', tests_data.parameters_validate_sieve_size)
def test_validate_sieve_size(test_input, expected):
    """
    | Tests validate_sieve_size() with different sieve sizes.

    :param int or None test_input: sieve_size
    :param int or None expected: validated sieve_size
    :returns: None
    :rtype: None
    """
    validated_sieve_size = Postprocessing.validate_sieve_size(value=test_input)

    assert validated_sieve_size == expected
    assert isinstance(validated_sieve_size, type(expected))


@pytest.mark.parametrize('test_input', tests_data.parameters_validate_sieve_size_exception)
def test_validate_sieve_size_exception(test_input):
    """
    | Tests the exception in validate_sieve_size() with different invalid sieve sizes.

    :param int test_input: invalid sieve_size
    :returns: None
    :rtype: None
    """
    with pytest.raises(SieveSizeError):
        _validated_sieve_size = Postprocessing.validate_sieve_size(value=test_input)  # noqa: F841


@pytest.mark.parametrize('test_input, expected', tests_data.parameters_validate_simplify)
def test_validate_simplify(test_input, expected):
    """
    | Tests validate_simplify() with different simplify values.

    :param bool or None test_input: simplify
    :param bool expected: validated simplify
    :returns: None
    :rtype: None
    """
    validated_simplify = Postprocessing.validate_simplify(value=test_input)

    assert validated_simplify == expected
    assert isinstance(validated_simplify, bool)


@pytest.mark.parametrize('test_input, expected', tests_data.parameters_Postprocessing)
def test_Postprocessing(test_input, expected):
    """
    | Tests Postprocessing with different values.

    :param list[int or bool or None] test_input: value
    :param list[int or bool or None] expected: validated value
    :returns: None
    :rtype: None
    """
    postprocessing = Postprocessing(sieve_size=test_input[0],
                                    simplify=test_input[1])

    assert postprocessing.sieve_size == expected[0]
    assert postprocessing.simplify == expected[1]
    assert isinstance(postprocessing.sieve_size, type(expected[0]))
    assert isinstance(postprocessing.simplify, type(expected[1]))


@pytest.mark.parametrize('test_input', tests_data.parameters_Postprocessing_exception)
def test_Postprocessing_exception(test_input):
    """
    | Tests the exception in Postprocessing with different invalid values.

    :param int test_input: invalid value
    :returns: None
    :rtype: None
    """
    with pytest.raises(SieveSizeError):
        _postprocessing = Postprocessing(sieve_size=test_input,  # noqa: F841
                                         simplify=None)
