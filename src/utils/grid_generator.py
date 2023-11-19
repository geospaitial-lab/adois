import geopandas as gpd
import numpy as np
from shapely.geometry import box, Polygon


class GridGenerator:
    def __init__(self,
                 bounding_box,
                 epsg_code):
        """
        | Initializer method

        :param (int, int, int, int) bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :param int epsg_code: epsg code of the coordinate reference system
        :returns: None
        :rtype: None
        """
        assert isinstance(bounding_box, tuple)
        assert len(bounding_box) == 4
        assert all(isinstance(coordinate, int) for coordinate in bounding_box)
        assert bounding_box[0] < bounding_box[2] and bounding_box[1] < bounding_box[3]

        assert isinstance(epsg_code, int)

        self.x_min, self.y_min, self.x_max, self.y_max = bounding_box
        self.epsg_code = epsg_code

    def compute_coordinates(self,
                            tile_size,
                            quantize=True):
        """
        | Returns the coordinates of the bottom left corner of each tile.

        :param int tile_size: tile size in meters
        :param bool quantize: if True, the bounding box is quantized to tile_size
        :returns: coordinates (x_min, y_min) of each tile
        :rtype: np.ndarray[np.int32]
        """
        assert isinstance(tile_size, int)
        assert tile_size > 0
        assert tile_size > (self.x_max - self.x_min) and tile_size > (self.y_max - self.y_min)

        assert isinstance(quantize, bool)

        if quantize:
            x_min = self.x_min - (self.x_min % tile_size)
            y_min = self.y_min - (self.y_min % tile_size)
        else:
            x_min = self.x_min
            y_min = self.y_min

        coordinates_x, coordinates_y = np.meshgrid(np.arange(x_min, self.x_max, tile_size),
                                                   np.arange(y_min, self.y_max, tile_size))

        coordinates = np.concatenate((coordinates_x.reshape(-1)[..., np.newaxis],
                                      coordinates_y.reshape(-1)[..., np.newaxis]),
                                     axis=-1).astype(np.int32)

        return coordinates

    @staticmethod
    def generate_polygons(coordinates, tile_size):
        """
        | Returns a polygon of each tile.

        :param np.ndarray[np.int32] coordinates: coordinates (x_min, y_min) of each tile
        :param int tile_size: tile size in meters
        :returns: polygon of each tile
        :rtype: list[Polygon]
        """
        polygons = [box(x_min, y_min, x_min + tile_size, y_min + tile_size)
                    for x_min, y_min in coordinates]

        return polygons

    def generate_grid(self,
                      tile_size,
                      quantize=True):
        """
        | Returns a geodataframe of the grid.

        :param int tile_size: tile size in meters
        :param bool quantize: if True, the bounding box is quantized to tile_size
        :returns: grid
        :rtype: gpd.GeoDataFrame
        """
        assert isinstance(tile_size, int)
        assert tile_size > 0
        assert tile_size > (self.x_max - self.x_min) and tile_size > (self.y_max - self.y_min)

        assert isinstance(quantize, bool)

        coordinates = self.compute_coordinates(tile_size=tile_size,
                                               quantize=quantize)

        polygons = self.generate_polygons(coordinates=coordinates,
                                          tile_size=tile_size)

        grid = gpd.GeoDataFrame(geometry=polygons,
                                crs=f'EPSG:{self.epsg_code}')

        return grid
