#!/bin/usr/python
#-- coding:utf8 --

import json


obj = [[1,2,3],123,123.123,'abc',{'key1':(1,2,3),'key2':(4,5,6)}]

encodedjson = json.dumps(obj)

print repr(obj)
print encodedjson
print type(encodedjson)

decodedjson = json.loads(encodedjson)
print type(decodedjson)
print decodedjson[4]['key1']
print decodedjson

jsonf = open('hosts.conf')
confstring = jsonf.read()
print confstring
decodedjson = json.loads(confstring)

for host in decodedjson:
	print host['hostname']
	print host['host']