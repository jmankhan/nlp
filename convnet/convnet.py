import numpy as np
from PIL import Image

img = Image.open("img.jpg").convert("RGB")
# r, g, b = img.getpixel((100, 10))

x = y = 0
while y < img.size[1]:
	while x < img.size[0]:
		print x, y
		x+=5
		y+=5

print 'size', img.size