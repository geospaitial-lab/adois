# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import pytest

from src.preprocessing.coordinates import get_coordinates


@pytest.mark.parametrize('test_input, expected',
                         [((256, 256, 512, 512), [(256., 384.), (384., 384.), (256., 512.), (384., 512.)]),
                          ((256, -512, 512, -256), [(256., -384.), (384., -384.), (256., -256.), (384., -256.)]),
                          ((-512, -512, -256, -256), [(-512., -384.), (-384., -384.), (-512., -256.), (-384., -256.)]),
                          ((-512, 256, -256, 512), [(-512., 384.), (-384., 384.), (-512., 512.), (-384., 512.)]),
                          ((-128, -128, 128, 128), [(-128., 0.), (0., 0.), (-128., 128.), (0., 128.)])])
def test_get_coordinates(test_input, expected):
    """Tests get_coordinates() with different bounding boxes and an image_size of 640.
    The tiles fit in the bounding boxes without remainder.

    :param (int, int, int, int) test_input: bounding box (x_1, y_1, x_2, y_2) of the area from
        the bottom left corner to the top right corner
    :param list[(float, float)] expected: coordinates
    :returns: None
    :rtype: None
    """
    coordinates = get_coordinates(bounding_box=test_input,
                                  image_size=640)
    assert coordinates == expected


@pytest.mark.parametrize('test_input, expected',
                         [((256, 256, 480, 480), [(256., 384.), (384., 384.), (256., 512.), (384., 512.)]),
                          ((256, -512, 480, -288), [(256., -384.), (384., -384.), (256., -256.), (384., -256.)]),
                          ((-512, -512, -288, -288), [(-512., -384.), (-384., -384.), (-512., -256.), (-384., -256.)]),
                          ((-512, 256, -288, 480), [(-512., 384.), (-384., 384.), (-512., 512.), (-384., 512.)]),
                          ((-128, -128, 96, 96), [(-128., 0.), (0., 0.), (-128., 128.), (0., 128.)])])
def test_get_coordinates_remainder(test_input, expected):
    """Tests get_coordinates() with different bounding boxes and an image_size of 640.
    The tiles do not fit in the bounding boxes without remainder.

    :param (int, int, int, int) test_input: bounding box (x_1, y_1, x_2, y_2) of the area from
        the bottom left corner to the top right corner
    :param list[(float, float)] expected: coordinates
    :returns: None
    :rtype: None
    """
    coordinates = get_coordinates(bounding_box=test_input,
                                  image_size=640)
    assert coordinates == expected
