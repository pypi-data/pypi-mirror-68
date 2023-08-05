
cd %~dp0
set PATH=C:\Python37-x64\python.exe\..;.\bin;bin\Qt\bin;%PATH%
set PYTHONPATH=C:\projects\openvisus\build_win\Release\OpenVisus;C:\Python37-x64\python37.zip;C:\Python37-x64\DLLs;C:\Python37-x64\lib;C:\Python37-x64;C:\Python37-x64\lib\site-packages
set QT_PLUGIN_PATH=bin\Qt\plugins
"bin\visusviewer.exe" %*
