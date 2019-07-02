from create_patches import create_patches
from reconstruct import reconstruct
from staintransfer import staintransfer
from openslide import open_slide

import pickle
import os

# ref: https://stackoverflow.com/questions/9816816/get-absolute-paths-of-all-files-in-a-directory
patch_size = 1000


def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


ee_list = [path for path in absoluteFilePaths('./data/temp')]

target_slname = './data/target/N14-02_02.svs'

target_slide = open_slide(target_slname)
x, y = target_slide.dimensions


target = target_slide.read_region((x//2, y//2), 0, (patch_size, patch_size))

for svs_img in ee_list:
    slide = open_slide(svs_img)
    patch_dict = create_patches(svs_img, patch_size, 0)
    transferlist = staintransfer(target, patch_dict)

    new_dict = {key: value for (key, value) in zip(
        patch_dict.keys(), transferlist)}
    reconstruct(slide,  new_dict)
