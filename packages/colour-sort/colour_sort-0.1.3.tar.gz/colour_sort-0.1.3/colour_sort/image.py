import enum
from functools import partial

import numpy as np
from PIL import Image, ImageCms
from colour_sort import sort_type, sort

try:
    import importlib.resource as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

IMAGE_SIZE = 4096
TOTAL_PIXELS = IMAGE_SIZE*IMAGE_SIZE

def _reshape_image(image):
    new_width, new_height = IMAGE_SIZE, IMAGE_SIZE

    thumb = image.resize((new_width, new_height))
    return np.reshape(np.array(thumb), (TOTAL_PIXELS, 3))

def _rgb_to_lab(image):
    # Convert the image to LAB colour space - https://stackoverflow.com/a/53353542
    srgb_p = ImageCms.createProfile("sRGB")
    lab_p  = ImageCms.createProfile("LAB")

    rgb2lab = ImageCms.buildTransformFromOpenProfiles(srgb_p, lab_p, "RGB", "LAB")
    return ImageCms.applyTransform(image, rgb2lab)

def _sort_map(src: np.ndarray, mapped: np.ndarray, order = None) -> np.ndarray:
    if order is not None:
        mapping = np.argsort(src)
    else:
        mapping = np.argsort(src, order=order)
    reverse_mapping = np.argsort(mapping)

    return mapped[reverse_mapping]

def _generate_all_colours():
    with pkg_resources.open_binary('colour_sort', 'all.npy') as colours:
        return np.load(colours)

def sorted_image(image: np.array, map_func, mode=sort_type.SortType.RGB):
    result = _generate_all_colours()

    criteria_image, criteria_result = map_func(image, result)
    results_sorted = result[np.argsort(criteria_result)]

    mapped = _sort_map(criteria_image, results_sorted)
    return Image.fromarray(np.reshape(mapped, (IMAGE_SIZE, IMAGE_SIZE, 3)), mode=mode)

def create_sorted_image(image: Image.Image, mode: sort_type.SortType) -> Image.Image:
    image = image.convert('RGB')
    result_mode = 'RGB'

    if mode is sort_type.SortType.BRIGHTNESS:
        image = _rgb_to_lab(image)
        map_func = sort.sort_brightness
        result_mode = 'LAB'
    elif mode is sort_type.SortType.AVG:
        map_func = sort.sort_avg
    else:
        map_func = partial(sort.sort_rgb, mode)

    reshaped = _reshape_image(image)
    return sorted_image(reshaped, map_func, result_mode)
