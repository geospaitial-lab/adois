# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from pathlib import Path

import pytest

from src.preprocessing.coordinates import filter_coordinates, get_coordinates


parameters_get_coordinates = \
    [((512, 512, 1024, 1024),  # no quantization, no remainder
      [(512, 768), (768, 768), (512, 1024), (768, 1024)]),
     ((512, -1024, 1024, -512),
      [(512, -768), (768, -768), (512, -512), (768, -512)]),
     ((-1024, -1024, -512, -512),
      [(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)]),
     ((-1024, 512, -512, 1024),
      [(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)]),
     ((-256, -256, 256, 256),
      [(-256, 0), (0, 0), (-256, 256), (0, 256)]),
     ((640, 640, 1024, 1024),  # quantization, no remainder
      [(512, 768), (768, 768), (512, 1024), (768, 1024)]),
     ((640, -896, 1024, -512),
      [(512, -768), (768, -768), (512, -512), (768, -512)]),
     ((-896, -896, -512, -512),
      [(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)]),
     ((-896, 640, -512, 1024),
      [(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)]),
     ((-128, -128, 256, 256),
      [(-256, 0), (0, 0), (-256, 256), (0, 256)]),
     ((512, 512, 896, 896),  # no quantization, remainder
      [(512, 768), (768, 768), (512, 1024), (768, 1024)]),
     ((512, -1024, 896, -640),
      [(512, -768), (768, -768), (512, -512), (768, -512)]),
     ((-1024, -1024, -640, -640),
      [(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)]),
     ((-1024, 512, -640, 896),
      [(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)]),
     ((-256, -256, 128, 128),
      [(-256, 0), (0, 0), (-256, 256), (0, 256)]),
     ((640, 640, 896, 896),  # quantization, remainder
      [(512, 768), (768, 768), (512, 1024), (768, 1024)]),
     ((640, -896, 896, -640),
      [(512, -768), (768, -768), (512, -512), (768, -512)]),
     ((-896, -896, -640, -640),
      [(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)]),
     ((-896, 640, -640, 896),
      [(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)]),
     ((-128, -128, 128, 128),
      [(-256, 0), (0, 0), (-256, 256), (0, 256)])]

parameters_filter_coordinates_empty_tiles_dir = \
    [([(512, 768), (768, 768), (512, 1024), (768, 1024)],
      [(512, 768), (768, 768), (512, 1024), (768, 1024)]),
     ([(512, -768), (768, -768), (512, -512), (768, -512)],
      [(512, -768), (768, -768), (512, -512), (768, -512)]),
     ([(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)],
      [(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)]),
     ([(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)],
      [(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)]),
     ([(-256, 0), (0, 0), (-256, 256), (0, 256)],
      [(-256, 0), (0, 0), (-256, 256), (0, 256)])]

parameters_filter_coordinates_not_empty_tiles_dir = \
    [([(512, 768), (768, 768), (512, 1024), (768, 1024)],  # some tiles are already being processed
      [(512, 768), (768, 768)]),
     ([(512, -768), (768, -768), (512, -512), (768, -512)],
      [(512, -768), (768, -768)]),
     ([(-1024, -768), (-768, -768), (-1024, -512), (-768, -512)],
      [(-1024, -768), (-768, -768)]),
     ([(-1024, 768), (-768, 768), (-1024, 1024), (-768, 1024)],
      [(-1024, 768), (-768, 768)]),
     ([(-256, 0), (0, 0), (-256, 256), (0, 256)],
      [(-256, 0), (0, 0)]),
     ([(512, 1024), (768, 1024)],  # all tiles are already being processed
      []),
     ([(512, -512), (768, -512)],
      []),
     ([(-1024, -512), (-768, -512)],
      []),
     ([(-1024, 1024), (-768, 1024)],
      []),
     ([(-256, 256), (0, 256)],
      [])]


@pytest.mark.parametrize('test_input, expected', parameters_get_coordinates)
def test_get_coordinates(test_input, expected):
    """Tests get_coordinates() with different bounding boxes.

    :param (int, int, int, int) test_input: bounding box (x_1, y_1, x_2, y_2) of the area from
        the bottom left corner to the top right corner
    :param list[(int, int)] expected: coordinates (x, y) of each tile
    :returns: None
    :rtype: None
    """
    coordinates = get_coordinates(bounding_box=test_input)

    assert coordinates == expected

    for coordinates_element in coordinates:
        assert type(coordinates_element[0]) is int
        assert type(coordinates_element[1]) is int


@pytest.mark.parametrize('test_input, expected', parameters_filter_coordinates_empty_tiles_dir)
def test_filter_coordinates_empty_tiles_dir(test_input,
                                            expected,
                                            output_dir_path_empty_tiles_dir):
    """Tests filter_coordinates() with different coordinates.
    The .tiles directory is empty.

    :param list[(int, int)] test_input: coordinates (x, y) of each tile
    :param list[(int, int)] expected: filtered coordinates (x, y) of each tile
    :param Path output_dir_path_empty_tiles_dir: path to the output directory
    :returns: None
    :rtype: None
    """
    filtered_coordinates = filter_coordinates(coordinates=test_input,
                                              output_dir_path=output_dir_path_empty_tiles_dir)

    assert filtered_coordinates == expected

    for filtered_coordinates_element in filtered_coordinates:
        assert type(filtered_coordinates_element[0]) is int
        assert type(filtered_coordinates_element[1]) is int


@pytest.mark.parametrize('test_input, expected', parameters_filter_coordinates_not_empty_tiles_dir)
def test_filter_coordinates_not_empty_tiles_dir(test_input,
                                                expected,
                                                output_dir_path_not_empty_tiles_dir):
    """Tests filter_coordinates() with different coordinates.
    The .tiles directory is not empty.

    :param list[(int, int)] test_input: coordinates (x, y) of each tile
    :param list[(int, int)] expected: filtered coordinates (x, y) of each tile
    :param Path output_dir_path_not_empty_tiles_dir: path to the output directory
    :returns: None
    :rtype: None
    """
    filtered_coordinates = filter_coordinates(coordinates=test_input,
                                              output_dir_path=output_dir_path_not_empty_tiles_dir)

    assert filtered_coordinates == expected

    for filtered_coordinates_element in filtered_coordinates:
        assert type(filtered_coordinates_element[0]) is int
        assert type(filtered_coordinates_element[1]) is int
