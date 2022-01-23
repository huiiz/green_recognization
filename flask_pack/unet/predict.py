#----------------------------------------------------#
#   对视频中的predict.py进行了修改，
#   将单张图片预测、摄像头检测和FPS测试功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
#----------------------------------------------------#
import time
import os
import cv2
import numpy as np
from PIL import Image

from unet import Unet

if __name__ == "__main__":
    #-------------------------------------------------------------------------#
    #   如果想要修改对应种类的颜色，到generate函数里修改self.colors即可
    #-------------------------------------------------------------------------#
    unet = Unet()
    #-------------------------------------------------------------------------#
    #   mode用于指定测试的模式：
    #   'dir'表示批量预测
    #-------------------------------------------------------------------------#
    mode = "dir"

    # save_path='D:'

    '''
        predict.py有几个注意点
        1、该代码无法直接进行批量预测，如果想要批量预测，可以利用os.listdir()遍历文件夹，利用Image.open打开图片文件进行预测。
        具体流程可以参考get_miou_prediction.py，在get_miou_prediction.py即实现了遍历。
        2、如果想要保存，利用r_image.save("img.jpg")即可保存。
        3、如果想要原图和分割图不混合，可以把blend参数设置成False。
        4、如果想根据mask获取对应的区域，可以参考detect_image函数中，利用预测结果绘图的部分，判断每一个像素点的种类，然后根据种类获取对应的部分。
        seg_img = np.zeros((np.shape(pr)[0],np.shape(pr)[1],3))
        for c in range(self.num_classes):
            seg_img[:, :, 0] += ((pr == c)*( self.colors[c][0] )).astype('uint8')
            seg_img[:, :, 1] += ((pr == c)*( self.colors[c][1] )).astype('uint8')
            seg_img[:, :, 2] += ((pr == c)*( self.colors[c][2] )).astype('uint8')
    '''
    if mode == 'dir':
        while(True):
            path = input('Input image file_path:')
            if path == 'exit':
                exit(1)  # 输入exit退出
            else:
                try:
                    img_list = [os.path.join(path, f) for f in os.listdir(
                        path) if f.endswith('.jpg') or f.endswith('.png')]
                    for img in img_list:
                        image = Image.open(img)
                        r_image = unet.detect_image(image)
                        r_image.show()

                except:
                    print('Open Error! Try again!')
                    continue
