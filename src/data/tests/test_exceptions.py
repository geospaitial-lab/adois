import pytest

from src.data.exceptions import (
    WMSConnectionError,
    WMSEPSGCodeError,
    WMSError,
    WMSFetchingError,
    WMSLayerError)

from .data.data_test_exceptions import (
    data_test_WMSEPSGCodeError,
    data_test_WMSLayerError)


def test_WMSError_default():
    """
    | Tests the default message of WMSError.

    :returns: None
    :rtype: None
    """
    expected = 'Invalid web map service in the config!'

    with pytest.raises(WMSError, match=expected):
        raise WMSError()


def test_WMSError():
    """
    | Tests WMSError.

    :returns: None
    :rtype: None
    """
    message = 'Test message.'

    expected = 'Test message.'

    with pytest.raises(WMSError, match=expected):
        raise WMSError(message=message)


def test_WMSConnectionError():
    """
    | Tests WMSConnectionError.

    :returns: None
    :rtype: None
    """
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
def test_WMSEPSGCodeError(test_input,
                          expected):
    """
    | Tests WMSEPSGCodeError.

    :param (int, list[int]) test_input: epsg_code, epsg_codes_valid
    :param str expected: message
    :returns: None
    :rtype: None
    """
    with pytest.raises(WMSEPSGCodeError, match=expected):
        raise WMSEPSGCodeError(epsg_code=test_input[0],
                               epsg_codes_valid=test_input[1])


def test_WMSFetchingError():
    """
    | Tests WMSFetchingError.

    :returns: None
    :rtype: None
    """
    url = 'https://invalid.wms.com'
    passed_exception = Exception('Test message.')

    expected = (
        r'An exception is raised while fetching the image from the web map service \(https://invalid.wms.com\).\n'
        'Test message.')

    with pytest.raises(WMSFetchingError, match=expected):
        raise WMSFetchingError(url=url,
                               passed_exception=passed_exception)


@pytest.mark.parametrize('test_input, expected', data_test_WMSLayerError)
def test_WMSLayerError(test_input,
                       expected):
    """
    | Tests WMSLayerError.

    :param (str, list[str]) test_input: layer, layers_valid
    :param str expected: message
    :returns: None
    :rtype: None
    """
    with pytest.raises(WMSLayerError, match=expected):
        raise WMSLayerError(layer=test_input[0],
                            layers_valid=test_input[1])
