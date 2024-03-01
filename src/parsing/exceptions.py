from pathlib import Path


class BoundingBoxError(Exception):

    def __init__(self,
                 message: str = 'Invalid bounding_box in the config!') -> None:
        """
        | Initializer method

        :param message: message
        :returns: None
        """
        super().__init__(message)


class BoundingBoxLengthError(BoundingBoxError):

    def __init__(self,
                 bounding_box: list[int]) -> None:
        """
        | Initializer method

        :param bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :returns: None
        """
        message = (
            'Invalid bounding_box in the config!\n'
            f'Expected 4 coordinates (x_min, y_min, x_max, y_max), got {len(bounding_box)} coordinates instead.')

        super().__init__(message)


class BoundingBoxNotDefinedError(BoundingBoxError):

    def __init__(self) -> None:
        """
        | Initializer method

        :returns: None
        """
        message = 'Neither path_boundary nor bounding_box are defined in the config!'
        super().__init__(message)


class BoundingBoxValueError(BoundingBoxError):

    def __init__(self,
                 bounding_box: list[int]) -> None:
        """
        | Initializer method

        :param bounding_box: bounding box (x_min, y_min, x_max, y_max)
        :returns: None
        """
        message = (
            'Invalid bounding_box in the config!\n'
            'Expected 4 coordinates (x_min, y_min, x_max, y_max) with x_min < x_max and y_min < y_max, '
            f"got ({', '.join(map(str, bounding_box))}) instead.")

        super().__init__(message)


class GeoDataError(Exception):

    def __init__(self,
                 message: str = 'Invalid geo data in the config!') -> None:
        """
        | Initializer method

        :param message: message
        :returns: None
        """
        super().__init__(message)


class GeoDataEmptyError(GeoDataError):

    def __init__(self,
                 field: str,
                 path: Path) -> None:
        """
        | Initializer method

        :param field: field
        :param path: path to the geo data
        :returns: None
        """
        message = (
            f'Invalid {field} in the config!\n'
            f'The geo data at {path} is empty.')

        super().__init__(message)


class GeoDataFormatError(GeoDataError):

    def __init__(self,
                 field: str,
                 path: Path) -> None:
        """
        | Initializer method

        :param field: field
        :param path: path to the geo data
        :returns: None
        """
        message = (
            f'Invalid {field} in the config!\n'
            f'Expected file extension .gpkg or .shp, got {path.suffix} instead.')

        super().__init__(message)


class GeoDataGeometryError(GeoDataError):

    def __init__(self,
                 field: str,
                 path: Path) -> None:
        """
        | Initializer method

        :param field: field
        :param path: path to the geo data
        :returns: None
        """
        message = (
            f'Invalid {field} in the config!\n'
            f'The geo data at {path} contains invalid polygons.')

        super().__init__(message)


class GeoDataLoadingError(GeoDataError):

    def __init__(self,
                 field: str,
                 path: Path,
                 passed_exception: Exception) -> None:
        """
        | Initializer method

        :param field: field
        :param path: path to the geo data
        :param passed_exception: passed exception
        :returns: None
        """
        message = (
            f'Invalid {field} in the config!\n'
            f'An exception is raised while loading the geo data at {path}.\n'
            f'{passed_exception}')

        super().__init__(message)


class GeoDataNotFoundError(GeoDataError):

    def __init__(self,
                 field: str,
                 path: Path) -> None:
        """
        | Initializer method

        :param field: field
        :param path: path to the geo data
        :returns: None
        """
        message = (
            f'Invalid {field} in the config!\n'
            f'The geo data at {path} does not exist.')

        super().__init__(message)


class GeoDataTypeError(GeoDataError):

    def __init__(self,
                 field: str,
                 path: Path) -> None:
        """
        | Initializer method

        :param field: field
        :param path: path to the geo data
        :returns: None
        """
        message = (
            f'Invalid {field} in the config!\n'
            f'The geo data at {path} contains geometries other than polygons.')

        super().__init__(message)


class OutputDirNotFoundError(Exception):

    def __init__(self,
                 path: Path) -> None:
        """
        | Initializer method

        :param path: path to the output directory
        :returns: None
        """
        message = (
            'Invalid path_output_dir in the config!\n'
            f'The output directory at {path} does not exist.')

        super().__init__(message)


class PrefixError(Exception):

    def __init__(self) -> None:
        """
        | Initializer method

        :returns: None
        """
        message = (
            'Invalid prefix in the config!\n'
            'The prefix contains only whitespaces or underscores.')

        super().__init__(message)


class SieveSizeError(Exception):

    def __init__(self,
                 sieve_size: int) -> None:
        """
        | Initializer method

        :param sieve_size: sieve size in square meters
        :returns: None
        """
        message = (
            'Invalid sieve_size in the config!\n'
            f'Expected a number in the range of 0 to 10, got {sieve_size} instead.')

        super().__init__(message)


class TileSizeError(Exception):

    def __init__(self,
                 tile_size: int) -> None:
        """
        | Initializer method

        :param tile_size: tile size in meters
        :returns: None
        """
        message = (
            'Invalid tile_size in the config!\n'
            f'Expected a number greater than 0, got {tile_size} instead.')

        super().__init__(message)
