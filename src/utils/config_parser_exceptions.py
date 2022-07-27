# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from pathlib import Path

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
                   f'Expected a number divisible by 32 in the range of 512 to 2560, got {image_size} instead.')
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


class ColorCodeNDSMError(Exception):
    def __init__(self, color_code):
        """Constructor method

        :param str color_code: color code ('(r_value, g_value, b_value) - mapped_value')
        :returns: None
        :rtype: None
        """
        message = ('Invalid color code in color_codes_ndsm in config file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   'Expected a color code with the following schema: (r_value, g_value, b_value) - mapped_value, '
                   f'got {color_code} instead.')
        super().__init__(message)


class SieveSizeError(Exception):
    def __init__(self, sieve_size):
        """Constructor method

        :param int sieve_size: sieve size in pixels
        :returns: None
        :rtype: None
        """
        message = ('Invalid sieve_size in config file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   f'Expected a number in the range of 0 to 1e4, got {sieve_size} instead.')
        super().__init__(message)


class TileSizeError(Exception):
    def __init__(self, tile_size):
        """Constructor method

        :param int tile_size: tile size in meters
        :returns: None
        :rtype: None
        """
        message = ('Invalid tile size in tile_size in config file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   f'Expected a number greater than 0, got {tile_size} instead.')
        super().__init__(message)


class ShpFileNotFoundError(Exception):
    def __init__(self, shp_path):
        """Constructor method

        :param str shp_path: path to the shape file (.shp)
        :returns: None
        :rtype: None
        """
        message = ('Invalid path to the shape file in shp_path in config file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   f'Shape file at {shp_path} does not exist.')
        super().__init__(message)


class ShpFileExtensionError(Exception):
    def __init__(self, shp_path):
        """Constructor method

        :param str shp_path: path to the shape file (.shp)
        :returns: None
        :rtype: None
        """
        message = ('Invalid path to the shape file in shp_path in config file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   f'Expected file extension .shp, got {Path(shp_path).suffix} instead.')
        super().__init__(message)


class OutputDirNotFoundError(Exception):
    def __init__(self, output_dir_path):
        """Constructor method

        :param str output_dir_path: path to the output directory
        :returns: None
        :rtype: None
        """
        message = ('Invalid output_dir_path in config file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   f'Directory at {output_dir_path} does not exist.')
        super().__init__(message)


class OutputDirNotEmptyError(Exception):
    def __init__(self, output_dir_path):
        """Constructor method

        :param str output_dir_path: path to the output directory
        :returns: None
        :rtype: None
        """
        message = ('Invalid output_dir_path in config file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   f'Directory at {output_dir_path} is not empty.')
        super().__init__(message)


class ShpPrefixError(Exception):
    def __init__(self):
        """Constructor method

        :returns: None
        :rtype: None
        """
        message = ('Invalid shp_prefix in config file!\n' + ' ' * (4 if utils.DEBUG else 2) +
                   'String contains only whitespaces or underscores.')
        super().__init__(message)
