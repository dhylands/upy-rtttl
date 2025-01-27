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

# Using RTTTL on the pyboard

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
for freq, msec in tune.notes():
    play_tone(freq, msec)
```

When using a piezo you basically provide a 50% PWM signal to the piezo using the frequency of the note. Some piezo speakers can vary the volume by using a different duty cycle. The piezo on the G30DEV board Dave Hylands this on, it didn't seem to make any difference.

In order to distinguish consecutive notes, you need a small gap between the notes.
Dave Hylands chose to use 90% of the duration to play the tone, and 10% of duration to play silence.

Dave Hylands used the following play_tone routine on the G30DEV board:
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

Dave Hylands put a recording of the above on YouTube: https://youtu.be/TadV2AEvfww

The G30DEV board definition files for MicroPython can be found here: https://github.com/dhylands/G30DEV

When using pin Y2 on a pyboard v1.0, change the timer/pin to:
```python
buz_tim = pyb.Timer(8, freq=440)
buz_ch = buz_tim.channel(2, pyb.Timer.PWM, pin=pyb.Pin('Y2'), pulse_width=0)
```

To see which timers are available on which pins, consult the MicroPython quickref:
http://docs.micropython.org/en/latest/pyboard/pyboard/quickref.html

# Using RTTTL on the Raspberry-Pi Pico
Revision of the `play_tone()` function to make it working on Raspberry-Pi Pico (tested with MicroPython v1.24.0). 

The Piezo buzzer is wired on the GP13 of the Pico (see [Pico-2-Explorer](https://shop.mchobby.be/product.php?id_product=2718) board for details)

```
from machine import Pin, PWM 
from rtttl import RTTTL
import songs
import time

PWM_VOL = 50 # 0..100 : reduce this to reduce the volume

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

```

# Using RTTTL with CircuitPython

David Glaude used the following play_tone routine on Circuit Python M0 board:
```
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
```

Files:

* circuit_test.py: Playing RTTTL on M0 Circuit Python board.
* pc_test.py: Printing RTTTL decoding on any platform (no sound produced).
* pyb_test.py: Playing RTTTL on G30DEV board.
* pico_test.py : Playing RTTTL on Raspberry-Pi Pico & Pico 2 boards.
* rtttl.py: RTTTL decoding library.
* songs.py: Optionnal collection of RTTTL songs to test the library.
