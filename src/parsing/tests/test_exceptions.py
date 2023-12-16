from pathlib import Path  # noqa: F401 (used for type hinting)

import pytest

from src.parsing.exceptions import (
    BoundingBoxError,
    BoundingBoxLengthError,
    BoundingBoxNotDefinedError,
    BoundingBoxValueError,
    GeoDataError,
    GeoDataEmptyError,
    GeoDataFormatError,
    GeoDataGeometryError,
    GeoDataLoadingError,
    GeoDataNotFoundError,
    GeoDataTypeError,
    OutputDirNotFoundError,
    PrefixError,
    SieveSizeError,
    TileSizeError)

from .data.data_test_exceptions import (
    data_test_BoundingBoxLengthError,
    data_test_BoundingBoxValueError,
    data_test_GeoDataEmptyError,
    data_test_GeoDataFormatError,
    data_test_GeoDataGeometryError,
    data_test_GeoDataLoadingError,
    data_test_GeoDataNotFoundError,
    data_test_GeoDataTypeError,
    data_test_OutputDirNotFoundError,
    data_test_SieveSizeError)


def test_BoundingBoxError_default():
    """
    | Tests the default message of BoundingBoxError.

    :returns: None
    :rtype: None
    """
    expected = 'Invalid bounding_box in the config!'

    with pytest.raises(BoundingBoxError, match=expected):
        raise BoundingBoxError()


def test_BoundingBoxError():
    """
    | Tests BoundingBoxError.

    :returns: None
    :rtype: None
    """
    message = 'Test message.'

    expected = 'Test message.'

    with pytest.raises(BoundingBoxError, match=expected):
        raise BoundingBoxError(message=message)


@pytest.mark.parametrize('test_input, expected', data_test_BoundingBoxLengthError)
def test_BoundingBoxLengthError(test_input,
                                expected):
    """
    | Tests BoundingBoxLengthError.

    :param list[int] test_input: bounding_box
    :param str expected: message
    :returns: None
    :rtype: None
    """
    with pytest.raises(BoundingBoxLengthError, match=expected):
        raise BoundingBoxLengthError(bounding_box=test_input)


def test_BoundingBoxNotDefinedError():
    """
    | Tests BoundingBoxNotDefinedError.

    :returns: None
    :rtype: None
    """
    expected = 'Neither path_boundary nor bounding_box are defined in the config!'

    with pytest.raises(BoundingBoxNotDefinedError, match=expected):
        raise BoundingBoxNotDefinedError()


@pytest.mark.parametrize('test_input, expected', data_test_BoundingBoxValueError)
def test_BoundingBoxValueError(test_input,
                               expected):
    """
    | Tests BoundingBoxValueError.

    :param list[int] test_input: bounding_box
    :param str expected: message
    :returns: None
    :rtype: None
    """
    with pytest.raises(BoundingBoxValueError, match=expected):
        raise BoundingBoxValueError(bounding_box=test_input)


def test_GeoDataError_default():
    """
    | Tests the default message of GeoDataError.

    :returns: None
    :rtype: None
    """
    expected = 'Invalid geo data in the config!'

    with pytest.raises(GeoDataError, match=expected):
        raise GeoDataError()


def test_GeoDataError():
    """
    | Tests GeoDataError.

    :returns: None
    :rtype: None
    """
    message = 'Test message.'

    expected = 'Test message.'

    with pytest.raises(GeoDataError, match=expected):
        raise GeoDataError(message=message)


@pytest.mark.parametrize('test_input, expected', data_test_GeoDataEmptyError)
def test_GeoDataEmptyError(test_input,
                           expected):
    """
    | Tests GeoDataEmptyError.

    :param (str, Path) test_input: field, path
    :param str expected: message
    :returns: None
    :rtype: None
    """
    with pytest.raises(GeoDataEmptyError, match=expected):
        raise GeoDataEmptyError(field=test_input[0],
                                path=test_input[1])


@pytest.mark.parametrize('test_input, expected', data_test_GeoDataFormatError)
def test_GeoDataFormatError(test_input,
                            expected):
    """
    | Tests GeoDataFormatError.

    :param (str, Path) test_input: field, path
    :param str expected: message
    :returns: None
    :rtype: None
    """
    with pytest.raises(GeoDataFormatError, match=expected):
        raise GeoDataFormatError(field=test_input[0],
                                 path=test_input[1])


@pytest.mark.parametrize('test_input, expected', data_test_GeoDataGeometryError)
def test_GeoDataGeometryError(test_input,
                              expected):
    """
    | Tests GeoDataGeometryError.

    :param (str, Path) test_input: field, path
    :param str expected: message
    :returns: None
    :rtype: None
    """
    with pytest.raises(GeoDataGeometryError, match=expected):
        raise GeoDataGeometryError(field=test_input[0],
                                   path=test_input[1])


@pytest.mark.parametrize('test_input, expected', data_test_GeoDataLoadingError)
def test_GeoDataLoadingError(test_input,
                             expected):
    """
    | Tests GeoDataLoadingError.

    :param (str, Path, Exception) test_input: field, path, passed_exception
    :param str expected: message
    :returns: None
    :rtype: None
    """
    with pytest.raises(GeoDataLoadingError, match=expected):
        raise GeoDataLoadingError(field=test_input[0],
                                  path=test_input[1],
                                  passed_exception=test_input[2])


@pytest.mark.parametrize('test_input, expected', data_test_GeoDataNotFoundError)
def test_GeoDataNotFoundError(test_input,
                              expected):
    """
    | Tests GeoDataNotFoundError.

    :param (str, Path) test_input: field, path
    :param str expected: message
    :returns: None
    :rtype: None
    """
    with pytest.raises(GeoDataNotFoundError, match=expected):
        raise GeoDataNotFoundError(field=test_input[0],
                                   path=test_input[1])


@pytest.mark.parametrize('test_input, expected', data_test_GeoDataTypeError)
def test_GeoDataTypeError(test_input,
                          expected):
    """
    | Tests GeoDataTypeError.

    :param (str, Path) test_input: field, path
    :param str expected: message
    :returns: None
    :rtype: None
    """
    with pytest.raises(GeoDataTypeError, match=expected):
        raise GeoDataTypeError(field=test_input[0],
                               path=test_input[1])


@pytest.mark.parametrize('test_input, expected', data_test_OutputDirNotFoundError)
def test_OutputDirNotFoundError(test_input,
                                expected):
    """
    | Tests OutputDirNotFoundError.

    :param Path test_input: path
    :param str expected: message
    :returns: None
    :rtype: None
    """
    with pytest.raises(OutputDirNotFoundError, match=expected):
        raise OutputDirNotFoundError(path=test_input)


def test_PrefixError():
    """
    | Tests PrefixError.

    :returns: None
    :rtype: None
    """
    expected = (
        r'Invalid prefix in the config!\n'
        'The prefix contains only whitespaces or underscores.')

    with pytest.raises(PrefixError, match=expected):
        raise PrefixError()


@pytest.mark.parametrize('test_input, expected', data_test_SieveSizeError)
def test_SieveSizeError(test_input,
                        expected):
    """
    | Tests SieveSizeError.

    :param int test_input: sieve_size
    :param str expected: message
    :returns: None
    :rtype: None
    """
    with pytest.raises(SieveSizeError, match=expected):
        raise SieveSizeError(sieve_size=test_input)


def test_TileSizeError():
    """
    | Tests TileSizeError.

    :returns: None
    :rtype: None
    """
    tile_size = -1

    expected = (
        r'Invalid tile_size in the config!\n'
        'Expected a number greater than 0, got -1 instead.')

    with pytest.raises(TileSizeError, match=expected):
        raise TileSizeError(tile_size=tile_size)
