# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import geopandas as gpd
from shapely.geometry import Polygon


polygon_coordinates_0 = [[-.25, -.25],
                         [.25, -.25],
                         [.25, .25],
                         [-.25, .25]]
polygon_coordinates_1 = [[-2.5, -2.5],
                         [-1.5, -2.5],
                         [-1.5, -1.5],
                         [-2.5, -1.5]]
polygon_coordinates_2 = [[-5.5, -5.5],
                         [-3.5, -5.5],
                         [-3.5, -3.5],
                         [-5.5, -3.5]]
polygon_coordinates_3 = [[1.5, -2.5],
                         [2.5, -2.5],
                         [2.5, -1.5],
                         [1.5, -1.5]]
polygon_coordinates_4 = [[3.5, -5.5],
                         [5.5, -5.5],
                         [5.5, -3.5],
                         [3.5, -3.5]]
polygon_coordinates_5 = [[1.5, 1.5],
                         [2.5, 1.5],
                         [2.5, 2.5],
                         [1.5, 2.5]]
polygon_coordinates_6 = [[3.5, 3.5],
                         [5.5, 3.5],
                         [5.5, 5.5],
                         [3.5, 5.5]]
polygon_coordinates_7 = [[-2.5, 1.5],
                         [-1.5, 1.5],
                         [-1.5, 2.5],
                         [-2.5, 2.5]]
polygon_coordinates_8 = [[-5.5, 3.5],
                         [-3.5, 3.5],
                         [-3.5, 5.5],
                         [-5.5, 5.5]]

polygon_0 = Polygon(polygon_coordinates_0)
polygon_1 = Polygon(polygon_coordinates_1)
polygon_2 = Polygon(polygon_coordinates_2)
polygon_3 = Polygon(polygon_coordinates_3)
polygon_4 = Polygon(polygon_coordinates_4)
polygon_5 = Polygon(polygon_coordinates_5)
polygon_6 = Polygon(polygon_coordinates_6)
polygon_7 = Polygon(polygon_coordinates_7)
polygon_8 = Polygon(polygon_coordinates_8)

sieve_gdf_polygons = [polygon_0,
                      polygon_1,
                      polygon_2,
                      polygon_3,
                      polygon_4,
                      polygon_5,
                      polygon_6,
                      polygon_7,
                      polygon_8]
sieve_gdf_gdf = gpd.GeoDataFrame(geometry=sieve_gdf_polygons, crs='EPSG:25832')

sieved_gdf_1_polygons = [polygon_1,
                         polygon_2,
                         polygon_3,
                         polygon_4,
                         polygon_5,
                         polygon_6,
                         polygon_7,
                         polygon_8]
sieved_gdf_1 = gpd.GeoDataFrame(geometry=sieved_gdf_1_polygons, crs='EPSG:25832')

empty_gdf = gpd.GeoDataFrame(geometry=[], crs='EPSG:25832')

parameters_sieve_gdf = \
    [
        ((sieve_gdf_gdf, 0), sieve_gdf_gdf),
        ((sieve_gdf_gdf, 1), sieved_gdf_1),
        ((sieve_gdf_gdf, 10), empty_gdf),
        ((empty_gdf, 0), empty_gdf),
        ((empty_gdf, 1), empty_gdf),
        ((empty_gdf, 10), empty_gdf)
    ]

polygon_coordinates = [[-6.5, -6.5],
                       [6.5, -6.5],
                       [6.5, 6.5],
                       [-6.5, 6.5]]

fill_polygon_polygon = Polygon(polygon_coordinates,
                               holes=[polygon_coordinates_0,
                                      polygon_coordinates_1,
                                      polygon_coordinates_2,
                                      polygon_coordinates_3,
                                      polygon_coordinates_4,
                                      polygon_coordinates_5,
                                      polygon_coordinates_6,
                                      polygon_coordinates_7,
                                      polygon_coordinates_8])
filled_polygon_1 = Polygon(polygon_coordinates,
                           holes=[polygon_coordinates_1,
                                  polygon_coordinates_2,
                                  polygon_coordinates_3,
                                  polygon_coordinates_4,
                                  polygon_coordinates_5,
                                  polygon_coordinates_6,
                                  polygon_coordinates_7,
                                  polygon_coordinates_8])
filled_polygon_10 = Polygon(polygon_coordinates)

parameters_fill_polygon = \
    [
        ((fill_polygon_polygon, 0), fill_polygon_polygon),
        ((fill_polygon_polygon, 1), filled_polygon_1),
        ((fill_polygon_polygon, 10), filled_polygon_10)
    ]
