# @author: Maryniak, Marius - Fachbereich Elektrotechnik, Westfälische Hochschule Gelsenkirchen

import logging
import sys
import traceback as tb

import src.utils as utils

logger = logging.getLogger('main_logger')


def exception_handler_production(exception_type, exception_message, _traceback):
    """
    | Logs exceptions without the traceback for production purposes.

    :param Exception exception_type: exception type
    :param Exception exception_message: exception message
    :param _traceback: traceback
    :returns: None
    :rtype: None
    """
    logger.critical(f'{exception_type.__name__}: {exception_message}')


def exception_handler_debug(exception_type, exception_message, traceback):
    """
    | Logs exceptions with the traceback for debugging purposes.

    :param Exception exception_type: exception type
    :param Exception exception_message: exception message
    :param traceback: traceback
    :returns: None
    :rtype: None
    """
    logger.critical(f'{exception_type.__name__}\n  '
                    f"Traceback (most recent call last):\n{''.join(tb.format_tb(traceback))}\n  "
                    f'{exception_type.__name__}: {exception_message}')


def set_exception_hook():
    """
    | Sets the exception hook to an exception handler (either for production or debugging purposes).

    :returns: None
    :rtype: None
    """
    if utils.DEBUG:
        sys.excepthook = exception_handler_debug
    else:
        sys.excepthook = exception_handler_production
