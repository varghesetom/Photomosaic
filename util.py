
def convert_to_rgb(im):
    try:
        return im.convert("RGB") 
    except ValueError as e:
        print(f"Error in trying to convert image to RGB: {e}") 
        pass 

def identify_files_in_img_dir():
    if len(sys.argv) < 2: 
        raise ValueError("Need image directory to iterate through")  
    directory = sys.argv[1] 
    for infile in os.listdir(sys.argv[1]):
        try:
            with Image.open(f"{directory}/{infile}") as im:
                print(infile, im.format, "%dx%d" % im.size, im.mode) 
        except OSError as e:
            print(e)
            pass 

def crop_img():
    try:
        img = get_img() 
        with Image.open(img) as im:
            box = (100, 100, 400, 400)
            region = im.crop(box) 
            region.show() 
    except OSError as e:
        print(e)
        pass 

def messing_with_rgb_bands():
    try:
        img = get_img()
        with Image.open(img) as im:
            print(f"color mode of {img} is {im.mode}") 
            rgb_im = convert_to_rgb(im) 
            r, g, b = rgb_im.split()
            rgb_im = Image.merge("RGB", (b, g, r)) 
            rgb_im.show() 
    except OSError as e:
        print(e)
        pass 

def most_frequent_color(self):
    '''
    if exceed default limit of 256 will return None so provide 
    the maximum number of colors which is equivalent to the number of pixels 
    '''
    width, height = self.img.size
    rgb_pixels = self.img.getcolors(width * height) 
    most_frequent_pixel = rgb_pixels[0]
    for count, rgb in rgb_pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, rgb)
    return most_frequent_pixel[1]


