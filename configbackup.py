#!/usr/bin/python
#-- coding:utf-8 --
  
import pexpect  
import sys  
import time  
import os 
import logging
logging.basicConfig(level=logging.INFO) 

outputfile = '1.out'
host = '10.252.21.254'
username = 'root'
password = 'tjkj@1216'
commandlist = ['dis ip int brief','dis ip rout','display current','quit']

fout = open(outputfile,'w')
fout.write ('==========Log Tile: Auto config backup==========\n')

#-----send password to login------
foo = pexpect.spawn('/usr/bin/ssh %s@%s' % (username, host))
foo.logfile_read = fout
foo.expect('.*ssword:')
foo.sendline(password)

#-----send command1--------
for command in commandlist:
	foo.expect('>')
	logging.info(command+'\n')
	foo.sendline(command)
	foo.sendline('                                                       ')

#-----end------------------
try:
	foo.expect('pexpect.EOF')
except pexpect.EOF:
	logging.info("End of the config\n")
fout.close()

#foo.interact()