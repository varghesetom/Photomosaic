import unittest
import subprocess
import os
import json

from PIL import Image
from pathlib import Path

from src.SourceImageProcessor import SourceImageProcessor


class SourceImageProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.sip = SourceImageProcessor
        self.test_img_dir = "img_sets/example_dir"

    def create_folders(self):
        """Create the test folders."""

        self.p = subprocess.Popen("mkdir test_img_sets", shell=True).wait()
        self.p = subprocess.Popen("mkdir test_img_sets/test", shell=True).wait()
        self.p = subprocess.Popen("mkdir test_img_sets/img_jsons", shell=True).wait()

    def remove_folders(self):
        """Remove the test folders."""

        self.p = subprocess.Popen(f"rm -rf test_img_sets/img_jsons", shell=True).wait()
        self.p = subprocess.Popen(f"rm -rf test_img_sets/test", shell=True).wait()
        self.p = subprocess.Popen(f"rm -rf test_img_sets", shell=True).wait()

    def create_json_file_and_folders(self):
        """Create the test json file and tests folders as well."""

        self.create_folders()
        with open("test_img_sets/img_jsons/test.txt", "w") as out:
            json.dump('{"name": "Bob"}', out)

    def remove_json_file_and_folders(self):
        """Remove the test json file and folders."""

        self.p = subprocess.Popen(f"rm test_img_sets/img_jsons/test.txt", shell=True).wait()
        self.remove_folders()

    def create_thumbnails_folder(self):
        """Create the test folders and test thumbnails folder."""

        self.p = subprocess.Popen("mkdir test_img_sets", shell=True).wait()
        self.p = subprocess.Popen("mkdir test_img_sets/test", shell=True).wait()
        self.p = subprocess.Popen("mkdir test_img_sets/test/thumbnails/", shell=True).wait()

    def remove_thumbnails_folder(self):
        """Remove the test folders and test thumbnails folder."""

        self.p = subprocess.Popen(f"rm -rf test_img_sets/test/thumbnails/", shell=True).wait()
        self.p = subprocess.Popen(f"rm -rf test_img_sets/test", shell=True).wait()
        self.p = subprocess.Popen(f"rm -rf test_img_sets", shell=True).wait()

    def create_test_with_everything(self):
        """Create the test folders, test json file, and test thumbnails folder."""

        self.p = subprocess.Popen("mkdir test_img_sets", shell=True).wait()
        self.p = subprocess.Popen("mkdir test_img_sets/img_jsons", shell=True).wait()
        self.p = subprocess.Popen("mkdir test_img_sets/test", shell=True).wait()
        self.p = subprocess.Popen("mkdir test_img_sets/test/thumbnails/", shell=True).wait()

        with open("test_img_sets/img_jsons/test.txt", "w") as out:
            json.dump('{"name": "Bob"}', out)

    def remove_test_with_everything(self):
        """Remove the test folders, test json file, and test thumbnails folder."""

        self.p = subprocess.Popen(f"rm -rf test_img_sets/test/thumbnails/", shell=True).wait()
        self.p = subprocess.Popen(f"rm -rf test_img_sets/test", shell=True).wait()
        self.p = subprocess.Popen(f"rm -rf test_img_sets/img_jsons", shell=True).wait()
        self.p = subprocess.Popen(f"rm -rf test_img_sets", shell=True).wait()

    def save_test_image(self):
        """Create a new test image and save it."""

        self.new_image = Image.new("RGBA", (50, 50))
        self.new_image.save("example.png")


class InitTestCase(SourceImageProcessorTestCase):
    """Test that the initial parameters are correct."""

    def test_img_dir_name_cleaned_read_in(self):
        self.assertTrue(self.sip(self.test_img_dir))

    def test_test_img_dir_name_cleaned_example_dir(self):
        self.assertEqual("example_dir",
                         self.sip(self.test_img_dir).img_dir_name_cleaned("img_sets/example_dir"))

    def test_test_img_dir_name_not_cleaned_example_dir(self):
        self.assertEqual("img_setsexample_dir",
                         self.sip(self.test_img_dir).img_dir_name_cleaned("img_setsexample_dir"))

    def test_default_image_size(self):
        self.assertEqual(self.sip("test").size, (50, 50))

    def test_is_from_img_sets(self):
        self.assertFalse(self.sip("test").is_from_img_sets)


class CreatingImageSubDirectoriesTestCase(SourceImageProcessorTestCase):
    """Test that the correct subfolders are created."""

    def test_tset_does_not_exist(self):
        self.assertFalse(os.path.exists("test_img_sets"))

    def test_tset_thumbnails_does_not_exist(self):
        self.assertFalse(os.path.exists("test_img_sets/test/thumbnails"))

    def test_creation_of_img_subdirs(self):
        self.p = subprocess.Popen("mkdir test_img_sets", shell=True).wait()

        self.sip("test", default_img_dir="test_img_sets").create_img_subdirs()
        self.assertTrue(os.path.exists("test_img_sets/test"))
        self.assertTrue(os.path.exists("test_img_sets/test/thumbnails"))

        self.remove_thumbnails_folder()


class ReadingFromJsonFileTestCase(SourceImageProcessorTestCase):
    """Test whether can read from JSON file. To do so, need a json text file
       as well as associated thumbnails already saved in the
       img_sets/[IMG_DIR]/thumbnails directory. These two requirements must be
       fulfilled before realizing efficiencies of reading directly from
       JSON/thumbnails.
    """

    def test_json_file_does_not_exist(self):
        """Test that there is not a json file."""
        self.create_folders()
        self.assertFalse(self.sip("test", default_img_dir="test_img_sets").read_from_existing_json_file())
        self.remove_folders()

    def test_check_for_thumbnails_directory(self):
        """Test that there must be a corresponding "test_img_sets/test/thumbnails"
         directory to read thumbnails for the JSON file."""
        self.create_json_file_and_folders()
        self.assertFalse(self.sip("test",
                                  default_img_dir="test_img_sets").check_if_json_corresponding_thumbnails())
        self.remove_json_file_and_folders()

    def test_it_all_works(self):
        """Test that with the correct folders and image, everything works."""
        self.create_test_with_everything()
        self.save_test_image()
        Path('example.png').rename('test_img_sets/test/thumbnails/example.png')
        self.assertTrue(self.sip("test",
                                 default_img_dir="test_img_sets").read_from_existing_json_file())
        self.remove_test_with_everything()


class GetImagesFromImgDir(SourceImageProcessorTestCase):
    """
    Test that images are properly retrieved from the image directory.
    """
    def test_get_images_from_img_dir(self):
        self.create_test_with_everything()
        check = self.sip("test", default_img_dir="test_img_sets")
        check.is_from_img_sets = True
        src1 = check.get_images_from_img_dir()
        with self.assertRaises(ValueError):
            a = next(src1)
        self.remove_test_with_everything()


if __name__ == '__main__':
    unittest.main()
