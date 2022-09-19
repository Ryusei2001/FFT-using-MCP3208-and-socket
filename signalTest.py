import signal
import threading
import time
from time import sleep

def callback(arg1, args2):
	global i
	#print(time.time())
	print(i)
	if i >= 128:
		signal.alarm(0)
	i = i + 1


def timer():
	while True:
		global i
		i = 0
		signal.signal(signal.SIGALRM, callback)
		signal.setitimer(signal.ITIMER_REAL, 0.1, 0.007)
		time.sleep(1)


		timer2()
		timer3()
		time.sleep(5)

def timer2():
	print("hello")

def timer3():
	print("signal")

timer()
