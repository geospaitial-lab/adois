# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from pathlib import Path
import re
from typing import List, Optional

import pydantic
import yaml
from owslib.wms import WebMapService
from pydantic import validator

from src.utils.config_parser_exceptions import *


class BaseModel(pydantic.BaseModel):
    class Config:
        allow_mutation = False


class Wms(BaseModel):
    wms_url: str
    wms_layer: str

    @validator('wms_url')
    def validate_wms_url(cls, value):
        """Validates wms_url defined in the config file.

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
        """Validates wms_layer defined in the config file.

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
    ndsm: Wms
    epsg_code: int
    image_size: int
    bounding_box: List[int]

    @validator('epsg_code')
    def validate_epsg_code(cls,
                           value,
                           values):
        """Validates epsg_code defined in the config file.

        :param int value: epsg_code
        :param dict[str, Any] values: config
        :returns: validated epsg_code
        :rtype: int
        :raises EPSGCodeError: if epsg_code is not in the valid epsg codes of the web map services
        """
        wms_rgb = WebMapService(values['rgb'].wms_url)
        wms_nir = WebMapService(values['nir'].wms_url)
        wms_ndsm = WebMapService(values['ndsm'].wms_url)
        valid_epsg_codes_rgb = [int(epsg_code[5:]) for epsg_code in wms_rgb[values['rgb'].wms_layer].crsOptions]
        valid_epsg_codes_nir = [int(epsg_code[5:]) for epsg_code in wms_nir[values['nir'].wms_layer].crsOptions]
        valid_epsg_codes_ndsm = [int(epsg_code[5:]) for epsg_code in wms_ndsm[values['ndsm'].wms_layer].crsOptions]
        valid_epsg_codes = list(set(valid_epsg_codes_rgb) & set(valid_epsg_codes_nir) & set(valid_epsg_codes_ndsm))

        if value not in valid_epsg_codes:
            raise EPSGCodeError(epsg_code=value,
                                valid_epsg_codes=valid_epsg_codes)
        return value

    @validator('image_size')
    def validate_image_size(cls, value):
        """Validates image_size defined in the config file.

        :param int value: image_size
        :returns: validated image_size
        :rtype: int
        :raises ImageSizeError: if image_size is not an even number in the range of 512 to 2560
        """
        if not 512 <= value <= 2560 or value % 2:
            raise ImageSizeError(image_size=value)
        return value

    @validator('bounding_box')
    def validate_bounding_box(cls, value):
        """Validates bounding_box defined in the config file.

        :param list[int] value: bounding_box (x_1, y_1, x_2, y_2)
        :returns: validated bounding_box
        :rtype: (int, int, int, int)
        :raises BoundingBoxLengthError: if the length of bounding_box is not equal to 4
        :raises BoundingBoxError: if x_1 >= x_2 or y_1 >= y_2
        """
        if len(value) != 4:
            raise BoundingBoxLengthError(bounding_box=value)
        if value[0] >= value[2] or value[1] >= value[3]:
            raise BoundingBoxError(bounding_box=value)
        value = tuple(value)
        return value


class Preprocessing(BaseModel):
    color_codes_ndsm: List[str]

    @validator('color_codes_ndsm')
    def validate_color_codes_ndsm(cls, value):
        """Validates color_codes_ndsm defined in the config file.

        :param list[str] value: color_codes_ndsm
        :returns: validated color_codes_ndsm
        :rtype: dict[tuple[int, int, int], int]
        :raises ColorCodeNDSMError: if color_code in color_codes_ndsm is not a color code with the following schema:
            '(r_value, g_value, b_value) - mapped_value'
        """
        color_codes_ndsm = {}
        pattern = re.compile(r'^\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*-\s*(\d+)\s*$')

        for color_code in value:
            match = pattern.search(color_code)
            if match is None:
                raise ColorCodeNDSMError(color_code=color_code)
            else:
                r_value = int(match.group(1))
                g_value = int(match.group(2))
                b_value = int(match.group(3))
                mapped_value = int(match.group(4))
                color_codes_ndsm[(r_value, g_value, b_value)] = int(mapped_value)
        value = color_codes_ndsm
        return value


class Postprocessing(BaseModel):
    sieve_size: Optional[int] = None
    simplify: Optional[bool] = None

    @validator('sieve_size')
    def validate_sieve_size(cls, value):
        """Validates sieve_size defined in the config file.

        :param int value: sieve_size
        :returns: validated sieve_size
        :rtype: int
        :raises SieveSizeError: if sieve_size is not a number in the range of 0 to 1e4
        """
        if value is not None:
            if not 0 <= value <= 1e4:
                raise SieveSizeError(sieve_size=value)
            if value == 0:
                value = None
        return value

    @validator('simplify')
    def validate_simplify(cls, value):
        """Validates simplify defined in the config file.

        :param bool or None value: simplify
        :returns: validated simplify
        :rtype: bool
        """
        if value is None:
            value = False
        return value


class Config(BaseModel):
    data: Data
    preprocessing: Preprocessing
    postprocessing: Postprocessing


class ConfigParser:
    def __init__(self, config_file_path):
        """Constructor method

        :param str or Path config_file_path: path to the config file (.yaml)
        :returns: None
        :rtype: None
        """
        self.config_file_path = Path(config_file_path)
        with open(self.config_file_path) as file:
            self.config_dict = yaml.safe_load(file)

    def parse_config(self):
        """Returns the parsed config.

        :returns: parsed config
        :rtype: Config
        """
        parsed_config = Config(**self.config_dict)
        return parsed_config
