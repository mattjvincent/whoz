# -*- coding: utf-8 -*-
#
# TODO: CHANGE LOGGING
#
# I DON'T LIKE THIS METHOD OF LOGGING
#
# I WANTED A VERBOSE METHOD, BUT DIDN'T WANT TO ADD A NEW LEVEL
#
# THUS...
#
# logging.WARNING is informational
# logging.INFO is user debug
# logging.DEBUG is developer debug
#

import logging
logging.basicConfig(format='[whoz] [%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def get_logger():
    """
    Get the logger.

    :return: logger
    """
    return logging.getLogger(__name__)


def configure_logging(level):
    """
    Configure the logger.

    :param level: 0 = WARNING, 1 = INFO, 2 = DEBUG
    :return: Nothing
    """
    if level == 0:
        get_logger().setLevel(logging.WARN)
    elif level == 1:
        get_logger().setLevel(logging.INFO)
    elif level > 1:
        get_logger().setLevel(logging.DEBUG)


