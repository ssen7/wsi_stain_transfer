import staintools
from openslide import open_slide
from PIL import Image
import math
import pickle


def reconstruct(slide, patch_dict, save_dir):
    '''
    Reconstruct images from Image name and coordinates present in the image.
    Image name format: (img_name)__x_y
    '''
    print("Reconstructing and saving the image...")

    result = Image.new("RGB", (slide.dimensions))

    for key in patch_dict.keys():
        name = key.split('__')[0]
        coords = key.split('__')[-1]
        x, y = [int(i) for i in coords.split('_')]

        img = patch_dict[key]
        # print(x, y, img.width, img.height)
        # print(img.width, img.height)

        result.paste(img, (x, y))

    result.save(save_dir + '/'+name + '.png')
