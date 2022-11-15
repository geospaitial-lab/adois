# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import re
from pathlib import Path

import geopandas as gpd

import src.utils as utils
from src.aggregation.grid_generator import GridGenerator


def get_coordinates(bounding_box):
    """
    | Returns the coordinates of the top left corner of each tile in the area of the bounding box.
        The bounding box is quantized to the image size in meters.

    :param (int, int, int, int) bounding_box: bounding box (x_1, y_1, x_2, y_2)
    :returns: coordinates (x, y) of each tile
    :rtype: list[(int, int)]
    """
    coordinates = []

    bounding_box = (bounding_box[0] - (bounding_box[0] % utils.IMAGE_SIZE_METERS),
                    bounding_box[1] - (bounding_box[1] % utils.IMAGE_SIZE_METERS),
                    bounding_box[2],
                    bounding_box[3])

    columns = (bounding_box[2] - bounding_box[0]) // utils.IMAGE_SIZE_METERS
    if (bounding_box[2] - bounding_box[0]) % utils.IMAGE_SIZE_METERS:
        columns += 1

    rows = (bounding_box[3] - bounding_box[1]) // utils.IMAGE_SIZE_METERS
    if (bounding_box[3] - bounding_box[1]) % utils.IMAGE_SIZE_METERS:
        rows += 1

    for row in range(rows):
        for column in range(columns):
            coordinates.append((bounding_box[0] + column * utils.IMAGE_SIZE_METERS,
                                bounding_box[1] + (row + 1) * utils.IMAGE_SIZE_METERS))

    return coordinates


def get_internal_coordinates(bounding_box,
                             epsg_code,
                             boundary_gdf):
    """
    | Returns the coordinates of the top left corner of each tile in the area of the boundary geodataframe.

    :param (int, int, int, int) bounding_box: bounding box (x_1, y_1, x_2, y_2)
    :param int epsg_code: epsg code of the coordinate reference system
    :param gpd.GeoDataFrame boundary_gdf: boundary geodataframe
    :returns: internal coordinates (x, y) of each tile
    :rtype: list[(int, int)]
    """
    coordinates = get_coordinates(bounding_box)

    grid_generator = GridGenerator(bounding_box=bounding_box,
                                   epsg_code=epsg_code)
    grid_gdf = grid_generator.get_grid(tile_size_meters=utils.IMAGE_SIZE_METERS)

    valid_coordinates = list(grid_gdf['geometry'].intersects(boundary_gdf['geometry'][0]))
    coordinates = [coordinates_element for (coordinates_element, valid) in zip(coordinates, valid_coordinates)
                   if valid]

    return coordinates


def filter_downloaded_coordinates(coordinates, output_dir_path):
    """
    | Returns the filtered coordinates. If a tile is already being downloaded (its shape file directory in
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
            processed_coordinates = (int(match.group(1)), int(match.group(2)))
            if processed_coordinates in coordinates:
                filtered_coordinates.remove(processed_coordinates)

    return filtered_coordinates
