import numpy as np

parameters_float32_casting_preprocess = (
    [(np.full(shape=(128, 128, 6),
              fill_value=(0, 51, 102, 153, 204, 255),
              dtype=np.uint8),
      np.full(shape=(128, 128, 6),
              fill_value=(0, 51, 102, 153, 204, 255),
              dtype=np.float32)),
     (np.full(shape=(128, 128, 6),
              fill_value=(0, 51, 102, 153, 204, 255),
              dtype=np.float32),
      np.full(shape=(128, 128, 6),
              fill_value=(0, 51, 102, 153, 204, 255),
              dtype=np.float32))])
