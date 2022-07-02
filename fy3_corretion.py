#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @Time : 2021/12/24 10:21 
# @Author :
# @File : fy3_corretion.py
from osgeo import gdal, osr
import os

def geoMERSI2(file, geoFile, afterGeoPath):
    '''

    Parameters
    ----------
    file : Absolute file path
Files that need to be corrected.
    geoFile : Absolute file path
Geographic coordinates exist in the file.
    afterGeoPath : Tif Indicates the absolute path of the tif folder
Corrected TIF format Albers projection 250m spatial resolution.
    Returns
    -------
    None.

    '''

    dataset = gdal.Open(file)

    vrtEV_EmissiveDir = os.path.splitext(file)[0]+'EV_Emissive' + '.vrt'
    vrtEV_RefSBDir = os.path.splitext(file)[0] + 'EV_RefSB' + '.vrt'
    subDatasetEV_Emissive = dataset.GetSubDatasets()[0][0]  #
    subDatasetEV_RefSB= dataset.GetSubDatasets()[1][0]
    vrtEV_EmissiveFile = gdal.Translate(vrtEV_EmissiveDir,
                             subDatasetEV_Emissive,
                             format='vrt')
    vrtEV_RefSBDirFile = gdal.Translate(vrtEV_RefSBDir,
                             subDatasetEV_RefSB,
                             format='vrt')
    '''
    Information describing the GEOLOCATION metadata field needs to be written：
        <Metadata domain="GEOLOCATION">
         <MDI key="LINE_OFFSET">1</MDI>
         <MDI key="LINE_STEP">1</MDI>
         <MDI key="PIXEL_OFFSET">1</MDI>
         <MDI key="PIXEL_STEP">1</MDI>
         <MDI key="SRS">GEOGCS["WGS84",DATUM["WGS_1984",SPHEROID["WGS84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9108"]],AUTHORITY["EPSG","4326"]]</MDI>
         <MDI key="X_BAND">1</MDI>
         <MDI key="X_DATASET">HDF5:"D:\dengkaiyuan\data\FY3C_VIRRX_GBAL_L1_20211110_0825_GEOXX_MS.HDF"://Geolocation/Longitude</MDI>
         <MDI key="Y_BAND">1</MDI>
         <MDI key="Y_DATASET">HDF5:"D:\dengkaiyuan\data\FY3C_VIRRX_GBAL_L1_20211110_0825_GEOXX_MS.HDF"://Geolocation/Latitude</MDI>
        </Metadata> 
    '''
    srs = osr.SpatialReference()
    srs.ImportFromProj4(
        '+proj=aea +lat_0=0 +lon_0=105 +lat_1=25 +lat_2=47 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs')

    lines = []
    with open(vrtEV_EmissiveDir, 'r') as f:
        for line in f:
            lines.append(line)

    lines.insert(1, '<Metadata domain="GEOLOCATION">\n')
    lines.insert(2, ' <MDI key="LINE_OFFSET">1</MDI>\n')
    lines.insert(3, ' <MDI key="LINE_STEP">1</MDI>\n')
    lines.insert(4, ' <MDI key="PIXEL_OFFSET">1</MDI>\n')
    lines.insert(5, ' <MDI key="PIXEL_STEP">1</MDI>\n')
    lines.insert(6,
                 ' <MDI key="SRS">GEOGCS["WGS84",DATUM["WGS_1984",SPHEROID["WGS84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9108"]],AUTHORITY["EPSG","4326"]]</MDI>\n')
    lines.insert(7, ' <MDI key="X_BAND">1</MDI>')
    lines.insert(8, ' <MDI key="X_DATASET">HDF5:"{}"://Geolocation/Longitude</MDI>\n'.format(geoFile))
    lines.insert(9, ' <MDI key="Y_BAND">1</MDI>\n')
    lines.insert(10, ' <MDI key="Y_DATASET">HDF5:"{}"://Geolocation/Latitude</MDI>\n'.format(geoFile))
    lines.insert(11, '</Metadata>\n')
    with open(vrtEV_EmissiveDir, 'w') as f:
        for line in lines:
            f.writelines(line)
    '''
    geoData = gdal.Warp('F:\Py_project\gdalDealMERSI2\Warp_B24_WGS.tif',  
              'F:\Py_project\gdalDealMERSI2\MERSI2_0403_B24_vrt.vrt', 
              format='GTiff', geoloc=True, dstSRS="EPSG:4326",
              xRes=0.25, yRes=0.25)
    '''
    # outfile name
    os.path.basename(file).split()
    tempname1= os.path.splitext(file)[0] + 'EV_Emissive' + '.tif'
    tempname2= os.path.splitext(file)[0] + 'EV_RefSB' + '.tif'

    EV_Emissivefile = os.path.join(afterGeoPath,os.path.basename(tempname1))
    geoData = gdal.Warp(EV_Emissivefile, vrtEV_EmissiveDir,
                        format='GTiff', geoloc=True, dstSRS=srs,
                        resampleAlg=gdal.GRIORA_Bilinear, xRes=1000, yRes=1000)
    lines = []
    with open(vrtEV_RefSBDir, 'r') as f:
        for line in f:
            lines.append(line)
    lines.insert(1, '<Metadata domain="GEOLOCATION">\n')
    lines.insert(2, ' <MDI key="LINE_OFFSET">1</MDI>\n')
    lines.insert(3, ' <MDI key="LINE_STEP">1</MDI>\n')
    lines.insert(4, ' <MDI key="PIXEL_OFFSET">1</MDI>\n')
    lines.insert(5, ' <MDI key="PIXEL_STEP">1</MDI>\n')
    lines.insert(6,
                 ' <MDI key="SRS">GEOGCS["WGS84",DATUM["WGS_1984",SPHEROID["WGS84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9108"]],AUTHORITY["EPSG","4326"]]</MDI>\n')
    lines.insert(7, ' <MDI key="X_BAND">1</MDI>')
    lines.insert(8, ' <MDI key="X_DATASET">HDF5:"{}"://Geolocation/Longitude</MDI>\n'.format(geoFile))
    lines.insert(9, ' <MDI key="Y_BAND">1</MDI>\n')
    lines.insert(10, ' <MDI key="Y_DATASET">HDF5:"{}"://Geolocation/Latitude</MDI>\n'.format(geoFile))
    lines.insert(11, '</Metadata>\n')
    with open(vrtEV_RefSBDir, 'w') as f:
        for line in lines:
            f.writelines(line)
    EV_RefSBfile = os.path.join(afterGeoPath, os.path.basename(tempname2))
    geoData = gdal.Warp(EV_RefSBfile, vrtEV_RefSBDir,
                        format='GTiff', geoloc=True, dstSRS=srs,
                        resampleAlg=gdal.GRIORA_Bilinear, xRes=1000, yRes=1000)
    if geoData == None:
        print('deal failure!')
    del geoData
    print('{} finish Geo\n'.format(file))


if __name__ == '__main__':

    afterGeoPath = r'D:\x\data\fy3'   # output
    fy3file = r'D:\x\data\fy3\FY3C_VIRRX_GBAL_L1_20211110_0825_1000M_MS.HDF'
    fy3GEOfile =r'D:\x\data\fy3\FY3C_VIRRX_GBAL_L1_20211110_0825_GEOXX_MS.HDF'

    geoMERSI2(fy3file, fy3GEOfile, afterGeoPath)


