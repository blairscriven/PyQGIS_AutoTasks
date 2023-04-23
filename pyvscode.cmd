@echo off
SET OSGEO4W_ROOT=C:\Your_QGIS_root_folder
call "%OSGEO4W_ROOT%"\bin\o4w_env.bat

path %PATH%;%OSGEO4W_ROOT%\apps\qgis-ltr\bin
path %PATH%;%OSGEO4W_ROOT%\apps\qt5\bin
path %PATH%;%OSGEO4W_ROOT%\apps\Python39\Scripts
set QGIS_PREFIX=%OSGEO4W_ROOT%\apps\qgis-ltr
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python39
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-ltr\python;%OSGEO4W_ROOT%\apps\qgis-ltr\python\plugins;%PYTHONPATH%
set QT_QPA_PLATFORM_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\Qt5\plugins\platforms
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis-ltr\qtplugins;%OSGEO4W_ROOT\apps\qt5\plugins

set GDAL_FILENAME_IS_UTF8=YES
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000

start "VSCode aware of QGIS" /B "C:\Your_VSCode_folder\Microsoft VS Code\Code.exe"
