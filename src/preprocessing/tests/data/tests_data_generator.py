import numpy as np


# region normalize_image()
image_top_left = np.full(shape=(640, 640, 4),
                         fill_value=np.array([0, 51, 102, 153]),
                         dtype=np.uint8)
image_top_right = np.full(shape=(640, 640, 4),
                          fill_value=np.array([102, 153, 204, 255]),
                          dtype=np.uint8)
image_bottom_left = np.full(shape=(640, 640, 4),
                            fill_value=np.array([255, 204, 153, 102]),
                            dtype=np.uint8)
image_bottom_right = np.full(shape=(640, 640, 4),
                             fill_value=np.array([153, 102, 51, 0]),
                             dtype=np.uint8)

image_top = np.concatenate((image_top_left, image_top_right), axis=1)
image_bottom = np.concatenate((image_bottom_left, image_bottom_right), axis=1)
test_input = np.concatenate((image_top, image_bottom), axis=0)

image_normalized_top_left = np.full(shape=(640, 640, 4),
                                    fill_value=np.array([0., .2, .4, .6]),
                                    dtype=np.float32)
image_normalized_top_right = np.full(shape=(640, 640, 4),
                                     fill_value=np.array([.4, .6, .8, 1.]),
                                     dtype=np.float32)
image_normalized_bottom_left = np.full(shape=(640, 640, 4),
                                       fill_value=np.array([1., .8, .6, .4]),
                                       dtype=np.float32)
image_normalized_bottom_right = np.full(shape=(640, 640, 4),
                                        fill_value=np.array([.6, .4, .2, 0.]),
                                        dtype=np.float32)

image_normalized_top = np.concatenate((image_normalized_top_left, image_normalized_top_right), axis=1)
image_normalized_bottom = np.concatenate((image_normalized_bottom_left, image_normalized_bottom_right), axis=1)
expected = np.concatenate((image_normalized_top, image_normalized_bottom), axis=0)

np.save('data_test_normalize_image_test_input', test_input)
np.save('data_test_normalize_image_expected', expected)
# endregion

# region get_image()
image_rgb_top_left = np.full(shape=(640, 640, 3),
                             fill_value=np.array([0, 51, 102]),
                             dtype=np.uint8)
image_rgb_top_right = np.full(shape=(640, 640, 3),
                              fill_value=np.array([153, 204, 255]),
                              dtype=np.uint8)
image_rgb_bottom_left = np.full(shape=(640, 640, 3),
                                fill_value=np.array([255, 204, 153]),
                                dtype=np.uint8)
image_rgb_bottom_right = np.full(shape=(640, 640, 3),
                                 fill_value=np.array([102, 51, 0]),
                                 dtype=np.uint8)

image_rgb_top = np.concatenate((image_rgb_top_left, image_rgb_top_right), axis=1)
image_rgb_bottom = np.concatenate((image_rgb_bottom_left, image_rgb_bottom_right), axis=1)
test_input_rgb = np.concatenate((image_rgb_top, image_rgb_bottom), axis=0)

image_nir_top_left = np.full(shape=(640, 640, 3),
                             fill_value=0,
                             dtype=np.uint8)
image_nir_top_right = np.full(shape=(640, 640, 3),
                              fill_value=102,
                              dtype=np.uint8)
image_nir_bottom_left = np.full(shape=(640, 640, 3),
                                fill_value=153,
                                dtype=np.uint8)
image_nir_bottom_right = np.full(shape=(640, 640, 3),
                                 fill_value=255,
                                 dtype=np.uint8)

image_nir_top = np.concatenate((image_nir_top_left, image_nir_top_right), axis=1)
image_nir_bottom = np.concatenate((image_nir_bottom_left, image_nir_bottom_right), axis=1)
test_input_nir = np.concatenate((image_nir_top, image_nir_bottom), axis=0)

image_top_left = np.full(shape=(640, 640, 4),
                         fill_value=np.array([0., .2, .4, 0.]),
                         dtype=np.float32)
image_top_right = np.full(shape=(640, 640, 4),
                          fill_value=np.array([.6, .8, 1., .4]),
                          dtype=np.float32)
image_bottom_left = np.full(shape=(640, 640, 4),
                            fill_value=np.array([1., .8, .6, .6]),
                            dtype=np.float32)
image_bottom_right = np.full(shape=(640, 640, 4),
                             fill_value=np.array([.4, .2, 0., 1.]),
                             dtype=np.float32)

image_top = np.concatenate((image_top_left, image_top_right), axis=1)
image_bottom = np.concatenate((image_bottom_left, image_bottom_right), axis=1)
expected = np.concatenate((image_top, image_bottom), axis=0)

np.save('data_test_get_image_test_input_rgb', test_input_rgb)
np.save('data_test_get_image_test_input_nir', test_input_nir)
np.save('data_test_get_image_expected', expected)
# endregion
