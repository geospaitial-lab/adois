import geopandas as gpd
import numpy as np
from numpy import typing as npt
from shapely.geometry import box, Polygon


class GridGenerator:

    def __init__(self,
                 bounding_box: tuple[int, int, int, int],
                 epsg_code: int) -> None:
        """
        | Initializer method

        :param bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :param epsg_code: epsg code
        :returns: None
        """
        assert isinstance(bounding_box, tuple)
        assert len(bounding_box) == 4
        assert all(isinstance(coordinate, int) for coordinate in bounding_box)
        assert bounding_box[0] < bounding_box[2] and bounding_box[1] < bounding_box[3]

        assert isinstance(epsg_code, int)

        self.x_min, self.y_min, self.x_max, self.y_max = bounding_box
        self.epsg_code = epsg_code

    def compute_coordinates(self,
                            tile_size: int,
                            quantize: bool = True) -> npt.NDArray[np.int32]:
        """
        | Returns the coordinates of the bottom left corner of each tile.

        :param tile_size: tile size in meters
        :param quantize: if True, the bounding box is quantized to tile_size
        :returns: coordinates (x_min, y_min) of each tile
        """
        assert isinstance(tile_size, int)
        assert tile_size > 0
        assert tile_size < (self.x_max - self.x_min) and tile_size < (self.y_max - self.y_min)

        assert isinstance(quantize, bool)

        if quantize:
            x_min = self.x_min - (self.x_min % tile_size)
            y_min = self.y_min - (self.y_min % tile_size)
        else:
            x_min = self.x_min
            y_min = self.y_min

        coordinates_range_x = np.arange(x_min, self.x_max, tile_size)
        coordinates_range_y = np.arange(y_min, self.y_max, tile_size)
        coordinates_x, coordinates_y = np.meshgrid(coordinates_range_x, coordinates_range_y)

        coordinates_x = coordinates_x.reshape(-1)[..., np.newaxis]
        coordinates_y = coordinates_y.reshape(-1)[..., np.newaxis]
        coordinates = np.concatenate((coordinates_x, coordinates_y), axis=-1).astype(np.int32)
        return coordinates

    def generate_polygons(self,
                          coordinates: npt.NDArray[np.int32],
                          tile_size: int) -> list[Polygon]:
        """
        | Returns a polygon of each tile.

        :param coordinates: coordinates (x_min, y_min) of each tile
        :param tile_size: tile size in meters
        :returns: polygon of each tile
        """
        assert isinstance(coordinates, np.ndarray)
        assert coordinates.dtype == np.int32
        assert coordinates.ndim == 2
        assert coordinates.shape[-1] == 2

        assert isinstance(tile_size, int)
        assert tile_size > 0
        assert tile_size < (self.x_max - self.x_min) and tile_size < (self.y_max - self.y_min)

        polygons = [box(x_min, y_min, x_min + tile_size, y_min + tile_size)
                    for x_min, y_min in coordinates]

        return polygons

    def generate_grid(self,
                      tile_size: int,
                      quantize: bool = True) -> gpd.GeoDataFrame:
        """
        | Returns a geodataframe of the grid.

        :param tile_size: tile size in meters
        :param quantize: if True, the bounding box is quantized to tile_size
        :returns: grid
        """
        assert isinstance(tile_size, int)
        assert tile_size > 0
        assert tile_size < (self.x_max - self.x_min) and tile_size < (self.y_max - self.y_min)

        assert isinstance(quantize, bool)

        coordinates = self.compute_coordinates(tile_size=tile_size,
                                               quantize=quantize)

        polygons = self.generate_polygons(coordinates=coordinates,
                                          tile_size=tile_size)

        grid = gpd.GeoDataFrame(geometry=polygons,
                                crs=f'EPSG:{self.epsg_code}')

        return grid

    def __repr__(self) -> str:
        """
        | Returns a representation of the object.

        :returns: representation
        """
        representation = (
            f'{self.__class__.__name__}('
            f'x_min={self.x_min}, y_min={self.y_min}, x_max={self.x_max}, y_max={self.y_max}, '
            f'epsg_code={self.epsg_code})')

        return representation
