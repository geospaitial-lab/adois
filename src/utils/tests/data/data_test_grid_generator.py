import geopandas as gpd
import numpy as np
from shapely.geometry import box

parameters_init = \
    [(((-128, -128, 128, 128), 25832), ((-128, -128, 128, 128), 25832))]

parameters_compute_coordinates = \
    [((128, True), np.array([[-128, -128], [0, -128], [-128, 0], [0, 0]], dtype=np.int32)),
     ((128, False), np.array([[-128, -128], [0, -128], [-128, 0], [0, 0]], dtype=np.int32)),
     ((127, True), np.array([[-254, -254], [-127, -254], [0, -254], [127, -254],
                             [-254, -127], [-127, -127], [0, -127], [127, -127],
                             [-254, 0], [-127, 0], [0, 0], [127, 0],
                             [-254, 127], [-127, 127], [0, 127], [127, 127]], dtype=np.int32)),
     ((127, False), np.array([[-128, -128], [-1, -128], [126, -128],
                              [-128, -1], [-1, -1], [126, -1],
                              [-128, 126], [-1, 126], [126, 126]], dtype=np.int32)),
     ((129, True), np.array([[-129, -129], [0, -129], [-129, 0], [0, 0]], dtype=np.int32)),
     ((129, False), np.array([[-128, -128], [1, -128], [-128, 1], [1, 1]], dtype=np.int32))]

parameters_generate_polygons = \
    [((np.array([[-128, -128], [0, -128], [-128, 0], [0, 0]], dtype=np.int32), 128),
      [box(-128, -128, 0, 0), box(0, -128, 128, 0), box(-128, 0, 0, 128), box(0, 0, 128, 128)])]

parameters_generate_grid = \
    [((128, True),
      gpd.GeoDataFrame(geometry=[box(-128, -128, 0, 0),
                                 box(0, -128, 128, 0),
                                 box(-128, 0, 0, 128),
                                 box(0, 0, 128, 128)],
                       crs='EPSG:25832'))]
