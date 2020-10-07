#!/usr/bin/env python

import sys 
import os 
from PIL import Image 
import functools 

def validate_input_image(func):
    @functools.wraps(func)
    def validated(*args):
        if len(sys.argv) < 2: 
            raise ValueError("Need image to crop") 
            sys.exit(1)
        result = func(*args)
        return result 
    return validated 

class PhotoMosaic:

    def __init__(self):
        self.img = self.get_img()
        self.palette = self.img.convert('P', palette=Image.ADAPTIVE, colors=16)
        self.region_colors = self.get_avg_color_for_regions()

    @validate_input_image
    def get_img(self):
        with Image.open(sys.argv[1]) as im:
            im.load()  ## PIL can be "lazy" so need to explicitly load image 
            return im 

    def get_avg_color_for_regions(self, piece_width=50, piece_height=50):
        width, height = self.img.size 
        region_colors = [] 
        for i in range(0, width // piece_width):
            for j in range(0, height // piece_height):
               box = (i * piece_width, j * piece_height, (i * piece_width) + piece_width, (j * piece_height) + piece_height)
               #box_coords.append(box) 
               avg_color = self.get_avg_color(self.img.crop(box))
               region_colors.append(avg_color)
        return region_colors 

    def get_avg_color(self, region):
#        width, height = self.img.size 
        width, height = region.size 
        rgb_pixels = region.getcolors(width * height)
        r_total = g_total = b_total = 0 
        for count, rgb in rgb_pixels:
            r_total, g_total, b_total = r_total + rgb[0], g_total + rgb[1], b_total + rgb[2] 
        r_avg, g_avg, b_avg = r_total / len(rgb_pixels), g_total / len(rgb_pixels), b_total / len(rgb_pixels) 
        return (round(r_avg), round(g_avg), round(b_avg)) 


if __name__ == "__main__":
    pm = PhotoMosaic()
    print(pm.most_frequent_color())
    print(pm.region_colors)


