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

	dirname = dirstr + "/" + area
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
	#convert {"a":1} to [("a",1)]
	commandlist = module['commandlist'].items()
	for command in commandlist:
		logging.info(command[0])
		foo.sendline(command[0])
		foo.sendline('                                                                         ')
		foo.expect(command[1])
	
	#-----end------------------
	foo.sendline(module['quit'])
	try:
		foo.expect('pexpect.EOF')
	except pexpect.EOF:
		logging.info("End of the configBackup!\n")
	fout.close()

def main():
	jsonf = open('hosts.conf')
	hosts = json.loads(jsonf.read())
	jsonf = open('modules.conf')
	modules = json.loads(jsonf.read())

	now = datetime.datetime.now()
	timestr = now.strftime("%Y-%m-%d_%H%M%S")
	dirstr = "configBackup.d/" + timestr

	for host in hosts:
		logging.info("--------Begin of backup of " + host['hostip'] + "-----------")
		configbackup(dirstr, host['area'], host['hostname'], host['hostip'], host['username'], host['password'], modules[0][host['modulename']]) 

	#svn commit -m "timestr" configBackup.d/
	os.system("/usr/bin/svn update configBackup.d/")
	os.system("/usr/bin/svn add configBackup.d/*")
	os.system("/usr/bin/svn commit -m '" + timestr + "' configBackup.d/")
	
		

if __name__ == '__main__':
	main()