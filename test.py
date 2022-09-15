import signal
import time


def scheduler(arg1, args2):
    print(time.time())

signal.signal(signal.SIGALRM, scheduler)
signal.setitimer(signal.ITIMER_REAL, 0.001, 0.01)
time.sleep(1000)
