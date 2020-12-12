#!/usr/bin/env python

"""
Here we abstract away from "Photomosaic.py" all the preprocessing we need
to do for the source images. Some similarities exist such as calculating
the average color. But whereas the input image was divided into boxes
and had a corresponding average color calculation, here each source image
is converted into a standardized thumbnail before calculating the average
color for the entire thumbnail. In other words, a 1:1 correspondence
between a source image and a specific color-tuple.
The other functionalities are specific to user handling. The program will create
an "img_sets/[IMG_DIR]" directory to store the img_set and a corresponding
JSON file of thumbnails in "img_sets/img_jsons/[IMG_DIR]". Having a JSON makes
it easier to directly read in all the thumbnails and their average colors
instead of calculating them all over again.
"""

from BaseImage import BaseImage
from utils import helpers

import os
import subprocess 
import json 
import re


class SourceImageProcessor(object):

    def __init__(self, img_dir, size=(50, 50)):
        self.is_from_img_sets = False 
        self.img_dir = self.img_dir_name_cleaned(img_dir) 
        self.size = size 

    def img_dir_name_cleaned(self, img_dir):
        """User could provide image directory from same file location or use one
        from the "img_sets". If it's the latter, then need to trim out the leading
        'img_set' verbiage before continuing.
        """
        if re.search(r'img_sets', img_dir): 
            base_img_dir = re.sub("img_sets/", "", img_dir)  
            self.is_from_img_sets = True 
        else:
            base_img_dir = img_dir 
        return base_img_dir 

    def read_source_avg_colors(self): 
        """Read from an existing JSON file else we create
        the source image subdirectory and start the
        calculation process to store them to JSON.
        """
        contents = self.read_from_existing_JSON_file() 
        if not contents: 
            print(f"JSON file provided does not exist. Running program to save "
                  f"avg_color results to JSON file as "
                  f"'img_sets/img_jsons/{self.img_dir}.json' and "
                  f"re-trying to read JSON contents.")
            self.create_img_subdirs() 
            self.save_avg_colors_to_JSON() 
            return self.read_JSON_contents()
        return contents 

    def read_from_existing_JSON_file(self):
        """Cannot read from a JSON if it and its thumbnails don't exist"""

        loc1 = f"img_sets/img_jsons/" + self.img_dir + ".txt" 
        if os.path.isfile(loc1) and self.check_if_JSON_corresponding_thumbnails():  
            print("Using existing JSON and thumbnails to construct mosaic") 
            return self.read_JSON_contents() 
        return False 

    def check_if_JSON_corresponding_thumbnails(self):
        thumbnail_path = f"img_sets/{self.img_dir}/thumbnails" 
        return False if not os.path.exists(thumbnail_path) or not os.listdir(thumbnail_path) else True

    def read_JSON_contents(self):
        loc1 = f"img_sets/img_jsons/" + self.img_dir + ".txt" 
        try: 
            with open(loc1, 'r') as json_file:
                return json.load(json_file) 
        except ValueError: 
            print("Decoding JSON has failed. Exiting...")
            return False 
        except FileNotFoundError:
            print("JSON file is not found. Exiting...") 
            return False 
    
    def create_img_subdirs(self):
        if not os.path.exists(f"img_sets/{self.img_dir}"):
            p = subprocess.Popen(f"mkdir img_sets/{self.img_dir}", shell = True) 
            p.wait() 
        if not os.path.exists(f"img_sets/{self.img_dir}/thumbnails"):
            p = subprocess.Popen(f"mkdir img_sets/{self.img_dir}/thumbnails/", shell = True) 
            p.wait() 

    def save_avg_colors_to_JSON(self):
        source_img_dict = [self.collect_avg_colors_for_source_imgs()]
        with open(f"img_sets/img_jsons/{self.img_dir}" + ".txt", "w") as out:
            json.dump(source_img_dict, out) 

    def collect_avg_colors_for_source_imgs(self):
        """For each thumbnail of the source image, we calculate its average color
        and store it into a dict that will be saved as a JSON file."""
        trimmed_thumbnails = self.standardize_source_images()
        source_img_dict = {} 
        for img_class, img in trimmed_thumbnails.items():
            if img_class.name not in source_img_dict: 
                try: 
                    source_img_dict[img_class.name] = img_class.get_avg_color(img)
                except TypeError:
                    pass 
        return source_img_dict

    def standardize_source_images(self): 
        '''
        Easier to have "square" thumbnails to work with in PIL. 
        '''
        output = {}
        for img_class in self.get_images_from_img_dir(): 
            thumbnail_name = f"img_sets/{self.img_dir}/thumbnails/" + self.trim_name(img_class) + "_thumbnail.jpg"
            width, height = img_class.img.size 
            trimmed_img = img_class.img 
            trimmed_img = helpers.trim_width(img_class.img, width, height)  
            trimmed_img = helpers.trim_height(img_class.img, width, height)  
            thumbnail = trimmed_img.thumbnail(self.size)  
            if not os.path.exists(f"{thumbnail_name}.png"):
                trimmed_img.save(thumbnail_name, "png")   ## the trimmed thumbnail will be used for our img
            output[BaseImage(thumbnail_name)] = trimmed_img 
        return output 

    def get_images_from_img_dir(self):
        """Ignore any non-images when searching the source image dir."""
        search_dir = self.img_dir 
        if self.is_from_img_sets: 
            search_dir = f"img_sets/{self.img_dir}" 
        for fn in os.listdir(search_dir):
            if fn.endswith(".jpg") or fn.endswith(".png") or fn.endswith(".jpeg"): 
                yield BaseImage(search_dir + "/" + fn) 

    def trim_name(self, img_class):
        replacements = [(self.img_dir, ""), ("/", ""), ("img_sets", "")] 
        new_name = img_class.name
        for old, new in replacements:
            new_name = re.sub(old, new, new_name) 
        return new_name 
