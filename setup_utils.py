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

"""Setup utils library."""

# Python 3 compatibility
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime as dt
import glob
import io  # Python 3 compatibility
import os
# import pprint as pp
import sys
# import sysconfig
import time
import zipfile as zip

# from builtins import input  # Python 3 compatibility

import appinfo


UTF_ENC = 'utf-8'


def check_copyright():
    """Check copyright on files that have to be updated manually."""
    files = ['setup_utils.py', 'build.cmd', 'appinfo.py']
    update_required = 0
    for filename in files:
        if os.path.isfile(filename):
            with io.open(filename, encoding=UTF_ENC) as f_in:
                text = f_in.readlines()
            for line in text:
                if appinfo.COPYRIGHT in line:
                    break
                if 'Copyright 2009-' in line:
                    print('Copyright in ' + filename + ' is not updated.')
                    update_required += 1
                    break
    if update_required:
        sys.exit(1)


def update_copyright():
    """Update copyright on source and license files."""
    files = glob.glob('*.py')
    files = [file_ for file_ in files if file_ not in ['appinfo.py',
                                                       'setup_utils.py']]
    files += glob.glob(appinfo.APP_NAME + '/*.py')
    for filename in files:
        with io.open(filename, encoding=UTF_ENC) as f_in:
            text = f_in.readlines()
        new_text = ''
        changed = False
        for line in text:
            if ((not changed) and (appinfo.COPYRIGHT not in line) and
               ('Copyright 2009-' in line)):
                new_text += '# ' + appinfo.COPYRIGHT + '\n'
                changed = True
            else:
                new_text += line
        if changed:
            with io.open(filename, 'w', encoding=UTF_ENC) as f_out:
                f_out.writelines(new_text)

    filename = 'doc/conf.py'
    if os.path.isfile(filename):
        with io.open(filename, encoding=UTF_ENC) as f_in:
            text = f_in.readlines()
        new_text = ''
        changed = False
        doc_copyright = ("copyright = u'2009-" + str(dt.date.today().year) +
                         ', ' + appinfo.APP_AUTHOR + "'")
        for line in text:
            if ((not changed) and ("copyright = u'2009-" in line) and
               (doc_copyright not in line)):
                new_text += doc_copyright + '\n'
                changed = True
            else:
                new_text += line
        if changed:
            with io.open(filename, 'w', encoding=UTF_ENC) as f_out:
                f_out.writelines(new_text)

    filename = 'LICENSE.rst'
    with io.open(filename, encoding=UTF_ENC) as f_in:
        text = f_in.readlines()
    new_text = ''
    changed = False
    for line in text:
        if ((not changed) and (appinfo.COPYRIGHT not in line) and
           ('Copyright ' + '2009-' in line)):
            new_text += '        ' + appinfo.COPYRIGHT + '\n'
            changed = True
        else:
            new_text += line
    if changed:
        with io.open(filename, 'w', encoding=UTF_ENC) as f_out:
            f_out.writelines(new_text)


def sleep(seconds=5):
    """Pause for specified time."""
    time.sleep(seconds)


def app_name():
    """Write application name to text file."""
    with io.open('app_name.txt', 'w', encoding=UTF_ENC) as f_out:
        f_out.write(appinfo.APP_NAME, )


def app_ver():
    """Write application version to text file if equal to ChangeLog.rst."""
    with io.open('ChangeLog.rst', encoding=UTF_ENC) as f_in:
        changelog_app_ver = f_in.readline().split()[0]
    if changelog_app_ver == appinfo.APP_VERSION:
        with io.open('app_ver.txt', 'w', encoding=UTF_ENC) as f_out:
            f_out.write(appinfo.APP_VERSION)
    else:
        print('ChangeLog.rst and appinfo.py are not in sync.')


def app_type():
    """Write application type (application or module) to text file."""
    with io.open('app_type.txt', 'w', encoding=UTF_ENC) as f_out:
        f_out.write(appinfo.APP_TYPE)


def py_ver():
    """Write Python version to text file."""
    with io.open('py_ver.txt', 'w', encoding=UTF_ENC) as f_out:
        f_out.write(str(sys.version_info.major) + '.' +
                    str(sys.version_info.minor))


def remove_copyright():
    """Remove Copyright from README.rst."""
    with io.open('README.rst', encoding=UTF_ENC) as f_in:
        text = f_in.readlines()

    new_text = ''
    for line in text:
        if 'Copyright ' in line:
            pass
        else:
            new_text += line

    with io.open('README.rst', 'w', encoding=UTF_ENC) as f_out:
        f_out.writelines(new_text)


def prep_rst2pdf():
    """Remove parts of rST to create a better pdf."""
    with io.open('index.ori', encoding=UTF_ENC) as f_in:
        text = f_in.readlines()

    new_text = ''
    for line in text:
        if 'Indices and tables' in line:
            break
        else:
            new_text += line

    with io.open('index.rst', 'w', encoding=UTF_ENC) as f_out:
        f_out.writelines(new_text)

    with io.open('../README.rst', encoding=UTF_ENC) as f_in:
        text = f_in.readlines()

    new_text = ''
    for line in text:
        if '.. image:: ' in line or '    :target: ' in line:
            pass
        else:
            new_text += line

    with io.open('../README.rst', 'w', encoding=UTF_ENC) as f_out:
        f_out.writelines(new_text)


def create_doc_zip():
    """Create doc.zip to publish in PyPI."""
    doc_path = appinfo.APP_NAME + '/doc'
    with zip.ZipFile('pythonhosted.org/doc.zip', 'w') as archive:
        for root, dirs, files in os.walk(doc_path):
            for file_ in files:
                if '.pdf' not in file_:
                    pathname = os.path.join(root, file_)
                    filename = pathname.replace(doc_path + os.sep, '')
                    archive.write(pathname, filename)


def upd_usage_in_readme():
    """Update usage in README.rst."""
    if os.path.isfile(appinfo.APP_NAME + '/usage.txt'):
        with io.open(appinfo.APP_NAME + '/usage.txt',
                     encoding=UTF_ENC) as f_in:
            usage_text = f_in.read()
            usage_text = usage_text[len(os.linesep) - 1:]  # remove 1st line

        with io.open('README.rst', encoding=UTF_ENC) as f_in:
            text = f_in.readlines()

        new_text = ''
        usage_section = False
        changed = False
        for line in text:
            if 'usage: ' in line:  # usage section start
                usage_section = True
                new_text += usage_text + '\n'
                changed = True
            elif usage_section and 'Resources' not in line:
                # bypass old usage section
                continue
            elif usage_section and 'Resources' in line:  # usage section end
                usage_section = False
                new_text += line
            else:
                new_text += line

        if changed:
            with io.open('README.rst', 'w', encoding=UTF_ENC) as f_out:
                f_out.writelines(new_text)


def change_sphinx_theme():
    """"Change Sphinx theme according to Sphinx version."""
    try:
        import sphinx
        sphinx_ver_str = sphinx.__version__
        sphinx_ver = int(sphinx_ver_str.replace('.', ''))

        with io.open('doc/conf.py', encoding=UTF_ENC) as f_in:
            text = f_in.readlines()

        new_text = ''
        changed = False
        for line in text:
            if "html_theme = 'default'" in line and sphinx_ver >= 131:
                new_text += "html_theme = 'alabaster'\n"
                changed = True
            elif "html_theme = 'alabaster'" in line and sphinx_ver < 131:
                new_text += "html_theme = 'default'\n"
                changed = True
            else:
                new_text += line

        if changed:
            with io.open('doc/conf.py', 'w', encoding=UTF_ENC) as f_out:
                f_out.write(new_text)
    except ImportError:  # as error:
        pass


def comment_import_for_py2exe(filename):
    """Comment unicode_literals import in filename for py2exe build."""
    with io.open(filename, encoding=UTF_ENC) as f_in:
        text = f_in.readlines()

    new_text = ''
    for line in text:
        if '                        unicode_literals)' in line:
            new_text += '                        )  # unicode_literals)\n'
        else:
            new_text += line

    with io.open(filename, 'w', encoding=UTF_ENC) as f_out:
        f_out.writelines(new_text)


def uncomment_import_for_py2exe(filename):
    """Uncomment unicode_literals import in filename for other builds."""
    with io.open(filename, encoding=UTF_ENC) as f_in:
        text = f_in.readlines()

    new_text = ''
    for line in text:
        if '                        )  # unicode_literals)' in line:
            new_text += '                        unicode_literals)\n'
        else:
            new_text += line

    with io.open(filename, 'w', encoding=UTF_ENC) as f_out:
        f_out.writelines(new_text)


def collect_to_do():
    """Collect To do from all py files."""
    files = glob.glob(appinfo.APP_NAME + '/*.py')
    to_do_lst = []
    for filename in files:
        with io.open(filename, encoding=UTF_ENC) as f_in:
            text = f_in.readlines()
        for line in text:
            if '# ToDo: ' in line:
                to_do_lst.append(filename.split(os.sep)[-1] + ': ' +
                                 line.replace('# ToDo: ', '').lstrip())

    to_do_text = ''
    for item in to_do_lst:
        to_do_text += item

    with io.open('README.rst', encoding=UTF_ENC) as f_in:
        text = f_in.readlines()

    new_text = ''
    to_do_section = False
    changed = False
    for line in text:
        if '**To do**' in line:  # to do section start
            to_do_section = True
            new_text += '**To do**\n\n' + to_do_text + '\n'
            changed = True
        elif to_do_section and 'Installation' not in line:
            # bypass old to do section
            continue
        elif to_do_section and 'Installation' in line:  # to do section end
            to_do_section = False
            new_text += line
        else:
            new_text += line

    if changed:
        with io.open('README.rst', 'w', encoding=UTF_ENC) as f_out:
            f_out.writelines(new_text)


# def std_lib_modules():
#     """List all (not complete) Standard library modules."""
#     std_lib_dir = sysconfig.get_config_vars('LIBDEST')[0]
#     modules_lst = []
#     for top, dirs, files in os.walk(std_lib_dir):
#         for nm in files:
#             if nm != '__init__.py' and nm[-3:] == '.py':
#                 module = os.path.join(top, nm)[len(std_lib_dir)+1:-3].replace('\\','.')
#                 if 'site-packages.' not in module:
#                     modules_lst.append(os.path.join(top, nm)[len(std_lib_dir)+1:-3].replace('\\','.'))
#     pp.pprint(modules_lst)


# def non_std_lib_modules():
#     """List all non Standard library modules."""
#     site_lib_dir = sysconfig.get_config_vars('LIBDEST')[0]
#     site_lib_dir += '/site-packages'
#     modules_lst = []
#     for top, dirs, files in os.walk(site_lib_dir):
#         for nm in files:
#             if nm != '__init__.py' and nm[-3:] == '.py':
#                 modules_lst.append(os.path.join(top, nm)[len(site_lib_dir)+1:-3].replace('\\','.'))
#     pp.pprint(modules_lst)


# def docstr2readme():
#     """Copy main module docstring to README.rst."""
#     with io.open(appinfo.APP_NAME + '/' + appinfo.APP_NAME + '.py',
#                  encoding=UTF_ENC) as f_in:
#         text = f_in.readlines()
#
#     text2copy = appinfo.APP_NAME + '\n' + '=' * len(appinfo.APP_NAME) + '\n\n'
#
#     start_copy = False
#     for line in text:
#         if '"""' in line:
#             if start_copy:
#                 break
#             else:
#                 start_copy = True
#         elif start_copy:
#             text2copy += line
#
#     text2copy += '\n'
#
#     with io.open('README.rst', encoding=UTF_ENC) as f_in:
#         text = f_in.readlines()
#
#     until_eof = False
#
#     for line in text:
#         if 'Resources' in line or until_eof:
#             text2copy += line
#             until_eof = True
#
#     with io.open('README.rst', 'w', encoding=UTF_ENC) as f_out:
#         f_out.writelines(text2copy)


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    eval(sys.argv[1])
