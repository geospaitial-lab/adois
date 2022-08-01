# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from pathlib import Path


def create_tiles_dir(output_dir_path):
    """Creates a hidden .tiles directory in the output directory.

    :param str or Path output_dir_path: path to the output directory
    :returns: None
    :rtype: None
    """
    output_dir_path = Path(output_dir_path)
    (output_dir_path / '.tiles').mkdir(exist_ok=True)


def create_dir_structure(output_dir_path,
                         export_raw_shp,
                         tile_sizes,
                         shp_paths):
    """Creates the directory structure in the output directory.

    :param str or Path output_dir_path: path to the output directory
    :param bool export_raw_shp: if True, a shape file without postprocessing is exported
    :param list[int] tile_sizes: tile sizes of the grid in meters for aggregation
    :param list[str] shp_paths: paths to the shape files for aggregation
    :returns: None
    :rtype: None
    """
    output_dir_path = Path(output_dir_path)
    (output_dir_path / 'impervious_surfaces').mkdir()

    if export_raw_shp:
        (output_dir_path / 'impervious_surfaces_raw').mkdir()

    if tile_sizes or shp_paths:
        (output_dir_path / 'impervious_surfaces_aggregated').mkdir()

        for tile_size in tile_sizes:
            (output_dir_path / 'impervious_surfaces_aggregated' / f'grid_{tile_size}m').mkdir()

        for shp_Path in shp_paths:
            (output_dir_path / 'impervious_surfaces_aggregated' / Path(shp_Path).stem).mkdir()
