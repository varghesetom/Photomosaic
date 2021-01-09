# Photomosaic 

Python CLI application to turn an input image into a photomosaic using images from a source image directory. 3 example source image directories are in "img_sets/". These example image sets were sourced from Kaggle. 


## Usage 

Developed with Python 3.8 on MacOS Catalina. 
1. Create a virtual environment as ```virtualenv venv ```, 
2. Activate the environment with ```source venv/bin/activate```
3. Install packages:  ```pip3 install -r requirements.txt``` 

When running application, need an input image and source image dir. Can place the source image dir either in the same location as the input_img and other python files OR place in "img_sets/". 

Run from command line as "python3 src/main.py --input [INPUT_IMG] --directory [IMG_DIR]". 

E.g. ```python3 src/main.py --input eagle.jpg --directory img_sets/flower_imgs```

To run the unittests, you will need to add in the module level for each file in the src folder. 

So for instance, ```from utils.helpers import trim_width, trim_height``` --> ```from src.utils.helpers import trim_width, trim_height```.


## References

[Efficient and precise calculation of the euclidean distance](https://stackoverflow.com/questions/37794849/efficient-and-precise-calculation-of-the-euclidean-distance)

[Unpacking (Tuples) in Python: Beyond Parallel Assignment](https://stackabuse.com/unpacking-in-python-beyond-parallel-assignment/)

[How can I use named arguments in a decorator?](https://stackoverflow.com/questions/627501/how-can-i-use-named-arguments-in-a-decorator)

[Advanced Uses of Python Decorators](https://www.codementor.io/@sheena/advanced-use-python-decorators-class-function-du107nxsv)

[Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/#classes-as-decorators)

[Benchmarking Functions for Computing Average RGB Value of Images](https://stackoverflow.com/questions/12703871/benchmarking-functions-for-computing-average-rgb-value-of-images)

[Python unittest Assertions](https://kapeli.com/cheat_sheets/Python_unittest_Assertions.docset/Contents/Resources/Documents/index)

[Logging to multiple log files from different classes in Python](https://stackoverflow.com/questions/17035077/logging-to-multiple-log-files-from-different-classes-in-python)

[Python Logging – Simplest Guide with Full Code and Examples](https://www.machinelearningplus.com/python/python-logging-guide/)

[Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing/)


[How to write to a file, using the logging Python module?](https://stackoverflow.com/questions/6386698/how-to-write-to-a-file-using-the-logging-python-module)


## TODO:

1.  Add in more unittests that test for instance type.


## License 
[MIT](https://choosealicense.com/licenses/mit/)
