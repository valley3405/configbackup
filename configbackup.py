#!/usr/bin/python
#-- coding:utf-8 --
  
import pexpect  
import sys  
import time  
import os 
import logging
import json
logging.basicConfig(level=logging.INFO) 


#host = '10.252.21.254'
#username = 'root'
#password = 'tjkj@1216'
#commandlist = ['dis ip int brief','dis ip rout','display current','quit']

def configbackup(host, username, password, module):
	outputfile = '1.out'
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

	os.makedirs("config/%s" % u"办公区")
	os.makedirs("config/%s" % u"开发测试区")

	for host in hosts:
		logging.info(host['hostip'])
		configbackup(host['hostip'], host['username'], host['password'], modules[0][host['modulename']]) 
	
		#configbackup('10.252.21.254', 'root', 'tjkj@1216', ['dis ip int brief','dis ip rout','display current','quit'])

if __name__ == '__main__':
	main()