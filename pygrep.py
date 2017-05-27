#!/usr/bin/env python3

import re
import os

class uInput:
	def __init__(self):
		self.os = None
		self.pwd = None
		self.uInFile = None
		self.slashdir = None
		self.confFile = None
		self.openConfFile = None
		self.uinBuiltInYN = None
		self.pickPattern = None
		self.setOS()
		self.setPWD()
		self.setslashdir()
		self._openConfFile()
		self._uinFile()
		self._uinRegex()
		self.debug()

	def setOS(self):
		self.os = os.name

	def setPWD(self):
		self.pwd = os.getcwd()

	def setslashdir(self):
		if self.os == 'nt':
			self.slashdir = '\\'
		else:
			self.slashdir = '/'

	def _openConfFile(self):
		self.confFile = self.pwd + self.slashdir + 'pygrep.conf'
		if os.path.isfile(self.confFile) == True:
			self.openConfFile = open(self.confFile, 'r')
			print('Found an existing pygrep.conf file...\n')
			for line in self.openConfFile.readlines():
				print(line)
		else:
			self.confFile = self.pwd + self.slashdir + 'pygrep.conf'
			self.openConfFile = open(self.confFile, 'a')

	def _uinFile(self):
		uInFile = input('What file would you like to search through?\nPlease provide the full path if the file is not in the current directory, \n"' + self.pwd + '."')
		if os.path.isfile(uInFile) != True:
			pwduInFile = self.pwd + uInFile
			if os.path.isfile(pwduInFile) != True:
				print('The file path provided,' + '(' + self.pwd + ')' + uInFile + ' does not exist, please try again.')
				self._uinFile()
			else:
				self.uInFile = pwduInFile
		else:
			self.uInFile = uInFile

	def _uinRegex(self):
		uinRegexYN = input('Would you like to use a built-in regex pattern, or provide your own? Y/N (N) ')
		if uinRegexYN == '' or str.upper(uinRegexYN) == 'N' or str.upper(uinRegexYN) == 'NO':
			self.uinBuiltInYN = False
			uinRegex = input('What is the regex pattern to search with? ')
			self.uinregexPattern = uinRegex
		elif str.upper(uinRegexYN) == 'Y' or str.upper(uinRegexYN) == 'YES':
			self.uinBuiltInYN = True
		else:
			print('Invalid input, ' + uinRegexYN + '  please try again')
			self._uinRegex()

	def debug(self):
		print('\nos: ' + str(self.os) + '\npwd: ' + str(self.pwd) + '\nuInFile: ' + str(self.uInFile) + '\nslashdir: ' + str(self.slashdir) + '\nconfFile ' + str(self.confFile))

class regex(uInput):
	def __init__(self):
		self.regexPattern = None
		self.builtinPattern = {}
		self.pickPattern = None
		self.buildBuiltinDict()
		self.collectResp()
		self._regex(self.pickPattern)
		self.debug()

	def buildBuiltinDict(self):
		#file = uIn.openConfFile.read()
		#for line in self.openConfFile.read():
			#impPatterns = re.findall('(.+),(.+)',line)
		print(uIn.openConfFile)
		impPatterns = re.findall('\".+\"\s\".+\"',uIn.openConfFile.read())
		print('impPatterns: ' + str(impPatterns))
		for x,y in impPatterns:
			self.builtinPattern = dict(x,y)
		print(str(self.builtinPattern))
	
	def collectResp(self):
		if uIn.uinBuiltInYN == True:
			print(self.builtinPattern)
			print('\n')
			for x,y in self.builtinPattern:
				print('\nName : Pattern\n' + x + ' = ' + y)
			self.pickPattern = input('What pattern name would you like to use? ')
			try:
				self.regexPattern = self.builtinPattern[self.pickPattern]
			except:
				print('Invalid input ' + self.pickPattern + '. Please try again.\n')
				self.collectResp()
		else:
			print('not true, in process')
			
	def _regex(self, pattern):
		getregexp = re.findall(pattern,uInput.uInFile)
		print(getregexp)
		
	def debug(self):
		print('\nself.regexPattern: ' + self.regexPattern + '\nself.builtinPattern: ' + str(self.builtinPattern))

uIn = uInput()
crex = regex()