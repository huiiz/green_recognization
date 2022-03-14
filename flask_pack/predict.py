from PIL import Image
from deeplab.deeplab import DeeplabV3
from unet.unet import Unet
import os
from threading import Thread
from calculate_rate import clear_rates_data, calculate_rate
from utils import save_img, cat_img
total_count = 0
result_ls = []
stop = False


def predict(path, img_path, num, input_net='0'):
    clear_rates_data()
    net = Unet(path, num) if input_net == '0' else DeeplabV3(path, num)
    try:
        # img_list = [f'{path}/png_temp/{i}_{j}.png' for i in range(x) for j in range(y)]
        img_list = [os.path.join(img_path, f) for f in os.listdir(
            img_path) if f.endswith('.jpg') or f.endswith('.png')]
        global result_ls, total_count, stop
        total_count = len(img_list)
        result_ls = []
        stop = False
        for img in img_list:
            if stop:
                break
            image = Image.open(img)
            # 返回①原始生成的图片与②生成图片与预测图片合并
            r_image_single, r_image_combined = net.detect_image(image)
            res_name1 = path+'/result_temp/'+img.split('\\')[-1]
            res_name2 = path+'/result_temp2/'+img.split('\\')[-1]
            res_name3 = path+'/result_temp3/'+img.split('\\')[-1]
            result_ls.append(img.split('\\')[-1])
            # print(res_name)
            t1 = Thread(target=save_img, args=(r_image_combined, res_name1))
            t2 = Thread(target=save_img, args=(r_image_single, res_name2))
            t3 = Thread(target=cat_img, args=(
                image, r_image_combined, res_name3))
            # r_image_combined.save(res_name1)
            # r_image_single.save(res_name2)
            t4 = Thread(target=calculate_rate, args=(
                path, img.split('\\')[-1], num))
            for t in [t1, t2, t3, t4]:
                t.start()

    except:
        print('Open Error! Try again!')


def get_predict_ls():
    return result_ls


def get_total_count():
    return total_count


def stop_predict():
    global stop
    stop = True
