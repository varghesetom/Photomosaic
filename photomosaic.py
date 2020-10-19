#!/usr/bin/env python

import sys 
import os 
from PIL import Image 
import functools 
import validation_util 

class PhotoMosaic:

    def __init__(self, filename = None):
        if filename is None: 
            filename = sys.argv[1] 
        self.img = self._get_img(filename)
        self.name = filename 
        self.piece_width = 50 
        self.piece_height = 50 
        self.palette = self.img.convert('P', palette=Image.ADAPTIVE, colors=16)
        self.region_colors = self.get_avg_color_for_regions()

    @validation_util.validate_input_is_image
    def _get_img(self, filename): 
        with Image.open(filename) as im:
            im.load()  ## PIL can be "lazy" so need to explicitly load image 
            return im 

    def get_avg_color_for_regions(self):
        box_regions = self.divvy_into_box_regions() 
        region_colors = [self.get_avg_color(self.img.crop(box)) for box in box_regions]
        return region_colors 

    def divvy_into_box_regions(self): 
        width, height = self.img.size 
        regions = [] 
        for i in range(width // self.piece_width):
            for j in range(height // self.piece_height):
                regions.append(self.calculate_box_region(i, j))
        return regions 

    def calculate_box_region(self, width, height):
        return (width * self.piece_width, height * self.piece_height, (width * self.piece_width) + self.piece_width, (height * self.piece_height) + self.piece_height)

    def get_avg_color(self, region):
        width, height = region.size 
        rgb_pixels = region.getcolors(width * height)
        r_total = g_total = b_total = 0 
        for count, rgb in rgb_pixels:
            r_total, g_total, b_total = r_total + rgb[0], g_total + rgb[1], b_total + rgb[2] 
        r_avg, g_avg, b_avg = r_total / len(rgb_pixels), g_total / len(rgb_pixels), b_total / len(rgb_pixels) 
        return (round(r_avg), round(g_avg), round(b_avg)) 

    def create_new_img(self):
        width, height = self.img.size 
        new_width, new_height = width // self.piece_width, height // self.piece_height 
        assert new_width * new_height == len(self.region_colors), "New image must be equal to dimension of array containing colors for all the broken up pieces of original" 
        im = Image.new("RGBA", (new_width, new_height)) 
        counter = 0  
        for i in range(width // self.piece_width):
            for j in range(height // self.piece_height):
                im.putpixel((i, j), self.region_colors[counter]) 
                counter += 1 
        im.save(f"new_img.png") 



if __name__ == "__main__":
    pm = PhotoMosaic()
    #print(pm.region_colors, len(pm.region_colors))
    #print(pm.img.size)
    #pm.create_new_img()


