import re
from pathlib import Path

import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import rasterio as rio
import rasterio.features
import topojson as tp
from shapely.geometry import box, Polygon

from src.utils.settings import RESOLUTION

pd.options.mode.chained_assignment = None


class Postprocessor:
    FIELD = 'class'

    def __init__(self,
                 path_output_dir: Path,
                 epsg_code: int) -> None:
        """
        :param path_output_dir: path to the output directory
        :param epsg_code: epsg code
        """
        assert isinstance(path_output_dir, Path)

        assert isinstance(epsg_code, int)

        self.path_tiles_processed_dir = path_output_dir / 'tiles_processed'
        self.epsg_code = epsg_code

    @staticmethod
    def vectorize_mask(mask: npt.NDArray[np.uint8],
                       coordinates: tuple[int, int]) -> list[dict[str, dict[str, any]]]:
        """
        | Returns the features of the mask.
        | The features implement the __geo_interface__ protocol.

        :param mask: mask
        :param coordinates: coordinates (x_min, y_max)
        :returns: features
        """
        assert isinstance(mask, np.ndarray)
        assert mask.dtype == np.uint8
        assert mask.ndim == 2

        assert isinstance(coordinates, tuple)
        assert len(coordinates) == 2
        assert all(isinstance(coordinate, int) for coordinate in coordinates)

        x_min, y_max = coordinates

        transform = rio.transform.from_origin(west=x_min,
                                              north=y_max,
                                              xsize=RESOLUTION,
                                              ysize=RESOLUTION)

        features = [{'properties': {Postprocessor.FIELD: int(value)},
                     'geometry': polygon}
                    for polygon, value in rio.features.shapes(mask, transform=transform)
                    if int(value) != 0]

        return features

    def export_features(self,
                        features: list[dict[str, dict[str, any]]],
                        coordinates: tuple[int, int]) -> None:
        """
        | Exports the features of the tile as a feather file to a subdirectory in the tiles_processed directory.

        :param features: features
        :param coordinates: coordinates (x_min, y_max)
        """
        assert isinstance(features, list)

        if __debug__:
            for features_element in features:
                assert isinstance(features_element, dict)
                assert 'properties' in features_element
                assert isinstance(features_element['properties'], dict)
                assert Postprocessor.FIELD in features_element['properties']
                assert isinstance(features_element['properties'][Postprocessor.FIELD], int)
                assert 'geometry' in features_element
                assert isinstance(features_element['geometry'], dict)

        assert isinstance(coordinates, tuple)
        assert len(coordinates) == 2
        assert all(isinstance(coordinate, int) for coordinate in coordinates)

        x_min, y_max = coordinates

        path_tile_processed_dir = self.path_tiles_processed_dir / f'{x_min}_{y_max}'

        path_tile_processed_dir.mkdir(exist_ok=True)

        for path in path_tile_processed_dir.iterdir():
            path.unlink()

        if features:
            path_tile_processed = path_tile_processed_dir / f'{x_min}_{y_max}.feather'

            gdf = gpd.GeoDataFrame.from_features(features=features,
                                                 crs=f'EPSG:{self.epsg_code}')

            gdf[Postprocessor.FIELD] = gdf[Postprocessor.FIELD].astype(np.uint8)
            gdf.to_feather(path_tile_processed)

    def concatenate_processed_tiles(self,
                                    coordinates: npt.NDArray[np.int32],
                                    value_map: dict[int, str] = None) -> gpd.GeoDataFrame:
        """
        | Returns a geodataframe of the concatenated processed tiles.

        :param coordinates: coordinates (x_min, y_max) of each tile
        :param value_map: value map
        :returns: concatenated processed tiles
        """
        assert isinstance(coordinates, np.ndarray)
        assert coordinates.dtype == np.int32
        assert coordinates.ndim == 2
        assert coordinates.shape[-1] == 2

        assert isinstance(value_map, dict) or value_map is None

        if value_map is not None:
            assert all(isinstance(value_int, int) for value_int in value_map.keys())
            assert all(isinstance(value_str, str) for value_str in value_map.values())

        tiles_processed = []

        pattern = re.compile(r'^(-?\d+)_(-?\d+)$')

        for path_tile_processed_dir in self.path_tiles_processed_dir.iterdir():
            if not path_tile_processed_dir.is_dir():
                continue

            match = pattern.search(path_tile_processed_dir.name)

            if match:
                x_min = int(match.group(1))
                y_max = int(match.group(2))

                coordinates_processed = np.array([x_min, y_max], dtype=np.int32)

                if np.any(np.all(coordinates == coordinates_processed, axis=1)):
                    path_tile_processed = (self.path_tiles_processed_dir
                                           / f'{x_min}_{y_max}'
                                           / f'{x_min}_{y_max}.feather')

                    if path_tile_processed.is_file():
                        tile_processed = gpd.read_feather(path_tile_processed)
                        tiles_processed.append(tile_processed)
                    else:
                        pass  # TODO: log warning

        tiles_processed_concatenated = gpd.GeoDataFrame(pd.concat(tiles_processed, ignore_index=True),
                                                        crs=f'EPSG:{self.epsg_code}')

        if value_map is not None:
            tiles_processed_concatenated[Postprocessor.FIELD] = (
                tiles_processed_concatenated[Postprocessor.FIELD].map(value_map).astype('category'))

        return tiles_processed_concatenated

    @staticmethod
    def sieve_gdf(gdf: gpd.GeoDataFrame,
                  sieve_size: int) -> gpd.GeoDataFrame:
        """
        | Returns the sieved geodataframe.

        :param gdf: geodataframe
        :param sieve_size: sieve size in square meters (minimum area of polygons to retain)
        :returns: sieved geodataframe
        """
        assert isinstance(gdf, gpd.GeoDataFrame)

        if gdf.empty:
            return gdf

        assert all(gdf['geometry'].geom_type == 'Polygon')
        assert all(gdf['geometry'].is_valid)

        assert isinstance(sieve_size, int)
        assert sieve_size >= 0

        if sieve_size == 0:
            return gdf

        gdf_sieved = gdf[gdf['geometry'].area >= sieve_size]

        gdf_sieved.reset_index(drop=True,
                               inplace=True)

        return gdf_sieved

    @staticmethod
    def fill_polygon(polygon: Polygon,
                     hole_size: int) -> Polygon:
        """
        | Returns the polygon without holes.

        :param polygon: polygon
        :param hole_size: hole size in square meters (maximum area of holes in the polygons to retain)
        :returns: filled polygon
        """
        assert isinstance(polygon, Polygon)
        assert polygon.is_valid

        if not polygon.interiors:
            return polygon

        assert isinstance(hole_size, int)
        assert hole_size >= 0

        if hole_size == 0:
            return Polygon(polygon.exterior.coords)

        interiors = [interior
                     for interior in polygon.interiors
                     if Polygon(interior).area >= hole_size]

        return Polygon(polygon.exterior.coords, holes=interiors)

    @staticmethod
    def fill_gdf(gdf: gpd.GeoDataFrame,
                 hole_size: int) -> gpd.GeoDataFrame:
        """
        | Returns the filled geodataframe.

        :param gdf: geodataframe
        :param hole_size: hole size in square meters (maximum area of holes in the polygons to retain)
        :returns: filled geodataframe
        """
        assert isinstance(gdf, gpd.GeoDataFrame)

        if gdf.empty:
            return gdf

        assert all(gdf['geometry'].geom_type == 'Polygon')
        assert all(gdf['geometry'].is_valid)

        assert isinstance(hole_size, int)
        assert hole_size >= 0

        gdf['geometry'] = gdf.apply(lambda x: Postprocessor.fill_polygon(x['geometry'], hole_size=hole_size), axis=1)

        return gdf

    def simplify_gdf(self,
                     gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        | Returns the simplified geodataframe.
        | The Douglas-Peucker algorithm is used.

        :param gdf: geodataframe
        :returns: simplified geodataframe
        """
        assert isinstance(gdf, gpd.GeoDataFrame)

        if gdf.empty:
            return gdf

        assert all(gdf['geometry'].geom_type == 'Polygon')
        assert all(gdf['geometry'].is_valid)
        assert gdf.crs == f'EPSG:{self.epsg_code}'

        topo = tp.Topology(gdf, prequantize=False)
        topo_simplified = topo.toposimplify(epsilon=RESOLUTION,
                                            simplify_with='simplification')

        return topo_simplified.to_gdf(crs=f'EPSG:{self.epsg_code}')

    def clip_gdf(self,
                 gdf: gpd.GeoDataFrame,
                 bounding_box: tuple[int, int, int, int],
                 boundary: gpd.GeoDataFrame = None) -> gpd.GeoDataFrame:
        """
        | Returns the clipped geodataframe.

        :param gdf: geodataframe
        :param bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :param boundary: boundary
        :returns: clipped geodataframe
        """
        assert isinstance(gdf, gpd.GeoDataFrame)

        if gdf.empty:
            return gdf

        assert all(gdf['geometry'].geom_type == 'Polygon')
        assert all(gdf['geometry'].is_valid)
        assert gdf.crs == f'EPSG:{self.epsg_code}'

        assert isinstance(bounding_box, tuple)
        assert len(bounding_box) == 4
        assert all(isinstance(coordinate, int) for coordinate in bounding_box)

        assert isinstance(boundary, gpd.GeoDataFrame) or boundary is None

        if boundary is not None:
            assert not boundary.empty
            assert all(boundary['geometry'].geom_type == 'Polygon')
            assert all(boundary['geometry'].is_valid)
            assert boundary.crs == f'EPSG:{self.epsg_code}'

        x_min, y_min, x_max, y_max = bounding_box

        if boundary is None:
            gdf_clipped = gpd.clip(gdf,
                                   mask=box(x_min, y_min, x_max, y_max),
                                   keep_geom_type=True).reset_index(drop=True)
        else:
            gdf_clipped = gpd.clip(gdf,
                                   mask=boundary['geometry'],
                                   keep_geom_type=True).reset_index(drop=True)

        return gdf_clipped
