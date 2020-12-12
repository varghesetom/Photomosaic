from src.SourceImageProcessor import SourceImageProcessor
from PIL import Image

import unittest
import subprocess
import os


class SourceImageProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.sip = SourceImageProcessor

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


class InitTestCase(SourceImageProcessorTestCase):

    def test_source_image_processor_init(self):

        self.assertEqual(self.sip("test").size, (50, 50))
        self.assertEqual(self.sip("test").is_from_img_sets, False)


class ImageDirectoryNameTestCase(SourceImageProcessorTestCase):

    def test_img_dir_name_cleaned(self):
        self.test_img_dir = "img_sets/example_dir"
        sip_from_img_set = self.sip("img_sets/example_dir")
        assert sip_from_img_set.is_from_img_sets == True
        assert "example_dir" == sip_from_img_set.img_dir_name_cleaned ("img_sets/example_dir")
        assert "img_setsexample_dir" == sip_from_img_set.img_dir_name_cleaned ("img_setsexample_dir")

''' Testing SourceImageProcessor '''



def test_creation_of_img_subdirs():
    sip = SourceImageProcessor("test")
    assert os.path.exists("img_sets/test") == False
    assert os.path.exists("img_sets/test/thumbnails") == False
    sip.create_img_subdirs()
    assert os.path.exists("img_sets/test") == True
    assert os.path.exists("img_sets/test/thumbnails") == True
    subprocess.Popen(f"rm -rf img_sets/test", shell=True)

def test_reading_from_JSON():
    '''
    Test whether can read from JSON file. To do so, need a json text file
    as well as associated thumbnails already saved in the img_sets/[IMG_DIR]/thumbnails
    directory. These two requirements must be fulfilled before realizing efficiencies
    of reading directly from JSON/thumbnails
    '''
    import json
    sip = SourceImageProcessor("test")
    assert sip.read_from_existing_JSON_file() == False
    p = subprocess.Popen(f"touch test.txt", shell = True)
    p.wait()
    assert sip.read_from_existing_JSON_file() == False         ## "test.txt" must be in img_sets/img_jsons/ location
    with open("img_sets/img_jsons/test.txt", "w") as out:
        json.dump('{"name": "Bob"}', out)
    assert sip.read_from_existing_JSON_file() == False         ## there must be a corresponding "img_sets/test/thumbnails" directory to read thumbnails for the JSON file
    p = subprocess.Popen("mkdir img_sets/test", shell = True).wait()
    p = subprocess.Popen("mkdir img_sets/test/thumbnails/", shell = True).wait()
    assert sip.read_from_existing_JSON_file() == False         ## even if thumbnails directory and JSON text file (in the appropriate place), need to still have thumbnails in the directory
    p = subprocess.Popen("touch img_sets/test/thumbnails/example.png", shell = True).wait()
    assert sip.read_from_existing_JSON_file() != False
    remove_test_dirs()

def test_get_images_from_img_dir():
    sip = SourceImageProcessor("img_sets/test")
    self.create_test_dirs()
    assert sum(1 for item in sip.get_images_from_img_dir()) == 0
    self.remove_test_dirs()


if __name__ == '__main__':
    unittest.main()
