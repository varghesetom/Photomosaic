import unittest
import os
import math
import PIL

from PIL import Image

from src.Photomosaic import PhotoMosaic


class PhotoMosaicTestCase(unittest.TestCase):
    def setUp(self):
        self.pm = PhotoMosaic
        self.sample_image_path = 'test_eagle.jpg'
        self.test_img_dir = 'test_img_sets'

    def create_test_image(self, width, height):
        """Create a new test image and save it."""
        self.im = Image.new("RGBA", (width, height))
        self.im.save("example.png")

    def delete_test_image(self):
        os.remove("example.png")


class InitTestCase(PhotoMosaicTestCase):
    """
    Test that the initial attributes are the correct type
    and greater than zero for some
    """
    def test_no_filename(self):
        with self.assertRaises(ValueError):
            self.pm()

    def test_none_directory(self):
        with self.assertRaises(ValueError):
            self.pm(filename=self.sample_image_path)

    def test_wrong_type_directory(self):
        """Note: this test will fail unless the type error is checked."""
        with self.assertRaises(TypeError):
            self.pm(filename=self.sample_image_path, directory=345)

    def test_image_size_type(self):
        self.assertTrue(isinstance(self.pm(filename=self.sample_image_path,
                                           directory=self.test_img_dir).img.size,
                                   tuple))

    def test_image_size_first_dimension_type(self):
        self.assertTrue(isinstance(self.pm(filename=self.sample_image_path,
                                           directory=self.test_img_dir).img.size[0], int))

    def test_image_size_second_dimension_type(self):
        self.assertTrue(isinstance(self.pm(filename=self.sample_image_path,
                                           directory=self.test_img_dir).img.size[1], int))

    def test_palette_type(self):
        self.assertTrue(isinstance(self.pm(filename=self.sample_image_path,
                                           directory=self.test_img_dir).palette, PIL.Image.Image))

    def test_regions_with_color_type(self):
        self.assertTrue(isinstance(self.pm(filename=self.sample_image_path,
                                           directory=self.test_img_dir).regions_with_colors, dict))

    def test_piece_width_type(self):
        self.assertTrue(isinstance(self.pm(filename=self.sample_image_path,
                                           directory=self.test_img_dir).piece_width, int))

    def test_piece_height_type(self):
        self.assertTrue(isinstance(self.pm(filename=self.sample_image_path,
                                           directory=self.test_img_dir).piece_height, int))

    def test_piece_width_division(self):
        self.assertEqual(divmod(self.pm(filename=self.sample_image_path,
                                        directory=self.test_img_dir).piece_width, 5)[1], 0)

    def test_piece_height_division(self):
        self.assertEqual(divmod(self.pm(filename=self.sample_image_path,
                                        directory=self.test_img_dir).piece_height, 5)[1], 0)

    def test_piece_width_greater_than_zero(self):
        self.assertGreater(self.pm(filename=self.sample_image_path,
                                   directory=self.test_img_dir).piece_width, 0)

    def test_piece_height_greater_than_zero(self):
        self.assertGreater(self.pm(filename=self.sample_image_path,
                                   directory=self.test_img_dir).piece_height, 0)


class DivvyIntoBoxRegionsTestCase(PhotoMosaicTestCase):
    """
    Test that the regions are divided into boxes via various width and
    height sizes.
    """
    def test_divvy_into_box_regions(self):

        widths = [4000, 1, 65, 310]
        heights = [2000, 1, 75, 543]
        for width, height in zip(widths, heights):
            self.create_test_image(width, height)
            new_pm = self.pm(filename="example.png", directory=os.getcwd())
            num_of_width_regions = width // new_pm.piece_width
            num_of_height_regions = height // new_pm.piece_height
            self.assertEqual(len(new_pm.divvy_into_box_regions()), num_of_width_regions * num_of_height_regions)
            self.delete_test_image()


class CalculateBoxRegionTestCase(PhotoMosaicTestCase):
    """
    Test that the boxes regions are calculated properly.
    """

    def test_calculate_box_region(self):
        """
        Test differing widths and heights representing image dimensions.
        """
        widths = [20, 40, 1]
        heights = [40, 20, 1]
        for width, height in zip(widths, heights):
            self.create_test_image(width, height)
            region = self.pm(filename="example.png",
                             directory=os.getcwd()).calculate_box_region(width, height)
            self.assertGreater(region[-1], region[1])
            self.assertGreater(region[-2], region[0])
            self.delete_test_image()


class TrimmedMosaicBaseTestCase(PhotoMosaicTestCase):
    """
    Test the various cases for the trimmed mosaic base.
    """

    def test_create_trimmed_mosaic_base_with_no_remainders(self):
        """
        Test the trimmed mosaic base was created without any remainders.
        """

        widths = [25, 50]
        heights = [75, 100]
        for width, height in zip(widths, heights):
            self.create_test_image(width, height)
            new_pm = self.pm(filename="example.png", directory=os.getcwd())
            new_mosaic_base = new_pm.create_trimmed_mosaic_base()
            new_width, new_height = new_mosaic_base.size
            count_1, rem_1 = divmod(width, new_pm.piece_width)
            self.assertEqual(rem_1, 0)
            self.assertEqual(new_width, count_1 * new_pm.piece_width)
            count_2, rem_2 = divmod(height, new_pm.piece_height)
            self.assertEqual(rem_2, 0)
            self.assertEqual(new_height, count_2 * new_pm.piece_height)

    def test_create_trimmed_mosaic_base_with_remainders(self):
        """
        Test the trimmed mosaic base was created with remainders.
        """

        widths = [67, 12]
        heights = [79, 28]
        for width, height in zip(widths, heights):
            self.create_test_image(width, height)
            new_pm = self.pm(filename="example.png", directory=os.getcwd())
            new_mosaic_base = new_pm.create_trimmed_mosaic_base()
            new_width, new_height = new_mosaic_base.size
            count_1, rem_1 = divmod(width, new_pm.piece_width)
            self.assertNotEqual(rem_1, 0)
            self.assertEqual(new_width, count_1 * new_pm.piece_width)
            count, rem_2 = divmod(height, new_pm.piece_height)
            self.assertNotEqual(rem_2, 0)


class GetIndexTestCase(PhotoMosaicTestCase):
    """
    Test that the color indexes are saved correctly
    and error-handled when instance types or integers
    are incorrect.
    """

    def test_empty_thumbnail_file_path(self):
        self.create_test_image(50, 50)
        self.sample_json_data = {"": 5, "monkey": [0, 7, 0]}
        with self.assertRaises(ValueError):
            self.pm(filename="example.png",
                    directory=os.getcwd()).get_index(self.sample_json_data)
        self.delete_test_image()

    def test_none_thumbnail_file_path(self):
        self.create_test_image(50, 50)
        self.sample_json_data = {None: 5, "monkey": [0, 7, 0]}
        with self.assertRaises(ValueError):
            self.pm(filename="example.png",
                    directory=os.getcwd()).get_index(self.sample_json_data)
        self.delete_test_image()

    def test_incorrect_type_thumbnail_file_path(self):
        self.create_test_image(50, 50)
        self.sample_json_data = {5: 5, "monkey": [0, 7, 0]}
        with self.assertRaises(TypeError):
            self.pm(filename="example.png",
                    directory=os.getcwd()).get_index(self.sample_json_data)
        self.delete_test_image()

    def test_thumbnail_file_does_not_exist(self):
        self.create_test_image(50, 50)
        self.sample_json_data = {"test_png_thumbnail_2.jpg": [104, 112, 99]}
        with self.assertRaises(FileNotFoundError):
            self.pm(filename="example.png",
                    directory=os.getcwd()).get_index(self.sample_json_data)
        self.delete_test_image()

    def test_empty_pixel_value(self):
        self.create_test_image(50, 50)
        self.sample_json_data = {"test_png_thumbnail.jpg": []}
        with self.assertRaises(ValueError):
            self.pm(filename="example.png",
                    directory=os.getcwd()).get_index(self.sample_json_data)
        self.delete_test_image()

    def test_none_pixel_value(self):
        self.create_test_image(50, 50)
        self.sample_json_data = {"test_png_thumbnail.jpg": None}
        with self.assertRaises(ValueError):
            self.pm(filename="example.png",
                    directory=os.getcwd()).get_index(self.sample_json_data)
        self.delete_test_image()

    def test_incorrect_pixel_value_type(self):
        self.create_test_image(50, 50)
        self.sample_json_data = {"test_png_thumbnail.jpg": "bananas"}
        with self.assertRaises(TypeError):
            self.pm(filename="example.png",
                    directory=os.getcwd()).get_index(self.sample_json_data)
        self.delete_test_image()

    def test_pixels_out_of_range(self):
        self.create_test_image(50, 50)
        self.sample_json_data = {"test_png_thumbnail.jpg": [7, 13, 400]}
        with self.assertRaises(ValueError):
            self.pm(filename="example.png",
                    directory=os.getcwd()).get_index(self.sample_json_data)
        self.delete_test_image()

    def test_negative_pixels_out_of_range(self):
        self.create_test_image(50, 50)
        self.sample_json_data = {"test_png_thumbnail.jpg": [-7, 13, 200]}
        with self.assertRaises(ValueError):
            self.pm(filename="example.png",
                    directory=os.getcwd()).get_index(self.sample_json_data)
        self.delete_test_image()

    def test_get_index_one(self):
        self.create_test_image(50, 50)
        self.sample_json_data = {"test_png_thumbnail.jpg": [104, 112, 99]}
        result = {(100, 110, 100): [('test_png_thumbnail.jpg', [104, 112, 99])]}
        self.assertEqual(result, self.pm(filename="example.png",
                                         directory=os.getcwd()).get_index(self.sample_json_data))
        self.delete_test_image()

    def test_get_index_two(self):
        self.create_test_image(50, 50)
        self.sample_json_data = {"test_png_thumbnail.jpg": [104, 112, 99],
                                 "test_png_thumbnail_2a.jpg": [132, 94, 19]}
        result = {(100, 110, 100): [('test_png_thumbnail.jpg', [104, 112, 99])],
                  (130, 90, 20): [('test_png_thumbnail_2a.jpg', [132, 94, 19])]}
        self.assertEqual(result, self.pm(filename="example.png",
                                         directory=os.getcwd()).get_index(self.sample_json_data))
        self.delete_test_image()


class EuclideanDistTestCase(PhotoMosaicTestCase):
    """
    Test that the euclidean distance formula is the same than the normal
    math.sqrt function.
    """

    def test_euclidean_distance(self):
        self.create_test_image(50, 50)
        tuples_1 = [(10, 10, 10), (14, 12, 58), (0, 0, 0)]
        tuples_2 = [(12, 12, 12), (523, 484, 980), (-1, -1, -1)]
        for tuple1, tuple2 in zip(tuples_1, tuples_2):
            val = math.sqrt(((tuple2[0]-tuple1[0]) ** 2 + (tuple1[1]-tuple2[1]) ** 2 + (tuple1[-1]-tuple2[-1]) ** 2))
            self.assertEqual(self.pm(filename="example.png",
                                     directory=os.getcwd()).calculate_euclidean_dist(tuple1, tuple2), val)
        self.delete_test_image()
