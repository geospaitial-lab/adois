from pathlib import Path
from typing import List, Union

import geopandas as gpd
import numpy as np
import pydantic
from natsort import natsorted
from owslib.wms import WebMapService
from pydantic import root_validator, validator

from src.parsing.config_exceptions import (
    BoundingBoxLengthError,
    BoundingBoxNotDefinedError,
    BoundingBoxValueError,
    EPSGCodeError,
    GeoDataEmptyError,
    GeoDataFormatError,
    GeoDataGeometryError,
    GeoDataLoadingError,
    GeoDataNotFoundError,
    GeoDataTypeError,
    OutputDirNotEmptyError,
    OutputDirNotFoundError,
    PrefixError,
    SieveSizeError,
    TileSizeError,
    WMSConnectionError,
    WMSLayerError)


class WMS(pydantic.BaseModel):
    url: str
    layer: str

    @validator('url')
    def validate_url(cls,
                     value):
        """
        | Validates url.

        :param str value: url
        :returns: validated url
        :rtype: str
        :raises WMSConnectionError: if an exception occurs while connecting to the web map service
            (the exception raised by owslib is passed)
        """
        try:
            _ = WebMapService(url=value,
                              version='1.1.1')

        except Exception as e:
            raise WMSConnectionError(url=value,
                                     passed_exception=e)

        return value

    @validator('layer')
    def validate_layer(cls,
                       value,
                       values):
        """
        | Validates layer.

        :param str value: layer
        :param dict[str, Any] values: values
        :returns: validated layer
        :rtype: str
        :raises WMSConnectionError: if an exception occurs while connecting to the web map service
            (the exception raised by owslib is passed)
        :raises WMSLayerError: if layer is not a valid layer of the web map service
        """
        try:
            web_map_service = WebMapService(url=values['url'],
                                            version='1.1.1')

        except Exception as e:
            raise WMSConnectionError(url=value,
                                     passed_exception=e)

        layers_valid = [*web_map_service.contents]

        if value not in layers_valid:
            raise WMSLayerError(layer=value,
                                layers_valid=layers_valid)

        return value


class Data(pydantic.BaseModel):
    rgb: WMS
    nir: WMS
    epsg_code: int
    path_boundary: str = None
    bounding_box: List[int] = None
    apply_padding: bool = False
    ignore_processed_tiles: bool = False

    @validator('epsg_code')
    def validate_epsg_code(cls,
                           value,
                           values):
        """
        | Validates epsg_code.

        :param int value: epsg_code
        :param dict[str, Any] values: values
        :returns: validated epsg_code
        :rtype: int
        :raises EPSGCodeError: if epsg_code is not a valid epsg code of the web map services
        """
        wms_rgb = WebMapService(url=values['rgb'].url,
                                version='1.1.1')

        wms_nir = WebMapService(url=values['nir'].url,
                                version='1.1.1')

        epsg_codes_valid_rgb = [int(epsg_code[5:])
                                for epsg_code in wms_rgb[values['rgb'].layer].crsOptions]

        epsg_codes_valid_nir = [int(epsg_code[5:])
                                for epsg_code in wms_nir[values['nir'].layer].crsOptions]

        epsg_codes_valid = list(set(epsg_codes_valid_rgb) & set(epsg_codes_valid_nir))

        if value not in epsg_codes_valid:
            raise EPSGCodeError(epsg_code=value,
                                epsg_codes_valid=epsg_codes_valid)

        return value

    @validator('path_boundary')
    def validate_path_boundary(cls,
                               value):
        """
        | Validates path_boundary.

        :param str or None value: path_boundary
        :returns: validated path_boundary
        :rtype: Path or None
        :raises GeoDataEmptyError: if the geo data is empty
        :raises GeoDataFormatError: if the file extension of the geo data is not .gpkg or .shp
        :raises GeoDataGeometryError: if the geo data contains invalid polygons
        :raises GeoDataLoadingError: if an exception occurs while loading the geo data
            (the exception raised by geopandas is passed)
        :raises GeoDataNotFoundError: if the geo data does not exist
        :raises GeoDataTypeError: if the geo data contains geometries other than polygons
        """
        if value is None:
            return value

        value = Path(value)

        if not value.is_file():
            raise GeoDataNotFoundError(field='path_boundary',
                                       path=value)

        if value.suffix not in ['.gpkg', '.shp']:
            raise GeoDataFormatError(field='path_boundary',
                                     path=value)

        try:
            boundary = gpd.read_file(value)
        except Exception as e:
            raise GeoDataLoadingError(field='path_boundary',
                                      path=value,
                                      passed_exception=e)

        if boundary.empty:
            raise GeoDataEmptyError(field='path_boundary',
                                    path=value)

        if not all(boundary['geometry'].geom_type == 'Polygon'):
            raise GeoDataTypeError(field='path_boundary',
                                   path=value)

        if not all(boundary['geometry'].is_valid):
            raise GeoDataGeometryError(field='path_boundary',
                                       path=value)

        return value

    @validator('bounding_box', always=True)
    def validate_bounding_box(cls,
                              value,
                              values):
        """
        | Validates bounding_box.

        :param list[int] or None value: bounding_box
        :param dict[str, Any] values: values
        :returns: validated bounding_box
        :rtype: (int, int, int, int)
        :raises BoundingBoxLengthError: if the length of bounding_box is not equal to 4
        :raises BoundingBoxNotDefinedError: if neither path_boundary nor bounding_box are defined in the config
        :raises BoundingBoxValueError: if x_min >= x_max or y_min >= y_max
        """
        if value is None and values['path_boundary'] is None:
            raise BoundingBoxNotDefinedError()

        if values['path_boundary'] is None:
            if len(value) != 4:
                raise BoundingBoxLengthError(bounding_box=value)

            if value[0] >= value[2] or value[1] >= value[3]:
                raise BoundingBoxValueError(bounding_box=value)

        else:
            boundary = gpd.read_file(Path(values['path_boundary']))
            bounding_box_boundary = boundary.total_bounds

            value = (
                [int(np.floor(bounding_box_boundary[0])),
                 int(np.floor(bounding_box_boundary[1])),
                 int(np.ceil(bounding_box_boundary[2])),
                 int(np.ceil(bounding_box_boundary[3]))])

        return tuple(value)

    @validator('apply_padding')
    def validate_apply_padding(cls,
                               value):
        """
        | Validates apply_padding.

        :param bool or None value: apply_padding
        :returns: validated apply_padding
        :rtype: bool
        """
        if value is None:
            value = False

        return value

    @validator('ignore_processed_tiles')
    def validate_ignore_processed_tiles(cls,
                                        value):
        """
        | Validates ignore_processed_tiles.

        :param bool or None value: ignore_processed_tiles
        :returns: validated ignore_processed_tiles
        :rtype: bool
        """
        if value is None:
            value = False

        return value


class Postprocessing(pydantic.BaseModel):
    sieve_size: int = None
    simplify: bool = False

    @validator('sieve_size')
    def validate_sieve_size(cls,
                            value):
        """
        | Validates sieve_size.

        :param int or None value: sieve_size
        :returns: validated sieve_size
        :rtype: int or None
        :raises SieveSizeError: if sieve_size is not a number in the range of 0 to 10
        """
        if value is None:
            return value

        if not 0 <= value <= 10:
            raise SieveSizeError(sieve_size=value)

        if value == 0:
            value = None

        return value

    @validator('simplify')
    def validate_simplify(cls,
                          value):
        """
        | Validates simplify.

        :param bool or None value: simplify
        :returns: validated simplify
        :rtype: bool
        """
        if value is None:
            value = False

        return value


class Aggregation(pydantic.BaseModel):
    tile_size: Union[int, List[Union[int, None]], None] = []
    path_aggregation_areas: Union[str, List[Union[str, None]], None] = []

    @validator('tile_size')
    def validate_tile_size(cls,
                           value):
        """
        | Validates tile_size.

        :param int or list[int or None] or None value: tile_size
        :returns: validated tile_size
        :rtype: list[int]
        :raises TileSizeError: if tile_size is not a number greater than 0
        """
        if value is None:
            return []

        if isinstance(value, int):
            value = [value]

        for i, tile_size in enumerate(value):
            if tile_size is not None:
                if tile_size < 0:
                    raise TileSizeError(tile_size=tile_size)

                if tile_size == 0:
                    value[i] = None

        value = [tile_size
                 for tile_size in value
                 if tile_size is not None]

        return list(set(value))

    @validator('path_aggregation_areas')
    def validate_path_aggregation_areas(cls,
                                        value):
        """
        | Validates path_aggregation_areas.

        :param str or list[str or None] or None value: path_aggregation_areas
        :returns: validated path_aggregation_areas
        :rtype: list[Path]
        :raises GeoDataEmptyError: if the geo data is empty
        :raises GeoDataFormatError: if the file extension of the geo data is not .gpkg or .shp
        :raises GeoDataGeometryError: if the geo data contains invalid polygons
        :raises GeoDataLoadingError: if an exception occurs while loading the geo data
            (the exception raised by geopandas is passed)
        :raises GeoDataNotFoundError: if the geo data does not exist
        :raises GeoDataTypeError: if the geo data contains geometries other than polygons
        """
        if value is None:
            return []

        if isinstance(value, str):
            value = [value]

        for path_aggregation_areas in value:
            if path_aggregation_areas is not None:
                path_aggregation_areas = Path(path_aggregation_areas)

                if not path_aggregation_areas.is_file():
                    raise GeoDataNotFoundError(field='path_aggregation_areas',
                                               path=path_aggregation_areas)

                if path_aggregation_areas.suffix not in ['.gpkg', '.shp']:
                    raise GeoDataFormatError(field='path_aggregation_areas',
                                             path=path_aggregation_areas)

                try:
                    aggregation_areas = gpd.read_file(path_aggregation_areas)
                except Exception as e:
                    raise GeoDataLoadingError(field='path_aggregation_areas',
                                              path=path_aggregation_areas,
                                              passed_exception=e)

                if aggregation_areas.empty:
                    raise GeoDataEmptyError(field='path_aggregation_areas',
                                            path=path_aggregation_areas)

                if not all(aggregation_areas['geometry'].geom_type == 'Polygon'):
                    raise GeoDataTypeError(field='path_aggregation_areas',
                                           path=path_aggregation_areas)

                if not all(aggregation_areas['geometry'].is_valid):
                    raise GeoDataGeometryError(field='path_aggregation_areas',
                                               path=path_aggregation_areas)

        value = [Path(path_aggregation_areas)
                 for path_aggregation_areas in value
                 if path_aggregation_areas is not None]

        return natsorted(list(set(value)))


class Export(pydantic.BaseModel):
    path_output_dir: str
    prefix: str

    @validator('path_output_dir')
    def validate_path_output_dir(cls,
                                 value):
        """
        | Validates path_output_dir.

        :param str value: path_output_dir
        :returns: validated path_output_dir
        :rtype: Path
        :raises OutputDirNotEmptyError: if the output directory is not empty
        :raises OutputDirNotFoundError: if the output directory does not exist
        """
        value = Path(value)

        if not value.is_dir():
            raise OutputDirNotFoundError(path=value)

        for path in value.iterdir():
            conditions = (
                [not path.name.startswith('.'),
                 not path.name == 'tiles_processed',
                 path.suffix not in ['.log', '.yml', '.yaml']])

            if all(conditions):
                raise OutputDirNotEmptyError(path=value)

        return value

    @validator('prefix')
    def validate_prefix(cls,
                        value):
        """
        | Validates prefix.

        :param str value: prefix
        :returns: validated prefix
        :rtype: str
        :raises PrefixError: if prefix contains only whitespaces or underscores
        """
        value = value.replace(' ', '').rstrip('_')

        if not value:
            raise PrefixError()

        return value


class Config(pydantic.BaseModel):
    data: Data
    postprocessing: Postprocessing = Postprocessing()
    aggregation: Aggregation = Aggregation()
    export: Export

    @root_validator
    def validate_tile_size(cls,
                           values):
        """
        | Validates tile_size.

        :param dict[str, Any] values: values
        :returns: validated values
        :rtype: dict[str, Any]
        """
        if not values['Aggregation'].tile_size:
            return values

        tile_size_max = min(values['data'].bounding_box[2] - values['data'].bounding_box[0],
                            values['data'].bounding_box[3] - values['data'].bounding_box[1])

        values['Aggregation'].tile_size = [tile_size
                                           for tile_size in values['Aggregation'].tile_size
                                           if tile_size <= tile_size_max]

        return values
