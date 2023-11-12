from pathlib import Path

import geopandas as gpd
import geopandas.testing
import pytest

from src.utils.coordinator import Coordinator
from src.utils.tests.data import *


def test_init(gdf_boundary):
    """
    | Tests __init__().

    :param gpd.GeoDataFrame gdf_boundary: boundary geodataframe
    :returns: None
    :rtype: None
    """
    coordinator = Coordinator(bounding_box=(-512, -512, 512, 512),
                              epsg_code=25832,
                              gdf_boundary=gdf_boundary)

    assert isinstance(coordinator, Coordinator)
    assert list(coordinator.__dict__.keys()) == ['bounding_box', 'epsg_code', 'gdf_boundary']

    assert isinstance(coordinator.bounding_box, tuple)
    for coordinate in coordinator.bounding_box:
        assert isinstance(coordinate, int)
    assert coordinator.bounding_box == (-512, -512, 512, 512)

    assert isinstance(coordinator.epsg_code, int)
    assert coordinator.epsg_code == 25832

    assert isinstance(coordinator.gdf_boundary, gpd.GeoDataFrame)
    gpd.testing.assert_geodataframe_equal(coordinator.gdf_boundary,
                                          gdf_boundary,
                                          check_index_type=False)


@pytest.mark.parametrize('test_input, expected', parameters_get_coordinates_no_gdf_boundary)
def test_get_coordinates_no_gdf_boundary(test_input,
                                         expected):
    """
    | Tests get_coordinates() with different bounding boxes.
    | The boundary geodataframe is not used.

    :param (int, int, int, int) test_input: bounding box (x_min, y_min, x_max, y_max)
    :param np.ndarray[np.int32] expected: coordinates (x_min, y_max) of each tile
    :returns: None
    :rtype: None
    """
    coordinator = Coordinator(bounding_box=test_input,
                              epsg_code=25832,
                              gdf_boundary=None)

    coordinates = coordinator.get_coordinates()

    assert coordinates.dtype == expected.dtype
    np.testing.assert_array_equal(coordinates, expected)


@pytest.mark.parametrize('test_input, expected', parameters_get_coordinates)
def test_get_coordinates(test_input,
                         expected,
                         gdf_boundary):
    """
    | Tests get_coordinates() with different bounding boxes.
    | The boundary geodataframe is used.

    :param (int, int, int, int) test_input: bounding box (x_min, y_min, x_max, y_max)
    :param np.ndarray[np.int32] expected: coordinates (x_min, y_max) of each tile
    :param gpd.GeoDataFrame gdf_boundary: boundary geodataframe
    :returns: None
    :rtype: None
    """
    coordinator = Coordinator(bounding_box=test_input,
                              epsg_code=25832,
                              gdf_boundary=gdf_boundary)

    coordinates = coordinator.get_coordinates()

    assert coordinates.dtype == expected.dtype
    np.testing.assert_array_equal(coordinates, expected)


@pytest.mark.parametrize('test_input, expected', parameters_filter_cached_coordinates_no_cached_tiles_dir)
def test_filter_cached_coordinates_no_cached_tiles_dir(test_input,
                                                       expected,
                                                       output_dir_path_no_cached_tiles_dir):
    """
    | Tests filter_cached_coordinates() with different coordinates.
    | The cached_tiles directory does not exist.

    :param np.ndarray[np.int32] test_input: coordinates (x_min, y_max) of each tile
    :param np.ndarray[np.int32] expected: filtered coordinates (x_min, y_max) of each tile
    :param Path output_dir_path_no_cached_tiles_dir: path to the output directory
    :returns: None
    :rtype: None
    """
    coordinates_filtered = Coordinator.filter_cached_coordinates(coordinates=test_input,
                                                                 output_dir_path=output_dir_path_no_cached_tiles_dir)

    assert coordinates_filtered.dtype == expected.dtype
    np.testing.assert_array_equal(coordinates_filtered, expected)


@pytest.mark.parametrize('test_input, expected', parameters_filter_cached_coordinates_empty_cached_tiles_dir)
def test_filter_cached_coordinates_empty_cached_tiles_dir(test_input,
                                                          expected,
                                                          output_dir_path_empty_cached_tiles_dir):
    """
    | Tests filter_cached_coordinates() with different coordinates.
    | The cached_tiles directory is empty.

    :param np.ndarray[np.int32] test_input: coordinates (x_min, y_max) of each tile
    :param np.ndarray[np.int32] expected: filtered coordinates (x_min, y_max) of each tile
    :param Path output_dir_path_empty_cached_tiles_dir: path to the output directory
    :returns: None
    :rtype: None
    """
    coordinates_filtered = Coordinator.filter_cached_coordinates(coordinates=test_input,
                                                                 output_dir_path=output_dir_path_empty_cached_tiles_dir)

    assert coordinates_filtered.dtype == expected.dtype
    np.testing.assert_array_equal(coordinates_filtered, expected)


@pytest.mark.parametrize('test_input, expected', parameters_filter_cached_coordinates_not_empty_cached_tiles_dir)
def test_filter_cached_coordinates_not_empty_cached_tiles_dir(test_input,
                                                              expected,
                                                              output_dir_path_not_empty_cached_tiles_dir):
    """
    | Tests filter_cached_coordinates() with different coordinates.
    | The cached_tiles directory is not empty.

    :param np.ndarray[np.int32] test_input: coordinates (x_min, y_max) of each tile
    :param np.ndarray[np.int32] expected: filtered coordinates (x_min, y_max) of each tile
    :param Path output_dir_path_not_empty_cached_tiles_dir: path to the output directory
    :returns: None
    :rtype: None
    """
    coordinates_filtered = \
        Coordinator.filter_cached_coordinates(coordinates=test_input,
                                              output_dir_path=output_dir_path_not_empty_cached_tiles_dir)

    assert coordinates_filtered.dtype == expected.dtype
    np.testing.assert_array_equal(coordinates_filtered, expected)
