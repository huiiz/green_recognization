from PIL import Image
import shutil
import os

def save_img(img: Image, name: str):
    """
    保存图片
    """
    img.save(name)


def cat_img(img1: Image, img2: Image, name: str, flag: str = 'horizontal'):
    """
    合并图片
    """
    # 自定义设置宽高(自行修改要拼接的图片分辨率)
    img1 = img1.resize((img1.size[0], img1.size[0]), Image.ANTIALIAS)
    img2 = img2.resize((img1.size[0], img1.size[0]), Image.ANTIALIAS)
    size1, size2 = img1.size, img2.size
    if flag == 'horizontal':
        # 横向拼接
        # 创建Image对象(模式，大小)，横向宽度就是两张图片相加，高度不变
        joint = Image.new('RGB', (size1[0] + size2[0], size1[1]))
        loc1, loc2 = (0, 0), (size1[0], 0)
        # 按位置拼接，二元组
        joint.paste(img1, loc1)
        joint.paste(img2, loc2)
    elif flag == 'vertical':
        joint = Image.new('RGB', (size1[0], size1[1] + size2[1]))
        loc1, loc2 = (0, 0), (0, size1[1])
        joint.paste(img1, loc1)
        joint.paste(img2, loc2)
    save_img(joint, name)


def clear_folds(path: str, folds: tuple):
    try:
        for fold in folds:
            shutil.rmtree(f'{path}/{fold}')
            os.mkdir(f'{path}/{fold}')
        return True
    except:
        return False

def make_folds(path, folds):
    try:
        for fold in folds:
            os.mkdir(f'{path}/{fold}')
        return True
    except:
        return False

def del_folds(path, folds):
    try:
        for fold in folds:
            shutil.rmtree(f'{path}/{fold}')
        return True
    except:
        return False