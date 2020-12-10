'''
Decorators to test validity of command line arguments passed in
'''

import os 
import sys 
import functools 

def validate_sys_input(func):
    @functools.wraps(func)
    def validated(*args):
        if len(sys.argv) < 3: 
            raise ValueError("Need additional image and img_dir argument") 
            sys.exit(1)
        result = func(*args)
        return result 
    return validated 

@validate_sys_input
def validate_input_is_image(func):
    @functools.wraps(func)
    def validated(*args):
        cli_arg = sys.argv[1] 
        if not (cli_arg.endswith(".png") or cli_arg.endswith(".jpg")):
            raise ValueError("input image argument does not end with an img extension.")
            sys.exit(1) 
        result = func(*args) 
        return result 
    return validated 

@validate_sys_input
def validate_img_dir(func):
    @functools.wraps(func)
    def validated(*args):
        if not os.path.isdir(sys.argv[2]):
            raise ValueError("Need to pass in existing (image) directory") 
            sys.exit(1) 
        if not os.listdir(sys.argv[2]):
            raise ValueError("Image directory argument is empty") 
        result = func(*args)
        return result
    return validated 

