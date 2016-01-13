"""

Helper functions for Filepool.

Author: roberto.polli@par-tec.it
License: GPLv2
"""
from time import mktime
from dateutil import parser as dateparser
from ConfigParser import ConfigParser

__author__ = 'roberto.polli@par-tec.it'


def str_to_seconds(date):
    """
    Return seconds since utc from the given datestring.

    :param date: a human-readable string parsed by dateutil.parser.
    :return: seconds since utc.
    :raises: ValueError if the parsed date is < 1970
    """
    return int(mktime(dateparser.parse(date).timetuple()))


def parse_config(config_file):
    """
    Parse a config file.
    :param config_file:
    :return:
    """
    config = ConfigParser()
    config.read(config_file)
    return dict(
            (section, dict(config.items(section)))
                 for section in config.sections()
    )
