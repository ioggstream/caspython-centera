"""
Test for CRUD methods.
"""
import contextlib
from time import ctime
import tempfile
import shutil

from Filepool.connector import CenteraConnection, str_to_seconds
from nose.plugins.skip import SkipTest
from nose.tools import *

from setup import log
from setup import POOL_ADDRESS

POOL_INFO = (
"infoVersion", "capacity", "freeSpace", "clusterid", "clusterName", "version", "replicaAddress",)

CLIP_ATTRIBUTES = ['refid', 'name', 'modification.date', 'totalsize', 'clusterid', 'modification.profile',
                       'creation.date', 'retention.period', 'numfiles', 'prev.clip', 'creation.poolid',
                       'modification.poolid', 'numtags', 'creation.profile', 'type', 'sdk.version',
                       'clip.naming.scheme']

context = type('TestContext', (object,), {})


@contextlib.contextmanager
def make_temp_directory():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


class TestConnectorList(object):

    def setup(self):
        self.connection = CenteraConnection(POOL_ADDRESS)

    def teardown(self):
        self.connection.close()

    def test_connection(self):
        assert self.connection
        assert all(getattr(self.connection.pool, x) for x in POOL_INFO), "Missing entry in connection pool."

    def test_get_attributes_ok(self):
        clip_id = "035DVUIOVKS4KeBNOO59IDCTC69G41A2O2RQ1103A64Q7NPLGE3DR"

        clip = self.connection.get(clip_id)
        assert clip.attributes
        for a in CLIP_ATTRIBUTES:
            assert a in clip.attributes, "Missing attribute %r" % a

    @SkipTest  # This works, but skip as it requires showing logs or monkey-patching connection to evaluate.
    def test_list_handle_exception(self):
        clips = self.connection.list(limit=5)
        n_clips = 0
        for c in clips:
            raise AssertionError("Mock exception to be nicely mangled.")

    def test_list_limit(self):
        clips = self.connection.list(limit=5)
        n_clips = 0
        for c in clips:
            log.warning("Get clip id %r", c.getClipId())
            n_clips += 1
        assert n_clips == 5

    def test_list_date(self):
        clips = self.connection.list(start='2014-12-05', limit=5)
        n_clips = 0
        for c in clips:
            timestamp = c.getTimestamp()
            log.warning("Get clip id %r with timestamp %r (%r)", c.getClipId(), timestamp, ctime(timestamp / 1000))
            assert timestamp > 1417734000000
            n_clips += 1
        assert n_clips == 5


def test_parse_date():
    def harn_date(date, expected):
        seconds = str_to_seconds(date)
        assert seconds == expected
    for date in ['2015-12-05', '20151205', '2015/12/05', '2015 05 Dec',
                 '2015-12-05 00:00:00', '2015-12-05 00:00']:
        yield harn_date, date, 1449270000


def test_parse_dayonly():
    for day in ('5', '05'):
        seconds = str_to_seconds(day)
        yield assert_true, seconds


def test_parse_dayonly_unsupported():
    for day in ('1205', '0512'):
        try:
            seconds = str_to_seconds(day)
            assert False, "Should raise ValueError: %r" % day
        except ValueError:
            pass