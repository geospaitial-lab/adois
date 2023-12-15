import inspect

import numpy as np
import pytest

from src.preprocessing.image_builder import ImageBuilder
from src.preprocessing.preprocessing_strategies import PreprocessingStrategy

from .data.data_test_image_builder import (
    data_test_getter_image_nir,
    data_test_getter_image_rgb,
    data_test_init,
    data_test_setter_image_nir,
    data_test_setter_image_rgb)


@pytest.mark.parametrize('test_input', data_test_init)
def test_init(test_input,
              request):
    """
    | Tests __init__().

    :param list[PreprocessingStrategy] test_input: mocked preprocessing strategies fixtures
    :param request: pytest request
    :returns: None
    :rtype: None
    """
    test_input = [request.getfixturevalue(fixture) for fixture in test_input]

    image_builder = ImageBuilder(preprocessing_strategies=test_input)

    assert isinstance(image_builder, ImageBuilder)
    attributes = ['_image_rgb', '_image_nir', 'preprocessing_strategies']
    assert list(vars(image_builder).keys()) == attributes

    assert image_builder._image_rgb is None
    assert image_builder._image_nir is None
    assert isinstance(image_builder.preprocessing_strategies, list)

    conditions = [isinstance(preprocessing_strategy, PreprocessingStrategy)
                  for preprocessing_strategy in image_builder.preprocessing_strategies]

    assert all(conditions)


@pytest.mark.parametrize('test_input, expected', data_test_getter_image_rgb)
def test_getter_image_rgb(test_input,
                          expected,
                          image_builder_without_preprocessing_strategies):
    """
    | Tests the getter method of image_rgb.

    :param np.ndarray[np.uint8] or None test_input: rgb image
    :param np.ndarray[np.uint8] or None expected: rgb image
    :param ImageBuilder image_builder_without_preprocessing_strategies: image builder fixture
    :returns: None
    :rtype: None
    """
    image_builder_without_preprocessing_strategies._image_rgb = test_input

    conditions = (
        [isinstance(image_builder_without_preprocessing_strategies.image_rgb, np.ndarray),
         image_builder_without_preprocessing_strategies.image_rgb is None])

    assert any(conditions)

    if expected is not None:
        assert image_builder_without_preprocessing_strategies.image_rgb.dtype == np.uint8
        assert image_builder_without_preprocessing_strategies.image_rgb.ndim == 3
        assert image_builder_without_preprocessing_strategies.image_rgb.shape[-1] == 3
        np.testing.assert_array_equal(image_builder_without_preprocessing_strategies.image_rgb, expected)


@pytest.mark.parametrize('test_input, expected', data_test_setter_image_rgb)
def test_setter_image_rgb(test_input,
                          expected,
                          image_builder_without_preprocessing_strategies):
    """
    | Tests the setter method of image_rgb.

    :param np.ndarray[np.uint8] or None test_input: rgb image
    :param np.ndarray[np.uint8] or None expected: rgb image
    :param ImageBuilder image_builder_without_preprocessing_strategies: image builder fixture
    :returns: None
    :rtype: None
    """
    image_builder_without_preprocessing_strategies.image_rgb = test_input

    conditions = (
        [isinstance(image_builder_without_preprocessing_strategies._image_rgb, np.ndarray),
         image_builder_without_preprocessing_strategies._image_rgb is None])

    assert any(conditions)

    if expected is not None:
        assert image_builder_without_preprocessing_strategies._image_rgb.dtype == np.uint8
        assert image_builder_without_preprocessing_strategies._image_rgb.ndim == 3
        assert image_builder_without_preprocessing_strategies._image_rgb.shape[-1] == 3
        np.testing.assert_array_equal(image_builder_without_preprocessing_strategies._image_rgb, expected)


@pytest.mark.parametrize('test_input, expected', data_test_getter_image_nir)
def test_getter_image_nir(test_input,
                          expected,
                          image_builder_without_preprocessing_strategies):
    """
    | Tests the getter method of image_nir.

    :param np.ndarray[np.uint8] or None test_input: nir image
    :param np.ndarray[np.uint8] or None expected: nir image
    :param ImageBuilder image_builder_without_preprocessing_strategies: image builder fixture
    :returns: None
    :rtype: None
    """
    image_builder_without_preprocessing_strategies._image_nir = test_input

    conditions = (
        [isinstance(image_builder_without_preprocessing_strategies.image_nir, np.ndarray),
         image_builder_without_preprocessing_strategies.image_nir is None])

    assert any(conditions)

    if expected is not None:
        assert image_builder_without_preprocessing_strategies.image_nir.dtype == np.uint8
        assert image_builder_without_preprocessing_strategies.image_nir.ndim == 3
        assert image_builder_without_preprocessing_strategies.image_nir.shape[-1] == 1
        np.testing.assert_array_equal(image_builder_without_preprocessing_strategies.image_nir, expected)


@pytest.mark.parametrize('test_input, expected', data_test_setter_image_nir)
def test_setter_image_nir(test_input,
                          expected,
                          image_builder_without_preprocessing_strategies):
    """
    | Tests the setter method of image_nir.

    :param np.ndarray[np.uint8] or None test_input: nir image
    :param np.ndarray[np.uint8] or None expected: nir image
    :param ImageBuilder image_builder_without_preprocessing_strategies: image builder fixture
    :returns: None
    :rtype: None
    """
    image_builder_without_preprocessing_strategies.image_nir = test_input

    conditions = (
        [isinstance(image_builder_without_preprocessing_strategies._image_nir, np.ndarray),
         image_builder_without_preprocessing_strategies._image_nir is None])

    assert any(conditions)

    if expected is not None:
        assert image_builder_without_preprocessing_strategies._image_nir.dtype == np.uint8
        assert image_builder_without_preprocessing_strategies._image_nir.ndim == 3
        assert image_builder_without_preprocessing_strategies._image_nir.shape[-1] == 1
        np.testing.assert_array_equal(image_builder_without_preprocessing_strategies._image_nir, expected)


@pytest.mark.skip(reason='Test not implemented yet.')
def test_concatenate_images():
    pass


@pytest.mark.skip(reason='Test not implemented yet.')
def test_preprocess_image():
    pass


def test_build_image_default(image_builder_without_preprocessing_strategies):
    """
    | Tests the default values of the parameters of build_image().

    :param ImageBuilder image_builder_without_preprocessing_strategies: image builder fixture
    :returns: None
    :rtype: None
    """
    signature = inspect.signature(image_builder_without_preprocessing_strategies.build_image)
    reset_default = signature.parameters['reset'].default

    assert isinstance(reset_default, bool)
    assert reset_default is True


@pytest.mark.skip(reason='Test not implemented yet.')
def test_build_image():
    pass
