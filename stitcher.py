# -*- coding: utf-8 -*-
"""
A simple script which converts all the images in the folder it is run from
into a single image. Images should be in "tile map set" folder format with
0-based numbered folders and images running from 0 - n, named as e.g. "0.png"
 
Used for http://forums.bistudio.com/showthread.php?178671-Tiled-maps-Google-maps-compatible-(WIP)
 
License: public domain
"""

from PIL import Image


class ImageDeTiler(object):

    ##
    ### Change the following numbers to match your tile set
    ## 
    NUMBER_OF_FOLDERS = 32
    NUMBER_OF_IMAGES_PER_FOLDER = 30
    ##
    ###
    ##

    folders = [str(x) for x in range(0, NUMBER_OF_FOLDERS + 1)]
    imageIds = [str(x) for x in range(NUMBER_OF_IMAGES_PER_FOLDER, -1, -1)] 
    
    # dimensions of a single tile, change if required
    tileDim = 256

    finalWidth = tileDim * len(folders)
    finalHeight = tileDim * len(folders) 

    def __init__(self):
        """
        Automatically traverses the directory the script is run from
        and tiles all the images together into a massive super image
        """
        print "----------------------------------------------"
        print " Preparing output image, %s by %s" % (
            self.finalWidth, self.finalHeight
        )
        print "----------------------------------------------"
        result = Image.new("RGBA", (self.finalWidth, self.finalHeight))
        
        for i, x in enumerate(self.folders):
            print "----------------------------------------------"
            print " Processing row " + str(i)
            print "----------------------------------------------"
            row = self.get_tile(x)
            
            result.paste(row, (i * self.tileDim, 0))
            
        result.save("output.png")
        
        print "----------------------------------------------\n" * 2
    
    def get_tile(self, path):
        """
        Takes a path and returns an image which contains all the tiled images
        """
        result = Image.new("RGBA", (self.tileDim, self.finalHeight))
        
        for i, x in enumerate(self.imageIds):
            newPath = path + "\\" + x + ".png"
            img = Image.open(newPath)
            
            x, y= img.size
            print "%s: %s, %s x %s" % (newPath, img.mode, x, y)
            
            result.paste(img, (0, i * self.tileDim))
            
        return result
            
if __name__ == "__main__":
    ImageDeTiler()