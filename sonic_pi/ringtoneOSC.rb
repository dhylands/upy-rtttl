#ringtoneOSC.rb
#by Robin Newman, November 2018
#utilises the python script spOSC2.py to extract and broadcast data
#for the rtttl file(s) to be played
use_osc "localhost",8000 #OSC server running on localhost in the python script

#The two lines  osc "/abort" and stop can be uncommented once the program is running, and then
#subsequent runs will stop the currently playing tune and select another one.
#If the program is stopped completely, you must comment the lines again
#for the first run to get the live_loops running again.

osc "/abort"
stop

live_loop :playring do #this live_loop receives and plays broadcast daat from the OSC server
  use_real_time
  use_synth :chiplead
  b= sync "/osc*/ringdata"
  play hz_to_midi(b[0])-12,release: b[1]/1000.0 if b[0] > 0
end

#the following live loop chooses an rttl song to play and sends the name
#to the python script via an OSC message
#it waits for the tune to finish playing when it receives an OSC cue /osc/finished
  #before choosing the next tune
  live_loop :playSong do
    #the list of songs refers to those songs whose data in in the songs.py file
    song_list=[ "Super Mario - Main Theme","Super Mario - Title Music","SMBtheme",
                "SMBwater","SMBunderground","Picaxe","The Simpsons","Indiana","TakeOnMe",
                "Entertainer","Muppets","Xfiles","Looney","20thCenFox","Bond","MASH",
                "StarWars","GoodBad","TopGun","A-Team","Flinstones","Jeopardy",
                "Gadget","Smurfs","MahnaMahna","LeisureSuit","MissionImp"]
    name=song_list.choose
    osc "/name",name
    sync "/osc*/finished"
  end
  