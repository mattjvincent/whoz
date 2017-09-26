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

from collections import OrderedDict
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


def dictify_row(cursor, row):
    """
    Turns the given row into a dictionary where the keys are the column names.

    :param cursor: the database cursor
    :param row: the current row
    :return: dictionary with keys being column names
    """
    d = OrderedDict()
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


def dictify_cursor(cursor):
    """
    Converts all cursor rows into dictionaries where the keys are the column names.

    :param cursor: the database cursor
    :return: dictionary with keys being column names
    """
    return (dictify_row(cursor, row) for row in cursor)


def format_time(start, end):
    """
    Format length of time between start and end.

    :param start: the start time
    :param end: the end time
    :return: a formatted string of hours, minutes, and seconds
    """
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)
