import unittest.mock as mock
from typing import cast

import pytest

from src.data.remote_sensing_data_fetcher import RemoteSensingDataFetcher
from src.data.web_map_service import WebMapServiceProtocol


@pytest.fixture(scope='function')
def remote_sensing_data_fetcher_with_mocked_web_map_service(
        mocked_web_map_service: WebMapServiceProtocol) -> tuple[RemoteSensingDataFetcher, WebMapServiceProtocol]:
    """
    | Returns a remote sensing data fetcher object with a mocked web map service.

    :param mocked_web_map_service: mocked web map service fixture
    :returns: remote sensing data fetcher fixture
    """
    remote_sensing_data_fetcher = RemoteSensingDataFetcher(web_map_service=mocked_web_map_service,
                                                           layer='test_layer',
                                                           epsg_code=25832)

    return remote_sensing_data_fetcher, mocked_web_map_service


@pytest.fixture(scope='function')
def mocked_web_map_service() -> WebMapServiceProtocol:
    """
    | Returns a mocked web map service object.

    :returns: mocked web map service fixture
    """
    mocked_web_map_service = mock.Mock(spec=WebMapServiceProtocol)
    mocked_web_map_service = cast(WebMapServiceProtocol, mocked_web_map_service)
    mocked_web_map_service.url = 'https://wms.com'
    return mocked_web_map_service
