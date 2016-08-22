#ecoding=utf-8
import os
import multiprocessing
from multiprocessing import Pool,Process,Manager,Queue
from subprocess import *

class screenshot(object):
	"""docstring for screenshot"""
	def __init__(self):
		super(screenshot, self).__init__()

	def get(self,filenums,filelist):
		if not filenums.empty():
			filenum = filenums.get(False)
			path = filelist[filenum]
			print(filenum,path)
			process = Popen(["casperjs" ,"2chcn.js",str(filenum)], shell=False, stdout = PIPE,stderr=STDOUT) 
			flag = 1
			while flag:  
		        		line = process.stdout.readline()
		        		if not line:  
		            			break  
		        		result = line.decode('UTF-8').replace('\n','')
		        		print (result)
		        		flag = 0
		else:
			return


if __name__=='__main__':
	manager = Manager()
	filenums = manager.Queue()
	pool_size=multiprocessing.cpu_count()
	print pool_size
	pool = Pool(processes=pool_size)
	for i in range(1,100):
		filenums.put(i)
	filelist = manager.list()
	for parent, dirnames, filenames in os.walk('./wx2ch_files/background'):
		for filename in filenames:
			if filename.find('img')!=-1:
				filelist.append(filename)
	print len(filelist)
	for i in xrange(8):
		pool.apply_async(screenshot.get, (filenums,filelist, ))

	# while len(filenums) > 0:
	# 	# print('value: %s' % len(values))
	# 	if not indexQ.empty():
	# 		# print('index: %s' % indexQ.qsize())
	# 		pool.apply_async(getscreen, (indexQ, ))
	# 		# Process(target=getscreen()).start()
	while True:
		if filenums.empty():
			pool.close()
			pool.join()
			break
		else:
			print filenums.qsize()
	
			
# with open('./wx2ch_files/wx2ch.css','w') as f:
# 	f.write('body{background:url(./background/'+filename+');}')

# screenshot()
