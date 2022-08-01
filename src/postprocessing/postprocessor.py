# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import re
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio as rio
import rasterio.features
import topojson as tp

import src.utils as utils


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

        features = [{'properties': {'class': int(value)}, 'geometry': shape}
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
    def simplify_gdf(gdf):
        """Returns a geodataframe with simplified polygons (Douglas-Peucker algorithm is used).

        :param gpd.GeoDataFrame gdf: geodataframe
        :returns: simplified geodataframe
        :rtype: gpd.GeoDataFrame
        """
        topo = tp.Topology(gdf, prequantize=False)
        simplified_gdf = topo.toposimplify(utils.RESOLUTION + .05).to_gdf()
        return simplified_gdf
