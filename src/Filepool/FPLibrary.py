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

from FPException import FPException
from FPNetException import FPNetException
from FPServerException import FPServerException
from FPClientException import FPClientException


class FPLibrary:

# GLOBAL OPTIONS

    FP_OPTION_BUFFERSIZE_W = u"buffersize"
    FP_OPTION_TIMEOUT_W = u"timeout"
    FP_OPTION_RETRYCOUNT_W = u"retrycount"
    FP_OPTION_RETRYSLEEP_W = u"retrysleep"
    FP_OPTION_MAXCONNECTIONS_W = u"maxconnections"
    FP_OPTION_ENABLE_MULTICLUSTER_FAILOVER_W = u"multiclusterfailover"
    FP_OPTION_DEFAULT_COLLISION_AVOIDANCE_W = u"collisionavoidance"
    FP_OPTION_PREFETCH_SIZE_W = u"prefetchsize"
    FP_OPTION_CLUSTER_NON_AVAIL_TIME_W = u"clusternonavailtime"
    FP_OPTION_PROBE_LIMIT_W = u"probetimelimit"
    FP_OPTION_EMBEDDED_DATA_THRESHOLD_W = u"embedding_threshold"
    FP_OPTION_OPENSTRATEGY_W = u"openstrategy"

    FP_OPTION_MULTICLUSTER_READ_STRATEGY_W = u"multicluster_read_strategy"
    FP_OPTION_MULTICLUSTER_WRITE_STRATEGY_W = u"multicluster_write_strategy"
    FP_OPTION_MULTICLUSTER_DELETE_STRATEGY_W = u"multicluster_delete_strategy"
    FP_OPTION_MULTICLUSTER_EXISTS_STRATEGY_W = u"multicluster_exists_strategy"
    FP_OPTION_MULTICLUSTER_QUERY_STRATEGY_W = u"multicluster_query_strategy"

    FP_OPTION_MULTICLUSTER_READ_CLUSTERS_W = u"multicluster_read_clusters"
    FP_OPTION_MULTICLUSTER_WRITE_CLUSTERS_W = u"multicluster_write_clusters"
    FP_OPTION_MULTICLUSTER_DELETE_CLUSTERS_W = u"multicluster_delete_clusters"
    FP_OPTION_MULTICLUSTER_EXISTS_CLUSTERS_W = u"multicluster_exists_clusters"
    FP_OPTION_MULTICLUSTER_QUERY_CLUSTERS_W = u"multicluster_query_clusters"

    FP_OPTION_BUFFERSIZE = "buffersize"
    FP_OPTION_TIMEOUT = "timeout"
    FP_OPTION_RETRYCOUNT = "retrycount"
    FP_OPTION_RETRYSLEEP = "retrysleep"
    FP_OPTION_MAXCONNECTIONS = "maxconnections"
    FP_OPTION_ENABLE_MULTICLUSTER_FAILOVER = "multiclusterfailover"
    FP_OPTION_DEFAULT_COLLISION_AVOIDANCE = "collisionavoidance"
    FP_OPTION_PREFETCH_SIZE = "prefetchsize"
    FP_OPTION_CLUSTER_NON_AVAIL_TIME = "clusternonavailtime"
    FP_OPTION_PROBE_LIMIT = "probetimelimit"
    FP_OPTION_EMBEDDED_DATA_THRESHOLD = "embedding_threshold"
    FP_OPTION_OPENSTRATEGY = "openstrategy"

    FP_OPTION_MULTICLUSTER_READ_STRATEGY = "multicluster_read_strategy"
    FP_OPTION_MULTICLUSTER_WRITE_STRATEGY = "multicluster_write_strategy"
    FP_OPTION_MULTICLUSTER_DELETE_STRATEGY = "multicluster_delete_strategy"
    FP_OPTION_MULTICLUSTER_EXISTS_STRATEGY = "multicluster_exists_strategy"
    FP_OPTION_MULTICLUSTER_QUERY_STRATEGY = "multicluster_query_strategy"

    FP_OPTION_MULTICLUSTER_READ_CLUSTERS = "multicluster_read_clusters"
    FP_OPTION_MULTICLUSTER_WRITE_CLUSTERS = "multicluster_write_clusters"
    FP_OPTION_MULTICLUSTER_DELETE_CLUSTERS = "multicluster_delete_clusters"
    FP_OPTION_MULTICLUSTER_EXISTS_CLUSTERS = "multicluster_exists_clusters"
    FP_OPTION_MULTICLUSTER_QUERY_CLUSTERS = "multicluster_query_clusters"

# FP_OPTION_MULTICLUSTER...STRATEGY Options

    FP_NO_STRATEGY = 0
    FP_FAILOVER_STRATEGY = 1
    FP_REPLICATION_STRATEGY = 2

# FP_OPTION_OPENSTRATEGY Options

    FP_PRIMARY_ONLY = 0
    FP_PRIMARY_AND_PRIMARY_REPLICA_CLUSTER_ONLY = 1
    FP_NO_REPLICA_CLUSTERS = 2
    FP_ALL_CLUSTERS = 3

    FP_NORMAL_OPEN = 0
    FP_LAZY_OPEN = 1

    FP_OPTION_EMBEDDED_DATA_MAX_SIZE = 102400

    FP_OPEN_ASTREE = 1
    FP_OPEN_FLAT = 2

    FP_OPTION_DEFAULT_OPTIONS = 0

    FP_OPTION_CALCID_MASK = 0x0000000F
    FP_OPTION_CLIENT_CALCID = 0x00000001
    FP_OPTION_CLIENT_CALCID_STREAMING = 0x00000002
    FP_OPTION_SERVER_CALCID_STREAMING = 0x00000003

    FP_OPTION_CALCID_NOCHECK = 0x00000010

    FP_OPTION_ENABLE_DUPLICATE_DETECTION = 0x00000020
    FP_OPTION_ENABLE_COLLISION_AVOIDANCE = 0x00000040
    FP_OPTION_DISABLE_COLLISION_AVOIDANCE = 0x00000080

    FP_OPTION_EMBED_DATA = 0x00000100
    FP_OPTION_LINK_DATA = 0x00000200


# Tag copy options

    FP_OPTION_NO_COPY_OPTIONS = 0x00
    FP_OPTION_COPY_BLOBDATA = 0x01
    FP_OPTION_COPY_CHILDREN = 0x02

    FP_OPTION_SECONDS_STRING = 0x00
    FP_OPTION_MILLISECONDS_STRING = 0x01

    FP_OPTION_DELETE_PRIVILEGED = 1

    FPPOOL_INFO_VERSION = 2

    FP_QUERY_RESULT_CODE_OK = 0
    FP_QUERY_RESULT_CODE_INCOMPLETE = 1
    FP_QUERY_RESULT_CODE_COMPLETE = 2
    FP_QUERY_RESULT_CODE_END = 3
    FP_QUERY_RESULT_CODE_ABORT = 4

    FP_QUERY_RESULT_CODE_ERROR = -1
    FP_QUERY_RESULT_CODE_PROGRESS = 99

    FP_QUERY_TYPE_EXISTING = 0x1
    FP_QUERY_TYPE_DELETED = 0x2

    FP_NO_RETENTION_PERIOD = 0
    FP_INFINITE_RETENTION_PERIOD = -1
    FP_DEFAULT_RETENTION_PERIOD = -2

    FP_LOGGING_COMPONENT_ALL = 0xFFFFFEFF

    FP_LOGGING_LEVEL_ERROR = 1
    FP_LOGGING_LEVEL_WARN = 2
    FP_LOGGING_LEVEL_LOG = 3

    FP_LOGGING_LOGFORMAT_XML = 0x00000000
    FP_LOGGING_LOGFORMAT_TAB = 0x00000001
    FP_LOGGING_LOGKEEP_OVERWRITE = 0x00000000
    FP_LOGGING_LOGKEEP_APPEND = 0x00000100
    FP_LOGGING_LOGKEEP_CREATE = 0x00000200
    FP_LOGGING_DEFAULT = (
        FP_LOGGING_LOGFORMAT_TAB | FP_LOGGING_LOGKEEP_OVERWRITE)

    FP_VERSION_FPLIBRARY_DLL = 1
    FP_VERSION_FPLIBRARY_JAR = 2

    FP_TRUE_W = u"true"
    FP_FALSE_W = u"false"

    FP_READ_W = u"read"
    FP_WRITE_W = u"write"
    FP_DELETE_W = u"delete"
    FP_PURGE_W = u"purge"
    FP_EXIST_W = u"exist"
    FP_CLIPENUMERATION_W = u"clip-enumeration"
    FP_RETENTION_W = u"retention"
    FP_BLOBNAMING_W = u"blobnaming"
    FP_MONITOR_W = u"monitor"
    FP_DELETIONLOGGING_W = u"deletionlogging"
    FP_PRIVILEGEDDELETE_W = u"privileged-delete"
    FP_POOL_POOLMAPPINGS_W = u"poolmappings"
    FP_COMPLIANCE_W = u"compliance"

    FP_ALLOWED_W = u"allowed"
    FP_SUPPORTED_W = u"supported"
    FP_UNSUPPORTED_W = u"unsupported"
    FP_DUPLICATEDETECTION_W = u"duplicate-detection"
    FP_DEFAULT_W = u"default"
    FP_SUPPORTED_SCHEMES_W = u"supported-schemes"
    FP_MD5_W = u"MD5"
    FP_MG_W = u"MG"
    FP_POOLS_W = u"pools"
    FP_PROFILES_W = u"profiles"
    FP_MODE_W = u"mode"
    FP_EVENT_BASED_RETENTION_W = u"ebr"
    FP_RETENTION_HOLD_W = u"retention-hold"
    FP_FIXED_RETENTION_MIN_W = u"fixedminimum"
    FP_FIXED_RETENTION_MAX_W = u"fixedmaximum"
    FP_VARIABLE_RETENTION_MIN_W = u"variableminimum"
    FP_VARIABLE_RETENTION_MAX_W = u"variablemaximum"
    FP_RETENTION_DEFAULT_W = u"default"
    FP_RETENTION_MIN_MAX_W = u"min-max"
    FP_VALUE_W = u"value"

    FP_TRUE = "true"
    FP_FALSE = "false"

    FP_READ = "read"
    FP_WRITE = "write"
    FP_DELETE = "delete"
    FP_PURGE = "purge"
    FP_EXIST = "exist"
    FP_CLIPENUMERATION = "clip-enumeration"
    FP_RETENTION = "retention"
    FP_BLOBNAMING = "blobnaming"
    FP_MONITOR = "monitor"
    FP_DELETIONLOGGING = "deletionlogging"
    FP_PRIVILEGEDDELETE = "privileged-delete"
    FP_POOL_POOLMAPPINGS = "poolmappings"
    FP_COMPLIANCE = "compliance"

    FP_ALLOWED = "allowed"
    FP_SUPPORTED = "supported"
    FP_UNSUPPORTED = "unsupported"
    FP_DUPLICATEDETECTION = "duplicate-detection"
    FP_DEFAULT = "default"
    FP_SUPPORTED_SCHEMES = "supported-schemes"
    FP_MD5 = "MD5"
    FP_MG = "MG"
    FP_POOLS = "pools"
    FP_PROFILES = "profiles"
    FP_MODE = "mode"
    FP_EVENT_BASED_RETENTION = "ebr"
    FP_RETENTION_HOLD = "retention-hold"
    FP_FIXED_RETENTION_MIN = "fixedminimum"
    FP_FIXED_RETENTION_MAX = "fixedmaximum"
    FP_VARIABLE_RETENTION_MIN = "variableminimum"
    FP_VARIABLE_RETENTION_MAX = "variablemaximum"
    FP_RETENTION_DEFAULT = "default"
    FP_RETENTION_MIN_MAX = "min-max"
    FP_VALUE = "value"


# CONSTANTS

    FP_GENERAL_ERROR = 0
    FP_NETWORK_ERROR = 1
    FP_SERVER_ERROR = 2
    FP_CLIENT_ERROR = 3

    def check_error(self):

        err = FPNative.get_last_error()

        if err != 0:

            errInfo = FPNative.get_last_error_info()

            if errInfo[5] == self.FP_NETWORK_ERROR:
                raise FPNetException(errInfo)
            elif errInfo[5] == self.FP_SERVER_ERROR:
                raise FPServerException(errInfo)
            elif errInfo[5] == self.FP_CLIENT_ERROR:
                raise FPClientException(errInfo)
            else:
                raise FPException(errInfo)
