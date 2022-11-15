# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import numpy as np


class Preprocessor:
    @staticmethod
    def normalize_image(image):
        """
        | Returns a normalized image.

        :param np.ndarray[np.uint8] image: image
        :returns: normalized image
        :rtype: np.ndarray[np.float32]
        """
        image = image.astype(np.float32) / 255.
        return image

    def get_image(self,
                  rgb_image,
                  nir_image):
        """
        | Returns a normalized 4 channel image (r, g, b, nir).

        :param np.ndarray[np.uint8] rgb_image: rgb image
        :param np.ndarray[np.uint8] nir_image: nir image
        :returns: image
        :rtype: np.ndarray[np.float32]
        """
        nir_image = np.expand_dims(nir_image[..., 0], axis=-1)
        image = np.concatenate([rgb_image, nir_image], axis=-1)
        image = self.normalize_image(image)
        return image
