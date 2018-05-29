#
# This particular test was coded for the GHI Electronics G30 Development
# Board: https://www.ghielectronics.com/catalog/product/555
#
import pyb
from rtttl import RTTTL
import songs

buz_tim = pyb.Timer(3, freq=440)
buz_ch = buz_tim.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.BUZZER, pulse_width=0)

def play_tone(freq, msec):
    print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
    if freq > 0:
        buz_tim.freq(freq)
        buz_ch.pulse_width_percent(50)
    pyb.delay(int(msec * 0.9))
    buz_ch.pulse_width_percent(0)
    pyb.delay(int(msec * 0.1))


tune = RTTTL(songs.find('Entertainer'))
try:
    for freq, msec in tune.notes():
        play_tone(freq, msec)
except KeyboardInterrupt:
    play_tone(0, 0)
