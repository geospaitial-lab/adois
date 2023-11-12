import numpy as np


parameters_filter_cached_coordinates_no_cached_tiles_dir = \
    [(np.array([[512, 768], [768, 768], [512, 1024], [768, 1024]], dtype=np.int32),
      np.array([[512, 768], [768, 768], [512, 1024], [768, 1024]], dtype=np.int32)),
     (np.array([[512, -768], [768, -768], [512, -512], [768, -512]], dtype=np.int32),
      np.array([[512, -768], [768, -768], [512, -512], [768, -512]], dtype=np.int32)),
     (np.array([[-1024, -768], [-768, -768], [-1024, -512], [-768, -512]], dtype=np.int32),
      np.array([[-1024, -768], [-768, -768], [-1024, -512], [-768, -512]], dtype=np.int32)),
     (np.array([[-1024, 768], [-768, 768], [-1024, 1024], [-768, 1024]], dtype=np.int32),
      np.array([[-1024, 768], [-768, 768], [-1024, 1024], [-768, 1024]], dtype=np.int32)),
     (np.array([[-256, 0], [0, 0], [-256, 256], [0, 256]], dtype=np.int32),
      np.array([[-256, 0], [0, 0], [-256, 256], [0, 256]], dtype=np.int32))]

parameters_filter_cached_coordinates_empty_cached_tiles_dir = \
    [(np.array([[512, 768], [768, 768], [512, 1024], [768, 1024]], dtype=np.int32),
      np.array([[512, 768], [768, 768], [512, 1024], [768, 1024]], dtype=np.int32)),
     (np.array([[512, -768], [768, -768], [512, -512], [768, -512]], dtype=np.int32),
      np.array([[512, -768], [768, -768], [512, -512], [768, -512]], dtype=np.int32)),
     (np.array([[-1024, -768], [-768, -768], [-1024, -512], [-768, -512]], dtype=np.int32),
      np.array([[-1024, -768], [-768, -768], [-1024, -512], [-768, -512]], dtype=np.int32)),
     (np.array([[-1024, 768], [-768, 768], [-1024, 1024], [-768, 1024]], dtype=np.int32),
      np.array([[-1024, 768], [-768, 768], [-1024, 1024], [-768, 1024]], dtype=np.int32)),
     (np.array([[-256, 0], [0, 0], [-256, 256], [0, 256]], dtype=np.int32),
      np.array([[-256, 0], [0, 0], [-256, 256], [0, 256]], dtype=np.int32))]

parameters_filter_cached_coordinates_not_empty_cached_tiles_dir = \
    [(np.array([[512, 768], [768, 768], [512, 1024], [768, 1024]], dtype=np.int32),
      np.array([[512, 768], [768, 768]], dtype=np.int32)),
     (np.array([[512, -768], [768, -768], [512, -512], [768, -512]], dtype=np.int32),
      np.array([[512, -768], [768, -768]], dtype=np.int32)),
     (np.array([[-1024, -768], [-768, -768], [-1024, -512], [-768, -512]], dtype=np.int32),
      np.array([[-1024, -768], [-768, -768]], dtype=np.int32)),
     (np.array([[-1024, 768], [-768, 768], [-1024, 1024], [-768, 1024]], dtype=np.int32),
      np.array([[-1024, 768], [-768, 768]], dtype=np.int32)),
     (np.array([[-256, 0], [0, 0], [-256, 256], [0, 256]], dtype=np.int32),
      np.array([[-256, 0], [0, 0]], dtype=np.int32)),

     (np.array([[512, 1024], [768, 1024]], dtype=np.int32),
      np.empty(shape=(0, 2), dtype=np.int32)),
     (np.array([[512, -512], [768, -512]], dtype=np.int32),
      np.empty(shape=(0, 2), dtype=np.int32)),
     (np.array([[-1024, -512], [-768, -512]], dtype=np.int32),
      np.empty(shape=(0, 2), dtype=np.int32)),
     (np.array([[-1024, 1024], [-768, 1024]], dtype=np.int32),
      np.empty(shape=(0, 2), dtype=np.int32)),
     (np.array([[-256, 256], [0, 256]], dtype=np.int32),
      np.empty(shape=(0, 2), dtype=np.int32))]
