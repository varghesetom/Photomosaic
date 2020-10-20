#!/usr/bin/env python

import sys 
import os 
import math 
import functools 
import validation_util 
import source_img_utils 
from PIL import Image 
from BaseImage import BaseImage

#log = open("log.txt", "w+") 

class PhotoMosaic(BaseImage):

    @validation_util.validate_input_is_image 
    def __init__(self, filename = None, piece_width=25, piece_height=25):
        if filename is None: 
            filename = sys.argv[1] 
        super().__init__(filename) 
        self.piece_width = piece_width
        self.piece_height = piece_height
        self.palette = self.img.convert('P', palette=Image.ADAPTIVE, colors=16)
        self.regions_with_colors = self.get_avg_color_for_regions()

    def get_avg_color_for_regions(self):
        return {box : self.get_avg_color(self.img.crop(box)) for box in self.divvy_into_box_regions()}

    def divvy_into_box_regions(self): 
        width, height = self.img.size 
        regions = [] 
        for i in range(width // self.piece_width):
            for j in range(height // self.piece_height):
                regions.append(self.calculate_box_region(i, j))
        return regions 

    def calculate_box_region(self, width, height):
        return (width * self.piece_width, height * self.piece_height, (width * self.piece_width) + self.piece_width, (height * self.piece_height) + self.piece_height)

    def create_mosaic(self):
        mosaic = self.img.copy() 
        size = (self.piece_width, self.piece_height) 
        source_img_data = source_img_utils.read_source_avg_colors(size=size)[0]  ## calling in thumbnail of src imgs 
        for region, region_color in self.regions_with_colors.items():
            #log.write(f"REGION: {region}, REGION_COLOR: {region_color}") 
            source_img_match = self.match_input_region_to_source_imgs(region_color, source_img_data) 
            thumbnail_img = Image.open(source_img_match["image_match"]) 
            upper_left = (region[0], region[1]) 
            img_mask = thumbnail_img.convert("RGBA") 
            mosaic.paste(thumbnail_img, upper_left) 
        mosaic.save("mosaic.png") 

    def match_input_region_to_source_imgs(self, region_color, source_img_data):
        min_dist = sys.maxsize 
        result = {'image_match' : 0}
        for name, color in source_img_data.items():
            dist = self.calculate_euclidean_dist(region_color, color) 
            #log.write(f"Name: {name}, Color: {color}, dist: {dist}\n")
            if dist < min_dist: 
                #log.write(f"MIN DIST: Name: {name}, Dist: {dist}\n\n") 
                min_dist = dist 
                result['image_match'] = name
        return result 

    def calculate_euclidean_dist(self, rgb_tup1, rgb_tup2):
        r1, g1, b1 = rgb_tup1 
        r2, g2, b2 = rgb_tup2 
        return  math.sqrt(((r2 - r1) ** 2 + (g1 - g2) ** 2 + (b1 -b2) ** 2))

    def create_pixellation_img(self):
        width, height = self.img.size 
        new_width, new_height = width // self.piece_width, height // self.piece_height 
        assert new_width * new_height == len(self.region_colors), "New image must be equal to dimension of array containing colors for all the broken up pieces of original" 
        im = Image.new("RGBA", (new_width, new_height)) 
        counter = 0  
        for i in range(width // self.piece_width):
            for j in range(height // self.piece_height):
                im.putpixel((i, j), self.region_colors[counter]) 
                counter += 1 
        im.save(f"pixellated.png") 

if __name__ == "__main__":
    pm = PhotoMosaic()
    pm.create_mosaic() 
    #log.close() 


