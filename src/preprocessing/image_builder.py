import numpy as np

from src.preprocessing.preprocessing_strategies import PreprocessingStrategy


class ImageBuilder:
    def __init__(self, preprocessing_strategies):
        """
        | Initializer method

        :param list[PreprocessingStrategy] preprocessing_strategies: preprocessing strategies
        :returns: None
        :rtype: None
        """
        assert isinstance(preprocessing_strategies, list)
        assert all(isinstance(preprocessing_strategy, PreprocessingStrategy)
                   for preprocessing_strategy in preprocessing_strategies)

        self.image_rgb = None
        self.image_nir = None
        self.preprocessing_strategies = preprocessing_strategies

    def set_image_rgb(self, image_rgb):
        """
        | Sets the rgb image.

        :param np.ndarray[np.uint8] image_rgb: rgb image
        :returns: image builder
        :rtype: ImageBuilder
        """
        assert isinstance(image_rgb, np.ndarray)
        assert image_rgb.dtype == np.uint8
        assert len(image_rgb.shape) == 3
        assert image_rgb.shape[-1] == 3

        self.image_rgb = image_rgb
        return self

    def set_image_nir(self, image_nir):
        """
        | Sets the nir image.

        :param np.ndarray[np.uint8] image_nir: nir image
        :returns: image builder
        :rtype: ImageBuilder
        """
        assert isinstance(image_nir, np.ndarray)
        assert image_nir.dtype == np.uint8
        assert len(image_nir.shape) == 3
        assert image_nir.shape[-1] == 3

        self.image_nir = image_nir[..., 0][..., np.newaxis]
        return self

    def set_preprocessing_strategies(self, preprocessing_strategies):
        """
        | Sets the preprocessing strategies.

        :param list[PreprocessingStrategy] preprocessing_strategies: preprocessing strategies
        :returns: image builder
        :rtype: ImageBuilder
        """
        assert isinstance(preprocessing_strategies, list)
        assert all(isinstance(preprocessing_strategy, PreprocessingStrategy)
                   for preprocessing_strategy in preprocessing_strategies)

        self.preprocessing_strategies = preprocessing_strategies
        return self

    def reset_images(self):
        """
        | Resets the rgb image and the nir image.

        :returns: None
        :rtype: None
        """
        self.image_rgb = None
        self.image_nir = None

    def concatenate_images(self):
        """
        | Returns the concatenated image.

        :returns: concatenated image
        :rtype: np.ndarray[np.uint8]
        """
        assert self.image_rgb is not None
        assert self.image_nir is not None

        image = np.concatenate((self.image_rgb,
                                self.image_nir),
                               axis=-1)

        return image

    def preprocess_image(self, image):
        """
        | Returns the preprocessed image.

        :param np.ndarray[np.uint8] image: image
        :returns: preprocessed image
        :rtype: np.ndarray
        """
        assert isinstance(image, np.ndarray)
        assert image.dtype == np.uint8

        for preprocessing_strategy in self.preprocessing_strategies:
            image = preprocessing_strategy.preprocess(image=image)

        return image

    def build_image(self, reset=True):
        """
        | Returns the built image.

        :param bool reset: if True, image_rgb and image_nir are set to None
        :returns: built image
        :rtype: np.ndarray
        """
        assert self.image_rgb is not None
        assert self.image_nir is not None

        image = self.concatenate_images()
        image = self.preprocess_image(image=image)

        if reset:
            self.reset_images()

        return image

    def __repr__(self):
        """
        | Returns a representation of the object.

        :returns: representation
        :rtype: str
        """
        representation = (f'{self.__class__.__name__}('
                          + f'image_rgb_type={type(self.image_rgb).__name__}, '
                          + f"image_rgb_dtype={getattr(self.image_rgb, 'dtype', None)}, "
                          + f"image_rgb_shape={getattr(self.image_rgb, 'shape', None)}, "
                          + f'image_nir_type={type(self.image_nir).__name__}, '
                          + f"image_nir_dtype={getattr(self.image_nir, 'dtype', None)}, "
                          + f"image_nir_shape={getattr(self.image_nir, 'shape', None)}, "
                          + f'preprocessing_strategies={self.preprocessing_strategies!r})')

        return representation
