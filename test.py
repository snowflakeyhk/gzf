#-*- coding:utf-8 -*-
import Image
import ImageEnhance
import ImageFilter
import sys


threshold = 210
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

image_name = 'yzm1.tiff'
im = Image.open(image_name)
imgry = im.convert('L')
out = imgry.point(table, '1')
