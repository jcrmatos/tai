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

"""Setup for py2exe."""

# Python 3 compatibility
from __future__ import (absolute_import, division, print_function,
                        )  # unicode_literals)
# the previous import is commented due to random Unicode errors

import glob
import io  # Python 3 compatibility
import os
import sys

# from builtins import input  # Python 3 compatibility
from setuptools import setup, find_packages
import py2exe  # must be after setuptools

import appinfo


UTF_ENC = 'utf-8'

DESC = LONG_DESC = ''
if os.path.isfile(appinfo.README_FILE):
    with io.open(appinfo.README_FILE, encoding=UTF_ENC) as f_in:
        LONG_DESC = f_in.read()
        DESC = LONG_DESC.split('\n')[3]

# PACKAGES = [appinfo.APP_NAME]  # use only if find_packages() doesn't work

REQUIREMENTS = ''
if os.path.isfile(appinfo.REQUIREMENTS_FILE):
    with io.open(appinfo.REQUIREMENTS_FILE, encoding=UTF_ENC) as f_in:
        REQUIREMENTS = f_in.read().splitlines()

PATH = appinfo.APP_NAME + '/'
SCRIPT = PATH + appinfo.APP_NAME + '.py'

DATA_FILES = [('', glob.glob(PATH + '*.txt'))]

if os.path.isdir(appinfo.APP_NAME + '/doc'):
    DATA_FILES += [('doc', glob.glob(PATH + 'doc/.*') +
                    glob.glob(PATH + 'doc/*.html') +
                    glob.glob(PATH + 'doc/*.pdf') +
                    glob.glob(PATH + 'doc/*.inv') +
                    glob.glob(PATH + 'doc/*.js')),
                   ('doc/_modules', glob.glob(PATH + 'doc/_modules/*.*')),
                   ('doc/_sources', glob.glob(PATH + 'doc/_sources/*.*')),
                   ('doc/_static', glob.glob(PATH + 'doc/_static/*.*'))]

OPTIONS = {'py2exe': {'compressed': True,
                      'ascii': False,
                      # 'packages': ['colorama'],
                      # 'bundle_files': 1,  # exe does not work
                      # 'includes': ['colorama'],
                      # 'excludes': ['doctest', 'pdb', 'unittest', 'difflib',
                      #              'inspect', 'pyreadline', 'optparse',
                      #              'calendar', 'email', '_ssl',
                      #              # 'locale', 'pickle'
                      #              ]
                      }
           }

# add modules_dir to PYTHONPATH so all modules inside it are included
# in py2exe library
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

      packages=find_packages(),
      # packages=setuptools.find_packages(exclude=['docs',
      #                                           'tests*']),

      # use only if find_packages() doesn't work
      # packages=PACKAGES,
      # package_dir={'': appinfo.APP_NAME},

      install_requires=REQUIREMENTS,

      console=[SCRIPT],
      options=OPTIONS,
      data_files=DATA_FILES,
      # windows=[{'script': appinfo.APP_NAME + '.py',
      #           'icon_resources': [(0, appinfo.APP_NAME + '.ico')]
      #          }],
      )
