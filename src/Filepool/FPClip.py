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

import FPNative

from FPLibrary import FPLibrary

class FPClip(FPLibrary):

  pool_handle = 0
  handle      = 0
  top_handle  = 0
  clipid      = ''


  def __init__( self, pool, name=None ):

    if( pool == None ):
      raise FPException( "No Pool Reference" )

    self.pool_handle = pool.handle

    if( name is not None ):

      self.handle = FPNative.clip_create( pool.handle, name )
      self.check_error()


  def open( self, clipid, mode ):

    self.clipid = clipid
    self.handle = FPNative.clip_open( self.pool_handle, clipid, mode )
    self.check_error()


  def write( self ):

    self.clipid = FPNative.clip_write( self.handle )
    self.check_error()

    return self.clipid


  def close( self ):

    if( self.top_handle != 0 ):
      FPNative.tag_close( self.top_handle )
      self.check_error()

    if( self.handle != 0 ):
      FPNative.clip_close( self.handle )

    self.check_error()


  def getTopTag( self ):

    if( self.top_handle == 0 ):
      self.top_handle = FPNative.get_top_tag( self.handle )
      self.check_error()

    return self.top_handle


  def auditedDelete( self, clipid, reason, options ):

    FPNative.clip_audited_delete( self.pool_handle, clipid, \
      reason, options )
    self.check_error()


  def delete( self, clipid ):

    FPNative.clip_delete( self.pool_handle, clipid )
    self.check_error()


  def enableEbrWithClass( self, retention_class ):

    FPNative.clip_enable_ebr_with_class( self.handle, retention_class )
    self.check_error()


  def enableEbrWithPeriod( self, seconds ):

    FPNative.clip_enable_ebr_with_period( self.handle, seconds )
    self.check_error()


  def rawOpen( self, clipid, stream, options ):

    self.clip = FPNative.clip_raw_open( self.pool_handle, clipid, \
      stream, options )
    self.check_error()


  def rawRead( self, stream ):

    FPNative.clip_raw_read( self.handle, stream )
    self.check_error()


  def removeRetentionClass( self ):

    FPNative.clip_remove_retention_class( self.handle )
    self.check_error()


  def setName( self, name ):

    FPNative.clip_set_name( self.handle, name )
    self.check_error()


  def setRetentionClass( self, retention_class ):

    FPNative.clip_set_retention_class( self.handle, retention_class )
    self.check_error()


  def setRetentionHold( self, flag, id ):

    FPNative.clip_set_retention_hold( self.handle, flag, id )
    self.check_error()


  def setRetentionPeriod( self, seconds ):

    FPNative.clip_set_retention_period( self.handle, seconds )
    self.check_error()


  def triggerEbrEvent( self ):

    FPNative.clip_trigger_ebr_event( self.handle )
    self.check_error()


  def triggerEbrEventWithClass( self, retention_class ):

    FPNative.clip_trigger_ebr_event_with_class( self.handle, \
      retention_class )
    self.check_error()


  def triggerEbrEventWithPeriod( self, seconds ):

    FPNative.clip_trigger_ebr_event_with_period( self.handle, \
      seconds )
    self.check_error()


  def getCanonicalFormat( self, clipid ):

    self.canonical = FPNative.clip_get_canonical_format( clipid ) 
    self.check_error()

    return self.canonical


  def getStringFormat( self, canonical ):

    clipid = FPNative.clip_get_string_format( canonical )
    self.check_error()

    return clipid


  def exists( self, clipid ):

    b = FPNative.clip_exists( self.pool_handle, clipid )
    self.check_error()

    return b


  def getClipId( self ):

    clipid = FPNative.clip_get_clip_id( self.handle )
    self.check_error()

    return clipid


  def getCreationDate( self ):

    date = FPNative.clip_get_creation_date( self.handle )
    self.check_error()

    return date


  def getEbrClassName( self ):

    classname = FPNative.clip_get_ebr_class_name( self.handle )
    self.check_error()

    return classname


  def getEbrEventTime( self ):

    time = FPNative.clip_get_ebr_event_time( self.handle )
    self.check_error()

    return time


  def getEbrPeriod( self ):

    seconds = FPNative.clip_get_ebr_period( self.handle )
    self.check_error()

    return seconds


  def getName( self ):

    name = FPNative.clip_get_name( self.handle )
    self.check_error()

    return name


  def getNumBlobs( self ):

    blob_num = FPNative.clip_get_num_blobs( self.handle )
    self.check_error()

    return blob_num


  def getNumTags( self ):

    tag_num = FPNative.clip_get_num_tags( self.handle )
    self.check_error()

    return tag_num


  def getPoolRef( self ):

    poolref = FPNative.clip_get_pool_ref( self.handle )
    self.check_error()

    return poolref


  def getRetentionClassName( self ):

    classname = FPNative.clip_get_retention_class_name( self.handle )
    self.check_error()

    return classname


  def isRetentionHold( self ):

    value = FPNative.clip_get_retention_hold( self.handle )
    self.check_error()

    return value


  def getRetentionPeriod( self ):

    seconds = FPNative.clip_get_retention_period( self.handle )
    self.check_error()

    return seconds


  def getTotalSize( self ):

    size = FPNative.clip_get_total_size( self.handle )
    self.check_error()

    return size


  def isEbrEnabled( self ):

    value = FPNative.clip_is_ebr_enabled( self.handle )
    self.check_error()

    return value


  def isModified( self ):

    value = FPNative.clip_is_modified( self.handle )
    self.check_error()

    return value


  def isRetentionClassValid( self, retention_class ):

    value = FPNative.clip_validate_retention_class( self.handle, \
      retention_class )
    self.check_error()

    return value


  def getDescriptionAttribute( self, attribute ):

    value = FPNative.clip_get_description_attribute( self.handle, \
      attribute )
    self.check_error()

    return value


  def getDescriptionAttributeIndex( self, index ):

    value = FPNative.clip_get_description_attribute_index( self.handle, \
      attribute )
    self.check_error()

    return value


  def getNumDescriptionAttributes( self ):

    value = FPNative.clip_get_num_description_attributes( self.handle )
    self.check_error()

    return value


  def removeDescriptionAttribute( self, name ):

    FPNative.clip_remove_description_attribute( self.handle, name )
    self.check_error()


  def setDescriptionAttribute( self, name, value ):

    FPNative.clip_set_description_attribute( self.handle, name, value )
    self.check_error()


  def fetchNext( self ):

    tag = FPNative.clip_fetch_next( self.handle )
    self.check_error()

    return tag
