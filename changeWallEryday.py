#!/usr/bin/env python
#
# Changing wallpaper everyday and adjusting conky colors accordingly
#
import os
import random
import sys
import math
from PIL import Image


# Papes path and extensions definition

papePath = os.environ.get('WALLS_PATH')
fileExtensions = (".jpg",".png")


# Get list of papes in papePath
# Returns list and count of papes

def directory(path, extension):
	list_dir = os.listdir(path)
	count = 0
	valid_papes = []
	for file in list_dir:
		if file.endswith(extension):
			count += 1
			valid_papes.append(file)
		if not list_dir:
			print("No usable image files found.")
	return (valid_papes, count)


# Randomize selection of a pape
# Returns path to random pape

def randomize_pape():
	papes, count = directory(papePath, fileExtensions)
	file_number = random.randint(0, count-1)
	return papePath + papes[file_number]


# Set a background using feh

def set_background(img):
	os.system('DISPLAY=:0 feh --bg-fill ' + img)
