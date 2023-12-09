from pathlib import Path  # noqa: F401 (used for type hinting)

from natsort import natsorted


class BoundingBoxError(Exception):

    def __init__(self,
                 message='Invalid bounding_box in the config!'):
        """
        | Initializer method

        :param str message: message
        :returns: None
        :rtype: None
        """
        super().__init__(message)


class BoundingBoxLengthError(BoundingBoxError):

    def __init__(self,
                 bounding_box):
        """
        | Initializer method

        :param list[int] bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :returns: None
        :rtype: None
        """
        message = (
            'Invalid bounding_box in the config!\n'
            f'Expected 4 coordinates (x_min, y_min, x_max, y_max), got {len(bounding_box)} coordinates instead.')

        super().__init__(message)


class BoundingBoxNotDefinedError(BoundingBoxError):

    def __init__(self):
        """
        | Initializer method

        :returns: None
        :rtype: None
        """
        message = 'Neither path_boundary nor bounding_box are defined in the config!'
        super().__init__(message)


class BoundingBoxValueError(BoundingBoxError):

    def __init__(self,
                 bounding_box):
        """
        | Initializer method

        :param list[int] bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :returns: None
        :rtype: None
        """
        message = (
            'Invalid bounding_box in the config!\n'
            'Expected 4 coordinates (x_min, y_min, x_max, y_max) with x_min < x_max and y_min < y_max, '
            f"got ({', '.join(map(str, bounding_box))}) instead.")

        super().__init__(message)


class EPSGCodeError(Exception):

    def __init__(self,
                 epsg_code,
                 epsg_codes_valid):
        """
        | Initializer method

        :param int epsg_code: epsg code
        :param list[int] epsg_codes_valid: valid epsg codes
        :returns: None
        :rtype: None
        """
        if len(epsg_codes_valid) == 1:
            epsg_codes_valid = epsg_codes_valid[0]
        else:
            epsg_codes_valid = natsorted(epsg_codes_valid)

            epsg_codes_valid = (
                f"{', '.join(map(str, epsg_codes_valid[:-1]))} "
                f'or {epsg_codes_valid[-1]}')

        message = (
            'Invalid epsg_code in the config!\n'
            f'Expected {epsg_codes_valid}, got {epsg_code} instead.')

        super().__init__(message)


class GeoDataError(Exception):

    def __init__(self,
                 message='Invalid geo data in the config!'):
        """
        | Initializer method

        :param str message: message
        :returns: None
        :rtype: None
        """
        super().__init__(message)


class GeoDataEmptyError(GeoDataError):

    def __init__(self,
                 field,
                 path):
        """
        | Initializer method

        :param str field: field
        :param Path path: path to the geo data
        :returns: None
        :rtype: None
        """
        message = (
            f'Invalid {field} in the config!\n'
            f'The geo data at {path} is empty.')

        super().__init__(message)


class GeoDataFormatError(GeoDataError):

    def __init__(self,
                 field,
                 path):
        """
        | Initializer method

        :param str field: field
        :param Path path: path to the geo data
        :returns: None
        :rtype: None
        """
        message = (
            f'Invalid {field} in the config!\n'
            f'Expected file extension .gpkg or .shp, got {path.suffix} instead.')

        super().__init__(message)


class GeoDataGeometryError(GeoDataError):

    def __init__(self,
                 field,
                 path):
        """
        | Initializer method

        :param str field: field
        :param Path path: path to the geo data
        :returns: None
        :rtype: None
        """
        message = (
            f'Invalid {field} in the config!\n'
            f'The geo data at {path} contains invalid polygons.')

        super().__init__(message)


class GeoDataLoadingError(GeoDataError):

    def __init__(self,
                 field,
                 path,
                 passed_exception):
        """
        | Initializer method

        :param str field: field
        :param Path path: path to the geo data
        :param Exception passed_exception: passed exception
        :returns: None
        :rtype: None
        """
        message = (
            f'Invalid {field} in the config!\n'
            f'An exception occurred while loading the geo data at {path}.\n'
            f'{passed_exception}')

        super().__init__(message)


class GeoDataNotFoundError(GeoDataError):

    def __init__(self,
                 field,
                 path):
        """
        | Initializer method

        :param str field: field
        :param Path path: path to the geo data
        :returns: None
        :rtype: None
        """
        message = (
            f'Invalid {field} in the config!\n'
            f'The geo data at {path} does not exist.')

        super().__init__(message)


class GeoDataTypeError(GeoDataError):

    def __init__(self,
                 field,
                 path):
        """
        | Initializer method

        :param str field: field
        :param Path path: path to the geo data
        :returns: None
        :rtype: None
        """
        message = (
            f'Invalid {field} in the config!\n'
            f'The geo data at {path} contains geometries other than polygons.')

        super().__init__(message)


class OutputDirError(Exception):

    def __init__(self,
                 message='Invalid path_output_dir in the config!'):
        """
        | Initializer method

        :param str message: message
        :returns: None
        :rtype: None
        """
        super().__init__(message)


class OutputDirNotEmptyError(OutputDirError):

    def __init__(self,
                 path):
        """
        | Initializer method

        :param Path path: path to the output directory
        :returns: None
        :rtype: None
        """
        message = (
            'Invalid path_output_dir in the config!\n'
            f'The output directory at {path} is not empty.')

        super().__init__(message)


class OutputDirNotFoundError(OutputDirError):

    def __init__(self,
                 path):
        """
        | Initializer method

        :param Path path: path to the output directory
        :returns: None
        :rtype: None
        """
        message = (
            'Invalid path_output_dir in the config!\n'
            f'The output directory at {path} does not exist.')

        super().__init__(message)


class PrefixError(Exception):

    def __init__(self):
        """
        | Initializer method

        :returns: None
        :rtype: None
        """
        message = (
            'Invalid prefix in the config!\n'
            'The prefix contains only whitespaces or underscores.')

        super().__init__(message)


class SieveSizeError(Exception):

    def __init__(self,
                 sieve_size):
        """
        | Initializer method

        :param int sieve_size: sieve size in square meters
        :returns: None
        :rtype: None
        """
        message = (
            'Invalid sieve_size in the config!\n'
            f'Expected a number in the range of 0 to 10, got {sieve_size} instead.')

        super().__init__(message)


class TileSizeError(Exception):

    def __init__(self,
                 tile_size):
        """
        | Initializer method

        :param int tile_size: tile size in meters
        :returns: None
        :rtype: None
        """
        message = (
            'Invalid tile_size in the config!\n'
            f'Expected a number greater than 0, got {tile_size} instead.')

        super().__init__(message)


class WMSError(Exception):

    def __init__(self,
                 message='Invalid web map service in the config!'):
        """
        | Initializer method

        :param str message: message
        :returns: None
        :rtype: None
        """
        super().__init__(message)


class WMSConnectionError(WMSError):

    def __init__(self,
                 wms_url,
                 passed_exception):
        """
        | Initializer method

        :param str wms_url: url of the web map service
        :param Exception passed_exception: passed exception
        :returns: None
        :rtype: None
        """
        message = (
            'Invalid wms_url in the config!\n'
            f'An exception occurred while connecting to the web map service ({wms_url}).\n'
            f'{passed_exception}')

        super().__init__(message)


class WMSLayerError(WMSError):

    def __init__(self,
                 wms_layer,
                 wms_layers_valid):
        """
        | Initializer method

        :param str wms_layer: layer of the web map service
        :param list[str] wms_layers_valid: valid layers of the web map service
        :returns: None
        :rtype: None
        """
        if len(wms_layers_valid) == 1:
            wms_layers_valid = wms_layers_valid[0]
        else:
            wms_layers_valid = natsorted(wms_layers_valid)
            wms_layers_valid = (
                f"{', '.join(map(str, wms_layers_valid[:-1]))} "
                f'or {wms_layers_valid[-1]}')

        message = (
            'Invalid wms_layer in the config!\n'
            f'Expected {wms_layers_valid}, got {wms_layer} instead.')

        super().__init__(message)
