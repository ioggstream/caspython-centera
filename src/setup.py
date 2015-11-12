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

import os
import platform
from distutils.core import setup, Extension


def get_bitsize():
    bitsize, bintype = platform.architecture()
    return bitsize[:2]

libraries = {
    '32': ['FPLibrary'],
    '64': ['FPLibrary64']
}
extra_compile_args = {
    '32': [],
    '64': ['-fPIC']
}

CASHOME = os.environ['CENTERA_HOME']
bitsize = get_bitsize()
native = Extension('FPNative',
                   sources=['native/pycentera.c'],
                   include_dirs=[CASHOME + '/include'],
                   libraries=libraries[bitsize],
                   library_dirs=[os.path.join(CASHOME, 'lib', bitsize)],
                   extra_compile_args=extra_compile_args[bitsize],
                   define_macros=[('POSIX', '1')])

setup(name='Filepool',
      version='1.2',
      author='Stephen Hu, Roberto Polli',
      author_email='hu_stephen@emc.com, roberto.polli@par-tec.it',
      description='This is a centera binding.',
      packages=["Filepool"],
      ext_modules=[native])
