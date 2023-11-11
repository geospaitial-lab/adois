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
        return image.astype(np.float32) / 255.

    def get_image(self,
                  image_rgb,
                  image_nir):
        """
        | Returns a normalized 4 channel image (r, g, b, nir).

        :param np.ndarray[np.uint8] image_rgb: rgb image
        :param np.ndarray[np.uint8] image_nir: nir image
        :returns: image
        :rtype: np.ndarray[np.float32]
        """
        image_nir = image_nir[..., 0]

        image = np.concatenate((image_rgb,
                                image_nir[..., np.newaxis]),
                               axis=-1)

        image = self.normalize_image(image)
        return image
