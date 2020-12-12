from src.Photomosaic import PhotoMosaic

from PIL import Image

import sys
import os
import math
import subprocess
import PIL

import unittest


class PhotoMosaicTestCase(unittest.TestCase):
    def setUp(self):
        # # For debug purposes
        # self.test_image = '/home/akhil/Photomosaic/eagle.jpg'
        # self.test_directory = '/home/akhil/Photomosaic/img_sets/flower_imgs'

        self.pm = PhotoMosaic

    ''' Misc. helper stub functions '''

    def create_test_dirs(self):
        self.p = subprocess.Popen ("touch img_sets/img_jsons/test.txt", shell=True)
        self.p.wait()
        self.p = subprocess.Popen ("mkdir img_sets/test", shell=True)
        self.p.wait()
        self.p = subprocess.Popen ("mkdir img_sets/test/thumbnails/", shell=True)
        self.p.wait()

    def remove_test_dirs(self):
        subprocess.Popen(f"rm test.txt", shell=True)
        subprocess.Popen(f"rm img_sets/img_jsons/test.txt", shell=True)
        subprocess.Popen(f"rm -rf img_sets/test", shell=True)

    def create_test_img(self, width, height):
        self.im = Image.new("RGBA", (width, height))
        return (self.im.putpixel((i, j), (0, 0, 0)) for i in range (width) for j in range (height))
        # return im


class InitTestCase(PhotoMosaicTestCase):
    """
    Test that the initial attributes are the correct type
    and greater than zero for some
    """

    def test_image_size_type(self):
        self.assertTrue(isinstance(self.pm().img.size, tuple))

    def test_image_size_first_dimension_type(self):
        self.assertTrue(isinstance(self.pm().img.size[0], int))

    def test_image_size_second_dimension_type(self):
        self.assertTrue(isinstance(self.pm().img.size[1], int))

    def test_palette_type(self):
        self.assertTrue(isinstance(self.pm().palette, PIL.Image.Image))

    def test_regions_with_color_type(self):
        self.assertTrue(isinstance(self.pm().regions_with_colors, dict))

    def test_piece_width_type(self):
        self.assertTrue(isinstance(self.pm().piece_width, int))

    def test_piece_height_type(self):
        self.assertTrue(isinstance(self.pm().piece_height, int))

    def test_piece_width_division(self):
        self.assertEqual(divmod(self.pm().piece_width, 5)[1], 0)

    def test_piece_height_division(self):
        self.assertEqual(divmod(self.pm().piece_height, 5)[1], 0)

    def test_piece_width_greater_than_zero(self):
        self.assertGreater(self.pm().piece_width, 0)

    def test_piece_height_greater_than_zero(self):
        self.assertGreater(self.pm().piece_height, 0)


class DivvyIntoBoxRegionsTestCase(PhotoMosaicTestCase):

    def test_divvy_into_box_regions(self):
        width, height = (4000, 2000)
        new_im = self.create_test_img(width, height)
        new_pm = self.pm(new_im)
        num_of_width_regions = width // new_pm.piece_width
        num_of_height_regions = height // new_pm.piece_height
        self.assertEqual(len(new_pm.divvy_into_box_regions()), num_of_width_regions * num_of_height_regions)


# IDK
# @pytest.mark.parametrize("size", [
#    (4000, 2000)
# ])
# def test_image_size(size):
#     width, height = size
#     assert width > 0
#     assert height > 0

# @pytest.mark.parametrize("width, height", [
#     (0, 0),
#     (65, 75),
#     (310, 543)
# ])
# def test_divvy_into_box_regions(width, height):
#     new_im = create_test_img(width, height)
#     new_pm = PhotoMosaic(new_im)
#     num_of_width_regions = width // new_pm.piece_width
#     num_of_height_regions = height // new_pm.piece_height
#     assert len(new_pm.divvy_into_box_regions()) == num_of_width_regions * num_of_height_regions
#
# '''
# Given test widths and heights representing different image dimensions,
# figure out whether calculate_box_region properly returns a tuple where
# the top-left corner is smaller than the one at the bottom-right.
# '''
# @pytest.mark.parametrize("width, height", [
#     (20, 40),
#     (40, 20),
#     (1, 1)
# ])
# def test_calculate_box_region(width, height):
#     top_left_x, top_left_y, bottom_right_x, bottom_right_y = pm.calculate_box_region(width, height)
#     assert bottom_right_y > top_left_y
#     assert bottom_right_x > top_left_x
#
# @pytest.mark.parametrize("width, height", [
#     (0, 0),
#     (25, 75),
#     (50, 100)
# ])
# def test_create_trimmed_mosaic_base_with_no_remainders(width, height):
#     new_im = create_test_img(width, height)
#     new_pm = PhotoMosaic(new_im)
#     new_mosaic_base = new_pm.create_trimmed_mosaic_base()
#     new_width, new_height = new_mosaic_base.size
#     count, rem = divmod(width, new_pm.piece_width)
#     assert rem == 0
#     assert new_width == count * new_pm.piece_width
#     count, rem = divmod(height, new_pm.piece_height)
#     assert rem == 0
#     assert new_height == count * new_pm.piece_height
#
#
# @pytest.mark.parametrize('width, height', [(67, 79),(12, 28)])
# def test_create_trimmed_mosaic_base_with_remainders(width, height):
#     new_im = create_test_img(width, height)
#     new_pm = PhotoMosaic(new_im)
#     new_mosaic_base = new_pm.create_trimmed_mosaic_base()
#     new_width, new_height = new_mosaic_base.size
#     count, rem = divmod(width, new_pm.piece_width)
#     assert rem != 0
#     assert new_width == count * new_pm.piece_width
#     count, rem = divmod(height, new_pm.piece_height)
#     assert rem != 0
#
# @pytest.mark.parametrize("tuple1, tuple2", [
#     ((10,10,10), (12,12,12)),
#     ((14, 12, 58), (523, 484, 980)),
#     ((0, 0, 0), (-1, -1, -1))
# ])
# def test_euclidean_distance(tuple1, tuple2):
#     r1, g1, b1 = tuple1
#     r2, g2, b2 = tuple2
#     val = math.sqrt(((r2 -r1) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2))
#     assert pm.calculate_euclidean_dist(tuple1, tuple2) == val
#
#






