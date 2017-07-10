#!/usr/bin/env python3

import re
import os
import argparse

class Environment:
	def __init__(self):
		self.osType = None
		self.pwd = None
		self.slashdir = None
		self.setOSTYPE()
		self.setPWD()
		self.setSLASHDIRECTION(self.osType)
		self.debug()
	
	def setOSTYPE(self):
		self.osType = os.name	
	
	def setPWD(self):
		self.pwd = os.getcwd()

	def setSLASHDIRECTION(self,OS):
		if OS == 'nt':
			self.slashdir = '\\'
		else:
			self.slashdir = '/'

	def clearscreen(self):
		if self.osType == 'nt':
			os.system('cls')
		elif self.osType == 'posix':
			os.system('clear')
		else:
			print('\n' * 200)
	
	def debug(self):
		if cmdOpt.debug == True:
			print('\n--Environment--' + '\nosType: ' + str(self.osType) + '\npwd: ' + str(self.pwd) + '\nslashdir: ' + str(self.slashdir))
			
class ParseConfig:
	def __init__(self):
		self.confFile = None
		self.openConfFile = None
		self.dictConfFile = {}
		self.setCONFFILE(env.pwd,env.slashdir)
		self.openCONFFILE(env.pwd,env.slashdir)
		self.debug()

	def setCONFFILE(self,pwd,slashdir):
		self.confFile = pwd + slashdir + 'pygrep.conf'
		
	def openCONFFILE(self,pwd,slashdir):
		env.clearscreen()
		self.confFile = pwd + slashdir + 'pygrep.conf'
		if os.path.isfile(self.confFile) == True:
			self.openConfFile = open(self.confFile, 'r')
			if cmdOpt.debug == True:
				#print('Found an existing pygrep.conf file...\n')
				for line in self.openConfFile.readlines():
					splitline = line.split()
					self.dictConfFile[(splitline[0])] = ','.join(splitline[1:])
			else:
				for line in self.openConfFile.readlines():
					splitline = line.split()
					self.dictConfFile[(splitline[0])] = ','.join(splitline[1:])
		else:
			self.openConfFile = open(self.confFile, 'a')
	
	def debug(self):
		if cmdOpt.debug == True:
			print('\n--ParseConfig--' + '\nconfFile: ' + str(self.confFile) + '\nopenConfFile: ' + str(self.openConfFile) + '\ndictConfFile: ' + str(self.dictConfFile) + '\n')

class UserInput:
	def __init__(self):
		self.uInFile = None
		self.uOutFile = None
		self.regexPattern = None
		self.display = None
		self.uinOutYN = None
		self.uInFILE(env.osType,env.pwd,env.slashdir)
		self.displayChoice()
		self.uInOUTFILE()
		self.debug()
	
	def uInFILE(self,osType,pwd,slashdir):
		if cmdOpt.inFile != None:
			if os.path.isfile(cmdOpt.inFile) != True:
				pwduInFile = pwd + cmdOpt.inFile
				if os.path.isfile(pwduInFile) != True:
					print('Invalid input file path, ' + cmdOpt.inFile + '.')
					quit()
				else:
					self.uInFile = pwduInFile
			else:
				self.uInFile = cmdOpt.inFile
		else:
			uInFile = input('What file would you like to search through?\nPlease provide the full path if the file is not in the current directory, \n"' + pwd + '."\npygrep>> ')
			if os.path.isfile(uInFile) != True:
				pwduInFile = pwd + uInFile
				if os.path.isfile(pwduInFile) != True:
					print('The file path provided,' + '(' + pwd + ')' + uInFile + ' does not exist, please try again.')
					self.uInFile()
				else:
					self.uInFile = pwduInFile
			else:
				self.uInFile = uInFile

	def displayChoice(self):
		if cmdOpt.outFile != None and cmdOpt.screen == True:
			self.uinOutYN = 3
		elif cmdOpt.outFile != None and cmdOpt.screen == False:
			self.uinOutYN = 1
		#elif cmdOpt.outFile == None and cmdOpt.screen != None:
			#self.uinOutYN = 2
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

	def uInOUTFILE(self):
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
						self.uInOUTFILE()
					elif str.upper(overwrite) == 'Y' or str.upper(overwrite) == 'YES':
						self.outFileW = True
						return
					else:
						print('Unrecognized input (' + overwrite + ') please try again.')
						self.uInOUTFILE()
				else:
					self.uinOutFilePath = uinOutFilePath
					self.outFileW = True
					print('uinOutFilePath: ' + self.uinOutFilePath)
		elif self.uinOutYN == 2:
			self.uinOutFile = 2
			return
		else:
			print('Invalid value of self.uinOutYN, please review coding.\nuinOutYN: ' + self.uinOutYN)
			self.displayChoice()
	
	def debug(self):
		if cmdOpt.debug == True:
			print('\n--UserInput--' + '\nuInFile: ' + str(self.uInFile) + '\nuOutFile: ' + str(self.uOutFile) + '\nregexPattern: ' + str(self.regexPattern) + '\ndisplay: ' + str(self.display) + '\nuinOutYN: ' + str(self.uinOutYN))
		
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
		argparse.ArgumentParser(prog='pygrep.py', prefix_chars='-')
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

	def CommandLineOptionsDebug(self):
		if self.debug == True:
			print('\n--CommandLineOptionsDebug--' + '\nself.debug: ' + str(self.debug) + '\ninFile: ' + str(self.inFile) + '\noutFile: ' + str(self.outFile) + '\nrp: ' + str(self.rp) + '\nrn: ' + str(self.rn) + '\nscreen: ' + str(self.screen) + '\nforce: ' + str(self.force))

cmdOpt = CommandLineOptions()
env = Environment()
pconf = ParseConfig()
uIn = UserInput()



"""		
class uInput:
	def __init__(self):

		self.uInFile = None
		self.slashdir = None
		self.openConfFile = None
		self.uinBuiltInYN = None
		self.pickPattern = None
		self.uinOutFilePath = None
		self.uinOutYN = None
		self.outFileW = None
		self.builtinDict = {}
		self._openConfFile()
		self._uinFile()
		self.displayChoice()
		self.uinOutFile()
		self._uinRegex()


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
		elif cmdOpt.outFile == None and cmdOpt.screen != None:
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
"""