import pytest

from src.parsing.config import (
    Postprocessing)

from src.parsing.exceptions import (
    SieveSizeError)

from .data.data_test_config import (
    data_test_validate_sieve_size,
    data_test_validate_sieve_size_SieveSizeError,
    data_test_validate_simplify)


def test_Postprocessing_default() -> None:
    """
    | Tests the default values of the parameters of Postprocessing.

    :returns: None
    """
    postprocessing = Postprocessing()

    assert isinstance(postprocessing, Postprocessing)
    attributes = ['sieve_size', 'simplify']
    assert list(vars(postprocessing).keys()) == attributes

    assert postprocessing.sieve_size is None
    assert postprocessing.simplify is False


@pytest.mark.parametrize('test_input, expected', data_test_validate_sieve_size)
def test_validate_sieve_size(test_input: int | None,
                             expected: int | None) -> None:
    """
    | Tests validate_sieve_size().

    :param test_input: sieve_size
    :param expected: validated sieve_size
    :returns: None
    """
    sieve_size = Postprocessing.validate_sieve_size(value=test_input)

    assert isinstance(sieve_size, int) or sieve_size is None
    assert sieve_size == expected


@pytest.mark.parametrize('test_input', data_test_validate_sieve_size_SieveSizeError)
def test_validate_sieve_size_SieveSizeError(test_input: int) -> None:
    """
    | Tests validate_sieve_size().

    :param test_input: sieve_size
    :returns: None
    """
    with pytest.raises(SieveSizeError):
        _ = Postprocessing.validate_sieve_size(value=test_input)


@pytest.mark.parametrize('test_input, expected', data_test_validate_simplify)
def test_validate_simplify(test_input: bool | None,
                           expected: bool) -> None:
    """
    | Tests validate_simplify().

    :param test_input: simplify
    :param expected: validated simplify
    :returns: None
    """
    simplify = Postprocessing.validate_simplify(value=test_input)

    assert isinstance(simplify, bool)
    assert simplify == expected
