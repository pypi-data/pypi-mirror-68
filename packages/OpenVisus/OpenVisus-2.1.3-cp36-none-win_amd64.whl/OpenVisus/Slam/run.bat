REM slam version for Windows 64 bit and Python 3.7 (the version is important)
REM Edit the file `run_slam.bat` and
REM (*) change the `PYTHON_EXECUTABLE` to point to your python
REM (*) change the last line to point to your slam sequence

set PYTHON_EXECUTABLE=C:/Python37/python.exe
set OpenVisusDir=%~dp0\..
cd %OpenVisusDir%
for /f "usebackq tokens=*" %%G in (`%PYTHON_EXECUTABLE% -c "import os,PyQt5; print(os.path.dirname(PyQt5.__file__))"`) do set Qt5_DIR=%%G\Qt
set PATH=%Qt5_DIR%\bin;%OpenVisusDir%\bin;%PATH%
set QT_PLUGIN_PATH=%Qt5_DIR%\plugins
set PYTHONPATH=%OpenVisusDir%\..
%PYTHON_EXECUTABLE% -B -m slam "E:\google_sci\visus_slam\TaylorGrant"




