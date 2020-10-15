
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
    assert type(pm.region_colors) == list 

@pytest.mark.parametrize("size", [
   (4000, 2000)
])
def test_image_size(size):
    width, height = size 
    assert width > 0
    assert height > 0 
