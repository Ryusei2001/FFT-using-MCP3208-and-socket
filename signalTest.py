import signal
import time
from time import sleep
#from gpiozero import MCP3208
import random

class signalTest:
	def __init__(self):
		global nSample
		nSample = 50

	def callback(self, arg1, args2):
		global i
		#adc = MCP3208(channel=0, differential=False)
		#print(adc.value)
		
		print(random.random())
		#print(i)
		if i >= nSample:
			signal.alarm(0)
		i = i + 1


	def timer(self):
		while True:
			global i
			global nSample
			i = 0
			signal.signal(signal.SIGALRM, self.callback)
			signal.setitimer(signal.ITIMER_REAL, 0.1, 1 / nSample)
			while i < nSample - 1:
				time.sleep(0.1)

if __name__ == "__main__":
	st = signalTest()
	st.timer()