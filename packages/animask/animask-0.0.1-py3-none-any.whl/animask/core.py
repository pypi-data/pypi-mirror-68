"""Core of animask"""
import numpy as np
import cv2
import imageio
from pygifsicle import optimize

from .utils import read_image, convert_to_rgb, replace_color


class _BaseAnimask:
    __name__ = "Animask object"

    def __init__(self, image, bg_beta=0.5, mask_color=None):
        """
        Create instance.
        Arguments:
            image {str|np.ndarray} -- image or path to image
        Keyword Arguments:
            bg_beta {float} -- mask opacity (default: {0.5})
            mask_color {tuple} -- RGB mask color in animation (default: {None})
        """
        if bg_beta < 0.0 or bg_beta > 1.0:
            raise ValueError("'bg_beta' must be from (0; 1)")
        if mask_color is not None:
            if len(mask_color) != 3:
                raise ValueError("'mask_color' must be a tuple and has format (R, G, B)")
        if isinstance(image, str):
            image = read_image(image)
        self.image = np.asarray(image, dtype=np.uint8)
        self.bg_beta = bg_beta
        self.mask_color = mask_color
        self.masks = list()
        self.titles = list()

    def add(self, mask):
        raise NotImplementedError()

    def save(self, filename):
        raise NotImplementedError()

    @property
    def mask_size(self):
        return self.image.shape[:2]

    @property
    def counter(self):
        return len(self.masks)

    @property
    def masks_with_background(self):
        raise NotImplementedError()

    def __repr__(self):
        return "<{0} with {1} layers>".format(self.__name__, self.counter)


class Animask(_BaseAnimask):
    """
    Base class for animask.
    """

    @property
    def masks_with_background(self):
        """image + masks"""
        layers = list()
        for mask in self.masks:
            mask = convert_to_rgb(mask)
            mask = replace_color(mask, self.mask_color)
            layer = cv2.addWeighted(src1=self.image,
                                    alpha=1.0 - self.bg_beta,
                                    src2=mask,
                                    beta=self.bg_beta,
                                    gamma=0)
            layers.append(layer)
        return layers

    def _add_titles(self, layers):
        """
        Add titles for all layers.
        """
        if len(layers) != len(self.titles):
            raise ValueError()
        for i, layer in enumerate(layers):
            layers[i] = cv2.putText(img=layer,
                                    text=self.titles[i],
                                    org=(25, 25),
                                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                                    fontScale=2,
                                    color=(150, 0, 0),
                                    thickness=2,
                                    lineType=cv2.LINE_AA)
        return layers

    def add(self, mask, desc=None):
        """
        Call this method every epoch to add predicted mask.
        Arguments:
            mask {np.ndarray} -- predicted mask for original image
        Keyword Arguments:
            desc {str} -- description of current epoch; 'epoch [N]' if None (default: {None})
        """
        if mask.max() <= 1:
            mask = mask * 255
        mask = np.asarray(mask, dtype=np.uint8)
        mask = cv2.resize(mask, self.mask_size)
        if desc is None:
            epoch = str(self.counter + 1)
            desc = "epoch {0}".format(epoch)
        self.masks.append(mask)
        self.titles.append(str(desc))

    def save(self, filepath, duration=0.5, with_background=False, with_annots=True):
        """
        Save GIF for current animask state.
        Call this method no more than once per epoch.
        Arguments:
            filepath {str} -- path where to save GIF
        Keyword Arguments:
            duration {float} -- seconds to show one epoch (default: {0.5})
            with_background {bool} -- show background under mask (default: {False})
            with_annots {bool} -- show titles (default: {True})
        """
        layers = self.masks
        if with_background:
            layers = self.masks_with_background
        if with_annots:
            layers = self._add_titles(layers)
        imageio.mimsave(filepath, layers, duration=duration)
        optimize(filepath)
