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

import sys, traceback, time


from Filepool.FPLibrary import FPLibrary
from Filepool.FPPool import FPPool
from Filepool.FPException import FPException
from Filepool.FPNetException import FPNetException
from Filepool.FPServerException import FPServerException
from Filepool.FPClientException import FPClientException
from Filepool.FPClip import FPClip
from Filepool.FPTag import FPTag
from Filepool.FPFileOutputStream import FPFileOutputStream
from Filepool.FPRetention import FPRetention
from Filepool.FPMonitor import FPMonitor
from Filepool.FPQuery import FPQuery
from Filepool.FPQueryExpression import FPQueryExpression
from Filepool.FPQueryResult import FPQueryResult



try:
  sec_in_day = 86400
  ip = "192.168.26.7" # raw_input( "Pool address: " )

  pool = FPPool( ip )
  queryExpression = FPQueryExpression()
  queryExpression.setType( FPLibrary.FP_QUERY_TYPE_EXISTING )
  # 1371735529
  ts = int( time.time() - 15*sec_in_day) #
  queryExpression.setStartTime(ts)

  query = FPQuery( pool )
  query.open( queryExpression )
  queryExpression.close()

  status = 0
  while True:

    res = FPQueryResult(query.fetchResult(0))
    status = res.getResultCode()

    if status in (
        FPLibrary.FP_QUERY_RESULT_CODE_END,
        FPLibrary.FP_QUERY_RESULT_CODE_ABORT,
        FPLibrary.FP_QUERY_RESULT_CODE_ERROR,
        FPLibrary.FP_QUERY_RESULT_CODE_INCOMPLETE,
        FPLibrary.FP_QUERY_RESULT_CODE_COMPLETE
    ):
        break
    elif status == FPLibrary.FP_QUERY_RESULT_CODE_PROGRESS:
        continue
    elif status == FPLibrary.FP_QUERY_RESULT_CODE_OK:
        print res.getClipId()

  query.close()
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
