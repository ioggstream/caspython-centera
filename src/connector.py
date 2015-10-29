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
        self.pool = FPPool(pool_ip)
        for k, v in options.items():
            self.pool.setGlobalOption(k, v)

        # getPoolInfo sets infos in self.pool.
        self.pool.getPoolInfo()
        # the application will be attached to the clip id
        self.pool.registerApplication(*application)

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
                filename = filename.replace("@", "_")
                with closing(FPTag(top_handle, "mytag_" + basename(filename))) as blob_tag:
                    with closing(FPFileInputStream(filename, 16 * 1024)) as fh:
                        blob_tag.blobWrite(fh.stream, 0)
            clip_id = clip.write()

        return clip_id

    def get(self, clip_id, tag=None):
        """
        Get a (closed) clip from worm.

        While storing or retrieving tags from worm,
        you may need to set a close_retry.
        :param clip:
        :return:
        """
        with closing(FPClip(self.pool, close_retries=3 if tag else 0)) as clip:
            try:
                clip.open(clip_id)
            except FPClientException as e:
                if e.errorString == 'FP_PARAM_ERR':
                    raise KeyError("Wrong parameter detected or ClipID not found: %r" % clip_id)
                raise

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
            try:
                clip.open(clip_id)
            except FPClientException as e:
                if e.errorString == 'FP_PARAM_ERR':
                    raise KeyError("Wrong parameter detected or ClipID not found: %r" % clip_id)
                raise

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
            try:
                clip.open(clip_id)
            except FPClientException as e:
                if e.errorString == 'FP_PARAM_ERR':
                    raise KeyError("Wrong parameter detected or ClipID not found: %r" % clip_id)
                raise

            for i in range(clip.getNumBlobs() + 1):
                blob_id = clip.fetchNext()
                if not blob_id:
                    break
                with closing(FPTag(blob_id)) as blob_tag:
                    tag_name_l = blob_tag.getTagName()
                    print("tag:", blob_tag, tag_name_l)
                    if tag_name_l != tag_name:
                        continue

                    if blob_tag.getBlobSize() < 1:
                        print("Empty blob %s" % i)
                        raise ValueError()

                    with closing(FPFileOutputStream(outfile)) as fh:
                        blob_tag.blobRead(fh.stream, 0)

                    return outfile

    def list(self, start=None, end=None):
        """
        List clips in the given interval.
        :param start:
        :param end:
        :return:
        """
        raise NotImplementedError
