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

	#检查是否存在对应备份目录，如不存在则新建目录
	dirname = dirstr + "/" + area
	if not os.path.exists(dirname):
		os.makedirs(dirname)
	
	#在指定备份目录新建备份文件	
	outputfile = dirname + "/" + hostname + '.txt'
	fout = open(outputfile,'w')
	fout.write ('==========Log Tile: Auto config backup==========\n')
	
	#使用pexpect库，执行ssh登录过程
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
	dirstr = prefix + "oa-backup/" + timestr

	#枚举hosts，针对每台设备，调用函数configbackup,执行对应命令集，保存结果，在指定目录生成备份文件
	for host in hosts:
		logging.info("--------Begin of backup of " + host['hostip'] + "-----------")
		configbackup(dirstr, host['area'], host['hostname'], host['hostip'], host['username'], host['password'], modules[0][host['modulename']]) 

	#执行操作系统指令tar,打包后执行svn，将备份文件更新入svn服务器
	
	logging.info("start zip the config files....................")
	logging.info("/bin/tar czvf "+prefix+"oa-backup/" + timestr + ".tar.gz " +  prefix + "oa-backup/" + timestr + "/")
	os.system("/bin/tar czvf "+prefix+"oa-backup/" + timestr + ".tar.gz " +  prefix + "oa-backup/" + timestr + "/")
	
	logging.info("start deleting the unzip files.................")
	logging.info("/bin/rm -rf  "+prefix+"oa-backup/" + timestr + "/")
	os.system("/bin/rm -rf  "+prefix+"oa-backup/" + timestr + "/")
	logging.info("Work is done, enjoy it!!!!!")

	#svn commit -m "timestr" oa-backup/
	logging.info("/usr/local/bin/svn update "+ prefix + "oa-backup/")
	os.system("/usr/local/bin/svn update "+ prefix + "oa-backup/")

	logging.info("/usr/local/bin/svn add "+prefix+"oa-backup/"+ timestr + ".tar.gz")
	os.system("/usr/local/bin/svn add "+prefix+"oa-backup/"+ timestr + ".tar.gz")

	logging.info("/usr/local/bin/svn commit -m '" + timestr +"' "+prefix+"oa-backup/")
	os.system("/usr/local/bin/svn commit -m '" + timestr +"' "+prefix+"oa-backup/")
