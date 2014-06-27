#########################################################################
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
#########################################################################

import sys, traceback

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

try:

  ip = raw_input( "Pool address: " )

  pool = FPPool( ip )

  pool.getPoolInfo()

  print "Cluster ID:\n"
  print "\t" + pool.clusterid + "\n"

  print "Cluster Name:\n"
  print "\t" + pool.clusterName + "\n"

  print "Pool Info Version:\n"
  print "\t" + str(pool.infoVersion) + "\n"

  print "CentraStar Version:\n"
  print "\t" + pool.version + "\n"

  print "Cluster Capacity:\n"
  print "\t" + str(pool.capacity) + "\n"

  print "Cluster Free Space:\n"
  print "\t" + str(pool.freeSpace) + "\n"

  print "Cluster Replica Address:\n"
  print "\t" + pool.replicaAddress + "\n"

  print "Native SDK Library Version:\n"
  print "\t" + pool.getComponentVersion( 
FPLibrary.FP_VERSION_FPLIBRARY_DLL ) + "\n"

  print "Cluster Time:\n"
  print "\t" + pool.getClusterTime() + "\n"

  print "Pool Capabilities:\n"

  print "\tRead Operation Allowed:";
  print "\t" + pool.getCapability( FPLibrary.FP_READ, 
FPLibrary.FP_ALLOWED) + "\n"

  print "\tWrite Operation Allowed:";
  print "\t" + pool.getCapability( FPLibrary.FP_WRITE, 
FPLibrary.FP_ALLOWED) + "\n"

  print "\tDelete Operation Allowed:";
  print "\t" + pool.getCapability( FPLibrary.FP_DELETE, 
FPLibrary.FP_ALLOWED) + "\n"

  print "\tPurge Operation Allowed:";
  print "\t" + pool.getCapability( FPLibrary.FP_PURGE, 
FPLibrary.FP_ALLOWED) + "\n"

  print "\tPrivileged Delete Operation Allowed:";
  print "\t" + pool.getCapability( FPLibrary.FP_PRIVILEGEDDELETE, 
FPLibrary.FP_ALLOWED) + "\n"

  print "\tExistence Checking Operation Allowed:";
  print "\t" + pool.getCapability( FPLibrary.FP_EXIST, 
FPLibrary.FP_ALLOWED) + "\n"

  print "\tMonitor Operation Allowed:";
  print "\t" + pool.getCapability( FPLibrary.FP_MONITOR, 
FPLibrary.FP_ALLOWED) + "\n"

  print "\tQuery Operation Allowed:";
  print "\t" + pool.getCapability( FPLibrary.FP_CLIPENUMERATION, 
FPLibrary.FP_ALLOWED) + "\n"

  print "\tDefault Retention Period:";
  print "\t" + pool.getCapability( FPLibrary.FP_RETENTION, 
FPLibrary.FP_DEFAULT) + "\n"

  print "\tEvent Based Retention Supported:";
  print "\t" + pool.getCapability( FPLibrary.FP_COMPLIANCE, 
FPLibrary.FP_EVENT_BASED_RETENTION) + "\n"

  print "\tRetention Hold Supported:";
  print "\t" + pool.getCapability( FPLibrary.FP_COMPLIANCE, 
FPLibrary.FP_RETENTION_HOLD) + "\n"

  print "\tDefault Blob Naming Scheme:";
  print "\t" + pool.getCapability( FPLibrary.FP_BLOBNAMING, 
FPLibrary.FP_SUPPORTED_SCHEMES) + "\n"

  print "\tDeletion logging enabled:";
  print "\t" + pool.getCapability( FPLibrary.FP_DELETIONLOGGING, 
FPLibrary.FP_SUPPORTED) + "\n"

  print "\tMin/Max Enabled:";
  print "\t" + pool.getCapability( FPLibrary.FP_COMPLIANCE, 
FPLibrary.FP_RETENTION_MIN_MAX) + "\n"

  print "\tRetention Variable Min:";
  print "\t" + pool.getCapability( FPLibrary.FP_RETENTION, 
FPLibrary.FP_VARIABLE_RETENTION_MIN) + "\n"

  print "\tRetention Variable Max:";
  print "\t" + pool.getCapability( FPLibrary.FP_RETENTION, 
FPLibrary.FP_VARIABLE_RETENTION_MAX) + "\n"

  print "\tRetention Fixed Min:";
  print "\t" + pool.getCapability( FPLibrary.FP_RETENTION, 
FPLibrary.FP_FIXED_RETENTION_MIN) + "\n"

  print "\tRetention Fixed Max:";
  print "\t" + pool.getCapability( FPLibrary.FP_RETENTION, 
FPLibrary.FP_FIXED_RETENTION_MAX) + "\n"

  print "\tRetention Default:";
  print "\t" + pool.getCapability( FPLibrary.FP_RETENTION, 
FPLibrary.FP_RETENTION_DEFAULT) + "\n"

  pool.openRetentionClassContext();
  r = pool.getNumRetentionClass();

  print "\tThere are " + str(r) + " retention classes defined on the cluster"

  print "\n"

  if( r > 0 ):
    first = pool.getFirstRetentionClass()
    rc = FPRetention(first)

    while( rc is not None ):

      print "\tRetention Class Name: "
      print "\t" + rc.getName()
      print "\tRetention Class Period: "
      print "\t" + str(rc.getPeriod())
      print "\n"

      rc.close()

      r = pool.getNextRetentionClass()
      if( r != 0 ):
        rc = FPRetention(r)
      else:
        rc = None

  print "\n"

  print "\tGlobal options:"

  print "\n"

  print "\tMax pool connections:";
  print "\t" + str(pool.getGlobalOption(
    FPLibrary.FP_OPTION_MAXCONNECTIONS)) + "\n"

  print "\tRetry count:";
  print "\t" + str(pool.getGlobalOption(
    FPLibrary.FP_OPTION_RETRYCOUNT)) + "\n"

  print "\tSleep duration between retries:";
  print "\t" + str(pool.getGlobalOption(
    FPLibrary.FP_OPTION_RETRYSLEEP)) + "\n"

  print "\tCluster unavailable time:";
  print "\t" + str(pool.getGlobalOption(
    FPLibrary.FP_OPTION_CLUSTER_NON_AVAIL_TIME)) + "\n"

  print "\tEmbedded blob threshold (bytes):";
  print "\t" + str(pool.getGlobalOption(
    FPLibrary.FP_OPTION_EMBEDDED_DATA_THRESHOLD)) + "\n"

  print "\tPool open strategy:";
  print "\t" + str(pool.getGlobalOption(
    FPLibrary.FP_OPTION_OPENSTRATEGY)) + "\n"

  print "\n"

  print "\tPool options:"

  print "\n"

  print "\tBuffersize:";
  print "\t" + str(pool.getIntOption(
    FPLibrary.FP_OPTION_BUFFERSIZE )) + "\n"

  print "\tPool connection timeout::";
  print "\t" + str(pool.getIntOption(
    FPLibrary.FP_OPTION_TIMEOUT )) + "\n"

  cluster_failover = pool.getIntOption(
    FPLibrary.FP_OPTION_ENABLE_MULTICLUSTER_FAILOVER )

  print "\tMulticluster failover enabled: "

  if( cluster_failover == 1 ):
    print "\tTrue"

    print "\t\tRead failover strategy:";
    print "\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_READ_STRATEGY )) + "\n"

    print "\t\tRead cluster strategy:";
    print "\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_READ_CLUSTERS )) + "\n"

    print "\t\tWrite failover strategy:";
    print "\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_WRITE_STRATEGY )) + "\n"

    print "\t\tWrite cluster strategy:";
    print "\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_WRITE_CLUSTERS )) + "\n"

    print "\t\tDelete failover strategy:";
    print "\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_DELETE_STRATEGY )) + "\n"

    print "\t\tDelete cluster strategy:";
    print "\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_DELETE_CLUSTERS )) + "\n"

    print "\t\tExists failover strategy:";
    print "\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_EXISTS_STRATEGY )) + "\n"

    print "\t\tExists cluster strategy:";
    print "\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_EXISTS_CLUSTERS )) + "\n"

    print "\t\tQuery failover strategy:";
    print "\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_QUERY_STRATEGY )) + "\n"

    print "\t\tQuery cluster strategy:";
    print "\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_QUERY_CLUSTERS )) + "\n"


  else:
    print "\tFalse"

  print "\tCollision avoidance enabled:";
  print "\t" + str(pool.getIntOption(
    FPLibrary.FP_OPTION_DEFAULT_COLLISION_AVOIDANCE )) + "\n"

  print "\tPrefetch buffer size:";
  print "\t" + str(pool.getIntOption(
    FPLibrary.FP_OPTION_PREFETCH_SIZE )) + "\n"




  print ""

  pool.close()

  
except FPClientException, c:
  print c
  traceback.print_exc(file=sys.stdout)
except FPServerException, s:
  print s
except FPNetException, n:
  print n
except FPException, e:
  print e
