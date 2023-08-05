
cd %~dp0
set PATH=C:\Python36-x64\python.exe\..;.\bin;bin\Qt\bin;%PATH%
set PYTHONPATH=C:\projects\openvisus\build_win\Release\OpenVisus;C:\Python36-x64\python36.zip;C:\Python36-x64\DLLs;C:\Python36-x64\lib;C:\Python36-x64;C:\Python36-x64\lib\site-packages
set QT_PLUGIN_PATH=bin\Qt\plugins
"bin\visusviewer.exe" %*
