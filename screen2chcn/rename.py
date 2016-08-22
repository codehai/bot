# encoding: utf-8  
import os  
import os.path  
  
curDir = os.getcwd()  
for parent, dirnames, filenames in os.walk(curDir):    
	for filename in filenames:
		print filename 
		# if filename.find(oldId)!=-1:  
		# 	newName = filename.replace(oldId, newId)  
		# 	print(filename, "---->", newName)  
		# 	os.rename(os.path.join(parent, filename), os.path.join(parent, newName))
