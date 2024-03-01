import unittest.mock as mock

import pytest

from src.preprocessing.image_builder import ImageBuilder

from src.preprocessing.preprocessing_strategies import (
    Float32Casting,
    PreprocessingStrategy,
    UInt8LinearScalingNormalization)


@pytest.fixture(scope='session')
def float32_casting() -> Float32Casting:
    """
    | Returns a float32 casting object.

    :returns: float32 casting fixture
    """
    return Float32Casting()


@pytest.fixture(scope='function')
def image_builder_without_preprocessing_strategies() -> ImageBuilder:
    """
    | Returns an image builder object without any preprocessing strategies.

    :returns: image builder fixture
    """
    return ImageBuilder(preprocessing_strategies=[])


@pytest.fixture(scope='function')
def image_builder_with_mocked_preprocessing_strategy(
        mocked_preprocessing_strategy: PreprocessingStrategy) -> ImageBuilder:
    """
    | Returns an image builder object with a mocked preprocessing strategy.

    :param mocked_preprocessing_strategy: mocked preprocessing strategy fixture
    :returns: image builder fixture
    """
    return ImageBuilder(preprocessing_strategies=[mocked_preprocessing_strategy])


@pytest.fixture(scope='function')
def image_builder_with_mocked_preprocessing_strategies(
        mocked_preprocessing_strategy: PreprocessingStrategy) -> ImageBuilder:
    """
    | Returns an image builder object with multiple mocked preprocessing strategies.

    :param mocked_preprocessing_strategy: mocked preprocessing strategy fixture
    :returns: image builder fixture
    """
    preprocessing_strategies = [mocked_preprocessing_strategy, mocked_preprocessing_strategy]
    image_builder = ImageBuilder(preprocessing_strategies=preprocessing_strategies)
    return image_builder


@pytest.fixture(scope='session')
def mocked_preprocessing_strategy() -> PreprocessingStrategy:
    """
    | Returns a mocked preprocessing strategy object.

    :returns: mocked preprocessing strategy fixture
    """
    return mock.Mock(spec=PreprocessingStrategy)


@pytest.fixture(scope='session')
def uint8_linear_scaling_normalization() -> UInt8LinearScalingNormalization:
    """
    | Returns an uint8 linear scaling normalization object.

    :returns: uint8 linear scaling normalization fixture
    """
    return UInt8LinearScalingNormalization()
