#!/usr/bin/env python3

from rtttl import RTTTL
import songs

def tone(freq, msec):
    print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))

tune = RTTTL(songs.find('Entertainer'))
for freq, msec in tune.notes():
    tone(freq, msec)

