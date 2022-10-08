#from gpiozero import MCP3208
from time import sleep
from matplotlib import pyplot as plt
import numpy as np
import signal
import time
import random

class readAnalog:
	def __init__(self):
		#global adc
		global nSample
		global SignalFrequency
		global BufferA
		#adc = MCP3208(channel=0, differential=False)
		nSample = 4096	
		SignalFrequency = 800
		BufferA = np.array([])

	def main(self):
		global SignalFrequency
		global BufferA
		while True:
			self.measurement()
			FFTrow = len(BufferA)
			self.FFT(BufferA, FFTrow, SignalFrequency)

	def measurement_callback(self, args1, args2):
		global CallbackCount
		global BufferA
		global adc
		Vref = 3.3
		#volt = np.round(adc.value * Vref, 5)
		volt = random.random()
		BufferA = np.append(BufferA, volt)
		if CallbackCount >= nSample - 1:
			print("Finished measurement with {} rows!".format(len(BufferA)))
			signal.alarm(0)
		else:
			CallbackCount = CallbackCount + 1

	def measurement(self):
		global CallbackCount
		global BufferA
		CallbackCount = 0
		BufferA = np.zeros(0)
		signal.signal(signal.SIGALRM, self.measurement_callback)
		signal.setitimer(signal.ITIMER_REAL, 0.1, 1 / SignalFrequency)

		while CallbackCount < nSample - 1:
			time.sleep(0.5)

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
		plt.plot(BufferA, color="b", linewidth=1.0, linestyle="-") 
		plt.title("Volts", fontsize=14, fontname='serif')
		plt.xlabel("Time", fontsize=14, fontname='serif') 
		plt.ylabel("Amplitude [V]", fontsize=14, fontname='serif')

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


analog = readAnalog()
analog.main()
