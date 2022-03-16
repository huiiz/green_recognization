# 废弃
import os
from osgeo import gdal
from seg_tif import seg
change_count = 0

def change(path):
    open_path = f'{path}/tif_temp'
    save_path = f'{path}/png_temp'
    global change_count
    change_count = 0
    images = os.listdir(open_path)
    for image in images:
        change_count += 1
        im = gdal.Open(os.path.join(open_path, image))
        driver = gdal.GetDriverByName('PNG')
        driver.CreateCopy(os.path.join(save_path, image.split('.')[0] + ".png"), im)

def seg_and_change(path):
    global change_count
    change_count = 0
    seg(path)
    change(path)

def get_change_count():
    return change_count