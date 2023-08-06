"""Utilities"""
import numpy as np
import cv2


def read_image(filepath):
    """
    Just read image as RGB
    """
    image = cv2.imread(filepath)
    if image is None:
        raise ValueError("Can't read 'image', there is no such path!")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def convert_to_rgb(mask):
    if len(mask.shape) == 2:
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    return mask

def replace_color(mask, color):
    if color:
        indices = np.where(mask != (0, 0, 0))
        mask[indices[0], indices[1], :] = color
    return mask
