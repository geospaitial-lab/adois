from io import BytesIO

import numpy as np
from PIL import Image
from owslib.wms import WebMapService

import src.utils as utils


class RemoteSensingDataDownloader:
    def __init__(self,
                 wms_url,
                 wms_layer,
                 epsg_code):
        """
        | Constructor method

        :param str wms_url: url of the web map service
        :param str wms_layer: layer of the web map service
        :param int epsg_code: epsg code of the coordinate reference system
        :returns: None
        :rtype: None
        """
        self.wms = WebMapService(wms_url)
        self.wms_layer = wms_layer
        self.epsg_code = epsg_code

    @staticmethod
    def get_bounding_box(coordinates):
        """
        | Returns the bounding box of a tile given its coordinates of the top left corner.

        :param (int, int) coordinates: coordinates (x, y)
        :returns: bounding_box (x_1, y_1, x_2, y_2)
        :rtype: (int, int, int, int)
        """
        bounding_box = (coordinates[0],
                        coordinates[1] - utils.IMAGE_SIZE_METERS,
                        coordinates[0] + utils.IMAGE_SIZE_METERS,
                        coordinates[1])
        return bounding_box

    def get_response(self, bounding_box):
        """
        | Wrapper of owslib.wms.WebMapService.getmap().read()
        | Returns a response (byte stream) of the web map service given its bounding box.

        :param (int, int, int, int) bounding_box: bounding_box (x_1, y_1, x_2, y_2)
        :returns: response
        :rtype: bytes
        """
        response = self.wms.getmap(layers=[self.wms_layer],
                                   srs=f'EPSG:{self.epsg_code}',
                                   bbox=bounding_box,
                                   format='image/tiff',
                                   size=(utils.IMAGE_SIZE, utils.IMAGE_SIZE),
                                   bgcolor='#000000').read()
        return response

    def get_image(self, coordinates):
        """
        | Returns an image given its coordinates of the top left corner.

        :param (int, int) coordinates: coordinates (x, y)
        :returns: image
        :rtype: np.ndarray[np.uint8]
        """
        bounding_box = self.get_bounding_box(coordinates)
        response = self.get_response(bounding_box)

        with Image.open(BytesIO(response)) as file:
            # noinspection PyTypeChecker
            image = np.array(file, dtype=np.uint8)

        return image
