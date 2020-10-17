#!/usr/bin/env python

import sys 
import os 
from PIL import Image 
import functools 
from PhotoMosaic import PhotoMosaic 
from PhotoMosaic import validate_sys_input 

@validate_sys_input
def validate_image_dir(func):
    @functools.wraps(func)
    def validated(*args):
        if not os.path.isdir(sys.argv[1]):
            raise ValueError("Need to pass in (image) directory") 
            sys.exit(1) 
        result = func(*args)
        return result
    return validated 

def get_avg_color_per_image():
    img_classes_trimmed = standardize_source_images() 
    for img_class, trimmed_img in img_classes_trimmed.items():
        print(f"img: {img_class.name}, avg_color: {img_class.get_avg_color(trimmed_img)}")
        img_class.create_new_img() 

@validate_image_dir 
def standardize_source_images():
    img_classes = [] 
    img_dir = sys.argv[1] 
    for fn in os.listdir(img_dir):
        if fn.endswith(".jpg") or fn.endswith(".png"): 
            img_classes.append(PhotoMosaic(img_dir + "/" + fn)) 
    output = {}
    for img_class in img_classes: 
        width, height = img_class.img.size 
        if width == height: continue 
        elif width > height:
            output[img_class] = trim_width(img_class.img, width, height) 
        else:
            output[img_class] = trim_height(img_class.img, width, height) 
    return output 

def trim_width(img, width, height):
    if width <= height: return im
    diff = width - height 
    left = top = 0 
    right = width - diff 
    return img.crop((left, top, right, height))  

def trim_height(img, width, height):
    if height <= width: return im
    diff = height - width 
    left = top = 0 
    bottom = height - diff 
    return im.crop((left, top, width, bottom)) 

if __name__ == "__main__":
    get_avg_color_per_image()  
