# resizes testing images to train Haar Classifier

import os
import cv2
import numpy as np
import string

# from the 112 website

# https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#listFiles
def listFiles(path):
    if (os.path.isdir(path) == False):
        # base case:  not a folder, but a file, so return singleton list with its path
        return [path]
    else:
        # recursive case: it's a folder, return list of all paths
        files = [ ]
        for filename in os.listdir(path):
            files += listFiles(path + "/" + filename)
        return files

def main():
    fpaths = listFiles(os.getcwd())
    # cuts off my files
    fpaths = fpaths[:-2]
    print (fpaths)
    # makes sure the path doesn't have duplicates
    assert(len(fpaths) == len(set(fpaths)))
    for path in fpaths:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        small = cv2.resize(img, (96, 96))
        index = string.rfind(path, '.')
        bmps = path[:index] + '.bmp'
        cv2.imwrite(bmps, small)
    print("Done")
        
    
if __name__ == '__main__':
    main()