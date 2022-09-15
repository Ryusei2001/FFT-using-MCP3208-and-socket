from gpiozero import MCP3208
import os
import socket
import struct
import math
import numpy as np
import time
import signal

class BlockingServerBase:
	def __init__(self, timeout=60, buffer=1024):
		global adc
		global CurrentBuffer
		global nSample
		global A, B
		adc = MCP3208(channel=0, differential=False)
		CurrentBuffer = -1
		nSample = 128
		self.__socket = None
		self.__timeout = timeout
		self.__buffer = buffer
		self.close()
		Vref = 3.3
		A = np.array([])
		B = np.array([])

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
				for i in range(nSample):
					if CurrentBuffer == 0:
						str = str + ('{:1.5f}'.format(A[i]) + ",")
					else:
						str = str + ('{:1.5f}'.format(B[i]) + ",")

				conn.send(str.encode('utf-8'))
			except ConnectionResetError:
				break
			except BrokenPipeError:
				break
		self.close()

	def measurement_callback(self):
		global CurrentBuffer
		global A
		global B
		if CurrentBuffer != 0:
			for i in range(nSample):
				#A[i] = adc.value
				A = np.append(A, adc.value)
			CurrentBuffer = 0
			time.sleep(1)
		else:
			for i in range(nSample):
				B = np.append(B, adc.value)
			CurrentBuffer = 1
			time.sleep(1)

	def measurement(self):
		signal.signal(signal.SIGALRM, measurement_callback)
		signal.setitimer(signal.ITIMER_REAL, 0.001, 0.01)
		time.sleep(1000)

	def respond(self, message:str) -> str:
		return ""

class InetServer(BlockingServerBase):
	def __init__(self, host:str="0.0.0.0", port:int=8080) -> None:
		self.server=(host,port)
		super().__init__(timeout=60, buffer=1024)
		self.measurement()
		self.accept(self.server, socket.AF_INET, socket.SOCK_STREAM, 0)

	def respond(self, message:str) -> str:
		print("received -> ", message)
		return ""


if __name__ == "__main__":
	InetServer()

#for i in range(8):
#	data.append(adc.value * Vref)
#print(data)
