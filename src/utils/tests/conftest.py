from pathlib import Path

import geopandas as gpd
import pytest
from shapely.geometry import Polygon

from src.utils.coordinator import Coordinator


@pytest.fixture(scope='session')
def shape_file_dir_path(tmp_path_factory):
    """
    | Returns the path to the temporary shape file directory.

    :param pytest.TempPathFactory tmp_path_factory: temporary path
    :returns: path to the shape file directory
    :rtype: Path
    """
    shape_file_dir_path = tmp_path_factory.mktemp('shape_file_dir')
    (shape_file_dir_path / 'shape_file.shp').touch()
    (shape_file_dir_path / 'shape_file_1.shp').touch()
    (shape_file_dir_path / 'shape_file_2.shp').touch()
    (shape_file_dir_path / 'shape_file_3.shp').touch()
    (shape_file_dir_path / 'shape_file_4.shp').touch()
    (shape_file_dir_path / 'invalid_shape_file.py').touch()
    return shape_file_dir_path


@pytest.fixture(scope='session')
def coordinator():
    """
    | Returns a coordinator instance.

    :returns: preprocessor
    :rtype: Preprocessor
    """
    coordinator = Coordinator()
    return coordinator


@pytest.fixture(scope='session')
def output_dir_path_empty_cached_tiles_dir(tmp_path_factory):
    """
    | Returns the path to the temporary output directory.
    | The cached_tiles directory is empty.

    :param pytest.TempPathFactory tmp_path_factory: temporary path
    :returns: path to the output directory
    :rtype: Path
    """
    output_dir_path = tmp_path_factory.mktemp('output_dir')
    (output_dir_path / 'cached_tiles').mkdir()
    return output_dir_path


@pytest.fixture(scope='session')
def output_dir_path_not_empty_cached_tiles_dir(tmp_path_factory):
    """
    | Returns the path to the temporary output directory.
    | The cached_tiles directory is not empty.

    :param pytest.TempPathFactory tmp_path_factory: temporary path
    :returns: path to the output directory
    :rtype: Path
    """
    output_dir_path = tmp_path_factory.mktemp('output_dir')
    (output_dir_path / 'cached_tiles').mkdir()
    (output_dir_path / 'cached_tiles' / '512_1024').mkdir()
    (output_dir_path / 'cached_tiles' / '768_1024').mkdir()
    (output_dir_path / 'cached_tiles' / '512_-512').mkdir()
    (output_dir_path / 'cached_tiles' / '768_-512').mkdir()
    (output_dir_path / 'cached_tiles' / '-1024_-512').mkdir()
    (output_dir_path / 'cached_tiles' / '-768_-512').mkdir()
    (output_dir_path / 'cached_tiles' / '-1024_1024').mkdir()
    (output_dir_path / 'cached_tiles' / '-768_1024').mkdir()
    (output_dir_path / 'cached_tiles' / '-256_256').mkdir()
    (output_dir_path / 'cached_tiles' / '0_256').mkdir()
    return output_dir_path


@pytest.fixture(scope='session')
def boundary_gdf():
    """
    | Returns a boundary geodataframe.

    :returns: boundary geodataframe
    :rtype: gpd.GeoDataFrame
    """
    polygon = Polygon([[-512, -512],
                       [512, -512],
                       [512, 512],
                       [-512, 512]])
    boundary_gdf = gpd.GeoDataFrame(geometry=[polygon], crs='EPSG:25832')
    return boundary_gdf


@pytest.fixture(scope='session')
def invalid_boundary_gdf():
    """
    | Returns an invalid boundary geodataframe (more than 1 polygon).

    :returns: invalid boundary geodataframe
    :rtype: gpd.GeoDataFrame
    """
    polygon_1 = Polygon([[-512, -512],
                         [0, -512],
                         [0, 0],
                         [-512, 0]])
    polygon_2 = Polygon([[0, -512],
                         [512, -512],
                         [512, 0],
                         [0, 0]])
    polygon_3 = Polygon([[0, 0],
                         [512, 0],
                         [512, 512],
                         [0, 512]])
    polygon_4 = Polygon([[-512, 0],
                         [0, 0],
                         [0, 512],
                         [-512, 512]])
    polygons = [polygon_1, polygon_2, polygon_3, polygon_4]
    invalid_boundary_gdf = gpd.GeoDataFrame(geometry=polygons, crs='EPSG:25832')
    return invalid_boundary_gdf
