import numpy as np
import time
import random
max = 1024
data = []
def main():
	global max
	global data
	for i in range(max):
		data.append(random.random())

	spectrumAmplitude = [0.0] * max
	start = time.time()
	F = np.fft.fft(data[0:0+max])
	for j in range(max):
		spectrumAmplitude[j] = np.sqrt(F[j].real * F[j].real + F[j].imag * F[j].imag)

	end = time.time()
	diff = (end - start) * 1000000000
	print (diff)

if __name__ == '__main__':
	main()
