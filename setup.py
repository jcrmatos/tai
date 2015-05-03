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

"""Setup for source, egg, wheel and wininst distributions."""

# Python 3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# import builtins  # Python 3 compatibility
# import future  # Python 3 compatibility
import io  # Python 3 compatibility
import os
import sys

import setuptools

import appinfo


SYS_ENC = sys.getfilesystemencoding()

DESC = LONG_DESC = ''
if os.path.isfile(appinfo.README_FILE):
    with io.open(appinfo.README_FILE, encoding=SYS_ENC) as file_:
        LONG_DESC = file_.read()
        DESC = LONG_DESC.split('\n')[3]

# PACKAGES = [appinfo.APP_NAME]  # use only if find_packages() doesn't work

REQUIREMENTS = ''
if os.path.isfile(appinfo.REQUIREMENTS_FILE):
    with io.open(appinfo.REQUIREMENTS_FILE, encoding=SYS_ENC) as file_:
        REQUIREMENTS = file_.read().splitlines()

ENTRY_POINTS = {'console_scripts': [appinfo.APP_NAME + '=' +
                                    appinfo.APP_NAME + '.' +
                                    appinfo.APP_NAME + ':main'],
                # 'gui_scripts' : ['app_gui=' + appinfo.APP_NAME + '.' +
                #                  appinfo.APP_NAME + ':start']
                }

setuptools.setup(name=appinfo.APP_NAME,
                 version=appinfo.APP_VERSION,
                 description=DESC,
                 long_description=LONG_DESC,
                 license=appinfo.APP_LICENSE,
                 url=appinfo.APP_URL,
                 author=appinfo.APP_AUTHOR,
                 author_email=appinfo.APP_EMAIL,

                 classifiers=appinfo.CLASSIFIERS,
                 keywords=appinfo.APP_KEYWORDS,

                 packages=setuptools.find_packages(),
                 # packages=setuptools.find_packages(exclude=['docs',
                 #                                            'tests*']),

                 # use only if find_packages() doesn't work
                 # packages=PACKAGES,
                 # package_dir={'': appinfo.APP_NAME},

                 # to create an executable
                 entry_points=ENTRY_POINTS,

                 install_requires=REQUIREMENTS,

                 # used only if the package is not in PyPI, but exists as an
                 # egg, sdist format or as a single .py file
                 # see http://peak.telecommunity.com/DevCenter/setuptools#dependencies-that-aren-t-in-pypi
                 # dependency_links = ['http://host.domain.local/dir/'],

                 include_package_data=True,  # use MANIFEST.in during install
                 )
