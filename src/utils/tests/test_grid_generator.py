import inspect
import unittest.mock as mock

import geopandas as gpd
import geopandas.testing
import numpy as np
import pytest
from shapely.geometry import box, Polygon

from src.utils.grid_generator import GridGenerator
from .data.data_test_grid_generator import parameters_compute_coordinates


def test_init():
    """
    | Tests __init__().

    :returns: None
    :rtype: None
    """
    bounding_box = (-128, -128, 128, 128)
    epsg_code = 25832

    grid_generator = GridGenerator(bounding_box=bounding_box,
                                   epsg_code=epsg_code)

    assert isinstance(grid_generator, GridGenerator)
    parameters = ['x_min', 'y_min', 'x_max', 'y_max', 'epsg_code']
    assert list(vars(grid_generator).keys()) == parameters

    assert isinstance(grid_generator.x_min, int)
    assert grid_generator.x_min == bounding_box[0]
    assert isinstance(grid_generator.y_min, int)
    assert grid_generator.y_min == bounding_box[1]
    assert isinstance(grid_generator.x_max, int)
    assert grid_generator.x_max == bounding_box[2]
    assert isinstance(grid_generator.y_max, int)
    assert grid_generator.y_max == bounding_box[3]
    assert isinstance(grid_generator.epsg_code, int)
    assert grid_generator.epsg_code == epsg_code


def test_compute_coordinates_default(grid_generator):
    """
    | Tests the default values of the parameters of compute_coordinates().

    :param GridGenerator grid_generator: grid generator fixture
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

    :param (int, bool) test_input: tile_size, quantize
    :param np.ndarray[np.int32] expected: coordinates (x_min, y_min) of each tile
    :param GridGenerator grid_generator: grid generator fixture
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


def test_generate_polygons(grid_generator):
    """
    | Tests generate_polygons().

    :param GridGenerator grid_generator: grid generator fixture
    :returns: None
    :rtype: None
    """
    coordinates = np.array([[-128, -128], [0, -128], [-128, 0], [0, 0]], dtype=np.int32)
    tile_size = 128

    expected = (
        [box(-128, -128, 0, 0),
         box(0, -128, 128, 0),
         box(-128, 0, 0, 128),
         box(0, 0, 128, 128)])

    polygons = grid_generator.generate_polygons(coordinates=coordinates,
                                                tile_size=tile_size)

    assert isinstance(polygons, list)
    assert all(isinstance(polygon, Polygon) for polygon in polygons)
    assert all(polygon.equals(expected[i]) for i, polygon in enumerate(polygons))


def test_generate_grid_default(grid_generator):
    """
    | Tests the default values of the parameters of generate_grid().

    :param GridGenerator grid_generator: grid generator fixture
    :returns: None
    :rtype: None
    """
    signature = inspect.signature(grid_generator.generate_grid)
    quantize_default = signature.parameters['quantize'].default

    assert isinstance(quantize_default, bool)
    assert quantize_default is True


@mock.patch('src.utils.grid_generator.GridGenerator.compute_coordinates')
@mock.patch('src.utils.grid_generator.GridGenerator.generate_polygons')
def test_generate_grid(mocked_generate_polygons,
                       mocked_compute_coordinates,
                       grid_generator):
    """
    | Tests generate_grid().

    :param mock.MagicMock mocked_generate_polygons: mocked generate_polygons method
    :param mock.MagicMock mocked_compute_coordinates: mocked compute_coordinates method
    :param GridGenerator grid_generator: grid generator fixture
    :returns: None
    :rtype: None
    """
    tile_size = 128
    quantize = True

    polygons = (
        [box(-128, -128, 0, 0),
         box(0, -128, 128, 0),
         box(-128, 0, 0, 128),
         box(0, 0, 128, 128)])

    expected = gpd.GeoDataFrame(geometry=polygons,
                                crs='EPSG:25832')

    mocked_compute_coordinates.return_value = np.array([[-128, -128], [0, -128], [-128, 0], [0, 0]], dtype=np.int32)
    mocked_generate_polygons.return_value = polygons

    grid = grid_generator.generate_grid(tile_size=tile_size,
                                        quantize=quantize)

    mocked_compute_coordinates.assert_called_once_with(tile_size=tile_size,
                                                       quantize=quantize)

    mocked_generate_polygons.assert_called_once_with(coordinates=mocked_compute_coordinates.return_value,
                                                     tile_size=tile_size)

    assert isinstance(grid, gpd.GeoDataFrame)
    assert not grid.empty
    assert grid.shape[1] == 1
    assert all(grid['geometry'].geom_type == 'Polygon')
    assert all(grid['geometry'].is_valid)
    assert grid.crs == f'EPSG:{grid_generator.epsg_code}'
    gpd.testing.assert_geodataframe_equal(grid, expected, check_geom_type=True)


@pytest.mark.integration
def test_generate_grid_integration(grid_generator):
    """
    | Tests generate_grid().
    | Integration test.

    :param GridGenerator grid_generator: grid generator fixture
    :returns: None
    :rtype: None
    """
    tile_size = 128
    quantize = True

    polygons = (
        [box(-128, -128, 0, 0),
         box(0, -128, 128, 0),
         box(-128, 0, 0, 128),
         box(0, 0, 128, 128)])

    expected = gpd.GeoDataFrame(geometry=polygons,
                                crs='EPSG:25832')

    grid = grid_generator.generate_grid(tile_size=tile_size,
                                        quantize=quantize)

    assert isinstance(grid, gpd.GeoDataFrame)
    assert not grid.empty
    assert grid.shape[1] == 1
    assert all(grid['geometry'].geom_type == 'Polygon')
    assert all(grid['geometry'].is_valid)
    assert grid.crs == f'EPSG:{grid_generator.epsg_code}'
    gpd.testing.assert_geodataframe_equal(grid, expected, check_geom_type=True)
