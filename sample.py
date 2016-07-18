import Image
import ImageEnhance
import ImageFilter
import ImageStat
import pytesser
import sys
import numpy as np

threshold = 128
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

def temp(i):

    imgry = im.convert('L')
    imgry.save('gyzm/g' + name)
    out = imgry.point(table, '1')
    out.save('byzm/b' + name)

def getverify1(name):
    im = Image.open('yzm/'+name)
    for ii in xrange(4):
        subname = bytes(ii)+'_'+name
        region = (0+13*ii,0,13*(ii+1),20)
        subIm = im.crop(region)
        subIm.save('subyzm/'+subname)
        imgry = subIm.convert('L')
        imgry.save('gyzm/g' + subname)

        pixel,slope,maxSlope = getPixelandSlop(imgry)
        setNewImg(imgry,pixel,slope,maxSlope)

        imgry.save('nyzm/' + subname)
        thr = 200#ImageStat.Stat(imgry).mean[0]*0.85
        #print thr
        table = []
        for i in range(256):
            if i < thr:
                table.append(0)
            else:
                table.append(1)
        out = imgry.point(table, '1')
        print pytesser.image_to_string(out)
        out.save('byzm/b' + subname)
        #print imgry.size


    print name

def setNewImg(im,pixel,slope,maxSlope):

    width = im.size[0]
    height = im.size[1]
    scale = 500/maxSlope
    #print scale
    newPixel = np.zeros((width,height))

    for h in xrange(height):
        for w in xrange(width):
            #print getMaxRound(pixel,w,h)
            #print scale * slope[w, h]
            newPixel[w, h] = pixel[w,h]
            if(slope[w, h]>maxSlope*0.2):
                newPixel[w, h] = max(int(getMaxRound(pixel,w,h) - scale * slope[w, h]),0)
            #print newPixel[w, h],
        #print ''


    for h in xrange(height):
        for w in xrange(width):
            im.putpixel((w,h),newPixel[w,h])




def getPixelandSlop(im):
    width = im.size[0]
    height = im.size[1]
    slope = np.zeros((width,height))
    pixel = np.zeros((width,height))

    for h in xrange(height):
        for w in xrange(width):
            pixel[w,h] = im.getpixel((w, h))
            #print pixel[w,h],
        #print  ''

    maxSlope = 0
    for h in xrange(height):
        for w in xrange(width):
            slope[w, h] = max(slope[w,h], getMaxRound(pixel,w,h) - pixel[w,h])
            maxSlope = max(maxSlope,slope[w,h])
            #print slope[w, h],
        #print ''


    return  pixel,slope,maxSlope

def getMaxRound(mat,x,y):
    I = mat.shape[0]
    J = mat.shape[1]
    maxValue = 0
    if x-1 >=0:
        maxValue = max(maxValue, mat[x-1,y])
    if x+1< I:
        maxValue = max(maxValue, mat[x+1,y])
    if y-1 >=0:
        maxValue = max(maxValue, mat[x,y-1])
    if y+1< I:
        maxValue = max(maxValue, mat[x,y+1])
    return maxValue


def getMinRound(mat,x,y):
    I = mat.shape[0]
    J = mat.shape[1]
    minValue = 0
    if x-1 >=0:
        minValue = min(minValue, mat[x-1,y])
    if x+1< I:
        minValue = min(minValue, mat[x+1,y])
    if y-1 >=0:
        minValue = min(minValue, mat[x,y-1])
    if y+1< I:
        minValue = min(minValue, mat[x,y+1])
    return minValue





def findEdge(im):
    width = im.size[0]
    height = im.size[1]
    print (width,height)
    edgeThr = ImageStat.Stat(im).mean[0]
    for h in xrange(height):
        for w in xrange(width):
            print im.getpixel((w,h)),
        print '   '

    lower = 0
    for h in xrange(height):
        vipFlag = 0
        for w in xrange(width):
            if im.getpixel((w,h)) < edgeThr:
                vipFlag = 1
        if vipFlag == 1:
            lower= h
            break

    upper = 0
    for h in xrange(height):
        vipFlag = 0
        for w in xrange(width):
            if im.getpixel((w,height-1-h)) < edgeThr:
                vipFlag = 1
        if vipFlag == 1:
            upper = height-1-h
            break

    left = 0
    for w in xrange(width):
        vipFlag = 0
        for h in xrange(height):
            if im.getpixel((w,h)) < edgeThr:
                vipFlag = 1
        if vipFlag == 1:
            left = w
            break


    right = 0
    for w in xrange(width):
        vipFlag = 0
        for h in xrange(height):
            if im.getpixel((width-1-w, h)) < edgeThr:
                vipFlag = 1
        if vipFlag == 1:
            right = width-1-w
            break
    edge = (left,lower,right+1,upper+1)
    return edge

def findThr(im):
    edge = findEdge(im)
    tmp = im.crop(edge)
    edgeThr = ImageStat.Stat(im).mean[0]
    return edgeThr

for i in xrange(100):
    getverify1('yzm'+bytes(i)+'.jpg')
#getverify1('yzm'+bytes(10)+'.jpg')