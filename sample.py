import Image
import ImageEnhance
import ImageFilter
import sys
from pytesser import *

threshold = 210
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)



def getverify1(name):
    im = Image.open('D:/ML/untitled/yzm/'+name)
    imgry = im.convert('L')
    imgry.save('D:/ML/untitled/yzm/g' + name)
    out = imgry.point(table, '1')
    out.save('D:/ML/untitled/yzm/b' + name)
    print name


    print text
    return text

for i in xrange(20):
    getverify1('yzm'+bytes(i)+'.tiff')
