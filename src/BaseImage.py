"""
Initializing image arguments into true PIL.Image classes. "get_avg_color"
is also placed here because this method is closely related to PIL.Images
and should only be used in relation to the BaseImage. In the program,
this method is used to calculate the average color for each square of
the base image.
"""

from PIL import Image

import sys
import pathlib


class BaseImage(object):

    def __init__(self, filename):
        self.name = filename
        self.img = self._get_img(filename)

    def _get_img(self, filename):

        try:
            with Image.open(filename) as im:
                im.load()  # PIL can be "lazy" so need to explicitly load image
                return im
        except OSError:
            # Check if the file does in fact exist

            # Check if the python version is 3.6 or greater
            if sys.version_info[1] >= 6:
                if pathlib.Path(filename).resolve(strict=True):
                    pass
                else:
                    raise FileNotFoundError
            else:
                if pathlib.Path(filename).resolve():
                    pass
                else:
                    raise FileNotFoundError

    def get_avg_color(self, region):
        """Given a region in a PIL Image, return average value of
           color as (r, g, b).

           Args:
                 region: region of interest

            Returns:
                a tuple with the average color values for r, g, b
        """
        width, height = region.size
        rgb_pixels = region.getcolors(width * height)
        sum_rgb = [(x[1][0], x[1][1], x[1][2]) for x in rgb_pixels]
        return tuple([sum(x)/len(rgb_pixels) for x in zip(*sum_rgb)])
