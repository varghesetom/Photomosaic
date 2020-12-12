#!/usr/bin/env python

"""
The main driver -- a mosaic is created for an input image based on
source images that will be processed in the SourceImageProcessor file.
The input image is divided into squares of 25 x 25 size and are
calculated for their average color. Calculating the average color
for a boxed region means getting 3 total counts of R, G, and B
colored pixels and dividing by the overall total number of pixels.
Next, we match that average color for a specific box with one of
the source images, which also have a corresponding average color.
Because we are looking for the "closest" match for a 3-valued tuple,
we can use Euclidean distance. But this can take a long time if
we have many source images and we have a large input image with
many regional boxes because we'd have to find the closest match by
going through all the images for each box. We can instead utilize an
index to match an input img color-tuple to see which source images
are the closest match. A rough hashing is done where the keys are
the color-tuples where each value in the color-tuple is rounded
to the nearest ten. The values in this dictionary-index are lists
of source images. We can then round the current input
region color-tuple to the nearest ten for R, G, and B and try to index it.
If it doesn't exist, then we search all the source images.

This means that an index would be more useful when the number of source
images are extremely high so that we can more likely find a key match.
If there are many misses, then our set of source images isn't large and we
can justify just iterating the entire set.
"""


# from utils import validation_util
from utils.helpers import round_to_nearest_10
from PIL import Image
from BaseImage import BaseImage
from SourceImageProcessor import SourceImageProcessor
from collections import defaultdict

import sys
import math

#log = open("log.txt", "w+") 


class PhotoMosaic(BaseImage):

    # @validation_util.validate_input_is_image
    # @validation_util.validate_img_dir
    def __init__(self, filename=None, directory=None, piece_width=25,
                 piece_height=25):
        # if filename is None:
        #     raise NameError('Error')
        #     filename = sys.argv[1]
        # else:   ## used only for testing -- the client should still pass in a CLI image arg
        # self.img = filename
        super().__init__(filename)
        self.directory = directory

        self.piece_width = piece_width
        self.piece_height = piece_height
        self.palette = self.img.convert('P', palette=Image.ADAPTIVE, colors=16)
        self.regions_with_colors = self.get_avg_color_for_regions()

    def get_avg_color_for_regions(self):
        """Determine the average color for each box region of the input image."""
        return {box: self.get_avg_color(self.img.crop(box)) for box in self.divvy_into_box_regions()}

    def divvy_into_box_regions(self): 
        """Helper to crop image into W*L boxes."""

        width, height = self.img.size 
        regions = [self.calculate_box_region(i, j) for i in range(width // self.piece_width)
                   for j in range(height // self.piece_height)]
        self.create_trimmed_mosaic_base() 
        return regions 

    def calculate_box_region(self, width, height):
        left = width * self.piece_width 
        top = height * self.piece_height 
        right = left + self.piece_width 
        bottom = top + self.piece_height 
        return (left, top, right, bottom)

    def create_mosaic(self):
        '''
        instantiate a SourceImageProcessor and read in the json_data of
        thumbnails and average color tuples. We create an index and then
        start matching input image regions to the source image json. 
        Once we find the closest match, we can then directly paste the 
        source thumbnail onto the region of the input image 
        '''
        mosaic = self.create_trimmed_mosaic_base() 
        size = (self.piece_width, self.piece_height) 
        s_img_p = SourceImageProcessor(self.directory, (25, 25))
        json_data = s_img_p.read_source_avg_colors()[0]  ## calling in src img thumbnails via JSON dict
        json_index = self.get_index(json_data) 
        try: 
            for region, region_color in self.regions_with_colors.items():
                #log.write(f"REGION: {region}, REGION_COLOR: {region_color}") 
                source_img_match = self.find_closest_match_with_index(region_color, json_index)  
                #log.write(f"index result for {region_color}, {source_img_match}")
                if not source_img_match: 
                    #log.write(f"\nNeed to go through entire set of imgs for this color here {region_color}\n") 
                    source_img_match = self.euclidean_match_with_json_data(region_color, json_data) 
                thumbnail_img = Image.open(source_img_match["image_match"]) 
                upper_left = (region[0], region[1]) 
                img_mask = thumbnail_img.convert("RGBA") 
                mosaic.paste(thumbnail_img, upper_left) 
            print("saving mosaic") 
            mosaic.save(f"mosaic_{self.name[:-4]}_{s_img_p.img_dir}.png") 
        except ValueError as v:
            print(f"Unexpected error came up after trying to use stored img dir to save mosaic: {v}") 
            sys.exit(1) 

    def create_trimmed_mosaic_base(self):
        """Uneven input images will result in the sides of the image not
        being properly handled during matching because our regions are 
        25 x 25 size. Much easier to simply trim the sides and ensure 
        all regions are accounted for 
        """
        mosaic = self.img.copy() 
        width, height = self.img.size 
        count, rem = divmod(width, self.piece_width)
        mosaic_width = self.piece_width * count 
        count, rem = divmod(height, self.piece_height) 
        mosaic_height = self.piece_height * count 
        return mosaic.crop((0, 0, mosaic_width, mosaic_height)) 

    def get_index(self, json_data):
        index = defaultdict(list)  
        for name, color in json_data.items(): 
            new_c1, new_c2, new_c3 = round_to_nearest_10(color[0]), round_to_nearest_10(color[1]), round_to_nearest_10(color[2]) 
            index[(new_c1, new_c2, new_c3)].append((name, color)) 
        return index 

    def find_closest_match_with_index(self, region_color, index):
        translated = (round_to_nearest_10(region_color[0]), round_to_nearest_10(region_color[1]), round_to_nearest_10(region_color[2]))
        if translated in index:
            source_imgs = index[translated] 
            min_dist = sys.maxsize 
            result = {"image_match": 0}
            for name, color in source_imgs:
                dist = self.calculate_euclidean_dist(region_color, color) 
                if dist < min_dist:
                    min_dist = dist 
                    result["image_match"] = name 
            #log.write(f"Returning index result\n") 
            return result 

    def euclidean_match_with_json_data(self, region_color, source_img_data):
        """ Euclidean distance matching with the json dict. This only occurs if
        we couldn't get a match with the index. 
        """
        min_dist = sys.maxsize 
        result = {'image_match': 0}
        for name, color in source_img_data.items():
            dist = self.calculate_euclidean_dist(region_color, color) 
            #log.write(f"Name: {name}, Color: {color}, dist: {dist}\n")
            if dist < min_dist: 
                #log.write(f"MIN DIST: Name: {name}, Dist: {dist}\n") 
                min_dist = dist 
                result['image_match'] = name
        return result 

    def calculate_euclidean_dist(self, rgb_tup1, rgb_tup2):
        return math.sqrt(sum([(a - b)**2 for a, b in zip(rgb_tup1, rgb_tup2)]))
