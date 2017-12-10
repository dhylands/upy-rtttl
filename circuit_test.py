from rtttl import RTTTL
import songs

import board
import pulseio
import time

speaker_pin   = board.D0  # Speaker is connected to this DIGITAL pin

# Initialize input/output pins
pwm       = pulseio.PWMOut(speaker_pin, variable_frequency=True, duty_cycle=0)

def play_tone(freq, msec):
#    print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
    if freq > 0:
        pwm.frequency  = int(freq)   # Set frequency
        pwm.duty_cycle = 32767  # 50% duty cycle
	time.sleep(msec*0.001)  # Play for a number of msec
    pwm.duty_cycle = 0          # Stop playing
    time.sleep(0.05)            # Delay 50 ms between notes

tune = RTTTL(songs.find('Entertainer'))

for freq, msec in tune.notes():
    play_tone(freq, msec)

