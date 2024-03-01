import numpy as np
from numpy import typing as npt

from src.utils.settings import (
    IMAGE_SIZE,
    IMAGE_SIZE_METERS,
    PADDING_SIZE,
    PADDING_SIZE_METERS)

from .web_map_service import WebMapServiceProtocol


class RemoteSensingDataFetcher:

    def __init__(self,
                 web_map_service: WebMapServiceProtocol,
                 layer: str,
                 epsg_code: int) -> None:
        """
        | Initializer method

        :param web_map_service: web map service
        :param layer: layer
        :param epsg_code: epsg code
        :returns: None
        """
        assert isinstance(layer, str)

        assert isinstance(epsg_code, int)

        self.web_map_service = web_map_service
        self.layer = layer
        self.epsg_code = epsg_code

    @staticmethod
    def compute_bounding_box(coordinates: tuple[int, int],
                             apply_padding: bool = False) -> tuple[int, int, int, int]:
        """
        | Returns the bounding box of a tile.

        :param coordinates: coordinates (x_min, y_max)
        :param apply_padding: if True, the bounding box is increased by PADDING_SIZE_METERS
        :returns: bounding box (x_min, y_min, x_max, y_max)
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
                    coordinates: tuple[int, int],
                    apply_padding: bool = False) -> npt.NDArray[np.uint8]:
        """
        | Returns the fetched image.

        :param coordinates: coordinates (x_min, y_max)
        :param apply_padding: if True, the image size is increased by PADDING_SIZE
        :returns: fetched image
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
