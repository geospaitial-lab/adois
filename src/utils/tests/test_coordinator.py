# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from pathlib import Path

import geopandas as gpd
import pytest

from src.utils.coordinator import Coordinator
from src.utils.tests.data import tests_data


def test_init():
    """
    | Tests __init__().

    :returns: None
    :rtype: None
    """
    coordinator = Coordinator()

    assert isinstance(coordinator, Coordinator)
    assert list(coordinator.__dict__.keys()) == []


@pytest.mark.parametrize('test_input, expected', tests_data.parameters_get_coordinates)
def test_get_coordinates(test_input,
                         expected,
                         coordinator):
    """
    | Tests get_coordinates() with different bounding boxes.

    :param (int, int, int, int) test_input: bounding box (x_1, y_1, x_2, y_2) of the area from
        the bottom left corner to the top right corner
    :param list[(int, int)] expected: coordinates (x, y) of each tile
    :param Coordinator coordinator: coordinator
    :returns: None
    :rtype: None
    """
    coordinates = coordinator.get_coordinates(bounding_box=test_input)

    assert coordinates == expected

    for coordinates_element in coordinates:
        assert isinstance(coordinates_element[0], int)
        assert isinstance(coordinates_element[1], int)


@pytest.mark.parametrize('test_input, expected', tests_data.parameters_filter_cached_coordinates_empty_tiles_dir)
def test_filter_cached_coordinates_empty_tiles_dir(test_input,
                                                   expected,
                                                   coordinator,
                                                   output_dir_path_empty_tiles_dir):
    """
    | Tests filter_cached_coordinates() with different coordinates.
    | The .tiles directory is empty.

    :param list[(int, int)] test_input: coordinates (x, y) of each tile
    :param list[(int, int)] expected: filtered coordinates (x, y) of each tile
    :param Coordinator coordinator: coordinator
    :param Path output_dir_path_empty_tiles_dir: path to the output directory
    :returns: None
    :rtype: None
    """
    filtered_coordinates = coordinator.filter_cached_coordinates(coordinates=test_input,
                                                                 output_dir_path=output_dir_path_empty_tiles_dir)

    assert filtered_coordinates == expected

    for filtered_coordinates_element in filtered_coordinates:
        assert isinstance(filtered_coordinates_element[0], int)
        assert isinstance(filtered_coordinates_element[1], int)


@pytest.mark.parametrize('test_input, expected', tests_data.parameters_filter_cached_coordinates_not_empty_tiles_dir)
def test_filter_cached_coordinates_not_empty_tiles_dir(test_input,
                                                       expected,
                                                       coordinator,
                                                       output_dir_path_not_empty_tiles_dir):
    """
    | Tests filter_cached_coordinates() with different coordinates.
    | The .tiles directory is not empty.

    :param list[(int, int)] test_input: coordinates (x, y) of each tile
    :param list[(int, int)] expected: filtered coordinates (x, y) of each tile
    :param Coordinator coordinator: coordinator
    :param Path output_dir_path_not_empty_tiles_dir: path to the output directory
    :returns: None
    :rtype: None
    """
    filtered_coordinates = coordinator.filter_cached_coordinates(coordinates=test_input,
                                                                 output_dir_path=output_dir_path_not_empty_tiles_dir)

    assert filtered_coordinates == expected

    for filtered_coordinates_element in filtered_coordinates:
        assert isinstance(filtered_coordinates_element[0], int)
        assert isinstance(filtered_coordinates_element[1], int)


@pytest.mark.parametrize('test_input, expected', tests_data.parameters_get_valid_coordinates)
def test_get_valid_coordinates(test_input,
                               expected,
                               coordinator,
                               boundary_gdf):
    """
    | Tests get_valid_coordinates() with different bounding boxes.

    :param (int, int, int, int) test_input: bounding box (x_1, y_1, x_2, y_2) of the area from
        the bottom left corner to the top right corner
    :param list[(int, int)] expected: valid coordinates (x, y) of each tile
    :param Coordinator coordinator: coordinator
    :param gpd.GeoDataFrame boundary_gdf: boundary geodataframe
    :returns: None
    :rtype: None
    """
    valid_coordinates = coordinator.get_valid_coordinates(bounding_box=test_input,
                                                          epsg_code=25832,
                                                          boundary_gdf=boundary_gdf)

    assert valid_coordinates == expected

    for valid_coordinates_element in valid_coordinates:
        assert isinstance(valid_coordinates_element[0], int)
        assert isinstance(valid_coordinates_element[1], int)
