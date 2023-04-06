import numpy as np
import onnxruntime

import src.utils.settings as settings


class Inference:
    def __init__(self,
                 model_path,
                 clip_border):
        """
        | Constructor method

        :param str model_path: path to the model (.onnx)
        :param bool clip_border: if True, the mask is clipped
        :returns: None
        :rtype: None
        """
        self.model = onnxruntime.InferenceSession(model_path)
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
        model_input = np.expand_dims(image, axis=0)
        mask = np.array(self.model.run([], {self.model_input_name: model_input}))
        mask = np.squeeze(mask)
        mask = np.argmax(mask, axis=-1).astype(np.uint8)

        if self.clip_border:
            mask = self.clip_mask(mask)
        return mask
