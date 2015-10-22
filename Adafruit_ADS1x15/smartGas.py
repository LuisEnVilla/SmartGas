#!/usr/bin/python
import time, signal, sys
import dweepy
import os
from Adafruit_ADS1x15 import ADS1x15

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

ADS1015 = 0x00  # 12-bit ADC
ADS1115 = 0x01	# 16-bit ADC
gain = 4096  # +/- 4.096V
sps = 250  # 250 samples per second
adc = ADS1x15(ic=ADS1115)
msgEnviado = False
while True:
	time.sleep(0.1)
	volts = adc.readADCSingleEnded(0, gain, sps) / 1000
	percent = int((volts*100)/3.5)
	dweepy.dweet_for('smartgasIoTRaspi', {'Gas': percent,'Volts':volts, 'sms':msgEnviado})
	if (volts<=1 and msgEnviado==False):
		msgEnviado = True
		os.system("python ../AlertWhats/run.py "+"5217721199947 "+ "'No hay gas...' &")
		#os.system("python ../AlertWhats/run.py "+"5213331676227 "+ "'No hay gas...'")
	if(volts>1):
		msgEnviado = False
	print "%.6f" % (volts)
	print percent
