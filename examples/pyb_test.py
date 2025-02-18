#
# This particular test was coded for the GHI Electronics G30 Development
# Board: https://www.ghielectronics.com/catalog/product/555
#
import pyb
from rtttl import RTTTL
import songs

# G30DEV
buz_tim = pyb.Timer(3, freq=440)
buz_ch = buz_tim.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.BUZZER, pulse_width=0)

# Y2 on pyboard
# buz_tim = pyb.Timer(8, freq=440)
# buz_ch = buz_tim.channel(2, pyb.Timer.PWM, pin=pyb.Pin('Y2'), pulse_width=0)

pwm = 50 # reduce this to reduce the volume

def play_tone(freq, msec):
    print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
    if freq > 0:
        buz_tim.freq(freq)
        buz_ch.pulse_width_percent(pwm)
    pyb.delay(int(msec * 0.9))
    buz_ch.pulse_width_percent(0)
    pyb.delay(int(msec * 0.1))

def play(tune):
    try:
        for freq, msec in tune.notes():
            play_tone(freq, msec)
    except KeyboardInterrupt:
        play_tone(0, 0)


def find(name):
    for song in songs.SONGS:
        song_name = song.split(':')[0]
        if song_name == name:
            return song

def play_song(search):
    play(RTTTL( find(search)) )


# play songs from songs.py
play_song('Entertainer')

# play songs directly
play(RTTTL('Monty Python:d=8,o=5,b=180:d#6,d6,4c6,b,4a#,a,4g#,g,f,g,g#,4g,f,2a#,p,a#,g,p,g,g,f#,g,d#6,p,a#,a#,p,g,g#,p,g#,g#,p,a#,2c6,p,g#,f,p,f,f,e,f,d6,p,c6,c6,p,g#,g,p,g,g,p,g#,2a#,p,a#,g,p,g,g,f#,g,g6,p,d#6,d#6,p,a#,a,p,f6,f6,p,f6,2f6,p,d#6,4d6,f6,f6,e6,f6,4c6,f6,f6,e6,f6,a#,p,a,a#,p,a,2a#'))
