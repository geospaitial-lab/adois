# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from argparse import ArgumentParser
from typing import List, Optional, Union


def get_argument_parser():
    """Returns the argument parser.

    :returns: argument parser
    :rtype: ArgumentParser
    """
    argument_parser = ArgumentParser(description='adois - automatic detection of impervious surfaces')
    argument_parser.add_argument('config_file_path',
                                 type=str,
                                 help='path to the config file (.yaml)')

    argument_parser.add_argument('-d', '--debug',
                                 action='store_true',
                                 help='debug mode')

    argument_parser.add_argument('--wms_url_rgb',
                                 type=str,
                                 help='url of the web map service (rgb)')
    argument_parser.add_argument('--wms_layer_rgb',
                                 type=str,
                                 help='layer of the web map service (rgb)')
    argument_parser.add_argument('--wms_url_nir',
                                 type=str,
                                 help='url of the web map service (nir)')
    argument_parser.add_argument('--wms_layer_nir',
                                 type=str,
                                 help='layer of the web map service (nir)')
    argument_parser.add_argument('--wms_url_ndsm',
                                 type=str,
                                 help='url of the web map service (ndsm)')
    argument_parser.add_argument('--wms_layer_ndsm',
                                 type=str,
                                 help='layer of the web map service (ndsm)')
    argument_parser.add_argument('--epsg_code',
                                 type=int,
                                 help='epsg code of the coordinate reference system')
    argument_parser.add_argument('--boundary_shape_file_path',
                                 type=Optional[str],
                                 help='path to the boundary shape file (.shp)')
    argument_parser.add_argument('--bounding_box',
                                 type=Optional[List[int]],
                                 help='bounding box (x_1, y_1, x_2, y_2)')

    argument_parser.add_argument('--color_codes_ndsm',
                                 type=List[str],
                                 help='color codes for the color mapping')

    argument_parser.add_argument('--sieve_size',
                                 type=Optional[int],
                                 help='sieve size in square meters')
    argument_parser.add_argument('--simplify',
                                 type=Optional[bool],
                                 help='if True, the shape file is simplified using the Douglas-Peucker algorithm')

    argument_parser.add_argument('--tile_size',
                                 type=Optional[Union[int, List[Union[int, None]]]],
                                 help='tile size in meters')
    argument_parser.add_argument('--shape_file_path',
                                 type=Optional[Union[str, List[Union[str, None]]]],
                                 help='path to the boundary shape file (.shp)')

    argument_parser.add_argument('--output_dir_path',
                                 type=str,
                                 help='path to the output directory')
    argument_parser.add_argument('--prefix',
                                 type=str,
                                 help='prefix of the shape file names')
    argument_parser.add_argument('--export_raw_shape_file',
                                 type=Optional[bool],
                                 help='if True, a shape file without postprocessing is exported')
    return argument_parser
