#!/usr/bin/env python3

import re
import os
import argparse

class FileHandler:
	
	def __init__(self,fullpath):
		self.pathname = None
		self.filename = None
		self.delimiter = None
		self.fileExists = False
		self.OSCheck(fullpath)
		self.separateFilePath(fullpath,self.delimiter)
		self.exists(fullpath)
	
	def OSCheck(self,fullpath):
		regexdPath = re.findall('^/',fullpath)
		if  regexdPath != []:
			self.delimiter = '/'	
		else:
			self.delimiter = '\\'

	def separateFilePath(self,fullpath,delimiter):
		#regexP = '(' + delimiter + '.+' + delimiter + ')(.+)'
		regexP = '(' + delimiter + ')'
		regexdPath = re.split(regexP,fullpath)
		lastfield = len(regexdPath) - 1 
		self.filename = regexdPath[lastfield]
		self.pathname = ''.join(regexdPath[0:lastfield])
	
	def exists(self,fullpath):
		if os.path.isfile(fullpath) == True:
			self.fileExists = True

#testpath = 'c:\program files\veritas\netbackup\bp.conf'
#testpath = '/usr/openv/netbackup/bp.conf'

uInput = input('What is the path to the file?\n>> ')
test = FileHandler(uInput)
#test = FileHandler(testpath)
print('path: ' + test.pathname)
print('filename: ' + test.filename)
print('file exists: ' + str(test.fileExists))