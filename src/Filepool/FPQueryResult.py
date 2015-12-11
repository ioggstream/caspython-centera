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
import logging
log = logging.getLogger(__name__)

import FPNative

from FPLibrary import FPLibrary


class FPQueryResult(FPLibrary):

    handle = 0L

    def __init__(self, handle):
        log.debug("Create %r", self)
        self.handle = handle

    def close(self):
        log.debug("Closing %r", self)
        FPNative.query_result_close(self.handle)
        self.check_error()

    def getClipId(self):

        clip = FPNative.query_result_get_clip_id(self.handle)
        self.check_error()

        return clip

    def getField(self, name):

        field = FPNative.query_result_get_field(self.handle, name)
        self.check_error()

        return field

    def getResultCode(self):

        code = FPNative.query_result_get_result_code(self.handle)
        self.check_error()

        return code

    def getTimestamp(self):

        timestamp = FPNative.query_result_get_timestamp(self.handle)
        self.check_error()

        return timestamp
