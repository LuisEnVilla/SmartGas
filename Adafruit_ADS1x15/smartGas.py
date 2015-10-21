#!/usr/bin/python
import time, signal, sys
import dweepy
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

while True:
	time.sleep(0.5)
	volts = adc.readADCSingleEnded(0, gain, sps) / 1000
	dweepy.dweet_for('smartgas', {'Gas': volts})
	print "%.6f" % (volts)
