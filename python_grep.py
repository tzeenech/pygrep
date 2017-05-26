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
            self.openConfFile = open(self.confFile, 'a+')
            f = self.openConfFile.readlines()
            print('Found an existing pygrep.conf file...\n' + self.confFile + '\n' + str(f))
        else:
            self.confFile = self.pwd + self.slashdir + 'pygrep.conf'
            self.openConfFile = open(self.confFile, 'a+')

    def _uinFile(self):
        uInFile = input('What file would you like to search through?\nPlease provide the full path if the file is not in the current directory, \n"' + self.pwd + '." ')
        if os.path.isfile(uInFile) != True:
            pwduInFile = self.pwd + uInFile
            if os.path.isfile(pwduInFile) != True:
                print('The file path provided,' + '(' + self.pwd + ')' + uInFile + ' does not exist, please try again.')
            else:
                self.uInFile = pwduInFile
        else:
            self.uInFile = uInFile

    def _uinRegex(self):
        uinRegexYN = input('Would you like to use a build-in regex pattern, or provide your own? Y/N (N) ')
        if uinRegexYN == '' or str.upper(uinRegexYN) == 'N' or str.upper(uinRegexYN) == 'NO':
            uinRegex = input('What is the regex pattern to search with? ')
            self.uinregexPattern = uinRegex
        else:
            crex._regex(crex.builtinPattern)

    def debug(self):
        print('\nos: ' + str(self.os) + '\npwd: ' + str(self.pwd) + '\nuInFile: ' + str(self.uInFile) + '\nslashdir: ' + str(self.slashdir) + '\nconfFile ' + str(self.confFile))

class regex:
    def __init__(self):
        self.regexPattern = None
        self.builtinPattern = '###\'(*)\''


    def _regex(self, pattern):
        f = uIn.pyfile
        getregexp = re.findall(pattern,f.read())
        print(getregexp)

crex = regex()
uIn = uInput()


###'.+'
###'(.+_\d+)'
