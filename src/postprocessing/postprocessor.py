# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio as rio
import rasterio.features
import topojson as tp

import src.utils as utils


class Postprocessor:
    def __init__(self,
                 sieve_size,
                 output_dir_path):
        """Constructor method

        :param int or None sieve_size: sieve size in pixels (minimum number of pixels to retain)
        :param str or Path output_dir_path: path to the output directory
        :returns: None
        :rtype: None
        """
        self.sieve_size = sieve_size
        self.features_dir_path = Path(output_dir_path) / '.features'

    def export_features(self,
                        features,
                        coordinates):
        """Exports features as a features file (.json) to the .features directory.
        Each features file name is in the following schema: x_y.json

        :param list[dict[str, dict[str, Any]]] features: features
        :param (int, int) coordinates: coordinates (x, y)
        :returns: None
        :rtype: None
        """
        path = self.features_dir_path / f'{coordinates[0]}_{coordinates[1]}.json'
        with open(path, mode='w') as file:
            json.dump(features, file, indent=4)

    def vectorize_mask(self,
                       mask,
                       coordinates):
        """Exports georeferenced features of the polygons in the vectorized mask given its coordinates
        of the top left corner as a features file (.json) to the .features directory.

        :param np.ndarray[np.uint8] mask: mask
        :param (int, int) coordinates: coordinates (x, y)
        :returns: None
        :rtype: None
        """
        if self.sieve_size is not None:
            mask = rio.features.sieve(mask, size=self.sieve_size)

        transform = rio.transform.from_origin(west=coordinates[0],
                                              north=coordinates[1],
                                              xsize=utils.RESOLUTION,
                                              ysize=utils.RESOLUTION)
        vectorized_mask = rio.features.shapes(mask, transform=transform)

        features = [{'properties': {'class': int(value)}, 'geometry': shape}
                    for shape, value in vectorized_mask if int(value) != 0]
        self.export_features(features=features,
                             coordinates=coordinates)

    @staticmethod
    def get_gdf(features):
        """Returns a geodataframe.

        :param dict features: features
        :returns: gdf
        :rtype: gpd.GeoDataFrame
        """
        gdf = gpd.GeoDataFrame.from_features(features)
        gdf = gdf.set_crs(epsg=25832)
        return gdf

    @staticmethod
    def simplify_gdf(gdf):
        """Returns a geodataframe with simplified polygons (Douglas-Peucker algorithm is used).

        :param gpd.GeoDataFrame gdf: gdf
        :returns: simplified gdf
        :rtype: gpd.GeoDataFrame
        """
        topo = tp.Topology(gdf, prequantize=False)
        gdf = topo.toposimplify(utils.RESOLUTION + .05).to_gdf()
        return gdf
