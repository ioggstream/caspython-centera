"""
Wrapper class for managing clips on centera.
"""
from contextlib import closing
from os.path import normpath, abspath, basename, isfile, isdir
import logging
from time import sleep
import re

from Filepool.FPPool import FPPool
from Filepool.FPLibrary import FPLibrary
from Filepool.FPQueryExpression import FPQueryExpression
from Filepool.FPQuery import FPQuery
from Filepool.FPQueryResult import FPQueryResult
from Filepool.FPLibrary import FPLibrary
from Filepool.FPPool import FPPool
from Filepool.FPException import FPException
from Filepool.FPNetException import FPNetException
from Filepool.FPServerException import FPServerException
from Filepool.FPClientException import FPClientException
from Filepool.FPClip import FPClip
from Filepool.FPTag import FPTag
from Filepool.FPFileInputStream import FPFileInputStream
from Filepool.FPBufferInputStream import FPBufferInputStream
from Filepool.FPRetention import FPRetention
from Filepool.FPFileOutputStream import FPFileOutputStream
from Filepool.FPBufferOutputStream import FPBufferOutputStream
from Filepool.util import str_to_seconds, longval

_version = "1.3rc6"
# Customize mytag to override issues in tag names (eg. eclip).s
#MYTAG_ = "mytag_"
MYTAG_ = ""

SEC_TO_MILLISEC = 1000

POOL_DEFAULT_OPTIONS = {
    FPLibrary.FP_OPTION_EMBEDDED_DATA_THRESHOLD: 100 * longval(1024)
}
RE_INVALID_TAGS = [
    (re.compile(r'^[^a-zA-Z]'), 'TAG must start with a letter.'),
    (re.compile(r'^eclip'), 'TAG starting with "eclip" are reserved for internal Centera use.'),
]

class CenteraConnection(object):

    """
    Manage the clips from a pool.
    :param object:
    :return:
    """

    def __init__(self, pool_ip, options=POOL_DEFAULT_OPTIONS, application=("caspython-centera-library", _version), replace=None):
        """
        Initialize a pool
        :param host:
        :param options:
        :param application: a couple (appname, version) attached to the clip_id
        :param replace: a translation map for replacing unsupported characters
        :return:
        """
        self.log = logging.getLogger(__name__)
        self.pool = FPPool(pool_ip)
        for k, v in options.items():
            self.pool.setGlobalOption(k, v)

        # getPoolInfo sets infos in self.pool.
        self.pool.getPoolInfo()
        # the application will be attached to the clip id
        self.pool.registerApplication(*application)

    def close(self):
        for i in range(3):
            try:
                self.pool.close()
                return
            except FPClientException as e:
                if e.errorString == 'FP_OBJECTINUSE_ERR':
                    self.log.error("Closing while pool still in use. Sleeping for 1 sec.")
                    sleep(1)
                    continue
                raise

    def put(self, clip_name, files, retention_sec):
        """
        Writes a clip and attached files to worm.

        :param clip_name:
        :param files:
        :param retention_sec:
        :return:
        """
        for f in files:
            self.validate_tag(f)

        with closing(FPClip(self.pool, clip_name, close_retries=3)) as clip:
            clip.setRetentionPeriod(long(retention_sec))
            top_handle = clip.getTopTag()
            for filename in files:
                tag_name = self.clean_tag(filename)
                with closing(FPTag(top_handle,  tag_name)) as blob_tag:
                    with closing(FPFileInputStream(filename, 16 * 1024)) as fh:
                        blob_tag.blobWrite(fh.stream, 0)
            clip_id = clip.write()

        return clip_id

    @staticmethod
    def validate_tag(filename):
        """
        Check if a filename is a valid centera tag name.
        :param filename:
        :return: None on succes
        :raises: ValueError if not valid
        """
        for re_m, msg in RE_INVALID_TAGS:
            if re_m.match(CenteraConnection.clean_tag(filename)):
                raise ValueError(msg)

    @staticmethod
    def clean_tag(filename):
        return MYTAG_ + basename(filename)  # .replace("@", "_")

    def get(self, clip_id, tag=None):
        """
        Get a (closed) clip from worm.

        While storing or retrieving tags from worm,
        you may need to set a close_retry.
        :param clip:
        :return:
        """
        with closing(FPClip(self.pool, close_retries=3 if tag else 0)) as clip:
            self._open_or_not_found(clip, clip_id)

            clip.attributes = clip.getDescriptionAttributes()
            if tag:
                clip.tags = [x for x in clip.getTags()]
            return clip

    def get(self, clip_id, tag=None):
        """
        Get a (closed) clip from worm.

        While storing or retrieving tags from worm,
        you may need to set a close_retry.
        :param clip:
        :return:
        """
        with closing(FPClip(self.pool, close_retries=3 if tag else 0)) as clip:
            self._open_or_not_found(clip, clip_id)

            clip.attributes = clip.getDescriptionAttributes()
            if tag:
                clip.tags = [x for x in clip.getTags()]
            return clip

    def download(self, clip_id, tag_name, outfile):
        """

        :param clip_id:
        :param tag_name:
        :param outfile:
        :return: the output file if present. None if not found.
        """
        outfile = normpath(abspath(outfile))
        with closing(FPClip(self.pool, close_retries=3)) as clip:
            self._open_or_not_found(clip, clip_id)

            for blob_id in clip.getBlobs():
                with closing(FPTag(blob_id)) as blob_tag:
                    blob_tag_name = blob_tag.getTagName()
                    if blob_tag_name != tag_name:
                        self.log.debug(
                            "Skipping tag: %s when looking for: %s", blob_tag_name, blob_tag)
                        continue

                    if blob_tag.getBlobSize() < 1:
                        self.log.debug("Empty blob %s" % blob_tag_name)
                        raise ValueError()

                    with closing(FPFileOutputStream(outfile)) as fh:
                        self.log.info(
                            "Writing blob %s to %s", blob_tag_name, outfile)
                        blob_tag.blobRead(fh.stream, 0)

                    return outfile

    def _open_or_not_found(self, clip, clip_id):
        try:
            clip.open(clip_id)
        except FPClientException as e:
            if e.errorString == 'FP_PARAM_ERR':
                raise KeyError(
                    "Wrong parameter detected or ClipID not found: %r" % clip_id)
            raise

    def list(self, start=None, end=None, limit=0):
        """
        Retrieve clips in the given interval.
        NOTE: Once iterated, the result is closed, so you cannot access the
        item any more!


        @see https://www.emc.com/collateral/TechnicalDocument/docu59169.pdf
        :param start:
        :param end:
        :param limit: max number of entries to retrieve. default 0 (unlimited).
        :return:
        """
        # 0 means unlimited.
        if limit == 0:
            limit = -1

        # Open and close FPQuery
        with closing(self._open_query(start, end)) as query:
            status = 0
            while limit != 0:
                # Implements point 5-7 opening and closing the FPQueryResult.
                with closing(FPQueryResult(query.fetchResult(0))) as res:
                    status = res.getResultCode()

                    if status in (
                        FPLibrary.FP_QUERY_RESULT_CODE_END,
                        FPLibrary.FP_QUERY_RESULT_CODE_ABORT,
                        FPLibrary.FP_QUERY_RESULT_CODE_ERROR,
                        FPLibrary.FP_QUERY_RESULT_CODE_INCOMPLETE,
                        FPLibrary.FP_QUERY_RESULT_CODE_COMPLETE
                    ):
                        break
                    elif status == FPLibrary.FP_QUERY_RESULT_CODE_PROGRESS:
                        continue
                    elif status == FPLibrary.FP_QUERY_RESULT_CODE_OK:
                        limit -= 1
                        # Implements point 6
                        yield res

    def _open_query(self, start=None, end=None, qtype=FPLibrary.FP_QUERY_TYPE_EXISTING):
        """
        Open a FPQuery and its associated QueryExpression as stated in the doc.
        The caller is in charge of closing the query.

        Implements points 1, 2, 3, 4, 10 of https://www.emc.com/collateral/TechnicalDocument/docu59169.pdf

        :param start:
        :param end:
        :param qtype:
        :return:
        """
        query_expression = FPQueryExpression()
        query_expression.setType(qtype)
        if start:
            query_expression.setStartTime(str_to_seconds(start) * SEC_TO_MILLISEC)
        if end:
            query_expression.setEndTime(str_to_seconds(end) * SEC_TO_MILLISEC)

        try:
            query = FPQuery(self.pool)
            query.open(query_expression)
            return query
        finally:
            query_expression.close()

    def info(self):
        """
        Return a dictionary with essential informations about the centera,
        like free space, replication options, ...

        :return: dict
        """

        fields = [ 'clusterid', 'clusterName', 'version', 'infoVersion',
                   'capacity', 'freeSpace', 'replicaAddress' ]
        self.pool.getPoolInfo()
        ret = dict((f, getattr(self.pool, f)) for f in fields )
        ret['clusterTime'] = self.pool.getClusterTime()
        return ret

