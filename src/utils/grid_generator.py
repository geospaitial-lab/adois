# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import geopandas as gpd
from shapely.geometry import Polygon

import src.utils as utils


class GridGenerator:
    def __init__(self,
                 bounding_box,
                 epsg_code):
        """
        | Constructor method

        :param (int, int, int, int) bounding_box: bounding box (x_1, y_1, x_2, y_2)
        :param int epsg_code: epsg code of the coordinate reference system
        :returns: None
        :rtype: None
        """
        self.bounding_box = bounding_box
        self.epsg_code = epsg_code

    def get_coordinates(self, tile_size_meters):
        """
        | Returns the coordinates of the top left corner of each tile in the area of the bounding box.
            The bounding box is quantized to the image size in meters.

        :param int tile_size_meters: tile size in meters
        :returns: coordinates (x, y) of each tile
        :rtype: list[(int, int)]
        """
        coordinates = []

        bounding_box = (self.bounding_box[0] - (self.bounding_box[0] % utils.IMAGE_SIZE_METERS),
                        self.bounding_box[1] - (self.bounding_box[1] % utils.IMAGE_SIZE_METERS),
                        self.bounding_box[2],
                        self.bounding_box[3])

        columns = (bounding_box[2] - bounding_box[0]) // tile_size_meters
        if (bounding_box[2] - bounding_box[0]) % tile_size_meters:
            columns += 1

        rows = (bounding_box[3] - bounding_box[1]) // tile_size_meters
        if (bounding_box[3] - bounding_box[1]) % tile_size_meters:
            rows += 1

        for row in range(rows):
            for column in range(columns):
                coordinates.append((bounding_box[0] + column * tile_size_meters,
                                    bounding_box[1] + (row + 1) * tile_size_meters))

        return coordinates

    @staticmethod
    def get_bounding_box(coordinates, tile_size_meters):
        """
        | Returns the bounding box of a tile given its coordinates of the top left corner.

        :param (int, int) coordinates: coordinates (x, y)
        :param int tile_size_meters: tile size in meters
        :returns: bounding box (x_1, y_1, x_2, y_2)
        :rtype: (int, int, int, int)
        """
        bounding_box = (coordinates[0],
                        coordinates[1] - tile_size_meters,
                        coordinates[0] + tile_size_meters,
                        coordinates[1])
        return bounding_box

    @staticmethod
    def get_polygon(coordinates, tile_size_meters):
        """
        | Returns the polygon of a tile given its coordinates of the top left corner.

        :param (int, int) coordinates: coordinates (x, y)
        :param int tile_size_meters: tile size in meters
        :returns: polygon
        :rtype: Polygon
        """
        bounding_box = GridGenerator.get_bounding_box(coordinates=coordinates,
                                                      tile_size_meters=tile_size_meters)
        polygon = Polygon([[bounding_box[0], bounding_box[1]],
                           [bounding_box[2], bounding_box[1]],
                           [bounding_box[2], bounding_box[3]],
                           [bounding_box[0], bounding_box[3]]])
        return polygon

    def get_grid(self, tile_size_meters):
        """
        | Returns a geodataframe of the grid.

        :param int tile_size_meters: tile size in meters
        :returns: geodataframe
        :rtype: gpd.GeoDataFrame
        """
        coordinates = self.get_coordinates(tile_size_meters=tile_size_meters)

        polygons = []

        for coordinates_element in coordinates:
            polygon = self.get_polygon(coordinates=coordinates_element,
                                       tile_size_meters=tile_size_meters)
            polygons.append(polygon)

        gdf = gpd.GeoDataFrame(geometry=polygons, crs=f'EPSG:{self.epsg_code}')
        return gdf
