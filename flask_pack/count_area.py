from PIL import Image
import cv2

img_path='train_1.png'
image = Image.open(img_path)  # 图片的路径

a, b = image.size  # 获得图像的长、宽
count=0
rate=1e+6   #比例尺
for i in range(a):  # 遍历图像的行
    for j in range(b):  # 遍历图像的列
        pixel = image.getpixel((i, j))  # 读取该点的像素值
        if pixel != 0:
            count+=1
size=cv2.imread(img_path).shape
img_size=size[0]*size[1]
print('面积为: {0:.2f} km²'.format(count/img_size*rate/100))