import numpy as np
import pytest

from src.preprocessing.image_builder import *
from src.preprocessing.preprocessing_strategies import PreprocessingStrategy
from src.preprocessing.tests.data.data_test_image_builder import *

parameters_image_builders = ['image_builder_without_preprocessing_strategies',
                             'image_builder_with_preprocessing_strategy']


@pytest.mark.parametrize('test_input, expected', parameters_init)
def test_init(test_input, expected):
    """
    | Tests __init__().

    :param list[PreprocessingStrategy] test_input: preprocessing strategies
    :param list[PreprocessingStrategy] expected: preprocessing strategies
    :returns: None
    :rtype: None
    """
    image_builder = ImageBuilder(preprocessing_strategies=test_input)

    assert isinstance(image_builder, ImageBuilder)
    assert list(image_builder.__dict__.keys()) == ['image_rgb', 'image_nir', 'preprocessing_strategies']
    assert image_builder.image_rgb is None
    assert image_builder.image_nir is None
    assert isinstance(image_builder.preprocessing_strategies, list)
    assert all(isinstance(preprocessing_strategy, type(expected[i]))
               for i, preprocessing_strategy in enumerate(image_builder.preprocessing_strategies))


@pytest.mark.parametrize('test_input, expected', parameters_set_image_rgb)
@pytest.mark.parametrize('image_builder', parameters_image_builders)
def test_set_image_rgb(test_input,
                       expected,
                       image_builder,
                       request):
    """
    | Tests set_image_rgb().

    :param np.ndarray[np.uint8] test_input: rgb image
    :param np.ndarray[np.uint8] expected: rgb image
    :param ImageBuilder image_builder: image builder
    :param request: request
    :returns: None
    :rtype: None
    """
    image_builder = request.getfixturevalue(image_builder)

    image_builder.image_rgb = None
    image_builder.set_image_rgb(test_input)

    assert isinstance(image_builder.image_rgb, np.ndarray)
    assert image_builder.image_rgb.dtype == np.uint8
    assert len(image_builder.image_rgb.shape) == 3
    assert image_builder.image_rgb.shape[-1] == 3
    # noinspection PyTypeChecker
    np.testing.assert_array_equal(image_builder.image_rgb, expected)


@pytest.mark.parametrize('test_input, expected', parameters_set_image_nir)
@pytest.mark.parametrize('image_builder', parameters_image_builders)
def test_set_image_nir(test_input,
                       expected,
                       image_builder,
                       request):
    """
    | Tests set_image_nir().

    :param np.ndarray[np.uint8] test_input: nir image
    :param np.ndarray[np.uint8] expected: nir image
    :param ImageBuilder image_builder: image builder
    :param request: request
    :returns: None
    :rtype: None
    """
    image_builder = request.getfixturevalue(image_builder)

    image_builder.image_nir = None
    image_builder.set_image_nir(test_input)

    assert isinstance(image_builder.image_nir, np.ndarray)
    assert image_builder.image_nir.dtype == np.uint8
    assert len(image_builder.image_nir.shape) == 3
    assert image_builder.image_nir.shape[-1] == 1
    # noinspection PyTypeChecker
    np.testing.assert_array_equal(image_builder.image_nir, expected)


@pytest.mark.parametrize('test_input, expected', parameters_set_preprocessing_strategies)
@pytest.mark.parametrize('image_builder', parameters_image_builders)
def test_set_preprocessing_strategies(test_input,
                                      expected,
                                      image_builder,
                                      request):
    """
    | Tests set_preprocessing_strategies().

    :param list[PreprocessingStrategy] test_input: preprocessing strategies
    :param list[PreprocessingStrategy] expected: preprocessing strategies
    :param ImageBuilder image_builder: image builder
    :param request: request
    :returns: None
    :rtype: None
    """
    image_builder = request.getfixturevalue(image_builder)

    image_builder.set_preprocessing_strategies(test_input)

    assert isinstance(image_builder.preprocessing_strategies, list)
    assert all(isinstance(preprocessing_strategy, type(expected[i]))
               for i, preprocessing_strategy in enumerate(image_builder.preprocessing_strategies))


@pytest.mark.parametrize('test_input', parameters_reset)
@pytest.mark.parametrize('image_builder', parameters_image_builders)
def test_reset(test_input,
               image_builder,
               request):
    """
    | Tests reset().

    :param np.ndarray[np.uint8] test_input: image
    :param ImageBuilder image_builder: image builder
    :param request: request
    :returns: None
    :rtype: None
    """
    image_builder = request.getfixturevalue(image_builder)

    image_builder.image_rgb = test_input
    image_builder.image_nir = test_input
    image_builder.reset()

    assert image_builder.image_rgb is None
    assert image_builder.image_nir is None


@pytest.mark.skip(reason='Test not implemented yet.')
def test_concatenate_images():
    pass


@pytest.mark.skip(reason='Test not implemented yet.')
def test_preprocess():
    pass


@pytest.mark.skip(reason='Test not implemented yet.')
def test_build():
    pass
