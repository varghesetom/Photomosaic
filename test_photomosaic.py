
import sys 
import os 
import math 
import subprocess
import PIL
from PIL import Image 
from PhotoMosaic import PhotoMosaic 
from SourceImageProcessor import SourceImageProcessor 
import pytest 

pm = PhotoMosaic() 

def test_init_types():
    assert type(pm.img.size) == tuple 
    assert type(pm.img.size[0]) == int 
    assert type(pm.img.size[1]) == int 
    assert type(pm.palette) == PIL.Image.Image 
    assert type(pm.regions_with_colors) == dict 
    assert type(pm.piece_width) == int 
    assert divmod(pm.piece_width, 5)[1] == 0 
    assert divmod(pm.piece_height, 5)[1] == 0 
    assert type(pm.piece_height) == int 
    assert pm.piece_width > 0 
    assert pm.piece_height > 0 

@pytest.mark.parametrize("size", [
   (4000, 2000)
])
def test_image_size(size):
    width, height = size 
    assert width > 0
    assert height > 0 

@pytest.mark.parametrize("width, height", [
    (0, 0),
    (65, 75),
    (310, 543) 
]) 
def test_divvy_into_box_regions(width, height):
    new_im = create_test_img(width, height) 
    new_pm = PhotoMosaic(new_im) 
    num_of_width_regions = width // new_pm.piece_width 
    num_of_height_regions = height // new_pm.piece_height 
    assert len(new_pm.divvy_into_box_regions()) == num_of_width_regions * num_of_height_regions

'''
Given test widths and heights representing different image dimensions,
figure out whether calculate_box_region properly returns a tuple where 
the top-left corner is smaller than the one at the bottom-right. 
'''
@pytest.mark.parametrize("width, height", [
    (20, 40),
    (40, 20),
    (1, 1)
])
def test_calculate_box_region(width, height):
    top_left_x, top_left_y, bottom_right_x, bottom_right_y = pm.calculate_box_region(width, height)  
    assert bottom_right_y > top_left_y 
    assert bottom_right_x > top_left_x 

@pytest.mark.parametrize("width, height", [
    (0, 0),
    (65, 75),
    (10, 20)
]) 
def test_create_trimmed_mosaic_base_with_no_remainders(width, height):
    new_im = create_test_img(width, height)
    new_pm = PhotoMosaic(new_im) 
    new_mosaic_base = new_pm.create_trimmed_mosaic_base() 
    new_width, new_height = new_mosaic_base.size
    count, rem = divmod(width, new_pm.piece_width) 
    assert rem == 0 
    assert new_width == count * new_pm.piece_width 
    count, rem = divmod(height, new_pm.piece_height) 
    assert rem == 0 
    assert new_height == count * new_pm.piece_height 


@pytest.mark.parametrize('width, height', [(67, 79),(12, 28)])
def test_create_trimmed_mosaic_base_with_remainders(width, height): 
    new_im = create_test_img(width, height)
    new_pm = PhotoMosaic(new_im) 
    new_mosaic_base = new_pm.create_trimmed_mosaic_base() 
    new_width, new_height = new_mosaic_base.size
    count, rem = divmod(width, new_pm.piece_width) 
    assert rem != 0 
    assert new_width == count * new_pm.piece_width 
    count, rem = divmod(height, new_pm.piece_height) 
    assert rem != 0 

@pytest.mark.parametrize("tuple1, tuple2", [
    ((10,10,10), (12,12,12)),
    ((14, 12, 58), (523, 484, 980)),
    ((0, 0, 0), (-1, -1, -1)) 
])
def test_euclidean_distance(tuple1, tuple2):
    r1, g1, b1 = tuple1 
    r2, g2, b2 = tuple2 
    val = math.sqrt(((r2 -r1) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2))
    assert pm.calculate_euclidean_dist(tuple1, tuple2) == val 


''' Testing SourceImageProcessor '''

def test_source_image_processor_init():
    sip = SourceImageProcessor("test") 
    assert sip.size == (50, 50) 
    assert sip.is_from_img_sets == False 

def test_img_dir_name_cleaned(): 
    test_img_dir = "img_sets/example_dir" 
    sip_from_img_set = SourceImageProcessor("img_sets/example_dir") 
    assert sip_from_img_set.is_from_img_sets == True 
    assert "example_dir" == sip_from_img_set.img_dir_name_cleaned("img_sets/example_dir") 
    assert "img_setsexample_dir" == sip_from_img_set.img_dir_name_cleaned("img_setsexample_dir") 

def test_creation_of_img_subdirs():
    sip = SourceImageProcessor("test") 
    assert os.path.exists("img_sets/test") == False 
    assert os.path.exists("img_sets/test/thumbnails") == False 
    sip.create_img_subdirs() 
    assert os.path.exists("img_sets/test") == True 
    assert os.path.exists("img_sets/test/thumbnails") == True  
    subprocess.Popen(f"rm -rf img_sets/test", shell=True) 

def test_reading_from_JSON():
    '''
    Test whether can read from JSON file. To do so, need a json text file
    as well as associated thumbnails already saved in the img_sets/[IMG_DIR]/thumbnails
    directory. These two requirements must be fulfilled before realizing efficiencies 
    of reading directly from JSON/thumbnails 
    '''
    import json 
    sip = SourceImageProcessor("test") 
    assert sip.read_from_existing_JSON_file() == False                       
    p = subprocess.Popen(f"touch test.txt", shell = True) 
    p.wait() 
    assert sip.read_from_existing_JSON_file() == False         ## "test.txt" must be in img_sets/img_jsons/ location 
    with open("img_sets/img_jsons/test.txt", "w") as out:
        json.dump('{"name": "Bob"}', out) 
    assert sip.read_from_existing_JSON_file() == False         ## there must be a corresponding "img_sets/test/thumbnails" directory to read thumbnails for the JSON file  
    p = subprocess.Popen("mkdir img_sets/test", shell = True).wait() 
    p = subprocess.Popen("mkdir img_sets/test/thumbnails/", shell = True).wait() 
    assert sip.read_from_existing_JSON_file() == False         ## even if thumbnails directory and JSON text file (in the appropriate place), need to still have thumbnails in the directory 
    p = subprocess.Popen("touch img_sets/test/thumbnails/example.png", shell = True).wait() 
    assert sip.read_from_existing_JSON_file() != False  
    remove_test_dirs() 

def test_get_images_from_img_dir():
    sip = SourceImageProcessor("img_sets/test") 
    create_test_dirs() 
    assert sum(1 for item in sip.get_images_from_img_dir()) == 0 
    remove_test_dirs() 

''' Misc. helper stub functions ''' 
def create_test_dirs():
    p = subprocess.Popen("touch img_sets/img_jsons/test.txt", shell = True)  
    p.wait() 
    p = subprocess.Popen("mkdir img_sets/test", shell = True) 
    p.wait() 
    p = subprocess.Popen("mkdir img_sets/test/thumbnails/", shell = True)    
    p.wait() 

def remove_test_dirs():
    subprocess.Popen(f"rm test.txt", shell = True) 
    subprocess.Popen(f"rm img_sets/img_jsons/test.txt", shell = True) 
    subprocess.Popen(f"rm -rf img_sets/test", shell = True) 

def create_test_img(width, height):
    im = Image.new("RGBA", (width, height))
    (im.putpixel((i, j), (0,0,0)) for i in range(width) for j in range(height)) 
    return im 


    


