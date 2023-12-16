import numpy as np

from src.utils.settings import IMAGE_SIZE, PADDING_SIZE
from .model import Model  # noqa: F401 (used for type hinting)


class Inference:

    def __init__(self,
                 model):
        """
        | Initializer method

        :param Model model: model
        :returns: None
        :rtype: None
        """
        self.model = model

    @staticmethod
    def remove_padding(mask):
        """
        | Returns the mask without padding.

        :param np.ndarray[np.uint8] mask: mask
        :returns: mask without padding
        :rtype: np.ndarray[np.uint8]
        """
        assert isinstance(mask, np.ndarray)
        assert mask.dtype == np.uint8
        assert mask.ndim == 2
        assert mask.shape == (IMAGE_SIZE + PADDING_SIZE, IMAGE_SIZE + PADDING_SIZE)

        return np.array(mask[PADDING_SIZE:-PADDING_SIZE, PADDING_SIZE:-PADDING_SIZE])

    def predict_mask(self,
                     image,
                     apply_padding=False):
        """
        | Returns the mask.

        :param np.ndarray[np.float32] image: image
        :param bool apply_padding: if True, the padding of the mask is removed
        :returns: mask
        :rtype: np.ndarray[np.uint8]
        """
        assert isinstance(image, np.ndarray)
        assert image.dtype == np.float32
        assert image.ndim == 3

        if apply_padding:
            assert image.shape == (IMAGE_SIZE + PADDING_SIZE, IMAGE_SIZE + PADDING_SIZE, 4)
        else:
            assert image.shape == (IMAGE_SIZE, IMAGE_SIZE, 4)

        mask = self.model.run(image=image)

        if apply_padding:
            mask = Inference.remove_padding(mask)

        return mask
