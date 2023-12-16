from pathlib import Path  # noqa: F401 (used for type hinting)
from typing import Protocol

import numpy as np
import onnxruntime as ort


class ModelProtocol(Protocol):

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
        self._session = ort.InferenceSession(str(self.path))

    def run(self,
            image):
        """
        | Returns the mask.

        :param np.ndarray[np.float32] image: image
        :returns: mask
        :rtype: np.ndarray[np.uint8]
        """
        assert isinstance(image, np.ndarray)
        assert image.dtype == np.float32

        image = image[np.newaxis, ...]

        input_name = self._session.get_inputs()[0].name

        mask = np.array(self._session.run(None, {input_name: image}))
        mask = np.squeeze(mask)
        mask = np.argmax(mask, axis=-1).astype(np.uint8)
        return mask
