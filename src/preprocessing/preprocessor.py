# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import numpy as np
from PIL import Image

import src.utils as utils


class Preprocessor:
    def __init__(self, color_codes):
        """Constructor method

        :param dict[tuple[int, int, int], int] color_codes: color codes for the color mapping to reduce the
            dimensions of an image from 3 dimensions to 2 dimensions (the key of the dictionary is the rgb value
            and the value of the dictionary is the corresponding mapped value)
        :returns: None
        :rtype: None
        """
        self.color_map = self.get_color_map(color_codes)

    @staticmethod
    def get_color_map(color_codes):
        """Returns a color map.
        Based on: https://stackoverflow.com/a/33196320

        :param dict[tuple[int, int, int], int] color_codes: color codes for the color mapping to reduce the
            dimensions of an image from 3 dimensions to 2 dimensions (the key of the dictionary is the rgb value
            and the value of the dictionary is the corresponding mapped value)
        :returns: color map
        :rtype: np.ndarray[np.uint8]
        """
        color_map = np.full(shape=(256 ** 3),
                            fill_value=0,
                            dtype=np.int32)
        for rgb_value, mapped_value in color_codes.items():
            rgb = rgb_value[0] * 65536 + rgb_value[1] * 256 + rgb_value[2]
            color_map[rgb] = mapped_value
        return color_map

    @staticmethod
    def resize_image(image):
        """Returns a resized image. Used for manually upsampling or downsampling images to an image size without
        interpolation artefacts (nearest-neighbor interpolation is used).

        :param np.ndarray[np.uint8] image: image
        :returns: resized image
        :rtype: np.ndarray[np.uint8]
        """
        resized_image = Image.fromarray(image).resize(size=(utils.IMAGE_SIZE, utils.IMAGE_SIZE),
                                                      resample=Image.NEAREST)
        # noinspection PyTypeChecker
        resized_image = np.array(resized_image, dtype=np.uint8)
        return resized_image

    def reduce_dimensions(self, image):
        """Returns a color mapped image with reduced dimensions (2 dimensions instead of 3 dimensions).
        Based on: https://stackoverflow.com/a/33196320

        :param np.ndarray[np.uint8] image: image
        :returns: color mapped image
        :rtype: np.ndarray[np.uint8]
        """
        image = np.dot(image, np.array([65536, 256, 1], dtype=np.int32))
        image = self.color_map[image].astype(np.uint8)
        return image

    @staticmethod
    def normalize_image(image):
        """Returns a normalized image.

        :param np.ndarray[np.uint8] image: image
        :returns: normalized image
        :rtype: np.ndarray[np.float32]
        """
        image = image.astype(np.float32) / 255.
        return image

    def get_image(self,
                  rgb_image,
                  nir_image,
                  ndsm_image):
        """Returns a normalized 5 channel image (r, g, b, nir, ndsm).

        :param np.ndarray[np.uint8] rgb_image: rgb image
        :param np.ndarray[np.uint8] nir_image: nir image
        :param np.ndarray[np.uint8] ndsm_image: ndsm image
        :returns: image
        :rtype: np.ndarray[np.float32]
        """
        nir_image = np.expand_dims(nir_image[..., 0], axis=-1)
        ndsm_image = self.resize_image(ndsm_image)
        ndsm_image = self.reduce_dimensions(ndsm_image)
        ndsm_image = np.expand_dims(ndsm_image, axis=-1)

        image = np.concatenate([rgb_image, nir_image, ndsm_image], axis=-1)
        image = self.normalize_image(image)
        return image
