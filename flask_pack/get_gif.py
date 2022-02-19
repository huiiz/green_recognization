from imageio import mimsave
import os
from PIL import Image

def create_gif(path,  gif_name='result.gif', duration=1):
    img_list = [os.path.join(f'{path}/result_temp', f) for f in os.listdir(f'{path}/result_temp') if f.endswith('.jpg') or f.endswith('.png')]
    frames = []
    for image_name in img_list:
        frames.append(Image.open(image_name))
    mimsave(f'{path}/{gif_name}', frames, 'GIF-PIL', duration=duration)
    