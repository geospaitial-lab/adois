from pathlib import Path
from typing import Protocol

import numpy as np
import onnxruntime as ort
from numpy import typing as npt


class ModelProtocol(Protocol):

    def run(self,
            image: npt.NDArray[np.float32]) -> npt.NDArray[np.uint8]:
        """
        | Returns the mask.

        :param image: image
        :returns: mask
        """
        ...


class ONNXModel:

    def __init__(self,
                 path: Path) -> None:
        """
        :param path: path to the onnx model
        """
        assert isinstance(path, Path)

        self.path = path
        self._session = ort.InferenceSession(str(self.path))

    def run(self,
            image: npt.NDArray[np.float32]) -> npt.NDArray[np.uint8]:
        """
        | Returns the mask.

        :param image: image
        :returns: mask
        """
        assert isinstance(image, np.ndarray)
        assert image.dtype == np.float32

        image = image[np.newaxis, ...]

        input_name = self._session.get_inputs()[0].name

        mask = np.array(self._session.run(None, {input_name: image}))
        mask = np.squeeze(mask)
        mask = np.argmax(mask, axis=-1).astype(np.uint8)
        return mask
