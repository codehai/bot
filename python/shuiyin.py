#/usr/bin/env python
#coding=utf-8
import os
import sys
import random
from PIL import Image,ImageFont,ImageDraw

imgDir = sys.argv[8]
pid =  sys.argv[9]
texts = u'任大包，一个神奇的公众号'
img = Image.open(imgDir)
w,h = img.size
# fontsize = random.randint(int(h*0.064),int(h*0.11))
fontsize = int(float(sys.argv[1]) * h)
font = ImageFont.truetype('cu.ttf',fontsize)
blank = Image.new("RGBA",(w,h),(0,0,0,1))  #创建用于添加文字的空白图像  
draw = ImageDraw.Draw(blank)
# color = rndColor()
color = (int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7]))
border = (w-fontsize*12)/2
draw.text((border,h/2), texts, font=font, fill=color)
# rotate = rndRotate()
rotate = int(sys.argv[2])
textRotate = blank.rotate(rotate)
# offsetX = random.randint(-border,border) 
# offsetY = random.randint(-(h/2-border/2-fontsize*2),h/2-border/2-fontsize*2)
offsetX = int(border * float(sys.argv[3]))
offsetY =  int((h/2-border/2-fontsize*2) * float(sys.argv[4]))
img.paste(textRotate,(offsetX,offsetY),mask=textRotate)
img.save('/dev/shm/'+pid+'.jpg', 'jpeg');
