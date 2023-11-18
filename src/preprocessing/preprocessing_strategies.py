from abc import ABC, abstractmethod

import numpy as np


class PreprocessingStrategy(ABC):
    @abstractmethod
    def preprocess(self, image):
        """
        | Returns the preprocessed image.

        :param np.ndarray image: image
        :returns: preprocessed image
        :rtype: np.ndarray
        """
        pass


class Float32Casting(PreprocessingStrategy):
    def preprocess(self, image):
        """
        | Returns the preprocessed image.
        | float32 casting is used to cast the values to float32.

        :param np.ndarray image: image
        :returns: preprocessed image
        :rtype: np.ndarray[np.float32]
        """
        assert isinstance(image, np.ndarray)

        return image.astype(np.float32)

    def __repr__(self):
        """
        | Returns a representation of the object.

        :returns: representation
        :rtype: str
        """
        return f'{self.__class__.__name__}()'


class UInt8LinearScalingNormalization(PreprocessingStrategy):
    def preprocess(self, image):
        """
        | Returns the preprocessed image.
        | uint8 linear scaling normalization is used to scale the values from their natural range between 0 and 255
            into a standard range between 0 and 1.

        :param np.ndarray[np.uint8] image: image
        :returns: preprocessed image
        :rtype: np.ndarray[np.float32]
        """
        assert isinstance(image, np.ndarray)
        assert image.dtype == np.uint8

        return image.astype(np.float32) / 255.

    def __repr__(self):
        """
        | Returns a representation of the object.

        :returns: representation
        :rtype: str
        """
        return f'{self.__class__.__name__}()'
