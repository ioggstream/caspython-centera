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

from nose.tools import *
from nose import *

import sys
import traceback
import time

from Filepool.FPLibrary import FPLibrary
from Filepool.FPPool import FPPool
from Filepool.FPException import FPException
from Filepool.FPNetException import FPNetException
from Filepool.FPServerException import FPServerException
from Filepool.FPClientException import FPClientException
from Filepool.FPClip import FPClip
from Filepool.FPTag import FPTag
from Filepool.FPFileOutputStream import FPFileOutputStream
from Filepool.FPRetention import FPRetention

from setup import POOL_ADDRESS
from setup import clipid
from setup import TestCentera


class TestCenteraRead(TestCentera):
    # TestCentera opens and closes the pool

    def test_description(self):
        expected_attributes = ['refid',
                               'name',
                               'modification.date',
                               'totalsize',
                               'clusterid',
                               'modification.profile',
                               'creation.date',
                               'retention.period',
                               'numfiles',
                               'prev.clip',
                               'creation.poolid',
                               'modification.poolid',
                               'numtags',
                               'creation.profile',
                               'type',
                               'sdk.version',
                               'clip.naming.scheme']

        clip = FPClip(self.pool)
        clip.open(clipid, FPLibrary.FP_OPEN_ASTREE)
        try:
            attributes = clip.getNumDescriptionAttributes()
            assert all(x in attributes for x in expected_attributes)
        finally:
            print("closing clip")
            clip.close()

    def test_files(self):
        #    outfilename = "test_files"
        try:
            clip = FPClip(self.pool)
            clip.open(clipid, FPLibrary.FP_OPEN_ASTREE)

            numfiles = clip.getNumBlobs()
            assert numfiles, "Missing blobs"
            for i in range(numfiles + 1):
                blob_id = clip.fetchNext()
                if not blob_id:
                    break

                blob_tag = FPTag(blob_id)
                print(("tag: %r" % blob_tag))
                if blob_tag.getBlobSize() < 1:
                    print(("Empty blob %s" % i))
                    blob_tag.close()
                    continue

                outfilename = blob_tag.getTagName()
                print(("tag name : %s" % outfilename))
                fh = FPFileOutputStream(
                    "outfile.{name}.{i}".format(name=outfilename, i=i))
                print("reading file from centera...")
                blob_tag.blobRead(fh.stream, 0)
                print("ok")
                fh.close()
                blob_tag.close()

        finally:
            print("closing clip")
            clip.close()

        assert outfilename, "Missing tag: %r" % outfilename
