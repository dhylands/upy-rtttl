# Raspberry Pi Pico RTTTL example
# scruss - 2021-02: sorry, not sorry ...

from rtttl import RTTTL
from time import sleep_ms
from machine import Pin, PWM

# nicked from https://gist.github.com/mhungerford/0af269ee46c0d44a813c
NvrGonna = 'NvrGonna:d=4,o=5,b=200:8g,8a,8c6,8a,e6,8p,e6,8p,d6.,p,8p,8g,8a,8c6,8a,d6,8p,d6,8p,c6,8b,a.,8g,8a,8c6,8a,2c6,d6,b,a,g.,8p,g,2d6,2c6.,p,8g,8a,8c6,8a,e6,8p,e6,8p,d6.,p,8p,8g,8a,8c6,8a,2g6,b,c6.,8b,a,8g,8a,8c6,8a,2c6,d6,b,a,g.,8p,g,2d6,2c6.'

# pin 26 - GP20; just the right distance from GND at pin 23
#  to use one of those PC beepers with the 4-pin headers
pwm = PWM(Pin(20))


def play_tone(freq, msec):
    # print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
    if freq > 0:
        pwm.freq(int(freq))       # Set frequency
        pwm.duty_u16(32767)       # 50% duty cycle
    sleep_ms(int(0.9 * msec))     # Play for a number of msec
    pwm.duty_u16(0)               # Stop playing for gap between notes
    sleep_ms(int(0.1 * msec))     # Pause for a number of msec


tune = RTTTL(NvrGonna)
for freq, msec in tune.notes():
    play_tone(freq, msec)
