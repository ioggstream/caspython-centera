"""
Test for CRUD methods.
"""
import contextlib
from Filepool.connector import CenteraConnection
from nose.tools import *
from os.path import isfile, basename
import tempfile
import shutil
import os
from setup import log, POOL_ADDRESS

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


class TestConnector(object):

    def setup(self):
        self.connection = CenteraConnection(POOL_ADDRESS)

    def teardown(self):
        self.connection.pool.close()

    def test_connection(self):
        assert self.connection
        assert all(getattr(self.connection.pool, x) for x in POOL_INFO), "Missing entry in connection pool."

    def test_info(self):
        assert 'clusterid' in self.connection.info()

    def test_get_attributes_ok(self):
        clip_id = "035DVUIOVKS4KeBNOO59IDCTC69G41A2O2RQ1103A64Q7NPLGE3DR"

        clip = self.connection.get(clip_id)
        assert clip.attributes
        for a in CLIP_ATTRIBUTES:
            assert a in clip.attributes, "Missing attribute %r" % a

    @raises(KeyError)
    def test_get_missing(self):
        clip_id = "MISSING_CLIP"
        clip = self.connection.get(clip_id)

    def test_get_tags_ok(self):
        clip_id = "1VF9AAIA4J9KMe7EJHA08MA3T1CG41A2O529350VD49RO9J33MT7A"
        expected_tags = 1

        clip = self.connection.get(clip_id, tag=True)
        assert clip.tags
        assert len(clip.tags) == expected_tags

    def test_download_small(self):
        clip_id = "035DVUIOVKS4KeBNOO59IDCTC69G41A2O2RQ1103A64Q7NPLGE3DR"
        tag_name = "mytag_1.xml"

        outfile = self.connection.download(clip_id, tag_name=tag_name, outfile="/tmp/file.out")
        assert len(open(outfile).read()) > 10

    def test_download_big(self):
        clip_id = "5KOC492PCL2QQe7E4R41ON43M03G41A2O526FO02CH29Q0P6B3OP6"
        tag_name = "file"
        outfile = "/tmp/file.out"
        if isfile(outfile):
            os.unlink(outfile)
        outfile = self.connection.download(clip_id, tag_name=tag_name, outfile=outfile)
        assert len(open(outfile).read()) > 10

    def test_put_one_small(self):
        expected_attributes = {
            'retention.period': '10',
            'name': 'test_put_one',
            'totalsize': '1234'
        }
        with tempfile.NamedTemporaryFile() as tf:
            tf.write("x" * 1234)
            tf.flush()
            clip_id = self.connection.put("test_put_one", files=[tf.name], retention_sec=10)
            assert clip_id

        clip = self.connection.get(clip_id, tag=True)
        assert clip.attributes
        print((clip_id, clip.attributes, clip.tags))
        for k, v in expected_attributes.items():
            assert_equal(clip.attributes.get(k), v)

    def test_put_many_small(self):
        expected_attributes = {
            'retention.period': 10,
            'name': 'test_put_one',
            'totalsize': '1234'
        }

        with make_temp_directory() as tmpdir:
            # Create 5 files to be added to the clip.
            files = [os.path.join(tmpdir, "x%d.xml" % i) for i in range(3)]
            files.extend([os.path.join(tmpdir, "noextension_%d" % i) for i in range(3)])

            for f in files:
                with open(f, "wb") as tf:
                    tf.write("x" * 1234)

            clip_id = self.connection.put("test_put_many_small", files=files, retention_sec=10)
            assert clip_id

        clip = self.connection.get(clip_id, tag=True)
        assert clip.attributes
        print((clip_id, clip.attributes, clip.tags))
        # All added files should be present as tag names.
        #  FIXME: check filename normalization.
        for f in files:
            assert basename(f) in dict(clip.tags), "%r %r" % (dict(clip.tags).keys(), basename(f))

    @raises(ValueError)
    def test_put_unsupported_files(self):
        expected_attributes = {
            'retention.period': 10,
            'name': 'test_put_one',
            'totalsize': '1234'
        }

        with make_temp_directory() as tmpdir:
            # Create files to be added to the clip.
            files = [os.path.join(tmpdir, "%d.xml" % i) for i in range(3)]
            for f in files:
                with open(f, "wb") as tf:
                    tf.write("x" * 1234)

            clip_id = self.connection.put("test_put_many_small", files=files, retention_sec=10)
            assert clip_id

        clip = self.connection.get(clip_id, tag=True)
        assert clip.attributes
        print((clip_id, clip.attributes, clip.tags))
        # All added files should be present as tag names.
        #  FIXME: check filename normalization.
        for f in files:
            assert basename(f) in dict(clip.tags), "%r %r" % (dict(clip.tags).keys(), basename(f))


def test_validate_tags():
    def assert_invalid_tags(filename):
        try:
            CenteraConnection.validate_tag(filename)
            assert False, "File is not valid: %r" % filename
        except ValueError:
            pass

    for f in ("eclip.xml", "1.xml", "2.xml", "11111111111111.xml", "@.xml", "1@2.xml"):
        yield assert_invalid_tags, f
