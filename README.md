# Automate Standard QGIS Tasks - PyQGIS

Contains a standalone python script that can be modified to automate your QGIS tasks, such as deleting fields, adding fields, field calculations, and geoprocessing (such as buffering and fixing geometries). So far, the script only works with vector files and with QGIS 3.28 (long-term relsease).

You must make the modifications necessary to the script to automate your procedure. For instance, if you need to use a particular QGIS tool in your procedure, it recommended to use the [QGIS User guide](https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/index.html) to find out how to use the 'out-of-the-box' geoprocessing operations. The script itself does contain some comments that will guide you, but you should have at least am intermediate level of Python knowledge to get the script to work how you want it to.

<br>

## Installation

Contains two .cmd files that creates a PYQGIS Environment through VSCode. You will need to install both QGIS (v. 3.28) and VSCode (along with a Python installation), and then modify these files to point to the destinations of installation. This way, the QGIS.Core and Processing libraries will be available to you.
