import re
from collections import OrderedDict
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio as rio
import rasterio.features
import topojson as tp
from shapely.geometry import box as Box  # PEP8 compliant
from shapely.geometry import Polygon

import src.utils.settings as settings

pd.options.mode.chained_assignment = None


class Postprocessor:
    ATTRIBUTES = OrderedDict()
    ATTRIBUTES['class'] = 'str:7'
    CLASS_MAP = {1: 'Hochbau', 2: 'Tiefbau'}
    SCHEMA = {'properties': ATTRIBUTES,
              'geometry': 'Polygon'}

    def __init__(self,
                 output_dir_path,
                 bounding_box,
                 epsg_code,
                 boundary_gdf):
        """
        | Constructor method

        :param str or Path output_dir_path: path to the output directory
        :param (int, int, int, int) bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :param int epsg_code: epsg code of the coordinate reference system
        :param gpd.GeoDataFrame or None boundary_gdf: boundary geodataframe
        :returns: None
        :rtype: None
        """
        self.cached_tiles_dir_path = Path(output_dir_path) / 'cached_tiles'
        self.x_min, self.y_min, self.x_max, self.y_max = bounding_box
        self.epsg_code = epsg_code
        self.boundary_gdf = boundary_gdf

    def create_cached_tiles_dir(self):
        """
        | Creates a cached_tiles directory in the output directory.

        :returns: None
        :rtype: None
        """
        self.cached_tiles_dir_path.mkdir(exist_ok=True)

    def export_features(self,
                        features,
                        coordinates):
        """
        | Exports features of a tile as a shape file (.shp) in a subdirectory to the cached_tiles directory.
        | Each subdirectory name is in the following schema: x_y

        :param list[dict[str, dict[str, Any]]] features: features
        :param (int, int) coordinates: coordinates (x, y)
        :returns: None
        :rtype: None
        """
        sub_dir_path = self.cached_tiles_dir_path / f'{coordinates[0]}_{coordinates[1]}'
        sub_dir_path.mkdir(exist_ok=True)

        for path in sub_dir_path.iterdir():
            path.unlink()

        if features:
            shape_file_path = sub_dir_path / f'{coordinates[0]}_{coordinates[1]}.shp'
            gdf = gpd.GeoDataFrame.from_features(features, crs=f'EPSG:{self.epsg_code}')
            gdf.to_file(str(shape_file_path), schema=Postprocessor.SCHEMA)

    def vectorize_mask(self,
                       mask,
                       coordinates):
        """
        | Exports a shape file (.shp) of the polygons in the vectorized mask given its coordinates
            of the top left corner in a subdirectory to the cached_tiles directory.

        :param np.ndarray[np.uint8] mask: mask
        :param (int, int) coordinates: coordinates (x, y)
        :returns: None
        :rtype: None
        """
        transform = rio.transform.from_origin(west=coordinates[0],
                                              north=coordinates[1],
                                              xsize=settings.RESOLUTION,
                                              ysize=settings.RESOLUTION)
        vectorized_mask = rio.features.shapes(mask, transform=transform)

        features = [{'properties': {'class': Postprocessor.CLASS_MAP.get(int(value))}, 'geometry': shape}
                    for shape, value in vectorized_mask if int(value) != 0]
        self.export_features(features=features,
                             coordinates=coordinates)

    def concatenate_cached_tiles(self, coordinates):
        """
        | Returns a geodataframe of the concatenated cached tiles.

        :param np.ndarray[np.int32] coordinates: coordinates (x_min, y_max) of each tile
        :returns: concatenated cached tiles
        :rtype: gpd.GeoDataFrame
        """
        cached_tiles = []

        pattern = re.compile(r'^(-?\d+)_(-?\d+)$')

        for path_cached_tile_dir in self.cached_tiles_dir_path.iterdir():
            match = pattern.search(path_cached_tile_dir.name)

            if match:
                x_min = int(match.group(1))
                y_max = int(match.group(2))

                coordinates_cached = np.array([x_min, y_max], dtype=np.int32)

                if np.any(np.all(coordinates == coordinates_cached, axis=1)):
                    path_cached_tile = (self.cached_tiles_dir_path /
                                        f'{x_min}_{y_max}' /
                                        f'{x_min}_{y_max}.gpkg')

                    if path_cached_tile.is_file():
                        cached_tile = gpd.read_file(path_cached_tile)
                        cached_tiles.append(cached_tile)

        cached_tiles_concatenated = gpd.GeoDataFrame(pd.concat(cached_tiles, ignore_index=True),
                                                     crs=f'EPSG:{self.epsg_code}')

        return cached_tiles_concatenated

    @staticmethod
    def sieve_gdf(gdf, sieve_size):
        """
        | Returns a sieved geodataframe.

        :param gpd.GeoDataFrame gdf: geodataframe
        :param int sieve_size: sieve size in square meters (minimum area of polygons to retain)
        :returns: sieved geodataframe
        :rtype: gpd.GeoDataFrame
        """
        if gdf.empty:
            return gdf

        mask = gdf.area >= sieve_size
        sieved_gdf = gdf.loc[mask]
        sieved_gdf.reset_index(drop=True,
                               inplace=True)
        return sieved_gdf

    @staticmethod
    def fill_polygon(polygon, hole_size):
        """
        | Returns a polygon without holes.
        |
        | Based on:
        | https://gis.stackexchange.com/a/409398

        :param Polygon polygon: polygon
        :param int hole_size: hole size in square meters (maximum area of holes in the polygons to retain)
        :returns: filled polygon
        :rtype: Polygon
        """
        if polygon.interiors:
            interiors = []
            for interior in polygon.interiors:
                polygon_interior = Polygon(interior)
                if polygon_interior.area >= hole_size:
                    interiors.append(interior)
            return Polygon(polygon.exterior.coords, holes=interiors)
        else:
            return polygon

    @staticmethod
    def fill_gdf(gdf, hole_size):
        """
        | Returns a geodataframe without holes in the polygons.
        | The hole size of buildings is doubled.
        |
        | Based on:
        | https://gis.stackexchange.com/a/409398
        | https://stackoverflow.com/a/61466689

        :param gpd.GeoDataFrame gdf: geodataframe
        :param int hole_size: hole size in square meters (maximum area of holes in the polygons to retain)
        :returns: filled geodataframe
        :rtype: gpd.GeoDataFrame
        """
        if gdf.empty:
            return gdf

        gdf['geometry'] = gdf.apply(lambda x:
                                    Postprocessor.fill_polygon(x['geometry'],
                                                               hole_size=2 * hole_size)
                                    if x['class'] == 'Hochbau'
                                    else Postprocessor.fill_polygon(x['geometry'],
                                                                    hole_size=hole_size),
                                    axis=1)
        return gdf

    def simplify_gdf(self, gdf):
        """
        | Returns a geodataframe with simplified polygons (Douglas-Peucker algorithm is used).

        :param gpd.GeoDataFrame gdf: geodataframe
        :returns: simplified geodataframe
        :rtype: gpd.GeoDataFrame
        """
        if gdf.empty:
            return gdf

        topo = tp.Topology(gdf, prequantize=False)
        simplified_gdf = topo.toposimplify(settings.RESOLUTION).to_gdf(crs=f'EPSG:{self.epsg_code}')
        return simplified_gdf

    def clip_gdf(self, gdf):
        """
        | Returns a clipped geodataframe.

        :param gpd.GeoDataFrame gdf: geodataframe
        :returns: clipped geodataframe
        :rtype: gpd.GeoDataFrame
        """
        if self.boundary_gdf is None:
            clipped_gdf = gpd.clip(gdf,
                                   mask=Box(self.x_min, self.y_min, self.x_max, self.y_max),
                                   keep_geom_type=True).reset_index(drop=True)
        else:
            clipped_gdf = gpd.clip(gdf,
                                   mask=self.boundary_gdf['geometry'],
                                   keep_geom_type=True).reset_index(drop=True)
        return clipped_gdf
