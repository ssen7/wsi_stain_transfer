import staintools
import pickle
import cv2 as cv
import numpy as np
from PIL import Image
from keep_tile import keep_tile
import warnings

# np.seterr(all='warn')

# warnings.filterwarnings('error')


def staintransfer(target, patch_dict):
    '''
    ref: https://github.com/Peter554/StainTools

    Used staintools python package and vahadane method
    '''
    print("Transferring target stain to image patches...")
    target = target.convert('RGB')
    target = np.array(target)  # convert to opencv RGB
    target = staintools.LuminosityStandardizer.standardize(
        target)  # standardize brightness

    # Stain normalize
    normalizer = staintools.StainNormalizer(method='vahadane')
    normalizer.fit(target)

    transformed_list = []
    for key, image in patch_dict.items():
        image = image.convert('RGB')
        image = np.array(image)  # convert to opencv RGB
        try:
            image = staintools.LuminosityStandardizer.standardize(
                image)  # standardize brightness
            image_gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
            if np.mean(image_gray) >= 249.0:  # skip mostly white images
                transformed = image
            # check if image has tissues (removed pink patches)
            if not keep_tile(image, 0.05):
                transformed = image
            else:

                transformed = normalizer.transform(image)
                # if transformed image is black,replace with original image
                if np.mean(transformed) == 0.0:
                    transformed = image

        except staintools.miscellaneous.exceptions.TissueMaskException:
            print('Exception: ' + key)
            transformed_list.append(Image.fromarray(image))
            continue

        transformed_list.append(Image.fromarray(transformed))

    return transformed_list
