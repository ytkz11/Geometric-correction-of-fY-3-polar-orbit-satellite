## Record of problems encountered:
1. For the geometric correction of fengyun polar-orbiting satellites, there are independent longitude, latitude and DN data. GLT correction was tried but failed
## Solution:
Construct VRT file and then make geometric correction.
# # VRT file
[official VRT] (https://www.osgeo.cn/gdal/drivers/raster/vrt.html)
The VRT driver is a format driver for GDAL that allows virtual GDAL datasets to be composed of other GDAL datasets, with relocation, algorithms that may be applied, and various metadata that can be changed or added. A VRT description of a data set can be saved in XML format, usually with an extension. VRT.

Sample of EV_Emissive and EV_RefSB data extraction for Fy-3