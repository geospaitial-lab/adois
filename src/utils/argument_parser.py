# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import argparse
from argparse import ArgumentParser
from typing import List, Union


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
    argument_parser.add_argument('-ldp', '--log_dir_path',
                                 type=str,
                                 default=argparse.SUPPRESS,
                                 help='path to the log directory')

    argument_parser.add_argument('--wms_url_rgb',
                                 type=str,
                                 default=argparse.SUPPRESS,
                                 help='url of the web map service (rgb)')
    argument_parser.add_argument('--wms_layer_rgb',
                                 type=str,
                                 default=argparse.SUPPRESS,
                                 help='layer of the web map service (rgb)')
    argument_parser.add_argument('--wms_url_nir',
                                 type=str,
                                 default=argparse.SUPPRESS,
                                 help='url of the web map service (nir)')
    argument_parser.add_argument('--wms_layer_nir',
                                 type=str,
                                 default=argparse.SUPPRESS,
                                 help='layer of the web map service (nir)')
    argument_parser.add_argument('--wms_url_ndsm',
                                 type=str,
                                 default=argparse.SUPPRESS,
                                 help='url of the web map service (ndsm)')
    argument_parser.add_argument('--wms_layer_ndsm',
                                 type=str,
                                 default=argparse.SUPPRESS,
                                 help='layer of the web map service (ndsm)')
    argument_parser.add_argument('--epsg_code',
                                 type=int,
                                 default=argparse.SUPPRESS,
                                 help='epsg code of the coordinate reference system')
    argument_parser.add_argument('--boundary_shape_file_path',
                                 type=str,
                                 nargs='?',
                                 const=None,
                                 default=argparse.SUPPRESS,
                                 help='path to the boundary shape file (.shp)')
    argument_parser.add_argument('--bounding_box',
                                 type=List[int],
                                 nargs='?',
                                 const=None,
                                 default=argparse.SUPPRESS,
                                 help='bounding box (x_1, y_1, x_2, y_2)')

    argument_parser.add_argument('--color_codes_ndsm',
                                 type=List[str],
                                 default=argparse.SUPPRESS,
                                 help='color codes for the color mapping')

    argument_parser.add_argument('--sieve_size',
                                 type=int,
                                 nargs='?',
                                 const=None,
                                 default=argparse.SUPPRESS,
                                 help='sieve size in square meters')
    argument_parser.add_argument('--simplify',
                                 type=bool,
                                 nargs='?',
                                 const=None,
                                 default=argparse.SUPPRESS,
                                 help='if True, the shape file is simplified using the Douglas-Peucker algorithm')

    argument_parser.add_argument('--tile_size',
                                 type=Union[int, List[Union[int, None]]],
                                 nargs='?',
                                 const=None,
                                 default=argparse.SUPPRESS,
                                 help='tile size in meters')
    argument_parser.add_argument('--shape_file_path',
                                 type=Union[str, List[Union[str, None]]],
                                 nargs='?',
                                 const=None,
                                 default=argparse.SUPPRESS,
                                 help='path to the boundary shape file (.shp)')

    argument_parser.add_argument('--output_dir_path',
                                 type=str,
                                 default=argparse.SUPPRESS,
                                 help='path to the output directory')
    argument_parser.add_argument('--prefix',
                                 type=str,
                                 default=argparse.SUPPRESS,
                                 help='prefix of the shape file names')
    argument_parser.add_argument('--export_raw_shape_file',
                                 type=bool,
                                 nargs='?',
                                 const=None,
                                 default=argparse.SUPPRESS,
                                 help='if True, a shape file without postprocessing is exported')
    return argument_parser
