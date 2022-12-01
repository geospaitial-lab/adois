# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

from io import BytesIO
from pathlib import Path
from unittest import mock

import numpy as np
import pytest
from PIL import Image

from src.data.remote_sensing_data_downloader import RemoteSensingDataDownloader
from src.data.tests.data import *

DATA_DIR_PATH = Path(__file__).resolve().parents[0] / 'data'

with BytesIO() as output:
    Image.open(DATA_DIR_PATH / 'data_test_get_image.tiff').save(output, format='TIFF')
    mocked_response = output.getvalue()


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


@mock.patch('src.data.remote_sensing_data_downloader.WebMapService', return_value=mock.MagicMock)
@mock.patch.object(RemoteSensingDataDownloader, 'get_response')
def test_get_image(mocked_get_response, _mocked_wms):
    """
    | Tests get_image() with a mocked get_response() and a mocked web map service.

    :param mock.MagicMock mocked_get_response: mocked get_response()
    :param mock.MagicMock _mocked_wms: mocked web map service
    :returns: None
    :rtype: None
    """
    remote_sensing_data_downloader = RemoteSensingDataDownloader(wms_url='https://www.wms.de/wms_url',
                                                                 wms_layer='wms_layer',
                                                                 epsg_code=25832)

    mocked_get_response.return_value = mocked_response

    image = remote_sensing_data_downloader.get_image(coordinates=(0, 0))

    with Image.open(DATA_DIR_PATH / 'data_test_get_image.tiff') as file:
        # noinspection PyTypeChecker
        expected = np.array(file, dtype=np.uint8)

    assert image.dtype == expected.dtype
    np.testing.assert_array_equal(image, expected)
