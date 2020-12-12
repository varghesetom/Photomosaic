"""This script provides helper functions for the Photomosaic file."""


def round_to_nearest_10(num):
    """Rounds to the nearest tens digit.

       Args:
             num: a number (either an int or float)
       Returns:
           num rounded to tne nearest tens digit

       Raises:
             TypeError: if num is not a float or int
    """

    if isinstance(num, int) or isinstance(num, float):
        rem = num % 10
        return int(num / 10) * 10 if rem < 5 else int((num + 10) / 10) * 10
    else:
        raise TypeError("num is not a number.")


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

    if not isinstance(width, int) or not isinstance(width, float):
        raise TypeError("width is not a number.")

    if not isinstance(height, int) or not isinstance(height, float):
        raise TypeError("height is not a number.")

    if width <= height:
        return img
    diff = width - height 
    right = width - diff 
    left = top = 0 
    return img.crop((left, top, right, height))  


def trim_height(img, width, height):
    """Crops the height of an image.

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

    if not isinstance(width, int) or not isinstance(width, float):
        raise TypeError("width is not a number.")

    if not isinstance(height, int) or not isinstance(height, float):
        raise TypeError("height is not a number.")

    if height <= width:
        return img
    diff = height - width 
    bottom = height - diff 
    left = top = 0 
    return img.crop((left, top, width, bottom)) 
