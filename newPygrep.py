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
		self.pwd = None
		self.fileContents = ''
		self.setPWD()
		self.OSCheck(self.pwd)
		self.separateFilePath(fullpath,self.delimiter)
		self.exists(fullpath)

	def setPWD(self):
		self.pwd = os.getcwd()
	
	def OSCheck(self,pwdPath):
		regexdPath = re.findall('^/',pwdPath)
		if  regexdPath != []:
			self.delimiter = '/'	
		else:
			self.delimiter = r'\\'

	def separateFilePath(self,fullpath,delimiter):
		regexP = '(' + delimiter + ')'
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
			print(k + '\t' + v + '\n')
	
	def checkInPattern(self,NorP):
		if self.dictRegex[NorP] == []:
			self.pattern = NorP
			print('If statement: ' + self.pattern)
		else:
			self.pattern = self.dictRegex[NorP]
			print('Else statement: ' + self.pattern)
	
	def employPattern(self,pattern,searchFile):
		#self.checkInPattern(pick)
		self.findall = re.findall(pattern,searchFile)
		
	def showResults(self):
		for line in self.findall:
			print(line)


# Build the built-in regex dictionary
brx = regex('pygrep.conf')
brx.readFile()
configList = re.findall('(.+) (.+)',brx.fileContents)
for x,y in configList:
	brx.createPattern(x,y)

# Get the file to search through
uInput = input('What is the path to the file to search through?\n>> ')
inFile = FileHandler(uInput)
print('path: ' + inFile.pathname)
print('filename: ' + inFile.filename)
print('file pre-existing: ' + str(inFile.filePreExists))
fp = inFile.pathname + inFile.filename
inFile.openFile(fp,'r')
print('\n--openedFile contents below--')
inFile.readFile()
print(inFile.fileContents)

# Create an output file
#uOutput = input('What would you like to do with the results?\n1) Display on the Screen\n2)Write to file\n3)Both\n>> ')
print('Creating output file in /tmp/file_test')
uOutput = '/tmp/file_test'
"""
print('temporarily defaulting to both')
outFile = FileHandler(uOutput)
print('path: ' + outFile.pathname)
print('filename: ' + outFile.filename)
print('file pre-existing: ' + str(outFile.filePreExists))
ofp = outFile.pathname + outFile.filename
outFile.openFile(ofp,'w+')
"""

# Search the inFile with the regex pattern
searchFile = regex(uOutput)
brx.listPatterns()
regPick = input('Enter the name of a pattern, or enter a regex pattern to search with.\n>> ')
brxregPick = brx.checkInPattern(regPick)
print('brxregPick: ' + str(brxregPick))
searchFile.employPattern(brx.pattern,inFile.fileContents)
searchFile.showResults()

# Display output file contents
print('\n--outFile contents below--')
outFile.seek()
outFile.readFile()
print(outFile.fileContents)

inFile.closeFile()
searchFile.closeFile()
