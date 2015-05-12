#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2009-2015 Joao Carlos Roseta Matos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Setup for cx-Freeze."""

# Python 3 compatibility
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import glob
import io  # Python 3 compatibility
import os
import sys

# from builtins import input  # Python 3 compatibility
from cx_Freeze import setup, Executable

import appinfo


UTF_ENC = 'utf-8'

DESC = LONG_DESC = ''
if os.path.isfile(appinfo.README_FILE):
    with io.open(appinfo.README_FILE, encoding=UTF_ENC) as f_in:
        LONG_DESC = f_in.read()
        DESC = LONG_DESC.split('\n')[3]

PATH = appinfo.APP_NAME + '/'
SCRIPT = PATH + appinfo.APP_NAME + '.py'
TARGET_NAME = appinfo.APP_NAME + '.exe'

DATA_FILES = glob.glob(PATH + '*.txt')

if os.path.isdir(PATH + 'doc'):
    DATA_FILES += glob.glob(PATH + 'doc')

BASE = None
# GUI applications require a different base on Windows (the default is for a
# console application).
if sys.platform == 'win32':
    BASE = 'Win32GUI'

OPTIONS = dict(compressed=True,
               # excludes=['macpath', 'PyQt4'],
               # includes=['atexit', 'PySide.QtNetwork'],
               include_files=DATA_FILES,
               # append any extra module by extending the list below
               # - 'contributed_modules+["lxml"]'
               # packages=contributed_modules
               )

# add modules_dir to PYTHONPATH so all modules inside it are included
# in cx-Freeze library
sys.path.insert(1, appinfo.APP_NAME)

setup(name=appinfo.APP_NAME,
      version=appinfo.APP_VERSION,
      description=DESC,
      long_description=LONG_DESC,
      license=appinfo.APP_LICENSE,
      url=appinfo.APP_URL,
      author=appinfo.APP_AUTHOR,
      author_email=appinfo.APP_EMAIL,

      classifiers=appinfo.CLASSIFIERS,
      keywords=appinfo.APP_KEYWORDS,

      executables=[Executable(script=SCRIPT,
                              base=BASE,
                              compress=True,
                              # icon=appinfo.APP_NAME + '.ico',
                              targetName=TARGET_NAME,
                              # copyDependentFiles=True
                              )],

      options=dict(build_exe=OPTIONS),
      )
