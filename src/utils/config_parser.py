# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from pathlib import Path
from typing import List, Optional, Union

# noinspection PyUnresolvedReferences
import geopandas as gpd
import numpy as np
import yaml
from owslib.wms import WebMapService
from pydantic import BaseModel, root_validator, validator

from src.utils.config_parser_exceptions import *


class Wms(BaseModel):
    wms_url: str
    wms_layer: str

    @validator('wms_url')
    def validate_wms_url(cls, value):
        """
        | Validates wms_url defined in the config file.

        :param str value: wms_url
        :returns: validated wms_url
        :rtype: str
        :raises WMSConnectionError: if the connection to the web map service cannot be established
            (exception of owslib is passed)
        """
        try:
            _ = WebMapService(value)
        except Exception as e:
            raise WMSConnectionError(wms_url=value,
                                     passed_exception=e)
        return value

    @validator('wms_layer')
    def validate_wms_layer(cls,
                           value,
                           values):
        """
        | Validates wms_layer defined in the config file.

        :param str value: wms_layer
        :param dict[str, Any] values: config
        :returns: validated wms_layer
        :rtype: str
        :raises WMSLayerError: if wms_layer is not in the valid layers of the web map service
        """
        wms = WebMapService(values['wms_url'])
        valid_wms_layers = [*wms.contents]

        if value not in valid_wms_layers:
            raise WMSLayerError(wms_layer=value,
                                wms_url=values['wms_url'],
                                valid_wms_layers=valid_wms_layers)
        return value


class Data(BaseModel):
    rgb: Wms
    nir: Wms
    epsg_code: int
    boundary_shape_file_path: Optional[str]
    bounding_box: Optional[List[int]]

    @validator('epsg_code')
    def validate_epsg_code(cls,
                           value,
                           values):
        """
        | Validates epsg_code defined in the config file.

        :param int value: epsg_code
        :param dict[str, Any] values: config
        :returns: validated epsg_code
        :rtype: int
        :raises EPSGCodeError: if epsg_code is not in the valid epsg codes of the web map services
        """
        wms_rgb = WebMapService(values['rgb'].wms_url)
        wms_nir = WebMapService(values['nir'].wms_url)
        valid_epsg_codes_rgb = [int(epsg_code[5:]) for epsg_code in wms_rgb[values['rgb'].wms_layer].crsOptions]
        valid_epsg_codes_nir = [int(epsg_code[5:]) for epsg_code in wms_nir[values['nir'].wms_layer].crsOptions]
        valid_epsg_codes = list(set(valid_epsg_codes_rgb) & set(valid_epsg_codes_nir))

        if value not in valid_epsg_codes:
            raise EPSGCodeError(epsg_code=value,
                                valid_epsg_codes=valid_epsg_codes)
        return value

    @validator('boundary_shape_file_path')
    def validate_boundary_shape_file_path(cls, value):
        """
        | Validates boundary_shape_file_path defined in the config file.

        :param str or None value: boundary_shape_file_path
        :returns: validated boundary_shape_file_path
        :rtype: str or None
        :raises ShapeFileNotFoundError: if shape file at boundary_shape_file_path does not exist
        :raises ShapeFileExtensionError: if file extension of boundary_shape_file_path is not .shp
        """
        if value is not None:
            if not Path(value).is_file():
                raise ShapeFileNotFoundError(shape_file_path=value)
            elif Path(value).suffix != '.shp':
                raise ShapeFileExtensionError(shape_file_path=value)
            boundary_gdf = gpd.read_file(value)
            if boundary_gdf.shape[0] != 1:
                raise ShapeFileLengthError(gdf=boundary_gdf)
        return value

    @validator('bounding_box')
    def validate_bounding_box(cls,
                              value,
                              values):
        """
        | Validates bounding_box defined in the config file.

        :param list[int] or None value: bounding_box (x_1, y_1, x_2, y_2)
        :param dict[str, Any] values: config
        :returns: validated bounding_box
        :rtype: (int, int, int, int) or None
        :raises BoundingBoxNotDefinedError: if neither boundary_shape_file_path nor bounding_box are defined
            in the config file
        :raises BoundingBoxLengthError: if the length of bounding_box is not equal to 4
        :raises BoundingBoxError: if x_1 >= x_2 or y_1 >= y_2
        """
        if value is None and values['boundary_shape_file_path'] is None:
            raise BoundingBoxNotDefinedError()
        if value is not None and values['boundary_shape_file_path'] is None:
            if len(value) != 4:
                raise BoundingBoxLengthError(bounding_box=value)
            elif value[0] >= value[2] or value[1] >= value[3]:
                raise BoundingBoxError(bounding_box=value)
        else:
            boundary_gdf = gpd.read_file(values['boundary_shape_file_path'])
            value = boundary_gdf.total_bounds.astype(np.int32)
        value = tuple(value)
        return value


class Postprocessing(BaseModel):
    sieve_size: Optional[int] = None
    simplify: Optional[bool] = None

    @validator('sieve_size')
    def validate_sieve_size(cls, value):
        """
        | Validates sieve_size defined in the config file.

        :param int or None value: sieve_size
        :returns: validated sieve_size
        :rtype: int or None
        :raises SieveSizeError: if sieve_size is not a number in the range of 0 to 10
        """
        if value is not None:
            if not 0 <= value <= 10:
                raise SieveSizeError(sieve_size=value)
            if value == 0:
                value = None
        return value

    @validator('simplify')
    def validate_simplify(cls, value):
        """
        | Validates simplify defined in the config file.

        :param bool or None value: simplify
        :returns: validated simplify
        :rtype: bool
        """
        if value is None:
            value = False
        return value


class Aggregation(BaseModel):
    tile_size: Optional[Union[int, List[Union[int, None]]]] = None
    shape_file_path: Optional[Union[str, List[Union[str, None]]]] = None

    @validator('tile_size')
    def validate_tile_size(cls, value):
        """
        | Validates tile_size defined in the config file.

        :param int or list[int or None] or None value: tile_size
        :returns: validated tile_size
        :rtype: list[int]
        :raises TileSizeError: if tile_size is not a number greater than 0
        """
        if value is not None:
            if isinstance(value, int):
                value = [value]
            for index, tile_size in enumerate(value):
                if tile_size is not None:
                    if tile_size < 0:
                        raise TileSizeError(tile_size=tile_size)
                    if tile_size == 0:
                        value[index] = None
            value = [tile_size for tile_size in value if tile_size is not None]
            value = list(set(value))
        else:
            value = []
        return value

    @validator('shape_file_path')
    def validate_shape_file_path(cls, value):
        """
        | Validates shape_file_path defined in the config file.

        :param str or list[str or None] or None value: shape_file_path
        :returns: validated shape_file_path
        :rtype: list[str]
        :raises ShapeFileNotFoundError: if shape file at shape_file_path does not exist
        :raises ShapeFileExtensionError: if file extension of shape_file_path is not .shp
        """
        if value is not None:
            if isinstance(value, str):
                value = [value]
            for shape_file_path in value:
                if shape_file_path is not None:
                    if not Path(shape_file_path).is_file():
                        raise ShapeFileNotFoundError(shape_file_path=shape_file_path)
                    elif Path(shape_file_path).suffix != '.shp':
                        raise ShapeFileExtensionError(shape_file_path=shape_file_path)
            value = [shape_file_path_element for shape_file_path_element in value
                     if shape_file_path_element is not None]
            value = list(set(value))
        else:
            value = []
        return value


class ExportSettings(BaseModel):
    output_dir_path: str
    prefix: str
    export_raw_shape_file: Optional[bool] = None

    @validator('output_dir_path')
    def validate_output_dir_path(cls, value):
        """
        | Validates output_dir_path defined in the config file.

        :param str value: output_dir_path
        :returns: validated output_dir_path
        :rtype: str
        :raises OutputDirNotFoundError: if directory at output_dir_path does not exist
        :raises OutputDirNotEmptyError: if directory at output_dir_path is not empty
        """
        if not Path(value).is_dir():
            raise OutputDirNotFoundError(output_dir_path=value)
        for path in Path(value).iterdir():
            if not path.name.startswith('.'):
                if path.suffix != '.log':
                    raise OutputDirNotEmptyError(output_dir_path=value)
        return value

    @validator('prefix')
    def validate_prefix(cls, value):
        """
        | Validates prefix defined in the config file.

        :param str value: prefix
        :returns: validated prefix
        :rtype: str
        :raises PrefixError: if prefix contains only whitespaces or underscores
        """
        value = value.replace(' ', '').rstrip('_')
        if not value:
            raise PrefixError()
        return value

    @validator('export_raw_shape_file')
    def validate_export_raw_shape_file(cls, value):
        """
        | Validates export_raw_shape_file defined in the config file.

        :param bool or None value: export_raw_shape_file
        :returns: validated export_raw_shape_file
        :rtype: bool
        """
        if value is None:
            value = False
        return value


class Config(BaseModel):
    data: Data
    postprocessing: Postprocessing
    aggregation: Aggregation
    export_settings: ExportSettings

    @root_validator
    def validate_export_raw_shape_file(cls, values):
        """
        | Validates export_raw_shape_file defined in the config file.

        :param dict[str, Any] values: config
        :returns: validated config
        :rtype: dict[str, Any]
        """
        if values['postprocessing'].sieve_size is None and values['postprocessing'].simplify is False:
            values['export_settings'].export_raw_shape_file = False
        return values


class ConfigParser:
    def __init__(self, config_file_path):
        """
        | Constructor method

        :param str or Path config_file_path: path to the config file (.yaml)
        :returns: None
        :rtype: None
        """
        self.config_file_path = Path(config_file_path)
        with open(self.config_file_path) as file:
            self.config_dict = yaml.safe_load(file)

    def update_config_dict(self, args):
        """
        | Updates the config dict with the optional parsed arguments.

        :param args: parsed arguments
        :returns: None
        :rtype: None
        """
        if hasattr(args, 'wms_url_rgb'):
            self.config_dict['data']['rgb']['wms_url'] = args.wms_url_rgb
        if hasattr(args, 'wms_layer_rgb'):
            self.config_dict['data']['rgb']['wms_layer'] = args.wms_layer_rgb
        if hasattr(args, 'wms_url_nir'):
            self.config_dict['data']['nir']['wms_url'] = args.wms_url_nir
        if hasattr(args, 'wms_layer_nir'):
            self.config_dict['data']['nir']['wms_layer'] = args.wms_layer_nir
        if hasattr(args, 'epsg_code'):
            self.config_dict['data']['epsg_code'] = args.epsg_code
        if hasattr(args, 'boundary_shape_file_path'):
            self.config_dict['data']['boundary_shape_file_path'] = args.boundary_shape_file_path
        if hasattr(args, 'bounding_box'):
            self.config_dict['data']['bounding_box'] = args.bounding_box

        if hasattr(args, 'sieve_size'):
            self.config_dict['postprocessing']['sieve_size'] = args.sieve_size
        if hasattr(args, 'simplify'):
            self.config_dict['postprocessing']['simplify'] = args.simplify

        if hasattr(args, 'tile_size'):
            self.config_dict['aggregation']['tile_size'] = args.tile_size
        if hasattr(args, 'shape_file_path'):
            self.config_dict['aggregation']['shape_file_path'] = args.shape_file_path

        if hasattr(args, 'output_dir_path'):
            self.config_dict['aggregation']['output_dir_path'] = args.output_dir_path
        if hasattr(args, 'prefix'):
            self.config_dict['aggregation']['prefix'] = args.prefix
        if hasattr(args, 'export_raw_shape_file'):
            self.config_dict['aggregation']['export_raw_shape_file'] = args.export_raw_shape_file

    def parse_config(self):
        """
        | Returns the parsed config.

        :returns: parsed config
        :rtype: Config
        """
        parsed_config = Config(**self.config_dict)
        return parsed_config
