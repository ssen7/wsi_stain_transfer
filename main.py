from create_patches import create_patches
from reconstruct import reconstruct
from staintransfer import staintransfer
from openslide import open_slide

import pickle
import os

target_slname = './data/target/N14-02_02.svs'
sl_name = './data/ee_pak/16_002.svs'

target_slide = open_slide(target_slname)
slide = open_slide(sl_name)

x, y = target_slide.dimensions

patch_size = 1000
target = target_slide.read_region((x//2, y//2), 0, (patch_size, patch_size))

# patch_dict = create_patches('./C06-27_01.svs', patch_size, 0)
isFile = os.path.isfile('patch.pkl')
print(isFile)
if (isFile):
    patch_dict = pickle.load(open('patch.pkl', 'rb'))
else:
    patch_dict = create_patches(sl_name, patch_size, 0)
    with open('patch.pkl', 'wb') as f:
        pickle.dump(patch_dict, f)

transferlist = staintransfer(target, patch_dict)

new_dict = {key: value for (key, value) in zip(
    patch_dict.keys(), transferlist)}

# print(new_dict)
reconstruct(slide,  new_dict)
