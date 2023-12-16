from io import BytesIO
from typing import Protocol

import numpy as np
import owslib.wms
from PIL import Image

from .exceptions import WMSConnectionError, WMSFetchingError


class WebMapServiceProtocol(Protocol):

    def get_layers(self):
        """
        | Returns the layers.

        :returns: layers
        :rtype: list[str]
        """
        ...

    def get_epsg_codes(self,
                       layer):
        """
        | Returns the epsg codes.

        :param str layer: layer
        :returns: epsg codes
        :rtype: list[int]
        """
        ...

    def fetch_image(self,
                    layer,
                    bounding_box,
                    image_size,
                    epsg_code):
        """
        | Returns the fetched image.

        :param str layer: layer
        :param (int, int, int, int) bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :param int image_size: image size in pixels
        :param int epsg_code: epsg code
        :returns: fetched image
        :rtype: np.ndarray[np.uint8]
        :raises WMSFetchingError: if an exception is raised while fetching the image
        """
        ...


class WebMapService:

    def __init__(self,
                 url):
        """
        | Initializer method

        :param str url: url
        :returns: None
        :rtype: None
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

    def get_layers(self):
        """
        | Returns the layers.

        :returns: layers
        :rtype: list[str]
        """
        return [*self._session.contents]

    def get_epsg_codes(self,
                       layer):
        """
        | Returns the epsg codes.

        :param str layer: layer
        :returns: epsg codes
        :rtype: list[int]
        """
        assert isinstance(layer, str)

        return [int(epsg_code[5:]) for epsg_code in self._session[layer].crsOptions]

    def fetch_image(self,
                    layer,
                    bounding_box,
                    image_size,
                    epsg_code):
        """
        | Returns the fetched image.

        :param str layer: layer
        :param (int, int, int, int) bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :param int image_size: image size in pixels
        :param int epsg_code: epsg code
        :returns: fetched image
        :rtype: np.ndarray[np.uint8]
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
