import numpy as np
import pytest
from numpy import typing as npt

from src.preprocessing.preprocessing_strategies import Float32Casting, UInt8LinearScalingNormalization
from .data.data_test_preprocessing_strategies import data_test_float32_casting_preprocess


def test_float32_casting_init() -> None:
    float32_casting = Float32Casting()

    assert isinstance(float32_casting, Float32Casting)
    attributes = []
    assert list(vars(float32_casting).keys()) == attributes


@pytest.mark.parametrize('test_input, expected', data_test_float32_casting_preprocess)
def test_float32_casting_preprocess(test_input: npt.NDArray,
                                    expected: npt.NDArray[np.float32],
                                    float32_casting: Float32Casting) -> None:
    """
    :param test_input: image
    :param expected: preprocessed image
    :param float32_casting: float32 casting fixture
    """
    image_preprocessed = float32_casting.preprocess(image=test_input)

    assert isinstance(image_preprocessed, np.ndarray)
    assert image_preprocessed.dtype == np.float32
    assert image_preprocessed.shape == expected.shape
    np.testing.assert_array_equal(image_preprocessed, expected)


def test_uint8_linear_scaling_normalization_init() -> None:
    uint8_linear_scaling_normalization = UInt8LinearScalingNormalization()

    assert isinstance(uint8_linear_scaling_normalization, UInt8LinearScalingNormalization)
    attributes = []
    assert list(vars(uint8_linear_scaling_normalization).keys()) == attributes


def test_uint8_linear_scaling_normalization_preprocess(
        uint8_linear_scaling_normalization: UInt8LinearScalingNormalization) -> None:
    """
    :param uint8_linear_scaling_normalization: uint8 linear scaling normalization fixture
    """
    image = np.full(shape=(128, 128, 6),
                    fill_value=(0, 51, 102, 153, 204, 255),
                    dtype=np.uint8)

    expected = np.full(shape=(128, 128, 6),
                       fill_value=(0., .2, .4, .6, .8, 1.),
                       dtype=np.float32)

    image_preprocessed = uint8_linear_scaling_normalization.preprocess(image=image)

    assert isinstance(image_preprocessed, np.ndarray)
    assert image_preprocessed.dtype == np.float32
    assert image_preprocessed.shape == expected.shape
    np.testing.assert_array_equal(image_preprocessed, expected)
