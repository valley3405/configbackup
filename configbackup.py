#!/usr/bin/python
#-- coding:utf-8 --
  
import pexpect  
import sys  
import time  
import os  

outputfile = '1.out'
host = '10.252.21.254'
username = 'root'
password = 'tjkj@1216'
commandlist = ['dis ip int brief','dis ip rout','display current','quit']

fout = open(outputfile,'w')
fout.write ('==========Log Tile: Auto config backup==========\n')

#-----send password to login------
foo = pexpect.spawn('/usr/bin/ssh %s@%s' % (username, host))
foo.logfile_read = sys.stdout
foo.expect('.*ssword:')
foo.sendline(password)

#-----send command1--------
for command in commandlist:
	foo.expect('>')
	print command+'\n'
	foo.sendline(command)
	foo.sendline('                                                       ')

#-----end------------------
#foo.expect('pexpect.EOF')
fout.close()

#foo.interact()