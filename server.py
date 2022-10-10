import os
import socket
import struct
import math
import numpy as np
import time
import signal
import random
from gpiozero import MCP3208
from time import sleep

class BlockingServerBase:
	def __init__(self, timeout=60, buffer=4096):
		global adc
		global nSample
		global BufferA
		global SignalFrequency
		adc = MCP3208(channel=0, differential=False)
		BufferA = np.array([])
		self.__socket = None
		self.__timeout = timeout
		self.__buffer = buffer
		self.close()
		nSample = 512
		SignalFrequency = 80

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
				self.measurement()
				for i in range(len(BufferA) - 1):
					str = str + ('{:1.5f}'.format(BufferA[i]) + ",")

				str = str + ('{:1.5f}'.format(BufferA[i]))
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
		global nSample

		Vref = 3.3
		volt = np.round(adc.value * Vref, 5)
		BufferA = np.append(BufferA, volt)
		if CallbackCount >= nSample - 1:
			print("Finished measurement with {} rows!".format(len(BufferA)))
			signal.alarm(0)
		else:
			CallbackCount = CallbackCount + 1

	def measurement(self):
		global CallbackCount
		global BufferA
		global SignalFrequency
		global nSample
		CallbackCount = 0
		BufferA = np.zeros(0)
		signal.signal(signal.SIGALRM, self.measurement_callback)
		signal.setitimer(signal.ITIMER_REAL, 0.1, 1 / SignalFrequency)
		while CallbackCount < nSample - 1:
			time.sleep(0.5)

	def respond(self, message:str) -> str:
		return ""

class InetServer(BlockingServerBase):
	def __init__(self, host:str="0.0.0.0", port:int=8080) -> None:
		self.server=(host,port)
		super().__init__(timeout=60, buffer=4096)
		self.accept(self.server, socket.AF_INET, socket.SOCK_STREAM, 0)

	def respond(self, message:str) -> str:
		print("received -> ", message)
		return ""


if __name__ == "__main__":
	InetServer()
