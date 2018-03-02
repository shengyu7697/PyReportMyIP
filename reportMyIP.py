#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import time
import signal
import sys
import fcntl
import struct
import getpass
from distutils.version import LooseVersion, StrictVersion
import os

gRunning = True
gCount = 0

# https://gist.github.com/gesquive/8363131
# http://hackthology.com/how-to-write-self-updating-python-programs-using-pip-and-git.html
def upgradeMyself():
	print("upgradeMyself")

def restartMyself():
	os.execv(sys.executable, [sys.executable] + sys.argv)

def signalHandler(signal, frame):
	print("You pressed Ctrl+C!")
	global gRunning
	gRunning = False

#### network util ####
def getIpAddress(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
	)[20:24])

# ref https://www.chenyudong.com/archives/python-get-local-ip-graceful.html
def getHostIp():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
	finally:
		s.close()

	return ip

def getIp():
	# 可以參考這篇作法看看 https://github.com/orenhe/myip
	return getHostIp()

def getHostname():
	return socket.getfqdn(socket.gethostname())

def getUsername():
	return getpass.getuser()

########

# msg type:
# getClientLeastVersion
# getServerVersion
# reportClientVersion
# reportInfo
def startClient():
	signal.signal(signal.SIGINT, signalHandler)
	version = "0.9.1"
	HOST = "0.0.0.0"
	PORT = 2330

	print("version: %s, pid: %s" % (version, os.getpid()))

	while gRunning == True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((HOST, PORT))
		except IOError as e:
			print(e)
			print("connect failed. wait 5s to reconnect.")
			time.sleep(1) # sleep 5 sec
			continue

		while gRunning == True:
			global gCount
			#print(gCount)
			if gCount % 10 == 1: # getClientLeastVersion
				msg = str({"type": "getClientLeastVersion"})
			elif gCount % 10 == 2: # getServerVersion
				msg = str({"type": "getServerVersion"})
			elif gCount % 10 == 3: # reportClientVersion
				msg = str({"type": "reportClientVersion", "reportClientVersion": version})
			else: # reportInfo
				dict1 = {
				"type": "reportInfo",
				"hostname": getHostname(),
				"user": getUsername(),
				"ip": getHostIp()
				}
				msg = str(dict1) # dict to string
			s.send(msg)
			gCount = gCount + 1

			data = s.recv(1024)
			if len(data) == 0: # connection closed
				print("Server closed connection.")
				break

			## process recv data
			dict2 = eval(data) # string to dict
			if "getClientLeastVersion" in dict2: # if dict2 has getClientLeastVersion key
				print(dict2["getClientLeastVersion"])
				clientLeastVersion = dict2["getClientLeastVersion"]
				if LooseVersion(clientLeastVersion) > LooseVersion(version): # ref https://stackoverflow.com/questions/11887762/how-do-i-compare-version-numbers-in-python
					s.close()
					print("Detect new version. I need upgrade (%s -> %s)." % (version, clientLeastVersion))
					upgradeMyself()
					restartMyself()
			else:
				print(data)
			time.sleep(1) # sleep 1 sec

		s.close()

if __name__ == '__main__':
	startClient()
	
	print("end of process.")