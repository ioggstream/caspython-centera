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


class FPQuery(FPLibrary):

    pool_handle = 0L
    query = 0
    expression = 0

    def __init__(self, pool):

        self.pool_handle = pool.handle

    def open(self, expression):
        log.debug("Opening %r", self)
        self.query = FPNative.pool_query_open(
            self.pool_handle, expression.handle)
        self.check_error()

    def close(self):
        log.debug("Closing %r", self)
        FPNative.pool_query_close(self.query)
        self.check_error()

    def fetchResult(self, timeout):

        result = FPNative.pool_query_fetch_result(self.query, timeout)
        self.check_error()

        return result

    def getPoolRef(self):

        pool = FPNative.pool_query_get_pool_ref(self.query)
        self.check_error()

        return pool
