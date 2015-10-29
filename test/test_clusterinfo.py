#
#
# Copyright (c) 2006 EMC Corporation. All Rights Reserved
#
# This file is part of Python wrapper for the Centera SDK.
#
# Python wrapper is free software; you can redistribute it and/or
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
from __future__ import print_function

from Filepool.FPLibrary import FPLibrary
from Filepool.FPRetention import FPRetention

from setup import TestCentera

import locale


class TestClusterInfo(TestCentera):

    def test_clusterinfo(self):
        print("Cluster ID", self.pool.clusterid)
        print("Cluster Name", self.pool.clusterName)
        print("self.pool Info Version", str(self.pool.infoVersion))
        print("CentraStar Version", self.pool.version)
        print("Cluster Capacity in GB", str(self.pool.capacity >> 30))
        print("Cluster Free Space in GB", str(self.pool.freeSpace >> 30))
        print("Cluster Free Space in bytes ", self.pool.freeSpace)
        print("Cluster Replica Address", self.pool.replicaAddress)
        print("Native SDK Library Version",
              self.pool.getComponentVersion(FPLibrary.FP_VERSION_FPLIBRARY_DLL))
        print("Cluster Time", self.pool.getClusterTime())

    def harn_getcapability_parameter(self, capability, parameter):
        """
        Get a given parameter of a centera capability
        :param capability:
        :param parameter:
        :return:
        """
        capability_code = getattr(FPLibrary, 'FP_{capability}'.format(
            capability=capability.upper()))
        parameter_code = getattr(FPLibrary, 'FP_{parameter}'.format(
            parameter=parameter.upper()))
        return self.pool.getCapability(capability_code, parameter_code)

    def test_capabilites_basic(self):
        print("self.pool Capabilities: Allowed Operations:\n")
        for c, label in [('read', 'read'),
                         ('write', 'write'),
                         ('delete', 'delete'),
                         ('purge', 'purge'),
                         ('privilegeddelete', 'privileged delete'),
                         ('exist', 'existence checking'),
                         ('monitor', 'monitor'),
                         ('clipenumeration', 'query')
                         ]:
            allowed = self.harn_getcapability_parameter(c, "allowed")
            print(("\t{label:10}: {allowed}".format(
                label=label, allowed=allowed)))

    def test_capabilites_retention(self):
        for c, label in [
            ('default', 'Default Retention Period'),
            ("VARIABLE_RETENTION_MIN",
             "Retention Variable Min"),
            ("VARIABLE_RETENTION_MAX",
             "Retention Variable Max"),
            ("FIXED_RETENTION_MIN",
             "Retention Fixed Min"),
            ("FIXED_RETENTION_MAX", "Retention Fixed Max"),
            ("RETENTION_DEFAULT", "Retention Default")
        ]:
            value = self.harn_getcapability_parameter("retention", c)
            print(("\t{label} : {value}".format(
                label=label, value=value)))

    def test_capabilities_other(self):
        for capability, parameter, label in [
            (FPLibrary.FP_BLOBNAMING, FPLibrary.FP_SUPPORTED_SCHEMES,
             "Default Blob Naming Scheme"),
            (FPLibrary.FP_DELETIONLOGGING,
             FPLibrary.FP_SUPPORTED, "Deletion logging enabled,"),
            (FPLibrary.FP_COMPLIANCE, FPLibrary.FP_EVENT_BASED_RETENTION,
             "Event Based Retention Supported,"),
            (FPLibrary.FP_COMPLIANCE, FPLibrary.FP_RETENTION_HOLD,
             "Retention Hold Supported,"),
            (FPLibrary.FP_COMPLIANCE,
             FPLibrary.FP_RETENTION_MIN_MAX, "Min/Max Enabled,")
        ]:
            print("{label:30} {value}".format(label=label,
                                              value=self.pool.getCapability(capability, parameter))
                  )

    def test_retention_classes(self):
        #
        # Retention Classes
        #
        self.pool.openRetentionClassContext()
        r = self.pool.getNumRetentionClass()
        print(
            "There are {r}  retention classes defined on the cluster".format(r=r))
        if r < 1:
            return

        first = self.pool.getFirstRetentionClass()
        rc = FPRetention(first)

        while rc is not None:
            print("Retention Class Name: ", rc.getName())
            print("Retention Class Period: ", str(rc.getPeriod()))
            print("\n")

            rc.close()

            rid = self.pool.getNextRetentionClass()
            if rid != 0:
                rc = FPRetention(rid)
            else:
                rc = None

    def test_global_option(self):
        print("\n" "Global options:"  "\n")
        for option, label in (
                ('maxconnections', 'Max self.pool connections'),
                ('retrycount', "Retry count"),
                ('retrysleep', "Sleep duration between retries"),
                ('cluster_non_avail_time',
                 "Cluster unavailable time"),
                ('embedded_data_threshold',
                 "Embedded blob threshold (bytes)"),
                ('openstrategy', "self.pool open strategy")
        ):
            optno = getattr(FPLibrary, 'FP_OPTION_{name}'.format(name=option.upper()))
            print(("{label}: {value}".format(
                label=label, value=self.pool.getGlobalOption(optno))))

    def test_pool_options(self):
        print("self.pool options:" "\n"
              "Buffersize",
              self.pool.getIntOption(FPLibrary.FP_OPTION_BUFFERSIZE)
        )

        print("self.pool connection timeout:", str(self.pool.getIntOption(
            FPLibrary.FP_OPTION_TIMEOUT)))

        cluster_failover = self.pool.getIntOption(
            FPLibrary.FP_OPTION_ENABLE_MULTICLUSTER_FAILOVER)

        print("Multicluster failover enabled: %r" % bool(
            cluster_failover == 1))

        if cluster_failover == 1:
            action = "READ WRITE DELETE EXISTS QUERY".split()
            mode = "STRATEGY CLUSTERS".split()
            for a in action:
                for m in mode:
                    option = 'FP_OPTION_MULTICLUSTER_%s_%s' % (a, m)
                    value = self.pool.getGlobalOption(
                        getattr(FPLibrary, option))
                    print("{action:9} {mode:.15} strategy:\t{strategy}".format(
                        action=a,
                        mode='cluster' if m == 'CLUSTERS' else 'failover',
                        strategy=value)
                    )
        else:
            print("False")

        print("Collision avoidance enabled:",  str(self.pool.getIntOption(
            FPLibrary.FP_OPTION_DEFAULT_COLLISION_AVOIDANCE)))

        print("Prefetch buffer size:", str(
            self.pool.getIntOption(FPLibrary.FP_OPTION_PREFETCH_SIZE)))
