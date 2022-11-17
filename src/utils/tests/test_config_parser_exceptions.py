# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import pytest

from src.utils.config_parser_exceptions import *
from src.utils.tests.data import tests_data


def test_WMSConnectionError():
    """
    | Tests WMSConnectionError exception.

    :returns: None
    :rtype: None
    """
    with pytest.raises(WMSConnectionError, match=r'No connection to WMS \(https://www.wms.de/wms_url\) in config_file!'
                                                 r'\n  Passed exception\.'):
        raise WMSConnectionError(wms_url='https://www.wms.de/wms_url',
                                 passed_exception=Exception('Passed exception.'))


@pytest.mark.parametrize('test_input, expected', tests_data.parameters_WMSLayerError)
def test_WMSLayerError(test_input, expected):
    """
    | Tests WMSLayerError exception with a different number of layers.

    :param list[str] test_input: valid layers
    :param str expected: exception message
    :returns: None
    :rtype: None
    """
    with pytest.raises(WMSLayerError, match=expected):
        raise WMSLayerError(wms_layer='invalid_wms_layer',
                            wms_url='https://www.wms.de/wms_url',
                            valid_wms_layers=test_input)


@pytest.mark.parametrize('test_input, expected', tests_data.parameters_EPSGCodeError)
def test_EPSGCodeError(test_input, expected):
    """
    | Tests EPSGCodeError exception with a different number of epsg codes.

    :param list[int] test_input: valid epsg codes
    :param str expected: exception message
    :returns: None
    :rtype: None
    """
    with pytest.raises(EPSGCodeError, match=expected):
        raise EPSGCodeError(epsg_code=0,
                            valid_epsg_codes=test_input)


def test_ShapeFileNotFoundError():
    """
    | Tests ShapeFileNotFoundError exception.

    :returns: None
    :rtype: None
    """
    with pytest.raises(ShapeFileNotFoundError, match=r'Invalid path to the shape file in shape_file_path '
                                                     r'in config file!'
                                                     r'\n  Shape file at /path/to/shape_file.shp does not exist\.'):
        raise ShapeFileNotFoundError(shape_file_path='/path/to/shape_file.shp')


def test_ShapeFileExtensionError():
    """
    | Tests ShapeFileExtensionError exception.

    :returns: None
    :rtype: None
    """
    with pytest.raises(ShapeFileExtensionError, match=r'Invalid path to the shape file in shape_file_path '
                                                      r'in config file!'
                                                      r'\n  Expected file extension .shp, got .py instead\.'):
        raise ShapeFileExtensionError(shape_file_path='/path/to/shape_file.py')


def test_ShapeFileLengthError(invalid_boundary_gdf):
    """
    | Tests ShapeFileLengthError exception.

    :returns: None
    :rtype: None
    """
    with pytest.raises(ShapeFileLengthError, match=r'Invalid shape file in shape_file_path in config file!'
                                                   r'\n  Expected shape file with 1 polygon, got 4 polygons instead\.'):
        raise ShapeFileLengthError(gdf=invalid_boundary_gdf)


def test_BoundingBoxNotDefinedError():
    """
    | Tests BoundingBoxNotDefinedError exception.

    :returns: None
    :rtype: None
    """
    with pytest.raises(BoundingBoxNotDefinedError, match=r'Neither boundary_shape_file_path nor bounding_box '
                                                         r'are defined in config file!'):
        raise BoundingBoxNotDefinedError()


def test_BoundingBoxLengthError():
    """
    | Tests BoundingBoxLengthError exception.

    :returns: None
    :rtype: None
    """
    with pytest.raises(BoundingBoxLengthError, match=r'Invalid bounding_box in config file!'
                                                     r'\n  Expected 4 coordinates \(x_1, y_1, x_2, y_2\), '
                                                     r'got 5 coordinates instead\.'):
        raise BoundingBoxLengthError(bounding_box=[0, 1, 2, 3, 4])


def test_BoundingBoxError():
    """
    | Tests BoundingBoxError exception.

    :returns: None
    :rtype: None
    """
    with pytest.raises(BoundingBoxError, match=r'Invalid bounding_box in config file!'
                                               r'\n  Expected 4 coordinates \(x_1, y_1, x_2, y_2\) '
                                               r'with x_1 \< x_2 and y_1 \< y_2, got \(1, 1, 0, 0\) instead\.'):
        raise BoundingBoxError(bounding_box=[1, 1, 0, 0])


def test_SieveSizeError():
    """
    | Tests SieveSizeError exception.

    :returns: None
    :rtype: None
    """
    with pytest.raises(SieveSizeError, match=r'Invalid sieve_size in config file!'
                                             r'\n  Expected a number in the range of 0 to 10, got 16 instead\.'):
        raise SieveSizeError(sieve_size=16)


def test_TileSizeError():
    """
    | Tests TileSizeError exception.

    :returns: None
    :rtype: None
    """
    with pytest.raises(TileSizeError, match=r'Invalid tile_size in config file!'
                                            r'\n  Expected a number greater than 0, got -1 instead\.'):
        raise TileSizeError(tile_size=-1)


def test_OutputDirNotFoundError():
    """
    | Tests OutputDirNotFoundError exception.

    :returns: None
    :rtype: None
    """
    with pytest.raises(OutputDirNotFoundError, match=r'Invalid output_dir_path in config file!'
                                                     r'\n  Directory at /path/to/output_dir does not exist\.'):
        raise OutputDirNotFoundError(output_dir_path='/path/to/output_dir')


def test_OutputDirNotEmptyError():
    """
    | Tests OutputDirNotEmptyError exception.

    :returns: None
    :rtype: None
    """
    with pytest.raises(OutputDirNotEmptyError, match=r'Invalid output_dir_path in config file!'
                                                     r'\n  Directory at /path/to/output_dir is not empty\.'):
        raise OutputDirNotEmptyError(output_dir_path='/path/to/output_dir')


def test_PrefixError():
    """
    | Tests PrefixError exception.

    :returns: None
    :rtype: None
    """
    with pytest.raises(PrefixError, match=r'Invalid prefix in config file!'
                                          r'\n  String contains only whitespaces or underscores\.'):
        raise PrefixError()
