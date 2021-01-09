#!/usr/bin/env python
"""Main driver file for the Photomosaic project."""

import argparse

from Photomosaic import PhotoMosaic
from utils import validation_util


@validation_util.validate_input_is_image
@validation_util.validate_img_dir
def parse_args():
    """Takes in the arguments passed in the shell to be used in the main script.

       Returns:
           args: (strings) arguments
    """
    parser = argparse.ArgumentParser(description='Turns input image '
                                                 'into a photomosaic')
    parser.add_argument('--input', help="enter the input image", type=str)
    parser.add_argument('--directory', help="enter the source input directory", type=str)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    photo_image = PhotoMosaic(filename=args.input, directory=args.directory)
    photo_image.create_mosaic()


if __name__ == "__main__":
    main()
