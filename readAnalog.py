from gpiozero import MCP3208
from time import sleep

Vref = 3.3

adc = MCP3208(channel=1, differential=False)

while True:
	str = '{:1.5f}'.format(adc.value) + ","
	print(str)
	sleep(0.1)
