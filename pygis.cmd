@echo off
SET OSGEO4W_ROOT=C:\Your_QGIS_root_folder
call "%OSGEO4W_ROOT%"\bin\o4w_env.bat
call "%OSGEO4W_ROOT%"\apps\grass\grass82\etc\env.bat
@echo off
path %PATH%;%OSGEO4W_ROOT%\apps\qgis-ltr\bin
path %PATH%;%OSGEO4W_ROOT%\apps\grass\grass82\lib
path %PATH%;C:\Your_QGIS_root_folder\apps\qt5\bin
path %PATH%;C:\Your_QGIS_root_folder\apps\Python39\Scripts

set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis-ltr\python
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python39


cmd.exe