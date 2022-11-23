# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import geopandas as gpd
from shapely.geometry import Polygon


sieved_gdf_polygon_0 = Polygon([[-.25, -.25],
                                [.25, -.25],
                                [.25, .25],
                                [-.25, .25]])
sieved_gdf_polygon_1 = Polygon([[-2.5, -2.5],
                                [-1.5, -2.5],
                                [-1.5, -1.5],
                                [-2.5, -1.5]])
sieved_gdf_polygon_2 = Polygon([[-5.5, -5.5],
                                [-3.5, -5.5],
                                [-3.5, -3.5],
                                [-5.5, -3.5]])
sieved_gdf_polygon_3 = Polygon([[1.5, -2.5],
                                [2.5, -2.5],
                                [2.5, -1.5],
                                [1.5, -1.5]])
sieved_gdf_polygon_4 = Polygon([[3.5, -5.5],
                                [5.5, -5.5],
                                [5.5, -3.5],
                                [3.5, -3.5]])
sieved_gdf_polygon_5 = Polygon([[1.5, 1.5],
                                [2.5, 1.5],
                                [2.5, 2.5],
                                [1.5, 2.5]])
sieved_gdf_polygon_6 = Polygon([[3.5, 3.5],
                                [5.5, 3.5],
                                [5.5, 5.5],
                                [3.5, 5.5]])
sieved_gdf_polygon_7 = Polygon([[-2.5, 1.5],
                                [-1.5, 1.5],
                                [-1.5, 2.5],
                                [-2.5, 2.5]])
sieved_gdf_polygon_8 = Polygon([[-5.5, 3.5],
                                [-3.5, 3.5],
                                [-3.5, 5.5],
                                [-5.5, 5.5]])

sieved_gdf_polygons = [sieved_gdf_polygon_0,
                       sieved_gdf_polygon_1,
                       sieved_gdf_polygon_2,
                       sieved_gdf_polygon_3,
                       sieved_gdf_polygon_4,
                       sieved_gdf_polygon_5,
                       sieved_gdf_polygon_6,
                       sieved_gdf_polygon_7,
                       sieved_gdf_polygon_8]
sieved_gdf = gpd.GeoDataFrame(geometry=sieved_gdf_polygons, crs='EPSG:25832')

sieved_gdf_1_polygons = [sieved_gdf_polygon_1,
                         sieved_gdf_polygon_2,
                         sieved_gdf_polygon_3,
                         sieved_gdf_polygon_4,
                         sieved_gdf_polygon_5,
                         sieved_gdf_polygon_6,
                         sieved_gdf_polygon_7,
                         sieved_gdf_polygon_8]
sieved_gdf_1 = gpd.GeoDataFrame(geometry=sieved_gdf_1_polygons, crs='EPSG:25832')

empty_gdf = gpd.GeoDataFrame(geometry=[], crs='EPSG:25832')

parameters_sieve_gdf = \
    [
        ((sieved_gdf, 0), sieved_gdf),
        ((sieved_gdf, 1), sieved_gdf_1),
        ((sieved_gdf, 10), empty_gdf),
        ((empty_gdf, 0), empty_gdf),
        ((empty_gdf, 1), empty_gdf),
        ((empty_gdf, 10), empty_gdf)
    ]
