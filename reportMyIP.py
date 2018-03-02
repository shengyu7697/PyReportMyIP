#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import time
import signal
import sys
import fcntl
import struct
import getpass

gRunning = True
gCount = 0

# https://gist.github.com/gesquive/8363131
# http://hackthology.com/how-to-write-self-updating-python-programs-using-pip-and-git.html
def upgradeMyself():
	print("upgradeMyself")

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

def startClient():
	signal.signal(signal.SIGINT, signalHandler)
	version = "0.9.1"
	HOST = "0.0.0.0"
	PORT = 2330

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
# type: 
# getClientLeastVersion
# getServerVersion
# reportClientVersion
# reportInfo
			
			global gCount
			#print(gCount)
			if gCount % 10 == 0: # getClientLeastVersion
				msg = str({"type": "getClientLeastVersion"})
			elif gCount % 10 == 1: # getServerVersion
				msg = str({"type": "getServerVersion"})
			elif gCount % 10 == 2: # reportClientVersion
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

			print(data)
			time.sleep(1) # sleep 1 sec

		s.close()

if __name__ == '__main__':
	startClient()

	print("end of process.")