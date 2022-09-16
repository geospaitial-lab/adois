# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from pathlib import Path

import numpy as np
import pytest

from src.preprocessing.preprocessor import Preprocessor


DATA_DIR_PATH = Path(__file__).resolve().parents[0] / 'data'

test_resize_image_test_input_large = np.load(DATA_DIR_PATH / 'test_resize_image_test_input_large.npy')
test_resize_image_test_input_small = np.load(DATA_DIR_PATH / 'test_resize_image_test_input_small.npy')
test_resize_image_expected = np.load(DATA_DIR_PATH / 'test_resize_image_expected.npy')

parameters_resize_image = [(test_resize_image_test_input_large, test_resize_image_expected),  # downsampling
                           (test_resize_image_test_input_small, test_resize_image_expected)]  # upsampling

test_get_image_test_input_ndsm_large = np.load(DATA_DIR_PATH / 'test_get_image_test_input_ndsm_large.npy')
test_get_image_test_input_ndsm_small = np.load(DATA_DIR_PATH / 'test_get_image_test_input_ndsm_small.npy')
test_get_image_expected = np.load(DATA_DIR_PATH / 'test_get_image_expected.npy')

parameters_get_image = [(test_get_image_test_input_ndsm_large, test_get_image_expected),  # downsampling
                        (test_get_image_test_input_ndsm_small, test_get_image_expected)]  # upsampling


def test_init(color_codes):
    """
    | Tests __init__().

    :param dict[tuple[int, int, int], int] color_codes: color codes
    :returns: None
    :rtype: None
    """
    preprocessor = Preprocessor(color_codes=color_codes)
    expected = np.load(DATA_DIR_PATH / 'test_init_expected.npy')

    np.testing.assert_array_equal(preprocessor.color_map, expected)
    assert preprocessor.color_map.dtype == expected.dtype


def test_get_color_map(color_codes):
    """
    | Tests get_color_map().

    :param dict[tuple[int, int, int], int] color_codes: color codes
    :returns: None
    :rtype: None
    """
    color_map = Preprocessor.get_color_map(color_codes=color_codes)
    expected = np.load(DATA_DIR_PATH / 'test_get_color_map_expected.npy')

    np.testing.assert_array_equal(color_map, expected)
    assert color_map.dtype == expected.dtype


@pytest.mark.parametrize('test_input, expected', parameters_resize_image)
def test_resize_image(test_input, expected):
    """
    | Tests resize_image() with different image sizes for downsampling and upsampling.

    :param np.ndarray[np.uint8] test_input: image
    :param np.ndarray[np.uint8] expected: resized image
    :returns: None
    :rtype: None
    """
    resized_image = Preprocessor.resize_image(image=test_input)

    np.testing.assert_array_equal(resized_image, expected)
    assert resized_image.dtype == expected.dtype


def test_reduce_dimensions(preprocessor):
    """
    | Tests reduce_dimensions().

    :param Preprocessor preprocessor: preprocessor
    :returns: None
    :rtype: None
    """
    test_input = np.load(DATA_DIR_PATH / 'test_reduce_dimensions_test_input.npy')
    color_mapped_image = preprocessor.reduce_dimensions(image=test_input)
    expected = np.load(DATA_DIR_PATH / 'test_reduce_dimensions_expected.npy')

    np.testing.assert_array_equal(color_mapped_image, expected)
    assert color_mapped_image.dtype == expected.dtype


def test_normalize_image():
    """
    | Tests normalize_image().

    :returns: None
    :rtype: None
    """
    test_input = np.load(DATA_DIR_PATH / 'test_normalize_image_test_input.npy')
    normalized_image = Preprocessor.normalize_image(image=test_input)
    expected = np.load(DATA_DIR_PATH / 'test_normalize_image_expected.npy')

    np.testing.assert_array_equal(normalized_image, expected)
    assert normalized_image.dtype == expected.dtype


@pytest.mark.parametrize('test_input, expected', parameters_get_image)
def test_get_image(test_input,
                   expected,
                   preprocessor):
    """
    | Tests get_image() with different ndsm image sizes for downsampling and upsampling.

    :param np.ndarray[np.uint8] test_input: ndsm image
    :param np.ndarray[np.float32] expected: image
    :param Preprocessor preprocessor: preprocessor
    :returns: None
    :rtype: None
    """
    test_input_rgb = np.load(DATA_DIR_PATH / 'test_get_image_test_input_rgb.npy')
    test_input_nir = np.load(DATA_DIR_PATH / 'test_get_image_test_input_nir.npy')
    image = preprocessor.get_image(rgb_image=test_input_rgb,
                                   nir_image=test_input_nir,
                                   ndsm_image=test_input)

    np.testing.assert_array_equal(image, expected)
    assert image.dtype == expected.dtype
