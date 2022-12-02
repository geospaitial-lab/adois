import re
from pathlib import Path

import geopandas as gpd

import src.utils.settings as settings
from src.utils.grid_generator import GridGenerator


class Coordinator:
    @staticmethod
    def get_coordinates(bounding_box):
        """
        | Returns the coordinates of the top left corner of each tile in the area of the bounding box.
            The bounding box is quantized to the image size in meters.

        :param (int, int, int, int) bounding_box: bounding box (x_1, y_1, x_2, y_2)
        :returns: coordinates (x, y) of each tile
        :rtype: list[(int, int)]
        """
        coordinates = []

        bounding_box = (bounding_box[0] - (bounding_box[0] % settings.IMAGE_SIZE_METERS),
                        bounding_box[1] - (bounding_box[1] % settings.IMAGE_SIZE_METERS),
                        bounding_box[2],
                        bounding_box[3])

        columns = (bounding_box[2] - bounding_box[0]) // settings.IMAGE_SIZE_METERS
        if (bounding_box[2] - bounding_box[0]) % settings.IMAGE_SIZE_METERS:
            columns += 1

        rows = (bounding_box[3] - bounding_box[1]) // settings.IMAGE_SIZE_METERS
        if (bounding_box[3] - bounding_box[1]) % settings.IMAGE_SIZE_METERS:
            rows += 1

        for row in range(rows):
            for column in range(columns):
                coordinates.append((bounding_box[0] + column * settings.IMAGE_SIZE_METERS,
                                    bounding_box[1] + (row + 1) * settings.IMAGE_SIZE_METERS))

        return coordinates

    def get_valid_coordinates(self,
                              bounding_box,
                              epsg_code,
                              boundary_gdf):
        """
        | Returns the coordinates of the top left corner of each tile in the area of the boundary geodataframe.

        :param (int, int, int, int) bounding_box: bounding box (x_1, y_1, x_2, y_2)
        :param int epsg_code: epsg code of the coordinate reference system
        :param gpd.GeoDataFrame boundary_gdf: boundary geodataframe
        :returns: valid coordinates (x, y) of each tile
        :rtype: list[(int, int)]
        """
        coordinates = self.get_coordinates(bounding_box)

        grid_generator = GridGenerator(bounding_box=bounding_box,
                                       epsg_code=epsg_code)
        grid_gdf = grid_generator.get_grid(tile_size_meters=settings.IMAGE_SIZE_METERS)

        intersections = list(grid_gdf['geometry'].intersects(boundary_gdf['geometry'][0]))
        valid_coordinates = [coordinates_element for (coordinates_element, valid) in zip(coordinates, intersections)
                             if valid]

        return valid_coordinates

    @staticmethod
    def filter_cached_coordinates(coordinates, output_dir_path):
        """
        | Returns the filtered coordinates. If a tile has already been downloaded (its shape file directory in
            .tiles directory exists), its coordinates are removed.

        :param list[(int, int)] coordinates: coordinates (x, y) of each tile
        :param str or Path output_dir_path: path to the output directory
        :returns: filtered coordinates (x, y) of each tile
        :rtype: list[(int, int)]
        """
        filtered_coordinates = coordinates[:]

        tiles_dir_path = Path(output_dir_path) / '.tiles'
        pattern = re.compile(r'^(-?\d+)_(-?\d+)$')

        for path in tiles_dir_path.iterdir():
            match = pattern.search(path.name)
            if match:
                cached_coordinates = (int(match.group(1)), int(match.group(2)))
                if cached_coordinates in coordinates:
                    filtered_coordinates.remove(cached_coordinates)

        return filtered_coordinates
