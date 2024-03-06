from io import BytesIO
from typing import Protocol

import numpy as np
import owslib.wms
from numpy import typing as npt
from PIL import Image

from .exceptions import WMSConnectionError, WMSFetchingError


class WebMapServiceProtocol(Protocol):
    url: str

    def get_layers(self) -> list[str]:
        """
        | Returns the layers.

        :returns: layers
        """
        ...

    def get_epsg_codes(self,
                       layer: str) -> list[int]:
        """
        | Returns the epsg codes.

        :param layer: layer
        :returns: epsg codes
        """
        ...

    def fetch_image(self,
                    layer: str,
                    bounding_box: tuple[int, int, int, int],
                    image_size: int,
                    epsg_code: int) -> npt.NDArray[np.uint8]:
        """
        | Returns the fetched image.

        :param layer: layer
        :param bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :param image_size: image size in pixels
        :param epsg_code: epsg code
        :returns: fetched image
        :raises WMSFetchingError: if an exception is raised while fetching the image
        """
        ...


class WebMapService:

    def __init__(self,
                 url: str) -> None:
        """
        :param url: url
        :raises WMSConnectionError: if an exception is raised while connecting to the web map service
        """
        assert isinstance(url, str)

        self.url = url

        try:
            self._session = owslib.wms.WebMapService(url=self.url,
                                                     version='1.1.1')

        except Exception as e:
            raise WMSConnectionError(url=self.url,
                                     passed_exception=e)

    def get_layers(self) -> list[str]:
        """
        | Returns the layers.

        :returns: layers
        """
        return [*self._session.contents]

    def get_epsg_codes(self,
                       layer: str) -> list[int]:
        """
        | Returns the epsg codes.

        :param layer: layer
        :returns: epsg codes
        """
        assert isinstance(layer, str)

        return [int(epsg_code[5:]) for epsg_code in self._session[layer].crsOptions]

    def fetch_image(self,
                    layer: str,
                    bounding_box: tuple[int, int, int, int],
                    image_size: int,
                    epsg_code: int) -> npt.NDArray[np.uint8]:
        """
        | Returns the fetched image.

        :param layer: layer
        :param bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :param image_size: image size in pixels
        :param epsg_code: epsg code
        :returns: fetched image
        :raises WMSFetchingError: if an exception is raised while fetching the image
        """
        assert isinstance(layer, str)

        assert isinstance(bounding_box, tuple)
        assert len(bounding_box) == 4
        assert all(isinstance(coordinate, int) for coordinate in bounding_box)
        assert bounding_box[0] < bounding_box[2] and bounding_box[1] < bounding_box[3]

        assert isinstance(image_size, int)

        assert isinstance(epsg_code, int)

        try:
            data = self._session.getmap(layers=[layer],
                                        srs=f'EPSG:{epsg_code}',
                                        bbox=bounding_box,
                                        format='image/tiff',
                                        size=(image_size, image_size),
                                        bgcolor='#000000').read()

        except Exception as e:
            raise WMSFetchingError(url=self.url,
                                   passed_exception=e)

        with Image.open(BytesIO(data)) as file:
            image = np.array(file, dtype=np.uint8)

        return image
