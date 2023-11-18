import pytest

from src.preprocessing.image_builder import ImageBuilder
from src.preprocessing.preprocessing_strategies import Float32Casting, UInt8LinearScalingNormalization


@pytest.fixture(scope='session')
def image_builder_without_preprocessing_strategies():
    """
    | Returns an image builder object without any preprocessing strategies.

    :returns: image builder
    :rtype: ImageBuilder
    """
    return ImageBuilder(preprocessing_strategies=[])


@pytest.fixture(scope='session')
def image_builder_with_preprocessing_strategy():
    """
    | Returns an image builder object with uint8 linear scaling normalization as the preprocessing strategy.

    :returns: image builder
    :rtype: ImageBuilder
    """
    return ImageBuilder(preprocessing_strategies=[UInt8LinearScalingNormalization()])


@pytest.fixture(scope='session')
def float32_casting():
    """
    | Returns a float32 casting object.

    :returns: float32 casting
    :rtype: Float32Casting
    """
    return Float32Casting()


@pytest.fixture(scope='session')
def uint8_linear_scaling_normalization():
    """
    | Returns an uint8 linear scaling normalization object.

    :returns: uint8 linear scaling normalization
    :rtype: UInt8LinearScalingNormalization
    """
    return UInt8LinearScalingNormalization()
