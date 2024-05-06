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
                                                                 epsg_code=25832,
                                                                 clip_border=False)

    assert isinstance(remote_sensing_data_downloader, RemoteSensingDataDownloader)
    assert list(remote_sensing_data_downloader.__dict__.keys()) == ['wms', 'wms_layer', 'epsg_code', 'clip_border']
    assert isinstance(remote_sensing_data_downloader.wms, type(mock.MagicMock))
    mocked_wms.assert_called_once_with('https://www.wms.de/wms_url')
    assert isinstance(remote_sensing_data_downloader.wms_layer, str)
    assert remote_sensing_data_downloader.wms_layer == 'wms_layer'
    assert isinstance(remote_sensing_data_downloader.epsg_code, int)
    assert remote_sensing_data_downloader.epsg_code == 25832
    assert isinstance(remote_sensing_data_downloader.clip_border, bool)
    assert remote_sensing_data_downloader.clip_border is False


@pytest.mark.parametrize('test_input, expected', parameters_get_bounding_box_no_clip_border)
def test_get_bounding_box_no_clip_border(test_input,
                                         expected,
                                         remote_sensing_data_downloader_no_clip_border):
    """
    | Tests get_bounding_box() with different coordinates.
    | Border clipping is not used.

    :param (int, int) test_input: coordinates (x, y)
    :param (int, int, int, int) expected: bounding box (x_1, y_1, x_2, y_2)
    :returns: None
    :rtype: None
    """
    bounding_box = remote_sensing_data_downloader_no_clip_border.get_bounding_box(coordinates=test_input)

    for bounding_box_element in bounding_box:
        assert isinstance(bounding_box_element, int)

    assert bounding_box == expected


@pytest.mark.parametrize('test_input, expected', parameters_get_bounding_box_clip_border)
def test_get_bounding_box_clip_border(test_input,
                                      expected,
                                      remote_sensing_data_downloader_clip_border):
    """
    | Tests get_bounding_box() with different coordinates.
    | Border clipping is used.

    :param (int, int) test_input: coordinates (x, y)
    :param (int, int, int, int) expected: bounding box (x_1, y_1, x_2, y_2)
    :returns: None
    :rtype: None
    """
    bounding_box = remote_sensing_data_downloader_clip_border.get_bounding_box(coordinates=test_input)

    for bounding_box_element in bounding_box:
        assert isinstance(bounding_box_element, int)

    assert bounding_box == expected


@mock.patch('src.data.remote_sensing_data_downloader.WebMapService', return_value=mock.MagicMock)
def test_get_response_no_clip_border(mocked_wms):
    """
    | Tests get_response() with a mocked web map service.
    | Border clipping is not used.

    :param mock.MagicMock mocked_wms: mocked web map service
    :returns: None
    :rtype: None
    """
    remote_sensing_data_downloader = RemoteSensingDataDownloader(wms_url='https://www.wms.de/wms_url',
                                                                 wms_layer='wms_layer',
                                                                 epsg_code=25832,
                                                                 clip_border=False)

    mocked_wms_instance = mocked_wms.return_value
    mocked_wms_instance.getmap = mock.MagicMock()

    remote_sensing_data_downloader.get_response(bounding_box=(0, 0, 256, 256))

    mocked_wms_instance.getmap.assert_called_once_with(layers=['wms_layer'],
                                                       srs='EPSG:25832',
                                                       bbox=(0, 0, 256, 256),
                                                       format='image/png',
                                                       size=(1280, 1280),
                                                       bgcolor='#000000')


@mock.patch('src.data.remote_sensing_data_downloader.WebMapService', return_value=mock.MagicMock)
def test_get_response_clip_border(mocked_wms):
    """
    | Tests get_response() with a mocked web map service.
    | Border clipping is used.

    :param mock.MagicMock mocked_wms: mocked web map service
    :returns: None
    :rtype: None
    """
    remote_sensing_data_downloader = RemoteSensingDataDownloader(wms_url='https://www.wms.de/wms_url',
                                                                 wms_layer='wms_layer',
                                                                 epsg_code=25832,
                                                                 clip_border=True)

    mocked_wms_instance = mocked_wms.return_value
    mocked_wms_instance.getmap = mock.MagicMock()

    remote_sensing_data_downloader.get_response(bounding_box=(-64, -64, 320, 320))

    mocked_wms_instance.getmap.assert_called_once_with(layers=['wms_layer'],
                                                       srs='EPSG:25832',
                                                       bbox=(-64, -64, 320, 320),
                                                       format='image/png',
                                                       size=(1920, 1920),
                                                       bgcolor='#000000')


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
                                                                 epsg_code=25832,
                                                                 clip_border=False)

    mocked_get_response.return_value = mocked_response

    image = remote_sensing_data_downloader.get_image(coordinates=(0, 256))

    with Image.open(DATA_DIR_PATH / 'data_test_get_image.tiff') as file:
        # noinspection PyTypeChecker
        expected = np.array(file, dtype=np.uint8)

    mocked_get_response.assert_called_once_with((0, 0, 256, 256))
    assert image.dtype == expected.dtype
    np.testing.assert_array_equal(image, expected)
