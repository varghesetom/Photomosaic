#!/usr/bin/env python

import sys 
import os 
import json 
import functools 
import validation_util 
from BaseImage import BaseImage 
from PIL import Image 

def read_source_avg_colors(filename="avg_colors_source_imgs.txt"):
    try:
        return read_JSON_contents(filename)
    except FileNotFoundError:
        print("JSON file provided does not exist. Running program to save avg_color results to JSON file as 'avg_colors_source_imgs.txt' and re-trying to read JSON contents.") 
        save_avg_colors_to_JSON() 
        return read_JSON_contents('avg_colors_source_imgs.txt') 

def read_JSON_contents(filename):
    with open(filename, 'r') as json_file:
        return json.load(json_file) 

def save_avg_colors_to_JSON(filename="avg_colors_source_imgs.txt"):
    source_img_dict = [collect_avg_colors_for_source_imgs()]
    with open(filename, "w") as out:
        json.dump(source_img_dict, out) 

def collect_avg_colors_for_source_imgs():
    trimmed_thumbnails = standardize_source_images() 
    source_img_dict = {} 
    for img_class, images in trimmed_thumbnails.items():
        if img_class.name not in source_img_dict: 
            thumbnail, trimmed_img = images 
            source_img_dict[img_class.name] = img_class.get_avg_color(trimmed_img)
    return source_img_dict

def standardize_source_images(size=(50,50)):
    output = {}
    for img_class in get_images_from_img_dir(): 
        thumbnail_name = "thumbnails/" + img_class.name[5:-4] + "_thumbnail.jpg"
        width, height = img_class.img.size 
        if width == height: continue 
        elif width > height:
            trimmed_img = trim_width(img_class.img, width, height)  
        else:
            trimmed_img = trim_height(img_class.img, width, height)  
        thumbnail = trimmed_img.thumbnail(size)  
        trimmed_img.save(thumbnail_name, "png") 
        #thumbnail = convert_to_thumbnail(thumbnail_name, trimmed_img) 
        output[BaseImage(thumbnail_name)] = [thumbnail, trimmed_img] 
    return output 

def convert_to_thumbnail(thumbnail_name, trimmed_img):
    print(f"Thumbnail: {thumbnail}") 
    return thumbnail  

def get_images_from_img_dir():
#    img_classes = [] 
    img_dir = "imgs" # sys.argv[2]  ## first argument will be the input image to photomosaic-ify
    for fn in os.listdir(img_dir):
        if fn.endswith(".jpg") or fn.endswith(".png"): 
#            img_classes.append(BaseImage(img_dir + "/" + fn)) 
            yield BaseImage(img_dir + "/" + fn) 

def trim_width(img, width, height):
    if width <= height: return img
    diff = width - height 
    left = top = 0 
    right = width - diff 
    return img.crop((left, top, right, height))  

def trim_height(img, width, height):
    if height <= width: return img
    diff = height - width 
    left = top = 0 
    bottom = height - diff 
    return img.crop((left, top, width, bottom)) 

if __name__ == "__main__":
    print(read_source_avg_colors())
