from create_patches import create_patches
from reconstruct import reconstruct
from staintransfer import staintransfer
from openslide import open_slide

import pickle
import os

target_slname = '../../research/data/target/N14-02_02.svs'
sl_name = '../../research/data/ee_pak/16_002.svs'
save_dir = '../../research/converted/'

target_slide = open_slide(target_slname)
slide = open_slide(sl_name)

x, y = target_slide.dimensions

patch_size = 1000
target = target_slide.read_region((x//2, y//2), 0, (patch_size, patch_size))

# patch_dict = create_patches('./C06-27_01.svs', patch_size, 0)
# save patches as pickle files to test without creating patches everytime
pkl_name = sl_name.split('/')[-1].split('.')[0] + '.pkl'
isFile = os.path.isfile(pkl_name)
print(isFile)
if (isFile):
    patch_dict = pickle.load(open(pkl_name, 'rb'))
else:
    patch_dict = create_patches(sl_name, patch_size, 0)
    with open(pkl_name, 'wb') as f:
        pickle.dump(patch_dict, f)

transferlist = staintransfer(target, patch_dict)

new_dict = {key: value for (key, value) in zip(
    patch_dict.keys(), transferlist)}

# print(new_dict)
reconstruct(slide,  new_dict, save_dir)
