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

  pool.setGlobalOption( FPLibrary.FP_OPTION_EMBEDDED_DATA_THRESHOLD,
    100 * 1024 )

  pool.getPoolInfo()

  pool.registerApplication( "python wrapper store example", "1.0" )

  clip = FPClip( pool, "python store example" )

  retention = raw_input( "Retention (in seconds): " )

  clip.setRetentionPeriod( long(retention) )

  top_handle  = clip.getTopTag()

  blob_tag = FPTag( top_handle, "file" )

  filename = raw_input( "Filename: " )

  file = FPFileInputStream( filename, 16*1024 )
 
  blob_tag.blobWrite( file.stream, 0 )

  file.close()
  blob_tag.close()

  clipid = clip.write()
  print clipid

  clip.close()

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
