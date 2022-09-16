# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import numpy as np
import onnxruntime


class Inference:
    def __init__(self, model_path):
        """
        | Constructor method

        :param str model_path: path to the model (.onnx)
        :returns: None
        :rtype: None
        """
        self.model = onnxruntime.InferenceSession(model_path)
        self.model_input_name = self.model.get_inputs()[0].name

    def get_mask(self, image):
        """
        | Returns a mask with 2 dimensions and the following pixel values:
        | - 0: pervious surfaces
        | - 1: buildings
        | - 2: impervious surfaces

        :param np.ndarray[np.float32] image: image
        :returns: mask
        :rtype: np.ndarray[np.uint8]
        """
        model_input = np.expand_dims(image, axis=0)
        mask = self.model.run([], {self.model_input_name: model_input})
        mask = np.squeeze(mask)
        mask = np.argmax(mask, axis=-1).astype(np.uint8)
        return mask
