# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import geopandas as gpd
import shapely.affinity
from shapely.geometry import Polygon


unit_polygon = Polygon([[0., 0.], [1., 0.], [1., 1.], [0., 1.]])

polygons = [shapely.affinity.affine_transform(unit_polygon, matrix=[1., 0., 0., 1., -.5, -.5]),

            shapely.affinity.affine_transform(unit_polygon, matrix=[.5, 0., 0., .5, -1.5, -1.5]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[1., 0., 0., 1., -3., -3.]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[2., 0., 0., 2., -5.5, -5.5]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[3., 0., 0., 3., -9., -9.]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[4., 0., 0., 4., -13.5, -13.5]),

            shapely.affinity.affine_transform(unit_polygon, matrix=[.5, 0., 0., .5, 1., -1.5]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[1., 0., 0., 1., 2., -3.]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[2., 0., 0., 2., 3.5, -5.5]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[3., 0., 0., 3., 6., -9.]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[4., 0., 0., 4., 9.5, -13.5]),

            shapely.affinity.affine_transform(unit_polygon, matrix=[.5, 0., 0., .5, 1., 1.]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[1., 0., 0., 1., 2., 2.]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[2., 0., 0., 2., 3.5, 3.5]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[3., 0., 0., 3., 6., 6.]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[4., 0., 0., 4., 9.5, 9.5]),

            shapely.affinity.affine_transform(unit_polygon, matrix=[.5, 0., 0., .5, -1.5, 1.]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[1., 0., 0., 1., -3., 2.]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[2., 0., 0., 2., -5.5, 3.5]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[3., 0., 0., 3., -9., 6.]),
            shapely.affinity.affine_transform(unit_polygon, matrix=[4., 0., 0., 4., -13.5, 9.5])]

gdf = gpd.GeoDataFrame(geometry=polygons, crs='EPSG:25832')

sieved_gdf_1 = gpd.GeoDataFrame(geometry=[polygon for polygon in polygons if polygon.area >= 1], crs='EPSG:25832')
sieved_gdf_10 = gpd.GeoDataFrame(geometry=[polygon for polygon in polygons if polygon.area >= 10], crs='EPSG:25832')

empty_gdf = gpd.GeoDataFrame(geometry=[], crs='EPSG:25832')

parameters_sieve_gdf = [((gdf, 0), gdf),
                        ((gdf, 1), sieved_gdf_1),
                        ((gdf, 10), sieved_gdf_10),
                        ((empty_gdf, 0), empty_gdf),
                        ((empty_gdf, 1), empty_gdf),
                        ((empty_gdf, 10), empty_gdf)]
