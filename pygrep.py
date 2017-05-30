#!/usr/bin/env python3

import re
import os
import argparse

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
		self.uinOutFilePath = None
		self.builtinDict = {}
		self.setOS()
		self.setPWD()
		self.setslashdir()
		self._openConfFile()
		self._uinFile()
		self.uinOutFile()
		self._uinRegex()
		self.debug()

	def setOS(self):
		self.os = os.name

	def clearscreen(self):
		if self.os == 'nt':
			os.system('cls')
		elif self.os == 'posix':
			os.system('clear')
		else:
			print('\n' * 200)

	def setPWD(self):
		self.pwd = os.getcwd()

	def setslashdir(self):
		if self.os == 'nt':
			self.slashdir = '\\'
		else:
			self.slashdir = '/'

	def _openConfFile(self):
		self.clearscreen()
		self.confFile = self.pwd + self.slashdir + 'pygrep.conf'
		if os.path.isfile(self.confFile) == True:
			self.openConfFile = open(self.confFile, 'r')
			print('Found an existing pygrep.conf file...\n')
			for line in self.openConfFile.readlines():
				splitline = line.split()
				self.builtinDict[(splitline[0])] = ','.join(splitline[1:])
		else:
			self.openConfFile = open(self.confFile, 'a')

	def _uinFile(self):
		uInFile = input('What file would you like to search through?\nPlease provide the full path if the file is not in the current directory, \n"' + self.pwd + '."\npygrep>> ')
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
		uinRegexYN = input('Would you like to use a built-in regex pattern, or provide your own? Y/N (N)\npygrep>> ')
		if uinRegexYN == '' or str.upper(uinRegexYN) == 'N' or str.upper(uinRegexYN) == 'NO':
			self.uinBuiltInYN = False
			uinRegex = input('What is the regex pattern to search with?\npygrep>> ')
			self.uinregexPattern = uinRegex
		elif str.upper(uinRegexYN) == 'Y' or str.upper(uinRegexYN) == 'YES':
			self.uinBuiltInYN = True
		else:
			print('Invalid input, ' + uinRegexYN + '  please try again')
			self._uinRegex()

	def uinOutFile(self):
		uinOutYN = input('Would you like to save the output to a file, or just display it on the screen?\n1 = File\n2 = Screen\n3 = Both \n(Screen) \npygrep>> ')
		if uinOutYN == '1' or str.upper(uinOutYN) == 'FILE' or str.upper(uinOutYN) == 'F':
			uinOutFilePath = input('Provide output file path: ')
			if os.path.isfile(uinOutFilePath) == True:
				self.uinOutFilePath = uinOutFilePath
				overwrite = input('That file exists (' + uinOutFilePath + '), overwrite? Y/N (N)\npygrep>> ')
				if overwrite == '' or str.upper(overwrite) == 'N' or str.upper(overwrite) == 'NO':
					self.uinOutFile()
				elif str.upper(overwrite) == 'Y' or str.upper(overwrite) == 'YES':
					outFile = open(self.uinOutFilePath, 'w')
				else:
					print('Unrecognized option (' + overwrite + ') please try again.')
			else:
				pass

	def debug(self):
		if cmdOpt.debug == True:
			print('\nos: ' + str(self.os) + '\npwd: ' + str(self.pwd) + '\nuInFile: ' + str(self.uInFile) + '\nslashdir: ' + str(self.slashdir) + '\nconfFile ' + str(self.confFile) + '\nself.builtinDict' + str(self.builtinDict))
		else:
			pass

class regex(uInput):
	def __init__(self):
		self.regexPattern = None
		self.builtinPattern = {}
		self.pickPattern = None
		self.openSearchFile = None
		self.inRegex = None
		self.inFile = None
		self.pullInDict()
		self.setinFile()
		self.collectResp()
		self._regex(self.regexPattern)
		self.debug()

	def pullInDict(self):
		print('uIn.builtinDict: ' + str(uIn.builtinDict))
		self.builtinPattern = uIn.builtinDict

	def setinFile(self):
		self.inFile = uIn.uInFile

	def collectResp(self):
		if uIn.uinBuiltInYN == True:
			print(self.builtinPattern)
			print('\n')
			for k, v in self.builtinPattern.items():
				print('\nName = Pattern\n' + k + ' = ' + v)
			self.pickPattern = input('What pattern name would you like to use?\npygrep>> ')
			try:
				self.regexPattern = self.builtinPattern[self.pickPattern]
			except:
				print('Invalid input ' + self.pickPattern + '. Please try again.\n')
				self.collectResp()
		else:
			self.regexPattern = uIn.uinregexPattern

	def _regex(self, pattern):
		self.openSearchFile = open(self.inFile,'r').read()
		getregexp = re.findall(pattern,self.openSearchFile)
		print('Found: ' + str(getregexp))

	def debug(self):
		if cmdOpt.debug == True:
			print('\nself.regexPattern: ' + self.regexPattern + '\nself.builtinPattern: ' + str(self.builtinPattern))
			print('Running re.findall:' + '\n\tpattern: ' + str(self.regexPattern) + '\n\tinFile: ' + str(self.inFile) + '\n\topenSearchFile: ' + str(self.openSearchFile))
		else:
			pass

class CommandLineOptions:
	'Allow for optional commandl-line input'
	def __init__(self):
		self.debug = ''
		self.switches()
		self.CommandLineOptionsDebug()


	def switches(self):
		parser = argparse.ArgumentParser()
		argparse.ArgumentParser(prog='pygrep.py', prefix_chars='-/')
		parser.add_argument('-debug', help='Print debugging information',action='store_true')
		args = parser.parse_args()
		self.debug = args.debug

	def getdebug(self):
		return(self.debug)

	def CommandLineOptionsDebug(self):
		if self.debug == True:
			print('\n--CommandLineOptionsDebug--')
			print('self.debug: ' + str(self.debug))
		else:
			pass


cmdOpt = CommandLineOptions()
uIn = uInput()
crex = regex()
