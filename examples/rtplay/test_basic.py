# test_basic.py - just run an RTTTL string and 
# one song from songs.py

from machine import Pin
from rtplay import *

buzzer = RingTonePlayer( Pin.board.GP13 ) # Pin used by the Buzzer

# Play a string encoded ringtone 
buzzer.play_str( 'Monty Python:d=8,o=5,b=180:d#6,d6,4c6,b,4a#,a,4g#,g,f,g,g#,4g,f,2a#,p,a#,g,p,g,g,f#,g,d#6,p,a#,a#,p,g,g#,p,g#,g#,p,a#,2c6,p,g#,f,p,f,f,e,f,d6,p,c6,c6,p,g#,g,p,g,g,p,g#,2a#,p,a#,g,p,g,g,f#,g,g6,p,d#6,d#6,p,a#,a,p,f6,f6,p,f6,2f6,p,d#6,4d6,f6,f6,e6,f6,4c6,f6,f6,e6,f6,a#,p,a,a#,p,a,2a#' )

# Play from songs.py 
buzzer.load_songs( 'songs.py' )
buzzer.play_song( 'Looney' )