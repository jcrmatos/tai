@echo off

rem Copyright 2009-2015 Joao Carlos Roseta Matos
rem
rem This program is free software: you can redistribute it and/or modify
rem it under the terms of the GNU General Public License as published by
rem the Free Software Foundation, either version 3 of the License, or
rem (at your option) any later version.
rem
rem This program is distributed in the hope that it will be useful,
rem but WITHOUT ANY WARRANTY; without even the implied warranty of
rem MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
rem GNU General Public License for more details.
rem
rem You should have received a copy of the GNU General Public License
rem along with this program.  If not, see <http://www.gnu.org/licenses/>.

set OLDPATH=%PATH%
set OLDPYTHONPATH=%PYTHONPATH%

set REBUILD_REFERENCE=YES
set CHECK_PY3_COMPATIBILITY=YES

if "%1"=="-h" goto :HELP
if "%1"=="help" goto :HELP
goto :NOHELP

:HELP
echo Usage:
echo.
echo build -h, help   show this help message
echo build            builds sdist/bdist_wheel or just sdist if APP_TYPE = 'module' inside appinfo.py
echo build clean      clears dirs and files
echo build cxf        builds windows exe including Python runtime - not working for the moment
echo build doc        builds doc
echo build dumb       builds bdist_dumb (zip on Windows, tar/ztar/gztar/zip on GNU Linux in the future)
echo build egg        builds bdist_egg (egg)
echo build exe        builds bdist_wininst (exe) - requires Python to be installed on destination
echo build msi        builds bdist_msi (msi) - requires Python to be installed on destination
echo build py2exe     builds windows exe including Python runtime
echo build pypi       uploads dists to PyPI (including documentation)
echo build pypitest   uploads dists to test
echo build rpm        builds bdist_rpm (rpm/srpm) - only works on GNU Linux (in the future)
echo build src        builds sdist (zip on Windows, tar.gz on GNU Linux in the future)
echo build test       run tests
echo build whl        builds bdist_wheel (whl)
echo.
echo See requirements-dev.txt for build requirements.
echo.
goto :EXIT

:NOHELP
cls
python setup_utils.py app_name()
if not exist app_name.txt goto :EXIT
for /f "delims=" %%f in (app_name.txt) do set PROJECT=%%f
del app_name.txt

if "%1"=="pypi" goto :PYPI
if "%1"=="pypitest" goto :PYPITEST

echo.
echo *** Clean
echo.
if exist app_ver.txt del app_ver.txt
if exist app_name.txt del app_name.txt
if exist app_type.txt del app_type.txt
if exist py_ver.txt del py_ver.txt
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist test\*.pyc del test\*.pyc

python setup_utils.py app_ver()
if not exist app_ver.txt goto :EXIT
for /f "delims=" %%f in (app_ver.txt) do set APP_VER=%%f
del app_ver.txt

if exist *.pyc del *.pyc
if exist %PROJECT%\*.pyc del %PROJECT%\*.pyc
if exist %PROJECT%.egg-info rd /s /q %PROJECT%.egg-info
if exist %PROJECT%-%APP_VER% rd /s /q %PROJECT%-%APP_VER%
if exist %PROJECT%\doc rd /s /q %PROJECT%\doc

if "%1"=="clean" goto :EXIT

echo.
echo *** Update some files
echo.

if "%PYTHON_EASYSETUP_AUTHOR%"=="" goto :NO_COPYRIGHT_UPD

:COPYRIGHT_UPD
python setup_utils.py check_copyright()
if ERRORLEVEL==1 goto :EXIT

python setup_utils.py update_copyright()

:NO_COPYRIGHT_UPD
python setup_utils.py upd_usage_in_readme()

copy /y README.rst %PROJECT%\README.txt > nul
copy /y LICENSE.rst %PROJECT%\LICENSE.txt > nul
copy /y AUTHORS.rst %PROJECT%\AUTHORS.txt > nul
copy /y ChangeLog.rst %PROJECT%\ChangeLog.txt > nul

copy /y appinfo.py %PROJECT% > nul

python setup_utils.py app_type()
if not exist app_type.txt goto :EXIT
for /f "delims=" %%f in (app_type.txt) do set PROJ_TYPE=%%f
del app_type.txt

python setup_utils.py py_ver()
if not exist py_ver.txt goto :EXIT
for /f "delims=" %%f in (py_ver.txt) do set PY_VER=%%f
del py_ver.txt

:CHECKERS
echo.
echo *** Checkers
echo.

for %%a in (%PROJECT%\*.py) do flake8 %%a
rem set PYTHONPATH=%PYTHONPATH%:%PROJECT%
rem for %%a in (%PROJECT%\*.py) do pylint -r n %%a
echo.
echo *** If there were errors or warnings press Ctrl-C to interrupt this batch file, fix them and rerun build.cmd.
echo.
pause

if "%CHECK_PY3_COMPATIBILITY%"=="" goto :NO_CHECK_PY3_COMPAT

echo.
echo *** Py3 compat checkers
echo.
for %%a in (%PROJECT%\*.py) do pylint -r n --py3k %%a
echo.
echo *** If there were errors or warnings (No config file found... is OK) press Ctrl-C to interrupt this batch file, fix them and rerun build.cmd.
echo *** If there weren't any errors above, consider an additional check by running the application with python -3 %PROJECT%
echo.
pause

:NO_CHECK_PY3_COMPAT
cls
if "%1"=="doc" goto :DOC

:TEST
if not exist test goto :DOC
echo.
echo *** Test
echo.

rem *** source doctest ***
rem python -m doctest %PROJECT%\%PROJECT%.py

rem *** doctest ***
rem python -m doctest -v test\test.rst

rem *** unittest ***
rem ren test\test_%PROJECT%.py pytest_test_%PROJECT%.py
rem ren test\doctest_test_%PROJECT%.py test_%PROJECT%.py
rem python -m unittest discover -v -s test
rem ren test\test_%PROJECT%.py doctest_test_%PROJECT%.py
rem ren test\pytest_test_%PROJECT%.py test_%PROJECT%.py

py.test --cov-report term-missing --cov %PROJECT% -v test
if ERRORLEVEL==1 goto :EXIT

if "%1"=="test" goto :EXIT
pause
cls

:DOC
if not exist doc goto :NO_DOC

echo.
echo *** Sphinx
echo.
set SPHINXOPTS=-E
set PATH=c:\miktex\miktex\bin;%PATH%

if "%REBUILD_REFERENCE%"=="YES" easysetup -q -r

python setup_utils.py change_sphinx_theme()

copy /y README.rst README.rst.bak > nul
python setup_utils.py remove_copyright()

cd doc
cmd /c make clean

cmd /c make html
if not exist ..\%PROJECT%\doc md ..\%PROJECT%\doc
xcopy /y /e _build\html\*.* ..\%PROJECT%\doc\ > nul

cmd /c make clean

if not exist index.ori ren index.rst index.ori
python ..\setup_utils.py prep_rst2pdf()

cmd /c make latex
cd _build\latex
pdflatex.exe %PROJECT%.tex
echo ***
echo *** Repeat to correct references
echo ***
pdflatex.exe %PROJECT%.tex
copy /y %PROJECT%.pdf ..\..\..\%PROJECT%\doc > nul
cd ..\..

if exist index.rst del index.rst
ren index.ori index.rst

cmd /c make clean
cd ..
del README.rst
ren README.rst.bak README.rst

python setup_utils.py create_doc_zip()

if "%1"=="doc" goto :EXIT

:NO_DOC
pause
cls

if "%1"=="cxf" goto :CXF
if "%1"=="dumb" goto :DUMB
if "%1"=="egg" goto :EGG
if "%1"=="exe" goto :EXE
if "%1"=="msi" goto :MSI
if "%1"=="py2exe" goto :PY2EXE
if "%1"=="rpm" goto :RPM
if "%1"=="whl" goto :WHL

:SRC
python setup_utils.py sleep(5)
echo.
echo *** sdist build
echo.
python setup.py sdist
echo.
echo *** End of sdist build. Check for errors.
echo.
if "%PROJ_TYPE%"=="module" goto :MSG
if "%1"=="src" goto :MSG
pause

:WHL
echo.
echo *** bdist_wheel build
echo.
python setup.py bdist_wheel
echo.
echo *** End of bdist_wheel build. Check for errors.
echo.
goto :MSG

:EGG
echo.
echo *** bdist_egg build
echo.
python setup.py bdist_egg
echo.
echo *** End of bdist_egg build. Check for errors.
echo.
goto :MSG

:EXE
echo.
echo *** bdist_wininst build
echo.
python setup.py bdist_wininst
echo.
echo *** End of bdist_winist build. Check for errors.
echo.
goto :MSG

:DUMB
echo.
echo *** bdist_dumb build
echo.
python setup.py bdist_dumb
echo.
echo *** End of bdist_dumb build. Check for errors.
echo.
goto :MSG

:MSI
echo.
echo *** bdist_msi build
echo.
python setup.py bdist_msi
echo.
echo *** End of bdist_msi build. Check for errors.
echo.
goto :MSG

:RPM
echo.
echo *** bdist_rpm build
echo.
python setup.py bdist_rpm
echo.
echo *** End of bdist_rpm build. Check for errors.
echo.
goto :MSG

:MSG
echo.
echo *** If there were filesystem errors (eg. directory not empty), random syntax or unicode errors, try repeating the build up to 3 times. At least on my system that works.
echo.
goto :EXIT

:CXF
echo.
echo *** CXF
echo.
echo Not working yet...
rem python cxf_setup.py build bdist_msi
rem python cxf_setup.py build_exe
rem cxfreeze cxf_setup.py build_exe
rem echo ***
rem echo *** Copy datafiles
rem echo ***
rem copy build\exe.win32-%PY_VER%\%PROJECT%\*.* build\exe.win32-%PY_VER%
goto :EXIT

:PY2EXE
echo.
echo *** PY2EXE
echo.
python setup_py2exe.py py2exe
if exist dist\__main__.exe ren dist\__main__.exe %PROJECT%.exe

echo.
echo *** Check if you need to add any files or directories to DATA_FILES_PY2EXE in setup_py2exe.py.
echo.
goto :EXIT

:PYPI
echo.
echo *** PyPI: Register and upload
echo.
python setup.py register -r pypi
twine upload dist/*
if ERRORLEVEL==1 goto :EXIT
rem *** old way ***
rem if "%PROJ_TYPE%"=="module" python setup.py sdist upload -r pypi
rem if "%PROJ_TYPE%"=="module" goto :EXIT
rem rem python setup.py sdist bdist_egg bdist_wininst bdist_wheel upload -r pypi
rem python setup.py sdist bdist_wheel upload -r pypi

if exist %PROJECT%\doc python setup.py register upload_docs --upload-dir=%PROJECT%\doc
goto :EXIT

:PYPITEST
echo.
echo *** PYPITEST: Register and upload
echo.
python setup.py register -r test
twine upload -r test dist/*
rem *** old way ***
rem if "%PROJ_TYPE%"=="module" python setup.py sdist upload -r test
rem if "%PROJ_TYPE%"=="module" goto :EXIT
rem rem python setup.py sdist bdist_egg bdist_wininst bdist_wheel upload -r test
rem python setup.py sdist bdist_wheel upload -r test

:EXIT
set PATH=%OLDPATH%
set PYTHONPATH=%OLDPYTHONPATH%
set OLDPATH=
set OLDPYTHONPATH=
set PY_VER=
set APP_VER=
set PROJ_TYPE=
set PROJECT=
set SPHINXOPTS=
set REBUILD_REFERENCE=
set CHECK_PY3_COMPATIBILITY=
