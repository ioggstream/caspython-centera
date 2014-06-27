///////////////////////////////////////////////////////////////////////////
//
//  Copyright (c) 2006 EMC Corporation. All Rights Reserved
//
//  This file is part of Python wrapper for the Centera SDK.
//
//  Python wrapper is free software; you can redistribute it and/or
//  modify it under the terms of the GNU General Public License as
//  published by the Free Software Foundation version 2.
//
//  In addition to the permissions granted in the GNU General Public
//  License version 2, EMC Corporation gives you unlimited permission
//  to link the compiled version of this file into combinations with
//  other programs, and to distribute those combinations without any
//  restriction coming from the use of this file. (The General Public
//  License restrictions do apply in other respects; for example,
//  they cover modification of the file, and distribution when not
//  linked into a combined executable.)
//
//  Python wrapper is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
//  General Public License version 2 for more details.
//
//  You should have received a copy of the GNU General Public License
//  version 2 along with Python wrapper; see the file COPYING. If not,
//  write to:
//
//   EMC Corporation 
//   Centera Open Source Intiative (COSI) 
//   80 South Street
//   1/W-1
//   Hopkinton, MA 01748 
//   USA
//
///////////////////////////////////////////////////////////////////////////

#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include "FPAPI.h"

#define MAX_ATTRIBUTE_LEN 102400
#define MAX_NAME_LEN      255
#define MAX_BUF_SIZE	  30*1024
/////////////////////////////////////////////////////////////////////
// Pool Functions
/////////////////////////////////////////////////////////////////////

//
//  pool_open
//
static PyObject *pool_open( PyObject *self, PyObject *args ) {

  const char *	connect;

  if( !PyArg_ParseTuple( args, "s", &connect ) ) {
    return NULL;
  }

  FPPoolRef pool = FPPool_Open( connect );

  return Py_BuildValue( "L", pool );


} // pool_open


//
//  pool_close
//
static PyObject *pool_close( PyObject *self, PyObject *args ) {

  FPPoolRef pool;

  if( !PyArg_ParseTuple( args, "L", &pool ) ) {
    return NULL;
  }

  FPPool_Close( pool );

  return Py_BuildValue( "b", true );

} // pool_close


//
//  get_component_version
//
static PyObject *get_component_version( PyObject *self, PyObject *args ) {

  const FPInt     component;
  char     	  version[128];
  FPInt           versionLen = 128;


  if( !PyArg_ParseTuple( args, "i", &component ) ) {
    return NULL;
  }

  FPPool_GetComponentVersion( component, version, &versionLen );

  return Py_BuildValue( "s", version );

} // get_component_version


//
//  SetGlobalOption
//
static PyObject *set_global_option( PyObject *self, PyObject *args ) {

  const char     *inOptionName;
  FPInt           inOptionValue;

  if( !PyArg_ParseTuple( args, "si", &inOptionName, &inOptionValue ) ) {
    return NULL;
  }

  FPPool_SetGlobalOption( inOptionName, inOptionValue );

  return Py_BuildValue( "b", true );

} // set_global_option


//
//  set_int_option
//
static PyObject *set_int_option( PyObject *self, PyObject *args ) {

  const char     *inOptionName;
  FPInt           inOptionValue;
  const FPPoolRef pool;

  if( !PyArg_ParseTuple( args, "Lsi", &pool, &inOptionName, &inOptionValue ) ) {
    return NULL;
  }

  FPPool_SetIntOption( pool, inOptionName, inOptionValue );

  return Py_BuildValue( "b", true );

} // set_int_option


//
//  get_cluster_time
//
static PyObject *get_cluster_time( PyObject *self, PyObject *args ) {

  const FPPoolRef pool;
  char           time[MAX_NAME_LEN];
  FPInt          length = MAX_NAME_LEN;

  if( !PyArg_ParseTuple( args, "L", &pool ) ) {
    return NULL;
  }

  FPPool_GetClusterTime( pool, time, &length );

  return Py_BuildValue( "s", time );

} // get_cluster_time


//
//  get_capability
//
static PyObject *get_capability( PyObject *self, PyObject *args ) {

  FPPoolRef       pool;
  const char     *name;
  const char     *attr_name;
  char	          value[MAX_NAME_LEN];
  FPInt		  value_length = MAX_NAME_LEN;

  if( !PyArg_ParseTuple( args, "Lss", &pool, &name, &attr_name ) ) {
    return NULL;
  }

  FPPool_GetCapability( pool, name, attr_name, value, &value_length );

  return Py_BuildValue( "s", value );

} // get_capability


//
//  get_clip_id
//
static PyObject *get_clip_id( PyObject *self, PyObject *args ) {

  FPPoolRef			pool;
  FPClipID			contentAddress;

  if( !PyArg_ParseTuple( args, "L", &pool ) ) {
    return NULL;
  }

  FPPool_GetClipID( pool, contentAddress );

  return Py_BuildValue( "s", contentAddress );

} // get_clip_id


//
//  get_global_option
//
static PyObject *get_global_option( PyObject *self, PyObject *args ) {

  const char     *inOptionName;
  FPInt           value;

  if( !PyArg_ParseTuple( args, "s", &inOptionName ) ) {
    return NULL;
  }

  value = FPPool_GetGlobalOption( inOptionName );

  return Py_BuildValue( "i", value );

} // get_global_option


//
//  get_int_option
//
static PyObject *get_int_option( PyObject *self, PyObject *args ) {

  FPPoolRef				pool;
  const char           *inOptionName;
  FPInt					value;

  if( !PyArg_ParseTuple( args, "Ls", &pool, &inOptionName ) ) {
    return NULL;
  }

  value = FPPool_GetIntOption( pool, inOptionName );

  return Py_BuildValue( "i", value );

} // get_int_option


//
//  get_pool_info
//
static PyObject *get_pool_info( PyObject *self, PyObject *args ) {

  FPPoolRef			pool;
  FPPoolInfo	    poolInfo;
  PyObject 		   *list		= NULL;

  if( !PyArg_ParseTuple( args, "L", &pool ) ) {
    return NULL;
  }

  FPPool_GetPoolInfo( pool, &poolInfo );

  list = PyList_New(0);

  if( PyList_Append( list, Py_BuildValue( "i", poolInfo.poolInfoVersion ) ) != 0 ) {
	PyErr_SetString( PyExc_Exception, "FPPoolInfo Parsing Failure" );
	return NULL;
  }

  if( PyList_Append( list, Py_BuildValue( "L", poolInfo.capacity ) ) != 0 ) {
	PyErr_SetString( PyExc_Exception, "FPPoolInfo Parsing Failure" );
	return NULL;
  }

  if( PyList_Append( list, Py_BuildValue( "L", poolInfo.freeSpace ) ) != 0 ) {
	PyErr_SetString( PyExc_Exception, "FPPoolInfo Parsing Failure" );
	return NULL;
  }

  if( PyList_Append( list, Py_BuildValue( "s", poolInfo.clusterID ) ) != 0 ) {
	PyErr_SetString( PyExc_Exception, "FPPoolInfo Parsing Failure" );
	return NULL;
  }

  if( PyList_Append( list, Py_BuildValue( "s", poolInfo.clusterName ) ) != 0 ) {
	PyErr_SetString( PyExc_Exception, "FPPoolInfo Parsing Failure" );
	return NULL;
  }

  if( PyList_Append( list, Py_BuildValue( "s", poolInfo.version ) ) != 0 ) {
	PyErr_SetString( PyExc_Exception, "FPPoolInfo Parsing Failure" );
	return NULL;
  }

  if( PyList_Append( list, Py_BuildValue( "s", poolInfo.replicaAddress ) ) != 0 ) {
	PyErr_SetString( PyExc_Exception, "FPPoolInfo Parsing Failure" );
	return NULL;
  }

  return list;

} // get_pool_info


//
//  get_retention_class_context
//
static PyObject *get_retention_class_context( PyObject *self, PyObject *args ) {

  FPPoolRef						pool;
  FPRetentionClassContextRef	classRef;

  if( !PyArg_ParseTuple( args, "L", &pool ) ) {
    return NULL;
  }

  classRef = FPPool_GetRetentionClassContext( pool );

  return Py_BuildValue( "L", classRef );

} // get_retention_class_context


//
//  register_application
//
static PyObject *register_application( PyObject *self, PyObject *args ) {

  const char     *inAppName;
  const char     *inAppVer;

  if( !PyArg_ParseTuple( args, "ss", &inAppName, &inAppVer ) ) {
    return NULL;
  }

  FPPool_RegisterApplication( inAppName, inAppVer );

  return Py_BuildValue( "b", true );

} // register_application


//
//  set_clip_id
//
static PyObject *set_clip_id( PyObject *self, PyObject *args ) {

  FPPoolRef				pool;
  const FPClipID		contentAddress;

  if( !PyArg_ParseTuple( args, "Ls", &pool, &contentAddress ) ) {
    return NULL;
  }

  FPPool_SetClipID( pool, contentAddress );

  return Py_BuildValue( "b", true );

} // set_clip_id



/////////////////////////////////////////////////////////////////////
// Error Handling Functions
/////////////////////////////////////////////////////////////////////

//
//  get_last_error
//
static PyObject *get_last_error( PyObject *self, PyObject *args ) {

  return Py_BuildValue( "i", FPPool_GetLastError() );

} // get_last_error


//
//  get_last_error_info
//
static PyObject *get_last_error_info( PyObject *self, PyObject *args ) {

  FPErrorInfo 	errInfo;
  PyObject     *list		= NULL;

  FPPool_GetLastErrorInfo(&errInfo);

  list = PyList_New(0);

  if( PyList_Append( list, Py_BuildValue( "i", errInfo.error ) ) != 0 ) {
    PyErr_SetString( PyExc_Exception, "ErrorInfo Structure Parsing Failure" );
    return NULL;
  }

  if( PyList_Append( list, Py_BuildValue( "i", errInfo.systemError ) ) != 0 ) {
    PyErr_SetString( PyExc_Exception, "ErrorInfo Structure Parsing Failure" );
    return NULL;
  }

  if( PyList_Append( list, PyString_FromString( errInfo.trace ) ) != 0 ) {
    PyErr_SetString( PyExc_Exception, "ErrorInfo Structure Parsing Failure" );
    return NULL;
  }

  if( PyList_Append( list, PyString_FromString( errInfo.message ) ) != 0 ) {
    PyErr_SetString( PyExc_Exception, "ErrorInfo Structure Parsing Failure" );
    return NULL;
  }

  if( PyList_Append( list, PyString_FromString( errInfo.errorString ) ) != 0 ) {
    PyErr_SetString( PyExc_Exception, "ErrorInfo Structure Parsing Failure" );
    return NULL;
  }

  if( PyList_Append( list, Py_BuildValue( "i", errInfo.errorClass ) ) != 0 ) {
    PyErr_SetString( PyExc_Exception, "ErrorInfo Structure Parsing Failure" );
    return NULL;
  }

  return list;

} // get_last_error_info


/////////////////////////////////////////////////////////////////////
// Clip Functions
/////////////////////////////////////////////////////////////////////


//
//  clip_create
//
//  @param  pool reference
//  @param  clip name
//
static PyObject *clip_create( PyObject *self, PyObject *args ) {

  FPClipRef	clip;
  const char *	clipname;
  FPPoolRef     pool;

  if( !PyArg_ParseTuple( args, "Ls", &pool, &clipname ) ) {
    return NULL;
  }

  clip = FPClip_Create( pool, clipname );

  return Py_BuildValue( "L", clip );


} // clip_create


//
//  clip_write
//
//  @param  pool reference
//  @param  file name
//
static PyObject *clip_write( PyObject *self, PyObject *args ) {

  FPClipRef	clip;
  FPClipID	clipid;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  FPClip_Write( clip, clipid );

  return Py_BuildValue( "s", clipid );


} // clip_write


//
//  clip_open
//
//  @param  pool reference
//  @param  clip id
//
static PyObject *clip_open( PyObject *self, PyObject *args ) {

  const FPPoolRef			pool;
  const FPClipID     			clipid;
  const char *                          id;
  const FPInt				mode;
  FPClipRef				clip;

  if( !PyArg_ParseTuple( args, "Lsi", &pool, &id, &mode ) ) {
    return NULL;
  }

  memcpy( (void *)clipid, id, 64 );
  clip = FPClip_Open( pool, clipid, mode );

  return Py_BuildValue( "L", clip );

} // clip_open


//
//  clip_close
//
//  @param  pool reference
//  @param  clip id
//
static PyObject *clip_close( PyObject *self, PyObject *args ) {

  FPClipRef     clip;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  FPClip_Close( clip );

  return Py_BuildValue( "b", true );

} // clip_close


//
//  get_top_tag
//
//  @param  pool reference
//  @param  file name
//
static PyObject *get_top_tag( PyObject *self, PyObject *args ) {

  FPClipRef     clip;
  FPTagRef      top;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  top = FPClip_GetTopTag(clip);

  return Py_BuildValue( "L", top );


} // get_top_tag


//
//  clip_audited_delete
//
static PyObject *clip_audited_delete( PyObject *self, PyObject *args ) {

  FPPoolRef			pool;
  FPClipID			clipid;
  const char                   *reason;
  FPLong			options;
  const char                   *id;

  if( !PyArg_ParseTuple( args, "LssL", &pool, &id, &reason, &options  ) ) {
    return NULL;
  }

  memcpy( (void *)clipid, id, 64 );

  FPClip_AuditedDelete( pool, clipid, reason, options );

  return Py_BuildValue( "b", true );

} // clip_audited_delete


//
//  clip_delete
//
static PyObject *clip_delete( PyObject *self, PyObject *args ) {

  FPPoolRef				pool;
  FPClipID				clipid;
  const char                           *id;  

  if( !PyArg_ParseTuple( args, "Ls", &pool, &id ) ) {
    return NULL;
  }

  memcpy( (void *)clipid, id, 64 );
  
  FPClip_Delete( pool, clipid );

  return Py_BuildValue( "b", true );

} // clip_delete


//
//  clip_enable_ebr_with_class
//
static PyObject *clip_enable_ebr_with_class( PyObject *self, PyObject *args ) {

  FPClipRef				clip;
  FPRetentionClassRef	retention_class;

  if( !PyArg_ParseTuple( args, "LL", &clip, &retention_class ) ) {
    return NULL;
  }

  FPClip_EnableEBRWithClass( clip, retention_class );

  return Py_BuildValue( "b", true );

} // clip_enable_ebr_with_class


//
//  clip_enable_ebr_with_period
//
static PyObject *clip_enable_ebr_with_period( PyObject *self, PyObject *args ) {

  FPClipRef				clip;
  FPLong				seconds;

  if( !PyArg_ParseTuple( args, "LL", &clip, &seconds ) ) {
    return NULL;
  }

  FPClip_EnableEBRWithPeriod( clip, seconds );

  return Py_BuildValue( "b", true );

} // clip_enable_ebr_with_period


//
//  clip_raw_open
//
static PyObject *clip_raw_open( PyObject *self, PyObject *args ) {

  FPPoolRef					pool;
  FPClipID					clipid;
  const FPStreamRef			stream;
  const FPLong				options;

  FPClipRef					clip;

  if( !PyArg_ParseTuple( args, "LsLL", &pool, &clipid, &stream,
    &options ) ) {
    return NULL;
  }

  clip = FPClip_RawOpen( pool, clipid, stream, options );

  return Py_BuildValue( "L", clip );

} // clip_raw_open


//
//  clip_raw_read
//
static PyObject *clip_raw_read( PyObject *self, PyObject *args ) {

  const FPClipRef					clip;
  const FPStreamRef					stream;

  if( !PyArg_ParseTuple( args, "LL", &clip, &stream ) ) {
    return NULL;
  }

  FPClip_RawRead( clip, stream );

  return Py_BuildValue( "b", true );

} // clip_raw_read


//
//  clip_remove_retention_class
//
static PyObject *clip_remove_retention_class( PyObject *self, PyObject *args ) {

  const FPClipRef				clip;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  FPClip_RemoveRetentionClass( clip );

  return Py_BuildValue( "b", true );

} // clip_remove_retention_class


//
//  clip_set_name
//
static PyObject *clip_set_name( PyObject *self, PyObject *args ) {

  const FPClipRef					clip;
  const char					   *clip_name;

  if( !PyArg_ParseTuple( args, "Ls", &clip, &clip_name ) ) {
    return NULL;
  }

  FPClip_SetName( clip, clip_name );

  return Py_BuildValue( "b", true );

} // clip_set_name


//
//  clip_set_retention_class
//
static PyObject *clip_set_retention_class( PyObject *self, PyObject *args ) {

  const FPClipRef				clip;
  const FPRetentionClassRef		retention_class;

  if( !PyArg_ParseTuple( args, "LL", &clip, &retention_class ) ) {
    return NULL;
  }

  FPClip_SetRetentionClass( clip, retention_class );

  return Py_BuildValue( "b", true );

} // clip_set_retention_class


//
//  clip_set_retention_hold
//
static PyObject *clip_set_retention_hold( PyObject *self, PyObject *args ) {

  const FPClipRef				clip;
  const FPBool					hold_flag;
  const char				   *holdid;

  if( !PyArg_ParseTuple( args, "Lbs", &clip, &hold_flag, &holdid ) ) {
    return NULL;
  }

  FPClip_SetRetentionHold( clip, hold_flag, holdid );

  return Py_BuildValue( "b", true );

} // clip_set_retention_hold


//
//  clip_set_retention_period
//
static PyObject *clip_set_retention_period( PyObject *self, PyObject *args ) {

  const FPClipRef				clip;
  const FPLong					seconds;

  if( !PyArg_ParseTuple( args, "LL", &clip, &seconds ) ) {
    return NULL;
  }

  FPClip_SetRetentionPeriod( clip, seconds );

  return Py_BuildValue( "b", true );

} // clip_set_retention_period


//
//  clip_trigger_ebr_event
//
static PyObject *clip_trigger_ebr_event( PyObject *self, PyObject *args ) {

  const FPClipRef			clip;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  FPClip_TriggerEBREvent( clip );

  return Py_BuildValue( "b", true );

} // clip_trigger_ebr_event


//
//  clip_trigger_ebr_event_with_class
//
static PyObject *clip_trigger_ebr_event_with_class( PyObject *self,
  PyObject *args ) {

  const FPClipRef				clip;
  const FPRetentionClassRef		retention_class;

  if( !PyArg_ParseTuple( args, "LL", &clip, &retention_class ) ) {
    return NULL;
  }

  FPClip_TriggerEBREventWithClass( clip, retention_class );

  return Py_BuildValue( "b", true );

} // clip_trigger_ebr_event_with_class


//
//  clip_trigger_ebr_event_with_period
//
static PyObject *clip_trigger_ebr_event_with_period( PyObject *self, PyObject *args ) {

  const FPClipRef				clip;
  const FPLong					seconds;

  if( !PyArg_ParseTuple( args, "LL", &clip, &seconds ) ) {
    return NULL;
  }

  FPClip_TriggerEBREventWithPeriod( clip, seconds );

  return Py_BuildValue( "b", true );

} // clip_trigger_ebr_event_with_period


//
//  clip_get_canonical_format
//
static PyObject *clip_get_canonical_format( PyObject *self, PyObject *args ) {

  const FPClipID				clipid;
  FPCanonicalClipID				canonical;

  if( !PyArg_ParseTuple( args, "s", &clipid ) ) {
    return NULL;
  }

  FPClipID_GetCanonicalFormat( clipid, canonical );

  return Py_BuildValue( "s", canonical );

} // clip_get_canonical_format


//
//  clip_get_string_format
//
static PyObject *clip_get_string_format( PyObject *self, PyObject *args ) {

  const FPCanonicalClipID				canonical;
  FPClipID								clipid;

  if( !PyArg_ParseTuple( args, "s", &canonical ) ) {
    return NULL;
  }

  FPClipID_GetStringFormat( canonical, clipid );

  return Py_BuildValue( "s", clipid );

} // clip_get_string_format


//
//  clip_exists
//
static PyObject *clip_exists( PyObject *self, PyObject *args ) {

  const FPPoolRef					pool;
  const FPClipID					clipid;
  FPBool						    value;

  if( !PyArg_ParseTuple( args, "Ls", &pool, &clipid ) ) {
    return NULL;
  }

  value = FPClip_Exists( pool, clipid );

  return Py_BuildValue( "b", value );

} // clip_exists


//
//  clip_get_clip_id
//
static PyObject *clip_get_clip_id( PyObject *self, PyObject *args ) {

  const FPClipRef				clip;
  FPClipID						clipid;

  if( !PyArg_ParseTuple( args, "Ls", &clip) ) {
    return NULL;
  }

  FPClip_GetClipID( clip, clipid );

  return Py_BuildValue( "s", clipid );

} // clip_get_clip_id


//
//  clip_get_creation_date
//
static PyObject *clip_get_creation_date( PyObject *self, PyObject *args ) {

  const FPClipRef				clip;
  char						date[MAX_NAME_LEN];
  FPInt						dateLen;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  FPClip_GetCreationDate( clip, date, &dateLen );

  return Py_BuildValue( "s", date );

} // clip_get_creation_date


//
//  clip_get_ebr_class_name
//
static PyObject *clip_get_ebr_class_name( PyObject *self, PyObject *args ) {

  const FPClipRef				clip;
  char						class_name[MAX_NAME_LEN];
  FPInt					        name_length;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  FPClip_GetEBRClassName( clip, class_name, &name_length );

  return Py_BuildValue( "s", class_name );

} // clip_get_ebr_class_name


//
//  clip_get_ebr_event_time
//
static PyObject *clip_get_ebr_event_time( PyObject *self, PyObject *args ) {

  const FPClipRef				clip;
  char						EBREventTime[MAX_NAME_LEN];
  FPInt						EBREventTimeLen;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  FPClip_GetEBREventTime( clip, EBREventTime, &EBREventTimeLen );

  return Py_BuildValue( "s", EBREventTime );

} // clip_get_ebr_event_time


//
//  clip_get_ebr_period
//
static PyObject *clip_get_ebr_period( PyObject *self, PyObject *args ) {

  const FPClipRef				clip;
  FPLong						period;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  period = FPClip_GetEBRPeriod( clip );

  return Py_BuildValue( "L", period );

} // clip_get_ebr_period


//
//  clip_get_name
//
static PyObject *clip_get_name( PyObject *self, PyObject *args ) {

  const FPClipRef				clip;
  char						name[MAX_NAME_LEN];
  FPInt						length;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  FPClip_GetName( clip, name, &length );

  return Py_BuildValue( "s", name );

} // clip_get_name


//
//  clip_get_num_blobs
//
static PyObject *clip_get_num_blobs( PyObject *self, PyObject *args ) {

  const FPClipRef			clip;
  FPInt						total;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  total = FPClip_GetNumBlobs( clip );

  return Py_BuildValue( "i", total );

} // clip_get_num_blobs


//
//  clip_get_num_tags
//
static PyObject *clip_get_num_tags( PyObject *self, PyObject *args ) {

  const FPClipRef			clip;
  FPInt						tag_total;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  tag_total = FPClip_GetNumTags( clip );

  return Py_BuildValue( "i", tag_total );

} // clip_get_num_tags


//
//  clip_get_pool_ref
//
static PyObject *clip_get_pool_ref( PyObject *self, PyObject *args ) {

  const FPClipRef			clip;
  FPPoolRef					pool;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  pool = FPClip_GetPoolRef( clip );

  return Py_BuildValue( "L", pool );

} // clip_get_pool_ref


//
//  clip_get_retention_class_name
//
static PyObject *clip_get_retention_class_name( PyObject *self, PyObject *args ) {

  const FPClipRef			clip;
  char					name[MAX_NAME_LEN];
  FPInt					length;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  FPClip_GetRetentionClassName( clip, name, &length );

  return Py_BuildValue( "s", name );

} // clip_get_retention_class_name


//
//  clip_get_retention_hold
//
static PyObject *clip_get_retention_hold( PyObject *self, PyObject *args ) {

  const FPClipRef			clip;
  FPBool					value;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  value = FPClip_GetRetentionHold( clip );

  return Py_BuildValue( "b", value );

} // clip_get_retention_hold


//
//  clip_get_retention_period
//
static PyObject *clip_get_retention_period( PyObject *self, PyObject *args ) {

  const FPClipRef			clip;
  FPLong				    seconds;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  seconds = FPClip_GetRetentionPeriod( clip );

  return Py_BuildValue( "L", seconds );

} // clip_get_retention_period


//
//  clip_get_total_size
//
static PyObject *clip_get_total_size( PyObject *self, PyObject *args ) {

  const FPClipRef			clip;
  FPLong					size;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  size = FPClip_GetTotalSize( clip );

  return Py_BuildValue( "L", size );

} // clip_get_total_size


//
//  clip_is_ebr_enabled
//
static PyObject *clip_is_ebr_enabled( PyObject *self, PyObject *args ) {

  const FPClipRef			clip;
  FPBool					value;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  };

  value = FPClip_IsEBREnabled( clip );

  return Py_BuildValue( "b", value );

} // clip_is_ebr_enabled


//
//  clip_is_modified
//
static PyObject *clip_is_modified( PyObject *self, PyObject *args ) {

  const FPClipRef			clip;
  FPBool					value;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  value = FPClip_IsModified( clip );

  return Py_BuildValue( "b", value );

} // clip_is_modified


//
//  clip_validate_retention_class
//
static PyObject *clip_validate_retention_class( PyObject *self, PyObject *args ) {

  const FPClipRef						clip;
  const FPRetentionClassContextRef		retention_class;
  FPBool								value;

  if( !PyArg_ParseTuple( args, "LL", &clip, &retention_class ) ) {
    return NULL;
  }

  value =FPClip_ValidateRetentionClass( clip, retention_class );

  return Py_BuildValue( "b", value );

} // clip_validate_retention_class


//
//  clip_get_description_attribute
//
static PyObject *clip_get_description_attribute( PyObject *self, PyObject *args ) {

  const FPClipRef			clip;
  const char			   *attr_name;
  char			           attr_value[MAX_ATTRIBUTE_LEN];
  FPInt			           length;

  if( !PyArg_ParseTuple( args, "Ls", &clip, &attr_name ) ) {
    return NULL;
  }

  FPClip_GetDescriptionAttribute( clip, attr_name, attr_value, &length );

  return Py_BuildValue( "s", attr_value );

} // clip_get_description_attribute


//
//  clip_get_description_attribute_index
//
static PyObject *clip_get_description_attribute_index( PyObject *self, PyObject *args ) {

  const FPClipRef			clip;
  const FPInt			    index;
  char			           attr_name[MAX_NAME_LEN];
  FPInt			           name_length;
  char			           attr_value[MAX_NAME_LEN];
  FPInt			           value_length;

  PyObject                 *list			= NULL;

  if( !PyArg_ParseTuple( args, "Ls", &clip, &index ) ) {
    return NULL;
  }

  FPClip_GetDescriptionAttributeIndex( clip, index, attr_name,
    &name_length, attr_value, &value_length );

  list = PyList_New(0);

  if( PyList_Append( list, Py_BuildValue( "s", attr_name ) ) != 0 ) {
  	PyErr_SetString( PyExc_Exception, "Clip Description Attribute Parsing Failure" );
  	return NULL;
  }

  if( PyList_Append( list, Py_BuildValue( "s", attr_value ) ) != 0 ) {
    PyErr_SetString( PyExc_Exception, "Clip Description Attribute Parsing Failure" );
    return NULL;
  }

  return list;

} // clip_get_description_attribute_index


//
//  clip_get_num_description_attributes
//
static PyObject *clip_get_num_description_attributes( PyObject *self, PyObject *args ) {

  const FPClipRef				clip;
  FPInt							total;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  total = FPClip_GetNumDescriptionAttributes( clip );

  return Py_BuildValue( "i", total );

} // clip_get_num_description_attributes


//
//  clip_remove_description_attribute
//
static PyObject *clip_remove_description_attribute( PyObject *self, PyObject *args ) {

  const FPClipRef				clip;
  const char				   *name;

  if( !PyArg_ParseTuple( args, "L", &clip, &name ) ) {
    return NULL;
  }

  FPClip_RemoveDescriptionAttribute( clip, name );

  return Py_BuildValue( "b", true );

} // clip_remove_description_attribute


//
//  clip_set_description_attribute
//
static PyObject *clip_set_description_attribute( PyObject *self, PyObject *args ) {

  const FPClipRef		clip;
  const char           *name;
  const char           *value;

  if( !PyArg_ParseTuple( args, "Lss", &clip, &name, &value ) ) {
    return NULL;
  }

  FPClip_SetDescriptionAttribute( clip, name, value );

  return Py_BuildValue( "b", true );

} // clip_set_description_attribute


//
//  clip_fetch_next
//
static PyObject *clip_fetch_next( PyObject *self, PyObject *args ) {

  const FPClipRef			clip;
  FPTagRef					tag;

  if( !PyArg_ParseTuple( args, "L", &clip ) ) {
    return NULL;
  }

  tag = FPClip_FetchNext( clip );

  return Py_BuildValue( "L", tag );

} // clip_fetch_next


/////////////////////////////////////////////////////////////////////
// Tag Functions
/////////////////////////////////////////////////////////////////////


//
//  tag_create
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_create( PyObject *self, PyObject *args ) {

  FPTagRef      top;
  const char *  tagname;
  FPTagRef      tag;

  if( !PyArg_ParseTuple( args, "Ls", &top, &tagname ) ) {
    return NULL;
  }

  tag = FPTag_Create( top, tagname );

  return Py_BuildValue( "L", tag );


} // tag_create


//
//  tag_close
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_close( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;

  if( !PyArg_ParseTuple( args, "L", &tag ) ) {
    return NULL;
  }

  FPTag_Close(tag);

  return Py_BuildValue( "b", true );


} // tag_close


//
//  tag_copy
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_copy( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  const FPTagRef  	parent;
  const FPInt		options;
  FPTagRef			newtag;

  if( !PyArg_ParseTuple( args, "LLi", &tag, &parent, &options ) ) {
    return NULL;
  }

  newtag = FPTag_Copy( tag, parent, options );

  return Py_BuildValue( "L", newtag );


} // tag_copy


//
//  tag_delete
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_delete( PyObject *self, PyObject *args ) {

  FPTagRef	tag;

  if( !PyArg_ParseTuple( args, "L", &tag ) ) {
    return NULL;
  }

  FPTag_Delete( tag );

  return Py_BuildValue( "b", true );


} // tag_delete


//
//  tag_get_blob_size
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_get_blob_size( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  FPLong			size;

  if( !PyArg_ParseTuple( args, "L", &tag ) ) {
    return NULL;
  }

  size = FPTag_GetBlobSize(tag);

  return Py_BuildValue( "L", size );


} // tag_get_blob_size


//
//  tag_get_clip_ref
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_get_clip_ref( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  FPClipRef			clip;

  if( !PyArg_ParseTuple( args, "L", &tag ) ) {
    return NULL;
  }

  clip = FPTag_GetClipRef( tag );

  return Py_BuildValue( "L", clip );


} // tag_get_clip_ref


//
//  tag_get_pool_ref
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_get_pool_ref( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  FPPoolRef			pool;

  if( !PyArg_ParseTuple( args, "L", &tag ) ) {
    return NULL;
  }

  pool = FPTag_GetPoolRef(tag);

  return Py_BuildValue( "L", pool );


} // tag_get_pool_ref


//
//  tag_get_tag_name
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_get_tag_name( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  char			name[MAX_NAME_LEN];
  FPInt			length;

  if( !PyArg_ParseTuple( args, "L", &tag ) ) {
    return NULL;
  }

  FPTag_GetTagName( tag, name, &length );

  return Py_BuildValue( "s", name );


} // tag_get_tag_name


//
//  tag_get_first_child
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_get_first_child( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  FPTagRef			child;

  if( !PyArg_ParseTuple( args, "L", &tag ) ) {
    return NULL;
  }

  child = FPTag_GetFirstChild( tag );

  return Py_BuildValue( "L", child );


} // tag_get_first_child


//
//  tag_get_parent
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_get_parent( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  FPTagRef			parent;

  if( !PyArg_ParseTuple( args, "L", &tag ) ) {
    return NULL;
  }

  parent = FPTag_GetParent( tag );

  return Py_BuildValue( "L", parent );


} // tag_get_parent


//
//  tag_get_prev_sibling
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_get_prev_sibling( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  FPTagRef			sibling;

  if( !PyArg_ParseTuple( args, "L", &tag ) ) {
    return NULL;
  }

  sibling = FPTag_GetPrevSibling( tag );

  return Py_BuildValue( "L", sibling );


} // tag_get_prev_sibling


//
//  tag_get_sibling
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_get_sibling( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  FPTagRef			sibling;

  if( !PyArg_ParseTuple( args, "L", &tag ) ) {
    return NULL;
  }

  sibling = FPTag_GetSibling( tag );

  return Py_BuildValue( "L", sibling );


} // tag_get_sibling


//
//  tag_get_bool_attribute
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_get_bool_attribute( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  const char	   *name;
  FPBool			value		= true;

  if( !PyArg_ParseTuple( args, "Ls", &tag, &name ) ) {
    return NULL;
  }

  value = FPTag_GetBoolAttribute( tag, name );

  return Py_BuildValue( "b", value );


} // tag_get_bool_attribute


//
//  tag_get_index_attribute
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_get_index_attribute( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  const FPInt		index;
  char			   name[MAX_ATTRIBUTE_LEN];
  FPInt			   name_length;
  char			   value[MAX_ATTRIBUTE_LEN];
  FPInt			   value_length;

  PyObject 		   *list			= NULL;

  if( !PyArg_ParseTuple( args, "Li", &tag, &index ) ) {
    return NULL;
  }

  FPTag_GetIndexAttribute( tag, index, name, &name_length, value,
    &value_length );

  list = PyList_New(0);

  if( PyList_Append( list, Py_BuildValue( "s", name ) ) != 0 ) {
    PyErr_SetString( PyExc_Exception, "Tag Index Attribute Parsing Failure" );
  	return NULL;
  }

  if( PyList_Append( list, Py_BuildValue( "s", value ) ) != 0 ) {
    PyErr_SetString( PyExc_Exception, "Tag Index Attribute Parsing Failure" );
  	return NULL;
  }

  return list;


} // tag_get_index_attribute


//
//  tag_get_long_attribute
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_get_long_attribute( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  const char       *name;
  FPLong			value;

  if( !PyArg_ParseTuple( args, "Ls", &tag, &name ) ) {
    return NULL;
  }

  value = FPTag_GetLongAttribute( tag, name );

  return Py_BuildValue( "L", value );


} // tag_get_long_attribute


//
//  tag_get_num_attribute
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_get_num_attribute( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  FPInt				value;

  if( !PyArg_ParseTuple( args, "L", &tag ) ) {
    return NULL;
  }

  value = FPTag_GetNumAttributes(tag);

  return Py_BuildValue( "i", value );


} // tag_get_num_attribute


//
//  tag_get_string_attribute
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_get_string_attribute( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  const char       *name;
  char             value[MAX_ATTRIBUTE_LEN];
  FPInt			   length		= MAX_ATTRIBUTE_LEN;

  if( !PyArg_ParseTuple( args, "Ls", &tag, &name ) ) {
    return NULL;
  }

  FPTag_GetStringAttribute( tag, name, value, &length );

  return Py_BuildValue( "s", value );


} // tag_get_string_attribute


//
//  tag_remove_attribute
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_remove_attribute( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  const char       *name;

  if( !PyArg_ParseTuple( args, "Ls", &tag, &name ) ) {
    return NULL;
  }

  FPTag_RemoveAttribute( tag, name );

  return Py_BuildValue( "b", true );


} // tag_remove_attribute


//
//  tag_set_bool_attribute
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_set_bool_attribute( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  const char       *name;
  const FPBool      value;

  if( !PyArg_ParseTuple( args, "Lsb", &tag, &name, &value ) ) {
    return NULL;
  }

  FPTag_SetBoolAttribute( tag, name, value );

  return Py_BuildValue( "b", true );


} // tag_set_bool_attribute


//
//  tag_set_long_attribute
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_set_long_attribute( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  const char       *name;
  const FPLong	    value;

  if( !PyArg_ParseTuple( args, "LsL", &tag, &name, &value ) ) {
    return NULL;
  }

  FPTag_SetLongAttribute( tag, name, value );

  return Py_BuildValue( "b", true );


} // tag_set_long_attribute


//
//  tag_set_string_attribute
//
//  @param  pool reference
//  @param  file name
//
static PyObject *tag_set_string_attribute( PyObject *self, PyObject *args ) {

  const FPTagRef	tag;
  const char       *name;
  const char       *value;

  if( !PyArg_ParseTuple( args, "Lss", &tag, &name, &value ) ) {
    return NULL;
  }

  FPTag_SetStringAttribute( tag, name, value );

  return Py_BuildValue( "b", true );


} // tag_set_string_attribute


/////////////////////////////////////////////////////////////////////
// Blob Functions
/////////////////////////////////////////////////////////////////////

//
//  blob_write
//
//  @param  pool reference
//  @param  file name
//
static PyObject *blob_write( PyObject *self, PyObject *args ) {

  FPStreamRef   stream;
  FPTagRef      tag;
  FPLong        options;

  if( !PyArg_ParseTuple( args, "LLL", &tag, &stream, &options ) ) {
    return NULL;
  }

  FPTag_BlobWrite( tag, stream, options );

  return Py_BuildValue( "b", true );


} // blob_write


//
//  blob_write_partial
//
//  @param  pool reference
//  @param  file name
//
static PyObject *blob_write_partial( PyObject *self, PyObject *args ) {

  FPStreamRef   stream;
  FPTagRef      tag;
  FPLong        options;
  FPLong        sequence_id;


  if( !PyArg_ParseTuple( args, "LLLL", &tag, &stream, &options,
    &sequence_id ) ) {

    return NULL;

  }

  FPTag_BlobWritePartial( tag, stream, options, sequence_id );

  return Py_BuildValue( "b", true );


} // blob_write_partial



//
//  blob_exists
//
//  @param  pool reference
//  @param  file name
//
static PyObject *blob_exists( PyObject *self, PyObject *args ) {

  FPTagRef      tag;
  int           value;

  if( !PyArg_ParseTuple( args, "L", &tag ) ) {
    return NULL;
  }

  value = FPTag_BlobExists( tag );

  return Py_BuildValue( "i", value );


} // blob_exists


//
//  blob_read
//
//  @param  pool reference
//  @param  file name
//
static PyObject *blob_read( PyObject *self, PyObject *args ) {

  FPStreamRef   stream;
  FPTagRef      tag;
  FPLong        options;

  if( !PyArg_ParseTuple( args, "LLL", &tag, &stream, &options ) ) {
    return NULL;
  }

  FPTag_BlobRead( tag, stream, options );

  return Py_BuildValue( "b", true );


} // blob_read


//
//  blob_read_partial
//
//  @param  pool reference
//  @param  file name
//
static PyObject *blob_read_partial( PyObject *self, PyObject *args ) {

  FPStreamRef   stream;
  FPTagRef      tag;
  FPLong        options;
  FPLong        offset;
  FPLong        read_length;

  if( !PyArg_ParseTuple( args, "LLLLL", &tag, &stream, &offset,
    &read_length, &options ) ) {

    return NULL;

  }

  FPTag_BlobReadPartial( tag, stream, offset, read_length, options );

  return Py_BuildValue( "b", true );


} // blob_read_partial



/////////////////////////////////////////////////////////////////////
// Stream Functions
/////////////////////////////////////////////////////////////////////

//
//  create_file_istream
//
//  @param  pool reference
//  @param  file name
//
static PyObject *create_file_istream( PyObject *self, PyObject *args ) {

  const char *  filename;
  const char *  flag;
  int           buffer;
  FPStreamRef   stream;

  if( !PyArg_ParseTuple( args, "ssi", &filename, &flag, &buffer ) ) {
    return NULL;
  }

  stream = FPStream_CreateFileForInput( filename, flag, buffer );

  return Py_BuildValue( "L", stream );


} // create_file_istream


//
//  create_file_ostream
//
//  @param  pool reference
//  @param  file name
//
static PyObject *create_file_ostream( PyObject *self, PyObject *args ) {

  FPStreamRef   stream;
  const char   *filepath;
  const char   *flag;

  if( !PyArg_ParseTuple( args, "ss", &filepath, &flag ) ) {
    return NULL;
  }

  stream = FPStream_CreateFileForOutput( filepath, flag );

  return Py_BuildValue( "L", stream );


} // create_file_ostream


//
//  create_buffer_istream
//
//  @param  pool reference
//  @param  file name
//
static PyObject *create_buffer_istream( PyObject *self, PyObject *args ) {

  FPStreamRef   stream;
  char         *buffer;
  int           length = 0;

  if( !PyArg_ParseTuple( args, "s#i", &buffer, &length ) ) {
    return NULL;
  }
  stream = FPStream_CreateBufferForInput( buffer, length );

  return Py_BuildValue( "L", stream );


} // create_buffer_istream


//
//  create_buffer_ostream
//
//  @param  pool reference
//  @param  file name
//
static PyObject *create_buffer_ostream( PyObject *self, PyObject *args ) {

  FPStreamRef   stream;
  char         *buffer;

  const unsigned long inBuffLen = 0;

  if( !PyArg_ParseTuple( args, "LL", &buffer, &inBuffLen ) ) {
    return NULL;
  }

  stream = FPStream_CreateBufferForOutput( buffer, inBuffLen );

  return Py_BuildValue( "L", stream );


} // create_buffer_ostream


//
//  close_stream
//
//  @param  pool reference
//  @param  file name
//
static PyObject *close_stream( PyObject *self, PyObject *args ) {

  FPStreamRef   stream;

  if( !PyArg_ParseTuple( args, "L", &stream ) ) {
    return NULL;
  }

  FPStream_Close(stream);

  return Py_BuildValue( "b", true );


} // close_stream



/////////////////////////////////////////////////////////////////////
// Query Functions
/////////////////////////////////////////////////////////////////////


//
//  query_expression_close
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_expression_close( PyObject *self, PyObject *args ) {

  const FPQueryExpressionRef			query;

  if( !PyArg_ParseTuple( args, "L", &query ) ) {
    return NULL;
  }

  FPQueryExpression_Close( query );

  return Py_BuildValue( "b", true );


} // query_expression_close


//
//  query_expression_create
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_expression_create( PyObject *self, PyObject *args ) {

  FPQueryExpressionRef			query;

  query = FPQueryExpression_Create();

  return Py_BuildValue( "L", query );


} // query_expression_create


//
//  query_expression_deselect_field
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_expression_deselect_field( PyObject *self, PyObject *args ) {

  const FPQueryExpressionRef			query;
  const	char						   *name;

  if( !PyArg_ParseTuple( args, "Ls", &query, &name ) ) {
    return NULL;
  }

  FPQueryExpression_DeselectField( query, name );

  return Py_BuildValue( "b", true );


} // query_expression_deselect_field


//
//  query_expression_get_end_time
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_expression_get_end_time( PyObject *self, PyObject *args ) {

  const FPQueryExpressionRef			query;
  FPLong								time;

  if( !PyArg_ParseTuple( args, "L", &query ) ) {
    return NULL;
  }

  time = FPQueryExpression_GetEndTime( query );

  return Py_BuildValue( "L", time );


} // query_expression_get_end_time


//
//  query_expression_get_start_time
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_expression_get_start_time( PyObject *self, PyObject *args ) {

  const FPQueryExpressionRef			query;
  FPLong								time;

  if( !PyArg_ParseTuple( args, "L", &query ) ) {
    return NULL;
  }

  time = FPQueryExpression_GetStartTime( query );

  return Py_BuildValue( "L", time );


} // query_expression_get_start_time


//
//  query_expression_get_type
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_expression_get_type( PyObject *self, PyObject *args ) {

  const FPQueryExpressionRef			query;
  FPInt									type;

  if( !PyArg_ParseTuple( args, "L", &query ) ) {
    return NULL;
  }

  type = FPQueryExpression_GetType( query );

  return Py_BuildValue( "i", time );


} // query_expression_get_type


//
//  query_expression_is_field_selected
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_expression_is_field_selected( PyObject *self, PyObject *args ) {

  const FPQueryExpressionRef			query;
  const char						   *name;
  FPBool								value;

  if( !PyArg_ParseTuple( args, "Ls", &query, &name ) ) {
    return NULL;
  }

  value = FPQueryExpression_IsFieldSelected( query, name );

  return Py_BuildValue( "b", value );


} // query_expression_is_field_selected


//
//  query_expression_select_field
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_expression_select_field( PyObject *self, PyObject *args ) {

  const FPQueryExpressionRef			query;
  const char						   *name;

  if( !PyArg_ParseTuple( args, "Ls", &query, &name ) ) {
    return NULL;
  }

  FPQueryExpression_SelectField( query, name );

  return Py_BuildValue( "b", true );


} // query_expression_select_field


//
//  query_expression_set_end_time
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_expression_set_end_time( PyObject *self, PyObject *args ) {

  const FPQueryExpressionRef			query;
  const FPLong							time;

  if( !PyArg_ParseTuple( args, "LL", &query, &time ) ) {
    return NULL;
  }

  FPQueryExpression_SetEndTime( query, time );

  return Py_BuildValue( "b", true );


} // query_expression_set_end_time


//
//  query_expression_set_start_time
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_expression_set_start_time( PyObject *self, PyObject *args ) {

  const FPQueryExpressionRef			query;
  const FPLong							time;

  if( !PyArg_ParseTuple( args, "LL", &query, &time ) ) {
    return NULL;
  }

  FPQueryExpression_SetStartTime( query, time );

  return Py_BuildValue( "b", true );


} // query_expression_set_start_time


//
//  query_expression_set_type
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_expression_set_type( PyObject *self, PyObject *args ) {

  const FPQueryExpressionRef			query;
  const FPInt							type;

  if( !PyArg_ParseTuple( args, "Li", &query, &type ) ) {
    return NULL;
  }

  FPQueryExpression_SetType( query, type );

  return Py_BuildValue( "b", true );


} // query_expression_set_type


//
//  pool_query_close
//
//  @param  pool reference
//  @param  file name
//
static PyObject *pool_query_close( PyObject *self, PyObject *args ) {

  const FPPoolQueryRef					query;

  if( !PyArg_ParseTuple( args, "L", &query ) ) {
    return NULL;
  }

  FPPoolQuery_Close( query );

  return Py_BuildValue( "b", true );


} // pool_query_close


//
//  pool_query_fetch_result
//
//  @param  pool reference
//  @param  file name
//
static PyObject *pool_query_fetch_result( PyObject *self, PyObject *args ) {

  const FPPoolQueryRef					query;
  const FPInt							timeout;
  FPPoolQueryRef						result;

  if( !PyArg_ParseTuple( args, "Li", &query, &timeout ) ) {
    return NULL;
  }

  result = FPPoolQuery_FetchResult( query, timeout );

  return Py_BuildValue( "L", result );


} // pool_query_fetch_result


//
//  pool_query_get_pool_ref
//
//  @param  pool reference
//  @param  file name
//
static PyObject *pool_query_get_pool_ref( PyObject *self, PyObject *args ) {

	const FPPoolQueryRef					query;
	FPPoolRef								pool;

	if( !PyArg_ParseTuple( args, "L", &query ) ) {
	  return NULL;
  	}

	pool = FPPoolQuery_GetPoolRef( query );

	return Py_BuildValue( "L", pool );


} // pool_query_get_pool_ref


//
//  pool_query_open
//
//  @param  pool reference
//  @param  file name
//
static PyObject *pool_query_open( PyObject *self, PyObject *args ) {

  const FPPoolRef				pool;
  FPQueryExpressionRef			expression;
  FPPoolQueryRef				query;

  if( !PyArg_ParseTuple( args, "LL", &pool, &expression ) ) {
    return NULL;
  }

  query = FPPoolQuery_Open( pool, expression );

  return Py_BuildValue( "L", query );


} // pool_query_open


//
//  query_result_close
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_result_close( PyObject *self, PyObject *args ) {

  FPQueryResultRef			result;

  if( !PyArg_ParseTuple( args, "L", &result ) ) {
    return NULL;
  }

  FPQueryResult_Close( result );

  return Py_BuildValue( "b", true );


} // query_result_close


//
//  query_result_get_clip_id
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_result_get_clip_id( PyObject *self, PyObject *args ) {

  const FPQueryResultRef					result;
  FPClipID									clipid;

  if( !PyArg_ParseTuple( args, "L", &result ) ) {
    return NULL;
  }

  FPQueryResult_GetClipID( result, clipid );

  return Py_BuildValue( "s", clipid );


} // query_result_get_clip_id


//
//  query_result_get_field
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_result_get_field( PyObject *self, PyObject *args ) {

  const FPQueryResultRef   			result;
  const char					   *name;
  char					        field[MAX_ATTRIBUTE_LEN];
  FPInt					        length;

  if( !PyArg_ParseTuple( args, "Ls", &result, &name ) ) {
    return NULL;
  }

  FPQueryResult_GetField( result, name, field, &length );

  return Py_BuildValue( "s", field );


} // query_result_get_field


//
//  query_result_get_result_code
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_result_get_result_code( PyObject *self, PyObject *args ) {

  const FPQueryResultRef			result;
  FPInt								code;

  if( !PyArg_ParseTuple( args, "L", &result ) ) {
    return NULL;
  }

  code = FPQueryResult_GetResultCode( result );

  return Py_BuildValue( "i", code );


} // query_result_get_result_code


//
//  query_result_get_timestamp
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_result_get_timestamp( PyObject *self, PyObject *args ) {

  const	FPQueryResultRef		result;
  FPLong						timestamp;

  if( !PyArg_ParseTuple( args, "L", &result ) ) {
    return NULL;
  }

  timestamp = FPQueryResult_GetTimestamp( result );

  return Py_BuildValue( "L", timestamp );


} // query_result_get_timestamp


//
//  query_result_get_type
//
//  @param  pool reference
//  @param  file name
//
static PyObject *query_result_get_type( PyObject *self, PyObject *args ) {

  const FPQueryResultRef				result;
  FPInt									type;

  if( !PyArg_ParseTuple( args, "L", &result ) ) {
    return NULL;
  }

  type = FPQueryResult_GetType( result );

  return Py_BuildValue( "i", type );


} // query_result_get_type


/////////////////////////////////////////////////////////////////////
// Monitor Functions
/////////////////////////////////////////////////////////////////////

//
//  event_callback_close
//
//  @param  pool reference
//  @param  file name
//
static PyObject *event_callback_close( PyObject *self, PyObject *args ) {

  FPEventCallbackRef			event;


  if( !PyArg_ParseTuple( args, "L", &event ) ) {
    return NULL;
  }

  FPEventCallback_Close( event );

  return Py_BuildValue( "b", true );


} // event_callback_close


//
//  event_callback_register_for_all_events
//
//  @param  pool reference
//  @param  file name
//
static PyObject *event_callback_register_for_all_events( PyObject *self, PyObject *args ) {

  FPEventCallbackRef			event;
  FPMonitorRef					monitor;
  FPStreamRef					stream;


  if( !PyArg_ParseTuple( args, "LL", &monitor, &stream ) ) {
    return NULL;
  }

  event = FPEventCallback_RegisterForAllEvents( monitor, stream );

  return Py_BuildValue( "L", event );


} // event_callback_register_for_all_events


//
//  monitor_close
//
//  @param  pool reference
//  @param  file name
//
static PyObject *monitor_close( PyObject *self, PyObject *args ) {

  FPMonitorRef				monitor;

  if( !PyArg_ParseTuple( args, "L", &monitor ) ) {
    return NULL;
  }

  FPMonitor_Close( monitor );

  return Py_BuildValue( "b", true );


} // monitor_close


//
//  monitor_get_all_statistics
//
//  @param  pool reference
//  @param  file name
//
static PyObject *monitor_get_all_statistics( PyObject *self, PyObject *args ) {

  const FPMonitorRef			monitor;
  char				        *buffer;
  FPInt					length = MAX_BUF_SIZE;
  FPInt                                 bsize  = length;
  FPInt					owaru  = 0;
  PyObject *ret;

  if( !PyArg_ParseTuple( args, "L", &monitor ) ) {
    return NULL;
  }

  while( !owaru ) {

    buffer = (char *) malloc( bsize );

    if( buffer == NULL ) {
      return NULL;
    }

    FPMonitor_GetAllStatistics( monitor, buffer, &length );
    
    if( length >= bsize ) {
      bsize = length;
      free(buffer);
    }
    else {
      owaru = 1;
    }
  }

  ret = PyString_FromStringAndSize( buffer, length );
  free(buffer);

  return ret;


} // monitor_get_all_statistics


//
//  monitor_get_all_statistics_stream
//
//  @param  pool reference
//  @param  file name
//
static PyObject *monitor_get_all_statistics_stream( PyObject *self, PyObject *args ) {

  const FPMonitorRef			monitor;
  FPStreamRef					stream;

  if( !PyArg_ParseTuple( args, "LL", &monitor, &stream ) ) {
    return NULL;
  }

  FPMonitor_GetAllStatisticsStream( monitor, stream );

  return Py_BuildValue( "b", true );


} // monitor_get_all_statistics_stream


//
//  monitor_get_discovery
//
//  @param  pool reference
//  @param  file name
//
static PyObject *monitor_get_discovery( PyObject *self, PyObject *args ) {

  const FPMonitorRef			monitor;
  char				        *buffer;
  FPInt					length = MAX_BUF_SIZE;
  FPInt                                 bsize  = length;
  FPInt					owaru  = 0;
  PyObject *ret;

  if( !PyArg_ParseTuple( args, "L", &monitor ) ) {
    return NULL;
  }


  while( !owaru ) {

    buffer = (char *) malloc( bsize );

    if( buffer == NULL ) {
      return NULL;
    }

    FPMonitor_GetDiscovery( monitor, buffer, &length );
    
    if( length >= bsize ) {
      bsize = length;
      free(buffer);
    }
    else {
      owaru = 1;
    }
  }

  ret = PyString_FromStringAndSize( buffer, length );
  free(buffer);

  return ret;

} // monitor_get_discovery


//
//  monitor_get_discovery_stream
//
//  @param  pool reference
//  @param  file name
//
static PyObject *monitor_get_discovery_stream( PyObject *self, PyObject *args ) {

  const FPMonitorRef			monitor;
  FPStreamRef					stream;

  if( !PyArg_ParseTuple( args, "LL", &monitor, &stream ) ) {
    return NULL;
  }

  FPMonitor_GetDiscoveryStream( monitor, stream );

  return Py_BuildValue( "b", true );


} // monitor_get_discovery_stream


//
//  monitor_open
//
//  @param  pool reference
//  @param  file name
//
static PyObject *monitor_open( PyObject *self, PyObject *args ) {

  FPMonitorRef   		monitor;
  const char		   *address;

  if( !PyArg_ParseTuple( args, "s", &address ) ) {
    return NULL;
  }

  monitor = FPMonitor_Open( address );

  return Py_BuildValue( "L", monitor );


} // monitor_open


/////////////////////////////////////////////////////////////////////
// Retention Class Functions
/////////////////////////////////////////////////////////////////////


//
//  retention_class_close
//
//  @param  pool reference
//  @param  file name
//
static PyObject *retention_class_close( PyObject *self, PyObject *args ) {

  FPRetentionClassRef   retention_class;

  if( !PyArg_ParseTuple( args, "L", &retention_class ) ) {
    return NULL;
  }

  FPRetentionClass_Close( retention_class );

  return Py_BuildValue( "b", true );


} // retention_class_close


//
//  retention_class_context_close
//
//  @param  pool reference
//  @param  file name
//
static PyObject *retention_class_context_close( PyObject *self, PyObject *args ) {

  FPRetentionClassContextRef		context;

  if( !PyArg_ParseTuple( args, "L", &context ) ) {
    return NULL;
  }

  FPRetentionClassContext_Close( context );

  return Py_BuildValue( "b", true );


} // retention_class_context_close


//
//  retention_class_context_get_first_class
//
//  @param  pool reference
//  @param  file name
//
static PyObject *retention_class_context_get_first_class( PyObject *self, PyObject *args ) {

  FPRetentionClassContextRef		context;
  FPRetentionClassRef				retention_class;

  if( !PyArg_ParseTuple( args, "L", &context ) ) {
    return NULL;
  }

  retention_class = FPRetentionClassContext_GetFirstClass( context );

  return Py_BuildValue( "L", retention_class );


} // retention_class_context_get_first_class


//
//  retention_class_context_get_last_class
//
//  @param  pool reference
//  @param  file name
//
static PyObject *retention_class_context_get_last_class( PyObject *self, PyObject *args ) {

  FPRetentionClassContextRef		context;
  FPRetentionClassRef				retention_class;

  if( !PyArg_ParseTuple( args, "L", &context ) ) {
    return NULL;
  }

  retention_class = FPRetentionClassContext_GetLastClass( context );

  return Py_BuildValue( "L", retention_class );


} // retention_class_context_get_last_class


//
//  retention_class_context_get_named_class
//
//  @param  pool reference
//  @param  file name
//
static PyObject *retention_class_context_get_named_class( PyObject *self, PyObject *args ) {

  FPRetentionClassContextRef			context;
  const char 						   *name;
  FPRetentionClassRef					retention_class;

  if( !PyArg_ParseTuple( args, "Ls", &context, &name ) ) {
    return NULL;
  }

  retention_class = FPRetentionClassContext_GetNamedClass( context, name );

  return Py_BuildValue( "L", retention_class );


} // retention_class_context_get_named_class


//
//  retention_class_context_get_next_class
//
//  @param  pool reference
//  @param  file name
//
static PyObject *retention_class_context_get_next_class( PyObject *self, PyObject *args ) {

  FPRetentionClassContextRef		context;
  FPRetentionClassRef				retention_class;

  if( !PyArg_ParseTuple( args, "L", &context ) ) {
    return NULL;
  }

  retention_class = FPRetentionClassContext_GetNextClass( context );

  return Py_BuildValue( "L", retention_class );


} // retention_class_context_get_next_class


//
//  retention_class_context_get_num_classes
//
//  @param  pool reference
//  @param  file name
//
static PyObject *retention_class_context_get_num_classes( PyObject *self, PyObject *args ) {

  FPRetentionClassContextRef		context;
  FPInt								total;

  if( !PyArg_ParseTuple( args, "L", &context ) ) {
    return NULL;
  }

  total = FPRetentionClassContext_GetNumClasses( context );

  return Py_BuildValue( "i", total );


} // retention_class_context_get_num_classes


//
//  retention_class_context_get_previous_class
//
//  @param  pool reference
//  @param  file name
//
static PyObject *retention_class_context_get_previous_class( PyObject *self, PyObject *args ) {

  FPRetentionClassContextRef		context;
  FPRetentionClassRef				retention_class;

  if( !PyArg_ParseTuple( args, "L", &context ) ) {
    return NULL;
  }

  retention_class = FPRetentionClassContext_GetPreviousClass( context );

  return Py_BuildValue( "L", retention_class );


} // retention_class_context_get_previous_class


//
//  retention_class_get_name
//
//  @param  pool reference
//  @param  file name
//
static PyObject *retention_class_get_name( PyObject *self, PyObject *args ) {

  FPRetentionClassRef			retention_class;
  char				        name[MAX_NAME_LEN];
  FPInt					length = MAX_NAME_LEN;

  if( !PyArg_ParseTuple( args, "L", &retention_class ) ) {
    return NULL;
  }

  FPRetentionClass_GetName( retention_class, name, &length );

  return Py_BuildValue( "s", name );


} // retention_class_get_name


//
//  retention_class_get_period
//
//  @param  pool reference
//  @param  file name
//
static PyObject *retention_class_get_period( PyObject *self, PyObject *args ) {

  FPRetentionClassRef			retention_class;
  FPLong						period;

  if( !PyArg_ParseTuple( args, "L", &retention_class ) ) {
    return NULL;
  }

  period = FPRetentionClass_GetPeriod( retention_class );

  return Py_BuildValue( "L", period );


} // retention_class_get_period


/////////////////////////////////////////////////////////////////////
// Time Class Functions
/////////////////////////////////////////////////////////////////////

//
//  time_milliseconds_to_string
//
//  @param  pool reference
//  @param  file name
//
static PyObject *time_milliseconds_to_string( PyObject *self, PyObject *args ) {

  FPLong				time;
  char				        time_str[MAX_NAME_LEN];
  int				        length;
  int					options;

  if( !PyArg_ParseTuple( args, "Li", &time, &options ) ) {
    return NULL;
  }

  FPTime_MillisecondsToString( time, time_str, &length, options );

  return Py_BuildValue( "s", time_str );


} // time_milliseconds_to_string


//
//  time_seconds_to_string
//
//  @param  pool reference
//  @param  file name
//
static PyObject *time_seconds_to_string( PyObject *self, PyObject *args ) {

  const FPLong				time;
  char				   	time_str[MAX_NAME_LEN];
  int				        length;
  int					options;

  if( !PyArg_ParseTuple( args, "Li", &time, &options ) ) {
    return NULL;
  }

  FPTime_MillisecondsToString( time, time_str, &length, options );

  return Py_BuildValue( "s", time_str );


} // time_seconds_to_string


//
//  time_string_to_milliseconds
//
//  @param  pool reference
//  @param  file name
//
static PyObject *time_string_to_milliseconds( PyObject *self, PyObject *args ) {

  FPLong				mseconds;
  const char		   *time_str;

  if( !PyArg_ParseTuple( args, "s", &time_str ) ) {
    return NULL;
  }

  mseconds = FPTime_StringToMilliseconds( time_str );

  return Py_BuildValue( "L", mseconds );


} // time_string_to_milliseconds


//
//  time_string_to_seconds
//
//  @param  pool reference
//  @param  file name
//
static PyObject *time_string_to_seconds( PyObject *self, PyObject *args ) {

  FPLong				seconds;
  const char		   *time_str;

  if( !PyArg_ParseTuple( args, "s", &time_str ) ) {
    return NULL;
  }

  seconds = FPTime_StringToSeconds( time_str );

  return Py_BuildValue( "L", seconds );


} // time_string_to_seconds


static PyMethodDef CenteraMethods[] = {

  { "pool_open", pool_open, METH_VARARGS, "" },
  { "pool_close", pool_close, METH_VARARGS, "" },
  { "get_component_version", get_component_version, METH_VARARGS, "" },
  { "set_global_option", set_global_option, METH_VARARGS, "" },
  { "set_int_option", set_int_option, METH_VARARGS, "" },
  { "get_cluster_time", get_cluster_time, METH_VARARGS, "" },
  { "get_capability", get_capability, METH_VARARGS, "" },
  { "get_clip_id", get_clip_id, METH_VARARGS, "" },
  { "get_global_option", get_global_option, METH_VARARGS, "" },
  { "get_int_option", get_int_option, METH_VARARGS, "" },
  { "get_pool_info", get_pool_info, METH_VARARGS, "" },
  { "get_retention_class_context", get_retention_class_context, METH_VARARGS, "" },
  { "register_application", register_application, METH_VARARGS, "" },
  { "set_clip_id", set_clip_id, METH_VARARGS, "" },
  { "get_last_error", get_last_error, METH_VARARGS, "" },
  { "get_last_error_info", get_last_error_info, METH_VARARGS, "" },
  { "clip_create", clip_create, METH_VARARGS, "" },
  { "clip_write", clip_write, METH_VARARGS, "" },
  { "clip_open", clip_open, METH_VARARGS, "" },
  { "clip_close", clip_close, METH_VARARGS, "" },
  { "get_top_tag", get_top_tag, METH_VARARGS, "" },
  { "clip_audited_delete", clip_audited_delete, METH_VARARGS, "" },
  { "clip_delete", clip_delete, METH_VARARGS, "" },
  { "clip_enable_ebr_with_class", clip_enable_ebr_with_class, METH_VARARGS, "" },
  { "clip_enable_ebr_with_period", clip_enable_ebr_with_period, METH_VARARGS, "" },
  { "clip_raw_open", clip_raw_open, METH_VARARGS, "" },
  { "clip_raw_read", clip_raw_read, METH_VARARGS, "" },
  { "clip_remove_retention_class", clip_remove_retention_class, METH_VARARGS, "" },
  { "clip_set_name", clip_set_name, METH_VARARGS, "" },
  { "clip_set_retention_class", clip_set_retention_class, METH_VARARGS, "" },
  { "clip_set_retention_hold", clip_set_retention_hold, METH_VARARGS, "" },
  { "clip_set_retention_period", clip_set_retention_period, METH_VARARGS, "" },
  { "clip_trigger_ebr_event", clip_trigger_ebr_event, METH_VARARGS, "" },
  { "clip_trigger_ebr_event_with_class", clip_trigger_ebr_event_with_class, METH_VARARGS, "" },
  { "clip_trigger_ebr_event_with_period", clip_trigger_ebr_event_with_period, METH_VARARGS, "" },
  { "clip_get_canonical_format", clip_get_canonical_format, METH_VARARGS, "" },
  { "clip_get_string_format", clip_get_string_format, METH_VARARGS, "" },
  { "clip_exists", clip_exists, METH_VARARGS, "" },
  { "clip_get_clip_id", clip_get_clip_id, METH_VARARGS, "" },
  { "clip_get_creation_date", clip_get_creation_date, METH_VARARGS, "" },
  { "clip_get_ebr_class_name", clip_get_ebr_class_name, METH_VARARGS, "" },
  { "clip_get_ebr_event_time", clip_get_ebr_event_time, METH_VARARGS, "" },
  { "clip_get_ebr_period", clip_get_ebr_period, METH_VARARGS, "" },
  { "clip_get_name", clip_get_name, METH_VARARGS, "" },
  { "clip_get_num_blobs", clip_get_num_blobs, METH_VARARGS, "" },
  { "clip_get_num_tags", clip_get_num_tags, METH_VARARGS, "" },
  { "clip_get_pool_ref", clip_get_pool_ref, METH_VARARGS, "" },
  { "clip_get_retention_class_name", clip_get_retention_class_name, METH_VARARGS, "" },
  { "clip_get_retention_hold", clip_get_retention_hold, METH_VARARGS, "" },
  { "clip_get_retention_period", clip_get_retention_period, METH_VARARGS, "" },
  { "clip_get_total_size", clip_get_total_size, METH_VARARGS, "" },
  { "clip_is_ebr_enabled", clip_is_ebr_enabled, METH_VARARGS, "" },
  { "clip_is_modified", clip_is_modified, METH_VARARGS, "" },
  { "clip_validate_retention_class", clip_validate_retention_class, METH_VARARGS, "" },
  { "clip_get_description_attribute", clip_get_description_attribute, METH_VARARGS, "" },
  { "clip_get_description_attribute_index", clip_get_description_attribute_index, METH_VARARGS, "" },
  { "clip_get_num_description_attributes", clip_get_num_description_attributes, METH_VARARGS, "" },
  { "clip_remove_description_attribute", clip_remove_description_attribute, METH_VARARGS, "" },
  { "clip_set_description_attribute", clip_set_description_attribute, METH_VARARGS, "" },
  { "clip_fetch_next", clip_fetch_next, METH_VARARGS, "" },
  { "tag_create", tag_create, METH_VARARGS, "" },
  { "tag_close", tag_close, METH_VARARGS, "" },
  { "tag_copy", tag_copy, METH_VARARGS, "" },
  { "tag_delete", tag_delete, METH_VARARGS, "" },
  { "tag_get_blob_size", tag_get_blob_size, METH_VARARGS, "" },
  { "tag_get_clip_ref", tag_get_clip_ref, METH_VARARGS, "" },
  { "tag_get_pool_ref", tag_get_pool_ref, METH_VARARGS, "" },
  { "tag_get_tag_name", tag_get_tag_name, METH_VARARGS, "" },
  { "tag_get_first_child", tag_get_first_child, METH_VARARGS, "" },
  { "tag_get_parent", tag_get_parent, METH_VARARGS, "" },
  { "tag_get_prev_sibling", tag_get_prev_sibling, METH_VARARGS, "" },
  { "tag_get_sibling", tag_get_sibling, METH_VARARGS, "" },
  { "tag_get_bool_attribute", tag_get_bool_attribute, METH_VARARGS, "" },
  { "tag_get_index_attribute", tag_get_index_attribute, METH_VARARGS, "" },
  { "tag_get_long_attribute", tag_get_long_attribute, METH_VARARGS, "" },
  { "tag_get_num_attribute", tag_get_num_attribute, METH_VARARGS, "" },
  { "tag_get_string_attribute", tag_get_string_attribute, METH_VARARGS, "" },
  { "tag_remove_attribute", tag_remove_attribute, METH_VARARGS, "" },
  { "tag_set_bool_attribute", tag_set_bool_attribute, METH_VARARGS, "" },
  { "tag_set_long_attribute", tag_set_long_attribute, METH_VARARGS, "" },
  { "tag_set_string_attribute", tag_set_string_attribute, METH_VARARGS, "" },
  { "blob_write", blob_write, METH_VARARGS, "" },
  { "blob_write_partial", blob_write_partial, METH_VARARGS, "" },
  { "blob_exists", blob_exists, METH_VARARGS, "" },
  { "blob_read", blob_read, METH_VARARGS, "" },
  { "blob_read_partial", blob_read_partial, METH_VARARGS, "" },
  { "create_file_istream", create_file_istream, METH_VARARGS, "" },
  { "create_file_ostream", create_file_ostream, METH_VARARGS, "" },
  { "create_buffer_istream", create_buffer_istream, METH_VARARGS, "" },
  { "create_buffer_ostream", create_buffer_ostream, METH_VARARGS, "" },
  { "close_stream", close_stream, METH_VARARGS, "" },
  { "query_expression_close", query_expression_close, METH_VARARGS, "" },
  { "query_expression_create", query_expression_create, METH_VARARGS, "" },
  { "query_expression_deselect_field", query_expression_deselect_field, METH_VARARGS, "" },
  { "query_expression_get_end_time", query_expression_get_end_time, METH_VARARGS, "" },
  { "query_expression_get_start_time", query_expression_get_start_time, METH_VARARGS, "" },
  { "query_expression_get_type", query_expression_get_type, METH_VARARGS, "" },
  { "query_expression_is_field_selected", query_expression_is_field_selected, METH_VARARGS, "" },
  { "query_expression_select_field", query_expression_select_field, METH_VARARGS, "" },
  { "query_expression_set_end_time", query_expression_set_end_time, METH_VARARGS, "" },
  { "query_expression_set_start_time", query_expression_set_start_time, METH_VARARGS, "" },
  { "query_expression_set_type", query_expression_set_type, METH_VARARGS, "" },
  { "pool_query_close", pool_query_close, METH_VARARGS, "" },
  { "pool_query_fetch_result", pool_query_fetch_result, METH_VARARGS, "" },
  { "pool_query_get_pool_ref", pool_query_get_pool_ref, METH_VARARGS, "" },
  { "pool_query_open", pool_query_open, METH_VARARGS, "" },
  { "query_result_close", query_result_close, METH_VARARGS, "" },
  { "query_result_get_clip_id", query_result_get_clip_id, METH_VARARGS, "" },
  { "query_result_get_field", query_result_get_field, METH_VARARGS, "" },
  { "query_result_get_result_code", query_result_get_result_code, METH_VARARGS, "" },
  { "query_result_get_timestamp", query_result_get_timestamp, METH_VARARGS, "" },
  { "query_result_get_type", query_result_get_type, METH_VARARGS, "" },
  { "event_callback_close", event_callback_close, METH_VARARGS, "" },
  { "event_callback_register_for_all_events", event_callback_register_for_all_events, METH_VARARGS, "" },
  { "monitor_close", monitor_close, METH_VARARGS, "" },
  { "monitor_get_all_statistics", monitor_get_all_statistics, METH_VARARGS, "" },
  { "monitor_get_all_statistics_stream", monitor_get_all_statistics_stream, METH_VARARGS, "" },
  { "monitor_get_discovery", monitor_get_discovery, METH_VARARGS, "" },
  { "monitor_get_discovery_stream", monitor_get_discovery_stream, METH_VARARGS, "" },
  { "monitor_open", monitor_open, METH_VARARGS, "" },
  { "retention_class_close", retention_class_close, METH_VARARGS, "" },
  { "retention_class_context_close", retention_class_context_close, METH_VARARGS, "" },
  { "retention_class_context_get_first_class", retention_class_context_get_first_class, METH_VARARGS, "" },
  { "retention_class_context_get_last_class", retention_class_context_get_last_class, METH_VARARGS, "" },
  { "retention_class_context_get_named_class", retention_class_context_get_named_class, METH_VARARGS, "" },
  { "retention_class_context_get_next_class", retention_class_context_get_next_class, METH_VARARGS, "" },
  { "retention_class_context_get_num_classes", retention_class_context_get_num_classes, METH_VARARGS, "" },
  { "retention_class_context_get_previous_class", retention_class_context_get_previous_class, METH_VARARGS, "" },
  { "retention_class_get_name", retention_class_get_name, METH_VARARGS, "" },
  { "retention_class_get_period", retention_class_get_period, METH_VARARGS, "" },
  { "time_milliseconds_to_string", time_milliseconds_to_string, METH_VARARGS, "" },
  { "time_seconds_to_string", time_seconds_to_string, METH_VARARGS, "" },
  { "time_string_to_milliseconds", time_string_to_milliseconds, METH_VARARGS, "" },
  { "time_string_to_seconds", time_string_to_seconds, METH_VARARGS, "" }

};


PyMODINIT_FUNC
initFPNative(void) {

  PyObject *m;

  m = Py_InitModule( "FPNative", CenteraMethods );

  //tmp = PyFloat_AsDouble(3);
  //PyDict_SetItemString( d, "pi", tmp );
  //Py_DECREF(tmp);

}
