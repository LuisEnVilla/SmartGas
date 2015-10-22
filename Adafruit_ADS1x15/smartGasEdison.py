#!/usr/bin/python
from time import sleep
import pyupm_grove as grove

# New Grove Slider on AIO pin 0
slider = grove.GroveSlide(0)
msgEnviado = False
# Loop indefinitely
while True:

	# Read values
	raw = slider.raw_value()
	volts = slider.voltage_value()

	print "Slider value: ", raw , " = %.2f" % volts , " V"
	percent = int((volts*100)/3.5)
	dweepy.dweet_for('smartgasIoTRaspi', {'Gas': percent,'Volts':volts, 'sms':msgEnviado})
	if (volts<=1 and msgEnviado==False):
		msgEnviado = True
		os.system("python ../AlertWhats/run.py "+"5217721199947 "+ "'No hay gas...' &")
		#os.system("python ../AlertWhats/run.py "+"5213331676227 "+ "'No hay gas...'")
	if(volts>1):
		msgEnviado = False
	# Sleep for 2.5 s
	sleep(0.1)