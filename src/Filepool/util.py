"""

Helper functions for Filepool.

Author: roberto.polli@par-tec.it
License: GPLv2
"""
from time import mktime
from dateutil import parser as dateparser

__author__ = 'roberto.polli@par-tec.it'


def str_to_seconds(date):
    """
    Return seconds since utc from the given datestring.

    :param date: a human-readable string parsed by dateutil.parser.
    :return: seconds since utc.
    """
    return int(mktime(dateparser.parse(date).timetuple()))
