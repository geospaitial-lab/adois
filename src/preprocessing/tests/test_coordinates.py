# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import pytest

from src.preprocessing.coordinates import get_coordinates


@pytest.mark.parametrize('test_input, expected',
                         [((512, 512, 1024, 1024),
                           [(512., 768.), (768., 768.), (512., 1024.), (768., 1024.)]),
                          ((512, -1024, 1024, -512),
                           [(512., -768.), (768., -768.), (512., -512.), (768., -512.)]),
                          ((-1024, -1024, -512, -512),
                           [(-1024., -768.), (-768., -768.), (-1024., -512.), (-768., -512.)]),
                          ((-1024, 512, -512, 1024),
                           [(-1024., 768.), (-768., 768.), (-1024., 1024.), (-768., 1024.)]),
                          ((-256, -256, 256, 256),
                           [(-256., 0.), (0., 0.), (-256., 256.), (0., 256.)])])
def test_get_coordinates(test_input, expected):
    """Tests get_coordinates() with different bounding boxes and an image_size of 1280.
    The tiles fit in the bounding boxes without remainder.

    :param (int, int, int, int) test_input: bounding box (x_1, y_1, x_2, y_2) of the area from
        the bottom left corner to the top right corner
    :param list[(float, float)] expected: coordinates
    :returns: None
    :rtype: None
    """
    coordinates = get_coordinates(bounding_box=test_input,
                                  image_size=1280)
    assert coordinates == expected

    for coordinates_element in coordinates:
        assert type(coordinates_element[0]) is float
        assert type(coordinates_element[1]) is float


@pytest.mark.parametrize('test_input, expected',
                         [((512, 512, 896, 896),
                           [(512., 768.), (768., 768.), (512., 1024.), (768., 1024.)]),
                          ((512, -1024, 896, -640),
                           [(512., -768.), (768., -768.), (512., -512.), (768., -512.)]),
                          ((-1024, -1024, -640, -640),
                           [(-1024., -768.), (-768., -768.), (-1024., -512.), (-768., -512.)]),
                          ((-1024, 512, -640, 896),
                           [(-1024., 768.), (-768., 768.), (-1024., 1024.), (-768., 1024.)]),
                          ((-256, -256, 128, 128),
                           [(-256., 0.), (0., 0.), (-256., 256.), (0., 256.)])])
def test_get_coordinates_remainder(test_input, expected):
    """Tests get_coordinates() with different bounding boxes and an image_size of 1280.
    The tiles do not fit in the bounding boxes without remainder.

    :param (int, int, int, int) test_input: bounding box (x_1, y_1, x_2, y_2) of the area from
        the bottom left corner to the top right corner
    :param list[(float, float)] expected: coordinates
    :returns: None
    :rtype: None
    """
    coordinates = get_coordinates(bounding_box=test_input,
                                  image_size=1280)
    assert coordinates == expected

    for coordinates_element in coordinates:
        assert type(coordinates_element[0]) is float
        assert type(coordinates_element[1]) is float
