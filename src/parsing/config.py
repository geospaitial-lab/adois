from pathlib import Path
from typing import cast, Self

import geopandas as gpd
import numpy as np
from natsort import natsorted

from pydantic import (
    BaseModel,
    field_validator,
    model_validator,
    ValidationInfo)

from src.data import WebMapService

from src.data.exceptions import (
    WMSEPSGCodeError,
    WMSLayerError)

from src.parsing.exceptions import (
    BoundingBoxLengthError,
    BoundingBoxNotDefinedError,
    BoundingBoxValueError,
    GeoDataEmptyError,
    GeoDataFormatError,
    GeoDataGeometryError,
    GeoDataLoadingError,
    GeoDataNotFoundError,
    GeoDataTypeError,
    OutputDirNotFoundError,
    PrefixError,
    SieveSizeError,
    TileSizeError)


class WMS(BaseModel):
    url: str
    layer: str

    # noinspection PyNestedDecorators
    @field_validator('url')
    @classmethod
    def validate_url(cls,
                     value: str) -> str:
        """
        | Validates url.

        :param value: url
        :returns: validated url
        """
        _ = WebMapService(url=value)
        return value

    # noinspection PyNestedDecorators
    @field_validator('layer')
    @classmethod
    def validate_layer(cls,
                       value: str,
                       values: ValidationInfo) -> str:
        """
        | Validates layer.

        :param value: layer
        :param values: values
        :returns: validated layer
        :raises WMSLayerError: if layer is not a valid layer
        """
        web_map_service = WebMapService(url=values.data['url'])
        layers_valid = web_map_service.get_layers()

        if value not in layers_valid:
            raise WMSLayerError(layer=value,
                                layers_valid=layers_valid)

        return value


class Data(BaseModel):
    rgb: WMS
    nir: WMS
    epsg_code: int
    path_boundary: str | None = None
    bounding_box: list[int] | None = None
    apply_padding: bool = False
    ignore_processed_tiles: bool = False

    # noinspection PyNestedDecorators
    @field_validator('epsg_code')
    @classmethod
    def validate_epsg_code(cls,
                           value: int,
                           values: ValidationInfo) -> int:
        """
        | Validates epsg_code.

        :param value: epsg_code
        :param values: values
        :returns: validated epsg_code
        :raises WMSEPSGCodeError: if epsg_code is not a valid epsg code
        """
        web_map_service_rgb = WebMapService(url=values.data['rgb'].url)
        web_map_service_nir = WebMapService(url=values.data['nir'].url)

        epsg_codes_valid_rgb = web_map_service_rgb.get_epsg_codes(values.data['rgb'].layer)
        epsg_codes_valid_nir = web_map_service_nir.get_epsg_codes(values.data['nir'].layer)

        epsg_codes_valid = list(set(epsg_codes_valid_rgb) & set(epsg_codes_valid_nir))

        if value not in epsg_codes_valid:
            raise WMSEPSGCodeError(epsg_code=value,
                                   epsg_codes_valid=epsg_codes_valid)

        return value

    # noinspection PyNestedDecorators
    @field_validator('path_boundary')
    @classmethod
    def validate_path_boundary(cls,
                               value: str | None) -> Path | None:
        """
        | Validates path_boundary.

        :param value: path_boundary
        :returns: validated path_boundary
        :raises GeoDataEmptyError: if the geo data is empty
        :raises GeoDataFormatError: if the file extension of the geo data is not .gpkg or .shp
        :raises GeoDataGeometryError: if the geo data contains invalid polygons
        :raises GeoDataLoadingError: if an exception is raised while loading the geo data
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

    # noinspection PyNestedDecorators
    @field_validator('bounding_box')
    @classmethod
    def validate_bounding_box(cls,
                              value: list[int] | None,
                              values: ValidationInfo) -> tuple[int, int, int, int]:
        """
        | Validates bounding_box.

        :param value: bounding_box
        :param values: values
        :returns: validated bounding_box
        :raises BoundingBoxLengthError: if the length of bounding_box is not equal to 4
        :raises BoundingBoxNotDefinedError: if neither path_boundary nor bounding_box are defined in the config
        :raises BoundingBoxValueError: if x_min >= x_max or y_min >= y_max
        """
        if value is None and values.data['path_boundary'] is None:
            raise BoundingBoxNotDefinedError()

        if values.data['path_boundary'] is None:
            if len(value) != 4:
                raise BoundingBoxLengthError(bounding_box=value)

            if value[0] >= value[2] or value[1] >= value[3]:
                raise BoundingBoxValueError(bounding_box=value)

        else:
            boundary = gpd.read_file(Path(values.data['path_boundary']))
            bounding_box_boundary = boundary.total_bounds

            value = (
                [int(np.floor(bounding_box_boundary[0])),
                 int(np.floor(bounding_box_boundary[1])),
                 int(np.ceil(bounding_box_boundary[2])),
                 int(np.ceil(bounding_box_boundary[3]))])

        value = tuple(value)
        value = cast(tuple[int, int, int, int], value)
        return value

    # noinspection PyNestedDecorators
    @field_validator('apply_padding')
    @classmethod
    def validate_apply_padding(cls,
                               value: bool | None) -> bool:
        """
        | Validates apply_padding.

        :param value: apply_padding
        :returns: validated apply_padding
        """
        if value is None:
            value = False

        return value

    # noinspection PyNestedDecorators
    @field_validator('ignore_processed_tiles')
    @classmethod
    def validate_ignore_processed_tiles(cls,
                                        value: bool | None) -> bool:
        """
        | Validates ignore_processed_tiles.

        :param value: ignore_processed_tiles
        :returns: validated ignore_processed_tiles
        """
        if value is None:
            value = False

        return value


class Postprocessing(BaseModel):
    sieve_size: int | None = None
    simplify: bool = False

    # noinspection PyNestedDecorators
    @field_validator('sieve_size')
    @classmethod
    def validate_sieve_size(cls,
                            value: int | None) -> int | None:
        """
        | Validates sieve_size.

        :param value: sieve_size
        :returns: validated sieve_size
        :raises SieveSizeError: if sieve_size is not a number in the range of 0 to 10
        """
        if value is None:
            return value

        if not 0 <= value <= 10:
            raise SieveSizeError(sieve_size=value)

        if value == 0:
            value = None

        return value

    # noinspection PyNestedDecorators
    @field_validator('simplify')
    @classmethod
    def validate_simplify(cls,
                          value: bool | None) -> bool:
        """
        | Validates simplify.

        :param value: simplify
        :returns: validated simplify
        """
        if value is None:
            value = False

        return value


class Aggregation(BaseModel):
    tile_size: int | list[int | None] | None = []
    path_aggregation_areas: str | list[str | None] | None = []

    # noinspection PyNestedDecorators
    @field_validator('tile_size')
    @classmethod
    def validate_tile_size(cls,
                           value: int | list[int | None] | None) -> list[int]:
        """
        | Validates tile_size.

        :param value: tile_size
        :returns: validated tile_size
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

    # noinspection PyNestedDecorators
    @field_validator('path_aggregation_areas')
    @classmethod
    def validate_path_aggregation_areas(cls,
                                        value: str | list[str | None] | None) -> list[Path]:
        """
        | Validates path_aggregation_areas.

        :param value: path_aggregation_areas
        :returns: validated path_aggregation_areas
        :raises GeoDataEmptyError: if the geo data is empty
        :raises GeoDataFormatError: if the file extension of the geo data is not .gpkg or .shp
        :raises GeoDataGeometryError: if the geo data contains invalid polygons
        :raises GeoDataLoadingError: if an exception is raised while loading the geo data
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


class Export(BaseModel):
    path_output_dir: str
    prefix: str

    # noinspection PyNestedDecorators
    @field_validator('path_output_dir')
    @classmethod
    def validate_path_output_dir(cls,
                                 value: str) -> Path:
        """
        | Validates path_output_dir.

        :param value: path_output_dir
        :returns: validated path_output_dir
        :raises OutputDirNotFoundError: if the output directory does not exist
        """
        value = Path(value)

        if not value.is_dir():
            raise OutputDirNotFoundError(path=value)

        return value

    # noinspection PyNestedDecorators
    @field_validator('prefix')
    @classmethod
    def validate_prefix(cls,
                        value: str) -> str:
        """
        | Validates prefix.

        :param value: prefix
        :returns: validated prefix
        :raises PrefixError: if prefix contains only whitespaces or underscores
        """
        value = value.replace(' ', '').rstrip('_')

        if not value:
            raise PrefixError()

        return value


class Config(BaseModel):
    data: Data
    postprocessing: Postprocessing = Postprocessing()
    aggregation: Aggregation = Aggregation()
    export: Export

    @model_validator(mode='after')
    def validate_tile_size(self) -> Self:
        """
        | Validates tile_size.

        :returns: validated values
        """
        if not self.aggregation.tile_size:
            return self

        tile_size_max = min(self.data.bounding_box[2] - self.data.bounding_box[0],
                            self.data.bounding_box[3] - self.data.bounding_box[1])

        self.aggregation.tile_size = [tile_size
                                      for tile_size in self.aggregation.tile_size
                                      if tile_size <= tile_size_max]

        return self
