from gpiozero import MCP3208
import os
import socket
import struct
import math
import numpy as np
import time
from time import sleep
import signal

class BlockingServerBase:
	def __init__(self, timeout=60, buffer=1024):
		global adc
		global nSample
		global BufferA
		adc = MCP3208(channel=0, differential=False)
		nSample = 128
		self.close()
		Vref = 3.3
		BufferA = np.array([])
		self.__socket = None
		self.__timeout = timeout
		self.__buffer = buffer
		self.close()

	def __del__(self):
		self.close()

	def close(self) -> None:
		try:
			self.__socket.shutdown(socket.SHUT_RDWR)
			self.__socket.close()
		except:
			pass

	def accept(self, address, family:int, typ:int, proto:int) -> None:
		self.__socket = socket.socket(family, typ, proto)
		self.__socket.settimeout(self.__timeout)
		self.__socket.bind(address)
		self.__socket.listen(1)
		print("Server started : ", address)
		conn, _ = self.__socket.accept()

		while True:
			try:
				str = ""
				message_recv = conn.recv(self.__buffer).decode('utf-8')
				message_resp = self.respond(message_recv)
				#conn.send(message_resp.encode('utf-8'))
				self.measurement()
				for i in range(nSample):
						str = str + ('{:1.5f}'.format(BufferA[i]) + ",")
				conn.send(str.encode('utf-8'))
			except ConnectionResetError:
				break
			except BrokenPipeError:
				break
		self.close()

	def measurement_callback(self, args1, args2):
		global CallbackCount
		global BufferA
		global adc
		BufferA = np.append(BufferA, adc.value)
		if CallbackCount >= 128:
			signal.alarm(0)
		else:
			CallbackCount = CallbackCount + 1

	def measurement(self):
		global CallbackCount
		CallbackCount = 0
		signal.signal(signal.SIGALRM, self.measurement_callback)
		signal.setitimer(signal.ITIMER_REAL, 0.1, 0.007)
		time.sleep(1)

	def respond(self, message:str) -> str:
		return ""

class InetServer(BlockingServerBase):
	def __init__(self, host:str="0.0.0.0", port:int=8080) -> None:
		self.server=(host,port)
		super().__init__(timeout=60, buffer=1024)
		self.accept(self.server, socket.AF_INET, socket.SOCK_STREAM, 0)

	def respond(self, message:str) -> str:
		print("received -> ", message)
		return ""


if __name__ == "__main__":
	InetServer()

#for i in range(8):
#	data.append(adc.value * Vref)
#print(data)
