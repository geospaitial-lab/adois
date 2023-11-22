import numpy as np

from src.preprocessing.preprocessing_strategies import Float32Casting, UInt8LinearScalingNormalization

parameters_init = \
    [([], []),
     ([Float32Casting()], [Float32Casting()]),
     ([UInt8LinearScalingNormalization()], [UInt8LinearScalingNormalization()]),
     ([Float32Casting(), UInt8LinearScalingNormalization()], [Float32Casting(), UInt8LinearScalingNormalization()])]

parameters_set_image_rgb = \
    [(np.full(shape=(128, 128, 3),
              fill_value=(0, 1, 2),
              dtype=np.uint8),
      np.full(shape=(128, 128, 3),
              fill_value=(0, 1, 2),
              dtype=np.uint8))]

parameters_set_image_nir = \
    [(np.full(shape=(128, 128, 3),
              fill_value=(0, 1, 2),
              dtype=np.uint8),
      np.full(shape=(128, 128, 1),
              fill_value=0,
              dtype=np.uint8))]

parameters_set_preprocessing_strategies = \
    [([], []),
     ([Float32Casting()], [Float32Casting()]),
     ([UInt8LinearScalingNormalization()], [UInt8LinearScalingNormalization()]),
     ([Float32Casting(), UInt8LinearScalingNormalization()], [Float32Casting(), UInt8LinearScalingNormalization()])]

parameters_reset_images = \
    [np.full(shape=(128, 128, 3),
             fill_value=(0, 1, 2),
             dtype=np.uint8)]
