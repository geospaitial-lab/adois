# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from io import BytesIO

import numpy as np
from PIL import Image
from owslib.wms import WebMapService

import src.utils as utils


class RemoteSensingDataDownloader:
    def __init__(self,
                 wms_url,
                 wms_layer,
                 epsg_code,
                 image_size):
        """Constructor method

        :param str wms_url: url of the web map service
        :param str wms_layer: layer of the web map service
        :param int epsg_code: epsg code of the coordinate reference system
        :param int image_size: image size in pixels
        :returns: None
        :rtype: None
        """
        self.wms = WebMapService(wms_url)
        self.wms_layer = wms_layer
        self.epsg_code = epsg_code
        self.image_size = image_size
        self.image_size_meters = self.image_size * utils.RESOLUTION

    def get_bounding_box(self, coordinates):
        """Returns the bounding box of a tile given its coordinates of the top left corner.

        :param (float, float) coordinates: coordinates (x, y)
        :returns: bounding_box
        :rtype: (float, float, float, float)
        """
        bounding_box = (coordinates[0],
                        coordinates[1] - self.image_size_meters,
                        coordinates[0] + self.image_size_meters,
                        coordinates[1])
        return bounding_box

    def get_image(self, coordinates):
        """Returns an image given its coordinates of the top left corner.

        :param (float, float) coordinates: coordinates (x, y)
        :returns: image
        :rtype: np.ndarray[np.uint8]
        """
        bounding_box = self.get_bounding_box(coordinates)
        response = self.wms.getmap(layers=[self.wms_layer],
                                   srs=f'EPSG:{self.epsg_code}',
                                   bbox=bounding_box,
                                   format='image/tiff',
                                   size=(self.image_size, self.image_size),
                                   bgcolor='#000000')
        with Image.open(BytesIO(response.read())) as file:
            # noinspection PyTypeChecker
            image = np.array(file, dtype=np.uint8)
        return image