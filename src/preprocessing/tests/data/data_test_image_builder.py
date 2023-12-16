import numpy as np

data_test_getter_image_nir = (
    [np.full(shape=(128, 128, 1),
             fill_value=0,
             dtype=np.uint8),
     None])

data_test_getter_image_rgb = (
    [np.full(shape=(128, 128, 3),
             fill_value=(0, 1, 2),
             dtype=np.uint8),
     None])

data_test_init = (
    [[],
     ['mocked_preprocessing_strategy'],
     ['mocked_preprocessing_strategy', 'mocked_preprocessing_strategy']])

data_test_setter_image_nir = (
    [(np.full(shape=(128, 128, 3),
              fill_value=(0, 1, 2),
              dtype=np.uint8),
      np.full(shape=(128, 128, 1),
              fill_value=0,
              dtype=np.uint8)),
     (None, None)])

data_test_setter_image_rgb = (
    [(np.full(shape=(128, 128, 3),
              fill_value=(0, 1, 2),
              dtype=np.uint8),
      np.full(shape=(128, 128, 3),
              fill_value=(0, 1, 2),
              dtype=np.uint8)),
     (None, None)])
