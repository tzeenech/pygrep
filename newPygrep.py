#!/usr/bin/env python3

import re
import os
import argparse

class FileHandler:
	'For handling all file functions'
	"""
	pathname = None
	filename = None
	delimiter = None
	filePreExists = None
	openType = None
	openedFile = None
	"""
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
		self.fileContents = ""
	
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
			self.fileContents = self.fileContents + line
		
	def writeFile(self,fileContent):
		self.openedFile.write(fileContent)
	
	def seekFile(self):
		self.openedFile.seek(0)
		
"""
class config:
	
	def __init__(self,pygrepconfPath):
		self.openpygrepCONF = fh.openFile(pygrepconfPath,'r')
		self.debug()
		
	def buildDefaultRegex:
		
	
	def debug(self):
		#print('--config.test--\npathPYGREPCONF: ' + str(self.openpygrepCONF))
		print('\n' + str(self.openpygrepCONF))
"""

class regex(FileHandler):
	'For dealing with regex patterns: provide a one-time use pattern, add a pattern to pygrep.conf, and apply a pattern to a file'
	
	def __init__(self,fullpath):
		super().__init__(fullpath)
		self.openFile(fullpath,self.openType)
		self.dictRegex = {}
		self.pattern = None
		self.findall = None
	
	def createPattern(self,name,pattern):
		self.dictRegex[name] = pattern
	
	def listPatterns(self):
		print('\nName\tPattern\n')
		for k, v in self.dictRegex.items():
			print(k + '\t' + v)
	
	def checkInPattern(self,NorP):
		if self.dictRegex[NorP] == []:
			self.pattern = NorP
		else:
			self.pattern = self.dictRegex[NorP]
	
	def employPattern(self,pick,searchFile):
		self.checkInPattern(pick)
		self.findall = re.findall(self.pattern,searchFile)
		
	def showResults(self):
		for line in self.findall:
			print(line)


# Build the built-in regex dictionary
"""pygrep_conf = 'pygrep.conf'
pbd = FileHandler(pygrep_conf)
pbd.openFile(pygrep_conf,pbd.openType)
configList = re.findall('(.+)\s(.+)',pbd.readFile())
brx = regex()
for x,y in configList:
	brx.createPattern(x,y)
pbd.closeFile()
brx.listPatterns()
"""
brx = regex('pygrep.conf')
brx.readFile()

configList = re.findall('(.+)\s(.+)',brx.fileContents)

for x,y in configList:
	brx.createPattern(x,y)

brx.listPatterns()

# Get the file to search through
uInput = input('What is the path to the file to search through?\n>> ')
fh = FileHandler(uInput)
print('path: ' + fh.pathname)
print('filename: ' + fh.filename)
print('file pre-existing: ' + str(fh.filePreExists))

fp = fh.pathname + fh.filename
fh.openFile(fp,fh.openType)
if fh.openType == 'r':
	print('\n--openedFile contents below--')
	print(fh.readFile())
else:
	file_text = 'This is a test\nPlease continue testing.\n'
	fh.writeFile(file_text)
	fh.seekFile()
	print('\n--openedFile contents below--')
	print(fh.readFile())


regX = regex()
regX.createPattern('test','(.+)')
regX.listPatterns()
regPick = input('Enter the name of a pattern, or enter a regex pattern to search with.\n>> ')
regX.employPattern(regPick,fh.openedFile.read())
regX.showResults()

fh.closeFile()
