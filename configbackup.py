#!/usr/bin/python
#-- coding:utf-8 --
  
import pexpect  
import sys  
import time  
import os 
import logging
logging.basicConfig(level=logging.ERROR) 


#host = '10.252.21.254'
#username = 'root'
#password = 'tjkj@1216'
#commandlist = ['dis ip int brief','dis ip rout','display current','quit']

def configbackup(host, username, password, commandlist[]):
	outputfile = '1.out'
	fout = open(outputfile,'w')
	fout.write ('==========Log Tile: Auto config backup==========\n')
	
	#-----send password to login------
	foo = pexpect.spawn('/usr/bin/ssh %s@%s' % (username, host))
	foo.logfile_read = fout
	foo.expect('.*ssword:')
	foo.sendline(password)
	
	#-----send commands--------
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

def main():
	configbackup('10.252.21.254', 'root', 'tjkj@1216', ['dis ip int brief','dis ip rout','display current','quit'])

if __name__ == '__main__':
	main()