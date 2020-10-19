#!/usr/bin/env python

import sys 
import os 
from PIL import Image 
import functools 
import validation_util 
from PhotoMosaic import PhotoMosaic 


@validation_util.validate_image_dir 
def standardize_source_images():
    img_classes = [] 
    img_dir = sys.argv[2]  ## reminder that the first argument will be the input image to photomosaic-ify
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

def collect_avg_colors_for_source_imgs():
    img_classes_trimmed = standardize_source_images() 
    source_img_dict = {} 
    for img_class, trimmed_img in img_classes_trimmed.items():
        if img_class.name not in source_img_dict: 
            source_img_dict[img_class.name] = img_class.get_avg_color(trimmed_img) 
        img_class.create_new_img() 
    return source_img_dict

if __name__ == "__main__":
    avg_colors = collect_avg_colors_for_source_imgs()  
    for k, v in avg_colors.items(): 
        print(f"img: {k}, avg_color: {v}")

