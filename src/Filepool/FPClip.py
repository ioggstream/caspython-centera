#
#
#  Copyright (c) 2006 EMC Corporation. All Rights Reserved
#
#  This file is part of Python wrapper for the Centera SDK.
#
#  Python wrapper is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation version 2.
#
#  In addition to the permissions granted in the GNU General Public
#  License version 2, EMC Corporation gives you unlimited permission
#  to link the compiled version of this file into combinations with
#  other programs, and to distribute those combinations without any
#  restriction coming from the use of this file. (The General Public
#  License restrictions do apply in other respects; for example,
#  they cover modification of the file, and distribution when not
#  linked into a combined executable.)
#
#  Python wrapper is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License version 2 for more details.
#
#  You should have received a copy of the GNU General Public License
#  version 2 along with Python wrapper; see the file COPYING. If not,
#  write to:
#
#   EMC Corporation
#   Centera Open Source Intiative (COSI)
#   80 South Street
#   1/W-1
#   Hopkinton, MA 01748
#   USA
#
#

import FPNative

from FPLibrary import FPLibrary
from FPException import FPException
import time
from Filepool.FPTag import FPTag
import logging

log = logging.getLogger()


def loggable(f):
    def tmp(*args, **kwds):
        log.debug("Calling %r", f.__name__)
        ret = f(*args, **kwds)
        return ret
    return tmp


class FPClip(FPLibrary):

    """
    Class take references of:
    - pool_handle
    - clip name
    - clip handle
    """
    pool_handle = 0
    handle = 0
    top_handle = 0
    clipid = ''

    # TODO split method by implicit parameters:
    #  - self.handle
    #  - class attributes should be moved under init
    _proxied_methods = [m.replace("clip_", "", 1)
                        for m in dir(FPNative) if m.startswith("clip_")]

    def __init__(self, pool, name=None, close_retries=0):
        # Validate inserted data.

        if pool is None:
            raise FPException("No Pool Reference")

        if name is not None:
            self.handle = FPNative.clip_create(pool.handle, name)
            self.check_error()

        self.pool_handle = pool.handle
        self.close_retries = close_retries

        def __getattr__(self, item):
            # Fallback on proxied methods.
            if item in _proxied_methods:
                def f(self, *args, **kwargs):
                    m = getattr(FPNative, 'clip_' + item)
                    ret = m(*args, **kwargs)
                    self.check_error()
                    f.__doc__ = m.__doc__
                    f.__name__ = m.__name__
                    return ret

                return f

    def open(self, clipid, mode=FPLibrary.FP_OPEN_ASTREE):
        """

        :param clipid:
        :param mode: FPLibrary.FP_OPEN_ASTREE (default) or FPLibrary.FP_OPEN_FLAT
        :return:
        """
        self.clipid = clipid
        self.handle = FPNative.clip_open(self.pool_handle, clipid, mode)
        self.check_error()

    def write(self):

        self.clipid = FPNative.clip_write(self.handle)
        self.check_error()

        return self.clipid

    def _close(self):
        """Close a clip. If it's not open, just don't check for errors.
        """
        if self.top_handle != 0:
            log.debug("Closing top_tag handle.")
            FPNative.tag_close(self.top_handle)
            self.check_error()
            self.top_handle = 0

        if self.handle != 0:
            log.debug("Closing handle.")
            FPNative.clip_close(self.handle)
            self.check_error()
            self.handle = 0

    def close(self, retries=None, retry_interval=1):
        """
        Close a clip retrying after a while n case of FPException.
        :param retries: by default does not retry.
        :param retry_interval:
        :return:
        """
        for i in range(retries or self.close_retries):
            try:
                self._close()
                return
            except FPException as e:
                if e.errorString == "FP_OBJECTINUSE_ERR":
                    log.debug("Object in use: waiting.")
                    time.sleep(retry_interval)
        # Should close at least one time.
        self._close()

    def getTopTag(self):

        if self.top_handle == 0:
            self.top_handle = FPNative.get_top_tag(self.handle)
            self.check_error()

        return self.top_handle

    def auditedDelete(self, clipid, reason, options):

        FPNative.clip_audited_delete(self.pool_handle, clipid,
                                     reason, options)
        self.check_error()

    def delete(self, clipid):

        FPNative.clip_delete(self.pool_handle, clipid)
        self.check_error()

    def enableEbrWithClass(self, retention_class):

        FPNative.clip_enable_ebr_with_class(self.handle, retention_class)
        self.check_error()

    def enableEbrWithPeriod(self, seconds):

        FPNative.clip_enable_ebr_with_period(self.handle, seconds)
        self.check_error()

    def rawOpen(self, clipid, stream, options):

        self.clip = FPNative.clip_raw_open(self.pool_handle, clipid,
                                           stream, options)
        self.check_error()

    def rawRead(self, stream):

        FPNative.clip_raw_read(self.handle, stream)
        self.check_error()

    def removeRetentionClass(self):

        FPNative.clip_remove_retention_class(self.handle)
        self.check_error()

    def setName(self, name):

        FPNative.clip_set_name(self.handle, name)
        self.check_error()

    def setRetentionClass(self, retention_class):

        FPNative.clip_set_retention_class(self.handle, retention_class)
        self.check_error()

    def setRetentionHold(self, flag, id):

        FPNative.clip_set_retention_hold(self.handle, flag, id)
        self.check_error()

    def setRetentionPeriod(self, seconds):

        FPNative.clip_set_retention_period(self.handle, seconds)
        self.check_error()

    def triggerEbrEvent(self):

        FPNative.clip_trigger_ebr_event(self.handle)
        self.check_error()

    def triggerEbrEventWithClass(self, retention_class):

        FPNative.clip_trigger_ebr_event_with_class(self.handle,
                                                   retention_class)
        self.check_error()

    def triggerEbrEventWithPeriod(self, seconds):

        FPNative.clip_trigger_ebr_event_with_period(self.handle,
                                                    seconds)
        self.check_error()

    def getCanonicalFormat(self, clipid):

        self.canonical = FPNative.clip_get_canonical_format(clipid)
        self.check_error()

        return self.canonical

    def getStringFormat(self, canonical):

        clipid = FPNative.clip_get_string_format(canonical)
        self.check_error()

        return clipid

    def exists(self, clipid):

        b = FPNative.clip_exists(self.pool_handle, clipid)
        self.check_error()

        return b

    def getClipId(self):

        clipid = FPNative.clip_get_clip_id(self.handle)
        self.check_error()

        return clipid

    def getCreationDate(self):

        date = FPNative.clip_get_creation_date(self.handle)
        self.check_error()

        return date

    def getEbrClassName(self):

        classname = FPNative.clip_get_ebr_class_name(self.handle)
        self.check_error()

        return classname

    def getEbrEventTime(self):

        time = FPNative.clip_get_ebr_event_time(self.handle)
        self.check_error()

        return time

    def getEbrPeriod(self):

        seconds = FPNative.clip_get_ebr_period(self.handle)
        self.check_error()

        return seconds

    def getName(self):

        name = FPNative.clip_get_name(self.handle)
        self.check_error()

        return name

    def getNumBlobs(self):

        blob_num = FPNative.clip_get_num_blobs(self.handle)
        self.check_error()

        return blob_num

    def getNumTags(self):

        tag_num = FPNative.clip_get_num_tags(self.handle)
        self.check_error()

        return tag_num

    def getPoolRef(self):

        poolref = FPNative.clip_get_pool_ref(self.handle)
        self.check_error()

        return poolref

    def getRetentionClassName(self):

        classname = FPNative.clip_get_retention_class_name(self.handle)
        self.check_error()

        return classname

    def isRetentionHold(self):

        value = FPNative.clip_get_retention_hold(self.handle)
        self.check_error()

        return value

    def getRetentionPeriod(self):

        seconds = FPNative.clip_get_retention_period(self.handle)
        self.check_error()

        return seconds

    def getTotalSize(self):

        size = FPNative.clip_get_total_size(self.handle)
        self.check_error()

        return size

    def isEbrEnabled(self):

        value = FPNative.clip_is_ebr_enabled(self.handle)
        self.check_error()

        return value

    def isModified(self):

        value = FPNative.clip_is_modified(self.handle)
        self.check_error()

        return value

    def isRetentionClassValid(self, retention_class):

        value = FPNative.clip_validate_retention_class(self.handle,
                                                       retention_class)
        self.check_error()

        return value

    def getDescriptionAttribute(self, attribute):

        value = FPNative.clip_get_description_attribute(self.handle,
                                                        attribute)
        self.check_error()

        return value

    def getDescriptionAttributeIndex(self, index):

        value = FPNative.clip_get_description_attribute_index(self.handle,
                                                              index)
        self.check_error()

        return value

    def getNumDescriptionAttributes(self):

        value = FPNative.clip_get_num_description_attributes(self.handle)
        self.check_error()

        return value

    def removeDescriptionAttribute(self, name):

        FPNative.clip_remove_description_attribute(self.handle, name)
        self.check_error()

    def setDescriptionAttribute(self, name, value):

        FPNative.clip_set_description_attribute(self.handle, name, value)
        self.check_error()

    def fetchNext(self):

        tag = FPNative.clip_fetch_next(self.handle)
        self.check_error()
        return tag

    def getDescriptionAttributes(self):
        """

        :return: a dict with the attributes.
        """
        a_len = range(self.getNumDescriptionAttributes())
        return dict(
            self.getDescriptionAttributeIndex(i)
            for i in a_len
        )

    def getTags(self):
        """

        :return: an iterable of (tag_name, tag_size)
        """
        numfiles = self.getNumBlobs()
        if not numfiles:
            return

        for blob_id in self.getBlobs():
            blob_tag = FPTag(blob_id)
            tag_name = blob_tag.getTagName()
            blob_size = blob_tag.getBlobSize()
            blob_tag.close()
            yield tag_name, blob_size

    def readFiles(self, tag_name=None, out_file=None):
        for blob_id in self.getBlobs():

            with closing(FPTag(blob_id)) as blob_tag:
                if not tag_name or blob_tag.getTagName() == tag_name:
                    fh = FPFileOutputStream(outfile + tag_name + ".%s" % i)
                    log.debug("reading file from centera...")
                    blob_tag.blobRead(fh.stream, 0)

    def getBlobs(self):
        """
        Iterate in all blob_id.
        :return:
        """
        n = self.getNumBlobs()
        for i in range(n + 1):
            ret = self.fetchNext()
            if not ret:
                log.debug("No more blobs.")
                break
            yield ret
