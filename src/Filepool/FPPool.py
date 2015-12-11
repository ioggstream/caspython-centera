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
import FPNative
from FPLibrary import FPLibrary

log = logging.getLogger(__name__)


class FPPool(FPLibrary):

    handle = ''
    infoVersion = ''
    capacity = 0
    freeSpace = 0
    clusterid = ''
    clusterName = ''
    version = ''
    replicaAddress = ''

    context = 0

    def __init__(self, address):
        """
        TODO: should I open the pool here?
        :param address:
        :return:
        """
        self._opened = False
        self.open(address)

    def open(self, address):

        self.handle = FPNative.pool_open(address)
        self.check_error()
        self._opened = True

    def close(self, force=False):
        """
        Deallocate pool resources.
        :param force: issue pool_close without checking if the pool is closed.
        :return:
        """
        if self._opened or force:
            log.debug("Closing pool with handle: %r", self.handle)
            FPNative.pool_close(self.handle)
            self.check_error()
            self._opened = False
            log.debug("Pool correctly closed: %r", self.handle)
        else:
            log.warning("Trying to close an already closed pool at handle %r.", self.handle)

    def setGlobalOption(self, name, value):

        FPNative.set_global_option(name, value)
        self.check_error()

    def setIntOption(self, name, value):

        FPNative.set_int_option(self.handle, name, value)
        self.check_error()

    def getComponentVersion(self, component):

        version = FPNative.get_component_version(component)
        self.check_error()

        return version

    def getClusterTime(self):

        time = FPNative.get_cluster_time(self.handle)
        self.check_error()

        return time

    def getCapability(self, name, attr_name):

        capability = FPNative.get_capability(self.handle, name, attr_name)
        self.check_error()

        return capability

    def getClipID(self):

        clipid = FPNative.get_clip_id(self.handle)
        self.check_error()

        return clipid

    def getGlobalOption(self, name):

        value = FPNative.get_global_option(name)
        self.check_error()

        return value

    def getIntOption(self, name):

        value = FPNative.get_int_option(self.handle, name)
        self.check_error()

        return value

    def getPoolInfo(self):

        poolInfo = FPNative.get_pool_info(self.handle)
        self.check_error()

        self.infoVersion = poolInfo[0]
        self.capacity = poolInfo[1]
        self.freeSpace = poolInfo[2]
        self.clusterid = poolInfo[3]
        self.clusterName = poolInfo[4]
        self.version = poolInfo[5]
        self.replicaAddress = poolInfo[6]

    def openRetentionClassContext(self):

        value = FPNative.get_retention_class_context(self.handle)
        self.check_error()

        self.context = value

        return value

    def closeRetentionClassContext(self):

        value = FPNative.retention_class_context_close(self.context)
        self.check_error()

    def getFirstRetentionClass(self):

        retention_class = FPNative.retention_class_context_get_first_class(
            self.context)
        self.check_error()

        return retention_class

    def getLastRetentionClass(self):

        retention_class = FPNative.retention_class_context_get_last_class(
            self.context)
        self.check_error()

        return retention_class

    def getNamedRetentionClass(self, name):

        retention_class = FPNative.retention_class_context_get_named_class(
            self.context, name)
        self.check_error()

        return retention_class

    def getNextRetentionClass(self):

        retention_class = FPNative.retention_class_context_get_next_class(
            self.context)
        self.check_error()

        return retention_class

    def getNumRetentionClass(self):

        total = FPNative.retention_class_context_get_num_classes(self.context)
        self.check_error()

        return total

    def getPreviousRetentionClass(self):

        retention_class = FPNative.retention_class_context_get_previous_class(
            self.context)
        self.check_error()

        return retention_class

    def registerApplication(self, name, version):

        FPNative.register_application(name, version)
        self.check_error()

    def setClipID(self, id):

        FPNative.set_clip_id(self.handle, id)
        self.check_error()
