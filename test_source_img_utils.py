import sys 
import os 
import pytest 
import PIL
from PIL import Image 
from source_img_utils import trim_width, trim_height 

def create_test_img(width, height):
    im = Image.new("RGBA", (width, height))
    (im.putpixel((i, j), (0,0,0)) for i in range(width) for j in range(height)) 
    return im 

@pytest.mark.parametrize("width, height", [
        (40, 20),
        (1000, 1),
        (101, 101),
        (1, 1)
]) 
def test_source_trim_func(width, height):
    trim_func(trim_width, width, height) 

@pytest.mark.parametrize("width, height", [
    (20, 40),
    (1, 1000),
    (101, 101),
    (1, 1)
])
def test_trim_height(width, height):
    trim_func(trim_height, width, height) 

def trim_func(func, width, height):
    test_img = create_test_img(width, height) 
    smallest_dimension = min(test_img.size) 
    output_img = func(test_img, width, height) 
    output_width, output_height = output_img.size 
    assert output_width == output_height
    assert output_width == smallest_dimension 

r = create_test_img(100,100)
print(r, r.size) 

