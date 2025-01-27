#
# This particular test was coded for Raspberry-Pi Pico / Pico 2 
# with Buzzer wired to GP13
#
# Pico-2-Explorer : https://shop.mchobby.be/product.php?id_product=2718
#
from machine import Pin, PWM 
from rtttl import RTTTL
import songs
import time

PWM_VOL = 50 # 0.100 : reduce this to reduce the volume

# Raspberry-Pi Pico / Pico 2
buzzer = PWM( Pin( Pin.board.GP13 ) )
buzzer.duty_u16( int(65535*PWM_VOL/100) ) # %Vol to duty cycle


def play_tone(freq, msec):
    print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
    if freq > 0:
        buzzer.freq(int(freq))
        buzzer.duty_u16( int(65535*PWM_VOL/100) )
    time.sleep_ms(int(msec * 0.9))
    buzzer.duty_u16(0)
    time.sleep_ms(int(msec * 0.1))

def play(tune):
    try:
        for freq, msec in tune.notes():
            play_tone(freq, msec)
    except KeyboardInterrupt:
        play_tone(0, 0)

def play_song(search):
    play(RTTTL(songs.find(search)))

# play songs from songs.py
play_song('Entertainer')

# play songs directly
play(RTTTL('Monty Python:d=8,o=5,b=180:d#6,d6,4c6,b,4a#,a,4g#,g,f,g,g#,4g,f,2a#,p,a#,g,p,g,g,f#,g,d#6,p,a#,a#,p,g,g#,p,g#,g#,p,a#,2c6,p,g#,f,p,f,f,e,f,d6,p,c6,c6,p,g#,g,p,g,g,p,g#,2a#,p,a#,g,p,g,g,f#,g,g6,p,d#6,d#6,p,a#,a,p,f6,f6,p,f6,2f6,p,d#6,4d6,f6,f6,e6,f6,4c6,f6,f6,e6,f6,a#,p,a,a#,p,a,2a#'))
