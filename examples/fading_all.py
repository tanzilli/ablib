#
# Fading all available leds
# 
# Run with: 
#  python fading_all.py
#
# Type ctrl-C to exit
#

import signal
import sys
import time
import ablib as AB

# catch ctrl-c for a clean exit
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        for i in range(0, ch_num):
            Leds[i].pwm_disable()
        sys.exit(0)

Leds = []
PERIOD=1000000

# read numbers of PWM channels
ch_num = AB.get_pwm_channels()
print "Detected %d channels" % ch_num

# export all channels with a pulse of
# 0 so that connected leds are off
for i in range(0, ch_num):
    Leds.append(AB.PWM(i, PERIOD, 0))
    Leds[i].pwm_enable()

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit')

while True:
    for i in range(0, ch_num):
        print "Fading led " + str(i)
        step = PERIOD/10
        delay = 0.1
        for val in range(0,PERIOD+step,step):
            Leds[i].pwm_pulse(val)
            time.sleep(delay)
        for val in range(PERIOD, 0-step, -step):
            Leds[i].pwm_pulse(val)
            time.sleep(delay)
        

signal.pause()
