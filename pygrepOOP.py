#!/usr/bin/env python3

import re
import os
import argparse

class Environment:
	'For setting up the defining the environmental details'
	
	def __init__(self):
		self.delimiter = None
		self.pwd = None
		self.setPWD()
		self.OSCheck(self.pwd)
		
	def setPWD(self):
		self.pwd = os.getcwd()
	
	def OSCheck(self,pwdPath):
		regexdPath = re.findall('^/',pwdPath)
		if  regexdPath != []:
			self.delimiter = '/'	
		else:
			self.delimiter = r'\\'

class FileHandler(Environment):
	'For handling all file functions'

	def __init__(self,fullpath):
		super().__init__()
		self.pathname = None
		self.filename = None
		self.filePreExists = None
		self.openType = None
		self.openedFile = None
		self.fileContents = ''
		self.separateFilePath(fullpath,self.delimiter)
		self.exists(fullpath)

	def separateFilePath(self,fullpath,slashdir):
		regexP = '(' + slashdir + ')'
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
		self.seekFile()
		for line in self.openedFile.readlines():
			self.fileContents = self.fileContents + line
		
	def writeFile(self,FileContent):
		self.seekFile()
		self.openedFile.write(FileContent)
	
	def seekFile(self):
		self.openedFile.seek(0)
		

class regex:
	'For dealing with regex patterns: provide a one-time use pattern, add a pattern to pygrep.conf, and apply a pattern to a file'
	
	def __init__(self,inFile,outFile,configPath):
		self.fhConfig = FileHandler(configPath)
		self.fhIN = FileHandler(inFile)
		self.fhOUT = FileHandler(outFile)
		self.dictRegex = {}
		self.pattern = ''
		self.findall = ''
		self.results = ''
		self.builtinPatterns(configPath)
		self.openInFile(inFile)
		self.openOutFile(outFile)
		
	def builtinPatterns(self,configPath):
		self.fhConfig.openFile(configPath,self.fhConfig.openType)
		self.fhConfig.readFile()
		configList = re.findall('(.+) (.+)',self.fhConfig.fileContents)
		for x,y in configList:
			self.createPattern(x,y)
		self.fhConfig.closeFile()
	
	def openInFile(self,inFile):
		self.fhIN.openFile(inFile,self.fhIN.openType)
		self.fhIN.readFile()
		
	def openOutFile(self,outFile):
		self.fhOUT.openFile(outFile,self.fhOUT.openType)
	
	def createPattern(self,name,pattern):
		self.dictRegex[name] = pattern
	
	def listPatterns(self):
		print('\nName\tPattern\n')
		for k, v in self.dictRegex.items():
			print(k + '\t' + v + '\n')
	
	def checkForPattern(self,NorP):
		if self.dictRegex[NorP] == []:
			self.pattern = NorP
		else:
			self.pattern = self.dictRegex[NorP]
	
	def employPattern(self,pattern,searchFile):
		self.findall = re.findall(pattern,searchFile)
		self.createResults()
		
	def createResults(self):
		for x in self.findall:
			#if x != '':
				#self.results = self.results + '\n' + x
			self.results = self.results + '\n' + x
	
	def showResults(self):
		print(self.results)
		
	def cleanup(self):
		self.fhIN.closeFile()
		self.fhOUT.closeFile()

class CommandLine:
	'To provide Command-line switch access'

	def __init__(self):
		self.inf = None
		self.of = None
		self.conf = None
		self.switches()
				
	def switches(self):
		parser = argparse.ArgumentParser()
		argparse.ArgumentParser(prog='pygrep.py', prefix_chars='-')
		parser.add_argument('-inf', help='Set the in file',action='store')
		parser.add_argument('-of', help='Set the out file',action='store')
		parser.add_argument('-conf', help='Set the pygrep.conf location',action='store')
		args = parser.parse_args()
		self.inf = args.inf
		self.of = args.of
		self.conf = args.conf

class UserInterface:
	'For getting any information from the user'
	
	def __init__(self):
		self.cmdOpts = CommandLine()
		self.uInInputFile = None
		self.uInOutputFile = None
		self.pygrepCONF = "pygrep.conf"
		self.setpygrepCONFfile()
		self.setInputFile()
		self.setOutputFile()
		self.run()
		
	def setInputFile(self):
		if self.cmdOpts.inf != None:
			self.uInInputFile = self.cmdOpts.inf
		else:
			self.uInInputFile = input('What is the path to the file to search through?\n>> ')
		print(self.uInInputFile)
	
	def setOutputFile(self):
		if self.cmdOpts.of != None:
			self.uInOutputFile = self.cmdOpts.of
		else:
			#uInOutputFile = input('What would you like to do with the results?\n1) Display on the Screen\n2)Write to file\n3)Both\n>> ')
			print('Creating output file in /tmp/file_test')
			self.uInOutputFile = '/tmp/file_test'
			print('temporarily defaulting to both')
		print(self.uInOutputFile)
		
	def setpygrepCONFfile(self):
		if self.cmdOpts.conf != None:
			self.pygrepCONF = self.cmdOpts.conf
		print(self.pygrepCONF)
	
	def run(self):
		# Search the inFile with the regex pattern
		searchFile = regex(self.uInInputFile,self.uInOutputFile,self.pygrepCONF)
		searchFile.listPatterns()
		regPick = input('Enter the name of a pattern, or enter a regex pattern to search with.\n>> ')
		searchFile.checkForPattern(regPick)
		searchFile.employPattern(searchFile.pattern,searchFile.fhIN.fileContents)
		# Display output file contents
		searchFile.fhOUT.writeFile(searchFile.results)
		print('\n--outFile contents below--')
		searchFile.fhOUT.readFile()
		print(searchFile.fhOUT.fileContents)
		print('\n--searchFile.showResults()--\n')
		searchFile.showResults()
		# Cleanup
		searchFile.cleanup()


	
		
UserInterface()