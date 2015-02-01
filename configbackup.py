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
command1 = 'display current'

fout = open(outputfile,'w')
fout.write ('==========Log Tile: Auto config backup==========\n')

foo = pexpect.spawn('/usr/bin/ssh %s@%s' % (username, host))
foo.logfile = fout
foo.expect('.*ssword:')
foo.sendline(password)
foo.sendline(command1)
foo.sendline('                                                       ')
foo.expect('>')
foo.sendline(' ')

fout.close()

#foo.interact()