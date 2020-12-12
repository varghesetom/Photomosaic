from src.BaseImage import BaseImage

import unittest


class BaseImageTestCase(unittest.TestCase):

    def test_no_filepath(self):
        with self.assertRaises(TypeError):
            self.base_im = BaseImage()

    def test_incorrect_filepath(self):
        with self.assertRaises(FileNotFoundError):
            self.base_im = BaseImage('blah')

if __name__ == '__main__':
    unittest.main()
