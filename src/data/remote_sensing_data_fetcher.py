import numpy as np  # noqa: F401 (used for type hinting)

from src.utils.settings import (
    IMAGE_SIZE,
    IMAGE_SIZE_METERS,
    PADDING_SIZE,
    PADDING_SIZE_METERS)

from .web_map_service import WebMapServiceProtocol  # noqa: F401 (used for type hinting)


class RemoteSensingDataFetcher:

    def __init__(self,
                 web_map_service,
                 layer,
                 epsg_code):
        """
        | Initializer method

        :param WebMapServiceProtocol web_map_service: web map service
        :param str layer: layer
        :param int epsg_code: epsg code
        :returns: None
        :rtype: None
        """
        assert isinstance(layer, str)

        assert isinstance(epsg_code, int)

        self.web_map_service = web_map_service
        self.layer = layer
        self.epsg_code = epsg_code

    @staticmethod
    def compute_bounding_box(coordinates,
                             apply_padding=False):
        """
        | Returns the bounding box of a tile.

        :param (int, int) coordinates: coordinates (x_min, y_max)
        :param bool apply_padding: if True, the bounding box is increased by PADDING_SIZE_METERS
        :returns: bounding box (x_min, y_min, x_max, y_max)
        :rtype: (int, int, int, int)
        """
        assert isinstance(coordinates, tuple)
        assert len(coordinates) == 2
        assert all(isinstance(coordinate, int) for coordinate in coordinates)

        assert isinstance(apply_padding, bool)

        x_min, y_max = coordinates

        if apply_padding:
            bounding_box = (
                (x_min - PADDING_SIZE_METERS,
                 y_max - IMAGE_SIZE_METERS - PADDING_SIZE_METERS,
                 x_min + IMAGE_SIZE_METERS + PADDING_SIZE_METERS,
                 y_max + PADDING_SIZE_METERS))

        else:
            bounding_box = (
                (x_min,
                 y_max - IMAGE_SIZE_METERS,
                 x_min + IMAGE_SIZE_METERS,
                 y_max))

        return bounding_box

    def fetch_image(self,
                    coordinates,
                    apply_padding=False):
        """
        | Returns the fetched image.

        :param (int, int) coordinates: coordinates (x_min, y_max)
        :param bool apply_padding: if True, the image size is increased by PADDING_SIZE
        :returns: fetched image
        :rtype: np.ndarray[np.uint8]
        """
        assert isinstance(coordinates, tuple)
        assert len(coordinates) == 2
        assert all(isinstance(coordinate, int) for coordinate in coordinates)

        assert isinstance(apply_padding, bool)

        bounding_box = self.compute_bounding_box(coordinates=coordinates,
                                                 apply_padding=apply_padding)

        if apply_padding:
            image_size = IMAGE_SIZE + 2 * PADDING_SIZE
        else:
            image_size = IMAGE_SIZE

        image = self.web_map_service.fetch_image(layer=self.layer,
                                                 bounding_box=bounding_box,
                                                 image_size=image_size,
                                                 epsg_code=self.epsg_code)

        return image
