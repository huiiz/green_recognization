from imageio import mimsave
import os
from PIL import Image, ImageDraw, ImageFont

setFont = ImageFont.truetype('font/simhei.ttf', 60)
fillColor = "#ffffff"

def create_gif(path,  gif_name='result.gif', duration=1):
    """
    创建gif动图
    """
    img_list = [os.path.join(f'{path}/result_temp', f) for f in os.listdir(f'{path}/result_temp') if f.endswith('.jpg') or f.endswith('.png')]
    img_list.sort()
    frames = []
    for image_name in img_list:
        text = '.'.join(image_name.split('\\')[-1].split('.')[:-1])
        image = Image.open(image_name)
        draw = ImageDraw.Draw(image)
        draw.text((5,5), text,font=setFont,fill=fillColor,direction=None)
        frames.append(image)
    mimsave(f'{path}/{gif_name}', frames, 'GIF-PIL', duration=duration)
