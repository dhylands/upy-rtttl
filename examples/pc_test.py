#!/usr/bin/env python3

from rtttl import RTTTL
import songs

def tone(freq, msec):
    print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))

def find(name):
    for song in songs.SONGS:
        song_name = song.split(':')[0]
        if song_name == name:
            return song


tune = RTTTL( find('Entertainer'))
for freq, msec in tune.notes():
    tone(freq, msec)

