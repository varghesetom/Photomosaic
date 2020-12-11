
def round_to_nearest_10(num):
    rem = num % 10 
    if rem < 5:
        return int(num / 10) * 10 
    else:
        return int((num + 10) / 10) * 10 


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

