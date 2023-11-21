import re
from pathlib import Path

import geopandas as gpd
import numpy as np

import src.utils.settings as settings
from src.utils.grid_generator import GridGenerator


class Coordinator:
    def __init__(self,
                 bounding_box,
                 epsg_code,
                 boundary):
        """
        | Constructor method

        :param (int, int, int, int) bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :param int epsg_code: epsg code of the coordinate reference system
        :param gpd.GeoDataFrame or None boundary: boundary
        :returns: None
        :rtype: None
        """
        assert isinstance(bounding_box, tuple)
        assert len(bounding_box) == 4
        assert all(isinstance(coordinate, int) for coordinate in bounding_box)
        assert bounding_box[0] < bounding_box[2] and bounding_box[1] < bounding_box[3]

        assert isinstance(epsg_code, int)

        assert isinstance(boundary, gpd.GeoDataFrame) or boundary is None

        if isinstance(boundary, gpd.GeoDataFrame):
            assert not boundary.empty
            assert boundary.shape[0] == 1
            assert all(boundary['geometry'].geom_type == 'Polygon')
            assert boundary.crs == f'EPSG:{epsg_code}'

        self.bounding_box = bounding_box
        self.epsg_code = epsg_code
        self.boundary = boundary

    def get_coordinates(self):
        """
        | Returns the coordinates of the top left corner of each tile.

        :returns: coordinates (x_min, y_max) of each tile
        :rtype: np.ndarray[np.int32]
        """
        grid_generator = GridGenerator(bounding_box=self.bounding_box,
                                       epsg_code=self.epsg_code)

        coordinates = grid_generator.get_coordinates(tile_size=settings.IMAGE_SIZE_METERS,
                                                     quantize=True)

        coordinates[:, 1] += settings.IMAGE_SIZE_METERS

        if self.boundary is None:
            return coordinates

        grid = grid_generator.get_grid(tile_size=settings.IMAGE_SIZE_METERS,
                                       quantize=True)

        mask = np.array(grid['geometry'].intersects(self.boundary['geometry'][0]), dtype=bool)

        return coordinates[mask]

    @staticmethod
    def filter_cached_coordinates(coordinates, output_dir_path):
        """
        | Returns the filtered coordinates of the top left corner of each tile.
        | If a tile has already been processed (its directory exists in the cached_tiles directory),
            its coordinates are removed.

        :param np.ndarray[np.int32] coordinates: coordinates (x_min, y_max) of each tile
        :param str or Path output_dir_path: path to the output directory
        :returns: filtered coordinates (x_min, y_max) of each tile
        :rtype: np.ndarray[np.int32]
        """
        assert isinstance(coordinates, np.ndarray) and coordinates.dtype == np.int32
        assert len(coordinates.shape) == 2
        assert coordinates.shape[-1] == 2

        assert isinstance(output_dir_path, str) or isinstance(output_dir_path, Path)

        path_cached_tiles_dir = Path(output_dir_path) / 'cached_tiles'

        if not path_cached_tiles_dir.is_dir():
            return coordinates

        mask = np.ones(coordinates.shape[0], dtype=bool)

        pattern = re.compile(r'^(-?\d+)_(-?\d+)$')

        for path_cached_tile_dir in path_cached_tiles_dir.iterdir():
            match = pattern.search(path_cached_tile_dir.name)

            if match:
                x_min = int(match.group(1))
                y_max = int(match.group(2))

                coordinates_cached = np.array([x_min, y_max], dtype=np.int32)
                mask &= np.any(coordinates != coordinates_cached, axis=1)

        return coordinates[mask]
