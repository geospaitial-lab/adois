import inspect

import numpy as np
import pytest

from src.preprocessing.image_builder import ImageBuilder
from src.preprocessing.preprocessing_strategies import PreprocessingStrategy
from src.preprocessing.tests.data.data_test_image_builder import (
    parameters_init,
    parameters_set_preprocessing_strategies)


@pytest.mark.parametrize('test_input', parameters_init)
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
    parameters = ['image_rgb', 'image_nir', 'preprocessing_strategies']
    assert list(image_builder.__dict__.keys()) == parameters

    assert image_builder.image_rgb is None
    assert image_builder.image_nir is None
    assert isinstance(image_builder.preprocessing_strategies, list)

    conditions = [isinstance(preprocessing_strategy, PreprocessingStrategy)
                  for preprocessing_strategy in image_builder.preprocessing_strategies]

    assert all(conditions)


def test_set_image_rgb(image_builder_without_preprocessing_strategies):
    """
    | Tests set_image_rgb().

    :param ImageBuilder image_builder_without_preprocessing_strategies: image builder fixture
    :returns: None
    :rtype: None
    """
    image_rgb = np.full(shape=(128, 128, 3),
                        fill_value=(0, 1, 2),
                        dtype=np.uint8)

    expected = np.full(shape=(128, 128, 3),
                       fill_value=(0, 1, 2),
                       dtype=np.uint8)

    image_builder_without_preprocessing_strategies.set_image_rgb(image_rgb=image_rgb)

    assert isinstance(image_builder_without_preprocessing_strategies.image_rgb, np.ndarray)
    assert image_builder_without_preprocessing_strategies.image_rgb.dtype == np.uint8
    assert len(image_builder_without_preprocessing_strategies.image_rgb.shape) == 3
    assert image_builder_without_preprocessing_strategies.image_rgb.shape[-1] == 3
    np.testing.assert_array_equal(image_builder_without_preprocessing_strategies.image_rgb, expected)


def test_set_image_nir(image_builder_without_preprocessing_strategies):
    """
    | Tests set_image_nir().

    :param ImageBuilder image_builder_without_preprocessing_strategies: image builder fixture
    :returns: None
    :rtype: None
    """
    image_nir = np.full(shape=(128, 128, 3),
                        fill_value=(0, 1, 2),
                        dtype=np.uint8)

    expected = np.full(shape=(128, 128, 1),
                       fill_value=0,
                       dtype=np.uint8)

    image_builder_without_preprocessing_strategies.set_image_nir(image_nir=image_nir)

    assert isinstance(image_builder_without_preprocessing_strategies.image_nir, np.ndarray)
    assert image_builder_without_preprocessing_strategies.image_nir.dtype == np.uint8
    assert len(image_builder_without_preprocessing_strategies.image_nir.shape) == 3
    assert image_builder_without_preprocessing_strategies.image_nir.shape[-1] == 1
    np.testing.assert_array_equal(image_builder_without_preprocessing_strategies.image_nir, expected)


@pytest.mark.parametrize('test_input', parameters_set_preprocessing_strategies)
def test_set_preprocessing_strategies(test_input,
                                      request,
                                      image_builder_without_preprocessing_strategies):
    """
    | Tests set_preprocessing_strategies().

    :param list[PreprocessingStrategy] test_input: mocked preprocessing strategies fixtures
    :param request: pytest request
    :param ImageBuilder image_builder_without_preprocessing_strategies: image builder fixture
    :returns: None
    :rtype: None
    """
    test_input = [request.getfixturevalue(fixture) for fixture in test_input]

    image_builder_without_preprocessing_strategies.set_preprocessing_strategies(test_input)

    assert isinstance(image_builder_without_preprocessing_strategies.preprocessing_strategies, list)

    conditions = [isinstance(preprocessing_strategy, PreprocessingStrategy)
                  for preprocessing_strategy in image_builder_without_preprocessing_strategies.preprocessing_strategies]

    assert all(conditions)


def test_reset_images(image_builder_without_preprocessing_strategies):
    """
    | Tests reset_images().

    :param ImageBuilder image_builder_without_preprocessing_strategies: image builder fixture
    :returns: None
    :rtype: None
    """
    image_rgb = np.full(shape=(128, 128, 3),
                        fill_value=(0, 1, 2),
                        dtype=np.uint8)

    image_nir = np.full(shape=(128, 128, 3),
                        fill_value=(0, 1, 2),
                        dtype=np.uint8)

    image_builder_without_preprocessing_strategies.image_rgb = image_rgb
    image_builder_without_preprocessing_strategies.image_nir = image_nir
    image_builder_without_preprocessing_strategies.reset_images()

    assert image_builder_without_preprocessing_strategies.image_rgb is None
    assert image_builder_without_preprocessing_strategies.image_nir is None


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
