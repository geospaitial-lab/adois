# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from shapely.geometry import Polygon


polygon_interior_coordinates = [[[-.25, -.25],
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

polygon_exterior_coordinates = [[-6.5, -6.5],
                                [6.5, -6.5],
                                [6.5, 6.5],
                                [-6.5, 6.5]]

polygon = Polygon(polygon_exterior_coordinates, holes=polygon_interior_coordinates)
filled_polygon_1 = Polygon(polygon_exterior_coordinates, holes=polygon_interior_coordinates[1:])
filled_polygon_10 = Polygon(polygon_exterior_coordinates)

parameters_fill_polygon = [((polygon, 0), polygon),
                           ((polygon, 1), filled_polygon_1),
                           ((polygon, 10), filled_polygon_10)]
