import numpy as np
from numpy import typing as npt

from .preprocessing_strategies import PreprocessingStrategy


class ImageBuilder:

    def __init__(self,
                 preprocessing_strategies: list[PreprocessingStrategy]) -> None:
        """
        :param preprocessing_strategies: preprocessing strategies
        """
        assert isinstance(preprocessing_strategies, list)

        conditions = [isinstance(preprocessing_strategy, PreprocessingStrategy)
                      for preprocessing_strategy in preprocessing_strategies]

        assert all(conditions)

        self._image_rgb = None
        self._image_nir = None
        self.preprocessing_strategies = preprocessing_strategies

    @property
    def image_rgb(self) -> npt.NDArray[np.uint8] | None:
        """
        | Returns the rgb image.

        :returns: rgb image
        """
        return self._image_rgb

    @image_rgb.setter
    def image_rgb(self,
                  image_rgb: npt.NDArray[np.uint8] | None) -> None:
        """
        | Sets the rgb image.

        :param image_rgb: rgb image
        """
        assert isinstance(image_rgb, np.ndarray) or image_rgb is None

        if image_rgb is not None:
            assert image_rgb.dtype == np.uint8
            assert image_rgb.ndim == 3
            assert image_rgb.shape[-1] == 3

        self._image_rgb = image_rgb

    @property
    def image_nir(self) -> npt.NDArray[np.uint8] | None:
        """
        | Returns the nir image.

        :returns: nir image
        """
        return self._image_nir

    @image_nir.setter
    def image_nir(self,
                  image_nir: npt.NDArray[np.uint8] | None) -> None:
        """
        | Sets the nir image.

        :param image_nir: nir image
        """
        assert isinstance(image_nir, np.ndarray) or image_nir is None

        if image_nir is not None:
            assert image_nir.dtype == np.uint8
            assert image_nir.ndim == 3
            assert image_nir.shape[-1] == 3

        if image_nir is not None:
            self._image_nir = image_nir[..., 0][..., np.newaxis]
        else:
            self._image_nir = image_nir

    def concatenate_images(self) -> npt.NDArray[np.uint8]:
        """
        | Returns the concatenated image.

        :returns: concatenated image
        """
        assert self.image_rgb is not None
        assert self.image_nir is not None

        image = np.concatenate((self.image_rgb, self.image_nir), axis=-1)
        return image

    def preprocess_image(self,
                         image: npt.NDArray[np.uint8]) -> npt.NDArray:
        """
        | Returns the preprocessed image.

        :param image: image
        :returns: preprocessed image
        """
        assert isinstance(image, np.ndarray)
        assert image.dtype == np.uint8

        for preprocessing_strategy in self.preprocessing_strategies:
            image = preprocessing_strategy.preprocess(image=image)

        return image

    def build_image(self,
                    reset: bool = True) -> npt.NDArray:
        """
        | Returns the built image.

        :param reset: if True, image_rgb and image_nir are set to None
        :returns: built image
        """
        assert self.image_rgb is not None
        assert self.image_nir is not None

        image = self.concatenate_images()
        image = self.preprocess_image(image=image)

        if reset:
            self.image_rgb = None
            self.image_nir = None

        return image

    def __repr__(self) -> str:
        representation = (
            f'{self.__class__.__name__}('
            f'image_rgb_type={type(self.image_rgb).__name__}, '
            f"image_rgb_dtype={getattr(self.image_rgb, 'dtype', None)}, "
            f"image_rgb_shape={getattr(self.image_rgb, 'shape', None)}, "
            f'image_nir_type={type(self.image_nir).__name__}, '
            f"image_nir_dtype={getattr(self.image_nir, 'dtype', None)}, "
            f"image_nir_shape={getattr(self.image_nir, 'shape', None)}, "
            f'preprocessing_strategies={self.preprocessing_strategies!r})')

        return representation
