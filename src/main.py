from Photomosaic import PhotoMosaic
from utils import validation_util

import argparse

#
# @validation_util.validate_input_is_image
# @validation_util.validate_img_dir
def parse_args():
    """Takes in the arguments passed in the shell to be used in the main script.
    Returns:
        args -- arguments
    """
    parser = argparse.ArgumentParser(description='Turns input image into a photomosaic')
    parser.add_argument('--input', help="enter the input image", type=str)
    parser.add_argument('--directory', help="enter the source input directory", type=str)
    args = parser.parse_args()
    return args


def main():
    # Input and Output files Error-Handling
    args = parse_args()
    if args.input is None:
        raise ImportError('Did not specify the correct input file!')
    if args.directory is None:
        raise ImportError('Did not specify the correct directory!')

    pm = PhotoMosaic(filename=args.input, directory=args.directory)
    pm.create_mosaic()


if __name__ == "__main__":
    main()

