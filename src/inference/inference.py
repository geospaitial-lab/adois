from pathlib import Path

import numpy as np
import onnxruntime

import src.utils.settings as settings


class Inference:
    def __init__(self,
                 model_path,
                 clip_border):
        """
        | Constructor method

        :param str or Path model_path: path to the onnx model
        :param bool clip_border: if True, the mask is clipped
        :returns: None
        :rtype: None
        """
        assert isinstance(model_path, str) or isinstance(model_path, Path)

        assert isinstance(clip_border, bool)

        self.model = onnxruntime.InferenceSession(str(model_path))
        self.model_input_name = self.model.get_inputs()[0].name
        self.clip_border = clip_border

    @staticmethod
    def clip_mask(mask):
        """
        | Returns a clipped mask.

        :param np.ndarray[np.uint8] mask: mask
        :returns: clipped mask
        :rtype: np.ndarray[np.uint8]
        """
        assert isinstance(mask, np.ndarray) and mask.dtype == np.uint8
        assert len(mask.shape) == 2

        assert mask.shape == (settings.IMAGE_SIZE + settings.BORDER_SIZE,
                              settings.IMAGE_SIZE + settings.BORDER_SIZE)

        return np.array(mask[settings.BORDER_SIZE:-settings.BORDER_SIZE, settings.BORDER_SIZE:-settings.BORDER_SIZE])

    def get_mask(self, image):
        """
        | Returns a mask with 2 dimensions and the following pixel values:
        | 0: pervious surface
        | 1: building
        | 2: pavement

        :param np.ndarray[np.float32] image: image
        :returns: mask
        :rtype: np.ndarray[np.uint8]
        """
        assert isinstance(image, np.ndarray) and image.dtype == np.float32
        assert len(image.shape) == 3

        if self.clip_border:
            assert image.shape == (settings.IMAGE_SIZE + settings.BORDER_SIZE,
                                   settings.IMAGE_SIZE + settings.BORDER_SIZE,
                                   4)
        else:
            assert image.shape == (settings.IMAGE_SIZE,
                                   settings.IMAGE_SIZE,
                                   4)

        model_input = image[np.newaxis, ...]
        mask = np.array(self.model.run([], {self.model_input_name: model_input}))
        mask = np.squeeze(mask)
        mask = np.argmax(mask, axis=-1).astype(np.uint8)

        if self.clip_border:
            mask = self.clip_mask(mask)

        return mask
