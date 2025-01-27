# test_songs.py - Dynamic load a songs file, list them and play them

from machine import Pin
from rtplay import *
import time

buzzer = RingTonePlayer( Pin.board.GP13 ) # Pin used by the Buzzer

# Play from songs.py 
buzzer.load_songs( 'songs.py' )
names = buzzer.dir_songs()
print( "Available songs :" )
print( names )
print( "" )
for name in names:
	print( "Playing %s ..." % name )
	buzzer.play_song( name )
	time.sleep( 2 )
	print( "" )