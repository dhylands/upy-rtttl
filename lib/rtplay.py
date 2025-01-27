# rtplay.py - machine.PWM based play basic routine required for playing a RTTTL song 
#
from machine import Pin, PWM 
from rtttl import RTTTL
import time
import sys

PWM_VOL = 50 # 0..100 : reduce this to reduce the volume

class RingTonePlayer:
	def __init__( self, pin_id, pwm_volume=PWM_VOL ):
		""" pin_id : Pin.board.GP13 """
		self.buzzer = PWM( Pin( pin_id ) )
		self.pwm_vol = pwm_volume
		self.buzzer.freq( 440 )
		self.buzzer.duty_u16( 0 ) 
		self.songs = None # reference to the last loaded songs


	def play_tone(self, freq, msec):
		# print('freq = {:6.1f} msec = {:6.1f}'.format(freq, msec))
		if freq > 0:
			self.buzzer.freq(int(freq))
			self.buzzer.duty_u16( int(65535*self.pwm_vol/100) )
		time.sleep_ms(int(msec * 0.9))
		self.buzzer.duty_u16(0)
		time.sleep_ms(int(msec * 0.1))

	def play(self, tune):
		# tune is a RTTTL parser
		try:
			for freq, msec in tune.notes():
				self.play_tone(freq, msec)
		except KeyboardInterrupt:
			self.play_tone(0, 0)

	def play_str( self, ringtone_str ):
		self.play( RTTTL(ringtone_str))

	# --- Songs related function ---
	def load_songs( self, module='songs.py' ):
		# Dynamic load the module.py and retreives the SONGS constant
		module = module.replace('.py','')
		if not( module in sys.modules ):
			__import__( module )
		_mod = sys.modules[module]
		# Get the SONGS constant
		self.songs = getattr( _mod, 'SONGS' )

	def find_song( self, name ):
		assert self.songs, "load_songs() first!"
		for song in self.songs:
			song_name = song.split(':')[0]
			if song_name == name:
				return song
		return None

	def play_song(self, search ):
		assert self.songs, "load_songs() first!"
		_s = self.find_song( search )
		if _s == None:
			raise ValueError('No song "%s" !' % (search))
		self.play(RTTTL(_s))

	def dir_songs(self):
		assert self.songs, "load_songs() first!"
		_r = []
		for song in self.songs:
			_r.append( song.split(':')[0] )			
		return _r
