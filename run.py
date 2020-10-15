#!/usr/bin/env python 

'''
Run this file as "python run_pytest.py [IMG_file] test_photomosaic.py" 
Because we need to import the sys.argv image argument and because pytest doesn't easily recognize them as CLI args instead of test files, we will have to import pytest here and store the image sys.argv argument here. In the original PhotoMosaic.py file, this image argument is considered to be "sys.argv[1]" so will need to match the exact number as well here. 
'''
import pytest 
import sys 

def main():
    arg = sys.argv[1] 
    pytest.main([sys.argv[2]])  ## call our test_photomosaic.py file 

if __name__ == "__main__":
    main() 
