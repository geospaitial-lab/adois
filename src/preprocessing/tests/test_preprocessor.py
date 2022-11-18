# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from pathlib import Path

import numpy as np

from src.preprocessing.preprocessor import Preprocessor


DATA_DIR_PATH = Path(__file__).resolve().parents[0] / 'data'


def test_init():
    """
    | Tests __init__().

    :returns: None
    :rtype: None
    """
    preprocessor = Preprocessor()

    assert isinstance(preprocessor, Preprocessor)


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


def test_get_image(preprocessor):
    """
    | Tests get_image().

    :param Preprocessor preprocessor: preprocessor
    :returns: None
    :rtype: None
    """
    test_input_rgb = np.load(DATA_DIR_PATH / 'test_get_image_test_input_rgb.npy')
    test_input_nir = np.load(DATA_DIR_PATH / 'test_get_image_test_input_nir.npy')
    image = preprocessor.get_image(rgb_image=test_input_rgb,
                                   nir_image=test_input_nir)
    expected = np.load(DATA_DIR_PATH / 'test_get_image_expected.npy')

    np.testing.assert_array_equal(image, expected)
    assert image.dtype == expected.dtype
