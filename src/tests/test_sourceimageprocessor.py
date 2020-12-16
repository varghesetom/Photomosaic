from src.SourceImageProcessor import SourceImageProcessor
from PIL import Image
from pathlib import Path

import unittest
import subprocess
import os
import json


class SourceImageProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.sip = SourceImageProcessor
        self.test_img_dir = "img_sets/example_dir"

    ''' Misc. helper stub functions '''

    def create_test_dirs(self):
        self.p = subprocess.Popen("mkdir test_img_sets/test", shell=True)
        self.p.wait()
        self.p = subprocess.Popen("mkdir test_img_sets/test/thumbnails/", shell=True)
        self.p.wait()
        self.p = subprocess.Popen("touch test_img_sets/img_jsons/test.txt", shell=True)
        self.p.wait()

    def remove_test_dirs(self):
        subprocess.Popen(f"rm test.txt", shell=True)
        subprocess.Popen(f"rm img_sets/img_jsons/test.txt", shell=True)
        subprocess.Popen(f"rm -rf img_sets/test", shell=True)

    # TODO: Is this needed?
    # def create_test_img(self, width, height):
    #     return Image.new("RGBA", (width, height))
    #     # return (self.im.putpixel((i, j), (0, 0, 0)) for i in range(width) for j in range(height))
    #     # return im

    def save_test_image(self):
        self.new_image = Image.new("RGBA", (50, 50))
        self.new_image.save("example.png")


class InitTestCase(SourceImageProcessorTestCase):

    def test_img_dir_name_cleaned_read_in(self):
        self.assertTrue(self.sip(self.test_img_dir))

    def test_test_img_dir_name_cleaned_example_dir(self):
        self.assertEqual("example_dir", self.sip(self.test_img_dir).img_dir_name_cleaned("img_sets/example_dir"))

    def test_test_img_dir_name_not_cleaned_example_dir(self):
        self.assertEqual("img_setsexample_dir", self.sip(self.test_img_dir).img_dir_name_cleaned("img_setsexample_dir"))

    def test_default_image_size(self):
        self.assertEqual(self.sip("test").size, (50, 50))

    def test_is_from_img_sets(self):
        self.assertFalse(self.sip("test").is_from_img_sets)


class CreatingImageSubDirectoriesTestCase(SourceImageProcessorTestCase):

    def test_tset_does_not_exist(self):
        self.assertFalse(os.path.exists("test_img_sets"))

    def test_tset_thumbnails_does_not_exist(self):
        self.assertFalse(os.path.exists("test_img_sets/thumbnails"))

    def test_creation_of_img_subdirs(self):
        self.sip("test").create_img_subdirs(path="test_img_sets")
        self.assertTrue(os.path.exists("test_img_sets"))
        self.assertTrue(os.path.exists("test_img_sets/thumbnails"))
        subprocess.Popen(f"rm -rf test_img_sets", shell=True)


class ReadingFromJsonFileTestCase(SourceImageProcessorTestCase):
    """Test whether can read from JSON file. To do so, need a json text file
    as well as associated thumbnails already saved in the img_sets/[IMG_DIR]/thumbnails
    directory. These two requirements must be fulfilled before realizing efficiencies
    of reading directly from JSON/thumbnails
    """

    def test_json_file_does_not_exist(self):
        """Test that there is not a json file."""
        self.assertFalse(self.sip("test").read_from_existing_json_file())

    def test_check_text_file_inside_correct_location(self):
        """Test that the "test.txt" must be in test_img_sets/img_jsons/
           location."""
        self.p = subprocess.Popen(f"touch test.txt", shell=True)
        self.p.wait()
        self.assertFalse(self.sip("test").read_from_existing_json_file())

    def test_check_for_thumbnails_directory(self):
        """Test that there must be a corresponding "img_sets/test/thumbnails"
         directory to read thumbnails for the JSON file."""
        self.p = subprocess.Popen("mkdir test_img_sets", shell=True)
        self.p.wait()
        self.p = subprocess.Popen("mkdir test_img_sets/img_jsons", shell=True)
        self.p.wait()
        with open("test_img_sets/img_jsons/test.txt", "w") as out:
            json.dump('{"name": "Bob"}', out)
        self.assertFalse(self.sip("test").read_from_existing_json_file())

    def test_thumbnails_in_directory(self):
        """Test that even if thumbnails directory and JSON text file are
           in the appropriate place), there still needs to be thumbnails
           in the directory.
        """
        self.p = subprocess.Popen("mkdir test_img_sets/test", shell=True).wait()
        self.p = subprocess.Popen("mkdir test_img_sets/test/thumbnails/", shell=True).wait()
        self.assertFalse(self.sip("test").read_from_existing_json_file())

    # TODO: Fix thi--Example.png file not being saved into the thumbnails folder
    def test_it_all_works(self):
        self.save_test_image()
        Path('example.png').rename('test_img_sets/test/thumbnails/example.png')
        self.assertTrue(self.sip("test").read_from_existing_json_file())
        self.remove_test_dirs()


# TODO: Fix this--do we have the right test input folders?
class GetImagesFromImgDir(SourceImageProcessorTestCase):
    def test_get_images_from_img_dir(self):
        self.create_test_dirs()
        self.assertEqual(sum([1 for _ in self.sip("test_img_sets/test").get_images_from_img_dir()]), 0)
        self.remove_test_dirs()


if __name__ == '__main__':
    unittest.main()
