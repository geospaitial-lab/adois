import inspect

import geopandas as gpd
import geopandas.testing
import numpy as np
import pytest
from shapely.geometry import Polygon

from src.utils.grid_generator import GridGenerator
from src.utils.tests.data.data_test_grid_generator import (
    parameters_init,
    parameters_compute_coordinates,
    parameters_generate_polygons,
    parameters_generate_grid)


@pytest.mark.parametrize('test_input, expected', parameters_init)
def test_init(test_input, expected):
    """
    | Tests __init__().

    :param ((int, int, int, int), int) test_input: bounding box (x_min, y_min, x_max, y_max), epsg code
        of the coordinate reference system
    :param ((int, int, int, int), int) expected: bounding box (x_min, y_min, x_max, y_max), epsg code
        of the coordinate reference system
    :returns: None
    :rtype: None
    """
    grid_generator = GridGenerator(bounding_box=test_input[0],
                                   epsg_code=test_input[1])

    assert isinstance(grid_generator, GridGenerator)
    assert list(grid_generator.__dict__.keys()) == ['x_min', 'y_min', 'x_max', 'y_max', 'epsg_code']
    assert isinstance(grid_generator.x_min, int)
    assert grid_generator.x_min == expected[0][0]
    assert isinstance(grid_generator.y_min, int)
    assert grid_generator.y_min == expected[0][1]
    assert isinstance(grid_generator.x_max, int)
    assert grid_generator.x_max == expected[0][2]
    assert isinstance(grid_generator.y_max, int)
    assert grid_generator.y_max == expected[0][3]
    assert isinstance(grid_generator.epsg_code, int)
    assert grid_generator.epsg_code == expected[1]


def test_compute_coordinates_default(grid_generator):
    """
    | Tests the default values of the parameters of compute_coordinates().

    :param GridGenerator grid_generator: grid generator
    :returns: None
    :rtype: None
    """
    signature = inspect.signature(grid_generator.compute_coordinates)
    quantize_default = signature.parameters['quantize'].default

    assert isinstance(quantize_default, bool)
    assert quantize_default is True


@pytest.mark.parametrize('test_input, expected', parameters_compute_coordinates)
def test_compute_coordinates(test_input,
                             expected,
                             grid_generator):
    """
    | Tests compute_coordinates().

    :param (int, bool) test_input: tile size in meters, quantize
    :param np.ndarray[np.int32] expected: coordinates (x_min, y_min) of each tile
    :param GridGenerator grid_generator: grid generator
    :returns: None
    :rtype: None
    """
    coordinates = grid_generator.compute_coordinates(tile_size=test_input[0],
                                                     quantize=test_input[1])

    assert isinstance(coordinates, np.ndarray)
    assert coordinates.dtype == np.int32
    assert len(coordinates.shape) == 2
    assert coordinates.shape[-1] == 2
    np.testing.assert_array_equal(coordinates, expected)


@pytest.mark.parametrize('test_input, expected', parameters_generate_polygons)
def test_generate_polygons(test_input,
                           expected,
                           grid_generator):
    """
    | Tests generate_polygons().

    :param (np.ndarray[np.int32], int) test_input: coordinates (x_min, y_min) of each tile, tile size in meters
    :param list[Polygon] expected: polygon of each tile
    :param GridGenerator grid_generator: grid generator
    :returns: None
    :rtype: None
    """
    polygons = GridGenerator.generate_polygons(coordinates=test_input[0],
                                               tile_size=test_input[1])

    assert isinstance(polygons, list)
    assert all(isinstance(polygon, Polygon) for polygon in polygons)
    assert all(polygon.equals(expected[i]) for i, polygon in enumerate(polygons))


def test_generate_grid_default(grid_generator):
    """
    | Tests the default values of the parameters of generate_grid().

    :param GridGenerator grid_generator: grid generator
    :returns: None
    :rtype: None
    """
    signature = inspect.signature(grid_generator.generate_grid)
    quantize_default = signature.parameters['quantize'].default

    assert isinstance(quantize_default, bool)
    assert quantize_default is True


@pytest.mark.parametrize('test_input, expected', parameters_generate_grid)
def test_generate_grid(test_input,
                       expected,
                       grid_generator):
    """
    | Tests generate_grid().

    :param (int, bool) test_input: tile size in meters, quantize
    :param gpd.GeoDataFrame expected: grid
    :param GridGenerator grid_generator: grid generator
    :returns: None
    :rtype: None
    """
    grid = grid_generator.generate_grid(tile_size=test_input[0],
                                        quantize=test_input[1])

    assert isinstance(grid, gpd.GeoDataFrame)
    gpd.testing.assert_geodataframe_equal(grid,
                                          expected,
                                          check_geom_type=True)
