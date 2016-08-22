#coding=utf-8
import multiprocessing
import time
from subprocess import *
import os
from PIL import Image
import colorsys


def get_dominant_color(image):
#颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')
#生成缩略图，减少计算量，减小cpu压力
    image.thumbnail((200, 200))
    max_score = None
    dominant_color = None
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过纯黑色
        if a == 0:
            continue
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        # 忽略高亮色
        if y > 0.9:
            continue
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (255-r, 255-g, 255-b)
            if r<150 and r>100 and 100<g and g<150 and b<150 and b>100:
                dominant_color = (0,0,0)
            elif r==b and b==g:
                if r<127:
                    dominant_color = (255,255,255)
                else:
                    dominant_color = (0,0,0)
    return dominant_color
 
def get(filenum,filelist,i):
    path = filelist[filenum]
    print(filenum,path)
    fontcolor = str(get_dominant_color(Image.open('./wx2ch_files/background/'+path)))
    print fontcolor
    with open('./wx2ch_files/wx2ch'+str(i+1)+'.css','w') as f:
        f.write('body{background:url(./background/'+path+');}\np,span{color:rgb'+fontcolor+'}')
    process = Popen(["casperjs" ,"2chcn.js", str(filenum) ,str(i+1)], shell=False, stdout = PIPE,stderr=STDOUT) 
    flag = 1
    while flag:  
                line = process.stdout.readline()
                if not line:  
                        break  
                result = line.decode('UTF-8').replace('\n','')
                flag = 0

def func(i,filenums,filelist):
    while True:
        if not filenums.empty():
            filenum = filenums.get()
            get(filenum,filelist,i)
            time.sleep(1)
        else:
            break
    return "done " + str(i)
 
if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=8)
    manager = multiprocessing.Manager()
    filenums = manager.Queue()
    filelist = manager.list()
    for parent, dirnames, filenames in os.walk('./wx2ch_files/background'):
        for filename in filenames:
            if filename.find('img')!=-1:
                filelist.append(filename)
    for i in range(1,10):
        filenums.put(i)
    result = []
    for i in xrange(10):
        result.append(pool.apply_async(func, (i, filenums, filelist)))
    pool.close()
    pool.join()
    for res in result:
        print res.get()
    print "Sub-process(es) done."