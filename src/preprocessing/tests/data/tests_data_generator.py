# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

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

normalized_image_top_left = np.full(shape=(640, 640, 4),
                                    fill_value=np.array([0., .2, .4, .6]),
                                    dtype=np.float32)
normalized_image_top_right = np.full(shape=(640, 640, 4),
                                     fill_value=np.array([.4, .6, .8, 1.]),
                                     dtype=np.float32)
normalized_image_bottom_left = np.full(shape=(640, 640, 4),
                                       fill_value=np.array([1., .8, .6, .4]),
                                       dtype=np.float32)
normalized_image_bottom_right = np.full(shape=(640, 640, 4),
                                        fill_value=np.array([.6, .4, .2, 0.]),
                                        dtype=np.float32)

normalized_image_top = np.concatenate((normalized_image_top_left, normalized_image_top_right), axis=1)
normalized_image_bottom = np.concatenate((normalized_image_bottom_left, normalized_image_bottom_right), axis=1)
expected = np.concatenate((normalized_image_top, normalized_image_bottom), axis=0)

np.save('data_test_normalize_image_test_input', test_input)
np.save('data_test_normalize_image_expected', expected)
# endregion

# region get_image()
rgb_image_top_left = np.full(shape=(640, 640, 3),
                             fill_value=np.array([0, 51, 102]),
                             dtype=np.uint8)
rgb_image_top_right = np.full(shape=(640, 640, 3),
                              fill_value=np.array([153, 204, 255]),
                              dtype=np.uint8)
rgb_image_bottom_left = np.full(shape=(640, 640, 3),
                                fill_value=np.array([255, 204, 153]),
                                dtype=np.uint8)
rgb_image_bottom_right = np.full(shape=(640, 640, 3),
                                 fill_value=np.array([102, 51, 0]),
                                 dtype=np.uint8)

rgb_image_top = np.concatenate((rgb_image_top_left, rgb_image_top_right), axis=1)
rgb_image_bottom = np.concatenate((rgb_image_bottom_left, rgb_image_bottom_right), axis=1)
test_input_rgb = np.concatenate((rgb_image_top, rgb_image_bottom), axis=0)

nir_image_top_left = np.full(shape=(640, 640, 3),
                             fill_value=0,
                             dtype=np.uint8)
nir_image_top_right = np.full(shape=(640, 640, 3),
                              fill_value=102,
                              dtype=np.uint8)
nir_image_bottom_left = np.full(shape=(640, 640, 3),
                                fill_value=153,
                                dtype=np.uint8)
nir_image_bottom_right = np.full(shape=(640, 640, 3),
                                 fill_value=255,
                                 dtype=np.uint8)

nir_image_top = np.concatenate((nir_image_top_left, nir_image_top_right), axis=1)
nir_image_bottom = np.concatenate((nir_image_bottom_left, nir_image_bottom_right), axis=1)
test_input_nir = np.concatenate((nir_image_top, nir_image_bottom), axis=0)

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
