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

def set_lockscreen(img):
	os.system('cp ' + img + ' ' + os.environ['LOCKSCREEN_BG'])


# Crop conky part of pape
# Returns 4-tuple with x,y coords of lower left and upper right pixel

def crop_for_conky(img):
	min_x, min_y, max_x, max_y = img.getbbox()
	lower_left = (max_x * (4 / 5), max_y * (1 / 2))
	upper_right = (max_x, max_y)
	return lower_left + upper_right


# Get pixel mean of an image
# Returns a tuple of average pixel color in each band (R, G, B)

def pixel_mean(img, bbox=None):
	if bbox is None:
		pixels = list(img.getdata())
	elif type(bbox) is tuple and len(bbox) == 4:
		pixels = list(img.crop(bbox).getdata())

	r = 0
	g = 0
	b = 0
	pixel_count = 0

	for pixel in pixels:
		r += pixel[0]
		g += pixel[1]
		b += pixel[2]
		pixel_count += 1

	avg_red = r / pixel_count
	avg_green = g / pixel_count
	avg_blue = b / pixel_count
	pixel_mean = (math.floor(avg_red), math.floor(avg_green), math.floor(avg_blue))

	return pixel_mean


# Inverses the color of pixel mean
# Returns a tuple of inversed average pixel color in each band (R, G, B)
# Returns none if argument isn't valid

def inverse_mean(mean):
	if type(mean) is tuple and len(mean) == 3:
		return (255 - mean[0], 255 - mean[1], 255 - mean[2])


# Make sure pixel is in RGB range

def clamp(pixel):
	return max(0, min(pixel, 255))


# Actually set a background and lockscreen

random_pape = randomize_pape()
set_background(random_pape)
set_lockscreen(random_pape)

# Begining of conky color change

pape_source = Image.open(random_pape)
conky_r, conky_g, conky_b = inverse_mean(pixel_mean(pape_source,crop_for_conky(pape_source))) # Get RGB color for conky

# Set colors for conky in hex

color1_hex = '{0:02x}{1:02x}{2:02x}'.format(conky_r, conky_g, conky_b) # Font color
color2_hex = '{0:02x}{1:02x}{2:02x}'.format(clamp(conky_r - 100), clamp(conky_g - 100), clamp(conky_b - 100)) # Current day in calendar

# Write to conky config

with open(os.environ['CONKY_CONFIG'], 'r+') as conky_config:
	config = conky_config.readlines()
	line_number = 0
	for line in config:
		if 'color1 = ' in line:
			break
		else:
			line_number += 1

	color1_line = config[line_number]
	color1_line = color1_line.split('\'')
	color1_line[1] = '\'' + color1_hex + '\''
	color1_line = "".join(color1_line)

	color2_line = config[line_number + 1]
	color2_line = color2_line.split('\'')
	color2_line[1] = '\'' + color2_hex + '\''
	color2_line = "".join(color2_line)

	config[line_number] = color1_line
	config[line_number + 1] = color2_line

	conky_config.seek(0)
	for line in config:
		conky_config.write(line)
