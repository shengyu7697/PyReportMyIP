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
import requests

gRunning = True
gCount = 0

#### download util ####
def downloadFile(url, filename):
	print("downloading %s to %s ..." % (url, filename))
	r = requests.get(url)
	if r.status_code == 404: # check url is downloadable
		return False
	handle = open(filename, "wb")
	handle.write(r.content)
	return True

########

# https://gist.github.com/gesquive/8363131
# http://hackthology.com/how-to-write-self-updating-python-programs-using-pip-and-git.html
# https://github.com/noobscode/kalel/blob/master/run.py#L310
def upgradeMyself(url):
	appPath = os.path.realpath(sys.argv[0])
	dlPath = appPath + ".new"
	backupPath = appPath + ".old"
	try:
		r = downloadFile(url, dlPath)
	except:
		print("downloadFile except, upgrade failed.")
		return False
	if r == False:
		print("upgrade failed.")
		return False

	try:
		os.rename(appPath, backupPath)
	except OSError, (errno, strerror):
		print("Unable to rename %s to %s: (%d) %s" % (appPath, backupPath, errno, strerror))
		return False

	try:
		os.rename(dlPath, appPath)
	except OSError, (errno, strerror):
		print("Unable to rename %s to %s: (%d) %s" % (dlPath, appPath, errno, strerror))
		return False

	try:
		import shutil
		shutil.copymode(backupPath, appPath)
	except:
		os.chmod(appPath, 0755)

	print("New version installed as %s" % appPath)
	print("Previous version backed up to %s" % (backupPath))
	return True

def restartMyself():
	# https://www.programcreek.com/python/example/986/os.execv
	# https://stackoverflow.com/questions/1750757/restarting-a-self-updating-python-script
	# In Linux, or any other form of unix, os.execl
	# On Windows, os.spawnl
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
# reportInfo
def startClient():
	signal.signal(signal.SIGINT, signalHandler)
	version = "0.9.5"
	if len(sys.argv) == 2:
		HOST = sys.argv[1]
	else:
		HOST = "0.0.0.0"
	PORT = 2330

	print("version: %s, pid: %s" % (version, os.getpid()))

	while gRunning == True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print("connect to %s:%d ..." % (HOST, PORT))
			s.connect((HOST, PORT))
		except IOError as e:
			print(e)
			print("connect failed. wait 5s to reconnect.")
			time.sleep(5) # sleep 5 sec
			continue

		while gRunning == True:
			global gCount
			#print(gCount)
			if gCount % 4 == 1: # getClientLeastVersion
				msg = str({"type": "getClientLeastVersion"})
			#elif gCount % 4 == 2: # getServerVersion
			#	msg = str({"type": "getServerVersion"})
			else: # reportInfo
				dict1 = {
				"type": "reportInfo",
				"hostname": getHostname(),
				"user": getUsername(),
				"ip": getHostIp(),
				"version": version
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
				clientLeastVersion = dict2["getClientLeastVersion"]
				if LooseVersion(clientLeastVersion) > LooseVersion(version): # ref https://stackoverflow.com/questions/11887762/how-do-i-compare-version-numbers-in-python

					print("Detect new version. I need upgrade (%s -> %s)." % (version, clientLeastVersion))
					r = upgradeMyself(dict2["url"])
					if r == True:
						s.close()
						restartMyself()
				else:
					print("I'm the least version %s, client least version %s." % (version, clientLeastVersion))
			else:
				print(data)
			time.sleep(5) # sleep 5 sec

		s.close()

if __name__ == '__main__':
	startClient()
	
	print("end of process.")