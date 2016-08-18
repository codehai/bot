#-*- coding: utf-8 -*-

from PIL import Image, ImageFilter,ImageChops

class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)
def trim(im):
        bg = Image.new(im.mode, im.size, (0,0,0))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
                return im.crop(bbox)

simg = 'demo.jpeg'
dimg = 'demo_blur.jpg'
image = Image.open(simg)
w,h = image.size
print w
print h
if w*1.0/h<1200.0/280:
    nh = w*280/1200
    region = (0,(h-nh)/2,w,nh+(h-nh)/2)
    image = image.crop(region)
else:
    nw = 1200*h/280
    region = ((w-nw)/2,0,nw+(w-nw)/2,h)
    image = image.crop(region)

image = image.filter(MyGaussianBlur(radius=35))
image = image.resize((1200, 280))
print image.size
image.show()
image.save('result.jpg')
