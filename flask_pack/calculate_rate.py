from PIL import Image
import cv2


def calculate_rate(path: str, img_name: str, num: str = '1') -> tuple:
    """
    输入路径、图片名称以及序号，获得绿化率
    num='1'时，(128, 0, 0)
    num='3'时，(0, 128, 0)
    为绿化
    """
    img_path = f'{path}/result_temp2/{img_name}'
    image = Image.open(img_path)  # 图片的路径

    a, b = image.size  # 获得图像的长、宽
    count1 = 0
    count2 = 0

    for i in range(a):  # 遍历图像的行
        for j in range(b):  # 遍历图像的列
            pixel = image.getpixel((i, j))  # 读取该点的像素值
            if pixel == (128, 0, 0):
                count1 += 1
            elif num == '3' and pixel == (0, 128, 0):
                count2 += 1
    
    return round(count1 / (a * b) * 100, 2), round(count2 / (a * b) * 100, 2), round((count1 + count2) / (a * b) * 100, 2)
