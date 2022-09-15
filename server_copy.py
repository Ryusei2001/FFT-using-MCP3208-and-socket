
from gpiozero import MCP3208
from time import sleep
import os
import socket
import math
import struct

class BlockingServerBase:
	def __init__(self, timeout=60, buffer=1024):
		global adc
		self.__socket = None
		self.__timeout = timeout
		self.__buffer = buffer
		self.close()
		Vref = 3.3
		adc = MCP3208(channel=0, differential=False)
		data = []


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
				for i in range(3):
					str = str + ('{:1.5f}'.format(adc.value) + ",")
				conn.send(str.encode('utf-8'))

			except ConnectionResetError:
				break
			except BrokenPipeError:
				break

		self.close()

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
