# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from natsort import natsorted

import src.utils as utils


class WMSConnectionError(Exception):
    def __init__(self,
                 wms_url,
                 passed_exception):
        """Constructor method

        :param str wms_url: url of the web map service
        :param Exception passed_exception: passed exception
        :returns: None
        :rtype: None
        """
        message = (f'No connection to WMS ({wms_url}) in config_file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   f'{passed_exception}')
        super().__init__(message)


class WMSLayerError(Exception):
    def __init__(self,
                 wms_layer,
                 wms_url,
                 valid_wms_layers):
        """Constructor method

        :param str wms_layer: layer of the web map service
        :param str wms_url: url of the web map service
        :param list[str] valid_wms_layers: valid layers
        :returns: None
        :rtype: None
        """
        valid_wms_layers = natsorted(valid_wms_layers)
        if len(valid_wms_layers) == 1:
            valid_wms_layers = valid_wms_layers[0]
        else:
            valid_wms_layers = (f"{', '.join(map(str, valid_wms_layers[:-1]))} "
                                f'or {valid_wms_layers[-1]}')
        message = (f'Invalid wms_layer of WMS ({wms_url}) in config file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   f'Expected {valid_wms_layers}, '
                   f'got {wms_layer} instead.')
        super().__init__(message)


class EPSGCodeError(Exception):
    def __init__(self,
                 epsg_code,
                 valid_epsg_codes):
        """Constructor method

        :param int epsg_code: epsg code of the coordinate reference system
        :param list[int] valid_epsg_codes: valid epsg codes
        :returns: None
        :rtype: None
        """
        valid_epsg_codes = natsorted(valid_epsg_codes)
        if len(valid_epsg_codes) == 1:
            valid_epsg_codes = valid_epsg_codes[0]
        else:
            valid_epsg_codes = (f"{', '.join(map(str, valid_epsg_codes[:-1]))} "
                                f'or {valid_epsg_codes[-1]}')
        message = ('Invalid epsg_code in config file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   f'Expected {valid_epsg_codes}, '
                   f'got {epsg_code} instead.')
        super().__init__(message)


class ImageSizeError(Exception):
    def __init__(self, image_size):
        """Constructor method

        :param int image_size: image size in pixels
        :returns: None
        :rtype: None
        """
        message = ('Invalid image_size in config file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   f'Expected an even number in the range of 512 to 2560, got {image_size} instead.')
        super().__init__(message)


class BoundingBoxLengthError(Exception):
    def __init__(self, bounding_box):
        """Constructor method

        :param list[int] bounding_box: bounding box (x_1, y_1, x_2, y_2)
        :returns: None
        :rtype: None
        """
        message = ('Invalid bounding_box in config file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   f'Expected 4 coordinates (x_1, y_1, x_2, y_2), got {len(bounding_box)} coordinates instead.')
        super().__init__(message)


class BoundingBoxError(Exception):
    def __init__(self, bounding_box):
        """Constructor method

        :param list[int] bounding_box: bounding box (x_1, y_1, x_2, y_2)
        :returns: None
        :rtype: None
        """
        message = ('Invalid bounding_box in config file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   'Expected 4 coordinates (x_1, y_1, x_2, y_2) with x_1 < x_2 and y_1 < y_2, '
                   f"got ({', '.join(map(str, bounding_box))}) instead.")
        super().__init__(message)
