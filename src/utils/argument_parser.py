import argparse
from argparse import ArgumentParser


def get_argument_parser():
    """
    | Returns the argument parser.

    :returns: argument parser
    :rtype: ArgumentParser
    """
    argument_parser = ArgumentParser(description='adois - automatic detection of impervious surfaces')
    argument_parser.add_argument('config_file_path',
                                 type=str,
                                 help='path to the config file (.yaml)')

    # region data
    argument_parser.add_argument('-d', '--debug',
                                 action='store_true',
                                 help='debug mode')
    argument_parser.add_argument('-ict', '--ignore_cached_tiles',
                                 action='store_true',
                                 help='ignore cached tiles')

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
    argument_parser.add_argument('--epsg_code',
                                 type=int,
                                 default=argparse.SUPPRESS,
                                 help='epsg code of the coordinate reference system')
    argument_parser.add_argument('--boundary_shape_file_path',
                                 type=str,
                                 default=argparse.SUPPRESS,
                                 help='path to the boundary shape file (.shp)')
    argument_parser.add_argument('--no-boundary_shape_file_path',
                                 action='store_const',
                                 const=None,
                                 dest='boundary_shape_file_path',
                                 default=argparse.SUPPRESS,
                                 help='set the path to the boundary shape file (.shp) to None')
    argument_parser.add_argument('--bounding_box',
                                 type=int,
                                 nargs=4,
                                 default=argparse.SUPPRESS,
                                 help='bounding box (x_1, y_1, x_2, y_2)')
    argument_parser.add_argument('--no-bounding_box',
                                 action='store_const',
                                 const=None,
                                 dest='bounding_box',
                                 default=argparse.SUPPRESS,
                                 help='set the bounding box (x_1, y_1, x_2, y_2) to None')
    # endregion

    # region postprocessing
    argument_parser.add_argument('--sieve_size',
                                 type=int,
                                 default=argparse.SUPPRESS,
                                 help='sieve size in square meters')
    argument_parser.add_argument('--no-sieve_size',
                                 action='store_const',
                                 const=None,
                                 dest='sieve_size',
                                 default=argparse.SUPPRESS,
                                 help='set the sieve size in square meters to None')
    argument_parser.add_argument('--simplify',
                                 action='store_true',
                                 default=argparse.SUPPRESS,
                                 help='set simplify (the shape file is simplified using the Douglas-Peucker algorithm) '
                                      'to True')
    argument_parser.add_argument('--no-simplify',
                                 action='store_false',
                                 dest='simplify',
                                 default=argparse.SUPPRESS,
                                 help='set simplify (the shape file is simplified using the Douglas-Peucker algorithm) '
                                      'to False')
    # endregion

    # region aggregation
    argument_parser.add_argument('--tile_size',
                                 type=int,
                                 nargs='*',
                                 default=argparse.SUPPRESS,
                                 help='tile size in meters')
    argument_parser.add_argument('--no-tile_size',
                                 action='store_const',
                                 const=None,
                                 dest='tile_size',
                                 default=argparse.SUPPRESS,
                                 help='set the tile size in meters to None')
    argument_parser.add_argument('--shape_file_path',
                                 type=str,
                                 nargs='*',
                                 default=argparse.SUPPRESS,
                                 help='path to the boundary shape file (.shp)')
    argument_parser.add_argument('--no-shape_file_path',
                                 action='store_const',
                                 const=None,
                                 dest='shape_file_path',
                                 default=argparse.SUPPRESS,
                                 help='set the path to the boundary shape file (.shp) to None')
    # endregion

    # region export settings
    argument_parser.add_argument('--output_dir_path',
                                 type=str,
                                 default=argparse.SUPPRESS,
                                 help='path to the output directory')
    argument_parser.add_argument('--prefix',
                                 type=str,
                                 default=argparse.SUPPRESS,
                                 help='prefix of the shape file names')
    argument_parser.add_argument('--export_raw_shape_file',
                                 action='store_true',
                                 default=argparse.SUPPRESS,
                                 help='set the export of the raw shape file to True')
    argument_parser.add_argument('--no-export_raw_shape_file',
                                 action='store_false',
                                 dest='export_raw_shape_file',
                                 default=argparse.SUPPRESS,
                                 help='set the export of the raw shape file to False')
    # endregion
    return argument_parser
