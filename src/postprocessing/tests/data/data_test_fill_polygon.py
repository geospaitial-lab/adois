# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

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

filled_polygon_1 = Polygon(polygon_exterior_coordinates,
                           holes=[list(polygon_interior.exterior.coords) for polygon_interior in polygons_interior
                                  if polygon_interior.area >= 1])
filled_polygon_10 = Polygon(polygon_exterior_coordinates,
                            holes=[list(polygon_interior.exterior.coords) for polygon_interior in polygons_interior
                                   if polygon_interior.area >= 10])

parameters_fill_polygon = [((polygon, 0), polygon),
                           ((polygon, 1), filled_polygon_1),
                           ((polygon, 10), filled_polygon_10)]
