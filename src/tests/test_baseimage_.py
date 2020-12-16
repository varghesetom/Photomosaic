from src.BaseImage import BaseImage

import unittest


class BaseImageTestCase(unittest.TestCase):
    """
    Test BaseImage Class for various initialization errors.
    """
    def setUp(self):
        self.base_im = BaseImage
        self.sample_image_path = 'test_eagle.jpg'


class InitTestCase(BaseImageTestCase):
    def test_no_filepath(self):
        with self.assertRaises(TypeError):
            self.base_im()

    def test_none_as_filepath(self):
        with self.assertRaises(ValueError):
            self.base_im(None)

    def test_incorrect_type_as_filepath(self):
        with self.assertRaises(TypeError):
            self.base_im(4.55)


class GetImgTestCase(BaseImageTestCase):
    def test_incorrect_filepath(self):
        with self.assertRaises(FileNotFoundError):
            self.base_im('blah')

# TODO: Unit test this...
# class GetAvgColor(BaseImageTestCase):
#     def test_no_region(self):
#         self.base_im(self.sample_image_path).get_avg_color()


if __name__ == '__main__':
    unittest.main()
