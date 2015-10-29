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


class FPQueryExpression(FPLibrary):

    handle = 0

    def __init__(self):

        self.handle = FPNative.query_expression_create()
        self.check_error()

    def close(self):

        FPNative.query_expression_close(self.handle)
        self.check_error()

    def deselectField(self, name):

        FPNative.query_expression_deselect_field(self.handle, name)
        self.check_error()

    def getEndTime(self):

        time = FPNative.query_expression_get_end_time(self.handle)
        self.check_error()

        return time

    def getStartTime(self):

        time = FPNative.query_expression_get_end_time(self.handle)
        self.check_error()

        return time

    def getType(self):

        type = FPNative.query_expression_get_end_time(self.handle)
        self.check_error()

        return type

    def isFieldSelected(self):

        value = FPNative.query_expression_get_end_time(self.handle)
        self.check_error()

        return value

    def selectField(self, name):

        FPNative.query_expression_select_field(self.handle, name)
        self.check_error()

    def setEndTime(self, time):

        FPNative.query_expression_set_end_time(self.handle, time)
        self.check_error()

    def setStartTime(self, time):

        FPNative.query_expression_set_start_time(self.handle, time)
        self.check_error()

    def setType(self, type):

        FPNative.query_expression_set_type(self.handle, type)
        self.check_error()
