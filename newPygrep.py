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
		print(regexdPath)
		if  regexdPath != []:
			self.delimiter = '/'	
		else:
			self.delimiter = '\\'

	def separateFilePath(self,fullpath,delimiter):
		regexP = '(' + delimiter + '.+' + delimiter + ')(.+)'
		regexdPath = re.split(regexP,fullpath)
		print(regexdPath)
		self.pathname = regexdPath[1]
		self.filename = regexdPath[2]
	
	def exists(self,fullpath):
		if os.path.isfile(fullpath) == True:
			self.fileExists = True

#testpath = 'c:\program files\veritas\netbackup\bp.conf'
#testpath = '/usr/openv/netbackup/bp.conf'

uInput = input('What is the path to the file?\n>> ')
test = FileHandler(uInput)
#test = FileHandler(testpath)
print(test.pathname + test.filename)
print(test.fileExists)