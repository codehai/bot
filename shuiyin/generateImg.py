#/usr/bin/env python
#coding=utf-8
import os
import sys
import random
from PIL import Image,ImageFont,ImageDraw
import json

def generateImg(tie):

        imgDir = tie['srcImg']
        texts = u'任大包，一个神奇的公众号'
        img = Image.open(imgDir)
        w,h = img.size
        fontsize = int(float(tie['randomImg']['fontsize']) * h)
        font = ImageFont.truetype('cu.ttf',fontsize)
        blank = Image.new("RGBA",(w,h),(0,0,0,1))  #创建用于添加文字的空白图像  
        draw = ImageDraw.Draw(blank)
        color = (int(tie['randomImg']['R']),int(tie['randomImg']['G']),int(tie['randomImg']['B']))
        border = (w-fontsize*12)/2
        draw.text((border,h/2), texts, font=font, fill=color)
        rotate = int(tie['randomImg']['rotate'])
        textRotate = blank.rotate(rotate)
        offsetX = int(border * float(tie['randomImg']['offsetX']))
        offsetY =  int((h/2-border/2-fontsize*2) * float(tie['randomImg']['offsetY']))
        img.paste(textRotate,(offsetX,offsetY),mask=textRotate)
        pid = os.getpid()
        if len(sys.argv)>1:           
                img.save(sys.argv[1]+str(pid)+'.jpg', 'jpeg');
        else:
                raise Exception('没有设置输出路径')

while True:
        tie = json.loads(sys.stdin.readline())
        if not tie:
                break
        try:            
                generateImg(tie)
        except Exception, e:
                raise

