#!/usr/bin/env python

import sys 
import os 
import subprocess 
import json 
import re 
import functools 
import validation_util 
from BaseImage import BaseImage 
from PIL import Image 

class SourceImageProcessor:

    def __init__(self, img_dir, size=(50,50)):
        self.is_from_img_sets = False 
        self.img_dir = self.img_dir_name_cleaned(img_dir) 
        self.size = size 

    def img_dir_name_cleaned(self, img_dir):
        '''
        User could provide image directory from same file location or use one 
        from the "img_sets". If it's the latter, then need to trim out the leading
        'img_set' verbiage before continuing. 
        '''
        if re.search(r'img_sets', img_dir): 
            base_img_dir = re.sub("img_sets/", "", img_dir)  
            self.is_from_img_sets = True 
        else:
            base_img_dir = img_dir 
        return base_img_dir 

    def read_source_avg_colors(self): 
        contents = self.read_from_existing_JSON_file() 
        if not contents: 
            print(f"JSON file provided does not exist. Running program to save avg_color results to JSON file as 'img_sets/img_jsons/{self.img_dir}.json' and re-trying to read JSON contents.") 
            self.create_img_subdirs() 
            self.save_avg_colors_to_JSON() 
            return self.read_JSON_contents()
        return contents 

    def read_from_existing_JSON_file(self):
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
        trimmed_thumbnails = self.standardize_source_images()
        source_img_dict = {} 
        for img_class, img in trimmed_thumbnails.items():
            if img_class.name not in source_img_dict: 
                try: 
                    source_img_dict[img_class.name] = img_class.get_avg_color(img) ## .getcolors() might not return a 4-color tuple 
                except TypeError:
                    pass 
        return source_img_dict

    def standardize_source_images(self): 
        output = {}
        for img_class in self.get_images_from_img_dir(): 
            thumbnail_name = f"img_sets/{self.img_dir}/thumbnails/" + self.trim_name(img_class) + "_thumbnail.jpg"
            width, height = img_class.img.size 
            trimmed_img = img_class.img 
            trimmed_img = trim_width(img_class.img, width, height)  
            trimmed_img = trim_height(img_class.img, width, height)  
            thumbnail = trimmed_img.thumbnail(self.size)  
            if not os.path.exists(f"{thumbnail_name}.png"):
                trimmed_img.save(thumbnail_name, "png")   ## the trimmed thumbnail will be used for our img
            output[BaseImage(thumbnail_name)] = trimmed_img 
        return output 

    def get_images_from_img_dir(self):
        search_dir = self.img_dir 
        if self.is_from_img_sets: 
            search_dir = f"img_sets/{self.img_dir}" 
        for fn in os.listdir(search_dir):
            if fn.endswith(".jpg") or fn.endswith(".png"): 
                yield BaseImage(search_dir + "/" + fn) 

    def trim_name(self, img_class):
        replacements = [(self.img_dir, ""), ("/", ""), ("img_sets", "")] 
        new_name = img_class.name
        for old, new in replacements:
            new_name = re.sub(old, new, new_name) 
        return new_name 

def trim_width(img, width, height):
    if width <= height: return img
    diff = width - height 
    right = width - diff 
    left = top = 0 
    return img.crop((left, top, right, height))  

def trim_height(img, width, height):
    if height <= width: return img
    diff = height - width 
    bottom = height - diff 
    left = top = 0 
    return img.crop((left, top, width, bottom)) 

if __name__ == "__main__":
    print(read_source_avg_colors())
