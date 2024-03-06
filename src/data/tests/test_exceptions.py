import pytest

from src.data.exceptions import (
    WMSConnectionError,
    WMSEPSGCodeError,
    WMSError,
    WMSFetchingError,
    WMSLayerError)

from .data.data_test_exceptions import data_test_WMSEPSGCodeError, data_test_WMSLayerError


def test_WMSError_default() -> None:
    expected = 'Invalid web map service in the config!'

    with pytest.raises(WMSError, match=expected):
        raise WMSError()


def test_WMSError() -> None:
    message = 'Test message.'

    expected = 'Test message.'

    with pytest.raises(WMSError, match=expected):
        raise WMSError(message=message)


def test_WMSConnectionError() -> None:
    url = 'https://invalid.wms.com'
    passed_exception = Exception('Test message.')

    expected = (
        r'Invalid url in the config!\n'
        r'An exception is raised while connecting to the web map service \(https://invalid.wms.com\).\n'
        'Test message.')

    with pytest.raises(WMSConnectionError, match=expected):
        raise WMSConnectionError(url=url,
                                 passed_exception=passed_exception)


@pytest.mark.parametrize('test_input, expected', data_test_WMSEPSGCodeError)
def test_WMSEPSGCodeError(test_input: tuple[int, list[int]],
                          expected: str) -> None:
    """
    :param test_input: epsg_code, epsg_codes_valid
    :param expected: message
    """
    with pytest.raises(WMSEPSGCodeError, match=expected):
        raise WMSEPSGCodeError(epsg_code=test_input[0],
                               epsg_codes_valid=test_input[1])


def test_WMSFetchingError() -> None:
    url = 'https://invalid.wms.com'
    passed_exception = Exception('Test message.')

    expected = (
        r'An exception is raised while fetching the image from the web map service \(https://invalid.wms.com\).\n'
        'Test message.')

    with pytest.raises(WMSFetchingError, match=expected):
        raise WMSFetchingError(url=url,
                               passed_exception=passed_exception)


@pytest.mark.parametrize('test_input, expected', data_test_WMSLayerError)
def test_WMSLayerError(test_input: tuple[str, list[str]],
                       expected: str) -> None:
    """
    :param test_input: layer, layers_valid
    :param expected: message
    """
    with pytest.raises(WMSLayerError, match=expected):
        raise WMSLayerError(layer=test_input[0],
                            layers_valid=test_input[1])
