from datetime import datetime as DateTime  # PEP8 compliant
from datetime import timedelta as TimeDelta  # PEP8 compliant
from pathlib import Path

import geopandas as gpd
import yaml


def create_tiles_dir(output_dir_path):
    """
    | Creates a hidden .tiles directory in the output directory.

    :param str or Path output_dir_path: path to the output directory
    :returns: None
    :rtype: None
    """
    output_dir_path = Path(output_dir_path)
    (output_dir_path / '.tiles').mkdir(exist_ok=True)


def create_dir_structure(output_dir_path,
                         export_raw_shape_file,
                         tile_sizes,
                         shape_file_paths):
    """
    | Creates the directory structure in the output directory.

    :param str or Path output_dir_path: path to the output directory
    :param bool export_raw_shape_file: if True, a shape file without postprocessing is exported
    :param list[int] tile_sizes: tile sizes of the grid in meters for aggregation
    :param list[str] shape_file_paths: paths to the shape files for aggregation
    :returns: None
    :rtype: None
    """
    output_dir_path = Path(output_dir_path)
    (output_dir_path / 'impervious_surfaces').mkdir()

    if export_raw_shape_file:
        (output_dir_path / 'impervious_surfaces_raw').mkdir()

    if tile_sizes or shape_file_paths:
        (output_dir_path / 'impervious_surfaces_aggregated').mkdir()

        for tile_size in tile_sizes:
            (output_dir_path / 'impervious_surfaces_aggregated' / f'grid_{tile_size}m').mkdir()

        for shape_file_path in shape_file_paths:
            (output_dir_path / 'impervious_surfaces_aggregated' / Path(shape_file_path).stem).mkdir()


def chop(time_delta):
    """
    | Returns a time delta with chopped microseconds.

    :param TimeDelta time_delta: time delta
    :return: chopped time delta
    :rtype: TimeDelta
    """
    return time_delta - TimeDelta(microseconds=time_delta.microseconds)


def get_metadata(config,
                 start_time,
                 end_time):
    """
    | Returns metadata.

    :param dict config: config
    :param DateTime start_time: start time
    :param DateTime end_time: end time
    :returns: metadata
    :rtype dict
    """
    time_delta = chop(end_time - start_time)

    metadata = {'general': {'time stamp': str(start_time.isoformat(sep='_', timespec='seconds')),
                            'execution time': str(time_delta)},
                'config': config}
    return metadata


class CustomDumper(yaml.Dumper):
    def increase_indent(self,
                        flow=False,
                        indentless=False):
        """
        | Fixes the indentation of lists.
        |
        | Based on:
        | https://stackoverflow.com/a/39681672

        :returns: None
        :rtype: None
        """
        super().increase_indent(flow, False)

    def write_line_break(self, data=None):
        """
        | Adds a blank line between top level keys.
        |
        | Based on:
        | https://github.com/yaml/pyyaml/issues/127#issuecomment-525800484

        :returns: None
        :rtype: None
        """
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


def export(output_dir_path,
           export_raw_shape_file,
           raw_gdf,
           postprocessed_gdf,
           prefix,
           tile_sizes,
           aggregation_gdfs_grid,
           shape_file_paths,
           aggregation_gdfs_shape_file,
           metadata):
    """
    | Exports the shape files to their corresponding directories in the output directory.

    :param str or Path output_dir_path: path to the output directory
    :param bool export_raw_shape_file: if True, a shape file without postprocessing is exported
    :param gpd.GeoDataFrame raw_gdf: raw geodataframe
    :param gpd.GeoDataFrame postprocessed_gdf: postprocessed geodataframe
    :param str prefix: prefix of the shape file names
    :param list[int] tile_sizes: tile sizes of the grid in meters for aggregation
    :param list[(gpd.GeoDataFrame, dict[str, OrderedDict[str, str] or str])] aggregation_gdfs_grid: geodataframes
        with statistical values of the aggregated geodataframe and its shape file schema
    :param list[str] shape_file_paths: paths to the shape files for aggregation
    :param list[(gpd.GeoDataFrame, dict[str, OrderedDict[str, str] or str])] aggregation_gdfs_shape_file: geodataframes
        with statistical values of the aggregated geodataframe and its shape file schema
    :param dict[str, Any] metadata: metadata
    :returns: None
    :rtype: None
    """
    output_dir_path = Path(output_dir_path)
    shape_file_path = output_dir_path / 'impervious_surfaces' / f'{prefix}_impervious_surfaces.shp'

    if postprocessed_gdf is not None:
        postprocessed_gdf.to_file(str(shape_file_path))
    else:
        raw_gdf.to_file(str(shape_file_path))

    if export_raw_shape_file:
        raw_shape_file_path = output_dir_path / 'impervious_surfaces_raw' / f'{prefix}_impervious_surfaces_raw.shp'
        raw_gdf.to_file(str(raw_shape_file_path))

    for index, tile_size in enumerate(tile_sizes):
        path = (output_dir_path / 'impervious_surfaces_aggregated' / f'grid_{tile_size}m' /
                f'{prefix}_impervious_surfaces_aggregated_grid_{tile_size}m.shp')
        aggregation_gdfs_grid[index][0].to_file(str(path), schema=aggregation_gdfs_grid[index][1])

    for index, shape_file_path in enumerate(shape_file_paths):
        path = (output_dir_path / 'impervious_surfaces_aggregated' / Path(shape_file_path).stem /
                f'{prefix}_impervious_surfaces_aggregated_{Path(shape_file_path).stem}.shp')
        aggregation_gdfs_shape_file[index][0].to_file(str(path), schema=aggregation_gdfs_shape_file[index][1])

    with open(output_dir_path / 'metadata.yaml', 'w') as yaml_file:
        yaml.dump(data=metadata,
                  stream=yaml_file,
                  Dumper=CustomDumper,
                  default_flow_style=False,
                  sort_keys=False)
