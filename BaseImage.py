
import validation_util 
from PIL import Image 

class BaseImage:

    def __init__(self, filename):
        self.name = filename 
        self.img = self._get_img(filename)

    def _get_img(self, filename): 
        with Image.open(filename) as im:
            im.load()  ## PIL can be "lazy" so need to explicitly load image 
            return im 

    def get_avg_color(self, region):
        width, height = region.size 
        rgb_pixels = region.getcolors(width * height)
        r_total = g_total = b_total = 0 
        for count, rgb in rgb_pixels:
            r_total, g_total, b_total = r_total + rgb[0], g_total + rgb[1], b_total + rgb[2] 
        r_avg, g_avg, b_avg = r_total / len(rgb_pixels), g_total / len(rgb_pixels), b_total / len(rgb_pixels) 
        return (round(r_avg), round(g_avg), round(b_avg)) 


