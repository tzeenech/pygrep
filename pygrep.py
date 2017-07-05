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
		self.uinOutYN = None
		self.outFileW = None
		self.builtinDict = {}
		self.setOS()
		self.setPWD()
		self.setslashdir()
		self._openConfFile()
		self._uinFile()
		self.displayChoice()
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
			if cmdOpt.debug == True:
				print('Found an existing pygrep.conf file...\n')
				for line in self.openConfFile.readlines():
					splitline = line.split()
					self.builtinDict[(splitline[0])] = ','.join(splitline[1:])
			else:
				for line in self.openConfFile.readlines():
					splitline = line.split()
					self.builtinDict[(splitline[0])] = ','.join(splitline[1:])
		else:
			self.openConfFile = open(self.confFile, 'a')

	def _uinFile(self):
		if cmdOpt.inFile != None:
			if os.path.isfile(cmdOpt.inFile) != True:
				pwduInFile = self.pwd + cmdOpt.inFile
				if os.path.isfile(pwduInFile) != True:
					print('Invalid input file path, ' + cmdOpt.inFile + '.')
					quit()
				else:
					self.uInFile = pwduInFile
			else:
				self.uInFile = cmdOpt.inFile
		else:
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
		if cmdOpt.rn != None:
			self.uinBuiltInYN = True
			self.uinregexPattern = cmdOpt.rn
		elif cmdOpt.rp != None:
			self.uinBuiltInYN = False
			self.uinregexPattern = cmdOpt.rp
		else:
			uinRegexYN = input('Would you like to use a built-in regex pattern. Y/N (Y)\npygrep>> ')
			if str.upper(uinRegexYN) == 'N' or str.upper(uinRegexYN) == 'NO':
				self.uinBuiltInYN = False
				uinRegex = input('What is the regex pattern to search with?\npygrep>> ')
				self.uinregexPattern = uinRegex
			elif uinRegexYN == '' or str.upper(uinRegexYN) == 'Y' or str.upper(uinRegexYN) == 'YES':
				self.uinBuiltInYN = True
			else:
				print('Invalid input, ' + uinRegexYN + '  please try again')
				self._uinRegex()

	def displayChoice(self):
		if cmdOpt.outFile != None and cmdOpt.screen == True:
			self.uinOutYN = 3
		elif cmdOpt.outFile != None and cmdOpt.screen == False:
			self.uinOutYN = 1
		elif cmdOpt.outFile == None and cmdOpt.screen == True:
			self.uinOutYN = 2
		else:
			uinOutYN = input('Would you like to save the output to a file, display it on the screen, or do both?\n1 = File Only\n2 = Screen Only\n3 = Both\n[Screen] pygrep>> ')
			if uinOutYN == '1' or str.upper(uinOutYN) == 'FILE' or str.upper(uinOutYN) == 'F':
				self.uinOutYN = 1
			elif uinOutYN == '2' or str.upper(uinOutYN) == 'SCREEN' or str.upper(uinOutYN) == 'S' or uinOutYN == '':
				self.uinOutYN = 2
				return
			elif uinOutYN == '3' or str.upper(uinOutYN) == 'BOTH' or str.upper(uinOutYN) == 'B':
				self.uinOutYN = 3
			else:
				print('Invalid input, please try again.')
				self.displayChoice()

	def uinOutFile(self):
		if self.uinOutYN == 1 or self.uinOutYN == 3:
			if cmdOpt.outFile != None:
				if os.path.isfile(cmdOpt.outFile) == True and cmdOpt.force == True:
					self.uinOutFilePath = cmdOpt.outFile
					self.outFileW = True
				elif os.path.isfile(cmdOpt.outFile) == True and cmdOpt.force == False:
					print('The output file, ' + cmdOpt.outFile + ', already exists. Please either force (-f) or provide another outfile name.')
					quit()
				elif os.path.isfile(cmdOpt.outFile) == False:
					self.uinOutFilePath = cmdOpt.outFile
					self.outFileW = True
			else:
				uinOutFilePath = input('Provide output file path\npygrep>> ')
				if os.path.isfile(uinOutFilePath) == True:
					self.uinOutFilePath = uinOutFilePath
					overwrite = input('That file exists (' + uinOutFilePath + '), overwrite? Y/N (N)\npygrep>> ')
					if overwrite == '' or str.upper(overwrite) == 'N' or str.upper(overwrite) == 'NO':
						newFileYN = input('Would you like to append to the file, or provide a new output path?\n1 = Append\n2 = New Path\n[new file] pygrep>> ')
						if newFileYN == '1' or str.upper(newFileYN) == 'APPEND' or str.upper(newFileYN) == 'A':
							self.outFileW = False
							return
						else:
							self.uinOutFile()
					elif str.upper(overwrite) == 'Y' or str.upper(overwrite) == 'YES':
						self.outFileW = True
						return
					else:
						print('Unrecognized input (' + overwrite + ') please try again.')
						self.uinoutFile()
				else:
					self.uinOutFilePath = uinOutFilePath
					self.outFileW = True
					print('uinOutFilePath: ' + self.uinOutFilePath)
		elif self.uinOutYN == 2:
			self.uinOutFile = 2
			return
		else:
			print('Invalid value of self.uinOutYN, please review coding.\nuinOutYN: ' + uinOutYN)
			self.displayChoice()

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
		self.openType = None
		self.pullInDict()
		self.setinFile()
		self.collectResp()
		self._regex(self.regexPattern)
		self.debug()

	def pullInDict(self):
		if cmdOpt.debug == True:
			print('uIn.builtinDict: ' + str(uIn.builtinDict))
		self.builtinPattern = uIn.builtinDict

	def setinFile(self):
		self.inFile = uIn.uInFile

	def collectResp(self):
		if uIn.uinBuiltInYN == True and cmdOpt.rn != None:
			try:
				self.regexPattern = self.builtinPattern[cmdOpt.rn]
			except:
				print('Regex pattern, ' + cmdOpt.rn + ', is not a valid pattern name.')
				quit()
		elif uIn.uinBuiltInYN == True and cmdOpt.rn == None:
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
		elif uIn.uinBuiltInYN == False and cmdOpt.rp == None:
			self.regexPattern = uIn.uinregexPattern
		elif uIn.uinBuiltInYN == False and cmdOpt.rp != None:
			self.regexPattern = cmdOpt.rp
		else:
			print('I missed an possible if statement.')

	def _regex(self, pattern):
		self.openSearchFile = open(self.inFile,'r').read()
		getregexp = re.findall(pattern,self.openSearchFile)
		if uIn.outFileW != None:
			if uIn.outFileW == True:
				self.openType = 'w'
			else:
				self.openType = 'a'
			print()
		if uIn.uinOutYN == 1:
			with open(uIn.uinOutFilePath, self.openType) as outFile:
				for result in getregexp:
					outFile.write('{}\n'.format(result))
			outFile.close
		elif uIn.uinOutYN == 2:
				print('Found:\n')
				for result in getregexp:
					print('{}\n'.format(result))
		elif uIn.uinOutYN == 3:
			print('Found: ' + str(getregexp))
			with open(uIn.uinOutFilePath, self.openType) as outFile:
				for result in getregexp:
					outFile.write('{}\n'.format(result))
			outFile.close
		else:
			pass
	def debug(self):
		if cmdOpt.debug == True:
			print('\nself.regexPattern: ' + self.regexPattern + '\nself.builtinPattern: ' + str(self.builtinPattern))
			print('Running re.findall:' + '\n\tpattern: ' + str(self.regexPattern) + '\n\tinFile: ' + str(self.inFile) + '\n\topenSearchFile: ' + str(self.openSearchFile) + '\nopenType: ' + self.openType)
		else:
			pass

class CommandLineOptions:
	'Allow for optional commandl-line input'
	def __init__(self):
		self.debug = None
		self.inFile = None
		self.outFile = None
		self.rp = None
		self.rn = None
		self.screen = False
		self.force = False
		self.switches()
		self.CommandLineOptionsDebug()


	def switches(self):
		parser = argparse.ArgumentParser()
		argparse.ArgumentParser(prog='pygrep.py', prefix_chars='-/')
		parser.add_argument('-debug', help='Print debugging information',action='store_true')
		parser.add_argument('-inf', help='Input file',action='store')
		parser.add_argument('-of', help='Output file',action='store')
		parser.add_argument('-rp', help='RegexPattern: Provide a regex pattern enclosed in single-quotes',action='store')
		parser.add_argument('-rn', help='RegexName: Use a regex from the pygrep.conf file with the given name',action='store')
		parser.add_argument('-s', help='Display output to screen',action='store_true')
		parser.add_argument('-f', help='Force -- Allow overwrites of existing files',action='store_true')
		args = parser.parse_args()
		self.debug = args.debug
		self.inFile = args.inf
		self.outFile = args.of
		self.rp = args.rp
		self.rn = args.rn
		self.screen = args.s
		self.force = args.f

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
