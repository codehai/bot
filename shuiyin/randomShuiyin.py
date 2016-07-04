#/usr/bin/env python
#coding=utf-8
import os
import sys
import random
def rndColor():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
def rndRotate():
        return random.randint(-30,30)

# imgDir = sys.argv[1] #图片路径
imgDir = './0b7b02087bf40ad13ef034aa552c11dfa9ecce67.jpg'
comand = 'python shuiyin.py'
fontsize = random.uniform(0.064,0.11)
color = rndColor() 
rotate = rndRotate() 
offsetX = random.uniform(-1,1) 
offsetY = random.uniform(-1,1)    
os.system("%s %s %s %s %s %s %s %s %s" %(comand,fontsize,rotate,offsetX,offsetY,color[0],color[1],color[2],imgDir))
