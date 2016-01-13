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

import sys
import traceback
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
from setup import POOL_ADDRESS
from setup import clipid
from setup import TestCentera
import time

from contextlib import closing


class TestCenteraRead(TestCentera):
    # TestCentera opens and closes the self.pool


    def test_store_small(self):
        try:

            retention_sec = 100
            filename = "myfile.xml"
            top_tag = "file"
            clip_name = "myclip_" + filename

            with closing(FPClip(self.pool, clip_name, close_retries=3)) as clip:
                clipid = self.write_clip(clip, filename, retention_sec, top_tag)
                print(clipid)

            self.assert_clip_name(clipid, filename)
        except FPClientException as c:
            print(c)
            traceback.print_exc(file=sys.stdout)
        except FPServerException as s:
            print(s)
        except FPNetException as n:
            print(n)
        except FPException as e:
            print(e)

    def assert_clip_name(self, clipid, filename):
        with closing(FPClip(self.pool, close_retries=3)) as ch:
            ch.open(clipid, FPLibrary.FP_OPEN_ASTREE)
            clip_attrs = ch.getDescriptionAttributes()
            assert filename in clip_attrs[
                'name'], "Missing data in %r" % clip_attrs
            print(clip_attrs)

    def test_store_large(self):
        retention_sec = 100
        filename = "textfile.out"
        top_tag = "file"
        clip_name = "myclip_" + filename

        with closing(FPClip(self.pool, clip_name, close_retries=3)) as clip:
            clipid = self.write_clip(clip, filename, retention_sec, top_tag)
            print(clipid)

    def test_store_many(self):
        retention_sec = 100
        files = "1.xml 2.xml 3.xml 4.xml".split()
        clip_name = "myclip_" + "manyfiles"

        with closing(FPClip(self.pool, clip_name, close_retries=3)) as clip:
            clip.setRetentionPeriod(long(retention_sec))
            top_handle = clip.getTopTag()
            for filename in files:
                with closing(FPTag(top_handle, "mytag_" + filename)) as blob_tag:
                    with closing(FPFileInputStream(filename, 16 * 1024)) as fh:
                        blob_tag.blobWrite(fh.stream, 0)
            clipid = clip.write()

    def write_clip(self, clip, filename, retention_sec, top_tag):
        clip.setRetentionPeriod(long(retention_sec))
        top_handle = clip.getTopTag()
        with closing(FPTag(top_handle, top_tag)) as blob_tag:
            with closing(FPFileInputStream(filename, 16 * 1024)) as fh:
                blob_tag.blobWrite(fh.stream, 0)
        clipid = clip.write()
        return clipid
