import geopandas as gpd
import shapely.affinity
from shapely.geometry import Polygon


polygon_exterior_coordinates = [[-14., -14.],
                                [14., -14.],
                                [14., 14.],
                                [-14., 14.]]

unit_polygon = Polygon([[0., 0.], [1., 0.], [1., 1.], [0., 1.]])

polygons_interior = [shapely.affinity.affine_transform(unit_polygon, matrix=[1., 0., 0., 1., -.5, -.5]),

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

polygon = Polygon(polygon_exterior_coordinates,
                  holes=[list(polygon_interior.exterior.coords) for polygon_interior in polygons_interior])

gdf_buildings = gpd.GeoDataFrame(geometry=[polygon], crs='EPSG:25832')
gdf_buildings['class'] = ['Hochbau']

gdf_pavements = gpd.GeoDataFrame(geometry=[polygon], crs='EPSG:25832')
gdf_pavements['class'] = ['Tiefbau']

gdf = gpd.GeoDataFrame(geometry=[shapely.affinity.affine_transform(polygon, matrix=[1., 0., 0., 1., -14.25, 0.]),
                                 shapely.affinity.affine_transform(polygon, matrix=[1., 0., 0., 1., 14.25, 0.])],
                       crs='EPSG:25832')
gdf['class'] = ['Hochbau', 'Tiefbau']

filled_polygon_buildings_1 = Polygon(polygon_exterior_coordinates,
                                     holes=[list(polygon_interior.exterior.coords) for polygon_interior in
                                            polygons_interior if polygon_interior.area >= 2])
filled_polygon_buildings_10 = Polygon(polygon_exterior_coordinates,
                                      holes=[list(polygon_interior.exterior.coords) for polygon_interior in
                                             polygons_interior if polygon_interior.area >= 20])

filled_gdf_buildings_1 = gpd.GeoDataFrame(geometry=[filled_polygon_buildings_1], crs='EPSG:25832')
filled_gdf_buildings_1['class'] = ['Hochbau']
filled_gdf_buildings_10 = gpd.GeoDataFrame(geometry=[filled_polygon_buildings_10], crs='EPSG:25832')
filled_gdf_buildings_10['class'] = ['Hochbau']

filled_polygon_pavements_1 = Polygon(polygon_exterior_coordinates,
                                    holes=[list(polygon_interior.exterior.coords) for polygon_interior in
                                           polygons_interior if polygon_interior.area >= 1])
filled_polygon_pavements_10 = Polygon(polygon_exterior_coordinates,
                                     holes=[list(polygon_interior.exterior.coords) for polygon_interior in
                                            polygons_interior if polygon_interior.area >= 10])

filled_gdf_pavements_1 = gpd.GeoDataFrame(geometry=[filled_polygon_pavements_1], crs='EPSG:25832')
filled_gdf_pavements_1['class'] = ['Tiefbau']
filled_gdf_pavements_10 = gpd.GeoDataFrame(geometry=[filled_polygon_pavements_10], crs='EPSG:25832')
filled_gdf_pavements_10['class'] = ['Tiefbau']

filled_gdf_1 = gpd.GeoDataFrame(geometry=[shapely.affinity.affine_transform(filled_polygon_buildings_1,
                                                                            matrix=[1., 0., 0., 1., -14.25, 0.]),
                                          shapely.affinity.affine_transform(filled_polygon_pavements_1,
                                                                            matrix=[1., 0., 0., 1., 14.25, 0.])],
                                crs='EPSG:25832')
filled_gdf_1['class'] = ['Hochbau', 'Tiefbau']
filled_gdf_10 = gpd.GeoDataFrame(geometry=[shapely.affinity.affine_transform(filled_polygon_buildings_10,
                                                                             matrix=[1., 0., 0., 1., -14.25, 0.]),
                                           shapely.affinity.affine_transform(filled_polygon_pavements_10,
                                                                             matrix=[1., 0., 0., 1., 14.25, 0.])],
                                 crs='EPSG:25832')
filled_gdf_10['class'] = ['Hochbau', 'Tiefbau']

empty_gdf = gpd.GeoDataFrame(geometry=[], crs='EPSG:25832')

parameters_fill_gdf = [((gdf_buildings, 0), gdf_buildings),
                       ((gdf_buildings, 1), filled_gdf_buildings_1),
                       ((gdf_buildings, 10), filled_gdf_buildings_10),
                       ((gdf_pavements, 0), gdf_pavements),
                       ((gdf_pavements, 1), filled_gdf_pavements_1),
                       ((gdf_pavements, 10), filled_gdf_pavements_10),
                       ((gdf, 0), gdf),
                       ((gdf, 1), filled_gdf_1),
                       ((gdf, 10), filled_gdf_10),
                       ((empty_gdf, 0), empty_gdf),
                       ((empty_gdf, 1), empty_gdf),
                       ((empty_gdf, 10), empty_gdf)]
