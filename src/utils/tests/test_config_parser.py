from pathlib import Path

import pytest

from src.utils.config_parser import Postprocessing, Aggregation
from src.utils.config_parser_exceptions import *
from src.utils.tests.data import *


@pytest.mark.parametrize('test_input, expected', parameters_validate_sieve_size)
def test_validate_sieve_size(test_input, expected):
    """
    | Tests validate_sieve_size() with different sieve sizes.

    :param int or None test_input: sieve_size
    :param int or None expected: validated sieve_size
    :returns: None
    :rtype: None
    """
    validated_sieve_size = Postprocessing.validate_sieve_size(value=test_input)

    assert isinstance(validated_sieve_size, type(expected))
    assert validated_sieve_size == expected


@pytest.mark.parametrize('test_input', parameters_validate_sieve_size_exception)
def test_validate_sieve_size_exception(test_input):
    """
    | Tests the exception in validate_sieve_size() with different invalid sieve sizes.

    :param int test_input: invalid sieve_size
    :returns: None
    :rtype: None
    """
    with pytest.raises(SieveSizeError):
        _validated_sieve_size = Postprocessing.validate_sieve_size(value=test_input)  # noqa: F841


@pytest.mark.parametrize('test_input, expected', parameters_validate_simplify)
def test_validate_simplify(test_input, expected):
    """
    | Tests validate_simplify() with different simplify values.

    :param bool or None test_input: simplify
    :param bool expected: validated simplify
    :returns: None
    :rtype: None
    """
    validated_simplify = Postprocessing.validate_simplify(value=test_input)

    assert isinstance(validated_simplify, bool)
    assert validated_simplify == expected


@pytest.mark.parametrize('test_input, expected', parameters_Postprocessing)
def test_Postprocessing(test_input, expected):
    """
    | Tests Postprocessing with different values.

    :param list[int or bool or None] test_input: values
    :param list[int or bool or None] expected: validated values
    :returns: None
    :rtype: None
    """
    postprocessing = Postprocessing(sieve_size=test_input[0],
                                    simplify=test_input[1])

    assert isinstance(postprocessing.sieve_size, type(expected[0]))
    assert isinstance(postprocessing.simplify, type(expected[1]))
    assert postprocessing.sieve_size == expected[0]
    assert postprocessing.simplify == expected[1]


@pytest.mark.parametrize('test_input', parameters_validate_sieve_size_exception)
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


def test_Postprocessing_default():
    """
    | Tests the default values in Postprocessing.

    :returns: None
    :rtype: None
    """
    postprocessing = Postprocessing()

    assert isinstance(postprocessing, Postprocessing)
    assert list(postprocessing.__dict__.keys()) == ['sieve_size', 'simplify']
    assert postprocessing.sieve_size is None
    assert postprocessing.simplify is None


@pytest.mark.parametrize('test_input, expected', parameters_validate_tile_size)
def test_validate_tile_size(test_input, expected):
    """
    | Tests validate_tile_size() with different tile sizes.

    :param int or list[int or None] or None test_input: tile_size
    :param list[int] expected: validated tile_size
    :returns: None
    :rtype: None
    """
    validated_tile_size = Aggregation.validate_tile_size(value=test_input)

    for validated_tile_size_element in validated_tile_size:
        assert isinstance(validated_tile_size_element, int)

    assert validated_tile_size == expected


@pytest.mark.parametrize('test_input', parameters_validate_tile_size_exception)
def test_validate_tile_size_exception(test_input):
    """
    | Tests the exception in validate_tile_size() with different invalid tile sizes.

    :param int test_input: invalid tile_size
    :returns: None
    :rtype: None
    """
    with pytest.raises(TileSizeError):
        _validated_tile_size = Aggregation.validate_tile_size(value=test_input)  # noqa: F841


@pytest.mark.parametrize('test_input, expected', parameters_validate_shape_file_path)
def test_validate_shape_file_path(test_input,
                                  expected,
                                  shape_file_dir_path):
    """
    | Tests validate_shape_file_path() with different shape file paths.

    :param str or list[str or None] or None test_input: shape_file_path
    :param list[str] expected: validated shape_file_path
    :param Path shape_file_dir_path: path to the shape file directory
    :returns: None
    :rtype: None
    """
    if test_input is None:
        pass
    elif isinstance(test_input, str):
        test_input = str(shape_file_dir_path / test_input)
    else:
        test_input = [str(shape_file_dir_path / x) for x in test_input if isinstance(x, str)]

    expected = [str(shape_file_dir_path / x) for x in expected if isinstance(x, str)]

    validated_shape_file_path = Aggregation.validate_shape_file_path(value=test_input)

    for validated_shape_file_path_element in validated_shape_file_path:
        assert isinstance(validated_shape_file_path_element, str)

    assert validated_shape_file_path == expected


@pytest.mark.parametrize('test_input', parameters_validate_shape_file_path_exception_1)
def test_validate_shape_file_path_exception_1(test_input, shape_file_dir_path):
    """
    | Tests the exception in validate_shape_file_path() with different invalid shape file paths.

    :param str or list[str or None] test_input: invalid shape_file_path
    :param Path shape_file_dir_path: path to the shape file directory
    :returns: None
    :rtype: None
    """
    if test_input is None:
        pass
    elif isinstance(test_input, str):
        test_input = str(shape_file_dir_path / test_input)
    else:
        test_input = [str(shape_file_dir_path / x) for x in test_input if isinstance(x, str)]

    with pytest.raises(ShapeFileNotFoundError):
        _shape_file_path = Aggregation.validate_shape_file_path(value=test_input)  # noqa: F841


@pytest.mark.parametrize('test_input', parameters_validate_shape_file_path_exception_2)
def test_validate_shape_file_path_exception_2(test_input, shape_file_dir_path):
    """
    | Tests the exception in validate_shape_file_path() with different invalid shape file paths.

    :param str or list[str or None] test_input: invalid shape_file_path
    :param Path shape_file_dir_path: path to the shape file directory
    :returns: None
    :rtype: None
    """
    if test_input is None:
        pass
    elif isinstance(test_input, str):
        test_input = str(shape_file_dir_path / test_input)
    else:
        test_input = [str(shape_file_dir_path / x) for x in test_input if isinstance(x, str)]

    with pytest.raises(ShapeFileExtensionError):
        _shape_file_path = Aggregation.validate_shape_file_path(value=test_input)  # noqa: F841


@pytest.mark.parametrize('test_input, expected', parameters_Aggregation)
def test_Aggregation(test_input,
                     expected,
                     shape_file_dir_path):
    """
    | Tests Aggregation with different values.

    :param list[int or str or None or list] test_input: values
    :param list[list] expected: validated values
    :param Path shape_file_dir_path: path to the shape file directory
    :returns: None
    :rtype: None
    """
    if test_input[1] is None:
        pass
    elif isinstance(test_input[1], str):
        test_input[1] = str(shape_file_dir_path / test_input[1])
    else:
        test_input[1] = [str(shape_file_dir_path / x) for x in test_input[1] if isinstance(x, str)]

    expected[1] = [str(shape_file_dir_path / x) for x in expected[1] if isinstance(x, str)]

    aggregation = Aggregation(tile_size=test_input[0],
                              shape_file_path=test_input[1])

    assert isinstance(aggregation.tile_size, type(expected[0]))
    assert isinstance(aggregation.shape_file_path, type(expected[1]))
    assert aggregation.tile_size == expected[0]
    assert aggregation.shape_file_path == expected[1]


@pytest.mark.parametrize('test_input', parameters_validate_tile_size_exception)
def test_Aggregation_exception_1(test_input):
    """
    | Tests the exception in Aggregation with different invalid values.

    :param int test_input: invalid value
    :returns: None
    :rtype: None
    """
    with pytest.raises(TileSizeError):
        _aggregation = Aggregation(tile_size=test_input,  # noqa: F841
                                   shape_file_path=None)


@pytest.mark.parametrize('test_input', parameters_validate_shape_file_path_exception_1)
def test_Aggregation_exception_2(test_input, shape_file_dir_path):
    """
    | Tests the exception in Aggregation with different invalid values.

    :param str or list[str or None] test_input: invalid value
    :param Path shape_file_dir_path: path to the shape file directory
    :returns: None
    :rtype: None
    """
    if isinstance(test_input, str):
        test_input = str(shape_file_dir_path / test_input)
    else:
        test_input = [str(shape_file_dir_path / x) for x in test_input if isinstance(x, str)]

    with pytest.raises(ShapeFileNotFoundError):
        _aggregation = Aggregation(tile_size=None,  # noqa: F841
                                   shape_file_path=test_input)


@pytest.mark.parametrize('test_input', parameters_validate_shape_file_path_exception_2)
def test_Aggregation_exception_3(test_input, shape_file_dir_path):
    """
    | Tests the exception in Aggregation with different invalid values.

    :param str or list[str or None] test_input: invalid value
    :param Path shape_file_dir_path: path to the shape file directory
    :returns: None
    :rtype: None
    """
    if isinstance(test_input, str):
        test_input = str(shape_file_dir_path / test_input)
    else:
        test_input = [str(shape_file_dir_path / x) for x in test_input if isinstance(x, str)]

    with pytest.raises(ShapeFileExtensionError):
        _aggregation = Aggregation(tile_size=None,  # noqa: F841
                                   shape_file_path=test_input)


def test_Aggregation_default():
    """
    | Tests the default values in Aggregation.

    :returns: None
    :rtype: None
    """
    aggregation = Aggregation()

    assert isinstance(aggregation, Aggregation)
    assert list(aggregation.__dict__.keys()) == ['tile_size', 'shape_file_path']
    assert aggregation.tile_size is None
    assert aggregation.shape_file_path is None
