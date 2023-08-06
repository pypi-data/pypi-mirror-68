import numpy as np
from colour_sort import sort_type

# image needs to be in LAB colour space
def sort_brightness(image: np.ndarray, result: np.ndarray):
    return image[:,0], result[:,0]


def sort_avg(image: np.ndarray, result: np.ndarray):
    return np.sum(image, axis=1), np.sum(result, axis=1)


def sort_rgb(mode: sort_type.SortType, image: np.ndarray, result: np.ndarray):
    if sort_type.is_clip(mode):
        # Originally this was a bug, since this allows the results of the left shifts to overflow
        # but I'm keeping it because I like the images it results in
        res_r, res_g, res_b = result.transpose()
        src_r, src_g, src_b = image.transpose()
    else:
        res_r, res_g, res_b = result.astype(np.uint32).transpose()
        src_r, src_g, src_b = image.astype(np.uint32).transpose()

    mode = sort_type.unclip(mode)

    # TODO better logic
    if mode is sort_type.SortType.RGB:
        combined_res = (res_r << 16) | (res_g << 8) | res_b
        combined_src = (src_r << 16) | (src_g << 8) | src_b
    elif mode is sort_type.SortType.RBG:
        combined_res = (res_r << 16) | (res_b << 8) | res_g
        combined_src = (src_r << 16) | (src_b << 8) | src_g
    elif mode is sort_type.SortType.BRG:
        combined_res = (res_b << 16) | (res_r << 8) | res_g
        combined_src = (src_b << 16) | (src_r << 8) | src_g
    elif mode is sort_type.SortType.BGR:
        combined_res = (res_b << 16) | (res_g << 8) | res_r
        combined_src = (src_b << 16) | (src_g << 8) | src_r
    elif mode is sort_type.SortType.GBR:
        combined_res = (res_g << 16) | (res_b << 8) | res_r
        combined_src = (src_g << 16) | (src_b << 8) | src_r
    elif mode is sort_type.SortType.GRB:
        combined_res = (res_g << 16) | (res_r << 8) | res_b
        combined_src = (src_g << 16) | (src_r << 8) | src_b

    return combined_src, combined_res
