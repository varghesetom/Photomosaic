# Photomosaic 

Python CLI application to turn an input image into a photomosaic using images from a source image directory. 3 example source image directories are in "img_sets/". These example image sets were sourced from Kaggle. 

## Usage 

Developed with Python 3.8 on MacOS Catalina. 
1. Create a virtual environment as ```virtualenv venv ```, 
2. Activate the environment with ```source venv/bin/activate```
3. Install packages:  ```pip install -r requirements.txt``` 

When running application, need an input image and source image dir. Can place the source image dir either in the same location as the input_img and other python files OR place in "img_sets/". 

Run from command line as "python photomosaic.py [INPUT_IMG] [IMG_DIR]". E.g. ```python photomosaic.py eagle.jpg img_sets/flower_imgs/```

## License 
[MIT](https://choosealicense.com/licenses/mit/)
