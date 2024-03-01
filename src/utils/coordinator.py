import re
from pathlib import Path

import geopandas as gpd
import numpy as np
from numpy import typing as npt

from src.utils.grid_generator import GridGenerator


class Coordinator:

    def __init__(self,
                 grid_generator: GridGenerator,
                 bounding_box: tuple[int, int, int, int],
                 tile_size: int,
                 epsg_code: int) -> None:
        """
        | Initializer method

        :param grid_generator: grid generator
        :param bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :param tile_size: tile size in meters
        :param epsg_code: epsg code
        :returns: None
        """
        assert isinstance(grid_generator, GridGenerator)

        assert isinstance(bounding_box, tuple)
        assert len(bounding_box) == 4
        assert all(isinstance(coordinate, int) for coordinate in bounding_box)
        assert bounding_box[0] < bounding_box[2] and bounding_box[1] < bounding_box[3]

        assert isinstance(tile_size, int)
        assert tile_size > 0
        assert tile_size < (bounding_box[2] - bounding_box[0]) and tile_size < (bounding_box[3] - bounding_box[1])

        assert isinstance(epsg_code, int)

        assert grid_generator.x_min == bounding_box[0]
        assert grid_generator.y_min == bounding_box[1]
        assert grid_generator.x_max == bounding_box[2]
        assert grid_generator.y_max == bounding_box[3]
        assert grid_generator.epsg_code == epsg_code

        self.grid_generator = grid_generator
        self.tile_size = tile_size
        self.epsg_code = epsg_code

    def compute_coordinates(self) -> npt.NDArray[np.int32]:
        """
        | Returns the coordinates of the top left corner of each tile.

        :returns: coordinates (x_min, y_max) of each tile
        """
        coordinates = self.grid_generator.compute_coordinates(tile_size=self.tile_size,
                                                              quantize=True)

        coordinates[:, 1] += self.tile_size
        return coordinates

    def filter_coordinates_outside_boundary(self,
                                            coordinates: npt.NDArray[np.int32],
                                            boundary: gpd.GeoDataFrame) -> npt.NDArray[np.int32]:
        """
        | Returns the filtered coordinates of the top left corner of each tile.
        | The coordinates are filtered based on whether they are inside the boundary or not.
            Only the coordinates of tiles that intersect the polygons of boundary are retained.

        :param coordinates: coordinates (x_min, y_max) of each tile
        :param boundary: boundary
        :returns: filtered coordinates (x_min, y_max) of each tile
        """
        assert isinstance(coordinates, np.ndarray)
        assert coordinates.dtype == np.int32
        assert coordinates.ndim == 2
        assert coordinates.shape[-1] == 2

        assert isinstance(boundary, gpd.GeoDataFrame)
        assert not boundary.empty
        assert all(boundary['geometry'].geom_type == 'Polygon')
        assert all(boundary['geometry'].is_valid)
        assert boundary.crs == f'EPSG:{self.epsg_code}'

        grid = self.grid_generator.generate_grid(tile_size=self.tile_size,
                                                 quantize=True)

        mask = np.array(grid['geometry'].intersects(boundary['geometry']).any(axis=1), dtype=bool)
        return coordinates[mask]

    @staticmethod
    def extract_coordinates_processed(path_tiles_processed_dir: Path) -> npt.NDArray[np.int32] | None:
        """
        | Returns the coordinates of the top left corner of each processed tile.
        | The coordinates are extracted from the names of the subdirectories in the processed tiles directory.

        :param path_tiles_processed_dir: path to the processed tiles directory
        :returns: coordinates (x_min, y_max) of each processed tile
        """
        assert isinstance(path_tiles_processed_dir, Path)

        if not path_tiles_processed_dir.is_dir():
            return None

        coordinates_processed = []

        pattern = re.compile(r'^(-?\d+)_(-?\d+)$')

        for path_tile_processed_dir in path_tiles_processed_dir.iterdir():
            if not path_tile_processed_dir.is_dir():
                continue

            match = pattern.search(path_tile_processed_dir.name)

            if match:
                x_min = int(match.group(1))
                y_max = int(match.group(2))
                coordinates_processed.append([x_min, y_max])

        if len(coordinates_processed) == 0:
            return None

        return np.array(coordinates_processed, dtype=np.int32)

    @staticmethod
    def filter_coordinates_processed(coordinates: npt.NDArray[np.int32],
                                     coordinates_processed: npt.NDArray[np.int32]) -> npt.NDArray[np.int32]:
        """
        | Returns the filtered coordinates of the top left corner of each tile.
        | The coordinates are filtered based on whether they are processed or not.
            Only the coordinates of tiles that are not processed are retained.

        :param coordinates: coordinates (x_min, y_max) of each tile
        :param coordinates_processed: coordinates (x_min, y_max) of each processed tile
        :returns: filtered coordinates (x_min, y_max) of each tile
        """
        assert isinstance(coordinates, np.ndarray)
        assert coordinates.dtype == np.int32
        assert coordinates.ndim == 2
        assert coordinates.shape[-1] == 2

        assert isinstance(coordinates_processed, np.ndarray)
        assert coordinates_processed.dtype == np.int32
        assert coordinates_processed.ndim == 2
        assert coordinates_processed.shape[-1] == 2

        mask = np.all(coordinates[:, np.newaxis, :] == coordinates_processed[np.newaxis, ...], axis=-1)
        return coordinates[~np.any(mask, axis=-1)]

    def filter_coordinates(self,
                           coordinates: npt.NDArray[np.int32],
                           boundary: gpd.GeoDataFrame | None = None,
                           path_tiles_processed_dir: Path | None = None) -> npt.NDArray[np.int32]:
        """
        | Returns the filtered coordinates of the top left corner of each tile.

        :param coordinates: coordinates (x_min, y_max) of each tile
        :param boundary: boundary
        :param path_tiles_processed_dir: path to the processed tiles directory
        :returns: filtered coordinates (x_min, y_max) of each tile
        """
        assert isinstance(coordinates, np.ndarray)
        assert coordinates.dtype == np.int32
        assert coordinates.ndim == 2
        assert coordinates.shape[-1] == 2

        assert isinstance(boundary, gpd.GeoDataFrame) or boundary is None

        if boundary is not None:
            assert not boundary.empty
            assert all(boundary['geometry'].geom_type == 'Polygon')
            assert all(boundary['geometry'].is_valid)
            assert boundary.crs == f'EPSG:{self.epsg_code}'

        assert isinstance(path_tiles_processed_dir, Path) or path_tiles_processed_dir is None

        if boundary is not None:
            coordinates = self.filter_coordinates_outside_boundary(coordinates=coordinates,
                                                                   boundary=boundary)

        if path_tiles_processed_dir is not None:
            coordinates_processed = (
                self.extract_coordinates_processed(path_tiles_processed_dir=path_tiles_processed_dir))

            if coordinates_processed is not None:
                coordinates = self.filter_coordinates_processed(coordinates=coordinates,
                                                                coordinates_processed=coordinates_processed)

        return coordinates

    def __repr__(self) -> str:
        """
        | Returns a representation of the object.

        :returns: representation
        """
        representation = (
            f'{self.__class__.__name__}('
            f'grid_generator={self.grid_generator!r}, '
            f'tile_size={self.tile_size}, '
            f'epsg_code={self.epsg_code})')

        return representation
