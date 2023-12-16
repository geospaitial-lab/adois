from natsort import natsorted


class WMSError(Exception):

    def __init__(self,
                 message='Invalid web map service in the config!'):
        """
        | Initializer method

        :param str message: message
        :returns: None
        :rtype: None
        """
        super().__init__(message)


class WMSConnectionError(WMSError):

    def __init__(self,
                 url,
                 passed_exception):
        """
        | Initializer method

        :param str url: url
        :param Exception passed_exception: passed exception
        :returns: None
        :rtype: None
        """
        message = (
            'Invalid url in the config!\n'
            f'An exception is raised while connecting to the web map service ({url}).\n'
            f'{passed_exception}')

        super().__init__(message)


class WMSEPSGCodeError(WMSError):

    def __init__(self,
                 epsg_code,
                 epsg_codes_valid):
        """
        | Initializer method

        :param int epsg_code: epsg code
        :param list[int] epsg_codes_valid: valid epsg codes
        :returns: None
        :rtype: None
        """
        if len(epsg_codes_valid) == 1:
            epsg_codes_valid = epsg_codes_valid[0]
        else:
            epsg_codes_valid = natsorted(epsg_codes_valid)

            epsg_codes_valid = (
                f"{', '.join(map(str, epsg_codes_valid[:-1]))} "
                f'or {epsg_codes_valid[-1]}')

        message = (
            'Invalid epsg_code in the config!\n'
            f'Expected {epsg_codes_valid}, got {epsg_code} instead.')

        super().__init__(message)


class WMSFetchingError(WMSError):

    def __init__(self,
                 url,
                 passed_exception):
        """
        | Initializer method

        :param str url: url
        :param Exception passed_exception: passed exception
        :returns: None
        :rtype: None
        """
        message = (
            f'An exception is raised while fetching the image from the web map service ({url}).\n'
            f'{passed_exception}')

        super().__init__(message)


class WMSLayerError(WMSError):

    def __init__(self,
                 layer,
                 layers_valid):
        """
        | Initializer method

        :param str layer: layer
        :param list[str] layers_valid: valid layers
        :returns: None
        :rtype: None
        """
        if len(layers_valid) == 1:
            layers_valid = layers_valid[0]
        else:
            layers_valid = natsorted(layers_valid)
            layers_valid = (
                f"{', '.join(map(str, layers_valid[:-1]))} "
                f'or {layers_valid[-1]}')

        message = (
            'Invalid layer in the config!\n'
            f'Expected {layers_valid}, got {layer} instead.')

        super().__init__(message)
