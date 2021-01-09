# Photomosaic 

Python CLI application to turn an input image into a photomosaic using images from a source image directory. 3 example source image directories are in "img_sets/". These example image sets were sourced from Kaggle. 


## Usage 

Developed with Python 3.8 on MacOS Catalina. 
1. Create a virtual environment as ```virtualenv venv ```, 
2. Activate the environment with ```source venv/bin/activate```
3. Install packages:  ```pip install -r requirements.txt``` 

When running application, need an input image and source image dir. Can place the source image dir either in the same location as the input_img and other python files OR place in "img_sets/". 

Run from command line as "python src/main.py --input [INPUT_IMG] --directory [IMG_DIR]". E.g. ```python src/main.py --input eagle.jpg --directory img_sets/flower_imgs```

To run the unittests, you will need to add in the module level for each file in the src folder. So for instance, ```from utils.helpers import trim_width, trim_height``` --> ```from src.utils.helpers import trim_width, trim_height```.


## License 
[MIT](https://choosealicense.com/licenses/mit/)
