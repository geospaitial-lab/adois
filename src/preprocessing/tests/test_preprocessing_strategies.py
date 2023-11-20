import numpy as np
import pytest

from src.preprocessing.preprocessing_strategies import Float32Casting, UInt8LinearScalingNormalization
from src.preprocessing.tests.data.data_test_preprocessing_strategies import (
    parameters_float32_casting_preprocess,
    parameters_uint8_linear_scaling_normalization_preprocess)


def test_float32_casting_init():
    """
    | Tests __init__().

    :returns: None
    :rtype: None
    """
    float32_casting = Float32Casting()

    assert isinstance(float32_casting, Float32Casting)
    assert list(float32_casting.__dict__.keys()) == []


@pytest.mark.parametrize('test_input, expected', parameters_float32_casting_preprocess)
def test_float32_casting_preprocess(test_input,
                                    expected,
                                    float32_casting):
    """
    | Tests preprocess().

    :param np.ndarray test_input: image
    :param np.ndarray[np.float32] expected: preprocessed image
    :param Float32Casting float32_casting: float32 casting
    :returns: None
    :rtype: None
    """
    image = float32_casting.preprocess(test_input)

    assert isinstance(image, np.ndarray)
    assert image.dtype == np.float32
    assert image.shape == expected.shape
    np.testing.assert_array_equal(image, expected)


def test_uint8_linear_scaling_normalization_init():
    """
    | Tests __init__().

    :returns: None
    :rtype: None
    """
    uint8_linear_scaling_normalization = UInt8LinearScalingNormalization()

    assert isinstance(uint8_linear_scaling_normalization, UInt8LinearScalingNormalization)
    assert list(uint8_linear_scaling_normalization.__dict__.keys()) == []


@pytest.mark.parametrize('test_input, expected', parameters_uint8_linear_scaling_normalization_preprocess)
def test_uint8_linear_scaling_normalization_preprocess(test_input,
                                                       expected,
                                                       uint8_linear_scaling_normalization):
    """
    | Tests preprocess().

    :param np.ndarray[np.uint8] test_input: image
    :param np.ndarray[np.float32] expected: preprocessed image
    :param UInt8LinearScalingNormalization uint8_linear_scaling_normalization: uint8 linear scaling normalization
    :returns: None
    :rtype: None
    """
    image = uint8_linear_scaling_normalization.preprocess(test_input)

    assert isinstance(image, np.ndarray)
    assert image.dtype == np.float32
    assert image.shape == expected.shape
    np.testing.assert_array_equal(image, expected)
