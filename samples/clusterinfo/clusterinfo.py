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
from sys import argv

try:
  try:
    ip = argv[1]
  except IndexError:
    ip = raw_input( "Pool address: " )

  pool = FPPool( ip )

  pool.getPoolInfo()

  print "Cluster ID\t" + pool.clusterid 
  print "Cluster Name\t" + pool.clusterName 
  print "Pool Info Version\t" + str(pool.infoVersion) 
  print "CentraStar Version\t" + pool.version 
  print "Cluster Capacity\t" + str(pool.capacity) 
  print "Cluster Free Space\t" + str(pool.freeSpace) 
  print "Cluster Replica Address\t" + pool.replicaAddress 
  print "Native SDK Library Version\t" + pool.getComponentVersion( FPLibrary.FP_VERSION_FPLIBRARY_DLL ) 
  print "Cluster Time\t" + pool.getClusterTime() 

  #
  # Capabilities
  # 
  print "Pool Capabilities:\n"
  print "\tRead Operation Allowed+\t" + pool.getCapability( FPLibrary.FP_READ, FPLibrary.FP_ALLOWED) 
  print "\tWrite Operation Allowed+\t" + pool.getCapability( FPLibrary.FP_WRITE, FPLibrary.FP_ALLOWED) 
  print "\tDelete Operation Allowed+\t" + pool.getCapability( FPLibrary.FP_DELETE, FPLibrary.FP_ALLOWED) 
  print "\tPurge Operation Allowed+\t" + pool.getCapability( FPLibrary.FP_PURGE, FPLibrary.FP_ALLOWED) 
  print "\tPrivileged Delete Operation Allowed+\t" + pool.getCapability( FPLibrary.FP_PRIVILEGEDDELETE, FPLibrary.FP_ALLOWED) 
  print "\tExistence Checking Operation Allowed+\t" + pool.getCapability( FPLibrary.FP_EXIST, FPLibrary.FP_ALLOWED) 
  print "\tMonitor Operation Allowed+\t" + pool.getCapability( FPLibrary.FP_MONITOR, FPLibrary.FP_ALLOWED) 
  print "\tQuery Operation Allowed+\t" + pool.getCapability( FPLibrary.FP_CLIPENUMERATION, FPLibrary.FP_ALLOWED) 
  print "\tDefault Retention Period+\t" + pool.getCapability( FPLibrary.FP_RETENTION, FPLibrary.FP_DEFAULT) 
  print "\tEvent Based Retention Supported+\t" + pool.getCapability( FPLibrary.FP_COMPLIANCE, FPLibrary.FP_EVENT_BASED_RETENTION) 
  print "\tRetention Hold Supported+\t" + pool.getCapability( FPLibrary.FP_COMPLIANCE, FPLibrary.FP_RETENTION_HOLD) 
  print "\tDefault Blob Naming Scheme+\t" + pool.getCapability( FPLibrary.FP_BLOBNAMING, FPLibrary.FP_SUPPORTED_SCHEMES) 
  print "\tDeletion logging enabled+\t" + pool.getCapability( FPLibrary.FP_DELETIONLOGGING, FPLibrary.FP_SUPPORTED) 
  print "\tMin/Max Enabled+\t" + pool.getCapability( FPLibrary.FP_COMPLIANCE, FPLibrary.FP_RETENTION_MIN_MAX) 
  print "\tRetention Variable Min+\t" + pool.getCapability( FPLibrary.FP_RETENTION, FPLibrary.FP_VARIABLE_RETENTION_MIN) 
  print "\tRetention Variable Max+\t" + pool.getCapability( FPLibrary.FP_RETENTION, FPLibrary.FP_VARIABLE_RETENTION_MAX) 
  print "\tRetention Fixed Min+\t" + pool.getCapability( FPLibrary.FP_RETENTION, FPLibrary.FP_FIXED_RETENTION_MIN) 
  print "\tRetention Fixed Max+\t" + pool.getCapability( FPLibrary.FP_RETENTION, FPLibrary.FP_FIXED_RETENTION_MAX) 
  print "\tRetention Default+\t" + pool.getCapability( FPLibrary.FP_RETENTION, FPLibrary.FP_RETENTION_DEFAULT) 

  #
  # Retention Classes
  #
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

  print "\tMax pool connections+\t" + str(pool.getGlobalOption(
    FPLibrary.FP_OPTION_MAXCONNECTIONS)) 

  print "\tRetry count+\t" + str(pool.getGlobalOption(
    FPLibrary.FP_OPTION_RETRYCOUNT)) 

  print "\tSleep duration between retries+\t" + str(pool.getGlobalOption(
    FPLibrary.FP_OPTION_RETRYSLEEP)) 

  print "\tCluster unavailable time+\t" + str(pool.getGlobalOption(
    FPLibrary.FP_OPTION_CLUSTER_NON_AVAIL_TIME)) 

  print "\tEmbedded blob threshold (bytes)+\t" + str(pool.getGlobalOption(
    FPLibrary.FP_OPTION_EMBEDDED_DATA_THRESHOLD)) 

  print "\tPool open strategy+\t" + str(pool.getGlobalOption(
    FPLibrary.FP_OPTION_OPENSTRATEGY)) 

  print "\n"

  print "\tPool options:"

  print "\n"

  print "\tBuffersize+\t" + str(pool.getIntOption(
    FPLibrary.FP_OPTION_BUFFERSIZE )) 

  print "\tPool connection timeout:+\t" + str(pool.getIntOption(
    FPLibrary.FP_OPTION_TIMEOUT )) 

  cluster_failover = pool.getIntOption(
    FPLibrary.FP_OPTION_ENABLE_MULTICLUSTER_FAILOVER )

  print "\tMulticluster failover enabled:\t %r" % bool(cluster_failover == 1) 

  if cluster_failover == 1:

    print "\t\tRead failover strategy+\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_READ_STRATEGY )) 

    print "\t\tRead cluster strategy+\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_READ_CLUSTERS )) 

    print "\t\tWrite failover strategy+\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_WRITE_STRATEGY )) 

    print "\t\tWrite cluster strategy+\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_WRITE_CLUSTERS )) 

    print "\t\tDelete failover strategy+\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_DELETE_STRATEGY )) 

    print "\t\tDelete cluster strategy+\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_DELETE_CLUSTERS )) 

    print "\t\tExists failover strategy+\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_EXISTS_STRATEGY )) 

    print "\t\tExists cluster strategy+\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_EXISTS_CLUSTERS )) 

    print "\t\tQuery failover strategy+\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_QUERY_STRATEGY )) 

    print "\t\tQuery cluster strategy+\t\t" + str(pool.getGlobalOption(
      FPLibrary.FP_OPTION_MULTICLUSTER_QUERY_CLUSTERS )) 


  else:
    print "\tFalse"

  print "\tCollision avoidance enabled+\t" + str(pool.getIntOption( FPLibrary.FP_OPTION_DEFAULT_COLLISION_AVOIDANCE )) 

  print "\tPrefetch buffer size+\t" + str(pool.getIntOption( FPLibrary.FP_OPTION_PREFETCH_SIZE )) 




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
