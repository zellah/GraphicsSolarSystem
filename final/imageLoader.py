import math
import Tkinter as tk
import numpy

class TextureImage (object):
    def __init__(self, w, h, data):
        self.width = w
        self.height = h
        self.data = data

def color_to_rgb(colorStr):
    """Returns tuple (r,g,b)"""
    return tuple(map(int, colorStr.split()));

def loadImage(fileName):
    root = tk.Tk()
    root.withdraw()

    img = tk.PhotoImage(file = fileName)
    # texture width and height must be a power of two
    data_width = math.ceil(math.sqrt(img.width()))**2;
    data_height = math.ceil(math.sqrt(img.height()))**2;
    ls = [(0,0,0)]*int(data_width * data_height);
    for y in range(img.height()) :
        yOffset = y * img.width();
        for x in range(img.width()):
            ls[x+yOffset] = color_to_rgb(img.get(x,y))
    data = numpy.array(ls, numpy.int8)
    return  TextureImage(data_width, data_height, data)
    
