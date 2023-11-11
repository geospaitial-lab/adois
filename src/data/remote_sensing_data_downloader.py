from io import BytesIO

import numpy as np
from PIL import Image
from owslib.wms import WebMapService

import src.utils.settings as settings


class RemoteSensingDataDownloader:
    def __init__(self,
                 wms_url,
                 wms_layer,
                 epsg_code,
                 clip_border):
        """
        | Constructor method

        :param str wms_url: url of the web map service
        :param str wms_layer: layer of the web map service
        :param int epsg_code: epsg code of the coordinate reference system
        :param bool clip_border: if True, the image size is increased by the border size
        :returns: None
        :rtype: None
        """
        self.wms = WebMapService(wms_url)
        self.wms_layer = wms_layer
        self.epsg_code = epsg_code
        self.clip_border = clip_border

    def get_bounding_box(self, coordinates):
        """
        | Returns the bounding box of a tile.

        :param (int, int) coordinates: coordinates (x_min, y_max)
        :returns: bounding_box (x_min, y_min, x_max, y_max)
        :rtype: (int, int, int, int)
        """
        x_min, y_max = coordinates

        if self.clip_border:
            bounding_box = (x_min - settings.BORDER_SIZE_METERS,
                            y_max - settings.IMAGE_SIZE_METERS - settings.BORDER_SIZE_METERS,
                            x_min + settings.IMAGE_SIZE_METERS + settings.BORDER_SIZE_METERS,
                            y_max + settings.BORDER_SIZE_METERS)
        else:
            bounding_box = (x_min,
                            y_max - settings.IMAGE_SIZE_METERS,
                            x_min + settings.IMAGE_SIZE_METERS,
                            y_max)

        return bounding_box

    def get_response(self, bounding_box):
        """
        | Wrapper of owslib.wms.WebMapService.getmap().read()
        | Returns a response (byte stream) of the web map service.

        :param (int, int, int, int) bounding_box: bounding_box (x_min, y_min, x_max, y_max)
        :returns: response
        :rtype: bytes
        """
        image_size = settings.IMAGE_SIZE + 2 * settings.BORDER_SIZE if self.clip_border else settings.IMAGE_SIZE

        response = self.wms.getmap(layers=[self.wms_layer],
                                   srs=f'EPSG:{self.epsg_code}',
                                   bbox=bounding_box,
                                   format='image/tiff',
                                   size=(image_size, image_size),
                                   bgcolor='#000000').read()

        return response

    def get_image(self, coordinates):
        """
        | Returns an image.

        :param (int, int) coordinates: coordinates (x_min, y_max)
        :returns: image
        :rtype: np.ndarray[np.uint8]
        """
        bounding_box = self.get_bounding_box(coordinates)
        response = self.get_response(bounding_box)

        with Image.open(BytesIO(response)) as file:
            # noinspection PyTypeChecker
            image = np.array(file, dtype=np.uint8)

        return image
