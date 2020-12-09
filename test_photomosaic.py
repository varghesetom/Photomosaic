
import sys 
import os 
import pytest 
import PIL
from PIL import Image 
from PhotoMosaic import PhotoMosaic 

pm = PhotoMosaic() 

def test_init_types():
    assert type(pm.img.size) == tuple 
    assert type(pm.img.size[0]) == int 
    assert type(pm.img.size[1]) == int 
    assert type(pm.palette) == PIL.Image.Image 
    assert type(pm.regions_with_colors) == dict 
    assert type(pm.piece_width) == int 
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

def create_test_img(width, height):
    im = Image.new("RGBA", (width, height))
    (im.putpixel((i, j), (0,0,0)) for i in range(width) for j in range(height)) 
    return im 


