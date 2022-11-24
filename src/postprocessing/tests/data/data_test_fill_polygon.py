# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

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
