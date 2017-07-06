#!/usr/bin/env python3

import re
import os
import argparse

class FileHandler:
	
	def __init__(self,fullpath):
		self.pathname = None
		self.filename = None
		self.delimiter = None
		self.filePreExists = None
		self.openType = None
		self.openedFile = None
		self.OSCheck(fullpath)
		self.separateFilePath(fullpath,self.delimiter)
		self.exists(fullpath)
		#self.openFile(fullpath,self.openType)
	
	def OSCheck(self,fullpath):
		regexdPath = re.findall('^/',fullpath)
		if  regexdPath != []:
			self.delimiter = '/'	
		else:
			self.delimiter = r'\\'

	def separateFilePath(self,fullpath,delimiter):
		print('fullpath: ' + fullpath)
		print('delimiter: ' + delimiter)
		#regexP = '(' + delimiter + '.+' + delimiter + ')(.+)'
		regexP = '(' + delimiter + ')'
		print('regexP: ' + regexP)
		regexdPath = re.split(regexP,fullpath)
		lastfield = len(regexdPath) - 1 
		self.filename = regexdPath[lastfield]
		self.pathname = ''.join(regexdPath[0:lastfield])
	
	def exists(self,fullpath):
		if os.path.isfile(fullpath) == True:
			self.filePreExists = True
			self.openType = 'r'
		else:
			self.filePreExists = False
			self.openType = 'w+'
	
	def openFile(self,fullpath,openType):
		self.openedFile = open(fullpath,openType)
		
	def closeFile(self):
		self.openedFile.close()
	
	def readFile(self):
		for line in self.openedFile.readlines():
			print(line)
		
"""		
class config:
	
	def __init__(self,pygrepconfPath):
		self.openpygrepCONF = fh.openFile(pygrepconfPath,'r')
		self.debug()
	
	def debug(self):
		#print('--config.test--\npathPYGREPCONF: ' + str(self.openpygrepCONF))
		print('\n' + str(self.openpygrepCONF))
	

class regex:
	
	def __init__(self):
		pass
	
	def createPattern(self):
		pass
"""
#testpath = 'c:\program files\veritas\netbackup\bp.conf'
#testpath = '/usr/openv/netbackup/bp.conf'


uInput = input('What is the path to the file?\n>> ')
fh = FileHandler(uInput)
print('path: ' + fh.pathname)
print('filename: ' + fh.filename)
print('file pre-existing: ' + str(fh.filePreExists))

pygrep_conf = os.getcwd() + fh.delimiter + 'pygrep.conf'
#cfg = config(pygrep_conf)

fp = fh.pathname + fh.filename
fh.openFile(fp,fh.openType)
file_text = 'This is a test\nPlease continue testing.\n'
fh.openedFile.write(file_text)
fh.openedFile.seek(0)
print('\n--openedFile contents below--')
fh.readFile()
fh.closeFile()
