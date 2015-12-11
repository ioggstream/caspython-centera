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

try:
    from sys import argv
    progname, clipid, outfilename = argv[:3]
except IndexError:
    pass




try:

  """                 /*Stores your application's name and version for registration on Centera
               This call should be made one time, before the FPPoolOpen() call,
               for each application that interfaces with centera
               *
               Applications can also be registered via the environment variables
               FP_OPTION_APP_NAME and FP_OPTION_APP_VER The values set through API
               will override what is set through environment variable.
  """

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


  ip = "192.168.26.7" #raw_input( "Pool address: " )
  clipid = "5GVU8O939OERGe1VV510G5SKVSIG418DHD4R2C05CENHRDNFDKNAG"
  pool = FPPool( ip )
  pool.setGlobalOption( FPLibrary.FP_OPTION_EMBEDDED_DATA_THRESHOLD,
    100 * 1024 )
  pool.getPoolInfo()
  # the application will be attached to the clip id
  pool.registerApplication( "python wrapper read example", "1.0" )

  clip = FPClip( pool )
  # clipid = raw_input( "Clip id: " )
  clip.open( clipid, FPLibrary.FP_OPEN_ASTREE)

  for a in "name retention.period numfiles".split():
      clip.getDescriptionAttribute(a)


  top = clip.getTopTag()
  print("tag: %r" % top)

  for i in range(clip.getNumBlobs() + 1):
    blob_id = clip.fetchNext()
    if not blob_id:
      break

    blob_tag = FPTag(blob_id)
    if blob_tag.getBlobSize() < 1:
      blob_tag.close()
      continue

    print("tag: %r" % blob_tag)

    file = FPFileOutputStream(outfilename + ".%s" % i)
    print("reading file from centera...")
    blob_tag.blobRead( file.stream, 0 )
    print("ok")

    file.close()
    blob_tag.close()

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
