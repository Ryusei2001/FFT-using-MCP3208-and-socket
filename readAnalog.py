from gpiozero import MCP3208
from time import sleep
import numpy as np
Vref = 3.3
adc = MCP3208(channel=1, differential=False)

while True:
	str = np.round(adc.value * Vref, 5)
	sleep(0.1)
	print("Message: {}".format(str))
