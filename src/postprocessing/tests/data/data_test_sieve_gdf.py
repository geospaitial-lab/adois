# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import geopandas as gpd
from shapely.geometry import Polygon


polygon_coordinates = [[[-.25, -.25],
                        [.25, -.25],
                        [.25, .25],
                        [-.25, .25]],
                       [[-2.5, -2.5],
                        [-1.5, -2.5],
                        [-1.5, -1.5],
                        [-2.5, -1.5]],
                       [[-5.5, -5.5],
                        [-3.5, -5.5],
                        [-3.5, -3.5],
                        [-5.5, -3.5]],
                       [[1.5, -2.5],
                        [2.5, -2.5],
                        [2.5, -1.5],
                        [1.5, -1.5]],
                       [[3.5, -5.5],
                        [5.5, -5.5],
                        [5.5, -3.5],
                        [3.5, -3.5]],
                       [[1.5, 1.5],
                        [2.5, 1.5],
                        [2.5, 2.5],
                        [1.5, 2.5]],
                       [[3.5, 3.5],
                        [5.5, 3.5],
                        [5.5, 5.5],
                        [3.5, 5.5]],
                       [[-2.5, 1.5],
                        [-1.5, 1.5],
                        [-1.5, 2.5],
                        [-2.5, 2.5]],
                       [[-5.5, 3.5],
                        [-3.5, 3.5],
                        [-3.5, 5.5],
                        [-5.5, 5.5]]]

polygons = [Polygon(polygon_coordinates_element) for polygon_coordinates_element in polygon_coordinates]

gdf = gpd.GeoDataFrame(geometry=polygons, crs='EPSG:25832')
sieved_gdf_1 = gpd.GeoDataFrame(geometry=polygons[1:], crs='EPSG:25832')
empty_gdf = gpd.GeoDataFrame(geometry=[], crs='EPSG:25832')

parameters_sieve_gdf = \
    [
        ((gdf, 0), gdf),
        ((gdf, 1), sieved_gdf_1),
        ((gdf, 10), empty_gdf),
        ((empty_gdf, 0), empty_gdf),
        ((empty_gdf, 1), empty_gdf),
        ((empty_gdf, 10), empty_gdf)
    ]
