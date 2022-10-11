import socket
import numpy as np
from matplotlib import pyplot as plt

class BaseClient:
	def __init__(self, timeout: int = 10, buffer: int = 4096):
		global SignalFrequency
		self.__socket = None
		self.__address = None
		self.__timeout = timeout
		self.__buffer = buffer
		SignalFrequency = 20

	def connect(self, address, family: int, typ: int, proto: int):
		self.__address = address
		self.__socket = socket.socket(family, typ, proto)
		self.__socket.settimeout(self.__timeout)
		self.__socket.connect(self.__address)

	def send(self, message: str = "") -> None:
		flag = False
		while True:
			message_recv = self.__socket.recv(self.__buffer).decode('utf-8')
			self.received(message_recv)
			if flag:
				break
		try:
			self.__socket.shutdown(socket.SHUT_RDWR)
			self.__socket.close()
		except:
			pass

	def received(self, message: str):
		global SignalFrequency
		value_raw = []
		value_raw = message.split(',')
		value = [float(n) for n in value_raw]
		print("Row:")
		print(message)
		print("List:")
		print(value)
		FFTrow = len(value)
		print("{}行のデータを受信".format(FFTrow))
		self.FFT(value, FFTrow, SignalFrequency)

	def FFT(self, value: list, FFTrow: int, freq: int):
		if list(bin(FFTrow)).count('1') != 1:
			print ("The number must be a power of 2. This is {}".format(FFTrow))
			return False
		else:
			SpectrumAmplitude = [0.0] * FFTrow
			Freqency = [0.0] * FFTrow
			FFT = np.fft.fft(value[0:FFTrow])
			for i in range(FFTrow):
				SpectrumAmplitude[i] = np.sqrt(
					FFT[i].real * FFT[i].real + FFT[i].imag * FFT[i].imag)
				Freqency[i] = (i * freq) / FFTrow

			plt.subplot(2,1,1)
			plt.axis([0.0,len(value),-0.5,4])
			plt.title("test", fontsize=14, fontname='serif')
			plt.xlabel("Time", fontsize=14, fontname='serif')
			plt.ylabel("Volt [V]", fontsize=14, fontname='serif')
			plt.plot(value, color="b", linewidth=1.0, linestyle="-")

			plt.subplot(2,1,2)
			plt.plot(Freqency, SpectrumAmplitude, color="b", linewidth=1.0, linestyle="-")
			plt.xlim(0, freq / 2)
			plt.ylim(0, 30)
			plt.title("Freqency spectrum", fontsize=14, fontname='serif')
			plt.xlabel("Freqency [Hz]", fontsize=14, fontname='serif')
			plt.ylabel("Amplitude", fontsize=14, fontname='serif')

			plt.tight_layout()
			plt.draw()
			plt.pause(0.0001)
			plt.clf()

class InetClient(BaseClient):
	def __init__(self, host:str="192.168.11.90", port:int=8080) -> None:
	#def __init__(self, host: str = "192.168.0.6", port: int = 8080) -> None:
		self.server = (host, port)
		super().__init__(timeout=60, buffer=4096)
		super().connect(self.server, socket.AF_INET, socket.SOCK_STREAM, 0)


if __name__ == "__main__":
	cli = InetClient()
	cli.send()
