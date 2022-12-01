# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from unittest import mock

import pytest

from src.data.remote_sensing_data_downloader import RemoteSensingDataDownloader
from src.data.tests.data import *


@mock.patch('src.data.remote_sensing_data_downloader.WebMapService', return_value=mock.MagicMock)
def test_init(mocked_wms):
    """
    | Tests __init__() with a mocked web map service.

    :param mock.MagicMock mocked_wms: mocked web map service
    :returns: None
    :rtype: None
    """
    remote_sensing_data_downloader = RemoteSensingDataDownloader(wms_url='https://www.wms.de/wms_url',
                                                                 wms_layer='wms_layer',
                                                                 epsg_code=25832)

    assert isinstance(remote_sensing_data_downloader, RemoteSensingDataDownloader)
    assert list(remote_sensing_data_downloader.__dict__.keys()) == ['wms', 'wms_layer', 'epsg_code']
    assert isinstance(remote_sensing_data_downloader.wms, type(mock.MagicMock))
    mocked_wms.assert_called_once_with('https://www.wms.de/wms_url')
    assert isinstance(remote_sensing_data_downloader.wms_layer, str)
    assert remote_sensing_data_downloader.wms_layer == 'wms_layer'
    assert isinstance(remote_sensing_data_downloader.epsg_code, int)
    assert remote_sensing_data_downloader.epsg_code == 25832


@pytest.mark.parametrize('test_input, expected', parameters_get_bounding_box)
def test_get_bounding_box(test_input, expected):
    """
    | Tests get_bounding_box() with different coordinates.

    :param (int, int) test_input: coordinates (x, y)
    :param (int, int, int, int) expected: bounding box (x_1, y_1, x_2, y_2)
    :returns: None
    :rtype: None
    """
    bounding_box = RemoteSensingDataDownloader.get_bounding_box(coordinates=test_input)

    for bounding_box_element in bounding_box:
        assert isinstance(bounding_box_element, int)

    assert bounding_box == expected


@pytest.mark.skip(reason='TODO')
def test_get_image():
    """
    | Tests get_image().

    :returns: None
    :rtype: None
    """
    pass
