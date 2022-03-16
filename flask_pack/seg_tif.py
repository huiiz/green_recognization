# -*- coding: utf-8 -*-
# 废弃
import os
from osgeo import gdal
from common import clear_fold
seg_count = 0
seg_total = 0
x_count = 0
y_count = 0

class GRID:
    # 读图像文件
    def read_img(self, filename):
        dataset = gdal.Open(filename)  # 打开文件

        im_width = dataset.RasterXSize  # 栅格矩阵的列数
        im_height = dataset.RasterYSize  # 栅格矩阵的行数

        im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
        im_proj = dataset.GetProjection()  # 地图投影信息
        im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 将数据写成数组，对应栅格矩阵

        del dataset
        return im_proj, im_geotrans, im_data

    # 写文件，以写成tif为例
    def write_img(self, filename, im_proj, im_geotrans, im_data):
        # gdal数据类型包括
        # gdal.GDT_Byte,
        # gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
        # gdal.GDT_Float32, gdal.GDT_Float64

        # 判断栅格数据的数据类型
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

        # 判读数组维数
        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        else:
            im_bands, (im_height, im_width) = 1, im_data.shape

            # 创建文件
        driver = gdal.GetDriverByName("GTiff")  # 数据类型必须有，因为要计算需要多大内存空间
        dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影

        if im_bands == 1:
            dataset.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
        else:
            for i in range(im_bands):
                dataset.GetRasterBand(i + 1).WriteArray(im_data[i])

        del dataset

def seg(path):
    proj, geotrans, data = GRID().read_img(f'{path}/tif_file/to_predict.tif')  # 读数据
    width, height = data.shape
    global seg_count, seg_total, x_count, y_count
    seg_count = 0
    x_count = width // 256
    y_count = height // 256
    seg_total = x_count * y_count
    if os.listdir(f'{path}/tif_temp/'):
        clear_fold(path, 'tif_temp')
        clear_fold(path, 'png_temp')
        clear_fold(path, 'result_temp')
    for i in range(width // 256):  # 切割成256*256小图
        for j in range(height // 256):
            seg_count += 1
            cur_image = data[i * 256:(i + 1) * 256, j * 256:(j + 1) * 256]
            GRID().write_img(f'{path}/tif_temp/{i}_{j}.tif', proj, geotrans, cur_image)  ##写数据

def get_seg_count():
    return seg_count

def get_seg_total():
    return x_count, y_count, seg_total