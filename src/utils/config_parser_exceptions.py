from pathlib import Path

import geopandas as gpd
from natsort import natsorted

import src.utils.settings as settings


class WMSConnectionError(Exception):
    def __init__(self,
                 wms_url,
                 passed_exception):
        """
        | Constructor method

        :param str wms_url: url of the web map service
        :param Exception passed_exception: passed exception
        :returns: None
        :rtype: None
        """
        message = (f'No connection to WMS ({wms_url}) in config_file!\n' + ' ' * (4 if settings.DEBUG else 2) +
                   f'{passed_exception}')
        super().__init__(message)


class WMSLayerError(Exception):
    def __init__(self,
                 wms_layer,
                 wms_url,
                 valid_wms_layers):
        """
        | Constructor method

        :param str wms_layer: layer of the web map service
        :param str wms_url: url of the web map service
        :param list[str] valid_wms_layers: valid layers
        :returns: None
        :rtype: None
        """
        if len(valid_wms_layers) == 1:
            valid_wms_layers = valid_wms_layers[0]
        else:
            valid_wms_layers = natsorted(valid_wms_layers)
            valid_wms_layers = (f"{', '.join(map(str, valid_wms_layers[:-1]))} "
                                f'or {valid_wms_layers[-1]}')
        message = (f'Invalid wms_layer of WMS ({wms_url}) in config file!\n' + ' ' * (4 if settings.DEBUG else 2) +
                   f'Expected {valid_wms_layers}, '
                   f'got {wms_layer} instead.')
        super().__init__(message)


class EPSGCodeError(Exception):
    def __init__(self,
                 epsg_code,
                 valid_epsg_codes):
        """
        | Constructor method

        :param int epsg_code: epsg code of the coordinate reference system
        :param list[int] valid_epsg_codes: valid epsg codes
        :returns: None
        :rtype: None
        """
        if len(valid_epsg_codes) == 1:
            valid_epsg_codes = valid_epsg_codes[0]
        else:
            valid_epsg_codes = natsorted(valid_epsg_codes)
            valid_epsg_codes = (f"{', '.join(map(str, valid_epsg_codes[:-1]))} "
                                f'or {valid_epsg_codes[-1]}')
        message = ('Invalid epsg_code in config file!\n' + ' ' * (4 if settings.DEBUG else 2) +
                   f'Expected {valid_epsg_codes}, '
                   f'got {epsg_code} instead.')
        super().__init__(message)


class ShapeFileNotFoundError(Exception):
    def __init__(self, shape_file_path):
        """
        | Constructor method

        :param str shape_file_path: path to the shape file (.shp)
        :returns: None
        :rtype: None
        """
        message = ('Invalid path to the shape file in shape_file_path in config file!\n' +
                   ' ' * (4 if settings.DEBUG else 2) +
                   f'Shape file at {shape_file_path} does not exist.')
        super().__init__(message)


class ShapeFileExtensionError(Exception):
    def __init__(self, shape_file_path):
        """
        | Constructor method

        :param str shape_file_path: path to the shape file (.shp)
        :returns: None
        :rtype: None
        """
        message = ('Invalid path to the shape file in shape_file_path in config file!\n' +
                   ' ' * (4 if settings.DEBUG else 2) +
                   f'Expected file extension .shp, got {Path(shape_file_path).suffix} instead.')
        super().__init__(message)


class ShapeFileLengthError(Exception):
    def __init__(self, gdf):
        """
        | Constructor method

        :param gpd.GeoDataFrame gdf: geodataframe
        :returns: None
        :rtype: None
        """
        message = ('Invalid shape file in shape_file_path in config file!\n' +
                   ' ' * (4 if settings.DEBUG else 2) +
                   f'Expected shape file with 1 polygon, got {gdf.shape[0]} polygons instead.')
        super().__init__(message)


class BoundingBoxNotDefinedError(Exception):
    def __init__(self):
        """
        | Constructor method

        :returns: None
        :rtype: None
        """
        message = 'Neither boundary_shape_file_path nor bounding_box are defined in config file!'
        super().__init__(message)


class BoundingBoxLengthError(Exception):
    def __init__(self, bounding_box):
        """
        | Constructor method

        :param list[int] bounding_box: bounding box (x_1, y_1, x_2, y_2)
        :returns: None
        :rtype: None
        """
        message = ('Invalid bounding_box in config file!\n' + ' ' * (4 if settings.DEBUG else 2) +
                   f'Expected 4 coordinates (x_1, y_1, x_2, y_2), got {len(bounding_box)} coordinates instead.')
        super().__init__(message)


class BoundingBoxError(Exception):
    def __init__(self, bounding_box):
        """
        | Constructor method

        :param list[int] bounding_box: bounding box (x_1, y_1, x_2, y_2)
        :returns: None
        :rtype: None
        """
        message = ('Invalid bounding_box in config file!\n' + ' ' * (4 if settings.DEBUG else 2) +
                   'Expected 4 coordinates (x_1, y_1, x_2, y_2) with x_1 < x_2 and y_1 < y_2, '
                   f"got ({', '.join(map(str, bounding_box))}) instead.")
        super().__init__(message)


class SieveSizeError(Exception):
    def __init__(self, sieve_size):
        """
        | Constructor method

        :param int sieve_size: sieve size in square meters
        :returns: None
        :rtype: None
        """
        message = ('Invalid sieve_size in config file!\n' + ' ' * (4 if settings.DEBUG else 2) +
                   f'Expected a number in the range of 0 to 10, got {sieve_size} instead.')
        super().__init__(message)


class TileSizeError(Exception):
    def __init__(self, tile_size):
        """
        | Constructor method

        :param int tile_size: tile size in meters
        :returns: None
        :rtype: None
        """
        message = ('Invalid tile_size in config file!\n' + ' ' * (4 if settings.DEBUG else 2) +
                   f'Expected a number greater than 0, got {tile_size} instead.')
        super().__init__(message)


class OutputDirNotFoundError(Exception):
    def __init__(self, output_dir_path):
        """
        | Constructor method

        :param str output_dir_path: path to the output directory
        :returns: None
        :rtype: None
        """
        message = ('Invalid output_dir_path in config file!\n' + ' ' * (4 if settings.DEBUG else 2) +
                   f'Directory at {output_dir_path} does not exist.')
        super().__init__(message)


class OutputDirNotEmptyError(Exception):
    def __init__(self, output_dir_path):
        """
        | Constructor method

        :param str output_dir_path: path to the output directory
        :returns: None
        :rtype: None
        """
        message = ('Invalid output_dir_path in config file!\n' + ' ' * (4 if settings.DEBUG else 2) +
                   f'Directory at {output_dir_path} is not empty.')
        super().__init__(message)


class PrefixError(Exception):
    def __init__(self):
        """
        | Constructor method

        :returns: None
        :rtype: None
        """
        message = ('Invalid prefix in config file!\n' + ' ' * (4 if settings.DEBUG else 2) +
                   'String contains only whitespaces or underscores.')
        super().__init__(message)
