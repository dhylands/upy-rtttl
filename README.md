Ring Tone Text Transfer Language Parser
=======================================

This library can parse RTTTL text lines and delivers the frequency and duration
for each note.

A typical RTTTL string looks like this:
```
Entertainer:d=4,o=5,b=140:8d,8d#,8e,c6,8e,c6,8e,2c.6,8c6,8d6,8d#6,8e6,8c6,8d6,e6,8b,d6,2c6,p,8d,8d#,8e,c6,8e,c6,8e,2c.6,8p,8a,8g,8f#,8a,8c6,e6,8d6,8c6,8a,2d6
```

You can find many more sample ring tones here: http://www.picaxe.com/RTTTL-Ringtones-for-Tune-Command/

You can find a description of RTTTL here: https://en.wikipedia.org/wiki/Ring_Tone_Transfer_Language

# Using RTTTL on the pyboad

Instantiate an instance of the RTTTL class, passing in the tune string to the
constructor.
```python
tune = RTTTL('Entertainer:d=4,o=5,b=140:8d,8d#,8e,c6,8e,c6,8e,2c.6,8c6,8d6,8d#6,8e6,8c6,8d6,e6,8b,d6,2c6,p,8d,8d#,8e,c6,8e,c6,8e,2c.6,8p,8a,8g,8f#,8a,8c6,e6,8d6,8c6,8a,2d6')
```

Then use the notes generator to enumerate the notes in the tune. The notes
generator will return a tuple, where the first entry in the tuple contains
the frequency of the note (in Hz) and the second entry in the tuple contains
the duration of the note.
```python
for freq, msec in tune.notes()
    play_tone(freq, msec)
```

When using a piezo you basically provide a 50% PWM signal to the piezo using the
frequency of the note. Some piezo speakers can vary the volume by using a
different duty cycle. The piezo on the G30DEV board I tested this on, it didn't
seem to make any difference.

In order to distinguish consequtive notes, you need a small gap between the notes.
I chose to use 90% of the duration to play the tone, and 10% of duration to play
silence.

I used the following play_tone routine on the G30DEV board:
```python
import pyb
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
```

I put a recording of the above on YouTube: https://youtu.be/TadV2AEvfww

The G30DEV board definition files for MicroPython can be found here: https://github.com/dhylands/G30DEV

