from abc import ABC

import numpy as np
from numpy import typing as npt


class PreprocessingStrategy(ABC):

    @staticmethod
    def preprocess(image: npt.NDArray) -> npt.NDArray:
        """
        | Returns the preprocessed image.

        :param image: image
        :returns: preprocessed image
        """
        pass


class Float32Casting(PreprocessingStrategy):

    @staticmethod
    def preprocess(image: npt.NDArray) -> npt.NDArray[np.float32]:
        """
        | Returns the preprocessed image.
        | float32 casting is used to cast the values to float32.

        :param image: image
        :returns: preprocessed image
        """
        assert isinstance(image, np.ndarray)

        return image.astype(np.float32)

    def __repr__(self) -> str:
        """
        | Returns a representation of the object.

        :returns: representation
        """
        return f'{self.__class__.__name__}()'


class UInt8LinearScalingNormalization(PreprocessingStrategy):

    @staticmethod
    def preprocess(image: npt.NDArray[np.uint8]) -> npt.NDArray[np.float32]:
        """
        | Returns the preprocessed image.
        | uint8 linear scaling normalization is used to scale the values from their native range between 0 and 255
            into a standard range between 0 and 1.

        :param image: image
        :returns: preprocessed image
        """
        assert isinstance(image, np.ndarray)
        assert image.dtype == np.uint8

        return image.astype(np.float32) / 255.

    def __repr__(self) -> str:
        """
        | Returns a representation of the object.

        :returns: representation
        """
        return f'{self.__class__.__name__}()'
