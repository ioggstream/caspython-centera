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


class FPTag(FPLibrary):

    handle = 0
    top_handle = 0

    def __init__(self, tag, name=None):

        if(name is None):

            self.handle = tag

        if(name is not None):

            self.top_handle = tag
            self.handle = FPNative.tag_create(self.top_handle, name)
            self.check_error()

    def close(self):

        if(self.handle != 0):
            FPNative.tag_close(self.handle)
            self.check_error()

    def copy(self, tag_copy, options):

        ntag = FPNative.tag_copy(self.handle, tag_copy, options)
        self.check_error()

        return ntag

    def delete(self):

        FPNative.tag_delete(self.handle)
        self.check_error()

    def getBlobSize(self):

        size = FPNative.tag_get_blob_size(self.handle)
        self.check_error()

        return size

    def getClipRef(self):

        clip = FPNative.tag_get_clip_ref(self.handle)
        self.check_error()

        return clip

    def getPoolRef(self):

        pool = FPNative.tag_get_pool_ref(self.handle)
        self.check_error()

        return pool

    def getTagName(self):

        name = FPNative.tag_get_tag_name(self.handle)
        self.check_error()

        return name

    def blobWrite(self, stream, options):

        FPNative.blob_write(self.handle, stream, options)
        self.check_error()

    def blobWritePartial(self, stream, options, sequenceid):

        FPNative.blob_write_partial(self.handle, stream, options, sequenceid)
        self.check_error()

    def blobExists(self):

        FPNative.blob_exists(self.handle)
        self.check_error()

    def blobRead(self, stream, options):

        FPNative.blob_read(self.handle, stream, options)
        self.check_error()

    def blobReadPartial(self, stream, offset, length, options):

        FPNative.blob_read_partial(
            self.handle, stream, offset, length, options)
        self.check_error()

    def getFirstChild(self):

        child = FPNative.tag_get_first_child(self.handle)
        self.check_error()

        return child

    def getParent(self):

        parent = FPNative.tag_get_first_child(self.handle)
        self.check_error()

        return parent

    def getPrevSibling(self):

        sibling = FPNative.tag_get_prev_sibling(self.handle)
        self.check_error()

        return sibling

    def getSibling(self):

        sibling = FPNative.tag_get_sibling(self.handle)
        self.check_error()

        return sibling

    def getBoolAttribute(self, name):

        attr = FPNative.tag_get_bool_attribute(self.handle, name)
        self.check_error()

        return attr

    def getIndexAttribute(self, index):

        list = FPNative.tag_get_index_attribute(self.handle)
        self.check_error()

        return list

    def getLongAttribute(self, name):

        value = FPNative.tag_get_long_attribute(self.handle, name)
        self.check_error()

        return value

    def getNumAttributes(self, name):

        value = FPNative.tag_get_num_attributes(self.handle, name)
        self.check_error()

        return value

    def getStringAttribute(self, name):

        value = FPNative.tag_get_string_attribute(self.handle, name)
        self.check_error()

        return value

    def removeAttribute(self, name):

        value = FPNative.tag_remove_attribute(self.handle, name)
        self.check_error()

        return value

    def setBoolAttribute(self, name, value):

        FPNative.tag_set_bool_attribute(self.handle, name, value)
        self.check_error()

    def setLongAttribute(self, name, value):

        FPNative.tag_set_long_attribute(self.handle, name, value)
        self.check_error()

    def setStringAttribute(self, name, value):

        FPNative.tag_set_string_attribute(self.handle, name, value)
        self.check_error()
