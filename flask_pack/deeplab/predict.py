from time import sleep
from PIL import Image
from deeplab.deeplab import DeeplabV3
import os
total_count = 0
result_ls = []
stop = False

def d_predict(path, img_path, num):
    deeplab = DeeplabV3(path, num)
    try:
        # img_list = [f'{path}/png_temp/{i}_{j}.png' for i in range(x) for j in range(y)]
        img_list = [os.path.join(img_path, f) for f in os.listdir(img_path) if f.endswith('.jpg') or f.endswith('.png')]
        global result_ls, total_count, stop
        total_count = len(img_list)
        result_ls = []
        stop = False
        for img in img_list:
            if stop:
                break
            image = Image.open(img)
            r_image = deeplab.detect_image(image)
            res_name = path+'/result_temp/'+img.split('\\')[-1]
            result_ls.append(img.split('\\')[-1])
            # print(res_name)
            r_image.save(res_name)

    except:
        print('Open Error! Try again!')


def get_d_predict_ls():
    return result_ls

def get_d_total_count():
    return total_count

def stop_d_predict():
    global stop
    stop = True