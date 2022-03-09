from PIL import Image
from unet.unet import Unet
import os
# result_count = 0
total_count = 0
result_ls = []
stop = False

def u_predict(path, img_path, num):
    unet = Unet(path, num)
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
            r_image_single, r_image_combined = unet.detect_image(image)
            res_name1 = path+'/result_temp/'+img.split('\\')[-1]
            res_name2 = path+'/result_temp2/'+img.split('\\')[-1]
            result_ls.append(img.split('\\')[-1])
            # result_count += 1
            r_image_combined.save(res_name1)
            r_image_single.save(res_name2)

    except:
        print('Open Error! Try again!')

def get_u_predict_ls():
    return result_ls

def get_u_total_count():
    return total_count

def stop_u_predict():
    global stop
    stop = True