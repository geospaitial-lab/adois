import pytest
from unittest import mock

from src.data.remote_sensing_data_downloader import RemoteSensingDataDownloader


@pytest.fixture(scope='session')
@mock.patch('src.data.remote_sensing_data_downloader.WebMapService', return_value=mock.MagicMock)
def remote_sensing_data_downloader_no_clip_border(_mocked_wms):
    """
    | Returns a remote_sensing_data_downloader instance.
    | Border clipping is not used.

    :returns: remote_sensing_data_downloader
    :rtype: RemoteSensingDataDownloader
    """
    remote_sensing_data_downloader = RemoteSensingDataDownloader(wms_url='https://www.wms.de/wms_url',
                                                                 wms_layer='wms_layer',
                                                                 epsg_code=25832,
                                                                 clip_border=False)
    return remote_sensing_data_downloader


@pytest.fixture(scope='session')
@mock.patch('src.data.remote_sensing_data_downloader.WebMapService', return_value=mock.MagicMock)
def remote_sensing_data_downloader_clip_border(_mocked_wms):
    """
    | Returns a remote_sensing_data_downloader instance.
    | Border clipping is used.

    :returns: remote_sensing_data_downloader
    :rtype: RemoteSensingDataDownloader
    """
    remote_sensing_data_downloader = RemoteSensingDataDownloader(wms_url='https://www.wms.de/wms_url',
                                                                 wms_layer='wms_layer',
                                                                 epsg_code=25832,
                                                                 clip_border=True)
    return remote_sensing_data_downloader
