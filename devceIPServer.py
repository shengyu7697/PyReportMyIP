#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import signal

gRunning = True

def signalHandler(signal, frame):
	print("You pressed Ctrl+C!")
	global gRunning
	gRunning = False

def startServer():
	signal.signal(signal.SIGINT, signalHandler)

	HOST = "0.0.0.0"
	PORT = 2330

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(5)

	print("Server start at: %s:%s") % (HOST, PORT)
	print("wait for connection...")

	while gRunning == True:
		try:
			conn, addr = s.accept()
			print("Connected by ", addr)
		except IOError as e:
			print(e)
			continue

		while gRunning == True:
			try:
				data = conn.recv(1024)
			except IOError as e:
				print(e)
				break
			
			if len(data) == 0: # connection closed
				conn.close()
				print("Client closed connection.")
				break
			print(data)

			conn.send("server received you message.")
		conn.close()



	# conn.close()

if __name__ == '__main__':
	startServer()

	print("end of process")
