from src.data.remote_sensing_data_fetcher import RemoteSensingDataFetcher
from src.data.web_map_service import WebMapServiceProtocol  # noqa: F401 (used for type hinting)


def test_init(mocked_web_map_service):
    """
    | Tests __init__().

    :param WebMapServiceProtocol mocked_web_map_service: mocked web map service fixture
    :returns: None
    :rtype: None
    """
    layer = 'layer_test'
    epsg_code = 25832

    remote_sensing_data_fetcher = RemoteSensingDataFetcher(web_map_service=mocked_web_map_service,
                                                           layer=layer,
                                                           epsg_code=epsg_code)

    assert isinstance(remote_sensing_data_fetcher, RemoteSensingDataFetcher)
    attributes = ['web_map_service', 'layer', 'epsg_code']
    assert list(vars(remote_sensing_data_fetcher).keys()) == attributes

    assert remote_sensing_data_fetcher.web_map_service.url == 'https://wms.com'
    assert isinstance(remote_sensing_data_fetcher.layer, str)
    assert remote_sensing_data_fetcher.layer == layer
    assert isinstance(remote_sensing_data_fetcher.epsg_code, int)
    assert remote_sensing_data_fetcher.epsg_code == epsg_code
