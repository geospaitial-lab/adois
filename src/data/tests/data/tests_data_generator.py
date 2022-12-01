# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import numpy as np
from PIL import Image


image_top_left = np.full(shape=(640, 640, 3),
                         fill_value=np.array([0, 51, 102]),
                         dtype=np.uint8)
image_top_right = np.full(shape=(640, 640, 3),
                          fill_value=np.array([153, 204, 255]),
                          dtype=np.uint8)
image_bottom_left = np.full(shape=(640, 640, 3),
                            fill_value=np.array([255, 204, 153]),
                            dtype=np.uint8)
image_bottom_right = np.full(shape=(640, 640, 3),
                             fill_value=np.array([102, 51, 0]),
                             dtype=np.uint8)

image_top = np.concatenate((image_top_left, image_top_right), axis=1)
image_bottom = np.concatenate((image_bottom_left, image_bottom_right), axis=1)
expected = np.concatenate((image_top, image_bottom), axis=0)

Image.fromarray(expected).save('data_test_get_image.tiff')
