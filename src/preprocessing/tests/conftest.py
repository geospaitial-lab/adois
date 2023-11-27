import unittest.mock as mock

import pytest

from src.preprocessing.image_builder import ImageBuilder
from src.preprocessing.preprocessing_strategies import (
    Float32Casting,
    PreprocessingStrategy,
    UInt8LinearScalingNormalization)


@pytest.fixture(scope='session')
def float32_casting():
    """
    | Returns a float32 casting object.

    :returns: float32 casting fixture
    :rtype: Float32Casting
    """
    return Float32Casting()


@pytest.fixture(scope='function')
def image_builder_without_preprocessing_strategies():
    """
    | Returns an image builder object without any preprocessing strategies.

    :returns: image builder fixture
    :rtype: ImageBuilder
    """
    return ImageBuilder(preprocessing_strategies=[])


@pytest.fixture(scope='function')
def image_builder_with_mocked_preprocessing_strategy(mocked_preprocessing_strategy):
    """
    | Returns an image builder object with a mocked preprocessing strategy.

    :param PreprocessingStrategy mocked_preprocessing_strategy: mocked preprocessing strategy fixture
    :returns: image builder fixture
    :rtype: ImageBuilder
    """
    return ImageBuilder(preprocessing_strategies=[mocked_preprocessing_strategy])


@pytest.fixture(scope='function')
def image_builder_with_mocked_preprocessing_strategies(mocked_preprocessing_strategy):
    """
    | Returns an image builder object with multiple mocked preprocessing strategies.

    :param PreprocessingStrategy mocked_preprocessing_strategy: mocked preprocessing strategy fixture
    :returns: image builder fixture
    :rtype: ImageBuilder
    """
    preprocessing_strategies = [mocked_preprocessing_strategy, mocked_preprocessing_strategy]
    image_builder = ImageBuilder(preprocessing_strategies=preprocessing_strategies)
    return image_builder


@pytest.fixture(scope='session')
def mocked_preprocessing_strategy():
    """
    | Returns a mocked preprocessing strategy object.

    :returns: mocked preprocessing strategy fixture
    :rtype: PreprocessingStrategy
    """
    return mock.Mock(spec=PreprocessingStrategy)


@pytest.fixture(scope='session')
def uint8_linear_scaling_normalization():
    """
    | Returns an uint8 linear scaling normalization object.

    :returns: uint8 linear scaling normalization fixture
    :rtype: UInt8LinearScalingNormalization
    """
    return UInt8LinearScalingNormalization()
