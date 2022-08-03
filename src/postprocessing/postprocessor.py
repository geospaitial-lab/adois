# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import re
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio as rio
import rasterio.features
import topojson as tp
from shapely.geometry import Polygon

import src.utils as utils


pd.options.mode.chained_assignment = None


class Postprocessor:
    def __init__(self,
                 output_dir_path,
                 epsg_code):
        """Constructor method

        :param str or Path output_dir_path: path to the output directory
        :param int epsg_code: epsg code of the coordinate reference system
        :returns: None
        :rtype: None
        """
        self.tiles_dir_path = Path(output_dir_path) / '.tiles'
        self.epsg_code = epsg_code

    def export_features(self,
                        features,
                        coordinates):
        """Exports features of a tile as a shape file (.shp) in a subdirectory to the .tiles directory.
        Each subdirectory name is in the following schema: x_y

        :param list[dict[str, dict[str, Any]]] features: features
        :param (int, int) coordinates: coordinates (x, y)
        :returns: None
        :rtype: None
        """
        (self.tiles_dir_path / f'{coordinates[0]}_{coordinates[1]}').mkdir()
        gdf_path = self.tiles_dir_path / f'{coordinates[0]}_{coordinates[1]}' / f'{coordinates[0]}_{coordinates[1]}.shp'
        gdf = gpd.GeoDataFrame.from_features(features, crs=f'EPSG:{self.epsg_code}')
        gdf.to_file(str(gdf_path))

    def vectorize_mask(self,
                       mask,
                       coordinates):
        """Exports a shape file (.shp) of the polygons in the vectorized mask given its coordinates
        of the top left corner in a subdirectory to the .tiles directory.

        :param np.ndarray[np.uint8] mask: mask
        :param (int, int) coordinates: coordinates (x, y)
        :returns: None
        :rtype: None
        """
        transform = rio.transform.from_origin(west=coordinates[0],
                                              north=coordinates[1],
                                              xsize=utils.RESOLUTION,
                                              ysize=utils.RESOLUTION)
        vectorized_mask = rio.features.shapes(mask, transform=transform)

        features = [{'properties': {'geometry': shape, 'class': int(value)}}
                    for shape, value in vectorized_mask if int(value) != 0]
        self.export_features(features=features,
                             coordinates=coordinates)

    def concatenate_gdfs(self, coordinates):
        """Returns a concatenated geodataframe.

        :param list[(int, int)] coordinates: coordinates (x, y) of each tile
        :returns: concatenated geodataframe
        :rtype: gpd.GeoDataFrame
        """
        gdfs = []

        pattern = re.compile(r'^(-?\d+)_(-?\d+)$')

        for path in self.tiles_dir_path.iterdir():
            match = pattern.search(path.name)
            if match:
                processed_coordinates = (int(match.group(1)), int(match.group(2)))
                if processed_coordinates in coordinates:
                    gdf_path = (self.tiles_dir_path / f'{processed_coordinates[0]}_{processed_coordinates[1]}' /
                                f'{processed_coordinates[0]}_{processed_coordinates[1]}.shp')
                    gdf = gpd.read_file(gdf_path)
                    gdfs.append(gdf)

        concatenated_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=f'EPSG:{self.epsg_code}')
        return concatenated_gdf

    @staticmethod
    def sieve_gdf(gdf, sieve_size):
        """Returns a sieved geodataframe.

        :param gpd.GeoDataFrame gdf: geodataframe
        :param int sieve_size: sieve size in square meters (minimum area of polygons to retain)
        :returns: sieved geodataframe
        :rtype: gpd.GeoDataFrame
        """
        mask = gdf.area > sieve_size
        sieved_gdf = gdf.loc[mask]
        return sieved_gdf

    @staticmethod
    def fill_polygon(polygon, hole_size):
        """Returns a polygon without holes.
        Based on: https://gis.stackexchange.com/a/409398

        :param Polygon polygon: polygon
        :param int hole_size: hole size in square meters (maximum area of holes in the polygons to retain)
        :returns: filled polygon
        :rtype: Polygon
        """
        if polygon.interiors:
            interiors = []
            for interior in polygon.interiors:
                polygon_interior = Polygon(interior)
                if polygon_interior.area > hole_size:
                    interiors.append(interior)
            return Polygon(polygon.exterior.coords, holes=interiors)
        else:
            return polygon

    @staticmethod
    def fill_gdf(gdf, hole_size):
        """Returns a geodataframe without holes in the polygons.
        Based on: https://gis.stackexchange.com/a/409398 and https://stackoverflow.com/a/61466689

        :param gpd.GeoDataFrame gdf: geodataframe
        :param int hole_size: hole size in square meters (maximum area of holes in the polygons to retain)
        :returns: filled geodataframe
        :rtype: gpd.GeoDataFrame
        """
        gdf['geometry'] = gdf['geometry'].apply(lambda polygon:
                                                Postprocessor.fill_polygon(polygon, hole_size=hole_size))
        return gdf

    def simplify_gdf(self, gdf):
        """Returns a geodataframe with simplified polygons (Douglas-Peucker algorithm is used).

        :param gpd.GeoDataFrame gdf: geodataframe
        :returns: simplified geodataframe
        :rtype: gpd.GeoDataFrame
        """
        topo = tp.Topology(gdf, prequantize=False)
        simplified_gdf = topo.toposimplify(utils.RESOLUTION + .05).to_gdf(crs=f'EPSG:{self.epsg_code}')
        return simplified_gdf
