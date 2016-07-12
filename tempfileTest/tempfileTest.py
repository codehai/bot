import os
import tempfile
import time
from PIL import Image,ImageFont,ImageDraw

img = Image.open('/home/hao/bot/tempfileTest/1.jpg')
temp = tempfile.NamedTemporaryFile(suffix='.jpg',dir='/home/hao/bot/tempfileTest')
img.save(temp.name)
time.sleep(5)
temp.close()
print 'Exists after close:', os.path.exists(temp.name)