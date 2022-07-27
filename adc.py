import sys
import matplotlib.pyplot as plt
import signal
import time
import numpy as np
from gpiozero import MCP3208
from time import sleep

ports = []
value = []
times = []
Vref = 5.0
imax = 4096
p = 0
nSample = 0
nStart = 0
freqency = []
for i in range(8):
	ports.append(MCP3208 (channel = i))

def callback(args1, args2):
	try:
		volts = int(imax * ports[0].value)
		volts = volts * Vref / 4096
		volts = round(volts,5)
		times.append(time.time())
		value.append(volts)

	except KeyboaedInterrupt:
		for i in range(8):
			ports[i].close()
		sys.exit
def FFT():
	global nSample
	global nStart
	fs = 100
	nSample = len(value)
	nStart = 0
#	amplitude_delta = 0.0
#	amplitude_sin = 0.0
#	amplitude_lowalpha = 0.0
#	amplitude_highalpha = 0.0
#	amplitude_lowbeta = 0.0
#	amplitude_highbeta = 0.0
#	amplitude_lowganma = 0.0
#	amplitude_midganma = 0.0

	#時間情報
	t1 = nStart / fs
	t2 = t1 + nSample / fs

	#高速離散フーリエ変換
	F = np.fft.fft(value[nStart:nStart + nSample])

	#振幅と位相
	spectrumAmplitude = [0.0] * nSample
	for k in range(0, nSample):
		spectrumAmplitude[k] = np.sqrt(F[k].real * F[k].real + F[k].imag * F[k].imag)

	#周波数
	freqency = [0.0] * nSample
	for k in range(0, nSample):
		freqency[k] = (k * fs) / nSample
	print ("FFT Done!")

	#グラフ表示
	plt.plot(freqency, spectrumAmplitude, color = "b", linewidth = 1.0, linestyle = "-")
	plt.xlim(0, 10)
	plt.ylim(0, 600.0)
	plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
	plt.yticks([0, 100, 200, 300, 400, 500, 600])
	plt.grid(True)
	plt.show()

	#ピーク周波数
	peakFreq = 0.0
	peakValue = 0.0
	for k in range(0, nSample):
		#0.5Hz成分以上からナイキスト周波数まで
		if freqency[k] > 0.5 and freqency[k] < fs /2.0:
			#値がこれまでの最大値より大きければ最大値情報を更新する
			if spectrumAmplitude[k] > peakValue:
				peakFreq = freqency[k]
				peakValue = spectrumAmplitude[k]
			#脳波種別に割り当て
			if float(spectrumAmplitude[k]) >= 0.5 and float(spectrumAmplitude[k]) <= 2.75:
				print ("f")
	print("peak frequency: " + str(peakFreq) + "[Hz]")
	print("heart rate: " + str(60 * peakFreq) + "[bpm]")

signal.signal(signal.SIGALRM, callback)
signal.setitimer(signal.ITIMER_REAL, 0.1, 0.01)
time.sleep(1)

signal.setitimer(signal.ITIMER_REAL, 1, 1)
time.sleep(2)

print (times)
print (value)

FFT()
