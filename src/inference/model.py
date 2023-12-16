from pathlib import Path  # noqa: F401 (used for type hinting)
from typing import Protocol

import numpy as np
import onnxruntime as ort


class Model(Protocol):

    def set_up(self):
        """
        | Sets up the model.

        :returns: None
        :rtype: None
        """
        ...

    def run(self,
            image):
        """
        | Returns the mask.

        :param np.ndarray[np.float32] image: image
        :returns: mask
        :rtype: np.ndarray[np.uint8]
        """
        ...


class ONNXModel:

    def __init__(self,
                 path):
        """
        | Initializer method

        :param Path path: path to the onnx model
        :returns: None
        :rtype: None
        """
        assert isinstance(path, Path)

        self.path = path
        self.session = None

    def set_up(self):
        """
        | Sets up the model.

        :returns: None
        :rtype: None
        """
        self.session = ort.InferenceSession(str(self.path))

    def run(self,
            image):
        """
        | Returns the mask.

        :param np.ndarray[np.float32] image: image
        :returns: mask
        :rtype: np.ndarray[np.uint8]
        """
        image = image[np.newaxis, ...]

        input_name = self.session.get_inputs()[0].name

        mask = np.array(self.session.run(None, {input_name: image}))
        mask = np.squeeze(mask)
        mask = np.argmax(mask, axis=-1).astype(np.uint8)
        return mask
