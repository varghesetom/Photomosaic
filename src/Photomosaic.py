#!/usr/bin/env python
"""In this script, a mosaic is created based on an input image."""

import sys
import math

from PIL import Image
from collections import defaultdict

from BaseImage import BaseImage
from SourceImageProcessor import SourceImageProcessor
from utils.helpers import round_to_nearest_10, Logger
from utils.validation_util import validate_directory, validate_json_data


class PhotoMosaic(BaseImage):
    """PhotoMosaic creates a mosaic for an input image based on source images,
       which are preprocessed in the SourceImageProcessor file. The input
       image is divided into squares of 25 x 25 size and each square is
       calculated for its average color. Calculating the average color for a
       boxed region means getting 3 total counts of R, G, and B colored
       pixels and dividing by the overall total number of pixels. Next,
       a match is performed between the average color for a specific box
       with one of the source images--which also have a corresponding
       average color--and the squares. To look for the "closest" match for a
       3-valued tuple, the Euclidean distance is implemented. In an effort
       to optimize runtime, an index is utilized to match an input
       img color-tuple to see which source images are the closest match.
       A rough hashing is done where the keys are the color-tuples, and
       each value in the color-tuple is rounded to the nearest tens digit.
       The values in this dictionary-index are lists of source images.

       We can then round the current input region color-tuple to the nearest
       tens digit for R, G, and B and try to index it. If it doesn't exist,
       then we search all the source images.

       Attributes:
           filename: (string) file name: Default None.
           directory: (string) image directory. Default: None
           piece_width: (int) the width of the box region
           piece_height: (int) the height of the box region
           palette: (PIL.image type)
           debug: (boolean) Starts logger as a debugger tool. Default: False

    """

    @validate_directory
    def __init__(self, filename=None, directory=None, piece_width=25,
                 piece_height=25, debug=False):
        """Initializes PhotoMosaic with filename, directory, piece_width size
           and piece_height size."""
        super().__init__(filename)
        self.directory = directory

        self.piece_width = piece_width
        self.piece_height = piece_height
        self.palette = self.img.convert('P', palette=Image.ADAPTIVE, colors=16)
        self.regions_with_colors = self.get_avg_color_for_regions()

        # Logger
        self.the_logger = None if not debug else Logger(log_file_name='test_log_1.log')
        self.turn_logger_on = False if self.the_logger is None else True

    def get_avg_color_for_regions(self):
        """Determine the average color for each box region of the input image."""
        return {box: self.get_avg_color(self.img.crop(box)) for box in self.divvy_into_box_regions()}

    def divvy_into_box_regions(self): 
        """Crops image into width x height boxes."""
        width, height = self.img.size 
        regions = [self.calculate_box_region(i, j) for i in range(width // self.piece_width)
                   for j in range(height // self.piece_height)]
        self.create_trimmed_mosaic_base() 
        return regions 

    def calculate_box_region(self, width, height):
        """Calculates the box region to crop image.

           Args:
               width: (int) specified width of box region
               height: (int) specified height of box region
        """

        left = width * self.piece_width 
        top = height * self.piece_height 
        right = left + self.piece_width 
        bottom = top + self.piece_height 
        return left, top, right, bottom

    def create_mosaic(self):
        """Instantiates a SourceImageProcessor and reads in the JSON data of
           the thumbnails and average color tuples. Next, an index is created
           to start matching input image regions to the source image JSON.
           Once a closet match is found, then the source thumbnail is directly
           pasted onto the region of the input image.
        """

        mosaic = self.create_trimmed_mosaic_base()
        s_img_p = SourceImageProcessor(self.directory, (25, 25))

        # Calling in source image thumbnails via JSON dictionary
        json_data = s_img_p.read_source_avg_colors()[0]

        json_index = self.get_index(json_data)
        try: 
            for region, region_color in self.regions_with_colors.items():

                if self.turn_logger_on:
                    # Logs message
                    self.the_logger.log_message(f"REGION: {region}, REGION_COLOR: {region_color}")

                source_img_match = self.find_closest_match_with_index(region_color, json_index)

                if self.turn_logger_on:
                    self.the_logger.log_message(f"index result for {region_color}, {source_img_match}")

                if not source_img_match:
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
        all regions are accounted for.
        """

        mosaic = self.img.copy()
        width, height = self.img.size
        count, rem = divmod(width, self.piece_width)
        mosaic_width = self.piece_width * count
        count, rem = divmod(height, self.piece_height)
        mosaic_height = self.piece_height * count
        return mosaic.crop((0, 0, mosaic_width, mosaic_height))

    @staticmethod
    def get_index(json_data):
        """For each thumbnail picture in the JSON data dictionary, retrieve
           the original pixel values and round up or down depending on the
           value. Save this new tuple into the index dictionary."""

        index = defaultdict(list)
        if validate_json_data(json_data):
            for name, color in json_data.items():
                *new_color, = map(round_to_nearest_10, color)
                index[tuple(new_color)].append((name, color))
            return index

    def find_closest_match_with_index(self, region_color, index):
        *translated, = map(round_to_nearest_10, region_color)
        if tuple(translated) in index:
            source_images = index.get(tuple(translated))
            min_dist = sys.maxsize
            result = {"image_match": 0}
            for name, color in source_images:
                dist = self.calculate_euclidean_dist(region_color, color)
                if dist < min_dist:
                    min_dist = dist
                    result["image_match"] = name
            return result

    def euclidean_match_with_json_data(self, region_color, source_img_data):
        """Euclidean distance matching with the JSON dictionary. This only
           occurs if there was not a match with the index.
        """

        min_dist = sys.maxsize
        result = {'image_match': 0}
        for name, color in source_img_data.items():
            dist = self.calculate_euclidean_dist(region_color, color)
            if dist < min_dist:
                min_dist = dist
                result['image_match'] = name
        return result

    @staticmethod
    def calculate_euclidean_dist(rgb_tup1, rgb_tup2):
        return math.sqrt(sum([(a - b)**2 for a, b in zip(rgb_tup1, rgb_tup2)]))
