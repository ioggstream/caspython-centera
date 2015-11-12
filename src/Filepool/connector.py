"""
Wrapper class for managing clips on centera.
"""
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
from contextlib import closing
from os.path import normpath, abspath, basename, isfile, isdir
import logging

POOL_DEFAULT_OPTIONS = {
    FPLibrary.FP_OPTION_EMBEDDED_DATA_THRESHOLD: 100 * 1024L
}


class CenteraConnection(object):

    """
    Manage the clips from a pool.
    :param object:
    :return:
    """

    def __init__(self, pool_ip, options=POOL_DEFAULT_OPTIONS, application=("caspython-centera-library", "1.0")):
        """
        Initialize a pool
        :param host:
        :param options:
        :param application: a couple (appname, version) attached to the clip_id
        :return:
        """
        self.log = logging.getLogger()
        self.pool = FPPool(pool_ip)
        for k, v in options.items():
            self.pool.setGlobalOption(k, v)

        # getPoolInfo sets infos in self.pool.
        self.pool.getPoolInfo()
        # the application will be attached to the clip id
        self.pool.registerApplication(*application)

    def close(self):
        self.pool.close()

    def put(self, clip_name, files, retention_sec):
        """
        Writes a clip and attached files to worm.

        :param clip_name:
        :param files:
        :param retention_sec:
        :return:
        """
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
    def clean_tag(filename):
        return "mytag_" + basename(filename).replace("@", "_")

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

    def list(self, start=None, end=None):
        """
        List clips in the given interval.
        :param start:
        :param end:
        :return:
        """
        raise NotImplementedError
