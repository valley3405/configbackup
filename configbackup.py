#!/usr/bin/python
#-- coding:utf-8 --
  
import pexpect  
import sys  
import time  
import os 
import logging
import json
import datetime
logging.basicConfig(level=logging.INFO) 

def configbackup(dirstr, area, hostname, host, username, password, module):

	dirname = dirstr + area
	if not os.path.exists(dirname):
		os.makedirs(dirname)
		
	outputfile = dirname + "/" + hostname + '.txt'
	fout = open(outputfile,'w')
	fout.write ('==========Log Tile: Auto config backup==========\n')
	
	#-----send password to login------
	foo = pexpect.spawn('/usr/bin/ssh %s@%s' % (username, host))
	foo.logfile_read = fout

	#-----send password to login or accept the RSA KEYS
	i = foo.expect(['\(yes\/no\)\?','.*ssword:'])
	if i == 0:
		foo.sendline('yes')
		foo.expect('.*password:')
		foo.sendline(password)
	else:
		foo.sendline(password)
	foo.expect(module['success_prompt'])
	
	#-----send commands--------
	commandlist = module['commandlist']
	for command in commandlist.keys():
		logging.info(command+'\n')
		foo.sendline(command)
		foo.sendline('                                                       ')
		foo.expect(commandlist[command])
	
	#-----end------------------
	foo.sendline(module['quit'])
	try:
		foo.expect('pexpect.EOF')
	except pexpect.EOF:
		logging.info("End of the config\n")
	fout.close()

def main():
	jsonf = open('hosts.conf')
	hosts = json.loads(jsonf.read())
	jsonf = open('modules.conf')
	modules = json.loads(jsonf.read())

	now = datetime.datetime.now()
	timestr = now.strftime("%Y-%m-%d_%H%M%S")
	dirstr = "config/" + timestr

	if not os.path.exists(dirstr):
		os.makedirs(dirstr)
		
	for host in hosts:
		logging.info(host['hostip'])
		configbackup(dirstr, host['area'], host['hostname'], host['hostip'], host['username'], host['password'], modules[0][host['modulename']]) 
	
		

if __name__ == '__main__':
	main()