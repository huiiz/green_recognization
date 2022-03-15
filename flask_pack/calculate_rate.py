import time
from PIL import Image


rates = {}

def clear_rates_data():
    global rates
    rates = {}

def calculate_rate(path: str, img_name: str, num: str = '1') -> tuple:
    """
    输入路径、图片名称以及序号，获得绿化率
    num='1'时，(128, 0, 0)
    num='3'时，(0, 128, 0)
    为绿化
    """
    img_name = ''.join(img_name.split('.')[:-1])+'.png'
    img_path = f'{path}/result_temp2/{img_name}'
    while True:
        try:
            image = Image.open(img_path)  # 图片的路径
            image.getpixel((0, 0))
            print(f'{img_path}图像文件打开成功')

        except:
            print(f'{img_path}图像文件打开失败')
            time.sleep(0.1)
        else:
            break


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
    
    global rates
    rates[img_name] = round(count1 / (a * b) * 100, 2), round(count2 / (a * b) * 100, 2), round((count1 + count2) / (a * b) * 100, 2)


def getting_rate(img_name: str):
    global rates
    img_name = ''.join(img_name.split('.')[:-1])+'.png'
    while not rates.get(img_name):
        time.sleep(0.5)
        print(f'{img_name}获取rate失败')
        print(rates)


    return rates.get(img_name)
