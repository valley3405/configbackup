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



if __name__ == '__main__':

	#指定脚本执行目录，从配置文件hosts.conf中读取设备清单，从modules.conf中读取执行命令集(针对不同设备)，解析json,并放入字典
	prefix = '/root/configbackup/'
	jsonf = open(prefix + 'hosts.conf')
	hosts = json.loads(jsonf.read())
	jsonf = open(prefix + 'modules.conf')
	modules = json.loads(jsonf.read())

	#取得当前时间，并组成由备份主目录+当前时间组合成的备份目录字符串，用于存放备份文件
	now = datetime.datetime.now()
	timestr = now.strftime("%Y-%m-%d_%H%M%S")
	dirstr = prefix + "configBackup.d/" + timestr

	#枚举hosts，针对每台设备，调用函数configbackup,执行对应命令集，保存结果，在指定目录生成备份文件
	for host in hosts:
		logging.info("--------Begin of backup of " + host['hostip'] + "-----------")
		configbackup(dirstr, host['area'], host['hostname'], host['hostip'], host['username'], host['password'], modules[0][host['modulename']]) 

	#执行操作系统指令svn，将备份文件更新入svn服务器
	#svn commit -m "timestr" configBackup.d/
	os.system("/usr/bin/svn update "+ prefix + "configBackup.d/")
	os.system("/usr/bin/svn add "+dirstr)
	os.system("/usr/bin/svn commit -m '" + timestr +"' "+prefix+"configBackup.d/")
