#! /usr/bin/env python
import os
import datetime
from PIL import Image
import pyocr
import re
import pyocr.builders
from selenium import webdriver

class Cddh(object):
	"""docstring for Cddh"""
	def __init__(self):
		#初始化浏览器和ocr tool
		self.driver = webdriver.Firefox(executable_path='./geckodriver')
		tools = pyocr.get_available_tools()
		if len(tools) == 0:
			sys.exit(1)
		self.tool = tools[0]
		self.im = None
		self.path = None
		self.crop_xy = [(35, 300, 770, 610), (35, 550, 770, 720), (35, 730, 770, 830), (35, 840, 770, 940)]

	def screenshot(self):
		self.path = "./screenshot/"+datetime.datetime.now().isoformat()+".png"
		cmd = "screencapture "+self.path
		os.system(cmd)
		self.im = Image.open(self.path)

	def crop_im(self, xy):
		image = Image.new('RGBA',(735, 290), '#FFFFFF')
		im = Image.open(self.path)
		# print(im.size)
		cropedIm = im.crop(xy)
		image.paste(cropedIm, (0, 0))
		return image

	def ocr_qa(self):
		results = []
		for xy in self.crop_xy:
			im = self.crop_im(xy)
			r = self.tool.image_to_string(im, lang="chi_sim") 
			r = r.replace(" ", "")
			r = re.sub("\d+\.", "", r)
			results.append(r)
		return results

	def factory(self):
		self.screenshot()
		results = self.ocr_qa()
		q = results[0]
		print("Q:", q)
		a = results[1:4]
		print(a)
		score = [0, 0, 0]
		answer = ["A", "B", "C"]
		max_score = 100
		url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd="+q
		self.driver.get(url)
		abstracts = self.driver.find_elements_by_class_name('c-abstract')
		for abstract in abstracts:
			for index,cells in enumerate(a):
				a_max_score = 0
				for cell in cells:
					if cell in abstract.text:
						a_max_score += max_score/len(cells)
				if a_max_score > score[index]:
					score[index] = a_max_score
		print(score)
		for i,s in enumerate(score):
			if s==100:
				print(answer[i])
				break
		else:
			max_s = max(score)
			print(answer[score.index(max_s)])

	def quit(self):
		self.driver.quit()


def main():
	cddh = Cddh()
	while True:
		command = input('Enter command:')
		if command in ["q", "Q"]:
			cddh.quit()
			break
		else:
			cddh.factory()

if __name__ == '__main__':
	main()

