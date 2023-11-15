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
        assert isinstance(image, np.ndarray) and image.dtype == np.uint8

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
        assert isinstance(image_rgb, np.ndarray) and image_rgb.dtype == np.uint8
        assert len(image_rgb.shape) == 3
        assert image_rgb.shape[-1] == 3

        assert isinstance(image_nir, np.ndarray) and image_nir.dtype == np.uint8
        assert len(image_nir.shape) == 3
        assert image_nir.shape[-1] == 3

        image_nir = image_nir[..., 0]

        image = np.concatenate((image_rgb,
                                image_nir[..., np.newaxis]),
                               axis=-1)

        image = self.normalize_image(image)
        return image
