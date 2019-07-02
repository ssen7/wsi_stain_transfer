#!/usr/bin/env python
# coding: utf-8


# !module load openslide
#get_ipython().system('pip install openslide-python')


import staintools
from openslide import open_slide
from PIL import Image
import math
import pickle

# In[25]:


def create_patches(img_path, patch_size, overlap):

    img_name = img_path.split('/')[-1].split('.')[0]
    print(img_name)
    # img_path = image.values()

    slide = open_slide(str(img_path))

    # steps to advance per axis with overlap
    step_size = patch_size - overlap

    # get dimensions of the image
    xlim = slide.level_dimensions[0][0]
    ylim = slide.level_dimensions[0][1]
    print("Dimensions x: " + str(xlim) + " y: " + str(ylim))

    # get the number of times to traverse each axis
    x_ind = math.ceil(xlim/(step_size))
    y_ind = math.ceil(ylim/(step_size))

    # initialize list to store patches
    patches = {}
    patches_dict = {}
    patches_vals = []

    # pixels left to traverse in the y-axis at the beginning of the traversal
    img_y_left = ylim
    # initialize the starting y corner
    y = 0 - step_size
    for y_ in range(y_ind):
        # patches_dict = {}
        # patches_vals = []
        # initialize the starting x corner
        x = 0-step_size

        # advance the y axis (note: it starts with 0)
        y = y + step_size

        # pixels left to traverse in the x-axis at the beginning of the traversal
        img_x_left = xlim

        # update the number of pixels left to traverse
        img_y_left = img_y_left - step_size
#         print('y - left: ' + str(img_y_left))

        # if more than patch size left, get the (patch_size x patch_size) image
        if (img_y_left > 0 and img_y_left > step_size):
            for x_ in range(x_ind):
                x = x + (step_size)
                img_x_left = img_x_left - step_size
#                 print(img_x_left)
                if (img_x_left > 0 and img_x_left > step_size):
                    img_name_key = img_name + "__"+str(x)+"_"+str(y)
                    patches_dict[img_name_key] = slide.read_region(
                        (x, y), 0, (patch_size, patch_size))
                    # patches_vals.append(slide.read_region((x, y), 0, (patch_size, patch_size)))
                    # patches[img_name]=patches_vals
                elif (img_x_left < step_size and img_x_left > 0):
                    #                     x = xlim - patch_size
                    img_name_key = img_name + "__"+str(x)+"_"+str(y)
                    patches_dict[img_name_key] = slide.read_region(
                        (x, y), 0, (img_x_left, 1000))
                    # patches_vals.append(slide.read_region((x, y), 0, (patch_size, patch_size)))
                    # patches[img_name]=patches_vals
                    break
                # patches[img_name]=patches_vals
        # if less than patch size left, get the rest of the image, regardless of the overlap
        elif (img_y_left > 0 and img_y_left < step_size):
            y = ylim - patch_size
            for x_ in range(x_ind):
                x = x + (step_size)
                img_x_left = img_x_left - step_size
                if (img_x_left > 0 and img_x_left > step_size):
                    img_name_key = img_name + "__"+str(x)+"_"+str(y)
                    patches_dict[img_name_key] = slide.read_region(
                        (x, y), 0, (patch_size, patch_size))
                    # patches_vals.append(slide.read_region((x, y), 0, (patch_size, patch_size)))
                    # patches[img_name]=patches_vals
                elif (img_x_left < step_size and img_x_left > 0):
                    #                     x = xlim - patch_size
                    img_name_key = img_name + "__"+str(x)+"_"+str(y)
                    patches_dict[img_name_key] = slide.read_region(
                        (x, y), 0, (img_x_left, img_y_left))
                    # patches_vals.append(slide.read_region((x, y), 0, (patch_size, patch_size)))
                    # patches[img_name]=patches_vals
                    break
            break

    return patches_dict


# # In[26]:


# patch_dict = create_patches('./C06-27_01.svs', 1000, 0)

# with open('patch.pkl', 'wb') as f:
#     pickle.dump(patch_dict, f)

patch_dict = pickle.load(open('./patch.pkl', 'rb'))

slide = open_slide('./C06-27_01.svs')
result = Image.new("RGBA", (slide.dimensions))
print(slide.dimensions)
for key in patch_dict.keys():
    coords = key.split('__')[-1]
    x, y = [int(i) for i in coords.split('_')]
    print(x, y)

    img = patch_dict[key]
    print(img.width, img.height)

    result.paste(img, (x, y))


result.save('test-3.png')
