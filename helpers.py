
def round_to_nearest_10(num):
    rem = num % 10 
    if rem < 5:
        return int(num / 10) * 10 
    else:
        return int((num + 10) / 10) * 10 

def trim_name(img_class):
    replacements = [(self.img_dir, ""), ("/", ""), ("img_sets", "")] 
    new_name = img_class.name
    for old, new in replacements:
        new_name = re.sub(old, new, new_name) 
    return new_name 

def trim_width(img, width, height):
    if width <= height: return img
    diff = width - height 
    right = width - diff 
    left = top = 0 
    return img.crop((left, top, right, height))  

def trim_height(img, width, height):
    if height <= width: return img
    diff = height - width 
    bottom = height - diff 
    left = top = 0 
    return img.crop((left, top, width, bottom)) 

