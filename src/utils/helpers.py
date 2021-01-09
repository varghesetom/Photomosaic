#!/usr/bin/env python
"""This script provides helper functions for the Photomosaic.py file."""

import functools
import logging


def validate_type(sample_object, sample_type):
    return isinstance(sample_object, sample_type)


def validate_round_to_nearest_10(func):
    """Raises a TypeError if num is not a float or int."""

    @functools.wraps(func)
    def validated(*args):
        if args[0] is None:
            raise ValueError("Error. Num field is none.")
        if not validate_type(args[0], int) and not validate_type(args[0], float):
            raise TypeError("Error. {} is not a number.".format(args[0]))
        result = func(*args)
        return result
    return validated


def validate_trim(func):
    """Raises a TypeError if width is not a number or if height is not
       a number."""

    @functools.wraps(func)
    def validated(*args):
        if args[1] is None:
            raise ValueError("Error. Width field is none.")
        if args[-1] is None:
            raise ValueError("Error. Height field is none.")
        if not validate_type(args[1], int) and not validate_type(args[1], float):
            raise TypeError("width is not a number.")
        if not validate_type(args[-1], int) and not validate_type(args[-1], float):
            raise TypeError("height is not a number.")
        result = func(*args)
        return result
    return validated


@validate_round_to_nearest_10
def round_to_nearest_10(num):
    """Rounds to the nearest tens digit.

       Args:
             num: a number
       Returns:
           num rounded to tne nearest tens digit
    """

    rem = num % 10
    return int(num / 10) * 10 if rem < 5 else int((num + 10) / 10) * 10


@validate_trim
def trim_width(img, width, height):
    """Crops the width of an image.

       Args:
           img: the image
           width: the width
           height: the height

       Returns:
           cropped image

       Raises:
           TypeError: if width is not a number (int or float)
           TypeError: if height is not a number (int or float)
    """

    if width <= height:
        return img
    diff = width - height 
    right = width - diff 
    left = top = 0 
    return img.crop((left, top, right, height))  


@validate_trim
def trim_height(img, width, height):
    """Crops the height of an image.

       Args:
           img: the image
           width: the width
           height: the height

       Returns:
           cropped image
    """

    if height <= width:
        return img
    diff = height - width 
    bottom = height - diff 
    left = top = 0 
    return img.crop((left, top, width, bottom)) 


class Logger(object):
    """
    Logger creates a logger object to help debug aspects of each module. It
    creates a logger--which holds the time, the file name, where in the file
    the message is appearing, as well as the message itself. Each message is
    recorded and written to a log file, which is in the main src directory.

    Attributes:
        logger: (string) name of the logger. Default: None
        log_file_name: (string) name of the log file. Default: logfile.log
    """

    def __init__(self, logger=None, log_file_name='logfile.log'):
        """Initializes the logger with logger and the log_file_name."""
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')

        # Writes the logger to the file
        self.file_handler = logging.FileHandler(log_file_name)
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.file_handler)

    def log_message(self, message):
        """Writes the message to the log."""
        self.logger.debug(message)
