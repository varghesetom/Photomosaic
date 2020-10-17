
import sys 
import os 
import pytest 
import PIL
from PIL import Image 
from PhotoMosaic import PhotoMosaic 

pm = PhotoMosaic() 

def create_test_img(width, height):
    im = Image.new("RGBA", (width, height))
    (im.putpixel((i, j), (0,0,0)) for i in range(width) for j in range(height)) 
    return im 

def test_init_types():
    assert type(pm.img.size) == tuple 
    assert type(pm.img.size[0]) == int 
    assert type(pm.img.size[1]) == int 
    assert type(pm.palette) == PIL.Image.Image 
    assert type(pm.region_colors) == list 
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
    (20, 40),
    (40, 20),
    (1, 1)
])
def test_box_region_is_valid_square(width, height):
    top_left_x, top_left_y, bottom_right_x, bottom_right_y = pm.calculate_box_region(width, height)  
    assert bottom_right_y > top_left_y 
    assert bottom_right_x > top_left_x 


