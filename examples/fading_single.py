#
# Fading one led
# 
# Run with: 
#  python fading_single.py
#
# Type ctrl-C to exit
#

import time
import ablib as AB

PERIOD=1000000

Led = AB.PWM(0, PERIOD, 0)
Led.pwm_enable()

print "Fading led "
while True:
    step = PERIOD/10
    delay = 0.1
    for val in range(0,PERIOD+step,step):
        Led.pwm_pulse(val)
        time.sleep(delay)
    for val in range(PERIOD, 0-step, -step):
        Led.pwm_pulse(val)
        time.sleep(delay)
