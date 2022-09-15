import numpy as np
import time
import random
max = 512
data = []

def main():
	global max
	global data
	for i in range(max):
		data.append(random.random())

	F = [0.0] * max
	#Start
	start = time.time()
	for j in range(max):
		for k in range(max):
			real = data[k] * np.cos(-2.0 * np.pi * j * k / max)
			imag = data[k] * np.sin(-2.0 * np.pi * j * k / max)
			F[k] = F[k] + complex(real, imag)

	spectrumAmplitude = [0.0] * max
	for l in range(max):
		spectrumAmplitude[l] = np.sqrt(F[k].real * F[k].real + F[k].imag * F[k].imag)

	#End
	end = time.time()
	diff = (end - start) * 1000000000
	print (diff)
if __name__ == '__main__':
	main()
