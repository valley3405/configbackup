#!/usr/bin/python
#-- coding:utf-8 --
  
import pexpect  
import sys  
import time  
import os  

host = '10.252.21.254'
username = 'root'
password = 'tjkj@1216'
command1 = 'display current'

foo = pexpect.spawn('/usr/bin/ssh %s@%s' % (username, host))
foo.expect('.*ssword:')
foo.sendline(password)
#foo.interact()
foo.sendline(command1)
foo.sendline('                                                       ')
foo.expect('>')

foo.interact()