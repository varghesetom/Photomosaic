#!/usr/bin/env python

"""Decorators to test validity of command line arguments passed in."""

import os
import sys
import functools


def validate_sys_input(func):
    """Validates the system inputs. First argument, after input, must be a image
       and the second argument, after directory, must be the image directory
       of thumbnails.
    """
    @functools.wraps(func)
    def validated(*args):
        if len(sys.argv) < 5:
            raise ValueError("Need additional image and img_dir argument.")
        result = func(*args)
        return result
    return validated


@validate_sys_input
def validate_input_is_image(func):
    """Validates if the first argument, after input, has a png, jpg
       extension. Even if none."""
    @functools.wraps(func)
    def validated(*args):
        cli_arg = sys.argv[2]
        if not (cli_arg.endswith(".png") or cli_arg.endswith(".jpg")):
            raise ValueError("Input image argument does not end with "
                             "an img extension.")
        if cli_arg is None:
            raise ImportError("Did not specify the correct input file!")
        if not isinstance(cli_arg, str):
            raise TypeError("Error. {} is not of string type.".format(cli_arg))
        result = func(*args)
        return result
    return validated


@validate_sys_input
def validate_img_dir(func):
    """Validates if the image directory for the thumbnails exists."""
    @functools.wraps(func)
    def validated(*args):
        dir_path = sys.argv[-1]
        if not os.path.isdir(dir_path):
            raise ValueError("Need to pass in existing (image) directory.")
        if not os.listdir(dir_path):
            raise ValueError("Image directory argument is empty.")
        if dir_path is None:
            raise ImportError('Did not specify the correct directory!')
        if not isinstance(dir_path, str):
            raise TypeError("Error. {} is not of string type.".format(dir_path))
        result = func(*args)
        return result
    return validated


def validate_filename(func):
    @functools.wraps(func)
    def validated(*args):
        if args[-1] is None:
            raise ValueError("Error. None is not a correct file name.")
        if not isinstance(args[-1], str):
            raise TypeError("Error. {} is not of type string.".format(args[-1]))
        result = func(*args)
        return result
    return validated
