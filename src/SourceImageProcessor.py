#!/usr/bin/env python
"""In this script, we perform the necessary preprocessing for the source images."""

import os
import subprocess 
import json 
import re

from BaseImage import BaseImage
from utils.helpers import trim_width, trim_height


class SourceImageProcessor(object):
    """SourceImageProcessor performs the preprocessing needed for the
       source images. While calculating the average color is performed,
       each source image is converted into a standardized thumbnail
       before calculating the average color for the entire thumbnail.
       In other words, there is a 1:1 correspondence between a source
       image and a specific color-tuple. The other functionalities are
       specific to user handling. The program will create an
       "img_sets/[IMG_DIR]" directory to store the img_set and a
        corresponding JSON file of thumbnails in "img_sets/img_jsons/[IMG_DIR]".
        Using a JSON file format, makes it easier to directly read in all the
        thumbnails and their average colors instead of calculating them all
        over again.

        Attributes:
            img_dir: (string) Image directory
            is_from_img_sets: (boolean) Describes whether to use current img_sets folders
                                        or outside ones. Default: False.
            default_img_dir: (string) Optional. Describes the default image directory.
                                      Can input one directly. Default: img_sets/
            size: (tuple) Size of the thumbnail.
    """

    def __init__(self, img_dir, size=(50, 50), default_img_dir="img_sets"):
        """Initializes SourceImageProcessor with img_dir, size, and default_img_direct."""
        self.is_from_img_sets = False
        self.default_img_dir = default_img_dir+'/'
        self.img_dir = self.img_dir_name_cleaned(img_dir)
        self.size = size

    def img_dir_name_cleaned(self, img_dir):
        """If the user uses one of the image directories in "img_sets,"
           then returns the directory name without the leading 'img_set' header.
           If the user provides an image directory from the same file location,
           then sets the directory to that file location.

           Args:
               img_dir: (string) image directory path

            Returns:
                base_img_dir: (string) image directory path (without the header img_sets)
        """

        if re.search(self.default_img_dir[:-1], img_dir):
            base_img_dir = re.sub(self.default_img_dir, "", img_dir)
            self.is_from_img_sets = True
        else:
            base_img_dir = img_dir
        return base_img_dir

    def read_source_avg_colors(self):
        """Read from an existing JSON file, otherwise create the source image
           subdirectory and start the calculation process to store the average
           colors in a JSON file format.

           Returns:
               JSON contents
        """

        contents = self.read_from_existing_json_file()
        if not contents:
            print(f"JSON file provided does not exist. Running program to save "
                  f"avg_color results to JSON file as "
                  f"{self.default_img_dir}img_jsons/{self.img_dir}.json' and "
                  f"re-trying to read JSON contents.")
            self.create_img_subdirs()
            self.save_avg_colors_to_json()
            return self.read_json_contents()
        return contents

    def read_from_existing_json_file(self):
        """Checks to see if the json file exists, and its corresponding
           thumbnails exist as well.

           Returns:
               JSON contents
        """

        loc1 = f"{self.default_img_dir}img_jsons/" + self.img_dir + ".txt"
        if os.path.isfile(loc1) and self.check_if_json_corresponding_thumbnails():
            print("Using existing JSON and thumbnails to construct mosaic")
            return self.read_json_contents()
        return False

    def check_if_json_corresponding_thumbnails(self):
        """Performs check to see if the thumbnails folder exists."""

        thumbnail_path = f"{self.default_img_dir}{self.img_dir}/thumbnails"
        return False if not os.path.exists(thumbnail_path) or not os.listdir(thumbnail_path) else True

    def read_json_contents(self):
        loc1 = f"{self.default_img_dir}img_jsons/" + self.img_dir + ".txt"
        try:
            with open(loc1, 'r') as json_file:
                return json.load(json_file)
        except ValueError:
            print("Decoding JSON has failed. Exiting...")
            return False
        except FileNotFoundError:
            print("JSON file is not found. Exiting...")
            return False
    
    def create_img_subdirs(self):
        path = f"{self.default_img_dir}{self.img_dir}"
        if not os.path.exists(path):
            p = subprocess.Popen(f"mkdir "+path, shell=True)
            p.wait()
        if not os.path.exists(f"{self.default_img_dir}img_jsons"):
            p = subprocess.Popen(f"mkdir {self.default_img_dir}img_jsons",
                                 shell=True)
            p.wait()
        if not os.path.exists(path+f"/thumbnails"):
            p = subprocess.Popen(f"mkdir "+path+f"/thumbnails", shell=True)
            p.wait()

    def save_avg_colors_to_json(self):
        source_img_dict = [self.collect_avg_colors_for_source_imgs()]
        with open(f"{self.default_img_dir}img_jsons/{self.img_dir}" + ".txt", "w") as out:
            json.dump(source_img_dict, out)

    def collect_avg_colors_for_source_imgs(self):
        """For each thumbnail of the source image, calculate its average color
           and store it into a dictionary, saved as a JSON file."""

        trimmed_thumbnails = self.standardize_source_images()
        source_img_dict = {}
        for img_class, img in trimmed_thumbnails.items():
            if img_class.name not in source_img_dict:
                try:
                    source_img_dict[img_class.name] = img_class.get_avg_color(img)
                except TypeError:
                    pass
        return source_img_dict

    def standardize_source_images(self): 
        """Standardize the source images into "square" thumbnails. This is
           easier to work with in PIL."""

        output = {}
        for img_class in self.get_images_from_img_dir():
            thumbnail_name = f"{self.default_img_dir}{self.img_dir}/thumbnails/" + self.trim_name(img_class) + "_thumbnail.jpg"
            width, height = img_class.img.size
            trimmed_img = img_class.img
            trimmed_img = trim_width(img_class.img, width, height)
            trimmed_img = trim_height(img_class.img, width, height)
            thumbnail = trimmed_img.thumbnail(self.size)
            if not os.path.exists(f"{thumbnail_name}.png"):

                # the trimmed thumbnail will be used for our img
                trimmed_img.save(thumbnail_name, "png")

            output[BaseImage(thumbnail_name)] = trimmed_img
        return output

    def get_images_from_img_dir(self):
        """Retrieves each image from the image directory. Ignore any non-images
           when searching the source image dir.

           Yields:
               BaseImage: PIL.Image

            Raises:
                ValueError: if there are no pictures in the folder
           """

        search_dir = self.img_dir
        if self.is_from_img_sets:
            search_dir = f"{self.default_img_dir}{self.img_dir}"
        for fn in os.listdir(search_dir):
            if fn.endswith(".jpg") or fn.endswith(".png") or fn.endswith(".jpeg"):
                yield BaseImage(search_dir + "/" + fn)
        raise ValueError("There are no pictures in the folder, {}.".format(search_dir))

    def trim_name(self, img_class):
        """Shortens file name.

           Args:
               img_class: (string) name of the image class

            Returns:
                (string) shortened name
         """

        replacements = [(self.img_dir, ""), ("/", ""), ("img_sets", "")]
        new_name = img_class.name
        for old, new in replacements:
            new_name = re.sub(old, new, new_name)
        return new_name
