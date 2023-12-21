import numpy as np
from numpy import typing as npt

from src.utils.settings import IMAGE_SIZE, PADDING_SIZE
from .model import ModelProtocol


class Inference:

    def __init__(self,
                 model: ModelProtocol) -> None:
        """
        | Initializer method

        :param model: model
        :returns: None
        """
        self.model = model

    @staticmethod
    def remove_padding(mask: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
        """
        | Returns the mask without padding.

        :param mask: mask
        :returns: mask without padding
        """
        assert isinstance(mask, np.ndarray)
        assert mask.dtype == np.uint8
        assert mask.ndim == 2
        assert mask.shape == (IMAGE_SIZE + PADDING_SIZE, IMAGE_SIZE + PADDING_SIZE)

        return np.array(mask[PADDING_SIZE:-PADDING_SIZE, PADDING_SIZE:-PADDING_SIZE])

    def predict_mask(self,
                     image: npt.NDArray[np.float32],
                     apply_padding: bool = False) -> npt.NDArray[np.uint8]:
        """
        | Returns the mask.

        :param image: image
        :param apply_padding: if True, the padding of the mask is removed
        :returns: mask
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
