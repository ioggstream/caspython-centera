"""

Helper functions for Filepool.

Author: roberto.polli@par-tec.it
License: GPLv2
"""
import sys
from time import mktime
from dateutil import parser as dateparser
if (sys.version_info > (3, 0)):
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser

__author__ = 'roberto.polli@par-tec.it'


def longval(val):
    if (sys.version_info > (3, 0)):
        return val
    return longvalue = long(1024)

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
